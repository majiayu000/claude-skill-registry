---
name: invoice-processing
description: Extract, validate, and categorize invoice data against purchase orders and GL codes. Use when the user requests invoice processing or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: community
  version: "1.0"
---

# Invoice Processing

Extract structured data from invoices, validate fields against purchase orders and vendor records, categorize line items by general ledger (GL) codes, and flag discrepancies for review. This skill handles both single invoice processing and batch operations, producing clean, auditable output ready for import into accounting systems.

## Workflow

1. **Receive and Parse Invoice**
   Accept invoice data in any format — raw text, OCR output, structured JSON, or CSV. Identify the document type (standard invoice, credit memo, debit note, proforma) and extract the header block: invoice number, date, due date, vendor name, vendor address, and payment terms.

2. **Extract Line Items and Totals**
   Parse each line item for description, quantity, unit price, extended amount, and tax. Validate that line item totals sum to the stated subtotal. Extract tax amounts, shipping charges, discounts, and the grand total. Flag any arithmetic inconsistencies between line items and totals.

3. **Validate Against Purchase Order**
   Match the invoice to its corresponding PO by PO number, vendor, or line item descriptions. Compare quantities and unit prices. Compute a three-way match score across PO, goods receipt, and invoice. Flag invoices where price variance exceeds a configurable threshold (default: 2%) or quantities don't match.

4. **Categorize by GL Code**
   Assign each line item to the appropriate general ledger account based on item description, vendor category, and historical patterns. Common mappings include office supplies → 6200, software subscriptions → 6500, professional services → 6300, raw materials → 5100. Apply department cost center codes where applicable.

5. **Flag Discrepancies and Generate Output**
   Produce a structured record for each invoice with all extracted fields, validation status, GL assignments, and any flags. Group flags by severity: blocking errors (missing PO, total mismatch > 5%), warnings (minor price variance, missing fields), and informational (new vendor, first invoice from vendor).

6. **Generate Processing Summary**
   For batch operations, produce a summary report showing total invoices processed, pass/fail counts, total dollar value, and a breakdown of flag types. List all blocked invoices requiring manual review with specific reasons.

## Usage

Provide invoice data as text, structured data, or describe the invoices you need processed. Specify any PO data for validation and your GL code mapping preferences.

**Example prompt:**
> Process this vendor invoice: Invoice #INV-2024-0847 from Acme Cloud Services, dated 2024-11-15, PO #PO-4521. Line items: 10x API Gateway licenses at $150/ea, 1x Premium Support at $2,400/yr. Tax 8.5%. Validate against PO and assign GL codes.

## Examples

### Example 1: Single Invoice Processing

**Input:**
```
Invoice #INV-2024-0847
Vendor: Acme Cloud Services (Vendor ID: V-1042)
Date: 2024-11-15 | Due: 2024-12-15 | Terms: Net 30
PO Reference: PO-4521

Line Items:
  1. API Gateway License (qty: 10, unit: $150.00) — $1,500.00
  2. Premium Support Annual (qty: 1, unit: $2,400.00) — $2,400.00

Subtotal: $3,900.00
Tax (8.5%): $331.50
Total: $4,231.50
```

**Output:**
```json
{
  "invoice_number": "INV-2024-0847",
  "vendor": { "name": "Acme Cloud Services", "id": "V-1042" },
  "date": "2024-11-15",
  "due_date": "2024-12-15",
  "po_reference": "PO-4521",
  "line_items": [
    {
      "description": "API Gateway License",
      "quantity": 10,
      "unit_price": 150.00,
      "amount": 1500.00,
      "gl_code": "6500",
      "gl_name": "Software Subscriptions",
      "cost_center": "IT-200"
    },
    {
      "description": "Premium Support Annual",
      "quantity": 1,
      "unit_price": 2400.00,
      "amount": 2400.00,
      "gl_code": "6510",
      "gl_name": "Software Maintenance & Support",
      "cost_center": "IT-200"
    }
  ],
  "subtotal": 3900.00,
  "tax": 331.50,
  "total": 4231.50,
  "validation": {
    "arithmetic_check": "PASS",
    "po_match": "PASS",
    "price_variance": "0.0%",
    "three_way_match": "PASS"
  },
  "flags": []
}
```

### Example 2: Batch Processing with Validation Errors

**Input:** 4 invoices from different vendors processed in batch.

**Output — Error Report:**

| Invoice #       | Vendor              | Amount     | Status  | Flags                                          |
|-----------------|---------------------|------------|---------|-------------------------------------------------|
| INV-2024-0847   | Acme Cloud Services | $4,231.50  | PASS    | —                                               |
| INV-2024-1193   | Delta Office Supply | $892.40    | WARNING | Unit price $14.20 vs PO price $12.99 (+9.3%)   |
| INV-2024-1205   | Spark Consulting    | $18,750.00 | BLOCKED | No matching PO found                            |
| INV-2024-1210   | GreenLeaf Catering  | $1,345.00  | BLOCKED | Line item total $1,280 ≠ stated subtotal $1,345 |

**Batch Summary:**
- **Total Processed:** 4
- **Passed:** 1 (25%) — $4,231.50
- **Warnings:** 1 (25%) — $892.40
- **Blocked:** 2 (50%) — $20,095.00
- **Total Value:** $25,168.90
- **Action Required:** 2 invoices require manual review before payment authorization.

## Best Practices

- Always verify arithmetic independently — never trust the stated totals without recalculating from line items.
- Maintain a vendor-to-GL mapping table and update it as new vendors or expense types appear.
- Set price variance thresholds appropriate to your industry: 2% for commodities, up to 10% for services with variable scope.
- Require PO matching for all invoices above a configurable dollar threshold to prevent unauthorized spending.
- Retain the raw invoice data alongside extracted fields for audit trail purposes.
- Process invoices in batch during off-peak hours and route exceptions to AP staff immediately.

## Safety Boundaries

- Treat the output as analytical support, not individualized financial, tax, investment, or accounting advice.
- Preserve source data and expose assumptions, formulas, units, and reconciliation checks so a reviewer can reproduce the result.
- Do not initiate payments, transactions, journal entries, filings, or account changes without explicit user authorization.
- Require a qualified professional to review material decisions, regulated filings, or conclusions based on incomplete data.

## Edge Cases

- **Invoices with no PO reference:** Flag as requiring manual approval. Check if the vendor has a blanket PO or standing agreement that covers the charges.
- **Credit memos and negative amounts:** Process as negative invoice entries. Validate that the credit references an existing invoice and that the credit amount doesn't exceed the original.
- **Multi-currency invoices:** Extract the stated currency, apply the exchange rate as of invoice date, and record both the original and converted amounts.
- **Duplicate invoice detection:** Check invoice number + vendor + amount + date against the last 90 days of records. Flag exact matches as likely duplicates and near-matches (same vendor + amount, different invoice number) as potential duplicates.
- **Partial shipments:** When goods receipt quantity is less than PO quantity, validate the invoice against received quantity, not PO quantity. Hold remaining balance as open.
