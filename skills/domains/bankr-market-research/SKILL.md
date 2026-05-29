---
name: Bankr Dev - Market Research
description: This skill should be used when building market data displays, implementing price feeds, or adding technical analysis. Covers prices, market caps, technical analysis, sentiment, and trending tokens.
version: 1.0.0
---

# Market Research Capability

Query market data and analysis via natural language prompts.

## What You Can Do

| Operation | Example Prompt |
|-----------|----------------|
| Token price | `What's the price of ETH?` |
| Market data | `Show me BTC market data` |
| Market cap | `What's the market cap of SOL?` |
| 24h volume | `What's the 24h volume for ETH?` |
| Holder count | `How many holders does BNKR have?` |
| Technical analysis | `Do technical analysis on BTC` |
| RSI | `What's the RSI for ETH?` |
| Price action | `Analyze SOL price action` |
| Sentiment | `What's the sentiment on ETH?` |
| Social mentions | `Check social mentions for DOGE` |
| Price chart | `Show ETH price chart` |
| Chart with period | `Show BTC price chart for 30d` |
| Trending tokens | `What tokens are trending today?` |
| Top gainers | `Show top gainers today` |
| Top losers | `Show top losers today` |
| Trending by chain | `What's trending on Base?` |
| Compare tokens | `Compare ETH vs SOL` |

## Prompt Patterns

```
What's the price of {token}?
Show me {token} market data
Do technical analysis on {token}
What's the sentiment on {token}?
Show {token} price chart [for {period}]
What tokens are trending today?
Compare {token1} vs {token2}
```

**Chart periods:** 1d, 7d, 30d, 90d, 1y

**Supported chains:** All chains (data aggregated from multiple sources)

## Usage

```typescript
import { execute } from "./bankr-client";

// Price check
await execute("What's the price of ETH?");

// Technical analysis
await execute("Do technical analysis on BTC");

// Sentiment
await execute("What's the sentiment on SOL?");

// Trending
await execute("What tokens are trending today?");
```

## Related Skills

- `bankr-client-patterns` - Client setup and execute function
- `bankr-api-basics` - API fundamentals
- `bankr-token-trading` - Execute trades based on research
