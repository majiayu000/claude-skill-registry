---
name: web-modules
description: (ePost) Use when integrating a component into a B2B module — adding screens, binding APIs, wiring stores, setting up routes
user-invocable: false

metadata:
  agent-affinity: [epost-fullstack-developer]
  keywords: [integrate, module, screen, page, api, store, hook, bind]
  platforms: [web]
  triggers: ["add to module", "integrate into", "create screen", "add page", "bind api"]
  connections:
    enhances: [web-frontend]
---

# Module Integration Skill

## Purpose

Patterns for integrating components into B2B modules with proper API binding, state management, routing, and design system compliance.

## Reference Files

| File | Purpose |
|------|---------|
| `references/module-scaffold.md` | File creation order for new features |
| `references/api-binding.md` | Component -> Hook -> Action -> Service pattern |
| `references/store-pattern.md` | Redux Toolkit slice creation |
| `references/routing.md` | Next.js App Router module routing |
| `references/consistency-checklist.md` | Design system compliance checklist |

## Integration Workflow

1. Read `module-scaffold.md` — understand file creation order
2. Create types in `_ui-models/`
3. Create service in `_services/`
4. Create actions in `_actions/`
5. Create hooks in `_hooks/`
6. Create store slice in `_stores/`
7. Create components in `_components/`
8. Wire up in `page.tsx`
9. Run `consistency-checklist.md`

## Related Skills

- `web-prototype` — Converting external code
- `domain-b2b` — Module knowledge
- `web-ui-lib` — Component reference
- `web-nextjs` — App Router patterns
