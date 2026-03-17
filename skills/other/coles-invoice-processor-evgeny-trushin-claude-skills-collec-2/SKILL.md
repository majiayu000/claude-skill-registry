---
name: coles-invoice-processor
description: Processes Coles grocery invoices to extract structured data and predict future orders. Use when user uploads/pastes invoice content, asks to analyze grocery purchases, or wants shopping predictions.
---

# Coles Invoice Processor Skill

Analyze Coles grocery store invoices using Python scripts to convert PDFs, extract structured data, and predict future orders with budget forecasts.

## When to Use This Skill

Activate when the user:
- Uploads Coles invoice PDFs or images
- Pastes invoice text content
- Asks to extract grocery item data
- Wants to analyze shopping history
- Requests future order predictions
- Needs shopping budget estimates

## Setup Requirements

Before using the scripts, ensure dependencies are installed:

```bash
# Create virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Required packages:** `pymupdf4llm`, `pandas`, `prophet`

## Pipeline Overview

The processing pipeline consists of 3 main scripts:

1. **01_convert.py** - Convert PDFs to Markdown
2. **03_extract_data.py** - Extract structured data from Markdown
3. **04_predict_orders.py** - Predict future orders and budget

## How to Process Invoices

### Step 1: Place Invoice PDFs

Place Coles invoice PDFs in the `input_invoices/` directory.

### Step 2: Convert PDFs to Markdown

```bash
python 01_convert.py
```

This converts each PDF in `input_invoices/` to a Markdown file in the same folder using `pymupdf4llm`.

### Step 3: Extract Structured Data

```bash
python 03_extract_data.py
```

Parses the Markdown invoices and extracts:
- Invoice metadata (number, date, time)
- Categories and items
- Product names, quantities, prices, weights

Output: `output_extracted/extracted_data.json`

### Step 4: Predict Future Orders

```bash
python 04_predict_orders.py
```

Analyzes purchase history and:
- Calculates average purchase intervals per product
- Determines typical quantities
- Forecasts ~150 days of future orders
- Groups orders within 3 days
- Merges small orders (<$50) with adjacent orders within 6 days
- Generates monthly budget estimates

## Data Extraction Details

The extraction script parses Markdown looking for:

**Invoice Metadata:**
- Invoice number: `**Invoice number:** #123456`
- Invoice date: `**Invoice date:** 7 December 2024`
- Invoice time: `**Invoice time:** 14:30:00`

**Product Categories:**
Categories appear as bold headers (e.g., `**Dairy**`, `**Bakery**`, `**Meat & Seafood**`)

**Product Line Items:**
Format: `[Product Name](link) Ordered Picked UnitPrice TotalPrice`

Example:
```
[Coles Full Cream Milk 3L](https://...) 2 2 $4.65 $9.30
```

Extracted fields:
- Product name (including weight/size from name like "3L", "500g", "1kg")
- Quantity ordered
- Quantity picked
- Unit price
- Total price

## Output Formats

### Extracted Data JSON Schema
```json
{
  "filename": "ea[REDACTED]_044712.md",
  "invoice_number": "[REDACTED]",
  "invoice_date": "7 December 2024",
  "invoice_time": "14:30:00",
  "categories": [
    {
      "name": "Dairy",
      "items": [
        {
          "product": "Coles Full Cream Milk 3L",
          "weight": "3L",
          "link": "https://...",
          "ordered": "2",
          "picked": "2",
          "unit_price": "$4.65",
          "total_price": "$9.30"
        }
      ]
    }
  ]
}
```

### Predicted Orders Output
```
Order #1 - Approx Date: 2025-12-15 - Total Est. Cost: $95.50
Product                                            | Qty   | Unit $   | Total $
--------------------------------------------------------------------------------
Coles Full Cream Milk 3L...                        | 2     | $4.65    | $9.30
```

### Monthly Budget Output
```
--- Estimated Monthly Budget ---
2025-December: $785.80
2026-January: $738.55
2026-February: $692.40
```

## Privacy Notes

- Invoice numbers are automatically redacted in filenames and output
- Filenames like `ea12345_67890.md` become `ea[REDACTED]_67890.md`
- Sensitive personal information should be manually reviewed
- Focus on product and pricing data only

## Common Categories in Coles Invoices

- Dairy
- Bakery
- Meat & Seafood
- Fruit & Vegetables
- Pantry
- Frozen
- Drinks
- Health & Beauty
- Baby
- Household
