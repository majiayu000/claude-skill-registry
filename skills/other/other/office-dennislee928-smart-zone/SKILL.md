---
name: office
description: |
  Generate Office documents (DOCX, XLSX, PDF, PPTX) with TypeScript. Pure JS libraries that work everywhere: Claude Code CLI, Cloudflare Workers, browsers. Uses docx (Word), xlsx/SheetJS (Excel), pdf-lib (PDF), pptxgenjs (PowerPoint).

  Use when: creating invoices, reports, spreadsheets, presentations, form filling, exporting data to Office formats, or troubleshooting "Packer.toBuffer", "XLSX.utils", "PDFDocument", "pptxgenjs" errors.
---

# Office Document Generation

**Status**: Production Ready
**Last Updated**: 2026-01-12
**Dependencies**: None (pure JavaScript libraries)
**Latest Versions**: docx@9.5.0, xlsx@0.18.5, pdf-lib@1.17.1, pptxgenjs@4.0.1

---

## Overview

Generate Microsoft Office documents and PDFs programmatically with TypeScript. All libraries are pure JavaScript with zero native dependencies, enabling universal runtime support:

| Format | Library | Workers | Browser | Node.js |
|--------|---------|---------|---------|---------|
| **DOCX** | `docx` | ✅ | ✅ | ✅ |
| **XLSX** | `xlsx` (SheetJS) | ✅ | ✅ | ✅ |
| **PDF** | `pdf-lib` | ✅ | ✅ | ✅ |
| **PPTX** | `pptxgenjs` | ⚠️* | ✅ | ✅ |

*PPTX in Workers: Works for local images/data. Remote image fetching needs workaround (uses `https` module).

---

## Quick Start

### Installation

```bash
# Install all four (or pick what you need)
npm install docx xlsx pdf-lib pptxgenjs
```

### Create a Word Document (30 seconds)

```typescript
import { Document, Packer, Paragraph, TextRun } from 'docx';
import { writeFileSync } from 'fs';

const doc = new Document({
  sections: [{
    children: [
      new Paragraph({
        children: [
          new TextRun({ text: 'Hello World', bold: true, size: 48 }),
        ],
      }),
    ],
  }],
});

// Node.js: Save to file
const buffer = await Packer.toBuffer(doc);
writeFileSync('hello.docx', buffer);

// Browser/Workers: Get as blob
const blob = await Packer.toBlob(doc);
```

### Create an Excel Spreadsheet (30 seconds)

```typescript
import * as XLSX from 'xlsx';

// Create workbook with data
const data = [
  ['Name', 'Amount', 'Date'],
  ['Invoice #1', 1500, '2026-01-12'],
  ['Invoice #2', 2300, '2026-01-13'],
];

const worksheet = XLSX.utils.aoa_to_sheet(data);
const workbook = XLSX.utils.book_new();
XLSX.utils.book_append_sheet(workbook, worksheet, 'Invoices');

// Node.js: Save to file
XLSX.writeFile(workbook, 'invoices.xlsx');

// Browser/Workers: Get as buffer
const buffer = XLSX.write(workbook, { type: 'buffer', bookType: 'xlsx' });
```

### Create a PDF (30 seconds)

```typescript
import { PDFDocument, StandardFonts, rgb } from 'pdf-lib';

const pdfDoc = await PDFDocument.create();
const page = pdfDoc.addPage([612, 792]); // Letter size
const font = await pdfDoc.embedFont(StandardFonts.Helvetica);

page.drawText('Hello World', {
  x: 50,
  y: 700,
  size: 24,
  font,
  color: rgb(0, 0, 0),
});

// Get as bytes (works everywhere)
const pdfBytes = await pdfDoc.save();

// Node.js: Save to file
writeFileSync('hello.pdf', pdfBytes);
```

### Create a PowerPoint (30 seconds)

```typescript
import pptxgen from 'pptxgenjs';

const pptx = new pptxgen();
pptx.author = 'Your Name';
pptx.title = 'Sample Presentation';

// Add a slide
const slide = pptx.addSlide();
slide.addText('Hello World', {
  x: 1, y: 1, w: 8, h: 1.5,
  fontSize: 36, bold: true, color: '363636',
});

// Node.js: Save to file
await pptx.writeFile({ fileName: 'hello.pptx' });

// Browser: Trigger download
await pptx.writeFile({ fileName: 'hello.pptx' });
```

