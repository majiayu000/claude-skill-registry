---
name: Multi-Agent Architect
description: Design and orchestrate multi-agent systems. Use when building complex AI systems requiring specialization, parallel processing, or collaborative problem-solving. Covers agent coordination, communication patterns, and task delegation strategies.
version: 1.0.0
---

# Multi-Agent Architect

Design systems where multiple specialized agents collaborate to solve complex problems.

## Core Principle

**Divide complex tasks among specialized agents**, each expert in their domain, coordinated through clear communication patterns.

## When to Use Multi-Agent Systems

### Use Multi-Agent When:

- ✅ Task requires multiple specializations (research + writing + coding)
- ✅ Parallel processing speeds up solution (independent subtasks)
- ✅ Need self-correction through peer review
- ✅ Complex workflows with decision points
- ✅ Scaling single-agent becomes unwieldy

### Don't Use Multi-Agent When:

- ❌ Single agent can handle task efficiently
- ❌ Task is simple and linear
- ❌ Communication overhead > parallelization benefit
- ❌ Team lacks multi-agent debugging expertise

---

## Multi-Agent Patterns

### Pattern 1: Sequential Pipeline

**Use**: Multi-step workflow where each agent builds on previous

```
User Query → Researcher → Analyst → Writer → Editor → Output
```

**Example**: Research report generation

1. Researcher: Gather sources
2. Analyst: Synthesize findings
3. Writer: Draft report
4. Editor: Refine and format

**Pros**: Clear dependencies, easy to debug
**Cons**: Sequential (no parallelization), bottlenecks

---

### Pattern 2: Hierarchical (Manager-Worker)

**Use**: Complex task broken into parallel subtasks

```
              Manager Agent
              /     |     \
    Worker 1   Worker 2   Worker 3
    (Search)   (Analyze)  (Summarize)
              \     |     /
              Aggregator Agent
```

**Example**: Market research across competitors

- Manager: Decompose into per-competitor analysis
- Workers: Research competitor A, B, C in parallel
- Aggregator: Combine findings

**Pros**: Parallelization, specialization
**Cons**: Manager complexity, coordination overhead

---

### Pattern 3: Peer Collaboration (Round Table)

**Use**: Multiple perspectives improve quality

```
Coder ↔ Reviewer ↔ Tester
  ↓        ↓        ↓
      Consensus
```

**Example**: Code generation with review

1. Coder: Write initial code
2. Reviewer: Check for issues
3. Tester: Validate functionality
4. Iterate until consensus

**Pros**: Quality through review, self-correction
**Cons**: May not converge, expensive (multiple LLM calls)

---

### Pattern 4: Agent Swarm

**Use**: Many agents explore solution space independently

```
Agent 1 → Candidate Solution 1
Agent 2 → Candidate Solution 2
Agent 3 → Candidate Solution 3
   ↓
Selector (pick best)
```

**Example**: Creative brainstorming

- 5 agents generate different approaches
- Selector evaluates and picks best

**Pros**: Exploration, creativity
**Cons**: Cost (N agents), may produce similar solutions

---

## Communication Patterns

### 1. Shared Memory

```python
shared_state = {
    "research_findings": [],
    "current_task": "analyze_competitors",
    "decisions": []
}

# All agents read/write to shared state
researcher.execute(shared_state)
analyst.execute(shared_state)
```

**Pros**: Simple, all agents see full context
**Cons**: Race conditions, hard to debug who changed what

---

### 2. Message Passing

```python
# Agent A sends message to Agent B
message = {
    "from": "researcher",
    "to": "analyst",
    "content": research_findings,
    "metadata": {"confidence": 0.9}
}

message_queue.send(message)
```

**Pros**: Clear communication flow, traceable
**Cons**: More complex to implement

---

### 3. Event-Driven

```python
# Agents subscribe to events
event_bus.subscribe("research_complete", analyst.on_research_complete)
event_bus.subscribe("analysis_complete", writer.on_analysis_complete)

# Agent publishes event when done
event_bus.publish("research_complete", research_data)
```

**Pros**: Loose coupling, scalable
**Cons**: Harder to follow execution flow

---

## Agent Coordination Strategies

### 1. Fixed Workflow

Predefined sequence, no dynamic decisions

```python
workflow = [
    ("researcher", gather_info),
    ("analyst", analyze_data),
    ("writer", create_report)
]

for agent_name, task in workflow:
    result = agents[agent_name].execute(task, context)
    context.update(result)
```

**Use**: Predictable tasks, clear dependencies

---

### 2. Dynamic Routing

Manager decides next agent based on context

```python
class ManagerAgent:
    def route_task(self, task, context):
        if requires_technical_expertise(task):
            return tech_specialist
        elif requires_creative_input(task):
            return creative_agent
        else:
            return generalist
```

**Use**: Tasks vary significantly, need flexibility

---

### 3. Consensus-Based

Agents vote or reach agreement

