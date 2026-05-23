---

name: tavily
description: "Tavily AI search API for LLM applications: web search, content extraction, site crawling, mapping, and research. Keywords: Tavily, AI search, RAG, web search API, LLM search, extract, crawl, map, research, tavily-python."
version: "0.7.21"
release_date: "2026-01-30"

# Tavily

AI-optimized search engine for building LLM applications with real-time web data.

## Quick Navigation

| Topic          | Reference                                         |
| -------------- | ------------------------------------------------- |
| REST API       | [api.md](references/api.md)                       |
| Python SDK     | [python.md](references/python.md)                 |
| JavaScript SDK | [javascript.md](references/javascript.md)         |
| Best Practices | [best-practices.md](references/best-practices.md) |
| Integrations   | [integrations.md](references/integrations.md)     |

## When to Use

- Building RAG applications with real-time web data
- AI agents that need current information
- Content extraction from web pages
- Site crawling with AI-guided instructions
- Autonomous research tasks

## Installation

```bash
# Python
pip install tavily-python

# JavaScript
npm i @tavily/core
```

## Quick Start

### Python

```python
from tavily import TavilyClient

client = TavilyClient(api_key="tvly-YOUR_API_KEY")
response = client.search("What is the latest news about AI?")
print(response)
```

### JavaScript

```javascript
import { tavily } from "@tavily/core";

const client = tavily({ apiKey: "tvly-YOUR_API_KEY" });
const response = await client.search("What is the latest news about AI?");
console.log(response);
```

### cURL

```bash
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer tvly-YOUR_API_KEY" \
  -d '{"query": "What is the latest news about AI?"}'
```

## Core APIs

| API      | Purpose                         | Credits          |
| -------- | ------------------------------- | ---------------- |
| Search   | Web search optimized for LLMs   | 1-2 per request  |
| Extract  | Extract content from URLs       | 1-2 per 5 URLs   |
| Map      | Map website structure           | 1-2 per 10 pages |
| Crawl    | Crawl + extract from sites      | Map + Extract    |
| Research | Autonomous deep research (beta) | 4-250 per task   |

## Pricing & Credits

**Free tier:** 1,000 credits/month (no credit card required)

| Plan       | Credits/month | Price/credit |
| ---------- | ------------- | ------------ |
| Researcher | 1,000         | Free         |
| Project    | 4,000         | $0.0075      |
| Bootstrap  | 15,000        | $0.0067      |
| Startup    | 38,000        | $0.0058      |
| Growth     | 100,000       | $0.005       |
| Pay-as-go  | Per usage     | $0.008       |

### Credit Costs

| API             | Basic               | Advanced   |
| --------------- | ------------------- | ---------- |
| Search          | 1                   | 2          |
| Extract         | 1/5 URLs            | 2/5 URLs   |
| Map             | 1/10 pages          | 2/10 pages |
| Crawl           | Map + Extract costs |
| Research (mini) | 4-110               | -          |
| Research (pro)  | 15-250              | -          |

## Rate Limits

| Environment | RPM (requests/min) |
| ----------- | ------------------ |
| Development | 100                |
| Production  | 1,000              |

**Note:** Crawl endpoint limited to 100 RPM for both environments.

Production keys require paid plan or PAYGO enabled.

## Search API

Primary endpoint for LLM-optimized web search.

```python
response = client.search(
    query="Latest AI developments",
    search_depth="advanced",      # "basic" (1 credit) or "advanced" (2 credits)
    max_results=10,               # 1-20 results
    include_answer=True,          # Include AI-generated answer
    include_raw_content=False,    # Include raw HTML
    include_domains=["arxiv.org"],  # Filter to specific domains
    exclude_domains=["pinterest.com"]  # Exclude domains
)
```

### Response Structure

```python
{
    "query": "...",
    "answer": "AI-generated summary...",  # if include_answer=True
    "results": [
        {
            "title": "Page Title",
            "url": "https://...",
            "content": "Extracted relevant content...",
            "score": 0.95,
            "raw_content": "..."  # if include_raw_content=True
        }
    ]
}
```

## Extract API

Extract content from specific URLs.

```python
response = client.extract(
    urls=["https://example.com/article1", "https://example.com/article2"],
    extract_depth="basic"  # "basic" or "advanced"
)
```

## Crawl API

Crawl websites with AI-guided instructions.

```python
response = client.crawl(
    url="https://docs.example.com",
    instructions="Find all pages about Python SDK",  # Optional AI guidance
    max_depth=2,
    limit=50
)
```

## Map API

Get website structure without extracting content.

```python
response = client.map(
    url="https://docs.example.com",
    instructions="Find documentation pages"  # Optional
)
```

## Research API (Beta)

Autonomous deep research on complex topics.

```python
response = client.research(
    input="What are the implications of quantum computing on cryptography?",
    model="pro"  # "pro" (15-250 credits) or "mini" (4-110 credits)
)
```

## Why Tavily?

| Feature          | Traditional Search | Tavily        |
| ---------------- | ------------------ | ------------- |
| Output           | URLs + snippets    | Full content  |
| Scraping         | Manual             | Built-in      |
| LLM optimization | None               | Purpose-built |
| Filtering        | Manual             | AI-powered    |
| Context limits   | Not handled        | Optimized     |

## Best Practices

1. **Use `search_depth="basic"`** for simple queries (saves credits)
2. **Use `include_answer=True`** for quick summaries
3. **Filter domains** to improve relevance
4. **Use Extract** when you know specific URLs
5. **Use Research** for complex, multi-step queries

## Prohibitions

- Do not expose API keys in client-side code
- Do not exceed rate limits (implement backoff)
- Do not scrape sites that block Tavily crawler

## Links

- [API Playground](https://app.tavily.com/playground)
- [Documentation](https://docs.tavily.com)
- [Community](https://discord.gg/tavily)
