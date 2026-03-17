---
name: analyze-trends-historical
description: >
  Analyze trends over time by comparing current entity mentions against historical
  data from memory. Identifies topics gaining or losing popularity, emerging themes,
  and provides trend velocity and trajectory analysis for weekly trend reports.
license: MIT
compatibility: Requires Memory MCP server for historical data access
metadata:
  kubani:
    domain: news
    category: diagnostic
    version: "1.0.0"
    mcp_servers:
      - memory-mcp-server
    requires_approval: false
    confidence: 0.75
input:
  - name: current_period_articles
    type: list[ProcessedArticle]
    description: Articles from the current analysis period
  - name: lookback_days
    type: int
    default: 14
    description: Number of days to look back for historical comparison
  - name: min_mentions
    type: int
    default: 3
    description: Minimum mentions for an entity to be considered trending
output:
  - name: trends
    type: list[TrendAnalysis]
    description: List of identified trends with velocity and trajectory
  - name: emerging_topics
    type: list[str]
    description: New topics not seen in historical period
  - name: declining_topics
    type: list[str]
    description: Topics significantly less mentioned than before
  - name: summary
    type: str
    description: Narrative summary of trend landscape
---

# Analyze Trends Historical

Compare current news coverage against historical data to identify trend trajectories and produce trend analysis reports.

## When to Use

- Weekly trend report generation
- Identifying emerging vs declining topics
- Understanding shift in AI news landscape
- Keywords: trends, historical, velocity, emerging, declining, analysis

## Prerequisites

- Memory MCP server available with historical article data
- Current period articles have been processed with entities extracted
- At least 7 days of historical data for meaningful comparison

## Input Schema

```json
{
  "current_period_articles": [
    {
      "url": "...",
      "title": "...",
      "entities": ["GPT-4", "OpenAI", "reasoning"],
      "importance_score": 8,
      "published_at": "2026-01-26"
    }
  ],
  "lookback_days": 14,
  "min_mentions": 3
}
```

## Actions

### Step 1: Extract Current Period Entities

From current articles:
1. Collect all entities mentioned
2. Count mentions per entity
3. Calculate average importance when mentioned
4. Note which sources covered each entity

### Step 2: Query Historical Data from Memory

Query memory for articles from lookback period:
```
Query: All articles from last {lookback_days} days
Filter: learning_type = "article"
Fields: entities, importance_score, published_at, source
```

### Step 3: Build Historical Entity Profile

For each entity in historical data:
1. Count total mentions
2. Calculate mention frequency (mentions per day)
3. Track sources that covered it
4. Note average importance

### Step 4: Calculate Trend Velocity

For each entity appearing in current period:
1. Compare current mention rate to historical rate
2. Calculate velocity: `(current_rate - historical_rate) / historical_rate`
3. Classify velocity:
   - **Surging**: velocity > 100% (more than doubled)
   - **Rising**: velocity 25-100%
   - **Stable**: velocity -25% to +25%
   - **Declining**: velocity -25% to -75%
   - **Fading**: velocity < -75%

### Step 5: Identify Emerging Topics

Topics are emerging if:
- At least `min_mentions` in current period
- Zero or minimal mentions (<2) in historical period
- Not a one-time event (appears across multiple sources)

### Step 6: Identify Declining Topics

Topics are declining if:
- Significant mentions in historical period (>5)
- Minimal or no mentions in current period
- Not a concluded news story (e.g., not "X acquisition complete")

### Step 7: Calculate Topic Clusters

Group related entities:
1. Entities that frequently co-occur
2. Entities with similar trajectory patterns
3. Create topic clusters with representative name

### Step 8: Generate Trend Summary

Write a 2-3 paragraph narrative:
1. Top rising trends and what's driving them
2. Notable emerging topics to watch
3. Topics losing steam and possible reasons

### Step 9: Rank and Prioritize

Sort trends by:
1. Absolute velocity (magnitude of change)
2. Current mention count (significance)
3. Importance score average (quality of coverage)

## Output Schema

```json
{
  "trends": [
    {
      "entity": "LoRA fine-tuning",
      "current_mentions": 15,
      "historical_mentions": 5,
      "current_rate": 2.14,
      "historical_rate": 0.36,
      "velocity": 4.94,
      "velocity_class": "surging",
      "avg_importance": 7.5,
      "sources": ["TechCrunch", "VentureBeat", "Hugging Face Blog"],
      "related_entities": ["PEFT", "QLoRA", "adapters"],
      "context": "Growing interest in parameter-efficient fine-tuning methods"
    }
  ],
  "emerging_topics": [
    "Claude 3.5 Opus",
    "mixture-of-agents"
  ],
  "declining_topics": [
    "GPT-3.5",
    "BERT"
  ],
  "summary": "The AI landscape this week shows a strong shift toward efficient fine-tuning methods, with LoRA-related coverage surging 5x compared to the previous two weeks. This aligns with several new library releases making fine-tuning more accessible. Meanwhile, discussion of older architectures like BERT continues to decline as transformer-based LLMs dominate. Emerging topics include Claude 3.5 Opus and mixture-of-agents architectures, both appearing for the first time with multiple high-importance mentions."
}
```

