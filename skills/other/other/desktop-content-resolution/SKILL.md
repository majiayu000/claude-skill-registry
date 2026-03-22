---
name: "desktop-content-resolution"
description: "Prefer real web bundles over fallback shell content in desktop host resolution"
domain: "desktop-hosting"
confidence: "high"
source: "bishop-investigation"
---

## Context

Hybrid desktop shells often ship a local fallback page while also supporting a repo-built Web UI bundle during development.

## Pattern

1. Enumerate candidate roots upward from the executable base directory.
2. Search every candidate root for the preferred web bundle first.
3. Only if no bundle exists anywhere should the resolver accept a bundled or source fallback page.

## Why

Desktop outputs commonly copy fallback content into the app base directory. If fallback checks are interleaved with upward traversal, the copied page can mask a valid bundle that exists higher in the repo tree.

## Example

- Preferred: `src\PanelNester.WebUI\dist\index.html`
- Fallbacks: `WebApp\index.html`, then `src\PanelNester.Desktop\WebApp\index.html`

## Anti-Pattern

- Checking `WebApp\index.html` in the current output directory before finishing the search for the real bundle.
