---
name: aspire__setup_mcp
description: Configure Aspire MCP server for AI agent access to logs, metrics, and traces. Use this to enable programmatic access to Aspire observability data.
---

Follow this guide to set up the Aspire MCP server for agent access to logs and metrics.

## What is Aspire MCP?

Aspire MCP (Model Context Protocol) server exposes Aspire's observability data to AI agents:
- **Console logs**: Real-time stdout/stderr from all services
- **Structured logs**: Filterable logs with correlation IDs
- **Metrics**: CPU, memory, HTTP request metrics
- **Traces**: Distributed tracing across services

## Setup Steps

// turbo
1. **Initialize Aspire MCP**
   ```bash
   cd /home/avazalma/projects/BookStore && aspire mcp init
   ```
   - Creates MCP configuration in the project
   - Sets up connection between Aspire and MCP clients

2. **Verify MCP Configuration**
   - Check that MCP server config was created
   - Aspire MCP integrates with Claude and other MCP-compatible agents

## Using Aspire MCP

Once configured, the MCP server provides tools for:

- **Querying logs**: Filter by service, log level, time range
- **Viewing metrics**: Get current metric values and trends
- **Tracing requests**: Follow requests across services via correlation IDs
- **Monitoring health**: Check service status and health endpoints

## Example Usage

After setup, agents can:
- Query logs: "Show me errors from the API service in the last 5 minutes"
- Check metrics: "What's the current memory usage of the web frontend?"
- Debug issues: "Find all logs with correlation ID xyz-123"

## Related Skills

**Prerequisites**:
- `/aspire__start_solution` - Solution must be running first

**Next Steps**:
- `/frontend__debug_sse` - Debug real-time issues using MCP logs
- `/cache__debug_cache` - Debug caching using MCP metrics

**See Also**:
- `docs/guides/aspire-guide.md`
- `docs/guides/logging-guide.md`
- https://learn.microsoft.com/en-us/dotnet/aspire/
