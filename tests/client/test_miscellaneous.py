"""Check documented HTTP contracts across every Miscellaneous endpoint."""

import asyncio
import json
from pathlib import Path

import httpx
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from pydantic import SecretStr

from luma_mcp.client import base
from luma_mcp.client.miscellaneous import MiscellaneousClient
from luma_mcp.models import miscellaneous as models


def test_documented_request_and_response(miscellaneous_case):
    asyncio.run(call_endpoint(miscellaneous_case))


async def call_endpoint(case):
    def respond(request):
        assert request.method == case["method"]
        assert request.url.host == "public-api.luma.com"
        assert request.url.path == case["path"]
        assert request.headers["x-luma-api-key"] == "synthetic-key"
        assert_payload(request, case)
        return httpx.Response(200, json=case["response"])

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as http:
        client = MiscellaneousClient(SecretStr("synthetic-key"), http)
        payload = getattr(models, case["model"] + "Request").model_validate(
            case["request"]
        )
        result = await getattr(client, case["operation"])(payload)
    assert result.model_dump(mode="json", exclude_unset=True) == case["response"]


def assert_payload(request, case):
    if case["method"] == "GET":
        expected = [
            (key, str(item))
            for key, value in case["request"].items()
            if value is not None
            for item in (value if isinstance(value, list) else [value])
        ]
        assert sorted(request.url.params.multi_items()) == sorted(expected)
        assert not request.content
    else:
        assert json.loads(request.content) == case["request"]


def test_presigned_url_is_not_recorded_in_spans(monkeypatch):
    cases = json.loads(
        (Path(__file__).parents[1] / "fixtures/miscellaneous.json").read_text()
    )
    case = next(case for case in cases if case["scenario"] == "create_upload_url_png")
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    monkeypatch.setattr(base, "tracer", provider.get_tracer("upload-test"))
    asyncio.run(call_endpoint(case))
    spans = exporter.get_finished_spans()
    assert spans and spans[0].name == "luma POST /v1/images/create-upload-url"
    exported = str([(span.attributes, span.events) for span in spans])
    assert "synthetic-upload-signature" not in exported
    assert "synthetic-key" not in exported
    provider.shutdown()
