---
name: vector-store
description: Transient vector store service for fast similarity search (FAISS)
triggers:
  - vector store
  - faiss
  - similarity search
  - vector index
allowed-tools: curl
commands:
  - name: serve
    description: Start the vector store service
    usage: ./run.sh serve
  - name: sanity
    description: Run sanity tests
    usage: ./sanity.sh
metadata:
  port: 8600
  endpoints:
    - /index
    - /search
    - /reset
    - /info

provides:
  - vector-store
composes:
  - memory
  - embedding
  - edge-verifier
  - task-monitor
---

# Vector Store Skill

Transient vector store service for fast similarity search using FAISS (IndexFlatIP).
Designed to be used by other skills (memory, edge-verifier) to accelerate KNN search.

## Configuration

- `VECTOR_STORE_PORT`: Port to listen on (default: 8600)

## API

### POST /index

Add vectors to the index.

```json
{
  "ids": ["id1", "id2"],
  "vectors": [[0.1, 0.2, ...], [0.3, 0.4, ...]],
  "reset": false
}
```

### POST /search

Search for nearest neighbors.

```json
{
  "query": [0.1, 0.2, ...],
  "k": 10
}
```

Returns:

```json
{
  "ids": ["id2", "id1"],
  "scores": [0.95, 0.88]
}
```

### DELETE /reset

Clear the index.

### GET /info

Get index stats.
