---
name: survival-analysis-km
description: Kaplan-Meier survival analysis with log-rank tests, Cox regression, and publication-ready survival curves for clinical and biological research.
license: MIT
skill-author: AIPOCH
---
# Survival Analysis (Kaplan-Meier)

Kaplan-Meier survival analysis tool for clinical and biological research. Generates publication-ready survival curves with statistical tests and hazard ratios.

## Quick Check

```bash
python -m py_compile scripts/main.py
pip install lifelines && python scripts/main.py --help
```

> **Note:** The `lifelines` package is required. Install it before running: `pip install lifelines`

## When to Use

- Overall survival (OS) or progression-free survival (PFS) analysis
- Comparing survival between treatment groups
- Generating KM curves for clinical manuscripts
- Cox proportional hazards regression with HR and 95% CI

## Usage

```bash
python scripts/main.py \
  --input clinical_data.csv \
  --time overall_survival_months \
  --event death \
  --group treatment_arm \
  --output ./results/ \
  --risk-table
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--input` | Yes | — | Input CSV file path |
| `--time` | Yes | — | Column name for survival time |
| `--event` | Yes | — | Event indicator column (1=event, 0=censored) |
| `--group` | No | — | Grouping variable for stratification |
| `--output` | Yes | — | Output directory for results |
| `--conf-level` | No | 0.95 | Confidence level |
| `--risk-table` | No | False | Include at-risk table in plot |
| `--dpi` | No | 300 | Output figure resolution |

## Input Format

CSV with required columns:

```csv
patient_id,time_months,death,treatment_group
P001,24.5,1,Drug_A
P002,36.2,0,Drug_A
P003,18.7,1,Placebo
```

## Output Files

- `km_curve.png` / `km_curve.pdf` — Survival curves with 95% CI
- `survival_stats.csv` — Median survival and confidence intervals
- `hazard_ratios.csv` — Cox regression results with HR and 95% CI
- `logrank_test.csv` — Pairwise comparison p-values
- `report.txt` — Human-readable summary

## Workflow

1. Confirm objective, required inputs, and constraints before proceeding.
2. Validate request matches documented scope; stop early if unsupported assumptions are needed.
3. **If `--group` is not provided:** emit "Note: No group column specified — log-rank test and Cox regression skipped. Single-arm KM only." before proceeding.
4. Run `scripts/main.py` with available inputs, or use the documented reasoning path.
5. Return structured result separating assumptions, deliverables, risks, and unresolved items.
6. On execution failure or incomplete inputs, switch to fallback path and state exactly what blocked completion.

## Fallback Template

If `scripts/main.py` cannot run (missing `lifelines`, missing inputs), respond with:

```
FALLBACK REPORT
───────────────────────────────────────
Objective      : <stated goal>
Blocked by     : <exact missing input or error>
Partial result : <what can still be assessed manually>
Next step      : pip install lifelines  OR  provide missing column names
───────────────────────────────────────
```

## Statistical Methods

- **Kaplan-Meier Estimator**: Ŝ(t) = Π(tᵢ≤t) (1 − dᵢ/nᵢ), Greenwood's formula for variance
- **Log-Rank Test**: Weighted comparison of survival curves; null = no group difference
- **Cox Proportional Hazards**: h(t|X) = h₀(t) × exp(βX); check PH assumption via Schoenfeld residuals

**High-risk scenarios requiring biostatistician review:**
- Small sample sizes (< 30 per group)
- Heavy censoring (> 50%)
- Proportional hazards assumption violations
- Time-varying covariates

## Output Requirements

Every response must make these explicit when relevant:

- Objective or requested deliverable
- Inputs used and assumptions introduced
- Workflow or decision path
- Core result, recommendation, or artifact
- **Statistical Caveats**: Surface relevant high-risk scenario warnings (small n, heavy censoring, PH violations, time-varying covariates) whenever they apply
- Constraints, risks, caveats, or validation needs
- Unresolved items and next-step checks

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what can still be completed safely, and provide the manual fallback above.
- Do not fabricate files, citations, data, search results, or execution outcomes.

## Input Validation

This skill accepts: CSV datasets with time-to-event and event indicator columns for Kaplan-Meier survival analysis and Cox regression.

If the request does not involve survival analysis — for example, asking to perform logistic regression, ROC curve analysis, general linear modeling, or **time-varying covariate analysis** — do not proceed. Instead respond:

> "survival-analysis-km is designed for Kaplan-Meier survival analysis and Cox regression. Your request appears to be outside this scope. Please provide a dataset with time and event columns, or use a more appropriate tool for your task. For time-varying covariate analysis, consider the `survival` package in R."

## Response Template

Use this fixed structure for non-trivial requests:

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Statistical Caveats (high-risk scenario warnings if applicable)
7. Risks and Limits
8. Next Checks

For simple requests, compress the structure but keep assumptions and limits explicit when they affect correctness.

## Prerequisites

```bash
pip install -r requirements.txt
# Requires: lifelines, matplotlib, seaborn, pandas, numpy, scipy
```
