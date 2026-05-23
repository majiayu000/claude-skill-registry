---
name: memory-usage
description: "Always-on MemoryManager + LearningPolicy workflow. Use when storing/retrieving memories, emitting retrieval signals, running consolidation/pruning, or when a session should default to the Atlas memory system (MemoryManager, MemoryConsolidator, LearningPolicy). Triggers: memory add/retrieve, consolidation, pruning, semantic search, or 'use the memory system by default.'"
---

# Memory Usage

## Overview

Use this skill to enforce the Atlas memory pipeline: **MemoryManager + LearningPolicy + MemoryConsolidator**. This makes memory storage/retrieval consistent, emits learning signals, and keeps the index healthy via consolidation + pruning.

## Workflow (Always-on)

### 1) Initialize policy + memory system
```ts
import { MemoryManager } from '../system/memory/manager';
import { LearningPolicy } from '../system/learning/ml-policy';

const policy = new LearningPolicy({});
await policy.initialize();

const memory = new MemoryManager({}, policy);
await memory.initialize();
```

### 2) Add memory (always with metadata)
```ts
await memory.add({
  type: 'fact',
  content: 'The capital of France is Paris',
  metadata: {
    source: 'session',
    sessionId: 'current',
    author: 'Atlas',
    provenance: { origin: 'user', confidence: 0.9 },
    tags: ['geo']
  }
});
```

### 3) Retrieve memory (signals are emitted)
```ts
const results = await memory.retrieve({ query: 'France capital', limit: 3 });
// memory_retrieved signal is recorded automatically
```

### 4) Consolidate + prune (daily/weekly)
```ts
await memory.consolidate({ window: 'last_24_hours' });
await memory.prune({
  age: 'older_than_90_days',
  threshold: 0.3,
  minRetrievalCount: 1
});
```

## Required Behaviors
- **Always initialize LearningPolicy** before MemoryManager.
- **Always use MemoryManager** for add/retrieve (no bypassing the index).
- **Do not** store memory without metadata (source/sessionId/provenance/tags).
- **Consolidate** regularly and **prune** low-value entries.

## Quick sanity checks
- Vector index size increases after add.
- Retrieval returns results with `score` and `metadata.similarity`.
- `signals.json` contains `memory_retrieved` events after retrieval.