---

## DOCX: Word Documents

### Key Concepts

The `docx` package uses a builder pattern:
- **Document** - The root container
- **Section** - Contains pages (most docs have 1 section)
- **Paragraph** - A line/block of text
- **TextRun** - Formatted text within a paragraph
- **Table** - Grid of TableRow → TableCell → Paragraph

### Document with Headings and Paragraphs

```typescript
import { Document, Packer, Paragraph, TextRun, HeadingLevel } from 'docx';

const doc = new Document({
  sections: [{
    children: [
      new Paragraph({
        text: 'Monthly Report',
        heading: HeadingLevel.HEADING_1,
      }),
      new Paragraph({
        children: [
          new TextRun('This is a '),
          new TextRun({ text: 'bold', bold: true }),
          new TextRun(' and '),
          new TextRun({ text: 'italic', italics: true }),
          new TextRun(' text example.'),
        ],
      }),
    ],
  }],
});
```

### Tables

```typescript
import { Document, Table, TableRow, TableCell, Paragraph, WidthType } from 'docx';

const table = new Table({
  width: { size: 100, type: WidthType.PERCENTAGE },
  rows: [
    new TableRow({
      children: [
        new TableCell({ children: [new Paragraph('Header 1')] }),
        new TableCell({ children: [new Paragraph('Header 2')] }),
      ],
    }),
    new TableRow({
      children: [
        new TableCell({ children: [new Paragraph('Data 1')] }),
        new TableCell({ children: [new Paragraph('Data 2')] }),
      ],
    }),
  ],
});

const doc = new Document({
  sections: [{ children: [table] }],
});
```

### Images

```typescript
import { Document, Paragraph, ImageRun } from 'docx';
import { readFileSync } from 'fs';

const imageBuffer = readFileSync('logo.png');

const doc = new Document({
  sections: [{
    children: [
      new Paragraph({
        children: [
          new ImageRun({
            data: imageBuffer,
            transformation: { width: 200, height: 100 },
            type: 'png',
          }),
        ],
      }),
    ],
  }],
});
```

### Export Patterns

```typescript
// Node.js - Save to file
import { writeFileSync } from 'fs';
const buffer = await Packer.toBuffer(doc);
writeFileSync('document.docx', buffer);

// Browser - Download
const blob = await Packer.toBlob(doc);
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'document.docx';
a.click();

// Cloudflare Workers - Return as Response
const buffer = await Packer.toBuffer(doc);
return new Response(buffer, {
  headers: {
    'Content-Type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'Content-Disposition': 'attachment; filename="document.docx"',
  },
});
```

---

## XLSX: Excel Spreadsheets

### Key Concepts

SheetJS (xlsx) uses utility functions:
- **Workbook** - Container for sheets
- **Worksheet** - Single sheet (grid of cells)
- **utils.aoa_to_sheet** - Array of arrays → worksheet
- **utils.json_to_sheet** - JSON array → worksheet
- **utils.book_new/book_append_sheet** - Create/add sheets

### From Array of Arrays

```typescript
import * as XLSX from 'xlsx';

const data = [
  ['Product', 'Price', 'Quantity', 'Total'],
  ['Widget A', 10, 5, { f: 'B2*C2' }],  // Formula
  ['Widget B', 15, 3, { f: 'B3*C3' }],
  ['', '', 'Grand Total:', { f: 'SUM(D2:D3)' }],
];

const ws = XLSX.utils.aoa_to_sheet(data);
const wb = XLSX.utils.book_new();
XLSX.utils.book_append_sheet(wb, ws, 'Sales');
```

### From JSON

```typescript
const invoices = [
  { id: 1, customer: 'Acme Corp', amount: 1500, date: '2026-01-12' },
  { id: 2, customer: 'Globex', amount: 2300, date: '2026-01-13' },
];

const ws = XLSX.utils.json_to_sheet(invoices);
const wb = XLSX.utils.book_new();
XLSX.utils.book_append_sheet(wb, ws, 'Invoices');
```

### Column Widths

```typescript
// Set column widths (in characters)
ws['!cols'] = [
  { wch: 10 },  // Column A
  { wch: 20 },  // Column B
  { wch: 15 },  // Column C
];
```

### Multiple Sheets

