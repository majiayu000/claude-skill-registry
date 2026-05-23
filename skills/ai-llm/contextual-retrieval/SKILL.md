---
name: contextual-retrieval
description: Anthropic's Contextual Retrieval technique for improved RAG. Use when chunks lose context during retrieval, implementing hybrid BM25+vector search, or reducing retrieval failures.
context: fork
agent: data-pipeline-engineer
version: 1.0.0
author: SkillForge
user-invocable: false
---
# Contextual Retrieval
Prepend situational context to chunks before embedding to preserve document-level meaning.

## The Problem

Traditional chunking loses context:
```
Original document: "ACME Q3 2024 Earnings Report..."
Chunk: "Revenue increased 15% compared to the previous quarter."

Query: "What was ACME's Q3 2024 revenue growth?"
Result: Chunk doesn't mention "ACME" or "Q3 2024" - retrieval fails
```

## The Solution

**Contextual Retrieval** prepends a brief context to each chunk:
```
Contextualized chunk:
"This chunk is from ACME Corp's Q3 2024 earnings report, specifically
the revenue section. Revenue increased 15% compared to the previous quarter."
```

## Implementation

### Context Generation
```python
import anthropic

client = anthropic.Anthropic()

CONTEXT_PROMPT = """
<document>
{document}
</document>

Here is the chunk we want to situate within the document:
<chunk>
{chunk}
</chunk>

Please give a short, succinct context (1-2 sentences) to situate this chunk
within the overall document. Focus on information that would help retrieval.
Answer only with the context, nothing else.
"""

def generate_context(document: str, chunk: str) -> str:
    """Generate context for a single chunk."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=150,
        messages=[{
            "role": "user",
            "content": CONTEXT_PROMPT.format(document=document, chunk=chunk)
        }]
    )
    return response.content[0].text

def contextualize_chunk(document: str, chunk: str) -> str:
    """Prepend context to chunk."""
    context = generate_context(document, chunk)
    return f"{context}\n\n{chunk}"
```

### Batch Processing with Caching
```python
from anthropic import Anthropic

client = Anthropic()

def contextualize_chunks_cached(document: str, chunks: list[str]) -> list[str]:
    """
    Use prompt caching to efficiently process many chunks from same document.
    Document is cached, only chunk changes per request.
    """
    results = []

    for i, chunk in enumerate(chunks):
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=150,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"<document>\n{document}\n</document>",
                        "cache_control": {"type": "ephemeral"}  # Cache document
                    },
                    {
                        "type": "text",
                        "text": f"""
Here is chunk {i+1} to situate:
<chunk>
{chunk}
</chunk>

Give a short context (1-2 sentences) to situate this chunk.
"""
                    }
                ]
            }]
        )
        context = response.content[0].text
        results.append(f"{context}\n\n{chunk}")

    return results
```

### Hybrid Search (BM25 + Vector)

Contextual Retrieval works best with hybrid search:

```python
from rank_bm25 import BM25Okapi
import numpy as np

class HybridRetriever:
    def __init__(self, chunks: list[str], embeddings: np.ndarray):
        self.chunks = chunks
        self.embeddings = embeddings

        # BM25 index on raw text
        tokenized = [c.lower().split() for c in chunks]
        self.bm25 = BM25Okapi(tokenized)

    def search(
        self,
        query: str,
        query_embedding: np.ndarray,
        top_k: int = 20,
        bm25_weight: float = 0.4,
        vector_weight: float = 0.6
    ) -> list[tuple[int, float]]:
        """Hybrid search combining BM25 and vector similarity."""
        # BM25 scores
        bm25_scores = self.bm25.get_scores(query.lower().split())
        bm25_scores = (bm25_scores - bm25_scores.min()) / (bm25_scores.max() - bm25_scores.min() + 1e-6)

        # Vector similarity
        vector_scores = np.dot(self.embeddings, query_embedding)
        vector_scores = (vector_scores - vector_scores.min()) / (vector_scores.max() - vector_scores.min() + 1e-6)

        # Combine
        combined = bm25_weight * bm25_scores + vector_weight * vector_scores

        # Top-k
        top_indices = np.argsort(combined)[::-1][:top_k]
        return [(i, combined[i]) for i in top_indices]
```

## Complete Pipeline

