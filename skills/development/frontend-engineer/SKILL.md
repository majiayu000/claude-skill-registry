---
name: frontend-engineer
description: Expert in Template Project frontend architecture, React patterns, TypeScript, TanStack Query, Zustand, and component development with strong type safety. Use when building UI components, implementing data fetching, managing state, writing forms, styling with Tailwind, testing React components, or integrating with backend APIs.
---

# Template Frontend Engineer

Expert knowledge of frontend patterns and architecture for the Template Project.

## Core Architecture

### Technology Stack

- **Framework**: React 18 with TypeScript
- **State Management**:
  - **Server State**: TanStack Query (React Query)
  - **Client State**: Zustand with Immer middleware
- **Styling**: Tailwind CSS + lucide-react icons
- **Forms**: react-hook-form + Zod validation
- **Testing**: Vitest + React Testing Library + MSW v2
- **HTTP Client**: Custom fetch wrapper with credentials

### Data Flow Architecture

```
Component (React)
    |
State Decision:
├── Server Data -> TanStack Query Hook -> API Service -> fetch
|                      |
|                 Type-Safe Response (@todos/schema/api)
|
└── UI State -> Zustand Store (with Immer)
    |
Type-Safe Types (from @todos/schema)
```

**Key Flow:**

1. Component calls TanStack Query hook or Zustand store
2. Hook uses API service layer
3. Request/Response types from `@todos/schema/src/api/`
4. UI state (selections, UI flags) in Zustand
5. Server state (data, caching) in TanStack Query

## CRITICAL: Where to Look Before Making Changes

### Pattern References (ALWAYS CHECK THESE FIRST)

| Pattern                          | Primary Reference                           | Notes                          |
| -------------------------------- | ------------------------------------------- | ------------------------------ |
| **Reusable Components**          | `packages/components/src/`                  | **ALWAYS CHECK FIRST**         |
| **API Types (Request/Response)** | `packages/schema/src/api/`                  | **CHECK HERE FIRST**           |
| **API Service Layer**            | `packages/ui/src/services/api.ts`           | Type-safe API calls            |
| **Zustand Store**                | `packages/ui/src/stores/todoStore.ts`       | State management with Immer    |
| **Component Test**               | `packages/ui/src/components/*.test.tsx`     | Testing patterns               |
| **Domain Types**                 | `packages/schema/src/types.ts`              | Shared type definitions        |

## Type Safety & Validation

### Use Enums and Constants, Not Magic Strings

**Never use magic strings.** Always use enums, constants, or Zod enums for:

- **API endpoints**: Define in constants file, not inline
- **Status values**: Use Zod enums for validation + type inference
- **Action types**: Use string literal unions or enums
- **Route paths**: Define as constants
- **Storage keys**: Define as const object, not inline strings

**Example - Route Constants**:

```typescript
// GOOD: Constants file
export const ROUTES = {
  HOME: '/',
  TODOS: '/todos',
  TODO_DETAIL: (id: string) => `/todos/${id}`,
} as const;

// Usage
navigate(ROUTES.TODO_DETAIL(todoId));

// BAD: Magic strings
navigate(`/todos/${todoId}`);
```

**Example - Zod Enums**:

```typescript
// GOOD: String literal union
const StatusSchema = z.enum(['pending', 'completed']);
type Status = z.infer<typeof StatusSchema>;

// BAD: Plain strings
type Status = string;
```

### Type Generation Rules

1. **Check Schema First**: `packages/schema/src/api/`
2. **Create in @todos/schema**: All request/response types
3. **Add Zod Schemas**: For runtime validation
4. **Export from Index**: Make available to both server and client

## Component Development

### Component Decision Flow

```
Need Component?
    |
1. Check packages/components/ first <- **ALWAYS START HERE**
    ├── Exists & works? -> Use it
    └── Doesn't exist or needs changes
        |
2. Is it reusable across features?
    ├── Yes -> Create/extend in packages/components/
    └── No -> Create in packages/ui/src/components/
```

### Component Structure

```
packages/components/          # Reusable component library
    ├── src/
    │   ├── ui/              # shadcn/ui base components
    │   └── index.ts         # Public exports

packages/ui/                 # Application-specific
    ├── src/
    │   ├── components/      # App-specific components
    │   ├── pages/           # Route pages
    │   ├── stores/          # Zustand stores
    │   └── services/        # API services
```

### Component Pattern

```typescript
// packages/ui/src/components/TodoList.tsx
import { useState } from 'react';
import { useTodoStore } from '../stores/todoStore';
import { Todo } from '@todos/schema';

interface TodoListProps {
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}

export function TodoList({ onToggle, onDelete }: TodoListProps) {
  const { todos, isLoading, error } = useTodoStore();

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <ul className="space-y-2">
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={onToggle}
          onDelete={onDelete}
        />
      ))}
    </ul>
  );
}
```

