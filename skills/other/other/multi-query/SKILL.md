---
name: multi-query
description: Use when search queries need better recall through query expansion - generates multiple query variants, retrieves with each, and fuses results using RRF for improved retrieval quality especially with ambiguous or under-specified queries
version: 0.5.0
---

# LLMemory Multi-Query Expansion

## Installation

```bash
uv add llmemory
# or
pip install llmemory
```

## Overview

Multi-query expansion improves search recall by:
1. Generating multiple query variants from the original query
2. Searching with each variant independently
3. Fusing results using Reciprocal Rank Fusion (RRF)
4. Returning unified, deduplicated results

**Two expansion modes:**
- **Heuristic (default)**: Fast lexical variants using keyword extraction, OR clauses, and phrase matching. No LLM calls, <1ms latency.
- **LLM-based (configurable)**: Semantic query variants using GPT-4o-mini or similar. Better recall, 50-200ms latency, requires API key.

**When to use multi-query expansion:**
- Queries are ambiguous or under-specified
- Want to capture different perspectives or phrasings
- Improve recall for complex information needs
- User queries tend to be short or vague

**When NOT to use:**
- Queries are already very specific
- Latency is critical (multi-query adds overhead)
- Simple keyword lookups

## Quick Start

```python
from llmemory import LLMemory, SearchType

async with LLMemory(connection_string="postgresql://localhost/mydb") as memory:
    # Enable query expansion
    results = await memory.search(
        owner_id="workspace-1",
        query_text="improve customer satisfaction",
        search_type=SearchType.HYBRID,
        query_expansion=True,  # Enable expansion
        max_query_variants=3,  # Generate 3 variants
        limit=10
    )

    # Results are from all 3 query variants, fused with RRF
    for result in results:
        print(f"[{result.rrf_score:.3f}] {result.content[:80]}...")
```

## Complete API Documentation

### search() with Query Expansion

**Signature:**
```python
async def search(
    owner_id: str,
    query_text: str,
    search_type: Union[SearchType, str] = SearchType.HYBRID,
    limit: int = 10,
    query_expansion: Optional[bool] = None,
    max_query_variants: Optional[int] = None,
    **kwargs
) -> List[SearchResult]
```

**Query Expansion Parameters:**
- `query_expansion` (bool, optional): Enable/disable query expansion
  - `None` (default): Follow global config (`LLMEMORY_ENABLE_QUERY_EXPANSION`)
  - `True`: Force enable for this search
  - `False`: Force disable for this search

- `max_query_variants` (int, optional): Maximum query variants to generate
  - Default: 3 (from config `search.max_query_variants`)
  - Range: 1-5 (practical limit for performance)
  - Includes original query + (N-1) generated variants

**Returns:**
- `List[SearchResult]` with multi-query specific behavior:
  - Results fused from all query variants using RRF
  - Each result's `rrf_score` reflects consensus across variants
  - Deduplicatedby chunk_id (same chunk from multiple variants counted once)

**Example:**
```python
# Basic multi-query search
results = await memory.search(
    owner_id="workspace-1",
    query_text="reduce server latency",
    search_type=SearchType.HYBRID,
    query_expansion=True,
    max_query_variants=3,
    limit=15
)

# Variants might be:
# 1. "reduce server latency" (original)
# 2. "improve server response time"
# 3. "optimize backend performance"

# All 3 variants are searched, results are fused
```

## How Multi-Query Works

### Query Variant Generation

llmemory generates query variants using **heuristic rules** (no LLM required by default):

```
Original Query: "customer retention strategies"

Generated Variants:
1. "customer retention strategies" (original, always included)
2. "customer OR retention OR strategies" (OR variant - widens lexical recall)
3. "\"customer retention strategies\"" (quoted phrase - exact match)

Each variant captures a different matching strategy:
- Original: Standard BM25 matching
- OR variant: Boolean OR to catch documents with any key term
- Quoted phrase: Exact phrase matching for precision
```

**With stopwords:**
```
Original Query: "how to improve the customer satisfaction"

Generated Variants:
1. "how to improve the customer satisfaction" (original)
2. "how improve customer satisfaction" (keyword variant - stopwords removed)
3. "how OR improve OR customer OR satisfaction" (OR variant)
4. "\"how to improve the customer satisfaction\"" (quoted phrase)
```

### Search Execution

