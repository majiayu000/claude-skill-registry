---
name: mcp-builder
description: "Comprehensive guide for building Model Context Protocol (MCP) servers with support for tools, resources, prompts, and authentication. Use when: (1) Creating custom MCP servers, (2) Integrating external APIs with Claude, (3) Building tool servers for specialized domains, (4) Creating resource providers for documentation, (5) Implementing authentication and security"
---

# MCP Builder - Model Context Protocol Server Development

## What is MCP?

Model Context Protocol (MCP) is an open standard created by Anthropic that enables AI assistants like Claude to securely connect to external data sources and tools. Think of it as a universal adapter that allows Claude to interact with any system, API, or data source through a standardized interface.

**Key Benefits:**
- **Standardization**: One protocol for all integrations
- **Security**: Built-in authentication and permission controls
- **Flexibility**: Support for tools, resources, and prompts
- **Scalability**: Designed for production workloads
- **Modularity**: Create reusable MCP servers for different domains

## Architecture Overview

MCP follows a client-server architecture:

```
┌─────────────┐         ┌─────────────┐         ┌──────────────┐
│   Claude    │ ←──MCP──→ │ MCP Server  │ ←──────→ │ External API │
│  (Client)   │         │  (Your Code) │         │  Database    │
└─────────────┘         └─────────────┘         └──────────────┘
```

**Components:**
- **Client**: Claude Desktop, Claude Code, or custom applications
- **Server**: Your MCP implementation (Python, TypeScript, etc.)
- **Transport**: Communication channel (stdio, HTTP, SSE)
- **Protocol**: Standardized message format (JSON-RPC 2.0)

For detailed protocol specification, see [Protocol Specification Reference](./references/protocol-specification.md).

## Core Components

### 1. Tools: Exposing Functions Claude Can Call

Tools are the primary way to give Claude new capabilities. Each tool is a function that Claude can invoke with specific arguments.

**Tool Definition Structure:**
```python
{
    "name": "tool_name",
    "description": "Clear description of what this tool does",
    "inputSchema": {
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Description of parameter"
            }
        },
        "required": ["param1"]
    }
}
```

**Key Principles:**
- **Clear naming**: Use descriptive, action-oriented names (e.g., `search_database`, not `db_query`)
- **Comprehensive descriptions**: Explain what the tool does, when to use it, and what it returns
- **Strong schemas**: Use JSON Schema to validate inputs and guide Claude
- **Error handling**: Return clear error messages when things go wrong

For complete schema design patterns and best practices, see [Tool Schema Reference](./references/tool-schemas.md).

### 2. Resources: Providing Data/Documentation Access

Resources allow Claude to access files, documentation, or structured data. Unlike tools (which perform actions), resources provide information.

**Resource Types:**
- **Static**: Fixed content (e.g., documentation files)
- **Dynamic**: Generated on-demand (e.g., database queries)
- **Templates**: Parameterized resources (e.g., user profiles)

**Resource URI Patterns:**
```
file:///path/to/file.txt          # Local file
http://example.com/api/docs       # HTTP resource
custom://database/users/123       # Custom scheme
template://report/{user_id}       # Template resource
```

### 3. Prompts: Reusable Prompt Templates

Prompts are pre-defined message templates that users can invoke. They help standardize common workflows and best practices.

**Prompt Definition:**
```python
{
    "name": "code_review",
    "description": "Comprehensive code review checklist",
    "arguments": [
        {
            "name": "language",
            "description": "Programming language",
            "required": True
        }
    ]
}
```

### 4. Authentication Methods

MCP supports multiple authentication methods:
- **No Authentication** (development only)
- **API Key Authentication** (simple, medium security)
- **OAuth 2.0** (third-party, high security)
- **Bearer Token** (API-to-API, high security)

For complete security implementation guides, see [Security Best Practices](./references/security-guide.md).

## Server Implementation Workflow

### Phase 1: Project Setup

Create your MCP server project:

```bash
# Create project directory
mkdir my-mcp-server
cd my-mcp-server

# Initialize Python project
uv init
uv add mcp

# Create server file
touch server.py
```

