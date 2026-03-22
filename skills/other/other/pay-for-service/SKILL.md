---
name: pay-for-service
description: Make a paid API request to an x402 endpoint with automatic USDC payment. Use when you or the user want to call a paid API, make an x402 request, use a paid service, or pay for an API call. Use after finding a service with search-for-service.
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx awal@latest status*)", "Bash(npx awal@latest balance*)", "Bash(npx awal@latest x402 pay *)"]
---

# Making Paid x402 Requests

Use the `npx awal@latest x402 pay` command to call paid API endpoints with automatic USDC payment on Base.

## Confirm wallet is initialized and authed

```bash
npx awal@latest status
```

If the wallet is not authenticated, refer to the `authenticate-wallet` skill.

## Command Syntax

```bash
npx awal@latest x402 pay <url> [-X <method>] [-d <json>] [-q <params>] [-h <json>] [--max-amount <n>] [--json]
```

## Options

| Option                  | Description                                        |
| ----------------------- | -------------------------------------------------- |
| `-X, --method <method>` | HTTP method (default: GET)                         |
| `-d, --data <json>`     | Request body as JSON string                        |
| `-q, --query <params>`  | Query parameters as JSON string                    |
| `-h, --headers <json>`  | Custom HTTP headers as JSON string                 |
| `--max-amount <amount>` | Max payment in USDC atomic units (1000000 = $1.00) |
| `--correlation-id <id>` | Group related operations                           |
| `--json`                | Output as JSON                                     |

## USDC Amounts

X402 uses USDC atomic units (6 decimals):

| Atomic Units | USD   |
| ------------ | ----- |
| 1000000      | $1.00 |
| 100000       | $0.10 |
| 50000        | $0.05 |
| 10000        | $0.01 |

**IMPORTANT**: Always single-quote amounts that use `$` to prevent bash variable expansion (e.g. `'$1.00'` not `$1.00`).

## Examples

```bash
# Make a GET request (auto-pays)
npx awal@latest x402 pay https://example.com/api/weather

# Make a POST request with body
npx awal@latest x402 pay https://example.com/api/sentiment -X POST -d '{"text": "I love this product"}'

# Limit max payment to $0.10
npx awal@latest x402 pay https://example.com/api/data --max-amount 100000
```

## Prerequisites

- Must be authenticated (`npx awal@latest status` to check, see `authenticate-wallet` skill)
- Wallet must have sufficient USDC balance (`npx awal@latest balance` to check)
- If you don't know the endpoint URL, use the `search-for-service` skill to find services first

## Error Handling

- "Not authenticated" - Run `awal auth login <email>` first, or see `authenticate-wallet` skill
- "No X402 payment requirements found" - URL may not be an x402 endpoint; use `search-for-service` to find valid endpoints
- "Insufficient balance" - Fund wallet with USDC; see `fund` skill
