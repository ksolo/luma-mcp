"""Regenerate Pydantic models from checked-in Luma OpenAPI snapshots."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def generate(domain: str) -> None:
    subprocess.run(
        [
            "datamodel-codegen",
            "--input",
            str(ROOT / "schemas" / f"{domain}.json"),
            "--input-file-type",
            "openapi",
            "--openapi-scopes",
            "schemas",
            "--output",
            str(ROOT / "src/luma_mcp/models" / f"{domain}.py"),
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
