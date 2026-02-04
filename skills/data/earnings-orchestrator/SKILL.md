---
name: earnings-orchestrator
description: Master orchestrator for batch earnings analysis
# No context: fork - orchestrator is always entry point, enables Task tool for orchestration
allowed-tools:
  - Task
  - TaskCreate
  - TaskList
  - TaskGet
  - TaskUpdate
  - Skill
  - Bash
  - Write
  - Read
  - Edit
  - EnterPlanMode
  - ExitPlanMode
permissionMode: dontAsk
hooks:
  PreToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "/home/faisal/EventMarketDB/.claude/hooks/validate_processed_guard.sh"
        - type: command
          command: "/home/faisal/EventMarketDB/.claude/hooks/validate_guidance_header.sh"
        - type: command
          command: "/home/faisal/EventMarketDB/.claude/hooks/validate_ok_marker.sh"
    - matcher: "TaskUpdate"
      hooks:
        - type: command
          command: "/home/faisal/EventMarketDB/.claude/hooks/guard_task_delete.sh"
    - matcher: Bash
      hooks:
        - type: command
          command: "/home/faisal/EventMarketDB/.claude/hooks/block_bash_guard.sh"
  PostToolUse:
    - matcher: Bash
      hooks:
        - type: command
          command: "/home/faisal/EventMarketDB/.claude/hooks/build-thinking-on-complete.sh"
---

# Earnings Orchestrator

## Input

`$ARGUMENTS` = `TICKER`

- TICKER: Company ticker (required)

## Task - MUST COMPLETE ALL STEPS

### Step 0: Record Start Time

```bash
echo "=== START: $(date '+%Y-%m-%d %H:%M:%S') ==="
```

### Step 1: Get Earnings Data

```bash
source /home/faisal/EventMarketDB/venv/bin/activate && python /home/faisal/EventMarketDB/scripts/earnings/get_earnings.py {TICKER}
```

**Output columns:** accession|date|fiscal_year|fiscal_quarter|market_session|daily_stock|daily_adj|sector_adj|industry_adj|trailing_vol|vol_days|vol_status|fye_month

**Parse:** Extract E1 (first data row after header), E2 (second data row after header). The script returns data sorted oldest-to-newest, so E1 is the OLDEST quarter, E2 is the second oldest. **Single-quarter mode:** only process one quarter per run (E1 unless fully cached). Note `trailing_vol` and `fye_month` for each. The `fye_month` (1-12) indicates the company's fiscal year end month (e.g., 9=September for Apple, 12=December for most companies).

**If ERROR returned:** Stop and report error to user.

### Step 1b: Check Processing Cache

Check both `earnings-analysis/news_processed.csv` and `earnings-analysis/guidance_processed.csv` for {TICKER}.

**News cache:** (format: `ticker|quarter|fiscal_year|processed_date`)
- Find row where `ticker={TICKER}` AND `quarter={E1.fiscal_quarter}` AND `fiscal_year=FY{E1.fiscal_year}`
- If row exists → `Q1_NEWS_CACHED=true`
- Repeat check for Q2 → `Q2_NEWS_CACHED`

**Guidance cache:** (format: `ticker|quarter|fiscal_year|processed_date`)
- Find row where `ticker={TICKER}` AND `quarter={E1.fiscal_quarter}` AND `fiscal_year=FY{E1.fiscal_year}`
- If row exists → `Q1_GUIDANCE_CACHED=true`
- Repeat check for Q2 → `Q2_GUIDANCE_CACHED`

**Skip logic for each quarter:**
| Q1_NEWS_CACHED | Q1_GUIDANCE_CACHED | Action |
|----------------|-------------------|--------|
| false | false | Run full Steps 2, 3, 3b for Q1 (both tracks) |
| true | false | Skip news in Steps 2, 3, 3b; run guidance only |
| false | true | Skip guidance in Steps 2, 3, 3b; run news only |
| true | true | **Skip Steps 2, 3, 3b entirely for Q1** → go to Step 4 |

Same logic applies to Q2 with Steps 4, 4b.

### Step 1c: Select Target Quarter (Single-Quarter Mode)

**Goal:** Process only one quarter per run.

Rules:
- If **Q1 is NOT fully cached** (Q1_NEWS_CACHED=false OR Q1_GUIDANCE_CACHED=false) → set `TARGET=Q1` and **process ONLY Q1**.
- Else if **Q2 is NOT fully cached** → set `TARGET=Q2` and **process ONLY Q2**.
- Else → **STOP** (nothing to do).

