---
name: using-vector-databases
description: Vector database implementation for AI/ML applications, semantic search, and RAG systems. Use when building chatbots, search engines, recommendation systems, or similarity-based retrieval. Covers Qdrant (primary), Pinecone, Milvus, pgvector, Chroma, embedding generation (OpenAI, Voyage, Cohere), chunking strategies, and hybrid search patterns.
---

# Vector Databases for AI Applications

## When to Use This Skill

Use this skill when implementing:
- **RAG (Retrieval-Augmented Generation)** systems for AI chatbots
- **Semantic search** capabilities (meaning-based, not just keyword)
- **Recommendation systems** based on similarity
- **Multi-modal AI** (unified search across text, images, audio)
- **Document similarity** and deduplication
- **Question answering** over private knowledge bases

## Quick Decision Framework

### 1. Vector Database Selection

```
START: Choosing a Vector Database

EXISTING INFRASTRUCTURE?
├─ Using PostgreSQL already?
│  └─ pgvector (<10M vectors, tight budget)
│      See: references/pgvector.md
│
└─ No existing vector database?
   │
   ├─ OPERATIONAL PREFERENCE?
   │  │
   │  ├─ Zero-ops managed only
   │  │  └─ Pinecone (fully managed, excellent DX)
   │  │      See: references/pinecone.md
   │  │
   │  └─ Flexible (self-hosted or managed)
   │     │
   │     ├─ SCALE: <100M vectors + complex filtering ⭐
   │     │  └─ Qdrant (RECOMMENDED)
   │     │      • Best metadata filtering
   │     │      • Built-in hybrid search (BM25 + Vector)
   │     │      • Self-host: Docker/K8s
   │     │      • Managed: Qdrant Cloud
   │     │      See: references/qdrant.md
   │     │
   │     ├─ SCALE: >100M vectors + GPU acceleration
   │     │  └─ Milvus / Zilliz Cloud
   │     │      See: references/milvus.md
   │     │
   │     ├─ Embedded / No server
   │     │  └─ LanceDB (serverless, edge deployment)
   │     │
   │     └─ Local prototyping
   │        └─ Chroma (simple API, in-memory)
```

### 2. Embedding Model Selection

```
REQUIREMENTS?

├─ Best quality (cost no object)
│  └─ Voyage AI voyage-3 (1024d)
│      • 9.74% better than OpenAI on MTEB
│      • ~$0.12/1M tokens
│      See: references/embedding-strategies.md
│
├─ Enterprise reliability
│  └─ OpenAI text-embedding-3-large (3072d)
│      • Industry standard
│      • ~$0.13/1M tokens
│      • Maturity shortening: reduce to 256/512/1024d
│
├─ Cost-optimized
│  └─ OpenAI text-embedding-3-small (1536d)
│      • ~$0.02/1M tokens (6x cheaper)
│      • 90-95% of large model performance
│
├─ Multilingual (100+ languages)
│  └─ Cohere embed-v3 (1024d)
│      • ~$0.10/1M tokens
│
└─ Self-hosted / Privacy-critical
   ├─ English: nomic-embed-text-v1.5 (768d, Apache 2.0)
   ├─ Multilingual: BAAI/bge-m3 (1024d, MIT)
   └─ Long docs: jina-embeddings-v2 (768d, 8K context)
```

## Core Concepts

### Document Chunking Strategy

**Recommended defaults for most RAG systems:**
- **Chunk size:** 512 tokens (not characters)
- **Overlap:** 50 tokens (10% overlap)

**Why these numbers?**
- 512 tokens balances context vs. precision
  - Too small (128-256): Fragments concepts, loses context
  - Too large (1024-2048): Dilutes relevance, wastes LLM tokens
- 50 token overlap ensures sentences aren't split mid-context

See `references/chunking-patterns.md` for advanced strategies by content type.

### Hybrid Search (Vector + Keyword)

**Hybrid Search = Vector Similarity + BM25 Keyword Matching**

```
User Query: "OAuth refresh token implementation"
           │
    ┌──────┴──────┐
    │             │
Vector Search   Keyword Search
(Semantic)      (BM25)
    │             │
Top 20 docs   Top 20 docs
    │             │
    └──────┬──────┘
           │
   Reciprocal Rank Fusion
   (Merge + Re-rank)
           │
    Final Top 5 Results
```

**Why hybrid matters:**
- Vector captures semantic meaning ("OAuth refresh" ≈ "token renewal")
- Keyword ensures exact matches ("refresh_token" literal)
- Combined provides best retrieval quality

See `references/hybrid-search.md` for implementation details.

## Getting Started

### Python + Qdrant Example

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# 1. Initialize client
client = QdrantClient("localhost", port=6333)

# 2. Create collection
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
)

