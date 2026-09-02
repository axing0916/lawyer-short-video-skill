#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_DIR=$(dirname -- "$SCRIPT_DIR")

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required to run the E2E tests." >&2
  exit 1
fi

python3 "$PROJECT_DIR/tests/e2e_runner.py"
