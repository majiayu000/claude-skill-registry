---
name: fastmcp
description: FastMCP TypeScript framework patterns for MCP servers. Auto-loads when building MCP servers, creating tools/resources/prompts, implementing authentication, configuring transports, or working with FastMCP in TypeScript.
user-invocable: false
---

# FastMCP Development Skill

FastMCP is a TypeScript framework for building Model Context Protocol (MCP) servers. This skill provides patterns for tools, resources, prompts, authentication, and transport configuration.

## Installation

```bash
npm install fastmcp
```

## Basic Server Setup

```typescript
import { FastMCP } from "fastmcp";
import { z } from "zod";

const server = new FastMCP({
  name: "My Server",
  version: "1.0.0",
});

server.start({ transportType: "stdio" });
```

## Tools

### Basic Tool with Zod Schema

```typescript
server.addTool({
  name: "add",
  description: "Add two numbers",
  parameters: z.object({
    a: z.number(),
    b: z.number(),
  }),
  execute: async (args) => {
    return String(args.a + args.b);
  },
});
```

### Tool Without Parameters

```typescript
server.addTool({
  name: "sayHello",
  description: "Say hello",
  execute: async () => {
    return "Hello, world!";
  },
});
```

### Tool with Logging

```typescript
server.addTool({
  name: "download",
  parameters: z.object({ url: z.string() }),
  execute: async (args, { log }) => {
    log.info("Downloading file...", { url: args.url });
    // ... process ...
    log.info("Downloaded file");
    return "done";
  },
});
```

### Tool with Progress Reporting

```typescript
server.addTool({
  name: "download",
  execute: async (args, { reportProgress }) => {
    await reportProgress({ progress: 0, total: 100 });
    // ... process ...
    await reportProgress({ progress: 100, total: 100 });
    return "done";
  },
});
```

### Tool with Streaming Output

```typescript
server.addTool({
  name: "generateText",
  parameters: z.object({ prompt: z.string() }),
  annotations: {
    streamingHint: true,
    readOnlyHint: true,
  },
  execute: async (args, { streamContent }) => {
    await streamContent({ type: "text", text: "Starting...\n" });
    const words = "The quick brown fox".split(" ");
    for (const word of words) {
      await streamContent({ type: "text", text: word + " " });
      await new Promise(resolve => setTimeout(resolve, 300));
    }
    return;
  },
});
```

### Tool with Multiple Content Types

```typescript
server.addTool({
  name: "download",
  description: "Download a file",
  parameters: z.object({ url: z.string() }),
  execute: async (args) => {
    return {
      content: [
        { type: "text", text: "First message" },
        { type: "text", text: "Second message" },
      ],
    };
  },
});
```

### Tool with Image Content

```typescript
import { imageContent } from "fastmcp";

server.addTool({
  name: "getImage",
  execute: async (args) => {
    return imageContent({
      url: "https://example.com/image.png",
    });
    // Or: path: "/path/to/image.png"
    // Or: buffer: Buffer.from(...)
  },
});
```

### Tool with Audio Content

```typescript
import { audioContent } from "fastmcp";

server.addTool({
  name: "getAudio",
  execute: async (args) => {
    return audioContent({
      url: "https://example.com/audio.mp3",
    });
  },
});
```

### Tool with Error Handling

```typescript
import { UserError } from "fastmcp";

server.addTool({
  name: "download",
  execute: async (args) => {
    if (args.url.startsWith("https://example.com")) {
      throw new UserError("This URL is not allowed");
    }
    return "done";
  },
});
```

### Tool with Annotations

```typescript
server.addTool({
  name: "fetch-content",
  description: "Fetch content from a URL",
  parameters: z.object({ url: z.string() }),
  annotations: {
    title: "Web Content Fetcher",
    readOnlyHint: true,
    openWorldHint: true,
  },
  execute: async (args) => {
    return await fetchWebpageContent(args.url);
  },
});
```

### Tool with Authorization

```typescript
server.addTool({
  name: "admin-tool",
  description: "An admin-only tool",
  canAccess: (auth) => auth?.role === "admin",
  execute: async () => "Welcome, admin!",
});
```

## Alternative Schema Libraries

### ArkType

```typescript
import { type } from "arktype";

server.addTool({
  name: "fetch-arktype",
  parameters: type({ url: "string" }),
  execute: async (args) => {
    return await fetchWebpageContent(args.url);
  },
});
```

### Valibot

```typescript
import * as v from "valibot";

server.addTool({
  name: "fetch-valibot",
  parameters: v.object({ url: v.string() }),
  execute: async (args) => {
    return await fetchWebpageContent(args.url);
  },
});
```

## Resources

### Basic Resource

