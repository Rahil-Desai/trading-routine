#!/usr/bin/env python3
"""Find BUY/SELL rows in memory/TRADE-LOG.md that log the same fill more than once.

Two rows are the same fill when date, ticker, side (BUY/SELL), shares and price (to the cent)
all match. Standard library only.

    python3 scripts/trade_log_dupes.py                           # every duplicate in the log
    python3 scripts/trade_log_dupes.py --baseline-ref origin/main # only duplicates NEW vs main

Use --baseline-ref before committing: older duplicates already on main are history and are
never edited; the check only stops a run from adding another copy. Exit code 1 = duplicates found.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = "memory/TRADE-LOG.md"
PRICE = re.compile(r"\$\s*([0-9][0-9,]*\.?[0-9]*)")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PRICE_COLS = ("entry", "entry (avg)", "price", "fill", "exit")

Key = tuple  # (date, ticker, side, shares, price)


def _plain(s: str) -> str:
    return re.sub(r"[*`]", "", s).strip()


def fills(text: str) -> dict[Key, list[int]]:
    """Map each fill key to the line numbers that log it."""
    out: dict[Key, list[int]] = defaultdict(list)
    header: list[str] | None = None
    for no, line in enumerate(text.splitlines(), start=1):
        if not line.lstrip().startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        lowered = [c.lower() for c in cells]
        if "ticker" in lowered and "side" in lowered:
            header = lowered
            continue
        if header is None or len(cells) != len(header):
            continue
        row = dict(zip(header, cells))
        day = _plain(row.get("date", ""))
        side_words = _plain(row.get("side", "")).upper().split()
        if not DATE.match(day) or not side_words or side_words[0] not in ("BUY", "SELL"):
            continue
        shares = _plain(row.get("shares", "")).replace(",", "")
        price_cell = next((row[c] for c in PRICE_COLS if c in row and PRICE.search(row[c])), None)
        if not shares.isdigit() or price_cell is None:
            continue  # can't identify the fill reliably; leave it alone
        price = round(float(PRICE.search(price_cell).group(1).replace(",", "")), 2)
        out[(day, _plain(row["ticker"]).upper(), side_words[0], int(shares), price)].append(no)
    return out


def duplicates(text: str, baseline: str | None = None) -> dict[Key, list[int]]:
    """Fills logged more than once. With a baseline, only fills logged MORE times than in the baseline."""
    now = fills(text)
    before = fills(baseline) if baseline is not None else {}
    return {k: v for k, v in now.items() if len(v) > 1 and len(v) > len(before.get(k, []))}


def read_ref(ref: str, path: str = LOG) -> str:
    return subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT, check=True, capture_output=True, text=True).stdout


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("path", nargs="?", default=str(ROOT / LOG))
    p.add_argument("--baseline-ref", help="git ref to compare against, e.g. origin/main")
    p.add_argument("--baseline", help="file to compare against (instead of a git ref)")
    args = p.parse_args(argv)
    text = Path(args.path).read_text(encoding="utf-8")
    baseline = None
    if args.baseline:
        baseline = Path(args.baseline).read_text(encoding="utf-8")
    elif args.baseline_ref:
        baseline = read_ref(args.baseline_ref)
    dups = duplicates(text, baseline)
    for (day, ticker, side, shares, price), lines in sorted(dups.items()):
        print(f"{day} {side} {shares} {ticker} @ ${price:g} is logged {len(lines)}x (lines {', '.join(map(str, lines))})")
    scope = "new " if baseline is not None else ""
    print(f"{len(dups)} {scope}duplicated fills.")
    if dups and baseline is not None:
        print("Remove the row(s) you just added; never edit rows that are already on main.")
    return 1 if dups else 0


if __name__ == "__main__":
    sys.exit(main())
