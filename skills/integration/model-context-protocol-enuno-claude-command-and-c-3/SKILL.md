---
name: model-context-protocol
version: "1.4.0"
description: Model Context Protocol (MCP) - Open standard for connecting AI applications to external data sources, tools, and systems. Use for building MCP servers (tools, resources, prompts), clients, understanding protocol architecture, and implementing AI integrations.
specification_version: "2024-11-05"
---

# Model Context Protocol Skill

The Model Context Protocol (MCP) is an open-source standard that provides a universal way to connect AI-powered applications to external data sources, tools, and systems. Think of MCP as a **USB-C port for AI applications** - a standardized interface that enables seamless integration regardless of the underlying implementation.

**Core Value Proposition**: Build once, connect anywhere. MCP servers work with any MCP-compatible AI application, eliminating the need for custom integrations per application.

## When to Use This Skill

This skill should be triggered when:
- Building MCP servers to expose tools, resources, or prompts
- Implementing MCP clients in AI applications
- Understanding MCP protocol architecture and message flow
- Creating tool handlers for AI agent operations
- Implementing resource providers for data access
- Building prompt templates for AI interactions
- Integrating external services with AI applications
- Debugging MCP server/client communication

## Protocol Overview

### The AI Integration Paradox

MCP addresses a fundamental challenge: **AI systems need dynamic, context-aware access to resources, but traditional APIs were built for predictable workflows.**

Traditional APIs assume:
- Known endpoints at design time
- Predictable request patterns
- Static data schemas

AI systems require:
- **Dynamic Discovery** - Identify needed resources at runtime
- **Rich Context Exchange** - Metadata and relationships flow with data
- **Secure Sandboxing** - Controlled access without direct AI permissions
- **Bidirectional Communication** - Systems ask questions, not just consume

### The Problem MCP Solves

Before MCP:
- Each AI application builds custom integrations for each data source
- Every data source implements provider-specific APIs
- N applications × M data sources = N×M integrations

After MCP:
- One protocol specification
- N + M implementations needed
- Any server works with any client

### The USB-C Analogy

Just as USB-C provides a universal connector for devices:
- **MCP Host** = Device (AI application like Claude Desktop)
- **MCP Client** = Port (connection manager within the host)
- **MCP Server** = Peripheral (service providing context)

### Mediated Access Pattern (Security Broker Model)

> "The Host mediates ALL AI-resource interactions"

```
┌────────────────────────────────────────────────────────┐
│                     HOST APPLICATION                    │
│            (Claude Desktop, IDE, Custom App)            │
│                                                        │
│   ┌──────────┐   ┌──────────┐   ┌──────────┐         │
│   │ Client 1 │   │ Client 2 │   │ Client 3 │         │
│   │   ↕      │   │   ↕      │   │   ↕      │         │
│   │Server A  │   │Server B  │   │Server C  │   1:1   │
│   └──────────┘   └──────────┘   └──────────┘  mapping │
└────────────────────────────────────────────────────────┘
```

Key security principles:
- Each Client-Server pair is isolated
- Host acts as central authority
- No direct AI-to-resource access
- Prevents resource interference

---

## Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP ARCHITECTURE                          │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                        HOST (AI App)                          │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                    MCP CLIENT                           │  │
│  │  • Maintains 1:1 connections with servers              │  │
│  │  • Handles protocol negotiation                         │  │
│  │  • Routes messages to/from servers                      │  │
│  └───────────┬────────────────────────┬───────────────────┘  │
│              │                        │                       │
└──────────────┼────────────────────────┼───────────────────────┘
               │ stdio                  │ HTTP
               ▼                        ▼
┌──────────────────────┐    ┌──────────────────────┐
│    LOCAL SERVER      │    │   REMOTE SERVER      │
│  (subprocess)        │    │   (network)          │
│                      │    │                      │
│  • Tools             │    │  • Tools             │
│  • Resources         │    │  • Resources         │
│  • Prompts           │    │  • Prompts           │
└──────────────────────┘    └──────────────────────┘
```

### Communication Protocol

MCP uses **JSON-RPC 2.0** over various transports (Specification: 2024-11-05):

**JSON-RPC Requirements:**
- `id` MUST NOT be null for requests (use string or integer)
- `id` MUST be unique within a session
- Requests expect responses; notifications do not
- Unknown methods return `-32601` (Method not found)

```typescript
// Request (id required, must be unique per session)
{
  "jsonrpc": "2.0",
  "id": "req-1",  // String or integer, never null
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": { "city": "San Francisco" }
  }
}

// Response (id matches request)
{
  "jsonrpc": "2.0",
  "id": "req-1",
  "result": {
    "content": [{
      "type": "text",
      "text": "Weather in San Francisco: 65°F, partly cloudy"
    }]
  }
}

