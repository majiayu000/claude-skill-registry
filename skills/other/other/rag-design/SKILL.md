---
name: rag-design
description: Production-grade RAG (Retrieval-Augmented Generation) system design patterns from OpenClaw. Use when implementing semantic search, vector retrieval, memory systems, or knowledge bases. Covers hybrid search (vector + keyword), embedding providers, MMR re-ranking, temporal decay, and enterprise features.
---

# RAG Design Patterns

Production-grade RAG implementation patterns extracted from OpenClaw's memory system.

## Core Architecture

### Hybrid Search Strategy

Combine vector and keyword search for optimal retrieval:

```typescript
// Parallel execution
const [vectorResults, keywordResults] = await Promise.all([
  vectorSearch(query, { limit: 50 }),
  keywordSearch(query, { limit: 50 })
]);

// Weighted merge
const merged = mergeResults({
  vector: vectorResults,
  keyword: keywordResults,
  vectorWeight: 0.7,  // Semantic relevance
  textWeight: 0.3     // Keyword matching
});
```

### Storage Layer

Use SQLite with extensions for production deployments:

- **Vector table**: `sqlite-vec` extension for embeddings
- **FTS table**: SQLite FTS5 for full-text search
- **Cache table**: Store computed embeddings to avoid recomputation

```sql
-- Vector storage
CREATE VIRTUAL TABLE chunks_vec USING vec0(
  embedding FLOAT[768]
);

-- Full-text search
CREATE VIRTUAL TABLE chunks_fts USING fts5(
  content, path, source
);

-- Embedding cache
CREATE TABLE embedding_cache (
  content_hash TEXT PRIMARY KEY,
  embedding BLOB,
  provider TEXT,
  model TEXT
);
```

## Embedding Providers

Support multiple providers with fallback:

```typescript
const providers = {
  openai: 'text-embedding-3-small',
  gemini: 'text-embedding-004',
  voyage: 'voyage-2',
  mistral: 'mistral-embed',
  local: 'node-llama-cpp'
};

// Auto-fallback on failure
async function createProvider(config) {
  try {
    return await initPrimary(config.provider);
  } catch (err) {
    if (config.fallback) {
      return await initFallback(config.fallback);
    }
    throw err;
  }
}
```

## Advanced Retrieval

### MMR Re-ranking

Balance relevance with diversity using Maximal Marginal Relevance:

```typescript
// Iteratively select diverse results
function applyMMR(results, lambda = 0.7) {
  const selected = [];
  const remaining = [...results];

  while (selected.length < maxResults && remaining.length > 0) {
    let bestIdx = 0;
    let bestScore = -Infinity;

    for (let i = 0; i < remaining.length; i++) {
      const relevance = remaining[i].score;
      const maxSim = maxSimilarity(remaining[i], selected);
      const mmrScore = lambda * relevance - (1 - lambda) * maxSim;

      if (mmrScore > bestScore) {
        bestScore = mmrScore;
        bestIdx = i;
      }
    }

    selected.push(remaining[bestIdx]);
    remaining.splice(bestIdx, 1);
  }

  return selected;
}
```

### Temporal Decay

Boost recent results with time-based scoring:

```typescript
function applyTemporalDecay(results, halfLifeDays = 30) {
  const now = Date.now();
  const halfLifeMs = halfLifeDays * 24 * 60 * 60 * 1000;

  return results.map(r => ({
    ...r,
    score: r.score * Math.exp(-Math.log(2) *
      (now - r.timestamp) / halfLifeMs)
  }));
}
```

## Query Enhancement

### Query Expansion

Extract keywords to improve recall:

```typescript
function expandQuery(query) {
  // Extract meaningful terms
  const keywords = query
    .match(/[\p{L}\p{N}_]+/gu)
    ?.filter(t => t.length > 2) ?? [];

  // Build FTS query
  return keywords
    .map(k => `"${k}"`)
    .join(' AND ');
}
```

## Enterprise Features

### Batch Processing

Reduce API costs with batch embedding:

```typescript
async function batchEmbed(texts, provider) {
  const batches = chunk(texts, provider.batchSize);
  const results = [];

  for (const batch of batches) {
    const embeddings = await provider.embedBatch(batch);
    results.push(...embeddings);

    // Rate limiting
    await sleep(provider.delayMs);
  }

  return results;
}
```

### Incremental Indexing

Watch files and update index on changes:

```typescript
const watcher = chokidar.watch('memory/**/*.md', {
  ignoreInitial: true
});

watcher.on('change', debounce(async (path) => {
  await reindexFile(path);
}, 1000));
```

### Error Recovery

Handle transient failures gracefully:

```typescript
async function embedWithRetry(text, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await embed(text);
    } catch (err) {
      if (i === maxRetries - 1) throw err;
      await sleep(Math.pow(2, i) * 1000);
    }
  }
}
```

## Agent Integration

Expose as tools for AI agents:

```typescript
const tools = [
  {
    name: 'memory_search',
    description: 'Semantic search over indexed documents',
    parameters: {
      query: 'string',
      maxResults: 'number?',
      minScore: 'number?'
    },
    execute: async (params) => {
      return await searchManager.search(params.query, {
        maxResults: params.maxResults ?? 10,
        minScore: params.minScore ?? 0.7
      });
    }
  }
];
```

## Performance Optimization

- **Cache embeddings**: Hash content and reuse computed vectors
- **Parallel search**: Run vector and keyword search concurrently
- **Limit context**: Return snippets, not full documents
- **Debounce updates**: Batch file changes before reindexing

## Reference Files

- [Architecture Details](references/architecture.md) - System design and data flow
- [Implementation Guide](references/implementation.md) - TypeScript step-by-step setup
- [Python Implementation](references/python-implementation.md) - Python version with LangChain/LlamaIndex
- [Configuration](references/configuration.md) - Tuning parameters
