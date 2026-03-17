---
name: ct-alpha
description: >
  Crypto Twitter intelligence and alpha research. Search X/Twitter for real-time crypto narratives,
  trending tokens, yield strategies, smart money signals, and protocol research. Features TweetRank
  (PageRank-inspired credibility scoring), multi-signal token detection, coordinated raid detection,
  and dynamic tool discovery for execution suggestions. Solana-first but covers all major chains.
creator: yashhsm
version: "1.0.0"
tags: [crypto-twitter, alpha, research, trending, tweetrank, solana, defi, sentiment, x-api, trading]
metadata:
  author: yashhsm
  runtime: bun
  api: X API v2 (pay-per-use)
---

# CT Alpha — Crypto Twitter Intelligence

Turn X/Twitter into an actionable crypto intelligence layer. Search CT for narratives, alpha, strategies, and sentiment, then rank results using TweetRank (a PageRank-inspired credibility scoring system), extract tokens/CAs from multiple signals, detect coordinated raids, and suggest execution steps using available tools.

## Overview

- **Search**: Query CT with crypto-optimized noise filters and relevancy sorting
- **TweetRank**: Score tweets by author credibility + engagement quality + recency
- **Multi-Signal Token Detection**: Cashtags, name-phrases, crypto URLs, contract addresses
- **Raid Detection**: Flag tickers promoted mostly by low-credibility accounts
- **Trending**: Detect trending tokens across multiple search queries
- **Watchlist**: Monitor trusted CT accounts by category
- **Thread Hydration**: Fetch full conversation threads
- **X Articles**: Full-text extraction of long-form posts (>280 chars)
- **Cost Tracking**: Per-session API spend tracking (~$0.005/tweet)
- **Dynamic Tool Discovery**: Suggest follow-up actions with DeFi Llama, Backpack, Polymarket, etc.

## Prerequisites

