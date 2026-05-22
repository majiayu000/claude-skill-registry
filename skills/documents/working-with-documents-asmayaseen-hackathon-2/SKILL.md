---
name: working-with-documents
description: |
  Creates and edits Office documents: Word (.docx), PDF, and PowerPoint (.pptx).
  Use when working with document creation, PDF manipulation, presentation generation,
  tracked changes, or converting between formats.
---

# Working with Documents

## Quick Reference

| Format | Read | Create | Edit |
|--------|------|--------|------|
| DOCX | pandoc, python-docx | docx-js | OOXML (unpack/edit/pack) |
| PDF | pdfplumber, pypdf | reportlab | pypdf (merge/split) |
| PPTX | markitdown | html2pptx | OOXML (unpack/edit/pack) |

## Word Documents (.docx)

### Reading Content

```bash
# Convert to markdown (preserves structure)
pandoc document.docx -o output.md

# With tracked changes visible
pandoc --track-changes=all document.docx -o output.md
```

### Creating New Documents

Use **docx-js** (JavaScript):

```javascript
const { Document, Packer, Paragraph, TextRun } = require('docx');

const doc = new Document({
  sections: [{
    children: [
      new Paragraph({
        children: [
          new TextRun({ text: "Hello World", bold: true }),
        ],
      }),
    ],
  }],
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("output.docx", buffer);
});
```

### Editing Existing Documents (Tracked Changes)

```bash
# 1. Unpack
python ooxml/scripts/unpack.py document.docx unpacked/

# 2. Edit XML files in unpacked/word/document.xml
# Key files:
#   - word/document.xml (main content)
#   - word/comments.xml (comments)
#   - word/media/ (images)

# 3. Pack
python ooxml/scripts/pack.py unpacked/ edited.docx
```

**Tracked changes XML pattern:**
```xml
<!-- Deletion -->
<w:del><w:r><w:delText>old text</w:delText></w:r></w:del>

<!-- Insertion -->
<w:ins><w:r><w:t>new text</w:t></w:r></w:ins>
```

## PDF Documents

### Reading PDFs

```python
import pdfplumber

# Extract text
with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        print(page.extract_text())

# Extract tables
with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                print(row)
```

### Creating PDFs

```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("output.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = [
    Paragraph("Report Title", styles['Title']),
    Paragraph("Body text goes here.", styles['Normal']),
]
doc.build(story)
```

### Merging/Splitting PDFs

```python
from pypdf import PdfReader, PdfWriter

# Merge
writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)
writer.write(open("merged.pdf", "wb"))

# Split
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    writer.write(open(f"page_{i+1}.pdf", "wb"))
```

### Command-Line Tools

```bash
# Extract text
pdftotext input.pdf output.txt
pdftotext -layout input.pdf output.txt  # Preserve layout

# Merge with qpdf
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split pages
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
```

## PowerPoint Presentations (.pptx)

### Reading Content

```bash
# Convert to markdown
python -m markitdown presentation.pptx
```

### Creating New Presentations

Use **html2pptx** workflow:

1. Create HTML slides (720pt × 405pt for 16:9)
2. Convert with html2pptx.js library
3. Validate with thumbnail grid

```bash
# Create thumbnails for validation
python scripts/thumbnail.py output.pptx --cols 4
```

### Editing Existing Presentations

```bash
# 1. Unpack
python ooxml/scripts/unpack.py presentation.pptx unpacked/

# Key files:
#   - ppt/slides/slide1.xml, slide2.xml, etc.
#   - ppt/notesSlides/ (speaker notes)
#   - ppt/media/ (images)

# 2. Edit XML

# 3. Validate
python ooxml/scripts/validate.py unpacked/ --original presentation.pptx

# 4. Pack
python ooxml/scripts/pack.py unpacked/ edited.pptx
```

### Rearranging Slides

```bash
# Duplicate, reorder, delete slides
python scripts/rearrange.py template.pptx output.pptx 0,3,3,5,7
# Creates: slide 0, slide 3 (twice), slide 5, slide 7
```

## Converting Between Formats

```bash
# DOCX/PPTX to PDF
soffice --headless --convert-to pdf document.docx

# PDF to images
pdftoppm -jpeg -r 150 document.pdf page
# Creates: page-1.jpg, page-2.jpg, etc.

# DOCX to Markdown
pandoc document.docx -o output.md
```

## OCR for Scanned Documents

```python
import pytesseract
from pdf2image import convert_from_path

images = convert_from_path('scanned.pdf')
text = ""
for image in images:
    text += pytesseract.image_to_string(image)
```

## Design Guidelines (Presentations)

### Color Palettes

Pick 3-5 colors that work together:

| Palette | Colors |
|---------|--------|
| Classic Blue | Navy #1C2833, Slate #2E4053, Silver #AAB7B8 |
| Teal & Coral | Teal #5EA8A7, Coral #FE4447, White #FFFFFF |
| Black & Gold | Gold #BF9A4A, Black #000000, Cream #F4F6F6 |

### Web-Safe Fonts Only

Arial, Helvetica, Times New Roman, Georgia, Verdana, Tahoma, Trebuchet MS, Courier New, Impact

### Layout Rules

- Two-column: Use for exactly 2 distinct items
- Three-column: Use for exactly 3 items
- Never vertically stack charts below text
- Full-bleed images with text overlays work well

## Dependencies

```bash
# Python
pip install pypdf pdfplumber reportlab python-docx openpyxl

# System tools
apt-get install pandoc poppler-utils libreoffice

# Node.js (for docx-js)
npm install docx
```

## Verification

Run: `python scripts/verify.py`

## Related Skills

- `working-with-spreadsheets` - Excel file handling
- `building-nextjs-apps` - Frontend for document uploads