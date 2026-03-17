---
name: hybrid-search
description: Use when building search systems that need both semantic similarity and keyword matching - covers combining vector and BM25 search with Reciprocal Rank Fusion, alpha tuning for search weight control, and optimizing retrieval quality
version: 0.5.0
---

# LLMemory Hybrid Search

## Installation

```bash
uv add llmemory
# or
pip install llmemory
```

## Overview

Hybrid search combines **vector similarity search** (semantic understanding) with **full-text search** (keyword matching) to deliver superior retrieval quality. Results are merged using **Reciprocal Rank Fusion (RRF)** to create a unified ranking.

**When to use hybrid search:**
- Need both semantic similarity AND exact keyword matches
- Queries contain specific terms, names, or technical jargon
- Want best-of-both-worlds retrieval quality (recommended default)

**When to use vector-only search:**
- Purely semantic/conceptual queries
- Cross-lingual search
- Queries with synonyms or paraphrasing

**When to use text-only search:**
- Exact keyword/phrase matching required
- Search in structured data or code
- When embeddings are not available

## Quick Start

```python
from llmemory import LLMemory, SearchType

async with LLMemory(connection_string="postgresql://localhost/mydb") as memory:
    # Hybrid search (default, recommended)
    results = await memory.search(
        owner_id="workspace-1",
        query_text="machine learning algorithms",
        search_type=SearchType.HYBRID,
        limit=10,
        alpha=0.5  # Equal weight to vector and text
    )

    for result in results:
        print(f"[RRF={result.rrf_score:.3f}] {result.content[:80]}...")
```

## Complete API Documentation

### SearchType Enum

```python
class SearchType(str, Enum):
    VECTOR = "vector"   # Vector similarity only
    TEXT = "text"       # Full-text search only
    HYBRID = "hybrid"   # Combines vector + text (recommended)
```

### search() - Hybrid Mode

**Signature:**
```python
async def search(
    owner_id: str,
    query_text: str,
    search_type: Union[SearchType, str] = SearchType.HYBRID,
    limit: int = 10,
    alpha: float = 0.5,
    metadata_filter: Optional[Dict[str, Any]] = None,
    id_at_origins: Optional[List[str]] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    include_parent_context: bool = False,
    context_window: int = 2
) -> List[SearchResult]
```

**Hybrid Search Parameters:**
- `search_type` (SearchType, default: HYBRID): Set to `SearchType.HYBRID` for hybrid search
- `alpha` (float, default: 0.5): Weight for vector vs text search
  - `0.0` = text search only
  - `0.5` = equal weight (balanced, recommended)
  - `1.0` = vector search only
  - `0.3` = favor text search (good for keyword-heavy queries)
  - `0.7` = favor vector search (good for semantic queries)

**Returns:**
- `List[SearchResult]` with hybrid-specific fields:
  - `rrf_score` (float): Reciprocal Rank Fusion score (primary ranking)
  - `similarity` (float): Vector similarity score (0-1)
  - `text_rank` (float): Full-text search rank
  - `score` (float): Overall score (equals rrf_score for hybrid)

**Example:**
```python
# Balanced hybrid search
results = await memory.search(
    owner_id="workspace-1",
    query_text="quarterly revenue growth",
    search_type=SearchType.HYBRID,
    alpha=0.5,  # Equal weight
    limit=20
)

for result in results:
    print(f"RRF Score: {result.rrf_score:.3f}")
    print(f"Vector Similarity: {result.similarity:.3f}")
    print(f"Text Rank: {result.text_rank:.3f}")
    print(f"Content: {result.content[:100]}...")
    print("---")
```

## Understanding Alpha Parameter

The `alpha` parameter controls the balance between vector and text search in hybrid mode.

### Alpha Values Guide

```python
# Text-heavy (alpha = 0.0 to 0.3)
# Use when: Query has specific keywords, names, or technical terms
results = await memory.search(
    owner_id="workspace-1",
    query_text="Python asyncio gather timeout",
    search_type=SearchType.HYBRID,
    alpha=0.3  # Favor keyword matching
)

# Balanced (alpha = 0.4 to 0.6)
# Use when: General queries, uncertain which is better
results = await memory.search(
    owner_id="workspace-1",
    query_text="customer retention strategies",
    search_type=SearchType.HYBRID,
    alpha=0.5  # Equal weight (recommended default)
)

# Semantic-heavy (alpha = 0.7 to 1.0)
# Use when: Conceptual queries, synonyms, paraphrasing
results = await memory.search(
    owner_id="workspace-1",
    query_text="ways to keep customers happy",
    search_type=SearchType.HYBRID,
    alpha=0.7  # Favor semantic similarity
)
```

