---
name: nextjs-mcp
description: Next.js framework integration utilities and server components
allowed-tools: [Bash, Read, Glob]
---

# Next.js MCP Skill

## Overview

Next.js framework integration with App Router, Server Components, and API routes. 90%+ context savings.

## Tools (Progressive Disclosure)

### Route Analysis

| Tool             | Description           |
| ---------------- | --------------------- |
| list-routes      | List all app routes   |
| analyze-route    | Analyze route handler |
| check-middleware | Analyze middleware    |

### Component Analysis

| Tool              | Description                     |
| ----------------- | ------------------------------- |
| list-components   | List server/client components   |
| detect-use-client | Find 'use client' directives    |
| analyze-rsc       | Analyze React Server Components |

### Build & Deploy

| Tool  | Description          | Confirmation |
| ----- | -------------------- | ------------ |
| build | Run production build | Yes          |
| dev   | Start dev server     | No           |
| lint  | Run Next.js linting  | No           |

## Agent Integration

- **developer** (primary): Next.js development
- **react-component-developer** (secondary): Component work
