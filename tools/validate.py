#!/usr/bin/env python3
"""Validate repository structure and safety invariants without network access."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "SKILL.md",
    "README.md",
    "CONTENT-SAFETY.md",
    "PRIVACY.md",
    "docs/01-quick-start.md",
    "modules/03-generation/prompts/00-main-prompt.md",
    "libraries/hook-library.md",
    "libraries/case-library.md",
    "libraries/cta-library.md",
    "config/version.json",
    "checklists/pre-publish.md",
]


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def main() -> int:
    failures: list[str] = []
    files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
    if len(files) < 120:
        fail(f"expected at least 120 files, found {len(files)}", failures)

    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            fail(f"missing required file: {relative}", failures)

    for path in files:
        try:
            path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            fail(f"not readable UTF-8: {path.relative_to(ROOT)} ({exc})", failures)

    for path in ROOT.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            fail(f"invalid JSON: {path.relative_to(ROOT)} ({exc})", failures)

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not re.match(r"^---\n(?:.|\n)*?\n---\n", skill):
        fail("SKILL.md frontmatter missing or malformed", failures)
    for key in ("name:", "description:"):
        if key not in skill.split("---", 2)[1]:
            fail(f"SKILL.md frontmatter missing {key}", failures)

    version = json.loads((ROOT / "config/version.json").read_text(encoding="utf-8"))
    version_doc = (ROOT / "VERSION.md").read_text(encoding="utf-8")
    if version["version"] not in version_doc or version["release_date"] not in version_doc:
        fail("VERSION.md does not match config/version.json", failures)

    for group in ("private-lending", "contract", "company", "family"):
        cards = sorted((ROOT / "libraries/scenarios" / group).glob("[0-9][0-9]-*.md"))
        if len(cards) < 5:
            fail(f"scenario group {group} has fewer than 5 cards", failures)
        for card in cards:
            if "虚构教学情景" not in card.read_text(encoding="utf-8"):
                fail(f"scenario not labeled fictional: {card.relative_to(ROOT)}", failures)

    library_counts = {
        "libraries/transition-words.md": (r"\bT\d{3}\b", 100),
        "libraries/emotion-words.md": (r"\bE\d{3}\b", 100),
        "libraries/key-phrases.md": (r"\bK\d{3}\b", 200),
    }
    for relative, (pattern, minimum) in library_counts.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        identifiers = set(re.findall(pattern, content))
        if len(identifiers) < minimum:
            fail(f"{relative} has {len(identifiers)} indexed items; expected {minimum}+", failures)

    for script in ("check-links.py", "content-audit.py"):
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / script)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode:
            fail(f"{script} failed:\n{result.stdout}{result.stderr}", failures)

    if failures:
        print("VALIDATION FAILED")
        for item in failures:
            print(f"- {item}")
        return 1

    print(f"VALIDATION PASSED: {len(files)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
