---
name: related-docs-sync
description: "Maintain bidirectional references in related_docs frontmatter across documentation. Use when linking documents together or when the user asks to sync related docs."
event: doc-update
auto_trigger: true
version: "2.0.0"
last_updated: "2026-01-26"

# Inputs/Outputs
inputs:
  - updated_doc_path
  - old_related_docs
  - new_related_docs
output: sync_report
output_format: "List of updated documents"

# Auto-Trigger Rules
auto_invoke:
  events:
    - "doc-update"
    - "related-docs-change"
  file_patterns:
    - "docs/**/*.md"
  conditions:
    - "related_docs frontmatter modified"

# Validation
validation_rules:
  - "referenced docs must exist"
  - "bidirectional links maintained"
  - "no orphan references"

# Chaining
chain_after: [frontmatter-validation]
chain_before: []

# Agent Association
called_by: ["@Scribe"]
mcp_tools:
  - read_file
  - replace_string_in_file
  - mcp_payment-syste_get_doc_context
---

# Related Documents Sync Skill

> **Purpose:** Maintain bidirectional references in `related_docs` frontmatter across documentation. When doc A references doc B, ensure doc B references doc A.

## Trigger

**When:** Document's `related_docs` section is modified
**Context Needed:** Changed document, old/new references, target docs
**MCP Tools:** `read_file`, `replace_string_in_file`, `mcp_payment-syste_get_doc_context`

## Related Docs Structure

```yaml
related_docs:
  database_schema: "docs/technical/backend/database/04-INVENTORY-SCHEMA.md"
  api_design: "docs/technical/backend/api/INVENTORY-API.md"
  ux_flow: "docs/technical/frontend/ux-flows/INVENTORY-UX.md"
  sync_strategy: "docs/technical/architecture/INVENTORY-SYNC.md"
  feature_design: "docs/technical/backend/features/FEAT-002-INVENTORY.md"
  adr: "docs/technical/architecture/adr/003-INVENTORY-STRATEGY.md"
```

## Relationship Types

| Field             | Points To    | Reverse Field     |
| :---------------- | :----------- | :---------------- |
| `database_schema` | \*-SCHEMA.md | `feature_design`  |
| `api_design`      | \*-API.md    | `database_schema` |
| `ux_flow`         | \*-UX.md     | `api_design`      |
| `sync_strategy`   | \*-SYNC.md   | `ux_flow`         |
| `feature_design`  | FEAT-\*.md   | `database_schema` |
| `adr`             | NNN-\*.md    | `feature_design`  |

## Sync Rules

### Adding Reference

```
Doc A adds: related_docs.database_schema = "path/to/B.md"
    ↓
Doc B gets: related_docs.feature_design = "path/to/A.md"
```

### Removing Reference

```
Doc A removes: related_docs.database_schema = ""
    ↓
Doc B removes: related_docs.feature_design = ""
```

### Renaming/Moving

```
Doc B renamed: old_path → new_path
    ↓
All docs referencing old_path → update to new_path
```

## Workflow

1. **Detect change** - Which related_docs changed?
2. **Parse diff** - Added vs removed references
3. **Load targets** - Read referenced documents
4. **Update targets** - Add/remove reverse references
5. **Validate** - Check all links resolve
6. **Report** - List all changes made

## Validation

After sync:

```yaml
# Doc A references Doc B
A.related_docs.database_schema: "B.md"

# Doc B must reference Doc A
B.related_docs.feature_design: "A.md"
```

## Orphan Detection

Find docs with broken references:

- Reference points to non-existent file
- Reference is not bidirectional
- Document has no related_docs

## Output Report

```json
{
  "synced": [{ "from": "A.md", "to": "B.md", "field": "database_schema" }],
  "orphans": [{ "doc": "C.md", "broken_ref": "deleted.md" }],
  "missing_reverse": [{ "doc": "D.md", "refs": "E.md", "missing_in": "E.md" }]
}
```

## Reference

- [DOCUMENTATION-WORKFLOW.md](/docs/process/standards/DOCUMENTATION-WORKFLOW.md)
- [docs.instructions.md](../instructions/docs.instructions.md)
