# src/windtrend/schema.py
from __future__ import annotations

from datetime import date
from typing import List, Optional, Tuple

from pydantic import BaseModel, model_validator, Field

from dateutil.relativedelta import relativedelta

class TrendRequest(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_constraints(self) -> "TrendRequest":
        if self.end_date < self.start_date:
            raise ValueError("end_date must be >= start_date")

        min_end = self.start_date + relativedelta(years=10)
        if self.end_date < min_end:
            raise ValueError("end_date must be at least 10 years after start_date")

        max_end = self.start_date + relativedelta(years=30)
        if self.end_date > max_end:
            raise ValueError("end_date cannot be more than 30 years after start_date")

        return self



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
