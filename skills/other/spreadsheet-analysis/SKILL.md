---
name: spreadsheet-analysis
description: Inspect, profile, clean, reconcile, analyze, visualize, and verify spreadsheet data while preserving formulas, formatting, types, and source files. Use when working with .xlsx, .xlsm, .xls, .ods, .csv, or .tsv files; answering questions from a workbook; auditing formulas or data quality; comparing sheets or versions; producing pivots, charts, forecasts, or summary workbooks; repairing malformed tables; or validating that spreadsheet edits and calculations are accurate.
---

# Spreadsheet Analysis

Preserve the source workbook, distinguish stored values from formulas, and support every conclusion with reproducible checks.

## Inputs

Collect or state:

- Source file(s), business question, intended audience, output format, and acceptance criteria.
- Relevant sheets/ranges, keys, units, currencies, date/time zones, accounting signs, and reporting period.
- Whether formulas, formatting, comments, hidden content, macros, external links, pivots, charts, and protection must remain intact.
- Authoritative totals or source systems for reconciliation.
- Confidentiality constraints and whether local-only processing is required.

Do not guess the meaning of unlabeled fields or ambiguous blanks, zeros, percentages, dates, and IDs. Record assumptions.

## Output contract

Return:

1. Source path, hash, format, workbook/sheet inventory, and analysis scope.
2. Findings with metric definition, formula or method, filters, units, period, denominator, and evidence location.
3. Data-quality and formula issues separated from business conclusions.
4. A new output workbook/data file when edits are requested; never silently overwrite the source.
5. Reconciliation, recalculation, re-open, and visual inspection results with limitations.

Clearly label calculated, estimated, cached, missing, and externally sourced values. Do not claim a workbook was recalculated if only cached formula results were read.

## Workflow

### 1. Preserve and inventory

- Resolve exact paths, calculate source hashes, and work from a copy or new output path.
- Do not open untrusted workbooks with macros enabled or refresh external connections.
- Run the bundled read-only profiler from this skill directory for CSV, TSV, XLSX, or XLSM inventory:

```bash
python3 scripts/profile_table.py /path/to/data.csv --pretty
python3 scripts/profile_table.py /path/to/workbook.xlsx --pretty
python3 scripts/profile_table.py /path/to/data.csv --output /path/to/profile.json --pretty
```

The script uses the Python standard library, streams logical CSV/TSV records (including quoted multiline fields), applies byte/row/field/member limits, does not calculate formulas, and does not modify the file. It does not emit profiled data-row cell values, but it does emit headers, sheet names, counts, numeric ranges, and structural metadata. With `--output`, it refuses input aliases and non-regular destinations, then atomically creates or replaces the report via a sibling temporary file. A `partial`, `row_limit_reached`, or `skipped_*` status means the inventory is incomplete; review the stated limit instead of treating the profile as a verdict.

### 2. Choose an available toolchain

Read [tool-routing.md](references/tool-routing.md). Inventory the installed spreadsheet application, Python/JavaScript libraries, and converters before selecting one. Prefer a workbook-aware engine when formulas, styles, charts, pivots, macros, or named ranges matter. Prefer a dataframe/query engine for tabular analysis after the workbook semantics are understood.

Do not install dependencies, upload data, or convert formats without permission. Conversion can lose formulas, formats, macros, dates, comments, charts, or multiple sheets.

### 3. Open or render a baseline

Open the original in a trusted spreadsheet application when available. For an untrusted original, require the controls defined in step 8: protected/read-only input, macros/VBA/events/add-ins/DDE disabled, no link/query refresh, and no network. If those controls cannot be verified, retain the static profiler output as partial and stop before application open or recalculation. Capture a visual baseline for every relevant sheet and any dashboard, print layout, chart, or unusual formatting. Inventory:

- Visible, hidden, and very-hidden sheets; used ranges; headers; merged cells; tables; filters; freezes; and defined names.
- Formulas, cached values, errors, array/spill formulas, circular references, and calculation mode.
- External links, data connections, queries, macros, validation rules, comments, and protection.
- Units, number formats, date systems, locale assumptions, and blank/null conventions.

Treat hidden rows/sheets as in scope for integrity and security, not automatically as analysis data.

### 4. Define the analytical grain

