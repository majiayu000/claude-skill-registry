---
name: zustand-store
description: Create Zustand stores for IntelliFill with immer, persist, and devtools middleware. Use when adding state management for new features.
---

# Zustand Store Development Skill

This skill provides comprehensive guidance for creating Zustand stores in the IntelliFill frontend (`quikadmin-web/`).

## Table of Contents

1. [Store Architecture](#store-architecture)
2. [Basic Store Pattern](#basic-store-pattern)
3. [Middleware Stack](#middleware-stack)
4. [Selectors and Hooks](#selectors-and-hooks)
5. [Async Actions](#async-actions)
6. [Persistence](#persistence)
7. [Testing Stores](#testing-stores)
8. [Best Practices](#best-practices)

## Store Architecture

IntelliFill organizes Zustand stores by domain:

```
quikadmin-web/src/stores/
├── authStore.ts              # Authentication state
├── documentStore.ts          # Document management
├── templateStore.ts          # Template management
├── knowledgeStore.ts         # Knowledge base
├── uiStore.ts                # UI state (modals, sidebar, etc.)
└── __tests__/                # Store tests
    ├── documentStore.test.ts
    └── ...
```

## Basic Store Pattern

IntelliFill uses a consistent pattern for all stores.

### Simple Store Template

```typescript
// quikadmin-web/src/stores/[domain]Store.ts
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';
import { devtools } from 'zustand/middleware';

// Types
interface Item {
  id: string;
  name: string;
  createdAt: string;
}

interface DomainState {
  // Data
  items: Item[];
  selectedItem: Item | null;

  // UI State
  loading: boolean;
  error: string | null;

  // Actions
  fetchItems: () => Promise<void>;
  getItem: (id: string) => Promise<void>;
  createItem: (data: Partial<Item>) => Promise<void>;
  updateItem: (id: string, data: Partial<Item>) => Promise<void>;
  deleteItem: (id: string) => Promise<void>;
  setSelectedItem: (item: Item | null) => void;
  clearError: () => void;
}

// Store
export const useDomainStore = create<DomainState>()(
  devtools(
    immer((set, get) => ({
      // Initial state
      items: [],
      selectedItem: null,
      loading: false,
      error: null,

      // Actions
      fetchItems: async () => {
        set({ loading: true, error: null });
        try {
          const response = await api.get('/domain');
          set({ items: response.data, loading: false });
        } catch (error) {
          set({
            error: 'Failed to fetch items',
            loading: false,
          });
        }
      },

      getItem: async (id: string) => {
        set({ loading: true, error: null });
        try {
          const response = await api.get(`/domain/${id}`);
          set({ selectedItem: response.data, loading: false });
        } catch (error) {
          set({
            error: 'Failed to fetch item',
            loading: false,
          });
        }
      },

      createItem: async (data: Partial<Item>) => {
        set({ loading: true, error: null });
        try {
          const response = await api.post('/domain', data);
          set((state) => {
            state.items.push(response.data);
            state.loading = false;
          });
        } catch (error) {
          set({
            error: 'Failed to create item',
            loading: false,
          });
          throw error;
        }
      },

      updateItem: async (id: string, data: Partial<Item>) => {
        set({ loading: true, error: null });
        try {
          const response = await api.patch(`/domain/${id}`, data);
          set((state) => {
            const index = state.items.findIndex((item) => item.id === id);
            if (index !== -1) {
              state.items[index] = response.data;
            }
            if (state.selectedItem?.id === id) {
              state.selectedItem = response.data;
            }
            state.loading = false;
          });
        } catch (error) {
          set({
            error: 'Failed to update item',
            loading: false,
          });
          throw error;
        }
      },

      deleteItem: async (id: string) => {
        set({ loading: true, error: null });
        try {
          await api.delete(`/domain/${id}`);
          set((state) => {
            state.items = state.items.filter((item) => item.id !== id);
            if (state.selectedItem?.id === id) {
              state.selectedItem = null;
            }
            state.loading = false;
          });
        } catch (error) {
          set({
            error: 'Failed to delete item',
            loading: false,
          });
          throw error;
        }
      },

      setSelectedItem: (item: Item | null) => {
        set({ selectedItem: item });
      },

      clearError: () => {
        set({ error: null });
      },
    })),
    { name: 'DomainStore' }
  )
);
```

## Middleware Stack

IntelliFill uses three middleware layers: immer, persist, and devtools.

### Middleware Order

```typescript
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';
import { persist } from 'zustand/middleware';
import { devtools } from 'zustand/middleware';

// Correct order: devtools(persist(immer(...)))
export const useStore = create<State>()(
  devtools(
    persist(
      immer((set, get) => ({
        // Store implementation
      })),
      {
        name: 'store-name',
      }
    ),
    { name: 'StoreName' }
  )
);
```

### Immer Middleware

Immer allows direct state mutation (safely):

```typescript
import { immer } from 'zustand/middleware/immer';

export const useStore = create<State>()(
  immer((set, get) => ({
    items: [],

    // WITHOUT immer (immutable updates)
    addItemOld: (item) => {
      set((state) => ({
        items: [...state.items, item],
      }));
    },

    // WITH immer (mutable style)
    addItem: (item) => {
      set((state) => {
        state.items.push(item); // Direct mutation!
      });
    },

    // Nested updates are easier
    updateNested: (id, value) => {
      set((state) => {
        const item = state.items.find((i) => i.id === id);
        if (item) {
          item.nested.deeply.value = value; // Easy!
        }
      });
    },
  }))
);
```

### Persist Middleware

Persist store state to localStorage:

```typescript
import { persist } from 'zustand/middleware';

export const useStore = create<State>()(
  persist(
    immer((set, get) => ({
      items: [],
      preferences: {},
    })),
    {
      name: 'domain-storage', // localStorage key

      // Partial persistence (only save specific fields)
      partialPersist: {
        preferences: true, // Save preferences
        items: false, // Don't save items
      },

      // Version for migrations
      version: 1,

      // Migration function
      migrate: (persistedState: any, version: number) => {
        if (version === 0) {
          // Migrate from v0 to v1
          persistedState.newField = 'default';
        }
        return persistedState;
      },
    }
  )
);
```

### Devtools Middleware

Enable Redux DevTools integration:

```typescript
import { devtools } from 'zustand/middleware';

export const useStore = create<State>()(
  devtools(
    immer((set, get) => ({
      count: 0,

      increment: () => {
        set((state) => {
          state.count++;
        }, false, 'increment'); // Action name in devtools
      },

      decrement: () => {
        set((state) => {
          state.count--;
        }, false, { type: 'decrement', payload: -1 }); // Detailed action
      },
    })),
    {
      name: 'CounterStore', // Store name in devtools
      enabled: process.env.NODE_ENV === 'development', // Only in dev
    }
  )
);
```

## Selectors and Hooks

Optimize re-renders with selectors.

### Basic Selectors

```typescript
// Component re-renders only when items change
function ItemList() {
  const items = useDomainStore((state) => state.items);

  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
}

// Component re-renders only when loading changes
function LoadingIndicator() {
  const loading = useDomainStore((state) => state.loading);

  if (!loading) return null;
  return <Spinner />;
}
```

### useShallow for Multiple Values

```typescript
import { useShallow } from 'zustand/react/shallow';

// BAD: Re-renders when ANY store property changes
function Component() {
  const { items, loading, error } = useDomainStore();
  // ...
}

// GOOD: Re-renders only when items, loading, or error change
function Component() {
  const { items, loading, error } = useDomainStore(
    useShallow((state) => ({
      items: state.items,
      loading: state.loading,
      error: state.error,
    }))
  );
  // ...
}
```

### Custom Selector Hooks

```typescript
// quikadmin-web/src/stores/domainStore.ts

// Export selector hooks for common patterns
export const useDomainItems = () =>
  useDomainStore((state) => state.items);

export const useDomainLoading = () =>
  useDomainStore((state) => state.loading);

export const useDomainError = () =>
  useDomainStore((state) => state.error);

export const useDomainActions = () =>
  useDomainStore(
    useShallow((state) => ({
      fetchItems: state.fetchItems,
      createItem: state.createItem,
      updateItem: state.updateItem,
      deleteItem: state.deleteItem,
    }))
  );

// Usage in components
function ItemList() {
  const items = useDomainItems();
  const { createItem, deleteItem } = useDomainActions();

  // Component only re-renders when items or actions change
}
```

### Derived State

```typescript
export const useDomainStore = create<DomainState>()(
  immer((set, get) => ({
    items: [],
    filter: '',

    // Computed/derived state
    get filteredItems() {
      const { items, filter } = get();
      if (!filter) return items;
      return items.filter((item) =>
        item.name.toLowerCase().includes(filter.toLowerCase())
      );
    },

    setFilter: (filter: string) => {
      set({ filter });
    },
  }))
);

// Usage
function FilteredList() {
  const filteredItems = useDomainStore((state) => state.filteredItems);
  return <ul>{filteredItems.map(...)}</ul>;
}
```

## Async Actions

Handle async operations with proper loading and error states.

### Async Action Pattern

```typescript
export const useDomainStore = create<DomainState>()(
  immer((set, get) => ({
    items: [],
    loading: false,
    error: null,

    fetchItems: async () => {
      // Set loading state
      set({ loading: true, error: null });

      try {
        // API call
        const response = await api.get('/domain');

        // Update state on success
        set({
          items: response.data,
          loading: false,
        });
      } catch (error) {
        // Handle error
        set({
          error: error instanceof Error ? error.message : 'Unknown error',
          loading: false,
        });

        // Optionally rethrow for component handling
        throw error;
      }
    },
  }))
);
```

### Optimistic Updates

```typescript
updateItem: async (id: string, data: Partial<Item>) => {
  // Save original state for rollback
  const originalItems = get().items;

  // Optimistic update
  set((state) => {
    const item = state.items.find((i) => i.id === id);
    if (item) {
      Object.assign(item, data);
    }
  });

  try {
    // API call
    const response = await api.patch(`/domain/${id}`, data);

    // Update with server response
    set((state) => {
      const item = state.items.find((i) => i.id === id);
      if (item) {
        Object.assign(item, response.data);
      }
    });
  } catch (error) {
    // Rollback on error
    set({ items: originalItems, error: 'Failed to update item' });
    throw error;
  }
},
```

### Debounced Actions

```typescript
import { debounce } from 'lodash-es';

export const useDomainStore = create<DomainState>()(
  immer((set, get) => ({
    searchQuery: '',
    searchResults: [],

    // Create debounced function outside of the store
    searchItems: debounce(async (query: string) => {
      if (!query) {
        set({ searchResults: [] });
        return;
      }

      set({ loading: true });
      try {
        const response = await api.get('/domain/search', { params: { q: query } });
        set({ searchResults: response.data, loading: false });
      } catch (error) {
        set({ error: 'Search failed', loading: false });
      }
    }, 300),

    setSearchQuery: (query: string) => {
      set({ searchQuery: query });
      get().searchItems(query); // Trigger debounced search
    },
  }))
);
```

## Persistence

Configure localStorage persistence for user preferences.

### Persist Configuration

```typescript
import { persist, createJSONStorage } from 'zustand/middleware';

export const usePreferencesStore = create<PreferencesState>()(
  persist(
    immer((set) => ({
      theme: 'light',
      language: 'en',
      sidebarCollapsed: false,

      setTheme: (theme) => set({ theme }),
      setLanguage: (language) => set({ language }),
      toggleSidebar: () =>
        set((state) => {
          state.sidebarCollapsed = !state.sidebarCollapsed;
        }),
    })),
    {
      name: 'user-preferences',
      storage: createJSONStorage(() => localStorage),

      // Only persist specific fields
      partialPersist: {
        theme: true,
        language: true,
        sidebarCollapsed: true,
      },
    }
  )
);
```

### Session Storage

```typescript
import { createJSONStorage } from 'zustand/middleware';

export const useSessionStore = create<SessionState>()(
  persist(
    immer((set) => ({
      // Session-only data
    })),
    {
      name: 'session-data',
      storage: createJSONStorage(() => sessionStorage), // Use sessionStorage
    }
  )
);
```

### Migration Example

```typescript
persist(
  immer((set) => ({
    // Store implementation
  })),
  {
    name: 'domain-storage',
    version: 2, // Current version

    migrate: (persistedState: any, version: number) => {
      // Migrate from v0 to v1
      if (version === 0) {
        persistedState.newField = 'default';
      }

      // Migrate from v1 to v2
      if (version === 1) {
        persistedState.renamedField = persistedState.oldField;
        delete persistedState.oldField;
      }

      return persistedState;
    },
  }
);
```

## Testing Stores

Test stores in isolation with mocked dependencies.

### Basic Store Test

```typescript
// quikadmin-web/src/stores/__tests__/domainStore.test.ts
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useDomainStore } from '../domainStore';
import * as api from '@/services/api';

// Mock API
vi.mock('@/services/api', () => ({
  api: {
    get: vi.fn(),
    post: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('useDomainStore', () => {
  beforeEach(() => {
    // Reset store state before each test
    useDomainStore.setState({
      items: [],
      loading: false,
      error: null,
    });
    vi.clearAllMocks();
  });

  it('fetches items successfully', async () => {
    const mockItems = [
      { id: '1', name: 'Item 1' },
      { id: '2', name: 'Item 2' },
    ];

    vi.mocked(api.api.get).mockResolvedValue({ data: mockItems });

    const { result } = renderHook(() => useDomainStore());

    await act(async () => {
      await result.current.fetchItems();
    });

    expect(result.current.items).toEqual(mockItems);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
  });

  it('handles fetch error', async () => {
    vi.mocked(api.api.get).mockRejectedValue(new Error('Network error'));

    const { result } = renderHook(() => useDomainStore());

    await act(async () => {
      try {
        await result.current.fetchItems();
      } catch (error) {
        // Expected to throw
      }
    });

    expect(result.current.items).toEqual([]);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeTruthy();
  });

  it('creates item', async () => {
    const newItem = { id: '1', name: 'New Item' };
    vi.mocked(api.api.post).mockResolvedValue({ data: newItem });

    const { result } = renderHook(() => useDomainStore());

    await act(async () => {
      await result.current.createItem({ name: 'New Item' });
    });

    expect(result.current.items).toContainEqual(newItem);
  });
});
```

### Testing Selectors

```typescript
it('returns filtered items', () => {
  const { result } = renderHook(() => useDomainStore());

  act(() => {
    useDomainStore.setState({
      items: [
        { id: '1', name: 'Apple' },
        { id: '2', name: 'Banana' },
        { id: '3', name: 'Apricot' },
      ],
      filter: 'ap',
    });
  });

  expect(result.current.filteredItems).toHaveLength(2);
  expect(result.current.filteredItems[0].name).toBe('Apple');
  expect(result.current.filteredItems[1].name).toBe('Apricot');
});
```

## Best Practices

1. **Use TypeScript interfaces** - Type all store state and actions
2. **Middleware order matters** - devtools → persist → immer
3. **Use immer for nested updates** - Simplifies complex state updates
4. **Select only what you need** - Use selectors to prevent unnecessary re-renders
5. **Use useShallow for objects** - Shallow comparison for multiple values
6. **Handle loading and errors** - Always track async operation states
7. **Optimize with derived state** - Use getters for computed values
8. **Test stores in isolation** - Mock API calls and dependencies
9. **Persist user preferences only** - Don't persist transient data
10. **Use action naming** - Name actions for Redux DevTools

## Common Patterns

### Store Composition

```typescript
// Combine multiple stores in a component
function Component() {
  const documents = useDocumentStore((state) => state.documents);
  const templates = useTemplateStore((state) => state.templates);
  const { user } = useAuthStore();

  // Use data from multiple stores
}
```

### Store Subscription

```typescript
import { useEffect } from 'react';

function Component() {
  useEffect(() => {
    // Subscribe to store changes
    const unsubscribe = useDomainStore.subscribe(
      (state) => state.items,
      (items) => {
        console.log('Items changed:', items);
      }
    );

    return unsubscribe;
  }, []);
}
```

### Reset Store

```typescript
export const useDomainStore = create<DomainState>()(
  immer((set) => ({
    items: [],
    loading: false,

    reset: () => {
      set({
        items: [],
        loading: false,
        error: null,
      });
    },
  }))
);
```

## References

- [Zustand Documentation](https://github.com/pmndrs/zustand)
- [Immer Documentation](https://immerjs.github.io/immer/)
- [React Testing Library](https://testing-library.com/react)
- [Vitest](https://vitest.dev/)
