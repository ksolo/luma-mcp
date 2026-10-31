"""Validate event input constraints and partial-update semantics."""

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from luma_mcp.models import events as models

SNAPSHOT = json.loads((Path(__file__).parents[2] / "schemas/events.json").read_text())


@pytest.mark.parametrize("part", ["request", "response"])
def test_fixtures_match_documented_schema(event_case, part):
    suffix = "Request" if part == "request" else "Response"
    schema = {
        "$ref": f"#/components/schemas/{event_case['model']}{suffix}",
        "components": SNAPSHOT["components"],
    }
    Draft202012Validator(schema).validate(event_case[part])


@pytest.mark.parametrize(
    "data",
    [
        {},
        {"name": "Meetup", "start_at": "invalid", "timezone": "America/Chicago"},
    ],
)
def test_create_event_requires_valid_fields(data):
    with pytest.raises(ValidationError):
        models.CreateEventRequest.model_validate(data)


def test_guest_status_rejects_unknown_status():
    with pytest.raises(ValidationError):
        models.UpdateGuestStatusRequest(
            event_id="evt-demo", guest_id="gst-demo", status="going"
        )


def test_cancel_requires_token():
    with pytest.raises(ValidationError):
        models.CancelEventRequest(event_id="evt-demo")


def test_partial_update_preserves_explicit_null():
    update = models.UpdateEventRequest(event_id="evt-demo", font=None)
    assert update.model_dump(mode="json", exclude_unset=True) == {
        "event_id": "evt-demo",
        "font": None,
    }


def test_coupon_code_length_is_enforced():
    with pytest.raises(ValidationError):
        models.CreateCouponRequest(event_id="evt-demo", code="X" * 21)


def test_optional_nonnullable_field_rejects_explicit_null():
    with pytest.raises(ValidationError):
        models.UpdateEventRequest(event_id="evt-demo", meeting_url=None)
