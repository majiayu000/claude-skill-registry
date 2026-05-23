---
name: faion-make-mcp-skill
user-invocable: false
description: "Create custom MCP servers in TypeScript or Python. Install and configure popular MCP servers. Covers Figma, Jira, Notion, Stripe, social media, analytics, and more."
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, AskUserQuestion, WebSearch
---

# MCP Server Development Skill

**Communication: User's language. Code: English.**

## Purpose

Create, install, and configure MCP (Model Context Protocol) servers:
- Build custom MCP servers in TypeScript or Python
- Install popular MCP servers for various services
- Configure MCP servers in Claude Code settings

---

## Creating MCP Servers

### TypeScript (Recommended for npm distribution)

**Setup:**
```bash
mkdir my-mcp-server && cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D @types/node typescript
```

**package.json:**
```json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "main": "build/index.js",
  "bin": {
    "my-mcp-server": "build/index.js"
  },
  "scripts": {
    "build": "tsc",
    "start": "node build/index.js"
  }
}
```

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./build",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "declaration": true
  },
  "include": ["src/**/*"]
}
```

**src/index.ts (Basic Server):**
```typescript
#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-mcp-server",
  version: "1.0.0",
});

// Define a tool
server.tool(
  "greet",
  "Greet a user by name",
  {
    name: z.string().describe("Name to greet"),
  },
  async ({ name }) => {
    return {
      content: [{ type: "text", text: `Hello, ${name}!` }],
    };
  }
);

// Define a resource
server.resource(
  "config",
  "config://app",
  async (uri) => ({
    contents: [{ uri, mimeType: "application/json", text: JSON.stringify({ version: "1.0" }) }],
  })
);

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

**Build & Test:**
```bash
npm run build
npx @modelcontextprotocol/inspector node build/index.js
```

---

### Python (Recommended for data/ML integrations)

**Setup:**
```bash
mkdir my-mcp-server && cd my-mcp-server
python -m venv venv
source venv/bin/activate
pip install "mcp[cli]" fastmcp
```

**server.py (FastMCP - Recommended):**
```python
#!/usr/bin/env python3
from fastmcp import FastMCP

mcp = FastMCP(name="my-mcp-server")

@mcp.tool
def greet(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"

@mcp.tool
def calculate(a: float, b: float, operation: str) -> float:
    """Perform arithmetic: add, subtract, multiply, divide."""
    ops = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else float('inf'),
    }
    return ops.get(operation, 0)

@mcp.resource("config://app")
def get_config() -> str:
    """Return app configuration."""
    import json
    return json.dumps({"version": "1.0"})

if __name__ == "__main__":
    mcp.run()
```

**server.py (Official SDK):**
```python
#!/usr/bin/env python3
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("my-mcp-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="greet",
            description="Greet a user",
            inputSchema={
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "greet":
        return [TextContent(type="text", text=f"Hello, {arguments['name']}!")]

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**Test:**
```bash
python -m mcp dev server.py
# or
fastmcp dev server.py
```

---

## MCP Server Catalog

### By Domain Skill

#### Marketing Domain (`faion-marketing-domain-skill`)

| Service | Package | Tools |
|---------|---------|-------|
| **Google Ads** | `google-ads-mcp` | Campaign management, reporting |
| **Meta Ads** | `@pipeboard-co/meta-ads-mcp` | FB/IG ads, audiences, A/B testing |
| **Mailgun** | `@mailgun/mailgun-mcp-server` | Transactional email, analytics |
| **SendGrid** | `sendgrid-mcp` | Email marketing, templates |
| **Mixpanel** | Mixpanel hosted MCP | Product analytics |
| **Stripe** | `@stripe/mcp` | Payments, subscriptions |

```bash
# Meta Ads (Facebook, Instagram)
claude mcp add meta-ads -s user -e META_ACCESS_TOKEN=... -- npx -y @pipeboard-co/meta-ads-mcp

# Google Ads
claude mcp add google-ads -s user -e GOOGLE_ADS_DEVELOPER_TOKEN=... -- npx -y google-ads-mcp

# Mailgun
claude mcp add mailgun -s user -e MAILGUN_API_KEY=... -e MAILGUN_DOMAIN=... -- npx -y @mailgun/mailgun-mcp-server

# SendGrid
claude mcp add sendgrid -s user -e SENDGRID_API_KEY=... -- npx -y sendgrid-mcp

# Stripe
claude mcp add stripe -s user -e STRIPE_SECRET_KEY=... -- npx -y @stripe/mcp --tools=all
```

#### Product Domain (`faion-product-domain-skill`)

| Service | Package | Tools |
|---------|---------|-------|
| **Mixpanel** | Hosted MCP | Analytics, funnels, cohorts |
| **Amplitude** | `amplitude-mcp` | Event analytics |
| **PostHog** | `posthog-mcp` | Product analytics, feature flags |
| **Statsig** | Statsig MCP | A/B testing, feature flags |

```bash
# Mixpanel (hosted - OAuth)
# Connect via https://mixpanel.com/mcp

