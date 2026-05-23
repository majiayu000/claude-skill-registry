---
name: earnings-orchestrator
description: Master orchestrator for batch earnings analysis
# No context: fork - orchestrator is always entry point, enables Task tool for parallel execution
allowed-tools:
  - Task
  - TaskCreate
  - TaskList
  - TaskGet
  - TaskUpdate
  - Bash
  - Write
  - Read
  - Edit
  - EnterPlanMode
  - ExitPlanMode
permissionMode: dontAsk
---

# Earnings Orchestrator

## Input

`$ARGUMENTS` = `TICKER`

- TICKER: Company ticker (required)

## Task - MUST COMPLETE ALL STEPS

### Step 1: Get Earnings Data

```bash
source /home/faisal/EventMarketDB/venv/bin/activate && python /home/faisal/EventMarketDB/scripts/earnings/get_earnings.py {TICKER}
```

**Output columns:** accession|date|fiscal_year|fiscal_quarter|market_session|daily_stock|daily_adj|sector_adj|industry_adj|trailing_vol|vol_days|vol_status

**Parse:** Extract E1 (first data row after header), E2 (second data row after header). The script returns data sorted oldest-to-newest, so E1 is the OLDEST quarter, E2 is the second oldest. Only process these two quarters. Note `trailing_vol` for each.

**If ERROR returned:** Stop and report error to user.

### Step 1b: Check News Cache

Check `earnings-analysis/news_processed.csv` for {TICKER}.

- Read CSV (format: `ticker|quarter|fiscal_year|processed_date`)
- Find row where `ticker={TICKER}` AND `quarter={E1.fiscal_quarter}` AND `fiscal_year=FY{E1.fiscal_year}`
- If row exists → Q1 already done, skip Steps 2-3b entirely
- If no matching row → continue to Step 2
- Repeat check for Q2

### Step 2: Get Significant Moves for Q1

Calculate:
- `START` = E1 date minus 3 months (or earliest available data)
- `END` = E1 date (just the date part, e.g., 2024-02-01)

```bash
source /home/faisal/EventMarketDB/venv/bin/activate && python /home/faisal/EventMarketDB/scripts/earnings/get_significant_moves.py {TICKER} {START} {END} {E1.trailing_vol}
```

**Output columns:** date|daily_stock|daily_macro|daily_adj

**Parse:** List of dates with significant moves.

**If OK|NO_MOVES returned:** No significant moves for Q1, skip to Step 4.

### Step 3: Concurrent News Analysis for Q1 (BZ → WEB → PPX)

**Phase 1: Create and spawn BZ agents**

For EACH significant date from Step 2:

1. **Create a task** via TaskCreate:
   - `subject`: `"BZ-{QUARTER} {TICKER} {DATE}"` (e.g., "BZ-Q4_FY2022 NOG 2023-01-03")
   - `description`: `"pending"`
   - `activeForm`: `"Analyzing {TICKER} {DATE}"`

2. **Spawn sub-agent** with the task ID and QUARTER:
   ```
   subagent_type: "news-driver-bz"
   description: "BZ news {TICKER} {DATE}"
   prompt: "{TICKER} {DATE} {DAILY_STOCK} {DAILY_ADJ} TASK_ID={N} QUARTER={E1.fiscal_quarter}_FY{E1.fiscal_year}"
   ```

**IMPORTANT:**
- Create ALL tasks first, THEN spawn ALL sub-agents in parallel (one per date, no cap)
- Sub-agents store results in their task via TaskUpdate
- Sub-agents create WEB-* tasks via TaskCreate if they need external research
- DO NOT WAIT for BZ agents to complete - proceed immediately to Phase 2

**Phase 2: Concurrent escalation loop**

Immediately after spawning BZ agents, enter this loop. DO NOT wait for BZ agents first:

```
WHILE any Q1 tasks (BZ-*, WEB-*, PPX-*) are pending or in_progress:
  1. Check TaskList for pending WEB-{QUARTER} {TICKER} tasks
     → For each pending WEB task (if not already spawned):
       - Read task description: "{TICKER} {DATE} {DAILY_STOCK} {DAILY_ADJ}"
       - Extract QUARTER from task subject (e.g., "WEB-Q1_FY2024 AAPL 2024-01-02" → Q1_FY2024)
       - Spawn:
         subagent_type: "news-driver-web"
         prompt: "{TICKER} {DATE} {DAILY_STOCK} {DAILY_ADJ} TASK_ID={task ID} QUARTER={QUARTER}"
     → WEB agents update their task via TaskUpdate
     → WEB agents create PPX-* tasks via TaskCreate if confidence < 50

  2. Check TaskList for pending PPX-{QUARTER} {TICKER} tasks
     → For each pending PPX task (if not already spawned):
       - Read task description: "{TICKER} {DATE} {DAILY_STOCK} {DAILY_ADJ}"
       - Spawn:
         subagent_type: "news-driver-ppx"
         prompt: "{TICKER} {DATE} {DAILY_STOCK} {DAILY_ADJ} TASK_ID={task ID}"
     → PPX agents update their task via TaskUpdate (final tier)

  3. Brief pause (2-3 seconds), then repeat
END WHILE
```

Track which task IDs you've already spawned agents for to avoid duplicates.

**Phase 3: Collect all results**

When all Q1 tasks are completed, collect results via TaskGet for each task. Read the `description` field — it contains the 10-field pipe-delimited result line.

**Merge results:** For each date, use the LAST tier's result (PPX > WEB > BZ).

