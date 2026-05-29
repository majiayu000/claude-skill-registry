---
name: semantic-caching
description: Redis semantic caching for LLM applications. Use when implementing vector similarity caching, optimizing LLM costs through cached responses, or building multi-level cache hierarchies.
context: fork
agent: data-pipeline-engineer
version: 1.0.0
author: SkillForge
user-invocable: false
---

# Semantic Caching

Cache LLM responses by semantic similarity.

## Cache Hierarchy

```
Request → L1 (Exact) → L2 (Semantic) → L3 (Prompt) → L4 (LLM)
           ~1ms         ~10ms           ~2s          ~3s
         100% save    100% save       90% save    Full cost
```

## Redis Semantic Cache

```python
from redisvl.index import SearchIndex
from redisvl.query import VectorQuery

class SemanticCacheService:
    def __init__(self, redis_url: str, threshold: float = 0.92):
        self.client = Redis.from_url(redis_url)
        self.threshold = threshold

    async def get(self, content: str, agent_type: str) -> dict | None:
        embedding = await embed_text(content[:2000])

        query = VectorQuery(
            vector=embedding,
            vector_field_name="embedding",
            filter_expression=f"@agent_type:{{{agent_type}}}",
            num_results=1
        )

        results = self.index.query(query)

        if results:
            distance = float(results[0].get("vector_distance", 1.0))
            if distance <= (1 - self.threshold):
                return json.loads(results[0]["response"])

        return None

    async def set(self, content: str, response: dict, agent_type: str):
        embedding = await embed_text(content[:2000])
        key = f"cache:{agent_type}:{hash_content(content)}"

        self.client.hset(key, mapping={
            "agent_type": agent_type,
            "embedding": embedding,
            "response": json.dumps(response),
            "created_at": time.time(),
        })
        self.client.expire(key, 86400)  # 24h TTL
```

## Similarity Thresholds

| Threshold | Distance | Use Case |
|-----------|----------|----------|
| 0.98-1.00 | 0.00-0.02 | Nearly identical |
| 0.95-0.98 | 0.02-0.05 | Very similar |
| 0.92-0.95 | 0.05-0.08 | Similar (default) |
| 0.85-0.92 | 0.08-0.15 | Moderately similar |

## Multi-Level Lookup

```python
async def get_llm_response(query: str, agent_type: str) -> dict:
    # L1: Exact match (in-memory LRU)
    cache_key = hash_content(query)
    if cache_key in lru_cache:
        return lru_cache[cache_key]

    # L2: Semantic similarity (Redis)
    similar = await semantic_cache.get(query, agent_type)
    if similar:
        lru_cache[cache_key] = similar  # Promote to L1
        return similar

    # L3/L4: LLM call with prompt caching
    response = await llm.generate(query)

    # Store in caches
    await semantic_cache.set(query, response, agent_type)
    lru_cache[cache_key] = response

    return response
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Threshold | Start at 0.92, tune based on hit rate |
| TTL | 24h for production |
| Embedding | text-embedding-3-small (fast) |
| L1 size | 1000-10000 entries |

## Common Mistakes

- Threshold too low (false positives)
- No cache warming (cold start)
- Missing metadata filters
- Not promoting L2 hits to L1

## Related Skills

- `prompt-caching` - Provider-native caching
- `embeddings` - Vector generation
- `cache-cost-tracking` - Langfuse integration

## Capability Details

### redis-vector-cache
**Keywords:** redis, vector, embedding, similarity, cache
**Solves:**
- Cache LLM responses by semantic similarity
- Reduce API costs with smart caching
- Implement multi-level cache hierarchy

### similarity-threshold
**Keywords:** threshold, similarity, tuning, cosine
**Solves:**
- Set appropriate similarity threshold
- Balance hit rate vs accuracy
- Tune cache performance

### skillforge-integration
**Keywords:** skillforge, integration, roi, cost-savings
**Solves:**
- Integrate caching with SkillForge
- Calculate ROI for caching
- Production implementation guide

### cache-service
**Keywords:** service, implementation, template, production
**Solves:**
- Production cache service template
- Complete implementation example
- Redis integration code
