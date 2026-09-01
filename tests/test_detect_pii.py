#!/usr/bin/env python3
"""Unit tests for PII detection tool."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

import importlib.util

spec = importlib.util.spec_from_file_location("detect_pii", str(ROOT / "tools" / "detect-pii.py"))
if spec is None or spec.loader is None:
    raise ImportError("Could not load detect-pii.py")
detect_pii_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(detect_pii_module)
detect_pii = detect_pii_module.detect_pii


class TestPIIDetection(unittest.TestCase):

    def test_id_card_18_detection(self):
        # Valid 18-digit ID
        text = "当事人身份证为 11010519491231002X，现居住于北京。"
        res = detect_pii(text)
        self.assertTrue(res["detected"])
        self.assertEqual(res["status"], "blocked")
        self.assertTrue(any(item["type"] == "id_card" for item in res["high_risk"]))
        id_item = next(item for item in res["high_risk"] if item["type"] == "id_card")
        self.assertEqual(id_item["masked_value"], "110105********002X")

    def test_id_card_15_detection(self):
        text = "初代身份证：320102750101001"
        res = detect_pii(text)
        self.assertTrue(res["detected"])
        self.assertEqual(res["status"], "blocked")
        self.assertTrue(any(item["type"] == "id_card" for item in res["high_risk"]))

    def test_phone_detection(self):
        text = "联系电话是 13800138000，请尽快回复。"
        res = detect_pii(text)
        self.assertTrue(res["detected"])
        self.assertEqual(res["status"], "blocked")
        phone_item = next(item for item in res["high_risk"] if item["type"] == "phone")
        self.assertEqual(phone_item["value"], "13800138000")
        self.assertEqual(phone_item["masked_value"], "138****8000")

    def test_usci_detection(self):
        text = "某企业信用代码 91110108MA01ABCD12 已被登记。"
        res = detect_pii(text)
        self.assertTrue(res["detected"])
        self.assertEqual(res["status"], "blocked")
        usci_item = next(item for item in res["high_risk"] if item["type"] == "usci")
        self.assertEqual(usci_item["value"], "91110108MA01ABCD12")

    def test_bank_card_detection(self):
        text = "请向银行卡 6222021234567890123 支付货款。"
        res = detect_pii(text)
        self.assertTrue(res["detected"])
        self.assertEqual(res["status"], "blocked")
        card_item = next(item for item in res["high_risk"] if item["type"] == "bank_card")
        self.assertTrue("622202" in card_item["masked_value"])

    def test_case_number_detection(self):
        text = "本纠纷见判决书（2023）京01民初1234号。"
        res = detect_pii(text)
        self.assertTrue(res["detected"])
        self.assertEqual(res["status"], "needs_review")
        self.assertEqual(len(res["high_risk"]), 0)
        self.assertEqual(len(res["medium_risk"]), 1)
        case_item = res["medium_risk"][0]
        self.assertEqual(case_item["type"], "case_number")
        self.assertEqual(case_item["value"], "（2023）京01民初1234号")

    def test_clean_material(self):
        text = "甲公司向乙先生转账借款数十万元，约定借期半年，年利率6%，目前到期未还。"
        res = detect_pii(text)
        self.assertFalse(res["detected"])
        self.assertEqual(res["status"], "passed")
        self.assertEqual(res["summary"]["total_count"], 0)

    def test_cli_execution(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "detect-pii.py"), "--text", "手机 13812345678"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 1)  # blocked exit code
        data = json.loads(proc.stdout)
        self.assertEqual(data["status"], "blocked")

    def test_cli_medium_risk_exit_code(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "detect-pii.py"), "--text", "（2023）京01民初1234号", "--format", "text"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 2)  # needs_review exit code
        self.assertIn("NEEDS_REVIEW", proc.stdout)

    def test_cli_clean_exit_code(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "detect-pii.py"), "--text", "甲向乙转账", "--format", "text"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0)  # passed exit code
        self.assertIn("PASSED", proc.stdout)


if __name__ == "__main__":
    unittest.main()
