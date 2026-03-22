---
name: outlier-detection-handler
description: Identify and handle statistical outliers in datasets using z-score, IQR, or Grubbs methods with regulatory-ready documentation.
license: MIT
skill-author: AIPOCH
status: beta
---
# Outlier Detection & Handling

Identify and manage statistical outliers in datasets using validated methods with regulatory-ready documentation.

## Input Validation

This skill accepts: tabular datasets (CSV or Excel) with numeric columns for statistical outlier detection and handling.

If the request does not involve detecting or handling statistical outliers in a numeric dataset — for example, asking to perform regression analysis, classify data, impute missing values, or process non-tabular inputs — do not proceed. Instead respond:

> "outlier-detection-handler is designed to identify and handle statistical outliers in numeric datasets. Your request appears to be outside this scope. Please provide a CSV or Excel file with numeric data, or use a more appropriate tool for your task. For missing value imputation, consider scikit-learn SimpleImputer, pandas fillna, or R mice."

**This refusal must fire as the absolute first action — before any data summary, context processing, or partial analysis. Do not generate any output about the data before emitting this refusal.**

## When to Use

- Data quality control before statistical analysis
- Pre-analysis screening of biomarker or clinical measurement datasets
- Regulatory compliance workflows requiring documented outlier handling (FDA data integrity)
- Generating outlier reports for audit trails

## Workflow

1. **Validate input** — confirm scope before any processing. Emit refusal immediately for out-of-scope requests.
2. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--data` | str | Yes | - | Path to dataset file (CSV/Excel) |
| `--method` | str | No | `zscore` | Detection method: `zscore`, `iqr`, or `grubbs` |
| `--threshold` | float | No | `3.0` | Threshold for z-score or Grubbs test |
| `--action` | str | No | `flag` | Handling action: `flag`, `remove`, or `winsorize` |

## Usage

```text
# Z-score outlier detection with flagging
python scripts/main.py --data measurements.csv --method zscore --threshold 3.0

# IQR method with removal
python scripts/main.py --data measurements.csv --method iqr --action remove

# Grubbs test for small samples
python scripts/main.py --data measurements.csv --method grubbs --action flag
```

## Output

- Outlier flagging report with method details and threshold used
- Per-observation flag with outlier score
- Handling recommendations with rationale
- Summary statistics before and after handling
- Documentation suitable for regulatory submission

## Example

Input: Biomarker measurements from 200 patients  
Output: 5 outliers identified (2.5%), recommended action: investigate then winsorize

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
```

## Error Handling

- If `--data` is missing, state this and request the dataset path.
- If the data file path contains `../` or points outside the workspace, reject with a path traversal warning. Do not open the file.
- If the dataset has no numeric columns, report this and stop.
- If the task goes outside the documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what still can be completed safely, and provide a manual fallback.
- If numpy/scipy are not installed, print: `pip install numpy scipy` and exit with a non-zero exit code. The script must wrap numpy/scipy imports in try/except to provide this graceful degradation.
- Do not fabricate outlier counts, scores, or recommendations.

## Fallback Template

When execution fails or inputs are incomplete, respond with this structure:

```
FALLBACK REPORT
───────────────────────────────────────
Objective      : [restate the goal]
Blocked by     : [exact missing input or error]
Partial result : [what can be completed — e.g., method selection guidance]
Assumptions    : [method, threshold, action assumed]
Constraints    : [regulatory requirements, sample size minimums]
Risks          : [small sample size for Grubbs, masking effect]
Unresolved     : [what still needs user input]
Next step      : [minimum action needed to unblock]
───────────────────────────────────────
```

## Response Template

Use the following fixed structure for non-trivial requests:

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks

If the request is simple, compress the structure but keep assumptions and limits explicit when they affect correctness.

## Prerequisites

```text
pip install -r requirements.txt
```
