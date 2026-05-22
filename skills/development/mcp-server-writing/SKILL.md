---
name: mcp-server-writing
description: Creates production-ready MCP servers with tools, resources, and prompts using TypeScript SDK or Python FastMCP. Use when building MCP integrations for Claude or LLM applications.
version: 1.0.0
---

# MCP Server Writing

## Purpose

Guide creation of production-ready Model Context Protocol (MCP) servers following official SDK patterns, security best practices, and real-world implementation patterns.

## When to Use This Skill

- Building a new MCP server from scratch
- Adding tools, resources, or prompts to an existing MCP server
- Choosing between TypeScript and Python implementations
- Implementing proper error handling and validation for MCP tools
- Setting up structured logging for MCP servers

## When NOT to Use This Skill

- Reviewing existing MCP code (use **mcp-server-reviewing**)
- Building simple CLI tools that don't need LLM integration
- Creating HTTP REST APIs (MCP uses JSON-RPC, not REST)
- General TypeScript/Python development unrelated to MCP

---

## Quick Decision: TypeScript vs Python

| Factor                   | TypeScript          | Python FastMCP    |
| ------------------------ | ------------------- | ----------------- |
| **Type Safety**          | Excellent (Zod/Ajv) | Good (type hints) |
| **Schema Validation**    | Built-in with Zod   | Decorator-based   |
| **Prototyping Speed**    | Medium              | Fast              |
| **Production Readiness** | High                | High              |
| **Ecosystem**            | Node.js, npm        | pip, uv           |

**Recommendation:** Use TypeScript for production servers with complex schemas. Use Python FastMCP for rapid prototyping or when integrating with Python libraries.

---

## Core Workflow

### Step 1: Initialize Server

**TypeScript:**

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server(
  { name: "my-mcp-server", version: "1.0.0" },
  { capabilities: { tools: {} } },
);
```

**Python FastMCP:**

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-mcp-server", json_response=True)
```

### Step 2: Define Tools with Input Schemas

Tools are functions the LLM can call. Always include:

- Clear `description` explaining what the tool does
- `inputSchema` with property descriptions
- Validation before processing

**TypeScript (Low-Level API):**

```typescript
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";

const TOOLS: Tool[] = [
  {
    name: "process_data",
    description:
      "Validates and transforms input data. Returns structured result with any validation errors.",
    inputSchema: {
      type: "object",
      properties: {
        data: {
          type: "string",
          description: "Raw data string to process",
        },
        format: {
          type: "string",
          enum: ["json", "csv", "xml"],
          description: "Expected input format",
        },
      },
      required: ["data", "format"],
    },
  },
];

server.setRequestHandler(ListToolsRequestSchema, () => ({ tools: TOOLS }));
```

**Python FastMCP:**

```python
@mcp.tool()
def process_data(data: str, format: str = "json") -> dict:
    """Validates and transforms input data.

    Args:
        data: Raw data string to process
        format: Expected input format (json, csv, xml)

    Returns:
        Structured result with validation errors if any
    """
    # Implementation here
    return {"success": True, "processed": data}
```

### Step 3: Implement Tool Handler with Validation

**Critical:** Always validate inputs before processing. Use Ajv for TypeScript.

```typescript
import Ajv from "ajv";

const ajv = new Ajv();
const validateProcessDataArgs = ajv.compile({
  type: "object",
  properties: {
    data: { type: "string" },
    format: { type: "string", enum: ["json", "csv", "xml"] },
  },
  required: ["data", "format"],
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "process_data") {
    // Validate inputs
    if (!validateProcessDataArgs(args)) {
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              error: "Validation failed",
              details: validateProcessDataArgs.errors,
              suggestion: "Check input parameters match the schema",
            }),
          },
        ],
        isError: true,
      };
    }

    // Process valid inputs
    const result = processData(args.data, args.format);
    return {
      content: [{ type: "text", text: JSON.stringify(result) }],
    };
  }

  return {
    content: [{ type: "text", text: `Unknown tool: ${name}` }],
    isError: true,
  };
});
```

### Step 4: Add Resources (Optional)

Resources expose data the LLM can read. Use for configuration, status, or reference data.

**TypeScript:**

```typescript
import {
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

server.setRequestHandler(ListResourcesRequestSchema, () => ({
  resources: [
    {
      uri: "config://settings",
      name: "Application Settings",
      description: "Current server configuration",
      mimeType: "application/json",
    },
  ],
}));

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  if (request.params.uri === "config://settings") {
    return {
      contents: [
        {
          uri: "config://settings",
          mimeType: "application/json",
          text: JSON.stringify({ theme: "dark", version: "1.0.0" }),
        },
      ],
    };
  }
  throw new Error(`Unknown resource: ${request.params.uri}`);
});
```

