---
name: web-prototype
description: (ePost) Use when converting an external prototype, mockup, or codebase into production code with your design system
user-invocable: false

metadata:
  agent-affinity: [epost-fullstack-developer]
  keywords: [convert, prototype, migrate, rewrite, transform, external, mockup]
  platforms: [web]
  triggers: ["/convert", "convert to klara-theme", "make it consistent"]
  connections:
    enhances: [convert]
---

# Prototype Conversion Skill

## Purpose

Convert external prototypes, mockups, or codebases into production-ready code using your design system components, semantic design tokens, and proper module architecture.

## Reference Files

| File | Purpose |
|------|---------|
| `references/analysis-checklist.md` | Prototype inventory and framework detection |
| `references/component-mapping.md` | Map common patterns to klara-theme equivalents |
| `references/token-mapping.md` | Map hardcoded values to klara-theme tokens |
| `references/style-migration.md` | Migrate style systems to klara-theme |
| `references/data-migration.md` | Replace mock data with real API integration |

## Conversion Workflow

1. **Analyze** — Read `analysis-checklist.md`, inventory prototype
2. **Map Components** — Read `component-mapping.md`, map to klara-theme
3. **Map Tokens** — Read `token-mapping.md`, replace hardcoded values
4. **Migrate Styles** — Read `style-migration.md`, convert style system
5. **Integrate Data** — Read `data-migration.md`, replace mock data
6. **Module Structure** — Place in correct module with `_components/` etc.

## Quick Reference

- Import: `@luz-next/klara-theme`
- Props: `styling` (not `variant`), `size`, `mode`, `radius`
- Tokens: `bg-base-background`, `p-200`, `gap-100`
- Data flow: Component -> Hook -> Action -> Service -> API

## Related Skills

- `web-modules` — Module integration patterns
- `web-ui-lib` — klara-theme component reference
- `domain-b2b` — Module knowledge
