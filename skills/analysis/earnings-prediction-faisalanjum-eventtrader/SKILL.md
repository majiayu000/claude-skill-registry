---
name: earnings-prediction
description: Predicts stock direction/magnitude at T=0 (report release). Uses PIT data only. Run before earnings-attribution.
context: fork
allowed-tools: Read, Write, Grep, Glob, Bash, TodoWrite, Skill
model: claude-opus-4-5
permissionMode: dontAsk
---

# Earnings Prediction

**Goal**: Predict stock direction and magnitude before market reacts, using point-in-time data only.

**Thinking**: ALWAYS use `ultrathink` for maximum reasoning depth.

**Input**: Accession number of 8-K earnings filing

---

## Prediction Output

| Field | Values |
|-------|--------|
| Direction | up / down |
| Magnitude | small (0-2%) / medium (2-5%) / large (5%+) |
| Confidence | high / medium / low |

**Tiny surprises (<1%)**: Predict small_up or small_down based on sign, use low confidence.

---

## PIT Rules (Critical)

All sub-agent queries MUST use PIT filtering: `[PIT: {filing_datetime}]`

**Allowed**:
- 8-K filing content (the actual results)
- Historical financials (prior 10-K/10-Q via XBRL)
- Prior earnings transcripts
- Pre-filing news
- Consensus estimates from Perplexity (filtered by article date)

**NOT Allowed**:
- Return data (daily_stock, hourly_stock) — that's what we're predicting
- Post-filing news reactions
- Post-filing analyst commentary

---

## Data Isolation Architecture

**ALL data queries go through the filter agent.** This includes Neo4j AND Perplexity.

```
YOU (earnings-prediction)
        │
        │ /filtered-data --agent {source} --query "[PIT: X] ..."
        ▼
┌─────────────────────────────────────┐
│       FILTER AGENT                  │
│                                     │
│  Sources: neo4j-*, perplexity-search│
│                                     │
│  Validates:                         │
│  1. Forbidden patterns              │
│  2. PIT compliance (dates <= PIT)   │
│                                     │
│  You NEVER see contaminated data    │
└─────────────────────────────────────┘
        │
        │ Clean data only
        ▼
YOU (continue with clean data)
```

### Why This Matters

Return data (daily_stock, hourly_stock, etc.) is what we're trying to predict. Post-filing articles mention stock reactions. If either enters your context, the prediction is contaminated. The filter agent ensures you never see it.

---

## Workflow (5 Steps)

Use TodoWrite to track progress. Mark each step `in_progress` before starting, `completed` immediately after.

**IMPORTANT**: Read `./QUERIES.md` and execute the exact commands shown there. Do not modify them.

### Step 1: Get Filing Metadata

Execute the `metadata` query from QUERIES.md.

Extract: ticker, filing_datetime (this becomes your PIT).

### Step 2: Get Actual Results from Filing

Execute the `exhibit` query from QUERIES.md.

Extract: Actual EPS, actual revenue, any guidance.

### Step 3: Get Historical Context (PIT)

Execute these queries from QUERIES.md: `xbrl`, `transcript`, `news`, `entity`

### Step 4: Get Consensus Estimates

Execute the `consensus` query from QUERIES.md.

### Step 5: Make Prediction

Calculate surprise:
```
Surprise % = ((Actual - Consensus) / |Consensus|) × 100
```

Reason from the data. Consider: surprise magnitude, guidance direction, historical patterns, sector context. Output prediction with reasoning.

---

## CSV Output

**File**: `earnings-analysis/predictions.csv`

**Columns**:
```csv
accession_no,ticker,filing_datetime,prediction_datetime,predicted_direction,predicted_magnitude,confidence,primary_reason,actual_direction,actual_magnitude,actual_return,correct
```

**Append** each prediction as a new row. Leave actual_* columns empty (filled by attribution later).

### CSV Append

1. Read existing CSV with Read tool
2. Append new row with Write tool (rewrite full file)
3. Escape commas in primary_reason with quotes: `"reason with, comma"`

**First run**: If CSV doesn't exist, create it with header row first.

---

## After Prediction (REQUIRED STEPS)

### Step 6: Append to CSV
Append prediction to `earnings-analysis/predictions.csv` (see CSV Output section).

### Step 7: Build Thinking Index (MANDATORY - DO NOT SKIP)

**This step is REQUIRED.** Execute this exact command:

```bash
python3 scripts/build-thinking-index.py {accession_no}
```

Replace `{accession_no}` with the actual accession number from your analysis (e.g., `0001234567-24-000001`).

This extracts thinking from all sessions and sub-agents and saves to Obsidian.

### Step 8: Attribution (Later)
Run `/earnings-attribution` separately to fill actual_* columns and verify prediction.

---

## Toggle Filtering

```bash
# In .claude/skills/earnings-prediction/
./enable-filter.sh   # PIT filtering ON (default)
./disable-filter.sh  # Direct mode (no filtering)
```

State persists until you run the other script.

---

## Session & Subagent History (Shared CSV)

**History file**: `.claude/shared/earnings/subagent-history.csv` (shared with earnings-attribution)

**Format**: See [subagent-history.md](../../shared/earnings/subagent-history.md) for full documentation.

```csv
accession_no,skill,created_at,primary_session_id,agent_type,agent_id,resumed_from
0001514416-24-000020,prediction,2026-01-13T09:00:00,aaa11111,primary,,
0001514416-24-000020,prediction,2026-01-13T09:01:05,aaa11111,neo4j-entity,abc12345,
```

**On analysis start**:
1. Read CSV (create with header if doesn't exist)
2. Append `primary` row: `{accession},prediction,{timestamp},{session_id},primary,,`

**Before calling a subagent**:
1. Query latest agent ID: `grep "{accession}" | grep ",{agent_type}," | tail -1 | cut -d',' -f6`
2. If agent ID exists → can use `resume: <id>` in Task call
3. If want fresh session → proceed without resume

**After each subagent completes**:
1. Extract `agentId` from Task response
2. Append row: `{accession},prediction,{timestamp},{session_id},{agent_type},{agent_id},{resumed_from}`

---

*Version 2.2 | 2026-01-16 | Made thinking index build mandatory (Step 7)*
