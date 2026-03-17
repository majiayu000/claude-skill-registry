---
name: "RAG Architecture Skill"
description: "Build retrieval-augmented generation systems that ground LLMs in your data."
applyTo: "**/*rag*,**/*retrieval*,**/*embedding*,**/*vector*,**/*knowledge*,**/*search*"
---

# RAG Architecture Skill

> Build retrieval-augmented generation systems that ground LLMs in your data.

## Core Principle

RAG = Retrieval + Generation. Instead of relying solely on the model's training data, retrieve relevant context at query time and include it in the prompt. This reduces hallucination and enables access to private/current data.

## RAG Pipeline

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Query     │────▶│   Embed     │────▶│  Retrieve   │────▶│   Augment   │
│  "How do I  │     │  Query to   │     │  Top-K      │     │  Add to     │
│   deploy?"  │     │  Vector     │     │  Documents  │     │  Prompt     │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                                                                   │
                                                                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Answer    │◀────│  Generate   │◀────│   Format    │◀────│  Context    │
│  Grounded   │     │  With LLM   │     │   Prompt    │     │  + Query    │
│  Response   │     │             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

## Indexing Pipeline

### Document Processing

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    Load      │────▶│    Clean     │────▶│    Chunk     │────▶│    Embed     │
│  Documents   │     │  & Parse     │     │   Content    │     │   Chunks     │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                      │
                                                                      ▼
                                                               ┌──────────────┐
                                                               │    Store     │
                                                               │  in Vector   │
                                                               │     DB       │
                                                               └──────────────┘
```

### Chunking Strategies

| Strategy | Description | Best For |
|----------|-------------|----------|
| Fixed Size | Split every N tokens/chars | Simple, predictable |
| Sentence | Split on sentence boundaries | Natural breaks |
| Paragraph | Split on paragraph breaks | Coherent units |
| Semantic | Split on topic changes | Meaningful segments |
| Recursive | Try large, fall back to smaller | Mixed content |
| Document | Keep whole documents | Short docs |

```python
# Recursive chunking example
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,  # Overlap prevents losing context at boundaries
    separators=["\n\n", "\n", ". ", " ", ""]
)

chunks = splitter.split_documents(documents)
```

### Chunk Size Tradeoffs

| Size | Pros | Cons |
|------|------|------|
| Small (100-500) | Precise retrieval | May lose context |
| Medium (500-1500) | Balanced | Good default |
| Large (1500-3000) | Full context | Less precise, costly |

**Rule of thumb**: Chunk should contain enough context to be useful standalone.

## Embedding Models

### Model Comparison

| Model | Dimensions | Speed | Quality | Cost |
|-------|------------|-------|---------|------|
| text-embedding-3-small | 1536 | Fast | Good | Low |
| text-embedding-3-large | 3072 | Medium | Best | Medium |
| ada-002 | 1536 | Fast | Good | Low |
| Cohere embed-v3 | 1024 | Fast | Good | Low |
| BGE-large | 1024 | Local | Good | Free |
| E5-large | 1024 | Local | Good | Free |

### Embedding Best Practices

```python
# Normalize embeddings for cosine similarity
import numpy as np

def normalize(embedding):
    return embedding / np.linalg.norm(embedding)

# Batch embeddings for efficiency
embeddings = embed_model.embed_documents(chunks)  # Not one at a time

# Cache embeddings - don't re-embed unchanged content
```

## Vector Databases

### Options

| Database | Type | Strengths | Use Case |
|----------|------|-----------|----------|
| Pinecone | Managed | Easy, scalable | Production |
| Weaviate | Managed/Self | Hybrid search | Enterprise |
| Qdrant | Self-hosted | Performance | Privacy-sensitive |
| Chroma | Embedded | Simple, local | Prototyping |
| pgvector | PostgreSQL ext | SQL + vectors | Existing Postgres |
| Azure AI Search | Managed | M365 integration | Azure ecosystem |
| FAISS | Library | Fast, offline | Local/research |

### Index Types

| Index | Speed | Accuracy | Memory |
|-------|-------|----------|--------|
| Flat (exact) | Slow | 100% | High |
| IVF | Fast | ~95% | Medium |
| HNSW | Very fast | ~98% | High |
| PQ | Very fast | ~90% | Low |

## Retrieval Strategies

### Basic Retrieval

```python
# Simple top-k retrieval
results = vector_store.similarity_search(query, k=5)
```

### Hybrid Search

Combine semantic (vector) with keyword (BM25) search:

```python
# Reciprocal Rank Fusion
def hybrid_search(query, k=5, alpha=0.5):
    semantic_results = vector_search(query, k=k*2)
    keyword_results = bm25_search(query, k=k*2)

    # Fuse rankings
    scores = {}
    for rank, doc in enumerate(semantic_results):
        scores[doc.id] = scores.get(doc.id, 0) + alpha * (1 / (rank + 60))
    for rank, doc in enumerate(keyword_results):
        scores[doc.id] = scores.get(doc.id, 0) + (1-alpha) * (1 / (rank + 60))

    return sorted(scores.items(), key=lambda x: -x[1])[:k]
```

### Reranking

Two-stage retrieval for better precision:

```python
# Stage 1: Fast retrieval (get candidates)
candidates = vector_store.similarity_search(query, k=20)