### Choosing Alpha for Different Query Types

| Query Type | Example | Recommended Alpha | Reasoning |
|------------|---------|-------------------|-----------|
| Specific keywords | "PostgreSQL CONNECTION_LIMIT error" | 0.2-0.3 | Need exact keyword matches |
| Product/person names | "iPhone 15 Pro specifications" | 0.3-0.4 | Names matter more than semantics |
| Technical jargon | "SOLID principles dependency injection" | 0.4-0.5 | Balance needed |
| General concepts | "improve team collaboration" | 0.5-0.6 | Balanced approach |
| Semantic queries | "how to motivate employees" | 0.6-0.7 | Semantic understanding key |
| Paraphrased questions | "what are good ways to retain staff" | 0.7-0.8 | Vector search excels |

## Reciprocal Rank Fusion (RRF)

Hybrid search uses RRF to merge vector and text search results into a unified ranking.

### How RRF Works

```python
k = 60  # RRF constant (prevents early results from dominating)

# Initialize score accumulator for each chunk
rrf_scores = {}

# Process vector search results
for rank, result in enumerate(vector_results):
    chunk_id = result["chunk_id"]
    vector_contribution = alpha / (k + rank + 1)
    rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0) + vector_contribution

# Process text search results
for rank, result in enumerate(text_results):
    chunk_id = result["chunk_id"]
    text_contribution = (1 - alpha) / (k + rank + 1)
    rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0) + text_contribution

# Sort by accumulated RRF score descending
sorted_results = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
```

**Key points:**
- Alpha is **inside** the division: `alpha / (k + rank + 1)`, not multiplied afterward
- Rank is 1-indexed: `rank + 1` where rank starts at 0
- Chunks appearing in **both** result lists get contributions from both
- k = 50 by default (configurable via `SearchConfig.rrf_k`)

### RRF Benefits

1. **Handles different score scales**: Vector similarities (0-1) and text ranks (varying) are normalized
2. **Position-based fusion**: Emphasizes consensus across search methods
3. **Robust to score outliers**: Single high score doesn't dominate
4. **Tunable with alpha**: Control the balance between search methods

### Example: RRF in Action

```python
results = await memory.search(
    owner_id="workspace-1",
    query_text="machine learning neural networks",
    search_type=SearchType.HYBRID,
    alpha=0.5,
    limit=5
)

for i, result in enumerate(results, 1):
    print(f"Result #{i}")
    print(f"  RRF Score: {result.rrf_score:.4f}")
    print(f"  Vector Sim: {result.similarity:.4f} (semantic match)")
    print(f"  Text Rank: {result.text_rank:.4f} (keyword match)")
    print(f"  Content: {result.content[:80]}...")
    print()

# Output shows how RRF balances both signals:
# Result #1
#   RRF Score: 0.0245  (highest combined score)
#   Vector Sim: 0.85   (very semantically similar)
#   Text Rank: 12.5    (good keyword match)
#   Content: Deep learning uses neural networks with multiple layers...
```

## Configuring Hybrid Search with SearchConfig

LLMemory's `SearchConfig` provides fine-grained control over hybrid search behavior, including HNSW vector index parameters and RRF fusion settings. You can configure these settings via environment variables or programmatically through `LLMemoryConfig`.

### HNSW Index Configuration

The HNSW (Hierarchical Navigable Small World) index powers fast approximate nearest neighbor vector search. LLMemory provides three preset profiles and supports custom configuration.

#### HNSW Parameters

- **`hnsw_m`** (int, default: 16): Number of bi-directional links per node
  - Higher values = better recall, larger index, slower construction
  - Range: 8-64, typical values: 8 (fast), 16 (balanced), 32 (accurate)

- **`hnsw_ef_construction`** (int, default: 200): Size of dynamic candidate list during index construction
  - Higher values = better index quality, slower construction
  - Range: 100-1000, typical values: 80 (fast), 200 (balanced), 400 (accurate)

- **`hnsw_ef_search`** (int, default: 100): Size of dynamic candidate list during search
  - Higher values = better recall, slower search
  - Range: 40-500, typical values: 40 (fast), 100 (balanced), 200 (accurate)

#### HNSW Presets

LLMemory includes three built-in presets for common use cases:

