---
name: instinct-import
description: Import instincts from other projects or exports
disable-model-invocation: true
---

# Instinct Import

Import instincts from an export file into the current project.

## Usage

```bash
# Dry run (preview what would be imported)
.claude/hooks/instinct-cli.sh import path/to/instincts-export.jsonl

# Apply changes
.claude/hooks/instinct-cli.sh import path/to/instincts-export.jsonl --apply

# Only import high-confidence patterns
.claude/hooks/instinct-cli.sh import path/to/export.jsonl --apply --min-confidence 0.6
```

## Merge Strategy

- **NEW** instinct (no matching ID): Added with `source: "inherited"` tag
- **DUPLICATE** (matching ID): Higher confidence wins, occurrences are summed
- **SKIP**: Below min-confidence threshold, or missing required fields

## Tags Added on Import

All imported instincts get:
- `source: "inherited"` (vs "session-observation" for local)
- `imported_from: <filename>`
- `imported_at: <ISO timestamp>`

These tags are preserved through confidence decay and promotion.
