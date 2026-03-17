---
name: qr-barcode-reader
description: Use when asked to scan, decode, read, or extract data from QR codes or barcodes in images.
---

# QR/Barcode Reader

Decode and extract data from QR codes and barcodes in images with support for multiple barcode formats.

## Purpose

Barcode scanning for:
- Inventory management and tracking
- Product information lookup
- Document verification
- Event check-in systems
- Automated data entry

## Features

- **Multiple Formats**: QR Code, EAN-13, Code128, Code39, UPC-A, DataMatrix
- **Batch Processing**: Scan multiple images in one operation
- **Data Extraction**: Decode to text, URLs, structured data
- **Image Preprocessing**: Auto-rotation, enhancement for better recognition
- **Validation**: Verify barcode checksums
- **Export**: JSON, CSV output with decoded data

## Quick Start

```python
from qr_barcode_reader import QRBarcodeReader

# Read QR code
reader = QRBarcodeReader()
result = reader.read_image('qr_code.png')
print(result.data)  # Decoded text

# Batch read directory
results = reader.read_directory('images/', formats=['qr', 'ean13'])
```

## CLI Usage

```bash
# Read single image
python qr_barcode_reader.py image.png

# Batch read directory
python qr_barcode_reader.py images/*.png --output results.json
```
