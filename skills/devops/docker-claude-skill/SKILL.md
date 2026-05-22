---
name: docker
description: Container-based development for isolated, reproducible environments. Use when running npm commands, installing packages, executing code, or managing project dependencies. Trigger phrases include "npm install", "run the build", "start the server", "install package", or any code execution request.
---

# Docker Development Skill

Execute all package installations and code execution inside Docker containers. This keeps the host machine clean and ensures consistent environments across projects.

---

## First-Time Setup (New Projects)

### Step 1: Answer Configuration Questions

Before setting up Docker for a new project, determine your requirements:

**Q1: Does your project use native Node.js modules?**

Native modules compile C/C++ code and have specific OS requirements.

| Module | Native? | Requires glibc? |
|--------|---------|-----------------|
| `better-sqlite3` | Yes | Yes |
| `onnxruntime-node` | Yes | Yes |
| `sharp` | Yes | Yes |
| `bcrypt` | Yes | Yes |
| `node-gyp` builds | Yes | Usually |
| Pure JS packages | No | No |

**Check your package.json:**
```bash
# Look for native module indicators
grep -E "node-gyp|prebuild|nan|napi" package.json package-lock.json 2>/dev/null | head -5
```

**Q2: What's your priority?**

| Priority | Recommended Base Image |
|----------|------------------------|
| Smallest image size | `node:20-alpine` (if no native modules) |
| Maximum compatibility | `node:20-slim` (Debian, has glibc) |
| Full tooling | `node:20` (full Debian) |

### Step 2: Create Project Configuration

Create `.claude/docker-config.json` in your project root:

```json
{
  "containerName": "my-project-dev-1",
  "baseImage": "node:20-slim",
  "port": 3000,
  "hasNativeModules": true,
  "devCommand": "npm run dev -- --host 0.0.0.0"
}
```

**Configuration Options:**

| Field | Description | Examples |
|-------|-------------|----------|
| `containerName` | Docker container name | `myapp-dev-1`, `api-dev-1` |
| `baseImage` | Base Docker image | `node:20-slim`, `node:20-alpine` |
| `port` | Dev server port | `3000`, `4321`, `5173` |
| `hasNativeModules` | Uses native modules? | `true`, `false` |
| `devCommand` | Command to start dev server | `npm run dev -- --host 0.0.0.0` |

### Step 3: Generate Docker Files

Based on your configuration, create these files:

#### If `hasNativeModules: true` (Recommended Default)

**Dockerfile:**
```dockerfile
FROM node:20-slim

WORKDIR /app

# Install build tools for native modules (Debian/glibc)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    make \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy package files for layer caching
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build if needed
RUN npm run build --if-present

# Default command
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

#### If `hasNativeModules: false` (Smaller Image)

**Dockerfile:**
```dockerfile
FROM node:20-alpine

WORKDIR /app

# Alpine uses apk, not apt-get
RUN apk add --no-cache python3 make g++ git

COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build --if-present

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

#### docker-compose.yml (Both)

```yaml
services:
  dev:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ${COMPOSE_PROJECT_NAME:-my-project}-dev-1
    ports:
      - "${DEV_PORT:-3000}:3000"
    volumes:
      - .:/app
      - node_modules:/app/node_modules
    environment:
      - NODE_ENV=development
    command: npm run dev -- --host 0.0.0.0
    profiles:
      - dev

volumes:
  node_modules:
```

### Step 4: Start Container

```bash
# Navigate to project root
cd /path/to/project

# Start the development container
docker compose --profile dev up -d

# Verify it's running
docker ps --filter "name=my-project"

# Install dependencies (first time)
docker exec my-project-dev-1 npm install
```

### Step 5: Verify Setup

Run this checklist:

```bash
# 1. Container running?
docker ps | grep my-project-dev-1

# 2. Can execute commands?
docker exec my-project-dev-1 node --version

# 3. Dependencies installed?
docker exec my-project-dev-1 npm list --depth=0

# 4. Dev server accessible?
curl -s http://localhost:3000 > /dev/null && echo "OK" || echo "Not responding"
```

