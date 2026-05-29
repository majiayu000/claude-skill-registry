---
name: agentuity-cli-auth-org-unselect
description: Clear the default organization preference. Use for managing authentication credentials
version: "0.1.24"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity auth org unselect"
  tags: "fast"
---

# Auth Org Unselect

Clear the default organization preference

## Usage

```bash
agentuity auth org unselect
```

## Examples

Clear default organization:

```bash
bunx @agentuity/cli auth org unselect
```

## Output

Returns JSON object:

```json
{
  "cleared": "boolean"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `cleared` | boolean | Whether the preference was cleared |
