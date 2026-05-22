---
name: md-tables
description: Fix markdown table alignment and spacing issues. Use when formatting tables in markdown files, aligning columns, normalizing cell padding, or ensuring proper table structure. Triggers: markdown table, md table, table formatting, column alignment, pipe table, GFM table, table generator, align columns, table spacing, table layout, fix table, format table, table structure.
---

# Markdown Table Formatting

Utility for fixing markdown table alignment and spacing. Normalizes column widths, ensures consistent padding, and preserves alignment markers.

## Quick Examples

```bash
# Preview fixed output
python fix-md-tables.py document.md

# Fix in-place
python fix-md-tables.py document.md -i
```

### Common Patterns

**Status tables:**
```markdown
| Stage    | Status    | Branch       |
| -------- | --------- | ------------ |
| build    | Complete  | loom/build   |
| test     | Executing | loom/test    |
```

**Configuration tables:**
```markdown
| Option      | Default | Description           |
| ----------- | ------- | --------------------- |
| timeout     | 300     | Session timeout (sec) |
| auto_merge  | false   | Enable auto merging   |
```

**Right-aligned numbers:**
```markdown
| Item  | Count | Total |
| ----- | ----: | ----: |
| Files |    42 |   500 |
| Lines | 1,234 | 5,000 |
```

## Features

- Aligns columns to consistent widths
- Single-space padding for cells
- Preserves alignment markers (`:---`, `:---:`, `---:`)
- Adds blank lines around tables

## Alignment Markers

| Syntax  | Alignment      |
| ------- | -------------- |
| `---`   | Left (default) |
| `:---`  | Left           |
| `---:`  | Right          |
| `:---:` | Center         |