// Notification (no id, no response expected)
{
  "jsonrpc": "2.0",
  "method": "notifications/resources/updated",
  "params": { "uri": "file:///data/config.json" }
}
```

### Connection Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                  CONNECTION LIFECYCLE                        │
└─────────────────────────────────────────────────────────────┘

1. INITIALIZATION (Version Negotiation)
   Client ──initialize──────► Server
     └─ protocolVersion: "2024-11-05"
     └─ capabilities: { sampling: {}, roots: {} }
     └─ clientInfo: { name, version }

   Client ◄──result────────── Server
     └─ protocolVersion: "2024-11-05"  (server's supported version)
     └─ capabilities: { tools: {}, resources: {} }
     └─ serverInfo: { name, version }

   Client ──initialized──────► Server (notification, no response)

2. OPERATION PHASE
   Client ◄──► Server (bidirectional messages)
   • Client calls server methods (tools/call, resources/read)
   • Server sends notifications (resource updates, progress)
   • Server may call client methods (sampling/createMessage)

3. TERMINATION
   For stdio:  Close input stream, wait for server exit, terminate
   For HTTP:   Send HTTP DELETE with Mcp-Session-Id header
```

**Version Negotiation:**
- Client sends supported `protocolVersion` in `initialize`
- Server responds with its version (SHOULD match or be compatible)
- If incompatible, client MAY disconnect or proceed with limitations

---

## Server Primitives

MCP servers expose three primary primitives:

### 1. Tools (Model-Controlled)

Tools are **executable functions** that AI models can invoke to perform actions:

```json
{
  "name": "send_email",
  "description": "Send an email to a recipient",
  "inputSchema": {
    "type": "object",
    "properties": {
      "to": {
        "type": "string",
        "description": "Recipient email address"
      },
      "subject": {
        "type": "string",
        "description": "Email subject line"
      },
      "body": {
        "type": "string",
        "description": "Email body content"
      }
    },
    "required": ["to", "subject", "body"]
  }
}
```

**Tool Call Flow:**
```
1. Client requests: tools/list
2. Server returns: Available tools with schemas
3. Model decides to call tool
4. Client sends: tools/call with arguments
5. Server executes and returns: result content
```

**Tool Result Content Types:**
- `text` - Plain text response
- `image` - Base64-encoded image data
- `audio` - Base64-encoded audio data
- `resource` - Embedded resource content

**Error Handling with `isError`:**
```json
// Normal result
{
  "content": [{ "type": "text", "text": "Success!" }],
  "isError": false  // Optional, defaults to false
}

// Execution error (not a JSON-RPC error)
{
  "content": [{ "type": "text", "text": "File not found: /data/missing.txt" }],
  "isError": true  // Tool ran but encountered an error
}
```

Use `isError: true` when the tool executed but encountered an expected error (file not found, validation failed, etc.). Use JSON-RPC errors for protocol-level failures.

### 2. Resources (Application-Controlled)

Resources are **data sources** that provide context to AI applications:

```json
{
  "uri": "file:///projects/myapp/README.md",
  "name": "README.md",
  "description": "Project readme file",
  "mimeType": "text/markdown"
}
```

**Resource URIs:**
- Standard schemes: `file://`, `https://`
- Custom schemes: `postgres://`, `git://`
- Resource templates: `file:///{path}` (parameterized)

**Resource Templates:**
```json
{
  "uriTemplate": "file:///{path}",
  "name": "Project Files",
  "description": "Access files in the project directory",
  "mimeType": "text/plain"
}
```
Templates use URI Template syntax (RFC 6570) for parameterized resource access. Servers that support templates should also expose `completion/complete` for auto-completion.

**Content Types:**
```json
// Text content
{
  "uri": "file:///README.md",
  "mimeType": "text/markdown",
  "text": "# Project Title\n..."
}

// Binary content (blob)
{
  "uri": "file:///image.png",
  "mimeType": "image/png",
  "blob": "iVBORw0KGgoAAAANSUhEUgAA..."  // base64-encoded
}
```

**Resource Operations:**
```json
// List resources
{ "method": "resources/list" }

// Read resource
{
  "method": "resources/read",
  "params": { "uri": "file:///data/config.json" }
}

// Subscribe to changes
{
  "method": "resources/subscribe",
  "params": { "uri": "file:///data/config.json" }
}
```

### 3. Prompts (User-Controlled)

Prompts are **reusable templates** for AI interactions:

