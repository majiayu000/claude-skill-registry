---
name: typescript
description: |
  Enforces TypeScript type safety and interface patterns for the Bookkeep frontend.
  Use when: writing React components, defining API types, creating hooks, or fixing type errors.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# TypeScript Skill

This project uses TypeScript 5.x with **relaxed strict mode** (`strict: false`, `strictNullChecks: false`). The codebase prioritizes developer velocity while maintaining type safety where it matters: API contracts, component props, and state management.

## Quick Start

### Component Props Pattern

```typescript
// src/components/books/BookCard.tsx
interface BookCardProps {
  book: Book;
  status?: 'available' | 'pending' | 'none';
  showRating?: boolean;
  requestStatus?: { ebook?: string | null; audiobook?: string | null };
}

export const BookCard = memo(function BookCard({
  book,
  status = 'none',
  showRating = true,
}: BookCardProps) {
  // ...
});
```

### Generic API Request

```typescript
// src/lib/api.ts
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  // Handles JWT auth, token refresh, error parsing
  return JSON.parse(text);
}

// Usage with explicit type
const data = await apiRequest<{ books: any[] }>('/api/hardcover/trending');
```

### Type Guard Pattern

```typescript
// Filter with type narrowing
const requestStatuses = statusSource
  ? [statusSource.ebook, statusSource.audiobook].filter((value): value is string => !!value)
  : [];
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Path alias | Import from `@/` | `import { Button } from '@/components/ui/button'` |
| Type-only imports | Separate type imports | `import type { Book } from '@/types/book'` |
| Union literals | Status/format enums | `'ebook' \| 'audiobook'` |
| Generic API calls | Type API responses | `apiRequest<T>(endpoint)` |
| Const assertions | Literal type preservation | `format: 'ebook' as const` |

## Common Patterns

### Context with Type Safety

```typescript
// src/contexts/UserContext.tsx
interface UserContextType {
  user: ApiUser | null;
  isAdmin: boolean;
  logout: () => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export function useUser() {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
}
```

### Hook Options Interface

```typescript
// src/hooks/useAvailabilityPolling.ts
interface AvailabilityPollingOptions {
  pendingRequests: PendingRequest[];
  enabled?: boolean;
  seriesId?: string | number;
}

export function useAvailabilityPolling({
  pendingRequests,
  enabled = true,
  seriesId,
}: AvailabilityPollingOptions) { /* ... */ }
```

## See Also

- [patterns](references/patterns.md) - Idiomatic TypeScript patterns
- [types](references/types.md) - Type definitions and interfaces
- [modules](references/modules.md) - Module organization and imports
- [errors](references/errors.md) - Error handling and type guards

## Related Skills

- See the **react** skill for component patterns
- See the **tanstack-query** skill for query typing
- See the **shadcn-ui** skill for UI component types