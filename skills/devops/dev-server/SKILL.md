---
name: dev-server
description: Start development servers with intelligent port management. Use when asked to "start the dev server", "run dev", "start development", "launch the server", "spin up the app", "get this running", "boot the frontend", or any request to run a local development server. Handles port conflicts, detects project type, cleans up stale processes, and opens the browser automatically.
license: MIT
metadata:
  author: petekp
  version: "0.1.0"
---

# Dev Server

## Workflow

1. **Check ports** - Run `scripts/check_ports.sh` to scan common dev ports
2. **Resolve conflicts**:
   - **Same project**: Use `--kill-if-same` to kill without asking
   - **Different project**: Ask user before killing or use alternate port
3. **Detect environment** - Check for docker-compose.yml, monorepo structure, or package.json
4. **Start server** - Use detected package manager with `--open` flag; add `--port <n>` if needed

## Port Script

```bash
scripts/check_ports.sh                   # Scan ports, show which project each belongs to
scripts/check_ports.sh 3000              # Check specific port with project info
scripts/check_ports.sh --find 3000       # Find first available port
scripts/check_ports.sh --kill-if-same 3000   # Kill only if same project (safe)
scripts/check_ports.sh --kill 3000       # Force kill (ask user first if different project)
```

The script detects project ownership by comparing the process's working directory to the current directory. "Same project" means the process was started from this directory or a parent/child of it.

## Environment Detection

**Docker projects**: If `docker-compose.yml` exists with a web/app service, suggest `docker compose up` instead.

**Monorepos**: Check if current directory has package.json with `dev` script. If not, look for:
- `apps/web/package.json` or `packages/app/package.json` (Turborepo/Nx pattern)
- Root package.json with workspace `dev` script that delegates

**Package manager**: Detect from lockfile (bun.lockb → bun, pnpm-lock.yaml → pnpm, yarn.lock → yarn, otherwise npm).

## Framework Notes

Most frameworks support `--open` and `--port` flags. Exceptions:

| Framework | Default Port | Notes |
|-----------|--------------|-------|
| Create React App | 3000 | Uses `PORT=3001` env var instead of `--port` |
| Gatsby | 8000 | Uses `-p` instead of `--port` |
| Remix | 3000 | `--port` works in dev mode |

When `--open` doesn't work, fall back to `open http://localhost:PORT` after server starts.
