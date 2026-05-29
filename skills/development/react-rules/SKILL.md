---
name: react-rules
description: React and component patterns
user-invocable: false
---

# React Rules

## Components
- Use named exports, not default exports: `export function AgentCard() {}`
- One component per file for route-level components
- Co-locate small helper components in the same file
- Use `className` with Tailwind — no CSS modules or styled-components

## Data Fetching
- Use TanStack Query (`useQuery`, `useSuspenseQuery`) for all data fetching
- Server Functions for mutations via `useMutation`
- Never use `useEffect` for data fetching
- Prefetch on the server with `queryClient.prefetchQuery` in route loaders

## State
- URL state first (search params via TanStack Router)
- Server state via TanStack Query (no Redux, no Zustand)
- Local UI state only with `useState` — keep it minimal
- Form state with controlled components or `useForm`

## Patterns
- Suspense boundaries at route level, not per-component
- Error boundaries for slice-level error handling
- Compose with props, not render props or HOCs
- Use shadcn/ui components — don't build custom UI primitives

## File Naming
- Route files: `route.tsx` (TanStack Router file-based routing)
- UI components: `PascalCase.tsx` or grouped in `ui.tsx` within a slice
- Hooks: `use-kebab-case.ts` (must start with `use` prefix — enforced by architecture tests)

## Slice Boundaries (enforced by automated tests)
- Never import a component from another feature's `ui/` directory directly
- Shared UI primitives go in `src/components/ui/` (shadcn convention)
- Cross-slice data: import hooks/types from the other slice's `model.ts` facade, not from internal files
- Route files must be thin — compose from slice hooks and components, don't import from `domain/` or `infra/` directly
- Example: `import { useAgents } from '@/features/registry/model'` (correct) vs `import { useAgents } from '@/features/registry/hooks/useAgents'` (wrong from outside registry)