- **Runtime**: [Bun](https://bun.sh) (TypeScript runtime)
- **API Token**: X API Bearer Token from [developer.x.com](https://developer.x.com) (pay-per-use via xAI)
- **Cost**: ~$0.005 per tweet read, ~$0.10 per quick search (20 tweets)

## Quick Start

### Installation

```bash
# Clone the skill
git clone https://github.com/yashhsm/skills.git
cd skills/skills/ct-alpha

# Run the installer (configures token, watchlist, cache)
bun run install.ts
```

### Environment Setup

```bash
# Set your X API Bearer Token
export X_BEARER_TOKEN="your_token_here"

# Or save to persistent env file
mkdir -p ~/.config/env
echo 'export X_BEARER_TOKEN="your_token_here"' >> ~/.config/env/global.env
source ~/.config/env/global.env
```

### Basic Usage

```bash
# Search for alpha on a token
bun run ct-search.ts search "$SOL alpha" --quick

# Detect trending tokens
bun run ct-search.ts trending --window 6h --solana-only

# Monitor watchlist accounts
bun run ct-search.ts watchlist --since 24h

# Read a specific tweet or article
bun run ct-search.ts read https://x.com/user/status/123456

# Check API spending
bun run ct-search.ts cost
```

## CLI Reference

### search — Core research command

```bash
bun run ct-search.ts search "<query>" [flags]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--quick` | 20 tweets, 1hr cache, ~$0.10 | **Default mode** |
| `--full` | Up to 100 tweets, 15min cache, ~$0.50 | Confirm cost first |
| `--limit N` | Max total tweets | 20 (quick), 100 (full) |
| `--sort <field>` | `likes`, `recency`, `relevancy` | `relevancy` |
| `--since <duration>` | `1h`, `6h`, `24h`, `7d` | `24h` |
| `--min-likes N` | Engagement filter | 3 (quick) |
| `--from user1,user2` | Restrict to specific accounts | — |
| `--extract-tickers` | Show extracted tickers | — |
| `--extract-cas` | Show contract addresses and crypto URLs | — |
| `--raw` | JSON output | — |

### trending — Multi-signal trending detection

```bash
bun run ct-search.ts trending [flags]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--window <duration>` | `1h`, `6h`, `24h` | `6h` |
| `--min-mentions N` | Minimum mention count | 3 |
| `--solana-only` | Solana ecosystem only | — |
| `--top N` | Top N results | 20 |

### watchlist — Monitor CT accounts

```bash
bun run ct-search.ts watchlist [flags]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--category <cat>` | Filter by category | all |
| `--since <duration>` | Time window | `24h` |

### read — Read a specific tweet/article

```bash
bun run ct-search.ts read <tweet_url_or_id> [--thread] [--raw]
```

Accepts x.com URLs, twitter.com URLs, or raw tweet IDs. Articles (long-form posts) are fetched in full.

### thread — Hydrate conversation thread

```bash
bun run ct-search.ts thread <tweet_id>
```

### cost — Track API spending

```bash
bun run ct-search.ts cost [--reset]
```

## Core Features

### TweetRank Scoring

Every tweet is scored by three factors multiplied together:

1. **AuthorCred (0-10)**: Watchlist membership (+5), follower/following ratio (capped +5), verification (+1), account age (log scale, capped +2), bot penalty (-3)
2. **EngagementQuality**: Bookmarks (×3, unfakeable) > Quotes (×2.5, high effort) > Likes (×1.5) > Retweets (×1, easily botted). All log-scaled.
3. **RecencyBoost**: `1 / (1 + hoursAgo / 24)` — newer tweets score higher.

```
TweetRank = AuthorCred × EngagementQuality × RecencyBoost
```

Each tweet receives a source label:
- `[WATCHLIST]` — Author is on your watchlist (highest trust)
- `[HIGH-CRED]` — AuthorCred ≥ 5
- `[UNKNOWN]` — Unverified author
- `[SUSPICIOUS]` — Bot-like patterns detected

### Multi-Signal Token Detection

Cashtag-only detection misses how tokens actually spread on CT. This extracts from four signal types:

| Signal | Example | Confidence |
|--------|---------|------------|
| **Cashtag** | `$SOL`, `$JTO` | High |
| **Name-phrase** | "pendle" + crypto context | High/Medium |
| **Crypto URL** | pump.fun, dexscreener, birdeye, jup.ag | High |
| **Contract Address** | Base58 (Solana) / 0x (Ethereum) with context | High/Low |

Supported crypto URL domains: pump.fun, dexscreener.com, birdeye.so, jup.ag, raydium.io, solscan.io, etherscan.io.

### Raid Detection

Detects coordinated pump campaigns by analyzing author credibility distribution per ticker:

- If >70% of authors mentioning a ticker have low credibility (AuthorCred < 3), it's flagged as a potential raid
- Output includes raid score, total/low-cred author counts

### Noise Filtering

Every search auto-appends crypto noise filters:
- `-is:retweet` (removes retweets)
- `-"airdrop"`, `-"giveaway"`, `-"whitelist"` (spam removal)
- `-"follow and RT"`, `-"follow & RT"`, `-"free mint"`, `-"dm to claim"` (engagement bait)
- Quick mode also adds `-is:reply`

### Caching

Aggressive caching prevents redundant API calls:

| Cache Type | TTL | Use Case |
|------------|-----|----------|
| Quick search | 1 hour | Default searches |
| Full search | 15 minutes | Deep dives |
| Thread | 2 hours | Conversation threads |
| Profile | 24 hours | User lookups |
| Watchlist | 4 hours | Account monitoring |

Cache is file-based (JSON) with auto-pruning on startup (24h hard limit).

## Research Methodology

Follow this 6-step loop for every research request:

### 1. Decompose
Break the user's question into 1-3 targeted search queries.
- Token research: search both `$TICKER` and plain name with OR
- Narratives: search thematic keywords, not just token names
- Strategies: include strategy/yield/APY keywords

### 2. Pre-Filter
Before any API call:
- Check cache (same query within TTL is free)
- Noise filters are automatic
- Estimate cost: Quick ~$0.10, Full ~$0.50-1.50
- Narrow time window: 24h for trending, 7d for research

### 3. Search
Execute with `--quick` mode first (always):
```bash
bun run ct-search.ts search "$TOKEN alpha" --quick --extract-tickers
```

### 4. Extract
Analyze TweetRank scores and trust labels. Look for extracted tickers, contract addresses, and crypto URLs.

### 5. Deep-Dive (if needed)
- Follow high-engagement threads: `bun run ct-search.ts thread <id>`
- Search specific authors: `--from author1,author2`
- Broaden with `--full` only if quick was insufficient

### 6. Synthesize
Combine findings into actionable intelligence:
- Group by theme, not by query
- Highlight tickers with strong multi-signal detection
- Flag raid risks
- Suggest verification and execution steps

## Query String Rules

The query argument supports X API v2 operators:

| Operator | Example | Description |
|----------|---------|-------------|
| keyword | `solana alpha` | Both words |
| `"exact"` | `"yield strategy"` | Exact phrase |
| `OR` | `$SOL OR solana` | Either term |
| `-` | `-airdrop` | Exclude term |
| `from:` | `from:username` | Tweets by user |
| `has:links` | `has:links` | Tweets with URLs |
| `lang:` | `lang:en` | Language filter |
| `$` | `$SOL` | Cashtag |

**Do NOT use these v1.1 operators** (they cause 400 errors on v2 pay-per-use):
- `min_faves:N`, `min_retweets:N` — use `--min-likes` CLI flag instead
- `place:`, `bio:`, `sample:` — not available on v2

**Do NOT manually include noise filters** in the query — the CLI auto-appends them.

## Dynamic Tool Discovery

After completing research, suggest execution steps using available MCP tools:

| Tool Prefix | Use Case | Example |
|-------------|----------|---------|
| `mcp__defillama__*` | TVL, yields, fees, prices | `get_protocol_tvl("pendle")` |
| `mcp__backpack__*` | Exchange price, depth, trades | `backpack_get_ticker("SOL_USDC")` |
| `mcp__polymarket__*` | Prediction markets | `search_polymarket("solana ETF")` |
| `mcp__coingecko__*` | Token data, market charts | `get_id_coins("solana")` |

Always frame suggestions as "verify" not "confirm" — encourage skepticism about CT alpha.

## Cost Protocol

1. **Always `--quick` first** (~$0.10 for 20 tweets). Relevancy sort = best results come first.
2. Only increase `--limit` if 20 results are genuinely insufficient.
3. Display cost estimate before `--full` mode.
4. Cache is aggressive — same query within TTL is free.
5. **Two-pass strategy**: First search 20 results. If more depth needed on a sub-topic, do a targeted follow-up rather than re-running with higher limits.

## Best Practices

- **Start narrow, broaden only if needed**: Specific ticker + context words first
- **Use `--from` for signal**: Restrict to watchlist accounts for highest signal-to-noise
- **Use `has:links` for substance**: Analytical content, not hot takes
- **Never present CT findings as authoritative**: Always include confidence levels and risk bullets
- **Contract addresses are always UNVERIFIED**: Verify on-chain before interacting
- **Two-pass research**: Quick search first, then targeted deep-dives
- **Track spending**: Use `cost` command to monitor API usage

## Security Considerations

- X Bearer Token is stored in `~/.config/env/global.env` — ensure proper file permissions
- Never commit tokens to version control
- Contract addresses extracted from tweets are ALWAYS unverified — always verify on-chain
- Watchlist data is local-only (not synced or shared)
- Cache files contain tweet data — consider cleanup for sensitive research

## Skill Structure

```
ct-alpha/
├── SKILL.md                    # This file — agent instructions
├── ct-search.ts                # Main CLI entry point
├── setup.ts                    # Interactive setup script
├── install.ts                  # Full installer
├── lib/
│   ├── api.ts                  # X API v2 integration, pagination, caching
│   ├── extract.ts              # Multi-signal token extraction
│   ├── tweetrank.ts            # TweetRank scoring and raid detection
│   ├── format.ts               # Output formatting with trust labels
│   ├── cache.ts                # File-based caching layer
│   ├── cost.ts                 # API cost tracking
│   └── filters.ts              # Noise filtering, engagement filtering
├── resources/
│   ├── x-api.md                # X API v2 reference
│   ├── query-templates.md      # Pre-built search patterns
│   └── tool-discovery.md       # Dynamic tool suggestion map
├── data/
│   ├── known-tokens.json       # Token name → ticker mappings
│   └── watchlist.default.json  # Default watchlist categories
└── examples/
    └── basic-search.ts         # Quick start example
```

## Resources

- [X API v2 Documentation](https://developer.x.com/en/docs/twitter-api)
- [Bun Runtime](https://bun.sh)
- [SendAI Skills Repository](https://github.com/sendaifun/skills)
