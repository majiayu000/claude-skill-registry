---
name: agentuity-cli-cloud-storage-get
description: Show details about a specific storage bucket. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.104"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<name>"
metadata:
  command: "agentuity cloud storage get"
  tags: "read-only fast requires-auth"
---

# Cloud Storage Get

Show details about a specific storage bucket

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud storage get <name> [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<name>` | string | Yes | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--showCredentials` | boolean | Yes | - | Show credentials in plain text (default: masked in terminal, unmasked in JSON) |

## Examples

Get bucket details:

```bash
bunx @agentuity/cli cloud storage get my-bucket
```

Show bucket information:

```bash
bunx @agentuity/cli cloud storage show my-bucket
```

Get bucket with credentials:

```bash
bunx @agentuity/cli cloud storage get my-bucket --show-credentials
```

## Output

Returns JSON object:

```json
{
  "bucket_name": "string",
  "access_key": "string",
  "secret_key": "string",
  "region": "string",
  "endpoint": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `bucket_name` | string | Storage bucket name |
| `access_key` | string | S3 access key |
| `secret_key` | string | S3 secret key |
| `region` | string | S3 region |
| `endpoint` | string | S3 endpoint URL |
