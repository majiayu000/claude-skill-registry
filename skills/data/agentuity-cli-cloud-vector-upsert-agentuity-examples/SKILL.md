---
name: agentuity-cli-cloud-vector-upsert
description: Add or update vectors in the vector storage. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.104"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<namespace> [key]"
metadata:
  command: "agentuity cloud vector upsert"
  tags: "mutating updates-resource slow requires-auth"
---

# Cloud Vector Upsert

Add or update vectors in the vector storage

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud vector upsert <namespace> [key] [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<namespace>` | string | Yes | - |
| `<key>` | string | No | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--document` | string | Yes | - | document text to embed |
| `--embeddings` | string | Yes | - | pre-computed embeddings as JSON array |
| `--metadata` | string | Yes | - | metadata as JSON object |
| `--file` | string | Yes | - | path to JSON file containing vectors, or "-" for stdin |

## Examples

Upsert a single vector with document text:

```bash
bunx @agentuity/cli vector upsert products doc1 --document "Comfortable office chair"
```

Upsert with metadata:

```bash
bunx @agentuity/cli vector upsert products doc1 --document "Chair" --metadata '{"category":"furniture"}'
```

Upsert with pre-computed embeddings:

```bash
bunx @agentuity/cli vector upsert embeddings vec1 --embeddings "[0.1, 0.2, 0.3]"
```

Bulk upsert from JSON file:

```bash
bunx @agentuity/cli vector upsert products --file vectors.json
```

Bulk upsert from stdin:

```bash
cat vectors.json | bunx @agentuity/cli vector upsert products -
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "namespace": "string",
  "count": "number",
  "results": "array",
  "durationMs": "number"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `namespace` | string | Namespace name |
| `count` | number | Number of vectors upserted |
| `results` | array | Upsert results with key-to-id mappings |
| `durationMs` | number | Operation duration in milliseconds |