```python
HNSW_PRESETS = {
    "fast": {
        "m": 8,
        "ef_construction": 80,
        "ef_search": 40
    },
    "balanced": {
        "m": 16,
        "ef_construction": 200,
        "ef_search": 100
    },
    "accurate": {
        "m": 32,
        "ef_construction": 400,
        "ef_search": 200
    }
}
```

**Preset Recommendations:**
- **fast**: Latency-critical applications (40-60ms search, ~95% recall)
- **balanced**: General-purpose use (80-120ms search, ~98% recall) - **Default**
- **accurate**: High-precision requirements (150-250ms search, ~99.5% recall)

#### Using HNSW Presets via Environment Variable

Set the `LLMEMORY_HNSW_PROFILE` environment variable to use a preset:

```bash
# Use fast profile for low-latency applications
export LLMEMORY_HNSW_PROFILE=fast

# Use accurate profile for high-precision requirements
export LLMEMORY_HNSW_PROFILE=accurate

# Use balanced profile (default, can be omitted)
export LLMEMORY_HNSW_PROFILE=balanced
```

Then initialize LLMemory normally - the preset will be applied automatically:

```python
from llmemory import LLMemory, SearchType

# Automatically uses HNSW preset from environment
async with LLMemory(connection_string="postgresql://localhost/mydb") as memory:
    results = await memory.search(
        owner_id="workspace-1",
        query_text="machine learning",
        search_type=SearchType.HYBRID,
        limit=10
    )
```

#### Programmatic HNSW Configuration

For more control, configure HNSW parameters programmatically:

```python
from llmemory import LLMemory, SearchType
from llmemory.config import LLMemoryConfig

# Create custom configuration
config = LLMemoryConfig()

# Configure search parameters
config.search.hnsw_ef_search = 150  # Higher search accuracy

# Configure database/index parameters
config.database.hnsw_m = 24
config.database.hnsw_ef_construction = 300

# Initialize with custom config
async with LLMemory(
    connection_string="postgresql://localhost/mydb",
    config=config
) as memory:
    results = await memory.search(
        owner_id="workspace-1",
        query_text="neural networks",
        search_type=SearchType.HYBRID,
        limit=10
    )
```

**Note:** Index construction parameters (`hnsw_m`, `hnsw_ef_construction`) only affect **new indexes**. To apply them to an existing index, you must recreate the index:

```sql
-- Recreate HNSW index with new parameters
DROP INDEX IF EXISTS llmemory.document_chunks_embedding_hnsw;
CREATE INDEX document_chunks_embedding_hnsw
ON llmemory.document_chunks
USING hnsw (embedding vector_cosine_ops)
WITH (m = 24, ef_construction = 300);
```

### RRF Configuration

The `rrf_k` parameter controls the Reciprocal Rank Fusion constant used to merge vector and text search results.

#### RRF Parameter

- **`rrf_k`** (int, default: 50): RRF constant that controls rank position sensitivity
  - Higher values = less weight on top positions, more democratic fusion
  - Lower values = more weight on top positions, favors high-ranking results
  - Range: 10-100, typical values: 30 (aggressive), 50 (balanced), 70 (democratic)

**How rrf_k affects fusion:**

```python
# For a chunk at rank position r (0-indexed):
rrf_score_contribution = alpha / (rrf_k + r + 1)

# Example with rrf_k=50:
# Rank 0: 1.0 / (50 + 0 + 1) = 0.0196
# Rank 1: 1.0 / (50 + 1 + 1) = 0.0192
# Rank 10: 1.0 / (50 + 10 + 1) = 0.0164

# Example with rrf_k=20 (favors top results):
# Rank 0: 1.0 / (20 + 0 + 1) = 0.0476
# Rank 1: 1.0 / (20 + 1 + 1) = 0.0455
# Rank 10: 1.0 / (20 + 10 + 1) = 0.0323

# Example with rrf_k=80 (more democratic):
# Rank 0: 1.0 / (80 + 0 + 1) = 0.0123
# Rank 1: 1.0 / (80 + 1 + 1) = 0.0122
# Rank 10: 1.0 / (80 + 10 + 1) = 0.0110
```

#### Configuring RRF via Environment Variable

```bash
# Lower k favors top-ranked results
export LLMEMORY_RRF_K=30

# Higher k gives more weight to mid-ranked results
export LLMEMORY_RRF_K=70

# Default balanced setting
export LLMEMORY_RRF_K=50
```

**Note:** Currently, `rrf_k` is not directly exposed via environment variable. To configure it, use programmatic configuration:

```python
from llmemory import LLMemory
from llmemory.config import LLMemoryConfig

config = LLMemoryConfig()
config.search.rrf_k = 30  # Favor top-ranked results

async with LLMemory(
    connection_string="postgresql://localhost/mydb",
    config=config
) as memory:
    results = await memory.search(
        owner_id="workspace-1",
        query_text="search query",
        search_type=SearchType.HYBRID,
        limit=10
    )
```

### Complete Configuration Example

Here's a complete example showing both environment variable and programmatic configuration:

```python
import os
from llmemory import LLMemory, SearchType
from llmemory.config import LLMemoryConfig

# Option 1: Environment variable configuration
os.environ["LLMEMORY_HNSW_PROFILE"] = "accurate"
# HNSW will use: m=32, ef_construction=400, ef_search=200

async with LLMemory(connection_string="postgresql://localhost/mydb") as memory:
    results = await memory.search(
        owner_id="workspace-1",
        query_text="deep learning transformers",
        search_type=SearchType.HYBRID,
        alpha=0.6,
        limit=15
    )

# Option 2: Programmatic configuration with fine-tuning
config = LLMemoryConfig()

# HNSW search configuration
config.search.hnsw_ef_search = 150  # Higher accuracy than default

# HNSW index construction (for new indexes)
config.database.hnsw_m = 20
config.database.hnsw_ef_construction = 250

# RRF configuration
config.search.rrf_k = 40  # Favor top-ranked results slightly

# Other search settings
config.search.default_limit = 20
config.search.default_search_type = "hybrid"

async with LLMemory(
    connection_string="postgresql://localhost/mydb",
    config=config
) as memory:
    # Search with custom configuration
    results = await memory.search(
        owner_id="workspace-1",
        query_text="neural network architectures",
        search_type=SearchType.HYBRID,
        alpha=0.5,
        limit=20
    )

    for result in results:
        print(f"RRF: {result.rrf_score:.4f} | "
              f"Vector: {result.similarity:.4f} | "
              f"Text: {result.text_rank:.4f}")
        print(f"  {result.content[:80]}...")
```

### Configuration Performance Impact

Different HNSW settings have measurable performance impacts:

| Profile | Index Size (100k docs) | Construction Time | Search Latency | Recall |
|---------|------------------------|-------------------|----------------|--------|
| fast | 150 MB | 5 min | 40-60ms | ~95% |
| balanced | 250 MB | 12 min | 80-120ms | ~98% |
| accurate | 450 MB | 30 min | 150-250ms | ~99.5% |

**Tuning Guidelines:**

1. **Start with balanced** (default) for most applications
2. **Use fast** if:
   - Search latency must be under 100ms
   - Recall around 95% is acceptable
   - Index size is a constraint
3. **Use accurate** if:
   - High precision is critical (medical, legal, financial)
   - Search latency under 300ms is acceptable
   - Maximum recall is required
4. **Custom tune** if:
   - You have specific latency/recall requirements
   - You've measured performance with your data
   - You're optimizing for your embedding model

## Search Type Comparison

### Vector Search Only

```python
# Pure semantic similarity
results = await memory.search(
    owner_id="workspace-1",
    query_text="artificial intelligence",
    search_type=SearchType.VECTOR,
    limit=10
)

# Good for:
# - "AI" matching "machine learning" (synonym)
# - "dog" matching "puppy" (semantic)
# - Cross-lingual search
#
# Weak for:
# - Specific keywords ("PostgreSQL 14.2")
# - Exact phrases ("return on investment")
# - Technical terms ("ValueError exception")
```

### Text Search Only

```python
# Pure keyword matching
results = await memory.search(
    owner_id="workspace-1",
    query_text="PostgreSQL CONNECTION_LIMIT",
    search_type=SearchType.TEXT,
    limit=10
)

# Good for:
# - Exact keyword matches
# - Technical error messages
# - Code search
# - Structured data
#
# Weak for:
# - Synonyms ("automobile" vs "car")
# - Paraphrasing
# - Conceptual queries
```

### Hybrid Search (Recommended)

```python
# Combines both vector and text
results = await memory.search(
    owner_id="workspace-1",
    query_text="reduce server response time",
    search_type=SearchType.HYBRID,
    alpha=0.5,
    limit=10
)

# Strengths:
# - Finds semantically similar content ("optimize latency")
# - Also finds exact keywords ("response time")
# - Best overall retrieval quality
# - Robust to different query styles
#
# Use cases:
# - General-purpose search (recommended default)
# - Unknown query patterns
# - Mixed keyword + semantic needs
```