```typescript
const wb = XLSX.utils.book_new();

const summaryData = [['Total Sales', 3800]];
const detailData = [['Item', 'Amount'], ['Item 1', 1500], ['Item 2', 2300]];

XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(summaryData), 'Summary');
XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(detailData), 'Details');
```

### Export Patterns

```typescript
// Node.js - Save to file
XLSX.writeFile(workbook, 'report.xlsx');

// Browser/Workers - Get buffer
const buffer = XLSX.write(workbook, { type: 'buffer', bookType: 'xlsx' });

// Cloudflare Workers - Return as Response
return new Response(buffer, {
  headers: {
    'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'Content-Disposition': 'attachment; filename="report.xlsx"',
  },
});
```

---

## PDF: PDF Documents

### Key Concepts

pdf-lib uses a page-based approach:
- **PDFDocument** - The PDF file
- **PDFPage** - Individual page
- **Coordinates** - Origin at BOTTOM-LEFT (not top-left!)
- **Units** - Points (72 points = 1 inch)

### Standard Page Sizes

```typescript
// Common sizes in points [width, height]
const LETTER = [612, 792];    // 8.5" x 11"
const A4 = [595.28, 841.89];  // 210mm x 297mm
const LEGAL = [612, 1008];    // 8.5" x 14"
```

### Text and Fonts

```typescript
import { PDFDocument, StandardFonts, rgb } from 'pdf-lib';

const pdfDoc = await PDFDocument.create();
const page = pdfDoc.addPage([612, 792]);

// Embed standard fonts
const helvetica = await pdfDoc.embedFont(StandardFonts.Helvetica);
const helveticaBold = await pdfDoc.embedFont(StandardFonts.HelveticaBold);

// Draw text (y=0 is BOTTOM of page)
page.drawText('Invoice #12345', {
  x: 50,
  y: 750,  // Near top of page
  size: 24,
  font: helveticaBold,
  color: rgb(0, 0, 0),
});

page.drawText('Thank you for your business!', {
  x: 50,
  y: 50,  // Near bottom of page
  size: 12,
  font: helvetica,
  color: rgb(0.5, 0.5, 0.5),
});
```

### Drawing Shapes

```typescript
// Rectangle
page.drawRectangle({
  x: 50,
  y: 600,
  width: 200,
  height: 100,
  borderColor: rgb(0, 0, 0),
  borderWidth: 1,
  color: rgb(0.95, 0.95, 0.95),  // Fill color
});

// Line
page.drawLine({
  start: { x: 50, y: 500 },
  end: { x: 550, y: 500 },
  thickness: 1,
  color: rgb(0, 0, 0),
});
```

### Images

```typescript
// From URL/fetch
const imageBytes = await fetch('https://example.com/logo.png').then(r => r.arrayBuffer());
const image = await pdfDoc.embedPng(imageBytes);

// Or embedJpg for JPEG
// const image = await pdfDoc.embedJpg(imageBytes);

page.drawImage(image, {
  x: 50,
  y: 700,
  width: 100,
  height: 50,
});
```

### Fill PDF Forms

```typescript
import { PDFDocument } from 'pdf-lib';

// Load existing PDF with form
const existingPdfBytes = await fetch('form.pdf').then(r => r.arrayBuffer());
const pdfDoc = await PDFDocument.load(existingPdfBytes);

// Get form and fields
const form = pdfDoc.getForm();
const nameField = form.getTextField('customer_name');
const dateField = form.getTextField('date');

// Fill fields
nameField.setText('John Doe');
dateField.setText('2026-01-12');

// Flatten form (make fields non-editable)
form.flatten();

const pdfBytes = await pdfDoc.save();
```

### Merge PDFs

```typescript
import { PDFDocument } from 'pdf-lib';

const pdf1Bytes = await fetch('doc1.pdf').then(r => r.arrayBuffer());
const pdf2Bytes = await fetch('doc2.pdf').then(r => r.arrayBuffer());

const mergedPdf = await PDFDocument.create();
const pdf1 = await PDFDocument.load(pdf1Bytes);
const pdf2 = await PDFDocument.load(pdf2Bytes);

// Copy all pages from both documents
const pages1 = await mergedPdf.copyPages(pdf1, pdf1.getPageIndices());
const pages2 = await mergedPdf.copyPages(pdf2, pdf2.getPageIndices());

pages1.forEach(page => mergedPdf.addPage(page));
pages2.forEach(page => mergedPdf.addPage(page));

const mergedBytes = await mergedPdf.save();
```

