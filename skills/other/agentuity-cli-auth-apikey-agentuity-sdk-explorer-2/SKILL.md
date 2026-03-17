---
name: agentuity-cli-auth-apikey
description: Display the API key for the currently authenticated user. Requires authentication. Use for managing authentication credentials
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity auth apikey"
  tags: "read-only fast requires-auth"
---

# Auth Apikey

Display the API key for the currently authenticated user

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity auth apikey
```

## Examples

Print the API key:

```bash
bunx @agentuity/cli auth apikey
```

Output API key in JSON format:

```bash
bunx @agentuity/cli --json auth apikey
```

## Output

Returns JSON object:

```json
{
  "apiKey": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `apiKey` | string | The API key for the authenticated user |
