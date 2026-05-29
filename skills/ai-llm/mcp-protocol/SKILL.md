# MCP Protocol Skill

> JSON-RPC 2.0 protocol reference for MCP.

---

## Request Format

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search_nodes",
    "arguments": {
      "query": "http"
    }
  }
}
```

## Response Format

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{
      "type": "text",
      "text": "{\"nodes\": [...]}"
    }]
  }
}
```

## Error Codes

| Code | Message |
|------|---------|
| -32700 | Parse error |
| -32600 | Invalid Request |
| -32601 | Method not found |
| -32602 | Invalid params |
| -32603 | Internal error |

## Methods

- `tools/list` — List available tools
- `tools/call` — Call a tool
- `resources/list` — List resources
- `prompts/list` — List prompts