---

## PPTX: PowerPoint Presentations

### Key Concepts

pptxgenjs uses a slide-based approach:
- **Presentation** - The PPTX file (new pptxgen())
- **Slide** - Individual slide (addSlide())
- **Elements** - Text, images, shapes, tables, charts
- **Units** - Inches by default (can change to cm/points)

### Basic Presentation

```typescript
import pptxgen from 'pptxgenjs';

const pptx = new pptxgen();
pptx.author = 'Author Name';
pptx.title = 'Presentation Title';
pptx.subject = 'Subject';
pptx.company = 'Company';

// Title slide
const titleSlide = pptx.addSlide();
titleSlide.addText('Quarterly Report', {
  x: 0.5, y: 2, w: 9, h: 1,
  fontSize: 44, bold: true, color: '0066CC', align: 'center',
});
titleSlide.addText('Q1 2026', {
  x: 0.5, y: 3.5, w: 9, h: 0.5,
  fontSize: 24, color: '666666', align: 'center',
});
```

### Slide with Bullet Points

```typescript
const contentSlide = pptx.addSlide();

// Title
contentSlide.addText('Key Highlights', {
  x: 0.5, y: 0.5, w: 9, h: 0.8,
  fontSize: 32, bold: true, color: '333333',
});

// Bullet points
contentSlide.addText([
  { text: 'Revenue up 25% YoY', options: { bullet: true, fontSize: 20 } },
  { text: 'Customer base grew to 10,000', options: { bullet: true, fontSize: 20 } },
  { text: 'New product launch successful', options: { bullet: true, fontSize: 20 } },
  { text: 'Expanded to 5 new markets', options: { bullet: true, fontSize: 20 } },
], { x: 0.5, y: 1.5, w: 8, h: 4, valign: 'top' });
```

### Tables

```typescript
const tableSlide = pptx.addSlide();

tableSlide.addText('Sales Summary', {
  x: 0.5, y: 0.5, w: 9, h: 0.8,
  fontSize: 28, bold: true,
});

const tableData = [
  [{ text: 'Region', options: { bold: true, fill: '0066CC', color: 'FFFFFF' } },
   { text: 'Q1', options: { bold: true, fill: '0066CC', color: 'FFFFFF' } },
   { text: 'Q2', options: { bold: true, fill: '0066CC', color: 'FFFFFF' } }],
  ['North America', '$2.5M', '$2.8M'],
  ['Europe', '$1.8M', '$2.1M'],
  ['Asia Pacific', '$1.2M', '$1.5M'],
];

tableSlide.addTable(tableData, {
  x: 0.5, y: 1.5, w: 9,
  border: { pt: 1, color: 'CCCCCC' },
  fontFace: 'Arial',
  fontSize: 14,
  align: 'center',
  valign: 'middle',
});
```

### Charts

```typescript
const chartSlide = pptx.addSlide();

chartSlide.addText('Revenue Trend', {
  x: 0.5, y: 0.5, w: 9, h: 0.6,
  fontSize: 28, bold: true,
});

chartSlide.addChart(pptx.ChartType.line, [
  { name: 'Revenue', labels: ['Jan', 'Feb', 'Mar', 'Apr'], values: [100, 120, 150, 180] },
  { name: 'Expenses', labels: ['Jan', 'Feb', 'Mar', 'Apr'], values: [80, 85, 90, 95] },
], {
  x: 0.5, y: 1.2, w: 9, h: 4,
  showLegend: true,
  legendPos: 'b',
  showTitle: false,
});
```

### Images

```typescript
import { readFileSync } from 'fs';

const imageSlide = pptx.addSlide();

// From file (Node.js)
imageSlide.addImage({
  path: 'logo.png',
  x: 0.5, y: 0.5, w: 2, h: 1,
});

// From base64
const imageBase64 = readFileSync('chart.png').toString('base64');
imageSlide.addImage({
  data: `image/png;base64,${imageBase64}`,
  x: 0.5, y: 2, w: 4, h: 3,
});

// From URL (Node.js only - uses https module)
imageSlide.addImage({
  path: 'https://example.com/image.png',
  x: 5, y: 2, w: 4, h: 3,
});
```

### Shapes

