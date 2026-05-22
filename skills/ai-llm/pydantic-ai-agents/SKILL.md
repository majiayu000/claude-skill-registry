---
name: pydantic-ai-agents
description: "Build and debug Pydantic AI agents using best practices for dependencies, dynamic system prompts, tools, and structured output validation. Use when the user wants to: (1) Create a new Pydantic AI agent, (2) Debug or fix an existing agent, (3) Add features like tools, validators, or dynamic prompts, (4) Integrate OpenRouter for multi-model access, (5) Add Logfire for debugging/observability, (6) Structure agent architecture with dependency injection."
---

# Pydantic AI Reference Skill

## Pydantic AI Developer Guide

### 0. Environment Setup

Store API keys in a `.env` file and add it to `.gitignore`:
```
OPENAI_API_KEY=your_key
OPENROUTER_API_KEY=your_key
LOGFIRE_API_KEY=your_key
```

Load with `python-dotenv`: `load_dotenv()`. Never hardcode keys in source code.

### 1. Core Architecture

Pydantic AI agents have four key components:

#### Dependencies (deps):
- **Reference**: `references/01_dependencies.py`
- Use dataclasses to hold API keys, database connections, and user context
- Never use global variables for state

#### System Prompts (system_prompt):
- **Reference**: `references/02_prompts.py`
- Make prompts dynamic using `@agent.system_prompt` decorator
- Inject data from `ctx.deps` into the prompt string

#### Tools (@agent.tool):
- **Reference**: `references/03_tools.py`
- **IMPORTANT**: When `deps_type` is set on the agent, ALL tools must have `ctx: RunContext` as first parameter - even if they don't use it
- Use `ctx.deps` to access injected dependencies

#### Validators (output_type):
- **Reference**: `references/04_validators.py`
- Use Pydantic models to enforce structured output
- Use `@field_validator` for logic checks

### 2. Promoting Instructions (System Prompt Engineering)

Follow these rules when writing system prompts:

1. **Role Definition**: Start with "You are a specialized agent for..."
2. **Context Awareness**: Explicitly mention the data available in the dependencies.
   - **Bad**: "I help users."
   - **Good**: "I help user {ctx.deps.user_name} (ID: {ctx.deps.user_id}) manage their account."
3. **Tool Coercion**: If tools are defined, instruct the model when to use them.
   - **Example**: "Use the lookup_order tool immediately if the user provides an order ID."
4. **Failure Modes**: Define what to do if a tool fails or data is missing.
   - **Example**: "If the database returns no results, politely ask the user for clarification."

### 3. OpenRouter Integration

**Reference**: `references/06_openrouter.py`

OpenRouter is an API gateway that provides access to multiple LLM models through a unified API.

#### Key Points:
- OpenRouter uses OpenAI-compatible API format
- Set `OPENROUTER_API_KEY` in your `.env` file
- Use `OpenAIProvider` with `base_url='https://openrouter.ai/api/v1'`
- Access to models like GPT-4o-mini, Claude, Llama, and more
- See https://openrouter.ai/models for available models

#### Example Setup:
```python
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

provider = OpenAIProvider(
    api_key=os.getenv('OPENROUTER_API_KEY'),
    base_url='https://openrouter.ai/api/v1'
)

model = OpenAIChatModel(
    model_name='gpt-4o-mini',
    provider=provider
)
```

### 4. Debugging with Logfire

**Reference**: `references/07_logfire.py`

Logfire is a platform tightly integrated with Pydantic AI for debugging and observability.

#### Key Features:
- **Spans**: Track execution time and context of operations
- **Logging Levels**: notice, info, debug, warn, error, fatal
- **Exception Tracking**: Capture stack traces and error context
- **Tracing**: Visualize agent execution flow

#### Setup:
1. Get API key from https://logfire.pydantic.dev/
2. Set `LOGFIRE_API_KEY` in your `.env` file
3. Configure: `logfire.configure(token=LOGFIRE_API_KEY)`

#### Usage Pattern:
```python
with logfire.span('Calling Agent') as span:
    result = agent.run_sync("user query")
    span.set_attribute('result', result.output)
    logfire.info('{result=}', result=result.output)
```

### 5. Advanced Patterns

#### Streaming Responses:
- **Reference**: `references/08_streaming.py`
- Use `agent.run_stream()` for real-time output
- Stream with `async for chunk in response.stream_text()`
- Get final result with `await response.get_output()`

#### Result Validators & Retry:
- **Reference**: `references/09_result_validators.py`
- Use `@agent.output_validator` for custom validation
- Raise `ModelRetry("feedback")` to trigger retry with guidance
- Set `retries=3` on Agent for auto-retry on validation failure

#### Model Settings:
- **Reference**: `references/10_model_settings.py`
- Pass `model_settings={'temperature': 0.7, 'max_tokens': 500}` to `agent.run()`
- Use low temperature (0.0-0.3) for factual tasks
- Use high temperature (0.7-1.0) for creative tasks