```python
from dataclasses import dataclass
import hashlib
import json

@dataclass
class ContextualChunk:
    original: str
    contextualized: str
    embedding: list[float]
    doc_id: str
    chunk_index: int

class ContextualRetriever:
    def __init__(self, embed_model, llm_client):
        self.embed_model = embed_model
        self.llm = llm_client
        self.chunks: list[ContextualChunk] = []
        self.bm25 = None

    def add_document(self, doc_id: str, text: str, chunk_size: int = 512):
        """Process and index a document."""
        # 1. Chunk the document
        raw_chunks = self._chunk_text(text, chunk_size)

        # 2. Generate context for each chunk (with caching)
        contextualized = self._contextualize_batch(text, raw_chunks)

        # 3. Embed contextualized chunks
        embeddings = self.embed_model.embed(contextualized)

        # 4. Store
        for i, (raw, ctx, emb) in enumerate(zip(raw_chunks, contextualized, embeddings)):
            self.chunks.append(ContextualChunk(
                original=raw,
                contextualized=ctx,
                embedding=emb,
                doc_id=doc_id,
                chunk_index=i
            ))

        # 5. Rebuild BM25 index
        self._rebuild_bm25()

    def search(self, query: str, top_k: int = 10) -> list[ContextualChunk]:
        """Hybrid search over contextualized chunks."""
        query_emb = self.embed_model.embed([query])[0]

        # BM25 on contextualized text
        bm25_scores = self.bm25.get_scores(query.lower().split())

        # Vector similarity
        embeddings = np.array([c.embedding for c in self.chunks])
        vector_scores = np.dot(embeddings, query_emb)

        # Normalize and combine
        bm25_norm = self._normalize(bm25_scores)
        vector_norm = self._normalize(vector_scores)
        combined = 0.4 * bm25_norm + 0.6 * vector_norm

        # Return top-k
        top_indices = np.argsort(combined)[::-1][:top_k]
        return [self.chunks[i] for i in top_indices]

    def _contextualize_batch(self, document: str, chunks: list[str]) -> list[str]:
        """Generate context for all chunks (use prompt caching)."""
        results = []
        for chunk in chunks:
            context = self._generate_context(document, chunk)
            results.append(f"{context}\n\n{chunk}")
        return results

    def _generate_context(self, document: str, chunk: str) -> str:
        # Implementation from above
        pass

    def _chunk_text(self, text: str, chunk_size: int) -> list[str]:
        """Simple sentence-aware chunking."""
        sentences = text.split('. ')
        chunks = []
        current = []
        current_len = 0

        for sent in sentences:
            if current_len + len(sent) > chunk_size and current:
                chunks.append('. '.join(current) + '.')
                current = [sent]
                current_len = len(sent)
            else:
                current.append(sent)
                current_len += len(sent)

        if current:
            chunks.append('. '.join(current))
        return chunks

    def _rebuild_bm25(self):
        tokenized = [c.contextualized.lower().split() for c in self.chunks]
        self.bm25 = BM25Okapi(tokenized)

    def _normalize(self, scores: np.ndarray) -> np.ndarray:
        return (scores - scores.min()) / (scores.max() - scores.min() + 1e-6)
```

## Optimization Tips

### 1. Cost Reduction with Caching
```python
# Prompt caching reduces cost by ~90% when processing
# many chunks from the same document
# Document cached on first request, reused for subsequent chunks
```

### 2. Parallel Processing
```python
import asyncio

async def contextualize_parallel(document: str, chunks: list[str]) -> list[str]:
    """Process chunks in parallel with rate limiting."""
    semaphore = asyncio.Semaphore(10)  # Max 10 concurrent

    async def process_chunk(chunk: str) -> str:
        async with semaphore:
            context = await async_generate_context(document, chunk)
            return f"{context}\n\n{chunk}"

    return await asyncio.gather(*[process_chunk(c) for c in chunks])
```

### 3. Context Quality
```python
# Good context examples:
"This chunk is from the API authentication section of the FastAPI documentation."
"This describes the company's Q3 2024 financial performance, specifically operating expenses."
"This section covers error handling in the user registration flow."

# Bad context (too generic):
"This is a chunk from the document."
"Information about the topic."
```

## Results (from Anthropic's research)

| Method | Retrieval Failure Rate |
|--------|----------------------|
| Traditional embeddings | 5.7% |
| + Contextual embeddings | 3.5% |
| + Contextual + BM25 hybrid | 1.9% |
| + Contextual + BM25 + reranking | 1.3% |

**67% reduction in retrieval failures** with full contextual retrieval pipeline.

## When to Use

**Use Contextual Retrieval when**:
- Documents have important metadata (dates, names, versions)
- Chunks frequently lose meaning without document context
- Retrieval quality is critical (customer-facing, compliance)
- You can afford the additional LLM cost during indexing

**Skip if**:
- Chunks are self-contained (Q&A pairs, definitions)
- Low latency indexing required (high-volume streaming)
- Cost-sensitive with many small documents

## Related Skills

- `rag-retrieval` - Core RAG pipeline patterns that contextual retrieval enhances
- `embeddings` - Text embedding strategies for the vector search component
- `reranking-patterns` - Post-retrieval reranking to further improve precision
- `hyde-retrieval` - Alternative retrieval enhancement using hypothetical documents

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Context generation model | Claude Sonnet | Balance of quality and cost for context generation |
| BM25/Vector weight split | 40%/60% | Anthropic research shows slight vector bias optimal |
| Chunk context length | 1-2 sentences | Enough context without excessive token overhead |
| Prompt caching | Ephemeral cache | 90% cost reduction when processing many chunks from same doc |

## Resources
- Anthropic Blog: https://www.anthropic.com/news/contextual-retrieval
- Prompt Caching: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching