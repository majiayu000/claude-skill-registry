---
name: managing-ports
description: Detects framework, finds available ports, and starts dev servers with correct port flags. Resolves port conflicts when multiple projects compete for the same default port (common with git worktrees). Scans running processes, identifies frameworks from config files, and uses the right CLI flag per framework. Use when starting dev server, port conflict, port in use, address already in use, EADDRINUSE, npm run dev, pnpm dev, yarn dev, listen EADDRINUSE, port 3000 taken, or managing multiple local servers.
user-invocable: false
argument-hint: "[--scan | --find | --kill <port>] [--port <number>]"
allowed-tools: Bash Read Grep Glob
compatibility: macOS, Linux, Windows (PowerShell)
metadata:
  author: Saturate
  version: "1.0"
---

# Port Management

Detect framework, find a free port, and start the dev server with the correct port flag. Resolves port conflicts automatically.

## Progress Checklist

```
Port Management Progress:
- [ ] Step 1: Parsed arguments (mode, preferred port)
- [ ] Step 2: Scanned ports for current usage
- [ ] Step 3: Detected framework from project files
- [ ] Step 4: Found available port
- [ ] Step 5: Started server with correct flag
```

## Step 1: Parse Arguments

**Modes:**
- *(default)* — detect framework, find free port, start server
- `--scan` — show what's running on ports 3000–3100
- `--find` — just report next free port (no server start)
- `--kill <port>` — kill the process occupying a specific port (with safety checks, see Step 2)

**Optional arguments:**
- `--port <number>` — preferred starting port (overrides framework default)

## Step 2: Scan Port Usage

Show what's currently occupying ports in the project's default range.

**macOS/Linux:**

```bash
lsof -iTCP -sTCP:LISTEN -nP 2>/dev/null | grep -E ':(3[0-9]{3}|4[0-3][0-9]{2}|4321|5[0-1][0-9]{2}|5173|8[0-9]{3})' | sort -t: -k2 -n
```

**Windows (PowerShell):**

```powershell
Get-NetTCPConnection -State Listen | Where-Object { $_.LocalPort -ge 3000 -and $_.LocalPort -le 9000 } | Sort-Object LocalPort | Format-Table LocalPort, OwningProcess, @{N='Process';E={(Get-Process -Id $_.OwningProcess).ProcessName}}
```

**Detect platform:** Check if `lsof` is available (`command -v lsof`). If not, fall back to `netstat -ano` or `Get-NetTCPConnection`.

**If mode is `--scan`:** Display results and stop.

**If mode is `--kill <port>`:**

**Never kill blindly.** First identify the process on the port:

macOS/Linux:
```bash
lsof -iTCP:<port> -sTCP:LISTEN -nP 2>/dev/null
```

Windows (PowerShell):
```powershell
Get-NetTCPConnection -LocalPort <port> | ForEach-Object { Get-Process -Id $_.OwningProcess } | Format-Table Id, ProcessName, Path
```

**Protected processes — never kill these:**
- Browsers: `firefox`, `chrome`, `safari`, `msedge`, `brave`, `arc`, `opera`
- System services: `launchd`, `systemd`, `svchost`, `WindowsServer`
- Databases: `postgres`, `mysqld`, `mongod`, `redis-server`
- Docker: `docker`, `containerd`, `com.docker.backend`

If the process matches a protected name, tell the user what's on the port and **do not kill it**. Suggest they close the relevant tab/connection manually or pick a different port instead.

**Only kill dev server processes** (e.g. `node`, `python`, `ruby`, `dotnet`, `cargo`, `go`). Even then, show the user the PID and process name and **ask for confirmation** before killing.

macOS/Linux:
```bash
kill <pid>
```

Windows (PowerShell):
```powershell
Stop-Process -Id <pid>
```

Prefer `kill` (SIGTERM) over `kill -9` (SIGKILL) to allow graceful shutdown. Only escalate to `kill -9` if the process doesn't exit within 3 seconds.

## Step 3: Detect Framework

Check project config files to determine the framework. Search in order of specificity:

**Check these files (stop at first match):**

| Config file | Framework |
|---|---|
| `next.config.*` (js/ts/mjs) | Next.js |
| `nuxt.config.*` (js/ts) | Nuxt |
| `vite.config.*` (js/ts/mjs) | Vite (check for SvelteKit/Remix plugins) |
| `svelte.config.*` | SvelteKit (via Vite) |
| `angular.json` | Angular |
| `astro.config.*` | Astro |
| `manage.py` | Django |
| `app.py` or `wsgi.py` | Flask |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `*.csproj` or `*.sln` | .NET |
| `Gemfile` with `rails` | Rails |

**If no specific config found, check `package.json` dependencies:**

```bash
# Read package.json and check dependencies + devDependencies for:
# - "react-scripts" → CRA
# - "next" → Next.js
# - "nuxt" → Nuxt
# - "vite" → Vite
# - "@angular/core" → Angular
# - "astro" → Astro
# - "express" → Express
# - "fastify" → Fastify
# - "hono" → Hono
# - "remix" → Remix
# - "@sveltejs/kit" → SvelteKit
```

**For Vite projects**, also check `vite.config.*` for framework plugins:
- `@sveltejs/kit` plugin → SvelteKit
- `@remix-run/dev` plugin → Remix
- Otherwise → plain Vite

