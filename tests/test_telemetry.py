"""Telemetry describes operations without recording credentials or payloads."""

import asyncio

import httpx
from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from pydantic import BaseModel, SecretStr

from luma_mcp import telemetry
from luma_mcp.client import base


class Payload(BaseModel):
    email: str


def test_upstream_span_omits_secrets_and_payload(monkeypatch):
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    monkeypatch.setattr(base, "tracer", provider.get_tracer("test"))
    asyncio.run(traced_request())
    spans = exporter.get_finished_spans()
    assert len(spans) == 1 and spans[0].name == "luma GET /v1/events/get"
    exported = str([(span.attributes, span.events) for span in spans])
    assert "private-key" not in exported and "guest@example.test" not in exported
    provider.shutdown()


async def traced_request():
    transport = httpx.MockTransport(
        lambda request: httpx.Response(200, json={"email": "guest@example.test"})
    )
    async with httpx.AsyncClient(transport=transport) as http:
        client = base.LumaClient(SecretStr("private-key"), http)
        await client.request(
            "GET", "/v1/events/get", Payload(email="guest@example.test"), Payload
        )


def test_no_export_without_configured_endpoint(monkeypatch):
    for name in [
        "OTEL_EXPORTER_OTLP_ENDPOINT",
        "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT",
        "OTEL_EXPORTER_OTLP_METRICS_ENDPOINT",
    ]:
        monkeypatch.delenv(name, raising=False)
    assert not telemetry.configured("TRACES")
    assert not telemetry.configured("METRICS")


def test_http_telemetry_redacts_headers_and_query():
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    asyncio.run(traced_http_request(provider))
    exported = str(
        [(span.attributes, span.events) for span in exporter.get_finished_spans()]
    )
    assert "private-key" not in exported
    assert "REDACTED" in exported
    provider.shutdown()


async def traced_http_request(provider):
    async def app(scope, receive, send):
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"ok"})

    instrumented = OpenTelemetryMiddleware(
        app,
        tracer_provider=provider,
        server_request_hook=telemetry.redact_request_url,
        http_capture_headers_server_request=[".*"],
        http_capture_headers_sanitize_fields=[".*"],
    )
    async with httpx.AsyncClient(transport=httpx.ASGITransport(instrumented)) as http:
        await http.get(
            "http://localhost:8000/mcp?secret=private-key",
            headers={"X-Luma-API-Key": "private-key"},
        )
