---
name: google-adk-python
description: Build AI agents with Google's Agent Development Kit (ADK) Python - an open-source toolkit for building, evaluating, and deploying AI agents. Features LlmAgent, workflow agents (sequential, parallel, loop), tool integration, multi-agent systems, and deployment to Vertex AI or Cloud Run.
license: MIT
---

# Google ADK Python

Open-source, code-first toolkit for building, evaluating, and deploying AI agents.

## When to Use

- Build AI agents with tool integration
- Create multi-agent systems with hierarchical coordination
- Implement workflow agents (sequential, parallel, loop)
- Integrate with Google Search, Code Execution, or custom tools
- Deploy to Vertex AI Agent Engine or Cloud Run
- Implement human-in-the-loop approval flows

## Installation

```bash
pip install google-adk
```

## Agent Types

### LlmAgent

LLM-powered agents with dynamic routing and adaptive behavior.

```python
from google.adk.agents import LlmAgent
from google.adk.tools import google_search

agent = LlmAgent(
    name="search_assistant",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant that searches the web.",
    tools=[google_search]
)
```

### SequentialAgent

Execute agents in defined order.

```python
from google.adk.agents import SequentialAgent

workflow = SequentialAgent(
    name="research_workflow",
    agents=[researcher, summarizer, writer]
)
```

### ParallelAgent

Run multiple agents concurrently.

```python
from google.adk.agents import ParallelAgent

parallel = ParallelAgent(
    name="parallel_research",
    agents=[web_researcher, paper_researcher]
)
```

## Multi-Agent System

```python
# Specialized agents
researcher = LlmAgent(
    name="Researcher",
    model="gemini-2.5-flash",
    tools=[google_search]
)

writer = LlmAgent(
    name="Writer",
    model="gemini-2.5-flash",
)

# Coordinator
coordinator = LlmAgent(
    name="Coordinator",
    model="gemini-2.5-flash",
    instruction="Delegate tasks to researcher and writer.",
    sub_agents=[researcher, writer]
)
```

## Custom Tools

```python
from google.adk.tools import Tool

def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two numbers."""
    return a + b

sum_tool = Tool.from_function(calculate_sum)
```

## Model Support

- gemini-2.5-flash (recommended)
- gemini-2.5-pro
- gemini-1.5-flash
- gemini-1.5-pro

## Best Practices

1. Code-first for version control and testing
2. Create specialized agents for specific domains
3. Use workflow agents for predictable pipelines
4. Implement confirmation flows for sensitive operations
5. Test agents systematically

## Resources

- GitHub: https://github.com/google/adk-python
- Docs: https://google.github.io/adk-docs/

## Credits

Source: https://github.com/mrgoonie/claudekit-skills
