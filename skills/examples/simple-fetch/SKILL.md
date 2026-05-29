---
name: simple-fetch
description: Basic MCP skill demonstrating CLI-based execution pattern for fetching URL content
---

# Simple Fetch Skill

## When to Use This Skill

Use this Skill to:
- Learn the basic skill pattern
- Fetch content from a URL
- Use as a template for creating custom skills

This is a **demonstration skill** showing the minimal CLI-based pattern.

## What This Skill Does

Demonstrates the core skill pattern:
1. Accept CLI arguments (--url)
2. Call an MCP tool (fetch__fetch)
3. Return result

## Instructions

When you need to fetch content from a URL, execute:

```bash
cd /home/khitomer/Projects/mcp-code-execution-enhanced

uv run python -m runtime.harness scripts/simple_fetch.py \
    --url "https://example.com"
```

### Parameters

- `--url`: The URL to fetch (required)

### Example Usage

```bash
# Fetch a webpage
uv run python -m runtime.harness scripts/simple_fetch.py \
    --url "https://docs.example.com/api"

# Fetch documentation
uv run python -m runtime.harness scripts/simple_fetch.py \
    --url "https://github.com/owner/repo/README.md"
```

## Expected Output

The skill returns the fetched content and prints:
- Success message with byte count
- Or error message if fetch fails

## MCP Servers Required

Configure a fetch-capable MCP server in `mcp_config.json`:

```json
{
  "mcpServers": {
    "fetch": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    }
  }
}
```

## Technical Notes

- **Pattern**: CLI args → MCP call → Result
- **Token cost**: ~110 tokens (discover + read + execute)
- **Time**: <10 seconds
- **Immutable**: Parameters via CLI, no file editing needed

This skill demonstrates the foundation for creating more complex MCP workflows.
