---
name: perplexity-search
description: Raw web search results (URLs, snippets). Use when you need a list of sources, not a synthesized answer.
---

# Perplexity Search

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| query | required | Search query |
| max_results | 10 | 1-20 results |
| max_tokens_per_page | 1024 | Content per result |
| country | - | ISO code filter |

## Output

```json
{"title": "...", "url": "...", "snippet": "...", "date": "..."}
```
