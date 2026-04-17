---
name: exa-search
description: Search the web with Exa AI — neural search, content extraction, similar page discovery, quick research with citations, and async pro research with structured output. Covers all Exa endpoints (/search, /contents, /findSimilar, /answer, /research/v1). Triggers on web search, find pages, similar pages, research with citations, Exa, neural search.
---

# Exa Search Skill

5 specialized scripts for Exa AI search API—neural search, content extraction, similar pages, research with citations, and async pro research.

**Prerequisite:** `EXA_API_KEY` environment variable. Get key at https://dashboard.exa.ai

## Token-Efficient Search

Inspired by Anthropic's [dynamic filtering](https://claude.com/blog/improved-web-search-with-dynamic-filtering)—always filter before reasoning. ~24% fewer tokens, ~11% better accuracy.

### The Principle: Search Cheaply → Filter → Extract Selectively → Reason

**DO:**
```bash
# Step 1: Search with --no-text (titles/URLs only — cheapest)
python3 ~/.claude/skills/exa-search/scripts/exa_search.py "query" -n 20 --no-text

# Step 2: Evaluate titles, pick best 3-5 URLs

# Step 3: Extract only those URLs with bounded content
python3 ~/.claude/skills/exa-search/scripts/exa_contents.py URL1 URL2 --highlights --max-chars 3000
```

**DON'T:** Search with full text for 50 results, then reason over all of it.

### Use API-Level Filters First (Free Filtering)

These reduce results at the API level before you ever see them:

- `--must-include "term"` — results must contain this string
- `--must-exclude "term"` — removes irrelevant results
- `--domains site1.com site2.com` — restrict to authoritative sources
- `--category "research paper"` — eliminate irrelevant content types
- `--after 2025-01-01` / `--before` — temporal filtering

### Use Summaries Over Full Text

When you need the gist, not raw content:
```bash
# AI-distilled summaries — much smaller than full text
python3 ~/.claude/skills/exa-search/scripts/exa_search.py "query" --summary "Key findings" -n 5
```

### Use Bounded Context for RAG

```bash
# Capped context string — prevents unbounded token usage
python3 ~/.claude/skills/exa-search/scripts/exa_search.py "query" --context --context-chars 5000
```

### Post-Process with filter_web_results.py

Pipe Exa JSON output through the Firecrawl filter script for additional reduction:
```bash
python3 ~/.claude/skills/exa-search/scripts/exa_search.py "query" --json | \
  python3 ~/.claude/skills/firecrawl/scripts/filter_web_results.py \
  --fields "title,url,text" --max-chars 3000
```

### Cost Tiers — Match to Task

| Type | Latency | Cost/1k | When |
|------|---------|---------|------|
| `--instant` | <150ms | Cheapest | Real-time lookups, autocomplete |
| `--fast` | ~500ms | Low | Quick checks, confirmations |
| `auto` (default) | -- | Medium | General search |
| `--deep` | 4-12s | $12 | Comprehensive research |
| `--deep-reasoning` | 12-50s | $15 | Maximum depth + synthesis |

### Structured Deep Search (Exa Deep)

Deep and deep-reasoning searches support structured JSON output via `outputSchema`. The API returns parsed content in `output.content` with per-field grounding citations and confidence scores.

| Quick Example | Purpose |
|---------------|---------|
| `... --deep --text-output "Short answer"` | Simple text answer |
| `... --deep-reasoning --schema-preset company` | Structured company research |
| `... --deep --output-schema '{"type":"object","properties":{"answer":{"type":"string"}}}'` | Custom schema |
| `... --deep --schema-file ~/schemas/analysis.json` | Schema from file |

Presets: `company`, `paper-survey`, `competitor-analysis`, `person`, `news-digest`

Output includes field-level grounding: per-field citations with [H]igh/[M]edium/[L]ow confidence.

---

## Available Scripts

### 1. exa_search.py — Neural Web Search

```bash
python3 ~/.claude/skills/exa-search/scripts/exa_search.py "query" [options]
```

| Quick Example | Purpose |
|---------------|---------|
| `... exa_search.py "AI frameworks"` | Basic search |
| `... exa_search.py "transformers" --category "research paper" -n 20` | Academic papers |
| `... exa_search.py "query" --deep --additional-queries "alt query"` | Deep search |
| `... exa_search.py "query" --domains docs.python.org` | Domain-filtered |
| `... exa_search.py "query" --after 2025-01-01 --category news` | Recent news |
| `... exa_search.py "query" --context --context-chars 10000` | RAG context |
| `... exa_search.py "query" --instant -n 5` | Sub-150ms lookup |
| `... exa_search.py "Top AI startups" --deep-reasoning --schema-preset company` | Structured company research |
| `... exa_search.py "Who is CEO of Stripe?" --deep --text-output "Short answer"` | Quick factual answer |

**Categories:** company, research paper, news, pdf, github, tweet, personal site, people, financial report

### 2. exa_contents.py — URL Content Extraction

```bash
python3 ~/.claude/skills/exa-search/scripts/exa_contents.py URL [URL2...] [options]
```

