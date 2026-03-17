---
name: pdf-skill
description: Expert in generating, parsing, and manipulating PDF documents using tools like PDFKit, PDF.js, and Puppeteer. Use when creating PDFs, extracting content, merging documents, or filling forms. Triggers include "PDF", "generate PDF", "parse PDF", "extract PDF", "merge PDF", "PDF form", "PDFKit".
---

# PDF Skill

## Purpose
Provides expertise in programmatic PDF generation, parsing, and manipulation. Specializes in creating PDFs from scratch, extracting content, merging/splitting documents, and handling forms using PDFKit, PDF.js, Puppeteer, and similar tools.

## When to Use
- Generating PDFs programmatically
- Extracting text or data from PDFs
- Merging or splitting PDF documents
- Filling PDF forms programmatically
- Converting HTML to PDF
- Adding watermarks or annotations
- Parsing PDF structure and metadata
- Building PDF report generators

## Quick Start
**Invoke this skill when:**
- Generating PDFs from code or data
- Extracting content from PDF files
- Merging, splitting, or manipulating PDFs
- Filling or creating PDF forms
- Converting HTML/web pages to PDF

**Do NOT invoke when:**
- Word document creation → use `/docx-skill`
- Excel/spreadsheet work → use `/xlsx-skill`
- PowerPoint creation → use `/pptx-skill`
- General file operations → use Bash or file tools

## Decision Framework
```
PDF Operation?
├── Generate from scratch
│   ├── Simple → PDFKit (Node) / ReportLab (Python)
│   └── Complex layouts → Puppeteer/Playwright + HTML
├── Parse/Extract
│   ├── Text extraction → pdf-parse / PyPDF2
│   └── Table extraction → Camelot / Tabula
├── Manipulate
│   └── pdf-lib (merge, split, edit)
└── Forms
    └── pdf-lib (fill) / PDFtk (advanced)
```

## Core Workflows

### 1. PDF Generation with PDFKit
1. Install PDFKit (`npm install pdfkit`)
2. Create new PDDocument
3. Add content (text, images, graphics)
4. Style with fonts and colors
5. Add pages as needed
6. Pipe to file or response

### 2. HTML to PDF Conversion
1. Set up Puppeteer/Playwright
2. Navigate to HTML content or URL
3. Configure page size and margins
4. Set print options (headers, footers)
5. Generate PDF buffer
6. Save or stream result

### 3. PDF Parsing and Extraction
1. Choose parser (pdf-parse, PyPDF2, pdfplumber)
2. Load PDF file
3. Extract text or structured data
4. Handle multi-page documents
5. Clean and normalize extracted text
6. Output in desired format

## Best Practices
- Use vector graphics over raster when possible
- Embed fonts for consistent rendering
- Test PDF output across different readers
- Handle large PDFs with streaming
- Use appropriate library for task complexity
- Consider accessibility (tagged PDFs)

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Image-only PDFs | Not searchable/accessible | Use text with fonts |
| No font embedding | Rendering issues | Embed required fonts |
| Memory loading large PDFs | Crashes | Stream processing |
| Ignoring encryption | Security/access issues | Handle encrypted PDFs |
| Wrong tool for job | Over-engineering | Match tool to complexity |
