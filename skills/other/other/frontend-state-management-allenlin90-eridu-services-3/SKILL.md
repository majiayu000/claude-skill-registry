---
name: frontend-state-management
description: Provides comprehensive state management patterns for React applications. This skill should be used when deciding how to manage different types of state, choosing state management solutions, or implementing state logic.
---

# Frontend State Management

This skill provides patterns for managing state in React applications.

## Canonical Examples

Study these real implementations:
- **URL State**: [use-table-url-state.ts](../../../packages/ui/src/hooks/use-table-url-state.ts)
- **Feature Hook**: [use-task-templates.ts](../../../apps/erify_studios/src/features/task-templates/hooks/use-task-templates.ts)

---

## State Categories

### 1. Server State (TanStack Query)

**Use for**: Data from APIs that needs caching, synchronization, and background updates.

```typescript
import { useQuery, useMutation } from '@tanstack/react-query';

// ✅ GOOD: Server state managed by TanStack Query
const { data, isLoading } = useQuery({
  queryKey: ['tasks', taskId],
  queryFn: () => fetchTask(taskId),
});
```

**Key Points**:
- ✅ Automatic caching and deduplication
- ✅ Background refetching
- ✅ Optimistic updates via mutations

### 2. URL State (TanStack Router)

**Use for**: Filters, pagination, search queries, tabs - anything that should be shareable via URL.

```typescript
import { useTableUrlState } from '@eridu/ui';

// ✅ GOOD: URL state for filters and search
const { columnFilters, onColumnFiltersChange } = useTableUrlState({
  from: '/studios/$studioId/tasks',
  searchColumnId: 'name',
});
```

**Key Points**:
- ✅ Shareable links
- ✅ Browser back/forward support
- ✅ Persists across page reloads

### 3. Local Component State (useState)

**Use for**: UI state that doesn't need to be shared (modals, dropdowns, form inputs).

```typescript
// ✅ GOOD: Local UI state
const [isOpen, setIsOpen] = useState(false);
const [searchInput, setSearchInput] = useState('');
```

### 4. Global Client State (Zustand)

**Use for**: Truly global state like auth user, theme, sidebar state.

```typescript
import { create } from 'zustand';

// ✅ GOOD: Global auth state
export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  logout: () => set({ user: null }),
}));
```

---

## Decision Tree

```
Is it from an API?
├─ YES → TanStack Query (server state)
└─ NO → Should it be in the URL?
    ├─ YES → TanStack Router search params (URL state)
    └─ NO → Does it need to be global?
        ├─ YES → Zustand (global client state)
        └─ NO → useState (local component state)
```

---

## Common Patterns

### Debounced Search with URL Sync

```typescript
const [localSearch, setLocalSearch] = useState('');
const debouncedSearch = useDebounce(localSearch, 300);

useEffect(() => {
  onColumnFiltersChange((old) => {
    const newFilters = old.filter((f) => f.id !== 'name');
    if (debouncedSearch) newFilters.push({ id: 'name', value: debouncedSearch });
    return newFilters;
  });
}, [debouncedSearch]);
```

### Optimistic Updates

```typescript
const mutation = useMutation({
  mutationFn: updateTask,
  onMutate: async (newTask) => {
    await queryClient.cancelQueries({ queryKey: ['tasks'] });
    const previous = queryClient.getQueryData(['tasks']);
    queryClient.setQueryData(['tasks'], (old) => [...old, newTask]);
    return { previous };
  },
  onError: (err, newTask, context) => {
    queryClient.setQueryData(['tasks'], context.previous);
  },
});
```

---

## Best Practices Checklist

- [ ] Server state managed by TanStack Query
- [ ] Filters/search/pagination in URL state
- [ ] Local UI state uses useState
- [ ] Global state uses Zustand (minimal usage)
- [ ] Debounced search with URL synchronization
- [ ] Optimistic updates for mutations
- [ ] Query invalidation on mutations

---

## Related Skills

- [frontend-api-layer](../frontend-api-layer/SKILL.md) - API integration patterns
- [studio-list-pattern](../studio-list-pattern/SKILL.md) - List state management
