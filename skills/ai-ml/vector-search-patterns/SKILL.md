---
name: Vector Search Patterns
description: Implementing semantic search and similarity search using vector embeddings and vector databases.
---

# Vector Search Patterns

## Overview

Vector search (also known as semantic search or similarity search) enables finding similar items based on their meaning rather than exact keyword matches. It uses vector embeddings to represent data as points in high-dimensional space, where similarity is measured as distance between points.

## Prerequisites

- Understanding of vector mathematics and linear algebra
- Knowledge of machine learning and embeddings
- Familiarity with Python and numerical computing (numpy, scikit-learn)
- Understanding of database concepts and indexing
- Basic knowledge of cloud services (AWS, GCP, Azure)
- Experience with vector databases or similarity search

## Key Concepts

- **Vector/Semantic Search**: Finding similar items based on meaning rather than exact keyword matches
- **Embeddings**: Converting text/images to vectors for similarity comparison
- **Vector Databases**: Specialized databases for efficient vector storage and retrieval
- **Distance Metrics**: Cosine similarity, Euclidean distance, dot product for measuring vector similarity
- **Indexing Algorithms**: HNSW (graph-based), IVF (clustering), PQ (quantization) for efficient search
- **Hybrid Search**: Combining vector search with keyword search for better results
- **RAG (Retrieval-Augmented Generation)**: Using retrieved context to improve LLM responses
- **Chunking**: Splitting documents into smaller pieces for better indexing and retrieval
- **Query Optimization**: Caching, batching, expansion techniques for better performance
- **Scaling Strategies**: Sharding, replication, horizontal scaling for large datasets
- **Evaluation Metrics**: Recall@K, Precision@K, MAP, MRR, NDCG for measuring search quality

## What is Vector Search / Semantic Search

### Traditional vs Vector Search

**Traditional Keyword Search:**
- Matches exact words or phrases
- Requires exact spelling
- Limited understanding of context
- Example: "car" won't match "automobile"

**Vector/Semantic Search:**
- Matches based on meaning
- Understands context and synonyms
- Handles typos and variations
- Example: "car" will match "automobile", "vehicle", "sedan"

### How It Works

1. **Embedding**: Convert text/images to vectors using ML models
2. **Indexing**: Store vectors in a vector database with efficient indexing
3. **Querying**: Convert query to vector, find nearest neighbors
4. **Ranking**: Return results sorted by similarity

```
Query: "Find similar products"

Text → Embedding Model → Vector: [0.1, -0.2, 0.8, ...]
                                    ↓
                              Vector Database
                                    ↓
                    [0.2, -0.1, 0.7, ...]  ← Product A (0.92 similar)
                    [0.3, -0.3, 0.6, ...]  ← Product B (0.87 similar)
                    [0.4, -0.4, 0.5, ...]  ← Product C (0.81 similar)
```

## Embeddings Fundamentals

### Text Embeddings

Text embeddings represent words, sentences, or documents as dense vectors.

```python
from sentence_transformers import SentenceTransformer

# Load pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
text = "The quick brown fox jumps over the lazy dog"
embedding = model.encode(text)

print(f"Embedding shape: {embedding.shape}")  # (384,)
print(f"Embedding: {embedding}")
```

**Popular Text Embedding Models:**

| Model | Dimension | Use Case | Provider |
|--------|-----------|-----------|----------|
| text-embedding-ada-002 | 1536 | General purpose | OpenAI |
| text-embedding-3-small | 1536 | Fast, cost-effective | OpenAI |
| all-MiniLM-L6-v2 | 384 | Lightweight, multilingual | Hugging Face |
| e5-large-v2 | 1024 | High quality | Hugging Face |
| Cohere embed-v3 | 1024 | Multilingual | Cohere |

### Image Embeddings

```python
from PIL import Image
import clip
import torch

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Generate image embedding
image = preprocess(Image.open("product.jpg")).unsqueeze(0).to(device)
with torch.no_grad():
    image_features = model.encode_image(image).float()

print(f"Image embedding shape: {image_features.shape}")
```

**Popular Image Embedding Models:**

| Model | Dimension | Use Case | Provider |
|--------|-----------|-----------|----------|
| CLIP ViT-B/32 | 512 | Image-text retrieval | OpenAI |
| CLIP ViT-L/14 | 768 | High quality | OpenAI |
| ResNet-50 | 2048 | Image similarity | PyTorch |

