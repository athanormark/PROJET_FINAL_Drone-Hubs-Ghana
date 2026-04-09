"""Cartes Folium du reseau MASA."""

import folium
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from app.config import (
    HUB_COLORS,
    OPERATOR_COLORS,
    RADIUS_MASA,
    RADIUS_ZIPLINE,
)

GHANA_CENTER: list[float] = [7.95, -1.03]
DEFAULT_ZOOM: int = 7

# Bornes Ghana avec marge pour les cercles de couverture
_GHANA_SW: list[float] = [4.5, -3.5]
_GHANA_NE: list[float] = [11.5, 1.5]


def _radius_for_hub(row: pd.Series) -> float:
    """Rayon en km selon l'operateur du hub."""
    op = str(row.get("Operateur", "MASA"))
    if op == "Zipline":
        return RADIUS_ZIPLINE
    return RADIUS_MASA


def _hub_popup(row: pd.Series) -> str:
    """Popup HTML pour un hub sur la carte reseau."""
    operateur = str(row.get("Operateur", "MASA"))
    color = OPERATOR_COLORS.get(operateur, "#95a5a6")
    rayon = _radius_for_hub(row)

    label_op = f"Opere par {operateur}"
    n_drones = int(row["N_drones"])
    drones_txt = (
        f'{n_drones}' if n_drones > 0
        else '<span style="color:#8899AA;">N/A</span>'
    )

    return (
        '<div style="background:#FFFFFF;color:#1A2A3A;'
        'padding:12px 14px;border-radius:8px;'
        'border:1px solid #E0E4E8;'
        'font-family:Inter,sans-serif;font-size:13px;'
        'min-width:180px;'
        'box-shadow:0 4px 12px rgba(0,0,0,0.1);">'
        f'<div style="font-weight:700;font-size:14px;'
        f'margin-bottom:6px;color:{color};">'
        f'Hub {int(row["Hub_ID"])}'
        f' <span style="color:#6B7D8E;font-weight:400;'
        f'font-size:12px;">({row["Type"]})</span></div>'
        f'<div style="color:#6B7D8E;line-height:1.8;">'
        f'{label_op}<br>'
        f'Rayon <span style="color:#1A2A3A;'
        f'font-weight:500;">{rayon:.0f} km</span><br>'
        f'Drones <span style="color:#1A2A3A;'
        f'font-weight:500;">{drones_txt}</span><br>'
        f'Facilities <span style="color:#1A2A3A;'
        f'font-weight:500;">'
        f'{int(row["N_facilities"])}</span>'
        '</div></div>'
    )


def _legend_html() -> str:
    """Legende en bas a droite de la carte."""
    return (
        '<div style="position:fixed;bottom:24px;right:24px;'
        'z-index:1000;'
        "background:rgba(255,255,255,0.95);"
        "backdrop-filter:blur(8px);"
        "padding:14px 18px;border-radius:12px;"
        "border:1px solid #E0E4E8;"
        'font-size:12px;color:#1A2A3A;'
        'font-family:Inter,sans-serif;'
        'box-shadow:0 4px 16px rgba(0,0,0,0.08);">'
        '<div style="font-weight:600;font-size:11px;'
        'color:#6B7D8E;letter-spacing:1px;'
        'text-transform:uppercase;margin-bottom:8px;">'
        'Legende</div>'
        '<div style="display:flex;align-items:center;'
        'gap:8px;margin:4px 0;">'
        '<span style="background:#00D4AA;width:10px;'
        'height:10px;border-radius:50%;"></span>'
        '<span>Hub MASA (30 km)</span></div>'
        '<div style="display:flex;align-items:center;'
        'gap:8px;margin:4px 0;">'
        '<span style="background:#FFB347;width:10px;'
        'height:10px;border-radius:50%;"></span>'
        '<span>Hub Zipline (80 km)</span></div>'
        '<div style="height:1px;background:#E0E4E8;'
        'margin:8px 0;"></div>'
        '<div style="display:flex;align-items:center;'
        'gap:8px;margin:4px 0;">'
        '<span style="background:#E63946;width:10px;'
        'height:10px;border-radius:50%;"></span>'
        '<span>Facility non couverte</span></div>'
        "</div>"
    )


