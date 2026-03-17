---
name: agentuity-cli-auth-logout
description: Logout of the Agentuity Cloud Platform. Use for managing authentication credentials
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity auth logout"
  tags: "mutating deletes-resource fast requires-auth"
---

# Auth Logout

Logout of the Agentuity Cloud Platform

## Usage

```bash
agentuity auth logout
```

## Examples

Logout from account:

```bash
bunx @agentuity/cli auth logout
```

Logout from account:

```bash
bunx @agentuity/cli logout
```
