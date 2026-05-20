---
name: mcp-tool-execution
description: |
  This skill registers, validates, and executes MCP (Model Context Protocol) tools deterministically, enforcing tool-mediated AI interactions. Use when implementing MCP server integrations, tool invocation lifecycles, or ensuring AI agents interact with external systems through proper tool mediation.
allowed-tools: Read, Grep, Glob, Bash
---

# MCP Tool Execution Skill

This skill implements deterministic MCP (Model Context Protocol) tool execution with parameter validation and tool-mediated AI enforcement. It provides the framework for registering MCP tools, validating parameters, and executing tool calls in a controlled manner.

## Core Capabilities

### 1. MCP Server Registration
- Registers MCP tools with proper parameter schemas
- Validates tool definitions against MCP specifications
- Ensures tools follow deterministic execution patterns
- Manages tool lifecycle (registration, validation, execution, cleanup)

### 2. Parameter Validation
- Validates input parameters against JSON Schema definitions
- Ensures type safety and format compliance
- Implements proper error handling for invalid parameters
- Provides detailed validation feedback

### 3. Deterministic Tool Execution
- Executes tools in a predictable, reproducible manner
- Maintains consistent execution order and behavior
- Handles tool failures gracefully with proper error reporting
- Implements retry mechanisms where appropriate

### 4. Tool-Mediated AI Enforcement
- Ensures all AI interactions occur through registered tools
- Prevents direct database or system access
- Implements security boundaries between AI and external systems
- Maintains audit trails for all tool invocations

## Implementation Pattern

### Server Initialization
```python
from mcp import FastMCP

def create_mcp_server(name: str, tools: list):
    """
    Create an MCP server with the specified tools
    """
    mcp = FastMCP(name=name, stateless_http=True)

    for tool in tools:
        register_tool(mcp, tool)

    return mcp.streamable_http_app()
```

### Tool Registration
```python
def register_tool(mcp, tool_definition):
    """
    Register a tool with parameter validation
    """
    @mcp.tool(
        name=tool_definition['name'],
        description=tool_definition['description']
    )
    async def tool_handler(**kwargs):
        # Validate parameters
        validated_params = validate_parameters(
            kwargs,
            tool_definition['input_schema']
        )

        # Execute tool deterministically
        result = await execute_tool_safely(
            tool_definition['implementation'],
            validated_params
        )

        return result
```

### Parameter Validation
```python
def validate_parameters(params: dict, schema: dict):
    """
    Validate parameters against JSON Schema
    """
    import jsonschema

    try:
        jsonschema.validate(params, schema)
        return params
    except jsonschema.ValidationError as e:
        raise ValueError(f"Parameter validation failed: {str(e)}")
```

### Safe Tool Execution
```python
async def execute_tool_safely(tool_func, params: dict):
    """
    Execute tool with proper error handling
    """
    try:
        result = await tool_func(**params)
        return {"success": True, "result": result}
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }
```

## MCP Integration Patterns

### Single Server Pattern (Correct Implementation)
```python
from mcp.server.fastmcp import FastMCP

# Create FastMCP application (correct implementation)
mcp_app = FastMCP(
    name="my-mcp-server",
    description="A simple MCP server for OpenAI Agents SDK integration.",
    stateless_http=True,
    json_response=True,  # Easier for HTTP clients without full SSE parsing
)

# Register tools using decorator pattern
@mcp_app.tool(
    name="greeting_from_server",
    description="Returns a personalized greeting from the MCP server."
)
def greeting_tool(name: str = "World") -> str:
    """A simple greeting tool."""
    return f"Hello, {name}! I am happy to serve you."

# Create streamable HTTP app for the server
def create_mcp_server():
    return mcp_app.streamable_http_app()

# Run the server
if __name__ == "__main__":
    import uvicorn
    app = create_mcp_server()
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Multiple Server Coordination (Correct Implementation)
```python
import asyncio
from contextlib import AsyncExitStack
from agents import Agent, OpenAIChatCompletionsModel, Runner
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams
from openai import AsyncOpenAI

