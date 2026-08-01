---
name: openkbs
description: OpenKBS AI agent development framework. Use when creating, modifying,
  or deploying AI agents with backend handlers (onRequest, onResponse, actions.js),
  frontend components (contentRender.js), or elast
---

---
name: openkbs
description: OpenKBS AI agent development framework. Use when creating, modifying, or deploying AI agents with backend handlers (onRequest, onResponse, actions.js), frontend components (contentRender.js), or elastic services (functions, postgres, storage, pulse). Trigger keywords: openkbs, kb, agent, handler, contentRender, elastic, memory, scheduled task.
---

# OpenKBS Development

OpenKBS is a framework for building AI-powered applications - from simple agents to full-stack platforms.

## Two Usage Modes

### 1. Agent-Only Mode
Build a single conversational AI agent with backend handlers and custom UI.
```
openkbs create my-agent
openkbs push
```
Simplest way to get started - just an agent with memory, commands, and custom frontend.

### 2. Platform Mode (Full-Stack)
Build complete SaaS platforms that **include agents** plus additional infrastructure.
```
openkbs deploy          # Deploy from openkbs.json
openkbs stack status    # View deployed resources
```

Platform mode extends agent capabilities with:
- **Multiple Agents**: Run several agents on one platform (in `agents/` folder)
- **Elastic Functions**: Serverless Lambda (Node.js, Python, Java)
- **Elastic Postgres**: Managed PostgreSQL (Neon) for relational data
- **Elastic Storage**: S3 buckets + CloudFront CDN for files
- **Elastic Pulse**: Real-time WebSocket pub/sub
- **Whitelabel**: Custom domains (`example.com`) with static site (`site/` folder)

**Architecture Note**: The whitelabel itself is a KB with its own `kbId` (a service agent, not user-facing). This "parent" kbId is used throughout the stack for elastic services. Each agent in `agents/` has its own separate `kbId`. All agents share the platform's elastic services via the parent kbId.

## Project Structure

### Agent Structure
```
my-agent/
├── app/
│   ├── settings.json       # Agent configuration (model, itemTypes, MCP)
│   └── instructions.txt    # System prompt for LLM
├── src/
│   ├── Events/
│   │   ├── onRequest.js    # Pre-process user messages
│   │   ├── onResponse.js   # Parse LLM output, execute commands
│   │   ├── actions.js      # Command implementations
│   │   ├── onCronjob.js    # Scheduled periodic tasks
│   │   └── onPublicAPIRequest.js  # Webhook handler
│   └── Frontend/
│       ├── contentRender.js    # Custom React UI
│       └── contentRender.json  # Frontend dependencies
└── openkbs.json            # Elastic services config
```

### Platform Structure
```
my-platform/
├── agents/                        # Multiple AI agents
│   ├── marketing-assistant/       # Each agent has full structure
│   │   ├── app/
│   │   │   ├── settings.json
│   │   │   └── instructions.txt
│   │   └── src/
│   │       ├── Events/
│   │       │   ├── onRequest.js
│   │       │   ├── onResponse.js
│   │       │   └── actions.js
│   │       └── Frontend/
│   │           └── contentRender.js
│   └── support-agent/             # Another agent
│       ├── app/
│       └── src/
├── functions/                     # Serverless Lambda functions
│   └── api/
│       └── index.mjs
├── site/                          # Static site for whitelabel domain
│   └── index.html
└── openkbs.json                   # Elastic services config
```

### openkbs.json
```json
{
  "elastic": {
    "postgres": true,
    "storage": true,
    "pulse": true,
    "functions": {
      "api": { "runtime": "nodejs22.x", "memory": 512 }
    }
  }
}
```

## Quick Commands

### Agent Commands
```bash
openkbs create <name>    # Create new agent
openkbs push             # Deploy to cloud
openkbs pull             # Download from cloud
openkbs update skills    # Update this skill
```

### Platform Commands
```bash
openkbs deploy           # Deploy all elastic services
openkbs stack status     # Show deployed resources
openkbs destroy          # Remove all resources (DANGEROUS)
```

### Elastic Services
```bash
openkbs fn list          # List Lambda functions
openkbs fn push api      # Deploy function
openkbs fn logs api      # View function logs
openkbs postgres shell   # Connect to Postgres
openkbs storage ls       # List S3 objects
openkbs pulse status     # WebSocket status
openkbs site push        # Deploy static site
```

## Backend Handler Pattern

Commands are XML tags with JSON content that the LLM outputs:

```xml
<commandName>{"param": "value"}</commandName>
```

The `handler.js` parses these tags, matches regex patterns in `actions.js`, and executes async functions:

```javascript
// actions.js pattern
[/<googleSearch>([\s\S]*?)<\/googleSearch>/s, async (match) => {
    const data = JSON.parse(match[1].trim());
    const results = await openkbs.googleSearch(data.query);
    return {
        type: 'SEARCH_RESULTS',
        data: results,
        _meta_actions: ["REQUEST_CHAT_MODEL"]  // Loop back to LLM
    };
}]
```

## Meta Actions

Control flow after command execution:

- `["REQUEST_CHAT_MODEL"]` - Send result back to LLM for processing
- `[]` - Display result to user, stop conversation

## Memory System

Configure in `settings.json`:

```json
{
  "itemTypes": {
    "memory": {
      "attributes": [
        { "attrName": "itemId", "attrType": "itemId", "encrypted": false },
        { "attrName": "body", "attrType": "body", "encrypted": true }
      ]
    }
  },
  "options": {
    "priorityItems": [{ "prefix": "memory_", "limit": 100 }]
  }
}
```

Priority items are auto-injected into LLM context.

## Additional Resources

- For backend SDK methods, see [reference/backend-sdk.md](reference/backend-sdk.md)
- For frontend React patterns, see [reference/frontend-sdk.md](reference/frontend-sdk.md)
- For XML command definitions, see [reference/commands.md](reference/commands.md)
- For elastic services, see [reference/elastic-services.md](reference/elastic-services.md)
- For complete examples, see [examples/](examples/)
