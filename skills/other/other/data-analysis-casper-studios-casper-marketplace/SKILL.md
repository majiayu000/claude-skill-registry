---
name: data-analysis
description: >
  Data analysis, visualization, and storytelling skill for financial and RevOps contexts.
  Use when: analyzing revenue data, building forecasts, cohort analysis, churn modeling,
  pipeline analytics, creating data-driven reports, building dashboards, cleaning messy data,
  sanity-checking analytical claims, exporting to Excel with formulas, or extracting data from PDFs.
  Features decision logging, bias-aware interpretation, and progressive disclosure
  (slide deck -> detailed report -> full notebook with all decisions documented).
---

# Data Analysis

## Overview

A comprehensive data analysis and storytelling skill optimized for financial, SaaS, and RevOps contexts. This skill provides structured workflows for turning raw data into actionable insights with full transparency on analytical decisions, bias awareness, and progressive disclosure reporting.

## Workflow Overview

Every analysis follows a 7-phase process:

```
1. SETUP    → Initialize Marimo notebook (run init_marimo_notebook.py)
2. INGEST   → Load data, document sources and assumptions
3. EXPLORE  → EDA with logged decisions (why this viz, why this filter)
4. MODEL    → If needed, with interpretable-first approach
5. INTERPRET → Apply bias checklist, hedge appropriately
6. WISHLIST → Document data gaps and proxies used
7. OUTPUT   → Generate appropriate tier (slides/report/notebook)
```

## Decision Logging Protocol

**Every analytical choice must be logged.** This creates an audit trail and enables reproducibility.

### What to Log

| Decision Type | Example | Log Format |
|---------------|---------|------------|
| Data filtering | Removed 47 records with null revenue | `FILTER: [reason] - [count] records affected` |
| Metric choice | Used logo churn vs revenue churn | `METRIC: [chosen] over [alternative] because [reason]` |
| Visualization | Line chart for time series | `VIZ: [type] because [reason]` |
| Assumption | Assumed linear growth for projection | `ASSUMPTION: [statement] - confidence: [H/M/L]` |
| Proxy used | Used support tickets as NPS proxy | `PROXY: [proxy] for [missing data] - quality: [S/M/W]` |

### Log Format in Notebook

```python
# === DECISION LOG ===
# FILTER: Excluded trial accounts - 1,247 records removed
# METRIC: NRR over GRR because expansion is significant factor
# ASSUMPTION: Q4 seasonality similar to prior year - confidence: M
# PROXY: Support ticket sentiment for NPS - quality: Weak
```

## Analysis Workflow Details

### Phase 1: Setup

Run the initialization script to create a new Marimo notebook with pre-built scaffolding:

```bash
python scripts/init_marimo_notebook.py <notebook_name>
```

This creates a `.py` file with:
- Decision log cell (markdown)
- Data loading template
- EDA template cells
- Bias checklist cell

### Phase 2: Data Ingestion

When loading data:
1. Document the source (file path, API, database query)
2. Record row/column counts
3. Note any immediate data quality issues
4. Log assumptions about data freshness

```python
# === DATA SOURCE ===
# Source: sales_data_2024.csv
# Loaded: 2024-01-15
# Records: 15,847 rows x 23 columns
# Note: Data through 2024-01-10, 5-day lag from source system
```

### Phase 3: Exploratory Data Analysis

Follow this EDA checklist:
- [ ] Distribution of key numeric variables
- [ ] Missing value patterns
- [ ] Outlier detection
- [ ] Time series patterns (if applicable)
- [ ] Segment breakdowns
- [ ] Correlation exploration

**Log every visualization choice and filtering decision.**

### Phase 4: Modeling (If Needed)

