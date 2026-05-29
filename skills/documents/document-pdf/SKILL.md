---
name: document-pdf
description: Extract text and tables from PDFs, create formatted PDFs, merge/split documents, handle forms and annotations. Supports pdf-lib, pdfkit, PyPDF2, pdfplumber, and ReportLab for comprehensive PDF workflows in Node.js and Python.
---

# Document PDF Skill — Quick Reference

This skill enables PDF creation, extraction, manipulation, and analysis. Claude should apply these patterns when users need to generate invoices, reports, extract data from PDFs, merge documents, or work with PDF forms.

**Modern Best Practices (Dec 2025)**:
- PDF is a release artifact, not the editable source of truth.
- Validate export fidelity (fonts, images, links) and accessibility baseline where applicable.
- Treat PDFs as sensitive: scrub metadata, ensure real redaction, and control distribution.

---

## Quick Reference

| Task | Tool/Library | Language | When to Use |
|------|--------------|----------|-------------|
| Create PDF | pdfkit | Node.js | Reports, invoices, certificates |
| Create PDF | ReportLab | Python | Complex layouts, tables |
| Edit PDF | pdf-lib | Node.js | Modify existing PDFs, add pages |
| Extract text | pdfplumber | Python | OCR-free text extraction |
| Extract tables | pdfplumber/camelot | Python | Structured data extraction |
| Parse PDF | pypdf | Python | Merge, split, rotate pages |
| Fill forms | pdf-lib | Node.js | Form automation |
| HTML to PDF | puppeteer | Node.js | Web page snapshots |

## When to Use This Skill

Claude should invoke this skill when a user requests:

- Generate PDFs from data (invoices, reports, certificates)
- Extract text or tables from existing PDFs
- Merge multiple PDFs into one document
- Split PDFs into separate files
- Fill PDF forms programmatically
- Add watermarks, headers, footers
- Convert HTML/web pages to PDF

---

## Core Operations

### Create PDF (Node.js - pdfkit)

```typescript
import PDFDocument from 'pdfkit';
import fs from 'fs';

const doc = new PDFDocument();
doc.pipe(fs.createWriteStream('output.pdf'));

// Title
doc.fontSize(25).text('Invoice', { align: 'center' });
doc.moveDown();

// Content
doc.fontSize(12).text('Bill To: Acme Corp');
doc.text('Date: 2025-01-15');
doc.moveDown();

// Table-like structure
doc.text('Item                  Qty    Price');
doc.text('Widget A               10    $100');
doc.text('Widget B                5    $250');
doc.moveDown();
doc.text('Total: $350', { align: 'right' });

// Image
doc.image('logo.png', { width: 100 });

doc.end();
```

### Create PDF (Python - ReportLab)

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# Simple canvas approach
c = canvas.Canvas('output.pdf', pagesize=letter)
c.setFont('Helvetica-Bold', 24)
c.drawString(100, 750, 'Invoice')
c.setFont('Helvetica', 12)
c.drawString(100, 700, 'Bill To: Acme Corp')
c.save()

# Table with platypus
doc = SimpleDocTemplate('table.pdf', pagesize=letter)
data = [
    ['Item', 'Qty', 'Price'],
    ['Widget A', '10', '$100'],
    ['Widget B', '5', '$250'],
]
table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))
doc.build([table])
```

### Extract Text (Python - pdfplumber)

```python
import pdfplumber

with pdfplumber.open('document.pdf') as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)

        # Extract tables
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                print(row)
```

### Modify PDF (Node.js - pdf-lib)

```typescript
import { PDFDocument, rgb, StandardFonts } from 'pdf-lib';
import fs from 'fs';

// Load existing PDF
const existingPdfBytes = fs.readFileSync('input.pdf');
const pdfDoc = await PDFDocument.load(existingPdfBytes);

// Add watermark to all pages
const helveticaFont = await pdfDoc.embedFont(StandardFonts.Helvetica);
const pages = pdfDoc.getPages();

for (const page of pages) {
  const { width, height } = page.getSize();
  page.drawText('CONFIDENTIAL', {
    x: width / 2 - 50,
    y: height / 2,
    size: 50,
    font: helveticaFont,
    color: rgb(0.9, 0.9, 0.9),
    rotate: { angle: 45, type: 'degrees' },
  });
}

