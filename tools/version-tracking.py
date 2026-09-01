#!/usr/bin/env python3
"""Initialize, update, and compare version metadata in Markdown delivery files."""

from __future__ import annotations

import argparse
import difflib
import hashlib
from datetime import UTC, datetime
from pathlib import Path


def split_frontmatter(text: str) -> tuple[str, str]:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[4:end], text[end + 5 :]
    return "", text


def parse_frontmatter(frontmatter: str) -> dict[str, str]:
    return dict(line.split(": ", 1) for line in frontmatter.splitlines() if ": " in line)


def content_hash(body: str) -> str:
    return f"sha256:{hashlib.sha256(body.encode('utf-8')).hexdigest()}"


def render(metadata: dict[str, str], body: str) -> str:
    order = ("version", "timestamp", "modified_by", "modification_type", "content_hash", "previous_hash")
    lines = [f"{key}: {metadata[key]}" for key in order if metadata.get(key)]
    frontmatter = "\n".join(lines)
    return f"---\n{frontmatter}\n---\n{body.lstrip()}"


def read_markdown(path: Path) -> tuple[dict[str, str], str]:
    frontmatter, body = split_frontmatter(path.read_text(encoding="utf-8"))
    return parse_frontmatter(frontmatter), body


def timestamp() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def initialize(destination: Path, template: Path | None, modifier: str, change_type: str) -> None:
    if destination.exists():
        raise ValueError(f"refusing to overwrite existing file: {destination}")
    body = template.read_text(encoding="utf-8") if template else "# 【待补充】\n"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        render(
            {"version": "1", "timestamp": timestamp(), "modified_by": modifier,
             "modification_type": change_type, "content_hash": content_hash(body)},
            body,
        ),
        encoding="utf-8",
    )


def update(path: Path, modifier: str, change_type: str) -> None:
    metadata, body = read_markdown(path)
    try:
        version = int(metadata.get("version", "0")) + 1
    except ValueError as exc:
        raise ValueError("existing version must be an integer") from exc
    path.write_text(
        render(
            {"version": str(version), "timestamp": timestamp(), "modified_by": modifier,
             "modification_type": change_type, "content_hash": content_hash(body),
             "previous_hash": metadata.get("content_hash", "")},
            body,
        ),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--init", type=Path, metavar="FILE", help="create a tracked Markdown file")
    action.add_argument("--update", type=Path, metavar="FILE", help="record a new version after editing")
    action.add_argument("--diff", nargs=2, type=Path, metavar=("OLD", "NEW"), help="compare tracked Markdown bodies")
    parser.add_argument("--template", type=Path, help="template used with --init")
    parser.add_argument("--modifier", default="【待补充】", help="person or system making the version")
    parser.add_argument("--type", dest="change_type", default="ai_generated",
                        choices=("ai_generated", "human_edit", "legal_review", "metadata_update"))
    args = parser.parse_args()
    try:
        if args.init:
            initialize(args.init, args.template, args.modifier, args.change_type)
            print(f"initialized version metadata: {args.init}")
        elif args.update:
            update(args.update, args.modifier, args.change_type)
            print(f"updated version metadata: {args.update}")
        else:
            _, old = read_markdown(args.diff[0])
            _, new = read_markdown(args.diff[1])
            print("".join(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
                                               fromfile=str(args.diff[0]), tofile=str(args.diff[1])))
                  or "no content differences")
    except (OSError, ValueError) as exc:
        print(f"version tracking failed: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
