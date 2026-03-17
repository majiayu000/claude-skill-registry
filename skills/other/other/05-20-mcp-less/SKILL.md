---
name: 05-20-mcp-less
description: "Use MCP without installing"
---

# MCP-Less / Code-mode

## Talk to ANY MCP directly (no client integration required)

You can call MCP servers directly from CLI/code with `bunx` — no Pi/Claude/Cursor connector setup required. Or write scripts/code for this flow.

## Method 1: Direct calls with MCP Inspector CLI

Use `@modelcontextprotocol/inspector` in CLI mode.

### A) Remote Streamable HTTP MCP

```bash
# List tools
bunx --yes @modelcontextprotocol/inspector \
  --cli https://your-mcp-server.example.com/mcp \
  --transport http \
  --method tools/list
```

```bash
# Call tool (no args)
bunx --yes @modelcontextprotocol/inspector \
  --cli https://your-mcp-server.example.com/mcp \
  --transport http \
  --method tools/call \
  --tool-name health_check
```

```bash
# Call tool (with args)
bunx --yes @modelcontextprotocol/inspector \
  --cli https://your-mcp-server.example.com/mcp \
  --transport http \
  --method tools/call \
  --tool-name my_tool \
  --tool-arg 'query=hello world' \
  --tool-arg 'limit=10'
```

### B) Remote SSE MCP

```bash
bunx --yes @modelcontextprotocol/inspector \
  --cli https://your-mcp-server.example.com/sse \
  --transport sse \
  --method tools/list
```

### C) Local stdio MCP process

```bash
# Example: node server
bunx --yes @modelcontextprotocol/inspector \
  --cli node ./dist/index.js \
  --method tools/list
```

## Method 2: Bridge remote MCP to stdio clients (optional)

If a client only supports stdio servers, proxy a remote MCP via `mcp-remote`:

```bash
bunx --yes mcp-remote https://your-mcp-server.example.com/mcp --transport http-first
```

This runs a local stdio proxy connected to the remote MCP server.


## Auth headers (when needed)

For token-protected HTTP/SSE servers:

```bash
bunx --yes @modelcontextprotocol/inspector \
  --cli https://your-mcp-server.example.com/mcp \
  --transport http \
  --header "Authorization: Bearer $TOKEN" \
  --method tools/list
```

## Practical workflow for agents

1. `tools/list`
2. Optional capability/discovery tool (often `read_me`, `help`, or `describe`)
3. `tools/call` with minimal valid args
4. Iterate using server errors/schema hints