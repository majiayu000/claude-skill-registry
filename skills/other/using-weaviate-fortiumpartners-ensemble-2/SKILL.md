---
name: using-weaviate
description: Weaviate vector database for semantic search, hybrid queries, and AI-native applications. Use for embeddings storage, similarity search, RAG pipelines, and multi-modal retrieval.
---

# Weaviate Vector Database Skill

**Version**: 1.0.0 | **Target**: <500 lines | **Purpose**: Fast reference for Weaviate operations

---

## Overview

**What is Weaviate**: Open-source vector database for AI-native applications combining vector search with structured filtering and keyword search.

**When to Use This Skill**:
- Storing and querying vector embeddings
- Implementing semantic/similarity search
- Building RAG (Retrieval-Augmented Generation) pipelines
- Hybrid search (vector + keyword)
- Multi-tenant vector applications

**Auto-Detection Triggers**:
- `weaviate-client` in `requirements.txt` or `pyproject.toml`
- `weaviate-client` or `weaviate-ts-client` in `package.json`
- `WEAVIATE_URL`, `WEAVIATE_API_KEY`, or `WCD_URL` environment variables
- `docker-compose.yml` with `semitechnologies/weaviate` image

**Progressive Disclosure**:
- **This file (SKILL.md)**: Quick reference for immediate use
- **REFERENCE.md**: Comprehensive patterns, modules, and advanced configuration

