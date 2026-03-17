---
name: scaffolding-openai-agents
description: |
  Builds AI agents using OpenAI Agents SDK with async/await patterns and multi-agent orchestration.
  Use when creating tutoring agents, building agent handoffs, implementing tool-calling agents, or orchestrating multiple specialists.
  Covers Agent class, Runner patterns, function tools, guardrails, and streaming responses.
  NOT when using raw OpenAI API without SDK or other agent frameworks like LangChain.
---

# Scaffolding OpenAI Agents

Build production AI agents using OpenAI Agents SDK with native async/await patterns.

## Quick Start

```bash
# Project setup
mkdir my-agent && cd my-agent
python -m venv .venv && source .venv/bin/activate
pip install openai-agents

# Set API key
export OPENAI_API_KEY=sk-...
```

```python
# main.py
import asyncio
from agents import Agent, Runner

agent = Agent(
    name="Python Tutor",
    instructions="You help students learn Python. Explain concepts clearly with examples."
)

async def main():
    result = await Runner.run(agent, "Explain list comprehensions")
    print(result.final_output)

asyncio.run(main())
```

## Agent Configuration

### Basic Agent

```python
from agents import Agent

tutor = Agent(
    name="Python Tutor",
    instructions="""You are an expert Python tutor.
    Explain concepts clearly with examples.
    Ask clarifying questions when needed.
    Provide practice exercises after explanations.""",
    model="gpt-4o"
)
```

### With Model Settings

```python
from agents import Agent, ModelSettings

agent = Agent(
    name="Creative Writer",
    instructions="Write creative stories based on prompts.",
    model="gpt-4o",
    model_settings=ModelSettings(
        temperature=0.9,
        max_tokens=2000
    )
)
```

### With Structured Output

```python
from pydantic import BaseModel
from agents import Agent

class CodeReview(BaseModel):
    issues: list[str]
    suggestions: list[str]
    score: int

reviewer = Agent(
    name="Code Reviewer",
    instructions="Review Python code for issues and improvements.",
    output_type=CodeReview  # Forces structured JSON output
)
```

## Runner Patterns

### Async Run (Primary)

```python
import asyncio
from agents import Agent, Runner

async def main():
    agent = Agent(name="Helper", instructions="Be helpful")

    # Single query
    result = await Runner.run(agent, "What is Python?")
    print(result.final_output)

    # With conversation history
    messages = [
        {"role": "user", "content": "My name is Alex"},
        {"role": "assistant", "content": "Nice to meet you, Alex!"},
        {"role": "user", "content": "What's my name?"}
    ]
    result = await Runner.run(agent, messages)
    print(result.final_output)  # "Your name is Alex"

asyncio.run(main())
```

### Sync Run (Simple Scripts)

```python
from agents import Agent, Runner

agent = Agent(name="Helper", instructions="Be helpful")
result = Runner.run_sync(agent, "Hello!")
print(result.final_output)
```

### Streaming Run

```python
import asyncio
from agents import Agent, Runner

async def main():
    agent = Agent(name="Storyteller", instructions="Tell engaging stories")

    result = Runner.run_streamed(agent, "Tell me a short story")

    async for event in result.stream_events():
        if hasattr(event, 'delta'):
            print(event.delta, end='', flush=True)

    print()  # Newline at end

asyncio.run(main())
```

### Conversation Continuation

```python
async def chat_session():
    agent = Agent(name="Tutor", instructions="You are a Python tutor")

    # First turn
    result1 = await Runner.run(agent, "Explain decorators")
    print(f"Tutor: {result1.final_output}")

    # Continue conversation
    messages = result1.to_input_list() + [
        {"role": "user", "content": "Show me an example"}
    ]
    result2 = await Runner.run(agent, messages)
    print(f"Tutor: {result2.final_output}")
```

## Function Tools

### Basic Tool

