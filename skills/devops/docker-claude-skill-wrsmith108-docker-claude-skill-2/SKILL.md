---
name: docker
version: 1.1.0
description: Container-based development for isolated, reproducible environments. Use when running npm commands, installing packages, executing code, or managing project dependencies. Trigger phrases include "npm install", "run the build", "start the server", "install package", or any code execution request.
---

# Docker Development Skill

Execute all package installations and code execution inside Docker containers. This keeps the host machine clean and ensures consistent environments across projects.

---

## Behavioral Classification

**Type**: Autonomous Execution

**Directive**: EXECUTE, DON'T ASK

This skill enforces Docker-first development automatically. When you request npm/node operations, commands are executed inside Docker without asking for permission.

**Enforcement Behavior**:
- Blocks host-machine npm/node commands
- Suggests or transforms commands to use `docker exec`
- Automatically checks container status before operations

---

## Quick Start

For new projects, see **[setup.md](setup.md)** for the complete first-time setup guide.

**Minimal setup**:

```bash
# 1. Start container
docker compose --profile dev up -d

# 2. Verify running
docker ps --filter "name=my-project"

# 3. Run commands in container
docker exec my-project-dev-1 npm install
docker exec my-project-dev-1 npm test
docker exec my-project-dev-1 npm run build
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
# Correct (works in Claude Code)
docker exec my-project-dev-1 npm run build

# Wrong (fails with "not a TTY")
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

## When to Use docker exec

| Operation | Use docker exec? | Reason |
|-----------|------------------|--------|
| `npm install` | **Always** | Packages install in container only |
| `npm run dev` | No | Already running via docker-compose |
| `npm test` | Yes | Tests run in container environment |
| `npm run build` | Yes | Build happens in container |
| `git` commands | No | Git runs on host (manages files) |
| File editing | No | Volume mount syncs automatically |
| Database migrations | Yes | Uses container's Node environment |

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

### Native Module Errors

See **[setup.md](setup.md)** for the complete native module troubleshooting guide including:
- `ERR_DLOPEN_FAILED` resolution
- Alpine vs Slim decision tree
- Rebuild instructions

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

## Health Checks

For automated health monitoring and CI integration, see **[health-checks.md](health-checks.md)**:
- Container healthcheck configuration
- Health check shell script
- NPM scripts integration
- Troubleshooting health failures

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

## Related Skills

For complete Docker development support, use with these complementary skills:

| Skill | Purpose |
|-------|---------|
| **docker-enforce** | Automatically blocks/transforms host commands to run inside Docker |
| **docker-optimizer** | Analyzes Dockerfiles for optimization opportunities |
| **docker-guard** | Prevents hangs when Docker daemon is unresponsive |

### docker-enforce

Provides automated enforcement of Docker-first policy:
- Intercepts `npm`, `npx`, `yarn`, `pnpm`, `node`, `tsx`, `bun` commands
- Blocks commands on host with suggestion to use `docker exec`
- Can auto-transform commands to run inside container
- Configurable allowlist for safe host commands

Install: `git clone https://github.com/wrsmith108/docker-enforce.git ~/.claude/skills/docker-enforce`

---

## Reference Documentation

| Document | Contents |
|----------|----------|
| [setup.md](setup.md) | First-time setup, native module troubleshooting, project configuration |
| [health-checks.md](health-checks.md) | Container healthchecks, monitoring scripts, NPM integration |

---

## Changelog

### v1.1.0 (2026-01-23)
- **Refactor**: Decompose into sub-files for progressive disclosure
- Extract first-time setup to setup.md
- Extract health checks to health-checks.md
- Add Behavioral Classification section (ADR-025)
- Main SKILL.md reduced from 718 to ~320 lines

### v1.0.0 (2025-01)
- Initial release
- Docker-first enforcement rules
- Container architecture documentation
- Troubleshooting guide

---

*Last updated: January 2026*
