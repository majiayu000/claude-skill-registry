---
name: hydration-safety
description: Next.js SSR hydration patterns and best practices. Use when fixing hydration mismatches, implementing client-only features, or working with localStorage/browser APIs.
---

# Hydration Safety Skill

## Overview

Next.js uses Server-Side Rendering (SSR), which means components render twice:

1. **Server-side** - Initial HTML generation
2. **Client-side** - React hydration with JavaScript

Mismatches between these two renders cause hydration errors. This skill covers patterns to prevent and fix these issues.

## The Core Problem

```typescript
// ❌ WRONG - Causes hydration mismatch
function Component() {
  const user = localStorage.getItem("user"); // localStorage not available on server
  return <div>Welcome {user}</div>;
}
```typescript

**Error:** "Text content does not match server-rendered HTML"

**Why:** Server renders `<div>Welcome </div>`, client tries to render `<div>Welcome John</div>`

## The isMounted Pattern (CRITICAL)

This is the **standard solution** for hydration-safe components:

```typescript
"use client";
import { useState, useEffect } from "react";

function Component() {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  // Return null or skeleton during SSR
  if (!isMounted) {
    return null; // or <Skeleton />
  }

  // Only runs on client after hydration
  const user = localStorage.getItem("user");
  return <div>Welcome {user}</div>;
}
```typescript

### How It Works

1. **Server-side:** `isMounted = false`, component returns `null`
2. **Client-side (first render):** `isMounted = false`, still returns `null`
3. **Client-side (after useEffect):** `isMounted = true`, renders with browser APIs
4. **Result:** Server and first client render match perfectly

## Common Hydration Triggers

### 1. Browser APIs

❌ **Causes Hydration Errors:**

- `localStorage`
- `sessionStorage`
- `window`
- `document`
- `navigator`
- Date/time without consistent timezone

✅ **Solution:** Use isMounted pattern

### 2. Random Values

```typescript
// ❌ WRONG
function Component() {
  const id = Math.random(); // Different on server vs client
  return <div id={id}>Content</div>;
}

// ✅ CORRECT
function Component() {
  const [id, setId] = useState<string>();

  useEffect(() => {
    setId(String(Math.random()));
  }, []);

  return <div id={id}>Content</div>;
}
```typescript

### 3. Date/Time

```typescript
// ❌ WRONG
function Clock() {
  return <div>{new Date().toLocaleTimeString()}</div>;
}

// ✅ CORRECT
"use client";
function Clock() {
  const [time, setTime] = useState<string>();

  useEffect(() => {
    setTime(new Date().toLocaleTimeString());
    const interval = setInterval(() => {
      setTime(new Date().toLocaleTimeString());
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  if (!time) return <div>--:--:--</div>; // Placeholder
  return <div>{time}</div>;
}
```typescript

## Implementation Patterns

### Pattern 1: Null During SSR

```typescript
"use client";
function Component() {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) return null;

  return <div>{/* Browser-dependent content */}</div>;
}
```typescript

**Use when:** Component doesn't need to show during SSR

### Pattern 2: Skeleton During SSR

```typescript
"use client";
function Component() {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    return <div className="animate-pulse bg-surf-1 h-10 w-32" />;
  }

  return <div>{/* Actual content */}</div>;
}
```typescript

**Use when:** Need loading state visible during SSR

### Pattern 3: Safe Defaults

```typescript
"use client";
function Component() {
  const [data, setData] = useState<string>("default");

  useEffect(() => {
    const stored = localStorage.getItem("key");
    if (stored) setData(stored);
  }, []);

  return <div>{data}</div>;
}
```typescript

**Use when:** Can show default value during SSR

## Project-Specific Patterns

### Sidebar Assistant (Example from codebase)

Location: `src/components/chat/chat-sidebar.tsx`

```typescript
"use client";
export function ChatSidebar() {
  const [isMounted, setIsMounted] = useState(false);
  const { isPinned, width } = useChatSidebar();

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    return null; // Sidebar hidden during SSR
  }

  return (
    <div style={{ width: `${width}px` }}>
      {/* Sidebar content */}
    </div>
  );
}
```typescript

### Global Chat Button

Location: `src/components/global-chat-button.tsx`

```typescript
"use client";
export function GlobalChatButton() {
  const { isOpen } = useChatSidebar();
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, [isOpen]); // Added isOpen to dependency array

  // Early return AFTER all hooks
  if (!isMounted || isOpen) {
    return null;
  }

  return <button>Open Chat</button>;
}
```typescript

**Note:** All hooks must be called before conditional returns!

## Testing Hydration Safety

### Unit Tests

```typescript
import { render, screen } from "@testing-library/react";
import { act } from "react";

describe("Hydrated Component", () => {
  it("should not show content during SSR", () => {
    render(<Component />);
    expect(screen.queryByTestId("hydrated-content")).not.toBeInTheDocument();
  });

  it("should show content after mount", async () => {
    render(<Component />);

    // Wait for useEffect
    await act(async () => {
      await new Promise((resolve) => setTimeout(resolve, 0));
    });

    expect(screen.getByTestId("hydrated-content")).toBeInTheDocument();
  });
});
```typescript