This ensures the run advances to the next quarter only after the previous quarter is fully processed.

**If TARGET=Q1, do NOT proceed past Step 3b. Stop the run after Q1 save.**

### Step 2: Discovery for Q1 (News + Guidance)

**Only run Step 2–3b if TARGET=Q1.** If TARGET=Q2, skip directly to Step 4.

Calculate:
- `START` = E1 date minus 3 months (no further adjustment; scripts handle empty ranges)
- `END` = E1 date (just the date part, e.g., 2024-02-01)

**Run discovery scripts (only for non-cached tracks; sequential OK):**

```bash
# News discovery (SKIP if Q1 news cached)
source /home/faisal/EventMarketDB/venv/bin/activate && python /home/faisal/EventMarketDB/scripts/earnings/get_significant_moves.py {TICKER} {START} {END} {E1.trailing_vol}

# Guidance discovery - all 5 (SKIP ALL if Q1 guidance cached)
source /home/faisal/EventMarketDB/venv/bin/activate && python /home/faisal/EventMarketDB/scripts/earnings/get_8k_filings_range.py {TICKER} {START} {END}
source /home/faisal/EventMarketDB/venv/bin/activate && python /home/faisal/EventMarketDB/scripts/earnings/get_10k_filings_range.py {TICKER} {START} {END}
source /home/faisal/EventMarketDB/venv/bin/activate && python /home/faisal/EventMarketDB/scripts/earnings/get_10q_filings_range.py {TICKER} {START} {END}
source /home/faisal/EventMarketDB/venv/bin/activate && python /home/faisal/EventMarketDB/scripts/earnings/get_transcript_range.py {TICKER} {START} {END}
source /home/faisal/EventMarketDB/venv/bin/activate && python /home/faisal/EventMarketDB/scripts/earnings/get_guidance_news_range.py {TICKER} {START} {END}
```

**Cache-aware execution:** (based on Step 1b flags)
- If `Q1_NEWS_CACHED=true` → skip `get_significant_moves.py`
- If `Q1_GUIDANCE_CACHED=true` → skip all 5 guidance discovery scripts
- If both cached → skip Steps 2, 3, 3b entirely for Q1

**Parse news results:**
- `get_significant_moves.py` output columns: date|daily_stock|daily_macro|daily_adj
- Parse: List of dates with significant moves

**Parse guidance results (content-level sources):**
All 5 discovery scripts return the SAME format: `report_id|date|source_type|source_key`

- `get_8k_filings_range.py` → 8-K content (source_type: exhibit, section, filing_text)
- `get_10k_filings_range.py` → 10-K content (source_type: exhibit, section, filing_text, financial_stmt, xbrl)
- `get_10q_filings_range.py` → 10-Q content (source_type: exhibit, section, filing_text, financial_stmt, xbrl)
- `get_transcript_range.py` → Transcripts (source_type: transcript, source_key: full)
- `get_guidance_news_range.py` → News (source_type: news, source_key: full)

**Combine all guidance sources into a single list.** Each line is one content source to process. Parse uniformly - no special handling needed.

**If OK|NO_MOVES returned:** No significant moves for Q1 news, skip news tasks but still process guidance if sources found.

### Step 3: Foreground Analysis for Q1 (News + Guidance)

**Phase 1: Create tasks upfront (only for non-cached tracks)**

**NEWS TASKS (with blockedBy dependencies) - SKIP if `Q1_NEWS_CACHED=true`:**
For EACH significant date from Step 2, create all 4 tasks with dependency chain:

1. **Create BZ task** via TaskCreate:
   - `subject`: `"BZ-{QUARTER} {TICKER} {DATE}"` (e.g., "BZ-Q4_FY2022 NOG 2023-01-03")
   - `description`: `"pending"`
   - `activeForm`: `"Analyzing {TICKER} {DATE}"`
   - Note the task ID as `BZ_ID`

2. **Create WEB task** via TaskCreate:
   - `subject`: `"WEB-{QUARTER} {TICKER} {DATE}"`
   - `description`: `"{TICKER} {DATE} {DAILY_STOCK} {DAILY_ADJ}"`
   - `activeForm`: `"Web research {TICKER} {DATE}"`
   - Then call TaskUpdate with `addBlockedBy: ["{BZ_ID}"]`
   - Note the task ID as `WEB_ID`

