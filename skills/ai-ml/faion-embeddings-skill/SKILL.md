---
name: faion-embeddings-skill
user-invocable: false
description: ""
---

# Text Embeddings Expert

You are an expert on text embeddings - numerical vector representations of text that capture semantic meaning. Help users choose models, implement embedding pipelines, optimize costs, and benchmark quality.

## Quick Reference

### Model Comparison

| Model | Provider | Dimensions | Max Tokens | Cost/1M tokens | Quality | Speed |
|-------|----------|------------|------------|----------------|---------|-------|
| **text-embedding-3-large** | OpenAI | 3072 (256-3072) | 8191 | $0.13 | Best | Fast |
| **text-embedding-3-small** | OpenAI | 1536 (256-1536) | 8191 | $0.02 | Good | Fast |
| **text-embedding-ada-002** | OpenAI | 1536 | 8191 | $0.10 | Good | Fast |
| **mistral-embed** | Mistral | 1024 | 8192 | $0.10 | Good | Fast |
| **embed-english-v3.0** | Cohere | 1024 | 512 | $0.10 | Very Good | Fast |
| **embed-multilingual-v3.0** | Cohere | 1024 | 512 | $0.10 | Very Good | Fast |
| **bge-large-en-v1.5** | Local | 1024 | 512 | Free | Very Good | Medium |
| **bge-m3** | Local | 1024 | 8192 | Free | Excellent | Slow |
| **all-MiniLM-L6-v2** | Local | 384 | 256 | Free | Adequate | Very Fast |
| **e5-large-v2** | Local | 1024 | 512 | Free | Very Good | Medium |
| **gte-large** | Local | 1024 | 512 | Free | Very Good | Medium |
| **nomic-embed-text-v1.5** | Local | 768 | 8192 | Free | Good | Fast |

### When to Use Which

| Use Case | Recommended Model | Why |
|----------|-------------------|-----|
| **Production RAG** | text-embedding-3-large | Best quality, scalable |
| **Cost-sensitive** | text-embedding-3-small or local BGE | Good quality, low cost |
| **Multilingual** | embed-multilingual-v3.0 or bge-m3 | 100+ languages |
| **Long documents** | bge-m3 or nomic-embed | 8K token context |
| **Air-gapped/Private** | sentence-transformers (local) | No API calls |
| **Real-time search** | all-MiniLM-L6-v2 | Fast inference |
| **Semantic similarity** | e5-large-v2 | Trained for similarity |

---

## OpenAI Embeddings

### Basic Usage

```python
from openai import OpenAI

client = OpenAI()  # Uses OPENAI_API_KEY env var

def get_embedding(text: str, model: str = "text-embedding-3-large") -> list[float]:
    """Get embedding for a single text."""
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding
```

### Batch Processing (Recommended)

```python
def get_embeddings_batch(
    texts: list[str],
    model: str = "text-embedding-3-large",
    batch_size: int = 2048  # OpenAI limit
) -> list[list[float]]:
    """Get embeddings for multiple texts efficiently."""
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = client.embeddings.create(
            input=batch,
            model=model
        )
        # Preserve order (API may return out of order)
        sorted_embeddings = sorted(response.data, key=lambda x: x.index)
        all_embeddings.extend([e.embedding for e in sorted_embeddings])

    return all_embeddings
```

### Matryoshka Embeddings (Dimension Reduction)

OpenAI's text-embedding-3 models support native dimension reduction:

```python
def get_embedding_reduced(
    text: str,
    model: str = "text-embedding-3-large",
    dimensions: int = 256  # Reduce from 3072 to 256
) -> list[float]:
    """Get reduced-dimension embedding (cheaper storage, similar quality)."""
    response = client.embeddings.create(
        input=text,
        model=model,
        dimensions=dimensions  # 256, 512, 1024, 1536, 3072
    )
    return response.data[0].embedding
```

**Dimension vs Quality Trade-off:**

| Dimensions | Storage | MTEB Score (approx) | Use Case |
|------------|---------|---------------------|----------|
| 3072 | 12KB | 64.6% | Maximum quality |
| 1536 | 6KB | 64.2% | Balanced |
| 1024 | 4KB | 63.8% | Good for most |
| 512 | 2KB | 62.5% | Cost-sensitive |
| 256 | 1KB | 60.1% | High-volume, basic similarity |

---

## Mistral Embeddings

