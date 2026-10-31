"""Calendar schema contracts, union responses, and partial-update semantics."""

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from luma_mcp.models import calendars as models

SNAPSHOT = json.loads(
    (Path(__file__).parents[2] / "schemas/calendars.json").read_text()
)


@pytest.mark.parametrize("part", ["request", "response"])
def test_fixtures_match_documented_schema(calendar_case, part):
    suffix = "Request" if part == "request" else "Response"
    schema = {
        "$ref": f"#/components/schemas/{calendar_case['model']}{suffix}",
        "components": SNAPSHOT["components"],
    }
    Draft202012Validator(schema).validate(calendar_case[part])


def test_calendar_update_preserves_null_empty_string_and_false():
    request = models.UpdateCalendarRequest(
        calendar_id="cal-meetup",
        website=None,
        twitter_handle="",
        event_defaults={"show_guest_list": False},
    )
    assert request.model_dump(mode="json", exclude_unset=True) == {
        "calendar_id": "cal-meetup",
        "website": None,
        "twitter_handle": "",
        "event_defaults": {"show_guest_list": False},
    }


def test_calendar_update_rejects_null_name():
    with pytest.raises(ValidationError):
        models.UpdateCalendarRequest(calendar_id="cal-meetup", name=None)


@pytest.mark.parametrize("emails", [[], ["admin@example.test"] * 21])
def test_add_admins_enforces_documented_batch_size(emails):
    with pytest.raises(ValidationError):
        models.AddCalendarAdminsRequest(emails=emails)


def test_event_tag_requires_nonempty_event_ids():
    with pytest.raises(ValidationError):
        models.ApplyEventTagRequest(tag="workshop", event_ids=[])


@pytest.mark.parametrize("platform", ["external", "unknown"])
def test_external_event_requires_details_and_known_platform(platform):
    with pytest.raises(ValidationError):
        models.AddEventRequest.model_validate(
            {"platform": platform, "event_id": "evt-meetup"}
        )


def test_discount_percentage_cannot_exceed_one_hundred():
    with pytest.raises(ValidationError):
        models.CreateCalendarCouponRequest.model_validate(
            {
                "code": "TOO-MUCH",
                "discount": {"discount_type": "percent", "percent_off": 101},
            }
        )


def test_listing_models_preserve_all_event_variants():
    cases = json.loads(
        (Path(__file__).parents[1] / "fixtures/calendars.json").read_text()
    )
    raw = next(case["response"] for case in cases if case["scenario"] == "list_events")
    result = models.ListEventsResponse.model_validate(raw).model_dump(
        mode="json", exclude_unset=True
    )
    assert [entry["platform"] for entry in result["entries"]] == [
        "luma",
        "luma",
        "external",
    ]
    assert result["entries"][0]["access"] == "manage"
    assert result["entries"][1]["access"] == "view"
    assert "meeting_url" not in result["entries"][1]
    assert result == raw


def test_fixtures_cover_every_calendar_endpoint():
    cases = json.loads(
        (Path(__file__).parents[1] / "fixtures/calendars.json").read_text()
    )
    documented = {
        (method.upper(), path)
        for path, methods in SNAPSHOT["paths"].items()
        for method in methods
    }
    assert {(case["method"], case["path"]) for case in cases} == documented
    assert len(documented) == 29