### Multi-Modal Embeddings

```python
# OpenAI CLIP for multi-modal
import openai

client = openai.OpenAI()

# Text embedding
text_embedding = client.embeddings.create(
    model="text-embedding-ada-002",
    input="A red sports car"
)

# Image embedding (using vision model)
image_embedding = client.images.embed(
    model="clip-vit-large-patch14",
    image=open("car.jpg", "rb")
)
```

## Vector Databases

### Pinecone

**Setup:**

```python
import pinecone

# Initialize Pinecone
pc = pinecone.Pinecone(
    api_key="your-api-key"
)

# Create index
index_name = "products"
if index_name not in [index.name for index in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=1536,  # OpenAI embedding dimension
        metric="cosine",  # Similarity metric
        spec=pinecone.ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Get index
index = pc.Index(index_name)
```

**Upsert Vectors:**

```python
# Upsert (update or insert) vectors
vectors = [
    {
        "id": "prod_1",
        "values": [0.1, -0.2, 0.8, ...],  # 1536-dimensional
        "metadata": {
            "name": "Running Shoes",
            "category": "Sports",
            "price": 99.99
        }
    },
    {
        "id": "prod_2",
        "values": [0.2, -0.1, 0.7, ...],
        "metadata": {
            "name": "Basketball",
            "category": "Sports",
            "price": 29.99
        }
    }
]

index.upsert(vectors=vectors)
```

**Query:**

```python
# Query for similar items
query_embedding = model.encode("athletic footwear")

results = index.query(
    vector=query_embedding.tolist(),
    top_k=5,
    include_metadata=True,
    filter={
        "category": {"$eq": "Sports"},
        "price": {"$lte": 100}
    }
)

for match in results['matches']:
    print(f"Product: {match['metadata']['name']}")
    print(f"Score: {match['score']}")
```

### Weaviate

**Setup:**

```python
import weaviate

# Connect to Weaviate
client = weaviate.Client(
    url="http://localhost:8080"
)

# Create class (schema)
client.schema.create_class({
    "class": "Product",
    "properties": [
        {
            "name": "name",
            "dataType": ["text"]
        },
        {
            "name": "description",
            "dataType": ["text"]
        },
        {
            "name": "price",
            "dataType": ["number"]
        },
        {
            "name": "category",
            "dataType": ["string"]
        }
    ],
    "vectorizer": "text2vec-openai",  # Use OpenAI embeddings
    "moduleConfig": {
        "type": "text",
        "model": "ada",
        "version": "002"
    }
})
```

**Add Objects:**

```python
# Add objects with automatic vectorization
product_obj = {
    "name": "Running Shoes",
    "description": "Comfortable running shoes for daily training",
    "price": 99.99,
    "category": "Sports"
}

client.data_object.create(
    class_name="Product",
    data_object=product_obj
)
```

**Query:**

```python
# Semantic search
query_text = "athletic footwear"

results = client.query.get(
    class_name="Product",
    properties=["name", "description", "price", "category"],
    near_text={
        "concepts": [query_text],
        "certainty": 0.7
    },
    limit=5
)

for result in results.objects:
    print(f"Product: {result.properties['name']}")
    print(f"Certainty: {result.certainty}")
```

### Qdrant

**Setup:**

```python
from qdrant_client import QdrantClient

# Initialize Qdrant
client = QdrantClient(url="http://localhost:6333")

# Create collection
client.recreate_collection(
    collection_name="products",
    vectors_config={
        "size": 1536,  # Embedding dimension
        "distance": "Cosine"
    }
)
```

**Upsert Points:**

```python
# Insert vectors
points = [
    {
        "id": 1,
        "vector": [0.1, -0.2, 0.8, ...],
        "payload": {
            "name": "Running Shoes",
            "category": "Sports",
            "price": 99.99
        }
    },
    {
        "id": 2,
        "vector": [0.2, -0.1, 0.7, ...],
        "payload": {
            "name": "Basketball",
            "category": "Sports",
            "price": 29.99
        }
    }
]

client.upsert(
    collection_name="products",
    points=points
)
```

**Query:**

