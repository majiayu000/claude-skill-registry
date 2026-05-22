---
name: solidstart-client-only
description: "SolidStart clientOnly: render components/pages exclusively on client, bypass SSR for browser APIs (window, document), dynamic imports with fallbacks."
metadata:
  globs:
    - "src/routes/**/*"
---

# SolidStart clientOnly

The `clientOnly` function renders components or pages exclusively on the client side, bypassing SSR.

## Component Usage

1. Create separate file for client-only component:

```tsx
// ClientOnlyComponent.tsx
export default function ClientOnlyComponent() {
  const location = document.location.href;
  return <div>Current URL: {location}</div>;
}
```

2. Import with `clientOnly`:

```tsx
import { clientOnly } from "@solidjs/start";

const ClientOnlyComp = clientOnly(() => import("./ClientOnlyComponent"));

export default function IsomorphicComponent() {
  return <ClientOnlyComp />;
}
```

3. Optional fallback:

```tsx
<ClientOnlyComp fallback={<div>Loading...</div>} />
```

## Page-Level Usage

Disable SSR for entire page:

```tsx
// routes/page.tsx
import { clientOnly } from "@solidjs/start";

export default clientOnly(async () => ({ default: Page }), { lazy: true });

function Page() {
  // This code runs only on client
  return <div>Client-only page content</div>;
}
```

## Parameters

**fn:** `() => Promise<{ default: () => JSX.Element }>`
- Function that dynamically imports component

**options:** `{ lazy?: boolean }`
- `lazy: true` (default) - Lazy load component
- `lazy: false` - Eager loading

**props:** `Record<string, any> & { fallback?: JSX.Element }`
- Props passed to component
- Optional `fallback` for loading state

## Use Cases

- Browser APIs (`window`, `document`, `localStorage`)
- Third-party widgets (maps, charts)
- DOM manipulation
- Avoiding SSR hydration issues
- Code that can't run on server

## Best Practices

1. Isolate client-only logic in separate files
2. Provide meaningful fallbacks for loading states
3. Use sparingly - prefer SSR when possible
4. Consider progressive enhancement where possible

