# Trading Strategy

## Mission
Beat the S&P 500 over the challenge window. Stocks only -- no options, ever.
Beating the index means OUT-returning it -- holding index-proxy ETFs or megacaps that track the S&P cannot win. Concentrate in higher-beta leaders, stay fully deployed, and keep capital working.

## Capital & Constraints
- Starting capital: ~$100,000
- Platform: Alpaca
- Instruments: Stocks ONLY
- PDT limit: 3 day trades per 5 rolling days (account < $25k). Swing entries held overnight are NOT day trades and do not consume the PDT budget -- this is not a reason to under-trade.

## Core Rules
1. NO OPTIONS -- ever.
2. STAY DEPLOYED: 90-100% target, hard floor 85%. Idle cash > 15% past ONE trading day = mandatory deploy on the next session, not a logged exception. The previous "log a specific blocking reason" loophole is removed -- a session with cash > 15% may not roll forward without a placed order.
3. 5-8 positions at a time. Max 25% per position (highest-conviction only; typical 15-20%).
4. Up to 6 new trades per week (PDT only limits same-day round-trips, not swings).
5. Bias to ACTION: take the best available setup each week. A good setup at full deployment beats a perfect setup left in cash. Don't wait for certainty.
6. Hunt alpha in individual leaders: earnings breakouts, sector leaders, relative-strength names outperforming the S&P. Broad/sector ETFs are a fast deployment vehicle only -- never the core book.
7. 10% trailing stop on every position as a real GTC order (up to 12% for high-beta names to avoid noise stop-outs). Stops are the risk control -- they are non-negotiable.
8. Cut losers at -7% manually.
9. Tighten trail: 7% at +15%, 5% at +20%.
10. Never within 3% of current price; never move a stop down.
11. Rotate fast: exit dead money (flat laggards, stalled/broken theses) to free capital for stronger setups. Don't let slots rot.
12. Follow sector AND single-name momentum. Exit a sector after 2 consecutive failed trades.
13. Max 30% of book per GICS sector (added 2026-05-29 after 5 consecutive weeks of energy-concentration paralysis). Sector ETFs count fully toward their sector; megacap proxies (e.g. XOM under Energy, NVDA under Tech) count toward the underlying sector even when held as singles. Breach = trim on next strength to reach compliance; no add that would lift a sector above 30%.
14. TRIM-INTO-STRENGTH (added 2026-07-03 after 8 consecutive weeks of the same paragraph in the weekly review and MTUM +8.66% Tue -> +0.30% Thu round-trip on week 9). Two independent triggers, either fires the trim:
    - Any single position at +15% unrealized (regardless of book %): trim 25-50% same session as the +15% print. Pairs with rule 9's +15% trail tighten -- the tighten locks the floor, the trim locks the cash.
    - Any single position drifted over 25% of book AND carrying >+5% unrealized: trim 25-50% same session as the cap breach is observed at EOD or midday.
    - Trim executes SAME SESSION as trigger. No "wait for confirmation," no "next-day," no "if it holds." Pre-write the exact share count Sunday research time for any position within 3pp of a trigger threshold.
    - Trim proceeds fund next high-conviction single-name leader add per rule 6 (not automatic re-deploy to ETF).

## Entry Checklist
- Specific catalyst? (earnings, breakout, rotation, news)
- Relative strength -- is it outperforming the S&P?
- Sector/theme in momentum?
- Stop level (7-12% below entry by volatility)
- Target (min 2:1 R:R)
