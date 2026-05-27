---
name: cache-cost-tracking
description: LLM cost tracking with Langfuse for cached responses. Use when monitoring cache effectiveness, tracking cost savings, or attributing costs to agents in multi-agent systems.
context: fork
agent: metrics-architect
version: 1.0.0
author: SkillForge
user-invocable: false
---

# Cache Cost Tracking

Monitor LLM costs and cache effectiveness.

## When to Use

- Cost attribution by agent
- Cache hit rate monitoring
- ROI analysis for caching
- Multi-agent cost rollup

## Langfuse Automatic Tracking

```python
from langfuse.decorators import observe, langfuse_context

@observe(as_type="generation")
async def call_llm_with_cache(
    prompt: str,
    agent_type: str,
    analysis_id: UUID
) -> str:
    """LLM call with automatic cost tracking."""

    # Link to parent trace
    langfuse_context.update_current_trace(
        name=f"{agent_type}_generation",
        session_id=str(analysis_id)
    )

    # Check caches
    if cache_key in lru_cache:
        langfuse_context.update_current_observation(
            metadata={"cache_layer": "L1", "cache_hit": True}
        )
        return lru_cache[cache_key]

    similar = await semantic_cache.get(prompt, agent_type)
    if similar:
        langfuse_context.update_current_observation(
            metadata={"cache_layer": "L2", "cache_hit": True}
        )
        return similar

    # LLM call - Langfuse tracks tokens/cost automatically
    response = await llm.generate(prompt)

    langfuse_context.update_current_observation(
        metadata={
            "cache_layer": "L4",
            "cache_hit": False,
            "prompt_cache_hit": response.usage.cache_read_input_tokens > 0
        }
    )

    return response.content
```

## Hierarchical Cost Rollup

```python
class AnalysisWorkflow:
    @observe(as_type="trace")
    async def run_analysis(self, url: str, analysis_id: UUID):
        """Parent trace aggregates child costs.

        Trace Hierarchy:
        run_analysis (trace)
        ├── security_agent (generation)
        ├── tech_agent (generation)
        └── synthesis (generation)
        """
        langfuse_context.update_current_trace(
            name="content_analysis",
            session_id=str(analysis_id),
            tags=["multi-agent"]
        )

        for agent in self.agents:
            await self.run_agent(agent, content, analysis_id)

    @observe(as_type="generation")
    async def run_agent(self, agent, content, analysis_id):
        """Child generation - costs roll up to parent."""
        langfuse_context.update_current_observation(
            name=f"{agent.name}_generation",
            metadata={"agent_type": agent.name}
        )
        return await agent.analyze(content)
```

## Cost Queries

```python
from langfuse import Langfuse

async def get_analysis_costs(analysis_id: UUID) -> dict:
    langfuse = Langfuse()

    traces = langfuse.get_traces(session_id=str(analysis_id), limit=1)

    if traces.data:
        trace = traces.data[0]
        return {
            "total_cost": trace.total_cost,
            "input_tokens": trace.usage.input_tokens,
            "output_tokens": trace.usage.output_tokens,
            "cache_read_tokens": trace.usage.cache_read_input_tokens,
        }

async def get_costs_by_agent() -> list[dict]:
    generations = langfuse.get_generations(
        from_timestamp=datetime.now() - timedelta(days=7),
        limit=1000
    )

    costs = {}
    for gen in generations.data:
        agent = gen.metadata.get("agent_type", "unknown")
        if agent not in costs:
            costs[agent] = {"total": 0, "calls": 0, "cache_hits": 0}

        costs[agent]["total"] += gen.calculated_total_cost or 0
        costs[agent]["calls"] += 1
        if gen.metadata.get("cache_hit"):
            costs[agent]["cache_hits"] += 1

    return list(costs.values())
```

## Cache Effectiveness

```python
cache_hits = 0
cache_misses = 0
cost_saved = 0.0

for gen in generations:
    if gen.metadata.get("cache_hit"):
        cache_hits += 1
        cost_saved += estimate_full_cost(gen)
    else:
        cache_misses += 1

hit_rate = cache_hits / (cache_hits + cache_misses)
print(f"Cache Hit Rate: {hit_rate:.1%}")
print(f"Cost Saved: ${cost_saved:.2f}")
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Trace grouping | session_id = analysis_id |
| Cost attribution | metadata.agent_type |
| Query window | 7-30 days |
| Dashboard | Langfuse web UI |

## Common Mistakes

- Not linking child to parent trace
- Missing metadata for attribution
- Not tracking cache hits separately
- Ignoring prompt cache savings

## Related Skills

- `semantic-caching` - Redis caching
- `prompt-caching` - Provider caching
- `langfuse-observability` - Full observability

## Capability Details

### prompt-caching
**Keywords:** prompt cache, cache prompt, prefix caching, cache breakpoints
**Solves:**
- Reduce token costs with cached prompts
- Configure cache breakpoints
- Implement provider-native caching

### response-caching
**Keywords:** response cache, semantic cache, cache response, LLM cache
**Solves:**
- Cache LLM responses for repeated queries
- Implement semantic similarity caching
- Reduce API calls with cached responses

### cost-calculation
**Keywords:** cost, token cost, calculate cost, pricing, usage cost
**Solves:**
- Calculate token costs by model
- Track input/output token pricing
- Estimate cost before execution

### usage-tracking
**Keywords:** usage, track usage, token usage, API usage, metrics
**Solves:**
- Track LLM API usage over time
- Monitor token consumption
- Generate usage reports

### cache-invalidation
**Keywords:** invalidate, cache invalidation, TTL, expire, refresh
**Solves:**
- Implement cache invalidation strategies
- Configure TTL for cached responses
- Handle stale cache entries
