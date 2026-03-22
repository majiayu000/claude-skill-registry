---
name: openai-agents
description: "Expert guidance for building AI agents with the OpenAI Agents SDK, from simple single-agent systems to complex multi-agent workflows. Use when working with: (1) Creating AI agents with tools and structured outputs, (2) Multi-agent orchestration with handoffs or manager patterns, (3) Agent guardrails and validation, (4) Conversation history with sessions, (5) Tracing and debugging agent workflows, (6) Tool integration and context management, (7) Production-ready agent systems. Supports async Python with comprehensive examples and patterns."
---

# OpenAI Agents SDK

Build AI agent systems from simple single-agent tools to complex multi-agent orchestrations using the official OpenAI Agents SDK.

## Installation and Setup

Install the SDK:

```bash
pip install openai-agents
```

Set your API key:

```bash
export OPENAI_API_KEY=sk-...
```

All agent workflows are asynchronous. Use `asyncio.run()` or `await` in async contexts:

```python
import asyncio
from agents import Agent, Runner

async def main():
    agent = Agent(name="Assistant", instructions="Be helpful")
    result = await Runner.run(agent, "Hello!")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

## Agent Development Workflow

Follow this progression based on complexity:

**1. Single Agent** → Start here for straightforward tasks (Q&A, analysis, generation)
**2. Agent with Tools** → Add when agents need to fetch data or perform actions
**3. Agent with Structured Output** → Use when you need validated, typed responses
**4. Multi-Agent System** → Scale when tasks require specialization or orchestration

## Quick Start: Single Agent

Create a basic agent with custom instructions:

```python
from agents import Agent, Runner
import asyncio

agent = Agent(
    name="Math Tutor",
    instructions="Help with math problems. Explain step-by-step.",
    model="gpt-4o"  # Optional: defaults to gpt-4o
)

async def main():
    result = await Runner.run(agent, "What is 15% of 200?")
    print(result.final_output)

asyncio.run(main())
```

## Adding Tools to Agents

Use the `@function_tool` decorator to give agents capabilities:

```python
from agents import Agent, Runner, function_tool
import asyncio

@function_tool
def get_weather(city: str) -> str:
    """Get current weather for a city.

    Args:
        city: The city name to check weather for
    """
    # In production, call a real weather API
    return f"Weather in {city}: Sunny, 72°F"

@function_tool
def convert_temperature(fahrenheit: float) -> str:
    """Convert Fahrenheit to Celsius.

    Args:
        fahrenheit: Temperature in Fahrenheit
    """
    celsius = (fahrenheit - 32) * 5/9
    return f"{fahrenheit}°F = {celsius:.1f}°C"

agent = Agent(
    name="Weather Assistant",
    instructions="Help users with weather information and temperature conversions.",
    tools=[get_weather, convert_temperature]
)

async def main():
    result = await Runner.run(
        agent,
        "What's the weather in Seattle and convert that temperature to Celsius?"
    )
    print(result.final_output)

asyncio.run(main())
```

**Key points:**
- Docstrings become tool descriptions (auto-parsed)
- Type hints generate JSON schema automatically
- Tools can be sync or async functions
- Multiple tools can be called in parallel (default behavior)

## Structured Output with Pydantic

When you need validated, typed responses instead of free-form text:

```python
from agents import Agent, Runner
from pydantic import BaseModel, Field
import asyncio

class CalendarEvent(BaseModel):
    name: str = Field(description="Event name")
    date: str = Field(description="Event date in YYYY-MM-DD format")
    participants: list[str] = Field(description="List of participant names")

agent = Agent(
    name="Calendar Extractor",
    instructions="Extract calendar events from text",
    output_type=CalendarEvent  # Forces structured output
)

async def main():
    result = await Runner.run(
        agent,
        "Schedule a meeting with John and Sarah on 2026-03-15 to discuss Q1 results"
    )

    # Access typed output
    event = result.final_output_as(CalendarEvent)
    print(f"Event: {event.name}")
    print(f"Date: {event.date}")
    print(f"Participants: {', '.join(event.participants)}")

