---
name: markdown-to-pdf
version: 1.0.0
description: '[Document Processing] Convert markdown files to PDF with syntax highlighting and custom CSS support. Cross-platform (Windows, macOS, Linux).'

allowed-tools: NONE
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Convert Markdown files to PDF with syntax highlighting and custom CSS support.

**Workflow:**
1. **Install** -- Ensure required tools (pandoc + wkhtmltopdf or weasyprint) are available
2. **Convert** -- Run conversion with syntax highlighting and optional CSS
3. **Verify** -- Check PDF output for formatting and completeness

**Key Rules:**
- Requires pandoc + a PDF engine (wkhtmltopdf or weasyprint)
- Supports syntax highlighting for code blocks
- Custom CSS can be applied for styling

# markdown-to-pdf

Convert markdown files to high-quality PDF documents with code syntax highlighting and custom CSS support.

## Installation Required

**This skill requires npm dependencies.** Run one of the following:

```bash
# Option 1: Install via ClaudeKit CLI (recommended)
ck init  # Runs install.sh which handles all skills

# Option 2: Manual installation
cd .claude/skills/markdown-to-pdf
npm install
```

**Dependencies:** `md-to-pdf`, `gray-matter`

**Note:** First run may download Chromium (~150MB) unless system Chrome is detected.

## Quick Start

```bash
# Basic conversion
node .claude/skills/markdown-to-pdf/scripts/convert.cjs --input ./README.md

# Specify output path
node .claude/skills/markdown-to-pdf/scripts/convert.cjs --input ./doc.md --output ./output.pdf

# With custom CSS
node .claude/skills/markdown-to-pdf/scripts/convert.cjs --input ./doc.md --css ./my-style.css
```

## CLI Options

| Option           | Short | Description                 | Default       |
| ---------------- | ----- | --------------------------- | ------------- |
| `--input`        | `-i`  | Input markdown file path    | (required)    |
| `--output`       | `-o`  | Output PDF file path        | `{input}.pdf` |
| `--css`          | `-c`  | Custom CSS file path        | built-in      |
| `--no-highlight` |       | Disable syntax highlighting | false         |
| `--help`         | `-h`  | Show help message           |               |

## Features

- **Syntax Highlighting:** Code blocks rendered with highlight.js
- **Custom CSS:** Override default styles with your own CSS
- **Cross-Platform:** Works on Windows, macOS, Linux
- **System Chrome:** Uses installed Chrome/Chromium when available
- **Frontmatter Support:** YAML frontmatter extracted for title/metadata

## Default Styling

The default PDF style includes:

- Serif font (Georgia) for body text
- Monospace font (Consolas/Monaco) for code
- Proper page margins (2cm)
- Code block background highlighting
- Table borders and alternating row colors

## Output

Returns JSON on success:

```json
{
    "success": true,
    "input": "/path/to/input.md",
    "output": "/path/to/output.pdf",
    "pages": 3
}
```

## Troubleshooting

**Chrome not found:** The skill will automatically download Chromium. Set `PUPPETEER_SKIP_DOWNLOAD=1` to prevent this.

**Memory issues:** Large documents may require more memory. Consider splitting into multiple files.

**Font issues:** Embed fonts via CSS `@font-face` with base64-encoded fonts for consistent rendering.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
