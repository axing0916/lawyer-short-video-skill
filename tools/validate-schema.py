#!/usr/bin/env python3
"""Validate JSON fixtures against config/schema.json using a minimal,
dependency-free subset of JSON Schema (draft-07): type, required,
properties, enum, pattern, items, minItems. This intentionally avoids a
third-party dependency so it can run anywhere python3 runs.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "config" / "schema.json"

# Fixtures under tests/fixtures/e2e/*/input.json are expected to conform to
# the input schema. Structural-only fixtures under tests/fixtures/*.json are
# intentionally minimal and are not schema targets.
TARGET_GLOB = "tests/fixtures/e2e/*/input.json"

TYPE_MAP = {
    "string": str,
    "boolean": bool,
    "array": list,
    "object": dict,
    "number": (int, float),
    "integer": int,
}


def check_type(value: Any, expected: str) -> bool:
    python_type = TYPE_MAP.get(expected)
    if python_type is None:
        return True
    if expected == "boolean" and isinstance(value, bool):
        return True
    if expected in ("number", "integer") and isinstance(value, bool):
        return False
    return isinstance(value, python_type)


def validate_node(value: Any, schema: dict, path: str, errors: list[str]) -> None:
    if "type" in schema and not check_type(value, schema["type"]):
        errors.append(f"{path}: expected type {schema['type']!r}, got {type(value).__name__}")
        return

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} not in enum {schema['enum']!r}")

    if "pattern" in schema and isinstance(value, str):
        if not re.match(schema["pattern"], value):
            errors.append(f"{path}: value {value!r} does not match pattern {schema['pattern']!r}")

    if schema.get("type") == "object" and isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing required property {key!r}")
        properties = schema.get("properties", {})
        for key, item_value in value.items():
            if key in properties:
                validate_node(item_value, properties[key], f"{path}.{key}", errors)

    if schema.get("type") == "array" and isinstance(value, list):
        min_items = schema.get("minItems")
        if min_items is not None and len(value) < min_items:
            errors.append(f"{path}: expected at least {min_items} item(s), got {len(value)}")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                validate_node(item, item_schema, f"{path}[{index}]", errors)


def validate_file(path: Path, schema: dict) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return [f"{path.relative_to(ROOT)}: invalid JSON ({exc})"]
    validate_node(data, schema, str(path.relative_to(ROOT)), errors)
    return errors


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    targets = sorted(ROOT.glob(TARGET_GLOB))
    if not targets:
        print(f"no fixtures matched {TARGET_GLOB}")
        return 1

    all_errors: list[str] = []
    for target in targets:
        errors = validate_file(target, schema)
        if errors:
            all_errors.extend(errors)
        else:
            print(f"OK  {target.relative_to(ROOT)}")

    if all_errors:
        print("SCHEMA VALIDATION FAILED")
        for error in all_errors:
            print(f"- {error}")
        return 1

    print(f"SCHEMA VALIDATION PASSED: {len(targets)} fixture(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
