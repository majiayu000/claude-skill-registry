---
name: commerce-accounts-payable
description: Manage supplier bills, payments, and AP aging. Use when recording supplier invoices, processing payments, running payment batches, or reviewing AP aging reports.
---

# Commerce Accounts Payable

Track supplier bills, process payments, run payment batches, and monitor AP aging.

## How It Works

1. Create bills from supplier invoices with line items.
2. Approve bills for payment.
3. Record individual payments or create payment runs for batch processing.
4. Allocate payments to specific bills.
5. Generate AP aging reports by supplier.

## Usage

- MCP tools: `list_bills`, `create_bill`, `approve_bill`, `record_bill_payment`, `create_payment_run`, `approve_payment_run`, `get_ap_aging`, `get_ap_summary`.
- Writes require `--apply`.

## Bill Statuses

- Draft -> Pending -> Approved -> PartiallyPaid -> Paid (or Cancelled/Disputed/Overdue)

## Payment Methods

- Check, ACH, Wire, CreditCard, Cash, Other

## Payment Run Statuses

- Draft -> Pending -> Approved -> Processing -> Completed (or Cancelled)

## Aging Buckets

- Current, 1-30 days, 31-60 days, 61-90 days, 90+ days

## Output

```json
{"status":"payment_recorded","bill_id":"BILL-2025-0050","amount_paid":2500.00,"balance_remaining":0.00,"payment_method":"ACH"}
```

## Present Results to User

- Bill number, supplier, and payment status.
- Amount paid and remaining balance.
- Aging summary with overdue amounts by bucket.
- Payment run totals and included bills.

## Troubleshooting

- Bill not approved: bills must be approved before payment.
- Payment exceeds balance: verify bill amount and prior payments.
- Duplicate bill: check existing bills for the same supplier invoice number.

## References
- references/ap-aging.md
- /home/dom/stateset-icommerce/crates/stateset-core/src/models/accounts_payable.rs
- /home/dom/stateset-icommerce/crates/stateset-embedded/src/accounts_payable.rs
