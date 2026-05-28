---
name: pane-mcp
description: Access personal finance data (bank accounts, transactions, balances, spending, investments, crypto) via Pane's hosted MCP server using mcporter. Requires a Pane account and API key.
homepage: https://pane.money
metadata: {"clawdbot":{"emoji":"💳","install":[{"id":"mcporter","kind":"skill","skill":"steipete/mcporter","label":"Install mcporter skill"}]},"openclaw":{"primaryEnv":"PANE_API_KEY","requires":{"env":["PANE_API_KEY"],"bins":["mcporter"],"skills":["mcporter"]}}}
---

# Pane MCP

Access a user's linked financial accounts via [Pane](https://pane.money), a hosted MCP server powered by Plaid. Query bank accounts, transactions, balances, spending summaries, recurring payments, investments, liabilities, and crypto holdings. Write persistent annotations to remember context across conversations.

## Setup

The user must have a Pane account with linked financial accounts and an API key from [pane.money/dashboard/connect](https://pane.money/dashboard/connect).

Set the `PANE_API_KEY` environment variable (do not paste the key directly into shell commands):

```bash
# Add to your shell profile (.zshrc, .bashrc, etc.)
export PANE_API_KEY="pane_sk_live_..."
```

Then configure mcporter:

```bash
# Add Pane as an MCP server using the env var
mcporter config add pane --url https://mcp.pane.money --header "Authorization: Bearer $PANE_API_KEY"

# Verify connection
mcporter list pane --schema
```

## Tools

### Financial data (read-only)

**get_accounts** — List linked accounts with balances

```bash
mcporter call pane.get_accounts type=all
mcporter call pane.get_accounts type=checking
```

**get_transactions** — Search and filter transactions

```bash
mcporter call pane.get_transactions search=Starbucks limit:50
mcporter call pane.get_transactions category=FOOD_AND_DRINK start_date=2026-01-01 end_date=2026-01-31
mcporter call pane.get_transactions account_id=<uuid> min_amount:50
```

Parameters: `account_id` (UUID), `start_date`/`end_date` (YYYY-MM-DD), `category` (Plaid category), `search` (max 200 chars), `min_amount`/`max_amount`, `limit` (1-500, default 50), `offset`.

**get_balances** — Current balances with net worth summary (triggers live Plaid refresh)

```bash
mcporter call pane.get_balances type=all
```

Returns per-account balances plus summary: `total_cash`, `total_credit_debt`, `total_investments`, `total_loans`, `total_crypto`, `net_worth`.

**get_spending_summary** — Spending grouped by category, merchant, week, or month

```bash
mcporter call pane.get_spending_summary period=this_month group_by=category
mcporter call pane.get_spending_summary period=last_30d group_by=merchant
mcporter call pane.get_spending_summary start_date=2026-01-01 end_date=2026-01-31 group_by=week
```

Period shortcuts: `last_7d`, `last_30d`, `this_week`, `last_week`, `this_month`, `last_month`, `this_year`. Use either `period` OR `start_date`+`end_date`, not both.

**get_recurring** — Subscriptions, bills, and income streams

```bash
mcporter call pane.get_recurring type=all
mcporter call pane.get_recurring type=subscriptions
```

Returns arrays for subscriptions/bills/income with monthly totals. Frequency conversion: weekly x4.33, biweekly x2.17, monthly x1, annually /12.

**get_investments** — Investment holdings and portfolio value

```bash
mcporter call pane.get_investments
mcporter call pane.get_investments account_id=<uuid>
```

Cached 15 minutes. Returns holdings with symbol, quantity, currentValue, costBasis.

**get_liabilities** — Credit, student loan, and mortgage details

```bash
mcporter call pane.get_liabilities type=all
mcporter call pane.get_liabilities type=credit
```

Cached 1 hour. Returns APRs, payment amounts, due dates.

**get_crypto** — Crypto holdings across exchange accounts and on-chain wallets

```bash
mcporter call pane.get_crypto blockchain=all
mcporter call pane.get_crypto wallet_id=<uuid> blockchain=ethereum
```

Requires crypto feature enabled. Triggers live wallet refresh.

### Annotations (read/write)

Annotations are persistent notes attached to transactions, merchants, accounts, or the user's profile. They appear in future tool results automatically.

**write_annotation** — Save a note

```bash
mcporter call pane.write_annotation scope=profile content="Freelancer, budgets $3k/month for essentials"
mcporter call pane.write_annotation scope=merchant target_id=WeWork content="Business expense — coworking"
mcporter call pane.write_annotation scope=account target_id=<uuid> content="Joint account with partner"
mcporter call pane.write_annotation scope=transaction target_id=<uuid> content="Reimbursable expense"
```

Scopes: `profile` (no target_id), `merchant` (case-insensitive name), `account` (UUID), `transaction` (UUID). Max 2,000 chars, max 50 per target.

**list_annotations** — List saved annotations

```bash
mcporter call pane.list_annotations
mcporter call pane.list_annotations scope=profile limit:10
```

**delete_annotation** — Delete by ID

```bash
mcporter call pane.delete_annotation annotation_id=<uuid>
```

## Resources

```bash
mcporter call pane.read_resource uri=pane://profile     # Text summary: accounts, net worth, income, model notes
mcporter call pane.read_resource uri=pane://accounts    # JSON list of accounts with names and types
mcporter call pane.read_resource uri=pane://insights    # JSON: net worth breakdown, unusual spending, low balance warnings, upcoming bills
```

Start with `pane://profile` for a quick overview, then drill in with tools.

## Privacy scopes

Each account has a privacy scope set by the user. The server enforces these automatically:

| Scope | Balances | Transactions | Merchants |
|-------|----------|-------------|-----------|
| `full` | Visible | Visible | Visible |
| `balances_and_redacted` | Visible | Visible | "Redacted" |
| `balances_only` | Visible | Hidden | Hidden |
| `hidden` | Hidden | Hidden | Hidden |

If transactions return empty for an account that exists, it's privacy-scoped — not missing data.

## Rate limits

30 requests/minute, 1,000/day per user. Prefer `get_spending_summary` over iterating `get_transactions`. Read resources first to plan tool calls.

## Common patterns

**Net worth**: `get_balances type=all` — check `summary.net_worth`

**Monthly spending**: `get_spending_summary period=this_month group_by=category` then `group_by=merchant` for detail

**Subscription audit**: `get_recurring type=subscriptions` — check `total_monthly_subscriptions`

**Transaction search**: `get_transactions search="merchant name"` or `category=FOOD_AND_DRINK min_amount:50`

**Plaid categories**: `FOOD_AND_DRINK`, `TRANSPORTATION`, `ENTERTAINMENT`, `RENT_AND_UTILITIES`, `GENERAL_MERCHANDISE`, `PERSONAL_CARE`, `TRAVEL`, `MEDICAL`, `EDUCATION`, `INCOME`, `TRANSFER_IN`, `TRANSFER_OUT`, `LOAN_PAYMENTS`, `BANK_FEES`

## Notes

- Amounts: positive = debits (spending), negative = credits (income)
- Dates: `YYYY-MM-DD` format, UTC
- Pagination: `limit` + `offset` on `get_transactions` and `list_annotations`
- Errors return `isError: true` — common: rate limit (wait + retry), subscription inactive (402), crypto not enabled
- Annotations are persistent and server-side — never store passwords, full account numbers, or secrets in annotation content
- Prefer `--output json` for machine-readable results
