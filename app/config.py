"""Constantes applicatives MASA."""

from pathlib import Path

# --- Chemins ---
REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data" / "processed"

# --- Application ---
APP_NAME = "MASA"
APP_FULL_NAME = "Medical Air Supply Application"
APP_ICON = "\U0001F6E9\uFE0F"

# --- Contraintes drone ---
DRONE_SPEED_KMH: float = 110.0
PREP_TIME_MIN: float = 5.0
MAX_RADIUS_KM: float = 80.0
DRONE_CAPACITY_KG: float = 4.0

# --- Rayons par operateur ---
RADIUS_MASA: float = 30.0
RADIUS_ZIPLINE: float = 80.0

# --- Catalogue produits ---
PRODUCTS: dict[str, dict] = {
    "sang": {
        "label": "Sang et produits sanguins",
        "poids_kg": 1.5,
        "urgence_defaut": "critique",
    },
    "vaccins": {
        "label": "Vaccins",
        "poids_kg": 0.8,
        "urgence_defaut": "haute",
    },
    "antivenins": {
        "label": "Antivenins",
        "poids_kg": 0.5,
        "urgence_defaut": "critique",
    },
    "paludisme": {
        "label": "Tests et traitements du paludisme",
        "poids_kg": 0.4,
        "urgence_defaut": "haute",
    },
    "douleur": {
        "label": "Medicaments contre la douleur",
        "poids_kg": 0.5,
        "urgence_defaut": "standard",
    },
    "toux": {
        "label": "Medicaments contre la toux",
        "poids_kg": 0.4,
        "urgence_defaut": "standard",
    },
    "parasites": {
        "label": "Traitements contre les parasites intestinaux",
        "poids_kg": 0.3,
        "urgence_defaut": "standard",
    },
    "nutrition": {
        "label": "Supplements nutritionnels",
        "poids_kg": 1.0,
        "urgence_defaut": "standard",
    },
    "obstetrique": {
        "label": "Kit obstetrique",
        "poids_kg": 1.2,
        "urgence_defaut": "haute",
    },
}

# --- Niveaux d'urgence ---
URGENCY_LEVELS: dict[str, dict] = {
    "critique": {"label": "Critique", "color": "#e74c3c", "priority": 1},
    "haute": {"label": "Haute", "color": "#e67e22", "priority": 2},
    "standard": {"label": "Standard", "color": "#3498db", "priority": 3},
}

# --- Statuts commande ---
ORDER_STEPS: list[str] = ["preparation", "en_vol", "livree"]

# --- Couleurs hubs (MASA vs Zipline) ---
HUB_COLORS: dict[str, str] = {
    "Hauts_Flux": "#00D4AA",
    "Standard": "#00D4AA",
    "Proximite": "#00D4AA",
    "Zipline": "#FFB347",
}

# --- Couleurs operateurs ---
OPERATOR_COLORS: dict[str, str] = {
    "MASA": "#00D4AA",
    "Zipline": "#FFB347",
}

# --- Comptes demo (facilities reelles du CSV) ---
DEMO_ACCOUNTS: dict[str, dict] = {
    "admin": {
        "password": "admin2026",
        "facility_name": "Administration MASA",
        "lat": 7.9465,
        "lon": -1.0232,
        "type": "admin",
        "region": "Ghana",
        "scenario": "admin",
        "role": "admin",
    },
    "BAM-CL-001": {
        "password": "demo",
        "facility_name": "BAMVIM CLINIC",
        "lat": 9.3638,
        "lon": -0.8349,
        "type": "Clinic",
        "region": "",
        "scenario": "proche",
        "role": "user",
    },
    "ABO-CL-002": {
        "password": "demo",
        "facility_name": "Aboadze Clinic",
        "lat": 4.9733,
        "lon": -1.6500,
        "type": "Clinic",
        "region": "",
        "scenario": "proche",
        "role": "user",
    },
    "ANK-CH-003": {
        "password": "demo",
        "facility_name": "Ankaako CHPS Compound",
        "lat": 5.3892,
        "lon": -1.4549,
        "type": "Clinic",
        "region": "",
        "scenario": "proche",
        "role": "user",
    },
    "AKO-ZP-004": {
        "password": "demo",
        "facility_name": "Akome CHPs Compound",
        "lat": 6.8201,
        "lon": 0.4678,
        "type": "CHPS",
        "region": "",
        "scenario": "zipline",
        "role": "user",
    },
    "ANL-HC-005": {
        "password": "demo",
        "facility_name": "Anloga Avete Clinic",
        "lat": 5.7916,
        "lon": 0.8826,
        "type": "Clinic",
        "region": "",
        "scenario": "hors_couverture",
        "role": "user",
    },
}
