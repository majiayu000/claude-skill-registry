---
name: mcp-development
description: Build Model Context Protocol (MCP) servers and clients. Create custom tool providers, resource handlers, and prompt templates. Use for extending Claude Code, building AI integrations, and creating reusable MCP components. Covers TypeScript and Python SDKs.
---

# MCP Server Development Skill

## Triggers

Use this skill when you see:
- mcp, model context protocol, tool provider
- mcp server, mcp client, mcp tools
- resources, prompts, sampling
- claude code extension, ai integration

## Instructions

### MCP Architecture Overview

MCP (Model Context Protocol) enables AI models to interact with external systems through:
- **Tools**: Functions the AI can call
- **Resources**: Data the AI can read
- **Prompts**: Pre-defined prompt templates
- **Sampling**: Request AI completions

### TypeScript MCP Server

#### Project Setup

```bash
# Initialize project
mkdir my-mcp-server && cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node tsx

# Configure TypeScript
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "declaration": true
  },
  "include": ["src/**/*"]
}
EOF
```

#### Basic Server Structure

```typescript
// src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";

// Create server instance
const server = new Server(
  {
    name: "my-mcp-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
      resources: {},
    },
  }
);

// Define tool input schemas
const ExampleToolSchema = z.object({
  input: z.string().describe("Input parameter"),
  optional: z.number().optional().describe("Optional number"),
});

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "example_tool",
        description: "An example tool that processes input",
        inputSchema: {
          type: "object",
          properties: {
            input: { type: "string", description: "Input parameter" },
            optional: { type: "number", description: "Optional number" },
          },
          required: ["input"],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "example_tool") {
    const parsed = ExampleToolSchema.parse(args);

    // Tool implementation
    const result = `Processed: ${parsed.input}`;

    return {
      content: [
        {
          type: "text",
          text: result,
        },
      ],
    };
  }

  throw new Error(`Unknown tool: ${name}`);
});

// List resources
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: "example://data",
        name: "Example Data",
        description: "Sample resource data",
        mimeType: "application/json",
      },
    ],
  };
});

// Read resources
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;

  if (uri === "example://data") {
    return {
      contents: [
        {
          uri,
          mimeType: "application/json",
          text: JSON.stringify({ key: "value" }),
        },
      ],
    };
  }

  throw new Error(`Unknown resource: ${uri}`);
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MCP server running on stdio");
}

main().catch(console.error);
```

#### Package Configuration

```json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "bin": {
    "my-mcp-server": "./dist/index.js"
  },
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx src/index.ts"
  }
}
```

### Python MCP Server

#### Project Setup

```bash
# Create project with uv
uv init my-mcp-server
cd my-mcp-server
uv add mcp pydantic

# Or with pip
pip install mcp pydantic
```

#### Basic Server Structure

```python
# src/server.py
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    Resource,
    ResourceContents,
)
from pydantic import BaseModel, Field

# Create server
server = Server("my-mcp-server")

# Define input models
class ExampleInput(BaseModel):
    input: str = Field(description="Input parameter")
    optional: int | None = Field(default=None, description="Optional number")

# List tools
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="example_tool",
            description="An example tool that processes input",
            inputSchema=ExampleInput.model_json_schema(),
        )
    ]

# Handle tool calls
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "example_tool":
        args = ExampleInput(**arguments)
        result = f"Processed: {args.input}"
        return [TextContent(type="text", text=result)]

    raise ValueError(f"Unknown tool: {name}")

# List resources
@server.list_resources()
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri="example://data",
            name="Example Data",
            description="Sample resource data",
            mimeType="application/json",
        )
    ]

# Read resources
@server.read_resource()
async def read_resource(uri: str) -> ResourceContents:
    if uri == "example://data":
        return ResourceContents(
            uri=uri,
            mimeType="application/json",
            text='{"key": "value"}',
        )

    raise ValueError(f"Unknown resource: {uri}")

# Main entry point
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())
```

### Claude Code Configuration

Add to `~/.claude/mcp-servers.json` or project's `.claude/mcp-servers.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/path/to/dist/index.js"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    },
    "python-server": {
      "command": "python",
      "args": ["-m", "my_mcp_server"],
      "cwd": "/path/to/project"
    }
  }
}
```

### Advanced Patterns

#### Error Handling

```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    // Tool logic
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error instanceof Error ? error.message : "Unknown error"}`,
        },
      ],
      isError: true,
    };
  }
});
```

#### Streaming Results

```typescript
// For long-running operations, return progress updates
return {
  content: [
    { type: "text", text: "Step 1 complete..." },
    { type: "text", text: "Step 2 complete..." },
    { type: "text", text: "Final result: success" },
  ],
};
```

#### Dynamic Resources

```typescript
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  // Fetch available resources dynamically
  const files = await fs.readdir("/data");
  return {
    resources: files.map((file) => ({
      uri: `file://${file}`,
      name: file,
      mimeType: "text/plain",
    })),
  };
});
```

### Testing MCP Servers

```bash
# Test with MCP Inspector
npx @modelcontextprotocol/inspector node dist/index.js

# Manual testing via stdio
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | node dist/index.js
```

### Best Practices

1. **Clear Tool Descriptions**: Help AI understand when to use each tool
2. **Validate Inputs**: Use Zod/Pydantic for type safety
3. **Handle Errors Gracefully**: Return helpful error messages
4. **Minimize Side Effects**: Tools should be predictable
5. **Document Resources**: Clear descriptions and MIME types
6. **Version Your Server**: Semantic versioning for compatibility
7. **Test Thoroughly**: Use MCP Inspector for debugging
8. **Environment Variables**: Use for secrets and configuration
