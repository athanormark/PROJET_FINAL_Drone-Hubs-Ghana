"""
Placement optimal de hubs de drones médicaux par K-Means.
Supply chain : Aéroport (cargo) → Route → Hub (relais) → Drone → Facility rurale.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score

from haversine import haversine_matrix as _haversine_matrix

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_PROCESSED = REPO_ROOT / "data" / "processed"

MAX_RADIUS_KM = 80.0

URBAN_TYPES = {
    "city", "suburb", "neighbourhood", "quarter", "city_block",
}

# Villes ghanéennes disposant d'un aéroport capable de recevoir du fret médical.
# Tier 1 : international, cargo régulier.
# Tier 2 : domestique, cargo moyen.
# Tier 3 : domestique, cargo léger uniquement.
AIRPORT_CITIES = {
    "Accra": 1,
    "Kumasi": 2,
    "Tamale": 2,
    "Sekondi-Takoradi": 3,
    "Sunyani": 3,
    "Wa": 3,
    "Bolgatanga": 3,
}

TIER_FACILITY_LIMITS = {"Micro": 150, "Standard": 400}
TIER_DRONES = {
    "Micro": (4, 8),
    "Standard": (10, 20),
    "Large": (25, 50),
}

CAPEX_USD = {"Micro": 700_000, "Standard": 2_000_000, "Large": 5_000_000}
OPEX_ANNUEL_USD = {"Micro": 150_000, "Standard": 350_000, "Large": 800_000}


# --- Filtrage rural / urbain ---

def filter_rural(villages: pd.DataFrame) -> pd.DataFrame:
    """Exclut les zones urbaines des cibles de couverture drone."""
    return villages[~villages["Place_Type"].isin(URBAN_TYPES)].copy()


def extract_rural_facilities(villages: pd.DataFrame) -> pd.DataFrame:
    """Facilities uniques référencées par au moins un village rural."""
    rural = filter_rural(villages)
    fac = (
        rural.groupby(
            ["Nearest_Facility_Name", "Nearest_Facility_Latitude",
             "Nearest_Facility_Longitude"],
        )
        .agg(N_villages=("Village", "count"), Population_rurale=("Population", "sum"))
        .reset_index()
        .rename(columns={
            "Nearest_Facility_Name": "Facility_Name",
            "Nearest_Facility_Latitude": "Latitude",
            "Nearest_Facility_Longitude": "Longitude",
        })
    )
    return fac


# --- Recherche du K optimal ---

def evaluate_k_range(
    coords: np.ndarray,
    k_min: int = 6,
    k_max: int = 15,
    villages_rural: pd.DataFrame | None = None,
    random_state: int = 42,
) -> pd.DataFrame:
    results = []

    for k in range(k_min, k_max + 1):
        km = KMeans(n_clusters=k, n_init=10, random_state=random_state)
        labels = km.fit_predict(coords)
        centroids = km.cluster_centers_

        inertia = km.inertia_
        sil = silhouette_score(coords, labels)
        db = davies_bouldin_score(coords, labels)

        couv_v, couv_p = None, None
        if villages_rural is not None:
            couv_v, couv_p = _coverage_pct(centroids, villages_rural)

        results.append({
            "K": k,
            "Inertie": round(inertia, 2),
            "Silhouette": round(sil, 4),
            "Davies_Bouldin": round(db, 4),
            "Couverture_villages_pct": couv_v,
            "Couverture_pop_pct": couv_p,
        })

        line = f"  K={k:2d}  Inertie={inertia:10.1f}  Sil={sil:.4f}  DB={db:.4f}"
        if couv_v is not None:
            line += f"  Couv_v={couv_v:.1f}%  Couv_p={couv_p:.1f}%"
        print(line)

    return pd.DataFrame(results)


def _coverage_pct(
    centroids: np.ndarray,
    villages: pd.DataFrame,
    max_km: float = MAX_RADIUS_KM,
) -> tuple[float, float]:
    v_lats = villages["Latitude"].values[:, np.newaxis]
    v_lons = villages["Longitude"].values[:, np.newaxis]
    c_lats = centroids[:, 0][np.newaxis, :]
    c_lons = centroids[:, 1][np.newaxis, :]

    dist = _haversine_matrix(v_lats, v_lons, c_lats, c_lons)
    covered = dist.min(axis=1) <= max_km

    pop = villages["Population"].values
    pct_v = 100 * covered.sum() / len(villages)
    pct_p = 100 * pop[covered].sum() / pop.sum()
    return round(pct_v, 2), round(pct_p, 2)


# --- Modèle final ---

def fit_hubs(
    coords: np.ndarray,
    k: int,
    random_state: int = 42,
) -> tuple[KMeans, np.ndarray]:
    km = KMeans(n_clusters=k, n_init=10, random_state=random_state)
    km.fit(coords)
    return km, km.cluster_centers_


# --- Assignation villages → hubs ---

def assign_villages(
    hubs: np.ndarray,
    villages: pd.DataFrame,
    max_radius_km: float = MAX_RADIUS_KM,
) -> pd.DataFrame:
    v_lats = villages["Latitude"].values[:, np.newaxis]
    v_lons = villages["Longitude"].values[:, np.newaxis]
    h_lats = hubs[:, 0][np.newaxis, :]
    h_lons = hubs[:, 1][np.newaxis, :]

    dist = _haversine_matrix(v_lats, v_lons, h_lats, h_lons)

    df = villages.copy()
    df["Hub_ID"] = dist.argmin(axis=1)
    df["Hub_Latitude"] = hubs[df["Hub_ID"].values, 0]
    df["Hub_Longitude"] = hubs[df["Hub_ID"].values, 1]
    df["Distance_Hub_km"] = np.round(dist.min(axis=1), 2)
    df["Covered"] = df["Distance_Hub_km"] <= max_radius_km
    return df


# --- Dimensionnement et budget ---

def _assign_tier(n_facilities: int) -> str:
    for tier, limit in TIER_FACILITY_LIMITS.items():
        if n_facilities <= limit:
            return tier
    return "Large"


def _calc_drones(n_facilities: int, tier: str) -> int:
    d_min, d_max = TIER_DRONES[tier]
    raw = max(d_min, int(np.ceil(n_facilities / 20)))
    return min(raw, d_max)


def hub_summary(
    assigned: pd.DataFrame,
    hubs: np.ndarray,
) -> pd.DataFrame:
    rows = []
    for hid in range(len(hubs)):
        sub = assigned[assigned["Hub_ID"] == hid]
        pop_total = int(sub["Population"].sum())

        rural_mask = ~sub["Place_Type"].isin(URBAN_TYPES)
        pop_rural = int(sub.loc[rural_mask, "Population"].sum())
        n_rural = int(rural_mask.sum())

        n_fac = sub.loc[rural_mask, "Nearest_Facility_Name"].nunique()
        tier = _assign_tier(n_fac)
        n_drones = _calc_drones(n_fac, tier)

        rows.append({
            "Hub_ID": hid,
            "Latitude": round(hubs[hid, 0], 6),
            "Longitude": round(hubs[hid, 1], 6),
            "Type": tier,
            "N_villages": len(sub),
            "N_rural": n_rural,
            "N_facilities_drone": n_fac,
            "Pop_totale": pop_total,
            "Pop_rurale": pop_rural,
            "Dist_max_km": round(sub["Distance_Hub_km"].max(), 2),
            "Dist_moy_km": round(sub["Distance_Hub_km"].mean(), 2),
            "N_non_couverts": int((~sub["Covered"]).sum()),
            "N_drones": n_drones,
            "CAPEX_USD": CAPEX_USD[tier],
            "OPEX_annuel_USD": OPEX_ANNUEL_USD[tier],
        })
    return pd.DataFrame(rows)


def network_budget(summary: pd.DataFrame) -> dict:
    capex = int(summary["CAPEX_USD"].sum())
    opex = int(summary["OPEX_annuel_USD"].sum())
    return {
        "N_hubs": len(summary),
        "Repartition": summary["Type"].value_counts().to_dict(),
        "N_drones_total": int(summary["N_drones"].sum()),
        "CAPEX_total_USD": capex,
        "OPEX_annuel_USD": opex,
        "TCO_5ans_USD": capex + 5 * opex,
    }


# --- Validation supply chain (aéroports) ---

def _get_airport_cities(villages: pd.DataFrame) -> pd.DataFrame:
    """Filtre les villes disposant d'un aéroport pour le fret médical."""
    cities = villages[villages["Place_Type"] == "city"].copy()
    mask = cities["Village"].isin(AIRPORT_CITIES.keys())
    airport = cities[mask].copy()
    airport["Airport_Tier"] = airport["Village"].map(AIRPORT_CITIES)
    return airport