```python
# Search for similar items
query_vector = model.encode("athletic footwear")

results = client.search(
    collection_name="products",
    query_vector=query_vector.tolist(),
    limit=5,
    with_payload=True,
    query_filter={
        "must": [
            {
                "key": "category",
                "match": {"value": "Sports"}
            },
            {
                "key": "price",
                "range": {"lte": 100}
            }
        ]
    }
)

for result in results:
    print(f"Product: {result.payload['name']}")
    print(f"Score: {result.score}")
```

### Milvus

**Setup:**

```python
from pymilvus import connections, utility, Collection

# Connect to Milvus
connections.connect(host="localhost", port="19530")

# Define collection schema
field_name = "product_id"
field_vector = "product_vector"
field_name = "product_name"
field_price = "price"
field_category = "category"

schema = [
    utility.FieldSchema(name=field_name, dtype=DataType.INT64, is_primary=True),
    utility.FieldSchema(name=field_vector, dtype=DataType.FLOAT_VECTOR, dim=1536),
    utility.FieldSchema(name=field_name, dtype=DataType.VARCHAR, max_length=256),
    utility.FieldSchema(name=field_price, dtype=DataType.DOUBLE),
    utility.FieldSchema(name=field_category, dtype=DataType.VARCHAR, max_length=64),
]

# Create collection
collection_name = "products"
if utility.has_collection(collection_name):
    utility.drop_collection(collection_name)

collection = Collection(
    name=collection_name,
    schema=schema
)
collection.create()

# Create index
index_params = {
    "metric_type": "COSINE",
    "index_type": "IVF_FLAT",
    "params": {"nlist": 128}
}
collection.create_index(
    field_name=field_vector,
    index_params=index_params
)
collection.load()
```

**Insert Vectors:**

```python
# Insert vectors
entities = [
    [1, [0.1, -0.2, 0.8, ...], "Running Shoes", 99.99, "Sports"],
    [2, [0.2, -0.1, 0.7, ...], "Basketball", 29.99, "Sports"],
]

ids = collection.insert(entities)
```

**Query:**

```python
# Search for similar items
query_vector = model.encode("athletic footwear")

search_params = {
    "metric_type": "COSINE",
    "params": {"nprobe": 16}
}

results = collection.search(
    data=[query_vector.tolist()],
    anns_field=field_vector,
    param=search_params,
    limit=5,
    expr=f"category == 'Sports' && price <= 100"
)

for result in results[0]:
    print(f"Product: {result['entity']['product_name']}")
    print(f"Distance: {result['distance']}")
```

### Chroma

**Setup:**

```python
import chromadb

# Initialize Chroma
chroma_client = chromadb.Client()

# Create collection
collection = chroma_client.create_collection(
    name="products",
    metadata={"hnsw:space": "cosine"}
)
```

**Add Documents:**

```python
# Add documents with embeddings
documents = [
    "Comfortable running shoes for daily training",
    "Professional basketball for competitive play"
]

metadatas = [
    {"name": "Running Shoes", "category": "Sports", "price": 99.99},
    {"name": "Basketball", "category": "Sports", "price": 29.99}
]

ids = ["prod_1", "prod_2"]

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)
```

**Query:**

```python
# Semantic search
query_text = "athletic footwear"

results = collection.query(
    query_texts=[query_text],
    n_results=5,
    where={"category": "Sports", "price": {"$lte": 100}}
)

for result in results['ids'][0]:
    print(f"ID: {result}")
    print(f"Document: {results['documents'][0][results['ids'][0].index(result)]}")
    print(f"Distance: {results['distances'][0][results['ids'][0].index(result)]}")
```

### pgvector (PostgreSQL)

**Setup:**

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table with vector column
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(256),
    description TEXT,
    price DECIMAL(10,2),
    category VARCHAR(64),
    embedding vector(1536)  -- 1536-dimensional vector
);

-- Create HNSW index for fast search
CREATE INDEX ON products USING hnsw (embedding vector_cosine_ops);
```

**Insert Vectors:**

```sql
-- Insert with embedding
INSERT INTO products (name, description, price, category, embedding)
VALUES (
    'Running Shoes',
    'Comfortable running shoes for daily training',
    99.99,
    'Sports',
    '[0.1, -0.2, 0.8, ...]'::vector
);
```

**Query:**

```sql
-- Semantic search
SELECT 
    id,
    name,
    description,
    price,
    category,
    1 - (embedding <=> '[0.1, -0.2, 0.8, ...]'::vector) AS similarity
