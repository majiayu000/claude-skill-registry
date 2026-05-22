---
name: generic-react-feature-developer
description: Guide feature development for React applications with architecture focus. Covers Zustand/Redux patterns, IndexedDB usage, component systems, lazy loading strategies, and seamless integration. Use when adding new features, refactoring existing code, or planning major changes.
---

# React Feature Developer

Guide feature development with React architecture patterns.

**Extends:** [Generic Feature Developer](../generic-feature-developer/SKILL.md) - Read base skill for development workflow, scope assessment, and build vs integrate decisions.

## React Architecture

### Project Structure

```
src/
├── components/
│   ├── ui/          # Reusable primitives (Button, Input)
│   ├── features/    # Feature-specific components
│   └── layout/      # Layout components (Header, Sidebar)
├── hooks/           # Custom hooks (useAuth, useStore)
├── stores/          # Zustand stores
├── services/        # API clients, IndexedDB wrappers
├── types/           # TypeScript interfaces
└── lib/             # Utilities
```

## State Management Patterns

### Zustand Store (Preferred)

```typescript
// stores/useFeatureStore.ts
interface FeatureState {
  items: Item[];
  isLoading: boolean;
  // Actions
  addItem: (item: Item) => void;
  removeItem: (id: string) => void;
}

const useFeatureStore = create<FeatureState>()(
  persist(
    (set) => ({
      items: [],
      isLoading: false,
      addItem: (item) => set((s) => ({ items: [...s.items, item] })),
      removeItem: (id) =>
        set((s) => ({
          items: s.items.filter((i) => i.id !== id),
        })),
    }),
    {
      name: "feature-storage",
      version: 1,
      migrate: (state, version) => {
        // Handle migrations between versions
        return state as FeatureState;
      },
    },
  ),
);
```

### Zustand Selectors (Performance)

```typescript
// Avoid re-renders with selectors
const items = useFeatureStore((state) => state.items);
const addItem = useFeatureStore((state) => state.addItem);

// Shallow compare for objects
import { shallow } from "zustand/shallow";
const { items, isLoading } = useFeatureStore(
  (state) => ({ items: state.items, isLoading: state.isLoading }),
  shallow,
);
```

### Context vs Zustand Decision

| Use Context                    | Use Zustand                |
| ------------------------------ | -------------------------- |
| Theme, locale (rarely changes) | Frequently updated data    |
| Authentication state           | Complex state with actions |
| Provider already exists        | Need persistence           |
| Prop drilling 1-2 levels       | Cross-cutting concern      |

## Server State (React Query)

```typescript
// Server state - React Query
const { data, isLoading, error } = useQuery({
  queryKey: ["items", userId],
  queryFn: () => fetchItems(userId),
  staleTime: 5 * 60 * 1000, // 5 minutes
});

// Mutations
const mutation = useMutation({
  mutationFn: createItem,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ["items"] });
  },
});
```

## IndexedDB Integration

### When to Use

| Scenario                    | Solution                         |
| --------------------------- | -------------------------------- |
| < 5MB total                 | localStorage via Zustand persist |
| > 5MB total                 | IndexedDB                        |
| Binary data (images, files) | IndexedDB                        |
| Simple key-value            | localStorage                     |
| Complex queries             | IndexedDB                        |

### Service Wrapper Pattern

```typescript
// services/indexedDBService.ts
class IndexedDBService {
  private db: IDBDatabase | null = null;

  async init() {
    return new Promise<void>((resolve, reject) => {
      const request = indexedDB.open("AppDB", 1);
      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        resolve();
      };
      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;
        db.createObjectStore("items", { keyPath: "id" });
      };
    });
  }

  async setItem<T>(store: string, value: T): Promise<void> {
    // Implementation
  }

  async getItem<T>(store: string, key: string): Promise<T | null> {
    // Implementation
  }
}

export const indexedDBService = new IndexedDBService();
```

## Lazy Loading

### Component Lazy Loading

```typescript
// Heavy components (>20KB)
const HeavyChart = lazy(() => import('./HeavyChart'));
const RichTextEditor = lazy(() => import('./RichTextEditor'));

// Pages
const SettingsPage = lazy(() => import('./pages/Settings'));

// Usage with Suspense
<Suspense fallback={<Skeleton />}>
  <HeavyChart data={data} />
</Suspense>
```

### Route-Level Code Splitting

```typescript
// React Router example
const routes = [
  {
    path: '/dashboard',
    element: <DashboardLayout />,
    children: [
      {
        path: 'settings',
        lazy: () => import('./pages/Settings'),
      },
    ],
  },
];
```

## Custom Hook Patterns

### Feature Hook

```typescript
// hooks/useItems.ts
function useItems() {
  const items = useFeatureStore((s) => s.items);
  const addItem = useFeatureStore((s) => s.addItem);

  const sortedItems = useMemo(
    () => [...items].sort((a, b) => b.createdAt - a.createdAt),
    [items],
  );

  return { items: sortedItems, addItem };
}
```

### Compound Hook (Combining Sources)

```typescript
// hooks/useDashboard.ts
function useDashboard() {
  // Local state
  const [filter, setFilter] = useState("all");

  // Server state
  const { data: items } = useQuery({ queryKey: ["items"] });

  // Client state
  const preferences = usePreferencesStore((s) => s.dashboard);

  // Derived
  const filteredItems = useMemo(
    () => items?.filter((i) => filter === "all" || i.status === filter),
    [items, filter],
  );

  return { filter, setFilter, items: filteredItems, preferences };
}
```

## Component Composition

### Compound Components

```tsx
// Usage: <Tabs><Tabs.List /><Tabs.Panel /></Tabs>
const TabsContext = createContext<TabsContextValue | null>(null);

function Tabs({ children, defaultValue }: TabsProps) {
  const [active, setActive] = useState(defaultValue);
  return (
    <TabsContext.Provider value={{ active, setActive }}>
      {children}
    </TabsContext.Provider>
  );
}

Tabs.List = function TabsList({ children }: { children: ReactNode }) {
  return <div role="tablist">{children}</div>;
};

Tabs.Panel = function TabsPanel({ value, children }: TabsPanelProps) {
  const { active } = useContext(TabsContext)!;
  if (value !== active) return null;
  return <div role="tabpanel">{children}</div>;
};
```

## React Feature Checklist

**Before Starting:**

- [ ] Read CLAUDE.md for project patterns
- [ ] Check existing components for reuse
- [ ] Plan state management approach
- [ ] Estimate bundle size impact

**During Development:**

- [ ] Follow project design system
- [ ] TypeScript strict mode
- [ ] Implement keyboard navigation
- [ ] Add ARIA labels
- [ ] Support dark mode

**Before Completion:**

- [ ] Write unit tests
- [ ] Lazy load heavy components
- [ ] Check bundle size: `npm run build`
- [ ] Review with code-reviewer skill

## See Also

- [Generic Feature Developer](../generic-feature-developer/SKILL.md) - Workflow, decisions
- [Code Review Standards](../_shared/CODE_REVIEW_STANDARDS.md) - Quality requirements
- [Design Patterns](../_shared/DESIGN_PATTERNS.md) - UI patterns