```python
# Internally, multi-query does:
# 1. Generate variants
variants = [
    "customer retention strategies",           # original
    "customer OR retention OR strategies",     # OR variant
    "\"customer retention strategies\""        # quoted phrase
]

# 2. Search with each variant (executed sequentially)
results_1 = await search(query=variants[0], ...)
results_2 = await search(query=variants[1], ...)
results_3 = await search(query=variants[2], ...)

# 3. Fuse results using RRF
final_results = rrf_fusion([results_1, results_2, results_3])
```

### RRF Fusion

Reciprocal Rank Fusion combines results from multiple query variants:

```
For each query variant:
    For each result in that variant:
        score = 1 / (k + rank + 1)

For each unique chunk (by chunk_id):
    total_score = sum of scores from all variants

Sort by total_score descending
```

Where `k = 50` (constant that prevents top-ranked results from dominating). Note the `+ 1` ensures the first result (rank=0) gets score `1/(50+0+1) = 1/51` rather than `1/50`.

**Key insight:** Chunks appearing in multiple variant result sets get higher RRF scores, indicating strong relevance consensus.

## Practical Examples

### Customer Support Search

```python
# Original query is vague
results = await memory.search(
    owner_id="support-team",
    query_text="login problems",
    search_type=SearchType.HYBRID,
    query_expansion=True,
    max_query_variants=3,
    limit=20
)

# Variants use different matching strategies:
# - "login problems" (original)
# - "login OR problems" (OR variant - widens recall)
# - "\"login problems\"" (exact phrase)
#
# Results include:
# - Documents with both "login" AND "problems" (original)
# - Documents with either "login" OR "problems" (OR variant)
# - Documents with exact phrase "login problems" (quoted variant)
```

### Product Documentation Search

```python
# Technical query benefits from multiple phrasings
results = await memory.search(
    owner_id="docs-site",
    query_text="async function error handling",
    search_type=SearchType.HYBRID,
    query_expansion=True,
    max_query_variants=4,
    limit=15
)

# Variants use different matching:
# - "async function error handling" (original)
# - "async function error handling" (keyword variant - no stopwords here)
# - "async OR function OR error OR handling" (OR variant)
# - "\"async function error handling\"" (exact phrase)
#
# Balances precision (exact phrase) with recall (OR variant)
```

### Research & Discovery

```python
# Exploratory queries need broad coverage
results = await memory.search(
    owner_id="research-db",
    query_text="climate change mitigation",
    search_type=SearchType.HYBRID,
    query_expansion=True,
    max_query_variants=5,
    limit=25
)

# Variants use different matching:
# - "climate change mitigation" (original)
# - "climate OR change OR mitigation" (OR variant)
# - "\"climate change mitigation\"" (exact phrase)
```

### E-commerce Search

```python
# Product searches benefit from synonyms and alternatives
results = await memory.search(
    owner_id="store-1",
    query_text="lightweight laptop for travel",
    search_type=SearchType.HYBRID,
    query_expansion=True,
    max_query_variants=3,
    metadata_filter={"category": "electronics"},
    limit=20
)

# Variants use different matching:
# - "lightweight laptop for travel" (original)
# - "lightweight laptop travel" (keyword variant - stopwords removed)
# - "lightweight OR laptop OR travel" (OR variant)
# - "\"lightweight laptop for travel\"" (exact phrase)
```

## Configuration

### Global Configuration

```bash
# Environment variables
LLMEMORY_ENABLE_QUERY_EXPANSION=1
LLMEMORY_MAX_QUERY_VARIANTS=3
```

### Programmatic Configuration

```python
from llmemory import LLMemoryConfig

config = LLMemoryConfig()
config.search.enable_query_expansion = True
config.search.max_query_variants = 3

memory = LLMemory(
    connection_string="postgresql://localhost/mydb",
    config=config
)
```

### LLM-Based Expansion (Advanced)

For semantic query diversity, enable LLM-based expansion:

**Environment Variables:**
```bash
LLMEMORY_ENABLE_QUERY_EXPANSION=1
LLMEMORY_QUERY_EXPANSION_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-...
```

**Programmatic Configuration:**
```python
from llmemory import LLMemoryConfig

config = LLMemoryConfig()
config.search.enable_query_expansion = True
config.search.query_expansion_model = "gpt-4o-mini"  # Enable LLM expansion
config.search.max_query_variants = 3

memory = LLMemory(
    connection_string="postgresql://localhost/mydb",
    openai_api_key="sk-...",
    config=config
)
```

