---
name: agentuity-cli-cloud-vector-search
description: Search for vectors using semantic similarity. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.104"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<namespace> <query>"
metadata:
  command: "agentuity cloud vector search"
  tags: "read-only slow requires-auth"
---

# Cloud Vector Search

Search for vectors using semantic similarity

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud vector search <namespace> <query> [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<namespace>` | string | Yes | - |
| `<query>` | string | Yes | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--limit` | number | Yes | - | maximum number of results to return (default: 10) |
| `--similarity` | number | Yes | - | minimum similarity threshold (0.0-1.0) |
| `--metadata` | string | Yes | - | filter by metadata (format: key=value or key1=value1,key2=value2) |

## Examples

Search for similar products:

```bash
bunx @agentuity/cli vector search products "comfortable office chair"
```

Search knowledge base:

```bash
bunx @agentuity/cli vector list knowledge-base "machine learning"
```

Limit results:

```bash
bunx @agentuity/cli vector search docs "API documentation" --limit 5
```

Set minimum similarity:

```bash
bunx @agentuity/cli vector search products "ergonomic" --similarity 0.8
```

Filter by metadata:

```bash
bunx @agentuity/cli vector ls embeddings "neural networks" --metadata category=ai
```

## Output

Returns JSON object:

```json
{
  "namespace": "string",
  "query": "string",
  "results": "array",
  "count": "number"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `namespace` | string | Namespace name |
| `query` | string | Search query used |
| `results` | array | Search results |
| `count` | number | Number of results found |
