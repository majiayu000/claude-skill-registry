---
name: qdrant-sparse
description: >
  Qdrant sparse vector operations: collection creation with SparseVectorParams,
  Modifier.IDF for miniCOIL/SPLADE/BM42, upserting SparseVector points, sparse search,
  hybrid search with prefetch + RRF/DBSF fusion, converting model outputs to SparseVector format,
  payload filtering, and performance tuning. Covers the sparse vector gap not handled by
  the official Qdrant MCP (which only supports dense vectors via FastEmbed).
---

# Qdrant Sparse Vector Reference

This skill covers everything needed to work with Qdrant's sparse vector features using the `qdrant-client` Python SDK. Sparse vectors are essential for lexical/token-level retrieval (miniCOIL, SPLADE, BM42) and hybrid search.

## 1. Collection Creation

### Sparse-Only Collection

```python
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")

client.create_collection(
    collection_name="sparse_only",
    vectors_config={},  # Empty — no dense vectors
    sparse_vectors_config={
        "text": models.SparseVectorParams(
            modifier=models.Modifier.IDF,  # Critical for miniCOIL/SPLADE/BM42
        )
    },
)
```

### Hybrid Collection (Dense + Sparse)

```python
client.create_collection(
    collection_name="hybrid",
    vectors_config={
        "dense": models.VectorParams(
            size=384,
            distance=models.Distance.COSINE,
        )
    },
    sparse_vectors_config={
        "sparse": models.SparseVectorParams(
            modifier=models.Modifier.IDF,
        )
    },
)
```

### Multiple Sparse Vector Fields

A collection can have multiple named sparse vector fields:

```python
client.create_collection(
    collection_name="multi_sparse",
    vectors_config={},
    sparse_vectors_config={
        "title": models.SparseVectorParams(modifier=models.Modifier.IDF),
        "body": models.SparseVectorParams(modifier=models.Modifier.IDF),
    },
)
```

## 2. Modifier.IDF — When and Why

**Always use `modifier=models.Modifier.IDF`** for miniCOIL, SPLADE, and BM42 models.

- Qdrant computes IDF weights automatically at query time.
- Formula: `ln(1 + (N - df + 0.5) / (df + 0.5))` where N = total docs, df = document frequency for that index (natural logarithm).
- Without IDF, common terms (stopwords, frequent tokens) dominate scoring — retrieval quality degrades severely.
- IDF is computed per-index across the entire collection, so it improves as you add more documents.

**When to omit IDF:**
- If your model already bakes in IDF-like weighting (rare).
- If you're doing exact term matching where frequency doesn't matter.

## 3. Sparse Vector Format

Sparse vectors have two parallel arrays:
- `indices`: `list[int]` — dimension IDs (arbitrary, non-contiguous integers)
- `values`: `list[float]` — corresponding weights

```python
sv = models.SparseVector(
    indices=[42, 1337, 9001],
    values=[0.5, 0.8, 0.3],
)
```

### Converting Model Outputs to SparseVector

Most sparse models output `dict[int, float]`. Convert like this:

```python
def to_sparse_vector(sparse_dict: dict[int, float]) -> models.SparseVector:
    """Convert {index: value} dict to Qdrant SparseVector."""
    if not sparse_dict:
        return models.SparseVector(indices=[], values=[])
    indices, values = zip(*sparse_dict.items())
    return models.SparseVector(
        indices=list(indices),
        values=list(values),
    )

# Usage with miniCOIL output
model_output = {102: 0.45, 3847: 0.92, 11023: 0.31}
sv = to_sparse_vector(model_output)
```

### miniCOIL Index Encoding

miniCOIL uses 4D meaning vectors per concept. The sparse index encoding is:
`index = concept_num * 4 + offset` where offset is 0-3 for the 4 dimensions.

```python
def minicoil_to_sparse(concepts: dict[int, list[float]]) -> models.SparseVector:
    """Convert miniCOIL output {concept_id: [v0, v1, v2, v3]} to SparseVector."""
    indices = []
    values = []
    for concept_id, vec in concepts.items():
        for offset, val in enumerate(vec):
            if val != 0.0:  # Only store non-zero values
                indices.append(concept_id * 4 + offset)
                values.append(val)
    return models.SparseVector(indices=indices, values=values)
```

## 4. Upserting Points

### Single Point

```python
client.upsert(
    collection_name="my_collection",
    points=[
        models.PointStruct(
            id=1,
            payload={"text": "The quick brown fox", "source": "doc1"},
            vector={
                "text": models.SparseVector(
                    indices=[102, 3847, 11023],
                    values=[0.45, 0.92, 0.31],
                )
            },
        )
    ],
)
```

### Batch Upsert

