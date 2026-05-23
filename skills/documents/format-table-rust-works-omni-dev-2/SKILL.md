---
name: format-table
description: Formats markdown tables with fixed-width columns for consistent alignment. Use when creating tables, reformatting existing tables, or ensuring table readability. Triggers on terms like "format table", "align table", "fix table", "table columns".
---

# Markdown Table Formatting Skill

This skill formats markdown tables with fixed-width columns for consistent alignment and readability.

## Table Format Rules

### Column Width Calculation

1. Find the maximum content width in each column (including header)
2. Add padding (minimum 1 space on each side)
3. Apply consistent width to all cells in that column

### Alignment

- **Left-aligned** (default): `| content |` with space padding on right
- **Right-aligned**: `:---` becomes `---:` in separator
- **Center-aligned**: `:---:` in separator

### Separator Row

The separator row uses dashes matching the column width:
- Left-aligned: `|----------|`
- Right-aligned: `|---------:|`
- Center-aligned: `|:--------:|`

## Example Transformation

### Before (inconsistent widths)

```markdown
| Option | Description | Example |
|--------|-------------|---------|
| `--use-context` | Enable contextual intelligence | `--use-context` |
| `--batch-size N` | Set batch size for large ranges | `--batch-size 3` |
| `--auto-apply` | Apply without confirmation | `--auto-apply` |
```

### After (fixed-width columns)

```markdown
| Option           | Description                     | Example          |
|------------------|---------------------------------|------------------|
| `--use-context`  | Enable contextual intelligence  | `--use-context`  |
| `--batch-size N` | Set batch size for large ranges | `--batch-size 3` |
| `--auto-apply`   | Apply without confirmation      | `--auto-apply`   |
```

## Formatting Algorithm

```
For each column:
  1. width = max(len(cell) for cell in column)
  2. width = max(width, 3)  # Minimum 3 chars for separator

For each row:
  1. For each cell:
     - Pad content to column width
     - Add single space before and after content
  2. Join cells with '|' delimiter
  3. Add '|' at start and end
```

## Special Cases

### Code in Cells

Preserve backticks when calculating width:
- `` `--flag` `` counts as 8 characters (including backticks)

### Empty Cells

Empty cells get full padding:
```markdown
| Column A | Column B |
|----------|----------|
| value    |          |
```

### Multi-word Headers

Headers determine minimum column width:
```markdown
| Long Header Name | Short |
|------------------|-------|
| value            | x     |
```

## Instructions

When formatting tables:

1. **Read the table** - Identify all rows and columns
2. **Calculate widths** - Find max content width per column
3. **Format header** - Apply consistent width with padding
4. **Format separator** - Match column widths with dashes
5. **Format data rows** - Apply same widths to all cells
6. **Preserve alignment** - Keep `:` markers for right/center alignment

## Quick Reference

| Element       | Format                          |
|---------------|---------------------------------|
| Cell padding  | Single space each side          |
| Min width     | 3 characters (for `---`)        |
| Separator     | Dashes matching column width    |
| Pipe spacing  | No space adjacent to pipes      |
| Line ending   | No trailing whitespace          |
