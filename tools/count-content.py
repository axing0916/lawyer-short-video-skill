#!/usr/bin/env python3
"""Report repository size without treating size as a quality score."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
characters = 0
for path in files:
    try:
        characters += len(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        pass

print(f"files={len(files)}")
print(f"utf8_characters={characters}")
for directory in sorted(path for path in ROOT.iterdir() if path.is_dir()):
    count = sum(1 for path in directory.rglob("*") if path.is_file())
    print(f"{directory.name}={count}")
