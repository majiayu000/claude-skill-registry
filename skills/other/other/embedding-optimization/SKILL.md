---
name: embedding-optimization
description: Optimizing vector embeddings for RAG systems through model selection, chunking strategies, caching, and performance tuning. Use when building semantic search, RAG pipelines, or document retrieval systems that require cost-effective, high-quality embeddings.
---

# Embedding Optimization

Optimize embedding generation for cost, performance, and quality in RAG and semantic search systems.

## When to Use This Skill

Trigger this skill when:
- Building RAG (Retrieval Augmented Generation) systems
- Implementing semantic search or similarity detection
- Optimizing embedding API costs (reducing by 70-90%)
- Improving document retrieval quality through better chunking
- Processing large document corpora (thousands to millions of documents)
- Selecting between API-based vs. local embedding models

## Model Selection Framework

Choose the optimal embedding model based on requirements:

**Quick Recommendations:**
- **Startup/MVP:** `all-MiniLM-L6-v2` (local, 384 dims, zero API costs)
- **Production:** `text-embedding-3-small` (API, 1,536 dims, balanced quality/cost)
- **High Quality:** `text-embedding-3-large` (API, 3,072 dims, premium)
- **Multilingual:** `multilingual-e5-base` (local, 768 dims) or Cohere `embed-multilingual-v3.0`

For detailed decision frameworks including cost comparisons, quality benchmarks, and data privacy considerations, see `references/model-selection-guide.md`.

**Model Comparison Summary:**

| Model | Type | Dimensions | Cost per 1M tokens | Best For |
|-------|------|-----------|-------------------|----------|
| all-MiniLM-L6-v2 | Local | 384 | $0 (compute only) | High volume, tight budgets |
| BGE-base-en-v1.5 | Local | 768 | $0 (compute only) | Quality + cost balance |
| text-embedding-3-small | API | 1,536 | $0.02 | General purpose production |
| text-embedding-3-large | API | 3,072 | $0.13 | Premium quality requirements |
| embed-multilingual-v3.0 | API | 1,024 | $0.10 | 100+ language support |

## Chunking Strategies

Select chunking strategy based on content type and use case:

**Content Type → Strategy Mapping:**
- **Documentation:** Recursive (heading-aware), 800 chars, 100 overlap
- **Code:** Recursive (function-level), 1,000 chars, 100 overlap
- **Q&A/FAQ:** Fixed-size, 500 chars, 50 overlap (precise retrieval)
- **Legal/Technical:** Semantic (large), 1,500 chars, 200 overlap (context preservation)
- **Blog Posts:** Semantic (paragraph), 1,000 chars, 100 overlap
- **Academic Papers:** Recursive (section-aware), 1,200 chars, 150 overlap

For detailed chunking patterns, decision trees, and implementation guidance, see `references/chunking-strategies.md`.

**Quick Start with CLI:**
```bash
python scripts/chunk_document.py \
  --input document.txt \
  --content-type markdown \
  --chunk-size 800 \
  --overlap 100 \
  --output chunks.jsonl
```

## Caching Implementation

Achieve 80-90% cost reduction through content-addressable caching.

**Caching Architecture by Query Volume:**
- **<10K queries/month:** In-memory cache (Python `lru_cache`)
- **10K-100K queries/month:** Redis (fast, TTL-based expiration)
- **100K-1M queries/month:** Redis (hot) + PostgreSQL (warm)
- **>1M queries/month:** Multi-tier (Redis + PostgreSQL + S3)

**Production Caching with Redis:**
```bash
# Embed documents with caching enabled
python scripts/cached_embedder.py \
  --model text-embedding-3-small \
  --input documents.jsonl \
  --output embeddings.npy \
  --cache-backend redis \
  --cache-ttl 2592000  # 30 days
```

**Caching ROI Example:**
- 50,000 document chunks
- 20% duplicate content
- Without caching: $0.50 API cost
- With caching (60% hit rate): $0.20 API cost
- **Savings: 60% ($0.30)**

## Dimensionality Trade-offs

Balance storage, search speed, and quality:

| Dimensions | Storage (1M vectors) | Search Speed (p95) | Quality | Use Case |
|-----------|---------------------|-------------------|---------|----------|
| 384 | 1.5 GB | 10ms | Good | Large-scale search |
| 768 | 3 GB | 15ms | High | General purpose RAG |
| 1,536 | 6 GB | 25ms | Very High | High-quality retrieval |
| 3,072 | 12 GB | 40ms | Highest | Premium applications |

