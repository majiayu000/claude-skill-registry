---
name: faion-vector-db-skill
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(pip:*, docker:*, curl:*, psql:*, ls:*, cat:*)
---

# Vector Database Skill

Technical skill for vector database operations and semantic search infrastructure.

## Purpose

Provides comprehensive knowledge for storing, indexing, and querying vector embeddings. Supports RAG (Retrieval-Augmented Generation) pipelines, semantic search, and similarity-based recommendations.

---

## Database Comparison

| Database | Best For | Hosting | Scale | Performance | Filtering |
|----------|----------|---------|-------|-------------|-----------|
| **Qdrant** | Production RAG | Self/Cloud | 100M+ | 41 QPS @ 50M | Payload filters |
| **Weaviate** | Knowledge graphs | Self/Cloud | 10M+ | GraphQL native | Hybrid search |
| **pgvector** | Existing Postgres | Self-hosted | 10M | Good w/ indexes | SQL WHERE |
| **Chroma** | Prototyping | In-memory | 1M | Fast, simple | Metadata |
| **Pinecone** | Managed scale | Cloud only | 1B+ | Serverless | Metadata |
| **Milvus** | Large scale | Self/Cloud | 1B+ | GPU support | Attribute |

### Selection Guide

```
Rapid prototyping       --> Chroma
Existing PostgreSQL     --> pgvector
Production self-hosted  --> Qdrant (recommended)
Knowledge graphs        --> Weaviate
Fully managed           --> Pinecone
Massive scale (1B+)     --> Milvus or Pinecone
```

---

## Qdrant (Recommended for Production)

### Installation

```bash
# Docker (recommended)
docker run -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage:z \
  qdrant/qdrant

# Docker Compose
# docker-compose.yml
version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - ./qdrant_storage:/qdrant/storage
    environment:
      - QDRANT__SERVICE__GRPC_PORT=6334

# Python client
pip install qdrant-client
```

### Collection Management

```python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, Distance, PointStruct,
    Filter, FieldCondition, MatchValue,
    HnswConfigDiff, OptimizersConfigDiff
)

# Connect
client = QdrantClient(host="localhost", port=6333)
# or cloud: QdrantClient(url="...", api_key="...")

# Create collection
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=1536,           # OpenAI embedding dimension
        distance=Distance.COSINE
    ),
    hnsw_config=HnswConfigDiff(
        m=16,                # Number of connections per element
        ef_construct=100,    # Search quality during construction
    ),
    optimizers_config=OptimizersConfigDiff(
        indexing_threshold=20000,  # Start indexing after N points
    ),
    on_disk_payload=True,    # Large payloads on disk
)

# Named vectors (multiple embeddings per point)
client.create_collection(
    collection_name="multimodal",
    vectors_config={
        "text": VectorParams(size=1536, distance=Distance.COSINE),
        "image": VectorParams(size=512, distance=Distance.COSINE),
    }
)

# Get collection info
info = client.get_collection("documents")
print(f"Points: {info.points_count}")
print(f"Indexed: {info.indexed_vectors_count}")
```

### Upserting Vectors

```python
# Single point
client.upsert(
    collection_name="documents",
    points=[
        PointStruct(
            id=1,
            vector=[0.1, 0.2, ...],  # 1536-dim embedding
            payload={
                "text": "Document content here",
                "source": "file.pdf",
                "page": 5,
                "category": "technical",
                "created_at": "2024-01-15"
            }
        )
    ]
)

# Batch upsert (recommended for large datasets)
batch_size = 100
points = []

for i, doc in enumerate(documents):
    points.append(PointStruct(
        id=i,
        vector=get_embedding(doc["text"]),
        payload={"text": doc["text"], "source": doc["source"]}
    ))

    if len(points) >= batch_size:
        client.upsert(
            collection_name="documents",
            points=points
        )
        points = []

# Upsert remaining
if points:
    client.upsert(collection_name="documents", points=points)

# Named vectors
client.upsert(
    collection_name="multimodal",
    points=[
        PointStruct(
            id=1,
            vector={
                "text": text_embedding,
                "image": image_embedding,
            },
            payload={"title": "Sample"}
        )
    ]
)
```

### Searching

