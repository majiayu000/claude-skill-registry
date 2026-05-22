---
name: agents
description: Patterns and architectures for building AI agents and workflows with LLMs. Use when designing systems that involve tool use, multi-step reasoning, autonomous decision-making, or orchestration of LLM-driven tasks.
---

# Building Agents

Agents are systems where LLMs dynamically direct their own processes and tool usage. This skill covers when to use agents vs workflows, common architectural patterns, and practical implementation guidance.

## Table of Contents

- [Agents vs Workflows](#agents-vs-workflows)
- [Workflow Patterns](#workflow-patterns)
- [Agent Architectures](#agent-architectures)
- [ReAct Pattern](#react-pattern)
- [Tool Design](#tool-design)
- [Best Practices](#best-practices)
- [References](#references)

## Agents vs Workflows

| Aspect | Workflows | Agents |
|--------|-----------|--------|
| **Control flow** | Predefined code paths | LLM determines next step |
| **Predictability** | High - deterministic steps | Lower - dynamic decisions |
| **Complexity** | Simpler to debug and test | More complex, harder to predict |
| **Best for** | Well-defined, repeatable tasks | Open-ended, adaptive problems |

**Key principle**: Start with the simplest solution. Use workflows when the task is predictable; use agents when flexibility is required.

## Workflow Patterns

### 1. Prompt Chaining

Decompose tasks into sequential LLM calls, where each step's output feeds the next.

```python
async def prompt_chain(input_text):
    # Step 1: Extract key information
    extracted = await llm.generate(
        "Extract the main entities and relationships from: " + input_text
    )

    # Step 2: Analyze
    analysis = await llm.generate(
        "Analyze these entities for patterns: " + extracted
    )

    # Step 3: Generate output
    return await llm.generate(
        "Based on this analysis, provide recommendations: " + analysis
    )
```

**Use when**: Tasks naturally decompose into fixed sequential steps.

### 2. Routing

Classify inputs and direct them to specialized handlers.

```python
async def route_request(user_input):
    # Classify the input
    category = await llm.generate(
        f"Classify this request into one of: [billing, technical, general]\n{user_input}"
    )

    handlers = {
        "billing": handle_billing,
        "technical": handle_technical,
        "general": handle_general,
    }

    return await handlers[category.strip()](user_input)
```

**Use when**: Different input types need fundamentally different processing.

### 3. Parallelization

Run multiple LLM calls concurrently for independent subtasks.

```python
import asyncio

async def parallel_analysis(document):
    # Run independent analyses in parallel
    results = await asyncio.gather(
        llm.generate(f"Summarize: {document}"),
        llm.generate(f"Extract key facts: {document}"),
        llm.generate(f"Identify sentiment: {document}"),
    )

    summary, facts, sentiment = results
    return {"summary": summary, "facts": facts, "sentiment": sentiment}
```

**Variants**:
- **Sectioning**: Break task into parallel subtasks
- **Voting**: Run same prompt multiple times, aggregate results

### 4. Orchestrator-Workers

Central LLM decomposes tasks and delegates to worker LLMs.

```python
class Orchestrator:
    async def run(self, task):
        # Break down the task
        subtasks = await self.plan(task)

        # Delegate to workers
        results = []
        for subtask in subtasks:
            worker_result = await self.delegate(subtask)
            results.append(worker_result)

        # Synthesize results
        return await self.synthesize(results)

    async def plan(self, task):
        response = await llm.generate(
            f"Break this task into subtasks:\n{task}\n\nReturn as JSON array."
        )
        return json.loads(response)

    async def delegate(self, subtask):
        return await llm.generate(f"Complete this subtask:\n{subtask}")

    async def synthesize(self, results):
        return await llm.generate(
            f"Combine these results into a coherent response:\n{results}"
        )
```

**Use when**: Tasks require dynamic decomposition that can't be predetermined.

### 5. Evaluator-Optimizer

One LLM generates, another evaluates and requests improvements.

```python
async def generate_with_feedback(task, max_iterations=3):
    response = await llm.generate(f"Complete this task:\n{task}")

    for _ in range(max_iterations):
        evaluation = await llm.generate(
            f"Evaluate this response for quality and correctness:\n{response}\n"
            "If improvements needed, specify them. Otherwise respond 'APPROVED'."
        )

        if "APPROVED" in evaluation:
            return response

        response = await llm.generate(
            f"Improve this response based on feedback:\n"
            f"Original: {response}\nFeedback: {evaluation}"
        )

    return response
```

**Use when**: Output quality is critical and can be objectively evaluated.

## Agent Architectures

### Autonomous Agent Loop

Agents operate in a loop: observe, think, act, repeat.

```python
class Agent:
    def __init__(self, tools: list, system_prompt: str):
        self.tools = {t.name: t for t in tools}
        self.system_prompt = system_prompt

    async def run(self, task: str, max_steps: int = 10):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": task},
        ]

        for step in range(max_steps):
            response = await llm.generate(messages, tools=self.tools)
            messages.append({"role": "assistant", "content": response})

            if response.tool_calls:
                for call in response.tool_calls:
                    result = await self.execute_tool(call)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": result
                    })
            else:
                # No tool calls - agent is done
                return response.content

        return "Max steps reached"

    async def execute_tool(self, call):
        tool = self.tools[call.name]
        return await tool.execute(**call.arguments)
```

### Human-in-the-Loop

Pause for human approval at critical checkpoints.

```python
class HumanInLoopAgent(Agent):
    def __init__(self, tools, system_prompt, approval_required: list):
        super().__init__(tools, system_prompt)
        self.approval_required = set(approval_required)

    async def execute_tool(self, call):
        if call.name in self.approval_required:
            approved = await self.request_approval(call)
            if not approved:
                return "Action cancelled by user"

        return await super().execute_tool(call)

    async def request_approval(self, call):
        print(f"Agent wants to execute: {call.name}({call.arguments})")
        response = input("Approve? (y/n): ")
        return response.lower() == "y"
```

## ReAct Pattern

ReAct (Reasoning and Acting) alternates between thinking and taking actions.

```python
REACT_PROMPT = """Answer the question using the available tools.

For each step:
1. Thought: Reason about what to do next
2. Action: Choose a tool and inputs
3. Observation: See the result
4. Repeat until you have the answer

Available tools: {tools}

Question: {question}
"""

async def react_agent(question, tools):
    prompt = REACT_PROMPT.format(
        tools=format_tools(tools),
        question=question
    )

    messages = [{"role": "user", "content": prompt}]

    while True:
        response = await llm.generate(messages)
        messages.append({"role": "assistant", "content": response})

        if "Final Answer:" in response:
            return extract_final_answer(response)

        action = parse_action(response)
        if action:
            observation = await execute_tool(action, tools)
            messages.append({
                "role": "user",
                "content": f"Observation: {observation}"
            })
```

**Advantages**:
- Explicit reasoning traces aid debugging
- More interpretable decision-making
- Better handling of complex multi-step tasks

## Tool Design

### Principles

1. **Self-contained**: Tools return complete, usable information
2. **Scoped**: Each tool does one thing well
3. **Descriptive**: Clear names and descriptions guide the LLM
4. **Error-robust**: Return informative errors, not exceptions

### Tool Definition Pattern

```python
class Tool:
    def __init__(self, name: str, description: str, parameters: dict, fn):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.fn = fn

    async def execute(self, **kwargs):
        try:
            return await self.fn(**kwargs)
        except Exception as e:
            return f"Error: {str(e)}"

# Example tool
search_tool = Tool(
    name="search_database",
    description="Search the database for records matching a query. "
                "Returns up to 10 matching records with their IDs and summaries.",
    parameters={
        "query": {"type": "string", "description": "Search query"},
        "limit": {"type": "integer", "description": "Max results (default 10)"},
    },
    fn=search_database
)
```

### Tool Interface Guidelines

- Prefer text inputs/outputs over complex structured data
- Include usage examples in descriptions for ambiguous tools
- Return truncated results when output could be large
- Provide clear feedback on what the tool did

## Best Practices

1. **Start simple**: Begin with the simplest architecture that could work. Add complexity only when it demonstrably improves outcomes.

2. **Maintain transparency**: Ensure the agent's planning steps are visible. This aids debugging and builds user trust.

3. **Design for failure**: Agents will make mistakes. Include guardrails, retries, and graceful degradation.

4. **Test extensively**: Use sandboxed environments. Test edge cases and failure modes, not just happy paths.

5. **Limit tool proliferation**: More tools means more confusion. Keep the tool set focused and well-documented.

6. **Implement checkpoints**: For long-running tasks, save state periodically to enable recovery.

7. **Set resource limits**: Cap iterations, token usage, and tool calls to prevent runaway agents.

8. **Log everything**: Record all LLM calls, tool executions, and decisions for debugging and improvement.

9. **Handle ambiguity**: When uncertain, have the agent ask for clarification rather than guessing.

10. **Measure outcomes**: Track task completion rates, accuracy, and efficiency to guide improvements.

## References

- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) - Anthropic's guide to agent patterns and best practices
- [LangGraph Workflows & Agents](https://docs.langchain.com/oss/javascript/langgraph/workflows-agents) - LangGraph documentation on agent architectures
- [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629) - Paper introducing the ReAct prompting pattern