```typescript
server.addResource({
  uri: "file:///logs/app.log",
  name: "Application Logs",
  mimeType: "text/plain",
  async load() {
    return {
      text: await readLogFile(),
    };
  },
});
```

### Resource with Binary Content

```typescript
server.addResource({
  uri: "file:///logs/app.log",
  async load() {
    return {
      blob: 'base64-encoded-data'
    };
  },
});
```

### Resource Template

```typescript
server.addResourceTemplate({
  uriTemplate: "file:///logs/{name}.log",
  name: "Application Logs",
  mimeType: "text/plain",
  arguments: [
    {
      name: "name",
      description: "Name of the log",
      required: true,
    },
  ],
  async load({ name }) {
    return {
      text: `Log content for ${name}`,
    };
  },
});
```

### Resource Template with Auto-Completion

```typescript
server.addResourceTemplate({
  uriTemplate: "file:///logs/{name}.log",
  arguments: [
    {
      name: "name",
      description: "Name of the log",
      required: true,
      complete: async (value) => {
        if (value === "Example") {
          return { values: ["Example Log"] };
        }
        return { values: [] };
      },
    },
  ],
  async load({ name }) {
    return {
      text: `Log content for ${name}`,
    };
  },
});
```

### Embedded Resources in Tools

```typescript
server.addTool({
  name: "get_user_data",
  parameters: z.object({ userId: z.string() }),
  execute: async (args) => {
    return {
      content: [
        {
          type: "resource",
          resource: await server.embedded(`user://profile/${args.userId}`),
        },
      ],
    };
  },
});
```

## Prompts

### Basic Prompt

```typescript
server.addPrompt({
  name: "git-commit",
  description: "Generate a Git commit message",
  arguments: [
    {
      name: "changes",
      description: "Git diff or description of changes",
      required: true,
    },
  ],
  load: async (args) => {
    return "Generate a concise commit message:\n\n" + args.changes;
  },
});
```

### Prompt with Auto-Completion

```typescript
server.addPrompt({
  name: "countryPoem",
  description: "Writes a poem about a country",
  load: async ({ name }) => {
    return "Write a poem about " + name + "!";
  },
  arguments: [
    {
      name: "name",
      description: "Name of the country",
      required: true,
      complete: async (value) => {
        if (value === "Germ") {
          return { values: ["Germany"] };
        }
        return { values: [] };
      },
    },
  ],
});
```

### Prompt with Enum Arguments

```typescript
server.addPrompt({
  name: "countryPoem",
  description: "Writes a poem about a country",
  load: async ({ name }) => {
    return "Write a poem about " + name + "!";
  },
  arguments: [
    {
      name: "name",
      description: "Name of the country",
      required: true,
      enum: ["Germany", "France", "Italy"],
    },
  ],
});
```

## Authentication

### Basic API Key Authentication

```typescript
const server = new FastMCP({
  name: "My Server",
  version: "1.0.0",
  authenticate: (request) => {
    const apiKey = request.headers["x-api-key"];

    if (apiKey !== "expected-key") {
      throw new Response(null, {
        status: 401,
        statusText: "Unauthorized",
      });
    }

    return { id: 1 };
  },
});

server.addTool({
  name: "sayHello",
  execute: async (args, { session }) => {
    return "Hello, " + session.id + "!";
  },
});
```

### Role-Based Authentication

```typescript
const server = new FastMCP<{ role: "admin" | "user" }>({
  authenticate: async (request) => {
    const role = request.headers["x-role"] as string;
    return { role: role === "admin" ? "admin" : "user" };
  },
  name: "My Server",
  version: "1.0.0",
});

server.addTool({
  name: "admin-dashboard",
  description: "An admin-only tool",
  canAccess: (auth) => auth?.role === "admin",
  execute: async () => {
    return "Welcome to the admin dashboard!";
  },
});

server.addTool({
  name: "public-info",
  description: "A tool available to everyone",
  execute: async () => {
    return "This is public information.";
  },
});
```

### OAuth with Google Provider

```typescript
import { FastMCP } from "fastmcp";
import { GoogleProvider } from "fastmcp/auth";

const authProxy = new GoogleProvider({
  clientId: process.env.GOOGLE_CLIENT_ID,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET,
  baseUrl: "https://your-server.com",
  scopes: ["openid", "profile", "email"],
});

const server = new FastMCP({
  name: "My Server",
  oauth: {
    enabled: true,
    authorizationServer: authProxy.getAuthorizationServerMetadata(),
    proxy: authProxy,
  },
});
```

## Session Management

### Session and Request ID Tracking

```typescript
const sessionCounters = new Map<string, number>();

