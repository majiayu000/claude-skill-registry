---
name: latest-react
description: Latest React features from React 19 and React Compiler (past 1.5 years - mid 2024 to 2026)
updated: 2026-01-11
---

# Latest React Skill

Comprehensive knowledge of React features released from mid-2024 through 2026, focusing on **React 19** (released December 2024, latest v19.2+), **React Compiler** (RC April 2025), and supporting ecosystem changes.

## Official Resources

- [React v19 Official Announcement](https://react.dev/blog/2024/12/05/react-19)
- [React Versions](https://react.dev/versions)
- [React 19 Upgrade Guide](https://react.dev/blog/2024/04/25/react-19-upgrade-guide)
- [React 19.2 Release](https://react.dev/blog/2025/10/01/react-19-2)

## Major Features by Category

### 1. New Hooks (React 19)

#### `useActionState`

Manages state for asynchronous actions, particularly useful for form submissions and mutations.

```tsx
import { useActionState } from "react";

async function submitForm(prevState, formData) {
  // Handle form submission
  const result = await submitToAPI(formData);
  return { success: true, message: "Submitted!" };
}

function MyForm() {
  const [state, formAction, isPending] = useActionState(submitForm, null);

  return (
    <form action={formAction}>
      <input name="email" />
      <button type="submit" disabled={isPending}>
        {isPending ? "Submitting..." : "Submit"}
      </button>
      {state?.message && <p>{state.message}</p>}
    </form>
  );
}
```

**Use cases**: Form submissions, mutations, any async action that needs pending/error states

#### `useOptimistic`

Handles optimistic UI updates while waiting for async operations to complete.

```tsx
import { useOptimistic } from "react";

function LikeButton({ postId, initialLikes }) {
  const [optimisticLikes, addOptimisticLike] = useOptimistic(
    initialLikes,
    (state, newLike) => state + newLike
  );

  async function handleLike() {
    addOptimisticLike(1);
    await updateLikes(postId);
  }

  return <button onClick={handleLike}>{optimisticLikes} likes</button>;
}
```

**Use cases**: Like buttons, todo lists, any UI that can show predicted state

#### `useFormStatus`

Accesses parent form submission status from within a child component.

```tsx
import { useFormStatus } from "react";

function SubmitButton() {
  const { pending, data, method, action } = useFormStatus();

  return (
    <button disabled={pending}>{pending ? "Submitting..." : "Submit"}</button>
  );
}

function MyForm() {
  return (
    <form action={submitAction}>
      <input name="field" />
      <SubmitButton />
    </form>
  );
}
```

**Use cases**: Form submit buttons, progress indicators, child components that need form state

### 2. Actions & Async Transitions

React 19 adds support for using async functions directly in transitions.

```tsx
import { useTransition } from "react";

function SearchComponent() {
  const [isPending, startTransition] = useTransition();

  function handleSearch(query: string) {
    startTransition(async () => {
      // Automatic pending state, error handling, and optimistic updates
      await searchAPI(query);
    });
  }

  return <input onChange={(e) => handleSearch(e.target.value)} />;
}
```

**Key capabilities**:

- Automatic pending state management
- Built-in error handling
- Support for optimistic updates
- Non-blocking UI updates

### 3. API Simplifications

#### Context Providers - No More `.Provider`

**Before React 19**:

```tsx
<MyContext.Provider value={someValue}>{children}</MyContext.Provider>
```

**React 19+**:

```tsx
<MyContext value={someValue}>{children}</MyContext>
```

#### Ref as a Prop - No More `forwardRef`

**Before React 19**:

```tsx
const MyButton = forwardRef((props, ref) => {
  return <button ref={ref} {...props} />;
});
```

**React 19+**:

```tsx
const MyButton = ({ ref, ...props }) => {
  return <button ref={ref} {...props} />;
};
```

The `ref` prop is now a standard prop that can be passed directly to function components.

### 4. Document Metadata Support

React 19 introduces native support for document metadata. You can now place `<title>`, `<meta>`, and `<link>` tags directly in components, and React automatically "hoists" them to the `<head>` section.

```tsx
function BlogPost({ title, description }) {
  return (
    <>
      <title>{title} | My Blog</title>
      <meta name="description" content={description} />
      <meta property="og:title" content={title} />
      <link rel="canonical" href={`https://example.com/blog/${slug}`} />

      <article>
        <h1>{title}</h1>
        {/* Post content */}
      </article>
    </>
  );
}
```

**Benefits**:

- No more third-party libraries needed for SEO metadata
- Works from nested components
- Automatic deduplication
- Server-side rendering support

### 5. Enhanced Ref Callbacks

Ref callbacks can now return cleanup functions that run when the component unmounts.

```tsx
function MyComponent() {
  const buttonRef = useCallback((element: HTMLButtonElement | null) => {
    if (!element) return; // cleanup on unmount

    const handler = () => console.log("Clicked!");
    element.addEventListener("click", handler);

    // Cleanup function
    return () => {
      element.removeEventListener("click", handler);
    };
  }, []);

  return <button ref={buttonRef}>Click me</button>;
}
```

### 6. Server Functions (formerly Server Actions)

As of September 2024, "Server Actions" were renamed to **Server Functions**. They integrate with Server Components and work seamlessly with `<Suspense>`.

```tsx
// Server Component
"use server";

export async function createUser(formData: FormData) {
  const user = await db.users.create({
    email: formData.get("email"),
  });
  return user;
}

// Client Component usage
import { createUser } from "./actions";

function UserForm() {
  return (
    <form action={createUser}>
      <input name="email" />
      <button type="submit">Create User</button>
    </form>
  );
}
```

### 7. Custom Elements Support

React 19 now has full support for Custom Elements (Web Components), addressing previous limitations with attribute handling and event propagation.

### 8. Hydration Improvements

- **Graceful DOM mismatch handling**: Better handling of unexpected DOM changes from third-party scripts
- **Enhanced error messages**: More detailed hydration error diffs
- **Consolidated error logging**: Single error containing all information instead of multiple console errors

### 9. New Error Callbacks

React 19 introduces new error handling callbacks at the root:

```tsx
createRoot(document.getElementById("root")!, {
  onCaughtError: (error, errorInfo) => {
    // Errors caught by Error Boundaries
    console.error("Caught error:", error, errorInfo);
  },
  onUncaughtError: (error, errorInfo) => {
    // Errors NOT caught by Error Boundaries
    console.error("Uncaught error:", error, errorInfo);
  },
});
```

### 10. Resource Preloading & Stylesheet Management

Native support for managing resource loading priorities:

```tsx
function Page() {
  return (
    <>
      <link rel="preload" href="/styles.css" as="style" />
      <link rel="stylesheet" href="/styles.css" />
    </>
  );
}
```

### 11. React Compiler (RC - April 2025)

The React Compiler is now feature-complete and production-ready.

**Key capabilities**:

- **Automatic memoization**: Eliminates need for manual `useMemo` and `useCallback`
- **Enhanced debugging**: New tools including Owner Stack
- **Performance optimization**: Automatic detection and optimization of re-renders

**Before Compiler**:

```tsx
const memoizedValue = useMemo(() => expensiveCalc(a, b), [a, b]);
const memoizedCallback = useCallback(() => doSomething(a, b), [a, b]);
```

**With Compiler**:

```tsx
// Compiler automatically optimizes - no hooks needed
const value = expensiveCalc(a, b);
const callback = () => doSomething(a, b);
```

### 12. Strict Mode Changes (React 19)

React 19 includes fixes to Strict Mode behavior:

- **useEffect double execution fixed**: No more double API calls in development
- **Better useMemo/useCallback behavior**: Improved behavior during double rendering
- **Clearer migration path**: Better guidance for Strict Mode issues

### 13. Enhanced Suspense Support

Improved Suspense integration with Server Components and Server Functions:

```tsx
<Suspense fallback={<Loading />}>
  <AsyncComponent />
</Suspense>
```

Streaming and loading states are now core features of React Server Components + Suspense.

## Migration Guide

### Upgrading to React 19

1. **Remove deprecated APIs**:

   - Replace `React.PropTypes` with `prop-types` package
   - Remove `ReactDOM.render` - use `createRoot`
   - Remove `UNSAFE_` lifecycle methods

2. **Simplify components**:

   - Remove `forwardRef` wrappers
   - Update Context providers to new syntax
   - Replace manual memoization where Compiler is used

3. **Update forms**:

   - Consider using `useActionState` for form submissions
   - Use `useFormStatus` in child components
   - Leverage Actions for async transitions

4. **Error handling**:
   - Add `onCaughtError` and `onUncaughtError` callbacks
   - Update Error Boundaries for better error info

## Best Practices (2025+)

1. **Prefer new hooks**: Use `useActionState`, `useOptimistic`, and `useFormStatus` for forms and async actions

2. **Simplify with Compiler**: Let React Compiler handle memoization instead of manual `useMemo`/`useCallback`

3. **Use native metadata**: Place `<title>`, `<meta>`, `<link>` directly in components instead of third-party libraries

4. **Leverage Server Functions**: Use Server Functions for mutations and data fetching when possible

5. **Utilize Actions**: Use async transitions with automatic error/pending state management

6. **Remove boilerplate**: Take advantage of the new simplified APIs (no `forwardRef`, no `.Provider`)

## Common Patterns (2025 Style)

### Form with Loading State

```tsx
function ContactForm() {
  const [state, formAction, isPending] = useActionState(submitContact, null);

  return (
    <form action={formAction}>
      <input name="email" disabled={isPending} />
      <button type="submit" disabled={isPending}>
        {isPending ? "Sending..." : "Send"}
      </button>
      {state?.error && <p className="error">{state.error}</p>}
      {state?.success && <p className="success">{state.success}</p>}
    </form>
  );
}
```

### Optimistic List Updates

```tsx
function TodoList({ initialTodos }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    initialTodos,
    (state, newTodo) => [...state, newTodo]
  );

  async function addTodo(text: string) {
    addOptimisticTodo({ id: Date.now(), text, pending: true });
    await api.addTodo(text);
  }

  return (
    <ul>
      {optimisticTodos.map((todo) => (
        <li key={todo.id} style={{ opacity: todo.pending ? 0.5 : 1 }}>
          {todo.text}
        </li>
      ))}
    </ul>
  );
}
```

### Document Metadata by Route

```tsx
function BlogPostPage({ slug }) {
  const post = use(fetchPost(slug));

  if (!post) return null;

  return (
    <>
      <title>{post.title} | My Blog</title>
      <meta name="description" content={post.excerpt} />
      <meta property="og:title" content={post.title} />
      <meta property="og:description" content={post.excerpt} />
      <meta property="og:image" content={post.image} />

      <article>{post.content}</article>
    </>
  );
}
```

## Ecosystem Considerations

### Next.js Integration

- Next.js 15+ supports React 19
- Server Actions renamed to Server Functions aligns with Next.js conventions
- App Router works seamlessly with React 19 features

### Testing

- React 19 is compatible with React Testing Library
- New hooks work with existing test patterns
- Strict Mode fixes improve test reliability

### TypeScript Support

- Full TypeScript support for all new APIs
- Updated `@types/react` available
- Better type inference for Actions

## Sources & Further Reading

- [React v19 Official Blog](https://react.dev/blog/2024/12/05/react-19)
- [React 19 Upgrade Guide](https://react.dev/blog/2024/04/25/react-19-upgrade-guide)
- [React 19.2 Release](https://react.dev/blog/2025/10/01/react-19-2)
- [React Versions](https://react.dev/versions)
- [Exploring New Hooks in React 19](https://www.manuelsanchezdev.com/blog/react-19-new-hooks-useoptimistic-useformstatus-useactionstate)
- [React 19: The 3 Simplifications You'll Love](https://medium.com/@janek.lewandoski/react-19-the-3-simplifications-youll-love-584b9843c05f)
- [What's New in React 19 - Vercel](https://vercel.com/blog/whats-new-in-react-19)
- [React 19 New Hooks Explained - freeCodeCamp](https://www.freecodecamp.org/news/react-19-new-hooks-explained-with-examples/)
- [React 19 Concurrency Deep Dive](https://dev.to/a1guy/react-19-concurrency-deep-dive-mastering-usetransition-and-starttransition-for-smoother-uis-51eo)
- [Server Functions Documentation](https://react.dev/reference/rsc/server-functions)
