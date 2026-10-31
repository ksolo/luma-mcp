"""Membership contracts, registration answers, and payment-related input flags."""

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from luma_mcp.models import memberships as models

SNAPSHOT = json.loads(
    (Path(__file__).parents[2] / "schemas/memberships.json").read_text()
)


@pytest.mark.parametrize("part", ["request", "response"])
def test_fixtures_match_documented_schema(membership_case, part):
    suffix = "Request" if part == "request" else "Response"
    Draft202012Validator(
        {
            "$ref": f"#/components/schemas/{membership_case['model']}{suffix}",
            "components": SNAPSHOT["components"],
        }
    ).validate(membership_case[part])


@pytest.mark.parametrize(
    "data",
    [
        {},
        {"email": "not-an-email", "membership_tier_id": "tier-community"},
        {"email": "alex@example.com"},
    ],
)
def test_add_member_requires_valid_email_and_tier(data):
    with pytest.raises(ValidationError):
        models.AddMemberToTierRequest.model_validate(data)


def test_skip_payment_is_not_invented_for_the_caller():
    request = models.AddMemberToTierRequest(
        email="alex@example.com", membership_tier_id="tier-community"
    )
    assert request.model_dump(mode="json", exclude_unset=True) == {
        "email": "alex@example.com",
        "membership_tier_id": "tier-community",
    }


@pytest.mark.parametrize(
    "data",
    [
        {"status": "approved"},
        {"user_id": "usr-alex"},
        {"user_id": "usr-alex", "status": "pending"},
    ],
)
def test_status_update_requires_identifier_and_supported_status(data):
    with pytest.raises(ValidationError):
        models.UpdateMemberStatusRequest.model_validate(data)


def test_skip_payment_cannot_be_null():
    with pytest.raises(ValidationError):
        models.AddMemberToTierRequest(
            email="alex@example.com",
            membership_tier_id="tier-community",
            skip_payment=None,
        )


def test_registration_answer_rejects_wrong_value_type():
    with pytest.raises(ValidationError):
        models.AddMemberToTierRequest.model_validate(
            {
                "email": "alex@example.com",
                "membership_tier_id": "tier-community",
                "registration_answers": [
                    {
                        "label": "Code of conduct",
                        "question_id": "q-conduct",
                        "question_type": "agree-check",
                        "value": {"unexpected": "object"},
                    }
                ],
            }
        )


def test_fixtures_cover_all_membership_endpoints():
    cases = json.loads(
        (Path(__file__).parents[1] / "fixtures/memberships.json").read_text()
    )
    documented = {
        (method.upper(), path)
        for path, methods in SNAPSHOT["paths"].items()
        for method in methods
    }
    assert {(case["method"], case["path"]) for case in cases} == documented
    assert len(documented) == 3
