---
name: agentuity-cli-cloud-storage-download
description: Download a file from storage bucket. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<name> <filename> [output]"
metadata:
  command: "agentuity cloud storage download"
  tags: "read-only requires-auth"
---

# Cloud Storage Download

Download a file from storage bucket

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud storage download <name> <filename> [output] [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<name>` | string | Yes | - |
| `<filename>` | string | Yes | - |
| `<output>` | string | No | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--metadata` | boolean | Yes | - | Download metadata only (not file contents) |

## Examples

Download file from bucket:

```bash
bunx @agentuity/cli cloud storage download my-bucket file.txt
```

Download file to specific path:

```bash
bunx @agentuity/cli cloud storage download my-bucket file.txt output.txt
```

Download file to stdout:

```bash
bunx @agentuity/cli cloud storage download my-bucket file.txt - > output.txt
```

Download metadata only:

```bash
bunx @agentuity/cli cloud storage download my-bucket file.txt --metadata
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "bucket": "string",
  "filename": "string",
  "size": "number",
  "contentType": "string",
  "lastModified": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether download succeeded |
| `bucket` | string | Bucket name |
| `filename` | string | Downloaded filename |
| `size` | number | File size in bytes |
| `contentType` | string | Content type |
| `lastModified` | string | Last modified timestamp |
