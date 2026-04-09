"""Point d'entree MASA -- Medical Air Supply Application."""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "src"))
sys.path.insert(0, str(_ROOT))

import streamlit as st

from app.auth import (
    demo_account_selector,
    get_current_facility,
    init_session,
    login_form,
    logout,
)
import base64
from app.config import APP_FULL_NAME, APP_ICON, APP_NAME

_LOGO_PATH = Path(__file__).parent / "assets" / "masa_logo.png"


def _logo_b64() -> str:
    """Encode le logo en base64 pour affichage HTML."""
    if _LOGO_PATH.exists():
        data = _LOGO_PATH.read_bytes()
        return base64.b64encode(data).decode()
    return ""
from app.data_loader import (
    get_network_stats,
    load_facilities,
    load_hubs,
    load_villages,
)
from app.theme import inject_theme
from app.components.analytics import render_analytics
from app.components.map_view import (
    render_facility_map,
    render_network_map,
)
from app.components.order_form import render_order_form
from app.components.tracking import render_tracking
from dispatch import can_dispatch, find_nearest_hub


def _setup_page() -> None:
    st.set_page_config(
        page_title=APP_NAME,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="collapsed",
    )


def _header_admin() -> str:
    """Header administrateur sans info facility."""
    nav_options = ["Reseau", "Analyse"]

    current = st.session_state.get(
        "nav_radio", nav_options[0],
    )
    if current not in nav_options:
        st.session_state["nav_radio"] = nav_options[0]

    _logo_style = (
        "height:38px;width:38px;border-radius:50%;"
        "object-fit:contain;vertical-align:middle;"
        "margin-right:8px;flex-shrink:0;"
    )
    with st.container(key="header_wrap"):
        st.markdown(
            f'<div class="masa-topbar">'
            f'<div class="masa-topbar-left">'
            f'<img src="data:image/png;base64,'
            f'{_logo_b64()}" class="masa-topbar-logo"'
            f' style="{_logo_style}">'
            f'<span class="masa-topbar-name">'
            f'{APP_NAME}</span>'
            f'<span class="masa-topbar-sep">|</span>'
            f'<span class="masa-topbar-full">'
            f'{APP_FULL_NAME}</span>'
            f'</div>'
            f'<div class="masa-topbar-right">'
            f'<span class="masa-topbar-facility">'
            f'Administration</span>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        col_nav, col_logout = st.columns([9, 1])
        with col_nav:
            page = st.radio(
                "nav",
                nav_options,
                horizontal=True,
                label_visibility="collapsed",
                key="nav_radio",
            )
        with col_logout:
            if st.button(
                "Deconnexion",
                key="btn_logout",
                type="secondary",
            ):
                logout()
                st.rerun()

    return page


def _header(facility: dict) -> str:
    region = facility.get("region", "")

    nav_options = ["Reseau", "Commander", "Suivi"]

    current = st.session_state.get(
        "nav_radio", nav_options[0],
    )
    if current not in nav_options:
        st.session_state["nav_radio"] = nav_options[0]

    _logo_style = (
        "height:38px;width:38px;border-radius:50%;"
        "object-fit:contain;vertical-align:middle;"
        "margin-right:8px;flex-shrink:0;"
    )
    with st.container(key="header_wrap"):
        st.markdown(
            f'<div class="masa-topbar">'
            f'<div class="masa-topbar-left">'
            f'<img src="data:image/png;base64,'
            f'{_logo_b64()}" class="masa-topbar-logo"'
            f' style="{_logo_style}">'
            f'<span class="masa-topbar-name">'
            f'{APP_NAME}</span>'
            f'<span class="masa-topbar-sep">|</span>'
            f'<span class="masa-topbar-full">'
            f'{APP_FULL_NAME}</span>'
            f'</div>'
            f'<div class="masa-topbar-right">'
            f'<span class="masa-topbar-facility">'
            f'{facility["name"]}</span>'
            f'<span class="masa-topbar-dot">'
            f'&middot;</span>'
            f'<span class="masa-topbar-region">'
            f'{region}</span>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        col_nav, col_logout = st.columns([9, 1])
        with col_nav:
            page = st.radio(
                "nav",
                nav_options,
                horizontal=True,
                label_visibility="collapsed",
                key="nav_radio",
            )
        with col_logout:
            if st.button(
                "Deconnexion",
                key="btn_logout",
                type="secondary",
            ):
                logout()
                st.rerun()

    return page


def _login_page(
    hubs: "pd.DataFrame",
    facilities: "pd.DataFrame",
) -> None:
    st.markdown(
        "<div style='height:4vh;'></div>",
        unsafe_allow_html=True,
    )

    _, col_center, _ = st.columns([1, 2, 1])

    with col_center:
        with st.container(key="login_card"):
            _login_logo_style = (
                "width:200px;height:200px;"
                "object-fit:contain;display:block;"
                "margin:0 auto 1.2rem auto;"
            )
            st.markdown(
                f'<div class="login-hero"'
                f' style="text-align:center;padding:1rem 0;">'
                f'<img src="data:image/png;base64,'
                f'{_logo_b64()}" class="login-logo"'
                f' style="{_login_logo_style}">'
                f'</div>',
                unsafe_allow_html=True,
            )

            if login_form():
                st.rerun()

            if demo_account_selector():
                st.rerun()

    st.markdown(
        "<div style='height:2rem;'></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="login-stats-label">'
        'Reseau deploye</div>',
        unsafe_allow_html=True,
    )

    stats = get_network_stats(hubs, facilities)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Hubs MASA", stats["n_hubs"])
    c2.metric("Drones", stats["n_drones"])
    c3.metric(
        "Couverture",
        f"{stats['couverture_pct']}%",
    )
    c4.metric(
        "Facilities couvertes",
        f"{stats['n_facilities_couvertes']:,}"
        f"/{stats['n_facilities_total']:,}",
    )

    capex = stats["capex_total"]
    opex = stats["opex_annuel"]
    tco = capex + 5 * opex
    st.markdown(
        f'<div class="login-budget-bar">'
        f'CAPEX <span class="text-accent">'
        f'${capex / 1e6:.2f}M</span>'
        f' &nbsp;|&nbsp; OPEX '
        f'<span class="text-info">'
        f'${opex / 1e6:.2f}M/an</span>'
        f' &nbsp;|&nbsp; TCO 5 ans '
        f'<span style="color:#E8EDF2;'
        f'font-weight:600;">'
        f'${tco / 1e6:.2f}M</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _operator_badge(operateur: str) -> None:
    """Affiche un badge colore selon l'operateur."""
    if operateur == "Zipline":
        st.markdown(
            '<div style="background:rgba(255,179,71,0.15);'
            'border:1px solid #FFB347;'
            'border-radius:12px;padding:12px 16px;'
            'margin-bottom:12px;">'
            '<span style="color:#FFB347;'
            'font-weight:700;font-size:0.95rem;">'
            'Opere par Zipline</span><br>'
            '<span style="color:#8899AA;'
            'font-size:0.8rem;">'
            'Commandes non disponibles via MASA '
            '-- contactez Zipline directement.'
            '</span></div>',
            unsafe_allow_html=True,
        )
    elif operateur == "MASA":
        st.markdown(
            '<div style="background:rgba(0,212,170,0.1);'
            'border:1px solid rgba(0,212,170,0.3);'
            'border-radius:12px;padding:12px 16px;'
            'margin-bottom:12px;">'
            '<span style="color:#00D4AA;'
            'font-weight:700;font-size:0.95rem;">'
            'Opere par MASA</span></div>',
            unsafe_allow_html=True,
        )


def _page_reseau(
    hubs: "pd.DataFrame",
    facilities: "pd.DataFrame",
) -> None:
    st.markdown("## Reseau de hubs")

    facility = get_current_facility()
    if facility:
        hub_info = find_nearest_hub(
            facility["lat"], facility["lon"], hubs,
        )

        col_map, col_info = st.columns([2, 1])
        with col_map:
            render_facility_map(facility, hub_info)
        with col_info:
            st.markdown("#### Votre hub")
            if hub_info:
                operateur = hub_info.get(
                    "operateur", "MASA",
                )
                _operator_badge(operateur)
                st.metric(
                    "Hub assigne",
                    f"#{hub_info['hub_id']}",
                )
                st.metric(
                    "Distance",
                    f"{hub_info['distance_km']:.1f} km",
                )
                st.metric("Type", hub_info["type"])
                if operateur == "MASA":
                    st.metric(
                        "Drones disponibles",
                        hub_info["n_drones"],
                    )
            else:
                st.error(
                    "Facility non couverte par "
                    "le reseau actuel."
                )
                st.markdown(
                    "Aucun hub a portee. "
                    "Cette facility ne peut pas "
                    "etre desservie."
                )
        st.divider()

    st.markdown("#### Vue globale du reseau")
    render_network_map(hubs, facilities)


def _page_commander(hubs: "pd.DataFrame") -> None:
    st.markdown("## Commander")
    facility = get_current_facility()
    if not facility:
        st.warning(
            "Connexion requise pour passer commande."
        )
        return

    hub_info = find_nearest_hub(
        facility["lat"], facility["lon"], hubs,
    )

    # Verifier si dispatch possible (MASA uniquement)
    if not can_dispatch(hub_info):
        if hub_info and hub_info.get(
            "operateur",
        ) == "Zipline":
            _operator_badge("Zipline")
            st.info(
                "Les commandes via MASA ne sont "
                "pas disponibles pour les facilities "
                "desservies par Zipline. "
                "Veuillez contacter Zipline."
            )
        else:
            st.error(
                "Facility non couverte. "
                "Aucun hub a portee."
            )
        return

    render_order_form(facility, hubs)


def _page_suivi() -> None:
    st.markdown("## Suivi des commandes")
    facility = get_current_facility()
    if not facility:
        st.warning(
            "Connexion requise pour le suivi."
        )
        return
    render_tracking(facility)


def _page_analyse(
    hubs: "pd.DataFrame",
    facilities: "pd.DataFrame",
) -> None:
    render_analytics(hubs, facilities)


def main() -> None:
    _setup_page()
    init_session()
    inject_theme()

    hubs = load_hubs()
    facilities = load_facilities()

    if not st.session_state.get(
        "authenticated", False,
    ):
        _login_page(hubs, facilities)
        return

    if "_goto_page" in st.session_state:
        st.session_state["nav_radio"] = (
            st.session_state.pop("_goto_page")
        )

    facility = get_current_facility()
    role = st.session_state.get("role", "user")

    if role == "admin":
        page = _header_admin()
        if page == "Reseau":
            st.markdown("## Reseau de hubs")
            st.markdown("#### Vue globale du reseau")
            render_network_map(hubs, facilities)
        elif page == "Analyse":
            _page_analyse(hubs, facilities)
    else:
        page = _header(facility)
        if page == "Reseau":
            _page_reseau(hubs, facilities)
        elif page == "Commander":
            _page_commander(hubs)
        elif page == "Suivi":
            _page_suivi()


if __name__ == "__main__":
    main()
