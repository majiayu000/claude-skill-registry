---
name: motherduck-build-cfa-app
description: Design a MotherDuck-backed customer-facing analytics app. Use when building embedded or product analytics for external users and the decision depends on per-customer isolation, backend routing, service-account boundaries, read scaling, or Hypertenancy-style patterns.
argument-hint: [app-or-tenant-scenario]
license: MIT
---

# Build a Customer-Facing Analytics App

Use this skill when the user is embedding analytics into a product for external users and needs a concrete serving architecture, not just a dashboard.

This is a use-case skill. It orchestrates `motherduck-connect`, `motherduck-explore`, `motherduck-model-data`, `motherduck-query`, and `motherduck-load-data`.

## Start Here: Is a MotherDuck Server Active?

Always determine this first.

- If a **remote MotherDuck MCP server** or **local MotherDuck server** is active, use it.
- If the user has not said which database backs the project, ask for the target database or workspace before designing the app.
- Then inspect the live data model:
  - databases and schemas
  - tables and views
  - columns and types
  - join keys
  - time dimensions
  - core serving metrics
- Use that discovery to shape the serving pattern, tenant boundaries, and example code.

Do not jump straight to an architecture diagram if live data discovery is available.

If no server is active, ask for a representative schema excerpt or table list and keep assumptions explicit.

## Use This Skill When

- The user needs embedded or product-facing analytics.
- Tenant isolation or blast radius matters.
- Read concurrency and latency matter.
- The project needs a backend contract, not just a Dive.
- The requirement is stronger than an internal dashboard or a read-only embed.

## Default Serving Choices

- **3-tier CFA** is the default:
  - browser -> backend API -> MotherDuck
- **Embedded Dives** are acceptable when:
  - the requirement is read-only
  - the product just needs a live dashboard surface
  - app-side policy and UX control are limited
- **DuckDB-Wasm** is acceptable only for small, browser-side, read-only workloads.
- **Single shared tenant_id filtering** is the fallback, not the recommendation.

## Workflow

1. Confirm whether live MotherDuck discovery is available.
2. Explore the actual data model that will back the app.
3. Choose the serving pattern:
   - 3-tier app
   - embedded Dive
   - browser-only prototype
4. Design the isolation model:
   - per customer database
   - per workload or service-account boundary
5. Choose the connection path and read-scaling posture.
6. Produce the implementation plan, API contract, and rollout sequence.

When this skill produces a native DuckDB (`md:`) connection, watermark it with `custom_user_agent=agent-skills/<latest-available-skills-version>(harness-<harness>;llm-<llm>)`. If metadata is missing, fall back to `harness-unknown` and `llm-unknown`.

## Output

The output of this skill should be:

- a recommended serving architecture
- the isolation model
- the connection strategy
- the first implementation slice
- the validation and rollout plan

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

- `references/CFA_IMPLEMENTATION_GUIDE.md` -- preserved detailed implementation content that used to live in this skill
- `references/CFA_ARCHITECTURE.md` -- architecture comparison, isolation model, and connection-path detail

## Runnable Artifact

- `artifacts/customer_routing_example.py` -- MotherDuck-backed Python example showing per-customer routing with separate database namespaces
- `artifacts/customer_routing_example.ts` -- TypeScript companion artifact with the same routing contract and output shape

Run it with:

```bash
uv run --with duckdb python skills/motherduck-build-cfa-app/artifacts/customer_routing_example.py
```

Run the same artifact against temporary MotherDuck databases:

```bash
MOTHERDUCK_ARTIFACT_USE_MOTHERDUCK=1 \
uv run --with duckdb python skills/motherduck-build-cfa-app/artifacts/customer_routing_example.py
```

Validate the TypeScript companion artifact:

```bash
uv run scripts/test_typescript_artifacts.py
```

## Related Skills

- `motherduck-connect` -- choose the correct PG endpoint or native DuckDB path
- `motherduck-explore` -- inspect the live database and schema before choosing an architecture
- `motherduck-model-data` -- design analytics-ready per-customer tables
- `motherduck-query` -- validate serving queries and latency-sensitive aggregations
- `motherduck-load-data` -- build ingestion paths for customer-facing data refresh
