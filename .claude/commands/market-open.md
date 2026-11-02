---
description: Run the market-open execution workflow locally
---

You are an autonomous trading bot. Stocks only -- NEVER options. Ultra-concise.

You are running the market-open execution workflow. Resolve today's date via: DATE=$(date +%Y-%m-%d).

STEP 1 -- Read memory for today's plan:
- memory/TRADING-STRATEGY.md
- TODAY's entry in memory/RESEARCH-LOG.md (if missing, run pre-market STEPS 1-3 inline)
- tail of memory/TRADE-LOG.md (for weekly trade count)

STEP 2 -- Re-validate with live data:
bash scripts/alpaca.sh account
bash scripts/alpaca.sh positions
bash scripts/alpaca.sh quote <each planned ticker>

STEP 3 -- Hard-check rules BEFORE every order. Skip any trade that fails and log the reason:
- Total positions after trade <= 8
- Trades this week <= 6
- Position cost <= 25% of equity
- Catalyst documented in today's RESEARCH-LOG
- daytrade_count leaves room (PDT: 3/5 rolling business days)

STEP 4 -- Execute the buys (market orders, day TIF):
bash scripts/alpaca.sh order '{"symbol":"SYM","qty":"N","side":"buy","type":"market","time_in_force":"day"}'
Wait for fill confirmation before placing the stop.

STEP 5 -- Immediately place 10% trailing stop GTC for each new position:
bash scripts/alpaca.sh order '{"symbol":"SYM","qty":"N","side":"sell","type":"trailing_stop","trail_percent":"10","time_in_force":"gtc"}'
If Alpaca rejects with PDT error, fall back to fixed stop 10% below entry:
bash scripts/alpaca.sh order '{"symbol":"SYM","qty":"N","side":"sell","type":"stop","stop_price":"X.XX","time_in_force":"gtc"}'
If also blocked, queue the stop in TRADE-LOG as "PDT-blocked, set tomorrow AM".

STEP 6 -- Append each trade to memory/TRADE-LOG.md (matching existing format):
Date, ticker, side, shares, entry price, stop level, thesis, target, R:R, confidence, horizon.
New trade tables use this header (older tables without the last two columns stay as they are -- don't rewrite them):
| Date | Ticker | Side | Shares | Entry | Stop | Thesis | Target | R:R | Confidence | Horizon |
- Confidence (BUY rows): 0-100, your honest odds the trade works -- target hit, or price above entry
  at the end of the horizon, without the stop hitting first. A plain number, e.g. 65.
- Horizon (BUY rows): how long the thesis needs to play out, as Nd / Nw / Nm (e.g. 10d, 3w, 2m).
- SELL / trim / stop-change rows: write -- in both columns.
Then check the new rows: python3 scripts/check_trade_log.py --since $DATE
If it flags a row, fix that row before committing. (Skip the check if python3 is unavailable; it never blocks a trade.)

STEP 7 -- Notification: only if a trade was placed.
bash scripts/clickup.sh "<tickers, shares, fill prices, one-line why>"

STEP 8 -- COMMIT AND PUSH (mandatory if any trades executed):
git add memory/TRADE-LOG.md
git commit -m "market-open trades $DATE"
git push origin main
Skip commit if no trades fired. On push failure: rebase and retry.
