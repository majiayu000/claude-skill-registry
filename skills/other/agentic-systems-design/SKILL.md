---
name: agentic-systems-design
description: "Use when designing tool-use agents, multi-step reasoning systems, planning loops, multi-agent architectures, or agent evaluation frameworks."
---

# Agentic Systems Design

## Agent Architecture Selection

| Architecture | Use When | Complexity | Latency |
|-------------|----------|-----------|---------|
| **Single-agent ReAct** | 1-5 tools, linear reasoning | Low | Low |
| **Plan-and-execute** | Multi-step tasks needing upfront planning | Medium | Medium |
| **Tree-of-Thought** | Tasks with branching solutions, math/logic | Medium | High |
| **LATS (Language Agent Tree Search)** | Complex search + evaluation loops | High | Very High |
| **Multi-agent supervisor** | Specialized sub-tasks, delegation | High | Medium |
| **Multi-agent debate** | Tasks needing verification, fact-checking | High | High |
| **Multi-agent chain** | Sequential pipeline, each agent transforms output | Medium | Medium-High |

**Decision rule**: Start with single-agent ReAct. Escalate to plan-and-execute if the agent frequently fails mid-task. Use multi-agent only when a single model cannot hold all required expertise in context.

## Planning Patterns

### ReAct (Reasoning + Acting)

The default pattern. Model alternates between reasoning (think) and acting (tool call).

```python
import anthropic

client = anthropic.Anthropic()

def react_agent(question: str, tools: list[dict], max_steps: int = 10) -> str:
    system = """You are a helpful agent. For each step:
1. Think about what you need to do next
2. Use a tool if needed
3. When you have enough information, provide the final answer"""

    messages = [{"role": "user", "content": question}]

    for step in range(max_steps):
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4096,
            system=system,
            tools=tools,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            text_blocks = [b.text for b in response.content if b.type == "text"]
            return "\n".join(text_blocks)

        # Process tool calls
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result),
                })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

    return "Max steps reached without resolution"
```

### Plan-and-Execute

Separate planning from execution. Model generates a plan upfront, then executes steps sequentially.

```python
def plan_and_execute(question: str, tools: list[dict]) -> str:
    # Phase 1: Generate plan
    plan_response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2048,
        messages=[{"role": "user", "content": f"""Create a step-by-step plan to answer this question.
Return a numbered list of steps. Each step should be a single action.

Question: {question}"""}],
    )
    plan = plan_response.content[0].text

    # Phase 2: Execute each step
    context = []
    for step in parse_plan_steps(plan):
        step_result = react_agent(
            f"Execute this step: {step}\n\nContext from previous steps:\n{chr(10).join(context)}",
            tools=tools,
            max_steps=3,
        )
        context.append(f"Step: {step}\nResult: {step_result}")

    # Phase 3: Synthesize
    synthesis = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2048,
        messages=[{"role": "user", "content": f"""Original question: {question}
Execution results:
{chr(10).join(context)}

Synthesize a final answer."""}],
    )
    return synthesis.content[0].text
```

### Tree-of-Thought

Generate multiple reasoning paths, evaluate each, expand the most promising.

```python
def tree_of_thought(problem: str, breadth: int = 3, depth: int = 3) -> str:
    def generate_thoughts(state: str, n: int) -> list[str]:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2048,
            messages=[{"role": "user", "content": f"""Problem: {problem}
Current reasoning: {state}

Generate {n} distinct next reasoning steps. Return each on a new line prefixed with [THOUGHT]."""}],
        )
        return parse_thoughts(response.content[0].text)

    def evaluate_thought(state: str) -> float:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=256,
            messages=[{"role": "user", "content": f"""Rate this reasoning path from 0.0 to 1.0 for correctness and progress toward solving: {problem}

Reasoning: {state}

Return only a number."""}],
        )
        return float(response.content[0].text.strip())

    # BFS with pruning
    current_states = [""]
    for _ in range(depth):
        candidates = []
        for state in current_states:
            thoughts = generate_thoughts(state, breadth)
            for thought in thoughts:
                new_state = f"{state}\n{thought}" if state else thought
                score = evaluate_thought(new_state)
                candidates.append((score, new_state))
        candidates.sort(reverse=True, key=lambda x: x[0])
        current_states = [s for _, s in candidates[:breadth]]

    return current_states[0]
```

