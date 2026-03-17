---
name: embedding
description: >
  Standalone embedding service for semantic search. Runs as persistent FastAPI
  server for millisecond-latency embeddings. Supports model swapping via env vars.
  Use when you need vectors for any database (ArangoDB, Pinecone, etc).
allowed-tools: Bash, WebFetch
triggers:
  - embed this
  - embed text
  - start embedding service
  - get embeddings
  - generate vectors
  - semantic search vectors
metadata:
  short-description: Persistent embedding service for semantic search
---

# Embedding Skill

Standalone embedding service for semantic search across any database.

## Architecture

```
┌─────────────────────────────────────────┐
│         embedding service (:8602)       │
│  Model: EMBEDDING_MODEL env var         │
│  Device: auto (CPU/GPU)                 │
└───────────────────┬─────────────────────┘
                    │
    ┌───────────────┼───────────────┐
    ▼               ▼               ▼
 memory        edge-verifier    your-project
 skill         searches         ArangoDB/etc
```

## Quick Start

```bash
# Start the service (first run loads model ~5-10s)
./run.sh serve

# Embed text (CLI)
./run.sh embed --text "your query here"

# Embed via HTTP (after service is running)
curl -X POST http://127.0.0.1:8602/embed -H "Content-Type: application/json" \
  -d '{"text": "your query here"}'
```

## Commands

| Command                           | Description                                 |
| --------------------------------- | ------------------------------------------- |
| `./run.sh serve`                  | Start persistent FastAPI server             |
| `./run.sh embed --text "..."`     | Embed single text (uses service if running) |
| `./run.sh embed --file input.txt` | Embed file contents                         |
| `./run.sh info`                   | Show model, device, service status          |

## Configuration

| Variable                | Default                 | Description                          |
| ----------------------- | ----------------------- | ------------------------------------ |
| `EMBEDDING_MODEL`       | `all-MiniLM-L6-v2`      | Sentence-transformers model name     |
| `EMBEDDING_DEVICE`      | `auto`                  | Device: `auto`, `cpu`, `cuda`, `mps` |
| `EMBEDDING_PORT`        | `8602`                  | Service port                         |
| `EMBEDDING_SERVICE_URL` | `http://127.0.0.1:8602` | Client connection URL                |

## Swapping Models

```bash
# Use a different model for this project
export EMBEDDING_MODEL="nomic-ai/nomic-embed-text-v1"
./run.sh serve

# Or for GPU-accelerated
export EMBEDDING_MODEL="intfloat/e5-large-v2"
export EMBEDDING_DEVICE="cuda"
./run.sh serve
```

## API Endpoints

### POST /embed

Embed single text.

```json
{"text": "query to embed"}
→ {"vector": [0.1, 0.2, ...], "model": "all-MiniLM-L6-v2", "dimensions": 384}
```

### POST /embed/batch

Embed multiple texts.

```json
{"texts": ["query 1", "query 2"]}
→ {"vectors": [[...], [...]], "model": "...", "count": 2}
```

### GET /info

Service status and configuration.

```json
{
  "model": "all-MiniLM-L6-v2",
  "device": "cuda",
  "dimensions": 384,
  "status": "ready"
}
```

## Integration Examples

### ArangoDB Semantic Search

```python
import httpx

# Get embedding
resp = httpx.post("http://127.0.0.1:8602/embed", json={"text": "find similar docs"})
vector = resp.json()["vector"]

# Use in AQL query
aql = """
FOR doc IN my_collection
  LET score = COSINE_SIMILARITY(doc.embedding, @vector)
  FILTER score > 0.7
  SORT score DESC
  RETURN doc
"""
```

### From Memory Skill

Memory skill can consume this service by setting:

```bash
export EMBEDDING_SERVICE_URL="http://127.0.0.1:8602"
```

## Cold Start

First invocation loads the model (~5-10 seconds). After that, embeddings are millisecond-latency. The service logs progress:

```
[embedding] Loading model: all-MiniLM-L6-v2...
[embedding] Model loaded in 6.2s
[embedding] Service ready on http://127.0.0.1:8602
```