```python
# Basic similarity search
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    limit=10,
    score_threshold=0.7,  # Minimum similarity
)

for result in results:
    print(f"ID: {result.id}, Score: {result.score}")
    print(f"Text: {result.payload['text'][:100]}...")

# Search with payload filter
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="category",
                match=MatchValue(value="technical")
            ),
            FieldCondition(
                key="page",
                range=Range(gte=1, lte=10)
            )
        ]
    ),
    limit=10,
    with_payload=True,
    with_vectors=False,  # Don't return vectors (faster)
)

# Search with named vectors
results = client.search(
    collection_name="multimodal",
    query_vector=("text", text_query_embedding),
    limit=10,
)
```

### Hybrid Search (Vector + Keyword)

```python
from qdrant_client.models import SparseVectorParams, SparseIndexParams

# Create collection with sparse vectors
client.create_collection(
    collection_name="hybrid_docs",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    sparse_vectors_config={
        "bm25": SparseVectorParams(
            index=SparseIndexParams(on_disk=False)
        )
    }
)

# Upsert with sparse vectors (BM25)
from qdrant_client.models import SparseVector

client.upsert(
    collection_name="hybrid_docs",
    points=[
        PointStruct(
            id=1,
            vector=dense_embedding,
            sparse_vectors={
                "bm25": SparseVector(
                    indices=[100, 500, 1000],  # Token IDs
                    values=[0.5, 0.3, 0.2]     # BM25 weights
                )
            },
            payload={"text": "..."}
        )
    ]
)

# Hybrid search with fusion
from qdrant_client.models import Prefetch, FusionQuery, Fusion

results = client.query_points(
    collection_name="hybrid_docs",
    prefetch=[
        Prefetch(query=dense_query, using="", limit=20),
        Prefetch(query=sparse_query, using="bm25", limit=20),
    ],
    query=FusionQuery(fusion=Fusion.RRF),  # Reciprocal Rank Fusion
    limit=10,
)
```

### Payload Indexing

```python
from qdrant_client.models import PayloadSchemaType

# Create payload index for faster filtering
client.create_payload_index(
    collection_name="documents",
    field_name="category",
    field_schema=PayloadSchemaType.KEYWORD
)

client.create_payload_index(
    collection_name="documents",
    field_name="created_at",
    field_schema=PayloadSchemaType.DATETIME
)

client.create_payload_index(
    collection_name="documents",
    field_name="page",
    field_schema=PayloadSchemaType.INTEGER
)

# Full-text index for keyword search
client.create_payload_index(
    collection_name="documents",
    field_name="text",
    field_schema=PayloadSchemaType.TEXT
)
```

### Quantization (Memory Optimization)

```python
from qdrant_client.models import (
    ScalarQuantization, ScalarQuantizationConfig,
    ProductQuantization, ProductQuantizationConfig,
    BinaryQuantization, BinaryQuantizationConfig
)

# Scalar quantization (4x memory reduction)
client.update_collection(
    collection_name="documents",
    quantization_config=ScalarQuantization(
        scalar=ScalarQuantizationConfig(
            type="int8",
            quantile=0.99,
            always_ram=True,
        )
    )
)

# Binary quantization (32x memory reduction, fastest)
client.update_collection(
    collection_name="documents",
    quantization_config=BinaryQuantization(
        binary=BinaryQuantizationConfig(always_ram=True)
    )
)

# Search with quantization rescoring
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    limit=10,
    search_params=SearchParams(
        quantization=QuantizationSearchParams(
            rescore=True,      # Rescore with original vectors
            oversampling=2.0,  # Fetch 2x candidates before rescoring
        )
    )
)
```

---

## Weaviate

### Installation

```bash
# Docker
docker run -p 8080:8080 -p 50051:50051 \
  -e QUERY_DEFAULTS_LIMIT=25 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  -e DEFAULT_VECTORIZER_MODULE=none \
  -v weaviate_data:/var/lib/weaviate \
  semitechnologies/weaviate:latest

# Python client
pip install weaviate-client
```

### Schema Design

