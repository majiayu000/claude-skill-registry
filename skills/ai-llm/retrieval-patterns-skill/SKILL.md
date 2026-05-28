---
name: retrieval-patterns
version: 1.0
triggers: ["hybrid search", "MMR", "reranking", "retrieval"]
---

# Retrieval Patterns SKILL

## 1. Hybrid Search (BM25 + Semantic)

```python
from langchain.retrievers import EnsembleRetriever

ensemble = EnsembleRetriever(
    retrievers=[bm25_retriever, semantic_retriever],
    weights=[0.5, 0.5]
)
```

## 2. MMR (Maximal Marginal Relevance)

```python
retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "lambda_mult": 0.5}
)
```

## 3. Cross-Encoder Reranking

```python
from langchain.retrievers.document_compressors import CrossEncoderReranker

compressor = CrossEncoderReranker(
    model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
)
```