// Save
const pdfBytes = await pdfDoc.save();
fs.writeFileSync('output.pdf', pdfBytes);
```

### Merge PDFs (Python - pypdf)

```python
from pypdf import PdfMerger

merger = PdfMerger()
merger.append('doc1.pdf')
merger.append('doc2.pdf')
merger.append('doc3.pdf', pages=(0, 5))  # First 5 pages only
merger.write('merged.pdf')
merger.close()
```

### HTML to PDF (Node.js - Puppeteer)

```typescript
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch();
const page = await browser.newPage();

// From URL
await page.goto('https://example.com');
await page.pdf({ path: 'page.pdf', format: 'A4' });

// From HTML string
await page.setContent('<h1>Hello World</h1><p>Generated PDF</p>');
await page.pdf({
  path: 'generated.pdf',
  format: 'A4',
  printBackground: true,
  margin: { top: '1in', bottom: '1in' }
});

await browser.close();
```

---

## PDF Structure Patterns

### Invoice Template

```text
INVOICE STRUCTURE
├── Header (logo, company info, invoice #)
├── Bill To / Ship To blocks
├── Line items table
│   ├── Description | Qty | Unit Price | Total
│   └── Subtotal, Tax, Total
├── Payment terms
└── Footer (contact, thank you)
```

### Report Template

```text
REPORT PDF STRUCTURE
├── Cover page (title, author, date)
├── Table of contents
├── Body sections with page numbers
├── Charts/images with captions
├── Appendices
└── Running header/footer
```

---

## Decision Tree

```text
PDF Task: [What do you need?]
    ├─ Create new PDF?
    │   ├─ Simple text/tables → pdfkit (Node) or ReportLab (Python)
    │   ├─ Complex layouts → ReportLab with Platypus
    │   └─ From HTML → Puppeteer or wkhtmltopdf
    │
    ├─ Extract from PDF?
    │   ├─ Text only → pdfplumber (Python)
    │   ├─ Tables → pdfplumber or camelot (Python)
    │   └─ Images → PyMuPDF/fitz (Python)
    │
    ├─ Modify existing PDF?
    │   ├─ Add text/images → pdf-lib (Node)
    │   ├─ Merge/split → pypdf or pdf-lib
    │   └─ Fill forms → pdf-lib
    │
    └─ Batch processing?
        └─ pypdf + pdfplumber pipeline
```

---

## Do / Avoid (Dec 2025)

### Do

- Keep a versioned source document (doc/slide/design file) alongside the PDF.
- Verify links and reading order for long documents.
- Use real redaction and test by copy/paste.

### Avoid

- Editing PDFs as the primary workflow when a source doc exists.
- Shipping PDFs with broken links or illegible charts.
- Including customer PII or secrets in PDFs without explicit approval.

## What Good Looks Like

- Fidelity: export is reproducible from a versioned source file (doc/slide/design) and looks identical across viewers.
- Accessibility: tags/reading order are correct; links work; scanned docs are OCRed when appropriate.
- Release hygiene: file naming includes version/date; metadata is clean; no “PDF as source of truth”.
- Security: redaction is verified (copy/paste test) and sensitive data is minimized.
- QA: release checklist completed using `templates/pdf-release-checklist.md`.

## Optional: AI / Automation

Use only when explicitly requested and policy-compliant.

- Generate a release checklist run; humans verify the final PDF manually.

## Navigation

**Resources**
- [resources/pdf-generation-patterns.md](resources/pdf-generation-patterns.md) — Complex layouts, multi-page docs
- [resources/pdf-extraction-patterns.md](resources/pdf-extraction-patterns.md) — Text, table, image extraction
- [data/sources.json](data/sources.json) — Library documentation links

**Templates**
- [templates/invoice-template.md](templates/invoice-template.md) — Invoice PDF generation
- [templates/report-template.md](templates/report-template.md) — Multi-page report structure
- [templates/pdf-release-checklist.md](templates/pdf-release-checklist.md) — Links, accessibility, export fidelity

**Related Skills**
- [../document-docx/SKILL.md](../document-docx/SKILL.md) — Word document generation
- [../document-xlsx/SKILL.md](../document-xlsx/SKILL.md) — Excel/spreadsheet workflows
- [../document-docx/SKILL.md](../document-docx/SKILL.md) — Document workflow automation
