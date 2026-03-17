---
skill_id: when-building-semantic-search-use-agentdb-vector-search
name: AgentDB Semantic Vector Search
version: 1.0.0
category: agentdb
subcategory: semantic-search
trigger_pattern: "when-building-semantic-search"
agents:
  - ml-developer
  - backend-dev
  - tester
complexity: intermediate
estimated_duration: 6-8 hours
prerequisites:
  - AgentDB basics
  - Embedding models knowledge
  - REST API development
outputs:
  - Semantic search engine
  - Document retrieval system
  - RAG-ready infrastructure
  - Query API endpoints
validation_criteria:
  - Search returns relevant results
  - Retrieval accuracy > 90%
  - Query latency < 100ms
  - API functional and documented
evidence_based_techniques:
  - Relevance evaluation
  - Precision/recall metrics
  - User feedback testing
metadata:
  author: claude-flow
  created: 2025-10-30
  tags:
    - agentdb
    - semantic-search
    - rag
    - vector-search
    - embeddings
---

# AgentDB Semantic Vector Search

## Overview

Implement semantic vector search with AgentDB for intelligent document retrieval, similarity matching, and context-aware querying. Build RAG systems, semantic search engines, and knowledge bases.

## SOP Framework: 5-Phase Semantic Search

### Phase 1: Setup Vector Database (1-2 hours)
- Initialize AgentDB
- Configure embedding model
- Setup database schema

### Phase 2: Embed Documents (1-2 hours)
- Process document corpus
- Generate embeddings
- Store vectors with metadata

### Phase 3: Build Search Index (1-2 hours)
- Create HNSW index
- Optimize search parameters
- Test retrieval accuracy

### Phase 4: Implement Query Interface (1-2 hours)
- Create REST API endpoints
- Add filtering and ranking
- Implement hybrid search

### Phase 5: Refine and Optimize (1-2 hours)
- Improve relevance
- Add re-ranking
- Performance tuning

## Quick Start

```typescript
import { AgentDB, EmbeddingModel } from 'agentdb-vector-search';

// Initialize
const db = new AgentDB({ name: 'semantic-search', dimensions: 1536 });
const embedder = new EmbeddingModel('openai/ada-002');

// Embed documents
for (const doc of documents) {
  const embedding = await embedder.embed(doc.text);
  await db.insert({
    id: doc.id,
    vector: embedding,
    metadata: { title: doc.title, content: doc.text }
  });
}

// Search
const query = 'machine learning tutorials';
const queryEmbedding = await embedder.embed(query);
const results = await db.search({
  vector: queryEmbedding,
  topK: 10,
  filter: { category: 'tech' }
});
```

## Features

- **Semantic Search**: Meaning-based retrieval
- **Hybrid Search**: Vector + keyword search
- **Filtering**: Metadata-based filtering
- **Re-ranking**: Improve result relevance
- **RAG Integration**: Context for LLMs

## Success Metrics

- Retrieval accuracy > 90%
- Query latency < 100ms
- Relevant results in top-10: > 95%
- API uptime > 99.9%

## Additional Resources

- Full docs: SKILL.md
- AgentDB Vector Search: https://agentdb.dev/docs/vector-search
