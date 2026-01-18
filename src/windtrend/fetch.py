# src/windtrend/fetch.py
from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Optional, Tuple

import requests

ARCHIVE_API = "https://archive-api.open-meteo.com/v1/archive"


def fetch_hourly_wind_speed_10m(
    lat: float,
    lon: float,
    start_date: date,
    end_date: date,
) -> Tuple[List[str], List[Optional[float]]]:
    """
    Fetch hourly wind_speed_10m from Open-Meteo Archive API.
    Returns:
      times: list of ISO strings like "2024-01-01T00:00"
      wind:  list of float or None, same length as times
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "hourly": "wind_speed_10m",
    }

    resp = requests.get(ARCHIVE_API, params=params)
    resp.raise_for_status()
    payload: Dict[str, Any] = resp.json()

    hourly = payload["hourly"]
    times = hourly["time"]
    wind_raw = hourly["wind_speed_10m"]

    wind: List[Optional[float]] = [None if v is None else float(v) for v in wind_raw]
    return list(times), wind