**Python FastMCP:**

```python
@mcp.resource("config://settings")
def get_settings() -> str:
    """Current server configuration."""
    return json.dumps({"theme": "dark", "version": "1.0.0"})
```

### Step 5: Add Prompts (Optional)

Prompts are reusable templates the LLM can request.

**Python FastMCP:**

```python
@mcp.prompt()
def review_code(code: str, language: str = "python") -> str:
    """Generate a code review prompt."""
    return f"Please review this {language} code for best practices:\n\n{code}"
```

### Step 6: Implement Structured Logging

**Critical for MCP:** Log to stderr, NEVER stdout. stdout is reserved for JSON-RPC.

```typescript
// utils/logger.ts
class Logger {
  private log(level: string, message: string, context?: object): void {
    const entry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      service: "my-mcp-server",
      ...context,
    };
    // CRITICAL: Use stderr, not stdout
    console.error(JSON.stringify(entry));
  }

  info(message: string, context?: object): void {
    this.log("INFO", message, context);
  }

  error(message: string, context?: object, error?: Error): void {
    this.log("ERROR", message, {
      ...context,
      error: error
        ? { name: error.name, message: error.message, stack: error.stack }
        : undefined,
    });
  }
}

export const logger = new Logger();
```

### Step 7: Start the Server

**TypeScript:**

```typescript
async function main(): Promise<void> {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  logger.info("MCP Server started", { transport: "stdio" });
}

main().catch((error) => {
  logger.error("Fatal error", {}, error);
  process.exit(1);
});
```

**Python FastMCP:**

```python
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

---

## Examples

### Example 1: Tool with Validation Error Response

```typescript
// Always return actionable suggestions with errors
if (!validateArgs(args)) {
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify({
          success: false,
          errors: [
            {
              field: "partner_id",
              message: "Invalid UUID format",
              suggestion: "Use format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            },
          ],
        }),
      },
    ],
    isError: true,
  };
}
```

### Example 2: ReDoS Prevention

```typescript
// Limit input length before regex processing
const MAX_INPUT_LENGTH = 50_000;

function safeInput(text: string): string {
  return text.length > MAX_INPUT_LENGTH
    ? text.slice(0, MAX_INPUT_LENGTH)
    : text;
}

// Use in tool handlers
const safeText = safeInput(args.text);
const matches = safeText.match(/pattern/);
```

### Example 3: Dynamic Resource Template

```python
@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: str) -> str:
    """Get user profile by ID."""
    user = fetch_user(user_id)
    return json.dumps({"id": user_id, "name": user.name, "role": user.role})
```

---

## Validation Checklist

Before deploying your MCP server:

- [ ] All tools have clear `description` fields
- [ ] All input schema properties have `description`
- [ ] Input validation runs before any processing
- [ ] Error responses include `isError: true` flag
- [ ] Error messages include actionable `suggestion`
- [ ] Logging goes to stderr (not stdout)
- [ ] Input length limited before regex processing (ReDoS prevention)
- [ ] No hardcoded secrets in code
- [ ] Environment variables used for configuration

---

## Common Patterns

### Pattern: Structured Error Response

```typescript
interface ToolError {
  field: string;
  message: string;
  suggestion: string;
}

function createErrorResponse(errors: ToolError[]) {
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify({ success: false, errors }),
      },
    ],
    isError: true,
  };
}
```

### Pattern: Tool Invocation Logging

```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  const startTime = Date.now();

  logger.info("Tool invocation started", {
    tool: name,
    args_keys: Object.keys(args || {}),
  });

  try {
    const result = await handleTool(name, args);
    logger.info("Tool invocation completed", {
      tool: name,
      duration_ms: Date.now() - startTime,
    });
    return result;
  } catch (error) {
    logger.error(
      "Tool invocation failed",
      {
        tool: name,
        duration_ms: Date.now() - startTime,
      },
      error,
    );
    throw error;
  }
});
```

---

## Troubleshooting

### Issue: Server hangs or produces garbled output

**Cause:** Logging to stdout instead of stderr
**Solution:** Change all `console.log()` to `console.error()` for logging

### Issue: Validation errors not shown to LLM

**Cause:** Missing `isError: true` in response
**Solution:** Add `isError: true` to all error responses

### Issue: Complex regex causes timeouts

**Cause:** ReDoS vulnerability with unbounded input
**Solution:** Limit input length with `safeInput()` function

---

## Related Skills

- **mcp-server-reviewing** - Audit MCP servers for best practices
- **security-scan** - Check for secrets before commits
- **quality-check** - Run linting and formatting

## Resources

- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Best Practices](https://modelcontextprotocol.info/docs/best-practices/)
- See **REFERENCE.md** for complete templates and advanced patterns
