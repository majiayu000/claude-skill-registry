---
name: doc-index-update
description: "Maintain table of contents and index files across documentation. Use when adding, removing, or renaming documentation files."
event: doc-change
auto_trigger: true
version: "2.0.0"
last_updated: "2026-01-26"

# Inputs/Outputs
inputs:
  - docs_directory
  - changed_files
  - action (create|delete|rename)
output: updated_indexes
output_format: "Updated README.md index files"

# Auto-Trigger Rules
auto_invoke:
  events:
    - "doc-change"
    - "doc-creation"
    - "doc-deletion"
  file_patterns:
    - "docs/**/*.md"
  conditions:
    - "documentation file created"
    - "documentation file deleted"
    - "documentation file renamed"

# Validation
validation_rules:
  - "all docs in directory listed"
  - "links must be valid"
  - "sorted alphabetically or by number"

# Chaining
chain_after: [documentation, adr-creation, schema-doc-sync, api-doc-generation]
chain_before: []

# Agent Association
called_by: ["@Scribe"]
mcp_tools:
  - list_dir
  - read_file
  - replace_string_in_file
---

# Documentation Index Update Skill

> **Purpose:** Maintain table of contents and index files across documentation. Auto-updates when docs are added, removed, or renamed.

## Trigger

**When:** Any documentation file is created, deleted, or renamed
**Context Needed:** Changed file path, action type, existing index
**MCP Tools:** `list_dir`, `read_file`, `replace_string_in_file`

## Index Files

| Directory                          | Index File | Purpose                |
| :--------------------------------- | :--------- | :--------------------- |
| `docs/`                            | README.md  | Main documentation hub |
| `docs/technical/architecture/`     | README.md  | Architecture overview  |
| `docs/technical/backend/database/` | README.md  | Schema index           |
| `docs/technical/frontend/`         | README.md  | Frontend docs index    |
| `docs/templates/`                  | README.md  | Template guide         |

## Index Format

```markdown
# [Directory Name]

## Contents

| Document            | Type           | Status   | Description       |
| :------------------ | :------------- | :------- | :---------------- |
| [Doc Name](path.md) | feature-design | approved | Brief description |
```

## Auto-Generated Sections

### From Frontmatter

```yaml
document_type: "feature-design" # → Type column
status: "approved" # → Status column
# First line of content          # → Description
```

### Directory Tree

```markdown
## Structure
```

docs/technical/backend/
├── DATABASE-DESIGN.md
├── database/
│ ├── 01-AUTH-SCHEMA.md
│ ├── 02-BUSINESS-SCHEMA.md
│ └── ...
└── features/
└── FEAT-001-AUTH-MODULE.md

```

```

## Update Actions

| Action         | Index Change                          |
| :------------- | :------------------------------------ |
| File created   | Add row to table                      |
| File deleted   | Remove row                            |
| File renamed   | Update link                           |
| Status changed | Update status column                  |
| Moved          | Update path, possibly different index |

## Workflow

1. **Detect change** - What file changed?
2. **Find parent index** - Which README.md?
3. **Read frontmatter** - Extract metadata
4. **Update table** - Add/remove/modify row
5. **Regenerate tree** - If structure changed
6. **Save index** - Write changes

## GLOSSARY.md Sync

When new terms are introduced:

1. Check if term exists in GLOSSARY.md
2. If not, add to appropriate section
3. Maintain alphabetical order

## Cross-Reference Validation

After index update:

- [ ] All links resolve
- [ ] No orphan files (not in any index)
- [ ] Status badges accurate
- [ ] Types match actual document_type

## Reference

- [DOCUMENTATION-WORKFLOW.md](/docs/process/standards/DOCUMENTATION-WORKFLOW.md)
- [GLOSSARY.md](/docs/GLOSSARY.md)
