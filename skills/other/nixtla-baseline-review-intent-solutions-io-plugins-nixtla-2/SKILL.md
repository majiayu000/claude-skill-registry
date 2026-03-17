---
name: nixtla-baseline-review
description: Analyze Nixtla baseline forecasting results (sMAPE/MASE on M4 or other
  benchmark datasets). Use when the user asks about baseline performance, model comparisons,
  or metric interpretation for Nixtla time-series experiments. Trigger with "baseline review",
  "interpret sMAPE/MASE", or "compare AutoETS vs AutoTheta".
allowed-tools: Read,Grep,Bash(ls:*)
version: 1.0.0
author: Jeremy Longshore <jeremy@intentsolutions.io>
license: MIT
---

# Nixtla Baseline Review Skill

## Overview

Analyze baseline forecasting results from the `nixtla-baseline-m4` workflow. Interpret metrics, compare models, surface patterns, and recommend next steps.

## When to Use This Skill

Activate this skill when the user:
- Asks "Which baseline model performed best?"
- Requests interpretation of sMAPE or MASE metrics
- Wants to compare AutoETS vs AutoTheta vs SeasonalNaive
- Says "Explain these baseline results"
- Needs guidance on model selection based on baseline performance

## Prerequisites

- Baseline results must exist in `nixtla_baseline_m4/` directory
- At minimum, `results_*.csv` file must be present
- CSV format: columns `series_id`, `model`, `sMAPE`, `MASE`

## Instructions

### Step 1: Locate Results Files

Use the **Read** tool to find baseline results:

```bash
# Check for results directory (use Bash tool)
ls -la nixtla_baseline_m4/

# Identify most recent results file
ls -t nixtla_baseline_m4/results_*.csv | head -1
```

Expected files:
- `results_M4_Daily_h{horizon}.csv` - Full metrics table
- `summary_M4_Daily_h{horizon}.txt` - Text summary (optional)

If files are missing, inform the user they need to run `/nixtla-baseline-m4` first.

### Step 2: Load and Parse Metrics

Read the metrics CSV file:

```bash
# View first few rows to confirm format
head -10 nixtla_baseline_m4/results_M4_Daily_h*.csv

# Or use Read tool to load the full file
```

Expected CSV structure:
```csv
series_id,model,sMAPE,MASE
D1,SeasonalNaive,15.23,1.05
D1,AutoETS,13.45,0.92
D1,AutoTheta,12.34,0.87
D2,SeasonalNaive,18.67,1.23
...
```

Calculate summary statistics manually or with bash:
- Count total series: `cut -d, -f1 results_*.csv | sort -u | wc -l`
- Extract model metrics: `grep "AutoTheta" results_*.csv`

### Step 3: Calculate Summary Statistics

For each model (SeasonalNaive, AutoETS, AutoTheta), calculate:
- **Mean sMAPE**: Average across all series
- **Median sMAPE**: Middle value (less sensitive to outliers)
- **Standard Deviation**: Measure of consistency
- **Series Won**: Count how many series each model performed best on

### Step 4: Interpret Metrics

**sMAPE (Symmetric Mean Absolute Percentage Error)**:
- Range: 0% (perfect) to 200% (worst)
- Good: < 10%, Acceptable: 10-20%, Poor: > 20%

**MASE (Mean Absolute Scaled Error)**:
- < 1.0: Better than seasonal naive baseline
- 1.0: Same as seasonal naive
- > 1.0: Worse than seasonal naive
- Interpretation: "MASE of 0.85 means this model is 15% better than naive seasonal"

**Model Characteristics**:
- **SeasonalNaive**: Simplest baseline, repeats seasonal pattern. Good for stable series.
- **AutoETS**: Exponential smoothing with automatic parameter selection. Good for trend + seasonality.
- **AutoTheta**: Theta method with optimization. Often wins on M4 benchmarks, handles trends well.

### Step 5: Identify Patterns

Look for:
- **Dominant model**: Which model wins most often?
- **Consistency**: Which model has lowest standard deviation in sMAPE?
- **Series-specific patterns**: Are there series types where certain models excel?
- **Failure cases**: Where do ALL models struggle? (sMAPE > 30%, MASE > 1.5)

### Step 6: Generate Structured Explanation

Provide analysis in this format:

```markdown
## Baseline Performance Analysis

Based on {N} series from M4-Daily with horizon={H}:

**Overall Winner**: {ModelName}
- Mean sMAPE: {X.XX}% (vs {Y.YY}% for second place)
- Wins on {N} out of {Total} series ({Percentage}%)
- Consistent performance (std dev {X.X}%)

**Key Insights**:
1. {Insight about winner's strengths}
2. {Insight about other models or patterns}
3. {Insight about failure cases or opportunities}

**Recommendation**: Use {ModelName} as production baseline. {Additional context about when to consider alternatives}

**Next Steps**:
- {Actionable recommendation 1}
- {Actionable recommendation 2}
```

## Output

- A structured markdown analysis with a clear winner, key insights, and recommended next steps.

## Examples

### Example 1: Simple Query

**User**: "Which model was best?"

**Response**:
```
Based on the baseline results (50 series, horizon=14):

**AutoTheta won** with average sMAPE of 12.3%
- Outperformed AutoETS (13.5%) and SeasonalNaive (15.2%)
- Most consistent with std dev of 4.2%
- Recommended for production use
```

### Example 2: Detailed Comparison

**User**: "Compare AutoETS vs AutoTheta performance"

**Response**:
```
## AutoETS vs AutoTheta Comparison

| Metric        | AutoETS | AutoTheta | Winner   |
|---------------|---------|-----------|----------|
| Mean sMAPE    | 13.5%   | 12.3%     | Theta ✓  |
| Median sMAPE  | 12.9%   | 11.8%     | Theta ✓  |
| Std Dev       | 5.1%    | 4.2%      | Theta ✓  |
| Series Won    | 18/50   | 32/50     | Theta ✓  |

**Key Differences**:
- Theta handles trends better (exponential smoothing with drift)
- ETS excels on strong seasonality (state space framework)
- Theta more consistent across diverse patterns

**Recommendation**: Use AutoTheta as default, fallback to AutoETS for highly seasonal data.
```

### Example 3: Metric Interpretation

**User**: "What does sMAPE of 12.3% mean?"

**Response**:
```
sMAPE of 12.3% is **good performance** for forecasting:

- This means on average, predictions are off by about 12% from actual values
- For M4 Daily benchmark, anything under 15% is considered good
- This is in the "acceptable" range (10-20%)

Context: If you're forecasting daily sales of 100 units, a 12.3% sMAPE means your forecast will typically be within ±12 units of the true value.

MASE provides additional context - if MASE < 1.0, this forecast beats a simple "repeat last year" baseline.
```

## Error Handling

**If results files are missing**:
```
I don't see baseline results in nixtla_baseline_m4/.

Please run the baseline command first:
Run: `/nixtla-baseline-m4 horizon=14 series_limit=50`

This will generate the metrics files I need to analyze.
```

**If CSV is malformed**:
```
The results file exists but appears malformed. Expected columns:
- series_id, model, sMAPE, MASE

Please re-run /nixtla-baseline-m4 to regenerate clean results.
```

## Resources

For complete technical details, see:
- Architecture: `000-docs/6767-a-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md`
- Planning: `000-docs/6767-b-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md`
- Baseline Lab Overview: `000-docs/6767-d-OD-OVRV-nixtla-baseline-lab-overview.md`