FROM products
WHERE category = 'Sports'
  AND price <= 100
ORDER BY embedding <=> '[0.1, -0.2, 0.8, ...]'::vector
LIMIT 5;
```

### Redis Vector Search

**Setup:**

```python
import redis
from redis.commands.search.field import VectorField

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Create index
r.ft.create_index(
    name="products_idx",
    schema=[
        VectorField("embedding", "HNSW", {
            "TYPE": "FLOAT32",
            "DIM": 1536,
            "DISTANCE_METRIC": "COSINE",
            "INITIAL_CAP": 1000,
            "BLOCK_SIZE": 128
        }),
        "name", "TEXT",
        "category", "TAG",
        "price", "NUMERIC"
    ]
)
```

**Add Documents:**

```python
# Add documents with embeddings
r.hset(
    "prod:1",
    mapping={
        "name": "Running Shoes",
        "category": "Sports",
        "price": 99.99,
        "embedding": np.array([0.1, -0.2, 0.8, ...]).astype(np.float32).tobytes()
    }
)

r.hset(
    "prod:2",
    mapping={
        "name": "Basketball",
        "category": "Sports",
        "price": 29.99,
        "embedding": np.array([0.2, -0.1, 0.7, ...]).astype(np.float32).tobytes()
    }
)
```

**Query:**

```python
# Semantic search
query_vector = model.encode("athletic footwear").astype(np.float32).tobytes()

results = r.ft.search(
    index_name="products_idx",
    query="*=>[KNN 5 @embedding $vector]",
    query_params={
        "vector": query_vector
    },
    filter="@category:{Sports} @price:[-inf 100]"
)

for result in results.docs:
    print(f"Product: {result.name}")
    print(f"Score: {result.__score}")
```

## Distance Metrics

### Cosine Similarity

Measures the cosine of the angle between two vectors. Range: [-1, 1].

```python
import numpy as np

def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return dot_product / (norm_v1 * norm_v2)

# Distance = 1 - similarity
cosine_distance = 1 - cosine_similarity(v1, v2)
```

**When to use:**
- Text embeddings (OpenAI, Cohere)
- Direction doesn't matter
- Magnitude doesn't matter

### Euclidean Distance

Measures the straight-line distance between two vectors.

```python
def euclidean_distance(v1, v2):
    return np.linalg.norm(v1 - v2)
```

**When to use:**
- When magnitude matters
- Spatial data
- Some image embeddings

### Dot Product

Measures the dot product of two vectors.

```python
def dot_product(v1, v2):
    return np.dot(v1, v2)
```

**When to use:**
- Normalized vectors
- Faster than cosine
- Same as cosine for normalized vectors

**Comparison:**

| Metric | Range | Use Case | Pros | Cons |
|--------|-------|-----------|-------|------|
| Cosine | [0, 2] | Text embeddings | Magnitude independent | Slower |
| Euclidean | [0, ∞] | Spatial data | Intuitive | Magnitude dependent |
| Dot Product | [-1, 1] | Normalized vectors | Fastest | Requires normalization |

## Indexing Algorithms

### HNSW (Hierarchical Navigable Small World)

A graph-based approximate nearest neighbor algorithm.

```python
# Pinecone uses HNSW by default
index = pc.Index("products", metric="cosine")

# HNSW parameters
index.update(
    name="products",
    spec=pinecone.ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)
```

**Pros:**
- Fast queries
- Good for large datasets
- Scalable

**Cons:**
- Approximate (not exact)
- Requires tuning (M, efConstruction)

### IVF (Inverted File)

Divides space into Voronoi cells.

```python
# Milvus IVF configuration
index_params = {
    "metric_type": "COSINE",
    "index_type": "IVF_FLAT",
    "params": {
        "nlist": 128  # Number of clusters
    }
}

collection.create_index(
    field_name="embedding",
    index_params=index_params
)
```

**Pros:**
- Good for medium datasets
- Faster than brute force
- Exact search

**Cons:**
- Requires tuning (nlist)
- Slower than HNSW for large datasets

### PQ (Product Quantization)

Compresses vectors for faster search and less memory.

```python
# Milvus PQ configuration
index_params = {
    "metric_type": "COSINE",
    "index_type": "IVF_PQ",
    "params": {
        "nlist": 128,
        "m": 8  # Number of sub-vectors
    }
}

