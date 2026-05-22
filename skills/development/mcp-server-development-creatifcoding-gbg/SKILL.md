---
name: mcp-server-development
description: Building Model Context Protocol (MCP) servers in Rust and TypeScript. Tool definitions, resource handling, prompts, and Claude Code integration. Use when implementing MCP servers, exposing APIs as tools, or integrating external services with Claude. Trigger phrases include "MCP server", "tool definition", "stdio server", "SSE server", "Model Context Protocol", or "Claude integration".
---

# MCP Server Development

## Overview

Model Context Protocol (MCP) enables Claude Code to integrate with external services through standardized tool, resource, and prompt interfaces. This skill covers building MCP servers in both Rust and TypeScript, following official MCP specifications and TMNL integration patterns.

**Key capabilities:**
- Expose APIs as Claude-callable tools
- Provide structured resources (files, data, schemas)
- Define reusable prompts for common workflows
- Support stdio, SSE, HTTP, and WebSocket transports

## Canonical Sources

**MCP Specification:**
- Official docs: https://modelcontextprotocol.io/
- TypeScript SDK: `@modelcontextprotocol/sdk`
- Rust SDK: `mcp-rs` (community)

**TMNL Integration:**
- Global MCP config: `~/.claude/CLAUDE.md` (user instructions)
- Plugin MCP integration: See `mcp-integration` skill
- Example servers: Official MCP marketplace

**Referenced Skills:**
- `mcp-integration` — Configuring MCP in Claude Code plugins
- `rust-effect-patterns` — Error handling in Rust MCP servers
- `tauri-rust-patterns` — IPC patterns applicable to MCP

## MCP Architecture

### Core Concepts

```
┌─────────────────────────────────────────────┐
│              Claude Code                     │
│  ┌─────────────────────────────────────┐   │
│  │        MCP Client                    │   │
│  │  • Discovers tools/resources/prompts │   │
│  │  • Invokes tools with arguments      │   │
│  │  │  Handles streaming responses       │   │
│  └──────────┬──────────────────────────┘   │
└─────────────┼────────────────────────────────┘
              │ stdio/SSE/HTTP/WebSocket
              │
┌─────────────▼────────────────────────────────┐
│           MCP Server                          │
│  ┌──────────────────────────────────────┐   │
│  │  Tool Handlers                        │   │
│  │  • file_read(path) → content          │   │
│  │  • db_query(sql) → results            │   │
│  │  • api_call(endpoint) → response      │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │  Resource Providers                   │   │
│  │  • file://project/README.md           │   │
│  │  • db://tables/users                  │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │  Prompt Templates                     │   │
│  │  • debug-error(stack_trace)           │   │
│  │  • review-code(diff)                  │   │
│  └──────────────────────────────────────┘   │
└───────────────────────────────────────────────┘
```

### Transport Types

| Transport | Use Case | Authentication | Pros | Cons |
|-----------|----------|----------------|------|------|
| **stdio** | Local tools, custom servers | Env vars | Simple, no network | Process lifecycle |
| **SSE** | Hosted services, OAuth | OAuth/tokens | Streaming, scalable | Server-sent only |
| **HTTP** | REST APIs, stateless | Tokens/headers | Stateless, cacheable | Request/response only |
| **WebSocket** | Real-time, bidirectional | Tokens/headers | Full duplex, low latency | Connection state |

## Pattern 1: TypeScript MCP Server (stdio)

### Basic Server Structure

```typescript
// server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";

// Initialize server
const server = new Server(
  {
    name: "example-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},  // This server provides tools
    },
  }
);

// Define tools
const tools: Tool[] = [
  {
    name: "read_file",
    description: "Read contents of a file",
    inputSchema: {
      type: "object",
      properties: {
        path: {
          type: "string",
          description: "Absolute file path",
        },
      },
      required: ["path"],
    },
  },
];

// List tools handler
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools,
}));

// Tool execution handler
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "read_file": {
      const { path } = args as { path: string };
      try {
        const content = await fs.promises.readFile(path, "utf-8");
        return {
          content: [
            {
              type: "text",
              text: content,
            },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text",
              text: `Error reading file: ${error}`,
            },
          ],
          isError: true,
        };
      }
    }
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MCP server running on stdio");
}

main().catch(console.error);
```

**Key Patterns:**
- Server initialization with name/version/capabilities
- `ListToolsRequestSchema` — Tool discovery
- `CallToolRequestSchema` — Tool execution
- Return `{ content: [...], isError?: boolean }`
- Use `console.error()` for logging (stdout is reserved for MCP)

### Tool Input Validation