```python
from mistralai import Mistral

client = Mistral(api_key="YOUR_API_KEY")

def get_mistral_embedding(text: str) -> list[float]:
    """Get embedding using Mistral."""
    response = client.embeddings.create(
        model="mistral-embed",
        inputs=[text]
    )
    return response.data[0].embedding

# Batch processing
def get_mistral_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Batch embeddings with Mistral."""
    response = client.embeddings.create(
        model="mistral-embed",
        inputs=texts
    )
    return [e.embedding for e in response.data]
```

---

## Cohere Embeddings

```python
import cohere

co = cohere.Client("YOUR_API_KEY")

def get_cohere_embedding(
    texts: list[str],
    input_type: str = "search_document"  # or "search_query"
) -> list[list[float]]:
    """
    Get Cohere embeddings.

    input_type options:
    - "search_document": For documents to be searched
    - "search_query": For search queries
    - "classification": For classification tasks
    - "clustering": For clustering tasks
    """
    response = co.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type=input_type,
        truncate="END"  # or "START", "NONE"
    )
    return response.embeddings
```

**Cohere Best Practices:**
- Use `input_type="search_document"` for indexing
- Use `input_type="search_query"` for queries
- This asymmetric approach improves retrieval quality

---

## Local Models (sentence-transformers)

### Installation

```bash
pip install sentence-transformers
# For GPU support
pip install sentence-transformers[gpu]
```

### Basic Usage

```python
from sentence_transformers import SentenceTransformer

# Load model (downloads on first use)
model = SentenceTransformer("BAAI/bge-large-en-v1.5")

# Single text
embedding = model.encode("Your text here")

# Batch processing (automatic batching)
texts = ["Text 1", "Text 2", "Text 3"]
embeddings = model.encode(texts, show_progress_bar=True)
```

### GPU Acceleration

```python
import torch
from sentence_transformers import SentenceTransformer

# Auto-detect GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer("BAAI/bge-large-en-v1.5", device=device)

# Encode with GPU
embeddings = model.encode(
    texts,
    batch_size=32,  # Adjust based on GPU memory
    show_progress_bar=True,
    convert_to_numpy=True,  # Return numpy array
    normalize_embeddings=True  # L2 normalize for cosine similarity
)
```

### Popular Local Models

```python
# Best quality (slow)
model = SentenceTransformer("BAAI/bge-m3")

# Good quality, balanced
model = SentenceTransformer("BAAI/bge-large-en-v1.5")
model = SentenceTransformer("intfloat/e5-large-v2")

# Fast inference
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Multilingual
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Long context (8K tokens)
model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)
```

### BGE-M3 (Best Local Model)

```python
from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)

# Dense embeddings (default)
embeddings = model.encode(texts)["dense_vecs"]

# Sparse embeddings (for hybrid search)
sparse = model.encode(texts, return_sparse=True)["lexical_weights"]

# Both dense + sparse
output = model.encode(texts, return_dense=True, return_sparse=True)
```

---

## Chunking Strategies

### Why Chunking Matters

Embedding models have token limits. Long documents must be split into chunks.

### Fixed-Size Chunks

```python
def chunk_fixed_size(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> list[str]:
    """Split text into fixed-size chunks with overlap."""
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap

    return chunks
```

### Token-Based Chunks (Recommended)

```python
import tiktoken

def chunk_by_tokens(
    text: str,
    max_tokens: int = 500,
    overlap_tokens: int = 50,
    model: str = "text-embedding-3-large"
) -> list[str]:
    """Split text by token count (more accurate)."""
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    chunks = []
    start = 0

    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunk_tokens = tokens[start:end]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)
        start = end - overlap_tokens

    return chunks
```

