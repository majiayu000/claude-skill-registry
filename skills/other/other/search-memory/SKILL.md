---
name: search-memory
version: "1.0.0"
description: >
  Search the hierarchical memory system for relevant memories. Searches across
  all tiers (working, episodic, semantic) and returns ranked results. Use for
  context retrieval and pattern matching. Keywords: memory, search, retrieve,
  recall, context, similarity.
metadata:
  domain: general
  category: memory
  requires-approval: false
  confidence: 0.9
  mcp-servers: []
---

# Search Memory

## Preconditions

Before applying this skill, verify:

- Memory system is initialized
- Search query is meaningful
- Result limit is specified

## Actions

### 1. Build Search Query

Prepare the semantic search query:
```yaml
query: $search_text
user_id: $user_id
limit: $result_limit (default: 10)
```

### 2. Search Each Tier

**Working Memory (exact + recency):**
```python
working_results = memory.search_working(query, limit=limit//3)
```

**Episodic Memory (semantic + time decay):**
```python
episodic_results = memory.search_episodic(
    query=query,
    user_id=user_id,
    limit=limit//3
)
```

**Semantic Memory (semantic + permanence):**
```python
semantic_results = memory.search_semantic(
    query=query,
    user_id=user_id,
    limit=limit//3
)
```

### 3. Merge and Rank Results

Combine results from all tiers:
- Apply tier-specific weights
- Remove duplicates
- Sort by relevance score
- Return top N results

## Success Criteria

The skill succeeds when:

- [ ] All accessible tiers searched
- [ ] Results ranked by relevance
- [ ] Metadata includes source tier

## Failure Handling

If search fails:

1. Return partial results from available tiers
2. Log which tiers were unreachable
3. Include error context in response

## Examples

**Input Context:**
```json
{
  "query": "nginx pod memory issues",
  "user_id": "k8s-monitor",
  "limit": 10
}
```

**Expected Output:**
```json
{
  "results": [
    {
      "content": "Pod nginx-abc crashed due to OOM. Fixed by increasing limits.",
      "tier": "episodic",
      "score": 0.89,
      "timestamp": "2024-01-15T10:30:00Z"
    },
    {
      "content": "Nginx pods require 1Gi memory minimum for production workloads",
      "tier": "semantic",
      "score": 0.85,
      "pattern_type": "resource_requirement"
    }
  ],
  "total_searched": 3,
  "tiers_searched": ["working", "episodic", "semantic"]
}
```
