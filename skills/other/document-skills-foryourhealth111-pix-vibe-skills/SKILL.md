---
name: document-skills
description: Umbrella skill for document workflows (PDF/DOCX/XLSX/PPTX). Dispatches to the most specific document skill to reduce noise and improve routing precision.
---

# Document Skills (Dispatcher)

Use this skill when the task is clearly “document work” but the exact format is not yet fixed, or when the user mixes multiple formats (e.g., “把论文里的表格做成 Excel，再导出 PDF 报告”).

Goal: **fast dispatch to the most specific skill** so we keep **high hit-rate / low noise**.

## Quick dispatch rules

1) **PDF** (`.pdf`, “PDF”, “pypdf”, “pdfplumber”, “render pages”)
- Prefer the **pdf** skill.
- Typical tasks: extract text/tables, render pages, review layout, generate PDF reports.

2) **Word / DOCX** (`.docx`, “Word”, “tracked changes”, “python-docx”)
- Prefer the **docx** skill (or **doc** when the task is explicitly `.docx` formatting/layout heavy and the doc skill is requested/required by your environment).

3) **Excel / Spreadsheets** (`.xlsx`, `.csv`, `.tsv`, “Excel”, “openpyxl”, “pivot table”)
- Prefer the **xlsx** skill.
- If the task is more “tabular ETL + analysis” than “Excel formatting”, you can use **spreadsheet** instead (but keep output fidelity requirements in mind).

4) **Slides / Posters / PPTX** (`.pptx`, “slides”, “poster”, “deck”, “PowerPoint”)
- Prefer **scientific-slides** for scientific slide decks.
- Prefer **pptx-posters** for posters.
- Use **infographics** / **markdown-mermaid-writing** when the user wants diagrams rather than editable slides.

## Safety / noise controls

- Do **not** guess formats. If the user didn’t specify a target file type, ask: “你最终需要交付的是 PDF / DOCX / XLSX / PPTX 哪一种？”
- If multiple outputs are requested, **sequence** them: source-of-truth document → derived exports (e.g., XLSX → charts → PPTX → PDF).

## Output expectations

- Always preserve formatting when the user provides a template.
- For any generated file, clearly state: **output path(s)** and **how to verify** (open in Office/Preview, check page breaks, confirm no Excel formula errors, etc.).
