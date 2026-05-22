---
name: apollo-mcp-server
description: >
  Guide for using Apollo MCP Server to connect AI agents with GraphQL APIs.
  Use this skill when: (1) setting up or configuring Apollo MCP Server,
  (2) defining MCP tools from GraphQL operations, (3) using introspection
  tools (introspect, search, validate, execute), (4) troubleshooting
  MCP server connectivity or tool execution issues.
license: MIT
compatibility: Requires rover CLI v0.37+, Node.js v18+. Works with Claude Code, Claude Desktop, Cursor.
metadata:
  author: apollographql
  version: "1.0"
allowed-tools: Bash(rover:*) Bash(npx:*) Read Write Edit Glob Grep
---

# Apollo MCP Server Guide

Apollo MCP Server exposes GraphQL operations as MCP tools, enabling AI agents to interact with GraphQL APIs through the Model Context Protocol.

## Quick Start

### Step 1: Install

```bash
# Using npm
npm install -g @apollo/mcp-server

# Or run directly with npx
npx @apollo/mcp-server
```

### Step 2: Configure

Create `mcp.yaml` in your project root:

```yaml
# mcp.yaml
endpoint: https://api.example.com/graphql
schema:
  type: local
  path: ./schema.graphql
operations:
  type: local
  paths:
    - ./operations/**/*.graphql
introspection:
  enabled: true
```

### Step 3: Connect

Add to your MCP client configuration:

**Claude Desktop (`claude_desktop_config.json`):**
```json
{
  "mcpServers": {
    "graphql-api": {
      "command": "npx",
      "args": ["@apollo/mcp-server", "--config", "./mcp.yaml"]
    }
  }
}
```

**Claude Code (`.mcp.json`):**
```json
{
  "mcpServers": {
    "graphql-api": {
      "command": "npx",
      "args": ["@apollo/mcp-server", "--config", "./mcp.yaml"]
    }
  }
}
```

## Built-in Tools

Apollo MCP Server provides four introspection tools:

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `introspect` | Explore schema types in detail | Need type definitions, fields, relationships |
| `search` | Find types in schema | Looking for specific types or fields |
| `validate` | Check operation validity | Before executing operations |
| `execute` | Run ad-hoc GraphQL operations | Testing or one-off queries |

## Defining Custom Tools

MCP tools are created from GraphQL operations. Three methods:

### 1. Operation Files (Recommended)

```yaml
operations:
  type: local
  paths:
    - ./operations/**/*.graphql
```

```graphql
# operations/users.graphql
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
    email
  }
}

mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    name
  }
}
```

Each named operation becomes an MCP tool.

### 2. Operation Collections

```yaml
operations:
  type: collection
  id: your-collection-id
```

Use GraphOS Studio to manage operations collaboratively.

### 3. Persisted Queries

```yaml
operations:
  type: manifest
  path: ./persisted-query-manifest.json
```

For production environments with pre-approved operations.

## Reference Files

Detailed documentation for specific topics:

- [Tools](references/tools.md) - Introspection tools and minify notation
- [Configuration](references/configuration.md) - All configuration options
- [Troubleshooting](references/troubleshooting.md) - Common issues and solutions

## Key Rules

### Security

- **Never expose sensitive operations** without authentication
- Use `headers` configuration for API keys and tokens
- Prefer `introspection.enabled: false` in production
- Set `introspection.mutationMode: prompt` to require confirmation for mutations

### Authentication

```yaml
# Static header
headers:
  Authorization: "Bearer ${APOLLO_API_KEY}"

# Dynamic header passthrough
headers:
  X-User-Token:
    from: x-forwarded-token
```

### Token Optimization

Enable minification to reduce token usage:

```yaml
introspection:
  minify: true
```

Minified output uses compact notation:
- **T** = type, **I** = input, **E** = enum
- **s** = String, **i** = Int, **b** = Boolean, **f** = Float
- **!** = required, **[]** = list

### Mutations

Control mutation behavior:

```yaml
introspection:
  mutationMode: allowed   # Execute directly
  mutationMode: prompt    # Require confirmation (default)
  mutationMode: disabled  # Block all mutations
```

## Common Patterns

### GraphOS Cloud Schema

```yaml
schema:
  type: uplink
graphos:
  key: ${APOLLO_KEY}
  graph_ref: my-graph@production
```

### Local Development

```yaml
endpoint: http://localhost:4000/graphql
schema:
  type: local
  path: ./schema.graphql
introspection:
  enabled: true
  mutationMode: allowed
```

### Production Setup

```yaml
endpoint: https://api.production.com/graphql
schema:
  type: uplink
operations:
  type: manifest
  path: ./persisted-query-manifest.json
introspection:
  enabled: false
```

## Ground Rules

- ALWAYS configure authentication before exposing to AI agents
- ALWAYS use `mutationMode: prompt` in shared environments
- NEVER expose introspection tools with write access to production data
- PREFER operation files over ad-hoc execute for predictable behavior
- USE GraphOS Studio collections for team collaboration
