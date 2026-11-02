#!/usr/bin/env python3
"""Check BUY rows in memory/TRADE-LOG.md for the Confidence and Horizon columns.

Only tables whose header has both columns are checked, so older tables (written before
the columns existed) always pass. Standard library only.

    python3 scripts/check_trade_log.py                    # whole log
    python3 scripts/check_trade_log.py --since 2026-11-02 # just rows on/after a date

Exit code 0 = fine, 1 = at least one BUY row has a missing or malformed value.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

DEFAULT_LOG = Path(__file__).resolve().parents[1] / "memory" / "TRADE-LOG.md"
HORIZON = re.compile(r"^\d+\s*[dwm]$", re.IGNORECASE)
CONFIDENCE = re.compile(r"^(\d{1,3})\s*%?$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass
class Problem:
    line_no: int
    message: str


@dataclass
class Report:
    checked: int = 0  # BUY rows in tables that have the new columns
    legacy: int = 0  # BUY rows in older tables (no columns; not checked)
    problems: list[Problem] | None = None


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def plain(text: str) -> str:
    return re.sub(r"[*`]", "", text).strip()


def check(text: str, since: str | None = None) -> Report:
    report = Report(problems=[])
    header: list[str] | None = None
    for no, line in enumerate(text.splitlines(), start=1):
        if not line.lstrip().startswith("|"):
            header = None
            continue
        row = cells(line)
        lowered = [c.lower() for c in row]
        if "ticker" in lowered and "side" in lowered:
            header = lowered
            continue
        if header is None or set("".join(row)) <= set("-: ") or len(row) != len(header):
            continue
        data = dict(zip(header, row))
        if not plain(data.get("side", "")).upper().startswith("BUY"):
            continue
        day = plain(data.get("date", ""))
        if since and DATE.match(day) and day < since:
            continue
        if "confidence" not in data or "horizon" not in data:
            report.legacy += 1
            continue
        report.checked += 1
        ticker = plain(data.get("ticker", "?"))
        conf = plain(data["confidence"])
        m = CONFIDENCE.match(conf)
        if not m or not 0 <= int(m.group(1)) <= 100:
            report.problems.append(Problem(no, f"{day} {ticker}: confidence should be 0-100, got {conf!r}"))
        horizon = plain(data["horizon"])
        if not HORIZON.match(horizon):
            report.problems.append(Problem(no, f"{day} {ticker}: horizon should look like 10d / 3w / 2m, got {horizon!r}"))
    return report


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("path", nargs="?", default=str(DEFAULT_LOG))
    p.add_argument("--since", help="only check rows dated on/after YYYY-MM-DD")
    args = p.parse_args(argv)
    if args.since and not DATE.match(args.since):
        p.error("--since must be YYYY-MM-DD")
    report = check(Path(args.path).read_text(encoding="utf-8"), args.since)
    for prob in report.problems:
        print(f"line {prob.line_no}: {prob.message}")
    print(f"{report.checked} BUY rows checked, {report.legacy} older rows without the columns (skipped), "
          f"{len(report.problems)} problems.")
    return 1 if report.problems else 0


if __name__ == "__main__":
    sys.exit(main())
