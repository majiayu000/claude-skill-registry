---
name: pdf
description: "Comprehensive PDF manipulation, extraction, and generation with support for text extraction, form filling, merging, splitting, annotations, and creation. Use when working with .pdf files for: (1) Extracting text and tables, (2) Filling PDF forms, (3) Merging/splitting PDFs, (4) Creating PDFs programmatically, (5) Adding watermarks/annotations, (6) PDF metadata management"
---

# PDF Manipulation Skill

Comprehensive guide for working with PDF files in Python, covering extraction, manipulation, creation, and advanced operations using progressive disclosure for efficiency.

## Core Capabilities

Extract and manipulate PDF content:
- Extract text with layout preservation
- Extract tables and parse structured data
- Fill PDF forms programmatically
- Merge multiple PDFs into a single document
- Split PDFs by pages or ranges
- Create PDFs from scratch with text, images, and graphics
- Add watermarks and annotations
- Extract and modify metadata (author, title, keywords)
- Add password protection and encryption
- Perform OCR on scanned documents
- Convert images to PDF
- Compress and optimize PDF files
- Extract images from PDFs
- Rotate and reorder pages

## Quick Start

Install required libraries:

```bash
pip install pypdf pdfplumber reportlab PyMuPDF pdf2image pytesseract pillow
```

For detailed installation instructions including system dependencies, see:
- [Library Installation Guide](./references/library-installation.md)

## Python Libraries Overview

**pypdf**: Basic operations (merge, split, rotate, metadata)
**pdfplumber**: Advanced text/table extraction with layout awareness
**reportlab**: Create PDFs from scratch (reports, invoices, documents)
**PyMuPDF (fitz)**: Advanced manipulation, annotations, compression
**pdf2image**: Convert PDF pages to images (requires poppler)
**pytesseract**: OCR for scanned documents (requires tesseract)

## Text Extraction Workflow

### Basic Extraction

```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
for page in reader.pages:
    text = page.extract_text()
    print(text)
```

### Layout-Aware Extraction

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        words = page.extract_words()  # With positioning
        print(text)
```

### Extract from Specific Region

```python
with pdfplumber.open("document.pdf") as pdf:
    page = pdf.pages[0]
    bbox = (0, 0, 612, 100)  # x0, y0, x1, y1
    header = page.crop(bbox).extract_text()
```

For detailed text extraction methods including OCR fallback and encoding handling, see:
- [Text Extraction Reference](./references/text-extraction.md)

## Table Extraction Workflow

### Extract All Tables

```python
import pdfplumber

with pdfplumber.open("report.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            print(table)
```

### Advanced Table Detection

```python
table_settings = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "snap_tolerance": 3
}

tables = page.extract_tables(table_settings=table_settings)
```

For detailed table extraction strategies and data cleaning, see:
- [Table Extraction Reference](./references/table-extraction.md)

## PDF Form Operations

### Fill Form Fields

```python
import fitz

doc = fitz.open("form.pdf")
for page in doc:
    for widget in page.widgets():
        if widget.field_name == "name":
            widget.field_value = "John Doe"
            widget.update()
doc.save("filled.pdf")
doc.close()
```

### Extract Form Field Names

```python
doc = fitz.open("form.pdf")
for page in doc:
    for widget in page.widgets():
        print(f"{widget.field_name}: {widget.field_type_string}")
doc.close()
```

For form filling, flattening, and debugging, see:
- [PDF Operations Reference](./references/pdf-operations.md)

## Merging and Splitting

### Merge PDFs

```python
from pypdf import PdfMerger

merger = PdfMerger()
for pdf in ["file1.pdf", "file2.pdf", "file3.pdf"]:
    merger.append(pdf)
merger.write("merged.pdf")
merger.close()
```

### Merge with Page Ranges

```python
merger = PdfMerger()
merger.append("doc1.pdf", pages=(0, 3))  # First 3 pages
merger.append("doc2.pdf")  # All pages
merger.write("compiled.pdf")
merger.close()
```

### Split into Individual Pages

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("document.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", 'wb') as f:
        writer.write(f)
```