collection.create_index(
    field_name="embedding",
    index_params=index_params
)
```

**Pros:**
- Very fast queries
- Low memory usage
- Good for very large datasets

**Cons:**
- Loss of precision
- Requires tuning
- More complex

**Comparison:**

| Algorithm | Speed | Memory | Precision | Use Case |
|----------|-------|--------|-----------|
| HNSW | Fast | Medium | High | Large datasets |
| IVF | Medium | Low | Exact | Medium datasets |
| PQ | Very Fast | Very Low | Medium | Very large datasets |
| Flat | Slow | High | Exact | Small datasets |

## Hybrid Search (Vector + Keyword)

### Combining Semantic and Keyword Search

```python
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")

# Hybrid search with both vector and keyword
results = client.search(
    collection_name="products",
    query_vector=query_embedding.tolist(),
    query_filter={
        "must": [
            {
                "key": "category",
                "match": {"value": "Sports"}
            },
            {
                "key": "name",
                "match": {"value": "*running*"}  # Keyword match
            }
        ]
    },
    limit=10
)
```

### Reciprocal Rank Fusion (RRF)

Combine results from multiple sources.

```python
def reciprocal_rank_fusion(vector_results, keyword_results, k=60):
    scores = {}
    
    # Score vector results
    for i, result in enumerate(vector_results):
        doc_id = result['id']
        rank = i + 1
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    
    # Score keyword results
    for i, result in enumerate(keyword_results):
        doc_id = result['id']
        rank = i + 1
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    
    # Sort by combined score
    sorted_results = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    return sorted_results[:10]
```

### Weighted Hybrid Search

```python
def weighted_hybrid_search(vector_results, keyword_results, alpha=0.5):
    combined = {}
    
    # Combine with weights
    for result in vector_results:
        doc_id = result['id']
        combined[doc_id] = combined.get(doc_id, 0) + alpha * result['score']
    
    for result in keyword_results:
        doc_id = result['id']
        combined[doc_id] = combined.get(doc_id, 0) + (1 - alpha) * result['score']
    
    # Sort by combined score
    sorted_results = sorted(
        combined.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    return sorted_results[:10]
```

## Filtering and Metadata

### Pre-Filtering

Filter results before vector search.

```python
# Pinecone pre-filtering
results = index.query(
    vector=query_embedding.tolist(),
    top_k=10,
    filter={
        "category": {"$eq": "Sports"},
        "price": {"$lte": 100},
        "in_stock": {"$eq": True}
    }
)
```

### Post-Filtering

Filter results after vector search.

```python
# Get results first
results = index.query(
    vector=query_embedding.tolist(),
    top_k=100  # Get more results
)

# Then filter
filtered_results = [
    r for r in results['matches']
    if r['metadata']['price'] <= 100
    and r['metadata']['category'] == 'Sports'
    and r['metadata']['in_stock'] == True
][:10]  # Take top 10
```

### Metadata Schema Design

```python
# Good metadata schema
metadata = {
    "name": "Running Shoes",           # String for filtering
    "category": "Sports",              # String for filtering
    "price": 99.99,                  # Numeric for range filtering
    "in_stock": True,                 # Boolean for filtering
    "brand": "Nike",                   # String for filtering
    "color": ["red", "blue"],         # Array for filtering
    "rating": 4.5,                    # Numeric for sorting
    "created_at": "2024-01-01"        # Date for filtering
}
```

## RAG (Retrieval Augmented Generation) Patterns

### Basic RAG Flow

```python
from openai import OpenAI

client = OpenAI()

# 1. Retrieve relevant documents
query_embedding = model.encode("What are the benefits of running?")
results = index.query(
    vector=query_embedding.tolist(),
    top_k=5
)

# 2. Construct prompt with retrieved context
context = "\n\n".join([
    f"{r['metadata']['name']}: {r['metadata']['description']}"
    for r in results['matches']
])

prompt = f"""
Context:
{context}

Question: What are the benefits of running?

Answer based on the context above.
"""

# 3. Generate response
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
)