## Tool Design Principles

### Schema Design

```python
# Good: specific description, constrained types, clear required fields
{
    "name": "search_orders",
    "description": "Search customer orders by order ID, customer email, or date range. Returns up to 10 matching orders with status and total.",
    "input_schema": {
        "type": "object",
        "properties": {
            "order_id": {"type": "string", "description": "Exact order ID (e.g., ORD-12345)"},
            "customer_email": {"type": "string", "format": "email"},
            "date_from": {"type": "string", "description": "ISO 8601 date (YYYY-MM-DD)"},
            "date_to": {"type": "string", "description": "ISO 8601 date (YYYY-MM-DD)"},
            "status": {"type": "string", "enum": ["pending", "shipped", "delivered", "cancelled"]},
        },
        "required": [],  # All optional -- at least one should be provided
    },
}
```

**Tool description rules**:
- Start with a verb: "Search", "Create", "Calculate", "Retrieve"
- Mention return format: "Returns a JSON list of...", "Returns a single..."
- Include example inputs in description when format is ambiguous
- Keep under 200 words; models parse long descriptions less reliably

### Error Handling in Tool Results

```python
def execute_tool(name: str, inputs: dict) -> str:
    try:
        result = TOOL_REGISTRY[name](**inputs)
        return json.dumps({"status": "success", "data": result})
    except KeyError:
        return json.dumps({"status": "error", "message": f"Unknown tool: {name}"})
    except ValidationError as e:
        return json.dumps({"status": "error", "message": f"Invalid input: {e}"})
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Tool execution failed: {e}"})
```

Always return structured errors. Models recover better from `{"status": "error", "message": "..."}` than from raw exceptions or empty strings.

## Multi-Agent Patterns

### Supervisor Pattern

One orchestrator agent delegates to specialist agents.

```python
def supervisor_agent(question: str, specialists: dict[str, callable]) -> str:
    router_tools = [
        {
            "name": "delegate",
            "description": "Delegate a sub-task to a specialist agent.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "specialist": {
                        "type": "string",
                        "enum": list(specialists.keys()),
                        "description": "Which specialist to delegate to",
                    },
                    "task": {"type": "string", "description": "The sub-task description"},
                },
                "required": ["specialist", "task"],
            },
        }
    ]

    messages = [{"role": "user", "content": question}]
    for _ in range(10):
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4096,
            system="You are a supervisor. Break the task into sub-tasks and delegate to specialists. Synthesize results.",
            tools=router_tools,
            messages=messages,
        )
        if response.stop_reason == "end_turn":
            return response.content[0].text

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                specialist_fn = specialists[block.input["specialist"]]
                result = specialist_fn(block.input["task"])
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})
```

### Debate Pattern

Two agents argue for/against, a judge decides.

```python
def debate_agents(question: str, rounds: int = 2) -> str:
    pro_history, con_history = [], []

    for r in range(rounds):
        pro = client.messages.create(
            model="claude-sonnet-4-5-20250929", max_tokens=1024,
            system="You argue FOR the proposition. Be specific and cite evidence.",
            messages=[{"role": "user", "content": f"Question: {question}\nRound {r+1}. Previous debate:\n{format_debate(pro_history, con_history)}"}],
        ).content[0].text
        pro_history.append(pro)

        con = client.messages.create(
            model="claude-sonnet-4-5-20250929", max_tokens=1024,
            system="You argue AGAINST the proposition. Counter the pro arguments specifically.",
            messages=[{"role": "user", "content": f"Question: {question}\nRound {r+1}. Previous debate:\n{format_debate(pro_history, con_history)}"}],
        ).content[0].text
        con_history.append(con)

    # Judge synthesizes
    verdict = client.messages.create(
        model="claude-sonnet-4-5-20250929", max_tokens=1024,
        system="You are an impartial judge. Evaluate both sides and give a final verdict with reasoning.",
        messages=[{"role": "user", "content": f"Question: {question}\n\nFull debate:\n{format_debate(pro_history, con_history)}"}],
    )
    return verdict.content[0].text
```

