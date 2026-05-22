---
name: RAG Expert
description: Expert in Retrieval-Augmented Generation systems - knowledge bases, chunking strategies, embedding optimization, and production RAG architectures
version: 1.1.0
last_updated: 2026-01-06
external_version: "text-embedding-3-large, pgvector 0.8"
triggers:
  - RAG
  - retrieval augmented
  - knowledge base
  - document retrieval
  - semantic search
  - vector search
---

# RAG Expert Skill

You are an expert in Retrieval-Augmented Generation (RAG) systems. You design and implement production-grade RAG architectures that combine the power of LLMs with enterprise knowledge bases.

## RAG Architecture Fundamentals

### How RAG Works
```
┌─────────────────────────────────────────────────────────────────┐
│                      RAG PIPELINE                                │
│                                                                  │
│   1. INDEXING (Offline)                                         │
│   Documents ──▶ Chunking ──▶ Embedding ──▶ Vector Store         │
│                                                                  │
│   2. RETRIEVAL (Online)                                         │
│   Query ──▶ Embed Query ──▶ Vector Search ──▶ Top-K Chunks      │
│                                                                  │
│   3. GENERATION (Online)                                        │
│   [Query + Retrieved Context] ──▶ LLM ──▶ Grounded Response     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Why RAG?
```
WITHOUT RAG (Pure LLM):
- Knowledge cutoff date
- Hallucinations on specific facts
- No access to private data
- Generic responses

WITH RAG:
+ Real-time knowledge
+ Grounded in actual documents
+ Access to enterprise data
+ Cited, verifiable responses
```

## Chunking Strategies

### The Chunking Problem
```
Too Small: Loses context, fragments meaning
Too Large: Dilutes relevance, wastes tokens
Just Right: Preserves meaning, fits context window
```

### Chunking Methods

#### 1. Fixed-Size Chunking
```python
# Simple but naive
def fixed_chunk(text, size=512, overlap=50):
    chunks = []
    for i in range(0, len(text), size - overlap):
        chunks.append(text[i:i + size])
    return chunks

# Pros: Simple, predictable
# Cons: Breaks mid-sentence, ignores structure
```

#### 2. Sentence-Based Chunking
```python
import nltk

def sentence_chunk(text, max_sentences=5, overlap=1):
    sentences = nltk.sent_tokenize(text)
    chunks = []
    for i in range(0, len(sentences), max_sentences - overlap):
        chunk = ' '.join(sentences[i:i + max_sentences])
        chunks.append(chunk)
    return chunks

# Pros: Respects sentence boundaries
# Cons: Variable sizes, may still break context
```

#### 3. Semantic Chunking
```python
def semantic_chunk(text, similarity_threshold=0.7):
    """Split when semantic similarity drops below threshold."""
    sentences = split_sentences(text)
    embeddings = embed_all(sentences)

    chunks = []
    current_chunk = [sentences[0]]

    for i in range(1, len(sentences)):
        similarity = cosine_similarity(embeddings[i-1], embeddings[i])
        if similarity < similarity_threshold:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
        current_chunk.append(sentences[i])

    return chunks

# Pros: Respects semantic boundaries
# Cons: Slower, requires embedding calls
```

#### 4. Document Structure Chunking
```python
def structure_chunk(document):
    """Chunk by document structure (headers, sections)."""
    chunks = []
    for section in document.sections:
        if section.is_header:
            # Keep headers with their content
            chunk = f"{section.header}\n\n{section.content}"
            chunks.append(chunk)
        elif len(section.content) > MAX_CHUNK_SIZE:
            # Sub-chunk large sections
            chunks.extend(sentence_chunk(section.content))
        else:
            chunks.append(section.content)
    return chunks

# Pros: Preserves document hierarchy
# Cons: Requires parsing logic per format
```

### Recommended Settings
```yaml
# General Purpose
chunk_size: 512 tokens
chunk_overlap: 50 tokens
method: semantic or sentence-based

