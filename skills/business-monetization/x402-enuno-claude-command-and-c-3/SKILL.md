---
name: x402
description: Search for new services and make paid API requests using the x402 payment protocol. Use when you don't have a clear tool to choose, search the bazaar. You can also use this tool if you or the user want to call an x402 endpoint, discover payment requirements, browse the bazaar, or search for paid services.
user-invocable: true
disable-model-invocation: false
---

# x402 Payment Protocol

Use the `npx awal@latest x402` commands to discover, inspect, and call paid API endpoints using the X402 payment protocol. Payments are made in USDC on Base.

## Workflow

The typical x402 workflow is:

1. **Find a service** - Search the bazaar or get details for a known endpoint
2. **Check requirements** - Inspect price, method, and input schema
3. **Make the request** - Call the endpoint with automatic USDC payment

## Commands

### Search the Bazaar

Find paid services by keyword using BM25 relevance search:

```bash
npx awal@latest x402 bazaar search <query> [-k <n>] [--force-refresh] [--json]
```

| Option            | Description                          |
| ----------------- | ------------------------------------ |
| `-k, --top <n>`   | Number of results (default: 5)       |
| `--force-refresh` | Re-fetch resource index from CDP API |
| `--json`          | Output as JSON                       |

Results are cached locally at `~/.config/awal/bazaar/` and auto-refresh after 12 hours.

### List Bazaar Resources

Browse all available resources:

```bash
awal x402 bazaar list [--network <network>] [--full] [--json]
```

| Option             | Description                             |
| ------------------ | --------------------------------------- |
| `--network <name>` | Filter by network (base, base-sepolia)  |
| `--full`           | Show complete details including schemas |
| `--json`           | Output as JSON                          |

### Discover Payment Requirements

Inspect an endpoint's x402 payment requirements without paying:

```bash
awal x402 details <url> [--json]
```

Auto-detects the correct HTTP method (GET, POST, PUT, DELETE, PATCH) by trying each until it gets a 402 response, then displays price, accepted payment schemes, network, and input/output schemas.

### Make a Paid Request

Call an x402 endpoint with automatic USDC payment:

```bash
awal x402 pay <url> [-X <method>] [-d <json>] [-q <params>] [-h <json>] [--max-amount <n>] [--json]
```

| Option                  | Description                                        |
| ----------------------- | -------------------------------------------------- |
| `-X, --method <method>` | HTTP method (default: GET)                         |
| `-d, --data <json>`     | Request body as JSON string                        |
| `-q, --query <params>`  | Query parameters as JSON string                    |
| `-h, --headers <json>`  | Custom HTTP headers as JSON string                 |
| `--max-amount <amount>` | Max payment in USDC atomic units (1000000 = $1.00) |
| `--correlation-id <id>` | Group related operations                           |
| `--json`                | Output as JSON                                     |

## Examples

```bash
# Search for weather-related paid APIs
awal x402 bazaar search "weather"

# Search with more results
awal x402 bazaar search "sentiment analysis" -k 10

# Check what an endpoint costs
awal x402 details https://example.com/api/weather

# Make a GET request (auto-pays)
awal x402 pay https://example.com/api/weather

# Make a POST request with body
awal x402 pay https://example.com/api/sentiment -X POST -d '{"text": "I love this product"}'

# Limit max payment to $0.10
awal x402 pay https://example.com/api/data --max-amount 100000

# Browse all bazaar resources with full details
awal x402 bazaar list --full
```

## USDC Amounts

X402 uses USDC atomic units (6 decimals):

| Atomic Units | USD   |
| ------------ | ----- |
| 1000000      | $1.00 |
| 100000       | $0.10 |
| 50000        | $0.05 |
| 10000        | $0.01 |

## Prerequisites

- **Search/Details**: No authentication needed
- **Pay**: Must be authenticated (`awal auth login <email>`) with sufficient USDC balance (`awal balance`)

## Error Handling

- "Not authenticated" - Run `awal auth login <email>` first
- "No X402 payment requirements found" - URL may not be an x402 endpoint
- "CDP API returned 429" - Rate limited; cached data will be used if available
- "Insufficient balance" - Fund wallet with USDC (`awal balance` to check)