# 3. Insert documents with embeddings
points = [
    PointStruct(
        id=idx,
        vector=embedding,  # From OpenAI/Voyage/etc
        payload={
            "text": chunk_text,
            "source": "docs/api.md",
            "section": "Authentication"
        }
    )
    for idx, (embedding, chunk_text) in enumerate(chunks)
]
client.upsert(collection_name="documents", points=points)

# 4. Search with metadata filtering
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    limit=5,
    query_filter={
        "must": [
            {"key": "section", "match": {"value": "Authentication"}}
        ]
    }
)
```

For complete examples, see `examples/qdrant-python/`.

### TypeScript + Qdrant Example

```typescript
import { QdrantClient } from '@qdrant/js-client-rest';

const client = new QdrantClient({ url: 'http://localhost:6333' });

// Create collection
await client.createCollection('documents', {
  vectors: { size: 1024, distance: 'Cosine' }
});

// Insert documents
await client.upsert('documents', {
  points: chunks.map((chunk, idx) => ({
    id: idx,
    vector: chunk.embedding,
    payload: {
      text: chunk.text,
      source: chunk.source
    }
  }))
});

// Search
const results = await client.search('documents', {
  vector: queryEmbedding,
  limit: 5,
  filter: {
    must: [
      { key: 'source', match: { value: 'docs/api.md' } }
    ]
  }
});
```

For complete examples, see `examples/typescript-rag/`.

## RAG Pipeline Architecture

### Complete Pipeline Components

```
1. INGESTION
   ├─ Document Loading (PDF, web, code, Office)
   ├─ Text Extraction & Cleaning
   ├─ Chunking (semantic, recursive, code-aware)
   └─ Embedding Generation (batch, rate-limited)

2. INDEXING
   ├─ Vector Store Insertion (batch upsert)
   ├─ Index Configuration (HNSW, distance metric)
   └─ Keyword Index (BM25 for hybrid search)

3. RETRIEVAL (Query Time)
   ├─ Query Processing (expansion, embedding)
   ├─ Hybrid Search (vector + keyword)
   ├─ Filtering & Post-Processing (metadata, MMR)
   └─ Re-Ranking (cross-encoder, LLM-based)

4. GENERATION
   ├─ Context Construction (format chunks, citations)
   ├─ Prompt Engineering (system + context + query)
   ├─ LLM Inference (streaming, temperature tuning)
   └─ Response Post-Processing (citations, validation)

5. EVALUATION (Production Critical)
   ├─ Retrieval Metrics (precision, recall, relevancy)
   ├─ Generation Metrics (faithfulness, correctness)
   └─ System Metrics (latency, cost, satisfaction)
```

## Essential Metadata for Production RAG

**Critical for filtering and relevance:**

```python
metadata = {
    # SOURCE TRACKING
    "source": "docs/api-reference.md",
    "source_type": "documentation",  # code, docs, logs, chat
    "last_updated": "2025-12-01T12:00:00Z",

    # HIERARCHICAL CONTEXT
    "section": "Authentication",
    "subsection": "OAuth 2.1",
    "heading_hierarchy": ["API Reference", "Authentication", "OAuth 2.1"],

    # CONTENT CLASSIFICATION
    "content_type": "code_example",  # prose, code, table, list
    "programming_language": "python",

    # FILTERING DIMENSIONS
    "product_version": "v2.0",
    "audience": "enterprise",  # free, pro, enterprise

    # RETRIEVAL HINTS
    "chunk_index": 3,
    "total_chunks": 12,
    "has_code": True
}
```

**Why metadata matters:**
- Enables filtering BEFORE vector search (reduces search space)
- Improves relevance through targeted retrieval
- Supports multi-tenant systems (filter by user/org)
- Enables versioned documentation (filter by product version)

## Evaluation with RAGAS

**Use scripts/evaluate_rag.py for automated evaluation:**

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,       # Answer grounded in context
    answer_relevancy,   # Answer addresses query
    context_recall,     # Retrieved docs cover ground truth
    context_precision   # Retrieved docs are relevant
)

# Test dataset
test_data = {
    "question": ["How do I refresh OAuth tokens?"],
    "answer": ["Use /token with refresh_token grant..."],
    "contexts": [["OAuth refresh documentation..."]],
    "ground_truth": ["POST to /token with grant_type=refresh_token"]
}

# Evaluate
results = evaluate(test_data, metrics=[
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision
])

# Production targets:
# faithfulness: >0.90 (minimal hallucination)
# answer_relevancy: >0.85 (addresses user query)
# context_recall: >0.80 (sufficient context retrieved)
# context_precision: >0.75 (minimal noise)
```

## Performance Optimization

### Embedding Generation
- **Batch processing:** 100-500 chunks per batch
- **Caching:** Cache embeddings by content hash
- **Rate limiting:** Respect API provider limits (exponential backoff)