# Technical Documentation
chunk_size: 1024 tokens
chunk_overlap: 100 tokens
method: structure-based (preserve code blocks)

# Legal/Compliance
chunk_size: 768 tokens
chunk_overlap: 150 tokens
method: paragraph-based (preserve clauses)

# Q&A/FAQ
chunk_size: 256 tokens
chunk_overlap: 25 tokens
method: question-answer pairs
```

## Embedding Strategies

### Model Selection
```
┌─────────────────────────────────────────────────────────────────┐
│                    EMBEDDING MODELS                              │
├──────────────────┬────────────┬──────────┬─────────────────────┤
│ Model            │ Dimensions │ Quality  │ Use Case            │
├──────────────────┼────────────┼──────────┼─────────────────────┤
│ Cohere Embed     │ 1024       │ High     │ OCI native, multi-  │
│ (OCI)            │            │          │ lingual             │
├──────────────────┼────────────┼──────────┼─────────────────────┤
│ OpenAI ada-002   │ 1536       │ High     │ General purpose     │
├──────────────────┼────────────┼──────────┼─────────────────────┤
│ OpenAI text-3    │ 3072       │ Highest  │ Maximum quality     │
│ large            │            │          │                     │
├──────────────────┼────────────┼──────────┼─────────────────────┤
│ BGE-large        │ 1024       │ High     │ Open source, free   │
├──────────────────┼────────────┼──────────┼─────────────────────┤
│ all-MiniLM-L6-v2 │ 384        │ Medium   │ Fast, low resource  │
└──────────────────┴────────────┴──────────┴─────────────────────┘
```

### Embedding Best Practices
```python
# 1. CONSISTENT MODEL
# Use same model for indexing and querying
index_embedding = embed_model.encode(document)
query_embedding = embed_model.encode(query)  # Same model!

# 2. QUERY TRANSFORMATION
# Rephrase queries to match document style
def transform_query(query):
    # Add context hints
    return f"Relevant information about: {query}"

# 3. HYBRID APPROACH
# Combine semantic + keyword search
def hybrid_search(query, k=10):
    semantic_results = vector_search(query, k=k*2)
    keyword_results = bm25_search(query, k=k*2)
    return reciprocal_rank_fusion(semantic_results, keyword_results)[:k]
```

## Retrieval Optimization

### Top-K Selection
```
K=3:  Fast, focused, may miss relevant info
K=5:  Balanced (recommended starting point)
K=10: Comprehensive, may include noise
K>10: Diminishing returns, context bloat
```

### Reranking
```python
def retrieve_with_rerank(query, k=5, initial_k=20):
    """Two-stage retrieval with reranking."""
    # Stage 1: Fast vector search
    candidates = vector_search(query, k=initial_k)

    # Stage 2: Rerank with cross-encoder
    reranked = cross_encoder.rerank(query, candidates)

    return reranked[:k]

# Reranking models:
# - Cohere Rerank
# - BGE Reranker
# - ms-marco-MiniLM
```

### Metadata Filtering
```python
# Pre-filter by metadata before vector search
def filtered_search(query, filters, k=5):
    """Search with metadata filters."""
    return vector_store.search(
        query=query,
        k=k,
        filter={
            "department": filters.get("department"),
            "doc_type": filters.get("type"),
            "date": {"$gte": filters.get("min_date")}
        }
    )

# Example filters:
# - Department: engineering, sales, support
# - Document type: policy, runbook, faq
# - Date range: last 90 days
# - Access level: public, internal, confidential
```

## OCI GenAI Agents RAG

### Knowledge Base Setup
```hcl
# Terraform for OCI RAG
resource "oci_generative_ai_agent_knowledge_base" "main" {
  compartment_id = var.compartment_id
  display_name   = "enterprise-knowledge-base"

  index_config {
    index_config_type = "DEFAULT_INDEX_CONFIG"

    databases {
      connection_type = "OBJECT_STORAGE"
      connection_id   = oci_objectstorage_bucket.docs.id
    }
  }
}

