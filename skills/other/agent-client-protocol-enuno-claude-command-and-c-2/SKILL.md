---
name: agent-client-protocol
version: "1.0.0"
description: Agent Client Protocol (ACP) - Standardized communication between code editors and AI coding agents. Use for building ACP-compatible agents, integrating agents with editors (Zed, JetBrains, Neovim), implementing tool calls, file operations, and session management.
---

# Agent Client Protocol Skill

The Agent Client Protocol (ACP) is a standardized communication framework between code editors (IDEs) and AI coding agents, similar to how the Language Server Protocol (LSP) unified language server integration. ACP enables any compatible agent to work with any compatible editor without custom integrations.

**Core Value Proposition**: Build once, run everywhere - agents implementing ACP work with any compatible editor, and editors supporting ACP gain access to all ACP-compatible agents.

## When to Use This Skill

This skill should be triggered when:
- Building AI coding agents that need editor integration
- Implementing ACP support in code editors or IDEs
- Creating tool call handlers for agent operations
- Managing file system operations from agents
- Implementing session management for AI assistants
- Building bridges between existing agents and ACP clients
- Understanding JSON-RPC messaging for agent-editor communication

## Protocol Overview

### The Problem ACP Solves

Before ACP:
- Each editor must build custom integrations for every agent
- Agents must implement editor-specific APIs
- N editors × M agents = N×M integrations needed

After ACP:
- One protocol specification
- N + M implementations needed
- Any agent works with any editor

### Deployment Models

```
┌─────────────────────────────────────────────────────────────┐
│                    LOCAL DEPLOYMENT                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌──────────┐  JSON-RPC/stdio  ┌──────────────────────┐   │
│   │  Editor  │◄────────────────►│  Agent (subprocess)  │   │
│   │  (Zed)   │                  │  (Claude Code)       │   │
│   └──────────┘                  └──────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   REMOTE DEPLOYMENT                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌──────────┐  HTTP/WebSocket  ┌──────────────────────┐   │
│   │  Editor  │◄────────────────►│  Cloud Agent         │   │
│   │          │                  │  (remote server)     │   │
│   └──────────┘                  └──────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Supported Ecosystem

### Compatible Agents (18+)

| Agent | Description |
|-------|-------------|
| **Claude Code** | Anthropic's coding agent (via Zed adapter) |
| **Gemini CLI** | Google's AI coding assistant |
| **Goose** | Block's open-source coding agent |
| **OpenHands** | Open-source AI software engineer |
| **Codex CLI** | OpenAI's coding agent (via adapter) |
| **Augment Code** | AI pair programming |
| **Blackbox AI** | Code generation agent |
| **Docker cagent** | Containerized agent |
| **Mistral Vibe** | Mistral AI coding assistant |
| **Qwen Code** | Alibaba's coding agent |
| **JetBrains Junie** | JetBrains AI agent (coming soon) |
| **fast-agent** | Lightweight ACP agent |
| **OpenCode** | Open-source coding agent |
| **Stakpak** | Infrastructure agent |
| **VT Code** | Visual coding agent |
| **AgentPool** | Multi-agent pool |
| **Code Assistant** | General coding assistant |
| **Kimi CLI** | Moonshot AI agent |

### Compatible Clients/Editors (15+)

| Client | Platform |
|--------|----------|
| **Zed** | Native desktop editor |
| **JetBrains** | IntelliJ IDEA, PyCharm, WebStorm, etc. |
| **Neovim** | Via CodeCompanion or avante.nvim |
| **Emacs** | Via agent-shell.el |
| **Obsidian** | Via Agent Client plugin |
| **marimo notebook** | Python notebook |
| **DeepChat** | Chat interface |
| **DuckDB** | Via sidequery extension |
| **Agmente** | iOS client |
| **AionUi** | Web UI |
| **aizen** | CLI client |
| **Tidewave** | Phoenix LiveView |
| **Toad** | Database client |
| **Web Browser** | Via AI SDK provider |
| **Sidequery** | Coming soon |

---

## Protocol Architecture

### Communication Model

ACP uses **JSON-RPC 2.0** with two message types:

```typescript
// Methods: Request-Response pairs
interface Request {
  jsonrpc: "2.0";
  id: string | number;
  method: string;
  params?: object;
}

interface Response {
  jsonrpc: "2.0";
  id: string | number;
  result?: any;
  error?: { code: number; message: string; data?: any };
}

// Notifications: One-way messages (no response)
interface Notification {
  jsonrpc: "2.0";
  method: string;
  params?: object;
}
```

### Session Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    SESSION LIFECYCLE                         │
└─────────────────────────────────────────────────────────────┘

1. INITIALIZATION
   Client ──initialize──► Agent
   Client ◄──capabilities── Agent
   Client ──authenticate──► Agent (if required)

2. SESSION SETUP
   Client ──session/new──► Agent (new conversation)
   OR
   Client ──session/load──► Agent (resume existing)

3. PROMPT TURN CYCLE (repeats)
   Client ──session/prompt──► Agent
   Agent ──session/update──► Client (streaming)
   Agent ──request_permission──► Client (if needed)
   Client ◄──response── Agent

4. TERMINATION
   Client ──session/cancel──► Agent (interrupt)
   OR
   Connection closes
```

