---
name: script-kit-mcp
description: |
  Model Context Protocol (MCP) implementation for Script Kit. Use when working with MCP server, JSON-RPC 2.0 protocol, kit tools, script tools, resources, or SSE streaming. Triggers on: "mcp", "json-rpc", "kit tools", "script tools", "resources", "sse streaming", "audit logging".
---

# Script Kit MCP Implementation

MCP (Model Context Protocol) enables AI agents to interact with Script Kit via JSON-RPC 2.0.

## Architecture Overview

```
mcp_server.rs      HTTP server on localhost:43210
    |
    v
mcp_protocol.rs    JSON-RPC 2.0 request/response handling
    |
    +---> mcp_kit_tools.rs      kit/* namespace tools
    +---> mcp_script_tools.rs   scripts/* namespace tools
    +---> mcp_resources.rs      Resource endpoints
    +---> mcp_streaming.rs      SSE streaming & audit logging
```

## Core Modules

### mcp_protocol.rs - JSON-RPC 2.0 Protocol

Handles request parsing, method routing, and response generation.

**Supported Methods:**
- `initialize` - Returns server capabilities
- `tools/list` - Lists all available tools
- `tools/call` - Executes a tool
- `resources/list` - Lists all resources
- `resources/read` - Reads a resource

**Key Types:**
```rust
pub struct JsonRpcRequest {
    pub jsonrpc: String,  // Must be "2.0"
    pub id: Value,        // Request identifier
    pub method: String,   // Method name
    pub params: Value,    // Optional parameters
}

pub struct JsonRpcResponse {
    pub jsonrpc: String,
    pub id: Value,
    pub result: Option<Value>,  // Success
    pub error: Option<JsonRpcError>,  // Failure
}
```

**Error Codes:**
- `-32700` PARSE_ERROR - Invalid JSON
- `-32600` INVALID_REQUEST - Invalid request object
- `-32601` METHOD_NOT_FOUND - Method not found
- `-32602` INVALID_PARAMS - Invalid parameters
- `-32603` INTERNAL_ERROR - Internal error

### mcp_server.rs - HTTP Server

Lightweight HTTP server using `std::net` (no async runtime).

**Features:**
- Runs on `localhost:43210` (configurable via `MCP_PORT`)
- Bearer token authentication from `~/.scriptkit/agent-token`
- Discovery file at `~/.scriptkit/server.json`
- Health endpoint at `GET /health`
- RPC endpoint at `POST /rpc`

**Server Lifecycle:**
```rust
let server = McpServer::with_defaults()?;
let handle = server.start()?;  // Starts in background thread
// ... server runs ...
handle.stop();  // Graceful shutdown
```

### mcp_kit_tools.rs - Kit Tools

Built-in tools in the `kit/*` namespace.

**Available Tools:**
| Tool | Description |
|------|-------------|
| `kit/show` | Show the Script Kit window |
| `kit/hide` | Hide the Script Kit window |
| `kit/state` | Get current app state |

**Tool Result Format:**
```rust
pub struct ToolResult {
    pub content: Vec<ToolContent>,
    #[serde(rename = "isError")]
    pub is_error: Option<bool>,  // Serializes as "isError" in JSON
}
```

### mcp_script_tools.rs - Script Tools

Auto-generates MCP tools from scripts with `schema.input`.

**Tool Naming:** `scripts/{script-name-slug}`
- "Create Note" -> `scripts/create-note`
- "Git Commit" -> `scripts/git-commit`

**Script Requirements:**
- Must have `schema = { input: {...} }` in metadata
- Empty `schema.input` is excluded

**Key Functions:**
```rust
// Generate tool definitions from scripts
pub fn get_script_tool_definitions(scripts: &[Arc<Script>]) -> Vec<ToolDefinition>

// Check if tool is in scripts/* namespace
pub fn is_script_tool(name: &str) -> bool

// Handle script tool calls
pub fn handle_script_tool_call(scripts, tool_name, arguments) -> ScriptToolResult
```

### mcp_resources.rs - Resources

Read-only data accessible via resource URIs.

**Available Resources:**
| URI | Description |
|-----|-------------|
| `kit://state` | Current app state (visible, focused, counts) |
| `scripts://` | List of available scripts |
| `scriptlets://` | List of available scriptlets |

**Resource Content Format:**
```rust
pub struct ResourceContent {
    pub uri: String,
    #[serde(rename = "mimeType")]
    pub mime_type: String,  // Serializes as "mimeType", value is "application/json"
    pub text: String,       // JSON stringified content
}
```

### mcp_streaming.rs - SSE Streaming & Audit

**SSE Event Types:**
- `progress` - Progress updates
- `output` - Output data
- `error` - Error messages
- `complete` - Completion notification

**SSE Format:**
```
event: progress
data: {"message":"working","progress":50}

```

**Audit Logging:**
Writes to `~/.scriptkit/logs/mcp-audit.jsonl`

```rust
pub struct AuditLogEntry {
    pub timestamp: String,    // ISO 8601
    pub method: String,       // Tool/method name
    pub params: Value,        // Parameters
    pub duration_ms: u64,     // Duration
    pub success: bool,        // Success flag
    pub error: Option<String>, // Error if failed
}
```

## Usage Patterns

### Adding a New Kit Tool

1. Add tool definition in `mcp_kit_tools.rs`:
```rust
ToolDefinition {
    name: "kit/new-tool".to_string(),
    description: "Description".to_string(),
    input_schema: serde_json::json!({
        "type": "object",
        "properties": {
            "param": { "type": "string" }
        }
    }),
}
```

2. Handle in `handle_kit_tool_call`:
```rust
"kit/new-tool" => ToolResult { ... }
```

### Making a Script Callable via MCP

Add schema to script metadata:
```typescript
// Name: My Script
// Description: Does something
schema = {
  input: {
    title: { type: "string", required: true, description: "Title" },
    count: { type: "number", min: 0, max: 100 }
  }
}
```

### Adding a New Resource

1. Add to `get_resource_definitions()`:
```rust
McpResource {
    uri: "new://resource".to_string(),
    name: "New Resource".to_string(),
    description: Some("Description".to_string()),
    mime_type: "application/json".to_string(),
}
```

2. Handle in `read_resource()`:
```rust
"new://resource" => read_new_resource(...)
```

## Testing

All modules use TDD with tests written first.

```bash
# Run MCP tests
cargo test mcp_

# Run specific module tests
cargo test mcp_protocol
cargo test mcp_server
cargo test mcp_kit_tools
cargo test mcp_script_tools
cargo test mcp_resources
cargo test mcp_streaming
```

## References

- [MCP Architecture](references/architecture.md) - Detailed module interactions
- [JSON-RPC 2.0 Spec](https://www.jsonrpc.org/specification)
- [MCP Specification](https://modelcontextprotocol.io/specification)
