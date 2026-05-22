---
name: hyde-retrieval
description: HyDE (Hypothetical Document Embeddings) for improved semantic retrieval. Use when queries don't match document vocabulary, retrieval quality is poor, or implementing advanced RAG patterns.
context: fork
agent: data-pipeline-engineer
version: 1.0.0
author: SkillForge
user-invocable: false
---

# HyDE (Hypothetical Document Embeddings)

Generate hypothetical answer documents to bridge vocabulary gaps in semantic search.

## The Problem

Direct query embedding often fails due to vocabulary mismatch:
```
Query: "scaling async data pipelines"
Docs use: "event-driven messaging", "Apache Kafka", "message brokers"
→ Low similarity scores despite high relevance
```

## The Solution

Instead of embedding the query, generate a hypothetical answer document:
```
Query: "scaling async data pipelines"
→ LLM generates: "To scale asynchronous data pipelines, use event-driven
   messaging with Apache Kafka. Message brokers provide backpressure..."
→ Embed the hypothetical document
→ Now matches docs using similar terminology
```

## Implementation

```python
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

class HyDEResult(BaseModel):
    """Result of HyDE generation."""
    original_query: str
    hypothetical_doc: str
    embedding: list[float]

async def generate_hyde(
    query: str,
    llm: AsyncOpenAI,
    embed_fn: callable,
    max_tokens: int = 150,
) -> HyDEResult:
    """Generate hypothetical document and embed it."""

    # Generate hypothetical answer
    response = await llm.chat.completions.create(
        model="gpt-4o-mini",  # Fast, cheap model
        messages=[
            {"role": "system", "content":
                "Write a short paragraph that would answer this query. "
                "Use technical terminology that documentation would use."},
            {"role": "user", "content": query}
        ],
        max_tokens=max_tokens,
        temperature=0.3,  # Low temp for consistency
    )

    hypothetical_doc = response.choices[0].message.content

    # Embed the hypothetical document (not the query!)
    embedding = await embed_fn(hypothetical_doc)

    return HyDEResult(
        original_query=query,
        hypothetical_doc=hypothetical_doc,
        embedding=embedding,
    )
```

## With Caching

```python
from functools import lru_cache
import hashlib

class HyDEService:
    def __init__(self, llm, embed_fn):
        self.llm = llm
        self.embed_fn = embed_fn
        self._cache: dict[str, HyDEResult] = {}

    def _cache_key(self, query: str) -> str:
        return hashlib.md5(query.lower().strip().encode()).hexdigest()

    async def generate(self, query: str) -> HyDEResult:
        key = self._cache_key(query)

        if key in self._cache:
            return self._cache[key]

        result = await generate_hyde(query, self.llm, self.embed_fn)
        self._cache[key] = result
        return result
```

## Per-Concept HyDE (Advanced)

For multi-concept queries, generate HyDE for each concept:

```python
async def batch_hyde(
    concepts: list[str],
    hyde_service: HyDEService,
) -> list[HyDEResult]:
    """Generate HyDE embeddings for multiple concepts in parallel."""
    import asyncio

    tasks = [hyde_service.generate(concept) for concept in concepts]
    return await asyncio.gather(*tasks)
```

## Overview

| Scenario | Use HyDE? |
|----------|-----------|
| Abstract/conceptual queries | Yes |
| Exact term searches | No (use keyword) |
| Code snippet searches | No |
| Natural language questions | Yes |
| Vocabulary mismatch suspected | Yes |

## Fallback Strategy

```python
async def hyde_with_fallback(
    query: str,
    hyde_service: HyDEService,
    embed_fn: callable,
    timeout: float = 3.0,
) -> list[float]:
    """HyDE with fallback to direct embedding on timeout."""
    import asyncio

    try:
        async with asyncio.timeout(timeout):
            result = await hyde_service.generate(query)
            return result.embedding
    except TimeoutError:
        # Fallback to direct query embedding
        return await embed_fn(query)
```

## Performance Tips

- Use fast model (gpt-4o-mini, claude-3-haiku) for generation
- Cache aggressively (queries often repeat)
- Set tight timeouts (2-3s) with fallback
- Keep hypothetical docs concise (100-200 tokens)
- Combine with query decomposition for best results

## Related Skills

- `rag-retrieval` - Core RAG patterns that HyDE enhances for better retrieval
- `embeddings` - Embedding models used to embed hypothetical documents
- `query-decomposition` - Complementary technique for multi-concept queries
- `semantic-caching` - Cache HyDE results to avoid repeated LLM calls

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Generation model | gpt-4o-mini / claude-3-haiku | Fast and cheap for hypothetical doc generation |
| Temperature | 0.3 | Low temperature for consistent, factual hypothetical docs |
| Max tokens | 100-200 | Concise docs match embedding sweet spot |
| Timeout with fallback | 2-3 seconds | Graceful degradation to direct query embedding |

## References

- [Gao et al. 2022 - HyDE Paper](https://arxiv.org/abs/2212.10496)
- [LangChain HyDE](https://python.langchain.com/docs/use_cases/query_analysis/techniques/hyde)