3. **Create PPX task** via TaskCreate:
   - `subject`: `"PPX-{QUARTER} {TICKER} {DATE}"`
   - `description`: `"{TICKER} {DATE} {DAILY_STOCK} {DAILY_ADJ}"`
   - `activeForm`: `"Perplexity research {TICKER} {DATE}"`
   - Then call TaskUpdate with `addBlockedBy: ["{WEB_ID}"]`
   - Note the task ID as `PPX_ID`

4. **Create JUDGE task** via TaskCreate:
   - `subject`: `"JUDGE-{QUARTER} {TICKER} {DATE}"`
   - `description`: `"pending"`
   - `activeForm`: `"Validating {TICKER} {DATE}"`
   - Then call TaskUpdate with `addBlockedBy: ["{PPX_ID}"]`
   - Note the task ID as `JUDGE_ID`

**GUIDANCE TASKS (NO dependencies; sequential OK) - SKIP if `Q1_GUIDANCE_CACHED=true`:**

For EACH content source line from guidance discovery (format: `report_id|date|source_type|source_key`), create a task:

- `subject`: `"GX-{QUARTER} {TICKER} {REPORT_ID} {SOURCE_TYPE}"`
  - Pattern: `GX-{quarter} {ticker} {id} {type}` where id format varies by source type
- `description`: `"{REPORT_ID}|{SOURCE_TYPE}|{SOURCE_KEY}"` (store for agent prompt)
- `activeForm`: `"Extracting guidance from {SOURCE_TYPE}"`

**All 7 source types use the same format** - no special handling needed for transcripts or news.

**Phase 1.5: Write manifest (Q1)**
Create directory (if needed):
`earnings-analysis/Companies/{TICKER}/manifests/`
Also create output directories:
- Guidance: `earnings-analysis/Companies/{TICKER}/manifests/{QUARTER}/gx/`
- News judge: `earnings-analysis/Companies/{TICKER}/manifests/{QUARTER}/judge/`

Write manifest file:
`earnings-analysis/Companies/{TICKER}/manifests/{QUARTER}.json`

Format:
```
{
  "ticker": "{TICKER}",
  "quarter": "{E1.fiscal_quarter}_FY{E1.fiscal_year}",
  "generated_at": "{ISO timestamp}",
  "news": {
    "expected_judge": {N},
    "judge_tasks": [
      {"id": "{JUDGE_ID}", "date": "{DATE}"},
      ...
    ]
  },
  "guidance": {
    "expected": {M},
    "tasks": [
      {"id": "{GX_ID}", "report_id": "{REPORT_ID}", "source_type": "{SOURCE_TYPE}", "source_key": "{SOURCE_KEY}"},
      ...
    ]
  }
}
```

If a track is cached, set its expected count to 0 and tasks to [].
This manifest is the **source of truth** for validation and aggregation.

**Phase 2: Spawn agents (only for non-cached tracks, foreground parallel batches)**

⚠️ **CRITICAL: ALL AGENTS MUST RUN IN FOREGROUND** ⚠️
- Do NOT use `run_in_background: true` on ANY Task tool call
- Foreground Task calls can run in parallel **within the same response**. Spawn in batches of **up to 50** Task calls per response, then proceed to the next batch.
- Background mode breaks result collection

⚠️ **CRITICAL: DO NOT SPAWN GUIDANCE-EXTRACT WITHOUT A TASK_ID** ⚠️
- Every guidance source MUST be TaskCreate'd first
- TASK_ID must be the TaskCreate ID for that source (never invent or omit)
- If a TASK_ID is missing, STOP and report the error before spawning

**NEWS: Spawn BZ agents for each significant date - SKIP if `Q1_NEWS_CACHED=true`:**
```
subagent_type: "news-driver-bz"
description: "BZ news {TICKER} {DATE}"
prompt: "{TICKER} {DATE} {DAILY_STOCK} {DAILY_ADJ} TASK_ID={BZ_ID} WEB_TASK_ID={WEB_ID} PPX_TASK_ID={PPX_ID} JUDGE_TASK_ID={JUDGE_ID} QUARTER={E1.fiscal_quarter}_FY{E1.fiscal_year}"
run_in_background: false  # ALWAYS foreground
```

