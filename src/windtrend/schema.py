# src/windtrend/schema.py
from __future__ import annotations

from datetime import date
from typing import List, Optional, Tuple

from pydantic import BaseModel


class TrendRequest(BaseModel):
    lat: float
    lon: float
    start_date: date
    end_date: date


class AnnualMean(BaseModel):
    year: int
    mean_wind_speed_10m: float


class TrendResult(BaseModel):
    slope_ms_per_year: float
    intercept_ms: float
    slope_ci95_low: float
    slope_ci95_high: float
    n_years: int


class TrendResponse(BaseModel):
    lat: float
    lon: float
    start_date: date
    end_date: date
    annual_means: List[AnnualMean]
    trend: Optional[TrendResult]