```json
{
  "name": "code_review",
  "title": "Request Code Review",
  "description": "Analyze code quality and suggest improvements",
  "arguments": [
    {
      "name": "code",
      "description": "The code to review",
      "required": true
    },
    {
      "name": "language",
      "description": "Programming language",
      "required": false
    }
  ]
}
```

**Prompt Messages:**
```json
{
  "method": "prompts/get",
  "params": {
    "name": "code_review",
    "arguments": {
      "code": "def hello(): print('world')",
      "language": "python"
    }
  }
}

// Response
{
  "result": {
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Please review this Python code:\ndef hello(): print('world')"
        }
      }
    ]
  }
}
```

---

## Client Features

### Sampling (Server → LLM)

Servers can request LLM completions through the client:

```json
{
  "method": "sampling/createMessage",
  "params": {
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Summarize this document..."
        }
      }
    ],
    "modelPreferences": {
      "hints": [{ "name": "claude-3-sonnet" }],
      "intelligencePriority": 0.8,
      "speedPriority": 0.5
    },
    "systemPrompt": "You are a helpful assistant.",
    "maxTokens": 500
  }
}
```

**Model Preferences (0-1 scale):**
- `costPriority` - Prefer cheaper models
- `speedPriority` - Prefer faster models
- `intelligencePriority` - Prefer more capable models

**Human-in-the-Loop:** Sampling requests SHOULD be reviewed by users before execution.

### Roots (Context Boundaries)

Clients can expose filesystem roots to servers:

```json
{
  "capabilities": {
    "roots": {
      "listChanged": true
    }
  }
}
```

Roots define boundaries for server access, allowing servers to understand which directories or resources they can interact with.

---

## Utilities

MCP includes base utilities and server utilities for protocol-level operations.

### Base Utilities

**Ping (Connection Health):**
```json
// Request
{ "jsonrpc": "2.0", "id": 1, "method": "ping" }

// Response
{ "jsonrpc": "2.0", "id": 1, "result": {} }
```
Used to check connection health. Either party can send ping; receiver MUST respond promptly.

**Cancellation:**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/cancelled",
  "params": {
    "requestId": "req-123",
    "reason": "User cancelled operation"
  }
}
```
Notification to cancel a pending request. The receiver SHOULD stop processing and MAY return a partial result or error.

**Progress Notifications:**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/progress",
  "params": {
    "progressToken": "token-456",
    "progress": 50,
    "total": 100,
    "message": "Processing files..."
  }
}
```
For long-running operations. The `progressToken` is provided in the original request's `_meta.progressToken`.

### Server Utilities

**Completion (Auto-complete):**
```json
// Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "completion/complete",
  "params": {
    "ref": {
      "type": "ref/resource",
      "uri": "file:///{path}"
    },
    "argument": {
      "name": "path",
      "value": "src/"
    }
  }
}

// Response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "completion": {
      "values": ["src/index.ts", "src/utils/", "src/types/"],
      "hasMore": false
    }
  }
}
```
Provides auto-completion suggestions for resource template arguments or prompt arguments.

**Logging:**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/message",
  "params": {
    "level": "info",  // debug, info, notice, warning, error, critical, alert, emergency
    "logger": "database",
    "data": "Connected to PostgreSQL at localhost:5432"
  }
}
```
Servers can send log messages to clients. The client MAY filter based on level threshold set via `logging/setLevel`.

**Pagination:**
For large result sets, use cursor-based pagination:
```json
// Request with cursor
{
  "method": "tools/list",
  "params": { "cursor": "eyJvZmZzZXQiOjEwMH0=" }
}

// Response with next cursor
{
  "result": {
    "tools": [...],
    "nextCursor": "eyJvZmZzZXQiOjIwMH0="  // null if no more results
  }
}
```
Cursors are opaque strings. Clients SHOULD NOT assume any structure.

---

## Transports

### stdio Transport (Local)

For subprocess-based communication:

```bash
# Server launched by client as subprocess
$ my-mcp-server

# Communication via stdin/stdout
Server reads: stdin (JSON-RPC messages)
Server writes: stdout (JSON-RPC responses)
Server logs: stderr (debugging only)
```

**Requirements:**
- Messages delimited by newlines
- Must NOT contain embedded newlines
- Client SHOULD support stdio whenever possible

### Streamable HTTP Transport (Remote)

For network-based communication:

```
POST /mcp HTTP/1.1
Content-Type: application/json
Accept: application/json, text/event-stream
MCP-Protocol-Version: 2025-06-18

