---
name: pydantic-ai-dependency-injection
description: Implement dependency injection in PydanticAI agents using RunContext and deps_type. Use when agents need database connections, API clients, user context, or any external resources.
---

# PydanticAI Dependency Injection

## Core Pattern

Dependencies flow through `RunContext`:

```python
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext

@dataclass
class Deps:
    db: DatabaseConn
    api_client: HttpClient
    user_id: int

agent = Agent(
    'openai:gpt-4o',
    deps_type=Deps,  # Type for static analysis
)

@agent.tool
async def get_user_balance(ctx: RunContext[Deps]) -> float:
    """Get the current user's account balance."""
    return await ctx.deps.db.get_balance(ctx.deps.user_id)

# At runtime, provide deps
result = await agent.run(
    'What is my balance?',
    deps=Deps(db=db_conn, api_client=client, user_id=123)
)
```

## Defining Dependencies

Use dataclasses or Pydantic models:

```python
from dataclasses import dataclass
from pydantic import BaseModel

# Dataclass (recommended for simplicity)
@dataclass
class Deps:
    db: DatabaseConnection
    cache: CacheClient
    user_context: UserContext

# Pydantic model (if you need validation)
class Deps(BaseModel):
    api_key: str
    endpoint: str
    timeout: int = 30
```

## Accessing Dependencies

In tools and instructions:

```python
@agent.tool
async def query_database(ctx: RunContext[Deps], query: str) -> list[dict]:
    """Run a database query."""
    return await ctx.deps.db.execute(query)

@agent.instructions
async def add_user_context(ctx: RunContext[Deps]) -> str:
    user = await ctx.deps.db.get_user(ctx.deps.user_id)
    return f"User name: {user.name}, Role: {user.role}"

@agent.system_prompt
def add_permissions(ctx: RunContext[Deps]) -> str:
    return f"User has permissions: {ctx.deps.permissions}"
```

## Type Safety

Full type checking with generics:

```python
# Explicit agent type annotation
agent: Agent[Deps, OutputModel] = Agent(
    'openai:gpt-4o',
    deps_type=Deps,
    output_type=OutputModel,
)

# Now these are type-checked:
# - ctx.deps in tools is typed as Deps
# - result.output is typed as OutputModel
# - agent.run() requires deps: Deps
```

## No Dependencies Pattern

When you don't need dependencies:

```python
# Option 1: No deps_type (defaults to NoneType)
agent = Agent('openai:gpt-4o')
result = agent.run_sync('Hello')  # No deps needed

# Option 2: Explicit None for type checker
agent: Agent[None, str] = Agent('openai:gpt-4o')
result = agent.run_sync('Hello', deps=None)

# In tool_plain, no context access
@agent.tool_plain
def simple_calc(a: int, b: int) -> int:
    return a + b
```

## Complete Example

```python
from dataclasses import dataclass
from httpx import AsyncClient
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext

@dataclass
class WeatherDeps:
    client: AsyncClient
    api_key: str

class WeatherReport(BaseModel):
    location: str
    temperature: float
    conditions: str

agent: Agent[WeatherDeps, WeatherReport] = Agent(
    'openai:gpt-4o',
    deps_type=WeatherDeps,
    output_type=WeatherReport,
    instructions='You are a weather assistant.',
)

@agent.tool
async def get_weather(
    ctx: RunContext[WeatherDeps],
    city: str
) -> dict:
    """Fetch weather data for a city."""
    response = await ctx.deps.client.get(
        f'https://api.weather.com/{city}',
        headers={'Authorization': ctx.deps.api_key}
    )
    return response.json()

async def main():
    async with AsyncClient() as client:
        deps = WeatherDeps(client=client, api_key='secret')
        result = await agent.run('Weather in London?', deps=deps)
        print(result.output.temperature)
```

## Override for Testing

```python
from pydantic_ai.models.test import TestModel

# Create mock dependencies
mock_deps = Deps(
    db=MockDatabase(),
    api_client=MockClient(),
    user_id=999
)

# Override model and deps for testing
with agent.override(model=TestModel(), deps=mock_deps):
    result = agent.run_sync('Test prompt')
```

## Best Practices

1. **Keep deps immutable**: Use frozen dataclasses or Pydantic models
2. **Pass connections, not credentials**: Deps should hold initialized clients
3. **Type your agents**: Use `Agent[DepsType, OutputType]` for full type safety
4. **Scope deps appropriately**: Create deps at the start of a request, close after
