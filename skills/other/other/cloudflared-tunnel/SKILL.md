---
name: cloudflared-tunnel
description: Create temporary public URLs for localhost apps using Cloudflare Quick Tunnels with tmux-based process management. Use when you need to preview a local app externally (mobile device, remote collaborator, QA), including host-allowlist fixes when a dev server blocks external hosts.
---

# Cloudflared Tunnel

Use this skill when a user wants to expose any localhost web app to the internet quickly and temporarily.

## What this skill standardizes

- Runs app + tunnel in `tmux` for stability.
- Avoids brittle background/nohup setups.
- Handles host-allowlist blocks when a dev server enforces `Host` checks.
- Gives clean start/stop/status commands.

## Preconditions

Run these checks first:

```bash
command -v tmux >/dev/null 2>&1 && echo "tmux ok" || echo "tmux missing"
command -v cloudflared >/dev/null 2>&1 && echo "cloudflared ok" || echo "cloudflared missing"
```

If `cloudflared` is missing on macOS:

```bash
brew install cloudflared
```

## Inputs you need

- Project path
- Dev server command
- Local port

If not provided, infer from the repo (scripts/config/docs), then proceed.

## Default tmux workflow

Use a stable session name (example: `dev-tunnel`).

1. Start app window:

```bash
cd <project-path>
tmux kill-session -t dev-tunnel 2>/dev/null || true
tmux new-session -d -s dev-tunnel -n app '<dev-command>'
```

2. Start tunnel window:

```bash
tmux new-window -t dev-tunnel -n tunnel 'cloudflared tunnel --url http://127.0.0.1:<port>'
```

3. Read tunnel URL:

```bash
sleep 6
tmux capture-pane -pt dev-tunnel:tunnel -S -160
```

Look for a URL ending in `.trycloudflare.com`.

## If Vite/Astro blocks the host

Symptom in browser:

- `Blocked request. This host ("<host>.trycloudflare.com") is not allowed.`

This is not Cloudflare-specific; it is a dev-server host allowlist rule. Only apply this fix when that error appears.

Fix by allowing trycloudflare hosts in the corresponding framework/server config.

### Astro (`astro.config.mjs`)

```js
vite: {
  server: {
    allowedHosts: ['.trycloudflare.com']
  }
}
```

### Vite (`vite.config.js|ts`)

```js
export default defineConfig({
  server: {
    allowedHosts: ['.trycloudflare.com']
  }
})
```

### webpack-dev-server (if used)

```js
module.exports = {
  devServer: {
    allowedHosts: '.trycloudflare.com'
  }
}
```

After editing config, restart the tmux session:

```bash
tmux kill-session -t dev-tunnel
# then run the start commands again
```

## Verification

- App window shows server ready and listening on expected port.
- Tunnel window shows `Your quick Tunnel has been created!`.
- External URL opens from mobile network.

## Shutdown and cleanup

Stop everything for this tunnel:

```bash
tmux kill-session -t dev-tunnel
pkill -f 'cloudflared tunnel --url http://127.0.0.1:<port>' || true
```

Optional checks:

```bash
lsof -nP -iTCP:<port> -sTCP:LISTEN || true
pgrep -fl 'cloudflared tunnel|astro dev|vite' || true
```

## Notes

- Quick Tunnel URLs are ephemeral and change each run.
- Keep tunnel process alive while testing.
- Most servers work without extra config; only change allowlists if blocked by host validation.
- If allowlist is needed, prefer wildcard `.trycloudflare.com` to avoid per-run edits.
- If the repo has strict conventions, keep edits minimal and revert only if requested.

## References

- `references/troubleshooting.md`
