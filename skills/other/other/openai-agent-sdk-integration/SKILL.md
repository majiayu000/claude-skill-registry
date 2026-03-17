---
name: openai-agent-sdk-integration
description: |
  This skill implements AI agents with MCP (Model Context Protocol) server integration using the OpenAI Agents SDK. It covers agent creation, tool definitions, MCP server connections (stdio, HTTP, SSE), tool filtering, caching, handoffs, guardrails, and multi-agent orchestration patterns. Use when building AI agents that connect to MCP servers, implementing tool-mediated AI interactions, or creating production-grade agentic systems.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# OpenAI Agents SDK Integration with MCP

This skill provides comprehensive guidance for building AI agents using the OpenAI Agents SDK with MCP (Model Context Protocol) server integration.

## Before Implementation

| Source | Gather |
|--------|--------|
| **Codebase** | Existing agent patterns, MCP server implementations, tool definitions |
| **Conversation** | User's specific requirements, transport type (HTTP/stdio), tool needs |
| **Skill References** | Domain patterns from `references/` (SDK patterns, MCP primitives, examples) |
| **User Guidelines** | Project-specific conventions, authentication requirements |

## Core Concepts

### Three Primitives of OpenAI Agents SDK

| Primitive | Purpose | Control Model |
|-----------|---------|---------------|
| **Agents** | LLMs with instructions and tools | Framework-controlled |
| **Handoffs** | Delegation between agents | Agent-controlled |
| **Guardrails** | Input/output validation | Developer-controlled |

### Three Primitives of MCP

| Primitive | Purpose | Control Model |
|-----------|---------|---------------|
| **Tools** | Functions AI can invoke | Model-controlled |
| **Resources** | Read-only data access | Application-controlled |
| **Prompts** | Pre-crafted instructions | User-controlled |

## Quick Start

### 1. Create MCP Server

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="my-mcp-server",
    stateless_http=True,
    json_response=True
)

@mcp.tool(name="my_tool", description="Tool description")
def my_tool(param: str) -> str:
    return f"Result: {param}"

# Create HTTP app
streamable_http_app = mcp.streamable_http_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:streamable_http_app", host="0.0.0.0", port=8001)
```

### 2. Create Agent with MCP Connection

```python
import asyncio
from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams
from openai import AsyncOpenAI

MCP_SERVER_URL = "http://localhost:8001/mcp/"

async def main():
    client = AsyncOpenAI(api_key="your-api-key")
    mcp_params = MCPServerStreamableHttpParams(url=MCP_SERVER_URL)

    async with MCPServerStreamableHttp(
        params=mcp_params,
        name="MyMCPClient"
    ) as mcp_server:
        agent = Agent(
            name="MyAgent",
            instructions="You are a helpful assistant.",
            mcp_servers=[mcp_server],
            model=OpenAIChatCompletionsModel(model="gpt-4o", openai_client=client)
        )

        result = await Runner.run(agent, "Your query here")
        print(result.final_output)

asyncio.run(main())
```

## MCP Transport Types

| Transport | Class | Use Case |
|-----------|-------|----------|
| **HTTP Streamable** | `MCPServerStreamableHttp` | Production, remote servers |
| **SSE** | `MCPServerSse` | Legacy systems (deprecated) |
| **Stdio** | `MCPServerStdio` | Local development, subprocesses |

## Key Patterns

### Tool Caching
```python
MCPServerStreamableHttp(
    params=mcp_params,
    cache_tools_list=True  # Enable caching
)
```

### Static Tool Filtering
```python
from agents.mcp import create_static_tool_filter

tool_filter = create_static_tool_filter(
    allowed_tool_names=["allowed_tool"],
    blocked_tool_names=["blocked_tool"]
)

MCPServerStreamableHttp(params=mcp_params, tool_filter=tool_filter)
```

### Dynamic Tool Filtering
```python
from agents.mcp import ToolFilterContext

def context_aware_filter(context: ToolFilterContext, tool) -> bool:
    return context.agent.name == "MyAgent" and tool.name == "my_tool"

MCPServerStreamableHttp(params=mcp_params, tool_filter=context_aware_filter)
```

### Multiple MCP Servers
```python
from contextlib import AsyncExitStack

