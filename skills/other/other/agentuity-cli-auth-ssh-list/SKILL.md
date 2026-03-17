---
name: agentuity-cli-auth-ssh-list
description: List all SSH keys on your account. Requires authentication. Use for managing authentication credentials
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity auth ssh list"
  tags: "read-only fast requires-auth"
---

# Auth Ssh List

List all SSH keys on your account

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity auth ssh list
```

## Examples

List items:

```bash
bunx @agentuity/cli auth ssh list
```

List items:

```bash
bunx @agentuity/cli auth ssh ls
```

Show output in JSON format:

```bash
bunx @agentuity/cli --json auth ssh list
```

## Output

Returns: `array`
