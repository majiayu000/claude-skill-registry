---
name: nextjs-devtools
description: Next.js development tooling via MCP. Inspect routes, components, build info, and debug Next.js apps. Use when working on Next.js applications, debugging routing, or inspecting app structure. NOT for general React or non-Next.js projects.
---

# Next.js DevTools

Inspect and debug Next.js applications via MCP server.

## Quick Start

```bash
# Start server (spawns on-demand)
bash scripts/start-server.sh

# Or use directly via mcp-client
python3 scripts/mcp-client.py call \
  -s "npx next-devtools-mcp@latest" \
  -t list-routes
```

## Available Tools

| Tool | Description |
|------|-------------|
| `list-routes` | Get all app routes |
| `get-route-info` | Details for specific route |
| `list-components` | React components in app |
| `get-build-info` | Build configuration |
| `get-config` | next.config.js settings |

## Workflow Patterns

### Pattern 1: Route Inspection

```bash
# List all routes
python3 scripts/mcp-client.py call \
  -s "npx next-devtools-mcp@latest" \
  -t list-routes

# Get specific route details
python3 scripts/mcp-client.py call \
  -s "npx next-devtools-mcp@latest" \
  -t get-route-info \
  -p '{"route": "/api/auth"}'
```

### Pattern 2: Debug Build Issues

```bash
# Check build config
python3 scripts/mcp-client.py call \
  -s "npx next-devtools-mcp@latest" \
  -t get-build-info

# Check next.config.js
python3 scripts/mcp-client.py call \
  -s "npx next-devtools-mcp@latest" \
  -t get-config
```

### Pattern 3: Component Discovery

```bash
python3 scripts/mcp-client.py call \
  -s "npx next-devtools-mcp@latest" \
  -t list-components
```

## Scripts

### start-server.sh

For persistent server (multiple calls):

```bash
bash scripts/start-server.sh
# Server runs on default port
# Use mcp-client.py with -u flag instead of -s
```

### On-Demand (Recommended)

For single calls, use `-s` flag which spawns server per-call:

```bash
python3 scripts/mcp-client.py call \
  -s "npx next-devtools-mcp@latest" \
  -t <tool-name>
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Server not starting | Check `npx next-devtools-mcp@latest` works manually |
| No routes found | Ensure running from Next.js project root |
| Build info empty | Run `next build` first |
