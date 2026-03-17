---
name: agentic-workflows
version: 1.0.0
description: Design and implement agentic AI workflows and patterns. Covers ReAct, planning agents, tool use, memory systems, and multi-agent orchestration. Use when building autonomous AI agents, implementing complex task automation, or designing intelligent workflow systems.
---

# Agentic Workflows: AI Agent Design Patterns

Design and implement effective agentic AI workflows using proven patterns for reasoning, planning, tool use, and multi-agent orchestration.

## Triggers

Use this skill when:
- Designing autonomous AI agent systems
- Implementing complex task automation
- Building multi-agent orchestration
- Creating self-improving AI workflows
- Implementing ReAct or planning patterns
- Keywords: agentic, agent, autonomous, ReAct, planning, tool use, multi-agent, orchestration, reasoning, memory

## Core Concepts

### What Makes an Agent

An AI agent is a system that:
1. **Perceives** its environment (reads context, files, APIs)
2. **Reasons** about what to do (plans, decides)
3. **Acts** on the environment (executes tools, writes files)
4. **Learns** from results (updates state, improves)

### Agent vs. Workflow

| Aspect | Traditional Workflow | Agentic Workflow |
|--------|---------------------|------------------|
| Control | Predefined steps | Dynamic decisions |
| Branching | Fixed conditions | Reasoned choices |
| Error Handling | Catch/retry | Analyze/adapt |
| Scope | Known tasks | Open-ended goals |

---

## Pattern 1: ReAct (Reasoning + Acting)

### Overview

ReAct interleaves reasoning and acting:

```
Thought: I need to find the user's order
Action: query_database("orders", {"user_id": "123"})
Observation: Found 3 orders: [...]
Thought: The most recent order is from January
Action: get_order_details("order-456")
Observation: Order contains 2 items...
Thought: I now have enough information
Action: respond_to_user("Your latest order...")
```

### Implementation Pattern

```python
def react_loop(goal: str, max_iterations: int = 10):
    context = {"goal": goal, "history": []}

    for i in range(max_iterations):
        # Reason about current state
        thought = llm_reason(context)
        context["history"].append({"type": "thought", "content": thought})

        # Decide on action
        action = llm_decide_action(context)

        if action.type == "final_answer":
            return action.content

        # Execute action
        observation = execute_tool(action)
        context["history"].append({
            "type": "observation",
            "action": action,
            "result": observation
        })

    return "Max iterations reached"
```

### Best Practices

- Keep thoughts concise but informative
- Validate tool outputs before proceeding
- Include error states in reasoning
- Set reasonable iteration limits

---

## Pattern 2: Plan-and-Execute

### Overview

Separate planning from execution:

```
PLAN:
1. Gather requirements from user
2. Research existing patterns
3. Design solution architecture
4. Implement core functionality
5. Add tests
6. Document

EXECUTE:
[Execute each step, revise plan if needed]
```

### Implementation Pattern

```python
def plan_and_execute(goal: str):
    # Phase 1: Planning
    plan = llm_create_plan(goal)

    # Phase 2: Execution with replanning
    results = []
    for step in plan.steps:
        result = execute_step(step)
        results.append(result)

        # Check if replanning needed
        if needs_replan(result, plan):
            plan = llm_revise_plan(goal, results, plan)

    return synthesize_results(results)
```

### When to Use

- Complex multi-step tasks
- Tasks requiring resource allocation
- Projects with dependencies
- When visibility into progress matters

---

## Pattern 3: Tool-Use Agent

### Overview

Agent that selects and uses tools dynamically:

```
Available Tools:
- search_code(query) - Search codebase
- read_file(path) - Read file contents
- write_file(path, content) - Write to file
- run_tests() - Execute test suite
- git_commit(message) - Commit changes

Task: "Fix the failing test in user-service"

Agent selects: search_code("user-service test")
Agent selects: read_file("tests/user-service.test.ts")
Agent selects: read_file("src/user-service.ts")
Agent selects: write_file("src/user-service.ts", fixed_content)
Agent selects: run_tests()
Agent selects: git_commit("fix: resolve user-service test failure")
```

