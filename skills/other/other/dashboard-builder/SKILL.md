---
name: dashboard-builder
description: Creates feature dashboards in Hex Threads. Given a feature name (and optionally a PRD, Figma link, or context), discovers events, builds a metric spec, gets human approval, and instructs Hex to build charts using business context. Hex writes its own SQL — Claude provides context, table/event names, and exact segmentation logic. Use when someone asks to create, build, or generate a feature dashboard.
tags: [analytics, hex, dashboard]
---

# Dashboard Builder (v2 — Hex-led SQL)

> **Key difference from v1:** Claude no longer writes exact SQL for every metric. Instead, Claude provides Hex with rich business context, table names, event names, metric definitions, and exact segmentation CTEs. Hex writes the SQL itself.

## When to use

- "Create a dashboard for {feature}"
- "Build analytics for {feature}"
- "Set up metrics for {feature}"
- "I need usage/retention/funnel for {feature}"
- "Create an analysis for {feature}"

## What it produces

A **Hex Thread** serving as the dashboard, containing:
1. Usage metrics (DAU, WAU, MAU, actions per user, adoption rate)
2. Funnel metrics (step-by-step conversion)
3. Retention metrics (D1/D3/D7/D14/D30)
4. Segmentation (by tier, plan type, country, etc.)
5. Additional metrics that the agent thinks are relevant for the feature

## Flow

```
PHASE 1: DISCOVER → Feature Brief
  ↓
PHASE 2: PLAN → Dashboard Spec + Hex Context Brief
  ↓
✋ HUMAN APPROVES SPEC
  ↓
PHASE 3: BUILD → Hex Thread (business context, Hex writes SQL)
  ↓
PHASE 4: VALIDATE → QA Report + Slack notification
```

---

## Phase 1: Discover

**Goal:** Build a Feature Brief with verified events.

1. **Gather inputs from the user:**
   - Feature name (required)
   - PRD or feature doc (optional)
   - Figma link (optional)
   - Specific metrics or dimensions they care about (optional)

2. **Look up events in the registry:**
   - Read `shared/event-registry.yaml`
   - Find the feature group that matches
   - List all events with their types and status

3. **Query Figma** (if link provided):
   - Use Figma MCP to get screens and flows
   - Map screens to likely user actions
   - Use screen names as keywords to find more events

4. **Search codebase** (if GitHub available):
   - Search for the feature name in tracking code
   - Look for patterns: `analytics.track`, `logEvent`, `trackEvent`
   - Cross-reference any found events against the registry

5. **Search Slack for context** (via Slack MCP):
   - Search for the feature name in relevant channels
   - Look for: PRDs, launch announcements, design discussions, known issues
   - Extract any context that helps understand the feature's purpose, target users, or success criteria
   - Note any stakeholder comments about what metrics they care about

6. **Build or load a Data Spec:**
   - Check if `docs/{feature}_spec.md` already exists
   - If it exists, read it — it contains verified table names, key columns, filtering patterns, and sample queries
   - If it doesn't exist, follow the build-data-spec skill (`.claude/skills/build-data-spec/SKILL.md`) to create one by exploring the dbt codebase at `~/dwh-data-model-transforms`
   - The data spec feeds directly into Phase 2: use its table names, column details, and filtering patterns when building the Hex Context Brief

7. **Present Feature Brief** using template from `agents/dashboard-builder/templates/feature-brief.md`:
   - List all events with verification status (✅ registry / ⚠️ code only / ❓ unverified)
   - Propose funnel steps
   - Propose retention activation + return events
   - Propose segmentation dimensions
   - List open questions

DO NOT proceed to Phase 2 without user confirming the Feature Brief.

---

## Phase 2: Plan

**Goal:** Build a Dashboard Spec and prepare the Hex Context Brief.

1. **Read shared files:**
   - `shared/metric-standards.md` — metric definitions and calculation logic
   - `shared/bq-schema.md` — table names, columns, joins

2. **Determine metric set.**

   **Every feature gets:**
   - Usage: DAU, actions per user, adoption rate
   - Funnel: map steps from the Feature Brief events
   - Retention: D1/D3/D7/D14/D30
   - Segmentation: by user segment (Enterprise, Heavy Users, Paying non-Enterprise, Free — see segmentation queries in `shared/bq-schema.md`)

   **Feature-specific metrics — evaluate per feature:**
   Look at the event's key_properties in `shared/event-registry.yaml`.
   Properties suggest additional metrics:
   - `fetch_result` → success rate (NOTE: column name is `fetch_result` not `result`)
   - `tokens` / `be_cost` → avg cost per action
   - `is_applied` → apply rate (applied / total views)
   - `video_duration_seconds` → avg duration
   - `model_name` / `model_gen_type` → breakdown by model

   Propose feature-specific metrics to the user — they must approve before inclusion.

   If unsure about funnel steps or retention events, ask the user.

