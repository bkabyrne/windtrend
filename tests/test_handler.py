import requests
from windtrend.handler import handler

def _valid_event():
    return {
        "lat": 48.43,
        "lon": -123.37,
        "start_date": "2015-01-01",
        "end_date": "2025-01-01",
    }

def test_handler_success(monkeypatch):
    # Fake 3 years of hourly-ish data (minimal)
    times = ["2015-01-01T00:00", "2016-01-01T00:00", "2017-01-01T00:00"]
    wind = [1.0, 2.0, 3.0]

    def fake_fetch(*args, **kwargs):
        return times, wind

    monkeypatch.setattr("windtrend.core.fetch_hourly_wind_speed_10m", fake_fetch)

    out = handler(_valid_event(), None)
    assert out["ok"] is True
    assert "result" in out
    assert "annual_means" in out["result"]
    assert "trend" in out["result"]
    assert out["result"]["trend"] is not None

def test_handler_invalid_request():
    event = {
        "lat": 48.43,
        "lon": -123.37,
        "start_date": "2015-01-01",
        "end_date": "2016-01-01",  # violates 10y rule
    }
    out = handler(event, None)
    assert out["ok"] is False
    assert out["error"]["code"] == "INVALID_REQUEST"

def test_handler_upstream_timeout(monkeypatch):
    def fake_fetch(*args, **kwargs):
        raise requests.Timeout()

    monkeypatch.setattr("windtrend.core.fetch_hourly_wind_speed_10m", fake_fetch)

    out = handler(_valid_event(), None)
    assert out["ok"] is False
    assert out["error"]["code"] == "UPSTREAM_TIMEOUT"

def test_handler_upstream_rate_limit(monkeypatch):
    resp = requests.Response()
    resp.status_code = 429
    err = requests.HTTPError(response=resp)

    def fake_fetch(*args, **kwargs):
        raise err

    monkeypatch.setattr("windtrend.core.fetch_hourly_wind_speed_10m", fake_fetch)

    out = handler(_valid_event(), None)
    assert out["ok"] is False
    assert out["error"]["code"] == "UPSTREAM_RATE_LIMIT"
