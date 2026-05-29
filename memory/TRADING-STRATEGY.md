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
2. STAY DEPLOYED: 90-100% target, hard floor 85%. Idle cash beyond one trading day with an open slot is a rule violation, not caution. Every session with cash > 15% must either deploy or log a specific blocking reason.
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

## Entry Checklist
- Specific catalyst? (earnings, breakout, rotation, news)
- Relative strength -- is it outperforming the S&P?
- Sector/theme in momentum?
- Stop level (7-12% below entry by volatility)
- Target (min 2:1 R:R)