### Tool Definition Pattern

```python
tools = [
    {
        "name": "search_code",
        "description": "Search codebase for pattern",
        "parameters": {
            "query": {"type": "string", "description": "Search pattern"}
        },
        "returns": "List of matching files and lines"
    },
    # ... more tools
]

def tool_use_agent(task: str, tools: list):
    while not is_complete(task):
        # Select tool based on current state
        tool_choice = llm_select_tool(task, tools, context)

        # Execute tool
        result = execute_tool(tool_choice)

        # Update context
        context.add_observation(tool_choice, result)
```

### Tool Design Principles

1. **Single Responsibility**: Each tool does one thing well
2. **Clear Descriptions**: Help agent select correctly
3. **Predictable Output**: Consistent return formats
4. **Error Information**: Return useful error messages
5. **Idempotency**: Safe to retry when possible

---

## Pattern 4: Memory Systems

### Types of Memory

| Type | Purpose | Implementation |
|------|---------|----------------|
| **Working** | Current task context | In-context prompt |
| **Episodic** | Past interactions | Conversation history |
| **Semantic** | Knowledge/facts | RAG/vector store |
| **Procedural** | How to do things | Skills/tools |

### Memory Architecture

```
                    ┌─────────────────┐
                    │   Agent Core    │
                    │   (Reasoning)   │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         v                   v                   v
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Working   │     │  Episodic   │     │  Semantic   │
│   Memory    │     │   Memory    │     │   Memory    │
│ (context)   │     │  (history)  │     │  (RAG/KB)   │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Implementation with Archon

```python
# Store episodic memory
manage_document("create",
    project_id=PROJECT_ID,
    title="Session Memory: 2025-01-23",
    document_type="note",
    content={
        "session_id": "session-001",
        "interactions": [...],
        "decisions": [...],
        "learnings": [...]
    }
)

# Retrieve for new session
docs = find_documents(project_id=PROJECT_ID, query="session memory")
```

---

## Pattern 5: Multi-Agent Systems

### Architectures

**Hierarchical:**
```
         ┌──────────────┐
         │  Orchestrator │
         └──────┬───────┘
                │
    ┌───────────┼───────────┐
    │           │           │
    v           v           v
┌───────┐  ┌───────┐  ┌───────┐
│Agent A│  │Agent B│  │Agent C│
│(Code) │  │(Test) │  │(Review)│
└───────┘  └───────┘  └───────┘
```

**Peer-to-Peer:**
```
┌───────┐     ┌───────┐
│Agent A│<--->│Agent B│
└───┬───┘     └───┬───┘
    │             │
    └──────┬──────┘
           │
           v
      ┌───────┐
      │Agent C│
      └───────┘
```

**Pipeline:**
```
┌───────┐   ┌───────┐   ┌───────┐   ┌───────┐
│ Input │-->│Agent A│-->│Agent B│-->│Agent C│-->│Output│
└───────┘   └───────┘   └───────┘   └───────┘
```

### Orchestrator Pattern

```python
class Orchestrator:
    def __init__(self, agents: dict):
        self.agents = agents
        self.state = {}

    def execute(self, task: str):
        plan = self.create_plan(task)

        for step in plan:
            agent = self.select_agent(step)
            result = agent.execute(step, self.state)
            self.state.update(result)

            if self.needs_replan(result):
                plan = self.revise_plan(plan, result)

        return self.synthesize(self.state)
```

### Agent Communication

```python
# Message passing
message = {
    "from": "coder-agent",
    "to": "tester-agent",
    "type": "work_complete",
    "content": {
        "files_changed": ["src/user.py"],
        "commit": "abc123"
    }
}