```python
proposals = [agent.propose_solution(task) for agent in agents]
scores = [agent.evaluate(proposals) for agent in agents]
best = proposals[argmax(mean(scores))]
```

**Use**: High-stakes decisions, quality critical

---

## Implementation with CrewAI

**CrewAI Pattern** (Role-based teams):

```python
from crewai import Agent, Task, Crew

# Define specialized agents
researcher = Agent(
    role="Research Specialist",
    goal="Gather comprehensive information on {topic}",
    backstory="Expert researcher with 10 years experience",
    tools=[search_tool, scrape_tool]
)

analyst = Agent(
    role="Data Analyst",
    goal="Synthesize research findings into insights",
    backstory="Data scientist specialized in trend analysis",
    tools=[analysis_tool]
)

writer = Agent(
    role="Technical Writer",
    goal="Create clear, compelling reports",
    backstory="Professional writer with technical expertise",
    tools=[writing_tool]
)

# Define tasks
research_task = Task(
    description="Research {topic} thoroughly",
    agent=researcher,
    expected_output="Comprehensive research findings with sources"
)

analysis_task = Task(
    description="Analyze research findings for key insights",
    agent=analyst,
    context=[research_task],  # Depends on research_task
    expected_output="List of key insights and trends"
)

writing_task = Task(
    description="Write executive summary based on analysis",
    agent=writer,
    context=[research_task, analysis_task],
    expected_output="500-word executive summary"
)

# Create crew and execute
crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, writing_task],
    verbose=True
)

result = crew.kickoff(inputs={"topic": "AI market trends"})
```

---

## Implementation with LangGraph

**LangGraph Pattern** (State machines):

```python
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    input: str
    research: str
    analysis: str
    output: str

def research_node(state):
    research = researcher_agent.run(state["input"])
    return {"research": research}

def analysis_node(state):
    analysis = analyst_agent.run(state["research"])
    return {"analysis": analysis}

def writing_node(state):
    output = writer_agent.run(state["analysis"])
    return {"output": output}

# Build graph
workflow = StateGraph(AgentState)

workflow.add_node("research", research_node)
workflow.add_node("analysis", analysis_node)
workflow.add_node("writing", writing_node)

workflow.set_entry_point("research")
workflow.add_edge("research", "analysis")
workflow.add_edge("analysis", "writing")
workflow.add_edge("writing", END)

app = workflow.compile()

# Execute
result = app.invoke({"input": "Analyze AI market trends"})
```

---

## Best Practices

### 1. Clear Agent Roles

Each agent should have specific expertise and responsibilities

### 2. Minimize Communication

More agents = more coordination overhead. Start simple.

### 3. Idempotent Operations

Agents should be restartable without side effects

### 4. Failure Handling

Design for agent failures (retry, fallback, skip)

### 5. Observable Execution

Log agent decisions, trace execution flow

### 6. Cost Management

Track token usage per agent, optimize expensive calls

---

## Common Multi-Agent Mistakes

❌ **Too many agents** → Start with 2-3, add only if needed
❌ **Unclear responsibilities** → Define explicit roles
❌ **No failure handling** → One agent failure breaks entire system
❌ **Synchronous bottlenecks** → Parallelize independent agents
❌ **Ignoring costs** → N agents = N× LLM calls
❌ **Over-engineering** → Single agent often sufficient

---

## Decision Framework: Single vs Multi-Agent

```
Task Complexity?
│
├─ Simple, linear → Single Agent
│
├─ Complex, requires specialization?
│  │
│  ├─ Sequential steps → Pipeline Pattern
│  ├─ Parallel subtasks → Hierarchical Pattern
│  ├─ Need review → Peer Collaboration
│  └─ Explore solutions → Swarm Pattern
│
└─ Uncertain → Start with Single Agent, refactor to Multi if needed
```

---

## Monitoring & Debugging

```python
# Track agent execution
class TrackedAgent(Agent):
    def execute(self, task, context):
        start = time.time()
        logger.info(f"{self.name} starting: {task}")

        result = super().execute(task, context)

        duration = time.time() - start
        logger.info(f"{self.name} completed in {duration}s")

        metrics.record({
            "agent": self.name,
            "task": task,
            "duration": duration,
            "tokens": result.token_count,
            "cost": result.cost
        })

        return result
```

**Key Metrics**:

- Agent execution time
- Token usage per agent
- Success/failure rates
- Handoff delays
- Overall workflow duration

---

## Related Resources

**Related Skills**:

- `rag-implementer` - For knowledge-grounded agents
- `knowledge-graph-builder` - For agent knowledge bases
- `api-designer` - For agent communication APIs

**Related Patterns**:

- `META/DECISION-FRAMEWORK.md` - Framework selection (CrewAI vs LangGraph)
- `STANDARDS/architecture-patterns/multi-agent-pattern.md` - Agent architectures (when created)

**Related Playbooks**:

- `PLAYBOOKS/deploy-multi-agent-system.md` - Deployment guide (when created)
- `PLAYBOOKS/debug-agent-workflows.md` - Debugging procedures (when created)
