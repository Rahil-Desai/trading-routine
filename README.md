# trading-routine

## Trade log columns

New BUY rows in `memory/TRADE-LOG.md` carry two extra columns, so trades can be graded and
reviewed for calibration by [Trade Thesis Journal](https://github.com/Rahil-Desai/trade-thesis-journal):

| Column | Meaning | Example |
| --- | --- | --- |
| Confidence | 0-100, odds the trade works (target hit, or above entry at the end of the horizon, without the stop hitting first) | `65` |
| Horizon | How long the thesis needs to play out: `Nd`, `Nw` or `Nm` | `3w` |

Older tables without these columns are left as they are and still parse.
Check the log with `python3 scripts/check_trade_log.py [--since YYYY-MM-DD]`.
Run its tests with `python3 -m unittest discover -s tests`.
