---
name: agentdb-persistent-memory-patterns
description: 'AgentDB Persistent Memory Patterns operates on 3 fundamental principles:'
---

---
name: agentdb-persistent-memory-patterns
description: AgentDB Persistent Memory Patterns operates on 3 fundamental principles:
allowed-tools: Read, Write, Edit, Task, TodoWrite, Glob, Grep
---

# AgentDB Persistent Memory Patterns



---

## LIBRARY-FIRST PROTOCOL (MANDATORY)

**Before writing ANY code, you MUST check:**

### Step 1: Library Catalog
- Location: `.claude/library/catalog.json`
- If match >70%: REUSE or ADAPT

### Step 2: Patterns Guide
- Location: `.claude/docs/inventories/LIBRARY-PATTERNS-GUIDE.md`
- If pattern exists: FOLLOW documented approach

### Step 3: Existing Projects
- Location: `D:\Projects\*`
- If found: EXTRACT and adapt

### Decision Matrix
| Match | Action |
|-------|--------|
| Library >90% | REUSE directly |
| Library 70-90% | ADAPT minimally |
| Pattern exists | FOLLOW pattern |
| In project | EXTRACT |
| No match | BUILD (add to library after) |

---

## Overview

Implement persistent memory patterns for AI agents using AgentDB - session memory, long-term storage, pattern learning, and context management for stateful agents, chat systems, and intelligent assistants.

## SOP Framework: 5-Phase Memory Implementation

### Phase 1: Design Memory Architecture (1-2 hours)
- Define memory schemas (episodic, semantic, procedural)
- Plan storage layers (short-term, working, long-term)
- Design retrieval mechanisms
- Configure persistence strategies

### Phase 2: Implement Storage Layer (2-3 hours)
- Create memory stores in AgentDB
- Implement session management
- Build long-term memory persistence
- Setup memory indexing

### Phase 3: Test Memory Operations (1-2 hours)
- Validate store/retrieve operations
- Test memory consolidation
- Verify pattern recognition
- Benchmark performance

### Phase 4: Optimize Performance (1-2 hours)
- Implement caching layers
- Optimize retrieval queries
- Add memory compression
- Performance tuning

### Phase 5: Document Patterns (1 hour)
- Create usage documentation
- Document memory patterns
- Write integration examples
- Generate API documentation

## Quick Start

```typescript
import { AgentDB, MemoryManager } from 'agentdb-memory';

// Initialize memory system
const memoryDB = new AgentDB({
  name: 'agent-memory',
  dimensions: 768,
  memory: {
    sessionTTL: 3600,
    consolidationInterval: 300,
    maxSessionSize: 1000
  }
});

const memoryManager = new MemoryManager({
  database: memoryDB,
  layers: ['episodic', 'semantic', 'procedural']
});

// Store memory
await memoryManager.store({
  type: 'episodic',
  content: 'User preferred dark theme',
  context: { userId: '123', timestamp: Date.now() }
});

// Retrieve memory
const memories = await memoryManager.retrieve({
  query: 'user preferences',
  type: 'episodic',
  limit: 10
});
```

## Memory Patterns

### Session Memory
```typescript
const session = await memoryManager.createSession('user-123');
await session.store('conversation', messageHistory);
await session.store('preferences', userPrefs);
const context = await session.getContext();
```

### Long-Term Storage
```typescript
await memoryManager.consolidate({
  from: 'working-memory',
  to: 'long-term-memory',
  strategy: 'importance-based'
});
```

### Pattern Learning
```typescript
const patterns = await memoryManager.learnPatterns({
  memory: 'episodic',
  algorithm: 'clustering',
  minSupport: 0.1
});
```

## Success Metrics

- Memory persists across agent restarts
- Retrieval latency < 50ms (p95)
- Pattern recognition accuracy > 85%
- Context maintained with 95% accuracy
- Memory consolidation working

## MCP Requirements

This skill operates using AgentDB's npm package and API only. No additional MCP servers required.

