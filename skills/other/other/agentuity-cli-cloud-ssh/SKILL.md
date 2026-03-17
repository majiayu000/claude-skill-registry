---
name: agentuity-cli-cloud-ssh
description: SSH into a cloud project. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.103"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "[identifier] [command]"
metadata:
  command: "agentuity cloud ssh"
  tags: "read-only slow requires-auth requires-deployment"
---

# Cloud Ssh

SSH into a cloud project

## Prerequisites

- Authenticated with `agentuity auth login`
- cloud deploy

## Usage

```bash
agentuity cloud ssh [identifier] [command] [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<identifier>` | string | No | - |
| `<command>` | string | No | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--show` | boolean | Yes | - | Show the command and exit |

## Examples

SSH into current project:

```bash
bunx @agentuity/cli cloud ssh
```

SSH into specific project:

```bash
bunx @agentuity/cli cloud ssh proj_abc123xyz
```

SSH into specific deployment:

```bash
bunx @agentuity/cli cloud ssh deploy_abc123xyz
```

Run command and exit:

```bash
bunx @agentuity/cli cloud ssh 'ps aux'
```

Run command on specific project:

```bash
bunx @agentuity/cli cloud ssh proj_abc123xyz 'tail -f /var/log/app.log'
```

Show SSH command without executing:

```bash
bunx @agentuity/cli cloud ssh --show
```
