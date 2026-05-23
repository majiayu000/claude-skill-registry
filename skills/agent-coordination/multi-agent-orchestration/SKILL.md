---
name: multi-agent-orchestration
description: Multi-agent coordination and synthesis patterns. Use when orchestrating multiple specialized agents, implementing fan-out/fan-in workflows, or synthesizing outputs from parallel agents.
context: fork
agent: workflow-architect
version: 1.0.0
author: SkillForge
user-invocable: false
---

# Multi-Agent Orchestration

Coordinate multiple specialized agents for complex tasks.

## Fan-Out/Fan-In Pattern

```python
async def multi_agent_analysis(content: str) -> dict:
    """Fan-out to specialists, fan-in to synthesize."""
    agents = [
        ("security", security_agent),
        ("performance", performance_agent),
        ("code_quality", quality_agent),
        ("architecture", architecture_agent),
    ]

    # Fan-out: Run all agents in parallel
    tasks = [agent(content) for _, agent in agents]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter successful results
    findings = [
        {"agent": name, "result": result}
        for (name, _), result in zip(agents, results)
        if not isinstance(result, Exception)
    ]

    # Fan-in: Synthesize findings
    return await synthesize_findings(findings)
```

## Supervisor Pattern

```python
class Supervisor:
    """Central coordinator that routes to specialists."""

    def __init__(self, agents: dict):
        self.agents = agents  # {"security": agent, "performance": agent}
        self.completed = []

    async def run(self, task: str) -> dict:
        """Route task through appropriate agents."""
        # 1. Determine which agents to use
        plan = await self.plan_routing(task)

        # 2. Execute in dependency order
        results = {}
        for agent_name in plan.execution_order:
            if plan.can_parallelize(agent_name):
                # Run parallel batch
                batch = plan.get_parallel_batch(agent_name)
                batch_results = await asyncio.gather(*[
                    self.agents[name](task, context=results)
                    for name in batch
                ])
                results.update(dict(zip(batch, batch_results)))
            else:
                # Run sequential
                results[agent_name] = await self.agents[agent_name](
                    task, context=results
                )

        return results

    async def plan_routing(self, task: str) -> RoutingPlan:
        """Use LLM to determine agent routing."""
        response = await llm.chat([{
            "role": "user",
            "content": f"""Task: {task}

Available agents: {list(self.agents.keys())}

Which agents should handle this task?
What order? Can any run in parallel?"""
        }])
        return parse_routing_plan(response.content)
```

## Conflict Resolution

```python
async def resolve_conflicts(findings: list[dict]) -> list[dict]:
    """When agents disagree, resolve by confidence or LLM."""
    conflicts = detect_conflicts(findings)

    if not conflicts:
        return findings

    for conflict in conflicts:
        # Option 1: Higher confidence wins
        winner = max(conflict.agents, key=lambda a: a.confidence)

        # Option 2: LLM arbitration
        resolution = await llm.chat([{
            "role": "user",
            "content": f"""Two agents disagree:

Agent A ({conflict.agent_a.name}): {conflict.agent_a.finding}
Agent B ({conflict.agent_b.name}): {conflict.agent_b.finding}

Which is more likely correct and why?"""
        }])

        # Record resolution
        conflict.resolution = parse_resolution(resolution.content)

    return apply_resolutions(findings, conflicts)
```

## Synthesis Pattern

```python
async def synthesize_findings(findings: list[dict]) -> dict:
    """Combine multiple agent outputs into coherent result."""
    # Group by category
    by_category = {}
    for f in findings:
        cat = f.get("category", "general")
        by_category.setdefault(cat, []).append(f)

    # Synthesize each category
    synthesis = await llm.chat([{
        "role": "user",
        "content": f"""Synthesize these agent findings into a coherent summary:

{json.dumps(by_category, indent=2)}

Output format:
- Executive summary (2-3 sentences)
- Key findings by category
- Recommendations
- Confidence score (0-1)"""
    }])

    return parse_synthesis(synthesis.content)
```

## Agent Communication Bus

```python
class AgentBus:
    """Message passing between agents."""

    def __init__(self):
        self.messages = []
        self.subscribers = {}

    def publish(self, from_agent: str, message: dict):
        """Broadcast message to all agents."""
        msg = {"from": from_agent, "data": message, "ts": time.time()}
        self.messages.append(msg)

        for callback in self.subscribers.values():
            callback(msg)

    def subscribe(self, agent_id: str, callback):
        """Register agent to receive messages."""
        self.subscribers[agent_id] = callback

    def get_history(self, agent_id: str = None) -> list:
        """Get message history, optionally filtered."""
        if agent_id:
            return [m for m in self.messages if m["from"] == agent_id]
        return self.messages
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Agent count | 3-8 specialists |
| Parallelism | Parallelize independent agents |
| Conflict resolution | Confidence score or LLM arbitration |
| Communication | Shared state or message bus |

## Common Mistakes

- No timeout per agent (one slow agent blocks all)
- No error isolation (one failure crashes workflow)
- Over-coordination (too much overhead)
- Missing synthesis (raw agent outputs not useful)

## Related Skills

- `langgraph-supervisor` - LangGraph supervisor pattern
- `langgraph-parallel` - Fan-out/fan-in with LangGraph
- `agent-loops` - Single agent patterns

## Capability Details

### agent-communication
**Keywords:** agent communication, message passing, agent protocol, inter-agent
**Solves:**
- Establish communication between agents
- Implement message passing patterns
- Handle async agent communication

### task-delegation
**Keywords:** delegate, task routing, work distribution, agent dispatch
**Solves:**
- Route tasks to specialized agents
- Implement work distribution strategies
- Handle agent capability matching

### result-aggregation
**Keywords:** aggregate, combine results, merge outputs, synthesis
**Solves:**
- Combine outputs from multiple agents
- Implement result synthesis patterns
- Handle conflicting agent outputs

### error-coordination
**Keywords:** error handling, retry, fallback agent, failure recovery
**Solves:**
- Handle agent failures gracefully
- Implement retry and fallback patterns
- Coordinate error recovery

### agent-lifecycle
**Keywords:** lifecycle, spawn agent, terminate, agent pool
**Solves:**
- Manage agent creation and termination
- Implement agent pooling
- Handle agent health checks
