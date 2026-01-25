# src/windtrend/handler.py
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
from pydantic import ValidationError

from windtrend.core import run
from windtrend.schema import TrendRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@dataclass(frozen=True)
class ErrorPayload:
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


def _map_exception(exc: Exception) -> ErrorPayload:
    # Input validation problems (includes ValueError from your model validators)
    if isinstance(exc, ValidationError):
        return ErrorPayload(
            code="INVALID_REQUEST",
            message="Request validation failed.",
            details={"errors": exc.errors()},
        )

    # Upstream request timed out
    if isinstance(exc, requests.Timeout):
        return ErrorPayload(
            code="UPSTREAM_TIMEOUT",
            message="Upstream weather service timed out.",
        )

    # Upstream returned non-2xx
    if isinstance(exc, requests.HTTPError):
        status = getattr(exc.response, "status_code", None)

        if status == 429:
            return ErrorPayload(
                code="UPSTREAM_RATE_LIMIT",
                message="Upstream weather service rate-limited the request. Try again later.",
                details={"status_code": status},
            )

        if status is not None and 500 <= status <= 599:
            return ErrorPayload(
                code="UPSTREAM_UNAVAILABLE",
                message="Upstream weather service returned an error. Try again later.",
                details={"status_code": status},
            )

        return ErrorPayload(
            code="UPSTREAM_BAD_RESPONSE",
            message="Upstream weather service rejected the request.",
            details={"status_code": status},
        )

    # Response schema drift / unexpected types / JSON parse issues
    if isinstance(exc, (KeyError, ValueError, TypeError)):
        return ErrorPayload(
            code="UPSTREAM_PARSE_ERROR",
            message="Failed to parse upstream weather service response.",
        )

    # Everything else is a bug
    return ErrorPayload(
        code="INTERNAL_ERROR",
        message="Unexpected internal error.",
    )


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Direct invocation contract:
      input: dict with lat/lon/start_date/end_date
      output: JSON-serializable dict
    """
    try:
        req = TrendRequest.model_validate(event)
        result = run(req)
        return {"ok": True, "result": result.model_dump(mode="json")}

    except Exception as exc:
        err = _map_exception(exc)

        logger.warning(
            "request_failed",
            extra={
                "error_code": err.code,
                "lat": event.get("lat"),
                "lon": event.get("lon"),
                "start_date": event.get("start_date"),
                "end_date": event.get("end_date"),
            },
        )

        out: Dict[str, Any] = {
            "ok": False,
            "error": {"code": err.code, "message": err.message},
        }
        if err.details:
            out["error"]["details"] = err.details
        return out
