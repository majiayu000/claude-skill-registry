---
name: solid-router-alternative
description: "Solid Router alternative routers: HashRouter for hash-based URLs, MemoryRouter for testing and in-memory navigation."
metadata:
  globs:
    - "**/*router*"
---

# Alternative Routers

## HashRouter

Uses hash portion of URL for routing. Client-side only routing (hash not handled by server).

```tsx
import { HashRouter, Route } from "@solidjs/router";

<HashRouter root={App}>
  <Route path="/" component={Home} />
  <Route path="/about" component={About} />
</HashRouter>
```

**Use cases:**
- Legacy hash-based URLs
- Client-side only applications
- No server routing needed

**URL format:** `https://example.com/#/about`

## MemoryRouter

Keeps router history in memory. Doesn't interact with browser URL. Useful for testing.

```tsx
import { MemoryRouter, Route } from "@solidjs/router";

<MemoryRouter root={App}>
  <Route path="/" component={Home} />
  <Route path="/about" component={About} />
</MemoryRouter>
```

**Use cases:**
- Testing router logic
- Controlling router state programmatically
- Testing without browser URL changes

**Note:** URL in address bar won't change, but router state changes.

## Best Practices

1. Use `HashRouter` for legacy compatibility or client-only apps
2. Use `MemoryRouter` for testing router behavior
3. Default `Router` is preferred for most applications (uses pathname)
4. All routers support same route configuration and features

