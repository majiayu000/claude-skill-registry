---
name: a2a-setup
description: Scaffold a new A2A project — install the SDK, create directory structure, configure the Agent Card, and set up a basic server/client. Use when starting a new A2A multi-agent project from scratch.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# A2A Project Setup

## Before writing code

**Fetch live docs**:
1. Fetch `https://a2a-protocol.org/latest/specification/` for the latest protocol overview
2. Web-search `site:github.com a2aproject a2a-python README` or `a2aproject a2a-js README` for the target SDK's current installation and quickstart
3. Web-search `site:github.com a2aproject a2a-samples` for official sample project structures
4. Fetch the SDK's PyPI/npm page for the latest version number

## Conceptual Architecture

### What Setup Involves

A2A project setup creates the foundation for a multi-agent system:
1. **Install the A2A SDK** for your language (Python, JS/TS, Go, Java, .NET)
2. **Create directory structure** — agent server, client, Agent Card, configuration
3. **Define the Agent Card** — the discovery document describing your agent
4. **Create a minimal server** — HTTP endpoint that handles JSON-RPC 2.0 A2A methods
5. **Create a minimal client** — code to discover and call another A2A agent

### Python Project Structure

```
my-a2a-agent/
├── agent_card.json          # Agent Card (also served at /.well-known/agent-card.json)
├── server.py                # A2A server entry point
├── client.py                # A2A client for testing
├── agent/
│   ├── __init__.py
│   └── handler.py           # Task processing logic
├── pyproject.toml           # or requirements.txt
└── tests/
    └── test_agent.py
```

### JS/TS Project Structure

```
my-a2a-agent/
├── agent-card.json
├── src/
│   ├── server.ts            # A2A server entry point
│   ├── client.ts            # A2A client for testing
│   └── handler.ts           # Task processing logic
├── package.json
├── tsconfig.json
└── tests/
    └── agent.test.ts
```

### Agent Card Skeleton

Every A2A agent needs an Agent Card. Minimal structure:

```json
{
  "name": "My Agent",
  "description": "What this agent does",
  "url": "http://localhost:8000",
  "version": "1.0.0",
  "protocolVersion": "0.2.1",
  "capabilities": {
    "streaming": false,
    "pushNotifications": false,
    "stateTransitionHistory": false
  },
  "skills": [
    {
      "id": "skill-1",
      "name": "Skill Name",
      "description": "What this skill does",
      "tags": ["tag1", "tag2"],
      "examples": ["Example input"]
    }
  ],
  "defaultInputModes": ["text/plain"],
  "defaultOutputModes": ["text/plain"]
}
```

### Key Setup Decisions

- **Language/SDK** — Python (`a2a-sdk`), JS/TS (`@a2a-js/sdk`), Go, Java, .NET
- **HTTP framework** — The SDK may provide a built-in server or integrate with frameworks (FastAPI, Express, etc.)
- **Capabilities** — Decide upfront: streaming? push notifications? state history?
- **Authentication** — None for local dev; API key or OAuth2 for production
- **Agent Card hosting** — Serve at `/.well-known/agent-card.json` or via a registry

### Best Practices

- Start with a minimal Agent Card and expand as you add skills
- Use the SDK's built-in server utilities rather than building raw JSON-RPC handling
- Keep the Agent Card in a separate file, loaded at server startup
- Add proper logging from the start — A2A debugging requires visibility into message flow
- Set up a test client alongside the server for rapid development

Fetch the SDK README for exact installation commands, class names, and quickstart code before scaffolding.
