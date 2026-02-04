---
name: barcode-generator
description: Generate barcodes in multiple formats (Code128, EAN13, UPC, Code39, QR). Supports batch generation from CSV and various output formats.
---

# Barcode Generator

Generate barcodes in various formats for retail, inventory, and identification. Supports 1D barcodes (Code128, EAN, UPC) and batch generation from CSV.

## Quick Start

```python
from scripts.barcode_gen import BarcodeGenerator

# Generate barcode
gen = BarcodeGenerator()
gen.generate("123456789012", format="ean13", output="barcode.png")

# Code128 (variable length)
gen.generate("ABC-12345", format="code128", output="product.png")

# Batch from CSV
gen.batch_generate("products.csv", code_column="sku", output_dir="./barcodes")
```

## Features

- **Multiple Formats**: Code128, EAN13, EAN8, UPC-A, Code39, ITF, ISBN
- **Output Formats**: PNG, SVG, PDF
- **Customization**: Size, colors, text display
- **Batch Generation**: From CSV files
- **Validation**: Check digit calculation and verification

## API Reference

### Basic Generation

```python
gen = BarcodeGenerator()

# Generate with auto-format detection
gen.generate("123456789012", output="barcode.png")

# Specific format
gen.generate("12345678", format="ean8", output="barcode.png")
```

### Customization

```python
gen.generate(
    "ABC123",
    format="code128",
    output="barcode.png",
    width=300,            # Image width
    height=150,           # Image height
    show_text=True,       # Show code below barcode
    font_size=12,         # Text size
    foreground="black",   # Bar color
    background="white"    # Background color
)
```

### Batch Generation

```python
# From CSV
gen.batch_generate(
    "products.csv",
    code_column="sku",
    format="code128",
    output_dir="./barcodes",
    filename_column="product_name"  # Use product name as filename
)

# From list
codes = ["ABC001", "ABC002", "ABC003"]
gen.batch_generate_list(codes, format="code128", output_dir="./barcodes")
```

### Validation

```python
# Validate barcode format
is_valid = gen.validate("5901234123457", format="ean13")

# Calculate check digit
check = gen.calculate_check_digit("590123412345", format="ean13")
# Returns: 7

# Generate with auto check digit
gen.generate("590123412345", format="ean13", auto_check_digit=True)
```

### Output Formats

```python
# PNG (default)
gen.generate("123", format="code128", output="barcode.png")

# SVG (vector)
gen.generate("123", format="code128", output="barcode.svg")

# PDF
gen.generate("123", format="code128", output="barcode.pdf")
```

## CLI Usage

```bash
# Generate single barcode
python barcode_gen.py --code "123456789012" --format ean13 --output barcode.png

# Code128
python barcode_gen.py --code "ABC-12345" --format code128 --output product.png

# Custom size
python barcode_gen.py --code "12345" --format code39 --width 400 --height 200

# Batch from CSV
python barcode_gen.py --batch products.csv --column sku --format code128 --output-dir ./barcodes

# Validate
python barcode_gen.py --validate "5901234123457" --format ean13
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--code` | Code to encode | - |
| `--format` | Barcode format | code128 |
| `--output` | Output file | - |
| `--width` | Image width | 300 |
| `--height` | Image height | 150 |
| `--no-text` | Hide code text | False |
| `--batch` | CSV file for batch | - |
| `--column` | Code column in CSV | code |
| `--output-dir` | Output directory | . |
| `--validate` | Validate code | - |

## Supported Formats

| Format | Length | Characters | Use Case |
|--------|--------|------------|----------|
| `code128` | Variable | ASCII | General purpose |
| `ean13` | 13 | Digits | Retail products |
| `ean8` | 8 | Digits | Small products |
| `upca` | 12 | Digits | US retail |
| `code39` | Variable | A-Z, 0-9, symbols | Industrial |
| `itf` | Even | Digits | Shipping |
| `isbn13` | 13 | Digits | Books |
| `isbn10` | 10 | Digits + X | Books (legacy) |

## Examples

### Product Label

```python
gen = BarcodeGenerator()

gen.generate(
    "5901234123457",
    format="ean13",
    output="product_barcode.png",
    width=250,
    height=100,
    show_text=True
)
```

### Inventory Tags

```python
gen = BarcodeGenerator()

inventory = [
    {"sku": "INV-001", "name": "Widget A"},
    {"sku": "INV-002", "name": "Widget B"},
    {"sku": "INV-003", "name": "Widget C"}
]

for item in inventory:
    gen.generate(
        item["sku"],
        format="code128",
        output=f"./tags/{item['name']}.png"
    )
```

### Book ISBN

```python
gen = BarcodeGenerator()

# ISBN-13 barcode
gen.generate(
    "9780134685991",
    format="isbn13",
    output="book_barcode.png"
)
```

### Batch Product Labels

```python
gen = BarcodeGenerator()

# products.csv:
# sku,product_name,price
# 123456789012,Widget A,9.99
# 234567890123,Widget B,14.99

gen.batch_generate(
    "products.csv",
    code_column="sku",
    format="ean13",
    output_dir="./product_labels",
    filename_column="product_name"
)
```

## Check Digit Calculation

The generator can automatically calculate and append check digits:

```python
gen = BarcodeGenerator()

# EAN-13: 12 digits + 1 check digit
gen.generate("590123412345", format="ean13", auto_check_digit=True)
# Generates barcode for "5901234123457"

# Manually calculate
check = gen.calculate_check_digit("590123412345", format="ean13")
print(f"Check digit: {check}")  # 7
```

## Dependencies

```
python-barcode>=0.15.0
Pillow>=10.0.0
```

## Limitations

- Some formats have strict length requirements
- Characters must match format specifications
- PDF output may require additional fonts
- Very long codes may not scan well at small sizes