**GUIDANCE: Spawn guidance-extract agents - SKIP if `Q1_GUIDANCE_CACHED=true`** (one per content source, foreground parallel batches of up to 50):

For EACH guidance task, read the description to get `{REPORT_ID}|{SOURCE_TYPE}|{SOURCE_KEY}`, then spawn:

```
subagent_type: "guidance-extract"
description: "Guidance {TICKER} {SOURCE_TYPE}"
prompt: "{TICKER} {REPORT_ID} {SOURCE_TYPE} {SOURCE_KEY} {QUARTER} FYE={fye_month} TASK_ID={TASK_ID}"
run_in_background: false  # ALWAYS foreground
```

**Key variations in prompt format:**
- Filing sources: `{TICKER} {accession} {source_type} {source_key} {QUARTER} FYE={fye_month} TASK_ID={id}`
- Transcript: `{TICKER} {transcript_id} transcript full {QUARTER} FYE={fye_month} TASK_ID={id}`
- News: `{TICKER} {news_id} news full {QUARTER} FYE={fye_month} TASK_ID={id}`

The `fye_month` comes from E1/E2 data (get_earnings.py output). Pass the same value for all guidance tasks of that company.

**IMPORTANT:**
- Create tasks only for non-cached tracks, THEN spawn agents for those tracks in foreground-parallel batches (≤50)
- If only news cached → create + spawn guidance agents only
- If only guidance cached → create + spawn news agents only
- BZ agents mark WEB+PPX as SKIPPED if they find answer (external_research=false)
- Guidance agents have NO dependencies - they complete independently
- After spawning all agents, immediately enter Phase 3 polling loop
- Do NOT proceed to Phase 4 until all relevant tasks are completed

**Phase 3: Escalation loop (foreground) - SKIP if `Q1_NEWS_CACHED=true`**

If `Q1_NEWS_CACHED=false`, immediately after spawning BZ agents, enter this loop:

⚠️ **REMINDER: ALL Task tool calls MUST have `run_in_background: false`** ⚠️

```
WHILE any Q1 tasks (BZ-*, WEB-*, PPX-*, JUDGE-*) are pending or in_progress:
  1. Check TaskList for WEB-{QUARTER} {TICKER} tasks that are:
     - status = "pending" AND blockedBy is empty (auto-unblocked when BZ completed)
     - NOT already spawned
     → For each such WEB task:
       - Get task via TaskGet to read description: "{TICKER} {DATE} {DAILY_STOCK} {DAILY_ADJ}"
       - Extract QUARTER from task subject
       - Find corresponding PPX and JUDGE task IDs from TaskList
       - Spawn (FOREGROUND ONLY):
         subagent_type: "news-driver-web"
         prompt: "{TICKER} {DATE} {DAILY_STOCK} {DAILY_ADJ} TASK_ID={WEB_ID} PPX_TASK_ID={PPX_ID} JUDGE_TASK_ID={JUDGE_ID} QUARTER={QUARTER}"
         run_in_background: false
     → WEB agents mark PPX as SKIPPED if confidence >= 50

  2. Check TaskList for PPX-{QUARTER} {TICKER} tasks that are:
     - status = "pending" AND blockedBy is empty (auto-unblocked when WEB completed)
     - NOT already spawned
     → For each such PPX task:
       - Get task via TaskGet to read description
       - Extract QUARTER from task subject
       - Find corresponding JUDGE task ID from TaskList
       - Spawn (FOREGROUND ONLY):
         subagent_type: "news-driver-ppx"
         prompt: "{TICKER} {DATE} {DAILY_STOCK} {DAILY_ADJ} TASK_ID={PPX_ID} JUDGE_TASK_ID={JUDGE_ID} QUARTER={QUARTER}"
         run_in_background: false
     → PPX agents always update JUDGE with result (final tier)

  3. Check TaskList for JUDGE-{QUARTER} {TICKER} tasks that are:
     - status = "pending" AND blockedBy is empty (auto-unblocked when PPX completed or skipped)
     - NOT already spawned
     - description starts with "READY:" (has result to validate)
     → For each such JUDGE task:
       - Spawn (FOREGROUND ONLY):
         subagent_type: "news-driver-judge"
         prompt: "TASK_ID={JUDGE_ID}"
         run_in_background: false
     → JUDGE agents validate and update task with final confidence

  4. Brief pause (2-3 seconds), then repeat
END WHILE
```

