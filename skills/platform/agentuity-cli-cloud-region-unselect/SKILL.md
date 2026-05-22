---
name: agentuity-cli-cloud-region-unselect
description: Clear the default region preference. Use for Agentuity cloud platform operations
version: "0.1.24"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud region unselect"
  tags: "fast"
---

# Cloud Region Unselect

Clear the default region preference

## Usage

```bash
agentuity cloud region unselect
```

## Examples

Clear default region:

```bash
bunx @agentuity/cli cloud region unselect
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