---

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Quick Start](#quick-start)
3. [CLI Decision Tree](#cli-decision-tree)
4. [Collection Schema](#collection-schema)
5. [Data Operations](#data-operations)
6. [Search Operations](#search-operations)
7. [Generative Search (RAG)](#generative-search-rag)
8. [Multi-Tenancy](#multi-tenancy)
9. [Docker Setup](#docker-setup)
10. [Error Handling](#error-handling)
11. [Best Practices](#best-practices)
12. [Quick Reference Card](#quick-reference-card)
13. [Agent Integration](#agent-integration)

---

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Collection** | Schema definition for a data type (formerly "Class") |
| **Object** | Individual data item with properties and vector |
| **Vector** | Numerical representation of data for similarity search |
| **Module** | Plugin for vectorization, generative AI, or reranking |
| **Tenant** | Isolated data partition for multi-tenant applications |

---

## Quick Start

### Python Setup

```python
import weaviate
from weaviate.classes.init import Auth

# Connect to Weaviate Cloud (recommended: use context manager)
with weaviate.connect_to_weaviate_cloud(
    cluster_url="https://your-cluster.weaviate.network",
    auth_credentials=Auth.api_key("your-wcd-api-key"),
    headers={"X-OpenAI-Api-Key": "your-openai-key"}
) as client:
    print(client.is_ready())  # True

# Or connect to local instance
client = weaviate.connect_to_local()
```

### TypeScript Setup

```typescript
import weaviate, { WeaviateClient } from 'weaviate-client';

const client: WeaviateClient = await weaviate.connectToWeaviateCloud(
  'https://your-cluster.weaviate.network',
  { authCredentials: new weaviate.ApiKey('your-wcd-api-key') }
);
await client.close();
```

### Environment Variables

```bash
export WEAVIATE_URL="https://your-cluster.weaviate.network"  # or http://localhost:8080
export WEAVIATE_API_KEY="your-wcd-api-key"
export OPENAI_API_KEY="sk-..."
```

---

## CLI Decision Tree

```
User wants to...
├── Connect to Weaviate
│   ├── Cloud (WCD) ─────────► weaviate.connect_to_weaviate_cloud()
│   ├── Local Docker ────────► weaviate.connect_to_local()
│   └── Custom URL ──────────► weaviate.connect_to_custom()
│
├── Create collection
│   ├── With auto-vectorization ► Configure.Vectorizer.text2vec_openai()
│   └── Bring own vectors ──────► Configure.Vectorizer.none()
│
├── Insert data
│   ├── Single object ──────► collection.data.insert()
│   ├── Bulk import ────────► collection.batch.dynamic()
│   └── With custom vector ─► DataObject(properties=..., vector=...)
│
├── Search data
│   ├── Semantic search ────► query.near_text() or query.near_vector()
│   ├── Keyword search ─────► query.bm25()
│   ├── Hybrid search ──────► query.hybrid()
│   └── With filters ───────► filters=Filter.by_property()
│
├── RAG / Generative
│   ├── Single prompt ──────► generate.near_text(single_prompt=...)
│   └── Grouped task ───────► generate.near_text(grouped_task=...)
│
└── Multi-tenancy
    ├── Create tenant ──────► collection.tenants.create()
    └── Query tenant ───────► collection.with_tenant("name")
```

---

## Collection Schema

### Create with Vectorizer

```python
from weaviate.classes.config import Configure, Property, DataType

client.collections.create(
    name="Article",
    vectorizer_config=Configure.Vectorizer.text2vec_openai(
        model="text-embedding-3-small"
    ),
    properties=[
        Property(name="title", data_type=DataType.TEXT),
        Property(name="content", data_type=DataType.TEXT),
        Property(name="category", data_type=DataType.TEXT),
        Property(name="view_count", data_type=DataType.INT)
    ]
)
```

### Property Data Types

| Type | Python | Description |
|------|--------|-------------|
| `TEXT` | str | Tokenized text, searchable |
| `INT` | int | Integer numbers |
| `NUMBER` | float | Floating point |
| `BOOLEAN` | bool | True/False |
| `DATE` | datetime | ISO 8601 date |
| `OBJECT` | dict | Nested object |

> **See REFERENCE.md**: Full data types, vectorizer modules, index configuration

---

## Data Operations

### Insert Single Object

```python
articles = client.collections.get("Article")

uuid = articles.data.insert(
    properties={
        "title": "Introduction to Vector Databases",
        "content": "Vector databases store embeddings...",
        "category": "Technology"
    }
)
```

### Batch Insert (Recommended for Bulk)

```python
articles = client.collections.get("Article")

with articles.batch.dynamic() as batch:
    for item in data:
        batch.add_object(properties=item)

    # Check errors INSIDE context manager
    if batch.number_errors > 0:
        for obj in batch.failed_objects[:5]:
            print(f"Error: {obj.message}")
```

### Update and Delete

```python
# Update properties
articles.data.update(uuid="...", properties={"view_count": 2000})

# Delete by UUID
articles.data.delete_by_id("12345678-...")

# Delete by filter
from weaviate.classes.query import Filter
articles.data.delete_many(
    where=Filter.by_property("category").equal("Outdated")
)
```

---

## Search Operations

### Vector Search (Semantic)

```python
from weaviate.classes.query import MetadataQuery

response = articles.query.near_text(
    query="machine learning algorithms",
    limit=5,
    return_metadata=MetadataQuery(distance=True)
)

for obj in response.objects:
    print(f"{obj.properties['title']} (distance: {obj.metadata.distance})")
```

### Hybrid Search (Vector + Keyword)

```python
response = articles.query.hybrid(
    query="neural network optimization",
    alpha=0.5,  # 0=keyword only, 1=vector only
    limit=10
)
```

### Filtered Search

```python
from weaviate.classes.query import Filter

response = articles.query.near_text(
    query="artificial intelligence",
    filters=(
        Filter.by_property("category").equal("Technology") &
        Filter.by_property("view_count").greater_than(1000)
    ),
    limit=10
)
```

### Filter Operators

| Operator | Usage |
|----------|-------|
| `equal` | `.equal(value)` |
| `not_equal` | `.not_equal(value)` |
| `greater_than` | `.greater_than(value)` |
| `less_than` | `.less_than(value)` |
| `like` | `.like("pattern*")` |
| `contains_any` | `.contains_any([...])` |

> **See REFERENCE.md**: Aggregations, reranking, advanced filter patterns

---

## Generative Search (RAG)

### Configure and Query

```python
from weaviate.classes.config import Configure

# Create with generative module
client.collections.create(
    name="KnowledgeBase",
    vectorizer_config=Configure.Vectorizer.text2vec_openai(),
    generative_config=Configure.Generative.openai(model="gpt-4o"),
    properties=[...]
)

# Single object generation
response = kb.generate.near_text(
    query="quantum computing",
    single_prompt="Summarize: {content}",
    limit=1
)
print(response.objects[0].generated)

# Grouped generation (RAG)
response = kb.generate.near_text(
    query="best practices",
    grouped_task="Based on these, provide 5 recommendations:",
    limit=5
)
print(response.generated)
```

> **See REFERENCE.md**: All generative modules, reranking configuration

---

## Multi-Tenancy

### Enable and Use

```python
from weaviate.classes.config import Configure
from weaviate.classes.tenants import Tenant

# Create multi-tenant collection
client.collections.create(
    name="CustomerData",
    multi_tenancy_config=Configure.multi_tenancy(enabled=True),
    vectorizer_config=Configure.Vectorizer.text2vec_openai(),
    properties=[...]
)

# Create tenants
collection = client.collections.get("CustomerData")
collection.tenants.create([
    Tenant(name="customer_123"),
    Tenant(name="customer_456")
])

# Query specific tenant
tenant_data = collection.with_tenant("customer_123")
tenant_data.data.insert(properties={"name": "Item 1"})
response = tenant_data.query.near_text(query="search", limit=10)
```

> **See REFERENCE.md**: Tenant management, activity status, offloading

---

## Docker Setup

### Basic docker-compose.yml

```yaml
version: '3.8'

services:
  weaviate:
    image: cr.weaviate.io/semitechnologies/weaviate:1.28.2
    restart: unless-stopped
    ports:
      - "8080:8080"
      - "50051:50051"
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      DEFAULT_VECTORIZER_MODULE: 'text2vec-openai'
      ENABLE_MODULES: 'text2vec-openai,generative-openai'
      OPENAI_APIKEY: ${OPENAI_API_KEY}
    volumes:
      - weaviate_data:/var/lib/weaviate

volumes:
  weaviate_data:
```

```bash
# Start
docker-compose up -d

# Check status
curl http://localhost:8080/v1/.well-known/ready

# View logs
docker-compose logs -f weaviate
```

> **See REFERENCE.md**: Production configuration, authentication, multiple modules

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `ConnectionError` | Weaviate not reachable | Check URL, Docker running |
| `AuthenticationError` | Invalid API key | Verify `WEAVIATE_API_KEY` |
| `UnexpectedStatusCodeError 422` | Schema validation | Check property types |
| `ObjectAlreadyExistsError` | Duplicate UUID | Use update or new UUID |

### Error Pattern

```python
from weaviate.exceptions import (
    WeaviateConnectionError,
    UnexpectedStatusCodeError,
    ObjectAlreadyExistsException
)

try:
    uuid = collection.data.insert(properties=data)
except ObjectAlreadyExistsException:
    logging.warning("Object exists, updating instead")
except UnexpectedStatusCodeError as e:
    if e.status_code == 429:
        time.sleep(5)  # Rate limited
    raise
```

> **See REFERENCE.md**: Comprehensive error handling, retry patterns

---

## Best Practices

1. **Use context managers** for automatic cleanup
2. **Batch for bulk operations** (10-100x faster)
3. **Filter before vector search** to reduce computation
4. **Use multi-tenancy** for customer isolation
5. **Tune hybrid alpha**: 0.5 start, lower for technical terms

### Anti-Patterns to Avoid

- Blocking sync calls in async code
- Ignoring batch errors (check inside context manager)
- Over-fetching properties (specify only needed ones)
- Individual inserts for bulk data

> **See REFERENCE.md**: Index optimization, compression, production readiness checklist

---

## Quick Reference Card

```python
# Connect
client = weaviate.connect_to_local()
client = weaviate.connect_to_weaviate_cloud(url, auth_credentials=Auth.api_key(key))

# Collection
client.collections.create(name="...", vectorizer_config=..., properties=[...])
collection = client.collections.get("...")

# Insert
collection.data.insert(properties={...})
with collection.batch.dynamic() as batch: batch.add_object(properties={...})

# Search
collection.query.near_text(query="...", limit=10)
collection.query.hybrid(query="...", alpha=0.5, limit=10)

# RAG
collection.generate.near_text(query="...", single_prompt="...", limit=1)

# Multi-tenant
collection.with_tenant("tenant_name").query.near_text(...)
```

---

## Agent Integration

| Agent | Use Case |
|-------|----------|
| `backend-developer` | Vector search, RAG pipelines |
| `deep-debugger` | Query performance, index optimization |
| `infrastructure-developer` | Docker/Kubernetes deployment |

**Handoff to Deep-Debugger**: Slow queries, index issues, batch failures. Provide query patterns, schema, errors.

---

## See Also

- [REFERENCE.md](REFERENCE.md) - Comprehensive API, all modules, advanced patterns
- [Weaviate Docs](https://weaviate.io/developers/weaviate)
