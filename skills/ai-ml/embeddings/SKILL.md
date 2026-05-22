---
name: embeddings
description: Text embeddings for semantic search and similarity. Use when converting text to vectors, choosing embedding models, implementing chunking strategies, or building document similarity features.
context: fork
agent: data-pipeline-engineer
version: 1.0.0
author: SkillForge
user-invocable: false
---

# Embeddings

Convert text to dense vector representations for semantic search and similarity.

## Quick Reference

```python
from openai import OpenAI

client = OpenAI()

# Single text embedding
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Your text here"
)
vector = response.data[0].embedding  # 1536 dimensions
```

```python
# Batch embedding (efficient)
texts = ["text1", "text2", "text3"]
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts
)
vectors = [item.embedding for item in response.data]
```

## Model Selection

| Model | Dims | Cost | Use Case |
|-------|------|------|----------|
| `text-embedding-3-small` | 1536 | $0.02/1M | General purpose |
| `text-embedding-3-large` | 3072 | $0.13/1M | High accuracy |
| `nomic-embed-text` (Ollama) | 768 | Free | Local/CI |

## Chunking Strategy

```python
def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks for embedding."""
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)

    return chunks
```

**Guidelines:**
- Chunk size: 256-1024 tokens (512 typical)
- Overlap: 10-20% for context continuity
- Include metadata (title, source) with chunks

## Similarity Calculation

```python
import numpy as np

def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Usage
similarity = cosine_similarity(vector1, vector2)
# 1.0 = identical, 0.0 = orthogonal, -1.0 = opposite
```

## Key Decisions

- **Dimension reduction**: Can truncate `text-embedding-3-large` to 1536 dims
- **Normalization**: Most models return normalized vectors
- **Batch size**: 100-500 texts per API call for efficiency

## Common Mistakes

- Embedding queries differently than documents
- Not chunking long documents (context gets lost)
- Using wrong similarity metric (cosine vs euclidean)
- Re-embedding unchanged content (cache embeddings)

## Advanced Patterns

See `references/advanced-patterns.md` for:
- **Late Chunking**: Embed full document, extract chunk vectors from contextualized tokens
- **Batch API**: Production batching with rate limiting and retry
- **Embedding Cache**: Redis-based caching to avoid re-embedding
- **Matryoshka Embeddings**: Dimension reduction with text-embedding-3

## Related Skills

- `rag-retrieval` - Using embeddings for RAG pipelines
- `hyde-retrieval` - Hypothetical document embeddings for vocabulary mismatch
- `contextual-retrieval` - Anthropic's context-prepending technique
- `reranking-patterns` - Cross-encoder reranking for precision
- `ollama-local` - Local embeddings with nomic-embed-text

## Capability Details

### text-to-vector
**Keywords:** embedding, text to vector, vectorize, embed text
**Solves:**
- Convert text to vector embeddings
- Choose appropriate embedding models
- Handle embedding API integration

### semantic-search
**Keywords:** semantic search, vector search, similarity search, find similar
**Solves:**
- Implement semantic search over documents
- Configure similarity thresholds
- Rank results by relevance

### chunking-strategies
**Keywords:** chunk, chunking, split, text splitting, overlap
**Solves:**
- Split documents into optimal chunks
- Configure chunk size and overlap
- Preserve semantic boundaries

### batch-embedding
**Keywords:** batch, bulk embed, parallel embedding, batch processing
**Solves:**
- Embed large document collections efficiently
- Handle rate limits and retries
- Optimize embedding costs

### local-embeddings
**Keywords:** local, ollama, self-hosted, on-premise, offline
**Solves:**
- Run embeddings locally with Ollama
- Deploy self-hosted embedding models
- Reduce API costs with local models