```typescript
const shapeSlide = pptx.addSlide();

// Rectangle
shapeSlide.addShape(pptx.ShapeType.rect, {
  x: 0.5, y: 0.5, w: 3, h: 2,
  fill: { color: '0066CC' },
  line: { color: '004499', pt: 2 },
});

// Circle/Oval
shapeSlide.addShape(pptx.ShapeType.ellipse, {
  x: 4, y: 0.5, w: 2, h: 2,
  fill: { color: '00AA00' },
});

// Arrow
shapeSlide.addShape(pptx.ShapeType.rightArrow, {
  x: 1, y: 3, w: 3, h: 1,
  fill: { color: 'FF6600' },
});
```

### Slide Layouts and Masters

```typescript
// Define a master slide
pptx.defineSlideMaster({
  title: 'COMPANY_MASTER',
  background: { color: 'FFFFFF' },
  objects: [
    { text: { text: 'Company Name', options: { x: 0.5, y: 0.2, w: 4, h: 0.3, fontSize: 10, color: '999999' } } },
    { line: { x: 0.5, y: 0.6, w: 9, h: 0, line: { color: '0066CC', pt: 2 } } },
  ],
});

// Use the master
const slide = pptx.addSlide({ masterName: 'COMPANY_MASTER' });
```

### Export Patterns

```typescript
// Node.js - Save to file
await pptx.writeFile({ fileName: 'presentation.pptx' });

// Browser - Trigger download
await pptx.writeFile({ fileName: 'presentation.pptx' });

// Get as base64 (for email, API, etc.)
const base64 = await pptx.write({ outputType: 'base64' });

// Get as Blob (browser)
const blob = await pptx.write({ outputType: 'blob' });

// Get as ArrayBuffer
const arrayBuffer = await pptx.write({ outputType: 'arraybuffer' });

// Cloudflare Workers - Return as Response
const arrayBuffer = await pptx.write({ outputType: 'arraybuffer' });
return new Response(arrayBuffer, {
  headers: {
    'Content-Type': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'Content-Disposition': 'attachment; filename="presentation.pptx"',
  },
});
```

---

## Cloudflare Workers Integration

All four libraries work in Cloudflare Workers (PPTX with caveats for remote images).

### DOCX Generation Endpoint

```typescript
import { Hono } from 'hono';
import { Document, Packer, Paragraph, TextRun } from 'docx';

const app = new Hono();

app.get('/api/invoice/:id', async (c) => {
  const invoiceId = c.req.param('id');

  const doc = new Document({
    sections: [{
      children: [
        new Paragraph({
          children: [new TextRun({ text: `Invoice #${invoiceId}`, bold: true, size: 48 })],
        }),
      ],
    }],
  });

  const buffer = await Packer.toBuffer(doc);

  return new Response(buffer, {
    headers: {
      'Content-Type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'Content-Disposition': `attachment; filename="invoice-${invoiceId}.docx"`,
    },
  });
});

export default app;
```

### HTML to PDF with Browser Rendering

For complex layouts with CSS, use Cloudflare Browser Rendering (paid feature):

```typescript
import puppeteer from '@cloudflare/puppeteer';

