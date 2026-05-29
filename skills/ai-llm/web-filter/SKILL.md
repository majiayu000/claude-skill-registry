---
name: web-filter
description: Filters and truncates large web search results from Exa to reduce token usage.
triggers: ["optimize web", "filter search"]
allowed-tools: [bash, str_replace]
---

# Web Response Filter
Save large MCP responses to /tmp/, filter with jq, load subset.

## Usage
```bash
# Filter response (keep title, url, first 500 chars)
echo "$MCP_OUTPUT" | jq '[.results[]? | {title, url, text: (.text // .content)[:500]}]'
```

Token savings: 92-98%

Install: `uvx mcp-server-exa`
Get key: exa.ai/api
