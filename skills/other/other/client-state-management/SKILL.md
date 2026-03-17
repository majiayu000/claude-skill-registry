---
name: client-state-management
description: Guide for implementing client-side state management in React applications. Use when building state architecture, selecting state libraries (Context, Zustand, Redux, Jotai), implementing caching strategies (React Query, SWR), optimistic updates, state persistence, or optimizing re-renders. Triggers on questions about global vs local state, state normalization, or selector patterns.
---

# Client-Side State Management

## Decision: Library Selection

| Need | Use | Why |
|------|-----|-----|
| Simple shared state, <5 consumers | **Context API** | Zero dependencies, built-in |
| Medium complexity, performance matters | **Zustand** | 1.5kb, no boilerplate, auto re-render optimization |
| Large app, strict patterns needed | **Redux Toolkit** | DevTools, middleware ecosystem, time-travel |
| Fine-grained reactivity, atoms | **Jotai** | Bottom-up, minimal re-renders, composable |
| Server state (fetching/caching) | **React Query** or **SWR** | Deduplication, background refresh, cache |

## Decision: Global vs Local State

**Keep Local** (useState/useReducer):
- Form input values before submission
- UI state (open/closed, hover, focus)
- Component-specific loading/error states

**Promote to Global**:
- User session/auth
- Theme/locale preferences
- Data shared across 3+ unrelated components
- State that must survive navigation

## State Normalization

Flatten nested data to avoid update complexity:

```typescript
// Bad: nested
{ posts: [{ id: 1, author: { id: 1, name: 'Jo' }, comments: [...] }] }

// Good: normalized
{
  posts: { byId: { 1: { id: 1, authorId: 1, commentIds: [1,2] } }, allIds: [1] },
  users: { byId: { 1: { id: 1, name: 'Jo' } } },
  comments: { byId: { 1: {...}, 2: {...} } }
}
```

## Optimistic Updates Pattern

Update UI immediately, rollback on error:

```typescript
// React Query
useMutation({
  mutationFn: updateTodo,
  onMutate: async (newTodo) => {
    await queryClient.cancelQueries({ queryKey: ['todos'] })
    const previous = queryClient.getQueryData(['todos'])
    queryClient.setQueryData(['todos'], old => [...old, newTodo])
    return { previous }
  },
  onError: (err, newTodo, context) => {
    queryClient.setQueryData(['todos'], context.previous)
  },
  onSettled: () => queryClient.invalidateQueries({ queryKey: ['todos'] })
})
```

## State Persistence

```typescript
// Zustand with persist middleware
import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

const useStore = create(
  persist(
    (set) => ({ theme: 'light', setTheme: (t) => set({ theme: t }) }),
    {
      name: 'app-settings',
      storage: createJSONStorage(() => localStorage), // or sessionStorage
      partialize: (state) => ({ theme: state.theme }) // persist only specific keys
    }
  )
)
```

## Performance: Selector Patterns

Prevent unnecessary re-renders by selecting only needed state:

```typescript
// Zustand - component only re-renders when `count` changes
const count = useStore((state) => state.count)

// Jotai - selectAtom for derived slices
const nameAtom = selectAtom(userAtom, (user) => user.name)

// React Query - select option
useQuery({
  queryKey: ['user'],
  queryFn: fetchUser,
  select: (data) => data.name // component only gets name
})
```

## Reference Files

- **[zustand-patterns.md](references/zustand-patterns.md)**: Store setup, middleware composition, TypeScript patterns
- **[server-state.md](references/server-state.md)**: React Query/SWR configuration, caching strategies, mutation patterns
- **[context-patterns.md](references/context-patterns.md)**: Context setup, optimization techniques

## Performance Checklist

- [ ] Selectors return minimal data needed
- [ ] Memoize selectors with expensive computations
- [ ] Split stores by domain (don't put everything in one store)
- [ ] Use `shallow` comparison for object selections in Zustand
- [ ] Set appropriate `staleTime`/`cacheTime` for server state
- [ ] Avoid storing derived state (compute from source)
