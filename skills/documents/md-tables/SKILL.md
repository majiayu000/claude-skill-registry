---
name: md-tables
description: 'Fix markdown table alignment and spacing issues. Use when formatting
  tables in markdown files, aligning columns, normalizing cell padding, or ensuring
  proper table structure. Triggers: markdown table,'
---

---
name: md-tables
description: Fix markdown table alignment and spacing issues. Use when formatting tables in markdown files, aligning columns, normalizing cell padding, or ensuring proper table structure. Triggers: markdown table, table alignment, table formatting, md table, align columns.
---

# Markdown Table Formatting

## Overview

This skill provides a Python script (`fix-md-tables.py`) to fix markdown table alignment and spacing issues. It normalizes column widths, ensures consistent cell padding, and handles separator row alignment markers.

## Features

- Aligns columns to consistent widths
- Normalizes cell spacing with single-space padding
- Preserves alignment markers (`:---`, `:---:`, `---:`)
- Handles tables with varying column counts
- Adds blank lines around tables when needed

## Usage

Run the script located in this skill's directory:

```bash
# Preview fixed output
python fix-md-tables.py document.md

# Fix tables in-place
python fix-md-tables.py document.md --in-place
python fix-md-tables.py document.md -i
```

## Example

### Before

```markdown
|Name|Age|City|
|---|---|---|
|Alice|30|New York|
|Bob|25|Los Angeles|
```

### After

```markdown
| Name  | Age | City        |
| ----- | --- | ----------- |
| Alice | 30  | New York    |
| Bob   | 25  | Los Angeles |
```

## Alignment Markers

The script preserves alignment markers in separator rows:

| Syntax  | Alignment      |
| ------- | -------------- |
| `---`   | Left (default) |
| `:---`  | Left           |
| `---:`  | Right          |
| `:---:` | Center         |