```python
import weaviate
from weaviate.classes.config import Configure, Property, DataType

# Connect
client = weaviate.connect_to_local()
# or cloud: weaviate.connect_to_wcs(cluster_url, auth_credentials)

# Create collection with schema
documents = client.collections.create(
    name="Document",
    vectorizer_config=Configure.Vectorizer.none(),  # Bring your own vectors
    properties=[
        Property(name="text", data_type=DataType.TEXT),
        Property(name="source", data_type=DataType.TEXT),
        Property(name="page", data_type=DataType.INT),
        Property(name="category", data_type=DataType.TEXT,
                 skip_vectorization=True),
    ],
    vector_index_config=Configure.VectorIndex.hnsw(
        ef=100,
        max_connections=16,
        distance_metric=Configure.VectorDistances.COSINE,
    ),
)

# With cross-references (knowledge graph)
client.collections.create(
    name="Author",
    properties=[
        Property(name="name", data_type=DataType.TEXT),
        Property(name="email", data_type=DataType.TEXT),
    ],
)

documents = client.collections.get("Document")
documents.config.add_reference(
    weaviate.classes.config.ReferenceProperty(
        name="hasAuthor",
        target_collection="Author"
    )
)
```

### Inserting Data

```python
documents = client.collections.get("Document")

# Single insert
uuid = documents.data.insert(
    properties={
        "text": "Document content...",
        "source": "file.pdf",
        "page": 1,
        "category": "technical"
    },
    vector=embedding_vector,
)

# Batch insert
with documents.batch.dynamic() as batch:
    for doc in documents_list:
        batch.add_object(
            properties={
                "text": doc["text"],
                "source": doc["source"],
            },
            vector=doc["embedding"],
        )
```

### Searching

```python
documents = client.collections.get("Document")

# Vector search
response = documents.query.near_vector(
    near_vector=query_embedding,
    limit=10,
    return_metadata=weaviate.classes.query.MetadataQuery(certainty=True)
)

for obj in response.objects:
    print(f"ID: {obj.uuid}")
    print(f"Certainty: {obj.metadata.certainty}")
    print(f"Text: {obj.properties['text'][:100]}")

# Hybrid search (vector + BM25)
response = documents.query.hybrid(
    query="search keywords",
    vector=query_embedding,
    alpha=0.5,  # 0=pure BM25, 1=pure vector
    limit=10,
)

# Filtered search
from weaviate.classes.query import Filter

response = documents.query.near_vector(
    near_vector=query_embedding,
    filters=Filter.by_property("category").equal("technical"),
    limit=10,
)
```

### GraphQL Queries (Advanced)

```python
# Raw GraphQL
result = client.graphql_raw_query("""
{
  Get {
    Document(
      nearVector: {vector: [...], certainty: 0.7}
      where: {path: ["category"], operator: Equal, valueText: "technical"}
      limit: 10
    ) {
      text
      source
      _additional {certainty}
    }
  }
}
""")

# Aggregate queries
result = client.graphql_raw_query("""
{
  Aggregate {
    Document {
      meta {count}
      category {
        count
        topOccurrences {value occurs}
      }
    }
  }
}
""")
```

---

## pgvector (PostgreSQL Extension)

### Installation

```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table with vector column
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    source VARCHAR(255),
    page INTEGER,
    category VARCHAR(100),
    embedding vector(1536),  -- OpenAI dimension
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create HNSW index (recommended)
CREATE INDEX ON documents
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Or IVFFlat index (faster build, less accurate)
CREATE INDEX ON documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);  -- sqrt(n) for n rows
```

### Python Usage

```python
import psycopg2
from pgvector.psycopg2 import register_vector

# Connect and register vector type
conn = psycopg2.connect("postgresql://user:pass@localhost/db")
register_vector(conn)

cur = conn.cursor()

# Insert
cur.execute("""
    INSERT INTO documents (content, source, embedding)
    VALUES (%s, %s, %s)
""", ("Document text...", "file.pdf", embedding))

# Batch insert
from psycopg2.extras import execute_values

data = [(doc["text"], doc["source"], doc["embedding"]) for doc in documents]
execute_values(cur, """
    INSERT INTO documents (content, source, embedding)
    VALUES %s
""", data)

conn.commit()
```

### Searching

