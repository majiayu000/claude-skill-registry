---
name: building-with-openai-agents
description: Use when building AI agents with OpenAI's Agents SDK. Triggers include creating agents, implementing tools, multi-agent handoffs, guardrails, MCP integration, tracing. Also for using LiteLLM to run agents on free/alternative models (Anthropic, Gemini). NOT for general OpenAI API usage (use openai-python SDK docs instead).
---

# Building with OpenAI Agents SDK

Production-ready agent framework with minimal abstractions, released March 2025.

## Persona

You are an OpenAI Agents SDK expert with production experience. You understand:
- Official SDK patterns from openai-agents-python
- LiteLLM integration for alternative model providers
- MCP (Model Context Protocol) integration patterns
- Multi-agent orchestration with handoffs
- Production guardrails and safety patterns

## Quick Start

### Installation

```bash
pip install openai-agents
export OPENAI_API_KEY=sk-...
```

For alternative models (free/low-cost):
```bash
pip install "openai-agents[litellm]"
```

### Hello World

```python
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant."
)

result = Runner.run_sync(agent, "Hello!")
print(result.final_output)
```

### With LiteLLM (Free Models)

```python
from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel

# Use any of 100+ models via LiteLLM
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model=LitellmModel(
        model="anthropic/claude-3-5-sonnet-20240620",
        api_key="your-anthropic-key"
    )
)

result = await Runner.run(agent, "Hello!")
```

Supported prefixes: `anthropic/`, `gemini/`, `bedrock/`, `azure/`, `mistral/`

## Core Primitives

| Primitive | Purpose |
|-----------|---------|
| **Agent** | LLM with instructions, tools, handoffs |
| **Tool** | Python function the agent can call |
| **Handoff** | Transfer control to another agent |
| **Guardrail** | Validate input/output before processing |
| **Session** | Automatic conversation history |
| **Runner** | Executes the agent loop |

## Creating Agents

```python
from agents import Agent

agent = Agent(
    name="Customer Support",
    instructions="You help customers with their orders.",
    model="gpt-4o",  # or use LitellmModel
    tools=[get_order_status, create_refund],
    handoffs=[billing_agent, shipping_agent],
    output_type=OrderResponse,  # Structured output
)
```

### Dynamic Instructions

```python
def dynamic_instructions(context, agent):
    user = context.context.user_name
    return f"You are helping {user} with their account."

agent = Agent(
    name="Support",
    instructions=dynamic_instructions
)
```

## Function Tools

### Basic Tool

```python
from agents import function_tool

@function_tool
def get_weather(city: str) -> str:
    """Get weather for a city.

    Args:
        city: The city name.
    """
    return f"Weather in {city}: Sunny, 72F"
```

### Async Tool

```python
@function_tool
async def fetch_order(order_id: str) -> dict:
    """Fetch order details from database."""
    order = await db.orders.get(order_id)
    return order.dict()
```

### Tool with Pydantic

```python
from pydantic import BaseModel

class Location(BaseModel):
    city: str
    country: str = "USA"

@function_tool
def search_restaurants(location: Location, cuisine: str) -> list:
    """Search restaurants by location and cuisine."""
    return [...]
```

### Tool Error Handling

```python
def custom_error(e: Exception) -> str:
    return f"Tool failed: {str(e)}. Try a different approach."

@function_tool(failure_error_function=custom_error)
def risky_operation(data: str) -> str:
    """Perform risky operation."""
    ...
```

## Multi-Agent Handoffs

### Basic Handoff

```python
from agents import Agent, handoff

billing_agent = Agent(
    name="Billing Agent",
    instructions="Handle billing questions."
)

support_agent = Agent(
    name="Support Agent",
    instructions="Handle general support.",
    handoffs=[billing_agent]  # Can hand off to billing
)
```

### Handoff with Callback

