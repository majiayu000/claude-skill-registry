---
name: _old-earnings-orchestrator
description: Master orchestrator for batch earnings analysis. Processes all 8-Ks for a company chronologically, running prediction→attribution loop with accuracy tracking.
allowed-tools: Read, Write, Grep, Glob, Bash, TodoWrite, Task, Skill, mcp__neo4j-cypher__read_neo4j_cypher
model: claude-opus-4-5
permissionMode: dontAsk
---

# Earnings Orchestrator

**Goal**: Process all 8-K earnings filings for a company chronologically, building a closed-loop prediction→attribution system with accuracy feedback.

**Thinking**: ALWAYS use `ultrathink` for maximum reasoning depth.

**Input**: Company ticker (e.g., "GBX", "AAPL")

---

## Architecture

```
Master Orchestrator (this skill)
    │
    ├─→ Query Neo4j for all 8-Ks with Item 2.02
    │
    └─→ For each filing chronologically:
            │
            ├─→ First filing: /earnings-attribution only
            │
            └─→ Subsequent filings:
                    │
                    ├─→ /earnings-prediction (predict before seeing outcome)
                    │
                    └─→ /earnings-attribution (verify & learn)
```

---

## Workflow

Use TodoWrite to track progress through all filings.

### Step 1: Query 8-K Universe

Query Neo4j for all 8-Ks with Item 2.02 (earnings) for the ticker:

```cypher
MATCH (r:Report)-[pf:PRIMARY_FILER]->(c:Company)
WHERE c.ticker = $ticker
  AND r.formType = '8-K'
  AND any(item IN r.items WHERE item CONTAINS 'Item 2.02')
  AND pf.daily_stock IS NOT NULL
RETURN r.accessionNo AS accession_no,
       c.ticker AS ticker,
       c.name AS company_name,
       r.created AS filing_datetime,
       pf.daily_stock AS daily_return,
       pf.daily_macro AS macro_adj_return,
       r.items AS items
ORDER BY r.created ASC
```

Extract list of accession numbers with filing dates.

### Step 2: Check Processing State

Read `earnings-analysis/8k_fact_universe.csv` and `earnings-analysis/predictions.csv` to determine:
- Which filings are already completed
- Which predictions exist (and whether they need attribution)

### Step 3: Process Each Filing

For each filing in chronological order:

#### First Filing (no prior history)
```
/earnings-attribution {accession_no}
```
Reason: No historical baseline to predict from. Attribution only.

#### Subsequent Filings
```
1. /earnings-prediction {accession_no}
   → Outputs prediction to predictions.csv

2. /earnings-attribution {accession_no}
   → Verifies prediction accuracy
   → Updates predictions.csv with actual_* columns
   → Stores company-specific learnings
```

### Step 4: Update Tracking

After each filing:
1. Mark `completed=TRUE` in 8k_fact_universe.csv
2. Update predictions.csv with actual outcomes
3. Compute running accuracy metrics

---

## Accuracy Tracking

### Direction Accuracy
```
correct = predicted_direction == actual_direction
```

### Magnitude Accuracy
```
magnitude_correct = predicted_magnitude == actual_magnitude
```

### Running Metrics

After processing, compute:
- Total filings processed
- Predictions made (excludes first filing)
- Direction accuracy: correct / predictions
- Magnitude accuracy: magnitude_correct / predictions

---

## Resume Logic

If a filing is partially processed:
1. Check predictions.csv for existing prediction
2. Check Companies/{TICKER}/{accession}.md for attribution
3. Skip completed steps, resume where needed

---

## Output Files

| File | Purpose |
|------|---------|
| `earnings-analysis/predictions.csv` | All predictions + actuals |
| `earnings-analysis/8k_fact_universe.csv` | Processing status tracker |
| `earnings-analysis/Companies/{TICKER}/{accession}.md` | Attribution reports |
| `earnings-analysis/Companies/{TICKER}/learnings.md` | Company-specific patterns |
| `earnings-analysis/orchestrator-runs/{ticker}_{timestamp}.md` | Run summary |

---

## Run Summary Format

After completing a ticker, write summary to `earnings-analysis/orchestrator-runs/{ticker}_{YYYYMMDD}.md`:

```markdown
# {TICKER} Orchestrator Run - {DATE}

## Summary
- Total 8-Ks found: N
- Already completed: N
- Processed this run: N
- First filing (attribution only): {accession}

## Prediction Accuracy
- Predictions made: N
- Direction correct: N/M (X%)
- Magnitude correct: N/M (X%)

## Filings Processed

| # | Accession | Date | Prediction | Actual | Correct |
|---|-----------|------|------------|--------|---------|
| 1 | xxx | 2023-01-01 | (first) | +5.2% | N/A |
| 2 | xxx | 2023-04-01 | up/medium | up/large | dir: Y, mag: N |
...

## Learnings Applied
- [List company-specific patterns discovered]
```

---

## Invocation Examples

### Process all filings for a ticker
```
/earnings-orchestrator GBX
```

### Process with limit
```
/earnings-orchestrator GBX --limit 5
```
Processes only first 5 unprocessed filings.

### Resume interrupted run
```
/earnings-orchestrator GBX --resume
```
Continues from last processed filing.

---

## Error Handling

1. **Neo4j query fails**: Log error, exit gracefully
2. **Skill invocation fails**: Log error, mark filing as failed, continue to next
3. **Missing data**: Note in summary, continue with available data
4. **Rate limits**: Built-in retry with exponential backoff

---

## Arguments

| Arg | Type | Default | Description |
|-----|------|---------|-------------|
| ticker | string | required | Company ticker to process |
| --limit | int | none | Max filings to process |
| --resume | flag | false | Resume from last completed |
| --dry-run | flag | false | Show plan without executing |

---

*Version 1.0 | 2026-01-16*
