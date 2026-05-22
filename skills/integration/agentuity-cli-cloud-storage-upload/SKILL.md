---
name: agentuity-cli-cloud-storage-upload
description: Upload a file to storage bucket. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.110"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<name> <filename>"
metadata:
  command: "agentuity cloud storage upload"
  tags: "write requires-auth"
---

# Cloud Storage Upload

Upload a file to storage bucket

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud storage upload <name> <filename> [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<name>` | string | Yes | - |
| `<filename>` | string | Yes | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--key` | string | Yes | - | Remote object key (defaults to basename or "stdin" for piped uploads) |
| `--contentType` | string | Yes | - | Content type (auto-detected if not provided) |

## Examples

Upload file to bucket:

```bash
bunx @agentuity/cli cloud storage upload my-bucket file.txt
```

Upload file with content type:

```bash
bunx @agentuity/cli cloud storage put my-bucket file.txt --content-type text/plain
```

Upload file with custom object key:

```bash
bunx @agentuity/cli cloud storage upload my-bucket file.txt --key custom-name.txt
```

Upload from stdin:

```bash
cat file.txt | bunx @agentuity/cli cloud storage upload my-bucket -
```

Upload from stdin with custom key:

```bash
cat data.json | bunx @agentuity/cli cloud storage upload my-bucket - --key data.json
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "bucket": "string",
  "filename": "string",
  "size": "number"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether upload succeeded |
| `bucket` | string | Bucket name |
| `filename` | string | Uploaded filename |
| `size` | number | File size in bytes |