# Shared state (via Archon)
manage_task("update",
    task_id=TASK_ID,
    metadata={
        "agent_state": {
            "last_agent": "coder",
            "next_agent": "tester",
            "handoff_data": {...}
        }
    }
)
```

---

## Pattern 6: Self-Improvement Loop

### Overview

Agent that learns from its mistakes:

```
┌─────────────────────────────────────────────┐
│                                             │
│    ┌──────────┐                             │
│    │  Execute │                             │
│    └────┬─────┘                             │
│         │                                   │
│         v                                   │
│    ┌──────────┐     ┌──────────┐           │
│    │ Evaluate │────>│  Learn   │           │
│    │  Result  │     │          │           │
│    └──────────┘     └────┬─────┘           │
│                          │                  │
│                          v                  │
│                    ┌──────────┐             │
│                    │  Update  │             │
│                    │ Strategy │             │
│                    └────┬─────┘             │
│                         │                   │
└─────────────────────────┘                   │
```

### Implementation

```python
def self_improving_agent(task: str, max_attempts: int = 3):
    strategy = load_default_strategy()

    for attempt in range(max_attempts):
        result = execute_with_strategy(task, strategy)

        evaluation = evaluate_result(result)

        if evaluation.success:
            # Store successful strategy
            save_strategy(task_type, strategy)
            return result

        # Learn from failure
        lessons = analyze_failure(result, evaluation)
        strategy = update_strategy(strategy, lessons)

    return escalate_to_human(task, attempts)
```

---

## Implementation Checklist

### Essential Components

- [ ] Clear goal/task definition
- [ ] Reasoning/planning capability
- [ ] Tool/action execution
- [ ] State management
- [ ] Error handling
- [ ] Termination conditions

### Quality Attributes

- [ ] Observability (logging, tracing)
- [ ] Controllability (pause, resume, cancel)
- [ ] Recoverability (checkpoints, retry)
- [ ] Explainability (decision logging)
- [ ] Resource limits (iterations, time, cost)

### Safety Considerations

- [ ] Sandboxed execution environment
- [ ] Permission boundaries
- [ ] Human-in-the-loop for critical actions
- [ ] Rollback capabilities
- [ ] Audit trail

---

## Archon Integration

### Project Structure for Agents

```python
# Create agent project
manage_project("create",
    title="Multi-Agent System",
    description="Orchestrated agent pipeline"
)

# Create tasks for each agent role
manage_task("create",
    project_id=PROJECT_ID,
    title="Coder Agent: Implement feature",
    feature="Agent-Coder"
)

manage_task("create",
    project_id=PROJECT_ID,
    title="Tester Agent: Validate implementation",
    feature="Agent-Tester"
)

# Store agent state in documents
manage_document("create",
    project_id=PROJECT_ID,
    title="Agent Orchestration State",
    document_type="note",
    content={
        "pipeline_state": "running",
        "current_agent": "coder",
        "completed_steps": [],
        "pending_steps": []
    }
)
```

---

## Best Practices

1. **Start Simple**: Begin with single-agent, add complexity as needed
2. **Clear Boundaries**: Define what each agent can/cannot do
3. **Explicit Handoffs**: Make agent transitions observable
4. **Fail Gracefully**: Always have fallback/escalation paths
5. **Test Incrementally**: Verify each agent independently first
6. **Monitor Everything**: Log decisions, actions, outcomes
7. **Human Oversight**: Keep humans in the loop for critical decisions
8. **Iterate**: Agent design improves through testing and refinement

---

## Related Skills

- `/autonomous-agent-harness` - Full harness implementation
- `/ralph-loop` - Iterative development loops
- `/speckit-workflow` - Spec-driven development
- `/archon-workflow` - Task and project management

---

## Notes

- Agentic systems require careful design and testing
- Start with well-defined tasks before attempting open-ended goals
- Multi-agent systems add complexity - use only when needed
- Always have escape hatches and human intervention points
- Document agent decisions for debugging and improvement
