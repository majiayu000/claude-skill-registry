---
name: invoice-organization
description: Organize and manage invoices with OCR extraction, categorization, and expense tracking
---

# Invoice Organization Skill

Organize, extract data from, and manage invoices for accounting and expense tracking.

## When to Use
- Expense management
- Accounting workflows
- Tax preparation
- Vendor payment tracking

## Core Capabilities
- OCR text extraction
- Data parsing (amount, date, vendor)
- Categorization (expense type)
- Duplicate detection
- Date-based filing
- Export to accounting software

## Workflow
1. **Scan/Upload**: Capture invoice images
2. **OCR**: Extract text
3. **Parse**: Extract key fields (amount, date, vendor, items)
4. **Categorize**: Assign expense category
5. **Store**: Organize by date/vendor/category
6. **Export**: Generate reports or export to QuickBooks/Xero

## Tools
- Tesseract OCR
- Invoice2data (Python)
- Tabula (PDF tables)
- Accounting software APIs

## Best Practices
- Standardize naming: `YYYYMMDD_Vendor_Amount.pdf`
- Backup regularly
- Verify OCR accuracy
- Track payment status
- Archive annually

## Resources
- Tesseract: https://github.com/tesseract-ocr/tesseract
- invoice2data: https://github.com/invoice-x/invoice2data
