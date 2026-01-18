# src/windtrend/core.py
from __future__ import annotations

from .fetch import fetch_hourly_wind_speed_10m
from .schema import TrendRequest, TrendResponse
from .stats import annual_means, fit_trend


def run(req: TrendRequest) -> TrendResponse:
    times, wind = fetch_hourly_wind_speed_10m(
        lat=req.lat,
        lon=req.lon,
        start_date=req.start_date,
        end_date=req.end_date,
    )
    annual = annual_means(times, wind)
    trend = fit_trend(annual)

    return TrendResponse(
        lat=req.lat,
        lon=req.lon,
        start_date=req.start_date,
        end_date=req.end_date,
        annual_means=annual,
        trend=trend,
    )