```typescript
import { z } from "zod";

// Define input schema with Zod
const ReadFileInputSchema = z.object({
  path: z.string().min(1),
  encoding: z.enum(["utf-8", "base64"]).default("utf-8"),
});

type ReadFileInput = z.infer<typeof ReadFileInputSchema>;

// Validate in handler
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "read_file": {
      // Validate input
      const input = ReadFileInputSchema.safeParse(args);
      if (!input.success) {
        return {
          content: [
            {
              type: "text",
              text: `Invalid input: ${input.error.message}`,
            },
          ],
          isError: true,
        };
      }

      const { path, encoding } = input.data;
      // ... read file with validated input
    }
  }
});
```

**Pattern:** Use Zod for runtime validation of tool inputs.

### Streaming Tool Responses (SSE)

```typescript
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "stream_logs") {
    const { logFile } = args as { logFile: string };

    // Stream log lines as they're read
    const stream = createReadStream(logFile, { encoding: "utf-8" });
    const content = [];

    for await (const chunk of stream) {
      content.push({
        type: "text",
        text: chunk.toString(),
      });
    }

    return { content };
  }
});

// Use SSE transport for streaming
const transport = new SSEServerTransport("/sse", async (req, res) => {
  // Handle SSE connection
});
```

## Pattern 2: Rust MCP Server (stdio)

### Basic Server with mcp-rs

```rust
// Cargo.toml
// [dependencies]
// mcp-rs = "0.1"  # Community Rust SDK
// tokio = { version = "1", features = ["full"] }
// serde = { version = "1", features = ["derive"] }
// serde_json = "1"
// thiserror = "2"

use mcp_rs::{Server, ServerCapabilities, Tool, ToolCallRequest, ToolListRequest};
use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Error, Debug)]
enum ServerError {
    #[error("File not found: {0}")]
    FileNotFound(String),

    #[error("IO error: {0}")]
    IoError(#[from] std::io::Error),
}

#[derive(Deserialize)]
struct ReadFileInput {
    path: String,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut server = Server::new(
        "rust-mcp-server",
        "1.0.0",
        ServerCapabilities {
            tools: true,
            resources: false,
            prompts: false,
        },
    );

    // Register tool list handler
    server.on_list_tools(|_req: ToolListRequest| async {
        Ok(vec![Tool {
            name: "read_file".to_string(),
            description: "Read file contents".to_string(),
            input_schema: serde_json::json!({
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path to read"
                    }
                },
                "required": ["path"]
            }),
        }])
    });

    // Register tool call handler
    server.on_call_tool(|req: ToolCallRequest| async move {
        match req.name.as_str() {
            "read_file" => {
                let input: ReadFileInput = serde_json::from_value(req.arguments)?;
                match tokio::fs::read_to_string(&input.path).await {
                    Ok(content) => Ok(serde_json::json!({
                        "content": [{
                            "type": "text",
                            "text": content
                        }]
                    })),
                    Err(e) => Ok(serde_json::json!({
                        "content": [{
                            "type": "text",
                            "text": format!("Error: {}", e)
                        }],
                        "isError": true
                    })),
                }
            }
            _ => Err(format!("Unknown tool: {}", req.name).into()),
        }
    });

    // Run stdio server
    server.run_stdio().await?;
    Ok(())
}
```

**Pattern:** Use `thiserror` for error types, `tokio::fs` for async I/O, `serde_json` for schemas.

### Advanced: Resource Provider

```rust
use mcp_rs::{Resource, ResourceListRequest, ReadResourceRequest};

// Register resource list handler
server.on_list_resources(|_req: ResourceListRequest| async {
    Ok(vec![
        Resource {
            uri: "file://project/README.md".to_string(),
            name: "Project README".to_string(),
            description: Some("Main project documentation".to_string()),
            mime_type: Some("text/markdown".to_string()),
        },
        Resource {
            uri: "db://tables/users".to_string(),
            name: "Users Table".to_string(),
            description: Some("User database schema".to_string()),
            mime_type: Some("application/json".to_string()),
        },
    ])
});

// Register resource read handler
server.on_read_resource(|req: ReadResourceRequest| async move {
    match req.uri.as_str() {
        "file://project/README.md" => {
            let content = tokio::fs::read_to_string("README.md").await?;
            Ok(serde_json::json!({
                "contents": [{
                    "uri": req.uri,
                    "mimeType": "text/markdown",
                    "text": content
                }]
            }))
        }
        "db://tables/users" => {
            // Query database, return JSON schema
            let schema = get_table_schema("users").await?;
            Ok(serde_json::json!({
                "contents": [{
                    "uri": req.uri,
                    "mimeType": "application/json",
                    "text": serde_json::to_string_pretty(&schema)?
                }]
            }))
        }
        _ => Err(format!("Resource not found: {}", req.uri).into()),
    }
});
```

