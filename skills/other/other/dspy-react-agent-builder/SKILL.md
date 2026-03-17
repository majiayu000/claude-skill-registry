---
name: dspy-react-agent-builder
version: "1.0.0"
dspy-compatibility: "3.1.2"
description: This skill should be used when the user asks to "create a ReAct agent", "build an agent with tools", "implement tool-calling agent", "use dspy.ReAct", mentions "agent with tools", "reasoning and acting", "multi-step agent", "agent optimization with GEPA", or needs to build production agents that use tools to solve complex tasks.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# DSPy ReAct Agent Builder

## Goal

Build production-quality ReAct agents that use tools to solve complex multi-step tasks with reasoning, acting, and error handling.

## When to Use

- Multi-step tasks requiring tool use
- Search + reasoning workflows
- Complex question answering with external data
- Tasks needing calculation, retrieval, or API calls

## Related Skills

- Optimize agents: [dspy-gepa-reflective](../dspy-gepa-reflective/SKILL.md)
- Define signatures: [dspy-signature-designer](../dspy-signature-designer/SKILL.md)
- Evaluate performance: [dspy-evaluation-suite](../dspy-evaluation-suite/SKILL.md)

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| `signature` | `str` | Task signature (e.g., "question -> answer") |
| `tools` | `list[callable]` | Available tools/functions |
| `max_iters` | `int` | Max reasoning steps (default: 20) |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `agent` | `dspy.ReAct` | Configured ReAct agent |

## Workflow

### Phase 1: Define Tools

Tools are Python functions with clear docstrings. The agent uses docstrings to understand tool capabilities:

```python
import dspy

def search(query: str) -> list[str]:
    """Search knowledge base for relevant information.

    Args:
        query: Search query string

    Returns:
        List of relevant text passages
    """
    retriever = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')
    results = retriever(query, k=3)
    return [r['text'] for r in results]

def calculate(expression: str) -> float:
    """Safely evaluate mathematical expressions.

    Args:
        expression: Math expression (e.g., "2 + 2", "sqrt(16)")

    Returns:
        Numerical result
    """
    try:
        interpreter = dspy.PythonInterpreter()
        return interpreter.execute(expression)
    except Exception as e:
        return f"Error: {e}"
```

### Phase 2: Create ReAct Agent

```python
# Configure LM
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))

# Create agent
agent = dspy.ReAct(
    signature="question -> answer",
    tools=[search, calculate],
    max_iters=5
)

# Use agent
result = agent(question="What is the population of Paris plus 1000?")
print(result.answer)
```

### Phase 3: Production Agent with Error Handling

```python
import dspy
import logging

logger = logging.getLogger(__name__)

class ResearchAgent(dspy.Module):
    """Production agent with error handling and logging."""

    def __init__(self, max_iters: int = 5):
        self.max_iters = max_iters
        self.agent = dspy.ReAct(
            signature="question -> answer",
            tools=[self.search, self.calculate, self.summarize],
            max_iters=max_iters
        )

    def search(self, query: str) -> list[str]:
        """Search for relevant documents."""
        try:
            retriever = dspy.ColBERTv2(
                url='http://20.102.90.50:2017/wiki17_abstracts'
            )
            results = retriever(query, k=5)
            return [r['text'] for r in results]
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return [f"Search unavailable: {e}"]

    def calculate(self, expression: str) -> str:
        """Evaluate mathematical expressions safely."""
        try:
            interpreter = dspy.PythonInterpreter()
            result = interpreter.execute(expression)
            return str(result)
        except Exception as e:
            logger.error(f"Calculation failed: {e}")
            return f"Error: {e}"

    def summarize(self, text: str) -> str:
        """Summarize long text into key points."""
        try:
            summarizer = dspy.Predict("text -> summary: str")
            return summarizer(text=text[:1000]).summary
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            return "Summarization unavailable"

    def forward(self, question: str) -> dspy.Prediction:
        """Execute agent with error handling."""
        try:
            return self.agent(question=question)
        except Exception as e:
            logger.error(f"Agent failed: {e}")
            return dspy.Prediction(answer=f"Error: {e}")

# Usage
agent = ResearchAgent(max_iters=6)
response = agent(question="What is the capital of France and its population?")
print(response.answer)
```

### Phase 4: Optimize with GEPA

ReAct agents benefit from reflective optimization:

```python
from dspy.evaluate import Evaluate

def feedback_metric(example, pred, trace=None, pred_name=None, pred_trace=None):
    """Provide textual feedback for GEPA."""
    is_correct = example.answer.lower() in pred.answer.lower()
    score = 1.0 if is_correct else 0.0
    feedback = "Correct." if is_correct else f"Expected '{example.answer}'. Check tool selection."
    return dspy.Prediction(score=score, feedback=feedback)

# Optimize agent
optimizer = dspy.GEPA(
    metric=feedback_metric,
    reflection_lm=dspy.LM("openai/gpt-4o"),
    auto="medium",
    enable_tool_optimization=True  # Also optimize tool docstrings
)

compiled = optimizer.compile(agent, trainset=trainset)
compiled.save("research_agent_optimized.json", save_program=False)
```

## Best Practices

1. **Clear tool docstrings** - Agent relies on docstrings to understand tool capabilities
2. **Error handling** - All tools should handle failures gracefully and return error messages
3. **Tool independence** - Test each tool separately before adding to agent
4. **Logging** - Track tool calls and agent reasoning for debugging
5. **Limit iterations** - Set reasonable `max_iters` to prevent infinite loops (default is 20, but 5-10 often sufficient for simpler tasks)

## Limitations

- ReAct works best with 3-7 tools; too many tools confuse the agent
- Not all LMs support tool calling equally well (GPT-4 > GPT-3.5)
- Agent may call tools unnecessarily or miss necessary calls
- Requires GEPA optimization for production quality
- Tool execution is sequential, not parallelized

## Official Documentation

- **DSPy Documentation**: https://dspy.ai/
- **DSPy GitHub**: https://github.com/stanfordnlp/dspy
- **ReAct Module**: https://dspy.ai/api/modules/ReAct/
- **Agents Tutorial**: https://dspy.ai/tutorials/agents/
