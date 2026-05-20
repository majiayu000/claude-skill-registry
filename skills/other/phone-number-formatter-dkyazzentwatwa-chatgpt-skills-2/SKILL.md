---
name: phone-number-formatter
description: Standardize and format phone numbers with international support, validation, and multiple output formats.
---

# Phone Number Formatter

Standardize and format phone numbers with validation.

## Features

- **Format Standardization**: Convert to E.164, national, international
- **Validation**: Check valid phone numbers
- **Country Detection**: Auto-detect country codes
- **Batch Processing**: Format multiple numbers
- **Carrier Info**: Extract carrier/type information
- **CSV Support**: Process phone columns

## CLI Usage

```bash
python phone_number_formatter.py --input phones.csv --column phone --format international --output formatted.csv
```

## Dependencies

- phonenumbers>=8.13.0
- pandas>=2.0.0