---

## ENFORCEMENT RULES

### BLOCKED: Never Run on Host

**These commands are BLOCKED on the host machine:**

```
npm install, npm ci, npm run, npm test, npm exec
npx <anything>
yarn add, yarn install, yarn run
pnpm add, pnpm install, pnpm run
node <script>
tsx <script>
bun <script>
```

**Why?** Installing packages on the host:
- Pollutes the host machine with project-specific dependencies
- Creates version conflicts between projects
- Makes environments non-reproducible
- Can cause security issues with global packages

### REQUIRED: Use docker exec

**All Node.js commands MUST use this prefix:**

```bash
docker exec <container-name> <command>
```

**Note:** Use `docker exec` WITHOUT the `-it` flag in Claude Code:

```bash
# ✅ Correct (works in Claude Code)
docker exec my-project-dev-1 npm run build

# ❌ Wrong (fails with "not a TTY")
docker exec -it my-project-dev-1 npm run build
```

---

## Pre-Flight Check (MANDATORY)

**Before running ANY npm/node command, verify the container is running.**

```bash
docker ps --filter "name=<container-name>" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

**Expected output:**
```
NAMES                   STATUS          PORTS
my-project-dev-1        Up X minutes    0.0.0.0:3000->3000/tcp
```

**If container is NOT running:**
```bash
cd /path/to/project
docker compose --profile dev up -d
docker ps --filter "name=<container-name>"
```

**If container shows "Exited":**
```bash
docker logs <container-name> --tail 20
docker compose --profile dev down
docker compose --profile dev up -d
```

---

## Quick Reference

### Check Container Status

```bash
docker ps --filter "name=<container-name>"
docker logs <container-name> --tail 50
curl -s http://localhost:<port> > /dev/null && echo "Running" || echo "Not running"
```

### Start/Stop Containers

```bash
docker compose --profile dev up -d        # Start
docker compose --profile dev down         # Stop
docker compose --profile dev restart dev  # Restart
docker compose --profile dev up -d --build  # Rebuild
```

### Execute Commands Inside Container

```bash
docker exec <container> npm install <package>     # Install package
docker exec <container> npm install -D <package>  # Install dev dependency
docker exec <container> npm test                  # Run tests
docker exec <container> npm run typecheck         # Type checking
docker exec <container> npm run lint              # Linting
docker exec <container> npm run build             # Build
docker exec <container> /bin/sh                   # Shell (use -it for interactive)
```

---

## Native Module Troubleshooting

### Error: `ERR_DLOPEN_FAILED`

**Symptom:**
```
Error: Error loading shared library ld-linux-aarch64.so.1: No such file or directory
```

**Cause:** Using Alpine image with modules that require glibc.

**Fix:**
1. Update Dockerfile to use `node:20-slim`
2. Change `apk` commands to `apt-get`
3. Rebuild container:

```bash
docker compose --profile dev down
docker volume rm <project>_node_modules
docker compose --profile dev build --no-cache
docker compose --profile dev up -d
docker exec <container> npm install
```

### Error: `Module not found` after switching images

**Fix:** Rebuild native modules inside container:

```bash
docker exec <container> npm rebuild
```

### Decision Tree: Alpine vs Slim

```
Does package.json contain native modules?
│
├─ YES → Use node:20-slim (glibc)
│        └─ Examples: sharp, bcrypt, sqlite3, onnxruntime
│
├─ UNSURE → Use node:20-slim (safe default)
│
└─ NO (pure JS only) → Use node:20-alpine (smaller)
         └─ Examples: express, react, typescript, lodash
