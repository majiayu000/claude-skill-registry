---
name: web-framework-react
description: Component architecture, hooks, patterns
---

# React Components

> **Quick Guide:** Tiered components (Primitives -> Components -> Patterns -> Templates). React 19: pass `ref` as a prop directly (no `forwardRef` needed). Expose `className` prop for styling flexibility. Use `useActionState` for forms, `useOptimistic` for instant feedback, `use()` for conditional promise/context reading. Ref callbacks can return cleanup functions.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST pass `ref` as a regular prop in React 19 - `forwardRef` is deprecated)**

**(You MUST expose `className` prop on ALL reusable components for customization)**

**(You MUST use `useActionState` for form submissions with pending/error state)**

**(You MUST call `useFormStatus` from a child component inside `<form>`, NOT in the component that renders the form)**

</critical_requirements>

---

**Auto-detection:** React 19, components, hooks, use(), useActionState, useFormStatus, useOptimistic, Actions, ref as prop, ref cleanup, forwardRef migration, component variants, error boundary

**When to use:**

- Building React components with type-safe props
- Migrating from forwardRef to React 19 ref-as-prop
- Handling form submissions with React 19 Actions API
- Creating custom hooks for reusable logic
- Implementing error boundaries with retry

**When NOT to use:**

- Simple one-off components without variants (skip variant abstractions)
- Static content without interactivity

**Key patterns covered:**

- Component architecture tiers and variant props
- React 19 ref as prop (replaces forwardRef)
- React 19 hooks: `use()`, `useActionState`, `useFormStatus`, `useOptimistic`
- Ref callback cleanup functions
- Error boundaries with retry and custom fallbacks
- Custom hooks (pagination, debounce, localStorage)
- Event handler naming conventions

---

<philosophy>

## Philosophy

React components follow a tiered architecture from low-level primitives to high-level templates. Components should be composable, type-safe, and expose necessary customization points (`className`, refs). Use variant abstractions only when components have multiple variant dimensions to avoid over-engineering. React is styling-agnostic -- apply styles via the `className` prop.

**React 19 Changes:** `forwardRef` is deprecated -- pass `ref` as a regular prop directly. New hooks (`use()`, `useActionState`, `useFormStatus`, `useOptimistic`) simplify data fetching and form handling with the Actions API. Ref callbacks can return cleanup functions, eliminating the need for separate `useEffect` cleanup.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Component Architecture Tiers

Components are organized in a tiered hierarchy:

1. **Primitives** (`src/primitives/`) - Low-level building blocks (skeleton)
2. **Components** (`src/components/`) - Reusable UI (button, switch, select)
3. **Patterns** (`src/patterns/`) - Composed patterns (feature, navigation)
4. **Templates** (`src/templates/`) - Page layouts (frame)

```typescript
// React 19: ref as a regular prop, no forwardRef needed
export type ButtonProps = React.ComponentProps<"button"> & {
  variant?: "default" | "ghost" | "link";
  size?: "default" | "large" | "icon";
  asChild?: boolean;
  ref?: React.Ref<HTMLButtonElement>;
};

export function Button({ variant = "default", size = "default", className, ref, ...props }: ButtonProps) {
  return <button className={className} data-variant={variant} data-size={size} ref={ref} {...props} />;
}
```

**Why good:** ref as regular prop eliminates forwardRef boilerplate, className enables external styling, data-attributes enable CSS selectors for variants

See [examples/core.md](examples/core.md) for complete component examples with good/bad comparisons.

---

### Pattern 2: Component Variant Props

Components with 2+ visual dimensions (variant, size) should expose type-safe variant props via TypeScript unions. Use `data-*` attributes so any styling solution can target them.

```typescript
export type AlertVariant = "info" | "warning" | "error" | "success";

export function Alert({ variant = "info", className, ref, ...props }: AlertProps) {
  return <div ref={ref} className={className} data-variant={variant} {...props} />;
}
```

**When not to use:** Components with a single visual style -- skip variant abstraction.

See [examples/core.md](examples/core.md) for variant props with good/bad examples.

---

### Pattern 3: Event Handler Naming

- `handle` prefix for internal handlers: `handleSubmit`, `handleNameChange`
- `on` prefix for callback props: `onClick`, `onSubmit`
- Type events explicitly: `FormEvent<HTMLFormElement>`, `ChangeEvent<HTMLInputElement>`

```typescript
const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
  e.preventDefault();
};

const handleNameChange = (e: ChangeEvent<HTMLInputElement>) => {
  setName(e.target.value);
};
```

See [examples/core.md](examples/core.md) for full event handler examples.

---

### Pattern 4: Custom Hooks

Extract reusable logic into custom hooks following the `use` prefix convention.

- `usePagination` - Pagination state and navigation
- `useDebounce` - Debounce values for search inputs
- `useLocalStorage` - Type-safe localStorage persistence with SSR safety

See [examples/hooks.md](examples/hooks.md) for complete implementations.

---

### Pattern 5: Error Boundaries with Retry

Error boundaries catch render errors and provide retry capability. Place them around feature sections, not just the root.

```typescript
// Key interface -- accepts custom fallback and error callback
interface Props {
  children: ReactNode;
  fallback?: (error: Error, reset: () => void) => ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}
```

**Limitation:** Error boundaries do not catch event handler errors, async errors, or SSR errors -- use try/catch for those.

See [examples/error-boundaries.md](examples/error-boundaries.md) for full implementation.

---

### Pattern 6: useActionState for Form Submissions

**Skip if your framework provides its own server-side form handling (Server Actions) — use that instead.**

Use `useActionState` for form submissions with automatic pending state and error handling. Replaces manual `useState` for loading/error.

