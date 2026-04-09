"""Suivi des commandes MASA -- timeline visuelle et carte de vol."""

import folium
import streamlit as st
import streamlit.components.v1 as components

from app.config import ORDER_STEPS, URGENCY_LEVELS


_STATUS_STYLES: dict[str, dict[str, str]] = {
    "preparation": {
        "label": "Preparation",
        "color": "#FFA502",
        "bg": "rgba(255,165,2,0.1)",
        "icon": "\U0001F4E6",
    },
    "en_vol": {
        "label": "En vol",
        "color": "#4FC3F7",
        "bg": "rgba(79,195,247,0.1)",
        "icon": "\U0001F6E9\uFE0F",
    },
    "livree": {
        "label": "Livree",
        "color": "#00D4AA",
        "bg": "rgba(0,212,170,0.1)",
        "icon": "\u2705",
    },
}


def _status_badge(status: str) -> str:
    style = _STATUS_STYLES.get(status, _STATUS_STYLES["preparation"])
    css_class = f"pill-{status.replace('_', '-')}"
    return (
        f'<span class="{css_class}" style="display:inline-block;'
        f"background:{style['bg']};color:{style['color']};"
        f'border-radius:20px;padding:4px 12px;font-weight:600;font-size:0.75rem;">'
        f"{style['icon']} {style['label']}</span>"
    )


def _urgency_badge(urgence: str) -> str:
    info = URGENCY_LEVELS.get(urgence, URGENCY_LEVELS["standard"])
    css_class = f"pill-{urgence}"
    return (
        f'<span class="{css_class}" style="display:inline-block;'
        f"background:rgba({_hex_to_rgb(info['color'])},0.15);"
        f"color:{info['color']};border-radius:20px;padding:4px 12px;"
        f'font-weight:600;font-size:0.75rem;">'
        f"{info['label']}</span>"
    )


def _hex_to_rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    return f"{int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)}"


def _render_timeline(order: dict) -> None:
    """Timeline horizontale a 3 etapes."""
    current_idx = ORDER_STEPS.index(order["statut"])

    html = (
        '<style>'
        '.timeline-row{display:flex;align-items:flex-start;'
        'justify-content:center;padding:8px 0;}'
        '.timeline-step{display:flex;flex-direction:column;'
        'align-items:center;min-width:70px;}'
        '.timeline-circle{width:32px;height:32px;border-radius:50%;'
        'display:flex;align-items:center;justify-content:center;'
        'font-weight:700;font-size:0.8rem;}'
        '.timeline-label{margin-top:4px;font-size:0.7rem;font-weight:600;}'
        '.timeline-line{flex:1;height:3px;margin:0 4px;align-self:center;}'
        '@media(max-width:480px){'
        '.timeline-step{min-width:50px;}'
        '.timeline-circle{width:26px;height:26px;font-size:0.7rem;}'
        '.timeline-label{font-size:0.6rem;}'
        '}'
        '</style>'
        f'<div class="timeline-row">'
    )

    for i, step in enumerate(ORDER_STEPS):
        style_info = _STATUS_STYLES[step]
        label = style_info["label"]

        if i < current_idx:
            bg, border, text_color = "#00D4AA", "#00D4AA", "#fff"
            content = "\u2713"
        elif i == current_idx:
            bg = style_info["color"]
            border = style_info["color"]
            text_color = "#fff"
            content = str(i + 1)
        else:
            bg, border, text_color = "transparent", "#555", "#555"
            content = str(i + 1)

        label_color = "#00D4AA" if i < current_idx else (
            style_info["color"] if i == current_idx else "#555"
        )

        connector = ""
        if i < len(ORDER_STEPS) - 1:
            line_color = "#00D4AA" if i < current_idx else "#555"
            connector = (
                f'<div class="timeline-line" '
                f'style="background:{line_color};"></div>'
            )

        html += (
            f'<div class="timeline-step">'
            f'<div class="timeline-circle" '
            f'style="background:{bg};border:2px solid {border};'
            f'color:{text_color};">{content}</div>'
            f'<div class="timeline-label" '
            f'style="color:{label_color};">{label}</div>'
            f"</div>{connector}"
        )

    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def _render_flight_map(order: dict) -> None:
    """Carte du trajet drone hub -> facility, format carre."""
    hub_lat = order.get("hub_lat")
    hub_lon = order.get("hub_lon")
    fac_lat = order.get("facility_lat")
    fac_lon = order.get("facility_lon")

    if hub_lat is None or fac_lat is None:
        return

    status = order["statut"]
    mid_lat = (hub_lat + fac_lat) / 2
    mid_lon = (hub_lon + fac_lon) / 2

    m = folium.Map(location=[mid_lat, mid_lon], zoom_start=10, tiles="CartoDB positron")

    margin = 0.20
    sw = [min(hub_lat, fac_lat) - margin, min(hub_lon, fac_lon) - margin]
    ne = [max(hub_lat, fac_lat) + margin, max(hub_lon, fac_lon) + margin]
    m.fit_bounds([sw, ne], padding=[25, 25])

    folium.Marker(
        location=[hub_lat, hub_lon],
        popup=f"Hub #{order['hub_id']}",
        icon=folium.Icon(color="green", icon="plus", prefix="fa"),
    ).add_to(m)

    folium.Marker(
        location=[fac_lat, fac_lon],
        popup=order.get("facility_name", "Facility"),
        icon=folium.Icon(color="red", icon="hospital-o", prefix="fa"),
    ).add_to(m)

    if status == "en_vol":
        folium.PolyLine(
            locations=[[hub_lat, hub_lon], [fac_lat, fac_lon]],
            color="#4FC3F7",
            weight=3,
            dash_array="8",
            opacity=0.8,
        ).add_to(m)

        drone_lat = hub_lat + 0.6 * (fac_lat - hub_lat)
        drone_lon = hub_lon + 0.6 * (fac_lon - hub_lon)

        folium.Marker(
            location=[drone_lat, drone_lon],
            icon=folium.DivIcon(
                html=(
                    '<div style="font-size:22px;text-shadow:0 2px 6px rgba(0,0,0,0.4);'
                    'filter:drop-shadow(0 0 4px rgba(79,195,247,0.6));">'
                    '\U0001F6E9\uFE0F</div>'
                ),
                icon_size=(30, 30),
                icon_anchor=(15, 15),
            ),
        ).add_to(m)

        folium.PolyLine(
            locations=[[hub_lat, hub_lon], [drone_lat, drone_lon]],
            color="#00D4AA",
            weight=3,
            opacity=0.9,
        ).add_to(m)

    elif status == "livree":
        folium.PolyLine(
            locations=[[hub_lat, hub_lon], [fac_lat, fac_lon]],
            color="#00D4AA",
            weight=3,
            opacity=0.7,
        ).add_to(m)

    components.html(m._repr_html_(), height=400, scrolling=False)


