#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_DIR=$(dirname -- "$SCRIPT_DIR")

python3 -c 'import json, pathlib, sys; root=pathlib.Path(sys.argv[1]); data=json.loads((root/"config/version.json").read_text()); doc=(root/"VERSION.md").read_text(); ok=data["version"] in doc and data["release_date"] in doc; print(data["version"], data["release_date"]); raise SystemExit(0 if ok else 1)' "$PROJECT_DIR"
