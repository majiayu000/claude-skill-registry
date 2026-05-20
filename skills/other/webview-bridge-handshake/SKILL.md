---
name: "webview-bridge-handshake"
description: "Contract-first browser preview pattern for WebView2-hosted React apps"
domain: "frontend"
confidence: "high"
source: "phase-0-ui"
---

## Context

Use this when a React UI and a WebView2 desktop host need to move in parallel without hard-blocking each other.

## Pattern

1. Define one shared `BridgeMessage` envelope and keep request payloads serializable.
2. Expose `window.hostBridge.receive(message)` early so the host can inject messages later without changing React code.
3. On the desktop side, post JSON with WebView2 and inject a document-created shim that forwards `message` events into `window.hostBridge.receive(...)` when that hook exists.
4. Resolve the real Web UI build first, but ship a bundled placeholder page so the WPF shell stays bootable and the bridge can be exercised before the real bundle exists.
5. Let preview and placeholder modes resolve to an explicit "host pending" handshake snapshot instead of throwing or inventing fake success states.
6. Keep page components read-only until real host capabilities are available; render bridge status and activity so integration work is observable.

## Why it helps

- Frontend and host work can proceed in parallel.
- The desktop host can boot honestly even when the real Web UI build is not ready yet.
- Placeholder UI still compiles and stays honest about missing capabilities.
- The host team gets one narrow seam to target instead of scattered component callbacks.
