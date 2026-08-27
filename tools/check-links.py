#!/usr/bin/env python3
"""Check relative Markdown links."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def main() -> int:
    failures: list[str] = []
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for raw in LINK.findall(text):
            target = raw.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                failures.append(f"link escapes repository: {path.relative_to(ROOT)} -> {raw}")
                continue
            if not resolved.exists():
                failures.append(f"missing link: {path.relative_to(ROOT)} -> {raw}")
    if failures:
        print("\n".join(failures))
        return 1
    print("LINK CHECK PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