```python
from pydantic import BaseModel
from agents import handoff, RunContextWrapper

class EscalationData(BaseModel):
    reason: str
    priority: str

async def on_escalate(ctx: RunContextWrapper, data: EscalationData):
    await log_escalation(data.reason, data.priority)

escalation_handoff = handoff(
    agent=escalation_agent,
    on_handoff=on_escalate,
    input_type=EscalationData,
    tool_name_override="escalate_to_human"
)
```

### Two Multi-Agent Patterns

**Pattern 1: Manager (Agents as Tools)**
- Central orchestrator invokes sub-agents as tools
- Orchestrator retains control
- Best for: predictable workflows, classification

```python
# Sub-agent as tool
research_agent = Agent(name="Researcher", ...)
writer_agent = Agent(name="Writer", ...)

manager = Agent(
    name="Manager",
    tools=[
        research_agent.as_tool(
            tool_name="do_research",
            tool_description="Research a topic"
        ),
        writer_agent.as_tool(
            tool_name="write_content",
            tool_description="Write content"
        )
    ]
)
```

**Pattern 2: Handoffs (Peer Agents)**
- Specialized agents hand off to each other
- Receiving agent takes full control
- Best for: customer support flows, expert routing

```python
triage_agent = Agent(
    name="Triage",
    instructions="Route to appropriate specialist.",
    handoffs=[billing_agent, technical_agent, sales_agent]
)
```

## Guardrails

### Input Guardrail

```python
from agents import Agent, input_guardrail, GuardrailFunctionOutput

@input_guardrail
async def check_no_pii(ctx, agent, input: str) -> GuardrailFunctionOutput:
    has_pii = detect_pii(input)
    return GuardrailFunctionOutput(
        output_info={"has_pii": has_pii},
        tripwire_triggered=has_pii
    )

agent = Agent(
    name="Support",
    input_guardrails=[check_no_pii]
)
```

### Output Guardrail

```python
from agents import output_guardrail

@output_guardrail
async def check_no_secrets(ctx, agent, output: str) -> GuardrailFunctionOutput:
    has_secrets = scan_for_secrets(output)
    return GuardrailFunctionOutput(
        output_info={"scanned": True},
        tripwire_triggered=has_secrets
    )

agent = Agent(
    name="CodeHelper",
    output_guardrails=[check_no_secrets]
)
```

### Handle Guardrail Failures

```python
from agents import InputGuardrailTripwireTriggered

try:
    result = await Runner.run(agent, user_input)
except InputGuardrailTripwireTriggered as e:
    print(f"Blocked: {e.guardrail_result.output_info}")
```

## MCP Integration

### Stdio Server (Local Process)

```python
from agents import Agent
from agents.mcp import MCPServerStdio

async with MCPServerStdio(
    name="Filesystem",
    params={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    }
) as mcp_server:
    agent = Agent(
        name="FileHelper",
        mcp_servers=[mcp_server]
    )
    result = await Runner.run(agent, "List files in /path")
```

### HTTP Server (Remote)

```python
from agents.mcp import MCPServerStreamableHttp

async with MCPServerStreamableHttp(
    name="Remote Tools",
    params={
        "url": "https://mcp.example.com/mcp",
        "headers": {"Authorization": f"Bearer {token}"}
    }
) as server:
    agent = Agent(mcp_servers=[server])
```

### Tool Filtering

```python
from agents.mcp import MCPServerStdio, create_static_tool_filter

server = MCPServerStdio(
    params={...},
    tool_filter=create_static_tool_filter(
        allowed_tool_names=["read_file", "list_directory"]
    )
)
```

## Sessions (Conversation Memory)

### SQLite (Simple)

```python
from agents import SQLiteSession

# In-memory (lost on restart)
session = SQLiteSession("user_123")

# File-based (persistent)
session = SQLiteSession("user_123", "conversations.db")

result = await Runner.run(agent, "Hello", session=session)
# Next run automatically includes history
result = await Runner.run(agent, "What did I say?", session=session)
```

### SQLAlchemy (Production)

