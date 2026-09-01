#!/usr/bin/env python3
"""Detect likely-unredacted personal or case identifiers in text.

Read-only, offline heuristic scanner. It does not access the network and
does not modify any file unless explicitly asked to print a masked copy.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (label, pattern, mask) — order matters, more specific patterns first.
PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    ("case_number", re.compile(r"[（(]\d{4}[）)][^\s，,。]{0,10}\d+号"), "【案号】"),
    ("id_card", re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)"), "【身份证号】"),
    ("id_card_15", re.compile(r"(?<!\d)\d{15}(?!\d)"), "【身份证号】"),
    ("phone", re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"), "【手机号】"),
    ("uscc", re.compile(r"\b[0-9A-HJ-NPQRTUWXY]{2}\d{6}[0-9A-HJ-NPQRTUWXY]{10}\b"), "【统一社会信用代码】"),
    ("bank_card", re.compile(r"(?<!\d)\d{16,19}(?!\d)"), "【银行卡号】"),
]


def scan_text(text: str) -> list[dict[str, str]]:
    """Return a list of findings with type, matched value, and position.

    All patterns are matched independently and then merged in a single pass
    (sorted by start, preferring longer matches first) so overlap resolution
    stays linear in the number of candidate matches instead of quadratic.
    """
    candidates: list[tuple[int, int, str, str]] = []
    for label, pattern, _mask in PATTERNS:
        for match in pattern.finditer(text):
            start, end = match.span()
            candidates.append((start, end, label, match.group(0)))
    candidates.sort(key=lambda item: (item[0], -(item[1] - item[0])))

    findings: list[dict[str, str]] = []
    next_free = 0
    for start, end, label, value in candidates:
        if start < next_free:
            continue
        findings.append({"type": label, "value": value, "start": str(start)})
        next_free = end
    return findings


def mask_text(text: str) -> str:
    """Return text with detected identifiers replaced by category labels."""
    findings = scan_text(text)
    if not findings:
        return text
    label_by_value = {label: mask for label, _pattern, mask in PATTERNS}
    result = text
    # Replace from the end so earlier offsets stay valid.
    ordered = sorted(findings, key=lambda item: int(item["start"]), reverse=True)
    for finding in ordered:
        start = int(finding["start"])
        end = start + len(finding["value"])
        result = result[:start] + label_by_value[finding["type"]] + result[end:]
    return result


def scan_path(path: Path) -> list[dict[str, str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    return scan_text(text)


SELF_TEST_CASES: list[tuple[str, bool]] = [
    ("身份证号：110101199003077758", True),
    ("联系电话 13812345678 请勿外传", True),
    ("案号（2024）京01民终1234号", True),
    ("统一社会信用代码 91110000123456789X", True),
    ("银行卡号 6222021234567890123", True),
    ("这是一段完全脱敏的教学文本，不含任何标识符。", False),
]


def self_test() -> int:
    failures = []
    for text, expect_hit in SELF_TEST_CASES:
        hit = bool(scan_text(text))
        if hit != expect_hit:
            failures.append(f"unexpected result for {text!r}: got {hit}, expected {expect_hit}")
    if failures:
        print("SELF-TEST FAILED")
        for item in failures:
            print(f"- {item}")
        return 1
    print(f"SELF-TEST PASSED: {len(SELF_TEST_CASES)} cases")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, help="scan a single file")
    parser.add_argument("--dir", type=Path, help="scan all files under a directory")
    parser.add_argument("--text", type=str, help="scan inline text")
    parser.add_argument("--json", action="store_true", help="emit JSON output")
    parser.add_argument("--self-test", action="store_true", help="run built-in self test")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    report: dict[str, list[dict[str, str]]] = {}
    if args.text is not None:
        report["<inline>"] = scan_text(args.text)
    if args.file is not None:
        report[str(args.file)] = scan_path(args.file)
    if args.dir is not None:
        for path in sorted(args.dir.rglob("*")):
            if path.is_file() and ".git" not in path.parts:
                findings = scan_path(path)
                if findings:
                    report[str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)] = findings

    if not (args.text is not None or args.file is not None or args.dir is not None):
        parser.print_help()
        return 2

    total = sum(len(findings) for findings in report.values())
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        if total == 0:
            print("PII SCAN: no identifiers detected")
        else:
            print(f"PII SCAN: {total} potential identifier(s) found")
            for source, findings in report.items():
                if not findings:
                    continue
                print(f"- {source}")
                for finding in findings:
                    print(f"  - {finding['type']}: {finding['value']}")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