# PostHog
claude mcp add posthog -s user -e POSTHOG_API_KEY=... -e POSTHOG_HOST=... -- npx -y posthog-mcp
```

#### PM Domain (`faion-pm-domain-skill`)

| Service | Package | Tools |
|---------|---------|-------|
| **Jira** | `@anthropic/jira-mcp` | Issues, sprints, boards |
| **Linear** | `@anthropic/linear-mcp` | Issue tracking |
| **ClickUp** | `@taazkareem/clickup-mcp-server` | Tasks (36 tools) |
| **Trello** | `trello-mcp` | Boards, cards, lists |
| **Monday** | `@waystation/mcp` | Workspaces |
| **Asana** | `asana-mcp` | Projects, tasks |

```bash
# Jira
claude mcp add jira -s user \
  -e JIRA_URL=https://your.atlassian.net \
  -e JIRA_EMAIL=email \
  -e JIRA_API_TOKEN=token \
  -- npx -y @anthropic/jira-mcp

# Linear
claude mcp add linear -s user -e LINEAR_API_KEY=... -- npx -y @anthropic/linear-mcp

# ClickUp
claude mcp add clickup -s user -e CLICKUP_API_KEY=... -- npx -y @taazkareem/clickup-mcp-server

# Trello
claude mcp add trello -s user -e TRELLO_API_KEY=... -e TRELLO_TOKEN=... -- npx -y trello-mcp
```

#### Development Domain (`faion-development-domain-skill`)

| Service | Package | Tools |
|---------|---------|-------|
| **GitHub** | `@anthropic/github-mcp` | Repos, PRs, issues |
| **GitLab** | `gitlab-mcp` | GitLab API |
| **PostgreSQL** | `@anthropic/postgres-mcp` | Database queries |
| **Redis** | `redis-mcp` | Cache operations |
| **Docker** | `docker-mcp` | Container management |

```bash
# GitHub
claude mcp add github -s user -e GITHUB_TOKEN=... -- npx -y @anthropic/github-mcp

# PostgreSQL
claude mcp add postgres -s user -e DATABASE_URL=postgres://... -- npx -y @anthropic/postgres-mcp
```

#### UX Domain (`faion-ux-domain-skill`)

| Service | Package | Tools |
|---------|---------|-------|
| **Figma** | `@anthropic/figma-mcp` | Design-to-code |
| **Figma (local)** | Desktop app | Layer inspection |

```bash
# Figma (remote)
claude mcp add figma -s user -- npx -y @anthropic/figma-mcp
```

#### Research Domain (`faion-research-domain-skill`)

| Service | Package | Tools |
|---------|---------|-------|
| **Airtable** | `airtable-mcp` | Database access |
| **Notion** | `@notionhq/notion-mcp-server` | Pages, databases |
| **Google Sheets** | `google-sheets-mcp` | Spreadsheet access |

```bash
# Notion
claude mcp add notion -s user -e NOTION_API_KEY=... -- npx -y @notionhq/notion-mcp-server

# Airtable
claude mcp add airtable -s user -e AIRTABLE_API_KEY=... -- npx -y airtable-mcp
```

### Social Media

| Service | Package | Tools |
|---------|---------|-------|
| **Twitter/X** | `mcp-twitter-server` | Posts, search (53 tools) |
| **Instagram** | `instagram-mcp` | Analytics, posts |
| **LinkedIn** | via `social-media-mcp-server` | Posts |
| **Telegram** | `telegram-mcp` | Messages, groups |

```bash
# Twitter/X (comprehensive)
claude mcp add twitter -s user \
  -e TWITTER_API_KEY=... \
  -e TWITTER_API_SECRET=... \
  -e TWITTER_ACCESS_TOKEN=... \
  -e TWITTER_ACCESS_SECRET=... \
  -- npx -y mcp-twitter-server

# Telegram
claude mcp add telegram -s user \
  -e TELEGRAM_API_ID=... \
  -e TELEGRAM_API_HASH=... \
  -- npx -y telegram-mcp

# Multi-platform (Twitter, LinkedIn, FB, IG via Ayrshare)
claude mcp add social -s user \
  -e AYRSHARE_API_KEY=... \
  -e GROQ_API_KEY=... \
  -- npx -y social-media-mcp-server
```

### E-commerce

| Service | Package | Tools |
|---------|---------|-------|
| **Stripe** | `@stripe/mcp` | Payments, subscriptions |
| **Shopify** | `shopify-mcp` | Products, orders |

```bash
# Stripe (official)
claude mcp add stripe -s user -e STRIPE_SECRET_KEY=... -- npx -y @stripe/mcp --tools=all

# Shopify
claude mcp add shopify -s user \
  -e SHOPIFY_STORE_URL=... \
  -e SHOPIFY_ACCESS_TOKEN=... \
  -- npx -y shopify-mcp