**LLM vs Heuristic Comparison:**

| Mode | Latency | Quality | Cost | Use Case |
|------|---------|---------|------|----------|
| Heuristic | <1ms | Good | Free | Default, high-QPS |
| LLM | 50-200ms | Excellent | ~$0.001/query | Quality-critical |

**LLM Expansion Example:**
```python
# Original: "improve customer retention"
# LLM variants:
#   1. "strategies to reduce customer churn"
#   2. "methods for increasing customer loyalty"
#   3. "how to keep customers from leaving"

results = await memory.search(
    owner_id="workspace-1",
    query_text="improve customer retention",
    query_expansion=True,
    max_query_variants=3,
    limit=10
)
```

### Per-Query Override

```python
# Override global config for specific searches

# Force enable (even if globally disabled)
results = await memory.search(
    owner_id="workspace-1",
    query_text="vague query here",
    query_expansion=True,  # Force enable
    max_query_variants=4,
    limit=10
)

# Force disable (even if globally enabled)
results = await memory.search(
    owner_id="workspace-1",
    query_text="very specific query",
    query_expansion=False,  # Force disable
    limit=10
)
```

## Performance Considerations

### Latency Impact

```python
import time

# Without query expansion (fast)
start = time.time()
results = await memory.search(
    owner_id="workspace-1",
    query_text="test query",
    query_expansion=False,
    limit=10
)
elapsed_single = (time.time() - start) * 1000
print(f"Single query: {elapsed_single:.2f}ms")

# With query expansion (slower)
start = time.time()
results = await memory.search(
    owner_id="workspace-1",
    query_text="test query",
    query_expansion=True,
    max_query_variants=3,
    limit=10
)
elapsed_multi = (time.time() - start) * 1000
print(f"Multi-query: {elapsed_multi:.2f}ms")

# Typical overhead:
# - Variant generation: <1ms (heuristic rules, no LLM)
# - Additional searches: 3x search time (executed in sequence)
# - RRF fusion: 5-10ms
# Total overhead: ~3x base search latency + minimal fusion overhead
```

### Optimizing Performance

```python
# Use fewer variants for speed
results = await memory.search(
    owner_id="workspace-1",
    query_text="query",
    query_expansion=True,
    max_query_variants=2,  # Faster than 3-4 (fewer searches to execute)
    limit=10
)
```

### When to Use Multi-Query

**Good use cases:**
- Queries that might match with different keyword combinations
- Short queries where OR expansion helps recall
- Queries where both exact and fuzzy matching are valuable
- Cases where you want to balance precision (quoted) and recall (OR)