## Practical Examples

### E-commerce Product Search

```python
# Product search benefits from hybrid
# - Vector: Understands "laptop for programming"
# - Text: Matches exact model numbers "MacBook Pro M3"

results = await memory.search(
    owner_id="store-1",
    query_text="fast laptop for developers",
    search_type=SearchType.HYBRID,
    alpha=0.6,  # Favor semantic understanding
    metadata_filter={"category": "computers"},
    limit=20
)
```

### Technical Documentation Search

```python
# Documentation needs both semantic and exact matches
# - Vector: Finds conceptually related docs
# - Text: Finds exact function/class names

results = await memory.search(
    owner_id="docs-site",
    query_text="authenticate users with OAuth2",
    search_type=SearchType.HYBRID,
    alpha=0.4,  # Slight favor to keywords ("OAuth2")
    metadata_filter={"doc_type": "api_reference"},
    limit=15
)
```

### Customer Support Search

```python
# Support tickets need semantic understanding
# - Vector: Matches similar issues ("can't log in" = "login failed")
# - Text: Matches error codes, product names

results = await memory.search(
    owner_id="support-team",
    query_text="error code 500 payment processing",
    search_type=SearchType.HYBRID,
    alpha=0.3,  # Favor exact error codes
    metadata_filter={"status": "resolved"},
    limit=10
)
```

### Research Paper Search

```python
# Academic search benefits from semantic understanding
# - Vector: Finds related concepts and methods
# - Text: Finds exact citations, author names

results = await memory.search(
    owner_id="research-db",
    query_text="transformer attention mechanism",
    search_type=SearchType.HYBRID,
    alpha=0.7,  # Favor semantic similarity
    date_from=datetime(2020, 1, 1),  # Recent papers
    limit=25
)
```

## Performance Optimization

### Hybrid Search Performance

Hybrid search runs vector and text searches **in parallel** for optimal performance:

```python
# Both searches execute concurrently
# Total time ≈ max(vector_time, text_time) + rrf_fusion_time
# Typically: 50-150ms for hybrid search

import time

start = time.time()
results = await memory.search(
    owner_id="workspace-1",
    query_text="customer retention",
    search_type=SearchType.HYBRID,
    limit=20
)
elapsed = (time.time() - start) * 1000
print(f"Search completed in {elapsed:.2f}ms")
```

### Tuning for Speed vs Quality

```python
# Faster hybrid search (fewer candidates)
results = await memory.search(
    owner_id="workspace-1",
    query_text="query text",
    search_type=SearchType.HYBRID,
    limit=10,  # Lower limit = faster
    alpha=0.5
)

# Higher quality hybrid search (more candidates considered)
# Note: Uses internal candidate multiplier (typically limit * 2)
results = await memory.search(
    owner_id="workspace-1",
    query_text="query text",
    search_type=SearchType.HYBRID,
    limit=20,  # Higher limit for better recall
    alpha=0.5
)
```

## Advanced Filtering with Hybrid Search

```python
# Combine hybrid search with metadata filters
results = await memory.search(
    owner_id="workspace-1",
    query_text="financial performance analysis",
    search_type=SearchType.HYBRID,
    alpha=0.5,
    metadata_filter={
        "department": "finance",
        "year": 2024,
        "confidential": False
    },
    date_from=datetime(2024, 1, 1),
    date_to=datetime(2024, 12, 31),
    limit=15
)

# Hybrid search finds:
# - Vector: Similar financial concepts
# - Text: Exact keyword "performance analysis"
# - Both filtered by metadata and date range
```

## Common Mistakes

❌ **Wrong: Always using default alpha=0.5**
```python
# This works but may not be optimal
results = await memory.search(
    owner_id="workspace-1",
    query_text="iPhone 14 Pro specs",  # Specific product name
    search_type=SearchType.HYBRID,
    alpha=0.5  # Equal weight not ideal here
)
```

✅ **Right: Tune alpha for query type**
```python
# Product names and specific terms favor text search
results = await memory.search(
    owner_id="workspace-1",
    query_text="iPhone 14 Pro specs",
    search_type=SearchType.HYBRID,
    alpha=0.3  # Favor exact keyword matching
)
```

❌ **Wrong: Using VECTOR for exact keyword matching**
```python
results = await memory.search(
    owner_id="workspace-1",
    query_text="ERROR CODE 404",
    search_type=SearchType.VECTOR  # Won't find exact "404"
)
```