Track which task IDs you've already spawned agents for to avoid duplicates.

**Note on SKIPPED tasks:** When BZ or WEB finds a confident answer, they mark downstream tasks as "completed" with description="SKIPPED: {tier} found answer". This auto-unblocks the next task in chain (JUDGE for BZ skip, JUDGE for WEB skip).

**Phase 4: Collect all results**

**NEWS RESULTS:**
When all Q1 news tasks (BZ-*, WEB-*, PPX-*, JUDGE-*) are completed, collect results from per-task files written by the judge subagents:
`earnings-analysis/Companies/{TICKER}/manifests/{QUARTER}/judge/{TASK_ID}.tsv`

Each file contains a single 12-field line (no header). Do **not** use TaskGet for news results.

**Note:** Each date has exactly one JUDGE task with the final validated result. BZ/WEB/PPX tasks contain intermediate results.

**GUIDANCE RESULTS:**
When all Q1 guidance tasks (GX-*) are completed, collect results from per-task files written by the guidance subagents:
`earnings-analysis/Companies/{TICKER}/manifests/{QUARTER}/gx/{TASK_ID}.tsv`

Each file contains newline-delimited guidance entries in the 18-field format below, or `NO_GUIDANCE|{source_type}|{source_key}`, or `ERROR|...`. **Do not use TaskGet for guidance.**

```
period_type|fiscal_year|fiscal_quarter|segment|metric|low|mid|high|unit|basis|derivation|qualitative|source_type|source_id|source_key|given_date|section|quote
```

**Field definitions:**
- `period_type`: `quarter`, `annual`, `half`, or `long-range`
- `fiscal_year`: e.g., `2025`
- `fiscal_quarter`: `1`, `2`, `3`, `4`, or `.` for annual
- `segment`: `Total` (default), or specific segment like `Services`, `iPhone`, `AWS`
- `metric`: Normalized name like `Revenue`, `EPS`, `Gross Margin`
- `low`, `mid`, `high`: Numbers or `.` for qualitative guidance
- `unit`: `%`, `USD`, `B USD`, `% YoY`, etc.
- `basis`: `GAAP`, `non-GAAP`, `as-reported`, etc.
- `derivation`: `explicit`, `calculated` (mid derived), `point`, or `implied` (qualitative only)
- `qualitative`: Non-numeric guidance text (e.g., "double digits") or `.`
- `source_type`, `source_id`, `source_key`: Source identification
- `given_date`: When guidance was issued (YYYY-MM-DD)
- `section`: Location in source (e.g., "CFO prepared remarks", "Outlook section")
- `quote`: Exact text with pipes replaced by ¦

Or `NO_GUIDANCE|{source_type}|{source_key}` if no guidance found in that source.

**Note:** Guidance tasks have no dependencies and complete independently of news tasks.

**Phase 4.5: Validation gate (MANDATORY, before Step 3b)**

**Fresh session rule (context saver):** Run Phase 4.5 + saving results in a **new session** using the same `CLAUDE_CODE_TASK_LIST_ID`. This avoids carrying the full spawn-phase context into validation.

Load the Q1 manifest from:
`earnings-analysis/Companies/{TICKER}/manifests/{QUARTER}.json`

Validation rules:
- For each `news.judge_tasks` ID:
  - Read file: `earnings-analysis/Companies/{TICKER}/manifests/{QUARTER}/judge/{TASK_ID}.tsv`
  - If file missing: mark missing
  - Must be a single 12-field pipe-delimited line
- For each `guidance.tasks` ID:
  - Read file: `earnings-analysis/Companies/{TICKER}/manifests/{QUARTER}/gx/{TASK_ID}.tsv`
  - If file missing: mark missing
  - For each non-empty line:
    - If line starts with `NO_GUIDANCE|` → skip
    - If line starts with `ERROR|` → invalid (retry)
    - Else must have **18 fields**
  - If file is empty/invalid: log it, add to retry file, and **do NOT** mark processed.

**Counting rule (no headers):**
- Per-task files (`gx/*.tsv` and `judge/*.tsv`) never include headers.
- If you sanity-check counts, count only `*.tsv` files and compare to manifest IDs.
- Do **not** add +1 for headers or count directories.

