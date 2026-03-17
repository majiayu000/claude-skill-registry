---
name: mcp-grep-code
description: Search real-world code examples from over a million public GitHub repositories. Use when finding code patterns, implementation examples, or how libraries are used in practice. Triggers on "find code examples", "how is [library] used", "search GitHub code", "grep.app search", "code pattern".
---

# Grep.app Code Search

MCP service at `https://mcp.grep.app` (http) with 1 tool.

## Requirements

- `mh` CLI must be installed. If not available, install with:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/vaayne/mcphub/main/scripts/install.sh | sh
  ```

## Usage

List tools: `mh -u https://mcp.grep.app -t http list`
Get tool details: `mh -u https://mcp.grep.app -t http inspect searchGitHub`
Invoke tool: `mh -u https://mcp.grep.app -t http invoke searchGitHub '{"query": "pattern"}'`

## Notes

- Run `inspect` before invoking unfamiliar tools to get full parameter schema
- Timeout: 30s default, use `--timeout <seconds>` to adjust
- **Important**: This searches for literal code patterns (like grep), NOT keywords
- Use actual code that would appear in files, not descriptions

## Tools

| Tool           | Description                                                                                                                 |
| -------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `searchGitHub` | Find real-world code examples from public GitHub repositories. Searches for literal code patterns across millions of repos. |

## Search Tips

**Good queries** (literal code patterns):

- `useState(`
- `import React from`
- `async function`
- `(?s)try {.*await`

**Bad queries** (keywords - won't work well):

- `react state management`
- `how to use hooks`

## Examples

```bash
# Find useState usage patterns
mh -u https://mcp.grep.app -t http invoke searchGitHub '{"query": "useState("}'

# Find async/await patterns
mh -u https://mcp.grep.app -t http invoke searchGitHub '{"query": "async function fetch"}'

# Find import patterns
mh -u https://mcp.grep.app -t http invoke searchGitHub '{"query": "from \"openai\""}'
```