**Detect package manager** (for Node.js projects):

```bash
if [ -f "bun.lockb" ]; then echo "bun"
elif [ -f "pnpm-lock.yaml" ]; then echo "pnpm"
elif [ -f "yarn.lock" ]; then echo "yarn"
else echo "npm"
fi
```

Also check for a `dev` or `start` script in `package.json` — the project may already use a custom port.

## Step 4: Find Available Port

Starting from the framework's default port (or `--port` if specified), find the first available port.

**macOS/Linux:**

```bash
check_port() {
  lsof -iTCP:"$1" -sTCP:LISTEN -nP 2>/dev/null | grep -q ":$1" && return 1 || return 0
}

find_free_port() {
  local port="${1:-3000}"
  while ! check_port "$port"; do
    port=$((port + 1))
  done
  echo "$port"
}
```

**Windows (PowerShell):**

```powershell
function Find-FreePort($start = 3000) {
  $port = $start
  while (Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue) { $port++ }
  return $port
}
```

**Framework default ports:**

| Framework | Default port |
|---|---|
| Next.js | 3000 |
| Nuxt | 3000 |
| CRA | 3000 |
| Express / Fastify / Hono | 3000 |
| Rails | 3000 |
| Vite / SvelteKit / Remix | 5173 |
| Astro | 4321 |
| Angular | 4200 |
| Flask | 5000 |
| .NET | 5000 |
| Django | 8000 |
| FastAPI (uvicorn) | 8000 |
| Go / Rust | 8080 |

**If mode is `--find`:** Report the free port and stop.

## Step 5: Start Server

Use the detected framework and package manager to start the dev server on the available port.

### Port flag per framework

| Framework | Start command | Port mechanism |
|---|---|---|
| Next.js | `{pm} run dev` | `-p <port>` appended (or `-- -p <port>` if using npm) |
| Nuxt | `{pm} run dev` | `-- --port <port>` |
| Vite / SvelteKit / Remix | `{pm} run dev` | `-- --port <port>` |
| CRA | `{pm} run start` | `PORT=<port>` env variable prefix |
| Astro | `{pm} run dev` | `-- --port <port>` |
| Angular | `{pm} run start` (or `ng serve`) | `-- --port <port>` |
| Express / Fastify / Hono | `{pm} run dev` | `PORT=<port>` env variable prefix |
| Django | `python manage.py runserver` | `0.0.0.0:<port>` positional arg |
| Flask | `flask run` | `--port <port>` |
| FastAPI | `uvicorn main:app` | `--port <port>` |
| Rails | `bin/rails server` | `-p <port>` |
| .NET | `dotnet run` | `--urls http://localhost:<port>` |
| Go | `go run .` | `PORT=<port>` env variable prefix |
| Rust | `cargo run` | `PORT=<port>` env variable prefix |

`{pm}` = detected package manager (npm, pnpm, yarn, bun).

**npm quirk:** When passing flags through npm scripts, use `--` separator: `npm run dev -- -p 3001`. pnpm/yarn/bun pass flags directly without `--`.

**Before starting:** Tell the user which framework was detected, which port will be used, and the exact command being run.

### Scripts with hardcoded ports

Before appending port flags, read the `dev`/`start` script value from `package.json` and check if it already contains a port flag (`-p`, `--port`, or a `PORT=` prefix).

If a port is already in the script:
1. Tell the user what port is configured and where (e.g. `"dev": "next dev -p 4000"`)
2. Check if that port is available — if so, just run the script as-is without extra flags
3. If that port is occupied, **do not** blindly append another port flag — most frameworks ignore duplicates or behave unpredictably with two port args
4. Instead, suggest the user either:
   - Temporarily edit the script to use the new port
   - Use an env var override if the framework supports it (e.g. `PORT=3001 pnpm run dev` for Express/CRA)
   - Run the underlying command directly (e.g. `pnpm next dev -p 3001` instead of `pnpm run dev`)

## Error Handling

**Port conflict in default mode:**
- Never kill processes. Always increment to the next free port.
- Tell the user which port was occupied and what port was chosen instead.

**`--kill` mode — process won't exit:**
- The process may take a moment to release the port. Wait 3 seconds and re-check.
- If still occupied after SIGTERM, ask the user before escalating to `kill -9`.

**No framework detected:**
- Tell the user no framework was identified.
- List what was checked.
- Ask which command they'd like to run.

**Dev script not found in package.json:**
- Check for common script names: `dev`, `start`, `serve`.
- If none found, ask the user for the start command.

## Examples

### Default: Start dev server

```
User: start the dev server
```

1. Scan ports → port 3000 in use by another Next.js instance
2. Detect framework → Next.js (found `next.config.ts`)
3. Detect package manager → pnpm
4. Find free port → 3001
5. Run: `pnpm run dev -- -p 3001`

### Scan mode

```
User: /managing-ports --scan
```

Output: Table of ports 3000–3100 showing PID, process name, and port.

### Find mode

```
User: /managing-ports --find --port 8080
```

Output: "Port 8080 is in use. Next available: 8081"

### Kill mode

```
User: /managing-ports --kill 3000
```

Output: "Killed process 12345 (node) on port 3000"