### Step 3b: Save Q1 Results

1. Create directory if needed: `earnings-analysis/Companies/{TICKER}/`
2. Append Q1 results to `earnings-analysis/Companies/{TICKER}/news.csv`:
   - Add `quarter` column with value `{E1.fiscal_quarter}_FY{E1.fiscal_year}` (e.g., `Q1_FY2024`)
   - Format: `quarter|date|news_id|driver|confidence|daily_stock|daily_adj|market_session|source|external_research|source_pub_date`
   - Create file with header if it doesn't exist
3. Update `earnings-analysis/news_processed.csv`:
   - Format: `ticker|quarter|fiscal_year|processed_date`
   - Append row: `{TICKER}|{E1.fiscal_quarter}|FY{E1.fiscal_year}|{today YYYY-MM-DD}`
   - Create file with header if it doesn't exist

### Step 4: Concurrent News Analysis for Q2 (BZ → WEB → PPX)

Calculate:
- `START` = E1 date + 1 day (exclude E1 earnings reaction)
- `END` = E2 date (exclusive, excludes E2 earnings reaction)

Run `get_significant_moves.py {TICKER} {START} {END} {E2.trailing_vol}` then follow the same concurrent pattern as Step 3:
- Phase 1: Create BZ-{Q2 QUARTER} tasks, spawn news-driver-bz agents in parallel
- Phase 2: Concurrent escalation loop for WEB-{Q2 QUARTER} and PPX-{Q2 QUARTER} tasks
- Phase 3: Collect all Q2 results when complete

Use `QUARTER={E2.fiscal_quarter}_FY{E2.fiscal_year}` for all Q2 tasks.

### Step 4b: Save Q2 Results

Same as Step 3b but for Q2:
1. Append to `earnings-analysis/Companies/{TICKER}/news.csv` with `quarter={E2.fiscal_quarter}_FY{E2.fiscal_year}`
2. Append to `news_processed.csv`: `{TICKER}|{E2.fiscal_quarter}|FY{E2.fiscal_year}|{today YYYY-MM-DD}`

### Step 5: Return Combined Results

```
=== EARNINGS ORCHESTRATOR: {TICKER} ===

--- EARNINGS DATA ---
E1: {accession} | {date} | FY{fiscal_year} {fiscal_quarter} | {daily_adj}% adj | vol={trailing_vol}% ({vol_days}d) {vol_status}
E2: {accession} | {date} | FY{fiscal_year} {fiscal_quarter} | {daily_adj}% adj | vol={trailing_vol}% ({vol_days}d) {vol_status}
...

--- Q1 ANALYSIS ({START} to {E1}) ---
Filter: |stock|>=4%, |adj|>=max(2×{trailing_vol}%,3%)
Significant dates: {count}

date|news_id|driver|confidence|daily_stock|daily_adj|market_session|source|external_research|source_pub_date
...

--- Q2 ANALYSIS ({E1} to {E2}) ---
Filter: |stock|>=4%, |adj|>=max(2×{trailing_vol}%,3%)
Significant dates: {count}

date|news_id|driver|confidence|daily_stock|daily_adj|market_session|source|external_research|source_pub_date
...

--- SUMMARY ---
Total dates analyzed: {N}
Explained by Benzinga: {B}
Explained by WebSearch: {W}
Explained by Perplexity: {P}
Still unknown (confidence=0): {U}

=== COMPLETE ===
```

## Rules

- **Full row replacement** - When a later tier returns a result, use its COMPLETE 10-field output. PPX replaces WEB, WEB replaces BZ. Never mix fields across tiers.
- **Always run get_earnings.py first** - provides trailing_vol for each quarter
- **Skip if done** - check news_processed.csv, skip quarters already processed
- **All sub-agents in parallel** - spawn one per date, no cap
- **Q1 complete before Q2** - finish all 3 tiers (BZ → WEB → PPX) + save for Q1, then Q2
- **Extract date only** - E1 date "2024-02-01T16:30:33-05:00" → use "2024-02-01"
- **Preserve news_id EXACTLY** - Copy URLs verbatim. NEVER shorten, summarize, or create short IDs. If sub-agent returns a URL, save the full URL exactly as returned.
- **Pass through raw output** - don't summarize or lose data
- **Always save results** - append to news.csv and mark done in news_processed.csv

## Error Handling

Script errors return structured format: `ERROR|CODE|MESSAGE|HINT`

If any script returns ERROR:
1. Log the error in output
2. Try to continue with remaining steps if possible
3. Report all errors in summary

## Example

Input: `AAPL`

Flow:
1. get_earnings.py AAPL → E1=2024-02-01 (Q1_FY2024, vol=0.90), E2=2024-05-02 (Q2_FY2024, vol=0.99)
2. Check news_processed.csv → no row for AAPL|Q1|FY2024 → process Q1
3. get_significant_moves.py AAPL 2023-11-01 2024-02-01 0.90 → internally: |stock|>=4%, |adj|>=max(2×0.90,3)=3%
4. Spawn news-driver-bz for each significant date → some explained, some create WEB tasks
5. Spawn news-driver-web for each WEB task → some explained, some create PPX tasks
6. Spawn news-driver-ppx for each PPX task → returns results (final tier)
7. Save Q1 to Companies/AAPL/news.csv, mark Q1_FY2024 done
8. Check news_processed.csv → row exists for AAPL|Q2|FY2024 → skip Q2
9. Return results (Q1 only, Q2 was cached)
