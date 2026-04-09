"""Formulaire de commande MASA -- panier multi-produits."""

import math
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

import pandas as pd
import streamlit as st

from app.config import (
    DRONE_CAPACITY_KG,
    MAX_RADIUS_KM,
    PRODUCTS,
    URGENCY_LEVELS,
)
from dispatch import find_nearest_hub, estimate_delivery
from scoring import flight_time_min


def _remove_from_cart(index: int) -> None:
    """Retire un article du panier par son index."""
    if 0 <= index < len(st.session_state.cart):
        st.session_state.cart.pop(index)


def _hub_type_label(hub_type: str) -> str:
    labels = {
        "Hauts_Flux": "Hauts Flux (5 drones)",
        "Standard": "Standard (3 drones)",
        "Proximite": "Proximite (2 drones)",
    }
    return labels.get(hub_type, hub_type)


def _max_urgency(items: list[dict]) -> str:
    """Determine l'urgence la plus elevee parmi les articles du panier."""
    priority_order = ["critique", "haute", "standard"]
    best = "standard"
    for item in items:
        u = item["urgence"]
        if priority_order.index(u) < priority_order.index(best):
            best = u
    return best


def render_order_form(facility: dict, hubs: pd.DataFrame) -> None:
    """Formulaire de commande avec panier pour la facility connectee."""

    if "cart" not in st.session_state:
        st.session_state.cart = []
    if "orders" not in st.session_state:
        st.session_state.orders = []

    st.subheader("Nouvelle commande")

    hub_info = find_nearest_hub(facility["lat"], facility["lon"], hubs)

    if hub_info is None:
        st.error(
            f"Aucun hub dans le rayon de {MAX_RADIUS_KM:.0f} km. "
            "Cette facility ne peut pas etre desservie."
        )
        return

    eta_min = flight_time_min(hub_info["distance_km"])
    col1, col2 = st.columns(2)
    col1.metric("Hub", f"#{hub_info['hub_id']}")
    col2.metric("Type", _hub_type_label(hub_info["type"]))
    col3, col4 = st.columns(2)
    col3.metric("Distance", f"{hub_info['distance_km']:.1f} km")
    col4.metric("ETA", f"{eta_min:.0f} min")

    st.divider()

    # --- Ajouter au panier ---
    st.markdown("**Ajouter au panier**")

    product_keys = list(PRODUCTS.keys())

    with st.form("add_to_cart", clear_on_submit=True):
        idx = st.selectbox(
            "Produit",
            range(len(product_keys)),
            format_func=lambda i: PRODUCTS[product_keys[i]]["label"],
        )
        selected_key = product_keys[idx]

        quantity = st.number_input(
            "Quantite",
            min_value=1,
            max_value=20,
            value=1,
            step=1,
        )

        default_urgence = PRODUCTS[selected_key]["urgence_defaut"]
        urgence_keys = list(URGENCY_LEVELS.keys())
        default_idx = urgence_keys.index(default_urgence)

        urgence_idx = st.selectbox(
            "Urgence",
            range(len(urgence_keys)),
            index=default_idx,
            format_func=lambda i: URGENCY_LEVELS[urgence_keys[i]]["label"],
        )
        urgence = urgence_keys[urgence_idx]

        add_submitted = st.form_submit_button("Ajouter au panier")

    if add_submitted:
        poids_unit = PRODUCTS[selected_key]["poids_kg"]
        poids_total = quantity * poids_unit
        poids_panier = sum(
            it["poids_total"]
            for it in st.session_state.cart
        )
        if poids_panier + poids_total > DRONE_CAPACITY_KG:
            st.warning(
                f"Poids maximum de "
                f"{DRONE_CAPACITY_KG:.0f} kg atteint "
                f"pour cette livraison."
            )
        else:
            st.session_state.cart.append({
                "product_key": selected_key,
                "label": PRODUCTS[selected_key]["label"],
                "quantity": quantity,
                "poids_unit": poids_unit,
                "poids_total": poids_total,
                "urgence": urgence,
            })
            st.success(
                f"{PRODUCTS[selected_key]['label']} "
                f"x{quantity} "
                f"({poids_total:.1f} kg) ajoute."
            )

    # --- Panier en cours ---
    if not st.session_state.cart:
        return

    st.divider()
    st.markdown("**Panier en cours**")

    for i, item in enumerate(st.session_state.cart):
        col_info, col_detail, col_btn = st.columns([3, 4, 1])
        col_info.write(item["label"])
        col_detail.write(
            f"x{item['quantity']} · {item['poids_total']:.1f} kg · "
            f"{URGENCY_LEVELS[item['urgence']]['label']}"
        )
        col_btn.button(
            "Retirer",
            key=f"remove_{i}",
            on_click=_remove_from_cart,
            args=(i,),
        )

    poids_total_panier = sum(
        item["poids_total"]
        for item in st.session_state.cart
    )
    n_drones = math.ceil(poids_total_panier / DRONE_CAPACITY_KG)

    st.markdown(f"**Poids total : {poids_total_panier:.1f} kg**")

    ratio = poids_total_panier / DRONE_CAPACITY_KG
    if ratio > 0.8:
        st.info(
            f"Capacite utilisee : "
            f"{ratio * 100:.0f}% "
            f"({DRONE_CAPACITY_KG:.0f} kg max)"
        )

    if st.button("Valider la commande", type="primary"):
        urgence_max = _max_urgency(st.session_state.cart)
        first_product = st.session_state.cart[0]["product_key"]

        delivery = estimate_delivery(
            hub_info,
            facility["lat"],
            facility["lon"],
            first_product,
            1,
        )

        order_id = len(st.session_state.orders) + 1
        order = {
            "id": order_id,
            "timestamp": datetime.now(
                tz=timezone.utc,
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "items": list(st.session_state.cart),
            "n_drones": n_drones,
            "poids_total_kg": round(poids_total_panier, 2),
            "urgence": urgence_max,
            "temps_vol_min": delivery["temps_vol_min"],
            "distance_km": delivery["distance_km"],
            "hub_id": delivery["hub_id"],
            "hub_lat": hub_info["hub_lat"],
            "hub_lon": hub_info["hub_lon"],
            "facility_lat": facility["lat"],
            "facility_lon": facility["lon"],
            "facility_name": facility["name"],
            "statut": "preparation",
        }

        st.session_state.orders.append(order)
        st.session_state.cart = []

        login_id = facility.get("login", "")
        if login_id:
            if "order_history" not in st.session_state:
                st.session_state.order_history = {}
            st.session_state.order_history[login_id] = list(
                st.session_state.orders
            )

        st.session_state._goto_page = "Suivi"
        st.rerun()
