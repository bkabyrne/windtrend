from datetime import date
import pytest
from pydantic import ValidationError

from windtrend.schema import TrendRequest

def test_trend_request_parses_string_dates():
    req = TrendRequest.model_validate({
        "lat": 48.43,
        "lon": -123.37,
        "start_date": "2015-01-01",
        "end_date": "2025-01-01",
    })
    assert req.start_date == date(2015, 1, 1)
    assert req.end_date == date(2025, 1, 1)

def test_min_10_years_enforced():
    with pytest.raises(ValidationError):
        TrendRequest.model_validate({
            "lat": 48.43,
            "lon": -123.37,
            "start_date": "2015-01-01",
            "end_date": "2024-12-31",  # < 10y
        })

def test_max_30_years_enforced():
    with pytest.raises(ValidationError):
        TrendRequest.model_validate({
            "lat": 48.43,
            "lon": -123.37,
            "start_date": "2010-01-01",
            "end_date": "2040-01-02",  # > 30y
        })

def test_lat_lon_bounds():
    with pytest.raises(ValidationError):
        TrendRequest.model_validate({"lat": 91, "lon": 0, "start_date": "2015-01-01", "end_date": "2025-01-01"})
    with pytest.raises(ValidationError):
        TrendRequest.model_validate({"lat": 0, "lon": 181, "start_date": "2015-01-01", "end_date": "2025-01-01"})