```python
from agents import Agent, function_tool

@function_tool
def get_current_time() -> str:
    """Get the current time."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

@function_tool
def calculate(expression: str) -> float:
    """Calculate a mathematical expression.

    Args:
        expression: A valid Python math expression like "2 + 2" or "10 * 5"
    """
    return eval(expression)  # Use safe_eval in production

agent = Agent(
    name="Assistant",
    instructions="Help with calculations and time queries.",
    tools=[get_current_time, calculate]
)
```

### Async Tool

```python
import httpx
from agents import Agent, function_tool

@function_tool
async def fetch_weather(city: str) -> str:
    """Fetch current weather for a city.

    Args:
        city: The city name to get weather for
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://wttr.in/{city}?format=3"
        )
        return response.text

agent = Agent(
    name="Weather Bot",
    instructions="Provide weather information.",
    tools=[fetch_weather]
)
```

### Tool with Pydantic Types

```python
from pydantic import BaseModel
from agents import Agent, function_tool

class SearchQuery(BaseModel):
    query: str
    max_results: int = 10

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str

@function_tool
async def search_docs(params: SearchQuery) -> list[SearchResult]:
    """Search documentation for a query."""
    # Implementation
    return [SearchResult(
        title="Python Tutorial",
        url="https://docs.python.org",
        snippet="Official Python documentation..."
    )]

agent = Agent(
    name="Doc Search",
    instructions="Search Python documentation.",
    tools=[search_docs]
)
```

## Multi-Agent Patterns

### Handoffs (Recommended for Routing)

```python
from agents import Agent, Runner

# Specialist agents
concepts_agent = Agent(
    name="Concepts Tutor",
    handoff_description="Explains Python concepts and fundamentals",
    instructions="Explain Python concepts clearly with examples."
)

debug_agent = Agent(
    name="Debug Helper",
    handoff_description="Helps debug Python code errors",
    instructions="Help diagnose and fix Python errors."
)

exercise_agent = Agent(
    name="Exercise Generator",
    handoff_description="Creates practice problems and exercises",
    instructions="Generate practice problems with solutions."
)

# Triage agent with handoffs
triage_agent = Agent(
    name="Triage",
    instructions="""Route student questions to the right specialist:
    - Concepts questions → Concepts Tutor
    - Error/bug questions → Debug Helper
    - Practice requests → Exercise Generator

    Analyze the question and hand off to the appropriate agent.""",
    handoffs=[concepts_agent, debug_agent, exercise_agent]
)

async def main():
    # Question gets routed automatically
    result = await Runner.run(
        triage_agent,
        "I'm getting a KeyError in my dictionary code"
    )
    print(result.final_output)  # Handled by debug_agent
```

### Agents as Tools (Orchestration)

```python
from agents import Agent, Runner

# Create specialist agents
researcher = Agent(
    name="Researcher",
    instructions="Research topics thoroughly."
)

writer = Agent(
    name="Writer",
    instructions="Write clear, engaging content."
)

# Manager uses agents as tools
manager = Agent(
    name="Content Manager",
    instructions="""Coordinate research and writing:
    1. Use researcher tool to gather information
    2. Use writer tool to create content""",
    tools=[
        researcher.as_tool(
            tool_name="research",
            tool_description="Research a topic"
        ),
        writer.as_tool(
            tool_name="write",
            tool_description="Write content about a topic"
        )
    ]
)

async def main():
    result = await Runner.run(
        manager,
        "Create a blog post about async Python"
    )
    print(result.final_output)
```

## Guardrails

### Input Validation

```python
from agents import Agent, input_guardrail, GuardrailFunctionOutput

@input_guardrail
async def check_homework_topic(context, agent, input_text: str) -> GuardrailFunctionOutput:
    """Ensure questions are homework-related."""
    keywords = ["python", "code", "programming", "function", "class", "error"]

    if not any(kw in input_text.lower() for kw in keywords):
        return GuardrailFunctionOutput(
            output_info="Not a programming question",
            tripwire_triggered=True
        )

    return GuardrailFunctionOutput(
        output_info="Valid programming question",
        tripwire_triggered=False
    )

tutor = Agent(
    name="Python Tutor",
    instructions="Help with Python homework.",
    input_guardrails=[check_homework_topic]
)
```