**Key Patterns:**

- **ALWAYS check `packages/components/` first before creating**
- Use lucide-react for icons
- Tailwind for styling
- Loading and error states built-in
- Prop-based callbacks

## State Management Decision Tree

### When to Use What?

```
State Needed -> From Server?
├── Yes -> Needs Caching?
│   ├── Yes -> TanStack Query
│   └── No -> Direct API Call in useEffect
└── No -> Shared Across Components?
    ├── Yes -> Complex Logic?
    │   ├── Yes -> Zustand Store
    │   └── No -> React Context
    └── No -> Local useState
```

### TanStack Query Patterns

```typescript
// hooks/useTodos.ts
export function useTodos() {
  return useQuery({
    queryKey: ['todos'],
    queryFn: () => api.getTodos(),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

// Usage in component
function TodoPage() {
  const { data: todos, isLoading, error } = useTodos();

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorMessage />;
  return <TodoList todos={todos} />;
}
```

### Zustand Store Patterns

```typescript
// stores/todoStore.ts
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';
import { api } from '../services/api';
import { Todo } from '@todos/schema';

interface TodoState {
  todos: Todo[];
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchTodos: () => Promise<void>;
  addTodo: (title: string, description?: string) => Promise<void>;
  toggleTodo: (id: string) => Promise<void>;
  deleteTodo: (id: string) => Promise<void>;
  clearError: () => void;
}

export const useTodoStore = create<TodoState>()(
  immer((set, get) => ({
    todos: [],
    isLoading: false,
    error: null,

    fetchTodos: async () => {
      set({ isLoading: true, error: null });
      try {
        const todos = await api.getTodos();
        set({ todos, isLoading: false });
      } catch (error) {
        set({ error: 'Failed to fetch todos', isLoading: false });
      }
    },

    addTodo: async (title, description) => {
      try {
        const newTodo = await api.createTodo({ title, description });
        set((state) => {
          state.todos.push(newTodo);
        });
      } catch (error) {
        set({ error: 'Failed to add todo' });
      }
    },

    toggleTodo: async (id) => {
      try {
        const updatedTodo = await api.toggleTodo(id);
        set((state) => {
          const index = state.todos.findIndex((t) => t.id === id);
          if (index !== -1) {
            state.todos[index] = updatedTodo;
          }
        });
      } catch (error) {
        set({ error: 'Failed to toggle todo' });
      }
    },

    deleteTodo: async (id) => {
      try {
        await api.deleteTodo(id);
        set((state) => {
          state.todos = state.todos.filter((t) => t.id !== id);
        });
      } catch (error) {
        set({ error: 'Failed to delete todo' });
      }
    },

    clearError: () => set({ error: null }),
  }))
);
```

**Key Patterns:**

- Use Immer middleware for immutable updates
- Keep UI state separate from server state
- Action names for debugging

## API Integration Patterns

### Service Layer Structure

```typescript
// services/api.ts
import {
  Todo,
  CreateTodoInput,
  UpdateTodoInput,
} from '@todos/schema';

const API_BASE = import.meta.env.VITE_API_URL || '';

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${url}`, {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }

  const data = await response.json();
  return data.data;
}

