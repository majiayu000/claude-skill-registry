---
name: docker-mcp
description: Comprehensive guide for Docker MCP Toolkit Dynamic Tools - discover and use ~170 MCP servers on-demand. Use when working with MCP servers, dynamic tools, database access, APIs, cloud services, or needing external integrations during conversations.
license: MIT
version: 1.0.0
---

# Docker MCP Dynamic Tools Skill

This skill provides expert guidance on using Docker MCP Toolkit's Dynamic MCP capabilities to discover and add MCP servers on-demand during conversations.

## When to Use This Skill

Use this skill when:
- User mentions "MCP", "mcp", "MCP server", or "dynamic tools"
- You need database access (PostgreSQL, MySQL, SQLite, MongoDB, Redis, etc.)
- You need Git/Cloud services (GitHub, GitLab, AWS, Cloudflare, etc.)
- You need web scraping or API integration (Apify, OpenAPI, etc.)
- You need specialized tools beyond base capabilities
- User asks about available integrations or external services

## What is Dynamic MCP?

Dynamic MCP enables AI agents to discover and add MCP servers on-demand during conversations, without manual pre-configuration. Instead of pre-configuring every MCP server before starting a session, you can search the MCP Catalog (~170 servers) and add servers as needed.

**Key Benefits:**
- ✅ **No pre-configuration needed** - Add servers during conversation
- ✅ **~170 official Docker servers** - All built, signed, and maintained by Docker
- ✅ **Containerized & secure** - Servers run in isolated containers
- ✅ **Session-scoped** - Added servers last for current conversation
- ✅ **Just-in-time capabilities** - Only load what you need

## Available Management Tools

When connected to MCP Gateway, you have access to these primordial tools:

| Tool | Description |
|------|-------------|
| `mcp-find` | Search for MCP servers in catalog by name or description |
| `mcp-add` | Add a new MCP server to current session |
| `mcp-config-set` | Configure settings for an MCP server |
| `mcp-remove` | Remove an MCP server from session |
| `mcp-exec` | Execute a tool by name that exists in current session |
| `code-mode` | Create JavaScript tool combining multiple MCP servers (experimental) |

## Basic Workflow

### 1. Search for Servers

```typescript
// Search using descriptive terms
mcp-find query="postgres" limit=10
mcp-find query="github" limit=5
mcp-find query="database" limit=20

// Common search terms:
// - Databases: "database", "postgres", "mysql", "sqlite", "mongo", "redis"
// - Git: "git", "github", "gitlab"
// - Cloud: "cloud", "aws", "cloudflare", "azure", "gcp"
// - APIs: "api", "openapi", "rest"
// - Web: "web", "scraping", "browser", "fetch"
```

