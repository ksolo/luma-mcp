"""Synthetic examples based on Luma's checked-in OpenAPI snapshot."""

import json
from pathlib import Path

import pytest

EVENT_CASES = json.loads((Path(__file__).parent / "fixtures/events.json").read_text())


@pytest.fixture(params=EVENT_CASES, ids=lambda case: case["operation"])
def event_case(request):
    return request.param
