---
name: paddle-ocr-validation  
description: "PaddleOCR-based receipt and BIR form extraction with validation"
---

# PaddleOCR Validation
Extract and validate data from receipts, invoices, and BIR forms.

## What This Does
- Receipt OCR (BIR format)
- Invoice data extraction
- Form validation
- Confidence scoring
- Field-level verification

## Quick Example
```python
receipt = paddle_ocr.extract_bir_form(
    image_path='receipt.jpg',
    fields=['merchant', 'tin', 'total', 'vat', 'or_number']
)
```

## Getting Started  
"Scan this restaurant receipt"
"Validate BIR form 1601-C"
