---
name: ocr-document-processor
description: Extract text from images and scanned PDFs using OCR. Supports 100+ languages, table detection, structured output (markdown/JSON), and batch processing.
---

# OCR Document Processor

Extract text from images, scanned PDFs, and photographs using Optical Character Recognition (OCR). Supports multiple languages, structured output formats, and intelligent document parsing.

## Core Capabilities

- **Image OCR**: Extract text from PNG, JPEG, TIFF, BMP images
- **PDF OCR**: Process scanned PDFs page by page
- **Multi-language**: Support for 100+ languages
- **Structured Output**: Plain text, Markdown, JSON, or HTML
- **Table Detection**: Extract tabular data to CSV/JSON
- **Batch Processing**: Process multiple documents at once
- **Quality Assessment**: Confidence scoring for OCR results

## Quick Start

```python
from scripts.ocr_processor import OCRProcessor

# Simple text extraction
processor = OCRProcessor("document.png")
text = processor.extract_text()
print(text)

# Extract to structured format
result = processor.extract_structured()
print(result['text'])
print(result['confidence'])
print(result['blocks'])  # Text blocks with positions
```

## Core Workflow

### 1. Basic Text Extraction

```python
from scripts.ocr_processor import OCRProcessor

# From image
processor = OCRProcessor("scan.png")
text = processor.extract_text()

# From PDF
processor = OCRProcessor("scanned.pdf")
text = processor.extract_text()  # All pages

# Specific pages
text = processor.extract_text(pages=[1, 2, 3])
```

### 2. Structured Extraction

```python
# Get detailed results
result = processor.extract_structured()

# Result contains:
# - text: Full extracted text
# - blocks: Text blocks with bounding boxes
# - lines: Individual lines
# - words: Individual words with confidence
# - confidence: Overall confidence score
# - language: Detected language
```

### 3. Export Formats

```python
# Export to Markdown
processor.export_markdown("output.md")

# Export to JSON
processor.export_json("output.json")

# Export to searchable PDF
processor.export_searchable_pdf("searchable.pdf")

# Export to HTML
processor.export_html("output.html")
```

## Language Support

```python
# Specify language for better accuracy
processor = OCRProcessor("german_doc.png", lang='deu')

# Multiple languages
processor = OCRProcessor("mixed_doc.png", lang='eng+fra+deu')

# Auto-detect language
processor = OCRProcessor("document.png", lang='auto')
```

### Supported Languages (Common)

| Code | Language | Code | Language |
|------|----------|------|----------|
| eng | English | fra | French |
| deu | German | spa | Spanish |
| ita | Italian | por | Portuguese |
| rus | Russian | chi_sim | Chinese (Simplified) |
| chi_tra | Chinese (Traditional) | jpn | Japanese |
| kor | Korean | ara | Arabic |
| hin | Hindi | nld | Dutch |

## Image Preprocessing

Preprocessing improves OCR accuracy on low-quality images.

```python
# Enable preprocessing
processor = OCRProcessor("noisy_scan.png")
processor.preprocess(
    deskew=True,        # Fix rotation
    denoise=True,       # Remove noise
    threshold=True,     # Binarize image
    contrast=1.5        # Enhance contrast
)
text = processor.extract_text()
```

### Available Preprocessing Options

| Option | Description | Default |
|--------|-------------|---------|
| `deskew` | Correct skewed/rotated images | False |
| `denoise` | Remove noise and artifacts | False |
| `threshold` | Convert to black/white | False |
| `threshold_method` | 'otsu', 'adaptive', 'simple' | 'otsu' |
| `contrast` | Contrast factor (1.0 = no change) | 1.0 |
| `sharpen` | Sharpen factor (0 = none) | 0 |
| `scale` | Upscale factor for small text | 1.0 |
| `remove_shadows` | Remove shadow artifacts | False |

## Table Extraction

```python
# Extract tables from document
tables = processor.extract_tables()

# Each table is a list of rows
for table in tables:
    for row in table:
        print(row)

# Export tables to CSV
processor.export_tables_csv("tables/")

# Export to JSON
processor.export_tables_json("tables.json")
```

## PDF Processing

### Multi-Page PDFs

```python
# Process all pages
processor = OCRProcessor("document.pdf")
full_text = processor.extract_text()

# Process specific pages
page_3 = processor.extract_text(pages=[3])

# Get per-page results
results = processor.extract_by_page()
for page_num, text in results.items():
    print(f"Page {page_num}: {len(text)} characters")
```

### Create Searchable PDF

```python
# Convert scanned PDF to searchable PDF
processor = OCRProcessor("scanned.pdf")
processor.export_searchable_pdf("searchable.pdf")
```

