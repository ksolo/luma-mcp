"""Exercise failures, retry boundaries, and write ambiguity without network calls."""

import asyncio
from unittest.mock import AsyncMock

import httpx
import pytest
from pydantic import BaseModel, SecretStr

from luma_mcp.client.base import LumaClient
from luma_mcp.client.errors import LumaError


class Payload(BaseModel):
    event_id: str = "evt-synthetic"


class Result(BaseModel):
    id: str


async def exchange(responses, method="GET", **kwargs):
    seen = []

    def respond(request):
        seen.append(request)
        item = responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as http:
        client = LumaClient(SecretStr("sensitive-key"), http, **kwargs)
        return await client.request(method, "/v1/events/get", Payload(), Result), seen


def test_rate_limit_honors_retry_after():
    sleep = AsyncMock()
    result, seen = asyncio.run(
        exchange(
            [
                httpx.Response(429, headers={"Retry-After": "0.25"}),
                httpx.Response(200, json={"id": "evt-synthetic"}),
            ],
            sleep=sleep,
        )
    )
    assert result.id == "evt-synthetic" and len(seen) == 2
    sleep.assert_awaited_once_with(0.25)


def test_long_rate_limit_returns_delay_without_waiting():
    sleep = AsyncMock()
    with pytest.raises(LumaError) as error:
        asyncio.run(
            exchange([httpx.Response(429, headers={"Retry-After": "60"})], sleep=sleep)
        )
    assert error.value.details["retry_after"] == 60
    sleep.assert_not_awaited()


@pytest.mark.parametrize("status", [400, 401, 403, 404, 422])
def test_permanent_errors_are_not_retried(status):
    sleep = AsyncMock()
    with pytest.raises(LumaError) as error:
        asyncio.run(
            exchange([httpx.Response(status, text="sensitive-key")], sleep=sleep)
        )
    assert error.value.details["status"] == status
    assert "sensitive-key" not in str(error.value.details)
    sleep.assert_not_awaited()


@pytest.mark.parametrize("status", [429, 500, 502, 503, 504])
def test_writes_are_never_retried(status):
    sleep = AsyncMock()
    with pytest.raises(LumaError) as error:
        asyncio.run(exchange([httpx.Response(status)], method="POST", sleep=sleep))
    assert error.value.details["outcome_unknown"] == (status >= 500)
    sleep.assert_not_awaited()


def test_read_transport_failure_is_retried(monkeypatch):
    monkeypatch.setattr("luma_mcp.client.base.backoff", lambda attempt: 0)
    result, seen = asyncio.run(
        exchange(
            [
                httpx.ReadTimeout("sensitive-key"),
                httpx.Response(200, json={"id": "evt-ok"}),
            ],
            sleep=AsyncMock(),
        )
    )
    assert result.id == "evt-ok" and len(seen) == 2


def test_write_timeout_reports_unknown_outcome():
    with pytest.raises(LumaError) as error:
        asyncio.run(exchange([httpx.ReadTimeout("sensitive-key")], method="POST"))
    assert error.value.details["outcome_unknown"] is True
    assert "sensitive-key" not in str(error.value)


def test_transient_reads_stop_at_attempt_limit(monkeypatch):
    monkeypatch.setattr("luma_mcp.client.base.backoff", lambda attempt: 0)
    responses = [httpx.Response(503) for _ in range(3)]
    with pytest.raises(LumaError):
        asyncio.run(exchange(responses, sleep=AsyncMock()))
    assert responses == []


@pytest.mark.parametrize("body", ['{"unexpected":true}', "not json"])
def test_invalid_response_is_sanitized(body):
    with pytest.raises(LumaError, match="invalid_upstream_response"):
        asyncio.run(exchange([httpx.Response(200, text=body)]))


def test_total_timeout_is_bounded():
    with pytest.raises(LumaError, match="request_timeout"):
        asyncio.run(slow_request())


async def slow_request():
    async def respond(request):
        await asyncio.sleep(1)
        return httpx.Response(200, json={"id": "late"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as http:
        client = LumaClient(SecretStr("key"), http, retry_budget=0.01)
        await client.request("GET", "/v1/events/get", Payload(), Result)
