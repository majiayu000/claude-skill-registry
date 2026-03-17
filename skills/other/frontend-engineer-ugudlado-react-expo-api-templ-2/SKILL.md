---
name: frontend-engineer
description: Expert in web app frontend architecture, React patterns, TypeScript, TanStack Query, Zustand, and component development with strong type safety. Use when building UI components, implementing data fetching, managing state, writing forms, styling with Tailwind, testing React components, or integrating with backend APIs.
---

# Frontend Engineer

Expert knowledge of frontend patterns and architecture for React web apps.

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
|                 Type-Safe Response (schema/api)
|
└── UI State -> Zustand Store (with Immer)
```

## Pattern References (ALWAYS CHECK THESE FIRST)

| Pattern                  | Reference Path                    | Notes                      |
| ------------------------ | --------------------------------- | -------------------------- |
| **Reusable Components**  | `packages/components/src/`        | **ALWAYS CHECK FIRST**     |
| **API Types**            | `packages/schema/src/api/`        | **CHECK HERE FIRST**       |
| **API Service Layer**    | `packages/ui/src/services/api.ts` | Type-safe API calls        |
| **Zustand Store**        | `packages/ui/src/stores/`         | State management w/ Immer  |
| **Component Tests**      | `packages/ui/src/components/*.test.tsx` | Testing patterns     |
| **Domain Types**         | `packages/schema/src/types.ts`    | Shared type definitions    |

## Type Safety & Validation

### No Magic Strings

Always use enums, constants, or Zod enums:

```typescript
// GOOD
export const ROUTES = {
  HOME: '/',
  ITEMS: '/items',
  ITEM_DETAIL: (id: string) => `/items/${id}`,
} as const;

// GOOD
const StatusSchema = z.enum(['pending', 'completed']);
type Status = z.infer<typeof StatusSchema>;

// BAD
navigate(`/items/${id}`);
type Status = string;
```

### Type Generation Rules

1. Check `packages/schema/src/api/` first
2. All request/response types in schema package
3. Add Zod schemas for runtime validation
4. Export from index for both server and client

## Component Development

### Component Decision Flow

```
Need Component?
    |
1. Check packages/components/ first <- ALWAYS START HERE
    ├── Exists? -> Use it
    └── Doesn't exist
        |
2. Reusable across features?
    ├── Yes -> Create in packages/components/
    └── No -> Create in packages/ui/src/components/
```

### Component Pattern

```typescript
interface ItemListProps {
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}

export function ItemList({ onToggle, onDelete }: ItemListProps) {
  const { items, isLoading, error } = useItemStore();

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <ul className="space-y-2">
      {items.map((item) => (
        <ListItem key={item.id} item={item} onToggle={onToggle} onDelete={onDelete} />
      ))}
    </ul>
  );
}
```

## State Management

### TanStack Query (Server State)

```typescript
export function useItems() {
  return useQuery({
    queryKey: ['items'],
    queryFn: () => api.getItems(),
    staleTime: 5 * 60 * 1000,
  });
}
```

### Zustand Store (Client State)

```typescript
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';

interface AppState {
  items: Item[];
  isLoading: boolean;
  error: string | null;
  fetchItems: () => Promise<void>;
}

export const useAppStore = create<AppState>()(
  immer((set) => ({
    items: [],
    isLoading: false,
    error: null,

    fetchItems: async () => {
      set({ isLoading: true, error: null });
      try {
        const items = await api.getItems();
        set({ items, isLoading: false });
      } catch (error) {
        set({ error: 'Failed to fetch', isLoading: false });
      }
    },
  }))
);
```

### Decision Tree

```
Server data with caching? -> TanStack Query
Shared UI state?          -> Zustand Store
Local component state?    -> useState
```

## Form Handling

### react-hook-form + Zod

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

export function ItemForm({ onSubmit }: { onSubmit: (data: CreateItemInput) => void }) {
  const form = useForm<CreateItemInput>({
    resolver: zodResolver(createItemSchema),
    defaultValues: { title: '', description: '' },
  });

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      <input {...form.register('title')} placeholder="Title" />
      {form.formState.errors.title && (
        <span>{form.formState.errors.title.message}</span>
      )}
      <button type="submit" disabled={form.formState.isSubmitting}>
        {form.formState.isSubmitting ? 'Saving...' : 'Save'}
      </button>
    </form>
  );
}
```

## Testing Patterns

### Priority Order

1. **Unit Tests First** — Test logic in isolation
2. **MSW Integration Tests** — Test API interactions
3. **E2E Tests Last** — Only for critical user flows

### Component Test

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';

describe('ItemList', () => {
  it('should render items', () => {
    render(<ItemList items={mockItems} onToggle={vi.fn()} onDelete={vi.fn()} />);
    expect(screen.getByText('Test Item')).toBeInTheDocument();
  });

  it('should call onToggle when clicked', async () => {
    const user = userEvent.setup();
    const onToggle = vi.fn();
    render(<ItemList items={mockItems} onToggle={onToggle} onDelete={vi.fn()} />);
    await user.click(screen.getAllByRole('checkbox')[0]);
    expect(onToggle).toHaveBeenCalledWith('1');
  });
});
```

## Common Commands

```bash
pnpm dev                    # Start dev server
pnpm build                  # Build for production
pnpm type-check             # Type checking

# Testing
pnpm test:changed           # FAST - Only changed files (RECOMMENDED)
pnpm test:unit              # Unit tests only
pnpm test                   # All tests including e2e
pnpm vitest run --no-coverage src/components/ItemList.test.tsx  # Specific file
```

## Component Checklist

- [ ] Check packages/components/ first
- [ ] Check packages/schema/src/api/ for types
- [ ] Type-safe with TypeScript
- [ ] Zod validation for forms
- [ ] Accessible (ARIA attributes)
- [ ] Responsive design
- [ ] Loading and error states
- [ ] Unit tests first, then MSW/integration
