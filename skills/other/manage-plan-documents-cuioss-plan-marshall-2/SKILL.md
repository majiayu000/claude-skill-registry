---
name: manage-plan-documents
description: Manage request documents within plan directories with schema validation and template-based creation
user-invocable: false
allowed-tools: Read, Glob, Bash
---

# Manage Plan Documents Skill

Domain-specific document management for request documents. Provides logical document names, schema validation, and structured read/update operations.

## What This Skill Provides

- Logical document names (abstract from physical filenames)
- Declarative document type definitions
- Template-based document creation
- Section-based reading and updates
- TOON output format

## When to Activate This Skill

Activate this skill when:
- Creating request documents (via template)
- Reading request documents with structured output
- Updating specific sections of request documents

**For solution outlines**, use the `pm-workflow:manage-solution-outline` skill instead.

---

## Document Types

| Type | File | Purpose |
|------|------|---------|
| `request` | `request.md` | Original user input (source of truth) |

---

## API: Noun-Verb Pattern

```
manage-plan-documents {document-type} {verb} [options]
```

### Verbs

| Verb | Description |
|------|-------------|
| `create` | Create document from template |
| `read` | Read document (parsed or raw) |
| `update` | Update specific section |
| `exists` | Check if document exists |
| `remove` | Delete document |

---

## Operations

Script: `pm-workflow:manage-plan-documents:manage-plan-documents`

### request create

Create a request document.

```bash
python3 .plan/execute-script.py pm-workflow:manage-plan-documents:manage-plan-documents \
  request create \
  --plan-id {plan_id} \
  --title "Feature Title" \
  --source description \
  --body "Full task description..."
```

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--plan-id` | Yes | Plan identifier |
| `--title` | Yes | Document title |
| `--source` | Yes | Source type: `description`, `lesson`, or `issue` |
| `--body` | Yes | Main content |
| `--source-id` | No | Source identifier (lesson ID, issue URL) |
| `--context` | No | Additional context |
| `--force` | No | Overwrite if exists |

**Output:**

```toon
status: success
plan_id: my-feature
document: request
file: request.md
action: created

document_info:
  title: Feature Title
  sections: title,source,source_id,body,context
```

### read

Read a document with parsed sections.

```bash
python3 .plan/execute-script.py pm-workflow:manage-plan-documents:manage-plan-documents \
  request read \
  --plan-id {plan_id}
```

**Output:**

```toon
status: success
plan_id: my-feature
document: request
file: request.md

content:
  _header: # Request: Feature Title...
  original_input: Full task description...
  context: Additional context...
```

**Options:**
- `--raw`: Output raw markdown content
- `--section {section_name}`: Read specific section only (e.g., `clarified_request`)

**Fallback behavior**: When `--section clarified_request` is used but the section doesn't exist, automatically falls back to `original_input`. The response includes both `section` (what was actually returned) and `requested_section` (what was requested). This simplifies callers who want the clarified request if available, otherwise the original input.

**Read specific section:**

```bash
python3 .plan/execute-script.py pm-workflow:manage-plan-documents:manage-plan-documents \
  request read \
  --plan-id {plan_id} \
  --section clarified_request
```

**Output:**

```toon
status: success
plan_id: my-feature
document: request
section: original_input          # actual section returned
requested_section: clarified_request  # what was requested
content: Migrate JSON output specifications to TOON format...
```

### update

Update a specific section.

```bash
python3 .plan/execute-script.py pm-workflow:manage-plan-documents:manage-plan-documents \
  request update \
  --plan-id {plan_id} \
  --section context \
  --content "Updated context information..."
```

**Parameters**:
- `--plan-id` (required): Plan identifier
- `--section` (required): Section name to update (e.g., `context`, `original_input`)
- `--content` (required): New content for the section

**Output:**

```toon
status: success
plan_id: my-feature
document: request
section: context
updated: true
```

### clarify

Add clarifications and clarified request sections to a document. Used in the uncertainty resolution flow.

```bash
python3 .plan/execute-script.py pm-workflow:manage-plan-documents:manage-plan-documents \
  request clarify \
  --plan-id {plan_id} \
  --clarifications "**Q: Should JSON in workflow context be included?**
