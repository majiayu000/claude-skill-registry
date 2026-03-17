---
name: plaid
description: Query financial accounts, balances, transactions, and spending via Plaid. Connect bank accounts and retrieve real-time balance and transaction data. Use when the user asks about bank balances, credit card balances, recent transactions, spending habits, financial summaries, or wants to connect a new bank account.
metadata: {"openclaw":{"emoji":"💳","requires":{"bins":["node"],"env":["PLAID_CLIENT_ID","PLAID_SECRET"]},"primaryEnv":"PLAID_CLIENT_ID"}}
---

# Plaid — Financial Data Skill

Query connected bank accounts for balances, transactions, and spending insights via Plaid API.

## Environment Variables

Required:
- `PLAID_CLIENT_ID` — Plaid client ID
- `PLAID_SECRET` — Plaid secret key
- `PLAID_ENV` — `production`, `sandbox`, or `development`

Optional:
- `PLAID_TOKENS_PATH` — Override token storage path (default: `$OPENCLAW_WORKSPACE/state/plaid-tokens.json`)

Load from a `.env` file:
```bash
export $(grep -E '^PLAID_(CLIENT_ID|SECRET|ENV)=' /path/to/.env | xargs)
```

## Install Dependencies

```bash
cd {baseDir} && npm install
```

## First-Time Setup: Connect a Bank

```bash
node {baseDir}/scripts/server.js
```

Opens at `http://localhost:3456`. Connect multiple banks — server stays running. Tokens saved automatically.

## Query Balances

```bash
node {baseDir}/scripts/balances.js [--json]
```

## Query Transactions

```bash
node {baseDir}/scripts/transactions.js [options]
```

Options: `--days N` (default 30), `--search "query"`, `--category "food"`, `--account "checking"`, `--json`

## Financial Insights

```bash
node {baseDir}/scripts/insights.js [--days N] [--json]
```

Returns: cash flow summary, category breakdown, top merchants, recurring/subscription detection, card usage, credit utilization.

## Notes

- Plaid categorizes transactions automatically (FOOD_AND_DRINK, TRANSPORTATION, etc.)
- Charge cards (Amex Gold/Platinum) don't report credit limits — utilization only reflects revolving cards
- `transactionsSync` is used for efficiency — first call may be slower as Plaid builds the cursor
- Token storage is a JSON file in the agent workspace; back it up if needed
