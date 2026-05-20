---
name: omnisearch
description: Unified web and social media search across 5 providers (Brave, Tavily, Xpoz, Exa, Firecrawl). Auto-routes queries to the best API, supports parallel multi-provider search with deduplication, AI-generated answers, and social media search. Triggers on web search, find news, search Twitter, search Reddit, social media search, multi-provider search, omnisearch, research news, OSINT, search for, look up, find information about.
---

# Omnisearch Skill

Unified search across 5 providers — Brave (Google SERP), Tavily (agent-native answers), Xpoz (social media), Exa (neural/semantic), and Firecrawl (scraping). Auto-classifies queries and routes to the best provider, or runs parallel searches across all with deduplication.

**Prerequisites:** At least one API key set. See [API Key Setup](#api-key-setup).

## Coverage Map

| Surface | Provider | Strength | Cost |
|---------|----------|----------|------|
| Google SERP | Brave | Web + news, freshness filtering, LLM Context API | $5/1k |
| Agent answers | Tavily | AI-synthesized answers with citations, content extraction | Free 1k/mo |
| Twitter/X | Xpoz | Tweet search, user timelines, threads, hashtags | Free 100k/mo |
| Reddit | Xpoz | Post search, subreddit browsing, trending | Free 100k/mo |
| Instagram | Xpoz | Post search, user profiles | Free 100k/mo |
| Neural/semantic | Exa (cross-skill) | Research papers, companies, similar pages | Per-query |
| Web scraping | Firecrawl (cross-skill) | Search + scrape, site crawling | Per-page |

## Token-Efficient Multi-Search

Same principle as Exa's dynamic filtering — search cheaply, filter, then extract selectively.

**DO:**
```bash
# Step 1: Multi-provider search, titles/URLs only
python3 ~/.claude/skills/omnisearch/scripts/omnisearch.py "query" --parallel --no-text

# Step 2: Evaluate titles, pick best URLs

# Step 3: Extract selected URLs
python3 ~/.claude/skills/exa-search/scripts/exa_contents.py URL1 URL2 --highlights --max-chars 3000
# OR
python3 ~/.claude/skills/firecrawl/scripts/firecrawl_api.py scrape URL --only-main-content
```

**DON'T:** Run `--parallel` with full text for 40+ results, then reason over all of it.

## Available Scripts

### 1. omnisearch.py — Meta-Router (start here)

Auto-classifies queries and dispatches to the best provider. Supports forced provider, parallel search, and social mode.

```bash
python3 ~/.claude/skills/omnisearch/scripts/omnisearch.py "query" [options]
```

| Quick Example | Purpose |
|---------------|---------|
| `... omnisearch.py "Iran oil sanctions"` | Auto-route to best provider |
| `... omnisearch.py "query" --provider brave` | Force specific provider |
| `... omnisearch.py "query" --parallel` | All web providers, merged + deduped |
| `... omnisearch.py "query" --social` | Twitter search via Xpoz |
| `... omnisearch.py "query" --social --platform reddit` | Reddit search |
| `... omnisearch.py "query" --answer` | AI-generated answer (Tavily/Brave) |
| `... omnisearch.py "query" --news --parallel` | News from all providers |
| `... omnisearch.py "query" --academic` | Route to Exa academic index |
| `... omnisearch.py "query" --verbose` | Show routing decisions on stderr |

**Query Classification (auto-route):**

| Signal | Category | Primary Provider |
|--------|----------|-----------------|
| @mentions, #hashtags, "tweet", "reddit", r/xxx | Social Media | Xpoz |
| "latest", "breaking", "today", date words | News | Brave |
| "paper", "arxiv", "study", "journal" | Academic | Exa |
| "who is", "what is", short questions | Factual Quick | Tavily (with answer) |
| "company", "startup", "funding", "IPO" | Company Research | Exa |
| "documentation", "API", "tutorial", "SDK" | Technical Docs | Exa |
| (default) | General Web | Brave |

### 2. brave_search.py — Brave Web & News Search

Google-indexed SERP with freshness filtering, country targeting, and LLM Context API.

```bash
python3 ~/.claude/skills/omnisearch/scripts/brave_search.py "query" [options]
```

| Quick Example | Purpose |
|---------------|---------|
| `... brave_search.py "Iran infrastructure"` | Web search |
| `... brave_search.py "query" --news` | Dedicated news endpoint |
| `... brave_search.py "query" --summarize` | LLM Context API (AI summary) |
| `... brave_search.py "query" --freshness pd` | Past day only |
| `... brave_search.py "query" --freshness pw --extra-snippets` | Past week + rich context |
| `... brave_search.py "query" --country US --lang en` | Localized results |
| `... brave_search.py "query" --filter web,news --markdown` | Multi-type + markdown |

**Freshness values:** `pd` (past day), `pw` (past week), `pm` (past month), `py` (past year), or `YYYY-MM-DDtoYYYY-MM-DD`

### 3. tavily_search.py — Agent-Native Search with Answers

AI-optimized search with grounded answers, topic modes, and content extraction.

```bash
python3 ~/.claude/skills/omnisearch/scripts/tavily_search.py "query" [options]
```

| Quick Example | Purpose |
|---------------|---------|
| `... tavily_search.py "oil prices" --answer` | Search + AI answer |
| `... tavily_search.py "query" --advanced --answer` | Deep search + answer |
| `... tavily_search.py "query" --news --days 3` | News, last 3 days |
| `... tavily_search.py "query" --finance` | Finance topic mode |
| `... tavily_search.py "query" --answer-only` | Pipe-friendly answer |
| `... tavily_search.py "query" --domains bellingcat.com` | Domain-restricted |
| `... tavily_search.py extract URL [URL...]` | Content extraction |

**Search depths:** `basic` (fast, ~1s) or `--advanced` (comprehensive, ~3-5s)
**Topics:** `general` (default), `--news`, `--finance`

### 4. xpoz_search.py — Social Media Search

Twitter/X, Reddit, and Instagram search via Xpoz SDK. 12 subcommands.

```bash
python3 ~/.claude/skills/omnisearch/scripts/xpoz_search.py SUBCOMMAND "query" [options]
```

| Quick Example | Purpose |
|---------------|---------|
| `... xpoz_search.py twitter "Iran conflict" -n 10` | Twitter search |
| `... xpoz_search.py twitter "query" --sort latest --min-likes 10` | Filtered tweets |
| `... xpoz_search.py twitter-user elikishtaini -n 10` | User timeline |
| `... xpoz_search.py twitter-thread 1234567890` | Full thread |
| `... xpoz_search.py twitter-hashtag IranStrikes -n 10` | Hashtag search |
| `... xpoz_search.py reddit "geopolitics Iran" -n 10` | Reddit search |
| `... xpoz_search.py reddit-sub worldnews -n 10 --sort hot` | Subreddit posts |
| `... xpoz_search.py reddit-post abc123` | Reddit post + comments |
| `... xpoz_search.py reddit-trending` | Trending subreddits |
| `... xpoz_search.py instagram "conflict" -n 10` | Instagram search |

**Twitter filters:** `--sort` (latest/popular/media), `--min-likes`, `--min-retweets`, `--since`/`--until`, `--lang`
**Reddit filters:** `--subreddit`, `--sort` (hot/new/top/rising), `--time` (hour/day/week/month/year/all)

## Provider Selection Guide

| Task | Best Approach |
|------|--------------|
| General web search | `omnisearch.py "query"` (auto-routes to Brave) |
| Breaking news | `omnisearch.py "query" --news` or `brave_search.py "query" --news --freshness pd` |
| Quick factual answer | `omnisearch.py "query" --answer` or `tavily_search.py "query" --answer` |
| Twitter OSINT | `omnisearch.py "query" --social` or `xpoz_search.py twitter "query"` |
| Reddit sentiment | `xpoz_search.py reddit "query"` or `omnisearch.py "query" --social --platform reddit` |
| Research papers | `omnisearch.py "query" --academic` (routes to Exa) |
| Company intelligence | `omnisearch.py "query"` (auto-detects company signals) |
| Multi-source corroboration | `omnisearch.py "query" --parallel --verbose` |
| Content extraction | `tavily_search.py extract URL` or Firecrawl |
| Domain-restricted search | `tavily_search.py "query" --domains site.com` or `brave_search.py "query" --goggles ID` |

## Omnisearch vs Exa vs Firecrawl

| Need | Best Tool | Why |
|------|-----------|-----|
| Google SERP surface | **Omnisearch** (Brave) | Exa has independent index |
| Social media search | **Omnisearch** (Xpoz) | Only tool with Twitter/Reddit |
| AI answer with citations | **Omnisearch** (Tavily) | Agent-native answers |
| Multi-provider parallel | **Omnisearch** `--parallel` | Dedup across providers |
| Semantic/neural search | **Exa** directly | Superior relevance ranking |
| Research papers | **Exa** `--category "research paper"` | Academic index |
| Find similar pages | **Exa** `exa_similar.py` | Semantic similarity |
| Single page scrape | **Firecrawl** `scrape` | Cleanest markdown |
| Full site crawl | **Firecrawl** `crawl` | Link following |
| News freshness filter | **Omnisearch** (Brave `--freshness`) | Hour/day/week/month |
| Content extraction | **Tavily** `extract` or **Firecrawl** | Both work |

## Common Workflows

### OSINT Research (WWW-style)
```bash
# Step 1: Multi-provider news sweep
python3 ~/.claude/skills/omnisearch/scripts/omnisearch.py "Iran infrastructure strike" --news --parallel --no-text

# Step 2: Social signal check
python3 ~/.claude/skills/omnisearch/scripts/xpoz_search.py twitter "Iran infrastructure" --sort latest -n 15

# Step 3: Extract best sources
python3 ~/.claude/skills/exa-search/scripts/exa_contents.py URL1 URL2 --highlights --max-chars 5000
```

### Quick Answer Pipeline
```bash
# AI answer with sources
python3 ~/.claude/skills/omnisearch/scripts/omnisearch.py "who commands CENTCOM" --answer --json | jq '.answer'
```

### Cross-Platform Corroboration
```bash
# Get the same story from 3+ sources
python3 ~/.claude/skills/omnisearch/scripts/omnisearch.py "Strait of Hormuz incident" --parallel --verbose
```

### Social Media Monitoring
```bash
# Track a developing story on Twitter
python3 ~/.claude/skills/omnisearch/scripts/xpoz_search.py twitter "#IranStrikes" --sort latest -n 20

# Check analyst activity
python3 ~/.claude/skills/omnisearch/scripts/xpoz_search.py twitter-user elikishtaini -n 10 --json
```

## API Key Setup

Three new keys in `~/.config/env/secrets.env`:

```bash
export BRAVE_API_KEY="..."      # https://api-dashboard.search.brave.com
export TAVILY_API_KEY="tvly-..."  # https://tavily.com (free tier, no CC)
export XPOZ_API_KEY="..."       # https://www.xpoz.ai
```

Existing keys (already configured for cross-skill routing):
```bash
export EXA_API_KEY="..."        # https://dashboard.exa.ai
export FIRECRAWL_API_KEY="..."  # https://firecrawl.dev
```

All scripts gracefully error with a clear message when their key is missing. You can use any subset.

## Reference Documentation

| File | Contents |
|------|----------|
| `references/brave-api-reference.md` | Brave Search API: endpoints, parameters, response schemas, LLM Context API |
| `references/tavily-api-reference.md` | Tavily API: search, extract, answer, topics, domains |
| `references/xpoz-api-reference.md` | Xpoz API: SDK methods, Twitter/Reddit/Instagram endpoints |

## Test Suite

```bash
python3 ~/.claude/skills/omnisearch/scripts/test_omnisearch.py --quick     # Offline + one per key
python3 ~/.claude/skills/omnisearch/scripts/test_omnisearch.py             # Full suite
python3 ~/.claude/skills/omnisearch/scripts/test_omnisearch.py --group router   # Classification tests
python3 ~/.claude/skills/omnisearch/scripts/test_omnisearch.py --group dedup    # Dedup tests
python3 ~/.claude/skills/omnisearch/scripts/test_omnisearch.py --verbose   # Detailed output
```

| Group | Tests | Live API? |
|-------|-------|-----------|
| `router` | classify_query (7 categories), select_providers (5 scenarios), routing_table_coverage | No |
| `dedup` | exact URL, normalized URL, title Jaccard, short titles, score sorting, mixed providers, URL normalize, Jaccard math | No |
| `format` | human-readable, markdown, JSON serialization, no-text mode | No |
| `brave` | web search, news, freshness, formatters | Yes |
| `tavily` | basic, advanced, answer, extract | Yes |
| `xpoz` | twitter search, reddit, user tweets | Yes |
| `integration` | auto-route, parallel, cross-skill exa, JSON CLI output | Yes |
