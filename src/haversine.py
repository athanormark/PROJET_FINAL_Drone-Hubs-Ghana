import math
import numpy as np


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def haversine_matrix(
    lats1: np.ndarray, lons1: np.ndarray,
    lats2: np.ndarray, lons2: np.ndarray,
) -> np.ndarray:
    R = 6371.0
    lat1 = np.radians(lats1)
    lat2 = np.radians(lats2)
    dlat = lat2 - lat1
    dlon = np.radians(lons2) - np.radians(lons1)
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