def _advance_status(order_idx: int) -> None:
    """Fait passer la commande au statut suivant."""
    order = st.session_state.orders[order_idx]
    pos = ORDER_STEPS.index(order["statut"])
    if pos < len(ORDER_STEPS) - 1:
        st.session_state.orders[order_idx]["statut"] = ORDER_STEPS[pos + 1]


def _format_items(order: dict) -> str:
    if "items" in order and isinstance(order["items"], list):
        parts = [
            f"{item['label']} x{item['quantity']}"
            for item in order["items"]
        ]
        return " | ".join(parts)
    return f"{order.get('label', '---')} x{order.get('quantite', 1)}"


def render_tracking(facility: dict) -> None:
    """Tableau de suivi : infos a gauche, carte a droite."""

    orders: list[dict] = st.session_state.get("orders", [])

    if not orders:
        st.info("Aucune commande pour cette session.")
        return

    for idx in range(len(orders) - 1, -1, -1):
        order = orders[idx]
        status = order["statut"]
        show_map = status in ("en_vol", "livree")

        with st.container():
            header = (
                '<div class="order-header">'
                '<div class="order-header-left">'
                f'<span class="order-id">Commande #{order["id"]}</span>'
                f'<span class="order-ts">{order.get("timestamp", "")}</span>'
                '</div>'
                '<div class="order-header-right">'
                f'{_urgency_badge(order["urgence"])}'
                f'{_status_badge(status)}'
                '</div>'
                '</div>'
            )
            st.markdown(header, unsafe_allow_html=True)

            if show_map:
                col_left, col_right = st.columns([1, 1])
            else:
                col_left = st.container()
                col_right = None

            with col_left:
                items_text = _format_items(order)
                st.markdown(f"**Articles** : {items_text}")

                n_drones = order.get("n_drones", 1)
                poids = order.get("poids_total_kg", 0.0)
                distance = order.get("distance_km", 0.0)
                eta = order.get("temps_vol_min", 0.0)

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Drones", n_drones)
                m2.metric("Poids", f"{poids:.1f} kg")
                m3.metric("Distance", f"{distance:.1f} km")
                m4.metric("ETA", f"{eta:.0f} min")

                _render_timeline(order)

                if status != "livree":
                    st.button(
                        "Simuler progression",
                        key=f"progress_{order['id']}",
                        on_click=_advance_status,
                        args=(idx,),
                    )

            if show_map and col_right is not None:
                with col_right:
                    _render_flight_map(order)

        st.divider()

    # --- Resume ---
    st.subheader("Resume")

    n_total = len(orders)
    total_eta = sum(o.get("temps_vol_min", 0.0) for o in orders)
    avg_eta = total_eta / n_total if n_total > 0 else 0.0
    total_drones = sum(o.get("n_drones", 1) for o in orders)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total commandes", n_total)
    col2.metric("Temps moyen", f"{avg_eta:.0f} min")
    col3.metric("Drones mobilises", total_drones)

    by_status: dict[str, int] = {}
    for o in orders:
        s = o["statut"]
        by_status[s] = by_status.get(s, 0) + 1

    badges_html = " &nbsp; ".join(
        f"{_status_badge(step)} <strong>{by_status.get(step, 0)}</strong>"
        for step in ORDER_STEPS
        if by_status.get(step, 0) > 0
    )
    if badges_html:
        st.markdown(
            f"**Ventilation** : {badges_html}",
            unsafe_allow_html=True,
        )