{"jsonrpc":"2.0","id":1,"method":"tools/list"}
```

**Response Types:**
- `application/json` - Single JSON response
- `text/event-stream` - SSE stream for multiple messages

**Session Management:**
```
1. Server returns: Mcp-Session-Id header
2. Client includes: Mcp-Session-Id in subsequent requests
3. Server MAY: Return 404 to terminate session
4. Client MAY: DELETE with session ID to close
```

**Security Requirements:**
- Validate `Origin` header (prevent DNS rebinding)
- Local servers bind to localhost only
- Implement authentication for remote access

---

## SDK Installation

### TypeScript

```bash
npm install @modelcontextprotocol/sdk
```

```typescript
import { McpServer, StdioServerTransport } from "@modelcontextprotocol/sdk/server";

const server = new McpServer({
  name: "my-server",
  version: "1.0.0"
});

// Add a tool
server.tool("get_weather", {
  description: "Get weather for a city",
  inputSchema: {
    type: "object",
    properties: {
      city: { type: "string", description: "City name" }
    },
    required: ["city"]
  }
}, async (args) => {
  const weather = await fetchWeather(args.city);
  return {
    content: [{ type: "text", text: `Weather: ${weather}` }]
  };
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

**GitHub**: https://github.com/modelcontextprotocol/typescript-sdk

### Python

```bash
pip install mcp
# or with uv
uv add mcp
```

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("my-server")

@server.tool()
async def get_weather(city: str) -> str:
    """Get weather for a city."""
    weather = await fetch_weather(city)
    return f"Weather: {weather}"

@server.resource("config://app")
async def get_config() -> str:
    """Get application configuration."""
    return json.dumps(config)

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**GitHub**: https://github.com/modelcontextprotocol/python-sdk

### Other SDKs

| Language | Installation | Repository |
|----------|--------------|------------|
| **Go** | `go get github.com/modelcontextprotocol/go-sdk` | [go-sdk](https://github.com/modelcontextprotocol/go-sdk) |
| **Kotlin** | Maven/Gradle | [kotlin-sdk](https://github.com/modelcontextprotocol/kotlin-sdk) |
| **Swift** | Swift Package Manager | [swift-sdk](https://github.com/modelcontextprotocol/swift-sdk) |
| **Java** | Maven | [java-sdk](https://github.com/modelcontextprotocol/java-sdk) |
| **C#** | NuGet | [csharp-sdk](https://github.com/modelcontextprotocol/csharp-sdk) |
| **Ruby** | `gem install mcp` | [ruby-sdk](https://github.com/modelcontextprotocol/ruby-sdk) |
| **Rust** | `cargo add mcp` | [rust-sdk](https://github.com/modelcontextprotocol/rust-sdk) |
| **PHP** | Composer | [php-sdk](https://github.com/modelcontextprotocol/php-sdk) |

---

## Building an MCP Server

### Minimal TypeScript Server

```typescript
import { McpServer, StdioServerTransport } from "@modelcontextprotocol/sdk/server";

const server = new McpServer({
  name: "example-server",
  version: "1.0.0",
  capabilities: {
    tools: {},
    resources: {},
    prompts: {}
  }
});

// Tool: Calculate
server.tool("calculate", {
  description: "Perform basic calculations",
  inputSchema: {
    type: "object",
    properties: {
      operation: { type: "string", enum: ["add", "subtract", "multiply", "divide"] },
      a: { type: "number" },
      b: { type: "number" }
    },
    required: ["operation", "a", "b"]
  }
}, async ({ operation, a, b }) => {
  let result: number;
  switch (operation) {
    case "add": result = a + b; break;
    case "subtract": result = a - b; break;
    case "multiply": result = a * b; break;
    case "divide": result = a / b; break;
  }
  return {
    content: [{ type: "text", text: `Result: ${result}` }]
  };
});

// Resource: Static config
server.resource("config://app", {
  name: "App Configuration",
  description: "Application settings",
  mimeType: "application/json"
}, async () => {
  return {
    contents: [{
      uri: "config://app",
      mimeType: "application/json",
      text: JSON.stringify({ version: "1.0", debug: false })
    }]
  };
});

// Prompt: Greeting
server.prompt("greeting", {
  name: "greeting",
  description: "Generate a personalized greeting",
  arguments: [
    { name: "name", description: "Person's name", required: true }
  ]
}, async ({ name }) => {
  return {
    messages: [{
      role: "user",
      content: { type: "text", text: `Please greet ${name} warmly.` }
    }]
  };
});

// Connect transport
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Minimal Python Server

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Resource, Prompt, PromptMessage

server = Server("example-server")

# Tool: Calculate
@server.tool()
async def calculate(operation: str, a: float, b: float) -> list[TextContent]:
    """Perform basic calculations (add, subtract, multiply, divide)."""
    ops = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else float('inf')
    }
    result = ops.get(operation, 0)
    return [TextContent(type="text", text=f"Result: {result}")]

# Resource: Config
@server.resource("config://app")
async def get_config() -> str:
    """Application configuration."""
    return '{"version": "1.0", "debug": false}'

# Prompt: Greeting
@server.prompt()
async def greeting(name: str) -> list[PromptMessage]:
    """Generate a personalized greeting."""
    return [
        PromptMessage(
            role="user",
            content=TextContent(type="text", text=f"Please greet {name} warmly.")
        )
    ]

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

---

## Building an MCP Client

### TypeScript Client

```typescript
import { McpClient, StdioClientTransport } from "@modelcontextprotocol/sdk/client";
import { spawn } from "child_process";

// Spawn server as subprocess
const serverProcess = spawn("node", ["path/to/server.js"]);

// Create client
const client = new McpClient({
  name: "my-client",
  version: "1.0.0"
});

// Connect via stdio
const transport = new StdioClientTransport({
  reader: serverProcess.stdout,
  writer: serverProcess.stdin
});

await client.connect(transport);

// Initialize and get capabilities
const capabilities = await client.initialize();
console.log("Server capabilities:", capabilities);

// List available tools
const tools = await client.listTools();
console.log("Available tools:", tools);

// Call a tool
const result = await client.callTool("calculate", {
  operation: "add",
  a: 5,
  b: 3
});
console.log("Tool result:", result);

// List and read resources
const resources = await client.listResources();
const config = await client.readResource("config://app");
console.log("Config:", config);

// Get a prompt
const prompt = await client.getPrompt("greeting", { name: "Alice" });
console.log("Prompt messages:", prompt.messages);

// Cleanup
await client.close();
serverProcess.kill();
```

### Python Client

```python
from mcp.client import ClientSession
from mcp.client.stdio import stdio_client
import subprocess
import asyncio

async def main():
    # Spawn server subprocess
    server = subprocess.Popen(
        ["python", "path/to/server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )

    # Connect client
    async with stdio_client(server.stdin, server.stdout) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()

            # List tools
            tools = await session.list_tools()
            print("Tools:", tools)

            # Call tool
            result = await session.call_tool("calculate", {
                "operation": "multiply",
                "a": 7,
                "b": 6
            })
            print("Result:", result)

            # Read resource
            config = await session.read_resource("config://app")
            print("Config:", config)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Capabilities Negotiation

Servers and clients exchange capabilities during initialization:

### Server Capabilities

```json
{
  "capabilities": {
    "tools": {
      "listChanged": true
    },
    "resources": {
      "subscribe": true,
      "listChanged": true
    },
    "prompts": {
      "listChanged": true
    },
    "logging": {}
  }
}
```

### Client Capabilities

```json
{
  "capabilities": {
    "sampling": {},
    "roots": {
      "listChanged": true
    }
  }
}
```

### Capability Flags

| Capability | Flag | Description |
|------------|------|-------------|
| `tools.listChanged` | boolean | Server sends notifications when tools change |
| `resources.subscribe` | boolean | Client can subscribe to resource updates |
| `resources.listChanged` | boolean | Server sends notifications when resources change |
| `prompts.listChanged` | boolean | Server sends notifications when prompts change |
| `sampling` | object | Client supports LLM sampling requests |
| `roots.listChanged` | boolean | Client sends notifications when roots change |

---

## Error Handling

### JSON-RPC Error Codes

| Code | Name | Description |
|------|------|-------------|
| -32700 | Parse error | Invalid JSON |
| -32600 | Invalid Request | Not a valid JSON-RPC request |
| -32601 | Method not found | Unknown method name |
| -32602 | Invalid params | Invalid method parameters |
| -32603 | Internal error | Server-side error |

### Error Response Format

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "details": "Missing required parameter: city"
    }
  }
}
```

### Best Practices

1. **Validate inputs** before processing
2. **Return descriptive errors** with actionable messages
3. **Use appropriate error codes** for different failure types
4. **Include error data** for debugging when helpful
5. **Log errors** for server-side troubleshooting

---

## Security Considerations

### Transport Security

- **stdio**: Inherently secure (same machine)
- **HTTP**: Use HTTPS in production
- **Origin validation**: Prevent DNS rebinding attacks
- **Session tokens**: Cryptographically secure (UUID, JWT)

### Input Validation

```typescript
// Always validate tool inputs
server.tool("query_database", schema, async (args) => {
  // Validate SQL to prevent injection
  if (!isValidQuery(args.query)) {
    throw new Error("Invalid query format");
  }
  // Sanitize parameters
  const sanitizedParams = sanitize(args.params);
  // Execute with prepared statements
  return await db.query(args.query, sanitizedParams);
});
```

### Resource Access

```typescript
// Validate resource URIs
server.resource("file://{path}", async (uri, params) => {
  const path = params.path;
  // Prevent directory traversal
  if (path.includes("..") || path.startsWith("/")) {
    throw new Error("Invalid path");
  }
  // Check allowed directories
  if (!isInAllowedDirectory(path)) {
    throw new Error("Access denied");
  }
  return await readFile(path);
});
```

### Sampling Security

- **Human-in-the-loop**: Always allow user review
- **Rate limiting**: Prevent abuse
- **Content filtering**: Validate request/response content
- **Cost controls**: Set token limits

---

## Best Practices

### For Server Developers

1. **Implement clear tool descriptions** - Models rely on these to decide when to use tools
2. **Use JSON Schema properly** - Define required fields, types, and constraints
3. **Return structured content** - Use appropriate content types (text, image, resource)
4. **Handle errors gracefully** - Provide actionable error messages
5. **Support notifications** - Emit `listChanged` when capabilities update
6. **Implement pagination** - For large resource/tool lists
7. **Document your server** - Describe capabilities and usage patterns

### For Client Developers

1. **Handle all message types** - Requests, responses, notifications
2. **Implement timeout handling** - Don't block indefinitely
3. **Support reconnection** - Handle transport failures gracefully
4. **Respect capabilities** - Only use features the server supports
5. **Implement human-in-the-loop** - For sampling requests
6. **Cache appropriately** - Tools/resources/prompts lists

### Security Best Practices

1. **Validate all inputs** - Never trust user or model input
2. **Use least privilege** - Request only necessary permissions
3. **Sanitize outputs** - Prevent injection attacks
4. **Implement rate limiting** - Protect against abuse
5. **Log audit trails** - Track all operations
6. **Use secure transports** - HTTPS for remote, validate origins

---

## Production Operations

### Performance Targets

Production MCP servers should target:

| Metric | Target | Notes |
|--------|--------|-------|
| **Throughput** | >1,000 req/sec | Per instance |
| **Latency (P95)** | <100ms | Simple operations |
| **Error Rate** | <0.1% | Under normal conditions |
| **Availability** | >99.9% | Uptime target |

### Architectural Principles

**Single Responsibility**: Each server should have one clear, well-defined purpose:
```
✅ weather-server     → Only weather data
✅ database-server    → Only database operations
❌ everything-server  → Too broad, hard to maintain
```

**Defense in Depth**: Layer security controls:
```
Network → Authentication → Authorization → Input Validation → Output Sanitization
```

**Fail-Safe Design**: Graceful degradation:
- Circuit breakers for external APIs
- Caching fallbacks when services are down
- Safe defaults when configuration missing

### Health Checks

Expose comprehensive health endpoints:
```json
{
  "status": "healthy",
  "checks": {
    "database": "connected",
    "cache": "available",
    "external_api": "reachable",
    "disk_space": "sufficient",
    "memory": "normal"
  },
  "uptime": 86400,
  "version": "1.0.0"
}
```

### Monitoring & Observability

**Key Metrics to Collect:**
- Request count, latency (P50, P95, P99)
- Active connections
- Error count by type
- Resource usage (CPU, memory)

**Structured Logging:**
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "info",
  "client_id": "client-123",
  "method": "tools/call",
  "tool": "get_weather",
  "duration_ms": 45,
  "status": "success"
}
```

---

## Testing and Debugging

### MCP Inspector

The MCP Inspector is an interactive developer tool for testing and debugging MCP servers. It provides a web-based interface without requiring installation.

**Basic Usage:**
```bash
# Run directly via npx (no installation needed)
npx @modelcontextprotocol/inspector <command>

# With arguments
npx @modelcontextprotocol/inspector <command> <arg1> <arg2>
```

**Inspecting Different Server Types:**
```bash
# NPM packages
npx -y @modelcontextprotocol/inspector npx @modelcontextprotocol/server-filesystem /path/to/dir

# PyPI packages
npx @modelcontextprotocol/inspector uvx mcp-server-git --repository ~/code/repo.git

# Local TypeScript server
npx @modelcontextprotocol/inspector node path/to/server/index.js args...

# Local Python server
npx @modelcontextprotocol/inspector uv --directory path/to/server run package-name args...
```

**Inspector UI Panels:**

| Panel | Purpose |
|-------|---------|
| **Server Connection** | Configure transport, command-line args, environment variables |
| **Resources Tab** | List resources, view metadata, inspect content, test subscriptions |
| **Prompts Tab** | View templates, test with custom arguments, preview generated messages |
| **Tools Tab** | Browse tool schemas, test with custom inputs, view execution results |
| **Notifications** | Monitor server logs and notifications in real-time |

**Development Workflow:**

```
┌─────────────────────────────────────────────────────────────┐
│                INSPECTOR DEVELOPMENT WORKFLOW                │
└─────────────────────────────────────────────────────────────┘

1. VERIFICATION
   • Launch Inspector with your server
   • Verify basic connectivity
   • Check capability negotiation

2. ITERATION
   • Make server code changes
   • Rebuild server
   • Reconnect Inspector
   • Test affected features
   • Monitor JSON-RPC messages

3. EDGE CASES
   • Test invalid inputs
   • Missing prompt arguments
   • Concurrent operations
   • Verify error handling
```

**Repository:** https://github.com/modelcontextprotocol/inspector

### Debugging Tips

1. **Enable verbose logging** - Set `DEBUG=mcp:*` environment variable
2. **Inspect JSON-RPC messages** - Log raw request/response pairs
3. **Test tools individually** - Before integrating with clients
4. **Validate schemas** - Ensure input/output schemas are correct
5. **Check capabilities** - Verify both sides support required features

### Common Debugging Scenarios

**Server won't connect:**
```bash
# Check if server starts independently
node path/to/server.js

# Check for port conflicts
lsof -i :3000

# Verify environment variables are set
env | grep API_KEY
```

**Tool calls failing:**
```typescript
// Add debug logging to tool handler
server.tool("my_tool", schema, async (args) => {
  console.error("Tool called with:", JSON.stringify(args));
  try {
    const result = await processArgs(args);
    console.error("Tool result:", JSON.stringify(result));
    return result;
  } catch (error) {
    console.error("Tool error:", error);
    throw error;
  }
});
```

**Capability mismatch:**
```bash
# In Inspector, check the initialization exchange:
# 1. Client capabilities sent
# 2. Server capabilities returned
# 3. Verify both sides support required features
```

### Claude Desktop Debugging

**Log locations:**
```bash
# macOS
~/Library/Logs/Claude/mcp*.log

# Windows
%APPDATA%\Claude\logs\mcp*.log

# Linux
~/.config/Claude/logs/mcp*.log

# Real-time log monitoring (macOS)
tail -n 20 -F ~/Library/Logs/Claude/mcp*.log
```

**Enable Chrome DevTools:**
```bash
# Create developer settings file
echo '{"allowDevTools": true}' > ~/Library/Application\ Support/Claude/developer_settings.json

# Access DevTools: Command-Option-Shift-i (macOS)
# Use Console panel for client-side errors
# Use Network panel for message payloads and timing
```

**Checking Server Status in Claude Desktop:**
- Click the **plug icon** to view connected servers, available prompts, and resources
- Click the **"Search and tools" slider icon** to view tools available to the model

**Common issues:**
- Malformed JSON in config file
- Relative paths instead of absolute (servers often start with `/` as working directory)
- Missing environment variables (servers only inherit `USER`, `HOME`, `PATH` by default)
- Rate limiting from external APIs

**Environment Variable Gotcha:**
```json
{
  "myserver": {
    "command": "mcp-server-myapp",
    "env": {
      "MYAPP_API_KEY": "your-key-here",
      "DATABASE_URL": "postgres://localhost/mydb"
    }
  }
}
```

**Reloading Changes:**
- **Configuration changes**: Restart Claude Desktop completely
- **Server code changes**: Use `Command-R` to reload servers

### Server-Side Logging

**Important**: Log to stderr, NOT stdout (stdout interferes with JSON-RPC protocol).

**Python:**
```python
import sys

# Direct stderr logging
print("Debug: Processing request", file=sys.stderr)

# Using MCP logging API
server.request_context.session.send_log_message(
    level="info",
    data="Server started successfully"
)
```

**TypeScript:**
```typescript
// Direct stderr logging
console.error("Debug: Processing request");

// Using MCP logging API
server.sendLoggingMessage({
  level: "info",
  data: "Server started successfully"
});
```

**What to Log:**
- Initialization steps and configuration loaded
- Resource access (URI, user, timestamp)
- Tool execution (name, arguments, duration, result type)
- Error conditions with stack traces
- Performance metrics (operation timing, message sizes)

### Debugging Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    DEBUGGING WORKFLOW                        │
└─────────────────────────────────────────────────────────────┘

1. INITIAL DEVELOPMENT
   └─ Use MCP Inspector for basic testing
   └─ Implement core functionality
   └─ Add logging at key points

2. INTEGRATION TESTING
   └─ Test in Claude Desktop
   └─ Monitor logs in real-time
   └─ Check error handling paths

3. TROUBLESHOOTING
   └─ Check server logs first
   └─ Verify configuration syntax
   └─ Test standalone with Inspector
   └─ Review environment variables
```

### Getting Help

**First steps:**
1. Check server logs for errors
2. Test with MCP Inspector standalone
3. Review `claude_desktop_config.json` syntax
4. Verify environment variables are set

**When reporting issues, provide:**
- Relevant log excerpts
- Configuration files (sanitized)
- Steps to reproduce
- Environment details (OS, Node/Python version)

---

## Integration Patterns

### Claude Desktop Configuration

Add MCP servers to Claude Desktop's configuration:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/path/to/server.js"],
      "env": {
        "API_KEY": "your-key"
      }
    },
    "remote-server": {
      "url": "https://mcp.example.com/",
      "headers": {
        "Authorization": "Bearer token"
      }
    }
  }
}
```

### AI SDK Integration

MCP works with various AI frameworks:

```typescript
// With Vercel AI SDK
import { experimental_createMCPClient } from "ai";

const mcpClient = await experimental_createMCPClient({
  transport: { type: "stdio", command: "node", args: ["server.js"] }
});

const tools = await mcpClient.tools();
// Use tools with AI model...
```

---

## Resources

### Official Documentation
- [MCP Website](https://modelcontextprotocol.io/)
- [Specification](https://modelcontextprotocol.io/specification)
- [Getting Started](https://modelcontextprotocol.io/docs/getting-started/intro)

### SDKs
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Go SDK](https://github.com/modelcontextprotocol/go-sdk)
- [All SDKs](https://github.com/modelcontextprotocol)

### Tools
- [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector)
- [MCP Servers Directory](https://github.com/modelcontextprotocol/servers)

### Community
- [GitHub Discussions](https://github.com/modelcontextprotocol/specification/discussions)
- [Discord](https://discord.gg/anthropic)

---

## Version History

- **1.4.0** (2026-01-10): Enhanced with comprehensive debugging documentation
  - Enhanced Claude Desktop Debugging:
    - Real-time log monitoring commands
    - Chrome DevTools integration (enable, access, panels)
    - Server status checking via UI icons
    - Environment variable inheritance gotcha (`USER`, `HOME`, `PATH` only)
    - Reloading changes (config vs code)
  - Added Server-Side Logging section:
    - stderr vs stdout importance
    - Python and TypeScript logging examples
    - MCP logging API usage
    - What to log checklist
  - Added Debugging Workflow diagram
  - Added Getting Help section with issue reporting guidance

- **1.3.0** (2026-01-10): Enhanced Testing and Debugging with MCP Inspector
  - Comprehensive MCP Inspector documentation:
    - Installation-free usage via npx
    - Commands for NPM, PyPI, and local servers
    - UI panels table (Server Connection, Resources, Prompts, Tools, Notifications)
    - Development workflow diagram (Verification → Iteration → Edge Cases)
  - Added Common Debugging Scenarios section:
    - Server connection troubleshooting
    - Tool call debugging with logging examples
    - Capability mismatch diagnosis
  - Added Claude Desktop Debugging:
    - Log file locations (macOS, Windows, Linux)
    - Common configuration issues

- **1.2.0** (2026-01-10): Enhanced with official documentation content
  - Added AI Integration Paradox design philosophy
  - Added Mediated Access Pattern (security broker model)
  - Added Production Operations section:
    - Performance targets (throughput, latency, error rate)
    - Architectural principles (single responsibility, defense in depth)
    - Health checks and monitoring patterns
    - Structured logging examples
  - Enhanced protocol overview with dynamic discovery concepts

- **1.1.0** (2026-01-10): Enhanced with official specification details
  - Added specification version reference (2024-11-05)
  - Enhanced JSON-RPC requirements (id uniqueness, null prohibition)
  - Added detailed lifecycle with version negotiation
  - Added shutdown procedures (stdio vs HTTP)
  - Added tool `isError` handling for execution errors
  - Added resource templates with URI Template syntax (RFC 6570)
  - Added blob content type for binary resources
  - Added Utilities section:
    - Ping (connection health)
    - Cancellation (notifications/cancelled)
    - Progress notifications
    - Completion (auto-complete)
    - Logging (notifications/message)
    - Pagination (cursor-based)

- **1.0.0** (2026-01-10): Initial skill release
  - Complete protocol overview (architecture, primitives, transports)
  - Server development guide (tools, resources, prompts)
  - Client development guide (connecting, calling, sampling)
  - 10 SDKs documented (TypeScript, Python, Go, Kotlin, Swift, Java, C#, Ruby, Rust, PHP)
  - Security best practices
  - Testing and debugging guidance
  - Integration patterns (Claude Desktop, AI SDKs)
