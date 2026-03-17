---
name: receipt-scanner
description: Extract vendor, date, items, amounts, and total from receipt images using OCR and pattern matching with structured JSON output.
---

# Receipt Scanner

Extract structured data from receipt images using OCR.

## Features

- **OCR Processing**: Extract text from receipt images
- **Data Extraction**: Vendor, date, items, amounts, total, tax
- **Pattern Matching**: Smart regex patterns for receipts
- **Multi-Format Support**: JPG, PNG, PDF receipts
- **JSON/CSV Export**: Structured data output
- **Batch Processing**: Process multiple receipts

## CLI Usage

```bash
python receipt_scanner.py --input receipt.jpg --output data.json
python receipt_scanner.py --batch receipts/ --output receipts.csv
```

## Dependencies

- pytesseract>=0.3.10
- pillow>=10.0.0
- opencv-python>=4.8.0
- pandas>=2.0.0