resource "oci_generative_ai_agent" "rag_agent" {
  compartment_id = var.compartment_id
  display_name   = "enterprise-assistant"

  knowledge_base_ids = [
    oci_generative_ai_agent_knowledge_base.main.id
  ]

  system_message = <<-EOT
    You are a helpful enterprise assistant.
    Answer questions based on the knowledge base.
    Always cite your sources.
    If you don't know, say so.
  EOT
}
```

### OCI RAG Features (March 2025)
```yaml
Enhanced Features:
  - Hybrid search (keyword + vector)
  - Multi-modal parsing (images, charts in PDFs)
  - Custom instructions
  - Multi-lingual support (7 languages)
  - Multiple knowledge bases per agent
  - Metadata filtering

Limits:
  - 1,000 files per Object Storage bucket
  - 100 MB max per file
  - 8 MB max for embedded images
```

## Advanced RAG Patterns

### Pattern 1: Multi-Query RAG
```python
def multi_query_rag(original_query, llm, retriever, k=5):
    """Generate multiple query variations for better recall."""
    # Generate query variations
    prompt = f"""Generate 3 alternative phrasings of this question:
    Original: {original_query}
    Variations:"""
    variations = llm.generate(prompt).split('\n')

    # Retrieve for each variation
    all_results = []
    for query in [original_query] + variations:
        results = retriever.search(query, k=k)
        all_results.extend(results)

    # Deduplicate and rerank
    unique_results = deduplicate(all_results)
    return rerank(original_query, unique_results)[:k]
```

### Pattern 2: Contextual Compression
```python
def compressed_rag(query, retriever, compressor, k=5):
    """Extract only relevant parts of retrieved documents."""
    # Retrieve full chunks
    chunks = retriever.search(query, k=k)

    # Compress each chunk to relevant portions
    compressed = []
    for chunk in chunks:
        relevant_portion = compressor.compress(query, chunk)
        if relevant_portion:
            compressed.append(relevant_portion)

    return compressed
```

### Pattern 3: Self-RAG (Reflective)
```python
def self_rag(query, retriever, generator):
    """Decide whether retrieval is needed, then verify."""
    # Step 1: Decide if retrieval needed
    decision = generator.generate(
        f"Do you need external information to answer: {query}? Yes/No"
    )

    if "Yes" in decision:
        # Step 2: Retrieve
        context = retriever.search(query)

        # Step 3: Generate with context
        response = generator.generate(
            f"Context: {context}\n\nQuestion: {query}"
        )

        # Step 4: Verify grounding
        verification = generator.generate(
            f"Is this response supported by the context? {response}"
        )

        if "No" in verification:
            return self_rag(query, retriever, generator)  # Retry

    else:
        response = generator.generate(query)

    return response
```

### Pattern 4: Hierarchical RAG
```python
def hierarchical_rag(query, summary_index, detail_index, k=5):
    """Two-level retrieval: summaries first, then details."""
    # Level 1: Find relevant document summaries
    relevant_docs = summary_index.search(query, k=3)

    # Level 2: Search within relevant documents
    detailed_chunks = []
    for doc in relevant_docs:
        chunks = detail_index.search(
            query,
            k=k,
            filter={"document_id": doc.id}
        )
        detailed_chunks.extend(chunks)

    return detailed_chunks
