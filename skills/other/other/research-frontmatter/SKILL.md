---
name: research-frontmatter
description: >
  Enforce standard YAML frontmatter on research documents in docs/research/.
  Use when creating, editing, or promoting research files, when user mentions
  "research metadata", "research frontmatter", or "research staleness".
---

# Research Frontmatter Standard

Ensure all research files in `docs/research/` have standard YAML frontmatter so GitHub renders metadata as a table and readers can judge staleness.

## Required Frontmatter

Every research file MUST have these 5 fields at the top of the YAML block:

```yaml
---
title: "Human-readable title"
version: "1.0.0"
status: Published           # Published | Draft | Living Document
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
---
```

Additional fields (slug, tags, aliases, promoted_at, last_refreshed, sources) MAY follow the standard fields.

## Field Definitions

| Field | Required | Format | Description |
|-------|----------|--------|-------------|
| `title` | Yes | Quoted string | Human-readable document title |
| `version` | Yes | Semver string | Content maturity version |
| `status` | Yes | Enum | `Published`, `Draft`, or `Living Document` |
| `created` | Yes | `YYYY-MM-DD` | Date first authored (from git or inline) |
| `last_updated` | Yes | `YYYY-MM-DD` | Date of last substantive content change |

## When to Increment Version

- **Patch** (1.0.0 -> 1.0.1): Typo fixes, formatting, minor clarifications
- **Minor** (1.0.0 -> 1.1.0): New sections added, examples updated
- **Major** (1.0.0 -> 2.0.0): Complete rewrite, fundamental scope change

## README Index

The `docs/research/README.md` table MUST use these columns:

```markdown
| Topic | Version | Status | Created | Last Updated |
```

When adding a new entry, append a row matching this format.

## Template

New research files should follow `docs/research/TEMPLATE.md`.

## Validation Checklist

When triggered, verify:
1. File has YAML frontmatter (starts with `---`)
2. All 5 required fields are present
3. `status` is one of the 3 allowed values
4. Dates use ISO 8601 format (`YYYY-MM-DD`)
5. Standard fields appear before any extra fields
6. README.md entry exists and columns match
