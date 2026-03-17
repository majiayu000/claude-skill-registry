---
name: add-hook
description: Create a shared React hook in packages/shared/hooks/
---

# Add Hook Skill

Create a shared React hook in `packages/shared/hooks/` for use across web, mobile, and desktop apps.

## Arguments

The user describes the hook. If unclear, ask for:

- Hook name (camelCase with `use` prefix, e.g., `useDebounce`, `useLocalStorage`)
- What it returns (state shape)
- Whether it needs a `.native.ts` variant for React Native

## File Location

- **Hook**: `packages/shared/hooks/{hookName}.ts` (or `.tsx` if JSX needed)
- **Native variant**: `packages/shared/hooks/{hookName}.native.ts` (optional)
- **Test**: `packages/shared/hooks/{hookName}.test.ts` (co-located)
- **Export**: `packages/shared/hooks/index.ts`

## Hook Template

Reference: `packages/shared/hooks/useAuth.ts`

````typescript
/**
 * Brief description of what the hook does.
 *
 * @example
 * ```tsx
 * const { value, setValue } = useMyHook('key');
 * ```
 */

export interface UseMyHookOptions {
  /** Option description */
  initialValue?: string;
}

export interface UseMyHookReturn {
  /** Return value description */
  value: string | null;
  /** Whether the hook is loading */
  isLoading: boolean;
  /** Update the value */
  setValue: (value: string) => void;
}

export function useMyHook(options: UseMyHookOptions = {}): UseMyHookReturn {
  const { initialValue = null } = options;

  // Hook implementation using React hooks
  // ...

  return {
    value,
    isLoading,
    setValue,
  };
}
````

## Native Variant (optional)

If the hook needs different behavior on React Native, create a `.native.ts` file:

```typescript
// packages/shared/hooks/useMyHook.native.ts
// React Native bundlers (Metro) automatically resolve .native.ts over .ts

export function useMyHook(options: UseMyHookOptions = {}): UseMyHookReturn {
  // React Native-specific implementation
}
```

## Export from Index

Add to `packages/shared/hooks/index.ts`:

```typescript
export { useMyHook } from './useMyHook';
export type { UseMyHookOptions, UseMyHookReturn } from './useMyHook';
```

## Test Template

```typescript
import { describe, test, expect } from 'bun:test';
import { renderHook, act } from '@testing-library/react';
import { useMyHook } from './useMyHook';

describe('useMyHook', () => {
  test('returns initial state', () => {
    const { result } = renderHook(() => useMyHook());
    expect(result.current.value).toBeNull();
    expect(result.current.isLoading).toBe(false);
  });

  test('updates value', () => {
    const { result } = renderHook(() => useMyHook());
    act(() => {
      result.current.setValue('new value');
    });
    expect(result.current.value).toBe('new value');
  });
});
```

## Conventions

- **Naming**: Always prefix with `use` (camelCase)
- **Types**: Export both options and return type interfaces
- **Dependencies**: Hooks in `packages/shared/` must NOT import from `apps/*`
- **JSX config**: If the hook file uses `.tsx`, ensure `packages/shared/tsconfig.json` has `"jsx": "react-jsx"`
- **File extension**: Use `.ts` unless JSX is needed, then `.tsx`

## Workflow

1. Create hook file at `packages/shared/hooks/{hookName}.ts`
2. Define options and return type interfaces
3. Implement the hook
4. Export from `packages/shared/hooks/index.ts`
5. Create `.native.ts` variant if needed
6. Create co-located test file
7. Run `bun turbo type-check` to verify
