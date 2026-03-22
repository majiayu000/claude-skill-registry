---
name: react-hook-patterns
description: Custom React hook best practices — dependency arrays, cleanup, stale closures, TypeScript generics, composition, and extraction heuristics
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash
argument-hint: "[hook file or pattern question]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: react, hooks, patterns
---

# React Hook Patterns

## Overview

Reference guide for writing correct, composable, and type-safe custom hooks in React + TypeScript. Apply these patterns when building or reviewing hooks to avoid stale closures, missing cleanup, and dependency array bugs.

## Dependency Array Correctness

### The Rule

Every reactive value (props, state, context, or anything derived from them) used inside a hook callback must appear in the dependency array. The ESLint rule `react-hooks/exhaustive-deps` catches most issues — never suppress it without documenting why.

```tsx
// GOOD: all reactive values in deps
function useDocumentTitle(title: string) {
  useEffect(() => {
    document.title = title;
  }, [title]);
}

// BAD: missing dep — title will be stale
function useDocumentTitle(title: string) {
  useEffect(() => {
    document.title = title;
  }, []); // eslint-disable-line — NEVER do this
}
```

### Stable References Reduce Deps

Use `useRef` for values you want to read without triggering re-runs.

```tsx
function useInterval(callback: () => void, delay: number | null) {
  const savedCallback = useRef(callback);

  // Update ref on every render — no dependency needed in the interval
  useLayoutEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    if (delay === null) return;
    const id = setInterval(() => savedCallback.current(), delay);
    return () => clearInterval(id);
  }, [delay]);
}
```

## Cleanup Patterns

Every effect that subscribes, connects, or allocates must return a cleanup function.

```tsx
// Event listeners
useEffect(() => {
  const handler = (e: KeyboardEvent) => {
    if (e.key === "Escape") onClose();
  };
  window.addEventListener("keydown", handler);
  return () => window.removeEventListener("keydown", handler);
}, [onClose]);

// Abort controller for fetch
useEffect(() => {
  const controller = new AbortController();
  fetch(url, { signal: controller.signal })
    .then((res) => res.json())
    .then(setData)
    .catch((err) => {
      if (err.name !== "AbortError") setError(err);
    });
  return () => controller.abort();
}, [url]);

// Timers
useEffect(() => {
  const id = setTimeout(() => setVisible(false), duration);
  return () => clearTimeout(id);
}, [duration]);

// Intersection Observer
useEffect(() => {
  if (!ref.current) return;
  const observer = new IntersectionObserver(([entry]) => {
    setIsVisible(entry.isIntersecting);
  }, options);
  observer.observe(ref.current);
  return () => observer.disconnect();
}, [options]);
```

## Stale Closure Prevention

Closures capture variables at creation time. When a callback is stored (e.g., in an event listener or timer), it can read stale state.

```tsx
// BAD: stale closure — count is captured at 0
function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setCount(count + 1); // Always sets to 1
    }, 1000);
    return () => clearInterval(id);
  }, []); // count not in deps
}

// FIX 1: Functional updater (preferred for state-only)
setCount((prev) => prev + 1);

// FIX 2: Ref for non-state values
const countRef = useRef(count);
countRef.current = count;
useEffect(() => {
  const id = setInterval(() => {
    console.log(countRef.current); // Always fresh
  }, 1000);
  return () => clearInterval(id);
}, []);
```

### Event Handlers in Effects

```tsx
// BAD: handler captures stale onSubmit
useEffect(() => {
  form.addEventListener("submit", onSubmit);
  return () => form.removeEventListener("submit", onSubmit);
}, []); // onSubmit missing

// GOOD: ref-based pattern
const onSubmitRef = useRef(onSubmit);
onSubmitRef.current = onSubmit;

useEffect(() => {
  const handler = (e: Event) => onSubmitRef.current(e);
  form.addEventListener("submit", handler);
  return () => form.removeEventListener("submit", handler);
}, []);
```

## TypeScript Generics in Hooks

Use generics to make hooks reusable across types while preserving inference.

```tsx
// Generic hook with constraint
function useLocalStorage<T>(key: string, initialValue: T) {
  const [stored, setStored] = useState<T>(() => {
    try {
      const item = localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback(
    (value: T | ((prev: T) => T)) => {
      setStored((prev) => {
        const next = value instanceof Function ? value(prev) : value;
        localStorage.setItem(key, JSON.stringify(next));
        return next;
      });
    },
    [key]
  );

  return [stored, setValue] as const;
}

// Usage — T is inferred from initialValue
const [user, setUser] = useLocalStorage("user", { name: "", age: 0 });
// user is { name: string; age: number }
```

