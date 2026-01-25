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
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "hourly": "wind_speed_10m",
    }

    resp = requests.get(ARCHIVE_API, params=params, timeout=(3.0, 20.0))
    resp.raise_for_status()
    payload: Dict[str, Any] = resp.json()

    hourly = payload.get("hourly")
    if not isinstance(hourly, dict):
        raise ValueError("Missing or invalid 'hourly' in Open-Meteo response")

    times = hourly.get("time")
    wind_raw = hourly.get("wind_speed_10m")

    if times is None or wind_raw is None:
        raise ValueError("Missing 'hourly.time' or 'hourly.wind_speed_10m' in Open-Meteo response")
    if len(times) != len(wind_raw):
        raise ValueError("Open-Meteo response length mismatch between time and wind_speed_10m")

    wind: List[Optional[float]] = [None if v is None else float(v) for v in wind_raw]
    return list(times), wind
