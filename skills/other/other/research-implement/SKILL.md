---
name: research-implement
description: Build a research definition and execute the study based on a Linear issue.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, mcp__linear__linear_getIssueById, mcp__linear__linear_updateIssue, mcp__linear__linear_createComment
argument-hint: "<linear-issue-id>"
---

# Research Implementation

Build a research study definition and execute it based on a Linear issue created by `/research-evaluate`.

## Usage

```bash
/research-implement ENG-XXX
```

## Workflow

### Step 1: Get Issue Details

```python
issue = mcp__linear__linear_getIssueById(id="ENG-XXX")
```

Extract from description:
- Source file path
- Data requirements (assets, timeframe, period)
- Methodology
- Charts/tables to reproduce

### Step 2: Read Source Material

```bash
# Read the source markdown file
cat report_notes/<topic>/<source_file>.md
```

Understand:
- Exact signal logic
- Position sizing rules
- Rebalancing frequency
- Any special conditions

### Step 3: Update Issue Status

```python
mcp__linear__linear_updateIssue(
    id="ENG-XXX",
    stateId="49c7285c-33c4-443c-a0af-49b51b8e1739"  # In Progress
)
```

### Step 4: Create Research Definition

Create a JSON definition file following the study generation grammar.

**File location:** `project/definitions/test_runner/<source_id>_research.json`

**Template:**
```json
{
  "name": "<source_id>_research",
  "type": "RESEARCH",
  "description": "<hypothesis from source>",
  "source_reference": {
    "id": "<source_id>",
    "url": "<source_url>",
    "title": "<source_title>"
  },
  "universe": {
    "assets": ["<asset1>", "<asset2>"],
    "timeframe": "1d"
  },
  "date_range": {
    "start": "YYYY-MM-DD",
    "end": "YYYY-MM-DD"
  },
  "transforms": [
    // Signal generation transforms
  ],
  "analysis": {
    "metrics": ["sharpe", "annual_return", "max_drawdown", "volatility"],
    "charts": [
      // Charts to generate matching source
    ],
    "tables": [
      // Tables to generate matching source
    ]
  }
}
```

### Step 5: Validate Definition

```bash
cd /home/adesola/EpochDev/ClaudeCodeResearch
source .venv/bin/activate

# Check JSON syntax
python -c "import json; json.load(open('project/definitions/test_runner/<source_id>_research.json'))"
```

### Step 6: Build Job Data Binary (if needed)

```bash
/build-job-data
```

### Step 7: Execute Study

```bash
/run-job-data "project/definitions/test_runner/<source_id>_research.json" --start YYYY-MM-DD --end YYYY-MM-DD
```

### Step 8: Analyze Results

```bash
# Get tearsheet reports
/study-reports <job_folder>

# Query data if needed
/query-study <job_folder> "SELECT * FROM market_data_1d_<asset> LIMIT 10"
```

### Step 9: Compare with Source

Document comparison:

| Metric | Source | Our Result | Difference |
|--------|--------|------------|------------|
| Sharpe | X.XX | Y.YY | ±Z.ZZ |
| Annual Return | X% | Y% | ±Z% |
| Max Drawdown | -X% | -Y% | ±Z% |

### Step 10: Update Linear Issue

Add comment with results:

```python
mcp__linear__linear_createComment(
    issueId="ENG-XXX",
    body="""## Research Results

**Job folder:** `project/research_studies/<job_id>`

### Performance Comparison

| Metric | Source | Our Result | Difference |
|--------|--------|------------|------------|
| Sharpe | X.XX | Y.YY | ±Z.ZZ |
| Annual Return | X% | Y% | ±Z% |
| Max Drawdown | -X% | -Y% | ±Z% |

### Charts Generated

1. [Chart 1 description]
2. [Chart 2 description]

### Observations

[Key findings and any discrepancies]

### Files

- Definition: `project/definitions/test_runner/<source_id>_research.json`
- Results: `project/research_studies/<job_id>/`
"""
)
```

Move to In Review:
```python
mcp__linear__linear_updateIssue(
    id="ENG-XXX",
    stateId="e93bf93b-77e3-41bb-afbd-5b76f8194653"  # In Review
)
```

### Step 11: Update research.csv

Update status to `IN_REVIEW` or `COMPLETED`.

## Definition Structure Reference

See `docs/STUDY_GEN_PROMPT.md` for full grammar.

### Common Transforms for Research

```json
// Returns
{"type": "returns", "period": 1}
{"type": "returns", "period": 21}  // Monthly

// Moving averages
{"type": "sma", "window": 20}
{"type": "ema", "window": 12}

// Volatility
{"type": "volatility", "window": 21}

// Cross-sectional rank
{"type": "cs_rank"}

// Z-score (mean reversion)
{"type": "zscore", "window": 252}
```

## Output Checklist

- [ ] Definition file created
- [ ] Study executed successfully
- [ ] Tearsheet generated
- [ ] Results compared with source
- [ ] Linear issue updated with results
- [ ] research.csv status updated
