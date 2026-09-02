#!/usr/bin/env sh
# Unified test entry point.
#
# Usage:
#   tests/run-all-tests.sh              # run repository validation, PII self-test, E2E and performance checks
#   tests/run-all-tests.sh --quick      # skip the performance check
#   tests/run-all-tests.sh --report html  # additionally write tests/report.html
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_DIR=$(dirname -- "$SCRIPT_DIR")

QUICK=0
REPORT_FORMAT=""

while [ $# -gt 0 ]; do
  case "$1" in
    --quick)
      QUICK=1
      shift
      ;;
    --report)
      REPORT_FORMAT=${2:-}
      shift 2
      ;;
    *)
      echo "unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required to run the test suite." >&2
  exit 1
fi

LOG_FILE=$(mktemp)
trap 'rm -f "$LOG_FILE"' EXIT

STATUS=0
STEPS="repository-validation pii-self-test schema-validation e2e-tests"
if [ "$QUICK" -eq 0 ]; then
  STEPS="$STEPS performance-smoke-test"
fi

run_step() {
  name=$1
  shift
  echo "=== $name ===" | tee -a "$LOG_FILE"
  step_output=$(mktemp)
  if "$@" >"$step_output" 2>&1; then
    step_status=0
  else
    step_status=1
  fi
  cat "$step_output" | tee -a "$LOG_FILE"
  rm -f "$step_output"
  if [ "$step_status" -eq 0 ]; then
    echo "[PASS] $name" | tee -a "$LOG_FILE"
  else
    echo "[FAIL] $name" | tee -a "$LOG_FILE"
    STATUS=1
  fi
}

for step in $STEPS; do
  case "$step" in
    repository-validation)
      run_step "repository-validation" python3 "$PROJECT_DIR/tools/validate.py"
      ;;
    pii-self-test)
      run_step "pii-self-test" python3 "$PROJECT_DIR/tools/detect-pii.py" --self-test
      ;;
    schema-validation)
      run_step "schema-validation" python3 "$PROJECT_DIR/tools/validate-schema.py"
      ;;
    e2e-tests)
      run_step "e2e-tests" python3 "$PROJECT_DIR/tests/e2e_runner.py"
      ;;
    performance-smoke-test)
      run_step "performance-smoke-test" python3 -c '
import sys, time, importlib.util
spec = importlib.util.spec_from_file_location("detect_pii", "'"$PROJECT_DIR"'/tools/detect-pii.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
text = "身份证110101199003077758电话13812345678" * 5000
start = time.perf_counter()
m.scan_text(text)
elapsed = time.perf_counter() - start
print(f"scanned {len(text)} chars in {elapsed:.3f}s")
sys.exit(0 if elapsed < 5 else 1)
'
      ;;
  esac
done

if [ -n "$REPORT_FORMAT" ]; then
  if [ "$REPORT_FORMAT" = "html" ]; then
    REPORT_PATH="$PROJECT_DIR/tests/report.html"
    {
      echo "<!DOCTYPE html><html lang=\"zh\"><head><meta charset=\"utf-8\"><title>测试报告</title></head><body>"
      echo "<h1>测试报告</h1><pre>"
      sed -e 's/&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g' "$LOG_FILE"
      echo "</pre></body></html>"
    } > "$REPORT_PATH"
    echo "HTML report written to $REPORT_PATH"
  else
    echo "unsupported --report format: $REPORT_FORMAT (only 'html' is supported)" >&2
    STATUS=1
  fi
fi

exit "$STATUS"
