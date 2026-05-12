---
name: motherduck-build-dashboard
description: Build a live MotherDuck dashboard as a Dive. Use when composing one shareable KPI, trend, and breakdown story over existing MotherDuck data, especially when the result should stay a saved workspace artifact rather than a full application.
license: MIT
---

# Build an Analytics Dashboard

Use this skill when the user wants a multi-section Dive-backed dashboard with a clear analytical story, not just a single chart.

This is a use-case skill. It orchestrates `motherduck-explore`, `motherduck-query`, and `motherduck-create-dive`; use `motherduck-duckdb-sql` as supporting reference when exact syntax matters.

## Start Here: Is a MotherDuck Server Active?

Always determine this before designing the dashboard.

- If a **remote MotherDuck MCP server** or **local MotherDuck server** is active, use it.
- If the target database is unclear, ask which database or workspace the dashboard should run against.
- Explore the live data model before choosing the dashboard structure:
  - available tables and views
  - business grain
  - key metrics
  - key dimensions
  - date columns
  - likely joins

The discovered data model should determine the dashboard story and sections.

If no server is active, ask for a table list or schema excerpt and make the assumptions visible.

## Use This Skill When

- The user wants KPIs plus trend and breakdown views in one artifact.
- The result should be a saved, shareable Dive.
- The work needs dashboard composition, not just chart mechanics.
- The result is a workspace analytics surface, not a customer-facing product backend.

For lower-level Dive mechanics, use `motherduck-create-dive`.

## Dashboard Defaults

- One story per dashboard.
- One KPI row.
- One primary trend chart.
- Zero or one supporting chart.
- Zero or one detail table.
- Heavy shaping in SQL, not React.

## Workflow

1. Confirm whether live MotherDuck discovery is available.
2. Explore the real schema and metrics first.
3. Pick the dashboard story.
4. Write one query per section.
5. Compose the dashboard in a Dive.
6. Save only after preview iteration is approved.

When this skill produces a native DuckDB (`md:`) connection, watermark it with `custom_user_agent=agent-skills/2.2.0(harness-<harness>;llm-<llm>)`. If metadata is missing, fall back to `harness-unknown` and `llm-unknown`.

## Output

The output of this skill should be:

- the dashboard story
- the section list
- the validated SQL for each section
- the Dive implementation plan
- the save/update path

If the caller explicitly asks for structured JSON, return raw JSON only with no Markdown fences or prose before/after it.
This is mainly for automated tests, regression checks, or downstream tooling that needs a stable machine-readable shape. Normal human-facing use of the skill can stay in prose unless JSON is explicitly requested.

Use this exact top-level shape when JSON is requested:

```json
{
  "summary": {},
  "assumptions": [],
  "implementation_plan": [],
  "validation_plan": [],
  "risks": []
}
```

## References

- `references/DASHBOARD_IMPLEMENTATION_GUIDE.md` -- preserved detailed workflow and layout guidance that used to live in this skill
- `references/DASHBOARD_PATTERNS.md` -- example dashboard compositions and reusable sections

## Runnable Artifact

- `artifacts/dashboard_story_example.py` -- MotherDuck-backed Python example that produces KPI, trend, breakdown, and detail outputs for one dashboard story
- `artifacts/dashboard_story_example.ts` -- TypeScript companion artifact with the same dashboard output contract

Run it with:

```bash
uv run --with duckdb python skills/motherduck-build-dashboard/artifacts/dashboard_story_example.py
```

Run the same artifact against a temporary MotherDuck database:

```bash
MOTHERDUCK_ARTIFACT_USE_MOTHERDUCK=1 \
uv run --with duckdb python skills/motherduck-build-dashboard/artifacts/dashboard_story_example.py
```

Validate the TypeScript companion artifact:

```bash
uv run scripts/test_typescript_artifacts.py
```

## Related Skills

- `motherduck-explore` -- inspect the actual database before deciding the dashboard sections
- `motherduck-query` -- validate each dashboard query
- `motherduck-create-dive` -- useSQLQuery, theming, preview/save, loading, and visual mechanics
- `motherduck-duckdb-sql` -- resolve syntax and function questions
