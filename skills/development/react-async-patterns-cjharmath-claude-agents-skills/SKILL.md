---
name: react-async-patterns
description: Async/await correctness in React with Zustand. Use when debugging race conditions, missing awaits, floating promises, or async timing issues. Works for both React web and React Native.
---

# React Async Patterns

## Problem Statement

Async bugs in React are insidious because they often work in development but fail under load or in edge cases. The most common issues: missing `await` on async functions, race conditions between state updates, and assuming operations complete in order.

---

## Pattern: Floating Promise Detection

**Problem:** Calling an async function without `await` causes it to run in the background. If subsequent code depends on its completion, you get a race condition.

```typescript
// Before (buggy) - saveData is async but not awaited
saveData(item);              // Fire and forget ❌
await processData(item);     // Runs before save completes

// After (fixed)
await saveData(item);        // Wait for state update ✅
await processData(item);     // Now runs in correct order
```

**Why it's subtle:** Both functions might have `async` in their signature, but only one was awaited. The code "looks right" at a glance.

**Detection:**

```bash
# Find potential floating promises - async calls without await
grep -rn "^\s*[a-zA-Z]*\s*(" --include="*.ts" --include="*.tsx" | \
  grep -v "await\|return\|const\|let\|if\|else\|=>"
```

**Prevention:**

1. ESLint rule `@typescript-eslint/no-floating-promises` - catches this at lint time
2. Code review trigger: Any line calling a function that might be async without `await`, `return`, or assignment

---

## Pattern: Post-Condition Validation

**Problem:** Assuming an async call succeeded without verifying. The call might return early, throw silently, or fail to update state.

```typescript
// Before (buggy) - assumed load worked
await loadData(id);
// Proceeded blindly with next steps...

// After (defensive)
await loadData(id);
const loaded = useStore.getState().data;
if (Object.keys(loaded).length === 0) {
  throw new Error(
    `Failed to load data for ${id} - cannot proceed`
  );
}
```

**Principle:** Treat every async call as potentially failed until proven otherwise.

**When to validate:**

- After loading data that subsequent operations depend on
- After state updates that must complete before continuing
- Before irreversible operations (submissions, deletions)

**Pattern template:**

```typescript
await someAsyncOperation();
const result = getRelevantState();
if (!isValid(result)) {
  throw new Error(`[${functionName}] Post-condition failed: ${diagnosticContext}`);
}
```

---

## Pattern: Async Function Identification

**Problem:** Not all async functions look async. Zustand actions, callbacks, and promise-returning functions may not have obvious `async` keywords.

**Hidden async patterns:**

```typescript
// Obvious async
async function fetchData() { ... }

// Less obvious - returns Promise
function fetchData(): Promise<Data> { ... }

// Hidden - Zustand action that's actually async
const useStore = create((set, get) => ({
  // This looks sync but calls async internally
  enableFeature: (id: string) => {
    someAsyncSetup().then(() => {  // ← Hidden async!
      set({ features: [...get().features, id] });
    });
  },
}));

// Proper async Zustand action
const useStore = create((set, get) => ({
  enableFeature: async (id: string) => {
    await someAsyncSetup();
    set({ features: [...get().features, id] });
  },
}));
```

**Detection:** Check function signatures and implementations:

```bash
# Find functions returning Promise
grep -rn "): Promise<" --include="*.ts" --include="*.tsx"

# Find .then() chains that might need await
grep -rn "\.then(" --include="*.ts" --include="*.tsx"
```

---

## Pattern: Sequential vs Parallel Async

**Problem:** Running async operations sequentially when they could be parallel (slow), or parallel when they must be sequential (race condition).

```typescript
// Sequential - correct when order matters
await stepOne();
await stepTwo();
await stepThree();

// Parallel - correct when operations are independent
const [user, settings, history] = await Promise.all([
  fetchUser(id),
  fetchSettings(id),
  fetchHistory(id),
]);

// WRONG - parallel when order matters
await Promise.all([
  stepOne(),   // These have dependencies!
  stepTwo(),
]);
```

**Decision framework:**

| Operations share state? | Must run in order? | Pattern |
|------------------------|-------------------|---------|
| No | No | `Promise.all()` |
| Yes | Yes | Sequential `await` |
| Yes | No | Usually sequential to be safe |

---

## Pattern: Async in useEffect

**Problem:** `useEffect` callbacks can't be async directly. Common mistakes with cleanup and race conditions.

```typescript
// WRONG - useEffect can't be async
useEffect(async () => {
  const data = await fetchData();
  setData(data);
}, []);

// CORRECT - async function inside
useEffect(() => {
  async function load() {
    const data = await fetchData();
    setData(data);
  }
  load();
}, []);

// BETTER - with cleanup for race conditions
useEffect(() => {
  let cancelled = false;

  async function load() {
    const data = await fetchData();
    if (!cancelled) {
      setData(data);
    }
  }
  load();

  return () => {
    cancelled = true;
  };
}, [dependency]);

// BEST - use AbortController for fetch
useEffect(() => {
  const controller = new AbortController();

  async function load() {
    try {
      const response = await fetch(url, { signal: controller.signal });
      const data = await response.json();
      setData(data);
    } catch (error) {
      if (error.name !== 'AbortError') {
        setError(error);
      }
    }
  }
  load();

  return () => controller.abort();
}, [url]);
```

---

## Pattern: React Query / TanStack Query

**Problem:** Manual async state management is error-prone. Use a library.

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// Fetching data
function UserProfile({ userId }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  if (isLoading) return <Spinner />;
  if (error) return <Error error={error} />;
  return <Profile user={data} />;
}

// Mutations with cache invalidation
function UpdateUser() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: updateUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['user'] });
    },
  });

  return (
    <button onClick={() => mutation.mutate(userData)}>
      Save
    </button>
  );
}
```

---

## ESLint Configuration

Add these rules to catch async issues at lint time:

```json
{
  "rules": {
    "@typescript-eslint/no-floating-promises": "error",
    "@typescript-eslint/require-await": "warn",
    "@typescript-eslint/await-thenable": "error",
    "@typescript-eslint/no-misused-promises": "error"
  }
}
```

**Required:** `@typescript-eslint/eslint-plugin` and proper TypeScript configuration.

---

## Code Review Checklist

When reviewing async code, check:

- [ ] Every async function call is either `await`ed, `return`ed, or explicitly fire-and-forget with comment
- [ ] Operations that depend on each other are sequenced with `await`
- [ ] Post-conditions validated after critical async operations
- [ ] `useEffect` with async uses the inner function pattern
- [ ] Race conditions considered when component could unmount during async
- [ ] Error handling exists for async failures
- [ ] AbortController used for fetch calls that should be cancellable

---

## Quick Debugging

When async timing issues occur:

```typescript
// Add timestamps to trace execution order
console.log(`[${Date.now()}] Starting step 1`);
await stepOne();
console.log(`[${Date.now()}] Finished step 1`);
console.log(`[${Date.now()}] Starting step 2`);
await stepTwo();
console.log(`[${Date.now()}] Finished step 2`);
```

Look for:
- Operations finishing out of expected order
- Operations starting before previous ones complete
- Suspiciously fast "completions" (might not have awaited)