server.addTool({
  name: "increment_counter",
  description: "Increment a per-session counter",
  parameters: z.object({}),
  execute: async (args, context) => {
    if (!context.sessionId) {
      return "Session ID not available (requires HTTP transport)";
    }

    const counter = sessionCounters.get(context.sessionId) || 0;
    const newCounter = counter + 1;
    sessionCounters.set(context.sessionId, newCounter);

    return "Counter: " + newCounter;
  },
});
```

### Server Events

```typescript
server.on("connect", (event) => {
  console.log("Client connected:", event.session);
});

server.on("disconnect", (event) => {
  console.log("Client disconnected:", event.session);
});
```

### Session Events

```typescript
server.on("connect", (event) => {
  const session = event.session;

  console.log("Initial roots:", session.roots);

  session.on("rootsChanged", (event) => {
    console.log("Roots changed:", event.roots);
  });

  session.on("error", (event) => {
    console.error("Error:", event.error);
  });
});
```

### Session Sampling

```typescript
await session.requestSampling({
  messages: [
    {
      role: "user",
      content: {
        type: "text",
        text: "What files are in the current directory?",
      },
    },
  ],
  systemPrompt: "You are a helpful file system assistant.",
  includeContext: "thisServer",
  maxTokens: 100,
});
```

## Transport Options

### HTTP Streaming Transport

```typescript
server.start({
  transportType: "httpStream",
  httpStream: {
    port: 8080,
  },
});
```

### HTTP Streaming with Custom Endpoint

```typescript
server.start({
  transportType: "httpStream",
  httpStream: {
    port: 8080,
    endpoint: "/mcp",
  },
});
```

### Stateless Mode (for Serverless)

```typescript
server.start({
  transportType: "httpStream",
  httpStream: {
    port: 8080,
    stateless: true,
  },
});
```

### SSE Transport

```typescript
server.start({
  transportType: "httpStream",
  httpStream: {
    port: 8080,
  },
});
// SSE automatically available at http://localhost:8080/sse
```

### Stdio Transport

```typescript
server.start({
  transportType: "stdio",
});
```

## Server Configuration

### Custom Logger

```typescript
import { FastMCP, Logger } from "fastmcp";

class CustomLogger implements Logger {
  debug(...args: unknown[]): void {
    console.log("[DEBUG]", new Date().toISOString(), ...args);
  }
  error(...args: unknown[]): void {
    console.error("[ERROR]", new Date().toISOString(), ...args);
  }
  info(...args: unknown[]): void {
    console.info("[INFO]", new Date().toISOString(), ...args);
  }
  log(...args: unknown[]): void {
    console.log("[LOG]", new Date().toISOString(), ...args);
  }
  warn(...args: unknown[]): void {
    console.warn("[WARN]", new Date().toISOString(), ...args);
  }
}

const server = new FastMCP({
  name: "My Server",
  version: "1.0.0",
  logger: new CustomLogger(),
});
```

### Health Check Endpoint

```typescript
const server = new FastMCP({
  name: "My Server",
  version: "1.0.0",
  health: {
    enabled: true,
    message: "healthy",
    path: "/healthz",
    status: 200,
  },
});
```

### Ping Configuration

```typescript
const server = new FastMCP({
  name: "My Server",
  version: "1.0.0",
  ping: {
    enabled: true,
    intervalMs: 10000,
    logLevel: "debug",
  },
});
```

### Instructions

```typescript
const server = new FastMCP({
  name: "My Server",
  version: "1.0.0",
  instructions: "This server provides file management tools. Use the list_files tool to see available files.",
});
```

## CLI Development Commands

```bash
# Development mode with hot reload
npx fastmcp dev src/server.ts

# HTTP streaming transport
npx fastmcp dev src/server.ts --transport http-stream --port 8080

# Stateless mode
npx fastmcp dev src/server.ts --transport http-stream --port 8080 --stateless true

# Or via environment variable
FASTMCP_STATELESS=true npx fastmcp dev src/server.ts
```

## Best Practices

1. **Use descriptive tool names**: Choose names that clearly indicate what the tool does
2. **Provide descriptions**: Always include descriptions for tools, resources, and prompts
3. **Validate inputs**: Use Zod/ArkType/Valibot for comprehensive parameter validation
4. **Handle errors gracefully**: Use `UserError` for user-facing errors
5. **Report progress**: For long-running operations, use `reportProgress`
6. **Use streaming**: For text generation, use `streamContent` with `streamingHint: true`
7. **Implement authorization**: Use `canAccess` for role-based access control
8. **Log appropriately**: Use the context `log` object for debugging
9. **Configure health checks**: Enable health endpoints for production deployments
10. **Use stateless mode**: For serverless deployments, enable stateless mode
