"""Scoring et calcul de temps de vol pour livraisons drone."""

PRIORITY_WEIGHTS: dict[str, float] = {
    "critique": 10.0,
    "haute": 5.0,
    "standard": 2.0,
}

PRODUCTS_URGENCY: dict[str, str] = {
    "sang": "critique",
    "vaccins": "haute",
    "antivenins": "critique",
    "paludisme": "haute",
    "douleur": "standard",
    "toux": "standard",
    "parasites": "standard",
    "nutrition": "standard",
    "obstetrique": "haute",
}


def flight_time_min(
    distance_km: float,
    speed_kmh: float = 110.0,
    prep_min: float = 5.0,
) -> float:
    """Temps total en minutes : preparation au sol + vol aller."""
    return prep_min + (distance_km / speed_kmh) * 60


def urgency_score(
    product_key: str,
    distance_km: float,
    population: float,
) -> float:
    """Score de priorite combine (plus eleve = plus prioritaire).

    Composantes :
    - poids d'urgence du produit (critique > haute > standard)
    - facteur distance (les facilities eloignees ont moins d'alternatives)
    - facteur population desservie (log-scale pour limiter l'ecart)
    """
    import math

    urgency = PRODUCTS_URGENCY.get(product_key, "standard")
    w_urgency = PRIORITY_WEIGHTS[urgency]

    dist_factor = min(distance_km / 80.0, 1.0)

    pop_factor = math.log10(max(population, 10))

    return w_urgency * (1 + dist_factor) * pop_factor