```python
points = [
    models.PointStruct(
        id=idx,
        payload={"text": doc["text"], "doc_id": doc["id"]},
        vector={
            "text": models.SparseVector(
                indices=doc["sparse_indices"],
                values=doc["sparse_values"],
            )
        },
    )
    for idx, doc in enumerate(documents)
]

# Upsert in batches of 100
BATCH_SIZE = 100
for i in range(0, len(points), BATCH_SIZE):
    client.upsert(
        collection_name="my_collection",
        points=points[i : i + BATCH_SIZE],
    )
```

### Hybrid Upsert (Dense + Sparse)

```python
client.upsert(
    collection_name="hybrid",
    points=[
        models.PointStruct(
            id=1,
            payload={"text": "The quick brown fox"},
            vector={
                "dense": [0.1, 0.2, 0.3, ...],  # Dense embedding (list of floats)
                "sparse": models.SparseVector(
                    indices=[102, 3847],
                    values=[0.45, 0.92],
                ),
            },
        )
    ],
)
```

## 5. Searching

### Basic Sparse Search

```python
results = client.query_points(
    collection_name="my_collection",
    query=models.SparseVector(
        indices=[102, 3847, 11023],
        values=[0.45, 0.92, 0.31],
    ),
    using="text",  # Name of the sparse vector field
    limit=10,
).points
```

**Key differences from dense search:**
- Scoring: Dot product by default (no need to specify distance metric).
- Search is always exact (not approximate like HNSW for dense vectors).
- Only documents with non-zero values in at least one of the query's indices are candidates.
- Speed is proportional to the number of non-zero values in the query.

### Sparse Search with Payload Filter

```python
results = client.query_points(
    collection_name="my_collection",
    query=models.SparseVector(
        indices=[102, 3847],
        values=[0.45, 0.92],
    ),
    using="text",
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="source",
                match=models.MatchValue(value="doc1"),
            )
        ]
    ),
    limit=10,
).points
```

### Sparse Search with Score Threshold

```python
results = client.query_points(
    collection_name="my_collection",
    query=models.SparseVector(
        indices=[102, 3847],
        values=[0.45, 0.92],
    ),
    using="text",
    score_threshold=0.5,  # Only return results with score >= 0.5
    limit=10,
).points
```

## 6. Hybrid Search (Prefetch + Fusion)

Hybrid search combines dense and sparse results using fusion strategies.

### Reciprocal Rank Fusion (RRF)

RRF is robust and doesn't require score normalization. Good default choice.

```python
# Standard RRF (v1.10+)
results = client.query_points(
    collection_name="hybrid",
    prefetch=[
        models.Prefetch(
            query=[0.1, 0.2, 0.3, ...],  # Dense query vector
            using="dense",
            limit=100,  # Prefetch more candidates than final limit
        ),
        models.Prefetch(
            query=models.SparseVector(
                indices=[102, 3847],
                values=[0.45, 0.92],
            ),
            using="sparse",
            limit=100,
        ),
    ],
    query=models.FusionQuery(fusion=models.Fusion.RRF),
    limit=10,
).points

# Parameterized RRF (v1.16+) — tune the k constant (default=2)
# Higher k reduces the influence of top ranks, lower k amplifies them
results = client.query_points(
    collection_name="hybrid",
    prefetch=[
        models.Prefetch(query=[0.1, 0.2, ...], using="dense", limit=100),
        models.Prefetch(query=models.SparseVector(indices=[102], values=[0.9]), using="sparse", limit=100),
    ],
    query=models.RrfQuery(rrf=models.Rrf(k=60)),
    limit=10,
).points
```

### Distribution-Based Score Fusion (DBSF)

DBSF normalizes scores based on their distribution. Better when score magnitudes are meaningful.

```python
results = client.query_points(
    collection_name="hybrid",
    prefetch=[
        models.Prefetch(
            query=[0.1, 0.2, 0.3, ...],
            using="dense",
            limit=100,
        ),
        models.Prefetch(
            query=models.SparseVector(
                indices=[102, 3847],
                values=[0.45, 0.92],
            ),
            using="sparse",
            limit=100,
        ),
    ],
    query=models.FusionQuery(fusion=models.Fusion.DBSF),
    limit=10,
).points
```

### Hybrid Search with Payload Filter

Filters apply to the final fused results:

```python
results = client.query_points(
    collection_name="hybrid",
    prefetch=[
        models.Prefetch(
            query=[0.1, 0.2, ...],
            using="dense",
            limit=100,
        ),
        models.Prefetch(
            query=models.SparseVector(indices=[102], values=[0.9]),
            using="sparse",
            limit=100,
        ),
    ],
    query=models.FusionQuery(fusion=models.Fusion.RRF),
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="category",
                match=models.MatchValue(value="science"),
            )
        ]
    ),
    limit=10,
).points
```

### Weighted Prefetch (Boosting One Signal)

Use `score_threshold` or nested prefetch to control contribution weight:

