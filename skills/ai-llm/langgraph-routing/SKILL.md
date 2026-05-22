---
name: langgraph-routing
description: LangGraph conditional routing patterns. Use when implementing dynamic routing based on state, creating branching workflows, or building retry loops with conditional edges.
context: fork
agent: workflow-architect
version: 1.0.0
author: SkillForge
user-invocable: false
---

# LangGraph Conditional Routing

Route workflow execution dynamically based on state.

## When to Use

- Dynamic branching based on results
- Retry loops with backoff
- Quality gates with pass/fail paths
- Multi-path workflows

## Basic Conditional Edge

```python
from langgraph.graph import StateGraph, END

def route_based_on_quality(state: WorkflowState) -> str:
    """Decide next step based on quality score."""
    if state["quality_score"] >= 0.8:
        return "publish"
    elif state["retry_count"] < 3:
        return "retry"
    else:
        return "manual_review"

workflow.add_conditional_edges(
    "quality_check",
    route_based_on_quality,
    {
        "publish": "publish_node",
        "retry": "generator",
        "manual_review": "review_queue"
    }
)
```

## Quality Gate Pattern

```python
def route_after_quality_gate(state: AnalysisState) -> str:
    """Route based on quality gate result."""
    if state["quality_passed"]:
        return "compress_findings"
    elif state["retry_count"] < 2:
        return "supervisor"  # Retry
    else:
        return END  # Return partial results

workflow.add_conditional_edges(
    "quality_gate",
    route_after_quality_gate,
    {
        "compress_findings": "compress_findings",
        "supervisor": "supervisor",
        END: END
    }
)
```

## Retry Loop Pattern

```python
def llm_call_with_retry(state):
    """Retry failed LLM calls."""
    try:
        result = call_llm(state["input"])
        state["output"] = result
        state["retry_count"] = 0
        return state
    except Exception as e:
        state["retry_count"] += 1
        state["error"] = str(e)
        return state

def should_retry(state) -> str:
    if state.get("output"):
        return "success"
    elif state["retry_count"] < 3:
        return "retry"
    else:
        return "failed"

workflow.add_conditional_edges(
    "llm_call",
    should_retry,
    {
        "success": "next_step",
        "retry": "llm_call",  # Loop back
        "failed": "error_handler"
    }
)
```

## Routing Patterns

```
Sequential:    A → B → C              (simple edges)
Branching:     A → (B or C)           (conditional edges)
Looping:       A → B → A              (retry logic)
Convergence:   (A or B) → C           (multiple inputs)
Diamond:       A → (B, C) → D         (parallel then merge)
```

## State-Based Router

```python
def dynamic_router(state: WorkflowState) -> str:
    """Route based on multiple state conditions."""
    if state.get("error"):
        return "error_handler"
    if not state.get("validated"):
        return "validator"
    if state["confidence"] < 0.5:
        return "enhance"
    return "finalize"
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Max retries | 2-3 for LLM calls |
| Fallback | Always have END fallback |
| Routing function | Keep pure (no side effects) |
| Edge mapping | Explicit mapping for clarity |

## Common Mistakes

- No END fallback (workflow hangs)
- Infinite loops (no max retry)
- Side effects in router (hard to debug)
- Missing edge mappings (runtime error)

## Related Skills

- `langgraph-state` - State design for routing
- `langgraph-supervisor` - Supervisor routing pattern
- `agent-loops` - ReAct loop patterns

## Capability Details

### conditional-routing
**Keywords:** conditional, branch, decision, if-else
**Solves:**
- Route based on conditions
- Implement branching logic
- Create decision nodes

### semantic-routing
**Keywords:** semantic, embedding, similarity, intent
**Solves:**
- Route by semantic similarity
- Intent-based routing
- Embedding-based decisions

### router-template
**Keywords:** template, router, semantic, implementation
**Solves:**
- Semantic router template
- Production router code
- Copy-paste implementation
