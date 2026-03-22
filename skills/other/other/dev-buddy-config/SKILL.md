---
name: dev-buddy-config
description: Dev Buddy web configuration portal for managing presets and pipeline config
user-invocable: true
allowed-tools: Bash
---

# Dev Buddy Web Configuration Portal

Launch the web configuration portal for managing AI provider presets and pipeline configuration.

## Starting the Portal

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/config-server.ts" --cwd "${CLAUDE_PROJECT_DIR}"
```

The server:
1. Starts on an OS-assigned port (printed to stdout as JSON)
2. Opens the user's default browser automatically
3. Serves the Alpine.js SPA for visual configuration
4. Auto-shuts down after 60 minutes of inactivity

## Portal Capabilities

| Tab | Features |
|-----|---------|
| **AI Presets** | List, add, update, remove presets; reveal/hide API keys |
| **Pipeline Config** | Configure which preset each stage uses |

## Startup Output

The server prints a single JSON line to stdout on successful start:

```json
{ "port": 12345, "url": "http://localhost:12345" }
```

Tell the user: `Web portal running at http://localhost:{port}. Press Ctrl+C or close the terminal to stop.`

The server also opens the browser automatically. If the browser does not open (e.g., SSH environment), the user can manually navigate to the URL.

## Stopping the Portal

The portal stops automatically after 60 minutes of inactivity. To stop it manually:
- Press `Ctrl+C` in the terminal running the server

## Security Notes

- The portal is localhost-only — CORS is restricted to the exact `http://localhost:{port}` origin
- API keys are masked by default; use the "Reveal Key" button to temporarily view a full key
- The portal auto-shuts down to minimize the attack window
