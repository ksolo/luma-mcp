"""Webhook subscription contracts and documented request constraints."""

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from luma_mcp.models import webhooks as models

SNAPSHOT = json.loads((Path(__file__).parents[2] / "schemas/webhooks.json").read_text())


@pytest.mark.parametrize("part", ["request", "response"])
def test_fixtures_match_documented_schema(webhook_case, part):
    suffix = "Request" if part == "request" else "Response"
    Draft202012Validator(
        {
            "$ref": f"#/components/schemas/{webhook_case['model']}{suffix}",
            "components": SNAPSHOT["components"],
        }
    ).validate(webhook_case[part])


@pytest.mark.parametrize(
    "data",
    [
        {},
        {"url": "https://example.test/hook"},
        {"url": "https://example.test/hook", "event_types": []},
        {"url": "ftp://example.test/hook", "event_types": ["event.created"]},
        {"url": "https://example.test/hook", "event_types": ["unknown.event"]},
    ],
)
def test_create_rejects_missing_or_invalid_fields(data):
    with pytest.raises(ValidationError):
        models.CreateWebhookRequest.model_validate(data)


@pytest.mark.parametrize(
    "data",
    [
        {"id": "hook-meetup", "event_types": []},
        {"id": "hook-meetup", "status": "disabled"},
        {"id": "hook-meetup", "status": None},
    ],
)
def test_update_rejects_invalid_values(data):
    with pytest.raises(ValidationError):
        models.UpdateWebhookRequest.model_validate(data)


def test_partial_update_does_not_invent_event_types():
    request = models.UpdateWebhookRequest(id="hook-meetup", status="paused")
    assert request.model_dump(mode="json", exclude_unset=True) == {
        "id": "hook-meetup",
        "status": "paused",
    }


@pytest.mark.parametrize(
    "model",
    [
        models.GetWebhookRequest,
        models.UpdateWebhookRequest,
        models.DeleteWebhookRequest,
    ],
)
def test_identifier_is_required(model):
    with pytest.raises(ValidationError):
        model.model_validate({})


def test_all_documented_event_types_are_supported():
    event_types = SNAPSHOT["components"]["schemas"]["CreateWebhookRequest"][
        "properties"
    ]["event_types"]["items"]["enum"]
    request = models.CreateWebhookRequest(
        url="https://example.test/hook", event_types=event_types
    )
    assert request.event_types == event_types


def test_fixtures_cover_all_webhook_endpoints():
    cases = json.loads(
        (Path(__file__).parents[1] / "fixtures/webhooks.json").read_text()
    )
    documented = {
        (method.upper(), path)
        for path, methods in SNAPSHOT["paths"].items()
        for method in methods
    }
    assert {(case["method"], case["path"]) for case in cases} == documented
    assert len(documented) == 5