All AgentDB memory operations are performed through:
- npm CLI: `npx agentdb@latest`
- TypeScript/JavaScript API: `import { AgentDB, MemoryManager } from 'agentdb-memory'`

## Additional Resources

- Full documentation: SKILL.md
- Process guide: PROCESS.md
- AgentDB Memory Docs: https://agentdb.dev/docs/memory

## Core Principles

AgentDB Persistent Memory Patterns operates on 3 fundamental principles:

### Principle 1: Memory Layering - Separate Short-Term, Working, and Long-Term Storage

Memory systems mirror human cognition by organizing information across distinct temporal layers. Short-term memory handles immediate context (current conversation), working memory maintains active task state, and long-term memory consolidates important patterns for future retrieval.

In practice:
- Store conversation context in session memory with TTL expiration (1-hour default)
- Use working memory for active agent tasks and intermediate computation results
- Consolidate proven patterns and user preferences to long-term storage using importance-based criteria

### Principle 2: Pattern Learning - Extract Reusable Knowledge from Episodic Memory

Raw episodic memories (specific events) are valuable but incomplete. True intelligence emerges when systems detect patterns across episodes - recurring user preferences, common error scenarios, effective solution strategies - and encode them as semantic knowledge.

In practice:
- Run clustering algorithms on episodic memory to identify recurring patterns (min support threshold: 10%)
- Convert pattern clusters into semantic memory entries with confidence scores
- Use procedural memory to store proven solution workflows that can be replayed in similar contexts

### Principle 3: Performance-First Retrieval - Sub-50ms Latency with HNSW Indexing

Memory systems fail if retrieval is slower than computation. Production AI agents require sub-50ms memory access to maintain real-time responsiveness, necessitating HNSW indexing, quantization, and aggressive caching strategies.

In practice:
- Build HNSW indexes on all memory stores during initialization (M=16, efConstruction=200)
- Apply product quantization for 4x memory reduction without accuracy loss
- Implement LRU caching with 70%+ hit rate for frequently accessed memories

## Common Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Memory Hoarder - Store Everything Forever** | Unbounded storage growth leads to slow retrieval, high costs, and context pollution. Agents retrieve irrelevant memories from 6 months ago. | Implement aggressive TTL policies (1-hour sessions, 30-day working memory, importance-based long-term retention). Use consolidation strategies to compress episodic memories into semantic patterns. |
| **Flat Memory - Single Storage Layer** | All memories treated equally creates retrieval chaos. No distinction between current conversation context and learned patterns from last year. | Use 3-layer architecture: session (ephemeral), working (task-scoped), long-term (consolidated). Apply different retrieval strategies per layer (recency for session, relevance for semantic). |
| **Retrieval Thrashing - Query Every Memory Store on Every Request** | Exhaustive searches across all memory layers cause latency spikes (200ms+ retrieval). Agents spend more time remembering than acting. | Use cascading retrieval: session first (fastest), semantic second (indexed), episodic last (cold storage). Implement query routing based on memory type and recency. Cache hot paths. |

## Conclusion

AgentDB Persistent Memory Patterns transforms stateless AI agents into intelligent systems with genuine memory. By implementing layered storage (session, working, long-term), pattern learning algorithms, and performance-optimized retrieval, you enable agents to accumulate knowledge across interactions rather than starting from zero on every request. The 5-phase SOP ensures systematic implementation from architecture design through performance tuning, with success validated through sub-50ms retrieval latency and 95%+ context accuracy.

This skill is essential when building chat systems requiring conversation history, intelligent assistants that learn user preferences over time, or multi-agent systems coordinating through shared memory. The pattern learning capabilities distinguish AgentDB from basic vector databases - instead of merely storing embeddings, it actively extracts reusable knowledge from experience. When agents can remember what worked before, recall user preferences without re-asking, and apply proven patterns to new problems, they transition from tools to true collaborators.

The performance requirements are non-negotiable for production systems. Users abandon agents that "think" for 500ms between responses. By combining HNSW indexing, quantization, and caching strategies, you achieve both intelligent memory and real-time responsiveness - the foundation for AI systems that feel genuinely aware.