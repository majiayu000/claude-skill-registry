---
name: pagent
description: Guide for using pagent - a PRD-to-code orchestration tool. Use when users ask how to use pagent, run agents, create PRDs, or transform requirements into code.
---

# Pagent Usage Guide

Pagent orchestrates specialist AI agents to transform Product Requirement Documents (PRDs) into working code.

## Quick Start

```bash
# Interactive TUI (recommended)
pagent ui

# Run with a PRD file
pagent run ./prd.md

# Check agent status
pagent status
```

## Agents

Pagent runs 5 specialist agents in dependency order:

| Agent | Output | Purpose |
|-------|--------|---------|
| `architect` | `architecture.md` | Technical design, API specs, data models |
| `qa` | `test-plan.md` | Test cases, acceptance criteria |
| `security` | `security-assessment.md` | Threat model, security requirements |
| `implementer` | `code/*` | Working code implementation |
| `verifier` | `*_test.go`, `verification-report.md` | Tests and validation |

### Execution Order

```
Level 0: architect
Level 1: qa, security (parallel)
Level 2: implementer
Level 3: verifier
```

## Commands

### Run Agents

```bash
# Run all agents (parallel by default)
pagent run ./prd.md

# Run specific agents
pagent run ./prd.md --agents architect,qa

# Sequential mode
pagent run ./prd.md --sequential

# Resume (skip up-to-date outputs)
pagent run ./prd.md --resume

# Force regeneration
pagent run ./prd.md --force

# Custom output directory
pagent run ./prd.md -o ./docs/
```

### Interactive TUI

```bash
pagent ui              # Start fresh
pagent ui ./prd.md     # Pre-fill with PRD
pagent ui --accessible # Screen reader support
```

### Monitor & Control

```bash
pagent status                    # Check running agents
pagent logs <agent>              # View agent output
pagent message <agent> "text"    # Send guidance
pagent stop <agent>              # Stop specific agent
pagent stop --all                # Stop all agents
```

### MCP Server

```bash
pagent mcp                                  # Stdio (Claude Desktop)
pagent mcp --transport http --port 8080     # HTTP mode
pagent mcp --transport http --oauth \
  --issuer https://company.okta.com \
  --audience api://pagent                   # With OAuth
```

## Personas

Control implementation style:

| Persona | Use Case |
|---------|----------|
| `minimal` | MVP, prototype - ship fast |
| `balanced` | Standard projects (default) |
| `production` | Enterprise - comprehensive testing, security |

```bash
pagent run ./prd.md --persona production
```

## Configuration

Initialize config:
```bash
pagent init
```

Creates `.pagent/config.yaml`:
```yaml
output_dir: ./outputs
timeout: 300
persona: balanced

preferences:
  api_style: rest      # rest | graphql | grpc
  language: go         # go | python | typescript
  testing_depth: unit  # none | unit | integration | e2e
  containerized: true
  include_ci: true

stack:
  cloud: aws
  compute: kubernetes
  database: postgres
  cache: redis
```

## Writing a PRD

A good PRD includes:

```markdown
# Product: [Name]

## Problem Statement
What problem are we solving?

## Features
- Feature 1: description
- Feature 2: description

## Requirements
- Functional requirements
- Non-functional requirements (performance, security)

## Constraints
- Technology constraints
- Timeline constraints
```

## Workflows

### Quick Architecture Review
```bash
pagent run ./prd.md --agents architect
# Review architecture.md, iterate on PRD
```

### Full Pipeline
```bash
pagent ui ./prd.md
# Select production persona
# Run all agents
cd outputs/code && go build ./...
```

### Iterative Development
```bash
pagent run ./prd.md --agents architect
# Review architecture.md
pagent run ./prd.md --resume  # Run remaining agents
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Timeout | `pagent run ./prd.md --timeout 600` |
| Port in use | `pagent stop --all` |
| Incomplete output | `pagent message <agent> "Please complete..."` |
| Agent stuck | `pagent stop <agent>` then re-run |
