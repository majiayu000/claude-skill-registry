---
name: agentuity-cli-upgrade
description: Upgrade the CLI to the latest version
version: "0.0.105"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity upgrade"
  tags: "update"
---

# Upgrade

Upgrade the CLI to the latest version

## Usage

```bash
agentuity upgrade
```

## Examples

Check for updates and prompt to upgrade:

```bash
agentuity upgrade
```

Force upgrade even if already on latest version:

```bash
agentuity upgrade --force
```
