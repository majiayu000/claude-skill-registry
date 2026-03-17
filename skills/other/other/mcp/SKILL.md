---
name: mcp
description: Guide for working with Splitrail's MCP server. Use when adding tools, resources, or modifying the MCP interface.
---

# MCP Server

Splitrail can run as an MCP server, allowing AI assistants to query usage statistics programmatically.

```bash
cargo run -- mcp
```

## Source Files

- `src/mcp/mod.rs` - Module exports
- `src/mcp/server.rs` - Server implementation and tool handlers
- `src/mcp/types.rs` - Request/response types

## Available Tools

- `get_daily_stats` - Query usage statistics with date filtering
- `get_model_usage` - Analyze model usage distribution
- `get_cost_breakdown` - Get cost breakdown over a date range
- `get_file_operations` - Get file operation statistics
- `compare_tools` - Compare usage across different AI coding tools
- `list_analyzers` - List available analyzers

## Resources

- `splitrail://summary` - Daily summaries across all dates
- `splitrail://models` - Model usage breakdown

## Adding a New Tool

1. Define the tool handler in `src/mcp/server.rs` using the `#[tool]` macro
2. Add request/response types to `src/mcp/types.rs` if needed

See existing tools in `src/mcp/server.rs` for the pattern.

## Adding a New Resource

1. Add URI constant to `resource_uris` module in `src/mcp/server.rs`
2. Add to `list_resources()` method
3. Handle in `read_resource()` method