```python
# Cosine similarity (closer to 1 is better)
cur.execute("""
    SELECT id, content, source,
           1 - (embedding <=> %s) AS similarity
    FROM documents
    WHERE category = %s
    ORDER BY embedding <=> %s
    LIMIT %s
""", (query_embedding, "technical", query_embedding, 10))

results = cur.fetchall()

# L2 distance (smaller is better)
cur.execute("""
    SELECT id, content, embedding <-> %s AS distance
    FROM documents
    ORDER BY embedding <-> %s
    LIMIT 10
""", (query_embedding, query_embedding))

# Inner product (larger is better, for normalized vectors)
cur.execute("""
    SELECT id, content, embedding <#> %s AS neg_inner_product
    FROM documents
    ORDER BY embedding <#> %s
    LIMIT 10
""", (query_embedding, query_embedding))
```

### Performance Tuning

```sql
-- Set probes for IVFFlat (accuracy vs speed tradeoff)
SET ivfflat.probes = 10;  -- Default: 1

-- Set ef_search for HNSW
SET hnsw.ef_search = 100;  -- Default: 40

-- Partial index for filtered queries
CREATE INDEX ON documents
USING hnsw (embedding vector_cosine_ops)
WHERE category = 'technical';

-- Vacuum and analyze after bulk inserts
VACUUM ANALYZE documents;

-- Check index usage
EXPLAIN ANALYZE
SELECT * FROM documents
ORDER BY embedding <=> '[...]'::vector
LIMIT 10;
```

### Django Integration

```python
# models.py
from django.db import models
from pgvector.django import VectorField, HnswIndex

class Document(models.Model):
    content = models.TextField()
    source = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    embedding = VectorField(dimensions=1536)

    class Meta:
        indexes = [
            HnswIndex(
                name="document_embedding_hnsw",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            )
        ]

# queries.py
from pgvector.django import CosineDistance

# Search
similar = Document.objects.annotate(
    distance=CosineDistance("embedding", query_embedding)
).filter(
    category="technical"
).order_by("distance")[:10]
```

---

## Chroma (Prototyping)

### Installation

```bash
pip install chromadb
```

### Usage

```python
import chromadb
from chromadb.config import Settings

# In-memory (default)
client = chromadb.Client()

# Persistent storage
client = chromadb.PersistentClient(path="./chroma_db")

# Create collection
collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}  # cosine, l2, ip
)

# Add documents
collection.add(
    ids=["doc1", "doc2", "doc3"],
    embeddings=[emb1, emb2, emb3],
    metadatas=[
        {"source": "file1.pdf", "page": 1},
        {"source": "file2.pdf", "page": 2},
        {"source": "file3.pdf", "page": 3},
    ],
    documents=["Text 1", "Text 2", "Text 3"],  # Optional
)

# Query
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=10,
    where={"source": {"$eq": "file1.pdf"}},
    where_document={"$contains": "keyword"},
    include=["documents", "metadatas", "distances"],
)

print(results["ids"])
print(results["distances"])
print(results["documents"])

# Update
collection.update(
    ids=["doc1"],
    embeddings=[new_embedding],
    metadatas=[{"source": "updated.pdf"}],
)

# Delete
collection.delete(ids=["doc1", "doc2"])
collection.delete(where={"source": "old.pdf"})
```

### LangChain Integration

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

# Create from documents
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="./chroma_db",
    collection_name="my_collection",
)

# Load existing
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
    collection_name="my_collection",
)

# Search
results = vectorstore.similarity_search_with_score(
    query="search query",
    k=10,
    filter={"source": "file.pdf"},
)
```

---

## Pinecone (Managed)

### Setup

```bash
pip install pinecone-client
```

### Usage

```python
from pinecone import Pinecone, ServerlessSpec

# Initialize
pc = Pinecone(api_key="your-api-key")

# Create index
pc.create_index(
    name="documents",
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)

# Connect to index
index = pc.Index("documents")

# Upsert vectors
index.upsert(
    vectors=[
        {
            "id": "doc1",
            "values": embedding,
            "metadata": {
                "text": "Document content...",
                "source": "file.pdf",
                "category": "technical"
            }
        }
    ],
    namespace="production"  # Optional namespace
)