export const api = {
  getTodos: () => request<Todo[]>('/api/todos'),

  getTodo: (id: string) => request<Todo>(`/api/todos/${id}`),

  createTodo: (data: CreateTodoInput) =>
    request<Todo>('/api/todos', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  updateTodo: (id: string, data: UpdateTodoInput) =>
    request<Todo>(`/api/todos/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  toggleTodo: (id: string) =>
    request<Todo>(`/api/todos/${id}/toggle`, {
      method: 'PATCH',
    }),

  deleteTodo: (id: string) =>
    request<void>(`/api/todos/${id}`, {
      method: 'DELETE',
    }),
};
```

## Testing Patterns

### Testing Priority Order (CRITICAL)

1. **Unit Tests First** - Test logic in isolation (functions, hooks, components)
2. **MSW Integration Tests** - Test API interactions
3. **E2E Tests Last** - Only for critical user flows

**ALWAYS write or update unit tests BEFORE MSW or integration tests.**

### Component Testing Setup

```typescript
// components/TodoList.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';
import { TodoList } from './TodoList';

describe('TodoList', () => {
  const mockTodos = [
    { id: '1', title: 'Test Todo', completed: false },
    { id: '2', title: 'Completed Todo', completed: true },
  ];

  it('should render todos', () => {
    render(<TodoList todos={mockTodos} onToggle={vi.fn()} onDelete={vi.fn()} />);

    expect(screen.getByText('Test Todo')).toBeInTheDocument();
    expect(screen.getByText('Completed Todo')).toBeInTheDocument();
  });

  it('should call onToggle when checkbox clicked', async () => {
    const user = userEvent.setup();
    const onToggle = vi.fn();

    render(<TodoList todos={mockTodos} onToggle={onToggle} onDelete={vi.fn()} />);

    await user.click(screen.getAllByRole('checkbox')[0]);

    expect(onToggle).toHaveBeenCalledWith('1');
  });
});
```

### Zustand Store Testing

```typescript
// stores/__tests__/todoStore.test.ts
import { renderHook, act } from '@testing-library/react';
import { useTodoStore } from '../todoStore';

describe('TodoStore', () => {
  beforeEach(() => {
    // Reset store state
    useTodoStore.setState({
      todos: [],
      isLoading: false,
      error: null,
    });
  });

  it('should add todo', async () => {
    const { result } = renderHook(() => useTodoStore());

    await act(async () => {
      await result.current.addTodo('New Todo');
    });

    expect(result.current.todos).toHaveLength(1);
  });
});
```

## Form Handling Patterns

### react-hook-form + Zod Integration

```typescript
// components/TodoForm.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { createTodoSchema, CreateTodoInput } from '@todos/schema';

export function TodoForm({ onSubmit }: { onSubmit: (data: CreateTodoInput) => void }) {
  const form = useForm<CreateTodoInput>({
    resolver: zodResolver(createTodoSchema),
    defaultValues: {
      title: '',
      description: '',
    },
  });

  const handleSubmit = form.handleSubmit(async (data) => {
    try {
      await onSubmit(data);
      form.reset();
    } catch (error) {
      form.setError('root', {
        message: 'Failed to create todo',
      });
    }
  });

  return (
    <form onSubmit={handleSubmit}>
      <input
        {...form.register('title')}
        placeholder="What needs to be done?"
      />
      {form.formState.errors.title && (
        <span>{form.formState.errors.title.message}</span>
      )}

      <button type="submit" disabled={form.formState.isSubmitting}>
        {form.formState.isSubmitting ? 'Adding...' : 'Add Todo'}
      </button>
    </form>
  );
}
```

## Common Commands

```bash
# Navigate to package first
cd packages/ui

# Development
pnpm dev                    # Start dev server
pnpm build                  # Build for production
pnpm type-check            # Type checking

# Testing (IMPORTANT: Use smart testing)
pnpm test:changed           # FAST - Only test changed (unit only) - RECOMMENDED
pnpm test:unit              # Unit tests only (excludes e2e)
pnpm test                   # SLOW - All tests including e2e

# Specific test file (FASTEST for focused work)
pnpm vitest run --no-coverage src/components/TodoList.test.tsx
pnpm vitest --no-coverage src/components/TodoList.test.tsx  # Watch mode

# From project root
pnpm test:changed           # Smart Nx testing - only affected packages
```

**Testing Strategy:**

- **Development**: `pnpm test:changed` (only tests what you changed)
- **Focused work**: `pnpm vitest run --no-coverage [file]`
- **Watch mode**: `pnpm vitest --no-coverage [file]` (auto-rerun)
- **Pre-commit**: `pnpm test:unit` (fast, no e2e)
- **Pre-push**: `pnpm test` (full suite)

## Quick Reference

### Essential Hooks

```typescript
// State
useTodoStore(); // Todo state and actions

// Data Fetching (if using TanStack Query)
useQuery(); // TanStack Query
useMutation(); // TanStack mutations

// Forms
useForm(); // react-hook-form
```

### Component Checklist

- [ ] Check packages/components/ first <- **CRITICAL**
- [ ] Check packages/schema/src/api/ for types <- **CRITICAL**
- [ ] Type-safe with TypeScript
- [ ] Zod validation for forms
- [ ] Accessible (ARIA attributes)
- [ ] Responsive design
- [ ] Loading states
- [ ] Error handling
- [ ] **Unit tests first**, then MSW/integration <- **CRITICAL**

### Performance Checklist

- [ ] Use React.memo for expensive components
- [ ] Optimize re-renders with useCallback/useMemo
- [ ] Lazy load routes with React.lazy
- [ ] Bundle splitting at route level

---

## Critical Reminders

**Before Any Development:**

1. Check `packages/components/` for reusable components
2. Check `packages/schema/src/api/` for request/response types
3. Write unit tests BEFORE integration/MSW tests
4. Use `pnpm test:changed` during development

**Architecture Flow:**

```
Component -> Zustand Store -> API Service -> @schema/api types
         or
Component -> TanStack Query -> API Service -> @schema/api types
```

**Remember**: Maintain type safety across all layers. Always validate with Zod at boundaries. Check component library before creating new components.
