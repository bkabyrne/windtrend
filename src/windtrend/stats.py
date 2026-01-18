# src/windtrend/stats.py
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import numpy as np

from .schema import AnnualMean, TrendResult


def annual_means(times: List[str], wind: List[Optional[float]]) -> List[AnnualMean]:
    """
    Aggregate hourly wind to annual means by:
      - dropping None values
      - grouping by year parsed from time string "YYYY-..."
    """
    by_year: Dict[int, List[float]] = {}

    for t, v in zip(times, wind, strict=True):
        if v is None:
            continue
        year = int(t[:4])
        by_year.setdefault(year, []).append(float(v))

    out: List[AnnualMean] = []
    for year in sorted(by_year):
        vals = np.array(by_year[year], dtype=float)
        out.append(AnnualMean(year=year, mean_wind_speed_10m=float(vals.mean())))
    return out


def fit_trend(annual: List[AnnualMean]) -> Optional[TrendResult]:
    """
    OLS fit of mean_wind_speed_10m vs year, using annual means.
    Returns slope + 95% CI (iid residual assumption).
    """
    n = len(annual)
    if n < 3:
        return None

    x = np.array([a.year for a in annual], dtype=float)
    y = np.array([a.mean_wind_speed_10m for a in annual], dtype=float)

    x_mean = float(x.mean())
    y_mean = float(y.mean())

    Sxx = float(np.sum((x - x_mean) ** 2))
    if Sxx == 0.0:
        return None

    slope = float(np.sum((x - x_mean) * (y - y_mean)) / Sxx)
    intercept = float(y_mean - slope * x_mean)

    y_hat = intercept + slope * x
    resid = y - y_hat
    s2 = float(np.sum(resid**2) / (n - 2))
    se_slope = float(np.sqrt(s2 / Sxx))

    ci_low = slope - 1.96 * se_slope
    ci_high = slope + 1.96 * se_slope

    return TrendResult(
        slope_ms_per_year=slope,
        intercept_ms=intercept,
        slope_ci95_low=ci_low,
        slope_ci95_high=ci_high,
        n_years=n,
    )