### Semantic Chunking

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_semantic(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> list[str]:
    """Split at natural boundaries (paragraphs, sentences)."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return splitter.split_text(text)
```

### Sentence-Based Chunks

```python
import nltk
nltk.download('punkt')

def chunk_by_sentences(
    text: str,
    sentences_per_chunk: int = 5,
    overlap_sentences: int = 1
) -> list[str]:
    """Split by sentences for better semantic coherence."""
    sentences = nltk.sent_tokenize(text)
    chunks = []
    start = 0

    while start < len(sentences):
        end = start + sentences_per_chunk
        chunk = " ".join(sentences[start:end])
        chunks.append(chunk)
        start = end - overlap_sentences

    return chunks
```

### Optimal Chunk Sizes

| Use Case | Chunk Size | Overlap | Rationale |
|----------|------------|---------|-----------|
| **Q&A RAG** | 256-512 tokens | 20% | Focused answers |
| **Document summary** | 1000-2000 tokens | 10% | More context |
| **Code search** | 100-200 tokens | 50% | Preserve functions |
| **Legal/Medical** | 500-1000 tokens | 25% | Complete clauses |

---

## Caching Strategies

### In-Memory Cache

```python
import hashlib
from functools import lru_cache
from typing import Tuple

def text_hash(text: str) -> str:
    """Create consistent hash for text."""
    return hashlib.sha256(text.encode()).hexdigest()[:16]

@lru_cache(maxsize=10000)
def get_embedding_cached(text_hash: str, text: str, model: str) -> Tuple[float, ...]:
    """Cache embeddings in memory."""
    embedding = get_embedding(text, model)
    return tuple(embedding)  # Tuples are hashable
```

### File-Based Cache

```python
import json
import hashlib
from pathlib import Path

class EmbeddingCache:
    def __init__(self, cache_dir: str = ".embedding_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_key(self, text: str, model: str) -> str:
        content = f"{model}:{text}"
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, text: str, model: str) -> list[float] | None:
        key = self._get_key(text, model)
        cache_file = self.cache_dir / f"{key}.json"

        if cache_file.exists():
            return json.loads(cache_file.read_text())
        return None

    def set(self, text: str, model: str, embedding: list[float]):
        key = self._get_key(text, model)
        cache_file = self.cache_dir / f"{key}.json"
        cache_file.write_text(json.dumps(embedding))

    def get_or_compute(
        self,
        text: str,
        model: str,
        compute_fn
    ) -> list[float]:
        cached = self.get(text, model)
        if cached:
            return cached

        embedding = compute_fn(text, model)
        self.set(text, model, embedding)
        return embedding
```

### Redis Cache (Production)

```python
import redis
import json
import hashlib

class RedisEmbeddingCache:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.client = redis.from_url(redis_url)
        self.ttl = 86400 * 30  # 30 days

    def _get_key(self, text: str, model: str) -> str:
        content = f"{model}:{text}"
        hash_val = hashlib.sha256(content.encode()).hexdigest()
        return f"emb:{hash_val}"

    def get(self, text: str, model: str) -> list[float] | None:
        key = self._get_key(text, model)
        data = self.client.get(key)
        return json.loads(data) if data else None

    def set(self, text: str, model: str, embedding: list[float]):
        key = self._get_key(text, model)
        self.client.setex(key, self.ttl, json.dumps(embedding))

    def get_batch(
        self,
        texts: list[str],
        model: str
    ) -> dict[str, list[float] | None]:
        """Get multiple embeddings from cache."""
        pipe = self.client.pipeline()
        keys = [self._get_key(t, model) for t in texts]

        for key in keys:
            pipe.get(key)

        results = pipe.execute()
        return {
            text: json.loads(data) if data else None
            for text, data in zip(texts, results)
        }
```

---

## Cost Optimization

### Cost Comparison

| Model | Cost/1M tokens | 1M docs (500 tokens) | Monthly (10M docs) |
|-------|----------------|----------------------|-------------------|
| text-embedding-3-large | $0.13 | $0.065 | $650 |
| text-embedding-3-small | $0.02 | $0.010 | $100 |
| mistral-embed | $0.10 | $0.050 | $500 |
| Local (GPU) | ~$0.001 | ~$0.0005 | ~$5 (compute) |
| Local (CPU) | ~$0.005 | ~$0.0025 | ~$25 (compute) |

### Optimization Strategies

#### 1. Use Dimension Reduction

```python
# Instead of 3072 dimensions ($0.13/1M)
# Use 1024 dimensions with minimal quality loss
embedding = get_embedding_reduced(text, dimensions=1024)
# Saves 66% storage, similar retrieval quality
```

#### 2. Batch Requests

```python
# Bad: 1000 API calls
for text in texts:
    get_embedding(text)  # 1000 requests

# Good: 1 API call
get_embeddings_batch(texts)  # 1 request for up to 2048 texts
```

#### 3. Cache Aggressively

```python
# Cache hit rate of 80% = 80% cost reduction
cache = RedisEmbeddingCache()
embedding = cache.get_or_compute(text, model, get_embedding)
```

#### 4. Use Smaller Models for Filtering

```python
# Two-stage retrieval:
# 1. Fast filter with small model
quick_results = search_with_model(query, "all-MiniLM-L6-v2", top_k=100)

# 2. Rerank with large model
final_results = rerank_with_model(query, quick_results, "text-embedding-3-large", top_k=10)
```

#### 5. Deduplicate Before Embedding

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def deduplicate_texts(texts: list[str], threshold: float = 0.95) -> list[str]:
    """Remove near-duplicate texts before embedding."""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)

    unique_texts = []
    for i, text in enumerate(texts):
        if not unique_texts:
            unique_texts.append(text)
            continue

        # Compare with existing
        current_vec = tfidf_matrix[i]
        existing_vecs = vectorizer.transform(unique_texts)
        similarities = cosine_similarity(current_vec, existing_vecs)[0]

        if max(similarities) < threshold:
            unique_texts.append(text)

    return unique_texts
```

---

## Benchmarking

### MTEB Leaderboard

The Massive Text Embedding Benchmark (MTEB) is the standard for comparing embedding models.

| Model | Average Score | Retrieval | Classification | Clustering |
|-------|---------------|-----------|----------------|------------|
| bge-m3 | 68.1% | 66.8% | 75.2% | 48.3% |
| text-embedding-3-large | 64.6% | 63.4% | 75.8% | 46.1% |
| e5-mistral-7b-instruct | 66.6% | 60.5% | 78.4% | 51.2% |
| bge-large-en-v1.5 | 63.6% | 54.3% | 75.1% | 46.1% |
| text-embedding-3-small | 62.3% | 51.7% | 74.6% | 44.9% |

### Custom Benchmarking

```python
import numpy as np
from typing import Callable
from sklearn.metrics.pairwise import cosine_similarity

def benchmark_retrieval(
    queries: list[str],
    documents: list[str],
    relevance: dict[int, list[int]],  # query_idx -> [relevant_doc_idxs]
    embed_fn: Callable[[list[str]], np.ndarray],
    k: int = 10
) -> dict[str, float]:
    """
    Benchmark retrieval quality.

    Returns:
    - Recall@K
    - MRR (Mean Reciprocal Rank)
    - Precision@K
    """
    # Embed all
    query_embeddings = embed_fn(queries)
    doc_embeddings = embed_fn(documents)

    # Compute similarities
    similarities = cosine_similarity(query_embeddings, doc_embeddings)

    recalls, mrrs, precisions = [], [], []

    for q_idx, relevant_docs in relevance.items():
        # Get top-k results
        scores = similarities[q_idx]
        top_k_idxs = np.argsort(scores)[::-1][:k]

        # Recall@K
        hits = len(set(top_k_idxs) & set(relevant_docs))
        recalls.append(hits / len(relevant_docs))

        # MRR
        for rank, doc_idx in enumerate(top_k_idxs, 1):
            if doc_idx in relevant_docs:
                mrrs.append(1 / rank)
                break
        else:
            mrrs.append(0)

        # Precision@K
        precisions.append(hits / k)

    return {
        "recall@k": np.mean(recalls),
        "mrr": np.mean(mrrs),
        "precision@k": np.mean(precisions)
    }
```

### Speed Benchmarking

```python
import time
import statistics

def benchmark_speed(
    texts: list[str],
    embed_fn: Callable,
    iterations: int = 5
) -> dict[str, float]:
    """Benchmark embedding speed."""
    times = []

    for _ in range(iterations):
        start = time.perf_counter()
        embed_fn(texts)
        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return {
        "mean_time": statistics.mean(times),
        "std_time": statistics.stdev(times) if len(times) > 1 else 0,
        "texts_per_second": len(texts) / statistics.mean(times),
        "ms_per_text": (statistics.mean(times) / len(texts)) * 1000
    }
```

---

## Production Patterns

### Async Batch Processing

```python
import asyncio
from openai import AsyncOpenAI

async_client = AsyncOpenAI()

async def get_embeddings_async(
    texts: list[str],
    model: str = "text-embedding-3-large",
    batch_size: int = 100,
    max_concurrent: int = 5
) -> list[list[float]]:
    """Process large volumes with controlled concurrency."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def process_batch(batch: list[str]) -> list[list[float]]:
        async with semaphore:
            response = await async_client.embeddings.create(
                input=batch,
                model=model
            )
            sorted_data = sorted(response.data, key=lambda x: x.index)
            return [e.embedding for e in sorted_data]

    # Create batches
    batches = [texts[i:i+batch_size] for i in range(0, len(texts), batch_size)]

    # Process concurrently
    results = await asyncio.gather(*[process_batch(b) for b in batches])

    # Flatten
    return [emb for batch in results for emb in batch]
```

### Retry with Exponential Backoff

```python
import time
import random
from openai import RateLimitError, APIError

def get_embedding_with_retry(
    text: str,
    model: str = "text-embedding-3-large",
    max_retries: int = 5
) -> list[float]:
    """Robust embedding with retry logic."""
    for attempt in range(max_retries):
        try:
            return get_embedding(text, model)
        except RateLimitError:
            wait = (2 ** attempt) + random.random()
            print(f"Rate limited. Waiting {wait:.1f}s...")
            time.sleep(wait)
        except APIError as e:
            if attempt == max_retries - 1:
                raise
            wait = 1 + random.random()
            print(f"API error: {e}. Retrying in {wait:.1f}s...")
            time.sleep(wait)

    raise Exception("Max retries exceeded")
```

### Embedding Pipeline

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class EmbeddingConfig:
    model: str = "text-embedding-3-large"
    dimensions: Optional[int] = None
    chunk_size: int = 500
    chunk_overlap: int = 50
    batch_size: int = 100
    cache_enabled: bool = True

class EmbeddingPipeline:
    def __init__(self, config: EmbeddingConfig):
        self.config = config
        self.cache = EmbeddingCache() if config.cache_enabled else None

    def process_document(self, text: str) -> list[list[float]]:
        """Full pipeline: chunk -> cache check -> embed."""
        # 1. Chunk
        chunks = chunk_by_tokens(
            text,
            max_tokens=self.config.chunk_size,
            overlap_tokens=self.config.chunk_overlap
        )

        # 2. Check cache
        uncached = []
        cached_embeddings = {}

        if self.cache:
            for i, chunk in enumerate(chunks):
                cached = self.cache.get(chunk, self.config.model)
                if cached:
                    cached_embeddings[i] = cached
                else:
                    uncached.append((i, chunk))
        else:
            uncached = list(enumerate(chunks))

        # 3. Embed uncached
        if uncached:
            indices, texts = zip(*uncached)
            new_embeddings = get_embeddings_batch(
                list(texts),
                model=self.config.model
            )

            for idx, emb in zip(indices, new_embeddings):
                cached_embeddings[idx] = emb
                if self.cache:
                    self.cache.set(chunks[idx], self.config.model, emb)

        # 4. Return in order
        return [cached_embeddings[i] for i in range(len(chunks))]
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| **Rate limit errors** | Too many requests | Batch requests, add retry logic |
| **Token limit exceeded** | Text too long | Chunk text before embedding |
| **Poor retrieval quality** | Wrong model/chunk size | Benchmark different configs |
| **High latency** | Network/model size | Use local models or caching |
| **High costs** | Too many API calls | Cache, deduplicate, use smaller models |
| **Dimension mismatch** | Mixed models in DB | Use consistent model per index |

### Quality Debugging

```python
def debug_similarity(
    query: str,
    documents: list[str],
    model: str = "text-embedding-3-large"
) -> None:
    """Debug why certain documents rank high/low."""
    query_emb = np.array(get_embedding(query, model))
    doc_embs = np.array(get_embeddings_batch(documents, model))

    similarities = cosine_similarity([query_emb], doc_embs)[0]

    print(f"Query: {query[:100]}...")
    print("-" * 50)

    for doc, sim in sorted(zip(documents, similarities), key=lambda x: -x[1]):
        print(f"Score: {sim:.4f} | {doc[:80]}...")
```

---

## Integration with Vector Databases

### Storing Embeddings

```python
# Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

client = QdrantClient("localhost", port=6333)
embeddings = get_embeddings_batch(texts)

points = [
    PointStruct(id=i, vector=emb, payload={"text": text})
    for i, (emb, text) in enumerate(zip(embeddings, texts))
]
client.upsert("my_collection", points)

# pgvector
import psycopg2

conn = psycopg2.connect("postgresql://...")
cur = conn.cursor()

for text, embedding in zip(texts, embeddings):
    cur.execute(
        "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
        (text, embedding)
    )
conn.commit()
```

### Searching

```python
# Qdrant
query_embedding = get_embedding(query)
results = client.search(
    collection_name="my_collection",
    query_vector=query_embedding,
    limit=10
)

# pgvector
cur.execute("""
    SELECT content, 1 - (embedding <=> %s) as similarity
    FROM documents
    ORDER BY embedding <=> %s
    LIMIT 10
""", (query_embedding, query_embedding))
```

---

## References

- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [Sentence Transformers](https://www.sbert.net/)
- [BGE-M3 Paper](https://arxiv.org/abs/2402.03216)
- [Matryoshka Representation Learning](https://arxiv.org/abs/2205.13147)
- [Chunking Strategies Guide](https://www.pinecone.io/learn/chunking-strategies/)