### Core Methods

#### Agent-Side Methods (Required)

| Method | Purpose |
|--------|---------|
| `initialize` | Negotiate protocol version and capabilities |
| `authenticate` | Validate client credentials |
| `session/new` | Create new conversation session |
| `session/prompt` | Process user input |

#### Client-Side Methods

| Method | Purpose |
|--------|---------|
| `session/request_permission` | Get user authorization for tool execution |
| `fs/read_text_file` | Read file contents |
| `fs/write_text_file` | Write/create files |

---

## Content Types

ACP defines structured content blocks for data exchange:

### Text Content

```json
{
  "type": "text",
  "text": "Hello, I can help you with your code."
}
```

### Image Content

```json
{
  "type": "image",
  "mimeType": "image/png",
  "data": "base64encodeddata..."
}
```

### Audio Content

```json
{
  "type": "audio",
  "mimeType": "audio/wav",
  "data": "base64encodedaudio..."
}
```

### Embedded Resource

```json
{
  "type": "resource",
  "resource": {
    "uri": "file:///path/to/file.ts",
    "mimeType": "text/typescript",
    "text": "const x = 1;"
  }
}
```

### Resource Link

```json
{
  "type": "resource_link",
  "uri": "file:///path/to/document.pdf",
  "name": "document.pdf",
  "mimeType": "application/pdf",
  "size": 1024000
}
```

---

## Tool Calls

### Creating Tool Calls

Agents report tool invocations via `session/update`:

```json
{
  "jsonrpc": "2.0",
  "method": "session/update",
  "params": {
    "sessionId": "session-123",
    "update": {
      "type": "tool_call",
      "toolCallId": "tc-456",
      "title": "Reading configuration file",
      "kind": "read",
      "status": "pending"
    }
  }
}
```

### Tool Call Kinds

| Kind | Description |
|------|-------------|
| `read` | Reading files or data |
| `edit` | Modifying existing content |
| `delete` | Removing files/resources |
| `move` | Moving/renaming files |
| `search` | Searching codebase |
| `execute` | Running commands |
| `think` | Agent reasoning |
| `fetch` | HTTP requests |
| `other` | Custom operations |

### Tool Call Status Lifecycle

```
pending ──► in_progress ──► completed
                  │
                  └──► failed
```

### Permission Requests

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "session/request_permission",
  "params": {
    "sessionId": "session-123",
    "toolCallId": "tc-456",
    "options": [
      { "label": "Allow", "action": "allow" },
      { "label": "Always Allow", "action": "allow_always" },
      { "label": "Deny", "action": "deny" }
    ]
  }
}
```

---

## File System Operations

### Reading Files

```json
// Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "fs/read_text_file",
  "params": {
    "sessionId": "session-123",
    "path": "/absolute/path/to/file.ts",
    "line": 1,
    "limit": 100
  }
}

// Response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": "const x = 1;\nconst y = 2;\n..."
  }
}
```

### Writing Files

```json
// Request
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "fs/write_text_file",
  "params": {
    "sessionId": "session-123",
    "path": "/absolute/path/to/newfile.ts",
    "content": "export const config = {};"
  }
}

// Response (success)
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": null
}
```

### Important Constraints

- All file paths MUST be absolute
- Line numbering is 1-based
- No edit-in-place operations (full read/write only)
- Check `clientCapabilities.fs` before using

---

## Session Modes

Agents can operate in different modes affecting behavior:

### Example Modes

| Mode | Description |
|------|-------------|
| **Ask** | Request permission before any changes |
| **Architect** | Design and plan without implementation |
| **Code** | Full tool access for code modifications |

### Switching Modes

**Client-initiated:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "session/set_mode",
  "params": {
    "sessionId": "session-123",
    "modeId": "code"
  }
}
```

**Agent-initiated (notification):**
```json
{
  "jsonrpc": "2.0",
  "method": "session/update",
  "params": {
    "sessionId": "session-123",
    "update": {
      "type": "current_mode_update",
      "modeId": "architect"
    }
  }
}
```

---

## SDK Installation

### TypeScript

```bash
npm install @agentclientprotocol/sdk
```

```typescript
import { AgentSideConnection, ClientSideConnection } from '@agentclientprotocol/sdk';

// For building an agent
const agentConnection = new AgentSideConnection();

// For building a client
const clientConnection = new ClientSideConnection();
```

**API Reference**: https://agentclientprotocol.github.io/typescript-sdk

### Python

```bash
pip install agent-client-protocol
# or with uv
uv add agent-client-protocol
```

```python
from agent_client_protocol import AgentConnection, ClientConnection

# For building an agent
agent = AgentConnection()

# For building a client
client = ClientConnection()
```

**API Reference**: https://agentclientprotocol.github.io/python-sdk

### Rust

```bash
cargo add agent-client-protocol
```

