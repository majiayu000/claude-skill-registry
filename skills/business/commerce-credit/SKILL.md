---
name: commerce-credit
description: Manage customer credit accounts, credit holds, and credit applications. Use when checking credit availability, placing holds on orders, or reviewing credit applications.
---

# Commerce Credit

Manage customer credit limits, perform credit checks, process credit applications, and place or release credit holds.

## How It Works

1. Create credit accounts for customers with limits and risk ratings.
2. Run credit checks before order approval.
3. Place credit holds on orders that exceed limits or have past-due balances.
4. Process credit applications with approval workflow.
5. Track credit transactions (charges, payments, adjustments).
6. Release holds after payment or approval override.

## Usage

- MCP tools: `create_credit_account`, `get_credit_account`, `update_credit_account`, `check_credit`, `place_credit_hold`, `release_credit_hold`, `submit_credit_application`, `review_credit_application`, `record_credit_transaction`, `get_customer_credit_summary`.
- Writes require `--apply`.

## Credit Account Statuses

- Active, Suspended, OnHold, Closed, PendingReview

## Risk Ratings

- Low, Medium, High, Critical

## Hold Types

- OverLimit: order would exceed credit limit
- PastDue: customer has past-due invoices
- Manual: manually placed by credit manager
- NewCustomer: first-time buyer review
- HighRisk: elevated risk rating

## Credit Application Statuses

- Pending -> UnderReview -> Approved/Denied/MoreInfoNeeded (or Withdrawn)

## Credit Transaction Types

- Charge, Payment, CreditMemo, Adjustment, WriteOff, LimitChange

## Output

```json
{"status":"credit_check","customer_id":"cust_123","approved":true,"credit_limit":10000.00,"available_credit":7500.00,"order_amount":2000.00}
```

## Present Results to User

- Credit check result (approved/denied/requires_approval).
- Current limit, used, and available credit.
- Active holds with reasons.
- Credit application decision and terms.

## Troubleshooting

- Order on hold: check hold type; release after payment or manager override.
- Credit check denied: customer over limit or has past-due balance.
- Application stuck: verify all required business information is provided.

## References
- references/credit-management.md
- /home/dom/stateset-icommerce/crates/stateset-core/src/models/credit.rs
- /home/dom/stateset-icommerce/crates/stateset-embedded/src/credit.rs
