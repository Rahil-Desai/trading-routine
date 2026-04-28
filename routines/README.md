# Cloud Routine Prompts

These prompts are pasted verbatim into Claude Code cloud routines. Five routines fire on weekdays.

| File | Cron (America/Chicago) | Description |
|------|------------------------|-------------|
| pre-market.md | `0 6 * * 1-5` | 6:00 AM -- research catalysts, write trade ideas |
| market-open.md | `30 8 * * 1-5` | 8:30 AM -- execute planned trades, set stops |
| midday.md | `0 12 * * 1-5` | 12:00 PM -- scan positions, cut losers, tighten stops |
| daily-summary.md | `0 15 * * 1-5` | 3:00 PM -- EOD snapshot, daily ClickUp message |
| weekly-review.md | `0 16 * * 5` | 4:00 PM Fridays -- weekly stats, grade, lessons |

Setup: see Part 7 of the setup guide. Key prereqs:
1. Install Claude GitHub App on this repo
2. Enable "Allow unrestricted branch pushes" on each routine
3. Set all env vars on the routine (NOT in .env)
