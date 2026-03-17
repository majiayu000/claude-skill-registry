---
name: components
description: UI component patterns for React 19, shadcn/ui, and Tailwind. Use when working on files in src/components/.
---

# Components Guidelines

## Patterns

- `"use client"` only if using hooks/interactivity
- Export interface with `Props` suffix, document props with JSDoc
- Always include optional `className` prop, use `cn()` for merging

## Styling

- Tailwind only - no CSS modules or styled-components
- Use shadcn/ui tokens: `text-muted-foreground`, `bg-background`, etc.
- All components must support dark mode via `dark:` prefix

## State

- **Local**: `useState` for UI-only state (dropdowns, modals)
- **CRDT**: `useVaultAction`/`useActiveTransactions` for data mutations
- **URL**: `useSearchParams` for filters that should persist

## Performance

- `useMemo`/`useCallback` for expensive computations and callbacks to memoized children
- Virtualize long lists (TransactionTable already does this)
- Avoid inline object/array literals in JSX props

## Accessibility

- Semantic HTML, aria-labels on icon-only buttons
- Keyboard navigation, focus management in modals
