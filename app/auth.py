"""Authentification par facility pour MASA.

Donnees en session_state uniquement, aucune persistence
externe (conformite RGPD).
"""

import streamlit as st

from app.config import DEMO_ACCOUNTS


def init_session() -> None:
    """Initialise les cles session_state si absentes."""
    defaults: dict = {
        "authenticated": False,
        "facility": None,
        "orders": [],
        "cart": [],
        "role": "user",
        "order_history": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def login_form() -> bool:
    """Affiche le formulaire de connexion.

    Returns
    -------
    bool
        True si l'utilisateur vient de se connecter.
    """
    login_id = st.text_input("Identifiant", placeholder="Ex : AGN-HC-001")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter", type="primary", use_container_width=True):
        if not login_id:
            st.error("Saisissez votre identifiant.")
            return False

        cleaned = login_id.strip()
        account = DEMO_ACCOUNTS.get(cleaned.upper())
        if account is None:
            account = DEMO_ACCOUNTS.get(cleaned)

        if account and password == account["password"]:
            _authenticate(cleaned, account)
            return True

        st.error("Identifiant ou mot de passe incorrect.")
    return False


def _authenticate(login_id: str, account: dict) -> None:
    """Stocke les informations de session apres authentification."""
    st.session_state.authenticated = True
    st.session_state.role = account.get("role", "user")
    st.session_state.facility = {
        "name": account["facility_name"],
        "login": login_id,
        "lat": account["lat"],
        "lon": account["lon"],
        "type": account["type"],
        "region": account.get("region", ""),
        "scenario": account["scenario"],
    }

    if "order_history" not in st.session_state:
        st.session_state.order_history = {}

    previous = st.session_state.order_history.get(login_id, [])
    st.session_state.orders = list(previous)
    st.session_state.cart = []


def demo_account_selector() -> bool:
    """Selecteur de compte demo en un clic.

    Returns
    -------
    bool
        True si un compte demo vient d'etre selectionne.
    """
    st.markdown(
        "<div style='text-align:center;color:#8899AA;margin:1.5rem 0 1rem;'>"
        "&mdash; ou &mdash;</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p style='color:#E8EDF2;font-weight:600;font-size:0.95rem;"
        "margin-bottom:0.5rem;'>Comptes de demonstration</p>",
        unsafe_allow_html=True,
    )

    scenario_labels = {
        "proche": "MASA proche",
        "zipline": "Zipline",
        "hors_couverture": "hors couverture",
        "admin": "admin",
    }

    options: list[str] = [""]
    account_map: dict[str, str] = {}
    for login_id, acc in DEMO_ACCOUNTS.items():
        scenario = scenario_labels.get(
            acc["scenario"], acc["scenario"],
        )
        region = acc.get("region", "")
        if region:
            label = (
                f"{acc['facility_name']}"
                f" — {region} ({scenario})"
            )
        else:
            label = (
                f"{acc['facility_name']}"
                f" ({scenario})"
            )
        options.append(label)
        account_map[label] = login_id

    selected = st.selectbox(
        "Compte demo",
        options,
        index=0,
        format_func=lambda x: "Choisir un compte..." if x == "" else x,
        label_visibility="collapsed",
        key="demo_selector",
    )

    if st.button(
        "Connexion rapide",
        type="primary",
        use_container_width=True,
        disabled=(selected == ""),
        key="btn_demo_login",
    ):
        login_id = account_map[selected]
        account = DEMO_ACCOUNTS[login_id]
        _authenticate(login_id, account)
        return True

    return False


def get_current_facility() -> dict | None:
    """Retourne la facility connectee ou None."""
    if not st.session_state.get("authenticated", False):
        return None
    return st.session_state.get("facility")


def logout() -> None:
    """Deconnecte et reinitialise la session."""
    facility = st.session_state.get("facility")
    if facility and st.session_state.get("orders"):
        login_id = facility.get("login", "")
        if login_id:
            st.session_state.order_history[login_id] = list(
                st.session_state.orders
            )

    st.session_state.authenticated = False
    st.session_state.facility = None
    st.session_state.orders = []
    st.session_state.cart = []
    st.session_state.role = "user"


def require_auth() -> bool:
    """Verifie l'authentification courante."""
    if st.session_state.get("authenticated", False):
        return True
    st.warning("Connexion requise pour acceder a cette page.")
    return False
