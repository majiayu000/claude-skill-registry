---
name: research-evaluate
description: Evaluate a research source from report_notes, understand its purpose, and create a Linear issue.
allowed-tools: Bash, Read, Glob, Grep, mcp__linear__linear_createIssue, mcp__linear__linear_searchIssues, Edit
argument-hint: "<source-id or query>"
---

# Research Source Evaluator

Find a research source in `report_notes/`, analyze its content (purpose, tables, charts, key findings), and create a Linear issue for implementation.

## Usage

```bash
# By source ID from research.csv
/research-evaluate RS-006

# By search query
/research-evaluate "mean reversion currencies"

# By file path
/research-evaluate report_notes/fx_seasonality_research/sources/quantpedia/002_mean_reversion_currencies.md
```

## Workflow

### Step 1: Find the Source

```bash
# If ID provided, look up in research.csv
grep "^$ID," /home/adesola/EpochDev/ClaudeCodeResearch/research.csv

# If query provided, search sources
grep -ri "$QUERY" /home/adesola/EpochDev/ClaudeCodeResearch/report_notes/*/sources/
```

### Step 2: Read and Analyze the Source

Read the markdown file and extract:

1. **Frontmatter** - URL, title, domain, crawl date
2. **Hypothesis** - Main research question/thesis
3. **Data Requirements** - Assets, timeframes, data sources needed
4. **Methodology** - How the strategy/analysis works
5. **Key Metrics** - Performance figures, statistics mentioned
6. **Charts/Tables** - Visual elements and their purpose

```python
# Example analysis structure
{
    "source_id": "RS-006",
    "title": "How to Build Mean Reversion Strategies in Currencies",
    "url": "https://quantpedia.com/...",
    "hypothesis": "Long undervalued and short overvalued currencies generates alpha",
    "data_requirements": {
        "assets": ["AD1", "BF1", "CD1", "EC1", "SF1", "JY1"],
        "asset_type": "FX futures",
        "timeframe": "daily",
        "period": "2007-2024"
    },
    "methodology": {
        "signal": "Deviation from average cumulative return",
        "long": "Currencies below average (undervalued)",
        "short": "Currencies above average (overvalued)",
        "rebalancing": "Monthly",
        "position_sizing": ["linear", "exponential"]
    },
    "key_metrics": {
        "sharpe": 0.XX,
        "annual_return": "X%",
        "max_drawdown": "-X%"
    },
    "charts": [
        {"name": "Cumulative returns", "purpose": "Shows mean reversion tendency"},
        {"name": "Strategy performance", "purpose": "Backtest equity curve"}
    ],
    "tables": [
        {"name": "Position sizing comparison", "purpose": "Linear vs exponential results"}
    ]
}
```

### Step 3: Check for Existing Issues

```python
mcp__linear__linear_searchIssues(
    query="$TITLE",
    projectId="aedc87b9-3cee-4bdb-95ef-ac3d49e1218f",  # Quantitative Research
    limit=5
)
```

### Step 4: Create Linear Issue

```python
mcp__linear__linear_createIssue(
    teamId="53f03fc6-d769-481a-b0f6-f7d6f8ab8085",
    projectId="aedc87b9-3cee-4bdb-95ef-ac3d49e1218f",  # Quantitative Research
    priority=3,
    title="Research: $TITLE",
    description="""## Summary

$HYPOTHESIS

**Source:** [$TITLE]($URL)
**Source ID:** $SOURCE_ID

## Data Requirements

- **Assets:** $ASSETS
- **Timeframe:** $TIMEFRAME
- **Period:** $PERIOD

## Methodology

$METHODOLOGY_DESCRIPTION

## Key Findings from Source

$KEY_METRICS_AND_FINDINGS

## Charts to Reproduce

$CHARTS_LIST

## Tables to Reproduce

$TABLES_LIST

## Implementation Tasks

- [ ] Create research definition
- [ ] Configure data sources
- [ ] Implement signal generation
- [ ] Run study
- [ ] Analyze results
- [ ] Compare with source findings

## Reference

- Source file: `$FILE_PATH`
- Research CSV: `research.csv` row $SOURCE_ID
"""
)
```

### Step 5: Update research.csv

Update the status and linear_issue columns:

```python
# Change status from PENDING to TODO
# Add Linear issue ID
```

## Output

After evaluation:
1. Linear issue created with full analysis
2. research.csv updated with issue link
3. Summary printed showing:
   - Source details
   - Key hypothesis
   - Data requirements
   - Issue URL

## Issue Description Template

```markdown
## Summary

[1-2 sentence hypothesis from the research source]

**Source:** [Title](URL)
**Source ID:** RS-XXX

## Data Requirements

- **Assets:** [list assets]
- **Timeframe:** [daily/hourly/etc]
- **Period:** [date range]

## Methodology

[Description of how the strategy/analysis works]

## Key Findings from Source

| Metric | Value |
|--------|-------|
| Sharpe | X.XX |
| Annual Return | X% |
| Max Drawdown | -X% |

## Charts to Reproduce

1. [Chart name] - [purpose]
2. [Chart name] - [purpose]

## Tables to Reproduce

1. [Table name] - [purpose]

## Implementation Tasks

- [ ] Create research definition
- [ ] Configure data sources
- [ ] Implement signal generation
- [ ] Run study
- [ ] Analyze results
- [ ] Compare with source findings

## Reference

- Source file: `report_notes/.../file.md`
- Research CSV: `research.csv` row RS-XXX
```
