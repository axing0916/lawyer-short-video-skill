#!/usr/bin/env python3
"""Automated Personally Identifiable Information (PII) detection tool for legal content.

Detects sensitive identifiers in Chinese legal workflow inputs:
- High Risk: ID Cards (18/15 digits), Mobile Phones (11 digits), Unified Social Credit Codes (USCI 18 chars), Bank Cards (16-19 digits)
- Medium Risk: Court Case Numbers (案号)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# Regular Expression Patterns
RE_ID_CARD_18 = re.compile(
    r"(?<!\d)([1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx])(?!\d)"
)
RE_ID_CARD_15 = re.compile(
    r"(?<!\d)([1-9]\d{5}\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3})(?!\d)"
)
RE_PHONE = re.compile(
    r"(?<!\d)(?:\+?86[- ]?)?(1[3-9]\d{9})(?!\d)"
)
RE_USCI = re.compile(
    r"(?<![0-9A-HJ-NPQRTUWXY])([1-9ANY][1-9]\d{6}[0-9A-HJ-NPQRTUWXY]{10})(?![0-9A-HJ-NPQRTUWXY])"
)
RE_BANK_CARD = re.compile(
    r"(?<!\d)([1-9]\d{3}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4,7})(?!\d)"
)
RE_CASE_NUMBER = re.compile(
    r"([（\(〔\[【]\s*(?:19|20)\d{2}\s*[）\)〕\]】][\u4e00-\u9fa5A-Za-z0-9]{2,25}?\d+号)"
)


def mask_string(val: str, pii_type: str) -> str:
    """Mask sensitive string based on PII type."""
    clean_val = val.strip()
    if pii_type == "id_card":
        if len(clean_val) == 18:
            return f"{clean_val[:6]}********{clean_val[14:]}"
        elif len(clean_val) == 15:
            return f"{clean_val[:6]}******{clean_val[12:]}"
        return f"{clean_val[:3]}***{clean_val[-3:]}"
    elif pii_type == "phone":
        digits = re.sub(r"\D", "", clean_val)
        if len(digits) >= 11:
            core = digits[-11:]
            return f"{core[:3]}****{core[7:]}"
        return f"{clean_val[:3]}***{clean_val[-2:]}"
    elif pii_type == "usci":
        if len(clean_val) == 18:
            return f"{clean_val[:4]}********{clean_val[12:]}"
        return f"{clean_val[:4]}***{clean_val[-4:]}"
    elif pii_type == "bank_card":
        digits = re.sub(r"\D", "", clean_val)
        if len(digits) >= 16:
            return f"{digits[:6]}******{digits[-4:]}"
        return f"{digits[:4]}***{digits[-4:]}"
    elif pii_type == "case_number":
        # Keep year and court prefix if possible, mask sequence number
        return re.sub(r"\d+号", "***号", clean_val)
    return clean_val


def check_id_card_checksum(id_card: str) -> bool:
    """Validate 18-digit mainland ID card checksum (GB 11643-1999)."""
    if len(id_card) != 18:
        return False
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_codes = "10X98765432"
    try:
        total = sum(int(id_card[i]) * weights[i] for i in range(17))
        return check_codes[total % 11].upper() == id_card[17].upper()
    except (ValueError, IndexError):
        return False


def spans_overlap(span1: tuple[int, int], span2: tuple[int, int]) -> bool:
    """Check if two 1D intervals [start, end) overlap."""
    return max(span1[0], span2[0]) < min(span1[1], span2[1])


def detect_pii(text: str) -> dict[str, Any]:
    """Scan text for sensitive PII identifiers and return categorized results."""
    high_risk: list[dict[str, Any]] = []
    medium_risk: list[dict[str, Any]] = []

    lines = text.splitlines()

    for line_idx, line in enumerate(lines, start=1):
        line_spans: list[tuple[int, int]] = []

        # 1. Detect ID cards (18-digit)
        for m in RE_ID_CARD_18.finditer(line):
            val = m.group(1)
            span = (m.start(1), m.end(1))
            is_valid_checksum = check_id_card_checksum(val)
            line_spans.append(span)
            high_risk.append({
                "type": "id_card",
                "type_label": "大陆身份证号(18位)",
                "risk_level": "high_risk",
                "value": val,
                "masked_value": mask_string(val, "id_card"),
                "line": line_idx,
                "column": m.start(1) + 1,
                "checksum_valid": is_valid_checksum,
                "description": "检测到18位大陆居民身份证号码，属于高风险直接个人标识符。"
            })

        # 2. Detect ID cards (15-digit)
        for m in RE_ID_CARD_15.finditer(line):
            val = m.group(1)
            span = (m.start(1), m.end(1))
            # Avoid subset/overlap with 18-digit ID card match
            if any(spans_overlap(span, s) for s in line_spans):
                continue
            line_spans.append(span)
            high_risk.append({
                "type": "id_card",
                "type_label": "大陆身份证号(15位)",
                "risk_level": "high_risk",
                "value": val,
                "masked_value": mask_string(val, "id_card"),
                "line": line_idx,
                "column": m.start(1) + 1,
                "description": "检测到15位初代大陆身份证号码，属于高风险直接个人标识符。"
            })

        # 3. Detect USCI (统一社会信用代码)
        for m in RE_USCI.finditer(line):
            val = m.group(1)
            span = (m.start(1), m.end(1))
            # Avoid matching pure numbers already matched as ID card
            if val.isdigit() and len(val) == 18:
                continue
            if any(spans_overlap(span, s) for s in line_spans):
                continue
            line_spans.append(span)
            high_risk.append({
                "type": "usci",
                "type_label": "统一社会信用代码",
                "risk_level": "high_risk",
                "value": val,
                "masked_value": mask_string(val, "usci"),
                "line": line_idx,
                "column": m.start(1) + 1,
                "description": "检测到18位统一社会信用代码，属于法人/机构高风险直接标识符。"
            })

        # 4. Detect Mobile Phone (11 digits)
        for m in RE_PHONE.finditer(line):
            val = m.group(1)
            span = (m.start(1), m.end(1))
            # Check if this overlaps with an already identified ID card or USCI
            if any(spans_overlap(span, s) for s in line_spans):
                continue
            line_spans.append(span)
            high_risk.append({
                "type": "phone",
                "type_label": "手机号码",
                "risk_level": "high_risk",
                "value": val,
                "masked_value": mask_string(val, "phone"),
                "line": line_idx,
                "column": m.start(1) + 1,
                "description": "检测到11位大陆手机号码，属于高风险直接联系方式。"
            })

        # 5. Detect Bank Card (16-19 digits)
        for m in RE_BANK_CARD.finditer(line):
            raw_val = m.group(1)
            digits = re.sub(r"\D", "", raw_val)
            if not (16 <= len(digits) <= 19):
                continue
            span = (m.start(1), m.end(1))
            # If overlapping with ID card or USCI, skip
            if any(spans_overlap(span, s) for s in line_spans):
                continue
            line_spans.append(span)
            high_risk.append({
                "type": "bank_card",
                "type_label": "银行卡号",
                "risk_level": "high_risk",
                "value": raw_val,
                "masked_value": mask_string(raw_val, "bank_card"),
                "line": line_idx,
                "column": m.start(1) + 1,
                "description": "检测到16-19位银行卡/借记卡/信用卡号，属于高风险金融账号信息。"
            })

        # 6. Detect Court Case Number (案号) - Medium risk
        for m in RE_CASE_NUMBER.finditer(line):
            val = m.group(1)
            medium_risk.append({
                "type": "case_number",
                "type_label": "司法案号",
                "risk_level": "medium_risk",
                "value": val,
                "masked_value": mask_string(val, "case_number"),
                "line": line_idx,
                "column": m.start(1) + 1,
                "description": "检测到具体司法审判/执行案号，易被检索关联公开裁判文书，具有重识别风险。"
            })

    total_count = len(high_risk) + len(medium_risk)
    detected = total_count > 0

    if len(high_risk) > 0:
        status = "blocked"
        recommendations = [
            "【阻断】检测到高风险个人/机构敏感标识符（身份证、手机号、信用代码或银行卡号）。",
            "根据系统安全规范，请先在本地对材料进行彻底脱敏（如替换为'张某'、'某公司'、'138****0000'等）后再行输入。"
        ]
    elif len(medium_risk) > 0:
        status = "needs_review"
        recommendations = [
            "【警告】检测到中风险案号标识符，可能导致当事人或案情被公开检索重识别。",
            "建议将案号泛化为'某合同纠纷一审案'或隐去具体年度与流水号。"
        ]
    else:
        status = "passed"
        recommendations = ["未检测到常见高风险及中风险直接敏感标识符。"]

    return {
        "detected": detected,
        "status": status,
        "summary": {
            "total_count": total_count,
            "high_risk_count": len(high_risk),
            "medium_risk_count": len(medium_risk)
        },
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "recommendations": recommendations
    }


def run_self_test() -> bool:
    """Run internal test cases to verify detection accuracy."""
    test_cases = [
        {
            "text": "客户张三，身份证号为 11010519491231002X，电话是 +86 13812345678。",
            "expected_high": 2,
            "expected_medium": 0,
            "expected_types": ["id_card", "phone"],
            "verify_checksum": True
        },
        {
            "text": "老式身份证号码：320102750101001，请注意核实。",
            "expected_high": 1,
            "expected_medium": 0,
            "expected_types": ["id_card"]
        },
        {
            "text": "公司统一社会信用代码为 91110108MA01ABCD12，向账户 6222021234567890123 转款。",
            "expected_high": 2,
            "expected_medium": 0,
            "expected_types": ["usci", "bank_card"]
        },
        {
            "text": "该纠纷经北京市第一中级人民法院（2023）京01民初123号民事判决书认定。",
            "expected_high": 0,
            "expected_medium": 1,
            "expected_types": ["case_number"]
        },
        {
            "text": "完全脱敏材料：甲公司向乙先生转账数十万元，未约定借期和利息。",
            "expected_high": 0,
            "expected_medium": 0,
            "expected_types": []
        }
    ]

    all_passed = True
    for idx, tc in enumerate(test_cases, start=1):
        res = detect_pii(tc["text"])
        high_cnt = res["summary"]["high_risk_count"]
        med_cnt = res["summary"]["medium_risk_count"]
        matched_types = [item["type"] for item in res["high_risk"] + res["medium_risk"]]

        if high_cnt != tc["expected_high"] or med_cnt != tc["expected_medium"]:
            print(f"Self-test case {idx} failed: expected {tc['expected_high']} high, {tc['expected_medium']} med, got {high_cnt} high, {med_cnt} med")
            all_passed = False
        for exp_t in tc["expected_types"]:
            if exp_t not in matched_types:
                print(f"Self-test case {idx} failed: missing expected type {exp_t}")
                all_passed = False
        if tc.get("verify_checksum"):
            id_item = next((item for item in res["high_risk"] if item["type"] == "id_card"), None)
            if not id_item or not id_item.get("checksum_valid"):
                print(f"Self-test case {idx} failed: expected checksum_valid=True")
                all_passed = False

    return all_passed


def format_text_report(results: dict[str, Any]) -> str:
    """Format human-readable text report."""
    status = results.get("status", "unknown")
    summary = results.get("summary", {})
    lines = [
        f"=== PII 检测报告 ===",
        f"状态: {status.upper()}",
        f"总计检出: {summary.get('total_count', 0)} (高风险: {summary.get('high_risk_count', 0)}, 中风险: {summary.get('medium_risk_count', 0)})",
    ]
    if results.get("high_risk"):
        lines.append("\n【高风险项 (阻断发布)】:")
        for item in results["high_risk"]:
            lines.append(f"  - [{item['type_label']}] 行 {item['line']}: {item['masked_value']} ({item['description']})")
    if results.get("medium_risk"):
        lines.append("\n【中风险项 (需人工核验)】:")
        for item in results["medium_risk"]:
            lines.append(f"  - [{item['type_label']}] 行 {item['line']}: {item['masked_value']} ({item['description']})")
    if results.get("recommendations"):
        lines.append("\n【处理建议】:")
        for rec in results["recommendations"]:
            lines.append(f"  * {rec}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Automated PII detection for legal short video materials.\n"
                    "Exit codes:\n"
                    "  0: Passed (clean)\n"
                    "  1: Blocked (high risk PII detected)\n"
                    "  2: Needs Review (medium risk PII detected)"
    )
    parser.add_argument("path", nargs="?", help="File or directory path to scan.")
    parser.add_argument("--text", "-t", help="Raw text string to scan directly.")
    parser.add_argument("--file", "-f", help="Specific file path to scan.")
    parser.add_argument("--stdin", action="store_true", help="Read input text from standard input.")
    parser.add_argument("--self-test", action="store_true", help="Run internal self-tests.")
    parser.add_argument("--format", choices=["json", "text"], default="json", help="Output format: json (default) or text.")

    args = parser.parse_args()

    if args.self_test:
        success = run_self_test()
        if success:
            print("PII DETECTION SELF-TEST PASSED")
            return 0
        else:
            print("PII DETECTION SELF-TEST FAILED")
            return 1

    content_to_scan = ""
    source_name = "raw_input"

    if args.stdin:
        content_to_scan = sys.stdin.read()
        source_name = "stdin"
    elif args.text:
        content_to_scan = args.text
        source_name = "command_line_text"
    elif args.file or args.path:
        target_path = Path(args.file or args.path)
        if not target_path.exists():
            err_obj = {"error": f"File or path not found: {target_path}"}
            print(json.dumps(err_obj, ensure_ascii=False, indent=2) if args.format == "json" else err_obj["error"])
            return 1
        if target_path.is_file():
            content_to_scan = target_path.read_text(encoding="utf-8")
            source_name = str(target_path)
        else:
            # Directory scan
            dir_results: dict[str, Any] = {"files": {}, "overall_status": "passed", "total_detected_files": 0}
            total_high = 0
            total_med = 0
            for file_path in target_path.rglob("*"):
                if (
                    file_path.is_file()
                    and not any(part.startswith(".") for part in file_path.parts)
                    and "__pycache__" not in file_path.parts
                ):
                    try:
                        text = file_path.read_text(encoding="utf-8")
                    except (UnicodeDecodeError, OSError):
                        continue
                    res = detect_pii(text)
                    if res["detected"]:
                        dir_results["files"][str(file_path)] = res
                        total_high += res["summary"]["high_risk_count"]
                        total_med += res["summary"]["medium_risk_count"]
            dir_results["total_detected_files"] = len(dir_results["files"])
            dir_results["overall_status"] = "blocked" if total_high > 0 else ("needs_review" if total_med > 0 else "passed")
            if args.format == "json":
                print(json.dumps(dir_results, ensure_ascii=False, indent=2))
            else:
                print(f"=== 目录扫描完成 ===")
                print(f"总体状态: {dir_results['overall_status']}")
                print(f"检出敏感文件数: {dir_results['total_detected_files']}")
                print(f"高风险项: {total_high}, 中风险项: {total_med}")
            if total_high > 0:
                return 1
            elif total_med > 0:
                return 2
            return 0
    else:
        # Default help or reading stdin if piped
        if not sys.stdin.isatty():
            content_to_scan = sys.stdin.read()
            source_name = "stdin"
        else:
            parser.print_help()
            return 0

    results = detect_pii(content_to_scan)
    results["source"] = source_name
    if args.format == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(format_text_report(results))

    if results["status"] == "blocked":
        return 1
    elif results["status"] == "needs_review":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
