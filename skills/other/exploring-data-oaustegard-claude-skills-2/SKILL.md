---
name: exploring-data
description: Exploratory data analysis using ydata-profiling. Use when users upload .csv/.xlsx/.json/.parquet files or request "explore data", "analyze dataset", "EDA", "profile data". Generates interactive HTML or JSON reports with statistics, visualizations, correlations, and quality alerts.
metadata:
  version: 0.0.3
---

# Exploring Data

## Workflow

### 1. Check if installed (instant)
```bash
bash /mnt/skills/user/exploring-data/scripts/check_install.sh
```
Returns: `installed` or `not_installed`

### 2. Install if needed (one-time, ~19s)
```bash
if [ "$(bash check_install.sh)" = "not_installed" ]; then
    bash /mnt/skills/user/exploring-data/scripts/install_ydata.sh
fi
```

### 3. Run analysis (always generates JSON + HTML by default)
```bash
bash /mnt/skills/user/exploring-data/scripts/analyze.sh <filepath> [minimal|full] [html|json]
```

**Defaults:** minimal + html (also generates JSON)

**Output:**
- `eda_report.html` - Interactive report for user
- `eda_report.json` - Machine-readable for Claude analysis

### 4. If Claude needs to analyze (user asks "what do you think?" etc.)
```bash
python /mnt/skills/user/exploring-data/scripts/summarize_insights.py /mnt/user-data/outputs/eda_report.json
```

**Reads:** `eda_report.json` (comprehensive ydata output)  
**Writes:** `eda_insights_summary.md` (condensed for Claude)  
**Outputs to stdout:** Formatted markdown summary

Claude should read the stdout markdown summary, NOT the full JSON report.

## Invocation Examples

```bash
# Standard workflow (user views HTML)
bash analyze.sh /mnt/user-data/uploads/data.csv
# Produces: eda_report.html + eda_report.json
# Link user to: computer:///mnt/user-data/outputs/eda_report.html

# User asks Claude to analyze
bash analyze.sh /mnt/user-data/uploads/data.csv
python summarize_insights.py /mnt/user-data/outputs/eda_report.json
# Claude reads the stdout markdown summary
# Claude can then provide analysis based on patterns/insights

# Full mode for comprehensive analysis
bash analyze.sh /mnt/user-data/uploads/data.csv full

# JSON-only output (skip HTML generation)
bash analyze.sh /mnt/user-data/uploads/data.csv minimal json
```

## Modes

**Minimal (default, 5-10s):**
Dataset overview, variable analysis, correlations, missing values, alerts

**Full (10-20s):**
Everything in minimal + scatter matrices, sample data, character analysis, more visualizations

## User Triggers for Full Mode
"comprehensive analysis", "detailed EDA", "full profiling", "deep analysis"

Otherwise use minimal.
