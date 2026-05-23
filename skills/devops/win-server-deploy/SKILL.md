---
name: win-server-deploy
description: Pack TermLink server into a self-contained zip for Windows deployment, install/uninstall as a background service using pm2, and manage the running server. Use when packaging the server for another Windows machine or setting up auto-start.
---

# Windows Server Deploy

Use this skill to package the TermLink Node.js server into a portable zip and deploy it as a Windows background service.

## Why Not Docker

`node-pty` requires native Windows conpty access for PowerShell/CMD terminals. Docker runs Linux containers and cannot provide Windows PTY, so the Win server must be deployed natively.

## Prerequisites

- **Build machine** (this machine): Node.js 20+, `npm install` already done
- **Target machine**: Node.js 20 LTS only (no build tools needed)

## Pack

Create a self-contained zip with pruned `node_modules` (excludes `@capacitor`, `xterm`, `nodemon` — not needed on server):

```powershell
powershell -ExecutionPolicy Bypass -File ./skills/win-server-deploy/scripts/pack-win-server.ps1
```

Output: `dist/termlink-win-<timestamp>.zip` (~22 MB)

The zip contains:
- `src/` — server source
- `public/` — web frontend assets
- `node_modules/` — pruned production dependencies (with pre-built `node-pty`)
- `ecosystem.config.js` — pm2 process config
- `.env.example` — environment configuration template
- `deploy-scripts/` — install/uninstall/start scripts
- `data/`, `logs/` — empty runtime directories

## Deploy on Target Machine

### 1. Extract

```powershell
# Right-click zip → Extract All, or:
Expand-Archive termlink-win-*.zip -DestinationPath C:\TermLink
```

### 2. Configure

```powershell
cd C:\TermLink
Copy-Item .env.example .env
notepad .env
```

**Must change** for production:
| Variable | Default | Description |
|----------|---------|-------------|
| `AUTH_USER` | `admin` | BasicAuth username |
| `AUTH_PASS` | `CHANGE_ME_TO_STRONG_PASSWORD` | BasicAuth password |
| `PORT` | `3000` | Listen port |

### 3. Install Service (as Administrator)

```powershell
powershell -ExecutionPolicy Bypass -File .\deploy-scripts\install-service.ps1
```

This automatically:
- Installs `pm2` globally
- Registers pm2 auto-start on Windows boot
- Starts TermLink
- Verifies `/api/health`

### 4. Verify

```powershell
pm2 status
pm2 logs termlink
curl http://localhost:3000/api/health
```

## Daily Management

```powershell
pm2 restart termlink    # Restart
pm2 stop termlink       # Stop
pm2 start termlink      # Start
pm2 logs termlink       # View logs
pm2 monit               # Real-time monitoring dashboard
```

## Uninstall

```powershell
powershell -ExecutionPolicy Bypass -File .\deploy-scripts\uninstall-service.ps1
```

## Quick Test (No Service Install)

For local testing without pm2, just run directly:

```powershell
cd C:\TermLink
node src/server.js
```

## Rules

- Always exclude `@capacitor/*` from server packages (contains Android DEX files with paths exceeding Windows MAX_PATH 260 limit).
- Use `robocopy` (not `Copy-Item`) when copying `node_modules` to handle any remaining long paths.
- The zip includes pre-compiled `node-pty` native bindings — the target machine does **not** need Python, Visual C++ Build Tools, or node-gyp.
- pm2 must run in `fork` mode (not `cluster`) because `node-pty` does not support cluster mode.
