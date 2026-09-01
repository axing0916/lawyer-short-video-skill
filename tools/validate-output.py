#!/usr/bin/env python3
"""Validate a generated JSON delivery package against config/output-schema.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "config" / "output-schema.json"


def validate(value: Any, schema: dict[str, Any], location: str, errors: list[str]) -> None:
    expected = schema.get("type")
    if expected:
        types = expected if isinstance(expected, list) else [expected]
        valid = {
            "object": isinstance(value, dict),
            "array": isinstance(value, list),
            "string": isinstance(value, str),
            "null": value is None,
            "boolean": isinstance(value, bool),
            "number": isinstance(value, (int, float)) and not isinstance(value, bool),
            "integer": isinstance(value, int) and not isinstance(value, bool),
        }
        if not any(valid.get(kind, False) for kind in types):
            errors.append(f"{location}: expected {' or '.join(types)}")
            return
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{location}: must be one of {schema['enum']}")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{location}: must not be empty")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{location}: does not match required pattern")
        if schema.get("format") == "date-time":
            try:
                datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                errors.append(f"{location}: must be an ISO 8601 date-time")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{location}: must contain at least {schema['minItems']} item(s)")
        for index, item in enumerate(value):
            validate(item, schema.get("items", {}), f"{location}[{index}]", errors)
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{location}: missing required property '{key}'")
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    errors.append(f"{location}: unexpected property '{key}'")
        for key, child in properties.items():
            if key in value:
                validate(value[key], child, f"{location}.{key}", errors)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", nargs="?", type=Path, help="generated JSON file to validate")
    parser.add_argument("--schema-check", action="store_true", help="verify the bundled draft-07 schema declaration")
    args = parser.parse_args()

    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid bundled schema: {exc}", file=sys.stderr)
        return 2
    if schema.get("$schema") != "http://json-schema.org/draft-07/schema#":
        print("schema must declare JSON Schema draft-07", file=sys.stderr)
        return 2
    if args.schema_check:
        print("OUTPUT SCHEMA PASSED: draft-07 declaration present")
        return 0
    if args.output is None:
        parser.error("output is required unless --schema-check is used")
    try:
        output = json.loads(args.output.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid output JSON: {exc}", file=sys.stderr)
        return 2
    errors: list[str] = []
    validate(output, schema, "$", errors)
    if errors:
        print("OUTPUT VALIDATION FAILED")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"OUTPUT VALIDATION PASSED: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
