---
name: kai-data-dashboard
description: Convert Kai workflow data, CSV exports, audit folders, SDR package outputs, and marketing reports into dashboard-ready specs or lightweight static dashboards. Use when "data dashboard", "operator dashboard", "operator room", "HTML operators room", "sales dashboard", "SDR dashboard", "turn this data into a dashboard", "dashboard handoff", "visualize Kai data", or any request to package sourced marketing, sales, audit, or SDR data for a dashboard or presentation surface.
---

# kai-data-dashboard - Data To Dashboard Handoff

Turn existing Kai artifacts into a dashboard spec, data contract, or lightweight static dashboard. This skill is a companion surface. It should not replace analytics setup, audit analysis, or outbound strategy.

Use `/kai-analytics` when the user needs a tracking plan or attribution model. Use `/kai-html-presentation` when the user needs a client-ready audit deck. Use this skill when the data already exists and needs to become a dashboard-ready operator surface.

## Phase 0: Identify The Source

Accept these inputs:

- `workspace/sdr-operator/<package-slug>/`
- Any folder with `kai-data.json`, `audit-data.json`, `_data-sources.md`, or `_data-gaps.md`
- CSV exports from CRM, ESP, sequencer, ads, analytics, or sales tools
- Markdown reports with source-backed findings
- User-provided metrics and targets

If there is no source folder or file, ask for it. Do not fabricate sample data unless the output is explicitly labeled `internal_demo`.

## Phase 1: Load Provenance

Before designing the dashboard:

1. Read `_data-sources.md`, `_data-gaps.md`, and available JSON/CSV files.
2. Declare data mode: `sales_external`, `onboarding_connected`, `user_provided`, or `internal_demo`.
3. List unsupported fields as gaps.
4. Do not add numbers that are not present in the source.

For audit folders, run:

```bash
python scripts/quality_gates/audit_provenance_lint.py <source-folder> --audit-dir
```

## Phase 2: Choose Dashboard Type

Pick the dashboard type from the source and request:

| Type | Best Fit | Primary View |
|---|---|---|
| `sdr_operator_room` | SDR package, lead ledger, reply data | Pipeline state, source quality, next actions |
| `marketing_ops` | Campaign, content, SEO, ad, lifecycle data | Channel performance and bottlenecks |
| `executive_scorecard` | Monthly/weekly report | KPIs, decisions, risks, next steps |
| `audit_delivery` | Audit folder | Findings, scorecards, fixes, data gaps |
| `connector_health` | API sync or integration data | Source freshness, failures, missing credentials |

Default to `sdr_operator_room` when the source is from `/kai-sdr-operator`.

## Phase 3: Produce Dashboard Artifacts

Write output to:

```text
<source-folder>/dashboard/
```

Required files:

```text
dashboard-spec.md
metrics-dictionary.md
data-contract.json
source-map.md
data-gaps.md
```

Optional file when the user asks for a usable static artifact:

```text
index.html
```

Do not build a full frontend app unless the user asks for implementation. For app builds, hand the spec to the relevant frontend skill or repository code.

## Dashboard Spec Requirements

Each dashboard spec must include:

- Audience: executive, operator, SDR, marketer, client, founder, or analyst.
- Jobs to be done.
- Metric definitions with exact formulas.
- Data source per metric.
- Refresh cadence and freshness warning.
- Widgets, filters, drilldowns, empty states, and error states.
- Alert thresholds with source or hypothesis label.
- Permissions and sensitive-data handling.
- Handoff notes for frontend, BI, or static HTML build.

For SDR dashboards, include:

- Status counts by `sourced`, `enriched`, `approved_for_copy`, `queued`, `sent`, `replied`, `meeting_booked`, `disqualified`, `suppressed`, and `blocked`.
- Source quality table.
- Fit score distribution.
- Next-action queue.
- Reply triage categories.
- Suppression, bounce, opt-out, and complaint warnings.
- Data gaps that block live outreach.

## Static HTML Rules

If writing `index.html`:

- Keep it single-file unless the user requests app integration.
- Use tables for dense operator data.
- Use restrained styling, readable status colors, and responsive layouts.
- Keep critical numbers visible as text, not only canvas or images.
- Include a source footer or source drawer.
- Include empty states for missing metrics.
- Do not hide gaps. Show them as a first-class panel.

## Quality Gates

Before handoff:

1. Confirm every number has a source, retrieval date, or `internal_demo` label.
2. Confirm every metric has a formula or definition.
3. Confirm `_data-gaps.md` or `data-gaps.md` is represented.
4. Confirm no placeholder text remains.
5. Confirm sensitive fields are either excluded, masked, or explicitly approved.
6. If HTML is produced, check desktop and mobile readability.

## Output Summary

Final response should include:

- Dashboard folder path.
- Dashboard type.
- Files produced.
- Data gaps.
- Whether a static HTML dashboard was built or only specified.