# Batch upsert
vectors = [
    {"id": f"doc{i}", "values": emb, "metadata": meta}
    for i, (emb, meta) in enumerate(zip(embeddings, metadatas))
]

# Upsert in batches of 100
for i in range(0, len(vectors), 100):
    batch = vectors[i:i+100]
    index.upsert(vectors=batch, namespace="production")
```

### Querying

```python
# Basic query
results = index.query(
    vector=query_embedding,
    top_k=10,
    include_metadata=True,
    namespace="production"
)

for match in results["matches"]:
    print(f"ID: {match['id']}, Score: {match['score']}")
    print(f"Metadata: {match['metadata']}")

# Filtered query
results = index.query(
    vector=query_embedding,
    top_k=10,
    filter={
        "category": {"$eq": "technical"},
        "$and": [
            {"page": {"$gte": 1}},
            {"page": {"$lte": 10}}
        ]
    },
    include_metadata=True,
)

# Hybrid search with sparse-dense
results = index.query(
    vector=dense_embedding,
    sparse_vector={
        "indices": [100, 200, 300],
        "values": [0.5, 0.3, 0.2]
    },
    top_k=10,
)
```

### Index Management

```python
# Describe index
stats = index.describe_index_stats()
print(f"Total vectors: {stats['total_vector_count']}")
print(f"Namespaces: {stats['namespaces']}")

# Delete vectors
index.delete(ids=["doc1", "doc2"], namespace="production")
index.delete(filter={"source": "old.pdf"}, namespace="production")
index.delete(delete_all=True, namespace="old_namespace")

# List indexes
indexes = pc.list_indexes()
```

---

## Indexing Strategies

### HNSW (Hierarchical Navigable Small World)

Best for: Most use cases, balanced speed/accuracy

```
Parameters:
- M: Number of connections per element (default: 16)
  - Higher = better recall, more memory
  - Recommended: 12-48

- ef_construction: Search quality during build (default: 100)
  - Higher = better index quality, slower build
  - Recommended: 100-500

- ef_search: Search quality at query time (default: 40)
  - Higher = better recall, slower search
  - Recommended: 50-200
```

### IVF (Inverted File Index)

Best for: Large datasets, faster build time

```
Parameters:
- nlist: Number of clusters (default: sqrt(n))
  - Higher = more clusters, better accuracy
  - Recommended: sqrt(n) to 4*sqrt(n)

- nprobe: Clusters to search (default: 1)
  - Higher = better recall, slower search
  - Recommended: nlist/10 to nlist/4
```

### Quantization Comparison

| Method | Memory Reduction | Speed Impact | Accuracy Loss |
|--------|------------------|--------------|---------------|
| None | 1x | Baseline | None |
| Scalar (int8) | 4x | Faster | 1-2% |
| Product (PQ) | 8-32x | Faster | 3-5% |
| Binary | 32x | Fastest | 5-10% |

---

## Query Patterns

### Basic Semantic Search

```python
def semantic_search(query: str, k: int = 10):
    """Simple semantic search."""
    query_embedding = get_embedding(query)

    results = client.search(
        collection_name="documents",
        query_vector=query_embedding,
        limit=k,
    )

    return [
        {"text": r.payload["text"], "score": r.score}
        for r in results
    ]
```

### Hybrid Search with Reranking

```python
from sentence_transformers import CrossEncoder

# Reranker model
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def hybrid_search_with_rerank(query: str, k: int = 10):
    """Hybrid search with cross-encoder reranking."""
    # Step 1: Get candidates (oversample)
    candidates = hybrid_search(query, k=k * 3)

    # Step 2: Rerank with cross-encoder
    pairs = [(query, c["text"]) for c in candidates]
    scores = reranker.predict(pairs)

    # Step 3: Sort by reranker score
    for i, score in enumerate(scores):
        candidates[i]["rerank_score"] = score

    candidates.sort(key=lambda x: x["rerank_score"], reverse=True)

    return candidates[:k]