3. **Define filters:**
   - Date range (default: last 90 days)
   - User segment (Enterprise, Heavy, Paid, Free — see segmentation queries in `shared/bq-schema.md`)
   - Platform (if applicable)
   - Subscription tier
   - Propose additional filters relevant to the feature

4. **Build dashboard mockup** — show the full layout based on the metrics determined in step 2:

   ```
   ┌──────────────────────────────────────────────────┐
   │  {Feature Name} Dashboard                         │
   │  Filters: {list filters from step 3}              │
   ├──────────────────────────────────────────────────┤
   │  USAGE                                            │
   │  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
   │  │ DAU      │ │ Actions/ │ │ Adoption rate    │ │
   │  │ (line)   │ │ user     │ │ (line or KPI)    │ │
   │  └──────────┘ └──────────┘ └──────────────────┘ │
   ├──────────────────────────────────────────────────┤
   │  FUNNEL                                           │
   │  ┌──────────────────────────────────────────────┐│
   │  │ {Step 1} → {Step 2} → ... → {Step N}        ││
   │  └──────────────────────────────────────────────┘│
   ├──────────────────────────────────────────────────┤
   │  RETENTION                                        │
   │  ┌──────────────────────────────────────────────┐│
   │  │ Cohort × Day-N heatmap                       ││
   │  └──────────────────────────────────────────────┘│
   ├──────────────────────────────────────────────────┤
   │  SEGMENTATION                                     │
   │  ┌──────────────────────────────────────────────┐│
   │  │ {Main metric} by user segment (stacked bar)  ││
   │  └──────────────────────────────────────────────┘│
   ├──────────────────────────────────────────────────┤
   │  FEATURE-SPECIFIC (if approved in step 2)         │
   │  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
   │  │ {metric} │ │ {metric} │ │ {metric}         │ │
   │  └──────────┘ └──────────┘ └──────────────────┘ │
   └──────────────────────────────────────────────────┘
   ```

   Adapt the mockup to the actual metrics.

5. **Prepare the Hex Context Brief** — this is what Hex will receive in the initial message. Compile:
   - Feature description and business context (1-2 paragraphs)
   - The main BigQuery table: `ltx-dwh-prod-processed.web.ltxstudio_user_all_actions`
   - Any additional tables needed (from `shared/bq-schema.md`)
   - Exact event names (action_name / action_name_detailed) from the approved Feature Brief
   - Key column names relevant to the feature (from `shared/bq-schema.md`)
   - Metric definitions in plain language (e.g., "Adoption rate = users who did X / total active users * 100")
   - Retention definition: activation event, return event, windows
   - Funnel steps with event names
   - Exact segmentation CTEs from `shared/bq-schema.md` lines 441-516 (verbatim — see Phase 3 step 0)
   - Important rules: use `lt_id` as user ID, exclude LT team (`is_lt_team IS FALSE`), filter on partition columns, exclude today's incomplete data, use `SAFE_DIVIDE` for percentages

6. **Present full spec** using template from `agents/dashboard-builder/templates/dashboard-spec.md` and dashboard mockup including filters

DO NOT proceed to Phase 3 without explicit user approval ("yes", "go ahead", "approved").
Incorporate any feedback before proceeding.

---

## Phase 3: Build

**Goal:** Create the dashboard in Hex via Threads MCP. Hex writes the SQL — Claude provides context and guidance.

0. **Prepare Segmentation Logic** (if dashboard includes user segmentation):
   - Read `shared/bq-schema.md` lines 441-516 to extract the segmentation CTEs
   - You will need:
     - Enterprise Users CTEs (`ent_users` and `ent_users_final`)
     - Heavy Users CTE (`heavy_users_over_time` with `weeks` helper)
     - The segmentation hierarchy logic
   - **CRITICAL:** You must paste these CTEs verbatim into the initial Hex prompt
   - **Do NOT** tell Hex to "use the segmentation from bq-schema.md" or describe it in words
   - Hex will approximate and produce wrong results unless given exact segmentation SQL

1. **Read `agents/dashboard-builder/hex-prompts/patterns.md`** — follow prompt patterns for how to communicate with Hex.