```

### AI & Generative

| Service | Package | Tools |
|---------|---------|-------|
| **OpenAI/DALL-E** | `openai-mcp` | Image generation |
| **Replicate** | `replicate-mcp` | ML models |
| **ElevenLabs** | `elevenlabs-mcp` | Voice synthesis |

```bash
# DALL-E / OpenAI Images
claude mcp add dalle -s user -e OPENAI_API_KEY=... -- npx -y openai-mcp

# ElevenLabs
claude mcp add elevenlabs -s user -e ELEVENLABS_API_KEY=... -- npx -y elevenlabs-mcp
```

### Infrastructure

| Service | Package | Tools |
|---------|---------|-------|
| **Cloudflare** | `@cloudflare/mcp-server-cloudflare` | DNS, Workers, KV, R2 |
| **Hetzner** | `mcp-hetzner` | Server management |
| **AWS** | `aws-mcp` | AWS services |
| **Vercel** | `vercel-mcp` | Deployments |

```bash
# Cloudflare (13 servers!)
claude mcp add cloudflare -s user \
  -e CLOUDFLARE_API_TOKEN=... \
  -e CLOUDFLARE_ACCOUNT_ID=... \
  -- npx -y @cloudflare/mcp-server-cloudflare

# Hetzner
claude mcp add hetzner -s user -e HETZNER_API_TOKEN=... -- npx -y mcp-hetzner
```

---

## MCP Server Templates

### API Wrapper Template (TypeScript)

```typescript
#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const API_KEY = process.env.MY_API_KEY;
const BASE_URL = "https://api.example.com";

const server = new McpServer({
  name: "example-api-mcp",
  version: "1.0.0",
});

async function apiCall(endpoint: string, method = "GET", body?: object) {
  const res = await fetch(`${BASE_URL}${endpoint}`, {
    method,
    headers: {
      "Authorization": `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  return res.json();
}

// List items
server.tool(
  "list_items",
  "List all items from the API",
  {},
  async () => {
    const data = await apiCall("/items");
    return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
  }
);

// Get item by ID
server.tool(
  "get_item",
  "Get a specific item by ID",
  { id: z.string().describe("Item ID") },
  async ({ id }) => {
    const data = await apiCall(`/items/${id}`);
    return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
  }
);

// Create item
server.tool(
  "create_item",
  "Create a new item",
  {
    name: z.string().describe("Item name"),
    description: z.string().optional().describe("Item description"),
  },
  async ({ name, description }) => {
    const data = await apiCall("/items", "POST", { name, description });
    return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

### Database Wrapper Template (Python)

```python
#!/usr/bin/env python3
import os
import json
from fastmcp import FastMCP
import asyncpg

DATABASE_URL = os.environ.get("DATABASE_URL")

mcp = FastMCP(name="database-mcp")

@mcp.tool
async def query(sql: str) -> str:
    """Execute a read-only SQL query."""
    if not sql.strip().upper().startswith("SELECT"):
        return "Error: Only SELECT queries are allowed"

    conn = await asyncpg.connect(DATABASE_URL)
    try:
        rows = await conn.fetch(sql)
        return json.dumps([dict(row) for row in rows], default=str)
    finally:
        await conn.close()

@mcp.tool
async def list_tables() -> str:
    """List all tables in the database."""
    sql = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        rows = await conn.fetch(sql)
        return json.dumps([row["table_name"] for row in rows])
    finally:
        await conn.close()

@mcp.tool
async def describe_table(table: str) -> str:
    """Get column information for a table."""
    sql = """
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = $1
    """
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        rows = await conn.fetch(sql, table)
        return json.dumps([dict(row) for row in rows])
    finally:
        await conn.close()

if __name__ == "__main__":
    mcp.run()
```

---

## Publishing MCP Servers

### npm (TypeScript)

```bash
# Build
npm run build

# Login to npm
npm login

# Publish
npm publish --access public
```

### PyPI (Python)

```bash
# Install build tools
pip install build twine

# Build
python -m build

# Upload
twine upload dist/*
```

---

## Testing & Debugging

```bash
# TypeScript - use MCP Inspector
npx @modelcontextprotocol/inspector node build/index.js

# Python - use FastMCP dev mode
fastmcp dev server.py

# Or official MCP dev
python -m mcp dev server.py
```

---

## Configuration in Claude Code

### Via CLI

```bash
claude mcp add <name> -s user -- <command> [args...]
claude mcp add <name> -s user -e KEY=value -- <command>
claude mcp list
claude mcp remove <name> -s user
```

### Via settings.json

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "my-mcp-server"],
      "env": {
        "API_KEY": "..."
      }
    }
  }
}
```

---

## Resources

- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP](https://gofastmcp.com/)
- [MCP Inspector](https://www.npmjs.com/package/@modelcontextprotocol/inspector)
- [Awesome MCP Servers](https://github.com/wong2/awesome-mcp-servers)
- [Official MCP Servers](https://github.com/modelcontextprotocol/servers)

---

*Created with [faion.net](https://faion.net) framework*
