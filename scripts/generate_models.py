"""Regenerate Pydantic models from checked-in Luma OpenAPI snapshots."""

import json
import subprocess
import sys
from itertools import product
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]


def union_variants(schema: dict, definitions: dict) -> list[dict]:
    target = (
        definitions[schema["$ref"].rsplit("/", 1)[1]] if "$ref" in schema else schema
    )
    choices = target.get("oneOf", target.get("anyOf"))
    if choices is None:
        return [schema]
    return [
        variant for choice in choices for variant in union_variants(choice, definitions)
    ]


def expand_intersections(value, definitions: dict):
    """Distribute Luma's disjoint event variants before model generation."""
    if isinstance(value, list):
        return [expand_intersections(item, definitions) for item in value]
    if not isinstance(value, dict):
        return value
    node = {key: expand_intersections(item, definitions) for key, item in value.items()}
    return distribute_intersection(node, definitions) if "allOf" in node else node


def distribute_intersection(node: dict, definitions: dict) -> dict:
    variants = [union_variants(part, definitions) for part in node["allOf"]]
    if all(len(parts) == 1 for parts in variants):
        return node
    return {
        **{key: value for key, value in node.items() if key != "allOf"},
        "anyOf": [{"allOf": list(parts)} for parts in product(*variants)],
    }


def generate(domain: str) -> None:
    snapshot = json.loads((ROOT / "schemas" / f"{domain}.json").read_text())
    normalized = expand_intersections(snapshot, snapshot["components"]["schemas"])
    with TemporaryDirectory() as directory:
        source = Path(directory) / f"{domain}.json"
        source.write_text(json.dumps(normalized))
        generate_file(source, ROOT / "src/luma_mcp/models" / f"{domain}.py")


def generate_file(source: Path, output: Path) -> None:
    subprocess.run(
        [
            "datamodel-codegen",
            "--input",
            str(source),
            "--input-file-type",
            "openapi",
            "--openapi-scopes",
            "schemas",
            "--output",
            str(output),
            "--output-model-type",
            "pydantic_v2.BaseModel",
            "--target-pydantic-version",
            "2.14",
            "--use-missing-sentinel",
            "--naming-strategy",
            "full-path",
            "--formatters",
            "ruff-check",
            "ruff-format",
            "--target-python-version",
            "3.13",
            "--use-standard-collections",
            "--use-union-operator",
            "--field-constraints",
            "--enum-field-as-literal",
            "all",
            "--use-schema-description",
            "--disable-timestamp",
        ],
        check=True,
    )


if __name__ == "__main__":
    generate(sys.argv[1])
