---
name: context-manager
description: Expert in managing the "Memory" of AI systems. Specializes in Vector Databases (RAG), Short/Long-term memory architectures, and Context Window optimization. Use when designing AI memory systems, optimizing context usage, or implementing conversation history management.
---

# Context Manager

## Purpose
Provides expertise in AI context management, memory architectures, and context window optimization. Handles conversation history, RAG memory systems, and efficient context utilization for LLM applications.

## When to Use
- Designing AI memory and context systems
- Optimizing context window usage
- Implementing conversation history management
- Building long-term memory for AI agents
- Managing RAG retrieval context
- Reducing token usage while preserving quality
- Designing multi-session memory persistence

## Quick Start
**Invoke this skill when:**
- Designing AI memory and context systems
- Optimizing context window usage
- Implementing conversation history management
- Building long-term memory for AI agents
- Reducing token usage while preserving quality

**Do NOT invoke when:**
- Building full RAG pipelines (use ai-engineer)
- Managing vector databases (use data-engineer)
- Coordinating multiple agents (use agent-organizer)
- Training embedding models (use ml-engineer)

## Decision Framework
```
Memory Type Selection:
├── Single conversation → Sliding window context
├── Multi-session user → Persistent memory store
├── Knowledge-heavy → RAG with vector DB
├── Task-oriented → Working memory + tool results
└── Long-running agent
    ├── Episodic memory → Event summaries
    ├── Semantic memory → Knowledge graph
    └── Procedural memory → Learned patterns
```

## Core Workflows

### 1. Context Window Optimization
1. Measure current token usage
2. Identify redundant or verbose content
3. Implement summarization for old messages
4. Prioritize recent and relevant context
5. Use compression techniques
6. Monitor quality vs. token tradeoff

### 2. Conversation Memory Design
1. Define memory retention requirements
2. Choose storage strategy (in-memory, DB)
3. Implement message windowing
4. Add summarization for overflow
5. Design retrieval for relevant history
6. Handle session boundaries

### 3. Long-term Memory Implementation
1. Define memory types needed
2. Design memory storage schema
3. Implement memory write triggers
4. Build retrieval mechanisms
5. Add memory consolidation
6. Implement forgetting policies

## Best Practices
- Summarize old context rather than truncating
- Use semantic search for relevant history retrieval
- Separate system instructions from conversation
- Cache frequently accessed context
- Monitor context utilization metrics
- Implement graceful degradation at limits

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Full history always | Exceeds context limits | Sliding window + summaries |
| No summarization | Lost important context | Summarize before eviction |
| Equal priority | Wastes tokens on irrelevant | Weight recent/relevant higher |
| No persistence | Lost memory across sessions | Store important memories |
| Ignoring token costs | Expensive API calls | Monitor and optimize usage |
