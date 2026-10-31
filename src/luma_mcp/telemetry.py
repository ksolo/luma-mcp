"""Export traces and metrics through OTLP when an endpoint is configured."""

import atexit
import os
from functools import cache
from urllib.parse import urlsplit, urlunsplit

from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


@cache
def configure() -> None:
    resource = Resource.create(
        {"service.name": os.getenv("OTEL_SERVICE_NAME", "luma-mcp")}
    )
    if configured("TRACES"):
        configure_traces(resource)
    if configured("METRICS"):
        configure_metrics(resource)


def configured(signal: str) -> bool:
    return bool(
        os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
        or os.getenv(f"OTEL_EXPORTER_OTLP_{signal}_ENDPOINT")
    )


def configure_traces(resource: Resource) -> None:
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    trace.set_tracer_provider(provider)
    atexit.register(provider.shutdown)


def configure_metrics(resource: Resource) -> None:
    reader = PeriodicExportingMetricReader(OTLPMetricExporter())
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(provider)
    atexit.register(provider.shutdown)


def redact_request_url(span, scope) -> None:
    if not span.is_recording():
        return
    for attribute in ("http.url", "url.full"):
        value = span.attributes.get(attribute)
        if value:
            parts = urlsplit(value)
            span.set_attribute(
                attribute, urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
            )
    span.set_attribute("http.target", scope.get("path", "/mcp"))
    span.set_attribute("url.query", "")
