---
name: agentuity-cli-build
description: Build Agentuity application for deployment
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity build"
  tags: "read-only slow requires-project"
---

# Build

Build Agentuity application for deployment

## Usage

```bash
agentuity build
```

## Examples

Build the project:

```bash
bunx @agentuity/cli build
```

Run in development mode:

```bash
bunx @agentuity/cli build --dev
```

Bundle the project:

```bash
bunx @agentuity/cli bundle
```
