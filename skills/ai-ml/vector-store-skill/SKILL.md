---
name: vector-store
version: 1.0
last_updated: 2025-12-04
description: Vector store schema protection and migration management
license: MIT
priority: critical
triggers:
  - "vector store", "Pinecone", "Milvus", "Chroma", "FAISS", "schema"
dependencies:
  - docs/protected-schemas.md
  - templates/rag-checklist.md
---

# 🗄️ Vector Store SKILL

## Purpose

**PROTECTED:** Vector store schema management. Changes require pre-modification checklist validation.

---

## Supported Vector Stores

### 1. Pinecone (Cloud)

```python
import pinecone
from langchain_pinecone import PineconeVectorStore

pinecone.init(api_key="your-key")

index = pinecone.Index("rag-demo")
vector_store = PineconeVectorStore(index, embeddings)
```

**Schema:** `{dimension: 1536, metric: "cosine"}`

---

### 2. Milvus (Self-hosted/Cloud)

```python
from langchain_community.vectorstores import Milvus

vector_store = Milvus(
    embeddings,
    connection_args={"host": "localhost", "port": "19530"},
    collection_name="rag_demo",
    index_params={"metric_type": "IP", "index_type": "IVF_FLAT"}
)
```

---

### 3. Chroma (Local)

```python
from langchain_community.vectorstores import Chroma

vector_store = Chroma(
    collection_name="rag_demo",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)
```

---

### 4. FAISS (Local)

```python
from langchain_community.vectorstores import FAISS

vector_store = FAISS.from_documents(documents, embeddings)
vector_store.save_local("./faiss_index")
```

---

## Schema Protection Rules

**HALT before:**
1. Dimension change → Breaks all vectors
2. Metric change → Affects rankings

**CAUTION before:**
3. Metadata schema change → Migration needed

**See:** `templates/rag-checklist.md`

---

## Migration Playbook

### Scenario: Change Embedding Model

```bash
# 1. Backup
python scripts/export_vectors.py --output backup.json

# 2. Create new index
python scripts/create_index.py --dimension 3072

# 3. Re-embed documents
python scripts/reindex.py --model text-embedding-3-large

# 4. Switch app
export VECTOR_STORE_INDEX="rag-demo-v2"

# 5. Monitor
python scripts/monitor_quality.py

# 6. Delete old index (after 30 days)
```

**Full guide:** `docs/protected-schemas.md`

---

**Last Updated:** 2025-12-04
**Version:** 1.0
**Adapted from:** WHRESUME blog-protection-SKILL.md
