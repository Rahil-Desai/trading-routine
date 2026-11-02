import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_trade_log as ctl  # noqa: E402

OLD = """| Date | Ticker | Side | Shares | Entry | Stop | Thesis | Target | R:R |
|------|--------|------|--------|-------|------|--------|--------|-----|
| 2026-04-29 | XLE | BUY | 340 | $58.46 | $52.59 (10% trail) | Energy leadership | $67.23 (+15%) | 2.5:1 |
"""

NEW = """| Date | Ticker | Side | Shares | Entry | Stop | Thesis | Target | R:R | Confidence | Horizon |
|------|--------|------|--------|-------|------|--------|--------|-----|------------|---------|
| 2026-11-02 | CVX | BUY | 44 | $235.52 | $211.97 (10% trail) | Q3 beat | $270.85 (+15%) | 2.5:1 | 65 | 4w |
| 2026-11-02 | NVDA | SELL (rule-8 cut) | 48 | $207.24 | -- | cut | -- | -- | -- | -- |
| 2026-11-03 | MU | BUY | 10 | $900 | $810 | AI memory | $1,000 | 1.1:1 | **70%** | 10 d |
"""


class CheckTradeLogTest(unittest.TestCase):
    def test_old_tables_are_skipped_not_flagged(self):
        r = ctl.check(OLD)
        self.assertEqual((r.checked, r.legacy, r.problems), (0, 1, []))

    def test_new_rows_pass_and_sells_are_ignored(self):
        r = ctl.check(OLD + "\n" + NEW)
        self.assertEqual(r.problems, [])
        self.assertEqual((r.checked, r.legacy), (2, 1))

    def test_bad_values_are_flagged(self):
        bad = NEW.replace("| 65 | 4w |", "| high | soon |").replace("| **70%** |", "| 140 |")
        r = ctl.check(bad)
        messages = [p.message for p in r.problems]
        self.assertEqual(len(messages), 3, messages)
        self.assertIn("confidence should be 0-100, got 'high'", messages[0])
        self.assertIn("horizon should look like", messages[1])
        self.assertIn("got '140'", messages[2])

    def test_missing_values_are_flagged(self):
        r = ctl.check(NEW.replace("| 65 | 4w |", "| -- | -- |"))
        self.assertEqual(len(r.problems), 2)

    def test_since_filters_by_date(self):
        bad = NEW.replace("| 65 | 4w |", "| x | y |")
        self.assertEqual(len(ctl.check(bad, since="2026-11-03").problems), 0)
        self.assertEqual(ctl.check(bad, since="2026-11-03").checked, 1)

    def test_real_trade_log_still_passes(self):
        r = ctl.check((ROOT / "memory" / "TRADE-LOG.md").read_text(encoding="utf-8"))
        self.assertEqual(r.problems, [])
        self.assertGreater(r.legacy, 0)

    def test_cli_exit_codes(self):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            good, bad = Path(d, "good.md"), Path(d, "bad.md")
            good.write_text(OLD + "\n" + NEW)
            bad.write_text(NEW.replace("| 65 |", "| 101 |"))
            self.assertEqual(ctl.main([str(good)]), 0)
            self.assertEqual(ctl.main([str(bad)]), 1)


if __name__ == "__main__":
    unittest.main()