@st.cache_data(show_spinner=False)
def _build_network_map_html(
    hubs: pd.DataFrame,
    facilities: pd.DataFrame,
) -> str:
    """HTML de la carte reseau (hubs + facilities)."""
    m = folium.Map(
        location=GHANA_CENTER,
        zoom_start=DEFAULT_ZOOM,
        tiles="CartoDB positron",
    )

    if not hubs.empty:
        lat_min = hubs["Latitude"].min()
        lat_max = hubs["Latitude"].max()
        lon_min = hubs["Longitude"].min()
        lon_max = hubs["Longitude"].max()
        margin = RADIUS_ZIPLINE / 111.0
        sw = [
            min(lat_min - margin, _GHANA_SW[0]),
            min(lon_min - margin, _GHANA_SW[1]),
        ]
        ne = [
            max(lat_max + margin, _GHANA_NE[0]),
            max(lon_max + margin, _GHANA_NE[1]),
        ]
        m.fit_bounds([sw, ne], padding=[30, 30])

    # --- Hubs MASA ---
    fg_masa = folium.FeatureGroup(
        name="Hubs MASA", show=True,
    )
    masa_hubs = hubs[hubs["Operateur"] == "MASA"]
    for _, row in masa_hubs.iterrows():
        lat = float(row["Latitude"])
        lon = float(row["Longitude"])
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(
                _hub_popup(row), max_width=220,
            ),
            icon=folium.Icon(
                color="green",
                icon_color="#FFFFFF",
                icon="plus",
                prefix="fa",
            ),
        ).add_to(fg_masa)
        folium.Circle(
            location=[lat, lon],
            radius=int(RADIUS_MASA * 1000),
            color="#00D4AA",
            weight=2,
            fill=True,
            fill_opacity=0.12,
        ).add_to(fg_masa)
    fg_masa.add_to(m)

    # --- Hubs Zipline ---
    fg_zl = folium.FeatureGroup(
        name="Hubs Zipline", show=True,
    )
    zl_hubs = hubs[hubs["Operateur"] == "Zipline"]
    for _, row in zl_hubs.iterrows():
        lat = float(row["Latitude"])
        lon = float(row["Longitude"])
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(
                _hub_popup(row), max_width=220,
            ),
            icon=folium.Icon(
                color="orange",
                icon_color="#FFFFFF",
                icon="plane",
                prefix="fa",
            ),
        ).add_to(fg_zl)
        folium.Circle(
            location=[lat, lon],
            radius=int(RADIUS_ZIPLINE * 1000),
            color="#FFB347",
            weight=1.5,
            fill=True,
            fill_opacity=0.06,
        ).add_to(fg_zl)
    fg_zl.add_to(m)

    # --- Facilities non couvertes ---
    uncovered = facilities[~facilities["Covered"]]
    fg_unc = folium.FeatureGroup(
        name="Facilities non couvertes", show=True,
    )
    for _, row in uncovered.iterrows():
        folium.CircleMarker(
            location=[
                float(row["Latitude"]),
                float(row["Longitude"]),
            ],
            radius=3,
            color="#E63946",
            fill=True,
            fill_opacity=0.85,
            weight=0,
        ).add_to(fg_unc)
    fg_unc.add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)
    m.get_root().html.add_child(  # type: ignore[attr-defined]
        folium.Element(_legend_html())
    )

    return m._repr_html_()


def render_network_map(
    hubs: pd.DataFrame,
    facilities: pd.DataFrame,
) -> None:
    """Affiche la carte du reseau deploye."""
    html = _build_network_map_html(hubs, facilities)
    components.html(html, height=680, scrolling=False)


