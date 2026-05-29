---
name: rover
description: >
  Guide for using Apollo Rover CLI to manage GraphQL schemas and federation. Use this skill when:
  (1) publishing or fetching subgraph/graph schemas,
  (2) composing supergraph schemas locally or via GraphOS,
  (3) running local supergraph development with rover dev,
  (4) validating schemas with check and lint commands,
  (5) configuring Rover authentication and environment.
license: MIT
compatibility: Node.js v18+, Linux/macOS/Windows
metadata:
  author: apollographql
  version: "1.0"
allowed-tools: Bash(rover:*) Bash(curl:*) Bash(npm:*) Bash(npx:*) Read Write Edit Glob Grep
---

# Apollo Rover CLI Guide

Rover is the official CLI for Apollo GraphOS. It helps you manage schemas, run composition locally, publish to GraphOS, and develop supergraphs on your local machine.

## Quick Start

### Step 1: Install

```bash
# macOS/Linux
curl -sSL https://rover.apollo.dev/nix/latest | sh

# npm (cross-platform)
npm install -g @apollo/rover

# Windows PowerShell
iwr 'https://rover.apollo.dev/win/latest' | iex
```

### Step 2: Authenticate

```bash
# Interactive authentication (opens browser)
rover config auth

# Or set environment variable
export APOLLO_KEY=your-api-key
```

### Step 3: Verify Installation

```bash
rover --version
rover config whoami
```

## Core Commands Overview

| Command | Description | Use Case |
|---------|-------------|----------|
| `rover subgraph publish` | Publish subgraph schema to GraphOS | CI/CD, schema updates |
| `rover subgraph check` | Validate schema changes | PR checks, pre-deploy |
| `rover subgraph fetch` | Download subgraph schema | Local development |
| `rover supergraph compose` | Compose supergraph locally | Local testing |
| `rover dev` | Local supergraph development | Development workflow |
| `rover graph publish` | Publish monograph schema | Non-federated graphs |

## Graph Reference Format

Most commands require a graph reference in the format:

```
<GRAPH_ID>@<VARIANT>
```

Examples:
- `my-graph@production`
- `my-graph@staging`
- `my-graph@current` (default variant)

Set as environment variable:
```bash
export APOLLO_GRAPH_REF=my-graph@production
```

## Subgraph Workflow

### Publishing a Subgraph

```bash
# From schema file
rover subgraph publish my-graph@production \
  --name products \
  --schema ./schema.graphql \
  --routing-url https://products.example.com/graphql

# From running server (introspection)
rover subgraph publish my-graph@production \
  --name products \
  --schema <(rover subgraph introspect http://localhost:4001/graphql) \
  --routing-url https://products.example.com/graphql
```

### Checking Schema Changes

```bash
# Check against production traffic
rover subgraph check my-graph@production \
  --name products \
  --schema ./schema.graphql
```

### Fetching Schema

```bash
# Fetch from GraphOS
rover subgraph fetch my-graph@production --name products

# Introspect running server
rover subgraph introspect http://localhost:4001/graphql
```

## Supergraph Composition

### Local Composition

Create `supergraph.yaml`:

```yaml
federation_version: =2.9.0
subgraphs:
  products:
    routing_url: http://localhost:4001/graphql
    schema:
      file: ./products/schema.graphql
  reviews:
    routing_url: http://localhost:4002/graphql
    schema:
      subgraph_url: http://localhost:4002/graphql
```

Compose:
```bash
rover supergraph compose --config supergraph.yaml > supergraph.graphql
```

### Fetch Composed Supergraph

```bash
rover supergraph fetch my-graph@production
```

## Local Development with `rover dev`

Start a local Router with automatic schema composition:

```bash
# Start with supergraph config
rover dev --supergraph-config supergraph.yaml

# Start with GraphOS variant as base
rover dev --graph-ref my-graph@staging --supergraph-config local.yaml
```

### With MCP Integration

```bash
# Start with MCP server enabled
rover dev --supergraph-config supergraph.yaml --mcp
```

## Reference Files

Detailed documentation for specific topics:

- [Subgraphs](references/subgraphs.md) - fetch, publish, check, lint, introspect, delete
- [Graphs](references/graphs.md) - monograph commands (non-federated)
- [Supergraphs](references/supergraphs.md) - compose, fetch, config format
- [Dev](references/dev.md) - rover dev for local development
- [Configuration](references/configuration.md) - install, auth, env vars, profiles

## Common Patterns

### CI/CD Pipeline

```bash
# 1. Check schema changes
rover subgraph check $APOLLO_GRAPH_REF \
  --name $SUBGRAPH_NAME \
  --schema ./schema.graphql

# 2. If check passes, publish
rover subgraph publish $APOLLO_GRAPH_REF \
  --name $SUBGRAPH_NAME \
  --schema ./schema.graphql \
  --routing-url $ROUTING_URL
```

### Schema Linting

```bash
# Lint against GraphOS rules
rover subgraph lint --name products ./schema.graphql

# Lint monograph
rover graph lint my-graph@production ./schema.graphql
```

### Output Formats

```bash
# JSON output for scripting
rover subgraph fetch my-graph@production --name products --format json

# Plain output (default)
rover subgraph fetch my-graph@production --name products --format plain
```

## Ground Rules

- ALWAYS authenticate before using GraphOS commands (`rover config auth` or `APOLLO_KEY`)
- ALWAYS use the correct graph reference format: `graph-id@variant`
- PREFER `rover subgraph check` before `rover subgraph publish` in CI/CD
- USE `rover dev` for local supergraph development instead of running Router manually
- NEVER commit `APOLLO_KEY` to version control; use environment variables
- USE `--format json` when parsing output programmatically
- SPECIFY `federation_version` explicitly in supergraph.yaml for reproducibility
- USE `rover subgraph introspect` to extract schemas from running services