## Success Criteria

- [ ] Historical data queried successfully
- [ ] Velocity calculated correctly for all current entities
- [ ] Emerging topics identified (if any exist)
- [ ] Declining topics identified (if any exist)
- [ ] Summary is coherent and insightful
- [ ] Trends sorted by significance

## Failure Handling

| Error Type | Handling Strategy |
|------------|-------------------|
| Memory query fails | Fall back to current-period-only analysis |
| Insufficient historical data | Note limitation, provide partial analysis |
| No significant trends | Return empty trends with explanation |

## Examples

### Example 1: Normal Trend Analysis

**Input:**
```json
{
  "current_period_articles": [
    {
      "title": "LoRA Fine-tuning Gets Easier",
      "entities": ["LoRA", "fine-tuning", "Hugging Face"],
      "importance_score": 8,
      "published_at": "2026-01-26"
    },
    {
      "title": "New LoRA Library Released",
      "entities": ["LoRA", "PEFT", "transformers"],
      "importance_score": 7,
      "published_at": "2026-01-25"
    },
    {
      "title": "Claude Updates",
      "entities": ["Claude", "Anthropic"],
      "importance_score": 9,
      "published_at": "2026-01-26"
    }
  ],
  "lookback_days": 14,
  "min_mentions": 2
}
```

**Memory Query Result (mocked):**
```json
{
  "historical_articles": [
    {"entities": ["GPT-4", "OpenAI"], "importance_score": 8},
    {"entities": ["LoRA"], "importance_score": 6},
    {"entities": ["Claude", "Anthropic"], "importance_score": 7}
  ]
}
```

**Output:**
```json
{
  "trends": [
    {
      "entity": "LoRA",
      "current_mentions": 2,
      "historical_mentions": 1,
      "velocity": 1.0,
      "velocity_class": "rising",
      "avg_importance": 7.5,
      "sources": ["TechCrunch", "Hugging Face"],
      "related_entities": ["PEFT", "fine-tuning"],
      "context": "Increased coverage of LoRA fine-tuning methods"
    },
    {
      "entity": "Claude",
      "current_mentions": 1,
      "historical_mentions": 1,
      "velocity": 0.0,
      "velocity_class": "stable",
      "avg_importance": 9.0,
      "sources": ["VentureBeat"],
      "related_entities": ["Anthropic"],
      "context": "Steady coverage of Claude developments"
    }
  ],
  "emerging_topics": ["PEFT"],
  "declining_topics": ["GPT-4"],
  "summary": "LoRA and parameter-efficient fine-tuning are seeing increased attention, with mentions doubling compared to the previous two weeks. This trend coincides with new library releases making these techniques more accessible. Claude maintains steady coverage with a high-importance update. GPT-4 discussion has notably declined, possibly as the community's attention shifts to newer developments."
}
```

### Example 2: Emerging Topic Detection

**Input:**
```json
{
  "current_period_articles": [
    {
      "title": "Mixture of Agents: New Architecture",
      "entities": ["mixture-of-agents", "MoA", "ensemble"],
      "importance_score": 9,
      "published_at": "2026-01-26"
    },
    {
      "title": "MoA Shows Promise",
      "entities": ["mixture-of-agents", "benchmarks"],
      "importance_score": 8,
      "published_at": "2026-01-25"
    }
  ],
  "lookback_days": 14,
  "min_mentions": 2
}
```

**Memory Query Result (mocked):**
```json
{
  "historical_articles": []
}
```

**Output:**
```json
{
  "trends": [
    {
      "entity": "mixture-of-agents",
      "current_mentions": 2,
      "historical_mentions": 0,
      "velocity": null,
      "velocity_class": "emerging",
      "avg_importance": 8.5,
      "sources": ["Multiple"],
      "related_entities": ["MoA", "ensemble"],
      "context": "New architectural approach appearing for first time"
    }
  ],
  "emerging_topics": ["mixture-of-agents", "MoA"],
  "declining_topics": [],
  "summary": "This week sees the emergence of 'mixture-of-agents' as a new topic in AI discourse, with multiple high-importance articles covering this architectural approach. With no prior mentions in the past two weeks, this represents a genuinely new development worth watching."
}
```

### Example 3: Insufficient Data

**Input:**
```json
{
  "current_period_articles": [
    {
      "title": "Random AI News",
      "entities": ["AI"],
      "importance_score": 5,
      "published_at": "2026-01-26"
    }
  ],
  "lookback_days": 14,
  "min_mentions": 3
}
```

**Output:**
```json
{
  "trends": [],
  "emerging_topics": [],
  "declining_topics": [],
  "summary": "Insufficient data for meaningful trend analysis. The current period contains too few articles or entities to identify significant trends. Consider increasing the analysis window or lowering the minimum mention threshold."
}
```

## Related Skills

- [analyze-trends](../analyze-trends/SKILL.md) - Basic trend detection without historical comparison
- [search-memory](../../general/memory/search-memory/SKILL.md) - Memory queries for historical data
- [compose-executive-digest](../../action/compose-executive-digest/SKILL.md) - Include trends in digest

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-27 | Initial version |