2. **Start the Thread** with `create_thread`:
   - Send the full Hex Context Brief prepared in Phase 2 step 5
   - Include the segmentation CTEs verbatim (if applicable)
   - Include the first metric request in business terms
   - Tell Hex which table(s) and event names to use, but let it write the SQL

3. **Add each metric** with `continue_thread`:
   - ONE chart per message
   - Describe the metric in business terms: what to measure, what events to use, what chart type
   - Provide table names, event names, and column names as hints
   - Specify chart type, title, and formatting expectations
   - Do NOT write the SQL — let Hex handle it

4. **Poll `get_thread`** after each message until status = "idle"
   - **Check Hex's response carefully:**
     - If Hex asks a question: STOP and answer it via `continue_thread`
       - If you know the answer: provide it immediately
       - If you DON'T know: ask the human user for clarification, then relay their answer to Hex
     - If Hex reports SQL errors: help it debug by providing relevant column names or table structure from `shared/bq-schema.md`. If you can't resolve the error after 2 attempts, escalate to the human user.
     - If Hex reports `AGENT_OVERLOADED` or capacity errors: wait 1 minute, then `continue_thread` with "try again" and restate the full context. Do NOT fall back to writing SQL queries — always let Hex write its own SQL.
     - If Hex says "Ready for next task": proceed to the next metric
   - **NEVER skip Hex's questions** — always address them before moving to the next metric

5. **Run data quality checks** after each query executes:
   - **Review Hex's output** to validate data quality
   - **Check for quality issues** (see Data Quality Validation section below)
   - **If issues found:** Tell Hex to add a warning or fix the query
   - **Continue with next metric** — data quality warnings are non-blocking

6. **Known blocker:** Hex MCP cannot convert a Thread into a Hex Project. After the Thread is complete, the user must do this manually in Hex (Thread → Save as Project).

---

## Data Quality Validation

**Goal:** Detect and report data quality issues during query execution.

After each metric executes in Hex, review the results and check for:

### 1. Missing or NULL Values
- **Check:** Critical columns contain NULLs (e.g., `lt_id`, `action_ts`, metric values)
- **Action:** Ask Hex to add a warning note if >5% NULLs in critical columns

### 2. Unexpected Row Counts
- **Check:**
  - Zero results returned
  - Suspiciously low counts (< 10 rows for time series)
  - Suspiciously high counts (> 10M rows suggesting missing filters)
- **Action:** Ask Hex to check its query. Provide hints about correct filters or event names.

### 3. Date Gaps in Time Series
- **Check:** Missing dates in daily/weekly series (more than 1 day gap)
- **Action:** Ask Hex to add a warning note about the gap

### 4. Invalid Values
- **Check:**
  - Negative values where not expected (counts, durations, costs)
  - Percentages > 100% or < 0%
  - Retention rates increasing (should be monotonically decreasing per cohort)
  - Funnel steps not decreasing (Step 2 > Step 1)
- **Action:** Ask Hex to review its query logic. Provide the correct metric definition from `shared/metric-standards.md`.

### 5. Schema Mismatches
- **Check:** Query fails due to missing columns or wrong table names
- **Action:** Provide the correct column/table name from `shared/bq-schema.md`

### 6. Sample Size Warnings
- **Check:** Cohort sizes < 100 users, segment sizes < 50 users
- **Action:** Ask Hex to add a note about small sample size

---

## Phase 4: Validate

**Goal:** Check output and share with stakeholders.

1. Do a final `get_thread` to review the complete Thread.

2. Check for issues:
   - Any SQL errors reported by Hex?
   - Any charts with zero results or empty data?
   - Do funnel steps decrease monotonically?
   - Does retention decrease monotonically per cohort?

3. **Ask Hex to validate and optimize its own queries:**
   - Send a `continue_thread` message asking Hex to review all SQL queries in the Thread
   - Hex should check for:
     - **Correctness:** Wrong column names, table names, join logic, or filters
     - **Redundant CTEs:** Multiple charts re-running identical segmentation CTEs — consolidate into shared upstream dataframes where possible
     - **Partition pruning:** Ensure `action_ts` filters are applied for BigQuery performance
     - **Unnecessary scans:** Missing WHERE clauses, selecting unused columns, full-table scans
     - **Approximation opportunities:** Use `APPROX_COUNT_DISTINCT` where exact counts aren't needed
   - Hex should apply fixes directly and report: (a) correctness issues found, (b) optimizations applied, (c) estimated performance impact
   - Review Hex's optimization report before proceeding

