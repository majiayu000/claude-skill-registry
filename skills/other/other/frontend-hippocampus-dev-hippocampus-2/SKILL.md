---
name: frontend
description: Frontend coding conventions using Preact and Tailwind. Use when writing or reviewing frontend JavaScript, HTML, or CSS code for web UI components.
keywords: preact, tailwind, frontend, フロントエンド, UI, コンポーネント, css, html
---

* Use Preact unless otherwise specified
* Use Tailwind unless otherwise specified

## Framework Selection

| Framework | When to Use |
|-----------|-------------|
| Next.js + shadcn/ui | `workers/` directory (Cloudflare Workers) |
| Preact + Tailwind | `cluster/applications/` static frontends |

## Preact

* Create elements with `h` function instead of JSX/TSX syntax

## Accessibility

| Framework | Approach |
|-----------|----------|
| shadcn/ui | Built-in accessibility via Radix UI primitives |
| Preact + Tailwind | Manual implementation required |

### Manual Accessibility Implementation

When not using shadcn/ui, ensure accessibility compliance:

| Element | Required |
|---------|----------|
| `<select>` | Associate with `<label>` using `for`/`id`, use `class: "sr-only"` if visual label not needed |
| `<input>` | Associate with `<label>` or use `aria-label` attribute |
| `<table>` headers | Use `<th scope="col">` or `<th scope="row">` |

Example (Preact):
```javascript
h("div", {class: "flex flex-col"}, [
    h("label", {for: "search-box", class: "sr-only"}, "Search"),
    h("select", {id: "search-box", ...}, [...]),
])
```
