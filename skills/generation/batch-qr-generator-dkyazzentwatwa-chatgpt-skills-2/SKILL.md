---
name: batch-qr-generator
description: Use when asked to generate multiple QR codes from CSV data, create bulk QR codes with tracking, or generate QR codes for events/products.
---

# Batch QR Generator

Generate bulk QR codes from CSV data with UTM tracking, logos, and customizable styling for events, products, and marketing.

## Purpose

Bulk QR code generation for:
- Event ticketing and check-in
- Product inventory tracking
- Marketing campaign tracking (UTM parameters)
- Business card contact sharing
- Bulk URL shortening with QR codes

## Features

- **CSV Input**: Generate from spreadsheet data
- **UTM Tracking**: Auto-add campaign tracking parameters
- **Custom Styling**: Colors, logos, error correction
- **Sequential Naming**: Auto-generate filenames
- **Metadata Export**: CSV with QR data and filenames
- **Format Options**: PNG, SVG output

## Quick Start

```python
from batch_qr_generator import BatchQRGenerator

# Generate from CSV
generator = BatchQRGenerator()
generator.load_csv('products.csv', url_column='product_url')
generator.add_utm_params(source='catalog', medium='qr', campaign='2024Q1')
generator.generate_batch(output_dir='qr_codes/')
```

## CLI Usage

```bash
# Generate QR codes from CSV
python batch_qr_generator.py --csv products.csv --url-column url --output-dir qr_codes/

# Add UTM tracking
python batch_qr_generator.py --csv products.csv --url-column url --utm-source catalog --utm-campaign 2024Q1 --output-dir qr_codes/

# Add logo
python batch_qr_generator.py --csv urls.csv --url-column link --logo logo.png --output-dir branded_qr/
```
