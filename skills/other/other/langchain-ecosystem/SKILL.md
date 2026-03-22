---
name: langchain-ecosystem
description: Complete guide for LangChain, LangGraph, and Deep Agents development. Covers framework selection, agents, tools, RAG, middleware, graphs, persistence, HITL, subagents, and memory. Triggers when code imports langchain/langgraph/deepagents, or user asks about building AI agents, RAG pipelines, stateful graphs, human-in-the-loop workflows, or agent orchestration.
---

# LangChain Ecosystem Router

## Framework Selection

Frameworks are **layered**, not competing:

```
┌─────────────────────────────────────┐
│         Deep Agents                 │  ← planning, memory, skills, files
├─────────────────────────────────────┤
│          LangGraph                  │  ← graphs, loops, state, control flow
├─────────────────────────────────────┤
│         LangChain                   │  ← models, tools, prompts, RAG
└─────────────────────────────────────┘
```

**Decision tree (answer in order):**
1. Needs sub-tasks, file management, persistent memory, or on-demand skills? → **Deep Agents**
2. Needs complex control flow (loops, branching, parallel, human-in-the-loop)? → **LangGraph**
3. Single-purpose agent with fixed tools? → **LangChain** (`create_agent`)
4. Pure model call, chain, or retrieval pipeline? → **LangChain** (LCEL)

| Capability | LangChain | LangGraph | Deep Agents |
|---|-----------|-----------|-------------|
| Control flow | Fixed tool loop | Custom graph | Middleware-managed |
| Planning | ✗ | Manual | ✓ TodoListMiddleware |
| File management | ✗ | Manual | ✓ FilesystemMiddleware |
| Persistent memory | ✗ | With checkpointer | ✓ MemoryMiddleware |
| Subagent delegation | ✗ | Manual | ✓ SubAgentMiddleware |
| Human-in-the-loop | ✗ | Manual interrupt | ✓ HumanInTheLoopMiddleware |

LangChain tools/chains/retrievers work inside LangGraph nodes and Deep Agents tools.
LangGraph compiled graphs can be registered as Deep Agents subagents.

## Quick Start (Most Common Patterns)

**Simple agent:**
```python
from langchain.agents import create_agent
agent = create_agent(model="anthropic:claude-sonnet-4-5", tools=[my_tool])
result = agent.invoke({"messages": [{"role": "user", "content": "Hello"}]})
print(result["messages"][-1].content)
```

**Stateful graph:**
```python
from langgraph.graph import StateGraph, START, END
graph = StateGraph(State).add_node("process", fn).add_edge(START, "process").add_edge("process", END).compile()
```

**Deep Agent:**
```python
from deepagents import create_deep_agent
agent = create_deep_agent(model="claude-sonnet-4-5-20250929", tools=[my_tool], system_prompt="...")
```

## Critical Rules (All Frameworks)

- **Persistence always needs `thread_id`**: `config = {"configurable": {"thread_id": "..."}}`
- **HITL always needs checkpointer**: `MemorySaver()` at minimum
- **Resume after interrupt**: `Command(resume={"decisions": [{"type": "approve"}]})` — never plain dict
- **LangChain 1.0 is LTS** — never start new projects on 0.3
- **Always install `langchain-core` explicitly** — not auto-hoisted in monorepos
- **Use dedicated packages** (e.g., `langchain-chroma`) not `langchain_community`

## Deep-Dive References

### LangChain
| Reference | When to Read |
|-----------|-------------|
| [references/langchain-fundamentals.md](references/langchain-fundamentals.md) | `create_agent`, tool definitions, persistence, TypeScript |
| [references/langchain-dependencies.md](references/langchain-dependencies.md) | Package versions, install commands, import paths, environment setup |
| [references/langchain-middleware.md](references/langchain-middleware.md) | HumanInTheLoopMiddleware, approval/edit/reject, per-tool policies |
| [references/langchain-rag.md](references/langchain-rag.md) | Document loaders, splitters, embeddings, vector stores, MMR search |

### LangGraph
| Reference | When to Read |
|-----------|-------------|
| [references/langgraph-fundamentals.md](references/langgraph-fundamentals.md) | StateGraph, reducers, nodes, edges, Command, Send, streaming |
| [references/langgraph-human-in-the-loop.md](references/langgraph-human-in-the-loop.md) | interrupt(), idempotency, approval workflows, parallel interrupts |
| [references/langgraph-persistence.md](references/langgraph-persistence.md) | Checkpointers, Store, time travel, subgraph scoping |

### Deep Agents
| Reference | When to Read |
|-----------|-------------|
| [references/deep-agents-core.md](references/deep-agents-core.md) | `create_deep_agent`, built-in tools, SKILL.md format, configuration |
| [references/deep-agents-memory.md](references/deep-agents-memory.md) | StateBackend, StoreBackend, FilesystemBackend, CompositeBackend |
| [references/deep-agents-orchestration.md](references/deep-agents-orchestration.md) | Subagents, task delegation, TodoList, HITL approval flow |

### Meta
| Reference | When to Read |
|-----------|-------------|
| [references/framework-selection.md](references/framework-selection.md) | Full decision tree, capability matrix, interoperability details |
