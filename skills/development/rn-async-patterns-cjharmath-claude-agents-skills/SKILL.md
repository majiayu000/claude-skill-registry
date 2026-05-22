---
name: rn-async-patterns
description: Async/await correctness in React Native with Zustand. Use when debugging race conditions, missing awaits, floating promises, or async timing issues in Expo/React Native apps.
---

# React Native Async Patterns

## Problem Statement

Async bugs in React Native are insidious because they often work in development but fail under load or on slower devices. The most common issues: missing `await` on async functions, race conditions between state updates, and assuming operations complete in order.

---

## Pattern: Floating Promise Detection

**Problem:** Calling an async function without `await` causes it to run in the background. If subsequent code depends on its completion, you get a race condition.

**Example (from retake bug):**

```typescript
// Before (buggy) - enableSkillAreaRetake is async but not awaited
enableSkillAreaRetake(skillArea);         // Fire and forget ❌
await clearSkillAreaAnswers(skillArea);   // Runs before enable completes

// After (fixed)
await enableSkillAreaRetake(skillArea);   // Wait for state update ✅
await clearSkillAreaAnswers(skillArea);   // Now runs in correct order
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

**Example (from retake bug):**

```typescript
// Before (buggy) - assumed load worked
await loadCompletedAssessmentAnswers(id);
// Proceeded blindly with retake flow...

// After (defensive)
await loadCompletedAssessmentAnswers(id);
const loaded = useAssessmentStore.getState().completedAssessmentAnswers;
if (Object.keys(loaded).length === 0) {
  throw new Error(
    `Failed to load answers for assessment ${id} - cannot proceed with retake`
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
  enableRetake: (area: string) => {
    someAsyncSetup().then(() => {  // ← Hidden async!
      set({ retakeAreas: [...get().retakeAreas, area] });
    });
  },
}));

// Proper async Zustand action
const useStore = create((set, get) => ({
  enableRetake: async (area: string) => {
    await someAsyncSetup();
    set({ retakeAreas: [...get().retakeAreas, area] });
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
await enableSkillAreaRetake(skillArea);
await clearSkillAreaAnswers(skillArea);
await loadRetakeQuestions(skillArea);

// Parallel - correct when operations are independent
const [user, settings, history] = await Promise.all([
  fetchUser(id),
  fetchSettings(id),
  fetchHistory(id),
]);

// WRONG - parallel when order matters
await Promise.all([
  enableSkillAreaRetake(skillArea),   // These have dependencies!
  clearSkillAreaAnswers(skillArea),
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
```

---

## ESLint Configuration

Apply config from `configs/eslint-async.json` to catch these issues at lint time:

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

---

## Quick Debugging

When async timing issues occur:

```typescript
// Add timestamps to trace execution order
console.log(`[${Date.now()}] Starting enableRetake`);
await enableSkillAreaRetake(skillArea);
console.log(`[${Date.now()}] Finished enableRetake`);
console.log(`[${Date.now()}] Starting clearAnswers`);
await clearSkillAreaAnswers(skillArea);
console.log(`[${Date.now()}] Finished clearAnswers`);
```

Look for:
- Operations finishing out of expected order
- Operations starting before previous ones complete
- Suspiciously fast "completions" (might not have awaited)
