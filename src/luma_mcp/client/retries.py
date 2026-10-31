"""Bounded retry policy for safe Luma reads; writes are never replayed."""

import random
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime

import httpx


def retry_after(response: httpx.Response) -> float | None:
    value = response.headers.get("Retry-After")
    if value is None:
        return None
    try:
        return max(0, float(value))
    except ValueError:
        return date_delay(value)


def date_delay(value: str) -> float | None:
    try:
        return max(
            0, (parsedate_to_datetime(value) - datetime.now(UTC)).total_seconds()
        )
    except (ValueError, TypeError, OverflowError):
        return None


def backoff(attempt: int) -> float:
    return random.uniform(0, min(2**attempt, 4))


def retryable(method: str, status: int) -> bool:
    return method == "GET" and status in {429, 500, 502, 503, 504}
