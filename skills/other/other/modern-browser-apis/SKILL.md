---
name: use-modern-browser-apis
description: Utilize built-in browser APIs (like Popover API, View Transitions etc) instead of building features manually via JavaScript
---

# Using Modern Browser APIs

We prefer native, modern browser APIs — _standardized, widely supported, and high-leverage_ — to heavy external libraries or custom fallbacks. Use them to simplify logic, improve performance, and reduce bundle size where appropriate.

## Philosophy

- **PREFER** browser-native capabilities over third-party dependencies
- **PROGRESSIVE ENHANCE**: Always provide sensible fallbacks for APIs that aren’t available in all clients
- **ASYNC & SECURE**: Use promise-based and secure context APIs for non-blocking, safe access

## Core & Widely Supported APIs

These APIs are stable, broadly implemented, and useful in everyday applications.

### UI & Interaction

- **Intersection Observer API** — Efficiently detect when elements enter/exit the viewport (lazy loading, infinite scroll).
- **ResizeObserver API** — React to element size changes without layout thrashing.
- **PerformanceObserver API** — Observe performance metrics (RUM/perf insights).
- **BroadcastChannel API** — Cross-tab communication in the same origin.

### Navigation & View Management

- **View Transitions API** — Native, hardware-accelerated transitions between UI states.
- **URLPattern API** — Declaratively match and parse URLs (helps in routing logic).

### Clipboard & Sharing

- **Clipboard Async API** — Non-blocking, modern clipboard read/write with user consent.
- **Web Share API Level 2** — Share text, links, files through native device dialogs.

### Files & Persistence

- **File System Access API** — Read/write local files with user permissions.
- **File Handle & Directory Picker** extensions for batch file/directory selection.

### Concurrency & Scheduling

- **Web Locks API** — Coordinate async access to shared resources (avoid races).
- **Scheduling API** — Prioritize/background non-essential work to improve responsiveness.

### Workers & Off-Main Thread

- **Web Workers API** — Run scripts off the main thread for intensive tasks.
- **OffscreenCanvas** — Use canvas rendering in workers for performant graphics/visuals.

### Speech & Accessibility

- **Web Speech API** — Integrate speech recognition and synthesis for accessibility and voice UI.

### Advanced Graphics & Compute

- **WebGPU API** — Low-level GPU access for high-perf rendering and compute workloads (in many browsers; includes Chromium + newer Safari + Firefox support).

### Real-Time & Networking

- **WebRTC** — Real-time peer-to-peer audio/video communication without plugins.

## When to Use & How to Fallback

- **FEATURE DETECTION** is required before use:
  ```js
  if ('clipboard' in navigator) { … }
  ```

For APIs not universally supported (e.g., WebGPU), provide a graceful fallback (WebGL or degraded UI).

Always combine user gesture requirements (e.g., for sharing or clipboard) with permission checks.

## Best Practices

**ASYNC FIRST**: Prefer promise/async APIs to avoid blocking UI.

**PERMISSIONS UI**: Convey clearly to users when the browser will ask for access (files, clipboard, sharing).

**PERFORMANCE MINDFUL**: Observe and prioritize main thread work using PerformanceObserver or Scheduling APIs.

**SECURE CONTEXTS**: Use HTTPS; many APIs require secure contexts to function.

## General Principles

Write code for browsers as platforms, not just JS engines.

Prefer native semantics (e.g., lazy loading via IntersectionObserver vs manual scroll handlers).

Reduce external dependencies where modern browser APIs suffice.

Document API usage and fallback patterns for maintenance and cross-browser support.
