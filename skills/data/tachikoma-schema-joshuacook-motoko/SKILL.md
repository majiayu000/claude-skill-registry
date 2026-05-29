---
name: tachikoma-schema
description: Analyze a Context Lake workspace and propose schema improvements. Use when asked to run schema cleanup, analyze workspace structure, create or update schema.yaml, or identify entity types.
allowed-tools: Read, Write, Glob, Grep
---

# Tachikoma Schema Cleanup

You are running schema cleanup on a Context Lake workspace. Your job is to analyze the workspace structure and propose schema improvements by creating decision files.

## Context Lake Structure

The workspace IS the Context Lake. Entity directories live at the workspace root:
- `.claude/schema.yaml` - Entity type definitions (may not exist yet)
- `.claude/tachikoma-summary.yaml` - Previous observations
- `{entity_type}/` - Entity directories (tasks/, notes/, roles/, etc.)
- `decisions/` - Where you write proposals

There is NO `lake/` subdirectory.

## Schema Format

Motoko uses this exact schema format:

```yaml
entities:
  {entity_type}:
    directory: {entity_type}         # Relative to workspace root
    naming: "{slug}.md"              # Filename pattern
    frontmatter:
      required: [field1, field2]     # Must be present
      optional: [field3, field4]     # May be present
      defaults:                      # Defaults for new entities
        status: open
```

DO NOT add fields like `description`, `structure`, `sections`, `types`, or `taxonomy` - these are not part of the schema format.

## What to Look For

1. **Missing entity types**: Directories without schema definitions (need 3+ files with consistent patterns)
2. **Missing required fields**: Frontmatter fields in ALL entities of a type
3. **Missing optional fields**: Frontmatter fields in SOME entities (multiple files, not just one)
4. **Naming patterns**: How files are named (date-based, slug-based, etc.)

## Process

1. Read `.claude/schema.yaml` if it exists
2. Read `.claude/tachikoma-summary.yaml` for previous observations
3. List workspace root directories (ignore .claude, .git, node_modules, etc.)
4. For each directory with 3+ .md files, sample files to identify patterns
5. Create ONE consolidated decision file in `decisions/`
6. Update `.claude/tachikoma-summary.yaml` with findings

## Decision Format

Write decisions to `decisions/` directory with frontmatter:

```markdown
---
title: "schema: create initial schema.yaml"
status: pending
decision_type: schema_update
confidence: 0.9
created_at: {ISO timestamp}
---

## Current State

No schema.yaml exists. Found N entity types.

## Suggested Change

Create .claude/schema.yaml:

```yaml
entities:
  tasks:
    directory: tasks
    naming: "{slug}.md"
    frontmatter:
      required: [title, status]
      optional: [priority, due]
      defaults:
        status: open
```

## Reasoning

Analyzed X files across Y directories. Patterns observed: ...
```

## Guidelines

- **CONSOLIDATE**: One decision per schema file, not per entity type
- **BE CONSERVATIVE**: Don't infer from single examples
- **SAMPLE ADEQUATELY**: Read at least 3 files per entity type
- When in doubt, make fields optional rather than required

## Output

When done, update `.claude/tachikoma-summary.yaml`:

```yaml
last_scan: {ISO timestamp}
cleanup_mode: schema
entity_counts:
  tasks: 10
  notes: 5
observations:
  - Schema exists with 3 entity types
  - Found 2 directories without definitions
pending_decisions:
  - schema-add-companies.md
```
