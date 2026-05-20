---
name: build-data-spec
description: "Build a structured data spec document for analytics topics by exploring the dbt codebase, identifying relevant events/models/columns, and producing a ready-to-use markdown reference. Use when: (1) starting a new data analysis, (2) documenting events for a feature or domain, (3) creating a reference for an agent or analyst."
tags: [analytics, dbt, documentation, data-spec]
metadata:
  author: aheden
  version: "1.0"
---

# Build Data Spec

## Target Repository

```
~/dwh-data-model-transforms
```

Remote: `origin` -> `github.com/Lightricks/dwh-data-model-transforms.git`
Default branch: `develop`

**All file reads, searches, and explorations must target this directory**, regardless of which repo this skill is invoked from. Use absolute paths (e.g., `~/dwh-data-model-transforms/models/`) or set working directory before running commands.

## When to Use

- User wants to analyze a feature, domain, or event category
- User needs a reference document for an agent or analyst
- User says "pull all events for X", "create a data spec", "document events for Y"
- Starting an analysis that requires understanding which tables, columns, and filters to use


## Output

A markdown file saved to `~/ltx-analytics-agents/docs/{feature}_spec.md`.

**Naming convention:** Use the feature name in snake_case (e.g., `brand_kits_spec.md`, `gen_space_spec.md`, `failed_generations_spec.md`). This filename must match what other agents (e.g., dashboard-builder) use to look up the spec.

## Workflow

### Phase 1: Scope the Topic

Clarify with the user:

1. **What to analyze** -- the feature, domain, or event category (e.g., "failed generations", "brand kit usage", "export events")
2. **Which product** -- LTX Studio, LTX Model, API
3. **Breadth** -- single feature deep-dive or cross-feature overview

If the user's request is broad, propose a focused scope before proceeding.

### Phase 2: Explore the Codebase

Search systematically across all layers in `~/dwh-data-model-transforms`. Use parallel exploration agents for speed.

**Search targets (in priority order):**

All paths below are relative to `~/dwh-data-model-transforms/`.

| Layer | Where to Look | What to Extract |
|-------|--------------|-----------------|
| **Event registry** | `docs/event-registry.yaml` | Canonical event names, key properties, status |
| **Mart models** | `models/**/marts/` | Final columns, filters, action_name/action_category mapping |
| **Intermediate models** | `models/**/intermediate/` | Business logic, joins, derived columns |
| **Base models** | `models/base/` | Raw source columns, process_started/ended pairs |
| **Macros** | `macros/` | Extraction logic, parsing, field derivation |
| **Source definitions** | `models/sources.yml` | Raw event table names |
| **Existing specs** | `docs/*_spec.md` | Related specs to cross-reference |

**Search strategies:**

- Filename search: `Glob` for model names containing the topic keyword
- Content search: `Grep` for column names, event names, action categories
- Semantic search: "How does X work?" scoped to relevant directories
- YAML search: Look at `.yml` files alongside `.sql` for column descriptions and tests

**Read priority:** Always read the SQL model files, not just YMLs. The SQL reveals:
- Actual column derivation logic (CASE statements, COALESCEs, joins)
- Filter conditions that define the event scope
- Macro calls that generate columns
- Incremental predicates and partition fields

### Phase 3: Read Key Models

For each relevant model found in Phase 2, read the full `.sql` file to extract:

1. **TL;DR block** -- model purpose and key features
2. **Config block** -- partition_by, cluster_by, schema, tags
3. **Column definitions** -- all SELECT columns with their derivation logic
4. **Filter conditions** -- WHERE clauses that scope the data
5. **Join logic** -- how tables connect (especially start/end event joins)
6. **Macro calls** -- which macros generate columns (read the macro too)

Also read the `.yml` file for:
- Column descriptions (especially "In this table:" context)
- Accepted values tests (reveal valid column values)
- Data quality tests (reveal important constraints)

### Phase 4: Compile the Spec Document

Write `~/ltx-analytics-agents/docs/{feature}_spec.md` following the structure in [references/spec-template.md](references/spec-template.md).

**Required sections:**

1. **Title + metadata** -- topic, last updated date
2. **Overview** -- what the spec covers, key definitions
3. **Primary tables** -- fully-qualified BigQuery table names, partition/cluster info
4. **Key columns** -- organized by category (error/result, context, timing, parameters, user)
5. **Filtering patterns** -- ready-to-use WHERE clauses for common scenarios
6. **Sample analysis queries** -- 4-6 BigQuery queries answering likely questions
7. **Model lineage** -- ASCII diagram showing source -> base -> intermediate -> mart flow
8. **Key macros** -- macros involved in column derivation
9. **Important notes** -- gotchas, caveats, edge cases

**Writing guidelines:**

- Use fully-qualified BigQuery table names (`` `project.schema.table` ``)
- Include column types (STRING, BOOLEAN, INT64, TIMESTAMP, FLOAT64)
- Show accepted values inline when known from tests
- Always include `NOT is_lt_team` in example queries
- Use partition column in WHERE for cost efficiency
- Provide both simple filters and full analysis queries

### Phase 5: Validate Completeness

Before finalizing, check:

- [ ] Every column referenced in queries exists in the column tables
- [ ] Filtering patterns cover the main use cases the user described
- [ ] Sample queries are syntactically valid BigQuery SQL
- [ ] Lineage diagram traces from source through to mart
- [ ] Important notes capture non-obvious behavior (nullability, edge cases, timing windows)
- [ ] Table names use correct project/schema from model config blocks

## Existing Specs as Reference

Current data spec documents in the project:

| File | Topic | Good Example Of |
|------|-------|-----------------|
| `docs/gen_space_events_spec.md` | Gen Space activity | Filtering patterns, page_workspace breakdown |
| `docs/brand_kits_events_spec.md` | Brand Kit events | Event-to-column mapping, action_category usage |
| `docs/gen_space_lightbox_actions_spec.md` | Lightbox/asset actions | UI-to-event mapping, cross-feature coverage |
| `docs/ltxstudio_failed_generations_spec.md` | Failed generations | Error analysis, multi-layer column tracking |

Read these for style and depth calibration when creating a new spec.

## Checklist

- [ ] Topic scoped and confirmed with user
- [ ] Codebase explored across all layers (mart -> intermediate -> base -> macro)
- [ ] Key model SQL files read (not just YMLs)
- [ ] Spec document written with all required sections
- [ ] Queries validated for correct table names and syntax
- [ ] File saved to `~/ltx-analytics-agents/docs/{feature}_spec.md`
