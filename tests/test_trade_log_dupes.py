import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import trade_log_dupes as tld  # noqa: E402

ORIGINAL = """## 2026-09-14 -- Market-Open Execution

| Date | Ticker | Side | Shares | Entry | Stop | Thesis | Target | R:R |
|------|--------|------|--------|-------|------|--------|--------|-----|
| 2026-09-14 | NVDA | SELL (rule-8 cut) | 26 | **$209.35** (order 3b0747a0) | -- | cut | -- | -- |
| 2026-09-14 | GOOGL | BUY | 58 | **$344.881896** (order 101cd0de) | $310.53 | redeploy | $380 | 2:1 |
"""

# The same fills, re-logged by a later run that couldn't see the first one (different wording/format).
RECONSTRUCTED = """## 2026-09-15 -- RECONSTRUCTED from Alpaca closed-order history

| Date | Ticker | Side | Shares | Price | Note |
|------|--------|------|--------|-------|------|
| 2026-09-14 | GOOGL | BUY | 58 | $344.88 | redeploy (101cd0de) |
| 2026-09-14 | NVDA | SELL | 26 | $209.35 | cut |
| 2026-09-14 | AMZN | BUY | 68 | $254.15 | redeploy |
"""


class TradeLogDupesTest(unittest.TestCase):
    def test_single_log_has_no_duplicates(self):
        self.assertEqual(tld.duplicates(ORIGINAL), {})

    def test_reconstructed_copy_is_caught_across_table_formats(self):
        dups = tld.duplicates(ORIGINAL + "\n" + RECONSTRUCTED)
        self.assertEqual(
            sorted(dups),
            [("2026-09-14", "GOOGL", "BUY", 58, 344.88), ("2026-09-14", "NVDA", "SELL", 26, 209.35)],
        )

    def test_distinct_fills_are_not_duplicates(self):
        other = RECONSTRUCTED.replace("| 58 | $344.88 |", "| 10 | $344.88 |").replace("| 26 | $209.35 |", "| 26 | $210.00 |")
        self.assertEqual(tld.duplicates(ORIGINAL + "\n" + other), {})

    def test_non_trade_rows_are_ignored(self):
        text = ORIGINAL + """
| Date | Ticker | Action | Old Stop | New Stop | Trail % | HWM |
|------|--------|--------|----------|----------|---------|-----|
| 2026-09-14 | GOOGL | RATCHET | $310 | $313 | 10% | $348 |
| 2026-09-14 | GOOGL | RATCHET | $310 | $313 | 10% | $348 |
"""
        self.assertEqual(tld.duplicates(text), {})

    def test_baseline_only_reports_new_copies(self):
        old = ORIGINAL + "\n" + RECONSTRUCTED  # history already on main, with duplicates
        self.assertEqual(tld.duplicates(old, baseline=old), {})
        third = old + "\n" + RECONSTRUCTED.replace("2026-09-15 --", "2026-09-18 --")
        new = tld.duplicates(third, baseline=old)
        self.assertIn(("2026-09-14", "GOOGL", "BUY", 58, 344.88), new)
        self.assertIn(("2026-09-14", "AMZN", "BUY", 68, 254.15), new)  # 1 copy before, 2 now

    def test_real_log_has_known_history_and_nothing_new(self):
        text = (ROOT / tld.LOG).read_text(encoding="utf-8")
        self.assertGreater(len(tld.duplicates(text)), 0)  # Sep/Oct recovery duplicates are history
        self.assertEqual(tld.duplicates(text, baseline=text), {})

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as d:
            base, new = Path(d, "base.md"), Path(d, "new.md")
            base.write_text(ORIGINAL)
            new.write_text(ORIGINAL + "\n" + RECONSTRUCTED)
            self.assertEqual(tld.main([str(base)]), 0)
            self.assertEqual(tld.main([str(new), "--baseline", str(base)]), 1)
            self.assertEqual(tld.main([str(new), "--baseline", str(new)]), 0)


if __name__ == "__main__":
    unittest.main()
