---
name: commerce-mcp-tools
description: Reference for StateSet MCP tool names, parameters, and example payloads. Use when composing or debugging `mcp__stateset-commerce__` tool calls or reviewing MCP schemas.
---

# Commerce MCP Tools

Reference map for StateSet MCP tools, grouped by domain with example payloads.

## How It Works

1. Find the tool by domain (orders, inventory, returns, etc).
2. Use the parameter list and example payload.
3. Cross-check with the source definitions if needed.

## Usage

Use this skill when you need to:
- Construct MCP tool calls.
- Verify parameter names and shapes.
- Debug tool failures.

## Output

```json
{"tool":"create_order","params":{"customerId":"<uuid>","items":[{"sku":"SKU-001","name":"Widget","quantity":1,"unitPrice":29.99}]}}
```

## Present Results to User

- Tool name and parameter payload.
- Any required vs optional fields.
- Source file for the tool definition.

## Troubleshooting

- Tool not found: verify the MCP server is running.
- Param mismatch: compare against the reference map and source file.

## References

- references/mcp-tools-map.md
- /home/dom/stateset-icommerce/cli/src/mcp-server.js
- /home/dom/stateset-icommerce/cli/src/autonomous/mcp-tools.js
