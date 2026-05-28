---
name: react-debugging
description: Debugging React render loops, infinite re-renders, and performance issues in Next.js. Use when encountering "Maximum update depth exceeded", useMemo/useCallback issues, useEffect dependency problems, or useSearchParams loops. Keywords: infinite loop, re-render, useMemo, useCallback, useEffect, Maximum update depth, React error 185.
compatibility: Antigravity, Claude Code, Cursor
metadata:
  version: "1.0"
  project: "stepleague"
---

# React Debugging Skill

## Overview

React's render cycle can cause infinite loops and performance issues. This skill covers the most common patterns that cause problems in StepLeague.

---

## ⚠️ Most Common Issues

### 1. "Maximum update depth exceeded" (React Error #185)

**Symptoms:**
- Page freezes or crashes
- Console shows "Maximum update depth exceeded"
- 1000s of re-renders before crash

**Root Causes:**

| Cause | Example | Fix |
|-------|---------|-----|
| Unstable dependency | `useEffect(() => {}, [searchParams])` | `useSearchParams()` returns new object each render |
| Missing memoization | `const items = data.filter(...)` | Wrap in `useMemo` |
| State update in render | `setCount(count + 1)` in component body | Move to `useEffect` |
| Object/array in deps | `useEffect(() => {}, [{ foo }])` | Destructure or use `.length` |

---

## Fix Patterns

### Pattern 1: useSearchParams Loops (REAL EXAMPLE)

**File:** `src/hooks/useFilterPersistence.ts`

**Problem:** `useSearchParams()` returns a new `URLSearchParams` object every render.

```typescript
// ❌ WRONG - This was causing infinite loops on /league/[id]/leaderboard
const searchParams = useSearchParams();

useEffect(() => {
  syncFilters(searchParams);
}, [searchParams]);  // New object every render = 7000+ renders → crash!
```

**Fix (from our codebase):**

```typescript
// ✅ CORRECT - Hydrate-once pattern (useFilterPersistence.ts lines 77-110)
const hasHydratedRef = useRef(false);

useEffect(() => {
  if (hasHydratedRef.current) return;  // Skip if already done
  hasHydratedRef.current = true;

  // Hydrate from URL/localStorage ONLY ONCE on mount
  const result = { ...defaults };
  syncKeys.forEach((key) => {
    const urlValue = searchParams.get(String(key));
    if (urlValue !== null) result[key] = urlValue;
  });
  
  setFiltersState(result);
  setIsHydrated(true);
}, []); // Empty deps - only run once on mount
```

---

### Pattern 2: Unstable Array References (REAL EXAMPLE)

**File:** `src/app/(dashboard)/submit-steps/page.tsx`

**Problem:** Creating new arrays in render causes infinite useEffect loops.

```typescript
// ❌ WRONG - This caused infinite loops (new array each render)
const adminLeagues = leagues.filter(l => l.role === "owner" || l.role === "admin");

useEffect(() => {
  loadProxies(adminLeagues);
}, [adminLeagues]);  // Infinite loop!
```

**Fix (from our codebase):**

```typescript
// ✅ CORRECT - Memoize the filtered array (submit-steps/page.tsx lines 78-82)
// Comment in code: "Memoize to prevent new array reference each render 
// (which would cause infinite useEffect loops)"
const adminLeagues = useMemo(() =>
  leagues.filter(l => l.role === "owner" || l.role === "admin"),
  [leagues]
);

// Now this is safe - adminLeagues only changes when leagues changes
useEffect(() => {
  loadProxies(adminLeagues);
}, [adminLeagues.length]); // Use .length for extra stability
```

---

### Pattern 3: Callback Stability

**Problem:** Inline callbacks cause child re-renders.

```typescript
// ❌ WRONG - New function every render
<ChildComponent onSelect={(item) => handleSelect(item)} />
```

**Fix:** Use `useCallback`:

```typescript
// ✅ CORRECT
const handleSelectMemo = useCallback((item) => {
  handleSelect(item);
}, [handleSelect]);

<ChildComponent onSelect={handleSelectMemo} />
```

---

## Debugging Checklist

When you hit a render loop:

- [ ] Check `useEffect` dependencies for objects/arrays
- [ ] Check for `useSearchParams()` in dependencies
- [ ] Check for inline object/array creation in render
- [ ] Add `console.log` at top of component to see render count
- [ ] Use React DevTools Profiler to identify re-renders

---

## Project-Specific Issues

### StepLeague Known Patterns

| File | Issue | Fix Applied |
|------|-------|-------------|
| `useFilterPersistence` | useSearchParams loop | Hydrate-once pattern |
| `submit-steps/page.tsx` | adminLeagues loop | useMemo for array |
| `LeagueInviteControl` | Dropdown not closing | useCallback for handlers |

---

## Related Skills

- `typescript-debugging` - Type errors that can cause render issues
- `architecture-philosophy` - When to extract to custom hooks
