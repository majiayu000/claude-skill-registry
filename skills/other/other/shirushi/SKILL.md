---
name: shirushi
description: Document ID management for Git repositories. Validates, assigns, and tracks immutable doc_ids across Markdown/YAML files. Use when working with doc_id, document IDs, "@see docid" references, document integrity validation, or shirushi commands.
---

# Shirushi - Document ID Manager

Shirushi ensures consistent, immutable document IDs across Git repositories with CI integration.

## Commands

| Command | Purpose |
|---------|---------|
| `shirushi lint` | Validate doc_ids and index integrity |
| `shirushi scan` | List documents with metadata |
| `shirushi show <id>` | Get document info by doc_id |
| `shirushi assign` | Assign IDs to new documents |
| `shirushi rehash` | Recalculate content hashes |

## Common Workflows

### Validate before commit
```bash
shirushi lint --base HEAD~1
```

### Find document by ID
```bash
shirushi show PCE-SPEC-2025-0001-G
```

### Add doc_id to new document
```bash
shirushi assign docs/new-spec.md
```

### List all documents
```bash
shirushi scan --format table
```

### Check for changes in PR
```bash
shirushi lint --base origin/main --check-references
```

## Configuration

Configuration is defined in `.shirushi.yml`:

```yaml
id_format: "{COMP}-{KIND}-{YEAR4}-{SER4}-{CHK1}"
dimensions:
  COMP:
    type: enum
    values: ["API", "UI", "DB"]
  KIND:
    type: enum_from_doc_type
    mapping:
      spec: SPEC
      adr: ADR
  YEAR4:
    type: year
    digits: 4
  SER4:
    type: serial
    digits: 4
    scope: ["COMP", "KIND", "YEAR4"]
  CHK1:
    type: checksum
    algorithm: mod26AZ
    digits: 1
```

## Document Format

Documents use YAML frontmatter:

```markdown
---
doc_id: API-SPEC-2025-0001-G
title: API Specification
doc_type: spec
---

# Content here...
```

## @see docid References

Reference documents in code comments:

```typescript
// @see API-SPEC-2025-0001-G
function handleRequest() { ... }
```

Shirushi tracks these references and warns when referenced documents change.
