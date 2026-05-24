---
name: typescript-excellence
description: |
  TypeScript best practices, type safety, and toolchain standards. Use when:
  - Writing or reviewing TypeScript code
  - Setting up TypeScript projects or tsconfig
  - Choosing state management patterns
  - Configuring build tools (tsup, Vitest)
  - Avoiding type gymnastics or any-abuse
  Keywords: TypeScript, tsconfig, strict mode, no-any, pnpm, Vitest, tsup,
  TanStack Query, discriminated unions, type safety, ESLint
---

# TypeScript Excellence

Type-safe, maintainable TypeScript with modern toolchain.

## Type Safety

**Never use `any`**. Alternatives:
```typescript
// Unknown for external data
function parse(input: unknown): User { ... }

// Union for specific options
type Status = 'loading' | 'success' | 'error';

// Generics for reusable code
function first<T>(arr: T[]): T | undefined { ... }

// Type assertion as last resort (with runtime check)
if (isUser(data)) { return data as User; }
```

**tsconfig.json essentials:**
```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}
```

## Module Organization

Feature-based, not layer-based:
```
src/
  features/
    auth/
      components/
      hooks/
      api.ts
      types.ts
      index.ts  # Barrel: controlled exports
    orders/
      ...
  shared/
    ui/
    utils/
```

Use path aliases: `@features/*`, `@shared/*` (avoid `../../../../`).

## State Management

**Server state**: TanStack Query exclusively.
```typescript
const { data, isLoading, error } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => fetchUser(userId),
});
```

**Client state**: Discriminated unions.
```typescript
type AuthState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'authenticated'; user: User }
  | { status: 'error'; error: AppError };
```

## Async Patterns

Always wrap, always context:
```typescript
async function fetchUser(id: string): Promise<User> {
  try {
    const res = await fetch(`/api/users/${id}`);
    if (!res.ok) throw new ApiError(res.status, await res.text());
    return res.json();
  } catch (error) {
    throw new AppError('Failed to fetch user', { cause: error });
  }
}
```

Cancellation: Use `AbortController` for long operations. Always clean up timeouts in `finally` blocks.

## Toolchain

| Tool | Purpose |
|------|---------|
| **pnpm** | Package manager (declare in `packageManager` field) |
| **Vitest** | Testing (unit/integration/e2e) |
| **tsup** | Builds (ESM + CJS + .d.ts) |
| **ESLint** | Linting (`@typescript-eslint/no-explicit-any: error`) |
| **Prettier** | Formatting |

## Anti-Patterns

- Type gymnastics (conditional types, template literals without justification)
- `useState` + `useEffect` for server data (use TanStack Query)
- Technical-layer folders (`/controllers`, `/services`, `/models`)
- `eslint-disable` without documented justification
- Mocking internal components (mock boundaries only)
- Mixed package managers or test frameworks

## References

- [toolchain-setup.md](references/toolchain-setup.md) - pnpm, Vitest, tsup, ESLint config
- [type-patterns.md](references/type-patterns.md) - Utility types, generics, guards
- [testing-strategy.md](references/testing-strategy.md) - Test pyramid, behavior focus
- [async-patterns.md](references/async-patterns.md) - Timeout cleanup, error-specific catch, cancellation
