---
name: modern-browser-apis
description: Leverage standardized browser APIs over custom solutions or heavy dependencies
---

# Using Modern Browser APIs

Prefer native browser capabilities over third-party dependencies. Use progressive enhancement with sensible fallbacks.

## Core Principles

- **PREFER** native APIs over third-party dependencies
- Use progressive enhancement with fallbacks for unsupported APIs
- Use async and secure patterns for safe, non-blocking access

## Observation & Monitoring

- Intersection Observer - viewport visibility detection
- ResizeObserver - element sizing changes
- PerformanceObserver - performance metrics

## Navigation & Transitions

- View Transitions API - hardware-accelerated state changes
- URLPattern API - declarative URL matching for routing

## Data Access

- Clipboard Async API - clipboard operations
- Web Share API - native sharing
- File System Access API - file operations with permissions

## Performance

- Web Locks API - coordinate resource access
- Scheduling API - task prioritization
- Web Workers - offload computation from main thread

## Implementation Guidance

Always use feature detection:
```js
if ('clipboard' in navigator) { … }
```

- Prioritize promise-based APIs
- Clearly communicate permission requests to users
- Always provide graceful fallbacks for unsupported browsers
