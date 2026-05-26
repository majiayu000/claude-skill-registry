---
name: agentuity-cli-profile-show
description: Show the configuration of a profile
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "[name]"
metadata:
  command: "agentuity profile show"
  tags: "read-only fast"
---

# Profile Show

Show the configuration of a profile

## Usage

```bash
agentuity profile show [name]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<name>` | string | No | - |

## Examples

Show details:

```bash
bunx @agentuity/cli profile show
```

Show details:

```bash
bunx @agentuity/cli profile show production
```

Show output in JSON format:

```bash
bunx @agentuity/cli profile show staging --json
```

## Output

Returns JSON object:

```json
{
  "name": "string",
  "auth": "object",
  "devmode": "object",
  "overrides": "unknown",
  "preferences": "object",
  "gravity": "object"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Profile name |
| `auth` | object | Authentication credentials (managed by login/logout commands) |
| `devmode` | object | Development mode configuration |
| `overrides` | unknown | URL and behavior overrides |
| `preferences` | object | User preferences |
| `gravity` | object | the gravity client information |