### Phase 2: Basic Server Structure

**Minimal working server:**

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio

app = Server("my-mcp-server")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="my_tool",
            description="Description of what this tool does",
            inputSchema={
                "type": "object",
                "properties": {
                    "param": {"type": "string"}
                },
                "required": ["param"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "my_tool":
        param = arguments["param"]
        result = f"Processed: {param}"
        return [TextContent(type="text", text=result)]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

### Phase 3: Tool Registration and Handlers

**Registration Pattern:**
```python
@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="calculator_add",
            description="Add two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        )
    ]
```

**Handler Pattern:**
```python
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "calculator_add":
        return await handle_calculator_add(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def handle_calculator_add(arguments: dict):
    a = arguments["a"]
    b = arguments["b"]
    result = a + b
    return [TextContent(type="text", text=f"{a} + {b} = {result}")]
```

### Phase 4: Resource Implementation

**Static and dynamic resource examples:**
```python
from mcp.types import Resource, ResourceContents, TextResourceContents

@app.list_resources()
async def list_resources():
    return [Resource(uri="file:///docs/readme.md", name="README",
                     description="Documentation", mimeType="text/markdown")]

@app.read_resource()
async def read_resource(uri: str):
    if uri.startswith("file://"):
        with open(uri[7:], 'r') as f:
            return ResourceContents(contents=[TextResourceContents(
                uri=uri, mimeType="text/markdown", text=f.read())])
```

See [Resource Server Example](./examples/resource-server.md) for complete implementation.

### Phase 5: Error Handling and Testing

**Error Response Pattern:**
```python
async def call_tool(name: str, arguments: dict):
    try:
        return [TextContent(type="text", text=await execute_tool(name, arguments))]
    except ValueError as e:
        return [TextContent(type="text", text=f"Invalid input: {str(e)}", isError=True)]
    except Exception as e:
        logger.exception("Unexpected error")
        return [TextContent(type="text", text=f"Error: {type(e).__name__}", isError=True)]
```

**Testing:**

```bash
# Test with MCP inspector
npx @modelcontextprotocol/inspector python server.py
```

See [Testing and Debugging Guide](./references/testing-debugging.md) for comprehensive strategies.

### Phase 6: Claude Desktop Integration

**Configuration:** Edit `claude_desktop_config.json`:
- macOS: `~/Library/Application Support/Claude/`
- Windows: `%APPDATA%\Claude/`
- Linux: `~/.config/Claude/`

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"],
      "env": {"API_KEY": "your-key"}
    }
  }
}
```

## Best Practices

### Tool Schema Design

**Use descriptive names:**
```python
# ✅ Good
"search_customer_by_email"
"calculate_shipping_cost"

# ❌ Bad
"search"
"calc"
```

**Provide comprehensive descriptions:**
```python
# ✅ Good
description="""
Search for customers by email address. Returns customer profile including:
- Contact information
- Order history
- Account status
"""

# ❌ Bad
description="Search customers"
```

**Use enums for fixed options:**
```python
# ✅ Good
"status": {
    "type": "string",
    "enum": ["pending", "approved", "rejected"],
    "description": "Application status"
}
```

### Error Handling Strategies

Categorize errors with custom exceptions and provide actionable messages:

```python
class ValidationError(Exception): pass
class AuthenticationError(Exception): pass

async def call_tool(name: str, arguments: dict):
    try:
        return await execute_tool(name, arguments)
    except ValidationError as e:
        return [TextContent(type="text", text=f"Invalid input: {str(e)}", isError=True)]
```

### Security Considerations

Always validate inputs and use environment variables for secrets:

```python
# Input validation
def validate_url(url: str) -> bool:
    if urlparse(url).scheme not in ['http', 'https']:
        raise ValidationError("Only HTTP/HTTPS URLs allowed")

# Secrets management
API_KEY = os.getenv("API_KEY")  # ✅ Good
# API_KEY = "sk-1234"  # ❌ Bad - Never hardcode!
```

### Performance Optimization

Use connection pooling and parallel async operations:

```python
# ✅ Parallel execution
results = await asyncio.gather(*[fetch_user_data(uid) for uid in user_ids])

