---
name: libvector
description: >
  libvector - Vector similarity search. VectorIndex stores embeddings with
  metadata and performs cosine similarity search. VectorProcessor handles
  embedding generation and indexing. Supports filtering by metadata and
  threshold-based retrieval. Use for semantic search, RAG retrieval, and
  similarity matching.
---

# libvector Skill

## When to Use

- Building semantic search functionality
- Implementing RAG retrieval pipelines
- Finding similar documents by embedding
- Filtering vector results by metadata

## Key Concepts

**VectorIndex**: Storage-backed index for vectors with cosine similarity search
and metadata filtering.

**VectorProcessor**: Processes documents into embeddings and indexes them.

**calculateDotProduct**: Utility function for computing dot product (cosine
similarity for normalized vectors) with loop unrolling for performance.

## Usage Patterns

### Pattern 1: Search by vector

```javascript
import { VectorIndex } from "@copilot-ld/libvector/index.js";

const index = new VectorIndex(storage, "content");
const results = await index.search(queryVector, {
  limit: 10,
  threshold: 0.7,
  filter: { type: "document" },
});
```

### Pattern 2: Add vectors

```javascript
await index.add({
  id: "doc-123",
  vector: embedding,
  metadata: { type: "document", title: "Example" },
});
```

### Pattern 3: Calculate similarity directly

```javascript
import { calculateDotProduct } from "@copilot-ld/libvector";

// For normalized vectors, dot product equals cosine similarity
const similarity = calculateDotProduct(vectorA, vectorB);
```

## Integration

Used by Vector service. Embeddings generated via LLM service. Stored in
data/vectors/.
