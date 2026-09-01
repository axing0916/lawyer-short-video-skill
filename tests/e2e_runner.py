#!/usr/bin/env python3
"""End-to-end test runner: computes a routing status for each E2E fixture
and compares it against the fixture's expected-output.json.

This encodes the routing rules described in QUALITY-GATES.md as executable
checks so the four documented end-to-end scenarios stay verifiable, without
generating or publishing any content.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES_DIR = ROOT / "tests" / "fixtures" / "e2e"

_spec = importlib.util.spec_from_file_location("detect_pii", ROOT / "tools" / "detect-pii.py")
detect_pii = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(detect_pii)

FICTIONAL_LABEL = "虚构教学情景"
MISSING_MARKERS = ("【待补充】", "unknown")


def evaluate(input_data: dict) -> dict:
    """Apply QUALITY-GATES routing rules to a single input fixture."""
    reasons: list[str] = []

    if not input_data.get("source_ids"):
        return {"status": "blocked", "reasons": ["source_lock_required"]}

    if not input_data.get("deidentified", False):
        return {"status": "blocked", "reasons": ["deidentification_required"]}

    narrative = input_data.get("narrative_text", "")
    if detect_pii.scan_text(narrative):
        return {"status": "blocked", "reasons": ["pii_detected"]}

    if input_data.get("fictional") and FICTIONAL_LABEL not in narrative:
        return {"status": "blocked", "reasons": ["fictional_label_required"]}

    if not input_data.get("legal_source_verified", False):
        return {"status": "needs_legal_review", "reasons": ["legal_source_unverified"]}

    key_facts = input_data.get("key_facts", {})
    flat_values = [str(value) for value in key_facts.values() if isinstance(value, str)]
    if input_data.get("legal_timepoint") in MISSING_MARKERS or any(
        marker in value for value in flat_values for marker in MISSING_MARKERS
    ):
        reasons.append("missing_key_facts")
        return {"status": "needs_supplement", "reasons": reasons}

    return {"status": "ready_for_legal_review", "reasons": []}


def run() -> int:
    if not FIXTURES_DIR.is_dir():
        print(f"no e2e fixtures found at {FIXTURES_DIR}")
        return 1

    scenarios = sorted(path for path in FIXTURES_DIR.iterdir() if path.is_dir())
    if not scenarios:
        print("no e2e scenario directories found")
        return 1

    failures: list[str] = []
    for scenario in scenarios:
        input_path = scenario / "input.json"
        expected_path = scenario / "expected-output.json"
        if not input_path.is_file() or not expected_path.is_file():
            failures.append(f"{scenario.name}: missing input.json or expected-output.json")
            continue

        input_data = json.loads(input_path.read_text(encoding="utf-8"))
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        actual = evaluate(input_data)

        if actual["status"] != expected["status"]:
            failures.append(
                f"{scenario.name}: expected status={expected['status']!r}, got {actual['status']!r}"
            )
            continue
        if set(actual.get("reasons", [])) != set(expected.get("reasons", [])):
            failures.append(
                f"{scenario.name}: expected reasons={expected.get('reasons')!r}, "
                f"got {actual.get('reasons')!r}"
            )
            continue
        print(f"PASS  {scenario.name}: status={actual['status']}")

    if failures:
        print("E2E TESTS FAILED")
        for item in failures:
            print(f"- {item}")
        return 1

    print(f"E2E TESTS PASSED: {len(scenarios)} scenarios")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
