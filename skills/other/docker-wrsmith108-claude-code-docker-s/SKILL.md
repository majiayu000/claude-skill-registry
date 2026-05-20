---
name: docker
description: Container-based development for isolated, reproducible environments. Use when running npm commands, installing packages, executing code, or managing project dependencies. Trigger phrases include "npm install", "run the build", "start the server", "install package", or any code execution request.
---

# Docker Development Skill

Execute all package installations and code execution inside Docker containers. This keeps the host machine clean and ensures consistent environments across projects.

## Core Principle

**NEVER run `npm`, `node`, `npx`, or project scripts directly on the host machine.**

Instead, use `docker exec` or ensure the container is running the dev server.

## Pre-Flight Check (MANDATORY)

**Before running ANY npm/node command, Claude Code MUST verify the container is running.**

Run this check first:

```bash
docker ps --filter "name=<project-name>" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

**Expected output:**
```
NAMES                  STATUS          PORTS
<project-name>-dev-1   Up X minutes    0.0.0.0:3000->3000/tcp
```

**If container is NOT running:**
```bash
# Navigate to project root first
cd /path/to/your/project

# Start container
docker-compose --profile dev up dev -d

# Verify it started
docker ps --filter "name=<project-name>"
```

**If container shows "Exited":**
```bash
# Check why it exited
docker logs <project-name>-dev-1 --tail 20

# Remove and restart
docker-compose --profile dev down
docker-compose --profile dev up dev -d
```

## Quick Reference

### Check Container Status

```bash
# List running containers for current project
docker ps --filter "name=<project-name>"

# Check container logs
docker logs <project-name>-dev-1 --tail 50

# Check if dev server is responding
curl -s http://localhost:3000 > /dev/null && echo "Server running" || echo "Server not running"
```

### Start/Stop Containers

```bash
# Start development container (from project root)
docker-compose --profile dev up dev -d

# Stop container
docker-compose --profile dev down

# Restart container
docker-compose --profile dev restart dev

# Rebuild after Dockerfile changes
docker-compose --profile dev up dev -d --build
```

### Execute Commands Inside Container

```bash
# Install a package
docker exec -it <project-name>-dev-1 npm install <package-name>

# Install dev dependency
docker exec -it <project-name>-dev-1 npm install -D <package-name>

# Run tests
docker exec -it <project-name>-dev-1 npm test

# Run type checking
docker exec -it <project-name>-dev-1 npm run typecheck

# Run linting
docker exec -it <project-name>-dev-1 npm run lint

# Run build
docker exec -it <project-name>-dev-1 npm run build

# Open shell inside container
docker exec -it <project-name>-dev-1 /bin/sh

# Run any arbitrary command
docker exec -it <project-name>-dev-1 <command>
```

## When to Use Docker exec

| Operation | Use docker exec? | Reason |
|-----------|------------------|--------|
| `npm install` | ✅ Yes | Packages install in container |
| `npm run dev` | ❌ No | Already running via docker-compose |
| `npm test` | ✅ Yes | Tests run in container environment |
| `npm run build` | ✅ Yes | Build happens in container |
| `git` commands | ❌ No | Git runs on host (manages files) |
| File editing | ❌ No | Volume mount syncs automatically |
| Database migrations | ✅ Yes | Uses container's Node environment |

## Container Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  HOST (macOS/Linux/Windows)                                 │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Docker Container (<project-name>-dev-1)            │   │
│  │                                                     │   │
│  │  Node 20 Alpine                                     │   │
│  │  └── node_modules/ (container-only)                 │   │
│  │  └── Dev server (port 3000)                         │   │
│  │                                                     │   │
│  │  Volume Mounts:                                     │   │
│  │  └── .:/app (source code sync)                      │   │
│  │  └── node_modules:/app/node_modules (persist deps)  │   │
│  └─────────────────────────────────────────────────────┘   │
│                         │                                   │
│                         ▼                                   │
│                   Port 3000 mapped                          │
│                         │                                   │
│                         ▼                                   │
│              http://localhost:3000                          │
└─────────────────────────────────────────────────────────────┘
```

## Volume Mount Behavior

The `docker-compose.yml` mounts the project directory into the container:

```yaml
volumes:
  - .:/app                           # Source code (synced)
  - /app/node_modules                # Dependencies (container-only)
```

**What this means:**
- Source code changes on host are immediately visible in container
- `node_modules/` in container is separate from any on host
- Hot reload works automatically with most frameworks

## Troubleshooting

### Container Not Running

```bash
# Check if container exists
docker ps -a --filter "name=<project-name>"

# If exited, check why
docker logs <project-name>-dev-1

# Restart
docker-compose --profile dev up dev -d
```

### Port Already in Use

```bash
# Find what's using the port
lsof -i :3000

# Kill the process or change port in docker-compose.yml
```

### Module Not Found Errors

```bash
# Rebuild container with fresh dependencies
docker-compose --profile dev down
docker-compose --profile dev build --no-cache dev
docker-compose --profile dev up dev -d
```

### File Changes Not Reflecting

```bash
# Check volume mounts
docker inspect <project-name>-dev-1 | grep -A 10 "Mounts"

# Restart container
docker-compose --profile dev restart dev
```

## Project Configuration

After installing this skill, update the placeholders for your project:

| Setting | Example Value |
|---------|---------------|
| Container name | `my-app-dev-1` |
| Port | 3000 (or your app's port) |
| Node version | 20 (Alpine) |
| Dev command | `npm run dev -- --host 0.0.0.0` |

### Environment Variables

Required env vars are loaded from `.env` file via docker-compose.

If a command needs a specific env var:
```bash
docker exec -it -e MY_VAR=value <project-name>-dev-1 <command>
```

## Best Practices

1. **Always check container status** before running commands
2. **Use `docker exec`** for all npm/node operations
3. **Let volume mounts** handle file syncing (no manual copying)
4. **Rebuild image** after changing `package.json` or `Dockerfile`
5. **Check logs** if something isn't working

## Integration with Claude Code

When Claude Code needs to:

| Task | Action |
|------|--------|
| Install dependency | `docker exec -it <project-name>-dev-1 npm install <pkg>` |
| Run tests | `docker exec -it <project-name>-dev-1 npm test` |
| Check types | `docker exec -it <project-name>-dev-1 npm run typecheck` |
| Build project | `docker exec -it <project-name>-dev-1 npm run build` |
| Start dev server | Container already runs it via docker-compose |
| Edit files | Edit directly (volume mount syncs) |
| Git operations | Run on host (not in container) |

## Sample docker-compose.yml

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    env_file:
      - .env
    restart: unless-stopped

  dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    env_file:
      - .env
    profiles:
      - dev
```

## Sample Dockerfile.dev

```dockerfile
FROM node:20-alpine

WORKDIR /app

# Install dependencies for native modules
RUN apk add --no-cache python3 make g++

# Copy package files and any scripts needed for postinstall
COPY package*.json ./
COPY scripts/ ./scripts/

# Install all dependencies
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=3000
ENV NODE_ENV=development

# Start development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```
