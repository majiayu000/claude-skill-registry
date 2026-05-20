---
name: pdf-manipulation
description: Manipulate PDF files including merge, split, extract, redact, convert, and secure workflows.
---

# PDF Manipulation Skill

Merge, split, extract, redact, and transform PDF files using free command-line tools and libraries. Covers common PDF operations for document automation workflows.

## When to use
- Merge multiple PDFs into one document
- Split large PDFs into separate files or page ranges
- Extract text, images, or specific pages
- Redact sensitive information
- Add watermarks, passwords, or metadata
- Convert PDFs to images or other formats

## Required tools
- **pdftk** — Swiss Army knife for PDF manipulation (merge, split, rotate, encrypt)
- **qpdf** — PDF transformation and encryption (linearize, decrypt, repair)
- **pdftotext / pdfimages** — Part of poppler-utils (extract text and images)
- **ghostscript (gs)** — Advanced PDF processing, compression, and conversion

### Installation
```bash
# Ubuntu/Debian
sudo apt-get install pdftk qpdf poppler-utils ghostscript

# macOS (Homebrew)
brew install pdftk-java qpdf poppler ghostscript

# For Node.js: npm i pdf-lib (pure JS, no system deps)
# For Python: pip install PyPDF2 pypdf
```

## Skills

### Merge PDFs
```bash
# Using pdftk (preserves bookmarks, forms)
pdftk file1.pdf file2.pdf file3.pdf cat output merged.pdf

# Using ghostscript (better compression)
gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=merged.pdf file1.pdf file2.pdf file3.pdf

# Using qpdf (preserves structure)
qpdf --empty --pages file1.pdf file2.pdf file3.pdf -- merged.pdf
```

**Node.js (pdf-lib):**
```javascript
const { PDFDocument } = require('pdf-lib');
const fs = require('fs');

async function mergePDFs(files, output) {
  const mergedPdf = await PDFDocument.create();
  
  for (const file of files) {
    const pdfBytes = fs.readFileSync(file);
    const pdf = await PDFDocument.load(pdfBytes);
    const pages = await mergedPdf.copyPages(pdf, pdf.getPageIndices());
    pages.forEach(page => mergedPdf.addPage(page));
  }
  
  const mergedBytes = await mergedPdf.save();
  fs.writeFileSync(output, mergedBytes);
}

// mergePDFs(['file1.pdf', 'file2.pdf'], 'merged.pdf');
```

### Split PDF (by page or range)
```bash
# Split every page into separate files
pdftk input.pdf burst output page_%02d.pdf

# Extract specific pages (e.g., pages 1-5 and 10)
pdftk input.pdf cat 1-5 10 output subset.pdf

# Extract page ranges with qpdf
qpdf input.pdf --pages . 1-5 -- output.pdf

# Split every N pages (e.g., every 2 pages)
pdftk input.pdf burst
# then manually combine or script it
```

**Node.js (pdf-lib):**
```javascript
const { PDFDocument } = require('pdf-lib');
const fs = require('fs');

async function extractPages(inputPath, pages, outputPath) {
  const pdfBytes = fs.readFileSync(inputPath);
  const pdfDoc = await PDFDocument.load(pdfBytes);
  const newPdf = await PDFDocument.create();
  
  for (const pageNum of pages) {
    const [page] = await newPdf.copyPages(pdfDoc, [pageNum - 1]);
    newPdf.addPage(page);
  }
  
  const newBytes = await newPdf.save();
  fs.writeFileSync(outputPath, newBytes);
}

// extractPages('input.pdf', [1, 3, 5], 'output.pdf');
```

### Extract text
```bash
# Extract all text (preserves layout)
pdftotext input.pdf output.txt

# Extract text as raw (no layout)
pdftotext -raw input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt

# Using qpdf + pdftotext
pdftotext -layout input.pdf -
```

**Node.js (pdf-parse):**
```javascript
const fs = require('fs');
const pdf = require('pdf-parse');

async function extractText(filePath) {
  const dataBuffer = fs.readFileSync(filePath);
  const data = await pdf(dataBuffer);
  return data.text;
}

// extractText('input.pdf').then(console.log);
```

### Extract images
```bash
# Extract all images from PDF
pdfimages -all input.pdf output_prefix

# Output: output_prefix-000.png, output_prefix-001.jpg, etc.

# Extract only JPEGs
pdfimages -j input.pdf output_prefix
```

### Redact / Remove pages
```bash
# Remove specific pages (e.g., remove pages 2-4)
pdftk input.pdf cat 1 5-end output redacted.pdf

# Keep only specific pages
pdftk input.pdf cat 1-10 20-30 output selected.pdf
```

### Add password protection
```bash
# Encrypt PDF with password
pdftk input.pdf output secured.pdf user_pw mypassword

# Remove password
pdftk secured.pdf input_pw mypassword output unlocked.pdf

# Using qpdf (AES-256)
qpdf --encrypt userpass ownerpass 256 -- input.pdf output.pdf
```

**Node.js (pdf-lib):**
```javascript
const { PDFDocument } = require('pdf-lib');
const fs = require('fs');

async function encryptPDF(inputPath, password, outputPath) {
  const pdfBytes = fs.readFileSync(inputPath);
  const pdfDoc = await PDFDocument.load(pdfBytes);
  
  const encryptedBytes = await pdfDoc.save({
    userPassword: password,
    ownerPassword: password
  });
  
  fs.writeFileSync(outputPath, encryptedBytes);
}
```