| Quick Example | Purpose |
|---------------|---------|
| `... exa_contents.py "https://arxiv.org/abs/2307.06435"` | Extract paper |
| `... exa_contents.py URL --summary "Key methods" --highlights` | Summarized extraction |
| `... exa_contents.py URL --livecrawl always` | Fresh content |
| `... exa_contents.py URL --max-chars 5000` | Bounded extraction |

### 3. exa_similar.py — Find Similar Pages

```bash
python3 ~/.claude/skills/exa-search/scripts/exa_similar.py URL [options]
```

| Quick Example | Purpose |
|---------------|---------|
| `... exa_similar.py "https://stripe.com" --category company --exclude-source` | Find competitors |
| `... exa_similar.py "https://arxiv.org/abs/..." -n 15` | Related papers |
| `... exa_similar.py URL --summary "How different?"` | Comparison summaries |

### 4. exa_research.py — AI-Powered Research

```bash
python3 ~/.claude/skills/exa-search/scripts/exa_research.py "question" [options]
```

| Quick Example | Purpose |
|---------------|---------|
| `... exa_research.py "React vs Vue differences?" --sources` | Research with citations |
| `... exa_research.py "query" --stream` | Real-time streaming |
| `... exa_research.py "query" --domains docs.python.org` | Authoritative sources |
| `... exa_research.py "query" --markdown` | Markdown with citations |
| `... exa_research.py "query" --answer-only` | Pipe-friendly output |

### 5. exa_research_async.py — Async Pro Research

```bash
python3 ~/.claude/skills/exa-search/scripts/exa_research_async.py "question" [options]
```

| Quick Example | Purpose |
|---------------|---------|
| `... exa_research_async.py "Compare AI frameworks" --pro --wait` | Pro model |
| `... exa_research_async.py "Quick overview" --fast` | Fast model |
| `... exa_research_async.py "query" --schema '{...}'` | Structured output |
| `... exa_research_async.py status r_abc123` | Check job |
| `... exa_research_async.py list` | List jobs |

---

## Script Selection Guide

| Task | Best Script |
|------|-------------|
| Web search with filters | `exa_search.py` |
| Research papers | `exa_search.py --category "research paper"` |
| Company/startup info | `exa_search.py --category company` |
| GitHub repos/code | `exa_search.py --category github` |
| Extract known URL content | `exa_contents.py` |
| Find competitors | `exa_similar.py --exclude-source` |
| Quick answers with citations | `exa_research.py --sources` |
| Complex structured research | `exa_research_async.py --pro` |
| Real-time search | `exa_search.py --instant` |
| RAG context building | `exa_search.py --context` |
| Structured research with grounding | `exa_search.py --deep-reasoning --schema-preset company` |
| Quick factual answer | `exa_search.py --deep --text-output "Short answer"` |

## Exa vs Firecrawl vs Native Claude Tools

| Need | Best Tool | Why |
|------|-----------|-----|
| Semantic/neural search | Exa `exa_search.py` | AI-powered relevance |
| Find research papers | Exa `--category "research paper"` | Academic index |
| Quick research answer | Exa `exa_research.py` | Citations + synthesis |
| Find similar pages | Exa `exa_similar.py` | Semantic similarity |
| Single page → markdown | Firecrawl `scrape --only-main-content` | Cleanest output |
| Crawl entire site | Firecrawl `crawl --wait --progress` | Link following |
| Autonomous data finding | Firecrawl `agent` | No URLs needed |
| Search + scrape combined | Firecrawl `search --scrape` | One operation |
| Claude API agent building | Native `web_search_20260209` | Built-in dynamic filtering |
| Twitter/X content | `jina URL` | Only tool that works |

---

## Common Workflows

### Research a Topic
```bash
python3 ~/.claude/skills/exa-search/scripts/exa_research.py "How does RAG work?" --sources --markdown
```

### Literature Review
```bash
# Find papers, then find similar to best hit
python3 ~/.claude/skills/exa-search/scripts/exa_search.py "transformer optimization" --category "research paper" -n 20 --summary "Key contributions"
python3 ~/.claude/skills/exa-search/scripts/exa_similar.py "https://arxiv.org/abs/1706.03762" --category "research paper" -n 15
```

### Documentation Research
```bash
python3 ~/.claude/skills/exa-search/scripts/exa_search.py "React useEffect cleanup" --domains react.dev developer.mozilla.org --context
```

### Build RAG Context
```bash
python3 ~/.claude/skills/exa-search/scripts/exa_search.py "Python async patterns" --context --context-chars 15000 --domains docs.python.org
```

---

## Reference Documentation

| File | Contents |
|------|----------|
| `references/exa-scripts-reference.md` | Full parameter reference for all 5 scripts, cost table, MCP comparison, test suite |

## Test Suite

```bash
python3 ~/.claude/skills/exa-search/scripts/test_exa.py --quick       # Quick validation
python3 ~/.claude/skills/exa-search/scripts/test_exa.py               # Full suite
python3 ~/.claude/skills/exa-search/scripts/test_exa.py --endpoint search  # Specific endpoint
```
