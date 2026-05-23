---
name: langgraph-parallel
description: LangGraph parallel execution patterns. Use when implementing fan-out/fan-in workflows, map-reduce over tasks, or running independent agents concurrently.
context: fork
agent: workflow-architect
version: 1.0.0
author: SkillForge
user-invocable: false
---

# LangGraph Parallel Execution

Run independent nodes concurrently for performance.

## When to Use

- Independent agents can run together
- Map-reduce over task lists
- Scatter-gather patterns
- Performance optimization

## Fan-Out/Fan-In Pattern

```python
from langgraph.graph import StateGraph

def fan_out(state):
    """Split work into parallel tasks."""
    state["tasks"] = [{"id": 1}, {"id": 2}, {"id": 3}]
    return state

def worker(state):
    """Process one task."""
    task = state["current_task"]
    result = process(task)
    return {"results": [result]}

def fan_in(state):
    """Combine parallel results."""
    combined = aggregate(state["results"])
    return {"final": combined}

workflow = StateGraph(State)
workflow.add_node("fan_out", fan_out)
workflow.add_node("worker", worker)
workflow.add_node("fan_in", fan_in)

workflow.add_edge("fan_out", "worker")
workflow.add_edge("worker", "fan_in")  # Waits for all workers
```

## Using Send API

```python
from langgraph.constants import Send

def router(state):
    """Route to multiple workers in parallel."""
    return [
        Send("worker", {"task": task})
        for task in state["tasks"]
    ]

workflow.add_conditional_edges("router", router)
```

## Parallel Agent Analysis

```python
from typing import Annotated
from operator import add

class AnalysisState(TypedDict):
    content: str
    findings: Annotated[list[dict], add]  # Accumulates

async def run_parallel_agents(state: AnalysisState):
    """Run multiple agents in parallel."""
    agents = [security_agent, tech_agent, quality_agent]

    # Run all concurrently
    tasks = [agent.analyze(state["content"]) for agent in agents]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter successful results
    findings = [r for r in results if not isinstance(r, Exception)]

    return {"findings": findings}
```

## Map-Reduce Pattern

```python
def map_node(state):
    """Map: Process each item independently."""
    items = state["items"]
    results = []

    for item in items:
        result = process_item(item)
        results.append(result)

    return {"mapped_results": results}

def reduce_node(state):
    """Reduce: Combine all results."""
    results = state["mapped_results"]

    summary = {
        "total": len(results),
        "passed": sum(1 for r in results if r["passed"]),
        "failed": sum(1 for r in results if not r["passed"])
    }

    return {"summary": summary}
```

## Error Isolation

```python
async def parallel_with_isolation(tasks: list):
    """Run parallel tasks, isolate failures."""
    results = await asyncio.gather(*tasks, return_exceptions=True)

    successes = []
    failures = []

    for task, result in zip(tasks, results):
        if isinstance(result, Exception):
            failures.append({"task": task, "error": str(result)})
        else:
            successes.append(result)

    return {"successes": successes, "failures": failures}
```

## Timeout per Branch

```python
import asyncio

async def parallel_with_timeout(agents: list, content: str, timeout: int = 30):
    """Run agents with per-agent timeout."""
    async def run_with_timeout(agent):
        try:
            return await asyncio.wait_for(
                agent.analyze(content),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            return {"agent": agent.name, "error": "timeout"}

    tasks = [run_with_timeout(a) for a in agents]
    return await asyncio.gather(*tasks)
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Max parallel | 5-10 concurrent (avoid overwhelming APIs) |
| Error handling | return_exceptions=True (don't fail all) |
| Timeout | 30-60s per branch |
| Accumulator | Use `Annotated[list, add]` for results |

## Common Mistakes

- No error isolation (one failure kills all)
- No timeout (one slow branch blocks)
- Sequential where parallel possible
- Forgetting to wait for all branches

## Related Skills

- `langgraph-state` - Accumulating state
- `multi-agent-orchestration` - Coordination patterns
- `langgraph-supervisor` - Supervised parallel execution

## Capability Details

### fanout-pattern
**Keywords:** fanout, parallel, concurrent, scatter
**Solves:**
- Run agents in parallel
- Implement fan-out pattern
- Distribute work across workers

### fanin-pattern
**Keywords:** fanin, gather, aggregate, collect
**Solves:**
- Aggregate parallel results
- Implement fan-in pattern
- Collect worker outputs

### parallel-template
**Keywords:** template, implementation, parallel, agent
**Solves:**
- Parallel agent fanout template
- Production-ready code
- Copy-paste implementation