def render_facility_map(
    facility: dict,
    hub: dict | None,
) -> None:
    """Mini-carte centree sur la facility et son hub.

    Parameters
    ----------
    facility : dict (keys: name, lat, lon, type)
    hub : dict from dispatch.find_nearest_hub
          (keys: hub_id, hub_lat, hub_lon, type, operateur)
          ou None si hors couverture.
    """
    lat, lon = facility["lat"], facility["lon"]

    if hub is not None:
        mid_lat = (lat + hub["hub_lat"]) / 2
        mid_lon = (lon + hub["hub_lon"]) / 2
        center = [mid_lat, mid_lon]
    else:
        center = [lat, lon]

    m = folium.Map(
        location=center,
        zoom_start=10,
        tiles="CartoDB positron",
    )

    if hub is not None:
        operateur = hub.get("operateur", "MASA")
        rayon_km = (
            RADIUS_ZIPLINE
            if operateur == "Zipline"
            else RADIUS_MASA
        )
        radius_deg = rayon_km / 111.0
        sw = [
            min(lat, hub["hub_lat"]) - radius_deg - 0.15,
            min(lon, hub["hub_lon"]) - radius_deg - 0.15,
        ]
        ne = [
            max(lat, hub["hub_lat"]) + radius_deg + 0.15,
            max(lon, hub["hub_lon"]) + radius_deg + 0.15,
        ]
        m.fit_bounds([sw, ne], padding=[40, 40])

    # Marqueur facility
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(
            '<div style="background:#FFFFFF;color:#1A2A3A;'
            'padding:12px 14px;border-radius:8px;'
            'border:1px solid #E0E4E8;'
            'font-family:Inter,sans-serif;font-size:13px;'
            'box-shadow:0 4px 12px rgba(0,0,0,0.1);">'
            f'<div style="font-weight:700;color:#E63946;'
            f'font-size:14px;margin-bottom:4px;">'
            f'{facility["name"]}</div>'
            f'<div style="color:#6B7D8E;">'
            f'{facility.get("type", "")}</div>'
            "</div>",
            max_width=220,
        ),
        icon=folium.Icon(
            color="red", icon="hospital-o", prefix="fa",
        ),
    ).add_to(m)

    if hub is not None:
        operateur = hub.get("operateur", "MASA")
        hub_color = OPERATOR_COLORS.get(operateur, "#00D4AA")
        rayon_km = (
            RADIUS_ZIPLINE
            if operateur == "Zipline"
            else RADIUS_MASA
        )
        icon_name = (
            "plane" if operateur == "Zipline" else "plus"
        )
        icon_color_folium = (
            "orange" if operateur == "Zipline" else "green"
        )

        folium.Marker(
            location=[hub["hub_lat"], hub["hub_lon"]],
            popup=folium.Popup(
                '<div style="background:#FFFFFF;'
                'color:#1A2A3A;padding:12px 14px;'
                'border-radius:8px;'
                'border:1px solid #E0E4E8;'
                'font-family:Inter,sans-serif;'
                'font-size:13px;'
                'box-shadow:0 4px 12px rgba(0,0,0,0.1);">'
                f'<div style="font-weight:700;'
                f'color:{hub_color};font-size:14px;'
                f'margin-bottom:4px;">'
                f'Hub {hub["hub_id"]}</div>'
                f'<div style="color:#6B7D8E;">'
                f'Opere par {operateur}</div>'
                "</div>",
                max_width=220,
            ),
            icon=folium.Icon(
                color=icon_color_folium,
                icon=icon_name,
                prefix="fa",
            ),
        ).add_to(m)
        folium.Circle(
            location=[hub["hub_lat"], hub["hub_lon"]],
            radius=int(rayon_km * 1000),
            color=hub_color,
            weight=2,
            fill=True,
            fill_opacity=0.10,
        ).add_to(m)
        folium.PolyLine(
            locations=[
                [lat, lon],
                [hub["hub_lat"], hub["hub_lon"]],
            ],
            color="#1A73E8",
            weight=2.5,
            dash_array="6",
        ).add_to(m)
    else:
        folium.Marker(
            location=[lat, lon],
            icon=folium.DivIcon(
                html=(
                    '<div style="font-size:11px;'
                    'color:#FF4757;font-weight:bold;'
                    'white-space:nowrap;">'
                    "Hors couverture</div>"
                ),
                icon_size=(100, 20),
                icon_anchor=(50, -10),
            ),
        ).add_to(m)

    components.html(
        m._repr_html_(), height=480, scrolling=False,
    )
