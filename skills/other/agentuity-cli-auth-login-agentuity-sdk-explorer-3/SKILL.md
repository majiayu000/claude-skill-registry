---
name: agentuity-cli-auth-login
description: "Login to the Agentuity Platform using a browser-based authentication flow. Use for managing authentication credentials"
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity auth login"
  tags: "mutating creates-resource slow api-intensive"
---

# Auth Login

Login to the Agentuity Platform using a browser-based authentication flow

## Usage

```bash
agentuity auth login
```

## Examples

Login to account:

```bash
bunx @agentuity/cli auth login
```

Login to account:

```bash
bunx @agentuity/cli login
```
