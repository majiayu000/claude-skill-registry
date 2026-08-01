---
name: react-state-management
description: 'Apply when deciding state management approach: local state, context,
  Zustand for client state, or TanStack Query for server state.'
---

---
name: react-state-management
description: Apply when deciding state management approach: local state, context, Zustand for client state, or TanStack Query for server state.
version: 1.0.0
tokens: ~750
confidence: high
sources:
  - https://react.dev/learn/managing-state
  - https://zustand-demo.pmnd.rs/
  - https://tanstack.com/query/latest
last_validated: 2025-01-10
next_review: 2025-01-24
tags: [react, state, zustand, tanstack-query, frontend]
---

## When to Use

Apply when deciding state management approach: local state, context, Zustand for client state, or TanStack Query for server state.

## Patterns

### Pattern 1: State Location Decision
```
Where should state live?

Local (useState)
├── Form input values
├── UI state (open/closed, selected tab)
└── Single-component data

Lifted State (parent → children)
├── Shared between 2-3 siblings
└── Form with multiple sections

Context
├── Theme, locale, auth status
└── Rarely-changing global data

Zustand (client state)
├── Shopping cart
├── User preferences
└── Complex UI state shared across routes

TanStack Query (server state)
├── API data (fetching, caching)
├── Optimistic updates
└── Background refetching
```

### Pattern 2: Zustand Store
```typescript
// Source: https://zustand-demo.pmnd.rs/
import { create } from 'zustand';

interface CartStore {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  total: () => number;
}

const useCartStore = create<CartStore>((set, get) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
  removeItem: (id) => set((state) => ({
    items: state.items.filter((i) => i.id !== id),
  })),
  total: () => get().items.reduce((sum, i) => sum + i.price, 0),
}));

// Usage
const items = useCartStore((state) => state.items);
const addItem = useCartStore((state) => state.addItem);
```

### Pattern 3: TanStack Query for Server State
```typescript
// Source: https://tanstack.com/query/latest
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => fetch('/api/users').then((r) => r.json()),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

function useCreateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (user: NewUser) => fetch('/api/users', {
      method: 'POST',
      body: JSON.stringify(user),
    }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
  });
}
```

### Pattern 4: Context for Theme/Auth
```typescript
// Source: https://react.dev/learn/passing-data-deeply-with-context
const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be within AuthProvider');
  return ctx;
};
```

## Anti-Patterns

- **Everything in global state** - Start local, lift only when needed
- **API data in Zustand** - Use TanStack Query for server state
- **Prop drilling 5+ levels** - Use context or state library
- **Context for frequently changing data** - Causes full subtree re-renders

## Verification Checklist

- [ ] Server state uses TanStack Query (not useState)
- [ ] Client state uses Zustand if shared across routes
- [ ] Context only for stable, global data (theme, auth)
- [ ] No unnecessary global state
