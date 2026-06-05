---
name: deepline-analytics
description: "Use this skill when answering business analytics, RevOps, GTM metric, pipeline, revenue, funnel, customer, or warehouse questions with Deepline. Triggers on phrases like 'query Snowflake', 'analyze pipeline', 'total ACV', 'break down by quarter', 'use the semantic layer', 'run a semantic query', or any use of snowflake_get_semantic_layer / snowflake_run_semantic_query. Skip prospecting, enrichment, contact finding, outbound, or personalization workflows; use deepline-gtm for those."
disable-model-invocation: false
---

# Deepline Analytics

Use this skill to answer customer analytics questions through Deepline's warehouse and semantic-layer tools. The goal is not just to run SQL; it is to preserve the customer's business definitions by starting from the semantic layer, validating the query path, and reporting exactly what metric definitions and filters were used.

## Before You Start

Use `deepline-gtm` instead when the task is prospecting, enrichment, contact finding, outbound sequencing, personalization, or row-by-row lead/account research. Analytics questions ask about existing customer data: revenue, pipeline, funnel, conversion, retention, usage, calls, accounts, opportunities, or warehouse tables.

If Snowflake credentials or a semantic layer are missing, stop and report the setup blocker. Guessing table names or falling straight to raw SQL hides the actual problem and usually produces incorrect business definitions.

## Decision Matrix

| User asks... | Job | Start with |
| --- | --- | --- |
| "What is total pipeline by quarter?" | Metric breakdown | `snowflake_get_semantic_layer`, then `snowflake_run_semantic_query` |
| "Break revenue down by product/month" | Dimensional analysis | Inspect semantic tables for revenue metrics and time dimensions |
| "How many opportunities / accounts / calls..." | Simple count metric | Find the semantic count metric before writing SQL |
| "Why does this number look wrong?" | Debug/validation | Run semantic query, inspect returned SQL, then compare with raw SQL only if needed |
| "Query this specific warehouse table" | SQL fallback | Check whether it is represented in the semantic layer; otherwise use `snowflake_run_query` |
| "Upload/edit/read the semantic layer" | Admin setup | Use `snowflake_update_semantic_layer` / `snowflake_get_semantic_layer`, then return here for querying |

## Standard Loop

Use the Deepline CLI for these tools. `snowflake_get_semantic_layer` and `snowflake_run_semantic_query` are Deepline tool IDs invoked with `deepline tools execute ...`; do not search for MCP/deferred tool names first.

1. **Confirm workspace context.** If the result depends on customer setup, run `deepline auth status` so you know which workspace receives the query.
2. **Inspect the semantic layer.** Run `deepline tools execute snowflake_get_semantic_layer ...` before constructing payloads. Use `includeYaml: false` for a quick table list, and `includeYaml: true` when choosing exact metrics, dimensions, or filters.
3. **Map the user's words to semantic objects.** Choose one semantic `table_name`, named `metrics`, named `dimensions` or `time_dimensions`, and named `filters` from the YAML. Do not invent them.
4. **Pilot the smallest useful query.** Start with one metric and low `rowLimit`; expand after it succeeds. This catches missing credentials, missing semantic objects, and warehouse schema drift cheaply.
5. **Inspect returned SQL and rows.** `snowflake_run_semantic_query` returns both result rows and rendered SQL. The SQL is the audit trail and the safest starting point for any raw-SQL fallback.
6. **Answer in business terms.** Name the metric, grouping dimensions, filters/base filters, row limits, and caveats. If the tool says results were limited, say that.

## Fastest Metric Path

For a customer metric question where the semantic table is knowable from the wording, use this exact CLI path. Do not call ToolSearch, do not look for MCP tools, and do not write raw SQL first.

1. Confirm the workspace:

```bash
deepline auth status
```

2. Read the relevant semantic table slice:

```bash
deepline tools execute snowflake_get_semantic_layer --payload '{"includeYaml": true}' --json
```

3. Run the semantic query with both the user-facing label and the sortable date-start dimension:

