---
id: stripe-billing-overview
name: Stripe Billing Overview
description: Search charges, balance and refund metrics
role: sales
requiredTools:
  - type: mcpService
    serviceType: stripe
---

## Stripe Billing Overview

When answering billing or revenue questions with Stripe:

- Use **stripe_search_charges** (tool name may have a suffix if multiple Stripe servers exist) to find charges by query string and/or email.
- Use **stripe_get_metrics** to retrieve balance and refunds for a required date range.
- Summarize revenue and refund trends clearly; cite the date range used.
- The integration is read-only; no write operations are performed.
- Always specify a date range for metrics; use the user's implied period (e.g. "this month") or ask if unclear.

## Step-by-step instructions

1. For "charges for customer X" or "find charge Y": call **stripe_search_charges** with query and/or email as appropriate.
2. For balance or refunds: call **stripe_get_metrics** with the required date range (start and end).
3. For revenue overview: use **stripe_get_metrics** for the period; summarize balance and refunds; optionally use **stripe_search_charges** to illustrate recent charges.
4. When summarizing: report amounts and date range; distinguish balance vs refunds when both are relevant.
5. If the user asks for a time period not given, infer (e.g. "last 30 days") or ask for clarification.

## Examples of inputs and outputs

- **Input**: "What's our Stripe balance and refunds for last month?"  
  **Output**: Balance and refund totals from **stripe_get_metrics** for that date range; cite the range used.

- **Input**: "Find charges for john@example.com."  
  **Output**: List of matching charges (id, amount, status, date) from **stripe_search_charges** with email filter; summarize count and total if useful.

## Common edge cases

- **No date range for metrics**: **stripe_get_metrics** requires a date range; infer from context (e.g. "this month") or ask the user.
- **No charges found**: Say "No charges matching [query/email]" and suggest widening the search.
- **Read-only**: Do not attempt to create refunds or modify data; only report what the tools return.
- **API/OAuth error**: Report that Stripe returned an error and suggest reconnecting or retrying.

## Tool usage for specific purposes

- **stripe_search_charges**: Use to find charges by Stripe query string and/or email; use for "charges for X" or "find charge".
- **stripe_get_metrics**: Use for balance and refunds in a date range; always provide the required date range for the period requested.
