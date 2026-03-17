---
name: instinct-export
description: Export learned instincts for cross-project sharing
disable-model-invocation: true
---

# Instinct Export

Exports instincts from `.claude/instincts/instincts.jsonl` for sharing across projects.

## Usage

```bash
# Export all instincts with confidence >= 0.5
.claude/hooks/instinct-cli.sh export

# Filter by category
.claude/hooks/instinct-cli.sh export --category debugging --min-confidence 0.3

# Custom output path
.claude/hooks/instinct-cli.sh export --output ~/shared-instincts.jsonl
```

## What Gets Exported

- Pattern description and action
- Category and confidence score
- Occurrence count

## What Gets Stripped (Privacy)

- Source branch names
- Dates (only year-month retained)
- File paths
- Session-specific metadata
- Already-promoted instincts (they're skills now)

## Sharing

Copy the exported file to another project and use `/instinct-import` to merge.