### Rotate pages
```bash
# Rotate all pages 90 degrees clockwise
pdftk input.pdf cat 1-endright output rotated.pdf

# Rotate specific pages
pdftk input.pdf cat 1-5 6right 7-end output rotated.pdf

# Options: right (90°), left (270°), down (180°)
```

### Compress / Reduce file size
```bash
# Using ghostscript (adjust quality)
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
   -dNOPAUSE -dQUIET -dBATCH -sOutputFile=compressed.pdf input.pdf

# Quality settings:
#   /screen   - low quality (72 dpi)
#   /ebook    - medium (150 dpi)
#   /printer  - high (300 dpi)
#   /prepress - highest (300 dpi, preserves color)

# Using qpdf (lossless compression)
qpdf --linearize --object-streams=generate input.pdf compressed.pdf
```

### Convert PDF to images
```bash
# Convert each page to PNG (300 DPI)
pdftoppm -png -r 300 input.pdf output_prefix

# Output: output_prefix-1.png, output_prefix-2.png, etc.

# Convert to JPEG
pdftoppm -jpeg -r 150 input.pdf output_prefix

# Using ImageMagick (alternative)
convert -density 300 input.pdf output_%03d.png
```

### Add watermark
```bash
# Overlay watermark.pdf on every page
pdftk input.pdf stamp watermark.pdf output watermarked.pdf

# Background watermark (behind content)
pdftk input.pdf background watermark.pdf output watermarked.pdf

# Watermark specific pages only
pdftk input.pdf multistamp watermark.pdf output watermarked.pdf
```

### Get PDF metadata
```bash
# Using pdftk
pdftk input.pdf dump_data

# Using qpdf
qpdf --show-object=1 input.pdf

# Using pdfinfo (poppler-utils)
pdfinfo input.pdf
```

### Multi-operation script (Node.js)
```javascript
const { PDFDocument } = require('pdf-lib');
const fs = require('fs');

class PDFHelper {
  static async merge(files, output) {
    const merged = await PDFDocument.create();
    for (const file of files) {
      const pdf = await PDFDocument.load(fs.readFileSync(file));
      const pages = await merged.copyPages(pdf, pdf.getPageIndices());
      pages.forEach(p => merged.addPage(p));
    }
    fs.writeFileSync(output, await merged.save());
  }

  static async split(input, ranges, output) {
    const pdf = await PDFDocument.load(fs.readFileSync(input));
    const newPdf = await PDFDocument.create();
    const pages = await newPdf.copyPages(pdf, ranges);
    pages.forEach(p => newPdf.addPage(p));
    fs.writeFileSync(output, await newPdf.save());
  }

  static async info(input) {
    const pdf = await PDFDocument.load(fs.readFileSync(input));
    return {
      pages: pdf.getPageCount(),
      title: pdf.getTitle(),
      author: pdf.getAuthor(),
      creator: pdf.getCreator()
    };
  }
}

module.exports = PDFHelper;
```

## Agent prompt
```text
You have PDF manipulation skills. When a user requests PDF operations:

1. Detect the operation: merge, split, extract (text/images/pages), redact, compress, encrypt, rotate, watermark, or get info.
2. Use appropriate tools:
   - pdftk for merge, split, rotate, encrypt, watermark
   - pdftotext/pdfimages for extraction
   - ghostscript for compression
   - qpdf for repair and advanced operations
3. Always validate input files exist before processing.
4. For scripting, prefer pdf-lib (Node.js) or PyPDF2 (Python) for portability.
5. Return structured output (file paths, metadata, text) in JSON format.
```

## Best practices
- **Validate PDFs** before processing (use `qpdf --check input.pdf`).
- **Preserve metadata** when possible (use pdftk or pdf-lib, avoid ghostscript for simple operations).
- **Use appropriate compression** — ghostscript `/ebook` is a good balance for most cases.
- **Security** — Always remove passwords before processing if user provides them; never log passwords.
- **Large files** — For 100+ page PDFs, process in chunks or use streaming APIs.

## Common workflows

### Invoice processing
```bash
# 1. Extract text for parsing
pdftotext invoice.pdf invoice.txt

# 2. Extract first page only (summary)
pdftk invoice.pdf cat 1 output summary.pdf

# 3. Compress for archival
gs -sDEVICE=pdfwrite -dPDFSETTINGS=/ebook -dBATCH -dNOPAUSE -q \
   -sOutputFile=invoice_compressed.pdf invoice.pdf
```

### Batch processing
```bash
# Merge all PDFs in a directory
pdftk *.pdf cat output combined.pdf

# Split each PDF in directory into individual pages
for f in *.pdf; do
  pdftk "$f" burst output "${f%.pdf}_page_%02d.pdf"
done

# Extract text from all PDFs
for f in *.pdf; do
  pdftotext "$f" "${f%.pdf}.txt"
done
```

## Troubleshooting
- **Corrupted PDF**: Use `qpdf --check` then `qpdf input.pdf --replace-input` to repair.
- **Encrypted PDF**: Remove password first with `qpdf --decrypt --password=PASS input.pdf output.pdf`.
- **Large file size**: Use ghostscript compression or remove embedded fonts/images if not needed.
- **Missing fonts**: Install `fonts-liberation` or `msttcorefonts` packages.

## See also
- [anonymous-file-upload.md](anonymous-file-upload.md) — Upload processed PDFs anonymously.
- [using-web-scraping.md](using-web-scraping.md) — Scrape web pages and convert to PDF.
