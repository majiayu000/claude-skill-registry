---
name: markdown-converter
description: 将Markdown转换为HTML、PDF或其他格式，支持语法高亮和自定义样式。
metadata:
  short-description: 转换Markdown文件
source:
  repository: https://github.com/Python-Markdown/markdown
  license: BSD-3-Clause
---

# Markdown Converter Tool

## Description
Convert Markdown documents to HTML, PDF, and other formats with support for syntax highlighting, tables, and custom CSS.

## Trigger
- `/markdown` command
- User needs to convert Markdown
- User wants to render documentation

## Usage

```bash
# Convert to HTML
python scripts/markdown_converter.py README.md --format html --output README.html

# Convert to HTML with syntax highlighting
python scripts/markdown_converter.py code.md --format html --highlight

# Convert with custom CSS
python scripts/markdown_converter.py doc.md --format html --css style.css

# Convert to PDF (requires weasyprint)
python scripts/markdown_converter.py doc.md --format pdf --output doc.pdf

# Convert multiple files
python scripts/markdown_converter.py *.md --format html --output-dir ./html/
```

## Tags
`markdown`, `html`, `pdf`, `converter`, `documentation`

## Compatibility
- Codex: ✅
- Claude Code: ✅
