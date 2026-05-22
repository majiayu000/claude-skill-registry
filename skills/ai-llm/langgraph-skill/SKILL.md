---
name: langgraph
category: backend
version: 2.0.0
description: LangGraph workflow patterns for agent orchestration
author: Unite Group
priority: 3
triggers:
  - langgraph
  - workflow
  - graph
  - agent workflow
---

# LangGraph Patterns

## Graph Structure

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END

class GraphState(TypedDict):
    """State passed between nodes."""
    input: str
    output: str | None
    error: str | None
    australian_context: dict | None  # Locale info

def create_graph() -> StateGraph:
    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("process", process_node)
    workflow.add_node("validate", validate_node)
    workflow.add_node("respond", respond_node)

    # Set entry point
    workflow.set_entry_point("process")

    # Add edges
    workflow.add_edge("process", "validate")
    workflow.add_conditional_edges(
        "validate",
        check_validation,
        {
            "valid": "respond",
            "invalid": END,
        }
    )
    workflow.add_edge("respond", END)

    return workflow.compile()
```

## Node Implementation

```python
async def process_node(state: GraphState) -> GraphState:
    """Process the input with Australian context."""
    try:
        # Load Australian context if not present
        if not state.get("australian_context"):
            state["australian_context"] = {
                "locale": "en-AU",
                "currency": "AUD",
                "date_format": "DD/MM/YYYY",
                "timezone": "Australia/Brisbane"
            }

        result = await process_input(state["input"], state["australian_context"])
        state["output"] = result
    except Exception as e:
        state["error"] = str(e)
    return state

def check_validation(state: GraphState) -> str:
    """Determine next step based on state."""
    if state.get("error"):
        return "invalid"
    return "valid"
```

## State Management

### Checkpointing
```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
graph = create_graph()
app = graph.compile(checkpointer=memory)

# Run with thread ID for persistence
result = await app.ainvoke(
    {
        "input": "process this",
        "australian_context": {"locale": "en-AU"}
    },
    config={"configurable": {"thread_id": "user-123"}}
)
```

### State Updates
```python
# Partial state updates
def update_node(state: GraphState) -> dict:
    return {"output": "updated value"}  # Only updates 'output'
```

## Conditional Routing

```python
def router(state: GraphState) -> str:
    """Route to different nodes based on state."""
    input_type = classify_input(state["input"])

    match input_type:
        case "question":
            return "answer_node"
        case "command":
            return "execute_node"
        case _:
            return "fallback_node"

workflow.add_conditional_edges(
    "classify",
    router,
    {
        "answer_node": "answer",
        "execute_node": "execute",
        "fallback_node": "fallback",
    }
)
```

## Parallel Execution

```python
from langgraph.graph import StateGraph
from typing import Annotated
import operator

class ParallelState(TypedDict):
    inputs: list[str]
    results: Annotated[list[str], operator.add]

async def parallel_process(state: ParallelState) -> ParallelState:
    tasks = [process(inp) for inp in state["inputs"]]
    results = await asyncio.gather(*tasks)
    return {"results": results}
```

## Multi-Agent Workflow Pattern

```python
class MultiAgentState(TypedDict):
    """State for multi-agent coordination."""
    task: str
    frontend_result: str | None
    backend_result: str | None
    database_result: str | None
    verification_result: str | None
    australian_context: dict

def create_multi_agent_workflow() -> StateGraph:
    """Orchestrate multiple specialist agents."""
    workflow = StateGraph(MultiAgentState)

    # Specialist agents as nodes
    workflow.add_node("frontend", frontend_agent_node)
    workflow.add_node("backend", backend_agent_node)
    workflow.add_node("database", database_agent_node)
    workflow.add_node("verification", verification_agent_node)

    # Parallel execution of specialists
    workflow.set_entry_point("frontend")
    workflow.add_edge("frontend", "backend")
    workflow.add_edge("backend", "database")
    workflow.add_edge("database", "verification")
    workflow.add_edge("verification", END)

    return workflow.compile()
```

## Error Handling

```python
async def safe_node(state: GraphState) -> GraphState:
    """Node with error handling."""
    try:
        result = await risky_operation(state["input"])
        return {"output": result}
    except ValidationError as e:
        return {"error": f"Validation: {e}"}
    except Exception as e:
        logger.error("Unexpected error", error=str(e), state=state)
        return {"error": "Internal error"}
```

## Australian Context in Workflows

```python
async def australian_context_node(state: GraphState) -> GraphState:
    """Ensure Australian context is applied."""
    if not state.get("australian_context"):
        state["australian_context"] = {
            "locale": "en-AU",
            "currency": "AUD",
            "date_format": "DD/MM/YYYY",
            "phone_format": "04XX XXX XXX",
            "regulations": ["Privacy Act 1988", "WCAG 2.1 AA"]
        }

    # Validate output against Australian standards
    if state.get("output"):
        state["output"] = apply_australian_formatting(
            state["output"],
            state["australian_context"]
        )

    return state
```

## Testing Graphs

```python
@pytest.mark.asyncio
async def test_graph_happy_path():
    graph = create_graph()

    result = await graph.ainvoke({
        "input": "test",
        "australian_context": {"locale": "en-AU"}
    })

    assert result["output"] is not None
    assert result["error"] is None
    assert result["australian_context"]["locale"] == "en-AU"

@pytest.mark.asyncio
async def test_graph_error_handling():
    graph = create_graph()

    result = await graph.ainvoke({"input": "invalid"})

    assert result["error"] is not None

@pytest.mark.asyncio
async def test_multi_agent_coordination():
    """Test orchestrator coordinating multiple agents."""
    workflow = create_multi_agent_workflow()

    result = await workflow.ainvoke({
        "task": "Build new feature",
        "australian_context": {"locale": "en-AU"}
    })

    assert result["frontend_result"] is not None
    assert result["backend_result"] is not None
    assert result["verification_result"] == "PASS"
```

## Verification

- [ ] Graph compiles without errors
- [ ] All nodes are connected
- [ ] Conditional edges cover all cases
- [ ] Error paths handled
- [ ] State types are correct
- [ ] Australian context preserved across nodes
- [ ] Verification node runs independently

## Integration with Agents

This skill is used by:
- `.claude/agents/orchestrator/` - Multi-agent coordination
- `.claude/agents/backend-specialist/` - Agent workflow implementation

See: `backend/fastapi.skill.md`, `verification/verification-first.skill.md`