4. **Aggregate data quality warnings:**
   - Review all warnings added during Phase 3
   - Summarize by severity:
     - **Critical:** Missing data, schema errors, invalid logic
     - **Warning:** Small sample sizes, minor gaps
     - **Info:** Performance suggestions, optimization opportunities

5. **Report to user:**
   ```
   ✅ Dashboard created: {Thread URL}

   Metrics: {metrics},
            Segmentation by {dimensions}

   ⚠️ Data Quality Issues (if any):
   Critical:
   - {Schema errors, missing data, invalid values}

   Warnings:
   - {Small sample sizes, date gaps, NULL values}

   Info:
   - {Performance suggestions}

   Manual step needed:
   - Convert Thread to Hex Project for long-term use

   Next steps:
   - {Suggested additions or improvements}
   ```

6. **Write a Hex Project organization prompt for the user:**
   - Hex Threads cannot organize layout, add headers, or structure the dashboard — but Hex Projects can.
   - After the Thread is converted to a Project, the user needs to ask Hex to organize it.
   - Write a ready-to-paste prompt for the user to send to Hex inside the Project. The prompt should tell Hex to:
     - Group charts into logical sections with markdown headers (e.g., "Health Metrics", "Feature Adoption", etc.)
     - Order charts in the sequence from the dashboard spec
     - Add a brief intro/summary section at the top with dashboard title, date range, and segment definitions
     - Clean up any leftover debug cells or duplicate charts from the Thread
     - Apply consistent formatting (chart titles, axis labels, color palettes)
   - Present this prompt to the user with instructions: "After converting the Thread to a Project, paste this into the Hex Project chat."

7. **Draft a stakeholder summary message:**
   - Write a short, ready-to-send message for the PM/stakeholder who requested the dashboard
   - Include: what was built (scope), the Thread link, and 3-5 key findings distilled from the charts
   - Highlight the strongest signals (positive and negative) — don't just list metrics, tell the story
   - Flag anything that needs attention (data anomalies, unexpected results, features with zero usage)
   - Keep it concise — a few sentences, not a wall of text

---

## Reference Files

### Shared (all agents)
| File | Read in phase |
|------|---------------|
| `shared/product-context.md` | Phase 1 |
| `shared/bq-schema.md` | Phase 2, Phase 3 (segmentation CTEs) |
| `shared/event-registry.yaml` | Phase 1 |
| `shared/metric-standards.md` | Phase 2 |

### Agent-specific
| File | Read in phase |
|------|---------------|
| `docs/{feature}_spec.md` (if exists) | Phase 1, Phase 2 |
| `.claude/skills/build-data-spec/SKILL.md` | Phase 1 (if spec missing) |
| `agents/dashboard-builder/hex-prompts/patterns.md` | Phase 3 |
| `agents/dashboard-builder/templates/feature-brief.md` | Phase 1 |
| `agents/dashboard-builder/templates/dashboard-spec.md` | Phase 2 |

## Rules

1. **Never invent event names.** Only events from `shared/event-registry.yaml` or confirmed by user.
2. **Never skip human approval.** Present spec → wait for approval → then build.
3. **One chart per Hex message.** Never combine multiple charts.
4. **Always provide segmentation CTEs verbatim.** This is the one thing Hex cannot figure out on its own.
5. **Always use `lt_id`.** Never `anonymous_id`. Tell Hex this explicitly.
6. **Always run data quality checks.** Review Hex's query results and flag issues.
7. **Let Hex write the SQL.** Provide business context, table names, event names, and metric definitions — not exact queries. Guide Hex if it gets stuck, but don't take over.
8. **Correct Hex when wrong.** If Hex uses wrong columns, tables, or logic, provide the correct information from the shared files. Don't let bad queries go unchecked. If you can't fix it after 2 attempts, stop and ask the human user for help.
9. **Always use full time periods.** Never show partial weeks, months, or days in charts. When aggregating weekly, exclude the first partial week (if the date range starts mid-week) and the current incomplete week. When aggregating monthly, exclude partial months at start/end. Every data point must represent a complete time window. Tell Hex to apply this filtering in the initial context message.
10. **Use `action_name_detailed` for generation filtering.** When filtering for specific generation types (e.g., `generate_video`, `generate_image`), always use `action_name_detailed`, NOT `action_name`. Hex tends to default to `action_name` which can produce incorrect results. Tell Hex this explicitly in the context message and correct it if it uses the wrong column.
