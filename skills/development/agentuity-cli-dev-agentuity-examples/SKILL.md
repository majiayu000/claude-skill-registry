---
name: agentuity-cli-dev
description: Build and run the development server
version: "0.0.103"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity dev"
  tags: "mutating slow requires-project"
---

# Dev

Build and run the development server

## Usage

```bash
agentuity dev
```

## Examples

Start development server:

```bash
bunx @agentuity/cli dev
```

Specify custom port:

```bash
bunx @agentuity/cli dev --port 8080
```

Run in local mode:

```bash
bunx @agentuity/cli dev --local
```

Disable public URL:

```bash
bunx @agentuity/cli dev --no-public
```