asyncio.run(main())
```

## Multi-Agent Systems

Two primary patterns for multi-agent architectures:

### Pattern 1: Manager/Orchestrator (Agents as Tools)

Central manager controls the workflow and delegates to specialized sub-agents:

```python
from agents import Agent, Runner
import asyncio

# Specialized agents
spanish_translator = Agent(
    name="Spanish Translator",
    instructions="Translate to Spanish. Return only the translation.",
)

french_translator = Agent(
    name="French Translator",
    instructions="Translate to French. Return only the translation.",
)

# Manager agent using specialists as tools
manager = Agent(
    name="Translation Manager",
    instructions="Use translation tools to translate messages.",
    tools=[
        spanish_translator.as_tool(
            tool_name="translate_spanish",
            tool_description="Translate text to Spanish"
        ),
        french_translator.as_tool(
            tool_name="translate_french",
            tool_description="Translate text to French"
        ),
    ],
)

async def main():
    result = await Runner.run(
        manager,
        "Translate 'Good morning' to Spanish and French"
    )
    print(result.final_output)

asyncio.run(main())
```

**When to use:** Manager retains control, coordinates multiple sub-tasks, aggregates results.

### Pattern 2: Peer Handoffs

Agents hand off control to specialized peers:

```python
from agents import Agent, Runner
import asyncio

# Specialist agents
math_tutor = Agent(
    name="Math Tutor",
    handoff_description="Expert in mathematics and problem-solving",
    instructions="Explain math concepts clearly with examples.",
)

history_tutor = Agent(
    name="History Tutor",
    handoff_description="Expert in historical events and context",
    instructions="Explain historical events with context and significance.",
)

# Triage agent routes to specialists
triage = Agent(
    name="Triage Agent",
    instructions="Route student questions to the appropriate tutor.",
    handoffs=[math_tutor, history_tutor]  # Peer agents
)

async def main():
    result = await Runner.run(
        triage,
        "Who was the first president of the United States?"
    )
    print(result.final_output)

asyncio.run(main())
```

**When to use:** Specialized workflows, conversational handoffs, decentralized control.

For detailed multi-agent patterns, see [references/multi-agent-patterns.md](references/multi-agent-patterns.md).

## Guardrails for Safety and Validation

Protect your agents with input and output guardrails:

```python
from agents import Agent, Runner, InputGuardrail, GuardrailFunctionOutput
from agents.exceptions import InputGuardrailTripwireTriggered
from pydantic import BaseModel
import asyncio

class HomeworkCheck(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Homework Checker",
    instructions="Determine if the user is asking about homework.",
    output_type=HomeworkCheck,
)

async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    check = result.final_output_as(HomeworkCheck)

    return GuardrailFunctionOutput(
        output_info=check,
        tripwire_triggered=not check.is_homework  # Block non-homework
    )

tutor_agent = Agent(
    name="Homework Tutor",
    instructions="Help with homework. Don't do it for them.",
    input_guardrails=[InputGuardrail(guardrail_function=homework_guardrail)]
)

