---
name: frontend-design
description: Unified frontend design skill covering React 19 patterns, Tailwind CSS v4, Web Design Guidelines (A11y, Animation, Forms), and AI prototyping tools (Stitch, Nano Banana Pro). Use when designing components, layouts, or building aesthetic interfaces.
---

# Frontend Design Skill

> **Philosophy:** Intentional Minimalism. Every element must earn its place.

---

## Tech Stack

| Layer | Technology | Notes |
|-------|------------|-------|
| Framework | React 19 + Vite | Function components, `ref` as prop |
| Styling | Tailwind CSS v4 | `@tailwindcss/vite` plugin |
| Components | shadcn/ui + Radix | Never reinvent primitives |
| Animation | Framer Motion 12 | Micro-interactions |
| Charts | Recharts 2 | Performance visualizations |

---

## React Performance Patterns (Vercel)

### Priority 1: Eliminating Waterfalls (CRITICAL)

| Rule | Pattern |
|------|---------|
| `async-defer-await` | Move `await` into branches where actually used |
| `async-parallel` | Use `Promise.all()` for independent operations |
| `async-suspense` | Use `<Suspense>` to stream content progressively |

```tsx
// ❌ Sequential waterfalls
const user = await getUser();
const posts = await getPosts();

// ✅ Parallel fetching
const [user, posts] = await Promise.all([getUser(), getPosts()]);
```

### Priority 2: Bundle Optimization (CRITICAL)

| Rule | Pattern |
|------|---------|
| `bundle-barrel-imports` | Avoid barrel files (`index.ts` re-exports) |
| `bundle-namespace-imports` | Use specific imports, not `import * as` |
| `bundle-dynamic-imports` | Use `next/dynamic` or `React.lazy` for heavy components |

```tsx
// ❌ Barrel import
import { Button, Card, Modal } from "@/components";

// ✅ Direct imports
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
```

### Priority 3: Component Boundaries (HIGH)

| Rule | Pattern |
|------|---------|
| `client-boundary` | Keep `"use client"` at leaf components |
| `server-default` | Default to Server Components, client only for interactivity |
| `rerender-children` | Pass children as props to avoid re-renders |

```tsx
// ❌ Client boundary too high
"use client"
export function Page() { ... } // Entire page is client

// ✅ Client boundary at leaf
export function Page() {
  return <Layout><InteractiveButton /></Layout> // Only button is client
}
```

---

## Web Design Standards (Vercel)

### Accessibility

| Rule | Standard |
|------|----------|
| Contrast | 4.5:1 minimum for text |
| Focus | Visible `focus-visible:ring-*`, never `outline-none` alone |
| Semantics | Use `<button>`, `<a>`, `<nav>` before ARIA |
| Headings | Hierarchical `<h1>`→`<h6>`, include skip links |

### Animation

| Rule | Standard |
|------|----------|
| Performance | Only `transform`/`opacity` (compositor-friendly) |
| Preference | Honor `prefers-reduced-motion` |
| Specificity | Never `transition: all`, list properties explicitly |
| Interruptible | Animations respond to user input mid-animation |

### Forms

| Rule | Standard |
|------|----------|
| Autocomplete | Always set `autocomplete` and meaningful `name` |
| Input Types | Use correct `type` (`email`, `tel`, `url`) and `inputmode` |
| Labels | Clickable via `htmlFor` or wrapping |
| Errors | Inline next to fields, focus first error on submit |
| Paste | Never block paste (`onPaste + preventDefault`) |

### Typography

| Rule | Standard |
|------|----------|
| Ellipsis | Use `…` not `...` |
| Quotes | Curly quotes `"` `"` not straight `"` |
| Numbers | `font-variant-numeric: tabular-nums` for columns |
| Loading | States end with `…`: "Loading…", "Saving…" |

---

## AI Prototyping Tools

### Stitch (Google Gemini)

Generate UI prototypes from text prompts via MCP.

```yaml
workflow:
  1. Create project: mcp_stitch_create_project
  2. Generate screen: mcp_stitch_generate_screen_from_text
     - Use GEMINI_3_PRO for high fidelity
     - Include design system colors in prompt
  3. Handle output_components (suggestions or code)
  4. Adapt to Tailwind v4 + shadcn/ui

prompt_template: |
  Create a [component type] for [purpose].
  Style: {from ui-ux-pro-max palette}
  Layout: [specific grid/flex requirements]
  Features: [interactive elements needed]
```

### Nano Banana Pro (Image Generation)

Generate assets using Gemini 3.0 Pro via `generate_image` tool.

```yaml
usage:
  - High-fidelity placeholders and mockups
  - UI illustrations and icons
  - Background patterns and gradients

best_practices:
  - Be specific about style, colors, dimensions
  - Reference design system palette
  - Request "clean, minimal, professional" for UI assets
```

---

## Quick Reference

### Component Checklist

- [ ] Uses shadcn/ui primitives (not custom buttons/modals)
- [ ] Client boundary at lowest possible level
- [ ] Parallel data fetching where applicable
- [ ] Visible focus states
- [ ] Respects `prefers-reduced-motion`
- [ ] Form inputs have `autocomplete` and `name`

### Import Pattern

```tsx
// UI Components
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

// Hooks
import { useState, useEffect } from "react";
import { trpc } from "@/lib/trpc";
```
