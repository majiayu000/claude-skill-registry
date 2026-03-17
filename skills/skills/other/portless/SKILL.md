---
name: portless
description: Stable named .localhost URLs for local dev servers. Use when running dev servers, port conflicts, needing stable URLs, or CORS issues with localhost. Triggers on "port", "localhost", "dev server", "local URL", "CORS localhost", "which port".
---

# Stable Local Dev URLs

STABILIZE. Replace random port numbers with named URLs. Agents and browser automation need deterministic, discoverable URLs — portless provides them. `myapp.localhost:1355` instead of `localhost:3247`.

## Rules

- Always use named URLs (`myapp.localhost:1355`) in browser automation, tests, and documentation — never hardcode port numbers
- Always integrate via `package.json` scripts — don't rely on manual `portless <name>` invocations
- One name per service — names are the contract, ports are the implementation detail
- URL format: `http://<name>.localhost:1355` — port 1355 is always part of the URL unless overridden

## When to Integrate

| Signal | Action |
|--------|--------|
| New project with dev server | Add portless to `package.json` scripts |
| Multi-service project | Name each service: api, web, docs |
| Browser automation needed | Set up portless first for stable URLs |
| Port conflicts between projects | Give each project a unique name |
| CORS issues on localhost | `.localhost` domains share cookies predictably |
| Agent needs to find the app | Name it — `portless list` shows all active routes |

## Flow: Project Setup

One-time integration — after this, `npm run dev` always produces a stable URL.

```bash
npm install -g portless
```

Add to `package.json`:
```json
{
  "scripts": {
    "dev": "portless myapp next dev"
  }
}
```

First run auto-starts the proxy. Verify with `portless list` — should show `myapp → localhost:<port>`.

Open `http://myapp.localhost:1355` — this URL never changes.

## Flow: Multi-Service Naming

Convention: `<service>.localhost:1355` for independent services, dotted names for subdomains.

```json
{
  "scripts": {
    "dev:api": "portless api pnpm start",
    "dev:web": "portless web next dev",
    "dev:docs": "portless docs vitepress dev"
  }
}
```

Results in:
- `http://api.localhost:1355`
- `http://web.localhost:1355`
- `http://docs.localhost:1355`

Dotted names create subdomains: `portless api.myapp pnpm start` → `http://api.myapp.localhost:1355`

Names are lowercased and validated: only `[a-z0-9.-]`, no consecutive dots.

## Flow: HTTPS Setup

When needed: OAuth callbacks, secure cookies, service workers.

```bash
portless proxy start --https
portless trust
```

After trust, `https://myapp.localhost:1355` works without browser warnings. HTTP/2 is enabled automatically with HTTPS. One-time setup per machine.

## Flow: Bypass

When you need to skip portless temporarily (debugging port issues, CI without proxy):

```bash
PORTLESS=0 npm run dev
```

Runs the command directly without proxy wrapping.

## How It Works

Proxy on port 1355, random app port (4000-4999) via `PORT` env var, framework auto-detection injects `--port` and `--host` flags for frameworks that need them (Vite, Astro, Angular).

`.localhost` domains resolve to `127.0.0.1` natively — no `/etc/hosts` edits needed.

Stale routes auto-clean when the owning process PID dies. WebSocket proxying (HMR) works automatically.

## Composition

- **With browser:** `agent-browser open "http://myapp.localhost:1355"` — stable URL across all sessions and restarts
- **With watch:** d3k wraps the dev command, portless wraps the name — `portless myapp d3k -c "bun run dev" --no-tui --no-skills --no-agent` for monitored development with stable URLs
- **With hope:loop:** consistent URLs across wave iterations — port changes between restarts don't break automation
- **With agents:** any agent can `portless list` to discover running services without knowing ports
