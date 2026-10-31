"""Synthetic examples based on Luma's checked-in OpenAPI snapshot."""

import json
from pathlib import Path

import pytest

EVENT_CASES = json.loads((Path(__file__).parent / "fixtures/events.json").read_text())


@pytest.fixture(params=EVENT_CASES, ids=lambda case: case["operation"])
def event_case(request):
    return request.param


CALENDAR_CASES = json.loads(
    (Path(__file__).parent / "fixtures/calendars.json").read_text()
)


@pytest.fixture(params=CALENDAR_CASES, ids=lambda case: case["scenario"])
def calendar_case(request):
    return request.param


MEMBERSHIP_CASES = json.loads(
    (Path(__file__).parent / "fixtures/memberships.json").read_text()
)


@pytest.fixture(params=MEMBERSHIP_CASES, ids=lambda case: case["scenario"])
def membership_case(request):
    return request.param
