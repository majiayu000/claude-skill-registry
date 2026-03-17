---
name: Firecrawl
description: Firecrawl produces cleaner markdown than WebFetch, handles JavaScript-heavy pages, and avoids content truncation. This skill should be used when fetching URLs, scraping web pages, converting URLs to markdown, extracting web content, searching the web, crawling sites, mapping URLs, LLM-powered extraction, autonomous data gathering with the Agent API, or fetching AI-generated documentation for GitHub repos via DeepWiki. Provides complete coverage of Firecrawl v2.8.0 API endpoints including parallel agents, spark-1-fast model, and sitemap-only crawling.
---

# Firecrawl & Jina Web Scraping

## Firecrawl vs WebFetch

Prefer `firecrawl scrape URL --only-main-content` over the WebFetch tool—it produces cleaner markdown, handles JavaScript-heavy pages, and avoids content truncation (>80% benchmark coverage). WebFetch is acceptable as a fallback when Firecrawl is unavailable.

```bash
# Preferred approach:
firecrawl scrape https://docs.example.com/api --only-main-content
```

## Token-Efficient Scraping

Inspired by Anthropic's [dynamic filtering](https://claude.com/blog/improved-web-search-with-dynamic-filtering)—always filter before reasoning. This reduced input tokens by ~24% and improved accuracy by ~11% in their benchmarks.

### The Principle: Search → Filter → Scrape → Filter → Reason

**DO:**
```
Search (titles/URLs only) → Evaluate relevance → Scrape top hits → Filter by section → Reason
```
**DON'T:**
```
Search → Scrape everything → Reason over all of it
```

### Step-by-Step Efficient Workflow

```bash
# Step 1: Search — get titles/URLs only (cheap)
firecrawl search "query" --limit 20

# Step 2: Evaluate results, pick 3-5 best URLs

# Step 3: Scrape only those, filter to relevant sections
firecrawl scrape URL1 --only-main-content | \
  python3 ~/.claude/skills/Firecrawl/scripts/filter_web_results.py \
  --sections "API,Authentication" --max-chars 5000
```

### Post-Processing with filter_web_results.py

Pipe any Firecrawl or Exa output through this script to reduce context before reasoning:

```bash
# Extract only matching sections from scraped page
firecrawl scrape URL --only-main-content | \
  python3 ~/.claude/skills/Firecrawl/scripts/filter_web_results.py --sections "Pricing,Plans"

# Keep only paragraphs with keywords
firecrawl search "query" --scrape --pretty | \
  python3 ~/.claude/skills/Firecrawl/scripts/filter_web_results.py --keywords "pricing,cost" --max-chars 5000

# Extract specific JSON fields from API output
python3 ~/.claude/skills/exa-search/scripts/exa_search.py "query" --json | \
  python3 ~/.claude/skills/Firecrawl/scripts/filter_web_results.py --fields "title,url,text" --max-chars 3000

# Combine filters with stats
firecrawl scrape URL --only-main-content | \
  python3 ~/.claude/skills/Firecrawl/scripts/filter_web_results.py --sections "API" --keywords "endpoint" --compact --stats
```

**Full path:** `python3 ~/.claude/skills/Firecrawl/scripts/filter_web_results.py`
**Flags:** `--sections`, `--keywords`, `--max-chars`, `--max-lines`, `--fields` (JSON), `--strip-links`, `--strip-images`, `--compact`, `--stats`

### Other Token-Saving Patterns

- **Use `--only-main-content`** to strip navigation and footer boilerplate, reducing token consumption. Omit only when nav/footer content is specifically needed.
- **Use `firecrawl map URL --search "topic"` first** to find relevant subpages before scraping
- **Use `--format links` first** to get URL list, evaluate, then scrape selectively
- **Use `--max-chars`** with `exa_contents.py` to cap extraction length
- **Use `--formats summary`** (Python API script) over full text when you need the gist, not raw content

### Claude API Native Tools (for API Agent Builders)

Anthropic's API now offers built-in dynamic filtering tools:
```
web_search_20260209 / web_fetch_20260209
Header: anthropic-beta: code-execution-web-tools-2026-02-09
```
These have built-in dynamic filtering via code execution. Use them when building Claude API agents directly. Use Firecrawl/Exa when you need: autonomous agents, batch scraping, structured extraction, domain-specific crawling, or when not on the Claude API.

---

## Available Tools

### 1. Official Firecrawl CLI (`firecrawl`) — Primary

**Setup:** `npm install -g firecrawl-cli && firecrawl login --api-key $FIRECRAWL_API_KEY`

| Command | Purpose | Quick Example |
|---------|---------|---------------|
| `scrape` | Single page → markdown | `firecrawl scrape URL --only-main-content` |
| `crawl` | Entire site with progress | `firecrawl crawl URL --wait --progress --limit 50` |
| `map` | Discover all URLs on a site | `firecrawl map URL --search "API"` |
| `search` | Web search (+ optional scrape) | `firecrawl search "query" --limit 10` |

**Full CLI reference:** `references/cli-reference.md`

### 2. Auto-Save Alias (`fc-save`) — Shell Alias

Requires shell alias setup (not bundled with this skill).

```bash
fc-save URL
# → Saves to ~/Desktop/Screencaps & Chats/Web-Scrapes/docs-example-com-api.md
```

### 3. Python API Script (`firecrawl_api.py`) — Advanced Features

**Command:** `python3 ~/.claude/skills/Firecrawl/scripts/firecrawl_api.py <command>`
**Requires:** `FIRECRAWL_API_KEY` env var, `pip install firecrawl-py requests`