print(response.choices[0].message.content)
```

### Reranking Results

```python
from sentence_transformers import CrossEncoder

# Load reranker
reranker = CrossEncoder('ms-marco-MiniLM-L-6-v3')

# 1. Get initial results
initial_results = index.query(
    vector=query_embedding.tolist(),
    top_k=20
)

# 2. Rerank with cross-encoder
query = "What are the benefits of running?"
documents = [r['metadata']['description'] for r in initial_results['matches']]

reranked_scores = reranker.predict(
    [(query, doc) for doc in documents]
)

# 3. Combine and sort
for i, result in enumerate(initial_results['matches']):
    result['rerank_score'] = reranked_scores[i]

final_results = sorted(
    initial_results['matches'],
    key=lambda x: x['rerank_score'],
    reverse=True
)[:10]  # Top 10
```

### Hybrid RAG

```python
def hybrid_rag(query):
    # Vector search
    query_embedding = model.encode(query)
    vector_results = index.query(
        vector=query_embedding.tolist(),
        top_k=10
    )
    
    # Keyword search
    keyword_results = keyword_search(query)
    
    # Combine with RRF
    combined = reciprocal_rank_fusion(
        vector_results['matches'],
        keyword_results
    )
    
    # Use top results for RAG
    context = "\n\n".join([
        f"{r['metadata']['name']}: {r['metadata']['description']}"
        for r in combined[:5]
    ])
    
    # Generate response
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ]
    )
    
    return response.choices[0].message.content
```

## Chunking Strategies for Documents

### Fixed-Size Chunking

```python
def fixed_size_chunking(text, chunk_size=500):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
    return chunks

text = "This is a long document that needs to be chunked..."
chunks = fixed_size_chunking(text, chunk_size=500)
```

### Semantic Chunking

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_chunking(text):
    sentences = text.split('. ')  # Simple sentence split
    chunks = []
    current_chunk = []
    current_embedding = None
    
    for sentence in sentences:
        sentence_embedding = model.encode(sentence)
        
        if current_embedding is None:
            current_chunk.append(sentence)
            current_embedding = sentence_embedding
        else:
            # Check similarity
            similarity = cosine_similarity(current_embedding, sentence_embedding)
            
            if similarity < 0.7:  # Low similarity, new chunk
                chunks.append('. '.join(current_chunk))
                current_chunk = [sentence]
                current_embedding = sentence_embedding
            else:
                current_chunk.append(sentence)
    
    if current_chunk:
        chunks.append('. '.join(current_chunk))
    
    return chunks
```

### Sliding Window Chunking

```python
def sliding_window_chunking(text, window_size=500, stride=250):
    chunks = []
    for i in range(0, len(text) - window_size + 1, stride):
        chunk = text[i:i + window_size]
        chunks.append(chunk)
    return chunks

text = "This is a long document that needs to be chunked..."
chunks = sliding_window_chunking(text, window_size=500, stride=250)
```

## Query Optimization

### Query Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_query(query_text):
    query_embedding = model.encode(query_text)
    return index.query(
        vector=query_embedding.tolist(),
        top_k=10
    )
```

### Batch Queries

```python
def batch_query(queries):
    query_embeddings = model.encode(queries)
    
    results = []
    for embedding in query_embeddings:
        result = index.query(
            vector=embedding.tolist(),
            top_k=10
        )
        results.append(result)
    
    return results
```

### Query Expansion

```python
def query_expansion(query):
    # Generate variations
    variations = [
        query,
        query.replace("shoes", "footwear"),
        query.replace("running", "athletic"),
    ]
    
    # Query all variations
    all_results = []
    for variation in variations:
        embedding = model.encode(variation)
        results = index.query(
            vector=embedding.tolist(),
            top_k=10
        )
        all_results.extend(results['matches'])
    
    # Deduplicate and re-rank
    seen = set()
    unique_results = []
    for result in all_results:
        if result['id'] not in seen:
            seen.add(result['id'])
            unique_results.append(result)
    
    return unique_results[:10]
```

## Scaling Vector Search

### Horizontal Scaling

```python
# Multiple Pinecone indexes
indexes = [
    pc.Index("products_shard_1"),
    pc.Index("products_shard_2"),
    pc.Index("products_shard_3"),
]

