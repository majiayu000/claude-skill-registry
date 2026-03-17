---
name: md-table-formatter
description: Automatically formats Markdown tables with proper column alignment after file edits. Use when working with Markdown files containing tables.
---

# Markdown Table Formatter

Automatically formats Markdown tables with proper column alignment.

## Features

- **Auto-formatting** - Tables are formatted after Write/Edit operations on .md files
- **Alignment support** - Left (`:---`), center (`:---:`), and right (`---:`)
- **Unicode aware** - Handles emoji and CJK characters correctly
- **Code preservation** - Preserves markdown inside inline code blocks

## How It Works

The PostToolUse hook triggers after file edits:
1. Detects if the file is Markdown (.md, .mdx)
2. Parses all tables in the file
3. Calculates column widths (accounting for hidden markdown symbols)
4. Pads cells for alignment
5. Writes formatted content back

## Table Syntax

```markdown
| Left | Center | Right |
|:-----|:------:|------:|
| A    |   B    |     C |
```

## Requirements

For best results with CJK/emoji characters:
```bash
pip install wcwidth
```