## Agent Evaluation

| Metric | What It Measures | How to Compute |
|--------|-----------------|----------------|
| **Task completion** | Did the agent solve the problem? | Human eval or automated check against gold answer |
| **Tool accuracy** | Did it call the right tools with right args? | Compare tool call trace to expected trace |
| **Step efficiency** | How many steps to solve? | Count tool calls; compare to optimal path |
| **Cost** | Total tokens consumed | Sum input + output tokens across all turns |
| **Hallucination rate** | Did it fabricate tool results or facts? | Check claims against tool outputs |

```python
def evaluate_agent(agent_fn, test_cases: list[dict]) -> dict:
    results = []
    for case in test_cases:
        trace = []
        result = agent_fn(case["question"], trace_callback=trace.append)
        results.append({
            "question": case["question"],
            "expected": case["expected_answer"],
            "actual": result,
            "correct": check_answer(result, case["expected_answer"]),
            "num_steps": len(trace),
            "tools_used": [t["name"] for t in trace],
            "expected_tools": case.get("expected_tools", []),
            "tool_accuracy": compute_tool_accuracy(trace, case.get("expected_tools", [])),
        })
    return {
        "task_completion": sum(r["correct"] for r in results) / len(results),
        "avg_steps": sum(r["num_steps"] for r in results) / len(results),
        "tool_accuracy": sum(r["tool_accuracy"] for r in results) / len(results),
        "results": results,
    }
```

## Guardrails

| Guardrail | Default | Why |
|-----------|---------|-----|
| **Max iterations** | 10-15 | Prevents infinite loops |
| **Timeout** | 60-120s total | Caps wall-clock time |
| **Token budget** | 50K-100K per task | Caps cost per execution |
| **Human-in-the-loop** | On destructive actions | Prevents irreversible damage |
| **Tool allowlist** | Explicit per agent | Limits blast radius |
| **Output validation** | Schema check on final output | Ensures usable result |

```python
import time
from dataclasses import dataclass

@dataclass
class AgentBudget:
    max_steps: int = 15
    max_tokens: int = 100_000
    timeout_seconds: float = 120.0
    require_approval_for: list[str] | None = None  # Tool names needing human approval

    def check(self, steps: int, tokens: int, start_time: float):
        if steps >= self.max_steps:
            raise BudgetExceeded(f"Max steps ({self.max_steps}) exceeded")
        if tokens >= self.max_tokens:
            raise BudgetExceeded(f"Token budget ({self.max_tokens}) exceeded")
        elapsed = time.time() - start_time
        if elapsed >= self.timeout_seconds:
            raise BudgetExceeded(f"Timeout ({self.timeout_seconds}s) exceeded")

    def needs_approval(self, tool_name: str) -> bool:
        if self.require_approval_for is None:
            return False
        return tool_name in self.require_approval_for
```

## Gotchas

### Tool Description Quality
Vague tool descriptions cause wrong tool selection. "Gets data" is bad. "Retrieves customer order history by email address, returning last 30 days of orders with status and totals" is good.

### Infinite Loops
Agents can loop calling the same tool with the same args. Track call history and inject "You already called {tool} with these args. Try a different approach." after 2 duplicate calls.

### Context Window Overflow
Long agent runs accumulate tokens fast. Summarize older tool results once context exceeds 50% of window. Keep the last 2-3 tool results verbatim.

### Overly Eager Tool Use
Models sometimes call tools when they already have the answer in context. Add "Only use a tool if you cannot answer from information you already have" to the system prompt.

### Multi-Agent Communication Overhead
Each handoff between agents adds latency and token cost. Minimize cross-agent calls. If two agents always work together, merge them into one with a richer tool set.

### Evaluation Pitfalls
- Don't evaluate agents only on final answer; inspect the full tool call trace
- Agent behavior is non-deterministic; run evals 3-5 times and report variance
- Test adversarial inputs: ambiguous questions, impossible tasks, tasks requiring tools the agent doesn't have
