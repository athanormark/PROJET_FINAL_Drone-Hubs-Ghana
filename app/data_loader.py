"""Chargement et cache des donnees reseau MASA."""

import pandas as pd
import streamlit as st

from app.config import DATA_DIR


@st.cache_data
def load_hubs() -> pd.DataFrame:
    """Charge le plan final des hubs (MASA + Zipline)."""
    path = DATA_DIR / "hubs_plan_final.csv"
    return pd.read_csv(path)


@st.cache_data
def load_villages() -> pd.DataFrame:
    """Charge les villages avec leur affectation hub."""
    path = DATA_DIR / "villages_assigned_final.csv"
    df = pd.read_csv(path)
    df["Covered"] = df["Covered"].astype(bool)
    return df


@st.cache_data
def load_facilities() -> pd.DataFrame:
    """Charge les facilities avec leur affectation hub."""
    path = DATA_DIR / "facilities_assigned.csv"
    df = pd.read_csv(path)
    df["Covered"] = df["Covered"].astype(bool)
    return df


def get_network_stats(
    hubs_df: pd.DataFrame,
    facilities_df: pd.DataFrame,
) -> dict[str, int | float]:
    """Indicateurs cles du reseau deploye.

    Budget = hubs MASA uniquement (Zipline deja opere).
    Couverture = % facilities couvertes (MASA + Zipline).
    """
    masa = hubs_df[hubs_df["Operateur"] == "MASA"]
    n_hubs_masa = len(masa)
    n_drones = int(masa["N_drones"].sum())

    n_total = len(facilities_df)
    n_covered = int(facilities_df["Covered"].sum())
    couverture_pct = (
        round(100.0 * n_covered / n_total, 1)
        if n_total
        else 0.0
    )

    capex_total = int(masa["CAPEX_USD"].sum())
    opex_annuel = int(masa["OPEX_annuel_USD"].sum())

    return {
        "n_hubs": n_hubs_masa,
        "n_drones": n_drones,
        "couverture_pct": couverture_pct,
        "n_facilities_couvertes": n_covered,
        "n_facilities_total": n_total,
        "capex_total": capex_total,
        "opex_annuel": opex_annuel,
    }
