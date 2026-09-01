#!/usr/bin/env python3
"""Unit tests for PII detection tool."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from importlib.machinery import SourceFileLoader
detect_pii_module = SourceFileLoader("detect_pii", str(ROOT / "tools" / "detect-pii.py")).load_module()
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
        self.assertTrue(id_item["masked_value"].startswith("110105********"))

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


if __name__ == "__main__":
    unittest.main()
