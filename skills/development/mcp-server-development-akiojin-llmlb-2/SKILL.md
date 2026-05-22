---
name: mcp-server-development
description: Expert guidance for building MCP (Model Context Protocol) servers using the TypeScript SDK. Use when developing MCP servers, implementing tools/resources/prompts, or working with the @modelcontextprotocol/sdk package. Covers server initialization, request handlers, Zod schemas, error handling, and JSON-RPC patterns.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

This skill provides comprehensive guidance for building robust MCP servers, with specific focus on the unity-mcp-server architecture and patterns.

## Core Philosophy

MCP servers bridge AI assistants to external systems. They must be:
- **Reliable**: Handle errors gracefully, never crash unexpectedly
- **Discoverable**: Tools should have clear, self-documenting schemas
- **Performant**: Minimize latency, especially for stdio transport
- **Protocol-compliant**: Follow JSON-RPC 2.0 and MCP spec exactly

## Architecture Patterns

### Handler-Based Design

**ALWAYS** use a handler class per tool. Each handler encapsulates:
- Input validation (Zod schema)
- Business logic execution
- Error handling and response formatting

```javascript
// Pattern: One handler per tool
export class SystemPingToolHandler extends BaseToolHandler {
  constructor(unityConnection) {
    super({
      name: 'system_ping',
      description: 'Check Unity Editor connectivity',
      inputSchema: { type: 'object', properties: {} }
    });
    this.unityConnection = unityConnection;
  }

  async execute(params) {
    const result = await this.unityConnection.send({ command: 'ping' });
    return { status: 'ok', ...result };
  }
}
```

### BaseToolHandler Contract

All handlers MUST:
1. Call `super()` with tool metadata
2. Implement `execute(params)` method
3. Return plain objects (framework handles JSON-RPC wrapping)
4. Throw errors with descriptive messages

### Input Validation with Zod

**ALWAYS** validate inputs before processing:

```javascript
import { z } from 'zod';

const inputSchema = z.object({
  name: z.string().min(1).describe('GameObject name'),
  primitiveType: z.enum(['cube', 'sphere', 'cylinder']).optional()
});

validate(input) {
  return inputSchema.parse(input);
}
```

## Transport Layer

### Content-Length Framing (Standard)

MCP uses LSP-style Content-Length framing for stdio:

```
Content-Length: 123\r\n
\r\n
{"jsonrpc":"2.0","id":1,"method":"tools/call"...}
```

**ALWAYS** use Content-Length for output. NEVER mix framing formats in a session.

### Hybrid Input (Compatibility)

Accept both Content-Length and NDJSON input for client compatibility:
- Claude Desktop: Content-Length
- Some CLI tools: NDJSON (newline-delimited)

## Error Handling

### Structured Errors

Use MCP error codes from the spec:

```javascript
const McpError = {
  ParseError: -32700,
  InvalidRequest: -32600,
  MethodNotFound: -32601,
  InvalidParams: -32602,
  InternalError: -32603
};

throw new Error(JSON.stringify({
  code: McpError.InvalidParams,
  message: 'primitiveType must be one of: cube, sphere, cylinder'
}));
```

### Error Response Format

```javascript
{
  jsonrpc: '2.0',
  id: requestId,
  error: {
    code: -32602,
    message: 'Invalid params',
    data: { field: 'name', issue: 'required' }
  }
}
```

## Unity-Specific Patterns

### Command Protocol

Unity communication uses a simple request/response pattern:

```javascript
const result = await this.unityConnection.send({
  command: 'gameobject_create',
  params: { name: 'Cube', primitiveType: 'cube' }
});
```

### Workspace Root Resolution

**ALWAYS** include `workspaceRoot` in commands requiring file paths:

```javascript
execute(params) {
  return this.unityConnection.send({
    command: 'screenshot_capture',
    workspaceRoot: config.workspaceRoot,
    ...params
  });
}
```

## Testing Patterns

### TDD for Handlers

1. **Contract test first**: Define expected input/output schema
2. **Mock Unity connection**: Isolate handler logic
3. **Test error paths**: Invalid input, connection failures
4. **Test happy path last**: After contracts are verified

```javascript
describe('CreateGameObjectHandler', () => {
  it('validates primitiveType enum', async () => {
    const handler = new CreateGameObjectHandler(mockConnection);
    await assert.rejects(
      () => handler.handle({ name: 'Cube', primitiveType: 'invalid' }),
      /primitiveType must be one of/
    );
  });
});
```

### Integration Testing

Test full request/response cycle including JSON-RPC framing:

```javascript
const stdin = new PassThrough();
const stdout = new PassThrough();
const transport = new HybridStdioServerTransport(stdin, stdout);

stdin.write('Content-Length: 50\r\n\r\n{"jsonrpc":"2.0","id":1,"method":"ping"}');
// Assert stdout contains Content-Length response
```

## Common Mistakes

**Mixing framing formats**:
- NEVER: Output NDJSON after receiving Content-Length input
- ALWAYS: Output Content-Length regardless of input format

**Swallowing errors**:
- NEVER: `catch (e) { return null; }`
- ALWAYS: Propagate errors with context

**Missing validation**:
- NEVER: Trust raw input from clients
- ALWAYS: Validate with Zod before processing

**Blocking stdio**:
- NEVER: Synchronous operations on transport
- ALWAYS: Use async/await throughout

## Handler Registration

Register all handlers in a central index:

```javascript
// src/handlers/index.js
export function createHandlers(unityConnection) {
  return [
    new SystemPingToolHandler(unityConnection),
    new CreateGameObjectHandler(unityConnection),
    new ScreenshotHandler(unityConnection),
    // ...
  ];
}
```

## Remember

- **Content-Length always**: Output framing must be consistent
- **Validate everything**: Never trust client input
- **One handler, one tool**: Keep handlers focused
- **Test error paths**: Most bugs hide in error handling
- **Protocol compliance**: Follow JSON-RPC 2.0 exactly
