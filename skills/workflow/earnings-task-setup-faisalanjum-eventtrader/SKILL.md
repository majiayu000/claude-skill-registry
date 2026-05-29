---
name: earnings-task-setup
description: Set up earnings tasks for a ticker with CSV persistence and Claude task tracking
context: fork
allowed-tools:
  - TaskCreate
  - TaskList
  - TaskGet
  - TaskUpdate
  - Read
  - Write
  - Bash
  - Glob
---

# Earnings Task Setup

Sets up tasks for earnings analysis workflow with:
1. CSV persistence (survives across sessions)
2. Claude task tracking (within-session dependencies)

## Arguments

Expects: `TICKER QUARTER ACCESSION`

Example: `AAPL Q1-2024 0000320193-24-000001`

If no arguments provided, will prompt for them.

**Arguments received**: $ARGUMENTS

## Workflow Pattern

```
Wave 1 (parallel):
  ├── {ticker}-{quarter}-news-impact
  └── {ticker}-{quarter}-guidance

Wave 2 (blocked by Wave 1):
  └── {ticker}-{quarter}-prediction

Wave 3 (blocked by Wave 2):
  └── {ticker}-{quarter}-attribution
```

## Instructions

### Step 1: Parse Arguments

Extract ticker, quarter, and accession from: `$ARGUMENTS`

If arguments are missing or empty, use these defaults for testing:
- Ticker: TEST
- Quarter: Q1-2024
- Accession: test-accession-001

### Step 2: Check CSV Tracker

Read `earnings-analysis/task-tracker.csv` to see current status.

If row doesn't exist for this ticker/quarter/accession, add it:
```csv
{ticker},{quarter},{accession},pending,pending,pending,pending,{ISO_TIMESTAMP}
```

If row exists, check which tasks are still pending.

### Step 3: Create Claude Tasks

For each PENDING task (not already completed in CSV), create a Claude task:

```
Subject: {TICKER}-{QUARTER}-{task_name}
Description: {task_description}
ActiveForm: {active_form}
```

Task descriptions:
- **news-impact**: "Analyze news sentiment and events around {TICKER} {QUARTER} earnings. Accession: {ACCESSION}"
- **guidance**: "Update cumulative guidance inventory for {TICKER} with {QUARTER} data. Accession: {ACCESSION}"
- **prediction**: "Predict {TICKER} stock direction at T=0 using PIT data. Accession: {ACCESSION}"
- **attribution**: "Analyze why {TICKER} moved after {QUARTER} earnings (T+1). Accession: {ACCESSION}"

### Step 4: Set Up Dependencies

Use TaskUpdate with addBlockedBy:
- prediction blocked by news-impact AND guidance
- attribution blocked by prediction

### Step 5: Output Summary

Write to `earnings-analysis/test-outputs/earnings-task-setup-{TICKER}-{QUARTER}.txt`:

```
EARNINGS TASK SETUP
==================
Ticker: {TICKER}
Quarter: {QUARTER}
Accession: {ACCESSION}
Timestamp: {ISO_TIMESTAMP}

CSV STATUS (before):
- news_impact: {status}
- guidance: {status}
- prediction: {status}
- attribution: {status}

CLAUDE TASKS CREATED:
- #{id} {TICKER}-{QUARTER}-news-impact [no blockers]
- #{id} {TICKER}-{QUARTER}-guidance [no blockers]
- #{id} {TICKER}-{QUARTER}-prediction [blocked by #{news_id}, #{guidance_id}]
- #{id} {TICKER}-{QUARTER}-attribution [blocked by #{prediction_id}]

NEXT STEPS:
1. Execute unblocked tasks (news-impact, guidance can run parallel)
2. After each task completes, run:
   python -c "from scripts.task_tracker import TaskTracker; TaskTracker().update_status('{TICKER}', '{QUARTER}', '{ACCESSION}', 'TASK_NAME', 'completed')"
3. Mark Claude task as completed with TaskUpdate

PARALLEL TASKS AVAILABLE:
{list tasks with no blockers}
```

### Step 6: Return Summary

Return a brief summary of:
- How many tasks were created
- Which tasks are ready to execute (no blockers)
- Command to check status: `python scripts/task_tracker.py status`
