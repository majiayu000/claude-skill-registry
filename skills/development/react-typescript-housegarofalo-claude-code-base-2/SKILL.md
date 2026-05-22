---
name: react-typescript
description: Build modern React applications with TypeScript. Covers React 18+ patterns, hooks, component architecture, state management (Zustand, Redux Toolkit), server components, and best practices. Use for React development, TypeScript integration, component design, and frontend architecture.
---

# React with TypeScript

Build production-ready React applications using TypeScript with modern patterns and best practices.

## Instructions

1. **Always use TypeScript** - Define proper types for props, state, and API responses
2. **Prefer functional components** - Use hooks over class components
3. **Follow component composition** - Build small, reusable, single-responsibility components
4. **Implement proper error boundaries** - Wrap critical UI sections
5. **Use React 18+ features** - Concurrent features, Suspense, transitions when appropriate

## Component Patterns

### Basic Component Structure

```tsx
import { useState, useCallback } from 'react';

interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary' | 'danger';
  disabled?: boolean;
  loading?: boolean;
}

export function Button({
  label,
  onClick,
  variant = 'primary',
  disabled = false,
  loading = false,
}: ButtonProps) {
  const handleClick = useCallback(() => {
    if (!disabled && !loading) {
      onClick();
    }
  }, [disabled, loading, onClick]);

  return (
    <button
      type="button"
      onClick={handleClick}
      disabled={disabled || loading}
      className={`btn btn-${variant}`}
      aria-busy={loading}
    >
      {loading ? <Spinner /> : label}
    </button>
  );
}
```

### Custom Hooks Pattern

```tsx
import { useState, useEffect, useCallback } from 'react';

interface UseApiResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => void;
}

function useApi<T>(url: string): UseApiResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const json = await response.json();
      setData(json);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setLoading(false);
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}
```

### Compound Component Pattern

```tsx
import { createContext, useContext, useState, ReactNode } from 'react';

interface AccordionContextType {
  openItems: Set<string>;
  toggle: (id: string) => void;
}

const AccordionContext = createContext<AccordionContextType | null>(null);

function useAccordion() {
  const context = useContext(AccordionContext);
  if (!context) throw new Error('Must be used within Accordion');
  return context;
}

interface AccordionProps {
  children: ReactNode;
  allowMultiple?: boolean;
}

export function Accordion({ children, allowMultiple = false }: AccordionProps) {
  const [openItems, setOpenItems] = useState<Set<string>>(new Set());

  const toggle = (id: string) => {
    setOpenItems(prev => {
      const next = new Set(allowMultiple ? prev : []);
      if (prev.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  return (
    <AccordionContext.Provider value={{ openItems, toggle }}>
      <div role="region">{children}</div>
    </AccordionContext.Provider>
  );
}

Accordion.Item = function AccordionItem({ id, title, children }: {
  id: string;
  title: string;
  children: ReactNode;
}) {
  const { openItems, toggle } = useAccordion();
  const isOpen = openItems.has(id);

  return (
    <div>
      <button
        onClick={() => toggle(id)}
        aria-expanded={isOpen}
        aria-controls={`panel-${id}`}
      >
        {title}
      </button>
      {isOpen && <div id={`panel-${id}`}>{children}</div>}
    </div>
  );
};
```

## State Management

### Zustand (Recommended for most cases)

```tsx
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface UserState {
  user: User | null;
  isAuthenticated: boolean;
  login: (user: User) => void;
  logout: () => void;
}

export const useUserStore = create<UserState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      login: (user) => set({ user, isAuthenticated: true }),
      logout: () => set({ user: null, isAuthenticated: false }),
    }),
    { name: 'user-storage' }
  )
);
```

### React Query for Server State

```tsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

function useTodos() {
  return useQuery({
    queryKey: ['todos'],
    queryFn: () => fetch('/api/todos').then(r => r.json()),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

function useAddTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (newTodo: Todo) =>
      fetch('/api/todos', {
        method: 'POST',
        body: JSON.stringify(newTodo),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });
}
```

## Project Structure

```
src/
├── components/
│   ├── ui/           # Reusable UI components
│   ├── features/     # Feature-specific components
│   └── layouts/      # Layout components
├── hooks/            # Custom hooks
├── stores/           # State management
├── services/         # API services
├── types/            # TypeScript types
├── utils/            # Utility functions
└── pages/            # Page components (if not using router)
```

## Best Practices

1. **Type everything** - No `any` types, use `unknown` if needed
2. **Memoize appropriately** - Use `useMemo`, `useCallback`, `React.memo` for expensive operations
3. **Handle loading/error states** - Every async operation needs these states
4. **Use proper keys** - Never use array index as key for dynamic lists
5. **Avoid prop drilling** - Use context or state management for deep prop passing
6. **Code split** - Use `React.lazy()` for route-level code splitting
7. **Test components** - Write unit tests with React Testing Library

## When to Use

- Building React applications with TypeScript
- Creating reusable component libraries
- Implementing complex state management
- Setting up new React projects
- Refactoring class components to functional

## Notes

- Requires React 18+ for latest features
- Use Vite for new projects (faster than CRA)
- Consider Next.js for SSR/SSG requirements
- Always include proper accessibility attributes