### Vector Search
- **Index type:** HNSW (Hierarchical Navigable Small World) for most cases
- **Distance metric:** Cosine for normalized embeddings
- **Pre-filtering:** Apply metadata filters before vector search
- **Result diversity:** Use MMR (Maximal Marginal Relevance) to reduce redundancy

### Cost Optimization
- **Embedding model:** Consider text-embedding-3-small for budget constraints
- **Dimension reduction:** Use maturity shortening (3072d → 1024d)
- **Caching:** Implement semantic caching for repeated queries
- **Batch operations:** Group insertions/updates for efficiency

## Common Workflows

### 1. Building a RAG Chatbot
- Vector database: Qdrant (self-hosted or cloud)
- Embeddings: OpenAI text-embedding-3-large
- Chunking: 512 tokens, 50 overlap, semantic splitter
- Search: Hybrid (vector + BM25)
- Integration: Frontend with ai-chat skill

See `examples/qdrant-python/` for complete implementation.

### 2. Semantic Search Engine
- Vector database: Qdrant or Pinecone
- Embeddings: Voyage AI voyage-3 (best quality)
- Chunking: Content-type specific (see chunking-patterns.md)
- Search: Hybrid with re-ranking
- Filtering: Pre-filter by metadata (date, category, etc.)

### 3. Code Search
- Vector database: Qdrant
- Embeddings: OpenAI text-embedding-3-large
- Chunking: AST-based (function/class boundaries)
- Metadata: Language, file path, imports
- Search: Hybrid with language filtering

See `examples/qdrant-python/` for code-specific implementation.

## Integration with Other Skills

### Frontend Skills
- **ai-chat**: Vector DB powers RAG pipeline behind chat interface
- **search-filter**: Replace keyword search with semantic search
- **data-viz**: Visualize embedding spaces, similarity scores

### Backend Skills
- **databases-relational**: Hybrid approach using pgvector extension
- **api-patterns**: Expose semantic search via REST/GraphQL
- **observability**: Monitor embedding quality and retrieval metrics

## Multi-Language Support

### Python (Primary)
- Client: `qdrant-client`
- Framework: LangChain, LlamaIndex
- See: `examples/qdrant-python/`

### Rust
- Client: `qdrant-client` (1,549 code snippets in Context7)
- Framework: Raw Rust for performance-critical systems
- See: `examples/rust-axum-vector/`

### TypeScript
- Client: `@qdrant/js-client-rest`
- Framework: LangChain.js, integration with Next.js
- See: `examples/typescript-rag/`

### Go
- Client: `qdrant-go`
- Use case: High-performance microservices

## Troubleshooting

### Poor Retrieval Quality
1. Check chunking strategy (too large/small?)
2. Verify metadata filtering (too restrictive?)
3. Try hybrid search instead of vector-only
4. Implement re-ranking stage
5. Evaluate with RAGAS metrics

### Slow Performance
1. Use HNSW index (not Flat)
2. Pre-filter with metadata before vector search
3. Reduce vector dimensions (maturity shortening)
4. Batch operations (insertions, searches)
5. Consider GPU acceleration (Milvus)

### High Costs
1. Switch to text-embedding-3-small
2. Implement semantic caching
3. Reduce chunk overlap
4. Use self-hosted embeddings (nomic, bge-m3)
5. Batch embedding generation

## Qdrant Context7 Documentation

**Primary resource:** `/llmstxt/qdrant_tech_llms-full_txt`
- **Trust score:** High
- **Code snippets:** 10,154
- **Quality score:** 83.1

Access via Context7:
```
resolve-library-id({ libraryName: "Qdrant" })
get-library-docs({
  context7CompatibleLibraryID: "/llmstxt/qdrant_tech_llms-full_txt",
  topic: "hybrid search collections python",
  mode: "code"
})
```

## Additional Resources

### Reference Documentation
- `references/qdrant.md` - Comprehensive Qdrant guide
- `references/pgvector.md` - PostgreSQL pgvector extension
- `references/milvus.md` - Milvus/Zilliz for billion-scale
- `references/embedding-strategies.md` - Embedding model comparison
- `references/chunking-patterns.md` - Advanced chunking techniques

### Code Examples
- `examples/qdrant-python/` - FastAPI + Qdrant RAG pipeline
- `examples/pgvector-prisma/` - PostgreSQL + Prisma integration
- `examples/typescript-rag/` - TypeScript RAG with Hono

### Automation Scripts
- `scripts/generate_embeddings.py` - Batch embedding generation
- `scripts/benchmark_similarity.py` - Performance benchmarking
- `scripts/evaluate_rag.py` - RAGAS-based evaluation

---

**Next Steps:**
1. Choose vector database based on scale and infrastructure
2. Select embedding model based on quality vs. cost trade-off
3. Implement chunking strategy for the content type
4. Set up hybrid search for production quality
5. Evaluate with RAGAS metrics
6. Optimize for performance and cost
