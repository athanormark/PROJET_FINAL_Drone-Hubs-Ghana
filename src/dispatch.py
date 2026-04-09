"""Dispatch : selection du hub optimal et estimation de livraison."""

import pandas as pd

from haversine import haversine_km
from scoring import flight_time_min, urgency_score, PRODUCTS_URGENCY

# Rayon max par operateur
_RADIUS: dict[str, float] = {
    "MASA": 30.0,
    "Zipline": 80.0,
}
MAX_RADIUS_KM: float = 80.0


def find_nearest_hub(
    fac_lat: float,
    fac_lon: float,
    hubs_df: pd.DataFrame,
) -> dict | None:
    """Identifie le hub le plus proche d'une facility.

    Le rayon depend de l'operateur :
    - MASA : 30 km (micro-hubs VTOL)
    - Zipline : 80 km (aile fixe)

    Retourne None si aucun hub n'est a portee.
    """
    best: dict | None = None
    best_dist = float("inf")

    for _, row in hubs_df.iterrows():
        h_lat = float(row["Latitude"])
        h_lon = float(row["Longitude"])
        operateur = str(row.get("Operateur", "MASA"))
        rayon = _RADIUS.get(operateur, MAX_RADIUS_KM)

        d = haversine_km(fac_lat, fac_lon, h_lat, h_lon)
        if d <= rayon and d < best_dist:
            best_dist = d
            best = {
                "hub_id": int(row["Hub_ID"]),
                "hub_lat": h_lat,
                "hub_lon": h_lon,
                "distance_km": round(d, 2),
                "type": str(row["Type"]),
                "n_drones": int(row["N_drones"]),
                "operateur": operateur,
            }

    return best


def can_dispatch(hub_info: dict | None) -> bool:
    """Verifie si une commande peut etre dispatchee.

    Seuls les hubs MASA gerent les commandes.
    Zipline est un operateur tiers, pas via MASA.
    """
    if hub_info is None:
        return False
    return hub_info.get("operateur", "MASA") == "MASA"


def estimate_delivery(
    hub_info: dict,
    fac_lat: float,
    fac_lon: float,
    product_key: str,
    quantity: int = 1,
) -> dict:
    """Estimation complete d'une livraison drone."""
    distance = haversine_km(
        hub_info["hub_lat"],
        hub_info["hub_lon"],
        fac_lat,
        fac_lon,
    )
    temps = flight_time_min(distance)
    urgence = PRODUCTS_URGENCY.get(product_key, "standard")
    operateur = hub_info.get("operateur", "MASA")
    rayon = _RADIUS.get(operateur, MAX_RADIUS_KM)

    if distance > rayon:
        statut = "hors_portee"
    else:
        statut = "realisable"

    score = urgency_score(product_key, distance, 1000.0)

    return {
        "temps_vol_min": round(temps, 1),
        "distance_km": round(distance, 2),
        "hub_id": hub_info["hub_id"],
        "statut": statut,
        "urgence": urgence,
        "score": round(score, 2),
        "operateur": operateur,
    }


def check_coverage(
    fac_lat: float,
    fac_lon: float,
    hubs_df: pd.DataFrame,
) -> dict:
    """Verifie si une facility est couverte par le reseau."""
    nearest = find_nearest_hub(fac_lat, fac_lon, hubs_df)

    if nearest is None:
        best_dist = float("inf")
        for _, row in hubs_df.iterrows():
            d = haversine_km(
                fac_lat, fac_lon,
                float(row["Latitude"]),
                float(row["Longitude"]),
            )
            if d < best_dist:
                best_dist = d

        return {
            "covered": False,
            "nearest_hub": None,
            "distance_km": round(best_dist, 2),
        }

    return {
        "covered": True,
        "nearest_hub": nearest,
        "distance_km": nearest["distance_km"],
    }
