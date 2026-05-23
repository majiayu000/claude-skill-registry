---
name: reranking-patterns
description: Reranking patterns for improving search precision. Use when implementing cross-encoder reranking, LLM-based relevance scoring, or improving retrieval quality in RAG pipelines.
context: fork
agent: data-pipeline-engineer
version: 1.0.0
author: SkillForge
user-invocable: false
---

# Reranking Patterns
Improve search precision by re-scoring retrieved documents with more powerful models.

## Overview

- Improving precision after initial retrieval
- When bi-encoder embeddings miss semantic nuance
- Combining multiple relevance signals
- Production RAG systems requiring high accuracy

Improve search precision by re-scoring retrieved documents with more powerful models.

## Why Rerank?

Initial retrieval (bi-encoder) prioritizes speed over accuracy:
- Bi-encoder: Embeds query and docs separately → fast but approximate
- Cross-encoder/LLM: Processes query+doc together → slow but accurate

**Solution**: Retrieve many (top-50), rerank few (top-10)

## Pattern 1: Cross-Encoder Reranking

```python
from sentence_transformers import CrossEncoder

class CrossEncoderReranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        documents: list[dict],
        top_k: int = 10,
    ) -> list[dict]:
        """Rerank documents using cross-encoder."""

        # Create query-document pairs
        pairs = [(query, doc["content"]) for doc in documents]

        # Score all pairs
        scores = self.model.predict(pairs)

        # Sort by score
        scored_docs = list(zip(documents, scores))
        scored_docs.sort(key=lambda x: x[1], reverse=True)

        # Return top-k with updated scores
        return [
            {**doc, "score": float(score)}
            for doc, score in scored_docs[:top_k]
        ]
```

## Pattern 2: LLM Reranking (Batch)

```python
from openai import AsyncOpenAI

async def llm_rerank(
    query: str,
    documents: list[dict],
    llm: AsyncOpenAI,
    top_k: int = 10,
) -> list[dict]:
    """Rerank using LLM relevance scoring."""

    # Build prompt with all candidates
    docs_text = "\n\n".join([
        f"[Doc {i+1}]\n{doc['content'][:300]}..."
        for i, doc in enumerate(documents)
    ])

    response = await llm.chat.completions.create(
        model="gpt-4o-mini",  # Fast, cheap
        messages=[
            {"role": "system", "content": """
Rate each document's relevance to the query (0.0-1.0).
Output one score per line, in order:
0.95
0.72
0.45
..."""},
            {"role": "user", "content": f"Query: {query}\n\nDocuments:\n{docs_text}"}
        ],
        temperature=0,
    )

    # Parse scores
    scores = parse_scores(response.choices[0].message.content, len(documents))

    # Sort and return
    scored_docs = list(zip(documents, scores))
    scored_docs.sort(key=lambda x: x[1], reverse=True)

    return [
        {**doc, "score": score}
        for doc, score in scored_docs[:top_k]
    ]


def parse_scores(response: str, expected_count: int) -> list[float]:
    """Parse LLM response into scores."""
    scores = []
    for line in response.strip().split("\n"):
        try:
            score = float(line.strip())
            scores.append(max(0.0, min(1.0, score)))
        except ValueError:
            scores.append(0.5)  # Default on parse error

    # Pad if needed
    while len(scores) < expected_count:
        scores.append(0.5)

    return scores[:expected_count]
```

## Pattern 3: Cohere Rerank API

```python
import cohere

class CohereReranker:
    def __init__(self, api_key: str):
        self.client = cohere.Client(api_key)

    def rerank(
        self,
        query: str,
        documents: list[dict],
        top_k: int = 10,
    ) -> list[dict]:
        """Rerank using Cohere's rerank API."""

        results = self.client.rerank(
            model="rerank-english-v3.0",
            query=query,
            documents=[doc["content"] for doc in documents],
            top_n=top_k,
        )

        return [
            {**documents[r.index], "score": r.relevance_score}
            for r in results.results
        ]
```

## Pattern 4: Combined Scoring

Combine multiple signals with weighted average:

```python
from dataclasses import dataclass

@dataclass
class ReRankScore:
    doc_id: str
    base_score: float      # Original retrieval score
    llm_score: float       # LLM relevance score
    recency_score: float   # Metadata-based (e.g., freshness)
    final_score: float

def combined_rerank(
    documents: list[dict],
    llm_scores: dict[str, float],
    alpha: float = 0.3,  # Base weight
    beta: float = 0.5,   # LLM weight
    gamma: float = 0.2,  # Recency weight
) -> list[dict]:
    """Combine multiple scoring signals."""

    scored = []
    for doc in documents:
        base = doc.get("score", 0.5)
        llm = llm_scores.get(doc["id"], 0.5)
        recency = calculate_recency_score(doc.get("created_at"))

        final = (alpha * base) + (beta * llm) + (gamma * recency)

        scored.append({
            **doc,
            "score": final,
            "score_components": {
                "base": base,
                "llm": llm,
                "recency": recency,
            }
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored
```

## Complete Reranking Service

```python
class ReRankingService:
    def __init__(
        self,
        llm: AsyncOpenAI,
        timeout_seconds: float = 5.0,
    ):
        self.llm = llm
        self.timeout = timeout_seconds

    async def rerank(
        self,
        query: str,
        documents: list[dict],
        top_k: int = 10,
    ) -> list[dict]:
        """Rerank with timeout and fallback."""
        import asyncio

        if len(documents) <= top_k:
            return documents

        try:
            async with asyncio.timeout(self.timeout):
                return await llm_rerank(
                    query, documents, self.llm, top_k
                )
        except TimeoutError:
            # Fallback: return by original score
            return sorted(
                documents,
                key=lambda x: x.get("score", 0),
                reverse=True
            )[:top_k]
```

## Model Selection Guide

| Model | Latency | Cost | Quality |
|-------|---------|------|---------|
| `cross-encoder/ms-marco-MiniLM-L-6-v2` | ~50ms | Free | Good |
| `BAAI/bge-reranker-large` | ~100ms | Free | Better |
| `cohere rerank-english-v3.0` | ~200ms | $1/1K | Best |
| `gpt-4o-mini` (LLM) | ~500ms | $0.15/1M | Great |

## Best Practices

1. **Retrieve more, rerank less**: Retrieve 50-100, rerank to 10
2. **Truncate content**: 200-400 chars per doc for LLM reranking
3. **Set timeouts**: Always fallback to base ranking
4. **Cache scores**: Same query+doc pair = same score
5. **Batch when possible**: One LLM call for all docs

## Related Skills

- `rag-retrieval` - Core RAG pipeline that reranking enhances
- `contextual-retrieval` - Contextual embeddings combined with reranking for best results
- `embeddings` - Bi-encoder embeddings for initial retrieval before reranking
- `llm-evaluation` - Evaluation patterns for measuring reranking quality

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Retrieve/rerank ratio | Retrieve 50-100, rerank to 10 | Balance coverage and precision |
| Default reranker | cross-encoder/ms-marco-MiniLM-L-6-v2 | Good quality, free, fast (~50ms) |
| LLM reranking | Batch all docs in one call | Reduces latency vs per-doc calls |
| Timeout handling | Fallback to base ranking | Graceful degradation on slow reranking |

## References

- [Cohere Rerank](https://docs.cohere.com/docs/rerank)
- [Sentence Transformers Cross-Encoders](https://www.sbert.net/docs/cross_encoder/usage/usage.html)
- [BGE Reranker](https://huggingface.co/BAAI/bge-reranker-large)