# Stage 2: Rerank with cross-encoder (more accurate)
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
scores = reranker.predict([(query, doc.content) for doc in candidates])
reranked = sorted(zip(candidates, scores), key=lambda x: -x[1])[:5]
```

### Query Transformation

```python
# Hypothetical Document Embedding (HyDE)
def hyde_search(query):
    # Generate hypothetical answer
    hypothetical = llm.generate(f"Write a passage that answers: {query}")
    # Search using the hypothetical (often better match)
    return vector_store.similarity_search(hypothetical, k=5)

# Multi-query retrieval
def multi_query_search(query):
    # Generate query variations
    variations = llm.generate(f"Generate 3 different ways to ask: {query}")
    # Search with each, combine results
    all_results = []
    for q in variations:
        all_results.extend(vector_store.similarity_search(q, k=3))
    return deduplicate(all_results)
```

## Prompt Augmentation

### Basic RAG Prompt

```
Use the following context to answer the question. If the context doesn't
contain the answer, say "I don't have information about that."

Context:
{retrieved_documents}

Question: {user_query}

Answer:
```

### Structured RAG Prompt

```
You are answering questions based on the provided documentation.

RULES:
1. Only use information from the provided context
2. Quote relevant passages when possible
3. If the context doesn't contain the answer, say so
4. If information is partial, acknowledge limitations

CONTEXT:
---
Source: {doc1.source}
{doc1.content}
---
Source: {doc2.source}
{doc2.content}
---

QUESTION: {query}

Provide your answer with citations to the source documents.
```

### Citation Handling

```python
# Include source metadata
for i, doc in enumerate(retrieved_docs):
    context += f"[{i+1}] Source: {doc.metadata['source']}\n{doc.content}\n\n"

# Prompt for citations
prompt += "\nCite sources using [1], [2], etc."
```

## Advanced Patterns

### Parent Document Retrieval

Store small chunks for retrieval, but return larger parent context:

```python
# Index small chunks (e.g., 200 tokens)
# But store mapping to parent (e.g., full section)

def retrieve_with_parent(query):
    small_chunks = vector_store.search(query, k=3)
    parent_ids = set(chunk.metadata['parent_id'] for chunk in small_chunks)
    return [doc_store.get(pid) for pid in parent_ids]
```

### Self-Query Retrieval

Let LLM write the filter query:

```python
# User: "What did we decide about authentication in 2024?"
# LLM generates: {"filter": {"year": 2024, "topic": "authentication"}}

retriever = SelfQueryRetriever(
    llm=llm,
    vectorstore=vectorstore,
    document_content_description="Meeting notes and decisions",
    metadata_field_info=[
        {"name": "year", "type": "integer"},
        {"name": "topic", "type": "string"},
    ]
)
```

### Agentic RAG

Let an agent decide when/what to retrieve:

```python
tools = [
    Tool("search_docs", "Search internal documentation", search_function),
    Tool("search_web", "Search the web for current info", web_search),
    Tool("search_code", "Search codebase", code_search),
]

agent = Agent(
    llm=llm,
    tools=tools,
    system_prompt="Decide which sources to search based on the question."
)
```

## Evaluation Metrics

### Retrieval Quality

| Metric | Measures | Formula |
|--------|----------|---------|
| Recall@K | Found relevant docs | Relevant in top-K / Total relevant |
| Precision@K | Top-K accuracy | Relevant in top-K / K |
| MRR | Rank of first relevant | 1 / rank of first relevant |
| NDCG | Ranking quality | Normalized discounted cumulative gain |

### Generation Quality

| Metric | Measures | How |
|--------|----------|-----|
| Faithfulness | Grounded in context | Check claims against sources |
| Relevance | Answers the question | Human evaluation |
| Completeness | Covers all aspects | Human evaluation |
| Hallucination rate | Made-up facts | Compare to source docs |

### RAG Evaluation Tools

```python
# Using ragas library
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

results = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_precision]
)
```

## Common Pitfalls

| Pitfall | Symptom | Solution |
|---------|---------|----------|
| Chunks too small | Answers lack context | Increase chunk size or use parent retrieval |
| Chunks too large | Irrelevant content included | Decrease size, improve chunking |
| Wrong K value | Too much/little context | Tune K based on evaluation |
| No metadata | Can't filter results | Add source, date, topic metadata |
| Stale index | Outdated answers | Implement refresh pipeline |
| Ignoring retrieved context | Hallucinations | Improve prompt, lower temperature |

## Production Considerations

### Caching

```python
# Cache embeddings
embedding_cache = {}
def get_embedding(text):
    if text not in embedding_cache:
        embedding_cache[text] = embed_model.embed(text)
    return embedding_cache[text]

# Cache frequent queries
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_search(query_hash):
    return vector_store.search(query, k=5)
```

### Monitoring

```python
# Log retrieval quality
logger.info({
    "query": query,
    "retrieved_docs": [d.id for d in results],
    "retrieval_time_ms": elapsed,
    "rerank_time_ms": rerank_elapsed,
    "total_time_ms": total_elapsed
})
```

### Cost Optimization

| Optimization | Savings |
|--------------|---------|
| Batch embeddings | API calls |
| Cache frequent queries | Compute + API |
| Use smaller embedding model | API cost |
| Compress vectors (PQ) | Storage |
| Filter before semantic search | Compute |

## Synapses

See [synapses.json](synapses.json) for connections.