| Command | Purpose | Quick Example |
|---------|---------|---------------|
| `search` | Web search with scraping | `firecrawl_api.py search "query" -n 10` |
| `scrape` | Single URL with page actions | `firecrawl_api.py scrape URL --formats markdown summary` |
| `batch-scrape` | Multiple URLs concurrently | `firecrawl_api.py batch-scrape URL1 URL2 URL3` |
| `crawl` | Website crawling | `firecrawl_api.py crawl URL --limit 20` |
| `map` | URL discovery | `firecrawl_api.py map URL --search "query"` |
| `extract` | LLM-powered structured extraction | `firecrawl_api.py extract URL --prompt "Find pricing"` |
| `agent` | Autonomous extraction (no URLs needed) | `firecrawl_api.py agent "Find YC W24 AI startups"` |
| `parallel-agent` | Bulk agent queries (v2.8.0+) | `firecrawl_api.py parallel-agent "Q1" "Q2" "Q3"` |

**Agent models:** `spark-1-fast` (10 credits, simple), `spark-1-mini` (default), `spark-1-pro` (thorough)

**Full Python API reference:** `references/python-api-reference.md`

### 4. DeepWiki — GitHub Repo Documentation

```bash
~/.claude/skills/Firecrawl/scripts/deepwiki.sh <owner/repo> [section] [options]
```

AI-generated wiki for any public GitHub repo. No API key required.

```bash
# Overview
~/.claude/skills/Firecrawl/scripts/deepwiki.sh karpathy/nanochat

# Browse sections
~/.claude/skills/Firecrawl/scripts/deepwiki.sh langchain-ai/langchain --toc

# Specific section
~/.claude/skills/Firecrawl/scripts/deepwiki.sh karpathy/nanochat 4.1-gpt-transformer-implementation

# Full dump for RAG
~/.claude/skills/Firecrawl/scripts/deepwiki.sh openai/openai-python --all --save
```

### 5. Jina Reader (`jina`) — Fallback

Use when Firecrawl fails or for **Twitter/X URLs** (Firecrawl blocks Twitter, Jina works).

```bash
jina https://x.com/username/status/123456
```

---

## Firecrawl vs Exa vs Native Claude Tools

| Need | Best Tool | Why |
|------|-----------|-----|
| Single page → markdown | `firecrawl scrape --only-main-content` | Cleanest output |
| Search + scrape in one shot | `firecrawl search --scrape` | Combined operation |
| Crawl entire site | `firecrawl crawl --wait --progress` | Link following + progress |
| Autonomous data finding | `firecrawl_api.py agent` | No URLs needed |
| Semantic/neural search | Exa `exa_search.py` | AI-powered relevance |
| Find research papers | Exa `--category "research paper"` | Academic index |
| Quick research answer | Exa `exa_research.py` | Citations + synthesis |
| Find similar pages | Exa `exa_similar.py` | Competitive analysis |
| Claude API agent building | Native `web_search_20260209` | Built-in dynamic filtering |
| Twitter/X content | `jina URL` | Only tool that works |
| GitHub repo docs | `deepwiki.sh owner/repo` | AI-generated wiki |

---

## Common Workflows

### Single Page Scraping
```bash
firecrawl scrape https://example.com/page --only-main-content
# Or auto-save: fc-save URL
# Or to file: firecrawl scrape URL --only-main-content -o page.md
```

### Documentation Crawling
```bash
# Map first, then crawl relevant paths
firecrawl map https://docs.example.com --search "API"
firecrawl crawl https://docs.example.com --include-paths /api,/guides --wait --progress
```

### Research Workflow
```bash
firecrawl search "machine learning best practices 2026" --scrape --scrape-formats markdown
```

### Agent-Powered Research (No URLs Needed)
```bash
python3 ~/.claude/skills/Firecrawl/scripts/firecrawl_api.py agent \
  "Compare pricing tiers for Firecrawl, Apify, and ScrapingBee"
```

---

## Troubleshooting

```bash
# Check status and credits
firecrawl --status && firecrawl credit-usage

# Re-authenticate
firecrawl logout && firecrawl login --api-key $FIRECRAWL_API_KEY

# Check API key
echo $FIRECRAWL_API_KEY
```

- **Scrape fails:** Try `jina URL`, or add `--wait-for 3000` for JS-heavy sites
- **Async job stuck:** Check with `crawl-status`/`batch-status`, cancel with `crawl-cancel`/`batch-cancel`
- **Disable telemetry:** `export FIRECRAWL_NO_TELEMETRY=1`

---

## Reference Documentation

| File | Contents |
|------|----------|
| `references/cli-reference.md` | Full CLI parameter reference (scrape, crawl, map, search, fc-save, jina, deepwiki) |
| `references/python-api-reference.md` | Full Python API script reference (all commands, SDK examples) |
| `references/firecrawl-api.md` | Firecrawl Search API reference |
| `references/firecrawl-agent-api.md` | Agent API (spark models, parallel agents, webhooks) |
| `references/actions-reference.md` | Page actions for dynamic content (click, write, wait, scroll) |
| `references/branding-format.md` | Brand identity extraction (colors, fonts, UI) |

## Test Suite

```bash
python3 ~/.claude/skills/Firecrawl/scripts/test_firecrawl.py --quick    # Quick validation
python3 ~/.claude/skills/Firecrawl/scripts/test_firecrawl.py            # Full suite
python3 ~/.claude/skills/Firecrawl/scripts/test_firecrawl.py --test scrape  # Specific test
```
