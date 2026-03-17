---
name: figjam-plugin
description: FigJam plugin development workflow. Use when working on plugin code (code.ts, ui.ts), debugging WebSocket communication, or building the plugin.
---

# FigJam Plugin Development

## Architecture

Two-thread model:

- `packages/plugin/src/code.ts` - Main thread (Figma API, renderer)
  - NO browser APIs (window, document, fetch)
  - Access to figma.* API
  - Renders nodes/edges to FigJam canvas

- `packages/plugin/src/ui.ts` - UI iframe (WebSocket client)
  - Browser APIs available
  - Manages WebSocket connection to CLI
  - Handles connection UI

## Communication Flow

```
CLI (serve) ←→ WebSocket ←→ Plugin UI (ui.ts) ←→ postMessage ←→ Plugin Main (code.ts)
```

## JSON Import (UI)

- Accepts DSL JSON (nodes as array) or IR JSON (nodes as object)
- Validates with `@figram/core` and normalizes to IR before posting to main thread
- Validation errors are surfaced in the UI alert with path/message details

## Build

```bash
cd packages/plugin && bun run build
```

Output: `packages/plugin/dist/` (code.js, ui.html)

## Import Plugin

1. Open Figma Desktop
2. Menu → Plugins → Development → Import plugin from manifest
3. Select `packages/plugin/manifest.json`

## Debugging

- **UI errors**: Browser DevTools console (right-click plugin UI → Inspect)
- **Main thread errors**: Figma DevTools (Menu → Plugins → Development → Open console)
- **WebSocket issues**: Check UI console for connection status

## Key Files

- `manifest.json` - Plugin configuration
- `src/code.ts` - Canvas rendering logic
- `src/ui.ts` - WebSocket client and connection UI
- `src/ui.html` - UI template (bundled by build)
- `src/icons/` - AWS service icons
