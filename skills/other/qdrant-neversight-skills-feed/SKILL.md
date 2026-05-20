---
name: qdrant
description: Qdrant vector database REST API via curl. Use this skill to store, search, and manage vector embeddings.
vm0_secrets:
  - QDRANT_API_KEY
vm0_vars:
  - QDRANT_URL
---

# Qdrant API

Use the Qdrant REST API via direct `curl` calls to **store and search vector embeddings** for RAG, semantic search, and recommendations.

> Official docs: `https://qdrant.tech/documentation/`

---

## When to Use

Use this skill when you need to:

- **Store vector embeddings** for semantic search
- **Search for similar vectors** using cosine, dot product, or euclidean distance
- **Build RAG applications** with retrieval from vector store
- **Implement recommendations** based on similarity
- **Filter search results** by metadata/payload

---

## Prerequisites

### Option 1: Qdrant Cloud (Recommended)

1. Sign up at [Qdrant Cloud](https://cloud.qdrant.io/)
2. Create a cluster and get your URL and API key
3. Store credentials in environment variables

```bash
export QDRANT_URL="https://xyz-example.aws.cloud.qdrant.io:6333"
export QDRANT_API_KEY="your-api-key"
```

### Option 2: Self-hosted

Run Qdrant locally with Docker:

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

```bash
export QDRANT_URL="http://localhost:6333"
export QDRANT_API_KEY="" # Optional for local
```

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

All examples below assume you have `QDRANT_URL` and `QDRANT_API_KEY` set.

---

### 1. Check Server Status

Verify connection to Qdrant:

```bash
bash -c 'curl -s -X GET "${QDRANT_URL}" --header "api-key: ${QDRANT_API_KEY}"'
```

---

### 2. List Collections

Get all collections:

```bash
bash -c 'curl -s -X GET "${QDRANT_URL}/collections" --header "api-key: ${QDRANT_API_KEY}"'
```

---

### 3. Create a Collection

Create a collection for storing vectors:

Write to `/tmp/qdrant_request.json`:

```json
{
  "vectors": {
    "size": 1536,
    "distance": "Cosine"
  }
}
```

Then run:

```bash
bash -c 'curl -s -X PUT "${QDRANT_URL}/collections/my_collection" --header "api-key: ${QDRANT_API_KEY}" --header "Content-Type: application/json" -d @/tmp/qdrant_request.json'
```

**Distance metrics:**
- `Cosine` - Cosine similarity (recommended for normalized vectors)
- `Dot` - Dot product
- `Euclid` - Euclidean distance
- `Manhattan` - Manhattan distance

**Common vector sizes:**
- OpenAI `text-embedding-3-small`: 1536
- OpenAI `text-embedding-3-large`: 3072
- Cohere: 1024

---

### 4. Get Collection Info

Get details about a collection:

```bash
bash -c 'curl -s -X GET "${QDRANT_URL}/collections/my_collection" --header "api-key: ${QDRANT_API_KEY}"'
```

---

### 5. Upsert Points (Insert/Update Vectors)

Add vectors with payload (metadata):

Write to `/tmp/qdrant_request.json`:

```json
{
  "points": [
    {
      "id": 1,
      "vector": [0.05, 0.61, 0.76, 0.74],
      "payload": {"text": "Hello world", "source": "doc1"}
    },
    {
      "id": 2,
      "vector": [0.19, 0.81, 0.75, 0.11],
      "payload": {"text": "Goodbye world", "source": "doc2"}
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X PUT "${QDRANT_URL}/collections/my_collection/points" --header "api-key: ${QDRANT_API_KEY}" --header "Content-Type: application/json" -d @/tmp/qdrant_request.json'
```

---

### 6. Search Similar Vectors

Find vectors similar to a query vector:

Write to `/tmp/qdrant_request.json`:

```json
{
  "query": [0.05, 0.61, 0.76, 0.74],
  "limit": 5,
  "with_payload": true
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${QDRANT_URL}/collections/my_collection/points/query" --header "api-key: ${QDRANT_API_KEY}" --header "Content-Type: application/json" -d @/tmp/qdrant_request.json'
```

**Response:**
```json
{
  "result": {
  "points": [
  {"id": 1, "score": 0.99, "payload": {"text": "Hello world"}}
  ]
  }
}
```

---

### 7. Search with Filters

Filter results by payload fields:

Write to `/tmp/qdrant_request.json`:

```json
{
  "query": [0.05, 0.61, 0.76, 0.74],
  "limit": 5,
  "filter": {
    "must": [
      {"key": "source", "match": {"value": "doc1"}}
    ]
  },
  "with_payload": true
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${QDRANT_URL}/collections/my_collection/points/query" --header "api-key: ${QDRANT_API_KEY}" --header "Content-Type: application/json" -d @/tmp/qdrant_request.json'
```

**Filter operators:**
- `must` - All conditions must match (AND)
- `should` - At least one must match (OR)
- `must_not` - None should match (NOT)

---

### 8. Get Points by ID

Retrieve specific points:

Write to `/tmp/qdrant_request.json`:

```json
{
  "ids": [1, 2],
  "with_payload": true,
  "with_vector": true
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${QDRANT_URL}/collections/my_collection/points" --header "api-key: ${QDRANT_API_KEY}" --header "Content-Type: application/json" -d @/tmp/qdrant_request.json'
```

---

### 9. Delete Points

Delete by IDs:

Write to `/tmp/qdrant_request.json`:

```json
{
  "points": [1, 2]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${QDRANT_URL}/collections/my_collection/points/delete" --header "api-key: ${QDRANT_API_KEY}" --header "Content-Type: application/json" -d @/tmp/qdrant_request.json'
```

Delete by filter:

Write to `/tmp/qdrant_request.json`:

```json
{
  "filter": {
    "must": [
      {"key": "source", "match": {"value": "doc1"}}
    ]
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${QDRANT_URL}/collections/my_collection/points/delete" --header "api-key: ${QDRANT_API_KEY}" --header "Content-Type: application/json" -d @/tmp/qdrant_request.json'
```

---

### 10. Delete Collection

Remove a collection entirely:

```bash
bash -c 'curl -s -X DELETE "${QDRANT_URL}/collections/my_collection" --header "api-key: ${QDRANT_API_KEY}"'
```

---

### 11. Count Points

Get total count or filtered count:

Write to `/tmp/qdrant_request.json`:

```json
{
  "exact": true
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${QDRANT_URL}/collections/my_collection/points/count" --header "api-key: ${QDRANT_API_KEY}" --header "Content-Type: application/json" -d @/tmp/qdrant_request.json'
```

---

## Filter Syntax

Common filter conditions:

```json
{
  "filter": {
  "must": [
  {"key": "city", "match": {"value": "London"}},
  {"key": "price", "range": {"gte": 100, "lte": 500}},
  {"key": "tags", "match": {"any": ["electronics", "sale"]}}
  ]
  }
}
```

**Match types:**
- `match.value` - Exact match
- `match.any` - Match any in list
- `match.except` - Match none in list
- `range` - Numeric range (gt, gte, lt, lte)

---

## Guidelines

1. **Match vector size**: Collection vector size must match your embedding model output
2. **Use Cosine for normalized vectors**: Most embedding models output normalized vectors
3. **Add payload for filtering**: Store metadata with vectors for filtered searches
4. **Batch upserts**: Insert multiple points in one request for efficiency
5. **Use score_threshold**: Filter out low-similarity results in search
