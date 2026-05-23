---
name: context-retrieval
description: Retrieve relevant episodic context from memory for informed decision-making. Use when you need past episodes, patterns, or solutions to similar tasks.
---

# Context Retrieval

Retrieve relevant episodic context from memory for informed decision-making.

## Retrieval Methods

### Semantic Search (Preferred)
When embeddings available:
```rust
let context = memory
    .retrieve_relevant_context(
        "implement async batch updates",
        task_context,
        limit: 5
    )
    .await?;
```

**Advantages**: Finds semantically similar tasks, captures intent

### Keyword Search (Fallback)
```rust
// SQL index-based search
SELECT * FROM episodes
WHERE task_type = ? AND tags LIKE ?
ORDER BY timestamp DESC
LIMIT ?;
```

**Advantages**: Fast, no embedding computation, deterministic

## Retrieval Strategy

1. Parse query (key terms, domain, task type)
2. Check embedding availability
3. Query cache (redb) first, fall back to Turso
4. Rank by relevance or recency
5. Filter and limit results
6. Format context structure

## Context Filtering

```rust
// By domain
TaskContext { domain: "storage".to_string(), .. }

// By task type
task_type_filter: Some("implementation")

// By recency (last 30 days)
since: Some(now - Duration::days(30))

// By success only
verdict: Some(Verdict::Success)
```

## Response Format

```rust
pub struct RetrievedContext {
    pub episodes: Vec<EpisodeSummary>,
    pub patterns: Vec<Pattern>,
    pub heuristics: Vec<Heuristic>,
    pub relevance_scores: Vec<f32>,
}

pub struct EpisodeSummary {
    pub id: String,
    pub task_description: String,
    pub verdict: Verdict,
    pub key_steps: Vec<String>,
    pub reflection: String,
    pub relevance: f32,
}
```

## Usage Examples

```rust
// Find similar implementation tasks
let retrieved = memory
    .retrieve_relevant_context(query, context, 10)
    .await?;

// Find common tool sequences
let patterns = memory
    .get_patterns_by_type("ToolSequence")
    .filter(|p| p.success_rate > 0.8)
    .await?;

// Find error resolutions
let solutions = memory
    .retrieve_error_resolutions("borrow checker error", 5)
    .await?;
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Low recall | Check embeddings, expand tags, increase limit |
| Slow retrieval | Check cache, verify indexes, reduce result set |
| Poor relevance | Use semantic search, improve query, filter by domain |
