---
name: mcp-exa-search
description: Search the web, research companies, and find code context using Exa AI. Use when performing web searches, company research, or finding programming documentation. Triggers on "search the web", "find online", "research company", "code context for [library]", "Exa search".
---

# Exa AI Search

MCP service at `https://mcp.exa.ai/mcp` (http) with 3 tools.

## Requirements

- `mh` CLI must be installed. If not available, install with:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/vaayne/mcphub/main/scripts/install.sh | sh
  ```

## Usage

List tools: `mh -u https://mcp.exa.ai/mcp -t http list`
Get tool details: `mh -u https://mcp.exa.ai/mcp -t http inspect <tool-name>`
Invoke tool: `mh -u https://mcp.exa.ai/mcp -t http invoke <tool-name> '{"param": "value"}'`

## Notes

- Run `inspect` before invoking unfamiliar tools to get full parameter schema
- Timeout: 30s default, use `--timeout <seconds>` to adjust
- `getCodeContextExa` is best for programming-related queries (libraries, SDKs, APIs)

## Tools

| Tool                 | Description                                                                                                                              |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `webSearchExa`       | Search the web using Exa AI with real-time results. Supports configurable result counts and returns content from most relevant websites. |
| `companyResearchExa` | Research companies - finds comprehensive info about businesses, operations, news, financials, and industry analysis.                     |
| `getCodeContextExa`  | Search and get relevant context for programming tasks. Best for libraries, SDKs, and API documentation with high quality, fresh context. |

## Examples

```bash
# Web search
mh -u https://mcp.exa.ai/mcp -t http invoke webSearchExa '{"query": "latest AI developments 2024"}'

# Company research
mh -u https://mcp.exa.ai/mcp -t http invoke companyResearchExa '{"company": "OpenAI"}'

# Code context
mh -u https://mcp.exa.ai/mcp -t http invoke getCodeContextExa '{"query": "React hooks best practices"}'
```
