---
name: pydantic-ai-testing
description: Test PydanticAI agents using TestModel, FunctionModel, VCR cassettes, and inline snapshots. Use when writing unit tests, mocking LLM responses, or recording API interactions.
---

# Testing PydanticAI Agents

## TestModel (Deterministic Testing)

Use `TestModel` for tests without API calls:

```python
import pytest
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel

def test_agent_basic():
    agent = Agent('openai:gpt-4o')

    # Override with TestModel for testing
    result = agent.run_sync('Hello', model=TestModel())

    # TestModel generates deterministic output based on output_type
    assert isinstance(result.output, str)
```

## TestModel Configuration

```python
from pydantic_ai.models.test import TestModel

# Custom text output
model = TestModel(custom_output_text='Custom response')
result = agent.run_sync('Hello', model=model)
assert result.output == 'Custom response'

# Custom structured output (for output_type agents)
from pydantic import BaseModel

class Response(BaseModel):
    message: str
    score: int

agent = Agent('openai:gpt-4o', output_type=Response)
model = TestModel(custom_output_args={'message': 'Test', 'score': 42})
result = agent.run_sync('Hello', model=model)
assert result.output.message == 'Test'

# Seed for reproducible random output
model = TestModel(seed=42)

# Force tool calls
model = TestModel(call_tools=['my_tool', 'another_tool'])
```

## Override Context Manager

```python
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel

agent = Agent('openai:gpt-4o', deps_type=MyDeps)

def test_with_override():
    mock_deps = MyDeps(db=MockDB())

    with agent.override(model=TestModel(), deps=mock_deps):
        # All runs use TestModel and mock_deps
        result = agent.run_sync('Hello')
        assert result.output
```

## FunctionModel (Custom Logic)

For complete control over model responses:

```python
from pydantic_ai import Agent, ModelMessage, ModelResponse, TextPart
from pydantic_ai.models.function import AgentInfo, FunctionModel

def custom_model(
    messages: list[ModelMessage],
    info: AgentInfo
) -> ModelResponse:
    """Custom model that inspects messages and returns response."""
    # Access the last user message
    last_msg = messages[-1]

    # Return custom response
    return ModelResponse(parts=[TextPart('Custom response')])

agent = Agent(FunctionModel(custom_model))
result = agent.run_sync('Hello')
```

### FunctionModel with Tool Calls

```python
from pydantic_ai import ToolCallPart, ModelResponse
from pydantic_ai.models.function import AgentInfo, FunctionModel

def model_with_tools(
    messages: list[ModelMessage],
    info: AgentInfo
) -> ModelResponse:
    # First request: call a tool
    if len(messages) == 1:
        return ModelResponse(parts=[
            ToolCallPart(
                tool_name='get_data',
                args='{"id": 123}'
            )
        ])

    # After tool response: return final result
    return ModelResponse(parts=[TextPart('Done with tool result')])

agent = Agent(FunctionModel(model_with_tools))

@agent.tool_plain
def get_data(id: int) -> str:
    return f"Data for {id}"

result = agent.run_sync('Get data')
```

## VCR Cassettes (Recorded API Calls)

Record and replay real LLM API interactions:

```python
import pytest

@pytest.mark.vcr
def test_with_recorded_response():
    """Uses recorded cassette from tests/cassettes/"""
    agent = Agent('openai:gpt-4o')
    result = agent.run_sync('Hello')
    assert 'hello' in result.output.lower()

# To record/update cassettes:
# uv run pytest --record-mode=rewrite tests/test_file.py
```

Cassette files are stored in `tests/cassettes/` as YAML.

## Inline Snapshots

Assert expected outputs with auto-updating snapshots:

```python
from inline_snapshot import snapshot

def test_agent_output():
    result = agent.run_sync('Hello', model=TestModel())

    # First run: creates snapshot
    # Subsequent runs: asserts against it
    assert result.output == snapshot('expected output here')

# Update snapshots:
# uv run pytest --inline-snapshot=fix
```

## Testing Tools

```python
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.test import TestModel

def test_tool_is_called():
    agent = Agent('openai:gpt-4o')
    tool_called = False

    @agent.tool_plain
    def my_tool(x: int) -> str:
        nonlocal tool_called
        tool_called = True
        return f"Result: {x}"

    # Force TestModel to call the tool
    result = agent.run_sync(
        'Use my_tool',
        model=TestModel(call_tools=['my_tool'])
    )

    assert tool_called
```

## Testing with Dependencies

```python
from dataclasses import dataclass
from unittest.mock import AsyncMock

@dataclass
class Deps:
    api: ApiClient

def test_tool_with_deps():
    # Create mock dependency
    mock_api = AsyncMock()
    mock_api.fetch.return_value = {'data': 'test'}

    agent = Agent('openai:gpt-4o', deps_type=Deps)

    @agent.tool
    async def fetch_data(ctx: RunContext[Deps]) -> dict:
        return await ctx.deps.api.fetch()

    with agent.override(
        model=TestModel(call_tools=['fetch_data']),
        deps=Deps(api=mock_api)
    ):
        result = agent.run_sync('Fetch data')

    mock_api.fetch.assert_called_once()
```

## Capture Messages

Inspect all messages in a run:

```python
from pydantic_ai import Agent, capture_run_messages

agent = Agent('openai:gpt-4o')

with capture_run_messages() as messages:
    result = agent.run_sync('Hello', model=TestModel())

# Inspect captured messages
for msg in messages:
    print(msg)
```

## Testing Patterns Summary

| Scenario | Approach |
|----------|----------|
| Unit tests without API | `TestModel()` |
| Custom model logic | `FunctionModel(func)` |
| Recorded real responses | `@pytest.mark.vcr` |
| Assert output structure | `inline_snapshot` |
| Test tools are called | `TestModel(call_tools=[...])` |
| Mock dependencies | `agent.override(deps=...)` |

## pytest Configuration

Typical `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"  # For async tests
```

Run tests:
```bash
uv run pytest tests/test_agent.py -v
uv run pytest --inline-snapshot=fix  # Update snapshots
```
