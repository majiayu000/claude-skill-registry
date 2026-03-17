---
name: document-skills
description: "Professional document creation, editing, and analysis for Office formats (docx, pdf, pptx, xlsx). Use when working with Word documents, PDFs, PowerPoint presentations, or Excel spreadsheets."
tags: [documents, office, docx, pdf, pptx, xlsx, word, excel, powerpoint]
---

# Document Skills Suite

Comprehensive document handling for Microsoft Office formats and PDFs.

## Available Sub-Skills

| Skill  | Format             | Capabilities                                     |
| ------ | ------------------ | ------------------------------------------------ |
| `docx` | Word (.docx)       | Create, edit, analyze, tracked changes, comments |
| `pdf`  | PDF (.pdf)         | Extract text, tables, metadata, merge/split      |
| `pptx` | PowerPoint (.pptx) | Create, edit presentations, layouts, charts      |
| `xlsx` | Excel (.xlsx)      | Spreadsheet manipulation, formulas, charts       |

## When to Use

- Creating professional documents from scratch
- Editing existing Office files
- Extracting content from PDFs
- Working with tracked changes
- Generating reports and presentations
- Data analysis in spreadsheets

## Workflow

1. Identify document type needed
2. Load appropriate sub-skill: `Skill(document-skills/docx)`, etc.
3. Follow sub-skill specific workflow

## Sub-Skill Details

### docx (Word Documents)

- **Create**: Use docx-js (JavaScript/TypeScript)
- **Edit**: Use Document library (Python)
- **Analyze**: Use pandoc for text extraction
- See `document-skills/docx/SKILL.md` for full details

### pdf (PDF Documents)

- Extract text, tables, metadata
- Merge and split documents
- See `document-skills/pdf/SKILL.md` for full details

### pptx (PowerPoint)

- Create and edit presentations
- Work with layouts and charts
- See `document-skills/pptx/SKILL.md` for full details

### xlsx (Excel)

- Spreadsheet manipulation
- Formulas and analysis
- See `document-skills/xlsx/SKILL.md` for full details