✅ **Right: Use HYBRID or TEXT for exact keywords**
```python
results = await memory.search(
    owner_id="workspace-1",
    query_text="ERROR CODE 404",
    search_type=SearchType.HYBRID,
    alpha=0.2  # Heavily favor exact keywords
)
```

❌ **Wrong: Using TEXT for conceptual queries**
```python
results = await memory.search(
    owner_id="workspace-1",
    query_text="how to improve customer satisfaction",
    search_type=SearchType.TEXT  # Misses semantic matches
)
```

✅ **Right: Use HYBRID for conceptual queries**
```python
results = await memory.search(
    owner_id="workspace-1",
    query_text="how to improve customer satisfaction",
    search_type=SearchType.HYBRID,
    alpha=0.7  # Favor semantic understanding
)
```

## Alpha Tuning Strategies

### A/B Testing Different Alpha Values

```python
# Test different alpha values to find optimal setting
query = "product launch strategy roadmap"
alpha_values = [0.3, 0.5, 0.7]

for alpha in alpha_values:
    results = await memory.search(
        owner_id="workspace-1",
        query_text=query,
        search_type=SearchType.HYBRID,
        alpha=alpha,
        limit=10
    )

    print(f"\nAlpha = {alpha}")
    for i, result in enumerate(results[:3], 1):
        print(f"  #{i}: {result.content[:60]}... (RRF={result.rrf_score:.4f})")
    # Compare results quality and adjust
```

### Dynamic Alpha Based on Query Analysis

```python
def calculate_alpha(query_text: str) -> float:
    """Dynamically adjust alpha based on query characteristics."""
    # Check for exact phrases (quotes)
    if '"' in query_text:
        return 0.2  # Favor exact matching

    # Check for technical terms or codes
    if any(char.isdigit() or char.isupper() for char in query_text.split()):
        return 0.3  # Favor keywords

    # Check for question words (semantic query)
    question_words = ["how", "why", "what", "when", "where", "who"]
    if any(word in query_text.lower() for word in question_words):
        return 0.7  # Favor semantic

    # Default balanced
    return 0.5

# Use dynamic alpha
query = "how to optimize database queries"
alpha = calculate_alpha(query)

results = await memory.search(
    owner_id="workspace-1",
    query_text=query,
    search_type=SearchType.HYBRID,
    alpha=alpha,
    limit=10
)
```

## Monitoring and Debugging

### Understanding Result Scores

```python
results = await memory.search(
    owner_id="workspace-1",
    query_text="test query",
    search_type=SearchType.HYBRID,
    alpha=0.5,
    limit=5
)

for result in results:
    # Inspect individual scores
    print(f"Chunk ID: {result.chunk_id}")
    print(f"  RRF Score: {result.rrf_score:.4f} (overall ranking)")
    print(f"  Vector Similarity: {result.similarity:.4f}")
    print(f"  Text Rank: {result.text_rank:.4f}")
    print(f"  Content preview: {result.content[:80]}...")
    print()

# Look for:
# - High RRF but low similarity = text search dominated
# - High RRF but low text rank = vector search dominated
# - High in both = strong consensus (best results)
```

## Related Skills

- `basic-usage` - Core document and search operations
- `multi-query` - Query expansion for better hybrid search results
- `rag` - Using hybrid search in RAG systems with reranking
- `multi-tenant` - Multi-tenant isolation patterns

## Important Notes

**HNSW Configuration:**
Hybrid search uses HNSW (Hierarchical Navigable Small World) index for fast vector similarity. Performance can be tuned with `LLMEMORY_HNSW_PROFILE` environment variable or programmatically via `SearchConfig`. See the "Configuring Hybrid Search with SearchConfig" section for comprehensive configuration details including:
- Three presets: `fast`, `balanced` (default), `accurate`
- Individual HNSW parameters (m, ef_construction, ef_search)
- RRF tuning with `rrf_k` parameter
- Performance impact comparison table

**Language Support:**
Text search automatically detects document language and uses appropriate full-text search configuration (supports 14+ languages including English, Spanish, French, German, etc.).

**Embedding Models:**
Vector search quality depends on embedding model. Default is OpenAI `text-embedding-3-small` (1536 dimensions). For local embeddings, use `all-MiniLM-L6-v2` (384 dimensions).

**Search Limits:**
Hybrid search internally retrieves `limit * 2` candidates from each search method before RRF fusion. This ensures high-quality results even when vector and text return different chunks.