Examples: manage-adr/SKILL.md, workflow-integration-ci/SKILL.md
A: Exclude workflow JSON - Only include explicit ## Output sections" \
  --clarified-request "Migrate JSON output specifications to TOON format in all marketplace bundles.

**Scope:**
- Components with explicit ## Output sections
- All bundles

**Exclusions:**
- JSON in workflow documentation"
```

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--plan-id` | Yes | Plan identifier |
| `--clarifications` | No | Q&A clarifications content |
| `--clarified-request` | No | Synthesized clarified request |

At least one of `--clarifications` or `--clarified-request` must be provided.

**Output:**

```toon
status: success
plan_id: my-feature
document: request
sections_added:
  - Clarifications
  - Clarified Request
```

**Resulting request.md structure:**

```markdown
# Request: Migrate JSON to TOON

## Original Input

Migrate agent/command/skill outputs from JSON to TOON format

## Context

...

## Clarifications

**Q: Should files with JSON in workflow context be included?**
Examples: manage-adr/SKILL.md, workflow-integration-ci/SKILL.md
A: Exclude workflow JSON - Only include explicit ## Output sections

## Clarified Request

Migrate JSON output specifications to TOON format in all marketplace bundles.

**Scope:**
- Components with explicit `## Output` sections
- All bundles

**Exclusions (based on clarifications):**
- JSON in workflow documentation
```

### exists

Check if document exists.

```bash
python3 .plan/execute-script.py pm-workflow:manage-plan-documents:manage-plan-documents \
  request exists \
  --plan-id {plan_id}
```

**Output:**

```toon
status: success
plan_id: my-feature
document: request
file: request.md
exists: true
```

Returns exit code 0 if exists, 1 if not.

### remove

Remove a document.

```bash
python3 .plan/execute-script.py pm-workflow:manage-plan-documents:manage-plan-documents \
  request remove \
  --plan-id {plan_id}
```

**Output:**

```toon
status: success
plan_id: my-feature
document: request
file: request.md
action: removed
```

### list-types

List available document types.

```bash
python3 .plan/execute-script.py pm-workflow:manage-plan-documents:manage-plan-documents \
  list-types
```

**Output:**

```toon
status: success
types:
  - name: request
    file: request.md
    fields: 5
```

---

## Error Handling

```toon
status: error
plan_id: my-feature
document: request
error: document_not_found
message: Request document does not exist for plan my-feature

suggestions[2]:
- Create the request document first
- Check plan_id spelling
```

---

## Scripts

**Script**: `pm-workflow:manage-plan-documents:manage-plan-documents`

| Command | Parameters | Description |
|---------|------------|-------------|
| `request create` | `--plan-id --title --source --body [--source-id] [--context] [--force]` | Create request document |
| `request read` | `--plan-id [--raw] [--section]` | Read document (parsed, raw, or specific section) |
| `request update` | `--plan-id --section --content` | Update specific section |
| `request clarify` | `--plan-id [--clarifications] [--clarified-request]` | Add clarifications and clarified request |
| `request exists` | `--plan-id` | Check if document exists |
| `request remove` | `--plan-id` | Delete document |
| `list-types` | (none) | List available document types |

---

## Architecture

See [standards/architecture.md](standards/architecture.md) for:
- Declarative engine design
- Document definition schema
- Adding new document types

See [standards/adding-document-types.md](standards/adding-document-types.md) for:
- Step-by-step guide to add new types

## Related Skills

- `pm-workflow:manage-solution-outline` - Solution outline management (validate, read, list-deliverables)

---

## Integration Points

### With plan-init

Plan initialization creates request document:

```bash
python3 .plan/execute-script.py pm-workflow:manage-plan-documents:manage-plan-documents \
  request create \
  --plan-id $PLAN_ID \
  --title "$TITLE" \
  --source description \
  --body "$BODY"
```

### With solution-outline-agent

The thin agent reads the request document:

```bash
python3 .plan/execute-script.py pm-workflow:manage-plan-documents:manage-plan-documents \
  request read \
  --plan-id $PLAN_ID
```

Then write solution outline using `pm-workflow:manage-solution-outline` skill.

### With file_ops

This skill uses `file_ops` utilities (`atomic_write_file`, `base_path`) directly for file I/O. Use manage-files for non-typed documents.