```

### Multi-Vector Search

```python
def multi_query_search(queries: list[str], k: int = 10):
    """Search with multiple query variations."""
    all_results = []

    for query in queries:
        embedding = get_embedding(query)
        results = client.search(
            collection_name="documents",
            query_vector=embedding,
            limit=k,
        )
        all_results.extend(results)

    # Deduplicate and rank by frequency + score
    seen = {}
    for r in all_results:
        if r.id not in seen:
            seen[r.id] = {"result": r, "count": 1, "total_score": r.score}
        else:
            seen[r.id]["count"] += 1
            seen[r.id]["total_score"] += r.score

    # Score = count * avg_score
    ranked = sorted(
        seen.values(),
        key=lambda x: x["count"] * (x["total_score"] / x["count"]),
        reverse=True
    )

    return [x["result"] for x in ranked[:k]]
```

### Filtered Search with Metadata

```python
def search_with_filters(
    query: str,
    source: str = None,
    category: str = None,
    date_from: str = None,
    date_to: str = None,
    k: int = 10
):
    """Search with optional filters."""
    filters = []

    if source:
        filters.append(FieldCondition(
            key="source", match=MatchValue(value=source)
        ))

    if category:
        filters.append(FieldCondition(
            key="category", match=MatchValue(value=category)
        ))

    if date_from or date_to:
        date_filter = {}
        if date_from:
            date_filter["gte"] = date_from
        if date_to:
            date_filter["lte"] = date_to
        filters.append(FieldCondition(
            key="created_at", range=Range(**date_filter)
        ))

    query_filter = Filter(must=filters) if filters else None

    return client.search(
        collection_name="documents",
        query_vector=get_embedding(query),
        query_filter=query_filter,
        limit=k,
    )
```

### MMR (Maximum Marginal Relevance)

```python
import numpy as np

def mmr_search(
    query: str,
    k: int = 10,
    fetch_k: int = 50,
    lambda_mult: float = 0.5
):
    """Search with diversity via MMR."""
    query_embedding = np.array(get_embedding(query))

    # Fetch candidates
    results = client.search(
        collection_name="documents",
        query_vector=query_embedding.tolist(),
        limit=fetch_k,
        with_vectors=True,
    )

    # MMR selection
    selected = []
    candidates = list(results)

    while len(selected) < k and candidates:
        mmr_scores = []

        for c in candidates:
            c_vec = np.array(c.vector)

            # Similarity to query
            query_sim = np.dot(query_embedding, c_vec)

            # Max similarity to selected
            if selected:
                selected_vecs = [np.array(s.vector) for s in selected]
                max_selected_sim = max(
                    np.dot(c_vec, s_vec) for s_vec in selected_vecs
                )
            else:
                max_selected_sim = 0

            # MMR score
            mmr = lambda_mult * query_sim - (1 - lambda_mult) * max_selected_sim
            mmr_scores.append(mmr)

        # Select best
        best_idx = np.argmax(mmr_scores)
        selected.append(candidates.pop(best_idx))

    return selected
```

---

## Performance Optimization

### Batch Operations

```python
# Always batch insertions
BATCH_SIZE = 100

async def bulk_upsert(documents: list[dict]):
    """Efficient bulk upsert."""
    points = []

    for doc in documents:
        points.append(PointStruct(
            id=doc["id"],
            vector=doc["embedding"],
            payload={"text": doc["text"]}
        ))

        if len(points) >= BATCH_SIZE:
            await client.upsert(
                collection_name="documents",
                points=points,
                wait=False,  # Don't wait for indexing
            )
            points = []

    # Final batch
    if points:
        await client.upsert(
            collection_name="documents",
            points=points,
            wait=True,  # Wait for final batch
        )
```

### Caching

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def cached_embedding(text: str) -> tuple:
    """Cache embeddings for repeated queries."""
    return tuple(get_embedding(text))

def search_cached(query: str, k: int = 10):
    """Search with cached query embedding."""
    embedding = list(cached_embedding(query))
    return client.search(
        collection_name="documents",
        query_vector=embedding,
        limit=k,
    )
```

### Connection Pooling

```python
# Qdrant with gRPC (faster)
from qdrant_client import QdrantClient

client = QdrantClient(
    host="localhost",
    port=6334,  # gRPC port
    prefer_grpc=True,
    timeout=30,
)

# pgvector with connection pool
from psycopg2 import pool

connection_pool = pool.ThreadedConnectionPool(
    minconn=5,
    maxconn=20,
    dsn="postgresql://user:pass@localhost/db"
)

def get_connection():
    return connection_pool.getconn()

def release_connection(conn):
    connection_pool.putconn(conn)
```

