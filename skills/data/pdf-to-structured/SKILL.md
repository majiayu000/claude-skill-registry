---
slug: "pdf-to-structured"
display_name: "PDF To Structured"
description: "Extract structured data from construction PDFs. Convert specifications, BOMs, schedules, and reports from PDF to Excel/CSV/JSON. Use OCR for scanned documents and pdfplumber for native PDFs."
---

# PDF to Structured Data Conversion

## Overview

Based on DDC methodology (Chapter 2.4), this skill transforms unstructured PDF documents into structured formats suitable for analysis and integration. Construction projects generate vast amounts of PDF documentation - specifications, BOMs, schedules, and reports - that need to be extracted and processed.

**Book Reference:** "Преобразование данных в структурированную форму" / "Data Transformation to Structured Form"

> "Преобразование данных из неструктурированной в структурированную форму — это и искусство, и наука. Этот процесс часто занимает значительную часть работы инженера по обработке данных."
> — DDC Book, Chapter 2.4

## ETL Process Overview

The conversion follows the ETL pattern:
1. **Extract**: Load the PDF document
2. **Transform**: Parse and structure the content
3. **Load**: Save to CSV, Excel, or JSON

## Quick Start

```python
import pdfplumber
import pandas as pd

# Extract table from PDF
with pdfplumber.open("construction_spec.pdf") as pdf:
    page = pdf.pages[0]
    table = page.extract_table()
    df = pd.DataFrame(table[1:], columns=table[0])
    df.to_excel("extracted_data.xlsx", index=False)
```

## Installation

```bash
# Core libraries
pip install pdfplumber pandas openpyxl

# For scanned PDFs (OCR)
pip install pytesseract pdf2image
# Also install Tesseract OCR: https://github.com/tesseract-ocr/tesseract

# For advanced PDF operations
pip install pypdf
```

## Native PDF Extraction (pdfplumber)

### Extract All Tables from PDF

```python
import pdfplumber
import pandas as pd

def extract_tables_from_pdf(pdf_path):
    """Extract all tables from a PDF file"""
    all_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table_num, table in enumerate(tables):
                if table and len(table) > 1:
                    # First row as header
                    df = pd.DataFrame(table[1:], columns=table[0])
                    df['_page'] = page_num + 1
                    df['_table'] = table_num + 1
                    all_tables.append(df)

    if all_tables:
        return pd.concat(all_tables, ignore_index=True)
    return pd.DataFrame()

# Usage
df = extract_tables_from_pdf("material_specification.pdf")
df.to_excel("materials.xlsx", index=False)
```

### Extract Text with Layout

```python
import pdfplumber

def extract_text_with_layout(pdf_path):
    """Extract text preserving layout structure"""
    full_text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)

    return "\n\n--- Page Break ---\n\n".join(full_text)

# Usage
text = extract_text_with_layout("project_report.pdf")
with open("report_text.txt", "w", encoding="utf-8") as f:
    f.write(text)
```

### Extract Specific Table by Position

```python
import pdfplumber
import pandas as pd

def extract_table_from_area(pdf_path, page_num, bbox):
    """
    Extract table from specific area on page

    Args:
        pdf_path: Path to PDF file
        page_num: Page number (0-indexed)
        bbox: Bounding box (x0, top, x1, bottom) in points
    """
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        cropped = page.within_bbox(bbox)
        table = cropped.extract_table()

        if table:
            return pd.DataFrame(table[1:], columns=table[0])
    return pd.DataFrame()

# Usage - extract table from specific area
# bbox format: (left, top, right, bottom) in points (1 inch = 72 points)
df = extract_table_from_area("drawing.pdf", 0, (50, 100, 550, 400))
```

## Scanned PDF Processing (OCR)

### Extract Text from Scanned PDF