async def main():
    try:
        result = await Runner.run(tutor_agent, "What's the capital of France?")
        print(result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("⛔ Input blocked by guardrail:", e)

asyncio.run(main())
```

For comprehensive guardrail patterns, see [references/guardrails.md](references/guardrails.md).

## Session Management for Conversation Memory

Enable multi-turn conversations with automatic history:

```python
from agents import Agent, Runner, SQLiteSession
import asyncio

agent = Agent(
    name="Assistant",
    instructions="Be helpful and concise.",
)

async def main():
    # Session persists conversation history
    session = SQLiteSession("user_123", "conversations.db")

    # Turn 1
    result1 = await Runner.run(
        agent,
        "What city is the Golden Gate Bridge in?",
        session=session
    )
    print(f"Turn 1: {result1.final_output}")

    # Turn 2 - Agent remembers previous context
    result2 = await Runner.run(
        agent,
        "What state is that in?",  # "that" refers to San Francisco
        session=session
    )
    print(f"Turn 2: {result2.final_output}")

asyncio.run(main())
```

For session patterns and multi-agent session sharing, see [references/sessions.md](references/sessions.md).

## Context Management

Share local context (not sent to LLM) across tools:

```python
from agents import Agent, Runner, RunContextWrapper, function_tool
from dataclasses import dataclass
import asyncio

@dataclass
class UserInfo:
    name: str
    user_id: int

@function_tool
async def get_user_data(ctx: RunContextWrapper[UserInfo]) -> str:
    """Fetch user-specific data."""
    return f"User {ctx.context.name} (ID: {ctx.context.user_id}) has 5 orders"

agent = Agent[UserInfo](
    name="Customer Service",
    tools=[get_user_data],
)

async def main():
    user = UserInfo(name="Alice", user_id=12345)

    result = await Runner.run(
        agent,
        "How many orders do I have?",
        context=user  # Shared across all tool calls
    )
    print(result.final_output)

asyncio.run(main())
```

## Error Handling

Handle common exceptions:

```python
from agents.exceptions import (
    MaxTurnsExceeded,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered
)

async def run_agent_safely(agent, user_input):
    try:
        result = await Runner.run(
            agent,
            user_input,
            max_turns=10  # Prevent infinite loops
        )
        return result.final_output
    except MaxTurnsExceeded:
        return "⚠️ Agent exceeded maximum turns. Task too complex."
    except InputGuardrailTripwireTriggered as e:
        return f"⛔ Input blocked: {e.guardrail_result.output.output_info}"
    except OutputGuardrailTripwireTriggered as e:
        return f"⛔ Output blocked: {e.guardrail_result.output.output_info}"
```

## Tracing and Debugging

Tracing is enabled by default. View traces at the OpenAI Traces dashboard:

```python
from agents.tracing.traces import trace

# Add metadata to traces
with trace(
    "Customer Support",
    group_id="chat_456",
    metadata={"customer": "user_789"}
):
    result = await Runner.run(agent, query)
```

Disable tracing globally:
```bash
export OPENAI_AGENTS_DISABLE_TRACING=1
```

Or per-run:
```python
from agents.run import RunConfig

result = await Runner.run(
    agent,
    input_text,
    run_config=RunConfig(tracing_disabled=True)
)
```

For advanced tracing and hooks, see [references/advanced.md](references/advanced.md).

## Reference Documentation

- **[single-agent-patterns.md](references/single-agent-patterns.md)** - Tools, structured outputs, model settings
- **[multi-agent-patterns.md](references/multi-agent-patterns.md)** - Handoffs, orchestration, agents as tools
- **[guardrails.md](references/guardrails.md)** - Input/output validation, tripwires
- **[sessions.md](references/sessions.md)** - Conversation memory, multi-agent sharing
- **[advanced.md](references/advanced.md)** - Tracing, hooks, streaming, custom configs

## Starter Templates

Quick-start templates in `assets/`:
- **hello-world-agent/** - Minimal single agent with tools
- **multi-agent-workflow/** - Complete triage + specialist pattern

## Common Patterns Summary

| Use Case | Pattern | Key Components |
|----------|---------|----------------|
| Simple Q&A | Single agent | `Agent` + `Runner.run()` |
| Data fetching | Agent + tools | `@function_tool` decorator |
| Typed responses | Structured output | `output_type=PydanticModel` |
| Task coordination | Manager pattern | `agent.as_tool()` |
| Specialized routing | Peer handoffs | `handoffs=[agent1, agent2]` |
| Input validation | Input guardrails | `input_guardrails=[...]` |
| Multi-turn chat | Sessions | `SQLiteSession` |
| Shared state | Context | `RunContextWrapper[T]` |

## Best Practices

1. **Start simple** - Single agent first, add complexity as needed
2. **Use type hints** - Enables automatic tool schema generation
3. **Write clear docstrings** - Becomes tool descriptions for the LLM
4. **Set max_turns** - Prevent infinite loops in production
5. **Use sessions** - Enable conversation memory for chat applications
6. **Add guardrails** - Validate inputs/outputs for safety-critical applications
7. **Enable tracing** - Essential for debugging multi-agent workflows
8. **Handle exceptions** - Catch `MaxTurnsExceeded` and guardrail exceptions
