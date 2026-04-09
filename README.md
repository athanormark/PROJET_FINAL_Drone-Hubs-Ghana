[![JEDHA](https://img.shields.io/badge/JEDHA-Certification-blueviolet?style=flat)](#)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=fff)](#)
[![scikit--learn](https://img.shields.io/badge/scikit--learn-1.7.2-F7931E?style=flat&logo=scikitlearn&logoColor=fff)](#)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.46.0-FF4B4B?style=flat&logo=streamlit&logoColor=fff)](#)
[![Folium](https://img.shields.io/badge/Folium-0.19.4-77B829?style=flat)](#)
[![Plotly](https://img.shields.io/badge/Plotly-5.24.1-3F4F75?style=flat&logo=plotly&logoColor=fff)](#)
[![GeoPandas](https://img.shields.io/badge/GeoPandas-1.0.1-139C5A?style=flat)](#)

# Optimisation de Hubs de Drones Médicaux au Ghana

Projet de groupe — certification Jedha Bootcamp (BLOC 6 — Direction de projets de gestion de données)
Promotion DSFS-FT-39-2026

**Application déployée** : [projetfinaldrone-apps-ghana.streamlit.app](https://projetfinaldrone-apps-ghana.streamlit.app/)

---

## À propos

Les zones rurales du Ghana (44 % de la population, ~14,5 millions de personnes) souffrent d'un accès limité aux soins d'urgence. Les routes sont dégradées, les délais d'acheminement de fournitures vitales atteignent plusieurs heures. La mortalité maternelle reste élevée (263 pour 100 000 naissances vivantes, OMS).

Ce projet utilise le Machine Learning non supervisé (K-Means) pour déterminer où placer des hubs de drones médicaux capables de livrer sang, vaccins et antivenins dans un rayon de 80 km (autonomie drone 160 km aller-retour, distances calculées par formule de Haversine).

Trois approches de modélisation ont été comparées. Le réseau hybride retenu couvre 98 % des établissements de santé du pays.

---

## Équipe

| Membre | Contribution |
|--------|-------------|
| Alicia MARZOUK | Analyse exploratoire (villages et facilities) |
| Mathieu LE FAOU | Modélisation hybride VTOL (micro-hubs 30 km) |
| Semia BEN AMARA | Extension du réseau Zipline existant |
| Athanor SAVOUILLAN | Modélisation from scratch, ETL, application Streamlit |

---

## Contexte

Le marché de la livraison médicale par drone est évalué à 294 M$ en 2024, projeté à 2,5 Mds$ d'ici 2034 (CAGR 24,1 %). L'Afrique subsaharienne affiche une croissance supérieure à 40 %.

Au Ghana, l'opérateur dominant Zipline (valorisé 7,6 Mds$) facture ~88 000 $/mois par centre au gouvernement, qui a accumulé ~15 M$ d'impayés en 2025. Les 6 hubs Zipline existants ne couvrent que 73 % des établissements de santé dans un rayon de 80 km.

Pour l'analyse concurrentielle complète, voir le [Cadrage Business](docs/cadrage_business.md).

---

## Données

### Sources

| Source | Type | Éléments |
|--------|------|----------|
| WorldPop 2020 + GeoNames/OSM | CSV | 8 905 villages avec coordonnées et population |
| OpenStreetMap (Overpass API) | Requête temps réel | Hôpitaux, cliniques, pharmacies, CHPS |
| HDX Healthsites (CSV) | Export statique | Centres référencés par healthsites.io |
| HDX HOT (GeoJSON) | Export statique | Facilities cartographiées par HOT/OSM |

Les trois sources de facilities sont croisées par `osm_id` puis par proximité (seuil 200 m Haversine), avec normalisation des types et score de confiance.

### Datasets produits

| Fichier | Lignes | Description |
|---------|--------|-------------|
| `data/Final Group/ghana_villages_eda_final.csv` | 8 905 | Villages nettoyés, facility la plus proche |
| `data/Final Group/ghana_health_eda_final.csv` | 2 463 | Facilities construites par ETL multi-source |
| `data/processed/hubs_plan_final.csv` | 31 | Hubs optimisés (25 MASA + 6 Zipline) |
| `data/processed/villages_assigned_final.csv` | 8 905 | Villages assignés aux hubs |

### Chiffres clés du dataset

| Métrique | Valeur |
|----------|--------|
| Villages total | 8 905 |
| Établissements de santé | 2 463 |
| Distance médiane village → facility | 7,07 km |
| Distance maximale | 64,71 km |
| Villages à plus de 30 km | 313 (3,5 %) |
| Population isolée (> 30 km) | 423 015 |
| Couverture Zipline actuelle (80 km) | 73 % (1 798 / 2 463) |

---

## Résultats

### Comparaison des 3 approches

| Approche | Auteur | Rayon | Hubs | Couverture | CAPEX | TCO 5 ans |
|----------|--------|-------|------|------------|-------|-----------|
| From scratch (K-Means Standard) | Athanor | 80 km | 11 Standard | 91,9 % | 22 M$ | 39,1 M$ |
| Extension Zipline (K=5 complément) | Semia | 80 km | 5 Standard + 6 Zipline | 93,3 % | 10 M$ | 19 M$ |
| Micro-hubs VTOL (MCLP) | Mathieu | 30 km | 25 micro + 6 Zipline | 98,1 % | 1,25 M$ | 4,4 M$ |

### Réseau retenu (hybride VTOL)

| Indicateur | Avant (Zipline seul) | Après (hybride) |
|------------|---------------------|-----------------|
| Facilities couvertes | 1 798 (73 %) | 2 417 (98,1 %) |
| CAPEX total | Non chiffré (contrat Zipline) | 1,25 M$ (25 micro-hubs) |
| OPEX annuel | ~6,3 M$/an (88 K$/centre) | 632 K$/an |
| TCO 5 ans | ~31,5 M$ | 4,4 M$ |

### Métriques ML

| Indicateur | Valeur |
|------------|--------|
| Silhouette Score (K=11, from scratch) | 0,51 |
| Couverture from scratch (K=11) | 91,9 % |
| Couverture hybride retenu (25+6 hubs) | 98,1 % |
| Couverture Zipline avant projet | 73,0 % |

---

## Recommandations

- Déployer le scénario hybride (25 micro-hubs VTOL + 6 hubs Zipline existants) pour maximiser la couverture à moindre coût.
- Prioriser les zones Nord et Volta où la couverture Zipline actuelle est la plus faible (< 40 %).
- Déploiement par phases : 8 micro-hubs prioritaires (zones critiques), puis 17 restants.
- Partenariat opérateur : DHG fournit l'optimisation, un opérateur local ou international déploie la flotte.

---

## Limites

- K-Means euclidien suppose des clusters convexes. La géographie réelle (cours d'eau, relief) n'est pas modélisée.
- Le rayon de 80 km est uniforme et ne tient pas compte des conditions saisonnières (saison des pluies juin-septembre).
- Les données de population sont estimées (WorldPop 2020), pas issues d'un recensement récent.
- Pas de pondération par fréquence réelle d'urgences médicales (données indisponibles).
- Le cycle de vente B2G (gouvernement) est long et incertain.

---

## Conformité RGPD

- Données utilisées : exclusivement géographiques et publiques (OpenStreetMap, WorldPop, HDX). Aucune donnée personnelle.
- Application : le dashboard ne collecte aucune donnée utilisateur, ne place aucun cookie et ne nécessite aucune inscription.
- Sources ouvertes : toutes les données proviennent de bases en licence ouverte (ODbL pour OSM, CC-BY pour HDX).

---

## Stack technique

| Composant | Technologie | Version |
|-----------|-------------|---------|
| Langage | Python | 3.11 |
| Manipulation | pandas | 2.3.2 |
| ML | scikit-learn | 1.7.2 |
| Géospatial | geopandas | 1.0.1 |
| Cartographie | folium | 0.19.4 |
| Dashboard | streamlit | 1.46.0 |
| Visualisations | plotly | 5.24.1 |
| API Météo | openmeteo-requests | 1.3.0 |

---

## Installation

### Prérequis

- Python 3.11
- Conda (recommandé) ou pip

### Mise en place

```bash
git clone https://github.com/athanormark/PROJET_FINAL_Drone-Hubs-Ghana.git
cd PROJET_FINAL_Drone-Hubs-Ghana
conda create -n drone-ghana python=3.11 -y
conda activate drone-ghana
pip install -r requirements.txt
```

### Lancer l'application

```bash
streamlit run app/main.py
```

### Reproduire les résultats

- EDA : exécuter `notebooks/01_eda.ipynb`
- Modélisation : exécuter `notebooks/02_modeling.ipynb`
- Contributions individuelles : voir `notebooks/contributions_modeling/`

---

## Structure du projet

```
PROJET_FINAL_Drone-Hubs-Ghana/
├── README.md
├── requirements.txt
├── .env.example
├── .streamlit/config.toml
├── docs/
│   └── cadrage_business.md
├── data/
│   ├── raw/                              # Données brutes (non versionné)
│   ├── Final Group/
│   │   ├── ghana_villages_eda_final.csv    # 8 905 villages
│   │   └── ghana_health_eda_final.csv      # 2 463 facilities
│   └── processed/
│       ├── hubs_plan_final.csv             # 31 hubs (25 MASA + 6 Zipline)
│       ├── villages_assigned_final.csv     # Villages assignés
│       └── scenarios_comparison.csv        # Comparaison 3 scénarios
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_modeling.ipynb
│   ├── contributions_EDA/
│   └── contributions_modeling/
│       ├── athanor_from_scratch.ipynb
│       ├── mathieu_clustering_hybride.ipynb
│       └── semia_extension_zipline.ipynb
├── src/
│   ├── etl.py
│   ├── haversine.py
│   ├── clustering.py
│   ├── scoring.py
│   └── dispatch.py
└── app/
    ├── main.py
    ├── config.py, auth.py, theme.py, data_loader.py
    ├── assets/masa_logo.png
    └── components/
        ├── map_view.py
        ├── analytics.py
        ├── order_form.py
        └── tracking.py
```

---

## Auteur

Équipe MASA — Jedha Bootcamp, promotion DSFS-FT-39-2026

| Membre | GitHub |
|--------|--------|
| Athanor SAVOUILLAN (lead technique) | [@athanormark](https://github.com/athanormark) |
| Alicia MARZOUK | — |
| Mathieu LE FAOU | — |
| Semia BEN AMARA | — |
