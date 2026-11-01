"""Miscellaneous API contracts, entity variants, searches, and upload parameters."""

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from luma_mcp.models import miscellaneous as models

SNAPSHOT = json.loads(
    (Path(__file__).parents[2] / "schemas/miscellaneous.json").read_text()
)


@pytest.mark.parametrize("part", ["request", "response"])
def test_fixtures_match_documented_schema(miscellaneous_case, part):
    suffix = "Request" if part == "request" else "Response"
    Draft202012Validator(
        {
            "$ref": f"#/components/schemas/{miscellaneous_case['model']}{suffix}",
            "components": SNAPSHOT["components"],
        }
    ).validate(miscellaneous_case[part])


@pytest.mark.parametrize(
    "model", [models.SearchPlacesRequest, models.SearchCoverImagesRequest]
)
@pytest.mark.parametrize("data", [{}, {"query": ""}, {"query": None}])
def test_search_requires_nonempty_query(model, data):
    with pytest.raises(ValidationError):
        model.model_validate(data)


def test_lookup_requires_slug():
    with pytest.raises(ValidationError):
        models.LookupEntityRequest.model_validate({})


def test_lookup_rejects_unknown_entity_type():
    with pytest.raises(ValidationError):
        models.LookupEntityResponse.model_validate(
            {"entity": {"type": "user", "id": "usr-alex"}}
        )


@pytest.mark.parametrize("content_type", ["image/gif", "text/plain"])
def test_upload_content_type_matches_documented_enum(content_type):
    with pytest.raises(ValidationError):
        models.CreateUploadUrlRequest(content_type=content_type)


def test_omitted_upload_content_type_is_not_invented():
    assert (
        models.CreateUploadUrlRequest().model_dump(mode="json", exclude_unset=True)
        == {}
    )


def test_explicit_null_upload_content_type_is_preserved():
    assert models.CreateUploadUrlRequest(content_type=None).model_dump(
        mode="json", exclude_unset=True
    ) == {"content_type": None}


def test_fixtures_cover_all_miscellaneous_endpoints():
    cases = json.loads(
        (Path(__file__).parents[1] / "fixtures/miscellaneous.json").read_text()
    )
    documented = {
        (method.upper(), path)
        for path, methods in SNAPSHOT["paths"].items()
        for method in methods
    }
    assert {(case["method"], case["path"]) for case in cases} == documented
    assert len(documented) == 5