### Constrained Generics

```tsx
function useApiResource<T extends { id: string }>(
  fetcher: () => Promise<T[]>
) {
  const [items, setItems] = useState<T[]>([]);
  const [byId, setById] = useState<Map<string, T>>(new Map());

  const refresh = useCallback(async () => {
    const data = await fetcher();
    setItems(data);
    setById(new Map(data.map((item) => [item.id, item])));
  }, [fetcher]);

  return { items, byId, refresh } as const;
}
```

## Common Hook Recipes

### useDebounce

```tsx
function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debounced;
}

// Usage
const debouncedSearch = useDebounce(searchTerm, 300);
useEffect(() => {
  fetchResults(debouncedSearch);
}, [debouncedSearch]);
```

### useFetch with TypeScript

```tsx
type FetchState<T> =
  | { status: "idle"; data: undefined; error: undefined }
  | { status: "loading"; data: undefined; error: undefined }
  | { status: "success"; data: T; error: undefined }
  | { status: "error"; data: undefined; error: Error };

function useFetch<T>(url: string | null): FetchState<T> {
  const [state, setState] = useState<FetchState<T>>({
    status: "idle",
    data: undefined,
    error: undefined,
  });

  useEffect(() => {
    if (!url) return;
    const controller = new AbortController();

    setState({ status: "loading", data: undefined, error: undefined });

    fetch(url, { signal: controller.signal })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json() as Promise<T>;
      })
      .then((data) =>
        setState({ status: "success", data, error: undefined })
      )
      .catch((err) => {
        if (err.name === "AbortError") return;
        setState({ status: "error", data: undefined, error: err });
      });

    return () => controller.abort();
  }, [url]);

  return state;
}

// Usage — discriminated union enables safe access
const result = useFetch<User[]>("/api/users");
if (result.status === "success") {
  result.data.map(/* TypeScript knows data is User[] */);
}
```

### useMediaQuery

```tsx
function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(() =>
    window.matchMedia(query).matches
  );

  useEffect(() => {
    const mql = window.matchMedia(query);
    const handler = (e: MediaQueryListEvent) => setMatches(e.matches);
    mql.addEventListener("change", handler);
    return () => mql.removeEventListener("change", handler);
  }, [query]);

  return matches;
}
```

## Composing Hooks

Build complex behavior by composing small hooks. Each hook should do one thing.

```tsx
// Small, focused hooks
function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  useEffect(() => {
    const goOnline = () => setIsOnline(true);
    const goOffline = () => setIsOnline(false);
    window.addEventListener("online", goOnline);
    window.addEventListener("offline", goOffline);
    return () => {
      window.removeEventListener("online", goOnline);
      window.removeEventListener("offline", goOffline);
    };
  }, []);
  return isOnline;
}

// Composed hook
function useResilientFetch<T>(url: string) {
  const isOnline = useOnlineStatus();
  const [fetchKey, setFetchKey] = useState(0);
  const result = useFetch<T>(isOnline ? url : null, fetchKey);
  const debouncedRetry = useDebounce(isOnline, 2000);

  const refetch = useCallback(() => setFetchKey((k) => k + 1), []);

  // Auto-retry when coming back online (debounced)
  useEffect(() => {
    if (debouncedRetry && result.status === "error") {
      refetch();
    }
  }, [debouncedRetry, result.status, refetch]);

  return { ...result, isOnline, refetch };
}
```

## When to Extract a Custom Hook

### The "3 Uses" Rule

Extract a custom hook when:
1. The same `useState` + `useEffect` combo appears in **3+ components**
2. A component has **5+ hooks** that serve a single concern
3. You need to **test** stateful logic independently of UI

Do NOT extract a hook for:
- A single `useState` — just use `useState` directly
- Logic used in only one component — a helper function is simpler
- "Just in case we need it later" — YAGNI

## Anti-patterns

### Hooks with Too Many Parameters

More than 3 parameters signals the hook is doing too much. Use an options object.

```tsx
// BAD: positional params are unclear
useDataFetcher(url, true, false, 5000, "GET", authToken);

// GOOD: options object with defaults
useDataFetcher(url, {
  auth: true,
  retry: false,
  timeout: 5000,
});
```

### Missing Cleanup

If your effect subscribes, it must unsubscribe. Forgetting cleanup causes memory leaks and ghost updates after unmount.

### Stale Closures in Event Handlers

If you pass a callback to `addEventListener` inside `useEffect` without a ref, the callback will read stale values when the effect does not re-run.

### Hooks That Do Too Much

A hook managing form state, validation, submission, and error display is four hooks. Split along concerns: `useFormState`, `useValidation`, `useSubmit`.
