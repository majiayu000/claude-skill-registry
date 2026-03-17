---
name: ai-llm-skills-guide
description: Guide for AI Agents and LLM development skills including RAG, multi-agent systems, prompt engineering, memory systems, and context engineering.
---

# AI Agents & LLM Development Skills

## Scope

Use this skill when:

- Finding or adding AI/LLM related skills
- Understanding agent architecture patterns
- Working with RAG, embeddings, or vector databases
- Implementing multi-agent systems

## Key Skill Categories

### Agent Frameworks

| Framework | Description |
|-----------|-------------|
| LangGraph | Stateful, multi-actor AI applications |
| CrewAI | Role-based multi-agent orchestration |
| AutoGen | Microsoft's multi-agent framework |

### RAG (Retrieval-Augmented Generation)

| Component | Skills |
|-----------|--------|
| Embeddings | Text embedding models, chunking strategies |
| Vector DBs | Pinecone, Weaviate, Chroma, Qdrant |
| Retrieval | Hybrid search, reranking, context optimization |

### Observability & Tracing

| Tool | Purpose |
|------|---------|
| Langfuse | Open-source LLM observability |
| LangSmith | LangChain tracing and debugging |
| Weights & Biases | ML experiment tracking |

### Memory Systems

| Type | Description |
|------|-------------|
| Short-term | Conversation buffer, sliding window |
| Long-term | Vector store persistence, entity memory |
| Episodic | Experience-based memory recall |

## Context Engineering Skills

### Core Concepts

- **Context fundamentals**: What context is and why it matters
- **Context degradation**: Lost-in-middle, poisoning, distraction patterns
- **Context compression**: Summarization, trimming strategies
- **Context optimization**: Caching, masking, compaction

### Multi-Agent Patterns

- Orchestrator pattern
- Peer-to-peer collaboration
- Hierarchical delegation
- Tool-using agents

## Where to Add in README

- **Agent frameworks**: `AI Agents & LLM Development`
- **RAG tools**: `AI Agents & LLM Development` or `Data & Analysis`
- **Observability**: `AI Agents & LLM Development`
- **Context engineering**: `Context Engineering`

## Key Repositories

```
sickn33/antigravity-awesome-skills/skills/
├── langgraph/
├── crewai/
├── langfuse/
├── rag-engineer/
├── prompt-engineer/
├── voice-agents/
├── agent-memory-systems/
└── autonomous-agents/

muratcankoylan/Agent-Skills-for-Context-Engineering/skills/
├── context-fundamentals/
├── context-degradation/
├── context-compression/
├── multi-agent-patterns/
└── memory-systems/
```

## Best Practices

1. **Modular design**: Separate retrieval, generation, and orchestration
2. **Evaluation**: Include benchmarks and test cases
3. **Cost awareness**: Document token usage and API costs
4. **Fallback strategies**: Handle API failures gracefully
5. **Streaming**: Support streaming responses where possible

## Full Resource List

For more detailed skill resources, complete link lists, or the latest information, use WebFetch to retrieve the full README.md:

```
https://raw.githubusercontent.com/gmh5225/awesome-skills/refs/heads/main/README.md
```

The README.md contains the complete categorized resource list with all links.
