---
name: parallel-ai
description: 'Parallel AI Search & Extract API for FX news research. Use when working with web search, news extraction, content research, or FX market data gathering. Triggers on: "parallel ai", "parallel search", "web search API", "FX news", "news research", "parallel-web", "extract API".'
---

## Overview

Parallel AI provides search and extraction APIs for gathering FX news and market research data. Used in AutoClaw for automated research about currency markets relevant to Mento stablecoins.

## Installation

```bash
pnpm add parallel-web
```

## Search API

```ts
import { Parallel } from 'parallel-web';

const parallel = new Parallel({
  apiKey: process.env.PARALLEL_API_KEY!,
});

// Search for FX news
const results = await parallel.search({
  query: 'EUR/USD exchange rate forecast',
  maxResults: 10,
});

for (const result of results) {
  console.log(result.title, result.url, result.snippet);
}
```

## Extract API

Extract structured content from web pages:

```ts
const extracted = await parallel.extract({
  url: 'https://example.com/fx-article',
});

console.log(extracted.title);
console.log(extracted.content); // Clean markdown text
console.log(extracted.publishedAt);
```

## Use Cases in AutoClaw

- **FX Rate Research**: Search for current exchange rate news for Mento stablecoin pairs
- **Market Sentiment**: Gather news sentiment about currencies (KES, NGN, BRL, PHP, etc.)
- **Economic Events**: Track central bank decisions affecting Mento stablecoin values
- **Price Verification**: Cross-reference on-chain Mento rates with real-world FX rates

## Environment Variables

| Variable | Description |
|---|---|
| `PARALLEL_API_KEY` | Parallel AI API key |

## Important Notes

- Rate-limit your requests to avoid hitting API quotas
- Cache search results when possible (FX news doesn't change every second)
- Always attribute sources when displaying search results to users
- The Extract API returns clean markdown — suitable for feeding to LLMs for summarization
