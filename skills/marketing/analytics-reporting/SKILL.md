---
name: analytics-reporting
description: Use for ad campaign performance analysis, weekly trend reporting, data correlation, and actionable optimization insights.
---

# Analytics Reporting

## Overview
This skill guides the execution of precise, data-driven campaign performance analysis. It ensures accuracy, proper sourcing, and actionable insights for weekly trends and optimization.

## When to Use
- Analyzing ad campaign performance
- Generating weekly trend reports
- Correlating data from multiple sources
- Seeking actionable optimization insights
- Validating analytics reports

## Core Principles
- **Data Accuracy First:** Never manually aggregate raw data. Calculations must be precise and reproducible.
- **Source Everything:** Cite the file and row for every single metric reported.
- **Use User-Specified Data:** Use the primary data file specified for all main metrics. Use secondary files only for anomalies.
- **Show Your Work:** Reveal formulas and steps for derived metrics.
- **Actionable Insights:** Convert every metric and finding into a specific, owner-assignable action.
- **Context is Key:** Do not start without confirming data sources and key metrics.

## Workflow

### 1. Context Gathering (Setup)
**Goal:** Gather verified quantitative context before computation.

1.  **Check Configuration:** Ensure data sources and metrics are set.
2.  **Elicit Information:**
    - Path to primary data file (e.g., weekly totals).
    - Optional secondary data file (e.g., daily results).
    - Optional changelog file.
    - List of primary metrics (e.g., "Subscriptions, Revenue, DAU").
    - Main funnel stages if applicable.
3.  **Load & Verify:** Load specified files and check for basic integrity (headers, accessibility).
4.  **Data Quality Alert:** If data is missing/inaccessible, issue a clear alert and stop.

### 2. Analysis Execution
- **Pre-Analysis:** Briefly state purpose and steps (e.g., "Validating data → Analyzing trends...").
- **During Analysis:** Narrate progress succinctly after each major calculation.
- **Persistence:** Continue until a complete, validated report or alert is produced. Never infer missing data.

### 3. Reporting
- **Structure:**
    - **Summary**
    - **Findings**
    - **Correlations**
    - **Recommendations**
    - **Sources**
- **Formatting:**
    - Use `backticks` for metric names, campaign names, file names.
    - Use code fences ` ``` ` for calculations and citations.
    - **Metric Format:** `[Metric Name] +19.6% (920→1,100, W5→W6, [file_name.csv] row 15)`.

### 4. Validation
- Verify all sources are cited.
- Ensure all findings lead to recommendations.

## Output Policy
- **Location:** ALWAYS create reports in `docs/analytics/`.
- **Prohibition:** NEVER write to internal AI directories for reports. Use project-specific output locations.

## Common Mistakes
- Manually aggregating data without showing the formula.
- Forgetting to cite the specific row/file for a number.
- Producing a report without actionable recommendations.
