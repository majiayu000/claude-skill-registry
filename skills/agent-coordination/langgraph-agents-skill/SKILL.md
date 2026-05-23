---
name: "langgraph-agents"
description: "Multi-agent systems with LangGraph - supervisor/swarm patterns, state coordination, multi-provider routing. Use when: build LangGraph agent, multi-agent workflow, supervisor pattern, agent orchestration, StateGraph, coordinate multiple agents, agentic workflow. Uses Claude, DeepSeek, Gemini (no OpenAI)."
---

# LangGraph Multi-Agent Systems

Production-tested patterns for building scalable, cost-optimized multi-agent systems with LangGraph and LangChain.

## When to Use This Skill

**Symptoms:**
- "State not updating correctly between agents"
- "Agents not coordinating properly"
- "LLM costs spiraling out of control"
- "Need to choose between supervisor vs swarm patterns"
- "Unclear how to structure agent state schemas"
- "Agents losing context or repeating work"

**Use Cases:**
- Multi-agent systems with 3+ specialized agents
- Complex workflows requiring orchestration
- Cost-sensitive production deployments
- Self-learning or adaptive agent systems
- Enterprise applications with multiple LLM providers

## Quick Reference: Orchestration Pattern Selection

| Pattern | Use When | Agent Count | Complexity | Reference |
|---------|----------|-------------|------------|-----------|
| **Supervisor** | Clear hierarchy, centralized routing | 3-10 | Low-Medium | `reference/orchestration-patterns.md` |
| **Swarm** | Peer collaboration, dynamic handoffs | 5-15 | Medium | `reference/orchestration-patterns.md` |
| **Master** | Learning systems, complex workflows | 10-30+ | High | `reference/orchestration-patterns.md` |

## Core Patterns

### 1. State Schema (Foundation)
```python
from typing import TypedDict, Annotated, Dict, Any
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

class AgentState(TypedDict, total=False):
    messages: Annotated[list[BaseMessage], add_messages]  # Auto-merge
    agent_type: str
    metadata: Dict[str, Any]
    next_agent: str  # For handoffs
```
**Deep dive:** `reference/state-schemas.md` (reducers, annotations, multi-level state)

### 2. Multi-Provider Configuration (via lang-core)
```python
# Use lang-core for unified provider access (NO OPENAI)
from lang_core.providers import get_llm_for_task, LLMPriority

# Auto-select by priority
llm_cheap = get_llm_for_task(priority=LLMPriority.COST)   # DeepSeek
llm_smart = get_llm_for_task(priority=LLMPriority.QUALITY)  # Claude
llm_fast = get_llm_for_task(priority=LLMPriority.SPEED)   # Cerebras
llm_local = get_llm_for_task(priority=LLMPriority.LOCAL)  # Ollama
```
**Deep dive:** `reference/base-agent-architecture.md`, `reference/cost-optimization.md`
**Infrastructure:** See `lang-core` package for middleware, tracing, caching

### 3. Tool Organization
```python
# Modular, testable tools
def create_agent_with_tools(llm, tools: list):
    return create_react_agent(llm, tools, state_modifier=state_modifier)

# Group by domain
research_tools = [tavily_search, wikipedia]
data_tools = [sql_query, csv_reader]
```
**Deep dive:** `reference/tools-organization.md`

### 4. Supervisor Pattern (Centralized)
```python
members = ["researcher", "writer", "reviewer"]
system_prompt = f"Route to: {members}. Return 'FINISH' when done."
supervisor_chain = prompt | llm.bind_functions([route_function])
```

### 5. Swarm Pattern (Distributed)
```python
# Agents hand off directly
def agent_node(state):
    result = agent.invoke(state)
    return {"messages": [result], "next_agent": determine_next(result)}

workflow.add_conditional_edges("agent_a", route_to_next, {
    "agent_b": "agent_b", "agent_c": "agent_c", "end": END
})
```

## Reference Files (Deep Dives)

- **`reference/state-schemas.md`** - TypedDict, Annotated reducers, multi-level state
- **`reference/base-agent-architecture.md`** - Multi-provider setup, agent templates
- **`reference/tools-organization.md`** - Modular tool design, testing patterns
- **`reference/orchestration-patterns.md`** - Supervisor vs swarm vs master (decision matrix)
- **`reference/context-engineering.md`** - Memory compaction, just-in-time loading
- **`reference/cost-optimization.md`** - Provider routing, caching, token budgets

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| State not updating | Add `Annotated[..., add_messages]` reducer |
| Infinite loops | Add termination condition in conditional edges |
| High costs | Route simple tasks to cheaper models |
| Context loss | Use checkpointers or memory systems |

## lang-core Integration

For production deployments, use **lang-core** for:
- **Middleware**: Cost tracking, budget enforcement, retry, caching, PII safety
- **LangSmith**: Unified tracing with `@traced_agent` decorators
- **Providers**: Auto-selection via `get_llm_for_task(priority=...)`
- **Celery**: Background agent execution with progress tracking
- **Redis**: Distributed locks, rate limiting, event pub/sub

```python
# Example: Agent with full lang-core stack
from lang_core import traced_agent, get_llm_for_task, LLMPriority
from lang_core.middleware import budget_enforcement_middleware, cost_tracking_middleware

@traced_agent("QualificationAgent", tags=["sales"])
async def run_qualification(data):
    llm = get_llm_for_task(priority=LLMPriority.SPEED)
    # ... agent logic
```
