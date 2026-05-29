---
name: rag-patterns
description: Chunking strategies, embedding model selection, hybrid search, reranking, eval metrics
---

# RAG Patterns

## Chunking Strategies

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Strategy 1: Recursive character splitting (general purpose)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=64,
    separators=["\n\n", "\n", ". ", " ", ""],
    length_function=len,
)

# Strategy 2: Semantic chunking (better coherence)
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

semantic_splitter = SemanticChunker(
    OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=95,
)

# Strategy 3: Parent-child chunking (preserves context)
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)

parent_docs = parent_splitter.split_documents(documents)
for parent in parent_docs:
    children = child_splitter.split_documents([parent])
    for child in children:
        child.metadata["parent_id"] = parent.metadata["id"]
```

## Embedding Model Selection

```yaml
Models by Use Case:
  General (English):
    - text-embedding-3-small (OpenAI, 1536d, cheap)
    - text-embedding-3-large (OpenAI, 3072d, best quality)
    - all-MiniLM-L6-v2 (local, 384d, fast)
  Code:
    - text-embedding-3-large with code-tuned prompts
    - voyage-code-2 (Voyage AI)
  Multilingual:
    - multilingual-e5-large (local)
    - text-embedding-3-large (OpenAI)

Selection Criteria:
  - Latency requirement < 50ms → local model
  - Quality critical → text-embedding-3-large
  - Budget constrained → text-embedding-3-small
  - Air-gapped → all-MiniLM-L6-v2
```

## Hybrid Search (Vector + BM25)

```python
from rank_bm25 import BM25Okapi
import numpy as np

class HybridRetriever:
    def __init__(self, vector_store, documents, alpha=0.5):
        self.vector_store = vector_store
        self.alpha = alpha  # 0=BM25 only, 1=vector only
        tokenized = [doc.page_content.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized)
        self.documents = documents

    def search(self, query: str, k: int = 10) -> list:
        # Vector search
        vector_results = self.vector_store.similarity_search_with_score(query, k=k)
        vector_scores = {doc.metadata["id"]: score for doc, score in vector_results}

        # BM25 search
        bm25_scores_raw = self.bm25.get_scores(query.lower().split())
        bm25_max = max(bm25_scores_raw) if max(bm25_scores_raw) > 0 else 1
        bm25_scores = {
            self.documents[i].metadata["id"]: score / bm25_max
            for i, score in enumerate(bm25_scores_raw)
        }

        # Reciprocal Rank Fusion
        all_ids = set(vector_scores) | set(bm25_scores)
        fused = {}
        for doc_id in all_ids:
            v_score = vector_scores.get(doc_id, 0)
            b_score = bm25_scores.get(doc_id, 0)
            fused[doc_id] = self.alpha * v_score + (1 - self.alpha) * b_score

        sorted_ids = sorted(fused, key=fused.get, reverse=True)[:k]
        return [self._get_doc(did) for did in sorted_ids]
```

## Reranking

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query: str, documents: list, top_k: int = 5) -> list:
    pairs = [(query, doc.page_content) for doc in documents]
    scores = reranker.predict(pairs)
    ranked = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in ranked[:top_k]]

# Pipeline: retrieve 20 → rerank to 5
candidates = hybrid_retriever.search(query, k=20)
final = rerank(query, candidates, top_k=5)
```

## Evaluation Metrics

```python
def evaluate_rag(queries, expected_answers, retriever, generator):
    metrics = {"retrieval_recall": [], "answer_correctness": [], "faithfulness": []}

    for query, expected in zip(queries, expected_answers):
        retrieved = retriever.search(query, k=5)
        retrieved_texts = [d.page_content for d in retrieved]

        # Retrieval recall: did we find the right chunks?
        relevant_found = any(expected["source"] in t for t in retrieved_texts)
        metrics["retrieval_recall"].append(1.0 if relevant_found else 0.0)

        # Generate answer
        answer = generator.generate(query, retrieved_texts)

        # Faithfulness: is answer grounded in retrieved context?
        # (Use LLM-as-judge or NLI model)
        metrics["faithfulness"].append(check_faithfulness(answer, retrieved_texts))

        # Correctness: does answer match expected?
        metrics["answer_correctness"].append(check_correctness(answer, expected["answer"]))

    return {k: sum(v) / len(v) for k, v in metrics.items()}
```

## Checklist

- [ ] Chunk size tuned for domain (code: 1000+, prose: 300-500)
- [ ] Chunk overlap prevents context loss at boundaries
- [ ] Metadata preserved (source, page, section) for attribution
- [ ] Hybrid search combines vector + keyword for robustness
- [ ] Reranker applied before final context assembly
- [ ] Context window budget managed (don't exceed LLM limit)
- [ ] Evaluation pipeline with retrieval recall + faithfulness
- [ ] Embedding model benchmarked on domain-specific queries

## Anti-Patterns

- Chunking without overlap (losing context at boundaries)
- Using only vector search (misses exact keyword matches)
- Stuffing all retrieved chunks into prompt (exceeds context window)
- No evaluation pipeline (can't measure improvements)
- Embedding queries and documents with different models
- Ignoring metadata filtering before vector search
- Not handling empty retrieval results gracefully