**Hard stop rule (fail-closed):**
- If any expected guidance file is missing, or any required judge file is missing, **STOP immediately**.
- Write a retry file (if needed) and **do NOT** write `guidance.csv`, `.ok`, or processed caches.
- Do **NOT** attempt to reconstruct results from memory/Neo4j.

**Best-effort mode (deterministic):**
- If any task is missing or invalid, **do NOT** stop the run (unless the hard stop rule above applies).
- Write a retry file listing only the failed task IDs:
  `earnings-analysis/Companies/{TICKER}/manifests/{QUARTER}.retry.json`
  Format: `{"failed":[{"id":"123","reason":"invalid_format"}, ...]}`
- Proceed to Step 3b and write **all valid rows**.
- **Do NOT** update processed caches unless there are **zero** failed tasks.

Only create the `.ok` marker when there are **zero** failed tasks. Processed CSV updates require the `.ok` marker; the retry file never unlocks processing.
**Use the Write tool (not Bash redirection) for `.ok` and processed CSVs** so hooks can enforce guards.
If **no** tasks are missing/invalid:
- Create marker file: `earnings-analysis/Companies/{TICKER}/manifests/{QUARTER}.ok`
  (This marker is required to unlock processed CSV updates.)

### Step 3b: Save Q1 Results

**NEWS RESULTS:**
Write all valid rows. If retry file exists, do NOT update processed cache.
Source of truth: per-task files in `earnings-analysis/Companies/{TICKER}/manifests/{QUARTER}/judge/`.
For each judge task ID in the manifest, read `{TASK_ID}.tsv` and append the 12-field line.
1. Create directory if needed: `earnings-analysis/Companies/{TICKER}/`
2. Append Q1 results to `earnings-analysis/Companies/{TICKER}/news.csv`:
   - Add `quarter` column with value `{E1.fiscal_quarter}_FY{E1.fiscal_year}` (e.g., `Q1_FY2024`)
   - Format: `quarter|date|news_id|driver|attr_confidence|pred_confidence|daily_stock|daily_adj|market_session|source|external_research|source_pub_date|judge_notes`
   - Create file with header if it doesn't exist
3. Update `earnings-analysis/news_processed.csv`:
   - Format: `ticker|quarter|fiscal_year|processed_date`
   - Append row: `{TICKER}|{E1.fiscal_quarter}|FY{E1.fiscal_year}|{today YYYY-MM-DD}`
   - Create file with header if it doesn't exist

**GUIDANCE RESULTS:**
Write all valid rows. If retry file exists, do NOT update processed cache.
Source of truth: per-task files in `earnings-analysis/Companies/{TICKER}/manifests/{QUARTER}/gx/`.
For each guidance task ID in the manifest, read `{TASK_ID}.tsv` and append any valid lines (skip `NO_GUIDANCE|...`).
4. Append Q1 guidance to `earnings-analysis/Companies/{TICKER}/guidance.csv`:
   - Add `quarter` column with value `{E1.fiscal_quarter}_FY{E1.fiscal_year}`
   - Format (19 fields): `quarter|period_type|fiscal_year|fiscal_quarter|segment|metric|low|mid|high|unit|basis|derivation|qualitative|source_type|source_id|source_key|given_date|section|quote`
   - `fiscal_quarter` here is numeric (`1-4`) from guidance-extract; do not convert to `Q1` format
   - Skip lines that start with `NO_GUIDANCE`
   - Create file with header if it doesn't exist
5. Update `earnings-analysis/guidance_processed.csv`:
   - Format: `ticker|quarter|fiscal_year|processed_date`
   - Append row: `{TICKER}|{E1.fiscal_quarter}|FY{E1.fiscal_year}|{today YYYY-MM-DD}`
   - Create file with header if it doesn't exist

### Step 4: Foreground Analysis for Q2 (News + Guidance) — ONLY IF TARGET=Q2

**Only run Step 4–4b if TARGET=Q2.**

Calculate:
- `START` = E1 date + 1 day (exclude E1 earnings reaction)
- `END` = E2 date (exclusive, excludes E2 earnings reaction). Scripts already use [start,end), so pass E2 as-is (do not subtract a day).

**Run discovery scripts (only for non-cached tracks; sequential OK):**

```bash
# News discovery (SKIP if Q2 news cached)
source /home/faisal/EventMarketDB/venv/bin/activate && python /home/faisal/EventMarketDB/scripts/earnings/get_significant_moves.py {TICKER} {START} {END} {E2.trailing_vol}

# Guidance discovery - all 5 (SKIP ALL if Q2 guidance cached)
source /home/faisal/EventMarketDB/venv/bin/activate && python /home/faisal/EventMarketDB/scripts/earnings/get_8k_filings_range.py {TICKER} {START} {END}
source /home/faisal/EventMarketDB/venv/bin/activate && python /home/faisal/EventMarketDB/scripts/earnings/get_10k_filings_range.py {TICKER} {START} {END}
source /home/faisal/EventMarketDB/venv/bin/activate && python /home/faisal/EventMarketDB/scripts/earnings/get_10q_filings_range.py {TICKER} {START} {END}
source /home/faisal/EventMarketDB/venv/bin/activate && python /home/faisal/EventMarketDB/scripts/earnings/get_transcript_range.py {TICKER} {START} {END}
source /home/faisal/EventMarketDB/venv/bin/activate && python /home/faisal/EventMarketDB/scripts/earnings/get_guidance_news_range.py {TICKER} {START} {END}
```

**Cache-aware execution:** (based on Step 1b flags)
- If `Q2_NEWS_CACHED=true` → skip `get_significant_moves.py`
- If `Q2_GUIDANCE_CACHED=true` → skip all 5 guidance discovery scripts
- If both cached → skip Steps 4, 4b entirely for Q2

Then follow the same foreground batch pattern as Step 3:
- Phase 1: Create ALL tasks (news with blockedBy + guidance without dependencies)
- Phase 1.5: Write manifest for Q2 (create gx/judge output dirs)
- Phase 2: Spawn BZ agents AND guidance agents in foreground-parallel batches (≤50)
- Phase 3: Escalation loop (foreground) - spawn WEB/PPX/JUDGE as they auto-unblock
- Phase 4: Collect all Q2 results (news from JUDGE-*, guidance from GX-*)
- Phase 4.5: Validation gate before saving results

Use `QUARTER={E2.fiscal_quarter}_FY{E2.fiscal_year}` for all Q2 tasks.

### Step 4b: Save Q2 Results

Same as Step 3b but for Q2:

**NEWS RESULTS:**
1. Append to `earnings-analysis/Companies/{TICKER}/news.csv` with `quarter={E2.fiscal_quarter}_FY{E2.fiscal_year}`
2. Append to `news_processed.csv`: `{TICKER}|{E2.fiscal_quarter}|FY{E2.fiscal_year}|{today YYYY-MM-DD}`

**GUIDANCE RESULTS:**
3. Append to `earnings-analysis/Companies/{TICKER}/guidance.csv` with `quarter={E2.fiscal_quarter}_FY{E2.fiscal_year}`
   - Source of truth: `earnings-analysis/Companies/{TICKER}/manifests/{QUARTER}/gx/{TASK_ID}.tsv`
4. Append to `guidance_processed.csv`: `{TICKER}|{E2.fiscal_quarter}|FY{E2.fiscal_year}|{today YYYY-MM-DD}`

### Step 5: Return Combined Results

```
=== EARNINGS ORCHESTRATOR: {TICKER} ===

--- EARNINGS DATA ---
E1: {accession} | {date} | FY{fiscal_year} {fiscal_quarter} | {daily_adj}% adj | vol={trailing_vol}% ({vol_days}d) {vol_status}
E2: {accession} | {date} | FY{fiscal_year} {fiscal_quarter} | {daily_adj}% adj | vol={trailing_vol}% ({vol_days}d) {vol_status}
...

--- Q1 NEWS ANALYSIS ({START} to {E1}) ---
Filter: |stock|>=4%, |adj|>=max(2×{trailing_vol}%,3%)
Significant dates: {count}

date|news_id|driver|attr_confidence|pred_confidence|daily_stock|daily_adj|market_session|source|external_research|source_pub_date|judge_notes
...

--- Q1 GUIDANCE EXTRACTION ---
Content sources processed: {total_sources}
  - exhibits: {exhibit_count}
  - sections: {section_count}
  - financial_stmt: {financial_stmt_count}
  - xbrl: {xbrl_count}
  - transcripts: {transcript_count}
  - news: {news_count}
Guidance entries found: {guidance_count}

quarter|period_type|fiscal_year|fiscal_quarter|segment|metric|low|mid|high|unit|basis|derivation|qualitative|source_type|source_id|source_key|given_date|section|quote
...

--- Q2 NEWS ANALYSIS ({E1} to {E2}) ---
Filter: |stock|>=4%, |adj|>=max(2×{trailing_vol}%,3%)
Significant dates: {count}

date|news_id|driver|attr_confidence|pred_confidence|daily_stock|daily_adj|market_session|source|external_research|source_pub_date|judge_notes
...

--- Q2 GUIDANCE EXTRACTION ---
Content sources processed: {total_sources}
  - exhibits: {exhibit_count}
  - sections: {section_count}
  - financial_stmt: {financial_stmt_count}
  - xbrl: {xbrl_count}
  - transcripts: {transcript_count}
  - news: {news_count}
Guidance entries found: {guidance_count}

quarter|period_type|fiscal_year|fiscal_quarter|segment|metric|low|mid|high|unit|basis|derivation|qualitative|source_type|source_id|source_key|given_date|section|quote
...

--- NEWS SUMMARY ---
Total dates analyzed: {N}
Explained by Benzinga: {B}
Explained by WebSearch: {W}
Explained by Perplexity: {P}
Still unknown (confidence=0): {U}
Validated by Judge: {J}

--- GUIDANCE SUMMARY ---
Total content sources processed: {total_sources}
  - exhibits: {exhibit_count}
  - sections: {section_count}
  - financial_stmt: {financial_stmt_count}
  - xbrl: {xbrl_count}
  - transcripts: {transcript_count}
  - news: {news_count}
Total guidance entries found: {total_guidance}

=== COMPLETE ===
```

### Step 6: Signal Completion (Auto-Triggers Thinking Build)

```bash
echo "=== ORCHESTRATOR_COMPLETE {TICKER} $(date '+%Y-%m-%d %H:%M:%S') ==="
```

**This command triggers the PostToolUse hook** which automatically runs:
- `build-news-thinking.py --ticker {TICKER}`
- `build-guidance-thinking.py --ticker {TICKER}`

Thinking files appear in Obsidian at `Companies/{TICKER}/thinking/{QUARTER}/` without explicit script calls.

## Rules

- **NEVER use run_in_background** - ALL Task tool calls MUST run in foreground. Do NOT set `run_in_background: true`. Wait for each batch to complete before proceeding. This is critical for proper result collection.
- **Create tasks first; spawn in foreground-parallel batches (≤50)** - Issue up to 50 Task calls per response; then proceed to the next batch.
- **Full row replacement** - When a later tier returns a result, use its COMPLETE output. PPX replaces WEB, WEB replaces BZ. Never mix fields across tiers. Judge outputs 12-field line.
- **Always run get_earnings.py first** - provides trailing_vol for each quarter
- **Skip if done** - check news_processed.csv, skip quarters already processed
- **No background mode** - use foreground-parallel batches (≤50); do NOT set `run_in_background: true`.
- **Q1 complete before Q2** - finish all 4 tiers (BZ → WEB → PPX → JUDGE) + save for Q1, then Q2
- **Processed cache format** - always write `fiscal_year` as `FY{YYYY}` (e.g., FY2023), never plain year
- **Extract date only** - E1 date "2024-02-01T16:30:33-05:00" → use "2024-02-01"
- **Preserve news_id EXACTLY** - Copy URLs verbatim. NEVER shorten, summarize, or create short IDs. If sub-agent returns a URL, save the full URL exactly as returned.
- **Pass through raw output** - don't summarize or lose data
- **Always save results** - append to news.csv/guidance.csv; update processed CSVs only when `.ok` exists (no retry file)
- **Verify before marking processed** - Confirm data rows were appended to CSV before updating processed.csv. If no results to save, do not mark as processed.

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
4. Spawn news-driver-bz for each significant date → some explained (create JUDGE), some create WEB tasks
5. Spawn news-driver-web for each WEB task → some explained (create JUDGE), some create PPX tasks
6. Spawn news-driver-ppx for each PPX task → all create JUDGE tasks
7. Spawn news-driver-judge for each JUDGE task → validates and returns final confidence
8. Save Q1 to Companies/AAPL/news.csv (from JUDGE results), mark Q1_FY2024 done
9. Check news_processed.csv → row exists for AAPL|Q2|FY2024 → skip Q2
10. Return results (Q1 only, Q2 was cached)