### Monitoring

```python
# Qdrant metrics
info = client.get_collection("documents")
print(f"Points: {info.points_count}")
print(f"Indexed: {info.indexed_vectors_count}")
print(f"Segments: {info.segments_count}")

# Search latency tracking
import time

def timed_search(query: str, k: int = 10):
    start = time.perf_counter()
    results = client.search(
        collection_name="documents",
        query_vector=get_embedding(query),
        limit=k,
    )
    latency = time.perf_counter() - start

    # Log or metric
    print(f"Search latency: {latency*1000:.2f}ms")

    return results
```

---

## Backup and Migration

### Qdrant Backup

```python
# Create snapshot
snapshot_info = client.create_snapshot(
    collection_name="documents"
)

# List snapshots
snapshots = client.list_snapshots(
    collection_name="documents"
)

# Restore from snapshot
client.recover_snapshot(
    collection_name="documents",
    location=f"http://localhost:6333/collections/documents/snapshots/{snapshot_name}"
)
```

### Cross-Database Migration

```python
def migrate_qdrant_to_pgvector(
    qdrant_client,
    pg_connection,
    collection_name: str,
    batch_size: int = 100
):
    """Migrate from Qdrant to pgvector."""
    offset = None

    while True:
        # Scroll through Qdrant
        points, offset = qdrant_client.scroll(
            collection_name=collection_name,
            limit=batch_size,
            offset=offset,
            with_vectors=True,
            with_payload=True,
        )

        if not points:
            break

        # Insert into PostgreSQL
        cur = pg_connection.cursor()
        data = [
            (p.id, p.payload.get("text"), p.vector)
            for p in points
        ]

        execute_values(cur, """
            INSERT INTO documents (id, content, embedding)
            VALUES %s
            ON CONFLICT (id) DO UPDATE SET
                content = EXCLUDED.content,
                embedding = EXCLUDED.embedding
        """, data)

        pg_connection.commit()

        if offset is None:
            break
```

---

## Security Best Practices

### API Key Management

```python
import os

# Environment variables
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

# Secure connection
client = QdrantClient(
    url="https://your-cluster.qdrant.io",
    api_key=QDRANT_API_KEY,
    https=True,
)
```

### Access Control

```python
# Qdrant with read-only key
read_only_client = QdrantClient(
    url="https://cluster.qdrant.io",
    api_key=READ_ONLY_API_KEY,
)

# PostgreSQL with restricted user
# CREATE USER vectordb_reader WITH PASSWORD '...';
# GRANT SELECT ON documents TO vectordb_reader;
```

### Data Encryption

```python
# Encrypt sensitive payloads
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt_payload(payload: dict) -> dict:
    """Encrypt sensitive fields."""
    encrypted = payload.copy()
    if "pii" in encrypted:
        encrypted["pii"] = cipher.encrypt(
            encrypted["pii"].encode()
        ).decode()
    return encrypted

def decrypt_payload(payload: dict) -> dict:
    """Decrypt sensitive fields."""
    decrypted = payload.copy()
    if "pii" in decrypted:
        decrypted["pii"] = cipher.decrypt(
            decrypted["pii"].encode()
        ).decode()
    return decrypted
```

---

## Integration

### Used By Agents

| Agent | Purpose |
|-------|---------|
| `faion-rag-agent` | Build and query knowledge bases |
| `faion-embedding-agent` | Generate and store embeddings |

### Related Skills

| Skill | Integration |
|-------|-------------|
| `faion-embeddings-skill` | Generate vectors for storage |
| `faion-langchain-skill` | LangChain vector store adapters |
| `faion-llamaindex-skill` | LlamaIndex vector store adapters |

---

## References

- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Weaviate Documentation](https://weaviate.io/developers/weaviate)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [Chroma Documentation](https://docs.trychroma.com/)
- [Pinecone Documentation](https://docs.pinecone.io/)

---

*Vector Database Skill v1.0*
*Technical Skill (Layer 3)*
*Part of AI/LLM Skill Suite*
