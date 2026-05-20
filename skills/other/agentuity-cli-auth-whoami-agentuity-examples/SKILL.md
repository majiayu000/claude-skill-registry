---
name: agentuity-cli-auth-whoami
description: Display information about the currently authenticated user. Requires authentication. Use for managing authentication credentials
version: "0.0.103"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity auth whoami"
  tags: "read-only fast requires-auth"
---

# Auth Whoami

Display information about the currently authenticated user

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity auth whoami
```

## Examples

Show current user:

```bash
bunx @agentuity/cli auth whoami
```

Show output in JSON format:

```bash
bunx @agentuity/cli --json auth whoami
```

## Output

Returns JSON object:

```json
{
  "userId": "string",
  "firstName": "string",
  "lastName": "string",
  "organizations": "array"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `userId` | string | Unique user identifier |
| `firstName` | string | User first name |
| `lastName` | string | User last name |
| `organizations` | array | Organizations the user belongs to |
