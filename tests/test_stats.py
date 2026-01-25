from windtrend.stats import annual_means, fit_trend
from windtrend.schema import AnnualMean

def test_annual_means_groups_and_drops_none():
    times = ["2015-01-01T00:00", "2015-01-01T01:00", "2016-01-01T00:00"]
    wind = [1.0, None, 3.0]
    out = annual_means(times, wind)
    assert [(a.year, a.mean_wind_speed_10m) for a in out] == [(2015, 1.0), (2016, 3.0)]

def test_fit_trend_requires_3_years():
    annual = [AnnualMean(year=2015, mean_wind_speed_10m=1.0),
              AnnualMean(year=2016, mean_wind_speed_10m=2.0)]
    assert fit_trend(annual) is None

def test_fit_trend_linear_slope():
    annual = [AnnualMean(year=2015, mean_wind_speed_10m=1.0),
              AnnualMean(year=2016, mean_wind_speed_10m=2.0),
              AnnualMean(year=2017, mean_wind_speed_10m=3.0)]
    tr = fit_trend(annual)
    assert tr is not None
    assert abs(tr.slope_ms_per_year - 1.0) < 1e-12
