---
name: pharmacy-dev
description: >
  Pharmacy module development guide for the HMIS project. Use when working on pharmacy
  features including GRN, purchase orders, stock transfers, disbursements, retail sales,
  pharmacy reports, stock management, item substitution, or pharmacy billing workflows.
user-invocable: true
---

# Pharmacy Module Development Guide

## Key Documentation

For detailed pharmacy development, refer to these files:

- [Pharmaceutical Management API](../../developer_docs/API_PHARMACEUTICAL_MANAGEMENT.md) - REST API for managing VTM, ATM, VMP, AMP, VMPP, AMPP, categories, dosage forms, and measurement units
- [GRN Fixes](../../developer_docs/pharmacy/grn-fully-issued-fix.md) - GRN completion patterns
- [Multi-Window Sales](../../developer_docs/pharmacy/PHARMACY_RETAIL_SALE_MULTI_WINDOW_GUIDE.md.md) - Multi-window handling
- [Cost Accounting Signs](../../developer_docs/pharmacy/cost-accounting-sign-conventions.md) - Sign normalization
- [Disbursement Signs](../../developer_docs/pharmacy/disbursement-sign-normalization.md) - Disbursement conventions
- [Quantity Decimals](../../developer_docs/pharmacy/quantity-decimal-validation-guide.md) - Decimal validation
- [Transfer Disbursement](../../developer_docs/billing/PHARMACY_TRANSFER_DISBURSEMENT_DOCUMENTATION.md) - Transfer workflow
- [Purchase Order Workflow](../../developer_docs/po-workflow-documentation.md) - PO workflow

## Configuration Options

Pharmacy uses `configOptionApplicationController.getBooleanValueByKey()` for feature toggles. Key patterns:
- `Pharmacy Transfer is by Purchase Rate` / `Cost Rate` / `Retail Rate`
- `Display Colours for Stock Autocomplete Items`
- `Pharmacy Disbursement Reports - Display *` (various column visibility)

## Common Patterns

### Stock Queries
- Always include `s.retired = false` and `s.itemBatch.item.retired = false`
- Filter inactive items with `s.itemBatch.item.inactive = false`
- Use DTOs for display, entities for business logic

### Transfer Workflow
- Transfer Request -> Transfer Issue -> Transfer Receive
- Each step creates a Bill with appropriate BillType
- Sign conventions matter for cost accounting

### Retail Sale
- Use StockDTO for autocomplete performance
- Cache autocomplete results for converter
- Defer expensive discount calculations

## Backward Compatibility

- Never "fix" `purcahseRate` spelling - it's a database column name
- Never rename composite components without checking ALL usage
