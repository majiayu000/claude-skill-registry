---
name: business-card-scanner
description: Extract contact information from business card images using OCR - name, company, email, phone, address.
---

# Business Card Scanner

Extract contact information from business card images using OCR.

## Features

- **OCR Extraction**: Extract text from card images
- **Contact Parsing**: Name, company, email, phone, address
- **Pattern Recognition**: Smart regex for contact fields
- **Multi-Format**: JPG, PNG support
- **Batch Processing**: Multiple cards
- **Export**: vCard, JSON, CSV output

## CLI Usage

```bash
python business_card_scanner.py --input card.jpg --output contact.json
```

## Dependencies

- pytesseract>=0.3.10
- pillow>=10.0.0
- opencv-python>=4.8.0
- pandas>=2.0.0