```

---

## When to Use docker exec

| Operation | Use docker exec? | Reason |
|-----------|------------------|--------|
| `npm install` | ✅ **Always** | Packages install in container only |
| `npm run dev` | ❌ No | Already running via docker-compose |
| `npm test` | ✅ Yes | Tests run in container environment |
| `npm run build` | ✅ Yes | Build happens in container |
| `git` commands | ❌ No | Git runs on host (manages files) |
| File editing | ❌ No | Volume mount syncs automatically |
| Database migrations | ✅ Yes | Uses container's Node environment |

---

## Container Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  HOST (macOS/Linux/Windows)                                 │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Docker Container (my-project-dev-1)                │   │
│  │                                                     │   │
│  │  Node 20 (Slim or Alpine)                           │   │
│  │  └── node_modules/ (container-only, NOT on host)    │   │
│  │  └── Dev server (port 3000)                         │   │
│  │                                                     │   │
│  │  Volume Mounts:                                     │   │
│  │  └── .:/app (source code sync)                      │   │
│  │  └── node_modules:/app/node_modules (persist deps)  │   │
│  └─────────────────────────────────────────────────────┘   │
│                         │                                   │
│                         ▼                                   │
│                   Port mapped                               │
│                         │                                   │
│                         ▼                                   │
│              http://localhost:<port>                        │
└─────────────────────────────────────────────────────────────┘
```

**Key Point:** `node_modules` exists ONLY in the container. The host machine stays clean.

---

## Volume Mount Behavior

```yaml
volumes:
  - .:/app                           # Source code (synced)
  - node_modules:/app/node_modules   # Dependencies (container-only)
```

**What this means:**
- Source code changes on host are immediately visible in container
- `node_modules/` lives in a named Docker volume, NOT on host filesystem
- Hot reload works automatically
- Host machine never has project dependencies installed

---

## Troubleshooting

### Container Not Running

```bash
docker ps -a --filter "name=<container-name>"
docker logs <container-name>
docker compose --profile dev up -d
```

### Port Already in Use

```bash
lsof -i :<port>
# Kill the process or change port in docker-compose.yml
```

### Module Not Found Errors

```bash
docker compose --profile dev down
docker compose --profile dev build --no-cache
docker compose --profile dev up -d
docker exec <container> npm install
```

### File Changes Not Reflecting

```bash
docker inspect <container-name> | grep -A 10 "Mounts"
docker compose --profile dev restart dev
```

### Wrong Architecture (M1/M2 Mac)

If you see platform warnings:

```yaml
# Add to docker-compose.yml service
platform: linux/amd64  # or linux/arm64
```

---

## Project Configuration Reference

### .claude/docker-config.json

```json
{
  "containerName": "my-project-dev-1",
  "baseImage": "node:20-slim",
  "port": 3000,
  "hasNativeModules": true,
  "devCommand": "npm run dev -- --host 0.0.0.0",
  "envFile": ".env",
  "additionalVolumes": [],
  "buildArgs": {}
}
```

### Environment Variables

Required env vars load from `.env` via docker-compose:

```yaml
env_file:
  - .env
```

For command-specific env vars:

```bash
docker exec -e MY_VAR=value <container-name> <command>
```

---

## Best Practices

1. **Always check container status** before running commands
2. **Use docker exec** for ALL npm/node operations
3. **Never install packages on host** - always in container
4. **Use node:20-slim by default** - switch to alpine only if no native modules
5. **Rebuild image** after changing `package.json` or `Dockerfile`
6. **Check logs** when something isn't working
7. **Use named volumes** for node_modules to persist between container restarts

---

## Integration with Claude Code

| Task | Action |
|------|--------|
| Install dependency | `docker exec <container> npm install <pkg>` |
| Run tests | `docker exec <container> npm test` |
| Check types | `docker exec <container> npm run typecheck` |
| Build project | `docker exec <container> npm run build` |
| Start dev server | Container already runs it via docker-compose |
| Edit files | Edit directly (volume mount syncs) |
| Git operations | Run on host (not in container) |

---

*Last updated: December 2025*
