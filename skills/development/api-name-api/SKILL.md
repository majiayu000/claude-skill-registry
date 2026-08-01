---
name: api-name-api
description: Interact with the {{API_NAME}} API. Use when {{TRIGGER_CONTEXTS}}. Supports
  {{CAPABILITIES}}.
---

---
name: {{API_NAME}}-api
description: Interact with the {{API_NAME}} API. Use when {{TRIGGER_CONTEXTS}}. Supports {{CAPABILITIES}}.
---

# {{API_NAME}} API

## Setup

Set your API key:

```bash
export {{API_NAME_UPPER}}_API_KEY="your-key-here"
```

## Available Operations

### {{OPERATION_1}}

{{Description of operation}}

```bash
bun run scripts/client.ts {{operation_1}} --param value
```

### {{OPERATION_2}}

{{Description of operation}}

```bash
bun run scripts/client.ts {{operation_2}} --param value
```

## Common Workflows

### Workflow 1: {{WORKFLOW_NAME}}

1. First, {{step 1}}
2. Then, {{step 2}}
3. Finally, {{step 3}}

## Error Handling

| Error | Meaning | Resolution |
|-------|---------|------------|
| 401 | Invalid API key | Check {{API_NAME_UPPER}}_API_KEY is set correctly |
| 429 | Rate limited | Wait and retry, or reduce request frequency |
| 500 | Server error | Retry after a moment |

## Requirements

- Bun runtime
- {{API_NAME_UPPER}}_API_KEY environment variable

## Tips

- Use `--verbose` flag for detailed output
- Results are returned as JSON for easy parsing
- Paginated endpoints support `--limit` and `--offset`
