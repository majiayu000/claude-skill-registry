---
name: compound-apply-spec
description: Write a CompoundSpec v2 JSON payload and apply it via compound_apply to create/update skills, instincts, and docs.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-27T17:03:09.731823+00:00"
  updated_at: "2026-01-27T17:03:09.731823+00:00"
  version: "1"
  tags: "skills,compounding,schema"
---
<!-- BEGIN:compound:skill-managed -->
## Why this exists

The plugin is deterministic. The agent is not.
So we separate:

- **Agent**: decides what to learn (writes the spec).
- **Tool** (`compound_apply`): validates and applies changes safely.

## CompoundSpec v2

Top-level keys (all optional except `schema_version`):

- `schema_version`: must be `2`
- `auto`: `{ reason, sessionID }`

### `instincts`

- `create[]`: `{ id, title, trigger, action, confidence }`
- `update[]`: `{ id, confidence_delta, evidence_note }`

### `skills`

- `create[]`: `{ name, description, body }`
- `update[]`: `{ name, description?, body }`

Notes:
- `name` must match `^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$`.
- `body` is markdown **without** frontmatter.
- If updating a skill: `skills.update[].body` must be the **entire final** managed body (no snippets/diffs).

### `docs`

- `sync`: boolean (refresh derived indexes/blocks)
- `blocks.upsert[]`: `{ file, id, content }`

Only upsert AI-managed blocks; do not rewrite human-owned text.

When writing markdown content inside `docs.blocks.upsert[].content`:
- Use repo-root-relative paths when referencing files/dirs (no absolute paths).

### `changelog`

- `{ note }`: a single sentence describing the memory delta.

## Apply

1. Draft the CompoundSpec v2 as a single JSON object.
2. Output JSON only (no code fences, no commentary).
3. Run `compound_apply()` to validate and write the memory/doc updates.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
