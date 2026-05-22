---
name: docker-watch-mode-2025
description: Docker Compose Watch mode for automatic hot reload during local development with sync, rebuild, and restart actions
---

# Docker Compose Watch Mode (2025 GA)

Docker Compose Watch enables automatic hot reload during local development by synchronizing file changes instantly without manual container restarts.

## Three Watch Actions

### 1. sync - Hot Reload
For frameworks with hot reload (React, Next.js, Node.js, Flask).
Copies changed files directly into running container.

### 2. rebuild - Compilation
For compiled languages (Go, Rust, Java) or dependency changes.
Rebuilds image and recreates container when files change.

### 3. sync+restart - Config Changes
For configuration files requiring restart.
Syncs files and restarts container.

## Usage

```yaml
services:
  frontend:
    build: ./frontend
    develop:
      watch:
        - action: sync
          path: ./frontend/src
          target: /app/src
          ignore: [node_modules/, .git/]
        - action: rebuild
          path: ./frontend/package.json
```

Start with: `docker compose up --watch`

## Benefits
- Better performance than bind mounts
- No file permission issues
- Intelligent syncing
- Supports rebuild capability
- Works on all platforms
