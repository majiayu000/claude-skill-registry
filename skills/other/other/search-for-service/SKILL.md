---
name: search-for-service
description: Search and browse the x402 bazaar marketplace for paid API services. Use when you or the user want to find available services, see what's available, discover APIs, or need an external service to accomplish a task. Also use as a fallback when no other skill clearly matches — search the bazaar to see if a paid service exists. Covers "what can I do?", "find me an API for...", "what services are available?", "search for...", "browse the bazaar".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx awal@latest x402 bazaar *)", "Bash(npx awal@latest x402 details *)"]
---

# Searching the x402 Bazaar

Use the `npx awal@latest x402` commands to discover and inspect paid API endpoints available on the x402 bazaar marketplace. No authentication or balance is required for searching.

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
npx awal@latest x402 bazaar list [--network <network>] [--full] [--json]
```

| Option             | Description                             |
| ------------------ | --------------------------------------- |
| `--network <name>` | Filter by network (base, base-sepolia)  |
| `--full`           | Show complete details including schemas |
| `--json`           | Output as JSON                          |

### Discover Payment Requirements

Inspect an endpoint's x402 payment requirements without paying:

```bash
npx awal@latest x402 details <url> [--json]
```

Auto-detects the correct HTTP method (GET, POST, PUT, DELETE, PATCH) by trying each until it gets a 402 response, then displays price, accepted payment schemes, network, and input/output schemas.

## Examples

```bash
# Search for weather-related paid APIs
npx awal@latest x402 bazaar search "weather"

# Search with more results
npx awal@latest x402 bazaar search "sentiment analysis" -k 10

# Browse all bazaar resources with full details
npx awal@latest x402 bazaar list --full

# Check what an endpoint costs
npx awal@latest x402 details https://example.com/api/weather
```

## Prerequisites

- No authentication needed for search, list, or details commands

## Next Steps

Once you've found a service you want to use, use the `pay-for-service` skill to make a paid request to the endpoint.

## Error Handling

- "CDP API returned 429" - Rate limited; cached data will be used if available
- "No X402 payment requirements found" - URL may not be an x402 endpoint
