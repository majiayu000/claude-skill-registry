---
name: address-parser
description: Parse unstructured addresses into structured components - street, city, state, zip, country with validation.
---

# Address Parser

Parse unstructured addresses into structured fields.

## Features

- **Component Extraction**: Street, city, state, zip, country
- **Format Standardization**: Normalize address formats
- **Validation**: Verify address components
- **Batch Processing**: Parse multiple addresses
- **International Support**: Multiple country formats
- **Geocoding Ready**: Output for geocoding APIs

## CLI Usage

```bash
python address_parser.py --input addresses.csv --column address --output parsed.csv
```

## Dependencies

- pandas>=2.0.0
