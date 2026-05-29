---
name: github-copilot-sdk
description: Comprehensive knowledge of GitHub Copilot SDK for embedding Copilot's agentic workflows in Python, TypeScript, Go, and .NET applications. Auto-activates for Copilot SDK integration, CopilotClient usage, session management, streaming responses, custom tools, and MCP server connections.
version: 1.0.0
last_updated: 2025-01-25
source_urls:
  - https://github.com/github/copilot-sdk
  - https://github.com/github/awesome-copilot/blob/main/collections/copilot-sdk.md
activation_keywords:
  - copilot sdk
  - github copilot sdk
  - copilot client
  - github copilot client
  - copilot session
  - copilot streaming
  - copilot custom tools
  - copilot mcp
  - embed copilot
  - copilot api
auto_activate: true
token_budget: 2000
---

# GitHub Copilot SDK - Comprehensive Skill

## Overview

The **GitHub Copilot SDK** enables developers to embed Copilot's agentic workflows programmatically in their applications. It exposes the same engine behind Copilot CLI as a production-tested agent runtime you can invoke from code.

### When to Use the Copilot SDK

**Use the Copilot SDK when:**

- Building applications that need Copilot's AI capabilities
- Implementing custom AI assistants with tool-calling abilities
- Creating integrations that leverage Copilot's code understanding
- Connecting to MCP (Model Context Protocol) servers for standardized tools
- Need streaming responses in custom UIs

**Don't use when:**

- GitHub Copilot CLI is sufficient (use CLI directly)
- No programmatic integration needed (use Copilot in VS Code)
- Building simple chat without tools (use standard LLM API)

### Language Support

| SDK                    | Installation                              |
| ---------------------- | ----------------------------------------- |
| **Node.js/TypeScript** | `npm install @github/copilot-sdk`         |
| **Python**             | `pip install github-copilot-sdk`          |
| **Go**                 | `go get github.com/github/copilot-sdk/go` |
| **.NET**               | `dotnet add package GitHub.Copilot.SDK`   |

### Prerequisites

1. **GitHub Copilot CLI installed** and authenticated
2. **Active Copilot subscription** (free tier available with limits)

## Quick Start

### Minimal Example (TypeScript)

```typescript
import { CopilotClient } from "@github/copilot-sdk";

const client = new CopilotClient();
const session = await client.createSession({ model: "gpt-4.1" });

const response = await session.sendAndWait({ prompt: "What is 2 + 2?" });
console.log(response?.data.content);

await client.stop();
```

### Minimal Example (Python)

```python
import asyncio
from copilot import CopilotClient

async def main():
    client = CopilotClient()
    await client.start()
    session = await client.create_session({"model": "gpt-4.1"})
    response = await session.send_and_wait({"prompt": "What is 2 + 2?"})
    print(response.data.content)
    await client.stop()

asyncio.run(main())
```

### Add Streaming

```typescript
const session = await client.createSession({
  model: "gpt-4.1",
  streaming: true,
});

session.on((event) => {
  if (event.type === "assistant.message_delta") {
    process.stdout.write(event.data.deltaContent);
  }
});

await session.sendAndWait({ prompt: "Tell me a joke" });
```

### Add Custom Tool

```typescript
import { defineTool } from "@github/copilot-sdk";

const getWeather = defineTool("get_weather", {
  description: "Get weather for a city",
  parameters: {
    type: "object",
    properties: {
      city: { type: "string", description: "City name" },
    },
    required: ["city"],
  },
  handler: async ({ city }) => ({
    city,
    temperature: `${Math.floor(Math.random() * 30) + 50}°F`,
    condition: "sunny",
  }),
});

const session = await client.createSession({
  model: "gpt-4.1",
  tools: [getWeather],
});
```

## Core Concepts

### Architecture

```
Your Application → SDK Client → JSON-RPC → Copilot CLI (server mode)
```

The SDK manages the CLI process lifecycle automatically or connects to an external CLI server.

### Key Components

1. **CopilotClient**: Entry point - manages connection to Copilot CLI
2. **Session**: Conversation context with model, tools, and history
3. **Tools**: Custom functions Copilot can invoke
4. **Events**: Streaming responses and tool call notifications
5. **MCP Integration**: Connect to Model Context Protocol servers

### Session Configuration

```typescript
const session = await client.createSession({
  model: "gpt-4.1", // Model to use
  streaming: true, // Enable streaming
  tools: [myTool], // Custom tools
  mcpServers: {
    // MCP server connections
    github: {
      type: "http",
      url: "https://api.githubcopilot.com/mcp/",
    },
  },
  systemMessage: {
    // Custom system prompt
    content: "You are a helpful assistant.",
  },
  customAgents: [
    {
      // Custom agent personas
      name: "code-reviewer",
      displayName: "Code Reviewer",
      description: "Reviews code for best practices",
      prompt: "Focus on security and performance.",
    },
  ],
});
```

## Navigation Guide

### When to Read Supporting Files

**reference.md** - Read when you need:

- Complete API reference for all 4 languages
- All method signatures with parameters and return types
- Session configuration options
- Event types and handling
- External CLI server connection

**examples.md** - Read when you need:

- Working copy-paste code for all 4 languages
- Error handling patterns
- Multiple sessions management
- Interactive assistant implementation
- Custom agent definition examples

**patterns.md** - Read when you need:

- Production-ready architectural patterns
- Streaming UI integration
- MCP server integration patterns
- Rate limiting and retry patterns
- Structured output extraction

**drift-detection.md** - Read when you need:

- Understanding how this skill stays current
- Validation workflow
- Update procedures

## Quick Reference

### Common Event Types

| Event Type (TS/Go)        | Python Enum                                |
| ------------------------- | ------------------------------------------ |
| `assistant.message_delta` | `SessionEventType.ASSISTANT_MESSAGE_DELTA` |
| `session.idle`            | `SessionEventType.SESSION_IDLE`            |
| `tool.invocation`         | `SessionEventType.TOOL_EXECUTION_START`    |
| `tool.result`             | `SessionEventType.TOOL_EXECUTION_COMPLETE` |

> **Python**: Import `from copilot.generated.session_events import SessionEventType`

### Default Tools

The SDK operates in `--allow-all` mode by default, enabling:

- File system operations
- Git operations
- Web requests
- All first-party Copilot tools

## Integration with Amplihack

Use the Copilot SDK to build custom agents within amplihack:

```python
# Create Copilot-powered agent for specific domain
from copilot import CopilotClient

async def create_code_review_agent():
    client = CopilotClient()
    await client.start()
    session = await client.create_session({
        "model": "gpt-4.1",
        "streaming": True,
        "systemMessage": {
            "content": "You are an expert code reviewer."
        }
    })
    return session
```

## Next Steps

1. **Start Simple**: Basic send/receive with default model
2. **Add Streaming**: Real-time responses for better UX
3. **Add Tools**: Custom functions for your domain
4. **Connect MCP**: Use GitHub MCP server for repo access
5. **Build UI**: Integrate into your application

For complete API details, see `reference.md`.
For working code in all languages, see `examples.md`.
For production patterns, see `patterns.md`.