def query_all_shards(query_embedding):
    results = []
    for index in indexes:
        result = index.query(
            vector=query_embedding.tolist(),
            top_k=10
        )
        results.extend(result['matches'])
    
    # Merge and re-rank
    merged = merge_results(results)
    return merged[:10]
```

### Sharding Strategy

```python
def get_shard_index(product_id, num_shards=3):
    # Consistent hashing
    shard_id = product_id % num_shards
    return f"products_shard_{shard_id}"

# Insert to correct shard
product_id = 123
shard_index_name = get_shard_index(product_id)
shard_index = pc.Index(shard_index_name)
```

### Replication

```python
# Replicate data for read scaling
primary_index = pc.Index("products_primary")
replica_index = pc.Index("products_replica")

# Query from nearest replica
results = replica_index.query(
    vector=query_embedding.tolist(),
    top_k=10
)
```

## Cost Optimization

### Dimensionality Reduction

```python
from sklearn.decomposition import PCA

# Original embeddings (1536 dimensions)
original_embeddings = model.encode(texts)

# Reduce to 256 dimensions
pca = PCA(n_components=256)
reduced_embeddings = pca.fit_transform(original_embeddings)

print(f"Original: {original_embeddings.shape}")
print(f"Reduced: {reduced_embeddings.shape}")
```

### Quantization

```python
import numpy as np

# Float32 to uint8
def quantize_vector(vector, bits=8):
    # Find min and max
    min_val = np.min(vector)
    max_val = np.max(vector)
    
    # Quantize
    quantized = np.round(
        (vector - min_val) / (max_val - min_val) * (2**bits - 1)
    ).astype(np.uint8)
    
    return quantized

# Store quantized vectors
quantized_embeddings = [quantize_vector(v) for v in embeddings]
```

### Caching Strategy

```python
from functools import lru_cache
import hashlib

def get_cache_key(text):
    return hashlib.md5(text.encode()).hexdigest()

@lru_cache(maxsize=1000)
def cached_search(query_text):
    cache_key = get_cache_key(query_text)
    
    # Check cache
    if cache_key in search_cache:
        return search_cache[cache_key]
    
    # Perform search
    query_embedding = model.encode(query_text)
    results = index.query(
        vector=query_embedding.tolist(),
        top_k=10
    )
    
    # Cache results
    search_cache[cache_key] = results
    
    return results
```

## Evaluation Metrics

### Recall@K

```python
def recall_at_k(relevant_ids, retrieved_ids, k):
    retrieved_at_k = set(retrieved_ids[:k])
    relevant_set = set(relevant_ids)
    
    recall = len(retrieved_at_k & relevant_set) / len(relevant_set)
    return recall

# Example
relevant_ids = [1, 5, 8, 12]  # Ground truth
retrieved_ids = [1, 3, 5, 8, 10, 12]  # Retrieved results

recall_5 = recall_at_k(relevant_ids, retrieved_ids, k=5)
print(f"Recall@5: {recall_5}")
```

### Precision@K

```python
def precision_at_k(relevant_ids, retrieved_ids, k):
    retrieved_at_k = set(retrieved_ids[:k])
    relevant_set = set(relevant_ids)
    
    precision = len(retrieved_at_k & relevant_set) / k
    return precision

precision_5 = precision_at_k(relevant_ids, retrieved_ids, k=5)
print(f"Precision@5: {precision_5}")
```

### Mean Reciprocal Rank (MRR)

```python
def mean_reciprocal_rank(relevant_ids, retrieved_ids):
    mrr = 0
    for relevant_id in relevant_ids:
        try:
            rank = retrieved_ids.index(relevant_id) + 1
            mrr += 1 / rank
        except ValueError:
            mrr += 0
    
    return mrr / len(relevant_ids)

mrr = mean_reciprocal_rank(relevant_ids, retrieved_ids)
print(f"MRR: {mrr}")
```

### Normalized Discounted Cumulative Gain (NDCG)

```python
def dcg(relevance_scores, k):
    dcg = relevance_scores[0]
    for i in range(1, min(k, len(relevance_scores))):
        dcg += relevance_scores[i] / np.log2(i + 2)
    return dcg

