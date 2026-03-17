---
name: agentuity-cli-cloud-storage-create
description: Create a new storage resource. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.104"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud storage create"
  tags: "mutating creates-resource slow requires-auth requires-deployment"
---

# Cloud Storage Create

Create a new storage resource

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud storage create
```

## Examples

Create a new cloud storage bucket:

```bash
bunx @agentuity/cli cloud storage create
```

Alias for "cloud storage create" (shorthand "new"):

```bash
bunx @agentuity/cli cloud storage new
```

Dry-run: display what would be created without making changes:

```bash
bunx @agentuity/cli --dry-run cloud storage create
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "name": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether creation succeeded |
| `name` | string | Created storage bucket name |
