---
name: visualization
description: Rules for charts and visualization. Use when the user asks for charts, graphs, plots, or visual representations (line, bar, pie, timeseries).
---

# Visualization Skill

When the user asks for charts, graphs, or visual representations, follow this workflow and rules.

## WORKFLOW (MANDATORY ORDER)

**a) Generate or obtain SQL:**
- **CHECK CONTEXT FIRST**: If valid SQL exists in the context (explicitly provided by the user or from a previous message), **USE IT DIRECTLY** and skip to step (b).
- **IF NO SQL FOUND**: You must generate it.
  - **Dependency**: Valid SQL generation REQUIRES the `sql-expert` skill.
  - **Action**: Check if `sql-expert` skill is loaded.
    - If **NOT loaded**: Call the `skill` tool with `['sql-expert']` IMMEDIATELY. Do not proceed to generate SQL until the skill is loaded.
    - If **ALREADY loaded**: Generate the SQL strictly following the rules in the `sql-expert` skill (including Schema Discovery, Schema Fidelity, ProfileEvents handling, and Performance Optimization).

**b) VALIDATION (MANDATORY):**
- **ALWAYS call `validate_sql` with the SQL before including the chart spec in your response.**
- **RETRY LOGIC**: If validation fails, retry up to 3 times by fixing the SQL (referring to `sql-expert` skill rules) and validating again.
- Only proceed to step (c) if validation returns success: true.

**c) After validation passes:**
- **Include the full chart spec in your response** using a markdown code block with language `chart-spec`. The content must be valid JSON matching the OUTPUT FORMAT below, and **must include** `datasource: { "sql": "<the validated SQL>" }`. Derive type, titleOption, legendOption, etc. from the CHART TYPE RULES and OUTPUT FORMAT above. Do not call any tool for this—put the complete spec in your reply.

**d) Execution:**
- **PROHIBITED**: Do **NOT** call `execute_sql`. The chart component in the client will automatically execute the query found in the `chart-spec`. Calling it here wastes tokens and causes duplicate execution.

## CHART TYPE RULES

### STEP 1: CHECK USER'S EXPLICIT CHART REQUEST (HIGHEST PRIORITY)

If user question contains ANY of these keywords, use the corresponding chart type:
- **"line chart"** → type: "line" (MANDATORY)
- **"bar chart"** → type: "bar" (MANDATORY)
- **"pie chart"** → type: "pie" (MANDATORY)
- **"timeseries"** or **"time series"** → type: "line" (MANDATORY)
- **"trend"** → type: "line" (MANDATORY)

### STEP 2: ANALYZE SQL (Only if no explicit chart request in Step 1)

- **"line"** - Time-based data with trends (DateTime/Date + GROUP BY time dimension; "over time", "by day/month/hour").
- **"bar"** - Categorical comparisons (GROUP BY categories; "compare", "by category").
- **"pie"** - Categorical distribution, proportions (single categorical dimension; "distribution", "breakdown", "proportion"; 2 columns: category + numeric value; best for 3-15 categories).
- **"table"** - Raw data listing (LAST RESORT): user asks for "table" or "list" with NO chart keywords; no numeric aggregations.

## CRITICAL RULES

- When legendOption.placement is "bottom" or "right", you MUST include a "values" array: base ["min", "max"]; add "sum"/"count" if SQL uses SUM/COUNT; add "avg" if SQL uses AVG.
- **Line/Bar**: Use "bottom" for GROUP BY with non-time dimensions, "none" for single metric.
- **Pie**: legendOption.placement "right"|"bottom"|"inside" (no "none"); omit legendOption.values; use labelOption (show, format) and valueFormat as needed.

## OUTPUT FORMAT (include in your response as a `chart-spec` code block)

Put the full chart spec in a markdown code block with language **chart-spec**. The JSON **must** include `datasource.sql` (the validated SQL). The client parses this block to render the chart.

### Line/Bar Chart example:
```chart-spec
{
  "type": "line",
  "titleOption": { "title": "Descriptive chart title", "align": "center" },
  "width": 6,
  "legendOption": { "placement": "bottom", "values": ["min", "max", "sum"] },
  "datasource": { "sql": "SELECT ..." }
}
```

### Pie Chart example:
```chart-spec
{
  "type": "pie",
  "titleOption": { "title": "Distribution by Category", "align": "center" },
  "width": 6,
  "legendOption": { "placement": "right" },
  "labelOption": { "show": true, "format": "name-percent" },
  "valueFormat": "short_number",
  "datasource": { "sql": "SELECT ..." }
}
```

- ❌ NEVER include a chart spec before validate_sql has succeeded.
- ❌ NEVER skip SQL generation if no SQL exists in context.
- ❌ NEVER write SQL in your text response—ALWAYS use the instructions in `sql-expert` skill.
- ✅ ALWAYS follow: Check for SQL → If missing, Load `sql-expert` Skill → Validation → Include chart spec in response.
- ✅ If validation fails, retry up to 3 times.
