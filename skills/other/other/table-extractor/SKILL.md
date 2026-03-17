---
name: table-extractor
description: Extract tables from PDFs and images to CSV or Excel. Support for scanned documents with OCR, multi-page PDFs, and complex table structures.
---

# Table Extractor

Extract tables from PDFs and images into structured data formats.

## Features

- **PDF Tables**: Extract tables from digital PDFs
- **Image Tables**: OCR-based extraction from images
- **Multiple Tables**: Extract all tables from document
- **Format Export**: CSV, Excel, JSON output
- **Table Detection**: Auto-detect table boundaries
- **Column Alignment**: Smart column detection
- **Multi-Page**: Process entire PDF documents

## Quick Start

```python
from table_extractor import TableExtractor

extractor = TableExtractor()

# Extract from PDF
extractor.load_pdf("document.pdf")
tables = extractor.extract_all()

# Save first table to CSV
tables[0].to_csv("table.csv")

# Extract from image
extractor.load_image("scanned_table.png")
table = extractor.extract_table()
print(table)
```

## CLI Usage

```bash
# Extract from PDF
python table_extractor.py --input document.pdf --output tables/

# Extract specific pages
python table_extractor.py --input document.pdf --pages 1-3 --output tables/

# Extract from image
python table_extractor.py --input scan.png --output table.csv

# Export to Excel
python table_extractor.py --input document.pdf --format xlsx --output tables.xlsx

# With OCR for scanned PDFs
python table_extractor.py --input scanned.pdf --ocr --output tables/
```

## API Reference

### TableExtractor Class

```python
class TableExtractor:
    def __init__(self)

    # Loading
    def load_pdf(self, filepath: str, pages: List[int] = None) -> 'TableExtractor'
    def load_image(self, filepath: str) -> 'TableExtractor'

    # Extraction
    def extract_table(self, page: int = 0) -> pd.DataFrame
    def extract_all(self) -> List[pd.DataFrame]
    def extract_page(self, page: int) -> List[pd.DataFrame]

    # Detection
    def detect_tables(self, page: int = 0) -> List[Dict]
    def get_table_count(self) -> int

    # Configuration
    def set_ocr(self, enabled: bool = True, lang: str = "eng") -> 'TableExtractor'
    def set_column_detection(self, mode: str = "auto") -> 'TableExtractor'

    # Export
    def to_csv(self, tables: List, output_dir: str) -> List[str]
    def to_excel(self, tables: List, output: str) -> str
    def to_json(self, tables: List, output: str) -> str
```

## Supported Formats

### Input
- PDF documents (text-based and scanned)
- Images: PNG, JPEG, TIFF, BMP
- Screenshots with tables

### Output
- CSV (one file per table)
- Excel (multiple sheets)
- JSON (array of tables)
- Pandas DataFrame

## Table Detection

```python
# Detect tables without extracting
tables_info = extractor.detect_tables(page=0)
# Returns:
# [
#     {"index": 0, "rows": 10, "cols": 5, "bbox": (x1, y1, x2, y2)},
#     {"index": 1, "rows": 8, "cols": 3, "bbox": (x1, y1, x2, y2)}
# ]
```

## Example Workflows

### PDF Report Tables
```python
extractor = TableExtractor()
extractor.load_pdf("quarterly_report.pdf")

# Extract all tables
tables = extractor.extract_all()

# Export each to CSV
for i, table in enumerate(tables):
    table.to_csv(f"table_{i}.csv", index=False)
```

### Scanned Document
```python
extractor = TableExtractor()
extractor.set_ocr(enabled=True, lang="eng")
extractor.load_image("scanned_form.png")

table = extractor.extract_table()
print(table)
```

## Dependencies

- pdfplumber>=0.10.0
- pillow>=10.0.0
- pandas>=2.0.0
- pytesseract>=0.3.10 (for OCR)
- opencv-python>=4.8.0
