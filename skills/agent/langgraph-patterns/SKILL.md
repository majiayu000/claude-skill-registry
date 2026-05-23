---
name: LangGraph Patterns Expert
description: Build production-grade agentic workflows with LangGraph using graph-based orchestration, state machines, human-in-the-loop, and advanced control flow
version: 1.1.0
last_updated: 2026-01-06
external_version: "LangGraph 1.0 GA, langgraph-sdk 0.3.1"
---

# LangGraph Patterns Expert Skill

## Purpose
Master LangGraph for building production-ready AI agents with fine-grained control, checkpointing, streaming, and complex state management.

## LangGraph 1.0 (GA - October 2025)

LangGraph 1.0 is the first stable major release in the durable agent framework space. After powering agents at Uber, LinkedIn, and Klarna, it's officially production-ready.

## Core Philosophy

**LangGraph is:** An orchestration framework with both declarative and imperative APIs focused on control and durability for production agents.

**Not:** High-level abstractions that hide complexity - instead provides building blocks for full control.

**BREAKING CHANGE (v1.0):** `langgraph.prebuilt` is deprecated. Use `langchain.agents` instead for prebuilt components.

## The Six Production Features

1. **Parallelization** - Run multiple nodes concurrently
2. **Streaming** - Real-time partial outputs
3. **Checkpointing** - Pause/resume execution
4. **Human-in-the-Loop** - Approval/correction workflows
5. **Tracing** - Observability and debugging
6. **Task Queue** - Asynchronous job processing

## Graph-Based Architecture

```python
from langgraph.graph import StateGraph, END

# Define state
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next_action: str

# Create graph
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("analyze", analyze_node)
graph.add_node("execute", execute_node)
graph.add_node("verify", verify_node)

# Define edges
graph.add_edge("analyze", "execute")
graph.add_conditional_edges(
    "execute",
    should_verify,
    {"yes": "verify", "no": END}
)

# Compile
app = graph.compile()
```

## Core Patterns

### Pattern 1: Agent with Tools
```python
from langgraph.prebuilt import create_react_agent

tools = [search_tool, calculator_tool, db_query_tool]

agent = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=MemorySaver()
)

# Run with streaming
for chunk in agent.stream({"messages": [("user", "Analyze sales data")]}):
    print(chunk)
```

### Pattern 2: Multi-Agent Collaboration
```python
# Supervisor coordinates specialist agents
supervisor_graph = StateGraph(SupervisorState)

supervisor_graph.add_node("supervisor", supervisor_node)
supervisor_graph.add_node("researcher", researcher_agent)
supervisor_graph.add_node("analyst", analyst_agent)
supervisor_graph.add_node("writer", writer_agent)

# Supervisor routes to specialists
supervisor_graph.add_conditional_edges(
    "supervisor",
    route_to_agent,
    {
        "research": "researcher",
        "analyze": "analyst",
        "write": "writer",
        "finish": END
    }
)
```

### Pattern 3: Human-in-the-Loop
```python
from langgraph.checkpoint.sqlite import SqliteSaver

checkpointer = SqliteSaver.from_conn_string("checkpoints.db")

graph = StateGraph(State)
graph.add_node("propose_action", propose)
graph.add_node("human_approval", interrupt())  # Pauses here
graph.add_node("execute_action", execute)

app = graph.compile(checkpointer=checkpointer)

# Run until human input needed
result = app.invoke(input, config={"configurable": {"thread_id": "123"}})

# Human reviews, then resume
app.invoke(None, config={"configurable": {"thread_id": "123"}})
```

## State Management

### Short-Term Memory (Session)
```python
class ConversationState(TypedDict):
    messages: Annotated[list, add_messages]
    context: dict

checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)

# Maintains context across turns
config = {"configurable": {"thread_id": "user_123"}}
app.invoke({"messages": [("user", "Hello")]}, config)
app.invoke({"messages": [("user", "What did I just say?")]}, config)
```

### Long-Term Memory (Persistent)
```python
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver.from_conn_string(db_url)

# Persists across sessions
app = graph.compile(checkpointer=checkpointer)
```

## Advanced Control Flow

### Conditional Routing
```python
def route_next(state):
    if state["confidence"] > 0.9:
        return "approve"
    elif state["confidence"] > 0.5:
        return "review"
    else:
        return "reject"

graph.add_conditional_edges(
    "classifier",
    route_next,
    {
        "approve": "auto_approve",
        "review": "human_review",
        "reject": "reject_node"
    }
)
```

### Cycles and Loops
```python
def should_continue(state):
    if state["iterations"] < 3 and not state["success"]:
        return "retry"
    return "finish"

graph.add_conditional_edges(
    "process",
    should_continue,
    {"retry": "process", "finish": END}
)
```

### Parallel Execution
```python
from langgraph.graph import START

# Fan out to parallel nodes
graph.add_edge(START, ["agent_a", "agent_b", "agent_c"])

# Fan in to aggregator
graph.add_edge(["agent_a", "agent_b", "agent_c"], "synthesize")
```

## Production Deployment

### Streaming for UX
```python
async for event in app.astream_events(input, version="v2"):
    if event["event"] == "on_chat_model_stream":
        print(event["data"]["chunk"].content, end="")
```

### Error Handling
```python
def error_handler(state):
    try:
        return execute_risky_operation(state)
    except Exception as e:
        return {"error": str(e), "next": "fallback"}

graph.add_node("risky_op", error_handler)
graph.add_conditional_edges(
    "risky_op",
    lambda s: "fallback" if "error" in s else "success"
)
```

### Monitoring with LangSmith
```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "..."

# All agent actions automatically logged to LangSmith
app.invoke(input)
```

## Best Practices

**DO:**
✅ Use checkpointing for long-running tasks
✅ Stream outputs for better UX
✅ Implement human approval for critical actions
✅ Use conditional edges for complex routing
✅ Leverage parallel execution when possible
✅ Monitor with LangSmith in production

**DON'T:**
❌ Use AgentExecutor (deprecated)
❌ Skip error handling on nodes
❌ Forget to set thread_id for stateful conversations
❌ Over-complicate graphs unnecessarily
❌ Ignore memory management for long conversations

## Integration Examples

### With Claude
```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-4-5")
agent = create_react_agent(llm, tools)
```

### With OpenAI
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")
agent = create_react_agent(llm, tools)
```

### With MCP Servers
```python
from langchain_mcp import MCPTool

github_tool = MCPTool.from_server("github-mcp")
tools = [github_tool, ...]
agent = create_react_agent(llm, tools)
```

## Decision Framework

**Use LangGraph when:**
- Need fine-grained control over agent execution
- Building complex state machines
- Require human-in-the-loop workflows
- Want production-grade durability (checkpointing)
- Need to support multiple LLM providers

**Use alternatives when:**
- Want managed platform (use OpenAI AgentKit)
- Need visual builder (use AgentKit)
- Want simpler API (use Claude SDK directly)
- Building on Oracle Cloud only (use Oracle ADK)

## Resources

- Docs: https://langchain-ai.github.io/langgraph/
- GitHub: https://github.com/langchain-ai/langgraph
- Tutorials: https://langchain-ai.github.io/langgraph/tutorials/

---

*LangGraph is the production-grade choice for complex agentic workflows requiring maximum control.*
