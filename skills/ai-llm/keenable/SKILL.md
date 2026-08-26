---
name: keenable
description: "Search the web and fetch page contents with Keenable AI — web search, page extraction, point-in-time queries, prompt-driven content extraction. Use when searching the web for current information, fetching webpage contents, extracting specific data from URLs, or researching topics with citations. Triggers on: web search, search the web, fetch page, read URL, find pages about, current information, Keenable, keen search, research with sources, look up, latest news, find information, check online, what is, who is."
---

# Keenable Search Skill

Web search and page fetch via Keenable AI — purpose-built for AI agents. Two scripts cover all use cases: search the web, fetch/extract page contents.

**Prerequisite:** `KEENABLE_API_KEY` environment variable. Get key at https://app.keenable.ai

## When to Use Keenable

- **Default web search** — 100K free requests/month, generous rate limits
- **Point-in-time search** — query the index as it existed at a past date (`--query-time`)
- **Prompt-driven extraction** — fetch a URL and have the API extract exactly what you need (`--prompt`)
- **High-volume research** — 100x the free tier of Exa (100K vs 1K/month)

## Token-Efficient Research

Search cheaply, pick the best results, extract selectively — reduces context by filtering before reasoning.

```bash
# Step 1: Search with short snippets to scan titles/descriptions
python3 ~/.claude/skills/keenable/scripts/keenable_search.py "query" --count 10 --snippet-length 200

# Step 2: Pick the 2-3 most relevant URLs from results

# Step 3: Extract only what you need from those URLs
python3 ~/.claude/skills/keenable/scripts/keenable_fetch.py URL --prompt "Extract the key findings"
```

## Available Scripts

### 1. keenable_search.py — Web Search

```bash
python3 ~/.claude/skills/keenable/scripts/keenable_search.py "query" [options]
```

| Quick Example | Purpose |
|---------------|---------|
| `... keenable_search.py "AI agents 2026"` | Basic search |
| `... keenable_search.py "Claude Code" --site docs.anthropic.com` | Site-restricted |
| `... keenable_search.py "transformer paper" --count 20` | More results |
| `... keenable_search.py "election results" --published-after 7d` | Recent only |
| `... keenable_search.py "AI safety" --query-time 2026-01-01` | Historical index |
| `... keenable_search.py "LLM benchmarks" --snippet-length 5000` | Longer snippets |

**Key options:**
- `--site DOMAIN` — restrict to a specific domain
- `--count N` — number of results (1-50, default 10)
- `--snippet-length N` — snippet max chars (180-10000)
- `--published-after DATE` — filter by publish date (absolute or relative: `7d`, `30min`, `2h`)
- `--published-before DATE` — upper bound on publish date
- `--query-time DATETIME` — search the index as it stood at this point in time
- `--json` — raw JSON output (default: formatted table)

### 2. keenable_fetch.py — Page Fetch & Extraction

```bash
python3 ~/.claude/skills/keenable/scripts/keenable_fetch.py URL [options]
```

| Quick Example | Purpose |
|---------------|---------|
| `... keenable_fetch.py "https://example.com"` | Fetch as markdown |
| `... keenable_fetch.py URL --live` | Force live fetch (not cached) |
| `... keenable_fetch.py URL --prompt "List all pricing tiers"` | Extract specific info |
| `... keenable_fetch.py URL --max-chars 5000` | Bounded output |
| `... keenable_fetch.py URL --live --prompt "What is the main argument?"` | Live + extract |

**Key options:**
- `--live` — fetch live page instead of indexed/cached copy
- `--prompt TEXT` — LLM-driven extraction (API reads page, returns only what you asked for)
- `--max-chars N` — truncate output to N characters
- `--json` — raw JSON response

### 3. keenable_setup.py — Setup & Validation

```bash
python3 ~/.claude/skills/keenable/scripts/keenable_setup.py --validate        # Test API key
python3 ~/.claude/skills/keenable/scripts/keenable_setup.py --setup-mcp       # Add MCP server
```

## Script Selection Guide

| Task | Best Approach |
|------|---------------|
| General web search | `keenable_search.py "query"` |
| Search specific site | `keenable_search.py "query" --site domain.com` |
| Recent news/articles | `keenable_search.py "topic" --published-after 7d` |
| Historical search | `keenable_search.py "query" --query-time 2025-06-01` |
| Read a known URL | `keenable_fetch.py URL` |
| Extract specific data from URL | `keenable_fetch.py URL --prompt "extract X"` |
| Fresh content (bypass cache) | `keenable_fetch.py URL --live` |
| Bounded page read | `keenable_fetch.py URL --max-chars 3000` |

## Keenable vs Exa vs Firecrawl

| Need | Best Tool | Why |
|------|-----------|-----|
| General web search | **Keenable** | 100K free/mo, fast, reliable |
| Point-in-time search | **Keenable** | Only tool that supports historical index queries |
| Extract specific data from URL | **Keenable** `--prompt` | API-side LLM extraction, no post-processing |
| Semantic/neural search | **Exa** | AI-powered relevance ranking |
| Find similar pages | **Exa** `exa_similar.py` | Semantic similarity |
| Deep site crawling | **Firecrawl** | Link following, JS rendering |
| Search + scrape combined | **Firecrawl** `search --scrape` | One operation |
| High-volume usage | **Keenable** | 100K vs Exa 1K vs Firecrawl 500 |

## Common Workflows

### Search then Read

```bash
# Find relevant pages
python3 ~/.claude/skills/keenable/scripts/keenable_search.py "React Server Components" --count 5

# Read the most relevant result
python3 ~/.claude/skills/keenable/scripts/keenable_fetch.py "https://react.dev/blog/..." --max-chars 8000
```

### Extract Structured Data

```bash
python3 ~/.claude/skills/keenable/scripts/keenable_fetch.py "https://example.com/pricing" \
  --prompt "List all pricing tiers with name, price, and features as a markdown table"
```

### Research with Date Bounds

```bash
python3 ~/.claude/skills/keenable/scripts/keenable_search.py "AI regulation" \
  --published-after 2026-01-01 --published-before 2026-06-01 --count 20
```

## MCP Alternative

For native tool access without scripts, add Keenable as an MCP server:

```bash
claude mcp add keenable \
  --transport http https://api.keenable.ai/mcp \
  --scope user \
  --header "X-API-Key: $KEENABLE_API_KEY"
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `KEENABLE_API_KEY not set` | Export in `~/.config/env/secrets.env` or shell profile |
| `401 Unauthorized` | Check key starts with `keen_` and is valid |
| `429 Rate Limited` | Authenticated: per-org limits. Unauthenticated: 1K/hr shared |
| Stale results | Use `--live` flag on fetch, or remove `--query-time` from search |
| Truncated content | Increase `--max-chars` or `--snippet-length` |
| Error fetching URL (404/422) | URL may not be indexed — add `--live` to fetch any URL |

## Reference

| File | Contents |
|------|----------|
| `references/api-reference.md` | Full API parameter reference for both endpoints |
| `references/selection-guide.md` | Detailed comparison with Exa and Firecrawl |
