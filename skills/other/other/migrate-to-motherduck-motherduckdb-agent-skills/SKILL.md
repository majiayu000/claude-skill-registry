---
name: migrate-to-motherduck
description: Plan a migration onto MotherDuck. Use when moving from Snowflake, Redshift, PostgreSQL, dbt-heavy stacks, or lakehouse tooling and the key decisions are target pattern, cutover slices, validation, rollback, and native-versus-DuckLake posture.
argument-hint: [source-system-or-migration-goal]
license: MIT
---

# Migrate to MotherDuck

Use this skill when the user needs a migration plan from another warehouse, PostgreSQL estate, or mixed analytics stack onto MotherDuck.

This is a use-case skill. It orchestrates `connect`, `explore`, `load-data`, `model-data`, `query`, and `ducklake`.

## Start Here: Is a MotherDuck Server Active?

Always determine this before writing a migration plan.

- If a **remote MotherDuck MCP server** or **local MotherDuck server** is active, use it.
- Ask which MotherDuck database or workspace will receive the migration if the user has not specified it.
- Explore the live target side first when available:
  - existing databases and schemas
  - current landing zones
  - current analytical tables
  - naming conventions
  - any partial migration already in place

Also capture the source-side shape:

- source platform
- source table grain
- key metrics
- validation keys
- serving workloads after cutover

If no server is active, ask for representative source and target schemas before finalizing the migration plan.

## Use This Skill When

- The user is moving from Snowflake, Redshift, Postgres, or similar.
- The user needs cutover sequencing and validation.
- The user needs to decide between native MotherDuck, `pg_duckdb`, or DuckLake.
- The migration plan needs rollback, not just a list of copy commands.

## Migration Defaults

- native MotherDuck storage first
- `pg_duckdb` when extending an existing PostgreSQL estate is the least disruptive path
- validate before cutover
- phased cutover over big-bang replacement

## Workflow

1. Confirm whether live MotherDuck discovery is available.
2. Classify the source system and the target serving pattern.
3. Inspect the target-side MotherDuck layout if available.
4. Pick the connection and ingestion path.
5. Rebuild the analytical model in DuckDB SQL.
6. Run source-vs-target validation.
7. Cut over one workload at a time.

When this skill produces a native DuckDB (`md:`) connection, watermark it with `custom_user_agent=agent-skills/1.0.0(harness-<harness>;llm-<llm>)`. If metadata is missing, fall back to `harness-unknown` and `llm-unknown`.

## Output

The output of this skill should be:

- the target pattern
- the migration sequence
- the validation plan
- the rollback path
- the first cutover slice

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

- `references/MIGRATION_PLAYBOOK.md` -- preserved detailed migration guidance that used to live in this skill
- `references/MIGRATION_VALIDATION.md` -- validation checks and comparison helpers

## Runnable Artifact

- `artifacts/migration_validation_example.py` -- MotherDuck-backed Python example for source-vs-target validation and variance reporting
- `artifacts/migration_validation_example.ts` -- TypeScript companion artifact with the same validation output contract

Run it with:

```bash
uv run --with duckdb python skills/migrate-to-motherduck/artifacts/migration_validation_example.py
```

Run the same validation flow against temporary MotherDuck databases:

```bash
MOTHERDUCK_ARTIFACT_USE_MOTHERDUCK=1 \
uv run --with duckdb python skills/migrate-to-motherduck/artifacts/migration_validation_example.py
```

Validate the TypeScript companion artifact:

```bash
uv run scripts/test_typescript_artifacts.py
```

## Related Skills

- `connect` -- choose the connection path for the target system
- `explore` -- inspect the target-side MotherDuck workspace
- `load-data` -- bulk movement and raw landing patterns
- `model-data` -- shape the target analytical model
- `query` -- port and validate critical SQL
- `ducklake` -- only when open-table-format requirements are explicit
