import pytest
from datetime import date

from windtrend.fetch import fetch_hourly_wind_speed_10m

class FakeResp:
    def __init__(self, payload):
        self._payload = payload
    def raise_for_status(self):
        return None
    def json(self):
        return self._payload

def test_fetch_missing_hourly(monkeypatch):
    def fake_get(*args, **kwargs):
        return FakeResp({"not_hourly": {}})

    monkeypatch.setattr("windtrend.fetch.requests.get", fake_get)

    with pytest.raises(ValueError, match="hourly"):
        fetch_hourly_wind_speed_10m(0, 0, date(2015,1,1), date(2015,1,2))

def test_fetch_length_mismatch(monkeypatch):
    def fake_get(*args, **kwargs):
        return FakeResp({
            "hourly": {"time": ["2015-01-01T00:00"], "wind_speed_10m": [1.0, 2.0]}
        })

    monkeypatch.setattr("windtrend.fetch.requests.get", fake_get)

    with pytest.raises(ValueError, match="length mismatch"):
        fetch_hourly_wind_speed_10m(0, 0, date(2015,1,1), date(2015,1,2))