# ❌ Sequential execution (slow)
for user_id in user_ids:
    result = await fetch_user_data(user_id)
```

## Common Pitfalls

### Schema Validation Errors

**Missing required validation:**
```python
# ❌ Bad: No validation
async def handle_create_user(arguments: dict):
    username = arguments["username"]  # Will crash if missing!

# ✅ Good: Validate inputs
async def handle_create_user(arguments: dict):
    if "username" not in arguments:
        return [TextContent(type="text", text="Error: username required", isError=True)]
    username = arguments["username"]
```

### Authentication Issues

**Insecure storage:**
```python
# ❌ Bad: Hardcoded API key
API_KEY = "sk-1234567890abcdef"

# ✅ Good: Environment variables
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable required")
```

### Transport Configuration

**Path issues:**
```python
# ❌ Bad: Relative path
{
  "command": "python",
  "args": ["server.py"]  # Won't work!
}

# ✅ Good: Absolute path
{
  "command": "python",
  "args": ["/Users/username/projects/mcp-server/server.py"]
}
```

### Error Propagation

**Silent failures:**
```python
# ❌ Bad: Silent failure
async def call_tool(name: str, arguments: dict):
    try:
        return await execute_tool(name, arguments)
    except Exception:
        return [TextContent(type="text", text="Something went wrong")]

# ✅ Good: Descriptive errors
async def call_tool(name: str, arguments: dict):
    try:
        return await execute_tool(name, arguments)
    except ValueError as e:
        return [TextContent(type="text", text=f"Invalid input: {str(e)}", isError=True)]
    except Exception as e:
        logger.exception("Unexpected error")
        return [TextContent(type="text", text=f"Error: {type(e).__name__}", isError=True)]
```

**Not marking errors:**
```python
# ❌ Bad
return [TextContent(type="text", text="Error: Failed")]

# ✅ Good
return [TextContent(type="text", text="Error: Failed", isError=True)]
```

## Additional Resources

### Official Documentation
- MCP Specification: https://modelcontextprotocol.io/
- Python SDK: https://github.com/modelcontextprotocol/python-sdk
- TypeScript SDK: https://github.com/modelcontextprotocol/typescript-sdk

### Detailed References
- [Protocol Specification](./references/protocol-specification.md) - Complete protocol details, message formats, transport mechanisms
- [Tool Schema Guide](./references/tool-schemas.md) - Comprehensive schema patterns and validation
- [Security Best Practices](./references/security-guide.md) - Authentication, authorization, input validation, secrets management
- [Testing and Debugging](./references/testing-debugging.md) - Unit tests, integration tests, MCP inspector usage, debugging techniques
- [Production Deployment](./references/production-deployment.md) - Production configuration, monitoring, scaling, Docker deployment

### Complete Examples
- [Simple Calculator Server](./examples/simple-calculator-server.md) - Basic arithmetic tools
- [REST API Wrapper](./examples/rest-api-wrapper.md) - GitHub API integration
- [Database Server](./examples/database-server.md) - Safe database query access
- [Resource Server](./examples/resource-server.md) - Static and dynamic resources

### Tools
- MCP Inspector: https://github.com/modelcontextprotocol/inspector
- Claude Desktop: https://claude.ai/download

## Quick Reference

### Server Template (Python)
```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio

app = Server("my-server")

@app.list_tools()
async def list_tools():
    return [Tool(name="my_tool", description="...", inputSchema={...})]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "my_tool":
        return [TextContent(type="text", text="Result")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

### Common Patterns

**Error handling:**
```python
return [TextContent(type="text", text="Error message", isError=True)]
```

**Async operations:**
```python
results = await asyncio.gather(*tasks)
```

**Input validation:**
```python
if "required_param" not in arguments:
    return [TextContent(type="text", text="Missing parameter", isError=True)]
```

---

**End of MCP Builder Skill Guide**

For complete working examples and detailed technical references, explore the `examples/` and `references/` directories.
