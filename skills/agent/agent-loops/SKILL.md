---
name: agent-loops
description: Agentic workflow patterns for autonomous LLM reasoning. Use when building ReAct agents, implementing reasoning loops, or creating LLMs that plan and execute multi-step tasks.
context: fork
agent: workflow-architect
version: 1.0.0
author: SkillForge
user-invocable: false
---

# Agent Loops

Enable LLMs to reason, plan, and take autonomous actions.

## When to Use

- Multi-step problem solving
- Tasks requiring planning
- Autonomous tool use
- Self-correcting workflows

## ReAct Pattern (Reasoning + Acting)

```python
REACT_PROMPT = """You are an agent that reasons step by step.

For each step, respond with:
Thought: [your reasoning about what to do next]
Action: [tool_name(arg1, arg2)]
Observation: [you'll see the result here]

When you have the final answer:
Thought: I now have enough information
Final Answer: [your response]

Available tools: {tools}

Question: {question}
"""

async def react_loop(question: str, tools: dict, max_steps: int = 10) -> str:
    """Execute ReAct reasoning loop."""
    history = REACT_PROMPT.format(tools=list(tools.keys()), question=question)

    for step in range(max_steps):
        response = await llm.chat([{"role": "user", "content": history}])
        history += response.content

        # Check for final answer
        if "Final Answer:" in response.content:
            return response.content.split("Final Answer:")[-1].strip()

        # Extract and execute action
        if "Action:" in response.content:
            action = parse_action(response.content)
            result = await tools[action.name](*action.args)
            history += f"\nObservation: {result}\n"

    return "Max steps reached without answer"
```

## Plan-and-Execute Pattern

```python
async def plan_and_execute(goal: str) -> str:
    """Create plan first, then execute steps."""
    # 1. Generate plan
    plan = await llm.chat([{
        "role": "user",
        "content": f"Create a step-by-step plan to: {goal}\n\nFormat as numbered list."
    }])

    steps = parse_plan(plan.content)
    results = []

    # 2. Execute each step
    for i, step in enumerate(steps):
        result = await execute_step(step, context=results)
        results.append({"step": step, "result": result})

        # 3. Check if replanning needed
        if should_replan(results):
            return await plan_and_execute(
                f"{goal}\n\nProgress so far: {results}"
            )

    # 4. Synthesize final answer
    return await synthesize(goal, results)
```

## Self-Correction Loop

```python
async def self_correcting_agent(task: str, max_retries: int = 3) -> str:
    """Agent that validates and corrects its own output."""
    for attempt in range(max_retries):
        # Generate response
        response = await llm.chat([{
            "role": "user",
            "content": task
        }])

        # Self-validate
        validation = await llm.chat([{
            "role": "user",
            "content": f"""Validate this response for the task: {task}

Response: {response.content}

Check for:
1. Correctness - Is it factually accurate?
2. Completeness - Does it fully answer the task?
3. Format - Is it properly formatted?

If valid, respond: VALID
If invalid, respond: INVALID: [what's wrong and how to fix]"""
        }])

        if "VALID" in validation.content:
            return response.content

        # Correct based on feedback
        task = f"{task}\n\nPrevious attempt had issues: {validation.content}"

    return response.content  # Return best attempt
```

## Memory Management

```python
class AgentMemory:
    """Sliding window memory for agents."""

    def __init__(self, max_messages: int = 20):
        self.messages = []
        self.max_messages = max_messages
        self.summary = ""

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

        # Summarize old messages when window full
        if len(self.messages) > self.max_messages:
            self._compress()

    def _compress(self):
        """Summarize oldest messages."""
        old = self.messages[:10]
        self.messages = self.messages[10:]

        # Async summarize would be better
        summary = summarize(old)
        self.summary = f"{self.summary}\n{summary}"

    def get_context(self) -> list:
        """Get messages with summary prefix."""
        context = []
        if self.summary:
            context.append({
                "role": "system",
                "content": f"Previous context summary: {self.summary}"
            })
        return context + self.messages
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Max steps | 5-15 (prevent infinite loops) |
| Temperature | 0.3-0.7 (balance creativity/focus) |
| Memory window | 10-20 messages |
| Validation | Every 3-5 steps |

## Common Mistakes

- No step limit (infinite loops)
- No memory management (context overflow)
- No error recovery (crashes on tool failure)
- Over-complex prompts (agent gets confused)

## Related Skills

- `function-calling` - Tool definitions and execution
- `multi-agent-orchestration` - Coordinating multiple agents
- `langgraph-workflows` - Stateful agent graphs

## Capability Details

### react-loop
**Keywords:** react, reason, act, observe, loop
**Solves:**
- Implement ReAct pattern
- Create reasoning loops
- Build iterative agents

### tool-use
**Keywords:** tool, function, call, execution
**Solves:**
- Implement tool calling
- Execute functions from LLM
- Parse tool responses

### workflow-template
**Keywords:** template, workflow, agent, typescript
**Solves:**
- Agent workflow template
- TypeScript implementation
- Copy-paste starter
