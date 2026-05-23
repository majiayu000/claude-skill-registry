---
name: mcp-protocol-fundamentals
version: "1.0"
description: >
  MCP is built on JSON-RPC 2.0 for bidirectional communication between Claude and servers.
  PROACTIVELY activate for: (1) understanding MCP protocol structure, (2) JSON-RPC message formats, (3) tool vs resource distinction.
  Triggers: "mcp protocol", "json-rpc", "model context protocol"
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# MCP Protocol Fundamentals Skill

## Metadata (Tier 1)

**Keywords**: mcp, model context protocol, json-rpc, protocol, specification

**File Patterns**: **/mcp_server.py, **/protocol.py

**Modes**: backend_python, api_development

---

## Instructions (Tier 2)

### JSON-RPC 2.0 Foundation

MCP is built on **JSON-RPC 2.0** for bidirectional communication between Claude and servers.

**Request Structure**:
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {"query": "test"}
  },
  "id": 1
}
```

**Response Structure**:
```json
{
  "jsonrpc": "2.0",
  "result": {"data": "..."},
  "id": 1
}
```

**Error Response**:
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32601,
    "message": "Method not found"
  },
  "id": 1
}
```

### Core Concepts

**Tools** (Model-Controlled):
- Exposed by server, invoked by Claude
- Have strict input/output schemas (Pydantic V2)
- Can have side effects (create, update, delete)
- Examples: search_code, create_file, execute_query

**Resources** (App-Controlled):
- Provide context to Claude (read-only)
- URI-based identification (file://, db://, api://)
- Returned in list_resources, read via read_resource
- Examples: project docs, database schemas, logs

**Prompts** (Optional):
- Pre-defined prompt templates
- Can include dynamic arguments
- Help standardize common workflows

### Protocol Methods

**Server → Client** (Server exposes):
```
tools/list       → List available tools
tools/call       → Execute a tool
resources/list   → List available resources
resources/read   → Read resource content
prompts/list     → List prompt templates
prompts/get      → Get prompt with arguments
```

**Client → Server** (Server can request):
```
sampling/createMessage → Request Claude to generate text
roots/list             → Get workspace roots
```

### Message Flow

```
Claude Desktop          MCP Server
      |                      |
      |---tools/list-------->|
      |<--[tool schemas]-----|
      |                      |
      |---tools/call-------->|
      |   {name, arguments}  |
      |<--result/error-------|
```

### Pydantic V2 Integration

**CRITICAL**: Use Pydantic strict mode for all schemas.

```python
from pydantic import BaseModel, ConfigDict

class ToolInput(BaseModel):
    model_config = ConfigDict(strict=True)
    param: str

# Auto-generates inputSchema:
# {
#   "type": "object",
#   "properties": {"param": {"type": "string"}},
#   "required": ["param"]
# }
```

### Transport Layer

MCP supports two transports:

1. **stdio** (Standard I/O):
   ```python
   async def main():
       async with stdio_server() as (read, write):
           await server.run(read, write)
   ```

2. **HTTP/SSE** (Server-Sent Events):
   ```python
   @app.post("/mcp")
   async def handle_mcp(request: JsonRpcRequest):
       return await server.handle_request(request)
   ```

### Error Codes (JSON-RPC 2.0)

```
-32700 → Parse error (invalid JSON)
-32600 → Invalid request
-32601 → Method not found
-32602 → Invalid params
-32603 → Internal error
-32000 to -32099 → Server-defined errors
```

### Anti-Patterns

❌ Manual JSON schema writing (use Pydantic)
❌ Blocking operations in async handlers
❌ Missing error handling
❌ Invalid JSON-RPC 2.0 structure

---

## Resources (Tier 3)

**Official Specification**: https://spec.modelcontextprotocol.io/
**JSON-RPC 2.0 Spec**: https://www.jsonrpc.org/specification
**Python SDK**: https://github.com/modelcontextprotocol/python-sdk

**Example Servers**:
- Filesystem MCP: Read/write local files
- GitHub MCP: Repository operations
- Database MCP: SQL query execution
