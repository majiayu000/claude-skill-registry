---
name: rag-retrieval
description: Retrieval-Augmented Generation patterns for grounded LLM responses. Use when building RAG pipelines, constructing context from retrieved documents, adding citations, or implementing hybrid search.
context: fork
agent: data-pipeline-engineer
version: 1.0.0
author: SkillForge
user-invocable: false
---

# RAG Retrieval

Combine vector search with LLM generation for accurate, grounded responses.

## Basic RAG Pattern

```python
async def rag_query(question: str, top_k: int = 5) -> str:
    """Basic RAG: retrieve then generate."""
    # 1. Retrieve relevant documents
    docs = await vector_db.search(question, limit=top_k)

    # 2. Construct context
    context = "\n\n".join([
        f"[{i+1}] {doc.text}"
        for i, doc in enumerate(docs)
    ])

    # 3. Generate with context
    response = await llm.chat([
        {"role": "system", "content":
            "Answer using ONLY the provided context. "
            "If not in context, say 'I don't have that information.'"},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ])

    return response.content
```

## RAG with Citations

```python
async def rag_with_citations(question: str) -> dict:
    """RAG with inline citations [1], [2], etc."""
    docs = await vector_db.search(question, limit=5)

    context = "\n\n".join([
        f"[{i+1}] {doc.text}\nSource: {doc.metadata['source']}"
        for i, doc in enumerate(docs)
    ])

    response = await llm.chat([
        {"role": "system", "content":
            "Answer with inline citations like [1], [2]. "
            "End with a Sources section."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ])

    return {
        "answer": response.content,
        "sources": [doc.metadata['source'] for doc in docs]
    }
```

## Hybrid Search (Semantic + Keyword)

```python
def reciprocal_rank_fusion(
    semantic_results: list,
    keyword_results: list,
    k: int = 60
) -> list:
    """Combine semantic and keyword search with RRF."""
    scores = {}

    for rank, doc in enumerate(semantic_results):
        scores[doc.id] = scores.get(doc.id, 0) + 1 / (k + rank + 1)

    for rank, doc in enumerate(keyword_results):
        scores[doc.id] = scores.get(doc.id, 0) + 1 / (k + rank + 1)

    # Sort by combined score
    ranked_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    return [get_doc(id) for id in ranked_ids]
```

## Context Window Management

```python
def fit_context(docs: list, max_tokens: int = 6000) -> list:
    """Truncate context to fit token budget."""
    total_tokens = 0
    selected = []

    for doc in docs:
        doc_tokens = count_tokens(doc.text)
        if total_tokens + doc_tokens > max_tokens:
            break
        selected.append(doc)
        total_tokens += doc_tokens

    return selected
```

**Guidelines:**
- Keep context under 75% of model limit
- Reserve tokens for system prompt + response
- Prioritize highest-relevance documents

## Context Sufficiency Check (2026 Best Practice)

```python
from pydantic import BaseModel

class SufficiencyCheck(BaseModel):
    """Pre-generation context validation."""
    is_sufficient: bool
    confidence: float  # 0.0-1.0
    missing_info: str | None = None

async def rag_with_sufficiency(question: str, top_k: int = 5) -> str:
    """RAG with hallucination prevention via sufficiency check.

    Based on Google Research ICLR 2025: Adding a sufficiency check
    before generation reduces hallucinations from insufficient context.
    """
    docs = await vector_db.search(question, limit=top_k)
    context = "\n\n".join([f"[{i+1}] {doc.text}" for i, doc in enumerate(docs)])

    # Pre-generation sufficiency check (prevents hallucination)
    check = await llm.with_structured_output(SufficiencyCheck).ainvoke(
        f"""Does this context contain sufficient information to answer the question?

Question: {question}

Context:
{context}

Evaluate:
- is_sufficient: Can the question be fully answered from context?
- confidence: How confident are you? (0.0-1.0)
- missing_info: What's missing if not sufficient?"""
    )

    # Abstain if context insufficient (high-confidence)
    if not check.is_sufficient and check.confidence > 0.7:
        return f"I don't have enough information to answer this question. Missing: {check.missing_info}"

    # Low confidence → retrieve more context
    if not check.is_sufficient and check.confidence <= 0.7:
        more_docs = await vector_db.search(question, limit=top_k * 2)
        context = "\n\n".join([f"[{i+1}] {doc.text}" for i, doc in enumerate(more_docs)])

    # Generate only with sufficient context
    response = await llm.chat([
        {"role": "system", "content":
            "Answer using ONLY the provided context. "
            "If information is missing, say so rather than guessing."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ])

    return response.content
```

**Why this matters (Google Research 2025):**
- RAG paradoxically increases hallucinations when context is insufficient
- Additional context increases model confidence → more likely to hallucinate
- Sufficiency check allows abstention when information is missing

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Top-k | 3-10 documents |
| Temperature | 0.1-0.3 (factual) |
| Context budget | 4K-8K tokens |
| Hybrid ratio | 50/50 semantic/keyword |

## Common Mistakes

- No citation tracking (unverifiable answers)
- Context too large (dilutes relevance)
- Temperature too high (hallucinations)
- Single retrieval method (misses keyword matches)

## Advanced Patterns

See `references/advanced-rag.md` for:
- **HyDE Integration**: Hypothetical document embeddings for vocabulary mismatch
- **Agentic RAG**: Multi-step retrieval with tool use
- **Self-RAG**: LLM decides when to retrieve and validates outputs
- **Corrective RAG**: Evaluate retrieval quality and correct if needed
- **Pipeline Composition**: Combine HyDE + Hybrid + Rerank

## Related Skills

- `embeddings` - Creating vectors for retrieval
- `hyde-retrieval` - Hypothetical document embeddings
- `query-decomposition` - Multi-concept query handling
- `reranking-patterns` - Cross-encoder and LLM reranking
- `contextual-retrieval` - Anthropic's context-prepending technique
- `langgraph-functional` - Building agentic RAG workflows

## Capability Details

### retrieval-patterns
**Keywords:** retrieval, context, chunks, relevance
**Solves:**
- Retrieve relevant context for LLM
- Implement RAG pipeline
- Optimize retrieval quality

### hybrid-search
**Keywords:** hybrid, bm25, vector, fusion
**Solves:**
- Combine keyword and semantic search
- Implement reciprocal rank fusion
- Balance precision and recall

### chatbot-example
**Keywords:** chatbot, rag, example, typescript
**Solves:**
- Build RAG chatbot example
- TypeScript implementation
- End-to-end RAG pipeline

### pipeline-template
**Keywords:** pipeline, template, implementation, starter
**Solves:**
- RAG pipeline starter template
- Production-ready code
- Copy-paste implementation