```python
import pytesseract
from pdf2image import convert_from_path
import pandas as pd

def ocr_scanned_pdf(pdf_path, language='eng'):
    """
    Extract text from scanned PDF using OCR

    Args:
        pdf_path: Path to scanned PDF
        language: Tesseract language code (eng, deu, rus, etc.)
    """
    # Convert PDF pages to images
    images = convert_from_path(pdf_path, dpi=300)

    extracted_text = []
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image, lang=language)
        extracted_text.append({
            'page': i + 1,
            'text': text
        })

    return pd.DataFrame(extracted_text)

# Usage
df = ocr_scanned_pdf("scanned_specification.pdf", language='eng')
df.to_csv("ocr_results.csv", index=False)
```

### OCR Table Extraction

```python
import pytesseract
from pdf2image import convert_from_path
import pandas as pd
import cv2
import numpy as np

def ocr_table_from_scanned_pdf(pdf_path, page_num=0):
    """Extract table from scanned PDF using OCR with table detection"""
    # Convert specific page to image
    images = convert_from_path(pdf_path, first_page=page_num+1,
                                last_page=page_num+1, dpi=300)
    image = np.array(images[0])

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Apply thresholding
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Extract text with table structure
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(gray, config=custom_config)

    # Parse text into table structure
    lines = text.strip().split('\n')
    data = [line.split() for line in lines if line.strip()]

    if data:
        # Assume first row is header
        df = pd.DataFrame(data[1:], columns=data[0] if len(data[0]) > 0 else None)
        return df
    return pd.DataFrame()

# Usage
df = ocr_table_from_scanned_pdf("scanned_bom.pdf")
print(df)
```

## Construction-Specific Extractions

### Bill of Materials (BOM) Extraction

```python
import pdfplumber
import pandas as pd
import re

def extract_bom_from_pdf(pdf_path):
    """Extract Bill of Materials from construction PDF"""
    all_items = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if not table or len(table) < 2:
                    continue

                # Find header row (look for common BOM headers)
                header_keywords = ['item', 'description', 'quantity', 'unit', 'material']
                for i, row in enumerate(table):
                    if row and any(keyword in str(row).lower() for keyword in header_keywords):
                        # Found header, process remaining rows
                        headers = [str(h).strip() for h in row]
                        for data_row in table[i+1:]:
                            if data_row and any(cell for cell in data_row if cell):
                                item = dict(zip(headers, data_row))
                                all_items.append(item)
                        break

    return pd.DataFrame(all_items)

# Usage
bom = extract_bom_from_pdf("project_bom.pdf")
bom.to_excel("bom_extracted.xlsx", index=False)
```

### Project Schedule Extraction

```python
import pdfplumber
import pandas as pd
from datetime import datetime

def extract_schedule_from_pdf(pdf_path):
    """Extract project schedule/gantt data from PDF"""
    with pdfplumber.open(pdf_path) as pdf:
        all_tasks = []

        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if not table:
                    continue

                # Look for schedule-like table
                headers = table[0] if table else []

                # Check if it looks like a schedule
                schedule_keywords = ['task', 'activity', 'start', 'end', 'duration']
                if any(kw in str(headers).lower() for kw in schedule_keywords):
                    for row in table[1:]:
                        if row and any(cell for cell in row if cell):
                            task = dict(zip(headers, row))
                            all_tasks.append(task)

    df = pd.DataFrame(all_tasks)

    # Try to parse dates
    date_columns = ['Start', 'End', 'Start Date', 'End Date', 'Finish']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    return df

# Usage
schedule = extract_schedule_from_pdf("project_schedule.pdf")
print(schedule)
```

### Specification Parsing

```python
import pdfplumber
import pandas as pd
import re

def parse_specification_pdf(pdf_path):
    """Parse construction specification document"""
    specs = []

    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    # Parse sections (common spec format)
    section_pattern = r'(\d+\.\d+(?:\.\d+)?)\s+([A-Z][^\n]+)'
    sections = re.findall(section_pattern, full_text)

    for num, title in sections:
        specs.append({
            'section_number': num,
            'title': title.strip(),
            'level': len(num.split('.'))
        })

    return pd.DataFrame(specs)

# Usage
specs = parse_specification_pdf("technical_spec.pdf")
print(specs)
```

## Batch Processing

### Process Multiple PDFs

```python
import pdfplumber
import pandas as pd
from pathlib import Path

def batch_extract_tables(folder_path, output_folder):
    """Process all PDFs in folder and extract tables"""
    pdf_files = Path(folder_path).glob("*.pdf")
    results = []

    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path.name}")
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    tables = page.extract_tables()
                    for table_num, table in enumerate(tables):
                        if table and len(table) > 1:
                            df = pd.DataFrame(table[1:], columns=table[0])
                            df['_source_file'] = pdf_path.name
                            df['_page'] = page_num + 1

                            # Save individual table
                            output_name = f"{pdf_path.stem}_p{page_num+1}_t{table_num+1}.xlsx"
                            df.to_excel(Path(output_folder) / output_name, index=False)
                            results.append(df)
        except Exception as e:
            print(f"Error processing {pdf_path.name}: {e}")

    # Combined output
    if results:
        combined = pd.concat(results, ignore_index=True)
        combined.to_excel(Path(output_folder) / "all_tables.xlsx", index=False)

    return len(results)

# Usage
count = batch_extract_tables("./pdf_documents/", "./extracted/")
print(f"Extracted {count} tables")
```

## Data Cleaning After Extraction

```python
import pandas as pd

def clean_extracted_data(df):
    """Clean common issues in PDF-extracted data"""
    # Remove completely empty rows
    df = df.dropna(how='all')

    # Strip whitespace from string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()

    # Remove rows where all cells are empty strings
    df = df[df.apply(lambda row: any(cell != '' for cell in row), axis=1)]

    # Convert numeric columns
    for col in df.columns:
        # Try to convert to numeric
        numeric_series = pd.to_numeric(df[col], errors='coerce')
        if numeric_series.notna().sum() > len(df) * 0.5:  # More than 50% numeric
            df[col] = numeric_series

    return df

# Usage
df = extract_tables_from_pdf("document.pdf")
df_clean = clean_extracted_data(df)
df_clean.to_excel("clean_data.xlsx", index=False)
```

## Export Options

```python
import pandas as pd
import json

def export_to_multiple_formats(df, base_name):
    """Export DataFrame to multiple formats"""
    # Excel
    df.to_excel(f"{base_name}.xlsx", index=False)

    # CSV
    df.to_csv(f"{base_name}.csv", index=False, encoding='utf-8-sig')

    # JSON
    df.to_json(f"{base_name}.json", orient='records', indent=2)

    # JSON Lines (for large datasets)
    df.to_json(f"{base_name}.jsonl", orient='records', lines=True)

# Usage
df = extract_tables_from_pdf("document.pdf")
export_to_multiple_formats(df, "extracted_data")
```

## Quick Reference

| Task | Tool | Code |
|------|------|------|
| Extract table | pdfplumber | `page.extract_table()` |
| Extract text | pdfplumber | `page.extract_text()` |
| OCR scanned | pytesseract | `pytesseract.image_to_string(image)` |
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Convert to image | pdf2image | `convert_from_path(pdf)` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Table not detected | Try adjusting table settings: `page.extract_table(table_settings={})` |
| Wrong column alignment | Use visual debugging: `page.to_image().draw_rects()` |
| OCR quality poor | Increase DPI, preprocess image, use correct language |
| Memory issues | Process pages one at a time, close PDF after processing |

## Resources

- **Book**: "Data-Driven Construction" by Artem Boiko, Chapter 2.4
- **Website**: https://datadrivenconstruction.io
- **pdfplumber Docs**: https://github.com/jsvine/pdfplumber
- **Tesseract OCR**: https://github.com/tesseract-ocr/tesseract

## Next Steps

- See `image-to-data` for image processing
- See `cad-to-data` for CAD/BIM data extraction
- See `etl-pipeline` for automated processing workflows
- See `data-quality-check` for validating extracted data
