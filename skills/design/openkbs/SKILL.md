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

> **Note:** In OpenKBS, "KB" (Knowledge Base) and "Agent" are used interchangeably. Every agent has a unique `kbId`.

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

**Architecture Note**: The whitelabel is a special "service agent" with its own `kbId` that holds the entire cloud setup:
- Domain configuration (`domainParkingState`)
- Elastic services (Postgres, Storage, Pulse, Functions)
- CloudFront distributions
- SSL certificates

This whitelabel `kbId` is used in `settings.json` files throughout the project. User-facing agents in `agents/` folder each get their own separate `kbId` when pushed.

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
│
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
  "region": "us-east-1",
  "spa": "/app/index.html",
  "postgres": true,
  "storage": {
    "cloudfront": "media"
  },
  "pulse": true,
  "functions": [
    { "name": "api", "runtime": "nodejs24.x", "memory": 512, "timeout": 30 }
  ],
  "site": "./site"
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
openkbs site spa /app/index.html  # Enable SPA routing
```

### Domain & Whitelabel
```bash
openkbs ls                        # List all agents - find whitelabel kbId here
openkbs ls <kbId>                 # View full agent details
openkbs ls <kbId> domain          # Get just the domain name
openkbs ls <kbId> domainParkingState  # Get domain setup details
openkbs publish example.com       # Link agent to custom domain
openkbs unpublish example.com     # Unlink agent from domain
```

**Quick domain lookup:**
```bash
# 1. Find the whitelabel agent (usually named "AI White Label" or similar)
openkbs ls

# 2. Get its domain
openkbs ls 1ya6foz1a7q3 domain
# -> jobavion.com
```

Available fields: `domain`, `domainParkingState`, `elasticPostgresHost`, `elasticStorageBucket`, `spaFallback`, etc.

### Image Generation Service
Generate images directly from CLI using OpenKBS AI services:

```bash
# Generate with GPT
openkbs service -m gpt-image -d '{"action":"createImage","prompt":"a logo"}' -o logo.png

# Generate with Gemini
openkbs service -m gemini-image -d '{"action":"createImage","prompt":"hero image"}' -o hero.png

# Edit existing image
openkbs service -m gpt-image -d '{"action":"createImage","prompt":"make it blue","imageUrls":["https://..."]}' -o edited.png
```

**Available models:**
- `gpt-image` - OpenAI GPT Image (gpt-image-1.5)
- `gemini-image` - Google Gemini Flash (gemini-2.5-flash-image)

**Options for gpt-image:**
| Option | Values | Default |
|--------|--------|---------|
| prompt | (required) | - |
| size | "1024x1024", "1024x1536", "1536x1024", "auto" | "auto" |
| quality | "low", "medium", "high", "auto" | "auto" |
| n | Number of images | 1 |
| output_format | "png", "jpg", "webp" | "png" |
| background | "transparent", "opaque", "auto" | "auto" |
| output_compression | 0-100 | 100 |
| imageUrls | Array of URLs for editing | - |

**Options for gemini-image:**
| Option | Values | Default |
|--------|--------|---------|
| prompt | (required) | - |
| aspect_ratio | "1:1", "16:9", "9:16", "4:3", "3:4" | "1:1" |
| imageUrls | Array of URLs for reference | - |

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

### Reference Documentation
- [reference/backend-sdk.md](reference/backend-sdk.md) - Backend SDK methods (openkbs.*)
- [reference/frontend-sdk.md](reference/frontend-sdk.md) - Frontend React patterns
- [reference/commands.md](reference/commands.md) - XML command definitions
- [reference/elastic-services.md](reference/elastic-services.md) - Functions, Postgres, Storage, Pulse

### Ready-to-Use Patterns
Production-tested code blocks for common tasks:

**Content & Media:**
- [patterns/image-generation.md](patterns/image-generation.md) - AI image generation with upload
- [patterns/video-generation.md](patterns/video-generation.md) - Async video generation with polling
- [patterns/file-upload.md](patterns/file-upload.md) - Presigned URL file uploads
- [patterns/web-publishing.md](patterns/web-publishing.md) - HTML page publishing

**Memory & Storage:**
- [patterns/memory-system.md](patterns/memory-system.md) - Memory CRUD with settings.json config
- [patterns/vectordb-archive.md](patterns/vectordb-archive.md) - Long-term archive with semantic search

**Scheduling & Automation:**
- [patterns/scheduled-tasks.md](patterns/scheduled-tasks.md) - Task scheduling (one-time & recurring)
- [patterns/cronjob-batch-processing.md](patterns/cronjob-batch-processing.md) - Batch file processing with state
- [patterns/cronjob-monitoring.md](patterns/cronjob-monitoring.md) - Continuous monitoring with pulse control

**External Integrations:**
- [patterns/telegram.md](patterns/telegram.md) - Telegram bot commands (send messages)
- [patterns/telegram-webhook.md](patterns/telegram-webhook.md) - Telegram webhook (receive messages)
- [patterns/public-api-item-proxy.md](patterns/public-api-item-proxy.md) - Public API with geolocation

### Complete Examples
- [examples/ai-copywriter-agent/](examples/ai-copywriter-agent/) - Content generation agent
- [examples/ai-marketing-agent/](examples/ai-marketing-agent/) - Marketing automation agent
- [examples/monitoring-bot/](examples/monitoring-bot/) - Cronjob + Telegram monitoring agent
- [examples/nodejs-demo/](examples/nodejs-demo/) - Platform with elastic functions