```bash
deepline tools execute snowflake_run_semantic_query --payload '{
  "type": "metrics",
  "params": {
    "table_name": "OPPORTUNITY",
    "metrics": ["total_pipeline_generated"],
    "dimensions": ["discovery_quarter_label", "discovery_quarter_start"]
  },
  "rowLimit": 100
}' --json
```

4. Read `result.data.rows` directly from the JSON response. Select latest periods by sorting `DISCOVERY_QUARTER_START` descending. Do not chase `extracted_csv` files, shell-sort CSV artifacts, or rerun the semantic query unless the JSON response is unavailable.

5. Do not open saved transcript files, `tool-results/*.txt`, or full semantic-layer blobs with `Read`, `cat`, or ad hoc Python just to confirm names. Large semantic YAML can exceed tool read limits. Use the current command output, targeted text search, or rerun with `includeYaml: false` for a table list before requesting full YAML.

6. Do not treat `rowLimit` as ordering. For labels like `Q226`, parse them as Q2 2026 only if no date-start dimension is available.

Use the same shape for other metrics: replace only `table_name`, `metrics`, and dimensions after confirming names in the semantic layer.

## Semantic Query Contract

The current public Snowflake semantic API accepts typed metrics payloads:

```json
{
  "type": "metrics",
  "params": {
    "table_name": "OPPORTUNITY",
    "metrics": ["num_opportunities"],
    "dimensions": ["close_quarter_label"],
    "filters": ["exclude_renewal_opportunities"]
  },
  "rowLimit": 100
}
```

It also accepts the legacy flat metrics form when needed:

```json
{
  "table_name": "OPPORTUNITY",
  "metrics": ["num_opportunities"],
  "dimensions": ["close_quarter_label"],
  "rowLimit": 100
}
```

Use the typed form by default because it matches the old Aero `run_semantic_query` shape and leaves room for other query types.

### Allowed Concepts

- `table_name` is a semantic table name from the YAML, not the model root name and not necessarily the physical Snowflake table.
- `metrics` are aggregate business definitions. Use them for reported numbers.
- `dimensions` and `time_dimensions` group the metric. Use semantic names, not raw SQL expressions.
- `facts` are row-level values. They can be useful for detail extracts but are not usually the right answer for aggregate reports.
- `filters` are named semantic filters from the YAML.
- `rowLimit` limits returned rows; use low limits for pilots and larger limits only after the payload is correct.

### Latest Periods Are Not Row Limits

Do not use `rowLimit: 5` to answer "last 5 quarters", "latest 12 months", or similar questions. Semantic query results are not ordered unless you explicitly sort the returned rows or run SQL that orders them.

For recent-period questions:

- Prefer pairing a label dimension with its sortable date-start dimension, for example `discovery_quarter_label` plus `discovery_quarter_start`.
- Query enough groups to cover the full period range, such as `rowLimit: 100` for quarters.
- Sort the returned rows by the date-start dimension when present, or parse labels like `Q226` as Q2 2026 before selecting the latest periods.
- Ignore malformed/null buckets like `Q` when choosing latest periods unless the user explicitly asks about missing-date records.
- Only after selecting the latest periods should you present the final N rows to the user.

### Custom SQL Knobs

The semantic tool supports Aero-compatible custom SQL fields:

```text
custom_dimensions
custom_filter_expressions
steps[].source_table
steps[].ts_expr
steps[].filter_expr
steps[].events_sql
```

Use these when the semantic layer has the right table/metric but lacks the exact date bucket or filter the user needs. They are raw SQL snippets, so prefer named semantic dimensions and filters when they exist. Custom dimensions should be expression-first with an alias, for example `DATE_TRUNC('month', close_date) AS close_month`, not alias-first.

## Choosing Semantic Objects

Read the YAML like a business contract:

- Tables describe the grain and base filters. A base filter is automatically applied, so mention it if it materially changes counts.
- Metric descriptions often say which time dimension they pair with. Follow those pairings; using `created_*` instead of `close_*` can change the business meaning.
- Time dimensions frequently have both date-start and label forms. Use label dimensions for user-facing grouped output and date-start dimensions when chronological ordering matters.
- Synonyms are hints, not payload names. The payload should use the canonical `name` unless the tool explicitly supports aliases.
- Relationship-backed fields may appear as qualified semantic names like `sf_account.industry`. Use them only if the YAML defines the relationship and the field.

Bad — invents SQL inside `filters`, so the renderer looks for a named filter with that whole string:

```json
{"filters": ["stage_name = 'Closed Won'"]}
```

Good — uses a named semantic filter when one exists:

```json
{"filters": ["exclude_renewal_opportunities"]}
```

Good — if no named filter exists, keep the semantic metric/table and put the raw predicate in `custom_filter_expressions`:

```json
{"custom_filter_expressions": ["stage_name = 'Closed Won'"]}
```

## Examples

Basic metric:

```bash
deepline tools execute snowflake_run_semantic_query --payload '{
  "type": "metrics",
  "params": {
    "table_name": "OPPORTUNITY",
    "metrics": ["num_opportunities"]
  },
  "rowLimit": 1
}'
```

Grouped metric:

```bash
deepline tools execute snowflake_run_semantic_query --payload '{
  "type": "metrics",
  "params": {
    "table_name": "OPPORTUNITY",
    "metrics": ["total_pipeline_generated"],
    "dimensions": ["discovery_quarter_label"]
  },
  "rowLimit": 100
}'
```

Read the semantic layer:

```bash
deepline tools execute snowflake_get_semantic_layer --payload '{"includeYaml": true}'
```

## Error Handling

Treat errors as diagnostic signal, not noise to hide.

| Error pattern | Meaning | Response |
| --- | --- | --- |
| `SNOWFLAKE_CREDENTIALS_REQUIRED` | Workspace has no Snowflake credentials | Ask user to connect Snowflake; do not retry different payloads |
| "No Snowflake semantic layer is configured" | No saved layer for this workspace | Ask for/upload semantic layer before querying |
| "table not found" in renderer | `table_name` is not a semantic table | Re-read YAML and use a table under `tables:` |
| "metric/dimension/filter not found" | Payload invented or misspelled a semantic object | Re-read YAML; use canonical names |
| SQL compilation `invalid identifier` | Rendered SQL references a warehouse column not available in the active Snowflake schema, or a renderer exposure bug | Show the rendered SQL/error; compare with raw SQL only after preserving the semantic intent |
| Results include blank/null buckets | Data has null dimension values or label expression permits blanks | Report the bucket and consider a named `has_*` filter if present |
| `limited: true` | Returned rows were truncated by `rowLimit` | Say the output is limited; rerun with a higher limit if the user needs all groups |

When a semantic query fails, fix the table/metric/dimension/filter and rerun before claiming an answer. If you fall back to raw SQL, state that it is a fallback and preserve the semantic metric definition you started from.

## Reporting Results

A good analytics answer includes:

- The result in plain business language.
- The semantic table, metrics, dimensions, and filters used.
- Any automatic base filters that matter, such as excluding deleted/test records.
- The time grain and whether it is created-date, close-date, occurred-date, discovery-date, or another business timestamp.
- Whether the result was limited or sampled.
- The rendered SQL when the user is debugging, validating, or likely to reuse it.

Avoid false precision. If the semantic layer says a metric is a forecast, pipeline, ACV, ARR, bookings, or net revenue, use that language exactly. These are not interchangeable.

## Raw SQL Fallbacks

Use `snowflake_run_query` when the question is outside the semantic layer, when you need to debug a warehouse/schema issue, or when the semantic renderer cannot express the requested shape even with custom dimensions/filters. Start from the rendered semantic SQL whenever possible because it carries base filters, joins, and metric definitions.

Do not silently replace a semantic metric with a hand-written approximation. If you change the definition, name the change and explain why.
