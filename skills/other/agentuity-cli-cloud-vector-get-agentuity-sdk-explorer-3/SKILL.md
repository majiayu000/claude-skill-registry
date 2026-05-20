---
name: agentuity-cli-cloud-vector-get
description: Get a specific vector entry by key. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<namespace> <key>"
metadata:
  command: "agentuity cloud vector get"
  tags: "read-only fast requires-auth"
---

# Cloud Vector Get

Get a specific vector entry by key

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud vector get <namespace> <key>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<namespace>` | string | Yes | - |
| `<key>` | string | Yes | - |

## Examples

Get a specific product vector:

```bash
bunx @agentuity/cli vector get products chair-001
```

Get a document from knowledge base:

```bash
bunx @agentuity/cli vector get knowledge-base doc-123
```

Get user profile embedding:

```bash
bunx @agentuity/cli vector get embeddings user-profile-456
```

## Output

Returns JSON object:

```json
{
  "exists": "boolean",
  "key": "string",
  "id": "string",
  "metadata": "object",
  "document": "string",
  "similarity": "number"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `exists` | boolean | Whether the vector exists |
| `key` | string | Vector key |
| `id` | string | Vector ID |
| `metadata` | object | Vector metadata |
| `document` | string | Original document text |
| `similarity` | number | Similarity score |
