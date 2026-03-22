---
name: managing-ports
description: Detects framework, finds available ports, and starts dev servers with correct port flags. Resolves port conflicts when multiple projects compete for the same default port (common with git worktrees). Scans running processes, identifies frameworks from config files, and uses the right CLI flag per framework. Use when starting dev server, port conflict, port in use, address already in use, EADDRINUSE, npm run dev, pnpm dev, yarn dev, listen EADDRINUSE, port 3000 taken, or managing multiple local servers.
user-invocable: false
argument-hint: "[--scan | --find | --kill <port>] [--port <number>]"
allowed-tools: Bash Read Grep Glob
---

# Port Management

Detect framework, find a free port, and start the dev server with the correct port flag. Resolves port conflicts automatically.

For OS-specific commands (macOS/Linux/Windows), see [references/platform-commands.md](references/platform-commands.md).

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

Show what's occupying ports in the project's default range using `lsof` (macOS/Linux) or `Get-NetTCPConnection` (Windows). See [references/platform-commands.md](references/platform-commands.md) for exact commands.

**If mode is `--scan`:** Display results and stop.

**If mode is `--kill <port>`:**

First identify the process on the port.

**Protected processes — never kill these:**
- Browsers: `firefox`, `chrome`, `safari`, `msedge`, `brave`, `arc`, `opera`
- System services: `launchd`, `systemd`, `svchost`, `WindowsServer`
- Databases: `postgres`, `mysqld`, `mongod`, `redis-server`
- Docker: `docker`, `containerd`, `com.docker.backend`

If the process matches a protected name, tell the user what's on the port and **do not kill it**. Suggest they close the relevant tab/connection manually or pick a different port instead.

**Only kill dev server processes** (e.g. `node`, `python`, `ruby`, `dotnet`, `cargo`, `go`). Even then, show the user the PID and process name and **ask for confirmation** before killing. Prefer SIGTERM over SIGKILL.

## Step 3: Detect Framework

Check project config files to determine the framework (stop at first match): `next.config.*`, `nuxt.config.*`, `vite.config.*`, `svelte.config.*`, `angular.json`, `astro.config.*`, `manage.py`, `app.py`/`wsgi.py`, `Cargo.toml`, `go.mod`, `*.csproj`/`*.sln`, `Gemfile` with `rails`.

If no config file found, check `package.json` dependencies/devDependencies for `react-scripts`, `next`, `nuxt`, `vite`, `@angular/core`, `astro`, `express`, `fastify`, `hono`, `remix`, `@sveltejs/kit`.

**For Vite projects**, also check `vite.config.*` for framework plugins (`@sveltejs/kit` → SvelteKit, `@remix-run/dev` → Remix).

**Detect package manager:** Check for `bun.lockb` → bun, `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, else npm.

Also check for a `dev` or `start` script in `package.json` — the project may already use a custom port.

## Step 4: Find Available Port

Starting from the framework's default port (or `--port` if specified), find the first available port by checking with `lsof`/`Get-NetTCPConnection` and incrementing.

**Framework default ports:**

| Framework | Default port |
|---|---|
| Next.js / Nuxt / CRA / Express / Fastify / Hono / Rails | 3000 |
| Vite / SvelteKit / Remix | 5173 |
| Astro | 4321 |
| Angular | 4200 |
| Flask / .NET | 5000 |
| Django / FastAPI | 8000 |
| Go / Rust | 8080 |

**If mode is `--find`:** Report the free port and stop.

**Auto-port frameworks (Next.js, Nuxt):** Skip port finding entirely unless the user explicitly requested a specific port. These frameworks handle port selection themselves and print the result to stdout.

## Step 5: Start Server

Use the detected framework and package manager to start the dev server on the available port.

### General principle: prefer framework auto-port selection

Some frameworks automatically detect port conflicts and pick the next available port, printing the chosen port to stdout. **Do not fight the framework** — if it handles port selection, let it. Only pass explicit port flags when:
- The user explicitly requested a specific port
- The framework does not support auto-port selection

When a framework auto-selects, read the port from stdout and report it to the user.

### Auto-port frameworks (Next.js, Nuxt)

Next.js and Nuxt automatically detect port conflicts and pick the next available port. They print the chosen port to stdout (e.g. `- Local: http://localhost:3001`).

**Default behavior (no explicit `--port` requested):** Just run `{pm} run dev` with no port flag. Let the framework handle it. Read the actual port from stdout and report it to the user.

**Only pass a port flag if the user explicitly requested a specific port.** In that case, use the port flag table below.

### Port flag per framework

| Framework | Start command | Port mechanism |
|---|---|---|
| Next.js | `{pm} run dev` | Auto-picks port. Only use `-p <port>` if user requests specific port |
| Nuxt | `{pm} run dev` | Auto-picks port. Only use `-- --port <port>` if user requests specific port |
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

**Important — npm requires `--` separator:** `npm run dev -- -p 3001`. pnpm/yarn/bun pass flags directly without `--`. Getting this wrong is a common source of port flags being silently ignored.

**Before starting:** Tell the user which framework was detected and the exact command being run. For auto-port frameworks, tell the user the port will be reported once the server starts.

### pnpm monorepo / workspace handling

When running in a pnpm workspace (detected by `pnpm-workspace.yaml` in the project root):

1. Read the root `package.json` dev script. If it uses `pnpm --filter <package> dev`, port flags appended at root level (`pnpm dev -- --port 3002`) will **not** propagate through the filter chain.
2. Instead, either:
   - Run the command directly at the filter level: `pnpm --filter <package> dev -- --port <port>`
   - Or `cd` into the package directory and run `pnpm dev -- --port <port>` there
3. For auto-port frameworks (Next.js, Nuxt) in a monorepo, prefer just running without port flags and reading the port from stdout — this avoids the filter propagation issue entirely.

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
- Wait 3 seconds and re-check. If still occupied after SIGTERM, ask the user before escalating to `kill -9`.

**No framework detected:**
- Tell the user no framework was identified, list what was checked, ask which command they'd like to run.

**Dev script not found in package.json:**
- Check for common script names: `dev`, `start`, `serve`. If none found, ask the user for the start command.

## Examples

### Default: Start dev server (auto-port framework)

```
User: start the dev server
```

1. Detect framework -> Next.js (found `next.config.ts`)
2. Detect package manager -> pnpm
3. Next.js auto-picks ports — no port flag needed
4. Run: `pnpm run dev`
5. Read stdout -> "Ready on http://localhost:3001"
6. Report: "Dev server running on port 3001 (3000 was in use, Next.js auto-selected 3001)"

### Default: Start dev server (non-auto-port framework)

```
User: start the dev server
```

1. Scan ports -> port 5173 in use
2. Detect framework -> Vite (found `vite.config.ts`)
3. Detect package manager -> pnpm
4. Find free port -> 5174
5. Run: `pnpm run dev -- --port 5174`

### Monorepo with pnpm filter

```
User: start the dev server on port 3002
```

1. Detect pnpm workspace (`pnpm-workspace.yaml` found)
2. Root dev script: `pnpm --filter @norriq/commerce-platform dev`
3. Detect framework -> Nuxt (in filtered package)
4. User requested specific port -> pass port flag at filter level
5. Run: `pnpm --filter @norriq/commerce-platform dev -- --port 3002`

### Scan mode

```
User: /managing-ports --scan
```

Output: Table of ports 3000-3100 showing PID, process name, and port.

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