def supply_distances(
    hubs: np.ndarray,
    villages: pd.DataFrame,
) -> pd.DataFrame:
    """Distance Haversine de chaque hub à l'aéroport le plus proche."""
    airports = _get_airport_cities(villages)
    if airports.empty:
        return pd.DataFrame()

    h_lats = hubs[:, 0][:, np.newaxis]
    h_lons = hubs[:, 1][:, np.newaxis]
    a_lats = airports["Latitude"].values[np.newaxis, :]
    a_lons = airports["Longitude"].values[np.newaxis, :]

    dist = _haversine_matrix(h_lats, h_lons, a_lats, a_lons)
    nearest_idx = dist.argmin(axis=1)
    nearest_dist = dist.min(axis=1)

    rows = []
    for hid in range(len(hubs)):
        aidx = nearest_idx[hid]
        rows.append({
            "Hub_ID": hid,
            "Aeroport": airports.iloc[aidx]["Village"],
            "Airport_Tier": int(airports.iloc[aidx]["Airport_Tier"]),
            "Distance_aeroport_km": round(nearest_dist[hid], 2),
        })
    return pd.DataFrame(rows)


# --- Simulation multi-scénarios ---

def compare_scenarios(
    coords: np.ndarray,
    villages: pd.DataFrame,
    k_values: list[int] | None = None,
    random_state: int = 42,
) -> pd.DataFrame:
    """Compare plusieurs valeurs de K sur couverture, budget et supply chain."""
    if k_values is None:
        k_values = [8, 9, 10, 11, 12]

    rural = filter_rural(villages)
    rows = []

    for k in k_values:
        _, hubs = fit_hubs(coords, k=k, random_state=random_state)
        assigned = assign_villages(hubs, villages)
        summary = hub_summary(assigned, hubs)
        budget = network_budget(summary)
        supply = supply_distances(hubs, villages)

        rural_assigned = assigned[~assigned["Place_Type"].isin(URBAN_TYPES)]
        n_cov = int(rural_assigned["Covered"].sum())
        pop_cov = rural_assigned.loc[rural_assigned["Covered"], "Population"].sum()
        pop_rur = rural_assigned["Population"].sum()

        rows.append({
            "K": k,
            "Couv_villages_pct": round(100 * n_cov / len(rural_assigned), 1),
            "Couv_pop_pct": round(100 * pop_cov / pop_rur, 1),
            "N_non_couverts": len(rural_assigned) - n_cov,
            "Micro": int((summary["Type"] == "Micro").sum()),
            "Standard": int((summary["Type"] == "Standard").sum()),
            "Large": int((summary["Type"] == "Large").sum()),
            "N_drones": budget["N_drones_total"],
            "CAPEX_M_USD": round(budget["CAPEX_total_USD"] / 1e6, 1),
            "OPEX_M_USD_an": round(budget["OPEX_annuel_USD"] / 1e6, 1),
            "Dist_aeroport_max_km": round(supply["Distance_aeroport_km"].max(), 1),
            "Dist_aeroport_moy_km": round(supply["Distance_aeroport_km"].mean(), 1),
        })

    return pd.DataFrame(rows)