For merging with bookmarks and splitting by size, see:
- [PDF Operations Reference](./references/pdf-operations.md)

## Creating PDFs

### Simple Text PDF

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

c = canvas.Canvas("output.pdf", pagesize=letter)
c.setFont("Helvetica", 12)
c.drawString(50, 750, "Hello, World!")
c.save()
```

### Styled Report

```python
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf")
styles = getSampleStyleSheet()
story = []

story.append(Paragraph("Report Title", styles['Title']))
story.append(Spacer(1, 12))
story.append(Paragraph("Content here", styles['BodyText']))

doc.build(story)
```

### PDF with Table

```python
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

data = [
    ['Product', 'Quantity', 'Price'],
    ['Widget A', '10', '$50'],
    ['Widget B', '5', '$75']
]

table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
```

For complete PDF creation workflows including images, multi-column layouts, and custom fonts, see:
- [PDF Creation Reference](./references/pdf-creation.md)

For practical examples:
- [Invoice Generator](./examples/invoice-generator.md)
- [Report Automation](./examples/report-automation.md)

## Metadata and Security

### Extract Metadata

```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
metadata = reader.metadata
print(f"Title: {metadata.get('/Title')}")
print(f"Author: {metadata.get('/Author')}")
```

### Modify Metadata

```python
from pypdf import PdfWriter

writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)

writer.add_metadata({
    '/Title': 'New Title',
    '/Author': 'John Doe'
})

with open("updated.pdf", 'wb') as f:
    writer.write(f)
```

### Add Password Protection

```python
writer.encrypt(
    user_password="user123",
    owner_password="owner456",
    algorithm="AES-256"
)
```

For detailed security operations and comprehensive metadata management, see:
- [Metadata, Security, and OCR Reference](./references/metadata-security-ocr.md)

## OCR for Scanned Documents

### Basic OCR

```python
from pdf2image import convert_from_path
import pytesseract

images = convert_from_path("scanned.pdf")
for i, image in enumerate(images):
    text = pytesseract.image_to_string(image)
    print(f"Page {i+1}:\n{text}")
```

### Multi-Language OCR

```python
text = pytesseract.image_to_string(image, lang='eng+fra+deu')
```

For searchable PDF creation and OCR preprocessing, see:
- [Metadata, Security, and OCR Reference](./references/metadata-security-ocr.md)

## Watermarks and Annotations

### Add Text Watermark

```python
import fitz

doc = fitz.open("document.pdf")
for page in doc:
    page.insert_textbox(
        page.rect,
        "CONFIDENTIAL",
        fontsize=50,
        rotate=45,
        opacity=0.3,
        color=(0.7, 0.7, 0.7)
    )
doc.save("watermarked.pdf")
doc.close()
```

### Add Annotations

```python
page.add_highlight_annot(rect)  # Highlight
page.add_text_annot(point, "Note")  # Text note
page.add_underline_annot(rect)  # Underline
```

For stamps and image watermarks, see:
- [Metadata, Security, and OCR Reference](./references/metadata-security-ocr.md)

## Page Operations

### Rotate Pages

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.rotate(90)
    writer.add_page(page)

with open("rotated.pdf", 'wb') as f:
    writer.write(f)
```

### Extract Images

```python
import fitz

doc = fitz.open("document.pdf")
for page_num in range(len(doc)):
    page = doc[page_num]
    for img_index, img in enumerate(page.get_images()):
        xref = img[0]
        base_image = doc.extract_image(xref)
        with open(f"image_{page_num}_{img_index}.png", "wb") as f:
            f.write(base_image["image"])
doc.close()
```

### Convert Images to PDF

```python
from PIL import Image
from reportlab.pdfgen import canvas

c = canvas.Canvas("output.pdf")
for img_path in ["img1.jpg", "img2.jpg"]:
    img = Image.open(img_path)
    c.setPageSize(img.size)
    c.drawImage(img_path, 0, 0, width=img.width, height=img.height)
    c.showPage()
c.save()
```