```typescript
import { useActionState } from "react";

async function updateProfile(prevState: string | null, formData: FormData) {
  try {
    await saveProfile({ name: formData.get("name") as string });
    return null;
  } catch {
    return "Failed to save profile";
  }
}

export function ProfileForm() {
  const [error, submitAction, isPending] = useActionState(updateProfile, null);

  return (
    <form action={submitAction}>
      <input type="text" name="name" disabled={isPending} />
      <button type="submit" disabled={isPending}>
        {isPending ? "Saving..." : "Save"}
      </button>
      {error && <p role="alert">{error}</p>}
    </form>
  );
}
```

**Why good:** hook manages pending and error state automatically, form action works with progressive enhancement, no manual useState for loading/error

See [examples/react-19-hooks.md](examples/react-19-hooks.md) for extended examples with success state.

---

### Pattern 7: useFormStatus for Submit Buttons

`useFormStatus` reads parent form's pending state without prop drilling. **Must** be called from a child component inside the `<form>`.

```typescript
import { useFormStatus } from "react-dom";

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending}>
      {pending ? "Submitting..." : "Submit"}
    </button>
  );
}
```

**Gotcha:** Calling `useFormStatus` in the component that renders `<form>` returns `pending: false` always -- it must be a descendant component.

See [examples/react-19-hooks.md](examples/react-19-hooks.md) for reusable submit button patterns.

---

### Pattern 8: useOptimistic for Instant UI Feedback

Show immediate UI updates while async operations complete. State automatically reverts if the request fails.

```typescript
import { useOptimistic, startTransition } from "react";

const [optimisticItems, addOptimistic] = useOptimistic(
  items,
  (state, update: Item) => [...state, { ...update, pending: true }],
);

// In handler -- setter MUST be called inside startTransition:
startTransition(async () => {
  addOptimistic(newItem);
  await saveItem(newItem);
});
```

See [examples/react-19-hooks.md](examples/react-19-hooks.md) for todo list and chat examples.

---

### Pattern 9: use() Hook for Promises and Context

`use()` reads promises and context conditionally in render -- unlike `useContext`, it can be called after early returns.

```typescript
import { use, Suspense } from "react";

function Comments({ commentsPromise }: { commentsPromise: Promise<Comment[]> }) {
  const comments = use(commentsPromise); // Suspends until resolved
  return <ul>{comments.map((c) => <li key={c.id}>{c.text}</li>)}</ul>;
}

// Wrap in Suspense boundary
<Suspense fallback={<p>Loading...</p>}>
  <Comments commentsPromise={fetchComments()} />
</Suspense>
```

**Gotcha:** `use()` cannot be called in try-catch blocks -- use Error Boundaries for rejected promise handling.

See [examples/react-19-hooks.md](examples/react-19-hooks.md) for conditional context reading.

---

### Pattern 10: Ref Callback Cleanup Functions

React 19 ref callbacks can return cleanup functions, replacing the need for separate `useEffect` cleanup.

```typescript
function VideoPlayer({ src }: { src: string }) {
  return (
    <video
      ref={(video) => {
        if (!video) return;
        video.play();
        return () => {
          video.pause();
          video.currentTime = 0;
        };
      }}
      src={src}
    />
  );
}
```

**Why good:** cleanup runs automatically on unmount, no separate useEffect needed, simpler than useRef + useEffect combination

**Note:** With ref cleanup functions, TypeScript rejects non-null/undefined return values from ref callbacks. The callback is no longer called with `null` on unmount -- the cleanup function handles that.

See [examples/react-19-hooks.md](examples/react-19-hooks.md) for IntersectionObserver cleanup example.

</patterns>

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Component architecture, variants, event handlers
- [examples/hooks.md](examples/hooks.md) - usePagination, useDebounce, useLocalStorage
- [examples/react-19-hooks.md](examples/react-19-hooks.md) - useActionState, useFormStatus, useOptimistic, use(), ref cleanup
- [examples/error-boundaries.md](examples/error-boundaries.md) - Error boundary implementation and recovery
- [reference.md](reference.md) - Decision frameworks, anti-patterns, checklists

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using `forwardRef` in React 19 -- deprecated, pass `ref` as a regular prop
- Calling `useFormStatus` in the component that renders `<form>` -- will always return `pending: false`
- Using `useState` for form loading/error when `useActionState` exists -- unnecessary boilerplate
- Not exposing `className` prop on reusable components -- prevents external styling
- Calling `use()` inside try-catch blocks -- use Error Boundaries instead

**Medium Priority Issues:**

- Adding variant abstractions for components without multiple variant dimensions
- Using `useCallback` on every handler regardless of child memoization (premature optimization)
- Wrapping ref callbacks in `useCallback` when the React Compiler handles memoization automatically
- Generic event handler names (`click`, `change`) instead of descriptive names (`handleNameChange`)

**Gotchas & Edge Cases:**

- Ref cleanup functions: TypeScript rejects non-null/undefined returns from ref callbacks -- use the cleanup pattern explicitly
- `useOptimistic` state reverts automatically on failure -- no manual rollback needed
- `use()` can be called conditionally (after early returns), unlike `useContext`
- Error boundaries do not catch event handler errors, async errors, or SSR errors
- `useCallback` without memoized children adds overhead without benefit
- SSR requires `typeof window !== "undefined"` before accessing browser APIs

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST pass `ref` as a regular prop in React 19 - `forwardRef` is deprecated)**

**(You MUST expose `className` prop on ALL reusable components for customization)**

**(You MUST use `useActionState` for form submissions with pending/error state)**

**(You MUST call `useFormStatus` from a child component inside `<form>`, NOT in the component that renders the form)**

**Failure to follow these rules will break component composition, form state management, and styling flexibility.**

</critical_reminders>
