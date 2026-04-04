---
name: multi-agent
description: Build multi-agent systems - orchestration, coordination, workflows, and distributed architectures
sasmp_version: "1.3.0"
bonded_agent: 05-multi-agent
bond_type: PRIMARY_BOND
version: "2.0.0"
---

# Multi-Agent Systems

Build coordinated multi-agent systems for complex tasks.

## When to Use This Skill

Invoke this skill when:
- Tasks require multiple specialized agents
- Building orchestrator-worker patterns
- Implementing agent workflows
- Coordinating parallel execution

## Parameter Schema

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `task` | string | Yes | Multi-agent goal | - |
| `architecture` | enum | No | `orchestrator-worker`, `hierarchical`, `peer-to-peer` | `orchestrator-worker` |
| `framework` | enum | No | `langgraph`, `autogen`, `crewai` | `langgraph` |

## Quick Start

```python
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import create_react_agent

# Create specialized agents
researcher = create_react_agent(llm, [web_search])
coder = create_react_agent(llm, [execute_code])

# Build graph
graph = StateGraph(MessagesState)
graph.add_node("researcher", researcher)
graph.add_node("coder", coder)
graph.add_conditional_edges("coordinator", router)
```

## Architecture Patterns

### Orchestrator-Worker
```
Orchestrator (Opus)
    ├── Researcher (Sonnet)
    ├── Analyst (Sonnet)
    └── Writer (Haiku)
```

### Hierarchical
```
Manager (Opus)
    ├── Research Lead (Sonnet)
    │   ├── Web Researcher (Haiku)
    │   └── Doc Analyst (Haiku)
    └── Engineering Lead (Sonnet)
        ├── Frontend Dev (Haiku)
        └── Backend Dev (Haiku)
```

## Model Allocation

| Agent Type | Model | Rationale |
|------------|-------|-----------|
| Orchestrator | Opus | Complex planning |
| Specialist | Sonnet | Reasoning |
| Worker | Haiku | Simple tasks |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Agents not coordinating | Check message bus |
| Deadlock | Add timeout, detect cycles |
| Inconsistent results | Synchronize state |
| High costs | Use cheaper models for workers |

## Best Practices

- One job per agent (single responsibility)
- Orchestrator handles planning only
- Use checkpointing for long workflows
- Implement circuit breakers per agent

## Related Skills

- `ai-agent-basics` - Single agents
- `agent-memory` - Shared state
- `tool-calling` - Per-agent tools

## References

- [LangGraph Multi-Agent](https://langchain-ai.github.io/langgraph/concepts/multi_agent/)
- [Anthropic Multi-Agent](https://www.anthropic.com/engineering/multi-agent-research-system)