For detailed page operations, see:
- [PDF Operations Reference](./references/pdf-operations.md)

## Optimization

### Compress PDF

```python
import fitz

doc = fitz.open("large.pdf")
doc.save(
    "optimized.pdf",
    garbage=4,
    deflate=True,
    clean=True
)
doc.close()
```

## Best Practices

### Memory Management

Process large PDFs in chunks:

```python
from pypdf import PdfReader
import gc

reader = PdfReader("large.pdf")
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    # Process text
    if i % 10 == 0:
        gc.collect()
```

### Error Handling

Always handle encryption and errors:

```python
from pypdf import PdfReader

try:
    reader = PdfReader("document.pdf")

    if reader.is_encrypted:
        reader.decrypt(password)

    for page in reader.pages:
        text = page.extract_text()
except Exception as e:
    print(f"Error: {e}")
```

### OCR Fallback

Detect and handle scanned documents:

```python
import fitz

doc = fitz.open("document.pdf")
text = doc[0].get_text()

if not text.strip():
    # Use OCR for scanned document
    from pdf2image import convert_from_path
    import pytesseract

    images = convert_from_path("document.pdf")
    text = pytesseract.image_to_string(images[0])
```

For comprehensive best practices, common pitfalls, and troubleshooting, see:
- [Best Practices and Common Pitfalls](./references/best-practices.md)

## Common Pitfalls

**Scanned Documents**: Text extraction returns empty for scanned PDFs. Use OCR (pytesseract).

**Table Detection**: Tables not detected correctly. Adjust table_settings strategies.

**Encrypted PDFs**: Operations fail. Check and decrypt with password first.

**Form Fields**: Can't find field names. Use debug helper to list all fields.

**Memory Issues**: Large PDFs cause crashes. Process in chunks with garbage collection.

**Encoding Issues**: Special characters corrupted. Handle with UTF-8 encoding explicitly.

For detailed solutions and debugging strategies, see:
- [Best Practices and Common Pitfalls](./references/best-practices.md)

## Quick Reference

**Text Extraction**:
- Simple: `pypdf` - `page.extract_text()`
- Advanced: `pdfplumber` - `page.extract_text()` + `page.extract_words()`

**Table Extraction**:
- Always use: `pdfplumber` - `page.extract_tables()`

**PDF Creation**:
- Use: `reportlab` - `canvas.Canvas()` or `SimpleDocTemplate()`

**Advanced Operations**:
- Use: `PyMuPDF (fitz)` - forms, annotations, compression

**OCR**:
- Use: `pytesseract` + `pdf2image`

**Merging/Splitting**:
- Use: `pypdf` - `PdfMerger()` and `PdfWriter()`

## Helper Scripts

The skill includes helper scripts for common operations:

```bash
# See scripts directory for utilities
python scripts/pdf_helper.py --help
```

## Additional Resources

**Comprehensive References**:
- [Library Installation](./references/library-installation.md) - Setup and dependencies
- [Text Extraction](./references/text-extraction.md) - All extraction methods
- [Table Extraction](./references/table-extraction.md) - Table detection strategies
- [PDF Operations](./references/pdf-operations.md) - Forms, merge, split, pages
- [PDF Creation](./references/pdf-creation.md) - Creating PDFs from scratch
- [Metadata, Security, OCR](./references/metadata-security-ocr.md) - Advanced operations
- [Best Practices](./references/best-practices.md) - Pitfalls and solutions

**Practical Examples**:
- [Invoice Generator](./examples/invoice-generator.md) - Professional invoice templates
- [Report Automation](./examples/report-automation.md) - Automated report generation

## Implementation Guidelines

When working with PDFs:

1. **Choose the right library** for your task (see Quick Reference)
2. **Handle errors** with try-except blocks
3. **Check for encryption** before processing
4. **Use OCR fallback** for scanned documents
5. **Process large files in chunks** to manage memory
6. **Validate input files** before operations
7. **Close documents** to free resources: `doc.close()`

For production use, always implement proper error handling, validate inputs, and test with various PDF types and versions.