### E2E Tests (Playwright)

```typescript
import { test, expect } from "@playwright/test";

test("should handle hydration correctly", async ({ page }) => {
  await page.goto("/", { waitUntil: "networkidle" });

  // Wait for React hydration to complete
  await page.waitForSelector('[data-testid="hydrated-component"]', {
    state: "attached",
    timeout: 10000,
  });

  // Wait for loading spinner to disappear (if present)
  await page.waitForSelector(".animate-spin", {
    state: "detached",
    timeout: 10000,
  });

  // Additional stabilization time
  await page.waitForTimeout(500);

  // Now safe to interact
  await page.click('[data-testid="interactive-element"]');
});
```typescript

### Why E2E Waits Are Critical

Without waits, E2E tests run on intermediate DOM states:

```typescript
// ❌ WRONG - Runs too early
test("wrong timing", async ({ page }) => {
  await page.goto("/");
  await page.click("button"); // May not be hydrated yet!
});

// ✅ CORRECT - Waits for hydration
test("correct timing", async ({ page }) => {
  await page.goto("/", { waitUntil: "networkidle" });
  await page.waitForSelector('[data-testid="ready"]');
  await page.waitForTimeout(500); // DOM stabilization
  await page.click("button"); // Now safe!
});
```typescript

## Debugging Hydration Errors

### Error Messages

**"Text content does not match server-rendered HTML"**

- Cause: Different text rendered on server vs client
- Solution: Use isMounted pattern or ensure consistent data

**"Hydration failed because the initial UI does not match"**

- Cause: Different structure rendered on server vs client
- Solution: Make server and client render the same initially

**"There was an error while hydrating"**

- Cause: Component error during hydration
- Solution: Check browser console for specific error

### Debugging Steps

1. **Check Browser Console** - Specific error details appear here
2. **Inspect Network Tab** - Compare SSR HTML vs hydrated DOM
3. **Use React DevTools** - Highlight hydration mismatches
4. **Add data-testid After Mount** - Verify component is hydrated

```typescript
return (
  <div data-testid={isMounted ? "hydrated" : undefined}>
    Content
  </div>
);
```typescript

5. **Check localStorage/sessionStorage Access** - Most common cause

## React Hooks Rules with Hydration

### ⚠️ Critical: Hooks Before Returns

```typescript
// ❌ WRONG - Hook after conditional return
function Component() {
  const { isOpen } = useContext();

  if (!isOpen) return null; // Early return

  useEffect(() => {  // ❌ Hook after return!
    // ...
  }, []);
}

// ✅ CORRECT - All hooks before returns
function Component() {
  const { isOpen } = useContext();
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {  // ✓ Hook before return
    setIsMounted(true);
  }, []);

  if (!isOpen || !isMounted) return null; // After all hooks
}
```typescript

## Common Mistakes

### Mistake 1: Checking window Directly

```typescript
// ❌ WRONG
function Component() {
  if (typeof window === "undefined") return null;
  return <div>{localStorage.getItem("key")}</div>;
}
```typescript

**Problem:** First client render still won't match server

### Mistake 2: Forgetting "use client"

```typescript
// ❌ WRONG - Missing directive
import { useState, useEffect } from "react";

function Component() {
  const [mounted, setMounted] = useState(false);
  // ...
}
```typescript

**Problem:** Server components can't use hooks

### Mistake 3: Using useLayoutEffect

```typescript
// ❌ WRONG - Causes SSR warnings
useLayoutEffect(() => {
  setIsMounted(true);
}, []);

// ✅ CORRECT - Use useEffect for hydration
useEffect(() => {
  setIsMounted(true);
}, []);
```typescript

## Checklist for Hydration-Safe Components

- [ ] Add "use client" directive if using hooks
- [ ] All hooks called before conditional returns
- [ ] Use isMounted pattern for browser APIs
- [ ] Return consistent structure during SSR and first client render
- [ ] Add data-testid after mount for E2E tests
- [ ] Test component in both SSR and client contexts
- [ ] Verify no hydration errors in browser console
- [ ] E2E tests wait for hydration before interactions

## Quick Reference

```typescript
// Standard isMounted pattern
const [isMounted, setIsMounted] = useState(false);
useEffect(() => { setIsMounted(true); }, []);
if (!isMounted) return null;

// E2E wait pattern
await page.goto("/", { waitUntil: "networkidle" });
await page.waitForSelector('[data-testid="ready"]');
await page.waitForTimeout(500);

// Debug in browser
// Check: document.documentElement.dataset.reactHydrated
```typescript

## Related Files

- `src/components/chat/chat-sidebar.tsx` - Production example
- `src/components/global-chat-button.tsx` - Production example
- `e2e/a11y.spec.ts` - E2E hydration patterns
- `src/lib/chat-sidebar-context.tsx` - Context with hydration safety