**Avoid for:**
- Very specific queries (expansion doesn't help)
- High-QPS API endpoints (multiplies search cost)
- When latency is critical (3x+ base search time)
- Pure semantic search (heuristic variants don't add semantic diversity)

## Combining with Other Features

### Multi-Query + Reranking

```python
# Combine query expansion with reranking for best quality
results = await memory.search(
    owner_id="workspace-1",
    query_text="machine learning deployment",
    search_type=SearchType.HYBRID,
    query_expansion=True,      # Generate variants
    max_query_variants=3,
    rerank=True,               # Rerank fused results
    rerank_top_k=50,           # Consider top 50 from RRF
    rerank_return_k=15,        # Return top 15 after reranking
    limit=15
)

# Pipeline:
# 1. Generate 3 query variants
# 2. Search with each variant
# 3. Fuse with RRF (top 50 candidates)
# 4. Rerank top 50 candidates
# 5. Return top 15 after reranking
```

### Multi-Query + Metadata Filtering

```python
# Apply filters to all query variants
results = await memory.search(
    owner_id="workspace-1",
    query_text="quarterly performance",
    search_type=SearchType.HYBRID,
    query_expansion=True,
    max_query_variants=3,
    metadata_filter={
        "department": "finance",
        "year": 2024
    },
    date_from=datetime(2024, 1, 1),
    limit=20
)

# All 3 variants search within filtered documents only
```

### Multi-Query + Hybrid Search Tuning

```python
# Tune alpha for all query variants
results = await memory.search(
    owner_id="workspace-1",
    query_text="customer feedback analysis",
    search_type=SearchType.HYBRID,
    alpha=0.6,              # Applied to all variants
    query_expansion=True,
    max_query_variants=3,
    limit=15
)

# Each variant uses alpha=0.6 for hybrid search
# Results are then fused with RRF
```

## Monitoring and Debugging

### Inspecting Query Variants

Multi-query search logs include the generated variants in diagnostics:

```python
# After search, variants are logged
# Check application logs or search history for:
# {
#   "query_variants": [
#     "original query",
#     "variant 1",
#     "variant 2"
#   ],
#   "variant_stats": [
#     {"query": "original", "result_count": 15, "latency_ms": 45.3},
#     {"query": "variant 1", "result_count": 18, "latency_ms": 42.1},
#     {"query": "variant 2", "result_count": 12, "latency_ms": 48.7}
#   ]
# }
```

### Understanding RRF Scores

```python
results = await memory.search(
    owner_id="workspace-1",
    query_text="test",
    query_expansion=True,
    max_query_variants=3,
    limit=10
)

for result in results:
    print(f"Chunk: {result.chunk_id}")
    print(f"  RRF Score: {result.rrf_score:.4f}")
    print(f"  Content: {result.content[:80]}...")
    print()

# Higher RRF scores indicate:
# - Chunk appeared in multiple variant results
# - Chunk ranked highly across variants
# - Strong consensus on relevance
```

## Common Mistakes

❌ **Wrong: Using multi-query for all searches**
```python
# Don't enable globally if not needed
results = await memory.search(
    owner_id="workspace-1",
    query_text="iPhone 14 Pro",  # Very specific, doesn't need expansion
    query_expansion=True,         # Adds latency without benefit
    limit=10
)
```

✅ **Right: Use selectively for complex queries**
```python
# Enable only when query benefits from expansion
if is_complex_query(query_text):
    query_expansion = True
else:
    query_expansion = False

results = await memory.search(
    owner_id="workspace-1",
    query_text=query_text,
    query_expansion=query_expansion,
    limit=10
)
```

❌ **Wrong: Too many query variants**
```python
results = await memory.search(
    owner_id="workspace-1",
    query_text="test",
    query_expansion=True,
    max_query_variants=10,  # Too many, diminishing returns
    limit=10
)
# Latency increases linearly but quality plateaus
```

✅ **Right: Use 2-4 variants for balance**
```python
results = await memory.search(
    owner_id="workspace-1",
    query_text="test",
    query_expansion=True,
    max_query_variants=3,  # Good balance of quality vs speed
    limit=10
)
```

❌ **Wrong: Ignoring latency requirements**
```python
# Real-time autocomplete endpoint
@app.get("/autocomplete")
async def autocomplete(q: str):
    results = await memory.search(
        owner_id="workspace-1",
        query_text=q,
        query_expansion=True,  # Too slow for autocomplete!
        limit=5
    )
    return results
```

✅ **Right: Consider latency constraints**
```python
# Use multi-query for main search, not autocomplete
@app.get("/autocomplete")
async def autocomplete(q: str):
    results = await memory.search(
        owner_id="workspace-1",
        query_text=q,
        query_expansion=False,  # Fast single query
        limit=5
    )
    return results

@app.get("/search")
async def search(q: str):
    results = await memory.search(
        owner_id="workspace-1",
        query_text=q,
        query_expansion=True,  # Quality search with expansion
        max_query_variants=3,
        limit=20
    )
    return results
```

## Query Variant Generation Strategies

Multi-query uses **heuristic rules** to generate variants, not LLM-based expansion:

### 1. Keyword Variant (Stopword Removal)

Removes common stopwords to focus on key terms:

```python
from llmemory.query_expansion import DEFAULT_STOPWORDS

# Stopwords include: a, an, and, are, as, at, be, by, for, from, has,
# in, is, it, of, on, or, that, the, to, was, were, will, with

# Example:
# Input:  "how to improve the customer satisfaction"
# Output: "how improve customer satisfaction"
#
# Input:  "best practices for the database"
# Output: "best practices database"
```

Enabled by default via `config.search.include_keyword_variant = True`.

### 2. OR Variant (Boolean Expansion)

Creates Boolean OR of all non-stopword terms to maximize recall:

```python
# Example:
# Input:  "customer retention strategies"
# Output: "customer OR retention OR strategies"
#
# Input:  "reduce server latency"
# Output: "reduce OR server OR latency"
```

Only generated for multi-word queries. Widens recall by matching documents containing ANY of the key terms.

### 3. Quoted Phrase Variant (Exact Match)

Wraps the query in quotes for exact phrase matching:

```python
# Example:
# Input:  "machine learning deployment"
# Output: "\"machine learning deployment\""
#
# Input:  "error handling"
# Output: "\"error handling\""
```

Only generated for multi-word queries. Ensures high precision by requiring exact phrase match.

### Complete Example

```python
from llmemory.query_expansion import QueryExpansionService
from llmemory.config import SearchConfig

service = QueryExpansionService(SearchConfig())

# With stopwords
variants = service._heuristic_variants(
    "how to improve the customer satisfaction",
    include_keywords=True
)
# Returns:
# 1. "how improve customer satisfaction" (keyword variant)
# 2. "how OR improve OR customer OR satisfaction" (OR variant)
# 3. "\"how to improve the customer satisfaction\"" (quoted phrase)

# Without stopwords
variants = service._heuristic_variants(
    "machine learning deployment",
    include_keywords=True
)
# Returns:
# 1. "machine OR learning OR deployment" (OR variant, no keyword variant since no stopwords)
# 2. "\"machine learning deployment\"" (quoted phrase)
```

### Advanced: Custom LLM-Based Expansion

The default implementation uses heuristics, but you can provide a custom LLM callback:

```python
from llmemory.query_expansion import QueryExpansionService, ExpansionCallback

async def my_llm_expander(query: str, max_variants: int) -> list[str]:
    """Custom LLM-based query expansion."""
    # Call your LLM here to generate semantic variants
    variants = await my_llm.generate_variants(query, max_variants)
    return variants

service = QueryExpansionService(
    search_config=config.search,
    llm_callback=my_llm_expander  # Optional custom expansion
)
```

When `llm_callback` is provided, it's tried first; heuristics are used as fallback if LLM fails.

## Advanced Patterns

### Conditional Multi-Query

```python
def should_expand_query(query_text: str) -> tuple[bool, int]:
    """Decide if query needs expansion and how many variants."""
    # Short queries benefit most from expansion
    if len(query_text.split()) <= 3:
        return True, 4

    # Questions and exploratory queries
    question_words = ["how", "what", "why", "when", "where", "who"]
    if any(word in query_text.lower() for word in question_words):
        return True, 3

    # Specific queries don't need expansion
    if any(char.isdigit() for char in query_text):  # Has numbers
        return False, 1

    if '"' in query_text:  # Has quotes (exact phrase)
        return False, 1

    # Default: moderate expansion
    return True, 2

# Use dynamic expansion
query = "how to improve performance"
expand, variants = should_expand_query(query)

results = await memory.search(
    owner_id="workspace-1",
    query_text=query,
    query_expansion=expand,
    max_query_variants=variants,
    limit=10
)
```

### A/B Testing Query Expansion

```python
import random

# Randomly enable/disable for 50% of queries
use_expansion = random.random() < 0.5

results = await memory.search(
    owner_id="workspace-1",
    query_text=query_text,
    query_expansion=use_expansion,
    limit=10
)

# Track metrics:
# - Click-through rate
# - Result relevance
# - User satisfaction
# - Search latency
# Compare A (no expansion) vs B (with expansion)
```

## Related Skills

- `basic-usage` - Core search operations
- `hybrid-search` - Vector + text hybrid search fundamentals
- `rag` - Using multi-query in RAG systems
- `multi-tenant` - Multi-tenant isolation patterns

## Important Notes

**Expansion Modes:**
- **Heuristic (default)**: Keyword extraction, OR clauses, phrase matching. Fast, no API calls.
- **LLM (configurable)**: Semantic variants via GPT-4o-mini. Set `query_expansion_model` in config.

**No LLM Required for Default:**
Query expansion works out-of-the-box with heuristic rules. No API key or LLM calls needed unless you configure `query_expansion_model`.

**Cost Considerations (LLM mode only):**
LLM expansion makes 1 API call per search. For high-volume applications with LLM expansion, consider:
- Caching common queries and their variants
- Using smaller models (gpt-4o-mini is fast and cheap)
- Enabling only for specific use cases
- Hybrid: Use heuristics for autocomplete, LLM for main search

**Quality vs Speed:**
- Heuristic: <1ms overhead, lexical diversity only
- LLM: 50-200ms overhead, semantic diversity

**Fallback Behavior:**
If LLM expansion fails or times out (8s), system automatically falls back to heuristic expansion. Search always completes.