# --- Impact drone sur villages isolés ---

def compare_baseline(assigned: pd.DataFrame) -> pd.DataFrame:
    """Villages isolés par la route : combien sont couverts par drone ?"""
    dist_fac = assigned["Distance_Nearest_Facility_km"]
    covered_drone = assigned["Covered"]
    pop = assigned["Population"]

    rows = []
    for seuil in [10, 20, 30, 50]:
        isoles = dist_fac > seuil
        n_isoles = int(isoles.sum())
        pop_isoles = int(pop[isoles].sum())

        rescues = int((isoles & covered_drone).sum())
        pop_rescues = int(pop[isoles & covered_drone].sum())

        rows.append({
            "Seuil_route_km": seuil,
            "Villages_isoles": n_isoles,
            "Pop_isolee": pop_isoles,
            "Couverts_drone": rescues,
            "Pop_couverte_drone": pop_rescues,
            "Taux_rescue_pct": round(
                100 * rescues / n_isoles, 1,
            ) if n_isoles else 0.0,
        })
    return pd.DataFrame(rows)


# --- Optimisation de couverture ---

def fit_hubs_weighted(
    coords: np.ndarray,
    weights: np.ndarray,
    k: int,
    random_state: int = 42,
) -> tuple[KMeans, np.ndarray]:
    """K-Means avec ponderation par demande rurale."""
    km = KMeans(n_clusters=k, n_init=10, random_state=random_state)
    km.fit(coords, sample_weight=weights)
    return km, km.cluster_centers_


def find_satellites(
    uncovered: pd.DataFrame,
    n_max: int = 5,
    random_state: int = 42,
) -> pd.DataFrame:
    """Evalue 1 a n_max satellites Micro sur les villages non couverts."""
    coords = uncovered[["Latitude", "Longitude"]].values
    pop = uncovered["Population"].values
    v_lats = coords[:, 0][:, np.newaxis]
    v_lons = coords[:, 1][:, np.newaxis]

    rows = []
    for n_sat in range(1, n_max + 1):
        km = KMeans(n_clusters=n_sat, n_init=10, random_state=random_state)
        km.fit(coords)
        centroids = km.cluster_centers_

        s_lats = centroids[:, 0][np.newaxis, :]
        s_lons = centroids[:, 1][np.newaxis, :]
        dist = _haversine_matrix(v_lats, v_lons, s_lats, s_lons)
        rescued = dist.min(axis=1) <= MAX_RADIUS_KM

        rows.append({
            "N_satellites": n_sat,
            "Rescued": int(rescued.sum()),
            "Pct_rescued": round(100 * rescued.sum() / len(uncovered), 1),
            "Pop_rescued": int(pop[rescued].sum()),
            "CAPEX_add_USD": n_sat * CAPEX_USD["Micro"],
        })

    return pd.DataFrame(rows)


def place_satellites(
    uncovered: pd.DataFrame,
    n_satellites: int,
    random_state: int = 42,
) -> np.ndarray:
    """Coordonnees optimales des hubs satellites."""
    coords = uncovered[["Latitude", "Longitude"]].values
    km = KMeans(n_clusters=n_satellites, n_init=10, random_state=random_state)
    km.fit(coords)
    return km.cluster_centers_