#### Multi-Agent Systems:
- **Reference**: `references/11_multi_agent.py`
- Orchestrate multiple specialized agents for complex tasks
- Use `asyncio.gather()` for parallel agent execution
- Implement routing for intent-based agent selection

### 6. Conversation History (Persistent Memory)

**Reference**: `references/12_conversation_history.py`

By default, each `agent.run()` call is stateless - the agent has no memory of previous interactions. To maintain conversation context across multiple turns, you must pass `message_history`.

#### Key Concepts:

1. **Get messages from result**: After each `run()`, call `result.all_messages()` to get the full conversation
2. **Pass history to next call**: Use `message_history=` parameter on subsequent `run()` calls
3. **Messages are immutable**: Each call returns a NEW list; the original is not modified

#### Basic Pattern:

```python
from pydantic_ai import Agent, ModelMessage

agent = Agent(model=model, system_prompt="You are helpful.")

# First turn - no history
result1 = agent.run_sync("My name is Alice")
messages: list[ModelMessage] = result1.all_messages()

# Second turn - pass history so agent remembers
result2 = agent.run_sync(
    "What is my name?",
    message_history=messages  # Agent now knows "Alice"
)
messages = result2.all_messages()  # Updated history

# Third turn - continue the conversation
result3 = agent.run_sync(
    "Tell me a joke about my name",
    message_history=messages
)
```

#### Function Signature Pattern:

When building conversation loops, return both the output and messages:

```python
from pydantic_ai import Agent, ModelMessage

def run_agent_with_history(
    user_input: str,
    message_history: list[ModelMessage] | None = None,
) -> tuple[str, list[ModelMessage]]:
    """Run agent and return output + updated history."""
    result = agent.run_sync(
        user_input,
        message_history=message_history or [],
    )
    return result.output, result.all_messages()

# Usage in a conversation loop
history = []
while True:
    user_input = input("You: ")
    response, history = run_agent_with_history(user_input, history)
    print(f"Agent: {response}")
```

#### Converting Custom Message Types:

If you store conversation history in your own format (e.g., database), convert to Pydantic AI format:

```python
from datetime import timezone
from pydantic_ai import ModelMessage
from pydantic_ai.messages import (
    ModelRequest, ModelResponse,
    UserPromptPart, TextPart
)

def convert_to_model_messages(my_messages: list[MyMessage]) -> list[ModelMessage]:
    """Convert custom message format to Pydantic AI format."""
    result: list[ModelMessage] = []

    for msg in my_messages:
        # Ensure timezone-aware timestamp
        ts = msg.timestamp.replace(tzinfo=timezone.utc) if msg.timestamp.tzinfo is None else msg.timestamp

        if msg.role == "user":
            result.append(ModelRequest(
                parts=[UserPromptPart(content=msg.content, timestamp=ts)],
                kind="request",
            ))
        elif msg.role == "assistant":
            result.append(ModelResponse(
                parts=[TextPart(content=msg.content)],
                kind="response",
                timestamp=ts,
            ))

    return result
```

#### Important Notes:

- **ModelMessage is a union type**: It's `ModelRequest | ModelResponse`, not a class you instantiate directly
- **User messages** → `ModelRequest` with `UserPromptPart`
- **Assistant messages** → `ModelResponse` with `TextPart`
- **Timestamps must be timezone-aware**: Use `timezone.utc`
- **System prompt is NOT in message_history**: It's set on the Agent and injected automatically

### 7. Testing Best Practices

#### Async/Sync Test Separation

**Warning**: When testing Pydantic AI agents, do NOT mix sync and async tests in the same file when using module-level agents.

**Problem**: Module-level agents create httpx clients at import time. When sync tests call `run_sync()`, they create/destroy temporary event loops which can corrupt the httpx connection pool. Subsequent async tests then fail with `Connection error`.

**Solution**: Separate async and sync tests into different files:

```python
# tests/test_agent_sync.py
from src.agent import run_agent_sync

def test_sync_behavior():
    result = run_agent_sync("input")
    assert result.field == expected

# tests/test_agent_async.py (SEPARATE FILE)
# Does NOT import run_agent_sync!
import pytest
from pydantic_ai import Agent

@pytest.mark.asyncio
async def test_async_behavior():
    # Create fresh agent inside test
    agent = Agent(model=model, output_type=Response)
    result = await agent.run("input")
    assert result.output.field == expected
```

**Alternative**: Convert all tests to async to use the same event loop consistently.

### 8. Usage

Build a new agent by:
1. Reading the requirement
2. Selecting the relevant components from the `references/` directory
3. Combining them into a single file following the pattern in `references/05_main.py`
4. Using OpenRouter (`references/06_openrouter.py`) for multi-model access
5. Adding Logfire (`references/07_logfire.py`) for debugging and monitoring
6. Adding conversation history (`references/12_conversation_history.py`) for multi-turn conversations
7. Adding advanced patterns (streaming, validators, multi-agent) as needed

### 9. Complete Example

See `references/05_main.py` for a complete working agent that demonstrates all patterns.