async def connect_multiple_servers(urls: list):
    mcp_servers = []
    async with AsyncExitStack() as stack:
        for url in urls:
            params = MCPServerStreamableHttpParams(url=url)
            client = await stack.enter_async_context(
                MCPServerStreamableHttp(params=params, name=f"Client_{url}")
            )
            mcp_servers.append(client)

        agent = Agent(
            name="MultiServerAgent",
            mcp_servers=mcp_servers,
            model=model
        )
        return agent
```

## Agent Configuration

### Agent Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str | Agent identifier |
| `instructions` | str/callable | System prompt or dynamic function |
| `model` | Model | LLM configuration |
| `tools` | list | Local function tools |
| `mcp_servers` | list | MCP server connections |
| `handoffs` | list | Delegation targets |
| `output_type` | Pydantic | Structured output schema |

### Runner Methods

| Method | Type | Description |
|--------|------|-------------|
| `Runner.run()` | async | Returns `RunResult` |
| `Runner.run_sync()` | sync | Wrapper for `.run()` |
| `Runner.run_streamed()` | async | Streaming with `RunResultStreaming` |

## MCP Server Patterns

### Defining Tools
```python
@mcp.tool(name="tool_name", description="Tool description")
def my_tool(param: str, optional: str = "default") -> str:
    """Docstring becomes parameter description."""
    return f"Result: {param}"
```

### Defining Resources
```python
@mcp.resource("docs://{doc_id}", mime_type="text/plain")
def get_document(doc_id: str) -> str:
    return documents[doc_id]
```

### Defining Prompts
```python
from pydantic import Field

@mcp.prompt(name="my_prompt", description="Prompt description")
def generate_instructions(focus: str = Field(description="Focus area")) -> str:
    return f"Instructions focused on {focus}..."
```

## Guardrails

### Input Guardrail
```python
from agents import input_guardrail, GuardrailFunctionOutput

@input_guardrail
async def validate_input(ctx, agent, input):
    if "forbidden" in input:
        return GuardrailFunctionOutput(tripwire_triggered=True)
    return GuardrailFunctionOutput(tripwire_triggered=False)
```

### Output Guardrail
```python
from agents import output_guardrail

@output_guardrail
async def validate_output(ctx, agent, output):
    # Validate final output
    return GuardrailFunctionOutput(tripwire_triggered=False)
```

## Handoffs

### Basic Handoff
```python
from agents import handoff

specialist = Agent(name="Specialist", instructions="...")

main_agent = Agent(
    name="Main",
    handoffs=[specialist]  # Direct handoff
)
```

### Custom Handoff
```python
from agents import handoff

custom_handoff = handoff(
    agent=specialist,
    tool_name_override="escalate_to_specialist",
    tool_description_override="Transfer to specialist for complex issues"
)
```

## Context Management

```python
from dataclasses import dataclass
from agents import RunContextWrapper

@dataclass
class MyContext:
    user_id: str
    session_id: str

async def main():
    ctx = MyContext(user_id="123", session_id="abc")
    result = await Runner.run(agent, "query", context=ctx)
```

## Tracing

```python
from agents import trace

with trace("My Workflow"):
    result1 = await Runner.run(agent, "First query")
    result2 = await Runner.run(agent, "Second query")
```

## Best Practices

1. **Use stateless HTTP transport** for production MCP servers
2. **Enable tool caching** when tool definitions are stable
3. **Implement tool filtering** for access control
4. **Use AsyncExitStack** for multiple server connections
5. **Add guardrails** for input/output validation
6. **Use context management** for dependency injection
7. **Enable tracing** for observability

## Error Handling

```python
try:
    result = await Runner.run(agent, query)
except MaxTurnsExceeded:
    # Handle max turns exceeded
    pass
except InputGuardrailTripwireTriggered:
    # Handle guardrail triggered
    pass
```

## Reference Files

| File | Content |
|------|---------|
| `references/agent-patterns.md` | Agent creation and configuration patterns |
| `references/mcp-server-patterns.md` | MCP server implementation patterns |
| `references/tool-filtering.md` | Static and dynamic tool filtering |
| `references/multi-agent-orchestration.md` | Multi-agent and handoff patterns |
| `references/transport-options.md` | HTTP, SSE, and stdio transports |
| `references/guardrails-tracing.md` | Guardrails and observability |
