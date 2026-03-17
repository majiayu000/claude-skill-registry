---
name: detect-trends
version: "2.0.0"
description: >
  Detect trending topics across multiple articles by analyzing entity co-occurrence
  and cross-source mentions. Uses memory search to find recent articles and
  LLM analysis to identify emerging trends.
license: MIT
allowed-tools:
  - use_llm                # Strands built-in LLM tool for trend analysis
  - memory/search          # Search for recent articles
  - memory/add             # Store detected trends
  - memory/link            # Link trends to source articles
metadata:
  kubani:
    domain: news
    category: analysis
    requires_approval: false
    confidence: 0.85
    version: "2.0.0"
---

# Detect Trends

Detect trending topics across multiple analyzed articles.

## When to Use

Use this skill when you need to:
- Identify topics mentioned across multiple sources
- Detect emerging trends in AI news
- Track topic momentum over time
- Prioritize topics for digest composition

## Instructions

### Step 1: Search for Recent Analyses

Use `memory/search` to find recent article analyses:
- namespace: "news/analyses"
- query: "recent AI news analysis"
- limit: 100 (or appropriate window)

This returns articles with their extracted entities and categories.

### Step 2: Extract Entity Mentions

From the search results, collect all entities and track:
- Which articles mention each entity
- How many times each entity appears
- Which sources mention each entity

**Entity normalization:**
- Lowercase and strip whitespace
- Handle variations (e.g., "GPT-4" = "GPT4" = "gpt-4")

### Step 3: Calculate Trend Scores

For each entity, calculate a trend score:

**Score formula:**
```
score = mention_count * source_diversity_bonus
source_diversity_bonus = 1.0 + (unique_sources - 1) * 0.2
```

**Thresholds for trend qualification:**
- Minimum 2 mentions
- Minimum 2 different articles

### Step 4: Analyze with LLM

Use `use_llm` to refine trend detection:

**Trend analysis prompt:**
```
Given these entity mention statistics from recent AI news:

{entity_stats}

Identify the top trending topics and classify each as:
- breaking: Rapidly emerging (momentum > 5)
- hot: Actively trending (momentum 2-5)
- rising: Emerging (momentum 0-2)
- established: Stable coverage
- fading: Declining interest

Filter out generic terms like "AI", "technology", "company".

Return as JSON list with: topic, status, mention_count, related_topics
```

### Step 5: Store Trends in Memory

For each identified trend, use `memory/add`:
- type: "trend"
- namespace: "news/trends"
- data: {topic, status, article_count, mention_count, momentum, related_topics}
- metadata: {detected_at, source_articles}

### Step 6: Link Trends to Articles

Use `memory/link` to connect trends to source articles:
- source_id: trend ID
- target_id: article ID (for each contributing article)
- relation_type: "DETECTED_FROM"

### Step 7: Return Results

Return trending topics including:
- Topic name
- Status (breaking, hot, rising, established, fading)
- Mention count
- Source articles
- Related topics

## Tool Usage Guidance

### memory/search
- Search namespace "news/analyses" for recent analyses
- Use broad query to capture all recent content
- Limit appropriately for time window

### use_llm
- Use for trend classification and noise filtering
- Provide entity statistics as context
- Request structured JSON output

### memory/add
- Store trends as type "trend"
- Include momentum and status

### memory/link
- Create DETECTED_FROM relationships
- Links each trend to contributing articles

## Trend Status Definitions

### Breaking (Momentum > 5)
- Rapidly emerging topic
- Mentioned in 10+ articles recently
- Requires immediate attention

### Hot (Momentum 2-5)
- Actively trending topic
- High current interest

### Rising (Momentum 0-2)
- Emerging topic gaining traction
- Growing interest

### Established (Momentum ≈ 0)
- Stable topic with consistent coverage
- Ongoing interest

### Fading (Momentum < -1)
- Topic losing relevance
- Declining interest

## Trend Data Schema

```json
{
  "id": "trend-abc123",
  "topic": "GPT-5",
  "status": "breaking",
  "article_count": 15,
  "mention_count": 23,
  "momentum": 8.5,
  "related_topics": ["OpenAI", "AGI", "language models"],
  "source_articles": ["article-1", "article-2", "..."],
  "detected_at": "2026-01-31T12:00:00Z"
}
```

## Noise Filtering

Filter out generic terms that aren't meaningful trends:
- "AI", "artificial intelligence", "machine learning", "ML"
- "technology", "tech", "company", "research"
- "model", "system", "data", "algorithm"

## Error Handling

- If search returns no results, return empty trends
- If LLM analysis fails, use raw entity counts
- Log but continue if memory operations fail

## Success Criteria

- Trends accurately reflect current news landscape
- Breaking/hot topics are identified correctly
- Noise is filtered out (no generic terms)
- Trends are linked to source articles
