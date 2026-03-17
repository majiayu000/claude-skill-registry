---
name: mcp-context7-docs
description: Query up-to-date documentation and code examples for any programming library or framework. Use when looking up API docs, finding code examples, or checking library usage. Triggers on "how to use [library]", "docs for [package]", "show me examples of [framework]", "Context7 lookup".
---

# Context7 Documentation

MCP service at `https://mcp.context7.com/mcp` (http) with 2 tools.

## Requirements

- `mh` CLI must be installed. If not available, install with:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/vaayne/mcphub/main/scripts/install.sh | sh
  ```

## Usage

List tools: `mh -u https://mcp.context7.com/mcp -t http list`
Get tool details: `mh -u https://mcp.context7.com/mcp -t http inspect <tool-name>`
Invoke tool: `mh -u https://mcp.context7.com/mcp -t http invoke <tool-name> '{"param": "value"}'`

## Notes

- Run `inspect` before invoking unfamiliar tools to get full parameter schema
- Timeout: 30s default, use `--timeout <seconds>` to adjust
- **Important**: Always call `resolveLibraryId` first to get the Context7-compatible library ID before calling `queryDocs`, unless user provides ID in `/org/project` format

## Tools

| Tool               | Description                                                                                                                                                                                          |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `queryDocs`        | Retrieves and queries up-to-date documentation and code examples from Context7 for any programming library or framework. Requires a Context7-compatible library ID obtained from `resolveLibraryId`. |
| `resolveLibraryId` | Resolves a package/product name to a Context7-compatible library ID. Must be called before `queryDocs` to get a valid library ID.                                                                    |

## Workflow

1. **Resolve library ID**: First, resolve the library name to a Context7 ID
   ```bash
   mh -u https://mcp.context7.com/mcp -t http invoke resolveLibraryId '{"libraryName": "react"}'
   ```

2. **Query documentation**: Use the resolved ID to fetch docs
   ```bash
   mh -u https://mcp.context7.com/mcp -t http invoke queryDocs '{"context7CompatibleLibraryID": "/facebook/react", "topic": "hooks"}'
   ```