## Pattern 3: Prompts (Reusable Templates)

### TypeScript Prompt Definition

```typescript
import { ListPromptsRequestSchema, GetPromptRequestSchema } from "@modelcontextprotocol/sdk/types.js";

// List prompts
server.setRequestHandler(ListPromptsRequestSchema, async () => ({
  prompts: [
    {
      name: "debug-error",
      description: "Help debug an error with stack trace",
      arguments: [
        {
          name: "error_message",
          description: "Error message or stack trace",
          required: true,
        },
        {
          name: "context",
          description: "Additional context about when error occurred",
          required: false,
        },
      ],
    },
  ],
}));

// Get prompt
server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "debug-error": {
      const { error_message, context } = args as {
        error_message: string;
        context?: string;
      };

      return {
        messages: [
          {
            role: "user",
            content: {
              type: "text",
              text: `I encountered this error:\n\n${error_message}\n\n${
                context ? `Context: ${context}\n\n` : ""
              }Please help me debug this. Analyze the error, identify potential causes, and suggest fixes.`,
            },
          },
        ],
      };
    }
    default:
      throw new Error(`Unknown prompt: ${name}`);
  }
});
```

**Pattern:** Prompts are parameterized templates that expand into Claude messages.

## Pattern 4: Authentication

### Environment Variable Configuration

```typescript
// Server reads from env
const API_KEY = process.env.API_KEY;
if (!API_KEY) {
  throw new Error("API_KEY environment variable required");
}

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  // Use API_KEY in tool handlers
  const response = await fetch(endpoint, {
    headers: {
      Authorization: `Bearer ${API_KEY}`,
    },
  });
});
```

**MCP Config:**
```json
{
  "my-server": {
    "command": "node",
    "args": ["server.js"],
    "env": {
      "API_KEY": "${MY_API_KEY}"
    }
  }
}
```

**Pattern:** Server reads from `process.env`, client provides via MCP config.

### OAuth (SSE Transport)

```typescript
// SSE server with OAuth
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import express from "express";

const app = express();

app.get("/oauth/authorize", (req, res) => {
  // Redirect to OAuth provider
  const authUrl = `https://provider.com/oauth/authorize?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}`;
  res.redirect(authUrl);
});

app.get("/oauth/callback", async (req, res) => {
  const { code } = req.query;
  // Exchange code for token
  const token = await exchangeCodeForToken(code);
  // Store token
  res.send("Authentication successful");
});

// SSE endpoint requires valid token
app.get("/sse", async (req, res) => {
  const token = req.headers.authorization?.replace("Bearer ", "");
  if (!isValidToken(token)) {
    return res.status(401).send("Unauthorized");
  }

  const transport = new SSEServerTransport("/sse", req, res);
  await server.connect(transport);
});

app.listen(3000);
```

**Pattern:** SSE servers can implement custom OAuth flows.

## Pattern 5: Error Handling

### Structured Error Responses

**TypeScript:**
```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    // Tool logic
    return {
      content: [{ type: "text", text: result }],
    };
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: error instanceof Error ? error.message : String(error),
        },
      ],
      isError: true,
    };
  }
});
```

**Rust:**
```rust
server.on_call_tool(|req: ToolCallRequest| async move {
    match execute_tool(&req.name, &req.arguments).await {
        Ok(result) => Ok(serde_json::json!({
            "content": [{ "type": "text", "text": result }]
        })),
        Err(e) => Ok(serde_json::json!({
            "content": [{ "type": "text", "text": format!("Error: {}", e) }],
            "isError": true
        })),
    }
});
```

**Pattern:** Always return structured response with `isError: true` for failures.

## TMNL Integration

### Plugin MCP Configuration

Create `.mcp.json` at plugin root:

```json
{
  "my-tool-server": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/tool-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
    "env": {
      "DATABASE_URL": "${DATABASE_URL}",
      "LOG_LEVEL": "info"
    }
  }
}
```

**Rust Server Binary:**
```rust
// servers/tool-server/src/main.rs
use clap::Parser;

#[derive(Parser)]
struct Args {
    #[arg(long)]
    config: String,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();
    let config = load_config(&args.config)?;

    let mut server = Server::new("tool-server", "1.0.0", capabilities);
    // Register handlers...
    server.run_stdio().await?;
    Ok(())
}
```

### TypeScript Server with Bun

```typescript
#!/usr/bin/env bun
// servers/api-server.ts

import { parseArgs } from "util";

const { values } = parseArgs({
  args: process.argv.slice(2),
  options: {
    config: { type: "string" },
  },
});