Identify what one row represents, the primary key, allowed duplicates, dimensions, measures, period boundaries, and join cardinality. Build a data dictionary for ambiguous columns. Read [analysis-checklist.md](references/analysis-checklist.md) for profiling and reconciliation checks.

Create a normalized analysis copy when necessary; retain source row identifiers so every result can be traced back.

### 5. Validate and reconcile before interpreting

Check row counts, duplicate keys, missingness, type drift, invalid categories, date gaps, outliers, formula inconsistencies, hidden exclusions, and join multiplication. Reconcile key totals to an authoritative control or explain why no control exists.

Inspect formulas as formulas and values separately. Detect hard-coded constants inside formula regions, relative-reference drift, mixed signs, inconsistent ranges, and error suppression. Never replace a formula with a value silently.

### 6. Analyze with explicit definitions

State the metric definition before calculating. Use precise filters, denominators, period logic, units, and rounding. Preserve full precision in calculations and round only for presentation. Separate descriptive results from forecasts or causal claims. For forecasts, document horizon, method, training window, seasonality, uncertainty, and backtest performance.

### 7. Create outputs minimally

Write only requested changes to a new workbook or table. Preserve formats, formulas, names, hidden state, validations, macros, and charts unless intentionally changed. Use formulas when recipients need an auditable model; use fixed values only when requested and label them.

Use [analysis-report-template.md](assets/analysis-report-template.md) for a standalone evidence record.

### 8. Recalculate, re-open, and render

When formulas were added or changed, recalculate with an actual compatible calculation engine only inside a controlled profile. For an untrusted workbook, first verify that macros, VBA and workbook events, DDE, add-ins, external-link/data-connection refresh, network access, and automatic updates are disabled. Use an isolated low-privilege environment with no secrets and a read-only source. If those controls cannot be guaranteed, do not recalculate the untrusted file.

Re-open the saved output and verify formulas, stored values, errors, names, links, and sheet structure. Render or open every changed sheet plus representative unchanged sheets. Inspect headers, widths, number formats, clipped text, chart ranges, print areas, and conditional formatting. If any result depends on a macro, event handler, add-in, connection, or external link that remained disabled, label that result `unverified—active dependency not executed`; do not substitute cached values for verification.

Re-run reconciliations and spot-check source rows against final metrics. Record tool/version differences that could affect formulas or layout.

## Safety and permission boundaries

- Keep personal, financial, health, customer, and confidential data local unless a specific upload is approved.
- Do not enable macros, DDE, external links, add-ins, queries, or refreshes from an untrusted workbook.
- Treat formulas beginning with `=`, `+`, `-`, or `@` in exported text as potential formula injection when reopened in spreadsheet software.
- Do not change production workbooks, publish dashboards, send reports, or refresh live sources without explicit authorization.
- Do not hide exclusions, data-quality failures, estimation, or manual overrides.
- Do not present forecasts, financial calculations, or statistical associations as guaranteed outcomes.
- Avoid logging raw sensitive cell values; use row IDs, ranges, aggregates, or redacted samples.

## Recovery

If analysis or save fails, preserve the source and failed output, record the exact tool/version/error, and restart from the unchanged source. If a workbook was overwritten accidentally, stop further writes and recover from version history or backup; do not improvise destructive repair. If external connections or macros were activated, record what ran, preserve logs, and escalate potential data exposure.

## Examples

### Revenue reconciliation

Request: “Explain why the monthly revenue tab is $48,200 above the ledger export.”

Hash both files, define period/currency/sign rules, profile keys and duplicates, reconcile totals by entity and month, trace the variance to exact rows or formula ranges, and deliver a variance bridge with unresolved items—not a forced match.

### Formula audit

Request: “Check this planning model for broken formulas before the board meeting.”

Open without refreshing links, inventory formulas and hidden sheets, find inconsistent formulas and hard-coded overrides, recalculate in a compatible engine, visually inspect dashboards, and provide cell-level findings with severity and correction options.

### Clean survey results

Request: “Turn this CSV into a summary workbook with charts.”

Preserve the CSV, confirm encoding/delimiter/grain, prevent formula injection, document missing-value and category mappings, calculate reproducible aggregates, create a new workbook, re-open it, and verify chart ranges and totals against the cleaned table.
