---
name: agentuity-cli-auth-org-current
description: Show the current default organization. Use for managing authentication credentials
version: "0.1.24"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity auth org current"
  tags: "read-only fast"
---

# Auth Org Current

Show the current default organization

## Usage

```bash
agentuity auth org current
```

## Examples

Show default organization:

```bash
bunx @agentuity/cli auth org current
```

Show output in JSON format:

```bash
bunx @agentuity/cli auth org current --json
```