```python
results = client.query_points(
    collection_name="hybrid",
    prefetch=[
        models.Prefetch(
            query=[0.1, 0.2, ...],
            using="dense",
            limit=200,  # More candidates = more influence in fusion
        ),
        models.Prefetch(
            query=models.SparseVector(indices=[102], values=[0.9]),
            using="sparse",
            limit=50,   # Fewer candidates = less influence
        ),
    ],
    query=models.FusionQuery(fusion=models.Fusion.RRF),
    limit=10,
).points
```

## 7. Model Integration Patterns

### SPLADE Integration

SPLADE models output token-weight dictionaries. The tokenizer vocab maps tokens to integer IDs which become sparse indices.

```python
from transformers import AutoModelForMaskedLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("naver/splade-cocondenser-ensembledistil")
model = AutoModelForMaskedLM.from_pretrained("naver/splade-cocondenser-ensembledistil")

def encode_splade(text: str) -> models.SparseVector:
    tokens = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
    with torch.no_grad():
        output = model(**tokens)
    # SPLADE: log(1 + ReLU(logits)) aggregated over tokens
    splade_vec = torch.max(
        torch.log1p(torch.relu(output.logits)) * tokens["attention_mask"].unsqueeze(-1),
        dim=1,
    ).values.squeeze()

    # Extract non-zero indices and values
    nonzero = splade_vec.nonzero().squeeze()
    indices = nonzero.tolist()
    values = splade_vec[nonzero].tolist()

    if isinstance(indices, int):
        indices = [indices]
        values = [values]

    return models.SparseVector(indices=indices, values=values)
```

### BM42 (Qdrant's Built-in Sparse)

BM42 is Qdrant's built-in sparse embedding approach. Use it via the Qdrant FastEmbed integration:

```python
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")

# BM42 uses the same SparseVectorParams with IDF
client.create_collection(
    collection_name="bm42_collection",
    vectors_config={},
    sparse_vectors_config={
        "text": models.SparseVectorParams(
            modifier=models.Modifier.IDF,
        )
    },
)
# Then upsert with sparse vectors produced by the BM42 model
# (BM42 outputs are in the same {indices, values} format)
```

## 8. Performance Considerations

1. **Search speed scales with query sparsity**: More non-zero indices in the query = slower search. Prune low-weight values if latency matters.
2. **Exact search via inverted index**: Sparse vectors don't use HNSW. Search is exact (no approximation) but efficient — the inverted index only scans documents with non-zero values in the queried dimensions, not the entire collection.
3. **Batch upserts**: Use batches of 64-256 points for optimal throughput. Going too large risks timeouts.
4. **IDF overhead**: Minimal — computed at query time from pre-maintained statistics, not a full scan.
5. **Memory**: Sparse vectors use less memory than dense for high-dimensional spaces because only non-zero values are stored.
6. **Index on disk + float16**: For large collections, use on-disk storage and half-precision to cut memory with negligible quality loss:

```python
client.create_collection(
    collection_name="large_sparse",
    vectors_config={},
    sparse_vectors_config={
        "text": models.SparseVectorParams(
            modifier=models.Modifier.IDF,
            index=models.SparseIndexParams(
                on_disk=True,                      # Memory-mapped inverted index
                datatype=models.Datatype.FLOAT16,  # Half memory per value
            ),
        )
    },
)
```

## 9. Error Patterns and Troubleshooting

### Common Errors

**"Sparse vector `text` not found"**
- The sparse vector field name in the query doesn't match the collection config.
- Fix: Check `using="text"` matches the key in `sparse_vectors_config`.

**Empty results despite matching documents**
- Missing `Modifier.IDF` — without it, common-term scores wash out rare-term signals.
- Fix: Recreate collection with `modifier=models.Modifier.IDF`.

**"Vector dimension mismatch"**
- This error is for dense vectors only. Sparse vectors have no fixed dimensionality.
- If you see this on a hybrid collection, the dense vector size is wrong.

**Scores are unexpectedly low**
- Sparse dot-product scores depend on value magnitude. Check your model outputs aren't near-zero.
- Verify indices actually overlap between query and stored documents.

**Timeout on large upserts**
- Reduce batch size (try 64 or 128 points per call).
- Use `client.upsert(..., wait=False)` for async indexing if you don't need immediate consistency.

### Debugging Tips

```python
# Retrieve a point to inspect its sparse vector
point = client.retrieve(
    collection_name="my_collection",
    ids=[1],
    with_vectors=True,
)
print(point[0].vector["text"])  # SparseVector(indices=[...], values=[...])

# Check collection info
info = client.get_collection("my_collection")
print(info.config.params.sparse_vectors_config)

# Count points in collection
count = client.count(collection_name="my_collection")
print(f"Total points: {count.count}")
```

## 10. Full Workflow Example

See `resources/examples.py` for a complete working example covering:
- Collection creation (sparse-only and hybrid)
- Model output conversion
- Batch upserting
- Sparse search
- Hybrid search with RRF fusion
- Payload filtering