### Output Validation

```python
from agents import Agent, output_guardrail, GuardrailFunctionOutput

@output_guardrail
async def check_no_solutions(context, agent, output: str) -> GuardrailFunctionOutput:
    """Ensure we don't give complete homework solutions."""
    solution_indicators = ["here's the complete", "full solution", "copy this code"]

    if any(ind in output.lower() for ind in solution_indicators):
        return GuardrailFunctionOutput(
            output_info="Contains complete solution",
            tripwire_triggered=True
        )

    return GuardrailFunctionOutput(
        output_info="Output is appropriate",
        tripwire_triggered=False
    )

tutor = Agent(
    name="Python Tutor",
    instructions="Guide students without giving full solutions.",
    output_guardrails=[check_no_solutions]
)
```

## Context Injection

### Shared State Across Agents

```python
from dataclasses import dataclass
from agents import Agent, Runner, function_tool, RunContextWrapper

@dataclass
class TutoringContext:
    student_id: str
    session_id: str
    topics_covered: list[str]
    difficulty_level: str = "beginner"

@function_tool
def log_topic(wrapper: RunContextWrapper[TutoringContext], topic: str) -> str:
    """Log a topic as covered in this session."""
    wrapper.context.topics_covered.append(topic)
    return f"Logged: {topic}"

tutor = Agent(
    name="Python Tutor",
    instructions="Teach Python, tracking topics covered.",
    tools=[log_topic]
)

async def main():
    ctx = TutoringContext(
        student_id="student-123",
        session_id="session-456",
        topics_covered=[]
    )

    result = await Runner.run(
        tutor,
        "Teach me about loops",
        context=ctx
    )

    print(f"Topics covered: {ctx.topics_covered}")
```

## Project Structure

```
learnflow-agents/
├── agents/
│   ├── __init__.py
│   ├── triage.py          # Routing agent
│   ├── concepts.py        # Concepts specialist
│   ├── debug.py           # Debug specialist
│   └── exercise.py        # Exercise generator
├── tools/
│   ├── __init__.py
│   ├── code_runner.py     # Execute Python safely
│   └── search.py          # Search documentation
├── guardrails/
│   ├── __init__.py
│   ├── input.py           # Input validation
│   └── output.py          # Output validation
├── main.py                # FastAPI integration
└── pyproject.toml
```

## FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents import Agent, Runner

app = FastAPI()

# Initialize agents
triage = Agent(
    name="Triage",
    instructions="Route questions to specialists",
    handoffs=[concepts_agent, debug_agent]
)

class Question(BaseModel):
    text: str
    session_id: str

class Answer(BaseModel):
    response: str
    agent_used: str

@app.post("/ask", response_model=Answer)
async def ask_question(question: Question):
    try:
        result = await Runner.run(triage, question.text)
        return Answer(
            response=result.final_output,
            agent_used=result.last_agent.name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask/stream")
async def ask_stream(question: Question):
    from fastapi.responses import StreamingResponse

    async def generate():
        result = Runner.run_streamed(triage, question.text)
        async for event in result.stream_events():
            if hasattr(event, 'delta'):
                yield event.delta

    return StreamingResponse(generate(), media_type="text/plain")
```

## Tracing & Debugging

### View Traces

Traces available at: https://platform.openai.com/traces

### Custom Tracing

```python
from agents import Runner, RunConfig

config = RunConfig(
    workflow_name="tutoring-session",
    trace_id="custom-trace-123"
)

result = await Runner.run(agent, "Hello", run_config=config)
```

## Verification

Run: `python scripts/verify.py`

## Related Skills

- `configuring-dapr-pubsub` - Agent-to-agent messaging
- `scaffolding-fastapi-dapr` - FastAPI backend integration
- `streaming-llm-responses` - Response streaming patterns
- `building-chat-interfaces` - Frontend chat UI