**Crates.io**: https://crates.io/crates/agent-client-protocol

### Kotlin

Available via Maven for JVM environments with samples included.

---

## Building an ACP Agent

### Minimal TypeScript Agent

```typescript
import { AgentSideConnection } from '@agentclientprotocol/sdk';

const agent = new AgentSideConnection();

// Handle initialization
agent.on('initialize', async (params) => {
  return {
    protocolVersion: '1.0.0',
    capabilities: {
      modes: {
        currentModeId: 'code',
        availableModes: [
          { id: 'code', name: 'Code', description: 'Full coding mode' }
        ]
      }
    }
  };
});

// Handle new sessions
agent.on('session/new', async (params) => {
  return {
    sessionId: crypto.randomUUID(),
    modes: {
      currentModeId: 'code',
      availableModes: [{ id: 'code', name: 'Code' }]
    }
  };
});

// Handle prompts
agent.on('session/prompt', async (params) => {
  const { sessionId, prompt } = params;

  // Stream updates to client
  agent.notify('session/update', {
    sessionId,
    update: {
      type: 'text_delta',
      delta: 'Processing your request...'
    }
  });

  // Process prompt with your LLM
  const response = await processWithLLM(prompt);

  return {
    stopReason: 'endTurn',
    content: [{ type: 'text', text: response }]
  };
});

// Start listening on stdio
agent.listen();
```

### Production Example

See the [Gemini CLI implementation](https://github.com/google-gemini/gemini-cli/blob/main/packages/cli/src/zed-integration/zedIntegration.ts) for a complete, production-ready ACP agent.

---

## MCP Integration

ACP integrates with Model Context Protocol (MCP) in three ways:

### 1. External MCP Servers

Editors pass user-configured MCP server configs to agents:

```json
{
  "mcpServers": [
    {
      "name": "filesystem",
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    }
  ]
}
```

### 2. Editor-Exported Tools

Editors expose their own MCP server to agents:

```json
{
  "editorMcpServer": {
    "transport": "stdio",
    "capabilities": ["search", "diagnostics", "refactor"]
  }
}
```

### 3. Proxy Tunneling

For stdio-only MCP support, editors provide proxies routing requests:

```
Agent ──MCP request──► Editor Proxy ──MCP──► External Server
```

---

## Design Principles

### MCP-Friendly

- Built on JSON-RPC 2.0
- Reuses MCP content types
- Compatible data representations

### UX-First

- Balances rendering flexibility
- Appropriate abstraction levels
- Supports diffs, terminal output, file locations

### Trusted

- Operates in trusted editor context
- User controls tool execution
- Agents access files and MCP servers

---

## Best Practices

### For Agent Developers

1. **Implement all baseline methods**: `initialize`, `authenticate`, `session/new`, `session/prompt`
2. **Stream updates frequently**: Use `session/update` for progress visibility
3. **Request permissions appropriately**: Use `request_permission` for destructive operations
4. **Handle cancellation**: Respect `session/cancel` notifications
5. **Use absolute paths**: All file operations require absolute paths

### For Client Developers

1. **Declare capabilities accurately**: Only advertise supported features
2. **Handle streaming updates**: Process `session/update` notifications in real-time
3. **Implement permission UI**: Show user-friendly permission dialogs
4. **Support multiple sessions**: Allow concurrent agent sessions

### Security Considerations

- Validate all file paths (prevent directory traversal)
- Implement rate limiting for tool calls
- Sanitize user input before passing to agents
- Log all operations for audit trails

---

## Error Handling

### JSON-RPC Error Codes

| Code | Meaning |
|------|---------|
| -32700 | Parse error |
| -32600 | Invalid request |
| -32601 | Method not found |
| -32602 | Invalid params |
| -32603 | Internal error |

### Error Response Format

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32601,
    "message": "Method not found",
    "data": { "method": "unknown/method" }
  }
}
```

---

## Resources

### Official Documentation
- [ACP Website](https://agentclientprotocol.com/)
- [Protocol Schema](https://github.com/agentclientprotocol/agent-client-protocol)

### SDKs
- [TypeScript SDK](https://github.com/agentclientprotocol/typescript-sdk)
- [Python SDK](https://github.com/agentclientprotocol/python-sdk)
- [Rust Crate](https://crates.io/crates/agent-client-protocol)

### Examples
- [Gemini CLI Integration](https://github.com/google-gemini/gemini-cli)
- [Goose Agent](https://github.com/block/goose)

### Community
- [Zed ACP Documentation](https://zed.dev/acp)
- [JetBrains AI Assistant ACP](https://www.jetbrains.com/help/ai-assistant/acp.html)

---

## Version History

- **1.0.0** (2026-01-10): Initial skill release
  - Complete protocol overview
  - Session lifecycle documentation
  - Tool call and permission handling
  - File system operations
  - Session modes
  - SDK installation guides (TypeScript, Python, Rust, Kotlin)
  - 18 supported agents, 15 supported clients
  - MCP integration patterns
  - Best practices and error handling