```python
from agents import SQLAlchemySession

session = SQLAlchemySession.from_url(
    "user_123",
    url="postgresql+asyncpg://user:pass@localhost/db",
    create_tables=True
)
```

## Streaming

```python
result = await Runner.run_streamed(agent, "Tell me a story")

async for event in result.stream_events():
    if event.type == "raw_response_event":
        print(event.data, end="", flush=True)
```

## Structured Outputs

```python
from pydantic import BaseModel

class OrderAnalysis(BaseModel):
    sentiment: str
    urgency: int
    action_required: bool

agent = Agent(
    name="Analyzer",
    instructions="Analyze customer orders.",
    output_type=OrderAnalysis
)

result = await Runner.run(agent, "My order is late!")
analysis: OrderAnalysis = result.final_output
print(f"Urgency: {analysis.urgency}")
```

## Tracing

Tracing is enabled by default. View in OpenAI Dashboard.

### Custom Spans

```python
from agents import trace

with trace("Customer Support Flow"):
    result1 = await Runner.run(triage, query)
    result2 = await Runner.run(specialist, query)
```

### Disable Tracing (for non-OpenAI models)

```python
from agents import set_tracing_disabled
set_tracing_disabled(True)
```

## Decision Logic

| Situation | Pattern |
|-----------|---------|
| Single agent, simple task | Basic Agent |
| Need conversation history | Add Session |
| Multiple specialized tasks | Handoffs between agents |
| Predictable routing | Manager with agents-as-tools |
| User-facing validation | Input guardrails |
| Output safety checks | Output guardrails |
| External tool ecosystem | MCP integration |
| Non-OpenAI models | LiteLLM |

## TaskManager Example

Complete example building a task management agent:

```python
from agents import Agent, Runner, function_tool
from pydantic import BaseModel
from typing import Optional

# Task model
class Task(BaseModel):
    id: str
    title: str
    completed: bool = False

# In-memory storage
tasks: dict[str, Task] = {}

@function_tool
def add_task(title: str) -> str:
    """Add a new task."""
    task_id = f"task_{len(tasks) + 1}"
    tasks[task_id] = Task(id=task_id, title=title)
    return f"Created task {task_id}: {title}"

@function_tool
def list_tasks() -> str:
    """List all tasks."""
    if not tasks:
        return "No tasks yet."
    return "\n".join(
        f"[{'x' if t.completed else ' '}] {t.id}: {t.title}"
        for t in tasks.values()
    )

@function_tool
def complete_task(task_id: str) -> str:
    """Mark a task as completed."""
    if task_id not in tasks:
        return f"Task {task_id} not found."
    tasks[task_id].completed = True
    return f"Completed: {tasks[task_id].title}"

# Create agent
task_agent = Agent(
    name="TaskManager",
    instructions="""You help users manage their tasks.
    Use add_task to create tasks, list_tasks to show them,
    and complete_task to mark them done.""",
    tools=[add_task, list_tasks, complete_task]
)

# Run
async def main():
    result = await Runner.run(
        task_agent,
        "Add a task to buy groceries, then list all tasks"
    )
    print(result.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Safety

### NEVER
- Expose API keys in code or logs
- Skip error handling for API calls
- Trust user input without validation
- Ignore rate limits

### ALWAYS
- Use environment variables for secrets
- Wrap API calls in try/except
- Implement input guardrails for user-facing agents
- Use output guardrails for sensitive content
- Test with tracing enabled

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `MaxTurnsExceeded` | Agent loops too long | Increase `max_turns` in RunConfig |
| `ModelBehaviorError` | Invalid LLM output | Check model compatibility |
| `InputGuardrailTripwireTriggered` | Input blocked | Handle exception, provide feedback |

## References

- [Official Docs](https://openai.github.io/openai-agents-python/)
- [GitHub Repo](https://github.com/openai/openai-agents-python)
- [LiteLLM Providers](https://docs.litellm.ai/docs/providers)
- [Customer Service Demo](https://github.com/openai/openai-cs-agents-demo)