export default {
  async fetch(request, env) {
    const browser = await puppeteer.launch(env.BROWSER);
    const page = await browser.newPage();

    // Set HTML content
    await page.setContent(`
      <html>
        <head>
          <style>
            body { font-family: Arial, sans-serif; padding: 40px; }
            h1 { color: #333; }
            table { width: 100%; border-collapse: collapse; }
            td, th { border: 1px solid #ddd; padding: 8px; }
          </style>
        </head>
        <body>
          <h1>Invoice #12345</h1>
          <table>
            <tr><th>Item</th><th>Amount</th></tr>
            <tr><td>Service</td><td>$500</td></tr>
          </table>
        </body>
      </html>
    `);

    const pdf = await page.pdf({ format: 'A4' });
    await browser.close();

    return new Response(pdf, {
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'attachment; filename="invoice.pdf"',
      },
    });
  },
};
```

**wrangler.jsonc binding:**
```jsonc
{
  "browser": {
    "binding": "BROWSER"
  }
}
```

---

## Critical Rules

### Always Do

✅ Use `await Packer.toBuffer()` for DOCX (it's async)
✅ Remember PDF coordinates start at BOTTOM-LEFT
✅ Use `type: 'buffer'` for XLSX in Workers/browser
✅ Embed fonts in PDF before using them
✅ Set proper Content-Type headers for downloads
✅ Use `await pptx.writeFile()` or `await pptx.write()` for PPTX
✅ Use base64 images in PPTX for Workers (avoid remote URLs)

### Never Do

❌ Use `Packer.toBuffer()` without await (returns Promise)
❌ Assume PDF y=0 is at top (it's at bottom)
❌ Use `writeFile` in Workers (use Response instead)
❌ Forget to set Content-Disposition for downloads
❌ Use Node.js fs module in browser/Workers
❌ Use PPTX path URLs in Workers (https module not available)

---

## Known Issues Prevention

### Issue #1: DOCX Packer Returns Promise
**Error**: `[object Promise]` in file or empty document
**Why**: `Packer.toBuffer()` is async but called without await
**Prevention**: Always `await Packer.toBuffer(doc)`

### Issue #2: PDF Text at Wrong Position
**Error**: Text appears at bottom of page or off-page
**Why**: PDF coordinates have origin at bottom-left, not top-left
**Prevention**: For text near top, use high y values (e.g., y=750 for letter size)

### Issue #3: XLSX Formula Not Calculating
**Error**: Cell shows formula text instead of result
**Why**: SheetJS doesn't execute formulas, Excel does on open
**Prevention**: This is expected - formulas calculate when opened in Excel

### Issue #4: Workers DOCX/PDF Returns Empty
**Error**: Downloaded file is empty or corrupted
**Why**: Returning wrong type or missing Content-Type header
**Prevention**: Return buffer directly with proper headers

### Issue #5: PPTX Remote Images Fail in Workers
**Error**: `https is not defined` or image not appearing
**Why**: pptxgenjs uses Node.js `https` module for remote images
**Prevention**: Use base64 data URIs or local images in Workers environment

---

## Using Bundled Resources

### Templates (templates/)

- `docx-basic.ts` - Complete Word document with headings, tables, images
- `xlsx-basic.ts` - Excel workbook with formulas and formatting
- `pdf-basic.ts` - PDF with text, images, shapes
- `pptx-basic.ts` - PowerPoint with slides, charts, tables
- `workers-pdf.ts` - Cloudflare Workers PDF generation example

### References (references/)

- `docx-api.md` - Quick reference for docx npm package
- `xlsx-api.md` - Quick reference for SheetJS functions
- `pdf-lib-api.md` - Quick reference for pdf-lib methods
- `pptxgenjs-api.md` - Quick reference for pptxgenjs

### Scripts (scripts/)

- `verify-deps.sh` - Check library versions are current

---

## Limitations vs Anthropic's Official Skills

This skill focuses on **document creation** with portable TypeScript libraries:

| Feature | This Skill | Anthropic's Skills |
|---------|------------|-------------------|
| Create DOCX/XLSX/PDF/PPTX | ✅ | ✅ |
| Works in Cloudflare Workers | ✅ | ❌ |
| Plugin installable | ✅ | ❌ |
| TypeScript-first | ✅ | ❌ (Python) |
| Edit existing DOCX with tracked changes | ❌ | ✅ |
| Excel formula validation | ❌ | ✅ |
| OCR scanned PDFs | ❌ | ✅ |

For advanced editing scenarios (tracked changes, formula validation), consider Anthropic's official skills with Python tooling.

---

## Package Versions (Verified 2026-01-12)

```json
{
  "dependencies": {
    "docx": "^9.5.0",
    "xlsx": "^0.18.5",
    "pdf-lib": "^1.17.1",
    "pptxgenjs": "^4.0.1"
  }
}
```

---

## Official Documentation

- **docx**: https://docx.js.org/
- **SheetJS (xlsx)**: https://docs.sheetjs.com/
- **pdf-lib**: https://pdf-lib.js.org/
- **pptxgenjs**: https://gitbrent.github.io/PptxGenJS/
- **Cloudflare Browser Rendering**: https://developers.cloudflare.com/browser-rendering/

---

## Complete Setup Checklist

- [ ] Installed required packages (`npm install docx xlsx pdf-lib`)
- [ ] Verified import statements match runtime (Node.js vs browser)
- [ ] Used proper export method for target environment
- [ ] Set Content-Type headers for HTTP responses
- [ ] Tested document opens correctly in target application
- [ ] Confirmed Workers compatibility (if deploying to edge)