def ndcg(relevance_scores, k):
    # Ideal DCG
    ideal_relevance = sorted(relevance_scores, reverse=True)
    idcg = dcg(ideal_relevance, k)
    
    # Actual DCG
    actual_dcg = dcg(relevance_scores, k)
    
    return actual_dcg / idcg if idcg > 0 else 0

relevance_scores = [1, 0, 1, 0, 1]  # Binary relevance
ndcg_5 = ndcg(relevance_scores, k=5)
print(f"NDCG@5: {ndcg_5}")
```

## Common Use Cases

### Semantic Document Search

```python
def search_documents(query, top_k=10):
    query_embedding = model.encode(query)
    
    results = index.query(
        vector=query_embedding.tolist(),
        top_k=top_k,
        include_metadata=True
    )
    
    return [
        {
            "id": r['id'],
            "title": r['metadata']['title'],
            "content": r['metadata']['content'],
            "score": r['score']
        }
        for r in results['matches']
    ]
```

### Similar Product Recommendations

```python
def similar_products(product_id, top_k=5):
    # Get product embedding
    product = get_product(product_id)
    product_embedding = product['embedding']
    
    # Find similar products
    results = index.query(
        vector=product_embedding.tolist(),
        top_k=top_k + 1,  # +1 to exclude self
        filter={"category": {"$eq": product['category']}}
    )
    
    # Exclude the product itself
    similar = [
        r for r in results['matches']
        if r['id'] != product_id
    ]
    
    return similar[:top_k]
```

### Question Answering

```python
def answer_question(question):
    # Retrieve relevant documents
    query_embedding = model.encode(question)
    results = index.query(
        vector=query_embedding.tolist(),
        top_k=5
    )
    
    # Build context
    context = "\n\n".join([
        f"Document: {r['metadata']['text']}"
        for r in results['matches']
    ])
    
    # Generate answer
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Answer the question based on the provided context."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ]
    )
    
    return response.choices[0].message.content
```

### Duplicate Detection

```python
def find_duplicates(text, threshold=0.95):
    text_embedding = model.encode(text)
    
    # Find similar documents
    results = index.query(
        vector=text_embedding.tolist(),
        top_k=10
    )
    
    # Filter by threshold
    duplicates = [
        r for r in results['matches']
        if r['score'] >= threshold
    ]
    
    return duplicates
```

## Best Practices and Gotchas

### Best Practices

1. **Embedding Selection**
   - Choose appropriate model for your use case
   - Consider embedding dimension vs performance
   - Test multiple models before committing

2. **Index Configuration**
   - Tune HNSW parameters (M, efConstruction)
   - Choose appropriate distance metric
   - Consider trade-offs between speed and accuracy

3. **Query Optimization**
   - Use pre-filtering when possible
   - Implement query caching
   - Consider reranking for better results

4. **Metadata Design**
   - Store relevant metadata for filtering
   - Use appropriate data types
   - Index metadata fields

5. **Monitoring**
   - Track query latency
   - Monitor hit rates
   - Set up alerts for anomalies

### Common Gotchas

1. **Embedding Dimension Mismatch**
   ```python
   # Wrong: Different dimensions
   model1 = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dim
   model2 = SentenceTransformer('all-MiniLM-L12-v2')  # 768 dim
   
   # Correct: Use same model for all embeddings
   model = SentenceTransformer('all-MiniLM-L6-v2')
   ```

2. **Not Normalizing Vectors**
   ```python
   # Wrong: Not normalized
   vector = model.encode(text)
   
   # Correct: Normalize for cosine similarity
   vector = model.encode(text)
   vector = vector / np.linalg.norm(vector)  # Normalize
   ```

3. **Ignoring Metadata Filtering**
   ```python
   # Wrong: No filtering
   results = index.query(vector=query, top_k=10)
   
   # Correct: Apply filters
   results = index.query(
       vector=query,
       top_k=10,
       filter={"category": {"$eq": "Sports"}}
   )
   ```

4. **Not Handling Empty Results**
   ```python
   # Wrong: Assume results exist
   results = index.query(vector=query, top_k=10)
   for r in results['matches']:
       print(r)
   
   # Correct: Handle empty results
   results = index.query(vector=query, top_k=10)
   if not results['matches']:
       return []
   ```

## Related Skills

- `04-database/vector-database`
- `06-ai-ml-production/rag-patterns`
- `06-ai-ml-production/embeddings`
