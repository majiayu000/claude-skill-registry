---
name: langgraph-supervisor
description: LangGraph supervisor-worker pattern. Use when building central coordinator agents that route to specialized workers, implementing round-robin or priority-based agent dispatch.
context: fork
agent: workflow-architect
version: 1.0.0
author: SkillForge
user-invocable: false
---

# LangGraph Supervisor Pattern

Coordinate multiple specialized agents with a central supervisor.

## When to Use

- Multiple specialist agents
- Central coordination needed
- Dynamic agent routing
- Progress tracking across agents

## Basic Supervisor

```python
from langgraph.graph import StateGraph, END

def supervisor(state: WorkflowState) -> WorkflowState:
    """Route to next worker based on state."""
    if state["needs_analysis"]:
        state["next"] = "analyzer"
    elif state["needs_validation"]:
        state["next"] = "validator"
    else:
        state["next"] = END
    return state

def analyzer(state: WorkflowState) -> WorkflowState:
    """Specialized analysis worker."""
    result = analyze(state["input"])
    state["results"].append(result)
    return state

# Build graph
workflow = StateGraph(WorkflowState)
workflow.add_node("supervisor", supervisor)
workflow.add_node("analyzer", analyzer)
workflow.add_node("validator", validator)

# Supervisor routes dynamically
workflow.add_conditional_edges(
    "supervisor",
    lambda s: s["next"],
    {
        "analyzer": "analyzer",
        "validator": "validator",
        END: END
    }
)

# Workers return to supervisor
workflow.add_edge("analyzer", "supervisor")
workflow.add_edge("validator", "supervisor")

workflow.set_entry_point("supervisor")
app = workflow.compile()
```

## Round-Robin Supervisor

```python
ALL_AGENTS = ["security", "tech", "implementation", "tutorial"]

def supervisor_node(state: AnalysisState) -> AnalysisState:
    """Route to next available agent."""
    completed = set(state["agents_completed"])
    available = [a for a in ALL_AGENTS if a not in completed]

    if not available:
        state["next"] = "quality_gate"
    else:
        state["next"] = available[0]

    return state

# Register all agent nodes
for agent_name in ALL_AGENTS:
    workflow.add_node(agent_name, create_agent_node(agent_name))
    workflow.add_edge(agent_name, "supervisor")
```

## Priority-Based Routing

```python
AGENT_PRIORITIES = {
    "security": 1,    # Run first
    "tech": 2,
    "implementation": 3,
    "tutorial": 4     # Run last
}

def priority_supervisor(state: WorkflowState) -> WorkflowState:
    """Route by priority, not round-robin."""
    completed = set(state["agents_completed"])
    available = [a for a in AGENT_PRIORITIES if a not in completed]

    if not available:
        state["next"] = "finalize"
    else:
        # Sort by priority
        next_agent = min(available, key=lambda a: AGENT_PRIORITIES[a])
        state["next"] = next_agent

    return state
```

## LLM-Based Supervisor (2026 Best Practice)

```python
from pydantic import BaseModel, Field
from typing import Literal

# Define structured output schema
class SupervisorDecision(BaseModel):
    """Validated supervisor routing decision."""
    next_agent: Literal["security", "tech", "implementation", "tutorial", "DONE"]
    reasoning: str = Field(description="Brief explanation for routing decision")

async def llm_supervisor(state: WorkflowState) -> WorkflowState:
    """Use LLM with structured output for reliable routing."""
    available = [a for a in AGENTS if a not in state["agents_completed"]]

    # Use structured output (2026 best practice)
    decision = await llm.with_structured_output(SupervisorDecision).ainvoke(
        f"""Task: {state['input']}

Completed: {state['agents_completed']}
Available: {available}

Select the next agent or 'DONE' if all work is complete."""
    )

    # Validated response - no string parsing needed
    state["next"] = END if decision.next_agent == "DONE" else decision.next_agent
    state["routing_reasoning"] = decision.reasoning  # Track decision rationale
    return state

# Alternative: OpenAI structured output
async def llm_supervisor_openai(state: WorkflowState) -> WorkflowState:
    """OpenAI with strict structured output."""
    response = await client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format=SupervisorDecision
    )
    decision = response.choices[0].message.parsed
    state["next"] = END if decision.next_agent == "DONE" else decision.next_agent
    return state
```

## Tracking Progress

```python
def agent_node_factory(agent_name: str):
    """Create agent node that tracks completion."""
    async def node(state: WorkflowState) -> WorkflowState:
        result = await agents[agent_name].run(state["input"])

        return {
            **state,
            "results": state["results"] + [result],
            "agents_completed": state["agents_completed"] + [agent_name],
            "current_agent": None
        }
    return node
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Routing strategy | Round-robin for uniform, priority for critical-first |
| Max agents | 3-8 specialists (avoid overhead) |
| Failure handling | Skip failed agent, continue with others |
| Coordination | Centralized supervisor (simpler debugging) |

## Common Mistakes

- No completion tracking (runs agents forever)
- Forgetting worker → supervisor edge
- Missing END condition
- Heavy supervisor logic (should be lightweight)

## Related Skills

- `langgraph-routing` - Conditional edges
- `multi-agent-orchestration` - Fan-out patterns
- `langgraph-state` - State for agent tracking

## Capability Details

### supervisor-design
**Keywords:** supervisor, orchestration, routing, delegation
**Solves:**
- Design supervisor agent patterns
- Route tasks to specialized workers
- Coordinate multi-agent workflows

### worker-delegation
**Keywords:** worker, delegation, specialized, agent
**Solves:**
- Create specialized worker agents
- Define worker capabilities
- Implement delegation logic

### skillforge-workflow
**Keywords:** skillforge, analysis, content, workflow
**Solves:**
- SkillForge analysis workflow example
- Production supervisor implementation
- Real-world orchestration pattern

### supervisor-template
**Keywords:** template, implementation, code, starter
**Solves:**
- Supervisor workflow template
- Production-ready code
- Copy-paste implementation

### content-analysis
**Keywords:** content, analysis, graph, multi-agent
**Solves:**
- Content analysis graph template
- SkillForge-specific workflow
- Multi-agent content processing
