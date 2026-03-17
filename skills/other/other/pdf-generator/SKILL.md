---
name: pdf-generator
description: 从HTML、Markdown或文本内容生成PDF文档，支持模板、样式和页面配置。
metadata:
  short-description: 从HTML/Markdown生成PDF
source:
  repository: https://github.com/foliojs/pdfkit
  license: MIT
---

# PDF Generator Tool

## Description
Generate PDF documents from HTML, Markdown, or text with customizable styling and layout.

## Trigger
- `/generate-pdf` command
- User requests PDF generation
- User needs to export document as PDF

## Usage

```bash
# Generate PDF from Markdown
python scripts/generate_pdf.py --input "document.md" --output "document.pdf"

# Generate PDF from HTML
python scripts/generate_pdf.py --input "report.html" --output "report.pdf" --format html

# Generate PDF with custom options
python scripts/generate_pdf.py --input "doc.md" --output "doc.pdf" --title "My Report" --author "John" --page-size A4
```

## Tags
`pdf`, `document`, `export`, `markdown`, `html`

## Compatibility
- Codex: ✅
- Claude Code: ✅
