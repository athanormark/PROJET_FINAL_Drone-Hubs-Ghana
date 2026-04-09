"""Theme et injection CSS pour MASA."""

import streamlit as st

# -- Palette ----------------------------------------------------------------

PRIMARY = "#0A1628"
SURFACE = "#1A2A3A"
ACCENT = "#00D4AA"
ACCENT_SECONDARY = "#4FC3F7"
DANGER = "#FF4757"
WARNING = "#FFA502"
TEXT = "#E8EDF2"
TEXT_MUTED = "#8899AA"

# -- CSS complet ------------------------------------------------------------

CUSTOM_CSS = """
<style>
/* ==========================================================================
   0. RESET / BASE
   ========================================================================== */

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #E8EDF2;
}

[data-testid="stAppViewContainer"] {
    background: #0A1628;
}

[data-testid="stApp"] {
    background: #0A1628;
}

[data-testid="stHeader"] {
    background: transparent;
}

/* ==========================================================================
   1. HEADER & NAVIGATION
   ========================================================================== */

/* -- Sticky wrapper via st.container(key="header_wrap") ----------------- */
/* Cible le container Streamlit qui contient .masa-topbar via :has() */
[data-testid="stVerticalBlockBorderWrapper"]:has(.masa-topbar) {
    position: sticky;
    top: 0;
    z-index: 999;
    background: linear-gradient(135deg, #0D1B2A 0%, #152238 100%);
    border: 1px solid rgba(0, 212, 170, 0.10);
    border-bottom: 2px solid rgba(0, 212, 170, 0.12);
    border-radius: 14px;
    margin-bottom: 1rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

/* -- Top bar (brand line) ----------------------------------------------- */
.masa-topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 24px 6px 24px;
}

.masa-topbar-left {
    display: flex;
    align-items: center;
    gap: 10px;
}

.masa-topbar-icon {
    font-size: 1.35rem;
}

.masa-topbar-logo {
    height: 38px;
    width: 38px;
    border-radius: 50%;
    object-fit: contain;
    vertical-align: middle;
    margin-right: 8px;
    border: 1.5px solid rgba(0, 212, 170, 0.25);
    filter: drop-shadow(0 2px 6px rgba(0,0,0,0.4));
    background: radial-gradient(
        circle, rgba(10,22,40,0.6) 60%, transparent 100%
    );
}

.masa-topbar-name {
    font-size: 1.15rem;
    font-weight: 800;
    color: #00D4AA;
    letter-spacing: 2.5px;
    text-transform: uppercase;
}

.masa-topbar-sep {
    color: rgba(136, 153, 170, 0.25);
    font-weight: 300;
    font-size: 1rem;
    margin: 0 2px;
}

.masa-topbar-full {
    color: #6B7D8E;
    font-size: 0.78rem;
    font-weight: 400;
    letter-spacing: 0.5px;
}

.masa-topbar-right {
    display: flex;
    align-items: center;
    gap: 8px;
    padding-right: 4px;
}

.masa-topbar-facility {
    font-size: 0.82rem;
    font-weight: 600;
    color: #E8EDF2;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 240px;
}

.masa-topbar-dot {
    color: #6B7D8E;
    font-size: 0.9rem;
}

.masa-topbar-region {
    font-size: 0.72rem;
    color: #6B7D8E;
    font-weight: 400;
    letter-spacing: 0.3px;
}

/* -- Nav row columns (below topbar, fused visually) --------------------- */

[data-testid="stVerticalBlockBorderWrapper"]:has(.masa-topbar) [data-testid="stHorizontalBlock"] {
    padding: 0 16px 10px 16px;
    align-items: center;
}

/* facility info now in .masa-topbar-right (see topbar section above) */

/* -- Navigation tabs (st.radio styled as pill tabs) --------------------- */

[data-testid="stRadio"] > div[role="radiogroup"] {
    gap: 5px !important;
    padding: 2px 0;
}

[data-testid="stRadio"] > div[role="radiogroup"] > label {
    background: rgba(21, 34, 56, 0.6);
    border: 1px solid rgba(136, 153, 170, 0.08);
    border-radius: 10px;
    padding: 7px 22px !important;
    transition: all 0.25s ease;
    cursor: pointer;
    font-weight: 500;
    font-size: 0.82rem;
    letter-spacing: 0.5px;
}

[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
    background: rgba(0, 212, 170, 0.06);
    border-color: rgba(0, 212, 170, 0.18);
    color: #E8EDF2;
}

[data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"] {
    background: linear-gradient(135deg, rgba(0, 212, 170, 0.14) 0%, rgba(79, 195, 247, 0.10) 100%);
    border-color: rgba(0, 212, 170, 0.35);
    color: #00D4AA !important;
    font-weight: 600;
    box-shadow: 0 2px 12px rgba(0, 212, 170, 0.1);
}

/* -- Deconnexion button styling ----------------------------------------- */

.stButton > button[kind="secondary"],
.stButton > button[data-testid="stBaseButton-secondary"] {
    background: transparent;
    border: 1px solid rgba(255, 107, 107, 0.22);
    color: #FF6B6B;
    border-radius: 8px;
    font-size: 0.72rem;
    font-weight: 500;
    padding: 6px 14px;
    letter-spacing: 0.3px;
    transition: all 0.2s ease;
    white-space: nowrap;
    min-height: auto;
    line-height: 1.3;
}

.stButton > button[kind="secondary"]:hover,
.stButton > button[data-testid="stBaseButton-secondary"]:hover {
    background: rgba(255, 71, 87, 0.12);
    border-color: rgba(255, 71, 87, 0.4);
    color: #FF4757;
}

/* -- Logout column vertical alignment ----------------------------------- */

[data-testid="stVerticalBlockBorderWrapper"]:has(.masa-topbar) [data-testid="stColumn"]:last-child {
    display: flex;
    align-items: center;
    justify-content: flex-end;
}

[data-testid="stVerticalBlockBorderWrapper"]:has(.masa-topbar) [data-testid="stColumn"]:last-child .stButton > button {
    width: auto !important;
    min-width: unset;
}

/* -- Sidebar ------------------------------------------------------------ */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1628 0%, #121E30 40%, #1A2A3A 100%);
    border-right: 1px solid rgba(0, 212, 170, 0.08);
}

/* ==========================================================================
   2. METRIC CARDS
   ========================================================================== */

[data-testid="stMetric"] {
    background: rgba(26, 42, 58, 0.55);
    border: 1px solid rgba(0, 212, 170, 0.12);
    border-radius: 16px;
    padding: 20px 24px;
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

[data-testid="stMetric"]:hover {
    border-color: rgba(0, 212, 170, 0.3);
    box-shadow: 0 4px 20px rgba(0, 212, 170, 0.06);
}

[data-testid="stMetricLabel"] {
    color: #8899AA;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

[data-testid="stMetricValue"] {
    font-size: 1.8rem;
    font-weight: 700;
    color: #E8EDF2;
}

[data-testid="stMetricDelta"] svg {
    display: inline;
}

[data-testid="stMetricDelta"] > div {
    font-weight: 600;
}

/* ==========================================================================
   3. BOUTONS
   ========================================================================== */

.stButton > button {
    border-radius: 12px;
    font-weight: 600;
    letter-spacing: 0.3px;
    transition: all 0.2s ease;
    border: 1px solid rgba(0, 212, 170, 0.2);
    padding: 0.5rem 1.5rem;
}

.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, #00D4AA 0%, #00B4D8 50%, #4FC3F7 100%);
    border: none;
    color: #0A1628;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-size: 0.85rem;
}

.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover {
    box-shadow: 0 6px 24px rgba(0, 212, 170, 0.35);
    transform: translateY(-2px);
}

.stButton > button[kind="primary"]:active,
.stButton > button[data-testid="stBaseButton-primary"]:active {
    transform: translateY(0);
    box-shadow: 0 2px 8px rgba(0, 212, 170, 0.2);
}


/* ==========================================================================
   4. FORMULAIRES
   ========================================================================== */

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(26, 42, 58, 0.5);
    border: 1px solid rgba(136, 153, 170, 0.2);
    border-radius: 12px;
    color: #E8EDF2;
    padding: 10px 14px;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #00D4AA;
    box-shadow: 0 0 0 3px rgba(0, 212, 170, 0.1);
    outline: none;
}

.stTextInput > label,
.stNumberInput > label,
.stTextArea > label,
.stSelectbox > label,
.stMultiSelect > label,
.stSlider > label,
.stRadio > label,
.stCheckbox > label {
    color: #8899AA;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}

.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: rgba(26, 42, 58, 0.5);
    border: 1px solid rgba(136, 153, 170, 0.2);
    border-radius: 12px;
    transition: border-color 0.2s ease;
}

.stSelectbox > div > div:hover,
.stMultiSelect > div > div:hover {
    border-color: rgba(0, 212, 170, 0.4);
}

.stSlider > div > div > div > div {
    background: #00D4AA;
}

/* ==========================================================================
   5. BADGES / PILLS
   ========================================================================== */

.pill-critique {
    display: inline-block;
    background: rgba(255, 71, 87, 0.15);
    color: #FF4757;
    border: 1px solid rgba(255, 71, 87, 0.3);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.3px;
}

.pill-haute {
    display: inline-block;
    background: rgba(255, 165, 2, 0.15);
    color: #FFA502;
    border: 1px solid rgba(255, 165, 2, 0.3);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.3px;
}

.pill-standard {
    display: inline-block;
    background: rgba(79, 195, 247, 0.15);
    color: #4FC3F7;
    border: 1px solid rgba(79, 195, 247, 0.3);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.3px;
}

.pill-preparation {
    display: inline-block;
    background: rgba(255, 215, 0, 0.12);
    color: #FFD700;
    border: 1px solid rgba(255, 215, 0, 0.25);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.3px;
}

.pill-en-vol {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(79, 195, 247, 0.15);
    color: #4FC3F7;
    border: 1px solid rgba(79, 195, 247, 0.3);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.3px;
}

.pill-livree {
    display: inline-block;
    background: rgba(0, 212, 170, 0.15);
    color: #00D4AA;
    border: 1px solid rgba(0, 212, 170, 0.3);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.3px;
}

/* ==========================================================================
   6. CARDS
   ========================================================================== */

/* Login centered container */
.login-container {
    max-width: 480px;
    margin: 0 auto;
}

.masa-card {
    background: rgba(26, 42, 58, 0.5);
    border: 1px solid rgba(136, 153, 170, 0.1);
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    margin-bottom: 1rem;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.masa-card:hover {
    border-color: rgba(136, 153, 170, 0.2);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.masa-card-highlight {
    background: rgba(26, 42, 58, 0.5);
    border: 1px solid rgba(0, 212, 170, 0.25);
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    margin-bottom: 1rem;
    box-shadow: 0 0 20px rgba(0, 212, 170, 0.04);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.masa-card-highlight:hover {
    border-color: rgba(0, 212, 170, 0.4);
    box-shadow: 0 4px 24px rgba(0, 212, 170, 0.08);
}

/* -- Login card via st.container(key="login_card") + :has() ------------ */
[data-testid="stVerticalBlockBorderWrapper"]:has(.login-hero) {
    background: linear-gradient(180deg, rgba(13, 27, 42, 0.92) 0%, rgba(21, 34, 56, 0.78) 100%);
    border: 1px solid rgba(0, 212, 170, 0.12);
    border-radius: 24px;
    padding: 1.5rem 0.5rem;
    box-shadow: 0 8px 40px rgba(0, 0, 0, 0.35), 0 0 80px rgba(0, 212, 170, 0.03);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}

.login-hero {
    text-align: center;
    padding: 1rem 0 1.2rem;
}

.login-icon {
    font-size: 3.5rem;
    margin-bottom: 0.5rem;
}

.login-logo {
    width: 200px;
    height: 200px;
    object-fit: contain;
    margin: 0 auto 1.2rem auto;
    display: block;
    filter: drop-shadow(0 4px 16px rgba(0, 212, 170, 0.25))
            drop-shadow(0 0 40px rgba(0, 212, 170, 0.08));
    transition: transform 0.3s ease;
}

.login-logo:hover {
    transform: scale(1.04);
}

.login-title {
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
    color: #E8EDF2 !important;
    margin: 0 !important;
    border-bottom: none !important;
    padding-bottom: 0 !important;
}

.login-subtitle {
    color: #8899AA;
    font-size: 0.95rem;
    margin-top: 0.3rem;
    letter-spacing: 0.5px;
}

.login-stats-label {
    text-align: center;
    font-size: 0.7rem;
    font-weight: 600;
    color: #6B7D8E;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

.login-budget-bar {
    text-align: center;
    color: #8899AA;
    font-size: 0.85rem;
    margin-top: 0.5rem;
}

.order-card {
    background: rgba(26, 42, 58, 0.45);
    border: 1px solid rgba(136, 153, 170, 0.08);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 10px;
    transition: all 0.2s ease;
}

.order-card:hover {
    background: rgba(26, 42, 58, 0.65);
    border-color: rgba(0, 212, 170, 0.15);
}

.order-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 4px;
}

.order-header-left {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-shrink: 0;
}

.order-header-left .order-id {
    font-weight: 700;
    font-size: 0.95rem;
    color: #E8EDF2;
}

.order-header-left .order-ts {
    font-size: 0.78rem;
    color: #8899AA;
    font-weight: 400;
}

.order-header-right {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-shrink: 0;
}

/* ==========================================================================
   7. ANIMATIONS
   ========================================================================== */

@keyframes pulse-glow {
    0%, 100% {
        opacity: 1;
        box-shadow: 0 0 0 0 rgba(79, 195, 247, 0.6);
    }
    50% {
        opacity: 0.6;
        box-shadow: 0 0 0 6px rgba(79, 195, 247, 0);
    }
}

.pulse-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #4FC3F7;
    animation: pulse-glow 2s ease-in-out infinite;
    vertical-align: middle;
}

@keyframes slide-in-up {
    from {
        opacity: 0;
        transform: translateY(12px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in {
    animation: slide-in-up 0.35s ease-out;
}

@keyframes progress-bar {
    from { width: 0; }
    to { width: 100%; }
}

.eta-bar {
    height: 4px;
    border-radius: 2px;
    background: linear-gradient(90deg, #00D4AA, #4FC3F7);
    animation: progress-bar 1.5s ease-out;
}

/* ==========================================================================
   8. RESPONSIVE
   ========================================================================== */

/* -- Tablet (max 768px) ------------------------------------------------- */
@media (max-width: 768px) {
    [data-testid="stMainBlockContainer"] {
        padding-left: 0.75rem;
        padding-right: 0.75rem;
    }

    [data-testid="stMetric"] {
        padding: 12px 14px;
        border-radius: 12px;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.3rem;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.65rem;
    }

    .masa-card, .masa-card-highlight {
        padding: 16px;
        border-radius: 12px;
    }

    .login-card {
        padding: 24px 18px;
        margin: 0 8px;
    }

    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap;
        gap: 0.5rem;
    }

    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        min-width: calc(50% - 8px);
        flex: 1 1 calc(50% - 8px);
    }

    h1 { font-size: 1.5rem !important; }
    h2 { font-size: 1.2rem !important; }
    h3 { font-size: 1rem !important; }

    /* Navigation radio - scroll horizontal */
    [data-testid="stRadio"] > div {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        white-space: nowrap;
        padding-bottom: 4px;
    }

    [data-testid="stRadio"] > div > label {
        font-size: 0.8rem !important;
        padding: 6px 12px !important;
    }

    /* Folium maps */
    iframe {
        max-height: 350px;
    }

    /* Boutons full width */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {
        width: 100%;
    }

    /* Dataframe scroll */
    [data-testid="stDataFrame"] {
        overflow-x: auto;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:has(.masa-topbar) {
        border-radius: 10px;
        margin-bottom: 0.75rem;
    }

    .masa-topbar {
        padding: 10px 14px 2px 14px;
    }

    .masa-topbar-logo {
        height: 32px;
        width: 32px;
        margin-right: 6px;
    }

    .login-logo {
        width: 160px;
        height: 160px;
    }

    .masa-topbar-full {
        display: none;
    }

    .masa-topbar-sep {
        display: none;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:has(.masa-topbar) [data-testid="stHorizontalBlock"] {
        padding: 0 10px 8px 10px;
    }

    .masa-topbar-right {
        gap: 6px;
    }

    .masa-topbar-facility {
        max-width: 140px;
        font-size: 0.75rem;
    }

    .masa-topbar-region {
        display: none;
    }

    .masa-topbar-dot {
        display: none;
    }

    /* Bouton Deconnexion compact sur tablette */
    [data-testid="stVerticalBlockBorderWrapper"]:has(.masa-topbar) [data-testid="stColumn"]:last-child .stButton > button {
        font-size: 0.65rem;
        padding: 5px 10px;
        width: auto !important;
    }
}

/* -- Mobile (max 480px) ------------------------------------------------- */
@media (max-width: 480px) {
    [data-testid="stMainBlockContainer"] {
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.1rem;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.6rem;
    }

    [data-testid="stMetric"] {
        padding: 10px 12px;
        border-radius: 10px;
    }

    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        min-width: calc(50% - 4px);
        flex: 1 1 calc(50% - 4px);
    }

    .masa-card, .masa-card-highlight {
        padding: 12px;
        border-radius: 10px;
    }

    .login-card {
        padding: 20px 14px;
    }

    h1 { font-size: 1.3rem !important; }
    h2 { font-size: 1.05rem !important; }
    h3 { font-size: 0.9rem !important; }

    /* Radio nav plus compact */
    [data-testid="stRadio"] > div > label {
        font-size: 0.72rem !important;
        padding: 5px 8px !important;
    }

    /* Folium maps */
    iframe {
        max-height: 280px;
    }

    /* Boutons full width sauf Deconnexion */
    .stButton > button {
        width: 100%;
        font-size: 0.8rem;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:has(.masa-topbar) [data-testid="stColumn"]:last-child .stButton > button {
        width: auto !important;
        font-size: 0.6rem;
        padding: 4px 8px;
    }

    /* Pills plus petits */
    .pill-critique, .pill-haute, .pill-standard,
    .pill-preparation, .pill-en-vol, .pill-livree {
        font-size: 0.65rem;
        padding: 3px 8px;
    }

    .order-header {
        flex-direction: column;
        align-items: flex-start;
    }

    .order-header-right {
        align-self: flex-start;
    }

    .masa-topbar-logo {
        height: 28px;
        width: 28px;
        margin-right: 4px;
    }

    .login-logo {
        width: 140px;
        height: 140px;
    }

    .masa-topbar-right {
        display: none;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:has(.login-hero) {
        padding: 1rem 0.25rem;
        border-radius: 18px;
    }

    .login-title {
        font-size: 2.2rem !important;
    }

    /* Formulaires */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        padding: 8px 10px;
        font-size: 0.85rem;
    }

    .stSelectbox > div > div {
        font-size: 0.85rem;
    }
}

/* -- Mobile small (max 375px) ------------------------------------------- */
@media (max-width: 375px) {
    [data-testid="stMetricValue"] {
        font-size: 1rem;
    }

    h1 { font-size: 1.2rem !important; }
}

/* ==========================================================================
   9. TYPOGRAPHIE
   ========================================================================== */

h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #E8EDF2;
    letter-spacing: -0.3px;
    line-height: 1.2;
}

h2 {
    font-size: 1.5rem;
    font-weight: 600;
    color: #00D4AA;
    border-bottom: 2px solid rgba(0, 212, 170, 0.15);
    padding-bottom: 8px;
    margin-top: 1.5rem;
}

h3 {
    font-size: 1.2rem;
    font-weight: 600;
    color: #E8EDF2;
}

p, li, span {
    color: #E8EDF2;
    line-height: 1.6;
}

a {
    color: #4FC3F7;
    text-decoration: none;
    transition: color 0.15s ease;
}

a:hover {
    color: #00D4AA;
}

small, .text-muted {
    color: #8899AA;
}

/* ==========================================================================
   10. MASQUER BRANDING STREAMLIT
   ========================================================================== */

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header[data-testid="stHeader"] { visibility: hidden; height: 0; }

[data-testid="stDecoration"] { display: none; }

[data-testid="stToolbar"] { display: none; }

/* ==========================================================================
   11. SCROLLBAR
   ========================================================================== */

::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: #0A1628;
}

::-webkit-scrollbar-thumb {
    background: rgba(0, 212, 170, 0.25);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 212, 170, 0.45);
}

* {
    scrollbar-width: thin;
    scrollbar-color: rgba(0, 212, 170, 0.25) #0A1628;
}

/* ==========================================================================
   12. CARTES FOLIUM (iframes)
   ========================================================================== */

iframe {
    border-radius: 14px !important;
    border: 1px solid rgba(0, 212, 170, 0.06) !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.18) !important;
    width: 100% !important;
}

/* ==========================================================================
   13. ELEMENTS COMPLEMENTAIRES
   ========================================================================== */

hr {
    border-color: rgba(0, 212, 170, 0.08);
    margin: 1.25rem 0;
}

[data-testid="stExpander"] {
    background: rgba(26, 42, 58, 0.35);
    border: 1px solid rgba(136, 153, 170, 0.1);
    border-radius: 12px;
}

[data-testid="stExpander"] summary {
    font-weight: 600;
    color: #E8EDF2;
}

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stDataFrame"] table {
    font-size: 0.85rem;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: transparent;
    border-bottom: 1px solid rgba(136, 153, 170, 0.1);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    padding: 8px 20px;
    font-weight: 500;
    color: #8899AA;
    transition: all 0.15s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #E8EDF2;
    background: rgba(0, 212, 170, 0.05);
}

.stTabs [aria-selected="true"] {
    color: #00D4AA !important;
    border-bottom: 2px solid #00D4AA;
}

.stAlert [data-testid="stAlertContentInfo"] {
    background: rgba(79, 195, 247, 0.08);
    border: 1px solid rgba(79, 195, 247, 0.2);
    border-radius: 12px;
    color: #E8EDF2;
}

.stAlert [data-testid="stAlertContentWarning"] {
    background: rgba(255, 165, 2, 0.08);
    border: 1px solid rgba(255, 165, 2, 0.2);
    border-radius: 12px;
    color: #E8EDF2;
}

.stAlert [data-testid="stAlertContentError"] {
    background: rgba(255, 71, 87, 0.08);
    border: 1px solid rgba(255, 71, 87, 0.2);
    border-radius: 12px;
    color: #E8EDF2;
}

.stAlert [data-testid="stAlertContentSuccess"] {
    background: rgba(0, 212, 170, 0.08);
    border: 1px solid rgba(0, 212, 170, 0.2);
    border-radius: 12px;
    color: #E8EDF2;
}

.stProgress > div > div > div {
    background: linear-gradient(90deg, #00D4AA, #4FC3F7);
    border-radius: 4px;
}

.stSpinner > div {
    border-top-color: #00D4AA;
}

[data-testid="stToast"] {
    background: #1A2A3A;
    border: 1px solid rgba(0, 212, 170, 0.2);
    border-radius: 12px;
    color: #E8EDF2;
}

/* ==========================================================================
   13. UTILITAIRES
   ========================================================================== */

.text-accent { color: #00D4AA; }
.text-info { color: #4FC3F7; }
.text-danger { color: #FF4757; }
.text-warning { color: #FFA502; }
.text-muted { color: #8899AA; }
.text-bold { font-weight: 700; }
.text-center { text-align: center; }
.text-sm { font-size: 0.8rem; }
.text-xs { font-size: 0.7rem; }
.text-lg { font-size: 1.25rem; }

.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mt-3 { margin-top: 1.5rem; }
.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }

.flex-row {
    display: flex;
    align-items: center;
    gap: 8px;
}

.flex-between {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

</style>
"""


_FONT_PRELOAD = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"'
    ' rel="stylesheet">'
)


def inject_theme() -> None:
    """Injecte le CSS dans la page Streamlit."""
    st.markdown(_FONT_PRELOAD, unsafe_allow_html=True)
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
