---
name: connecting-to-logseq
version: 1.0.0
description: >
  Manages connections to Logseq graphs via HTTP API, CLI, or MCP Server.
  Auto-invokes when users mention connecting to Logseq, API tokens,
  graph paths, connection issues, or backend configuration. Handles
  backend detection, environment setup, and connectivity troubleshooting.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Connecting to Logseq

## When to Use This Skill

This skill auto-invokes when:
- User wants to connect Claude to their Logseq graph
- Setting up Logseq integration or API tokens
- Troubleshooting connection issues
- Configuring graph paths or backends
- User mentions "connect to logseq", "logseq api", "logseq token"
- Questions about HTTP API, CLI, or MCP server setup

**Setup Scripts**: See `{baseDir}/scripts/` for initialization utilities.

## Available Backends

| Backend | Requires Logseq Running | Read | Write | Best For |
|---------|------------------------|------|-------|----------|
| HTTP API | Yes | Full | Full | Real-time, interactive |
| CLI | No | Full | Limited | Offline, batch, CI/CD |
| MCP Server | Yes (via HTTP) | Full | Full | Claude-native tools |

## Quick Start

### 1. Enable Logseq HTTP API

In Logseq:
1. **Settings** → **Advanced** → **Developer mode**: ON
2. **Settings** → **Advanced** → **HTTP APIs server**: ON
3. **Settings** → **Advanced** → **Authorization tokens** → Create token

### 2. Set Environment Variable

```bash
export LOGSEQ_API_TOKEN="your-token-here"
```

### 3. Initialize Plugin

Run the setup wizard:
```bash
python {baseDir}/scripts/init-environment.py
```

Or use the command: `/logseq:init`

## Backend Details

### HTTP API (Primary)

**URL**: `http://127.0.0.1:12315/api`

**Request Format**:
```json
POST /api
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN

{
  "method": "logseq.Editor.getPage",
  "args": ["PageName"]
}
```

**Common Methods**:
- `logseq.App.getCurrentGraph` - Get current graph info
- `logseq.Editor.getPage` - Get page by name
- `logseq.Editor.getBlock` - Get block by UUID
- `logseq.DB.datascriptQuery` - Execute Datalog query
- `logseq.Editor.insertBlock` - Create new block

### CLI (@logseq/cli)

**Installation**:
```bash
npm install -g @logseq/cli
```

**Usage**:
```bash
# Query local graph
logseq query "[:find ?title :where [?p :block/title ?title]]" --graph ~/logseq/my-graph

# With running Logseq (in-app mode)
logseq query "..." --in-app -a YOUR_TOKEN
```

### MCP Server

The plugin includes a custom MCP server that exposes Logseq operations as Claude tools.

**Location**: `servers/logseq-mcp/`

**Build**:
```bash
cd servers/logseq-mcp
npm install
npm run build
```

## Configuration File

**Location**: `.claude/logseq-expert/env.json`

```json
{
  "backend": "auto",
  "http": {
    "url": "http://127.0.0.1:12315",
    "token": "${LOGSEQ_API_TOKEN}"
  },
  "cli": {
    "graphPath": "/path/to/graph",
    "inApp": false
  },
  "mcp": {
    "enabled": true
  },
  "preferences": {
    "defaultGraph": null,
    "confirmWrites": false,
    "backupBeforeWrite": false
  }
}
```

## Troubleshooting

### "Cannot connect to Logseq"

1. **Check Logseq is running** with HTTP API enabled
2. **Verify port**: Default is 12315, check Settings → Advanced
3. **Check firewall**: Ensure localhost:12315 is accessible
4. **Test manually**:
   ```bash
   curl -X POST http://127.0.0.1:12315/api \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -d '{"method":"logseq.App.getCurrentGraph"}'
   ```

### "Authentication failed"

1. **Verify token**: Check it matches what's in Logseq settings
2. **Token format**: Ensure no extra whitespace
3. **Environment variable**: Check `echo $LOGSEQ_API_TOKEN`

### "CLI not found"

1. **Install globally**: `npm install -g @logseq/cli`
2. **Or use npx**: `npx @logseq/cli --help`
3. **Check PATH**: Ensure npm global bin is in PATH

### "MCP server not working"

1. **Build server**: `cd servers/logseq-mcp && npm run build`
2. **Check Node.js**: Requires Node 18+
3. **Verify HTTP API**: MCP server uses HTTP API internally

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `init-environment.py` | Interactive setup wizard |
| `detect-backend.py` | Auto-detect available backends |
| `test-connection.py` | Test connectivity |
| `preflight-checks.sh` | Validate environment |

Run scripts from plugin root:
```bash
python logseq-expert/scripts/init-environment.py
```

## Security Notes

- **Never commit tokens** to version control
- Use **environment variables** for sensitive data
- Token in config supports `${VAR}` syntax for env vars
- HTTP API only listens on localhost by default
