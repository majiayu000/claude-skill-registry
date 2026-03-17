---
name: currency-converter
description: Convert currencies with real-time exchange rates, historical data, and multi-currency calculations.
---

# Currency Converter

Convert between currencies with exchange rates and formatting.

## Features

- **Exchange Rates**: Convert between 150+ currencies
- **Historical Rates**: Date-based conversions
- **Batch Conversion**: Process multiple amounts
- **Currency Formatting**: Locale-specific formatting
- **CSV Support**: Convert currency columns
- **Rate Caching**: Efficient API usage

## CLI Usage

```bash
python currency_converter.py --amount 100 --from USD --to EUR
python currency_converter.py --file amounts.csv --from_col usd --to EUR --output converted.csv
```

## Dependencies

- forex-python>=1.8
- pandas>=2.0.0
