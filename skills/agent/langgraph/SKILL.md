---
name: langgraph
description: Expert guidance for building stateful, multi-actor AI agents with LangGraph - graphs, nodes, edges, state management, and agent architectures.
allowed-tools: Read, Edit, Bash, Grep, mcp_context7
---

# LangGraph Skill

Use this skill when building stateful, cyclic AI agent workflows with LangGraph.

## 📚 Documentation Lookup (Context7)

Always verify patterns with latest docs:
```
mcp_context7_resolve-library-id(libraryName="langgraph", query="StateGraph conditional edges")
mcp_context7_query-docs(libraryId="/langchain-ai/langgraph", query="checkpointer persistence")
```

## Core Concepts

### 1. State Definition
```python
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    context: str
    iteration: int

# With Pydantic
from pydantic import BaseModel

class State(BaseModel):
    messages: list = []
    current_step: str = "start"
```

### 2. Basic Graph Structure
```python
from langgraph.graph import StateGraph, START, END

# Define the graph
workflow = StateGraph(AgentState)

# Add nodes (functions that transform state)
def agent_node(state: AgentState) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def tool_node(state: AgentState) -> dict:
    # Execute tools based on last message
    return {"messages": [tool_result]}

workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

# Add edges
workflow.add_edge(START, "agent")
workflow.add_edge("tools", "agent")

# Conditional edge
def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow.add_conditional_edges("agent", should_continue)

# Compile
app = workflow.compile()
```

### 3. Prebuilt Components
```python
from langgraph.prebuilt import create_react_agent, ToolNode

# Quick ReAct agent
tools = [search_tool, calculator_tool]
agent = create_react_agent(llm, tools)

# Tool execution node
tool_node = ToolNode(tools)
```

### 4. Checkpointing (Memory/Persistence)
```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver

# In-memory (for development)
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# SQLite (for persistence)
with SqliteSaver.from_conn_string(":memory:") as saver:
    app = workflow.compile(checkpointer=saver)

# Invoke with thread_id for conversation continuity
config = {"configurable": {"thread_id": "user-123"}}
result = app.invoke({"messages": [HumanMessage("Hi")]}, config)

# Continue conversation
result = app.invoke({"messages": [HumanMessage("Follow up")]}, config)
```

### 5. Human-in-the-Loop
```python
from langgraph.graph import StateGraph

# Add interrupt before sensitive operations
app = workflow.compile(
    checkpointer=memory,
    interrupt_before=["sensitive_action"]  # Pause here
)

# Resume after human approval
result = app.invoke(None, config)  # Continues from checkpoint
```

### 6. Subgraphs
```python
# Define inner graph
inner_workflow = StateGraph(InnerState)
inner_workflow.add_node("process", process_node)
inner_workflow.add_edge(START, "process")
inner_workflow.add_edge("process", END)
inner_graph = inner_workflow.compile()

# Use as node in outer graph
outer_workflow = StateGraph(OuterState)
outer_workflow.add_node("subgraph", inner_graph)
```

### 7. Streaming
```python
# Stream node outputs
for event in app.stream({"messages": [HumanMessage("Hello")]}):
    for node_name, output in event.items():
        print(f"{node_name}: {output}")

# Stream tokens from LLM
async for event in app.astream_events(input, version="v2"):
    if event["event"] == "on_chat_model_stream":
        print(event["data"]["chunk"].content, end="")
```

## Agent Architectures

### ReAct Agent
```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model=llm,
    tools=tools,
    state_modifier="You are a helpful assistant."  # System prompt
)
```

### Plan-and-Execute
```python
class PlanExecuteState(TypedDict):
    input: str
    plan: list[str]
    past_steps: list[tuple[str, str]]
    response: str

def planner(state):
    # Generate plan
    plan = plan_chain.invoke({"input": state["input"]})
    return {"plan": plan.steps}

def executor(state):
    # Execute current step
    task = state["plan"][0]
    result = execute_chain.invoke({"task": task})
    return {
        "past_steps": [(task, result)],
        "plan": state["plan"][1:]
    }

def should_end(state):
    return END if not state["plan"] else "executor"

workflow = StateGraph(PlanExecuteState)
workflow.add_node("planner", planner)
workflow.add_node("executor", executor)
workflow.add_edge(START, "planner")
workflow.add_conditional_edges("planner", should_end)
workflow.add_conditional_edges("executor", should_end)
```

### Multi-Agent Supervisor
```python
from langgraph.prebuilt import create_react_agent

# Create specialized agents
researcher = create_react_agent(llm, [search_tool])
coder = create_react_agent(llm, [code_tool])

class SupervisorState(TypedDict):
    messages: Annotated[list, add_messages]
    next: str

def supervisor(state):
    # Decide which agent to call
    decision = router_chain.invoke(state["messages"])
    return {"next": decision.next_agent}

def call_researcher(state):
    result = researcher.invoke({"messages": state["messages"]})
    return {"messages": result["messages"]}

def call_coder(state):
    result = coder.invoke({"messages": state["messages"]})
    return {"messages": result["messages"]}

workflow = StateGraph(SupervisorState)
workflow.add_node("supervisor", supervisor)
workflow.add_node("researcher", call_researcher)
workflow.add_node("coder", call_coder)

workflow.add_edge(START, "supervisor")
workflow.add_conditional_edges("supervisor", lambda s: s["next"])
workflow.add_edge("researcher", "supervisor")
workflow.add_edge("coder", "supervisor")
```

## Best Practices

1. **State Design** - Keep state minimal; use `add_messages` reducer for message accumulation
2. **Node Functions** - Return partial state updates, not full state
3. **Conditional Edges** - Use for dynamic routing based on state
4. **Checkpointing** - Always use for production to enable persistence
5. **Streaming** - Use `astream_events` for real-time UX
6. **Error Handling** - Add retry logic in nodes or use fallback edges
7. **Testing** - Test nodes individually before composing

## Common Patterns

### State Reducer
```python
from operator import add
from typing import Annotated

class State(TypedDict):
    items: Annotated[list, add]  # Appends to list
    messages: Annotated[list, add_messages]  # Smart message merging
```

### Parallel Branches
```python
workflow.add_node("branch_a", node_a)
workflow.add_node("branch_b", node_b)
workflow.add_edge(START, "branch_a")
workflow.add_edge(START, "branch_b")  # Both run in parallel
workflow.add_edge("branch_a", "join")
workflow.add_edge("branch_b", "join")
```

### Dynamic Tool Selection
```python
def route_to_tool(state):
    tool_call = state["messages"][-1].tool_calls[0]
    return tool_call["name"]

workflow.add_conditional_edges("agent", route_to_tool, {
    "search": "search_node",
    "calculate": "calc_node"
})
```

## Installation
```bash
pip install langgraph
pip install langgraph-checkpoint-sqlite  # For SQLite persistence
```
