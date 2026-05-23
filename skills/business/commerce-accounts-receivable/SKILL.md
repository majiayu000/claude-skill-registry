---
name: commerce-accounts-receivable
description: Manage customer receivables, collections, credit memos, and AR aging. Use when tracking overdue invoices, sending dunning letters, creating write-offs, or generating customer statements.
---

# Commerce Accounts Receivable

Track customer receivables, manage collections, issue credit memos, and monitor AR aging.

## How It Works

1. Monitor AR aging to identify overdue accounts.
2. Log collection activities (dunning letters, calls, emails).
3. Issue credit memos for returns, pricing errors, or goodwill.
4. Apply payments and credit memos to outstanding invoices.
5. Write off uncollectible balances with approval.
6. Generate customer statements.

## Usage

- MCP tools: `get_ar_aging`, `get_customer_ar_aging`, `log_collection_activity`, `create_credit_memo`, `apply_credit_memo`, `apply_payment_to_invoice`, `create_write_off`, `get_customer_statement`, `get_customer_ar_summary`.
- Writes require `--apply`.

## Collection Statuses

- None -> Reminder1Sent -> Reminder2Sent -> Reminder3Sent -> InCollections -> SentToAgency (or WrittenOff/PromiseToPay/PaymentPlan)

## Dunning Letter Types

- Reminder1, Reminder2, Reminder3, DemandLetter, CollectionNotice

## Credit Memo Reasons

- ReturnedGoods, PricingError, Overpayment, Damaged, ServiceCredit, GoodwillAdjustment, Other

## Write-Off Reasons

- Uncollectible, Bankruptcy, CustomerDispute, SmallBalance, AccountClosed, Deceased, Other

## Aging Buckets

- Current, 1-30 days, 31-60 days, 61-90 days, 90+ days

## Output

```json
{"status":"dunning_sent","customer_id":"cust_123","dunning_type":"Reminder2","total_overdue":3250.00,"invoices_overdue":3}
```

## Present Results to User

- Customer name and total outstanding balance.
- Aging breakdown by bucket.
- Collection activity history and next recommended action.
- Credit memo and write-off totals.

## Troubleshooting

- Credit memo won't apply: verify memo status is Open and invoice has remaining balance.
- Write-off rejected: ensure approver and GL account are provided.
- Aging mismatch: confirm invoice dates and payment applications are current.

## References
- references/ar-collections.md
- /home/dom/stateset-icommerce/crates/stateset-core/src/models/accounts_receivable.rs
- /home/dom/stateset-icommerce/crates/stateset-embedded/src/accounts_receivable.rs
