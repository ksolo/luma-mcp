"""Request-scoped Luma HTTP client with safe errors and bounded read retries."""

import asyncio
import time
from collections.abc import Awaitable, Callable

import httpx
from opentelemetry import metrics, trace
from pydantic import BaseModel, SecretStr, ValidationError

from luma_mcp.client.errors import LumaError
from luma_mcp.client.retries import backoff, retry_after, retryable

BASE_URL = "https://public-api.luma.com"
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)
requests = meter.create_counter("luma.requests")
latency = meter.create_histogram("luma.request.duration", unit="s")


class LumaClient:
    def __init__(
        self,
        api_key: SecretStr,
        http: httpx.AsyncClient,
        *,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
        retry_budget: float = 5,
        max_attempts: int = 3,
    ) -> None:
        self.api_key, self.http, self.sleep = api_key, http, sleep
        self.retry_budget, self.max_attempts = retry_budget, max_attempts

    async def request[T: BaseModel](
        self,
        method: str,
        path: str,
        payload: BaseModel,
        response_model: type[T],
    ) -> T:
        with tracer.start_as_current_span(
            f"luma {method} {path}", record_exception=False
        ):
            response = await self.within_budget(method, path, payload)
            return validate_response(response, response_model)

    async def within_budget(
        self, method: str, path: str, payload: BaseModel
    ) -> httpx.Response:
        try:
            async with asyncio.timeout(self.retry_budget):
                return await self.send_with_retries(method, path, payload)
        except TimeoutError:
            raise LumaError(
                "request_timeout", outcome_unknown=method != "GET"
            ) from None

    async def send_with_retries(
        self,
        method: str,
        path: str,
        payload: BaseModel,
    ) -> httpx.Response:
        deadline = time.monotonic() + self.retry_budget
        for attempt in range(self.max_attempts):
            try:
                response = await self.attempt(method, path, payload, deadline)
            except LumaError:
                await self.retry_transport(method, attempt, deadline)
                continue
            if response.is_success:
                return response
            await self.retry_or_raise(method, response, attempt, deadline)
        raise LumaError("retry_exhausted")

    async def attempt(
        self, method: str, path: str, payload: BaseModel, deadline: float
    ) -> httpx.Response:
        started = time.monotonic()
        try:
            response = await self.http.request(
                method,
                BASE_URL + path,
                timeout=max(0.001, deadline - started),
                **self.options(method, payload),
            )
        except httpx.TransportError:
            record_response(method, path, 0, time.monotonic() - started)
            raise LumaError(
                "transport_error", outcome_unknown=method != "GET"
            ) from None
        record_response(method, path, response.status_code, time.monotonic() - started)
        return response

    def options(self, method: str, payload: BaseModel) -> dict:
        data = payload.model_dump(mode="json", by_alias=True, exclude_unset=True)
        return {
            "headers": {"x-luma-api-key": self.api_key.get_secret_value()},
            "params" if method == "GET" else "json": (
                {
                    key: query_value(value)
                    for key, value in data.items()
                    if value is not None
                }
                if method == "GET"
                else data
            ),
        }

    async def retry_transport(self, method: str, attempt: int, deadline: float) -> None:
        wait = backoff(attempt)
        if (
            method != "GET"
            or attempt + 1 >= self.max_attempts
            or time.monotonic() + wait > deadline
        ):
            raise LumaError(
                "transport_error", outcome_unknown=method != "GET"
            ) from None
        await self.sleep(wait)

    async def retry_or_raise(
        self,
        method: str,
        response: httpx.Response,
        attempt: int,
        deadline: float,
    ) -> None:
        delay = retry_after(response)
        wait = delay if delay is not None else backoff(attempt)
        if (
            not retryable(method, response.status_code)
            or attempt + 1 >= self.max_attempts
        ):
            raise response_error(response, method, delay)
        if time.monotonic() + wait > deadline:
            raise response_error(response, method, delay)
        await self.sleep(wait)


def validate_response[T: BaseModel](response: httpx.Response, model: type[T]) -> T:
    try:
        return model.model_validate_json(response.content)
    except ValidationError:
        raise LumaError(
            "invalid_upstream_response", status=response.status_code
        ) from None


def query_value(value):
    return int(value) if isinstance(value, float) and value.is_integer() else value


def response_error(
    response: httpx.Response, method: str, delay: float | None
) -> LumaError:
    return LumaError(
        {
            401: "invalid_api_key",
            403: "forbidden",
            404: "not_found",
            429: "rate_limited",
        }.get(response.status_code, "upstream_error"),
        status=response.status_code,
        retry_after=delay,
        outcome_unknown=method != "GET" and response.status_code >= 500,
    )


def record_response(method: str, path: str, status: int, duration: float) -> None:
    attributes = {
        "http.request.method": method,
        "http.route": path,
        "http.response.status_code": status,
    }
    requests.add(1, attributes)
    latency.record(duration, attributes)
    trace.get_current_span().set_attributes(attributes)
