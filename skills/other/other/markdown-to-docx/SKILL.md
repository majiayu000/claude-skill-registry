---
name: markdown-to-docx
version: 1.0.0
description: '[Document Processing] Convert markdown files to Microsoft Word (.docx) format with GFM support and math rendering'

allowed-tools: NONE
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Convert Markdown files to Microsoft Word (.docx) format with GFM support and proper formatting.

**Workflow:**
1. **Install** -- Ensure pandoc is available (required dependency)
2. **Convert** -- Run pandoc with docx output, apply reference template if provided
3. **Verify** -- Check output file for formatting fidelity

**Key Rules:**
- Requires pandoc installed on the system
- Supports GFM tables, code blocks, and images
- Optional reference.docx template for custom styling

# markdown-to-docx

Convert markdown files to editable Microsoft Word documents with support for tables, code blocks, images, and LaTeX math equations.

## Installation Required

**This skill requires npm dependencies.** Run one of:

```bash
# Option 1: ClaudeKit CLI (recommended)
ck init

# Option 2: Manual
cd .claude/skills/markdown-to-docx
npm install
```

**Dependencies:** `markdown-docx`, `gray-matter`

## Quick Start

```bash
# Basic conversion
node .claude/skills/markdown-to-docx/scripts/convert.cjs --input ./README.md

# Specify output path
node .claude/skills/markdown-to-docx/scripts/convert.cjs -i ./doc.md -o ./output.docx

# With custom theme
node .claude/skills/markdown-to-docx/scripts/convert.cjs -i ./doc.md --theme ./theme.json
```

## CLI Options

| Option     | Short | Description         | Default        |
| ---------- | ----- | ------------------- | -------------- |
| `--input`  | `-i`  | Input markdown file | (required)     |
| `--output` | `-o`  | Output DOCX path    | `{input}.docx` |
| `--theme`  | `-t`  | Custom theme JSON   | built-in       |
| `--title`  |       | Document title      | filename       |
| `--help`   | `-h`  | Show help           |                |

## Features

- **GFM Support:** Tables, strikethrough, task lists
- **Code Blocks:** Syntax preserved with monospace font
- **Images:** Local and URL images embedded
- **Math:** LaTeX equations rendered by default (`$...$`, `$$...$$`)
- **Frontmatter:** YAML metadata extracted for title
- **No System Dependencies:** Pure JavaScript, no Chrome needed

## Output

Returns JSON on success:

```json
{
    "success": true,
    "input": "/path/to/input.md",
    "output": "/path/to/output.docx"
}
```

## Compatibility

Generated DOCX files work with:

- Microsoft Word (2007+)
- Google Docs (upload to Drive)
- LibreOffice Writer
- Apple Pages

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
