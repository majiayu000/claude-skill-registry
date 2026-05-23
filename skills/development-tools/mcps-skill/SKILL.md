---
name: mcps
description: MCP CLI Manager - Manage MCP servers and call tools
homepage: https://github.com/maplezzk/mcps
metadata: {"clawdbot":{"emoji":"🔌","requires":{"bins":["mcps"]},"install":[{"id":"npm","kind":"node","package":"@maplezzk/mcps","bins":["mcps"],"label":"Install mcps"}]}}
---

# mcps - MCP CLI Manager

A powerful command-line tool for managing and calling MCP (Model Context Protocol) servers.

## Installation

```bash
npm install -g @maplezzk/mcps
```

## Configuration Examples

### Adding Various MCP Servers

```bash
# Add fetch server (web scraping)
mcps add fetch --command uvx --args mcp-server-fetch

# Add PostgreSQL server
mcps add postgres --command npx --args @modelcontextprotocol/server-postgres --env POSTGRES_CONNECTION_STRING="${DATABASE_URL}"

# Add GitLab server
mcps add gitlab --command npx --args gitlab-mcp-server

# Add SSE server
mcps add remote --type sse --url http://localhost:8000/sse

# Add HTTP server
mcps add http-server --type http --url http://localhost:8000/mcp
```

### Config File Example (~/.mcps/mcp.json)

```json
{
  "servers": [
    {
      "name": "fetch",
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    },
    {
      "name": "postgres",
      "type": "stdio",
      "command": "npx",
      "args": ["@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${DATABASE_URL}"
      }
    },
    {
      "name": "gitlab",
      "type": "stdio",
      "command": "npx",
      "args": ["gitlab-mcp-server"],
      "env": {
        "GITLAB_PERSONAL_ACCESS_TOKEN": "${GITLAB_TOKEN}",
        "GITLAB_API_URL": "https://gitlab.com/api/v4"
      }
    }
  ]
}
```

**Note**: Use environment variables for sensitive data (`${VAR_NAME}` format).

## Quick Start

```bash
# 1. Add an MCP server
mcps add fetch --command uvx --args mcp-server-fetch

# 2. Start the daemon
mcps start

# 3. Check status
mcps status

# 4. List available tools
mcps tools fetch

# 5. Call a tool
mcps call fetch fetch url="https://example.com"
```

## Command Reference

### Server Management

| Command | Description |
|---------|-------------|
| `mcps ls` | List all configured servers |
| `mcps add <name> --command <cmd> --args <args>` | Add a new server |
| `mcps rm <name>` | Remove a server |
| `mcps update [name]` | Update server configuration |
| `mcps update <name> --disabled true` | Disable a server |

### Daemon Control

| Command | Description |
|---------|-------------|
| `mcps start [--verbose]` | Start daemon (verbose mode for debugging) |
| `mcps stop` | Stop daemon |
| `mcps restart [server]` | Restart daemon or specific server |
| `mcps status` | Check daemon status |

### Tool Invocation

| Command | Description |
|---------|-------------|
| `mcps tools <server> [--simple]` | List available tools |
| `mcps call <server> <tool> [args...]` | Call a tool |

## Tool Invocation: Parameter Passing

### Default Mode (Auto JSON Parsing)

```bash
# String values are sent as-is
mcps call fetch fetch url="https://example.com"

# Numbers and booleans are auto-parsed
mcps call fetch fetch max_length=5000 follow_redirects=true
# Sends: { "max_length": 5000, "follow_redirects": true }

# JSON objects (use single quotes outside)
mcps call my-server createUser user='{"name": "Alice", "age": 30}'
```

### --raw Mode (Keep Values as Strings)

```bash
# Use --raw for SQL IDs, codes, or strings that should not be parsed
mcps call my-db createOrder --raw order_id="12345" sku="ABC-001"
# Sends: { "order_id": "12345", "sku": "ABC-001" }

# SQL with special characters
mcps call alibaba-dms createDataChangeOrder --raw \
  database_id="123" \
  script="DELETE FROM table WHERE id = 'xxx';" \
  logic="true"
```

### --json Mode (Complex Parameters)

```bash
# From JSON string
mcps call my-server createUser --json '{"name": "Alice", "age": 30}'

# From file
mcps call my-server createUser --json params.json
```

## Real-World Usage Examples

### Scenario 1: Web Scraping and Search

```bash
# Fetch webpage content
mcps call fetch fetch url="https://example.com" max_length=5000

# Deep fetch (follow links)
mcps call fetch fetch url="https://example.com" follow_redirects=true max_depth=2

# Filtered fetch
mcps call fetch fetch url="https://news.example.com" include_tags='["article", "p"]' exclude_tags='["script", "style"]'
```

### Scenario 2: Database Query

```bash
# Query data (auto-parsed parameters)
mcps call postgres query sql="SELECT * FROM users WHERE active = true LIMIT 10"

# Keep parameters as strings (use --raw)
mcps call postgres query --raw sql="SELECT * FROM orders WHERE id = '12345'"
```

### Scenario 3: Complex Parameter Passing

```bash
# JSON object parameters
mcps call my-server createUser user='{"name": "Alice", "age": 30, "tags": ["admin", "user"]}'

# Load JSON from file
mcps call my-server createUser --json user.json

# Mixed parameters (some auto-parsed, some raw)
mcps call my-server update --raw id="123" data='{"name": "Updated"}'
```

### Scenario 4: Server Management

```bash
# View all server configurations
mcps ls

# Check active connections
mcps status

# Restart a single server
mcps restart postgres

# Restart all servers
mcps restart

# Disable a server (without removing config)
mcps update my-server --disabled true

# Remove a server
mcps rm my-server
```

### Scenario 5: Tool Filtering and Search

```bash
# Show only tool names (simple mode)
mcps tools postgres --simple

# Filter tools by keyword
mcps tools postgres --tool query --tool describe

# Find tools containing "create"
mcps tools postgres --tool create
```

## Configuration

- **Config file**: `~/.mcps/mcp.json`
- **Environment variables**:
  - `MCPS_CONFIG_DIR`: Config directory
  - `MCPS_PORT`: Daemon port (default: 4100)
  - `MCPS_VERBOSE`: Verbose logging mode

## FAQ

**Q: How to check server status?**
```bash
mcps status  # Check active connections
mcps ls      # Check all configurations (including disabled)
```

**Q: Server connection failed?**
```bash
mcps start --verbose  # View detailed logs
mcps restart my-server  # Restart specific server
```

**Q: How to quickly find tools?**
```bash
mcps tools my-server --tool keyword  # Filter by keyword
mcps tools my-server --simple        # Show names only
```

**Q: Special characters in parameters (e.g., SQL)?**
```bash
# Use --raw to keep string format
mcps call alibaba-dms createDataChangeOrder --raw \
  database_id="123" \
  script="DELETE FROM table WHERE id = 'xxx';" \
  logic="true"
```

**Q: Daemon starts slowly?**
- First start loads all servers, 10-15 seconds is normal
- Subsequent starts are faster (~2 seconds)
- Use `mcps ls` to check config without starting daemon