const config = JSON.parse(await Bun.file(values.config!).text());

const server = new Server({ name: "api-server", version: "1.0.0" }, { capabilities: { tools: {} } });
// Register handlers...

await server.connect(new StdioServerTransport());
```

**Make executable:**
```bash
chmod +x servers/api-server.ts
```

## Testing MCP Servers

### Unit Testing Tool Handlers

**TypeScript (Vitest):**
```typescript
import { describe, it, expect } from "vitest";
import { handleToolCall } from "./handlers";

describe("read_file handler", () => {
  it("reads file successfully", async () => {
    const result = await handleToolCall({
      name: "read_file",
      arguments: { path: "test.txt" },
    });

    expect(result.content).toHaveLength(1);
    expect(result.content[0].type).toBe("text");
    expect(result.isError).toBeUndefined();
  });

  it("handles file not found", async () => {
    const result = await handleToolCall({
      name: "read_file",
      arguments: { path: "nonexistent.txt" },
    });

    expect(result.isError).toBe(true);
    expect(result.content[0].text).toContain("Error");
  });
});
```

**Rust (cargo test):**
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_read_file_success() {
        let input = ReadFileInput {
            path: "test.txt".to_string(),
        };

        let result = handle_read_file(input).await;
        assert!(result.is_ok());
    }

    #[tokio::test]
    async fn test_read_file_not_found() {
        let input = ReadFileInput {
            path: "nonexistent.txt".to_string(),
        };

        let result = handle_read_file(input).await;
        assert!(result.is_err());
    }
}
```

### Integration Testing (MCP Inspector)

Use official MCP Inspector CLI:

```bash
# Install
npm install -g @modelcontextprotocol/inspector

# Test stdio server
mcp-inspector node server.js

# Test with config
mcp-inspector --config .mcp.json my-server
```

**Automated testing:**
```typescript
import { spawn } from "child_process";

async function testMCPServer() {
  const server = spawn("node", ["server.js"]);

  // Send list_tools request
  const listToolsRequest = JSON.stringify({
    jsonrpc: "2.0",
    method: "tools/list",
    id: 1,
  });

  server.stdin.write(listToolsRequest + "\n");

  // Read response
  server.stdout.on("data", (data) => {
    const response = JSON.parse(data.toString());
    console.log("Tools:", response.result.tools);
    server.kill();
  });
}
```

## Anti-Patterns

### 1. Using stdout for Logging

**WRONG:**
```typescript
console.log("Processing request...");  // Breaks MCP protocol!
```

**RIGHT:**
```typescript
console.error("Processing request...");  // stderr is for logs
```

### 2. Unvalidated Tool Inputs

**WRONG:**
```typescript
const { path } = args as any;  // No validation
const content = fs.readFileSync(path);
```

**RIGHT:**
```typescript
const input = ReadFileInputSchema.safeParse(args);
if (!input.success) {
  return { content: [{ type: "text", text: "Invalid input" }], isError: true };
}
```

### 3. Blocking Operations in Async Context

**WRONG (Rust):**
```rust
server.on_call_tool(|req| async move {
    let content = std::fs::read_to_string("file.txt")?;  // Blocks async runtime!
});
```

**RIGHT:**
```rust
server.on_call_tool(|req| async move {
    let content = tokio::fs::read_to_string("file.txt").await?;
});
```

### 4. Hardcoded Credentials

**WRONG:**
```typescript
const API_KEY = "sk-1234567890";  // Hardcoded!
```

**RIGHT:**
```typescript
const API_KEY = process.env.API_KEY;
if (!API_KEY) throw new Error("API_KEY required");
```

## Quick Reference

### Tool Response Format

```json
{
  "content": [
    { "type": "text", "text": "Result text" },
    { "type": "image", "data": "base64...", "mimeType": "image/png" },
    { "type": "resource", "uri": "file://path", "text": "content" }
  ],
  "isError": false
}
```

### Resource Response Format

```json
{
  "contents": [
    {
      "uri": "file://path",
      "mimeType": "text/plain",
      "text": "content"
    }
  ]
}
```

### Prompt Response Format

```json
{
  "messages": [
    {
      "role": "user",
      "content": {
        "type": "text",
        "text": "Prompt text"
      }
    }
  ]
}
```

## Further Reading

- **MCP Specification**: https://modelcontextprotocol.io/
- **TypeScript SDK**: https://github.com/modelcontextprotocol/sdk-typescript
- **Official Servers**: https://github.com/modelcontextprotocol/servers
- **TMNL MCP Integration**: See `mcp-integration` skill
- **Rust Error Handling**: See `rust-effect-patterns` skill
