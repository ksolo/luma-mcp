"""Organization API contracts, legacy fields, and required write parameters."""

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from luma_mcp.models import organizations as models

SNAPSHOT = json.loads(
    (Path(__file__).parents[2] / "schemas/organizations.json").read_text()
)


@pytest.mark.parametrize("part", ["request", "response"])
def test_fixtures_match_documented_schema(organization_case, part):
    suffix = "Request" if part == "request" else "Response"
    Draft202012Validator(
        {
            "$ref": f"#/components/schemas/{organization_case['model']}{suffix}",
            "components": SNAPSHOT["components"],
        }
    ).validate(organization_case[part])


@pytest.mark.parametrize(
    "data", [{}, {"name": None}, {"name": "Meetup", "launch_status": "draft"}]
)
def test_create_calendar_requires_name_and_known_status(data):
    with pytest.raises(ValidationError):
        models.CreateCalendarRequest.model_validate(data)


@pytest.mark.parametrize(
    "location",
    [
        None,
        {"type": "lookup", "query": ""},
        {"type": "google", "place_id": ""},
        {"type": "manual", "address": "Indianapolis"},
    ],
)
def test_location_matches_documented_lookup_or_google_shape(location):
    with pytest.raises(ValidationError):
        models.CreateCalendarRequest(name="Community", location=location)


def test_create_calendar_preserves_optional_null_and_empty_string():
    request = models.CreateCalendarRequest(
        name="Community", website=None, twitter_handle=""
    )
    assert request.model_dump(mode="json", exclude_unset=True) == {
        "name": "Community",
        "website": None,
        "twitter_handle": "",
    }


def test_create_calendar_leaves_defaults_to_luma():
    request = models.CreateCalendarRequest(name="Community")
    assert request.model_dump(mode="json", exclude_unset=True) == {"name": "Community"}


@pytest.mark.parametrize(
    "data", [{}, {"event_id": "evt-meetup"}, {"calendar_id": "cal-labs"}]
)
def test_transfer_requires_event_and_destination_calendar(data):
    with pytest.raises(ValidationError):
        models.TransferEventCalendarRequest.model_validate(data)


@pytest.mark.parametrize(
    "data", [{"after": "invalid-date"}, {"sort_direction": "sideways"}]
)
def test_event_filters_reject_invalid_values(data):
    with pytest.raises(ValidationError):
        models.ListOrganizationEventsRequest.model_validate(data)


def test_event_listing_preserves_legacy_ids_and_calendar_associations():
    cases = json.loads(
        (Path(__file__).parents[1] / "fixtures/organizations.json").read_text()
    )
    raw = next(
        case["response"]
        for case in cases
        if case["scenario"] == "list_events_with_calendar_associations"
    )
    result = models.ListOrganizationEventsResponse.model_validate(raw).model_dump(
        mode="json", exclude_unset=True
    )
    entry = result["entries"][0]
    assert entry["api_id"] == entry["id"]
    assert {calendar["id"] for calendar in entry["managing_calendars"]} == {
        "cal-meetup",
        "cal-labs",
    }
    assert result == raw


def test_fixtures_cover_all_organization_endpoints():
    cases = json.loads(
        (Path(__file__).parents[1] / "fixtures/organizations.json").read_text()
    )
    documented = {
        (method.upper(), path)
        for path, methods in SNAPSHOT["paths"].items()
        for method in methods
    }
    assert {(case["method"], case["path"]) for case in cases} == documented
    assert len(documented) == 5