Prioritize interpretability:
1. **First choice:** Descriptive statistics, cohort analysis
2. **Second choice:** Linear regression, decision trees
3. **Last resort:** Complex ML (document why simpler won't work)

Always provide:
- Model assumptions
- Feature importance / coefficients
- Confidence intervals
- What the model cannot tell us

### Phase 5: Interpretation

**Before finalizing insights, run the bias checklist.** See `references/biases.md` for full checklist.

Quick check:
- [ ] Survivorship bias: Am I only looking at "survivors"?
- [ ] Simpson's paradox: Do segment trends differ from aggregate?
- [ ] Selection bias: Is my sample representative?
- [ ] Small-n warning: Is sample size sufficient for claims?

**Hedge appropriately:**
- Use "suggests" not "proves"
- State confidence levels
- Note what additional data would strengthen conclusions

### Phase 5.5: Validation Gate (MANDATORY)

**⚠️ GATE: Before proceeding to output, you MUST run the data quality validation checklist.**

This is not optional. Run through `references/data-quality-validator.md` before finalizing:

**Critical Patterns Checklist:**
- [ ] **Market Context:** Are YoY changes compared to market/baseline?
- [ ] **Weighting Sensitivity:** If using composite scores, tested 5-6 weight scenarios?
- [ ] **Bootstrap CIs:** For small samples, generated P10/P50/P90 ranges?
- [ ] **Survivorship Quantified:** Data_Availability column added? Coverage % reported?

**Statistical Checks:**
- [ ] Sample sizes disclosed with confidence intervals?
- [ ] Multiple comparisons accounted for?
- [ ] Cherry-picked baselines avoided?

**Logic Checks:**
- [ ] Correlation not claimed as causation?
- [ ] Alternative explanations considered?
- [ ] Back-of-envelope validation passed?

**Methodology Note on Time Horizons:**
When assessing skill vs luck (e.g., sales rep performance, investment returns):
- Longer time horizons (3+ years) reveal inconsistency that short windows hide
- More periods = higher bar for "likely skill"
- A rep who is "top 10%" for 2 quarters could easily be luck
- A rep who is "top 10%" for 12 quarters is more likely skill
- Always state the number of periods analyzed and what that implies for confidence

**Do not proceed to Phase 6/7 until this checklist is complete.**

### Phase 6: Data Wishlisting

Document gaps and proxies. See `references/data-wishlisting.md` for patterns.

Format:
```
## Data Wishlist

| Missing Data | Proxy Used | Quality | Impact on Analysis |
|--------------|------------|---------|-------------------|
| Customer NPS | Support sentiment | Weak | Core finding, needs validation |
| True LTV | 12-month value | Moderate | Acceptable for segmentation |
```

### Phase 7: Output Generation

Choose output tier based on audience and purpose:

| Tier | When to Use | Tool |
|------|-------------|------|
| **Slides** | Executive summary, board deck | `generate_pptx_summary.py` |
| **Report** | Detailed findings, stakeholder review | Markdown/PDF |
| **Notebook** | Full analysis, data team handoff | Marimo .py file |

---

## Data Cleaning Workflow

For messy data that needs cleaning before analysis:

### 1. Profile the Data

```bash
python scripts/profile_data.py <csv_file> --output data_quality_report.md
```

This generates:
- Column-level statistics (nulls, uniques, types)
- Data quality score (A-F grading)
- Suspicious pattern detection
- Suggested cleaning steps

### 2. Apply Cleaning Patterns

Reference `references/data-cleaning.md` for:
- Missing value strategies (drop, impute, flag)
- Outlier detection methods (IQR, z-score, domain rules)
- Common transforms (pivot, melt, merge patterns)
- Type coercion recipes
- Deduplication patterns

### 3. Handle Datetime Issues

Reference `references/datetime-handling.md` for:
- Timezone conversion patterns
- Date parsing for mixed formats
- Fiscal calendar handling (FY vs CY)
- Period aggregation (daily → weekly → monthly)
- Business day calculations

---

## Dashboard Building Workflow

For interactive monitoring dashboards:

### 1. Initialize Dashboard

```bash
python scripts/init_dashboard.py <dashboard_name>
```

This creates a Marimo dashboard with:
- KPI cards row
- Filter sidebar (segment, date range, period)
- Time series trend chart
- Summary data table
- Responsive layout

### 2. Apply Dashboard Patterns

Reference `references/dashboard-patterns.md` for:
- Marimo layout patterns (sidebar, tabs, grid)
- KPI card templates with sparklines
- Filter/slider patterns for interactivity
- Data table styling and formatting
- Time series with range selection
- Refresh patterns for live data

---

## Data Quality Validation Workflow

Before presenting or accepting analytical claims:

### Run the Data Quality Validation Checklist

Reference `references/data-quality-validator.md` for comprehensive checklists:

**Statistical Sins:**
- P-hacking / multiple comparisons
- Small sample extrapolation
- Missing confidence intervals
- Cherry-picked baselines

**Chart Crimes:**
- Truncated y-axis
- Dual y-axis manipulation
- 3D charts
- Misleading scales

**Logic Fallacies:**
- Correlation ≠ causation
- Ecological fallacy
- Base rate neglect
- Survivorship bias

**Sanity Checks:**
- Does this pass the smell test?
- Back-of-envelope validation
- Historical comparison
- Cross-source validation

---

## Excel Output Workflow

For exporting analysis results to Excel with proper formulas and formatting:

### Financial Model Standards

Reference `references/xlsx-patterns.md` for:
- Color coding convention (blue=inputs, black=formulas, green=cross-sheet links)
- Number formatting standards (currency, percentages, multiples)
- Formula construction rules (use formulas, not hardcoded values)
- Common formula patterns for analysis

### Verification

After creating Excel files with formulas, always recalculate:

```bash
python scripts/recalc.py output.xlsx
```

This ensures:
- All formulas are calculated (openpyxl doesn't evaluate formulas)
- Zero formula errors (#REF!, #DIV/0!, etc.)
- JSON output shows any errors to fix

---

## PDF Handling Workflow

For extracting data from PDFs or creating PDF reports:

### Extracting Data

Reference `references/pdf-patterns.md` for:
- Text extraction (pypdf, pdfplumber)
- Table extraction to DataFrame
- OCR for scanned documents
- Command-line tools (pdftotext, qpdf)

### Creating Reports

Reference `references/pdf-patterns.md` for:
- Basic report creation with reportlab
- Professional reports with sections and tables
- Embedding matplotlib charts in PDFs
- Merge/split operations

---

## Reference Files

Load these as needed during analysis:

| Reference | When to Use |
|-----------|-------------|
| `references/metrics.md` | Calculating SaaS/RevOps metrics |
| `references/biases.md` | Interpretation phase, before finalizing insights |
| `references/report-templates.md` | Structuring output (pyramid vs consulting style) |
| `references/visualization-guide.md` | Choosing chart types, avoiding anti-patterns |
| `references/data-wishlisting.md` | Documenting gaps, rating proxy quality |
| `references/data-cleaning.md` | Data quality checks, cleaning patterns |
| `references/datetime-handling.md` | Timezone, parsing, fiscal calendars |
| `references/dashboard-patterns.md` | Marimo layouts, KPIs, interactivity |
| `references/data-quality-validator.md` | Data quality validation, detecting issues |
| `references/xlsx-patterns.md` | Excel output, financial model standards, formulas |
| `references/pdf-patterns.md` | PDF extraction, report creation, manipulation |

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/init_marimo_notebook.py` | Initialize analysis workspace | `python scripts/init_marimo_notebook.py <name>` |
| `scripts/generate_pptx_summary.py` | Create slide deck from findings | `python scripts/generate_pptx_summary.py <config.json>` |
| `scripts/profile_data.py` | Generate data quality report | `python scripts/profile_data.py <csv_file>` |
| `scripts/init_dashboard.py` | Scaffold interactive dashboard | `python scripts/init_dashboard.py <name>` |
| `scripts/recalc.py` | Recalculate Excel formulas | `python scripts/recalc.py <xlsx_file>` |

## Technology Stack

| Tool | Purpose | Why |
|------|---------|-----|
| **Marimo** | Notebook environment | Pure Python files, reactive, git-friendly |
| **pandas** | Data manipulation | Reliable LLM code generation, mature ecosystem |
| **Matplotlib/Seaborn** | Visualization | Publication-quality, static, well-supported |
| **python-pptx** | Slide generation | Programmatic PowerPoint creation |
| **openpyxl** | Excel files | Formulas, formatting, financial models |
| **pypdf/pdfplumber** | PDF handling | Extract text, tables; create reports |
| **reportlab** | PDF creation | Professional PDF reports |

## Example Invocations

**Revenue analysis:**
> "Analyze our ARR trends by segment and identify drivers of growth/churn"

**Pipeline analytics:**
> "Build a win rate analysis by deal size and sales rep"

**Cohort analysis:**
> "Create a retention cohort analysis for customers acquired in 2023"

**Forecasting:**
> "Project next quarter revenue based on current pipeline"

**Board deck:**
> "Create an executive summary deck of our key SaaS metrics"

**Data cleaning:**
> "Clean this messy CSV and profile the data quality"

**Dashboard:**
> "Build a dashboard to monitor our key SaaS metrics"

**Data validation:**
> "Validate these findings before I present them"

**Excel output:**
> "Export this analysis to Excel with proper formulas and formatting"

**PDF extraction:**
> "Extract the tables from this quarterly report PDF"

**Financial model:**
> "Create a revenue projection model in Excel with scenario inputs"