async def connect_to_multiple_mcp_servers(server_urls: list):
    """
    Connect to multiple MCP servers and aggregate tools using AsyncExitStack
    """
    mcp_servers = []

    async with AsyncExitStack() as stack:
        for url in server_urls:
            mcp_params = MCPServerStreamableHttpParams(url=url)
            mcp_server_client = await stack.enter_async_context(
                MCPServerStreamableHttp(
                    params=mcp_params,
                    name=f"MCPClient_{url}",
                    cache_tools_list=True  # Enable tool caching for performance
                )
            )
            mcp_servers.append(mcp_server_client)

    # Create agent with multiple MCP servers (correct implementation)
    client = AsyncOpenAI(api_key="your-api-key")

    assistant = Agent(
        name="MultiMCPAssistant",
        mcp_servers=mcp_servers,  # Pass all server clients to agent
        model=OpenAIChatCompletionsModel(model="gpt-4o", openai_client=client),
    )

    return assistant
```

### Agent Integration Pattern
```python
from agents import Runner

async def run_agent_with_mcp_tools(assistant, user_input: str):
    """
    Run agent interaction with MCP tools using Runner pattern
    """
    result = await Runner.run(assistant, user_input)
    return result.final_output

# Complete integration example
async def main():
    server_urls = [
        "http://localhost:8001/mcp/",  # First MCP server
        "http://localhost:8002/mcp/",  # Second MCP server
    ]

    assistant = await connect_to_multiple_mcp_servers(server_urls)

    # Agent now has access to tools from all connected servers
    response = await run_agent_with_mcp_tools(assistant, "Use available tools")

    return response
```

## Security Considerations

### Access Control
- All database access must occur through registered tools
- No direct AI access to sensitive systems
- Implement proper authentication for MCP servers
- Log all tool invocations for audit purposes

### Parameter Sanitization
- Validate all inputs before processing
- Implement rate limiting for expensive operations
- Sanitize outputs before returning to AI
- Implement timeouts for long-running operations

## Error Handling

### Validation Errors
- Return descriptive error messages for invalid parameters
- Include schema information in error responses
- Maintain consistent error formats across tools

### Execution Errors
- Catch exceptions and return structured error responses
- Implement circuit breakers for failing tools
- Provide fallback mechanisms when possible

## Best Practices

### Tool Naming
- Use descriptive, unique names across all MCP servers
- Follow consistent naming conventions (e.g., `service_action` format)
- Avoid naming conflicts between different MCP integrations

### Schema Definition
- Define comprehensive JSON schemas for all tool inputs
- Include examples and descriptions in schemas
- Validate required parameters and data types

### Deterministic Behavior
- Ensure tools produce consistent results for identical inputs
- Avoid tools that rely on external state when possible
- Implement idempotent operations where feasible

## Integration with OpenAI Agent SDK

### Connecting MCP Servers
```python
from openai import OpenAI
from mcp_sdk import MCPServerStreamableHttp, MCPServerStreamableHttpParams

# Connect to MCP servers
mcp_servers = await connect_to_multiple_mcp_servers([
    "http://localhost:8000/mcp/",
    "http://localhost:8001/mcp/"
])

# Configure OpenAI client with MCP integration
client = OpenAI()
# The OpenAI Agent SDK will automatically discover and use
# tools from connected MCP servers
```

## MCP Specification Compliance

### Transport Layer
- HTTP-based communication using JSON-RPC 2.0
- Stateless HTTP transport for scalability
- Proper error handling and status codes

### Capability Discovery
- Dynamic tool discovery from MCP servers
- Schema-based parameter validation
- Comprehensive error reporting

## Monitoring and Observability

### Tool Invocation Tracking
- Log all tool calls with parameters and results
- Track execution times and success rates
- Monitor for unusual patterns or failures

### Performance Metrics
- Tool execution duration
- Error rates by tool
- Resource utilization