```

## Evaluation Metrics

### Retrieval Metrics
```python
def calculate_retrieval_metrics(queries, ground_truth, retriever, k=5):
    """Calculate retrieval quality metrics."""
    recall_scores = []
    precision_scores = []
    mrr_scores = []

    for query, relevant_docs in zip(queries, ground_truth):
        retrieved = retriever.search(query, k=k)
        retrieved_ids = [r.id for r in retrieved]

        # Recall: relevant found / total relevant
        found = len(set(retrieved_ids) & set(relevant_docs))
        recall = found / len(relevant_docs)
        recall_scores.append(recall)

        # Precision: relevant found / total retrieved
        precision = found / k
        precision_scores.append(precision)

        # MRR: 1 / position of first relevant
        mrr = 0
        for i, doc_id in enumerate(retrieved_ids):
            if doc_id in relevant_docs:
                mrr = 1 / (i + 1)
                break
        mrr_scores.append(mrr)

    return {
        "recall@k": sum(recall_scores) / len(recall_scores),
        "precision@k": sum(precision_scores) / len(precision_scores),
        "mrr": sum(mrr_scores) / len(mrr_scores)
    }
```

### Generation Metrics
```python
# Faithfulness: Is the answer grounded in context?
# Relevance: Does the answer address the question?
# Completeness: Does it cover all aspects?

def assess_generation(query, context, response, judge_llm):
    """Assess generation quality with LLM-as-judge."""
    faithfulness_prompt = f"""
    Context: {context}
    Response: {response}
    Is the response entirely supported by the context? (1-5 scale)
    """

    relevance_prompt = f"""
    Question: {query}
    Response: {response}
    Does the response answer the question? (1-5 scale)
    """

    return {
        "faithfulness": judge_llm.generate(faithfulness_prompt),
        "relevance": judge_llm.generate(relevance_prompt)
    }
```

## Production Considerations

### Caching
```python
from functools import lru_cache
import hashlib
import json

# Cache embeddings
@lru_cache(maxsize=10000)
def cached_embed(text):
    return embed_model.encode(text)

# Cache retrieval results with Redis
from redis import Redis
cache = Redis()

def cached_search(query, k=5, ttl=3600):
    cache_key = f"rag:{hashlib.md5(query.encode()).hexdigest()}:{k}"
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)

    results = retriever.search(query, k=k)
    cache.setex(cache_key, ttl, json.dumps(results))
    return results
```

### Monitoring
```python
import time

# Track RAG pipeline metrics
def monitored_rag(query, metrics_client):
    start = time.time()

    # Embedding time
    embed_start = time.time()
    query_embedding = embed(query)
    metrics_client.timing("rag.embed_ms", (time.time() - embed_start) * 1000)

    # Retrieval time
    retrieve_start = time.time()
    contexts = retrieve(query_embedding)
    metrics_client.timing("rag.retrieve_ms", (time.time() - retrieve_start) * 1000)
    metrics_client.gauge("rag.num_chunks", len(contexts))

    # Generation time
    gen_start = time.time()
    response = generate(query, contexts)
    metrics_client.timing("rag.generate_ms", (time.time() - gen_start) * 1000)

    # Total time
    metrics_client.timing("rag.total_ms", (time.time() - start) * 1000)

    return response
```

## Common Pitfalls

### Pitfall 1: Poor Chunking
```
Problem: Chunks break mid-sentence or concept
Impact: Retrieval returns incomplete information
Solution: Use semantic or structure-aware chunking
```

### Pitfall 2: Embedding Mismatch
```
Problem: Different models for index vs. query
Impact: Poor semantic matching
Solution: Always use same embedding model
```

### Pitfall 3: Context Overload
```
Problem: Too many chunks -> exceeds context window
Impact: Truncation, lost information
Solution: Limit chunks, compress, or summarize
```

### Pitfall 4: Missing Metadata
```
Problem: No filtering capability
Impact: Irrelevant results from wrong domains
Solution: Add rich metadata during indexing
```

### Pitfall 5: Stale Index
```
Problem: Documents updated but not re-indexed
Impact: Outdated responses
Solution: Implement continuous ingestion pipeline
```

## Resources

- [OCI GenAI Agents Documentation](https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/overview.htm)
- [LangChain RAG Guide](https://python.langchain.com/docs/use_cases/question_answering/)
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [RAG Survey Paper](https://arxiv.org/abs/2312.10997)
