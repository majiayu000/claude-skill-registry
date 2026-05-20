---
name: nx
description: >-
  Build and manage monorepos with Nx. Use when a user asks to set up a monorepo, manage multiple packages/apps, cache builds, run affected tests, or migrate from Lerna.
license: Apache-2.0
compatibility: 'Node.js, any framework'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: development
  tags:
    - nx
    - monorepo
    - build
    - cache
    - workspace
---

# Nx

## Overview
Nx is a build system for monorepos. It provides computation caching (local + remote), task orchestration, dependency graph, code generators, and affected commands. Works with React, Angular, Node.js, Next.js, and any language.

## Instructions

### Step 1: Create Workspace
```bash
npx create-nx-workspace@latest my-org --preset=ts
cd my-org
```

### Step 2: Add Projects
```bash
nx g @nx/react:app my-app
nx g @nx/js:lib shared-utils
nx g @nx/node:app api
```

### Step 3: Run Tasks
```bash
nx serve my-app
nx build api
nx test shared-utils
nx affected -t test         # only what changed
nx run-many -t build test   # everything
```

### Step 4: nx.json Configuration
```json
// nx.json — Workspace configuration
{
  "targetDefaults": {
    "build": { "dependsOn": ["^build"], "cache": true },
    "test": { "cache": true },
    "lint": { "cache": true }
  }
}
```

## Guidelines
- Nx caches task results — second run is instant if inputs haven't changed.
- Use nx affected in CI to only build/test what changed in a PR.
- Nx Cloud provides remote caching — share cache across team/CI.
- Nx works without plugins too — add it to any repo with npx nx init.