## Batch Processing

```python
from scripts.ocr_processor import batch_ocr

# Process directory of images
results = batch_ocr(
    input_dir="scans/",
    output_dir="extracted/",
    output_format="markdown",
    lang="eng",
    recursive=True
)

print(f"Processed: {results['success']} files")
print(f"Failed: {results['failed']} files")
```

## Receipt/Document Parsing

### Receipt Extraction

```python
# Parse receipt structure
processor = OCRProcessor("receipt.jpg")
receipt_data = processor.parse_receipt()

# Returns structured data:
# - vendor: Store name
# - date: Transaction date
# - items: List of items with prices
# - subtotal: Subtotal amount
# - tax: Tax amount
# - total: Total amount
```

### Business Card Parsing

```python
# Extract business card info
processor = OCRProcessor("card.jpg")
contact = processor.parse_business_card()

# Returns:
# - name: Person's name
# - title: Job title
# - company: Company name
# - email: Email addresses
# - phone: Phone numbers
# - address: Physical address
# - website: Website URLs
```

## Configuration

```python
processor = OCRProcessor("document.png")

# Configure OCR settings
processor.config.update({
    'psm': 3,           # Page segmentation mode
    'oem': 3,           # OCR engine mode
    'dpi': 300,         # DPI for processing
    'timeout': 30,      # Timeout in seconds
    'min_confidence': 60,  # Minimum word confidence
})
```

### Page Segmentation Modes (PSM)

| Mode | Description |
|------|-------------|
| 0 | Orientation and script detection only |
| 1 | Automatic page segmentation with OSD |
| 3 | Fully automatic page segmentation (default) |
| 4 | Assume single column of text |
| 6 | Assume single uniform block of text |
| 7 | Treat image as single text line |
| 8 | Treat image as single word |
| 11 | Sparse text. Find as much text as possible |
| 12 | Sparse text with OSD |

## Quality Assessment

```python
# Get confidence scores
result = processor.extract_structured()

# Overall confidence (0-100)
print(f"Confidence: {result['confidence']}%")

# Per-word confidence
for word in result['words']:
    print(f"{word['text']}: {word['confidence']}%")

# Filter low-confidence words
high_conf_words = [w for w in result['words'] if w['confidence'] > 80]
```

## Output Formats

### Markdown Export

```python
processor.export_markdown("output.md")
```

Output includes:
- Document title (if detected)
- Structured headings
- Paragraphs
- Tables (as Markdown tables)
- Page breaks for multi-page docs

### JSON Export

```python
processor.export_json("output.json")
```

Output structure:
```json
{
  "source": "document.pdf",
  "pages": 5,
  "language": "eng",
  "confidence": 92.5,
  "text": "Full extracted text...",
  "blocks": [
    {
      "type": "paragraph",
      "text": "Block text...",
      "bbox": [x, y, width, height],
      "confidence": 95.2
    }
  ],
  "tables": [...]
}
```

### HTML Export

```python
processor.export_html("output.html")
```

Creates styled HTML with:
- Preserved layout approximation
- Highlighted low-confidence regions
- Embedded images (optional)
- Print-friendly styling

## CLI Usage

```bash
# Basic extraction
python ocr_processor.py image.png -o output.txt

# Extract to markdown
python ocr_processor.py document.pdf -o output.md --format markdown

# Specify language
python ocr_processor.py german.png --lang deu

# Batch processing
python ocr_processor.py scans/ -o extracted/ --batch

# With preprocessing
python ocr_processor.py noisy.png --preprocess --deskew --denoise
```

## Error Handling

```python
from scripts.ocr_processor import OCRProcessor, OCRError

try:
    processor = OCRProcessor("document.png")
    text = processor.extract_text()
except OCRError as e:
    print(f"OCR failed: {e}")
except FileNotFoundError:
    print("File not found")
```

## Performance Tips

1. **Image Quality**: Higher resolution (300+ DPI) improves accuracy
2. **Preprocessing**: Use for low-quality scans
3. **Language**: Specifying language improves speed and accuracy
4. **PSM Mode**: Choose appropriate mode for document type
5. **Large Files**: Process PDFs page by page for memory efficiency

## Limitations

- Handwritten text: Limited accuracy
- Complex layouts: May lose structure
- Very low quality: Preprocessing helps but has limits
- Non-Latin scripts: Require specific language packs

## Dependencies

```
pytesseract>=0.3.10
Pillow>=10.0.0
PyMuPDF>=1.23.0
opencv-python>=4.8.0
numpy>=1.24.0
```

## System Requirements

- Tesseract OCR engine must be installed
- Language data files for non-English languages
