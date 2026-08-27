#!/usr/bin/env python3
"""Check a small set of repository-wide factual and safety invariants."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = {
    "support@lawyer-skill.com": "unverified support address",
    '"release_date": "2025-01-27"': "incorrect release date",
    '"status": "production"': "unverified production status",
    '"success_rate": 75': "fabricated success-rate setting",
}


def main() -> int:
    failures: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.name == "content-audit.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for phrase, reason in FORBIDDEN.items():
            if phrase in text:
                failures.append(f"{path.relative_to(ROOT)}: {reason}")
    if failures:
        print("\n".join(failures))
        return 1
    print("CONTENT AUDIT PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
