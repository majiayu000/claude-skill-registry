---
name: mcp-debug
# prettier-ignore
description: "Use when testing MCP servers, debugging MCP tool responses, exploring MCP capabilities, or diagnosing why an MCP tool returns unexpected data"
version: 1.0.0
category: debugging
triggers:
  - "mcp"
  - "test mcp"
  - "debug mcp"
  - "mcp tool"
  - "mcp server"
  - "mcptools"
---

<objective>
Enable Claude to directly test and debug MCP servers during development sessions. Call
MCP tools directly, see raw responses, and diagnose issues in real-time.
</objective>

<when-to-use>
Use this skill when:
- Testing an MCP server during development
- Debugging why an MCP tool isn't returning expected data
- Exploring what operations an MCP server supports
- Verifying MCP server connectivity and auth
- Working across application and MCP server repos simultaneously
</when-to-use>

<prerequisites>
This skill uses `mcptools` (https://github.com/f/mcptools) for MCP communication.

Before using MCP debug commands, ensure mcptools is installed:

```bash
# Check if installed
which mcp || which mcpt

# Install via Homebrew (macOS)
brew tap f/mcptools && brew install mcp

# Or via Go
go install github.com/f/mcptools/cmd/mcptools@latest
```

If mcptools is not found, install it first before proceeding. </prerequisites>

<config-discovery>
MCP server configs can come from multiple sources:

1. **Claude Code config**: `~/.config/claude/claude_desktop_config.json`
2. **Direct URL**: `http://localhost:9900` with optional auth
3. **mcptools aliases**: Previously saved with `mcp alias add`

To find available servers:

```bash
# Scan all known config locations
mcp configs scan

# List saved aliases
mcp alias list
```

</config-discovery>

<commands>

## List Tools

See what tools/operations an MCP server provides:

```bash
# HTTP server with bearer auth
mcp tools http://localhost:9900 --headers "Authorization=Bearer $AUTH_TOKEN"

# Using an alias
mcp tools server-alias

# Pretty JSON output
mcp tools --format pretty http://localhost:9900
```

## Call a Tool

Execute an MCP tool directly with parameters:

```bash
# Call with JSON params
mcp call describe --params '{"action":"describe"}' http://localhost:9900 \
  --headers "Authorization=Bearer $AUTH_TOKEN"

# Gateway-style (single tool with action param)
mcp call server-tool --params '{"action":"messages_recent","params":{"limit":5}}' \
  http://localhost:9900 --headers "Authorization=Bearer $AUTH_TOKEN"

# Format output as pretty JSON
mcp call tool_name --params '{}' --format pretty http://localhost:9900
```

## Interactive Shell

Open persistent connection for multiple commands:

```bash
mcp shell http://localhost:9900 --headers "Authorization=Bearer $AUTH_TOKEN"

# Then in shell:
# mcp> tools
# mcp> call describe --params '{"action":"describe"}'
```

## Web Interface

Visual debugging in browser:

```bash
mcp web http://localhost:9900 --headers "Authorization=Bearer $AUTH_TOKEN"
# Opens http://localhost:41999
```

</commands>

<example-server>

## Example: Gateway Pattern MCP Server

Many MCP servers use a gateway pattern - a single tool with an `action` parameter for
progressive disclosure:

```bash
# List all operations
mcp call server-tool --params '{"action":"describe"}' http://localhost:9900 \
  --headers "Authorization=Bearer $AUTH_TOKEN"

# Call specific operation
mcp call server-tool --params '{"action":"resource_list","params":{"limit":5}}' \
  http://localhost:9900 --headers "Authorization=Bearer $AUTH_TOKEN"
```

### Common Debug Commands

```bash
# Check if server is responding
curl -s http://localhost:9900/health

# List all tools via mcptools
mcp tools http://localhost:9900 --headers "Authorization=Bearer $AUTH_TOKEN"

# Get operation descriptions
mcp call server-tool --params '{"action":"describe"}' --format pretty \
  http://localhost:9900 --headers "Authorization=Bearer $AUTH_TOKEN"

# Test a specific operation
mcp call server-tool --params '{"action":"resource_list","params":{"limit":3}}' \
  --format pretty http://localhost:9900 --headers "Authorization=Bearer $AUTH_TOKEN"
```

</example-server>

<troubleshooting>

## Common Issues

**Connection refused**

- Check if server is running: `curl http://localhost:9900/health`
- Check if process is running (e.g., `ps aux | grep mcp-server`)
- Check logs: `tail -20 /path/to/server/logs/error.log`

**401 Unauthorized**

- Verify token: `echo $AUTH_TOKEN`
- Check mcptools header syntax: `Authorization=Bearer` (mcptools uses `=`, HTTP uses
  `:`)

**Tool not found**

- Gateway pattern servers use a single tool with `action` param
- Not direct tool names - check server documentation for tool name

**Empty/error results**

- Check server permissions and configuration
- Run server-specific diagnostics if available
- Check server logs for errors

**mcptools not found**

- Install: `brew tap f/mcptools && brew install mcp`
- Or: `go install github.com/f/mcptools/cmd/mcptools@latest`

</troubleshooting>

<workflow>

## Typical Debug Session

1. **Verify connectivity**

   ```bash
   curl -s http://localhost:9900/health
   ```

2. **List available tools**

   ```bash
   mcp tools http://localhost:9900 --headers "Authorization=Bearer $AUTH_TOKEN"
   ```

3. **Get operation descriptions**

   ```bash
   mcp call server-tool --params '{"action":"describe"}' --format pretty \
     http://localhost:9900 --headers "Authorization=Bearer $AUTH_TOKEN"
   ```

4. **Test specific operation**

   ```bash
   mcp call server-tool --params '{"action":"resource_list","params":{"limit":3}}' \
     --format pretty http://localhost:9900 --headers "Authorization=Bearer $AUTH_TOKEN"
   ```

5. **If issues, check logs**
   ```bash
   tail -50 /path/to/server/logs/error.log
   ```

</workflow>

<output-interpretation>

## Reading MCP Results

MCP tools return JSON with this structure:

```json
{
  "content": [
    {
      "type": "text",
      "text": "{ ... actual result as JSON string ... }"
    }
  ]
}
```

The inner `text` field contains the actual result, often as a JSON string that needs
parsing. Use `jq` to extract:

```bash
mcp call server-tool --params '...' --format json http://localhost:9900 \
  --headers "Authorization=Bearer $AUTH_TOKEN" \
  | jq -r '.content[0].text' | jq .
```

</output-interpretation>
