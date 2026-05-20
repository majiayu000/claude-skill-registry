---
skill: add-hook
description: Create a custom React hook with TypeScript and tests
arguments: hook name and purpose
---

# Add Hook: $ARGUMENTS

Create a custom React hook with proper typing and tests.

## Process

### 1. Plan the Hook

Determine:
- What state does it manage?
- What side effects does it handle?
- What does it return?

### 2. Create Hook File

Location: `hooks/use[HookName].ts`

```typescript
import { useState, useEffect, useCallback } from 'react';

interface UseHookNameOptions {
  // configuration options
  initialValue?: string;
}

interface UseHookNameReturn {
  // return type
  value: string;
  setValue: (value: string) => void;
  isLoading: boolean;
  error: Error | null;
}

export function useHookName(options: UseHookNameOptions = {}): UseHookNameReturn {
  const { initialValue = '' } = options;

  const [value, setValue] = useState(initialValue);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const handleSetValue = useCallback((newValue: string) => {
    setValue(newValue);
  }, []);

  useEffect(() => {
    // Side effects here
  }, []);

  return {
    value,
    setValue: handleSetValue,
    isLoading,
    error,
  };
}
```

### 3. Add to Exports

```typescript
// hooks/index.ts
export { useHookName } from './useHookName';
```

### 4. Create Tests

```typescript
// hooks/useHookName.test.ts
import { renderHook, act } from '@testing-library/react';
import { useHookName } from './useHookName';

describe('useHookName', () => {
  test('returns initial value', () => {
    const { result } = renderHook(() => useHookName());
    expect(result.current.value).toBe('');
  });

  test('updates value', () => {
    const { result } = renderHook(() => useHookName());
    act(() => {
      result.current.setValue('new value');
    });
    expect(result.current.value).toBe('new value');
  });

  test('accepts initial value option', () => {
    const { result } = renderHook(() =>
      useHookName({ initialValue: 'custom' })
    );
    expect(result.current.value).toBe('custom');
  });
});
```

### 5. Validate

```bash
npm run build
npm run lint
npm test
```

## Common Hook Patterns

**Data fetching:**
```typescript
export function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  // ...
}
```

**Local storage:**
```typescript
export function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initialValue;
  });
  // ...
}
```

**Debounce:**
```typescript
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);
  // ...
}
```

**Media query:**
```typescript
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);
  // ...
}
```