**Key Insight:** For most RAG applications, 768 dimensions (BGE-base-en-v1.5 local or equivalent) provides the best quality/cost/speed balance.

## Batch Processing Optimization

Maximize throughput for large-scale ingestion:

**OpenAI API:**
- Batch up to 2,048 inputs per request
- Implement rate limiting (tier-dependent: 500-5,000 RPM)
- Use parallel requests with backoff on rate limits

**Local Models (sentence-transformers):**
- GPU acceleration (CUDA, MPS for Apple Silicon)
- Batch size tuning (32-128 based on GPU memory)
- Multi-GPU support for maximum throughput

**Expected Throughput:**
- OpenAI API: 1,000-5,000 texts/minute (rate limit dependent)
- Local GPU (RTX 3090): 5,000-10,000 texts/minute
- Local CPU: 100-500 texts/minute

## Performance Monitoring

Track key metrics for optimization:

**Critical Metrics:**
- **Latency:** Embedding generation time (p50, p95, p99)
- **Throughput:** Embeddings per second/minute
- **Cost:** API usage tracking (USD per 1K/1M tokens)
- **Cache Efficiency:** Hit rate percentage

For detailed monitoring setup, metric collection patterns, and dashboarding, see `references/performance-monitoring.md`.

**Monitor with Wrapper:**
```python
from scripts.performance_monitor import MonitoredEmbedder

monitored = MonitoredEmbedder(
    embedder=your_embedder,
    cost_per_1k_tokens=0.00002  # OpenAI pricing
)

embeddings = monitored.embed_batch(texts)
metrics = monitored.get_metrics()
print(f"Cache hit rate: {metrics['cache_hit_rate_pct']}%")
print(f"Total cost: ${metrics['total_cost_usd']}")
```

## Working Examples

See `examples/` directory for complete implementations:

**Python Examples:**
- `examples/openai_cached.py` - OpenAI embeddings with Redis caching
- `examples/local_embedder.py` - sentence-transformers local embedding
- `examples/smart_chunker.py` - Content-aware recursive chunking
- `examples/performance_monitor.py` - Pipeline performance tracking
- `examples/batch_processor.py` - Large-scale document processing

All examples include:
- Complete, runnable code
- Dependency installation instructions
- Error handling and retry logic
- Configuration options

## Integration Points

**Upstream (This skill provides to):**
- **Vector Databases:** Embeddings flow to Pinecone, Weaviate, Qdrant, pgvector
- **RAG Systems:** Optimized embeddings for retrieval pipelines
- **Semantic Search:** Query and document embeddings for similarity search

**Downstream (This skill uses from):**
- **Document Processing:** Chunk documents before embedding
- **Data Ingestion:** Process documents from various sources

**Related Skills:**
- For RAG architecture, see `building-ai-chat` skill
- For vector database operations, see `databases-vector` skill
- For data ingestion pipelines, see `ingesting-data` skill

## Common Patterns

**Pattern 1: RAG Pipeline**
```
Document → Chunk → Embed → Store (vector DB) → Retrieve
```

**Pattern 2: Semantic Search**
```
Query → Embed → Search (vector DB) → Rank → Display
```

**Pattern 3: Multi-Stage Retrieval (Cost Optimization)**
```
Query → Cheap Embedding (384d) → Initial Search →
Expensive Embedding (1,536d) → Rerank Top-K → Return
```
**Cost Savings:** 70% reduction vs. single-stage with expensive embeddings

## Quick Reference Checklist

**Model Selection:**
- [ ] Identified data privacy requirements (local vs. API)
- [ ] Calculated expected query volume
- [ ] Determined quality requirements (good/high/highest)
- [ ] Checked multilingual support needs

**Chunking:**
- [ ] Analyzed content type (code, docs, legal, etc.)
- [ ] Selected appropriate chunk size (500-1,500 chars)
- [ ] Set overlap to prevent context loss (50-200 chars)
- [ ] Validated chunks preserve semantic boundaries

**Caching:**
- [ ] Implemented content-addressable hashing
- [ ] Selected cache backend (Redis, PostgreSQL)
- [ ] Set TTL based on content volatility
- [ ] Monitoring cache hit rate (target: >60%)

**Performance:**
- [ ] Tracking latency (embedding generation time)
- [ ] Measuring throughput (embeddings/sec)
- [ ] Monitoring costs (USD spent on API calls)
- [ ] Optimizing batch sizes for maximum efficiency
