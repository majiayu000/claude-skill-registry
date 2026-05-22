---
name: using-perplexity-platform
description: Perplexity Sonar API development with search-augmented generation, real-time web search, citations, and OpenAI-compatible Chat Completions. Use for AI-powered applications requiring up-to-date information, research assistants, and grounded responses with sources.
---

# Perplexity Sonar API Development Skill

## Quick Reference

Perplexity Sonar API development with Python and TypeScript/JavaScript clients. Covers Sonar model family for search-augmented generation, Chat Completions API (OpenAI-compatible), real-time web search, citations, and streaming.

---

## Table of Contents

1. [When to Use](#when-to-use)
2. [Sonar Model Family](#sonar-model-family)
3. [Quick Start](#quick-start)
4. [Chat Completions API](#chat-completions-api)
5. [Citations and Sources](#citations-and-sources)
6. [Search Configuration](#search-configuration)
7. [Streaming](#streaming)
8. [Error Handling](#error-handling)
9. [Best Practices](#best-practices)
10. [Anti-Patterns](#anti-patterns)
11. [Integration Checklist](#integration-checklist)
12. [When to Use Perplexity vs Others](#when-to-use-perplexity-vs-others)
13. [CLI Quick Test](#cli-quick-test)
14. [See Also](#see-also)

---

## When to Use

This skill is loaded by `backend-developer` when:
- `openai` package in `requirements.txt` or `pyproject.toml` with Perplexity base URL
- Environment variables `PERPLEXITY_API_KEY` or `PPLX_API_KEY` present
- User mentions "Perplexity", "Sonar", or "search-augmented" in task
- Code uses `api.perplexity.ai` base URL

**Minimum Detection Confidence**: 0.8 (80%)

---

## Sonar Model Family

### Available Models

| Model | Context | Search | Use Case | Speed |
|-------|---------|--------|----------|-------|
| `sonar` | 128K | Yes | General search-augmented | Fast |
| `sonar-pro` | 200K | Yes | Complex research, deeper search | Medium |
| `sonar-reasoning` | 128K | Yes | Multi-step reasoning with search | Slower |
| `sonar-reasoning-pro` | 200K | Yes | Advanced reasoning, citations | Slowest |

### Model Selection Guide

```
Task Complexity -> Model Selection
+-- Simple factual queries     -> sonar (fast, affordable)
+-- Research with citations    -> sonar-pro (deeper search)
+-- Multi-step reasoning       -> sonar-reasoning
+-- Complex analysis           -> sonar-reasoning-pro
```

### Pricing (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| sonar | $1.00 | $1.00 |
| sonar-pro | $3.00 | $15.00 |
| sonar-reasoning | $1.00 | $5.00 |
| sonar-reasoning-pro | $2.00 | $8.00 |

---

## Quick Start

### Python Setup (Using OpenAI SDK)

```python
from openai import OpenAI

client = OpenAI(
    api_key="pplx-...",  # or use PERPLEXITY_API_KEY env var
    base_url="https://api.perplexity.ai"
)

response = client.chat.completions.create(
    model="sonar",
    messages=[
        {"role": "system", "content": "Be precise and concise. Cite sources."},
        {"role": "user", "content": "What are the latest developments in AI?"}
    ]
)

print(response.choices[0].message.content)

# Access citations if available
if hasattr(response, 'citations'):
    for citation in response.citations:
        print(f"  - {citation}")
```

### TypeScript Setup

```typescript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.PERPLEXITY_API_KEY,
  baseURL: 'https://api.perplexity.ai'
});

const response = await client.chat.completions.create({
  model: 'sonar',
  messages: [
    { role: 'system', content: 'Be precise and concise. Cite sources.' },
    { role: 'user', content: 'What are the latest developments in AI?' }
  ]
});

console.log(response.choices[0].message.content);
```

### Environment Configuration

```bash
export PERPLEXITY_API_KEY="pplx-..."
# Alternative: export PPLX_API_KEY="pplx-..."
```

---

## Chat Completions API

### Common Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Model ID (required) |
| `messages` | array | Conversation messages (required) |
| `temperature` | float (0-2) | Randomness (0=deterministic) |
| `max_tokens` | int | Max response tokens |
| `stream` | boolean | Enable streaming |

### Perplexity-Specific Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `search_domain_filter` | array | Limit search to specific domains |
| `return_images` | boolean | Include relevant images |
| `return_related_questions` | boolean | Suggest follow-up questions |
| `search_recency_filter` | string | Filter by recency (day, week, month, year) |

```python
# Advanced search configuration
response = client.chat.completions.create(
    model="sonar-pro",
    messages=[{"role": "user", "content": "Recent tech layoffs?"}],
    extra_body={
        "search_domain_filter": ["techcrunch.com", "theverge.com"],
        "search_recency_filter": "week",
        "return_related_questions": True
    }
)
```

---

## Citations and Sources

Perplexity automatically includes citations. Extract and display them:

```python
def get_response_with_citations(client, query, model="sonar"):
    """Get response with structured citations."""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": query}]
    )

    content = response.choices[0].message.content
    citations = []

    if hasattr(response, 'citations'):
        citations = response.citations

    return content, citations

# Usage
answer, sources = get_response_with_citations(client, "Who won the latest Super Bowl?")
print("Answer:", answer)
for source in sources:
    print(f"  - {source}")
```

---

## Search Configuration

### Domain Filtering

```python
response = client.chat.completions.create(
    model="sonar-pro",
    messages=[{"role": "user", "content": "Latest research on LLMs"}],
    extra_body={
        "search_domain_filter": ["arxiv.org", "openai.com", "anthropic.com"]
    }
)
```

### Recency Filtering

```python
response = client.chat.completions.create(
    model="sonar",
    messages=[{"role": "user", "content": "Stock market news"}],
    extra_body={
        "search_recency_filter": "day"  # day, week, month, year
    }
)
```

### Academic Focus

```python
response = client.chat.completions.create(
    model="sonar-pro",
    messages=[{
        "role": "system",
        "content": "Focus on peer-reviewed academic sources."
    }, {
        "role": "user",
        "content": "Research on sleep and memory consolidation?"
    }],
    extra_body={
        "search_domain_filter": [
            "pubmed.ncbi.nlm.nih.gov", "nature.com", "science.org"
        ]
    }
)
```

---

## Streaming

### Synchronous Streaming

```python
stream = client.chat.completions.create(
    model="sonar",
    messages=[{"role": "user", "content": "Explain machine learning."}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Async Streaming

```python
import asyncio
from openai import AsyncOpenAI

async def stream_response(prompt: str):
    client = AsyncOpenAI(
        api_key="pplx-...",
        base_url="https://api.perplexity.ai"
    )

    stream = await client.chat.completions.create(
        model="sonar",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    async for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)

asyncio.run(stream_response("What's happening in AI today?"))
```

---

## Error Handling

```python
from openai import (
    OpenAI, RateLimitError, AuthenticationError, APIConnectionError
)
import time

def safe_search(query: str, max_retries: int = 3) -> str | None:
    client = OpenAI(api_key="pplx-...", base_url="https://api.perplexity.ai")

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="sonar",
                messages=[{"role": "user", "content": query}]
            )
            return response.choices[0].message.content

        except AuthenticationError:
            raise  # Don't retry auth errors

        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            wait_time = (2 ** attempt) + 1
            time.sleep(wait_time)

        except APIConnectionError:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)

    return None
```

---

## Best Practices

### 1. Model Selection for Task

```python
def get_model_for_task(task_type: str) -> str:
    models = {
        "quick_lookup": "sonar",
        "research": "sonar-pro",
        "analysis": "sonar-reasoning",
        "complex": "sonar-reasoning-pro"
    }
    return models.get(task_type, "sonar")
```

### 2. Optimize for Search Quality

```python
# BAD: vague query
messages = [{"role": "user", "content": "AI"}]

# GOOD: specific query with context
messages = [
    {"role": "system", "content": "You are a tech industry analyst."},
    {"role": "user", "content": "Top 3 AI startups that raised funding in 2024?"}
]
```

### 3. Use Recency Filters Appropriately

```python
# Current events - use day/week filter
extra_body = {"search_recency_filter": "day"}

# General research - no filter needed
extra_body = {}
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Using Perplexity for creative writing | Paying for unused search | Use OpenAI/Anthropic instead |
| Ignoring citations | Losing valuable source info | Always capture and display citations |
| Overly broad queries | Irrelevant search results | Be specific, add system context |
| Hardcoding API keys | Security risk | Use environment variables |

---

## Integration Checklist

### Pre-Flight

- [ ] `PERPLEXITY_API_KEY` environment variable set
- [ ] Error handling with retry logic implemented
- [ ] Appropriate model selected for task
- [ ] Citation handling implemented

### Production Readiness

- [ ] Secrets in secret manager
- [ ] Monitoring for API errors
- [ ] Usage tracking and cost alerts
- [ ] Fallback behavior for API failures

---

## When to Use Perplexity vs Others

| Use Case | Provider |
|----------|----------|
| Real-time information | Perplexity |
| Research with citations | Perplexity (Sonar Pro) |
| Current events | Perplexity |
| General chat/completion | OpenAI or Anthropic |
| Code generation | OpenAI or Anthropic |
| Creative writing | OpenAI or Anthropic |

---

## CLI Quick Test

```bash
# Test API access
curl -X POST https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "sonar", "messages": [{"role": "user", "content": "Hello"}]}'
```

---

## See Also

- [REFERENCE.md](REFERENCE.md) - Comprehensive API documentation with advanced patterns
  - Multi-turn conversation management
  - Enterprise data integrations
  - Context7 integration patterns
  - Server-Sent Events for web applications
  - Production-ready code patterns
- [templates/](templates/) - Production-ready code templates
- [examples/](examples/) - Working examples
- [Perplexity API Docs](https://docs.perplexity.ai/)

---

**Progressive Disclosure**: Start here for quick reference. Load REFERENCE.md for advanced patterns and comprehensive documentation.
