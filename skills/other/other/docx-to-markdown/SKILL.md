---
name: docx-to-markdown
version: 1.0.0
description: '[Document Processing] Convert Microsoft Word (.docx) files to Markdown with GFM support (tables, images, code blocks). Cross-platform.'

allowed-tools: NONE
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Convert Microsoft Word (.docx) files to Markdown with GFM support (tables, images, formatting).

**Workflow:**
1. **Install** -- Ensure pandoc is available (required dependency)
2. **Convert** -- Run pandoc with GFM output format and image extraction
3. **Clean** -- Post-process markdown for consistency

**Key Rules:**
- Requires pandoc installed on the system
- Extracts images to a media/ directory alongside the markdown
- Preserves tables, formatting, and document structure

# docx-to-markdown

Convert Microsoft Word (.docx) files to Markdown format with GitHub-Flavored Markdown support.

## Installation Required

**This skill requires npm dependencies.** Run one of the following:

```bash
# Option 1: Install via ClaudeKit CLI (recommended)
ck init  # Runs install.sh which handles all skills

# Option 2: Manual installation
cd .claude/skills/docx-to-markdown
npm install
```

**Dependencies:** `mammoth`, `turndown`, `turndown-plugin-gfm`

## Quick Start

```bash
# Basic conversion
node .claude/skills/docx-to-markdown/scripts/convert.cjs --input ./document.docx

# Specify output path
node .claude/skills/docx-to-markdown/scripts/convert.cjs -i ./doc.docx -o ./output.md

# Preserve images to folder
node .claude/skills/docx-to-markdown/scripts/convert.cjs -i ./doc.docx --images ./images/
```

## CLI Options

| Option     | Short | Description                    | Default       |
| ---------- | ----- | ------------------------------ | ------------- |
| `--input`  | `-i`  | Input DOCX file path           | (required)    |
| `--output` | `-o`  | Output markdown file path      | `{input}.md`  |
| `--images` |       | Directory for extracted images | inline base64 |
| `--help`   | `-h`  | Show help message              |               |

## Features

- **GFM Tables:** Properly converts Word tables to markdown tables
- **Images:** Extracts embedded images (base64 inline or to folder)
- **Lists:** Ordered and unordered lists preserved
- **Code Blocks:** Monospace text converted to code blocks
- **Links:** Hyperlinks preserved
- **Headings:** Heading levels maintained
- **Cross-Platform:** Works on Windows, macOS, Linux

## Conversion Pipeline

```
DOCX → mammoth → HTML → turndown → Markdown
```

The two-stage conversion (DOCX→HTML→MD) follows mammoth's official recommendation for best results.

## Output

Returns JSON on success:

```json
{
    "success": true,
    "input": "/path/to/input.docx",
    "output": "/path/to/output.md",
    "stats": {
        "images": 3,
        "tables": 2,
        "headings": 5
    }
}
```

## Limitations

- Complex layouts (columns, text boxes) may not preserve structure
- Merged table cells produce basic markdown tables
- Comments and track changes are stripped
- Some formatting (fonts, colors) lost in conversion

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
