---
name: web-search
version: 1.0.0
description: General-purpose web search for facts, documentation, and current information.
metadata:
  openclaw:
    emoji: 🌐
    category: research
---

# Web Search

General-purpose web search for facts, documentation, and current information.

## Basic Usage

```
web_search(query="...", count=5)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Search query |
| `count` | number | Results (1-10) |
| `country` | string | Region code (US, DE, ALL) |
| `freshness` | string | `pd` (day), `pw` (week), `pm` (month), `py` (year) |
| `search_lang` | string | ISO language code |

## When to Use

| Scenario | Example |
|----------|---------|
| **Quick facts** | "Python 3.12 release date" |
| **Documentation** | "Docker compose syntax volumes" |
| **Current events** | "OpenAI news this week" |
| **Troubleshooting** | "Error: connection refused port 5432" |
| **Comparisons** | "Ubuntu 22.04 vs 24.04" |

## Advanced Queries

### Time-Bound

```python
# Last week only
freshness="pw"

# Specific date range
freshness="2026-01-01to2026-02-01"
```

### Site-Specific

Add to query:
```
"query" site:github.com
"query" site:stackoverflow.com
"query" site:docs.python.org
```

### Region-Specific

```python
country="DE"  # German results
search_lang="de"  # German language
```

## Integration with Research

Use web_search as first step, then:

1. **Quick facts** → Use directly
2. **Complex topics** → Follow with `web_fetch` on top results
3. **Deep research** → Feed to `perplexity-deep-search` or `pokee-deep-research`

## Best Practices

1. **Be specific** — "Docker volume mount permissions" > "Docker issues"
2. **Include context** — "Python" vs "Python programming language"
3. **Check dates** — Use `freshness` for time-sensitive topics
4. **Verify sources** — Prefer official docs over forums
5. **Chain tools** — Search → Fetch → Synthesize