**Important:**
- `query` parameter is **required** (can't list all servers)
- Server names are **case-sensitive**
- Results include `required_secrets` and `config_schema` info

### 2. Check Requirements

Look at search results for:
- **`required_secrets`**: API keys, tokens, connection strings needed
- **`config_schema`**: Additional configuration requirements
- **`description`**: What the server does

### 3. Add Server to Session

```typescript
// Add server (case-sensitive name from search)
mcp-add name="SQLite" activate=false

// Server is immediately available
// Tools appear in your tool list
```

### 4. Configure (If Needed)

```typescript
// Only for servers with config_schema
mcp-config-set server="postgres" key="url" value="postgresql://..."

// Secrets handled separately by Docker
// Docker will prompt user for required secrets
```

### 5. Use the Tools

After adding, tools are immediately available. Use them directly in conversation.

## Real-World Examples

### Example 1: SQLite Database

```typescript
// User asks: "Can you query my SQLite database?"

// 1. Find SQLite servers
mcp-find query="sqlite" limit=3
// Returns: SQLite, sqlite-mcp-server, simplechecklist

// 2. Add the simple one
mcp-add name="SQLite"
// Adds 6 tools: read_query, write_query, create_table,
//                list_tables, describe_table, append_insight

// 3. Use tools
// "read_query" - Execute SELECT queries
// "write_query" - INSERT, UPDATE, DELETE
// "create_table" - Create tables
// "list_tables" - See all tables
// "describe_table" - Get table schema
```

### Example 2: GitHub Integration

```typescript
// User asks: "Create a GitHub issue for this bug"

// 1. Find GitHub servers
mcp-find query="github" limit=5
// Returns: github, github-chat, github-official, deepwiki, hoverfly-mcp-server

// 2. Add GitHub server
mcp-add name="github"
// Requires: github.personal_access_token secret
// Docker will prompt user for token

// 3. Use GitHub tools
// Now have: create_issue, search_repos, read_file, etc.
```

### Example 3: PostgreSQL Database

```typescript
// User asks: "Connect to my Postgres database"

// 1. Find Postgres servers
mcp-find query="postgres" limit=5
// Returns: postgres, prisma-postgres, dreamfactory-mcp, database-server

// 2. Add Postgres server
mcp-add name="postgres"
// Requires: postgres.url secret (connection string)

// 3. Use tools
// Read-only access: schema inspection, SELECT queries
// Security: No write access by default
```

### Example 4: Multi-Server Workflow

```typescript
// User asks: "Scrape a website and store results in database"

// 1. Add web scraping
mcp-find query="scraping" limit=5
mcp-add name="apify"

// 2. Add database
mcp-find query="sqlite" limit=3
mcp-add name="SQLite"

// 3. Use both
// Scrape with Apify tools → Store with SQLite tools
```

## Common Server Categories

### Databases (20+ servers)
- **postgres** - Read-only PostgreSQL access
- **mysql** - MySQL database operations
- **SQLite** - SQLite database with BI capabilities
- **mongodb** - MongoDB operations
- **redis** - Redis key-value store
- **neo4j-memory** - Graph database for persistent memory
- **database-server** - Multi-database (SQLite, Postgres, MySQL)

### Git & Version Control (5+ servers)
- **git** - Git repository automation
- **github** - GitHub API integration
- **gitlab** - GitLab API integration
- **gitmcp** - Git repository tools

### Cloud Platforms (15+ servers)
- **aws-api** - Comprehensive AWS API support
- **cloudflare-workers** - Cloudflare Workers development
- **cloudflare-browser-rendering** - Browser automation
- **gcp** - Google Cloud Platform tools

### Web & APIs (15+ servers)
- **apify** - Web scraping marketplace
- **openapi** - OpenAPI/Swagger spec tools
- **mcp-api-gateway** - Universal API integration
- **cloudflare-browser-rendering** - Browser automation

### Document Processing (5+ servers)
- **gemini-document-processing** - PDF analysis with Gemini
- **gemini-vision** - Image understanding
- **gemini-audio** - Audio transcription/TTS

### Development Tools (10+ servers)
- **schemacrawler-ai** - Database schema documentation
- **instant** - Real-time, offline-first database
- **neon** - Serverless Postgres

## Important Notes

### Session Scope
- ✅ Added servers only last for current conversation
- ✅ Start fresh session = no servers active
- ✅ Can add same servers again anytime

### Security Model
- ✅ All servers are official Docker-built images
- ✅ Servers run in isolated containers
- ✅ Restricted resources and privileges
- ✅ Credentials managed securely by gateway
- ✅ Code mode (experimental) runs in isolated sandbox

### Best Practices

1. **Search first, add second**
   - Always search to see what's available
   - Check requirements before adding
   - Choose the right server for your needs

2. **Case-sensitive names**
   - Use exact name from `mcp-find` results
   - "SQLite" ≠ "sqlite"

3. **Handle secrets gracefully**
   - Servers with `required_secrets` need credentials
   - Docker will prompt user securely
   - Never hardcode secrets

4. **Prefer MCP over manual**
   - If MCP server exists, use it
   - Don't ask user to install tools manually
   - More secure and reliable

5. **Remove when done**
   ```typescript
   mcp-remove name="SQLite"  // Clean up
   ```

6. **Check for errors**
   - Some servers need configuration
   - Read error messages carefully
   - Use `mcp-config-set` when needed

## Troubleshooting

### "Server not found"
- Check spelling (case-sensitive)
- Search again: `mcp-find query="term"`
- Verify server name from search results

### "Required secrets missing"
- Server needs API keys/tokens
- Docker will prompt user
- User must provide credentials

### "Configuration required"
- Check `config_schema` in search results
- Use `mcp-config-set` to configure
- Example: `mcp-config-set server="postgres" key="host" value="localhost"`

### "Tool not working"
- Verify server added successfully
- Check if server requires setup
- Try removing and re-adding: `mcp-remove`, then `mcp-add`

## Advanced: Code Mode (Experimental)

**Note:** Code mode is experimental and not yet reliable for general use.

Create custom JavaScript functions combining multiple MCP tools:

```typescript
// Create tool combining postgres + github
code-mode servers=["postgres", "github"] name="db-to-issue"

// Sandbox with access to both servers' tools
// New tool "db-to-issue" registered
// Execute coordinated workflows
```

**Architecture:**
1. Agent calls `code-mode` with server list and tool name
2. Gateway creates sandbox with those servers' tools
3. New tool registered in session
4. Agent calls the tool
5. JavaScript executes in isolated sandbox
6. Results returned to agent

**Security:** Sandbox can only interact via MCP tools (already containerized).

## Disabling Dynamic MCP

If you prefer static configuration only:

```bash
docker mcp feature disable dynamic-tools

# Re-enable later:
docker mcp feature enable dynamic-tools
```

May need to restart MCP clients after changing.

## Further Reading

- **Docker MCP Toolkit Docs**: https://docs.docker.com/desktop/features/mcp/dynamic-mcp/
- **Blog Post**: https://docker.com/blog (Dynamic MCP examples)
- **MCP Catalog**: Search with `mcp-find` to explore ~170 servers

## Quick Reference Card

```typescript
// Search catalog
mcp-find query="keyword" limit=10

// Add server
mcp-add name="ServerName" activate=false

// Configure
mcp-config-set server="name" key="setting" value="value"

// Remove
mcp-remove name="ServerName"

// Execute tool
mcp-exec name="tool-name" arguments={...}
```

---

**Remember:** When user mentions MCP or needs external integrations, search the catalog first. The ~170 servers cover most common needs - databases, APIs, cloud services, web scraping, and more. It's almost always better to use an official MCP server than to ask the user to install tools manually.
