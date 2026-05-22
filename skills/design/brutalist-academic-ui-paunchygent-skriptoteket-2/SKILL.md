---
name: brutalist-academic-ui
description: Skriptoteket-specific brutalist/academic UI design for the Vue 3 + Vite SPA. Uses Tailwind v4 utilities mapped to HuleEdu tokens and SPA primitives.
---

# Brutalist Academic UI

Opinionated design skill for interfaces where intellectual rigor, typographic precision, and structural honesty matter.

## Skriptoteket Compatibility (must follow)

- Vue 3 + Vite SPA only. SSR/HTMX is removed; do not re-introduce it.
- Tailwind CSS v4 with `@theme inline` token bridge. Prefer utilities in templates over custom CSS.
- Tokens are canonical: `src/skriptoteket/web/static/css/huleedu-design-tokens.css` (do not edit directly).
- SPA entry point: `frontend/apps/skriptoteket/src/assets/main.css` (import Tailwind + tokens + theme once).
- Use SPA primitives before inventing new ones:
  - Buttons: `.btn-primary`, `.btn-cta`, `.btn-ghost`
  - Panels (nested): `.panel-inset`, `.panel-inset-canvas`
  - Messages: `.toast-*` (via `ToastHost`), `.system-message*` (via `SystemMessage`)
  - Badges: `.status-pill`
  - Page text: `.page-title`, `.page-description`
- **No stacked brutal shadows**: only the outermost “panel/card” gets `shadow-brutal*`. Panels/fields nested inside a
  shadowed surface must use `shadow-none` + thicker, uniform borders (`panel-inset*`, or `border-2 border-navy/20`) to
  keep the UI calm and readable.
- No Tailwind default palette leakage in product UI: avoid `bg-slate-*`, `text-gray-*`, etc. Use token-mapped utilities
  (`bg-canvas`, `text-navy`, `shadow-brutal-sm`) or CSS variables (`var(--color-*)`, `var(--huleedu-*)`).
- Editor ergonomics: full-height editor routes require `min-h-0` + `overflow` discipline; follow the Script Editor
  layout patterns (`route-stage--editor`, `AuthLayout`).

## When to Use

Activate when user:
- Builds websites, landing pages, dashboards, documentation sites
- Needs institutional or academic visual language
- Mentions: "brutalist", "academic", "minimal", "serious UI"
- Wants to avoid generic startup aesthetics (gradients, soft shadows, pill-everything)

## I Need To...

| Task | Read |
|------|------|
| Token + Tailwind mapping rules | `.agent/rules/045-huleedu-design-system.md` |
| Tailwind v4 token bridge ADR | `docs/adr/adr-0032-tailwind-4-theme-tokens.md` |
| Canonical tokens | `src/skriptoteket/web/static/css/huleedu-design-tokens.css` |
| SPA token bridge | `frontend/apps/skriptoteket/src/styles/tokens.css` + `frontend/apps/skriptoteket/src/styles/tailwind-theme.css` |
| SPA primitives (buttons, toasts, system messages) | `frontend/apps/skriptoteket/src/assets/main.css` |
| Well-aligned editor layout example | `frontend/apps/skriptoteket/src/views/admin/ScriptEditorView.vue` |
| Workspace panel (IDE layout) | `frontend/apps/skriptoteket/src/components/editor/EditorWorkspacePanel.vue` |
| Grid/typography/color principles | [fundamentals.md](fundamentals.md) |
| Layout patterns | [patterns.md](patterns.md) |
| Components | [examples/components.md](examples/components.md) |
| Tables + ledgers | [examples/tables-ledgers.md](examples/tables-ledgers.md) |

## Quick Reference

### Do

- Use token-mapped utilities: `bg-canvas`, `text-navy`, `border-navy`, `shadow-brutal-sm`, `font-serif`.
- Use CSS variables when a token is not mapped: `p-[var(--huleedu-space-4)]`, `text-[var(--huleedu-text-sm)]`.
- Use the SPA button primitives for actions.
- Prefer opacity-only transitions (hard borders/shadows shimmer when translated).
- Prefer **one** brutal shadow per major surface (page card / editor workspace / modal). Nested sections get borders, not
  shadows.

### Avoid

- Tailwind default palette (`bg-slate-*`, `text-gray-*`) in product UI.
- Hardcoded hex colors or ad-hoc shadows.
- Large radii, blur/backdrop filters, or decorative gradients.
- Motion/hover transforms that distort “hard” edges (`translate`, `scale`) unless there’s a strong UX reason.

### Font Stack

Use token fonts via Tailwind utilities: `font-sans`, `font-serif`, `font-mono`.

### Button Primitives

```html
<button class="btn-primary">Spara</button>
<button class="btn-cta">Publicera</button>
<button class="btn-ghost">Redigera</button>
```

### Utility Buttons (Toolbars / Micro UI)

Use `.btn-ghost` as a base and override size/shadow for dense controls:

```html
<button
  class="btn-ghost shadow-none h-[28px] px-2.5 py-1 text-[10px] font-semibold normal-case tracking-[var(--huleedu-tracking-label)] border-navy/30 bg-canvas leading-none"
>
  Formatera
</button>
```

## Core Principle

The best interface is one where you notice the content, not the interface. Every element earns its place. Typography does the work. Whitespace is structure.
