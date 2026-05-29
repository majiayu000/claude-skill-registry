---
name: project-context
description: Loads project structure, tech stack, and coding conventions for the Photography Order Management ERP. Use when understanding the codebase, onboarding, or needing project context.
---

# Project Context Skill

Provides quick access to project structure and conventions without reading full documentation.

## Tech Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Framework | React | 19.x |
| Build | Vite | 7.x |
| Styling | Tailwind CSS | 4.x |
| UI Library | HeroUI v3 Beta 3 | @heroui/react |
| Routing | TanStack Router | 1.x |
| Data | TanStack Query | 5.x |
| Icons | Iconify (lucide) | latest |

## Directory Structure

```text
src/
├── components/         # PascalCase: OrderInfo.tsx, ServiceConfigCard.tsx
├── data/               # kebab-case: mock-order.ts
├── hooks/              # camelCase: useOrder.ts, useProjectPage.ts
├── providers/          # QueryProvider.tsx
├── router.tsx          # TanStack Router configuration
├── App.tsx             # Entry point
└── index.css           # Tailwind v4 + HeroUI styles
```

## Key Conventions

1. **Named exports only**: `export function ComponentName() {}`
2. **HeroUI compound components**: `<Card.Content>`, `<Modal.Body>`
3. **Use `onPress`** for interactions (not `onClick`)
4. **Direct imports** from `@heroui/react` — no wrappers
5. **TanStack Router** for navigation: `<Link to="/path">`
6. **TanStack Query** for data: `useQuery({ queryKey, queryFn })`

## HeroUI MCP Tools

Before creating any UI component, use these tools:

- `mcp_heroui-react_list_components` — Check availability
- `mcp_heroui-react_get_component_info` — Understand anatomy
- `mcp_heroui-react_get_component_props` — Get TypeScript types
- `mcp_heroui-react_get_component_examples` — See correct patterns

## References

For full details, read these files:

- `dev_instruction_v3.md` — Primary source of truth
- `package.json` — All dependencies
- `.agent/workflows/onboarding.md` — Onboarding process
