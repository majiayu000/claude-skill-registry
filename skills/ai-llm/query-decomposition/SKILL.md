---
name: query-decomposition
description: Query decomposition for multi-concept retrieval. Use when handling complex queries spanning multiple topics, implementing multi-hop retrieval, or improving coverage for compound questions.
context: fork
agent: data-pipeline-engineer
version: 1.0.0
author: SkillForge
user-invocable: false
---

# Query Decomposition
Break complex queries into independent concepts for parallel retrieval and fusion.

## Overview

- Complex queries spanning multiple topics or concepts
- Multi-hop questions requiring chained reasoning
- Queries where single retrieval misses relevant documents
- Improving recall for compound questions

Break complex queries into independent concepts for parallel retrieval and fusion.

## The Problem

Complex queries span multiple topics that may not co-occur in single documents:
```
Query: "How do chunking strategies affect reranking in RAG?"
→ Single search may miss docs about chunking OR reranking
→ Poor coverage across all concepts
```

## The Solution

Decompose into independent concepts, retrieve separately, then fuse:
```
Query: "How do chunking strategies affect reranking in RAG?"
→ Concepts: ["chunking strategies", "reranking methods", "RAG pipeline"]
→ Search each concept independently
→ Fuse results with Reciprocal Rank Fusion (RRF)
→ Full coverage across all topics
```

## Implementation

### 1. Heuristic Detection (Fast Path)

```python
MULTI_CONCEPT_INDICATORS = [
    " vs ", " versus ", " compared to ", " or ",
    " and ", " with ", " affect ", " impact ",
    "difference between", "relationship between",
]

def is_multi_concept_heuristic(query: str) -> bool:
    """Fast check for multi-concept indicators (<1ms)."""
    query_lower = query.lower()
    return any(ind in query_lower for ind in MULTI_CONCEPT_INDICATORS)
```

### 2. LLM Decomposition

```python
from pydantic import BaseModel, Field
from openai import AsyncOpenAI

class ConceptExtraction(BaseModel):
    """LLM output schema for concept extraction."""
    concepts: list[str] = Field(
        ...,
        min_length=1,
        max_length=5,
        description="Distinct concepts from the query",
    )
    reasoning: str | None = None

async def decompose_query(
    query: str,
    llm: AsyncOpenAI,
) -> list[str]:
    """Extract independent concepts using LLM."""

    response = await llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """
Extract 2-4 independent concepts from this query.
Each concept should be searchable on its own.
Output JSON: {"concepts": ["concept1", "concept2"], "reasoning": "..."}
"""},
            {"role": "user", "content": query}
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )

    result = ConceptExtraction.model_validate_json(
        response.choices[0].message.content
    )
    return result.concepts
```

### 3. Parallel Retrieval + RRF Fusion

```python
import asyncio
from collections import defaultdict

async def decomposed_search(
    query: str,
    search_fn: callable,
    llm: AsyncOpenAI,
    top_k: int = 10,
) -> list[dict]:
    """Search with query decomposition and RRF fusion."""

    # Check if decomposition needed
    if not is_multi_concept_heuristic(query):
        return await search_fn(query, limit=top_k)

    # Decompose into concepts
    concepts = await decompose_query(query, llm)

    if len(concepts) <= 1:
        return await search_fn(query, limit=top_k)

    # Parallel retrieval for each concept
    tasks = [search_fn(concept, limit=top_k) for concept in concepts]
    results_per_concept = await asyncio.gather(*tasks)

    # RRF fusion
    return reciprocal_rank_fusion(results_per_concept, k=60)


def reciprocal_rank_fusion(
    result_lists: list[list[dict]],
    k: int = 60,
) -> list[dict]:
    """Combine ranked lists using RRF."""
    scores: defaultdict[str, float] = defaultdict(float)
    docs: dict[str, dict] = {}

    for results in result_lists:
        for rank, doc in enumerate(results, start=1):
            doc_id = doc["id"]
            scores[doc_id] += 1.0 / (k + rank)
            docs[doc_id] = doc

    # Sort by RRF score
    ranked_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    return [docs[doc_id] for doc_id in ranked_ids]
```

## Complete Service

```python
class QueryDecomposer:
    def __init__(self, llm, search_fn):
        self.llm = llm
        self.search_fn = search_fn
        self._cache: dict[str, list[str]] = {}

    async def search(
        self,
        query: str,
        top_k: int = 10,
    ) -> list[dict]:
        """Search with automatic decomposition."""

        # Fast path: single concept
        if not is_multi_concept_heuristic(query):
            return await self.search_fn(query, limit=top_k)

        # Check cache
        cache_key = query.lower().strip()
        if cache_key in self._cache:
            concepts = self._cache[cache_key]
        else:
            concepts = await decompose_query(query, self.llm)
            self._cache[cache_key] = concepts

        # Single concept after decomposition
        if len(concepts) <= 1:
            return await self.search_fn(query, limit=top_k)

        # Parallel retrieval
        tasks = [self.search_fn(c, limit=top_k) for c in concepts]
        results_per_concept = await asyncio.gather(*tasks)

        # Fuse with RRF
        return reciprocal_rank_fusion(results_per_concept)[:top_k]
```

## Combining with HyDE

```python
async def decomposed_hyde_search(
    query: str,
    decomposer: QueryDecomposer,
    hyde_service: HyDEService,
    vector_search: callable,
    top_k: int = 10,
) -> list[dict]:
    """Best of both: decomposition + HyDE for each concept."""

    # Decompose query
    concepts = await decomposer.get_concepts(query)

    # Generate HyDE for each concept in parallel
    hyde_results = await asyncio.gather(*[
        hyde_service.generate(concept) for concept in concepts
    ])

    # Search with HyDE embeddings
    search_tasks = [
        vector_search(embedding=hr.embedding, limit=top_k)
        for hr in hyde_results
    ]
    results_per_concept = await asyncio.gather(*search_tasks)

    # Fuse results
    return reciprocal_rank_fusion(results_per_concept)[:top_k]
```

## When to Decompose

| Query Type | Decompose? |
|------------|------------|
| "What is X?" | No |
| "X vs Y" | Yes |
| "How does X affect Y?" | Yes |
| "Best practices for X" | No |
| "X and Y in Z" | Yes |
| "Difference between X, Y, Z" | Yes |

## Performance Tips

- Use heuristics first (sub-millisecond)
- Cache decomposition results
- Limit to 2-4 concepts max
- Set timeout with fallback to original query
- Combine with HyDE for vocabulary bridging

## Related Skills

- `rag-retrieval` - Core RAG patterns enhanced by query decomposition
- `hyde-retrieval` - Combine with HyDE for vocabulary bridging per concept
- `reranking-patterns` - Rerank fused results for final precision
- `embeddings` - Embedding strategies for parallel concept retrieval

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Decomposition detection | Heuristic first, LLM second | Sub-millisecond fast path for simple queries |
| Max concepts | 2-4 | More concepts increase latency without proportional benefit |
| Fusion algorithm | Reciprocal Rank Fusion (RRF) | Robust, parameter-free rank combination |
| LLM for decomposition | gpt-4o-mini | Fast, cheap, good at concept extraction |

## References

- [Multi-hop Question Answering](https://arxiv.org/abs/2305.14283)
- [Query2Doc](https://arxiv.org/abs/2303.07678)