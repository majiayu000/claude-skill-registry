---
name: latest-nextjs
description: Latest React and Next.js features for past 1.5 years (mid-2024 to 2026)
updated: 2026-01-11
---

# Latest React & Next.js Skill

Comprehensive knowledge of React and Next.js features from mid-2024 through 2025. This skill fills the gap between LLM training cutoffs and current knowledge, covering **React 19.2** (October 2025), **Next.js 16** (October 2025), and supporting ecosystem changes.

## React 19.2 (Latest - October 2025)

### Current Status

- **Latest stable version**: React 19.2 (released October 1, 2025)
- **Previous updates**: React 19.1 (March 2025 - refinement release)
- **Initial release**: React 19 (December 2024)

### Key Improvements in 19.1-19.2

- No breaking changes from 19.0
- Performance optimizations
- Enhanced DevTools features
- 30-40% smaller JavaScript bundle sizes
- Faster TTFB (Time to First Byte)

## React 19 Core Features

### New Hooks

#### `useOptimistic`

Manages optimistic UI updates during async mutations:

```tsx
import { useOptimistic } from "react";

function LikeButton({ postId, initialLiked }) {
  const [optimisticLiked, addOptimistic] = useOptimistic(
    initialLiked,
    (state, newLiked) => !state
  );

  async function handleToggle() {
    addOptimistic(!optimisticLiked);
    await toggleLike(postId);
  }

  return (
    <button onClick={handleToggle}>
      {optimisticLiked ? "Unlike" : "Like"}
    </button>
  );
}
```

**Use cases**: Like buttons, todo lists, any UI showing predicted state during server updates.

#### `useActionState`

Connects forms to action functions and tracks response state:

```tsx
import { useActionState } from "react";

const [state, formAction, isPending] = useActionState(
  async (prevState, formData) => {
    const email = formData.get("email");
    await subscribe(email);
    return { success: true, message: "Subscribed!" };
  },
  null
);
```

**Replaces**: Manual form state management, loading states, error handling.

#### `useFormStatus`

Accesses parent form status from nested components:

```tsx
import { useFormStatus } from "react";

function SubmitButton() {
  const { pending, data, method, action } = useFormStatus();
  return (
    <button disabled={pending}>{pending ? "Sending..." : "Submit"}</button>
  );
}
```

**Key use case**: Submit buttons that need parent form state.

#### Enhanced `useTransition`

Now supports async functions with automatic state management:

```tsx
const [isPending, startTransition] = useTransition();

startTransition(async () => {
  // Automatic pending, error, and optimistic UI handling
  await searchAPI(query);
});
```

#### New `use` Hook

Reads resources (Promises, Context) in render:

```tsx
import { use } from "react";

// Read promises in Server Components
const data = use(fetchPromise);

// Read context
const theme = use(ThemeContext);
```

**Use case**: Streaming data in Server Components without useEffect.

### Server Components (Stable)

Production-ready and used at scale by Meta (Facebook, Instagram):

```tsx
// Server Component - runs on server only
async function BlogPost({ id }) {
  const post = await db.post.findUnique({ where: { id } });
  return <article>{post.content}</article>;
}
```

**Key characteristics:**

- Zero JavaScript bundled to client
- Direct database access
- Build-time or per-request rendering
- Next.js defaults to Server Components

### React Compiler (Stable Integration with Next.js 16)

Automatically optimizes components without manual memoization:

**Before:**

```tsx
const memoizedValue = useMemo(() => expensiveCalc(a, b), [a, b]);
const memoizedCallback = useCallback(() => doSomething(a, b), [a, b]);
```

**With Compiler:**

```tsx
// Compiler automatically optimizes
const value = expensiveCalc(a, b);
const callback = () => doSomething(a, b);
```

**Capabilities:**

- Eliminates need for useMemo/useCallback in most cases
- Automatic re-render optimization
- Integrated and stable in Next.js 16

### Server Functions (formerly Server Actions)

Simplified server-side mutations:

```tsx
// app/actions.ts
"use server";

export async function updateProfile(formData: FormData) {
  const name = formData.get("name");
  await db.user.update({ where: { id }, data: { name } });
}

// Client Component usage
import { updateProfile } from "./actions";

export default function ProfileForm() {
  return (
    <form action={updateProfile}>
      <input name="name" />
      <button type="submit">Update</button>
    </form>
  );
}
```

### Simplified Forms

React 19 eliminates much of the complexity:

```tsx
// No more controlled state needed
export default function ContactForm() {
  return (
    <form
      action={async (formData) => {
        await submitToServer(formData);
      }}
    >
      <input name="email" />
      <button type="submit">Submit</button>
    </form>
  );
}
```

### API Simplifications

#### Context Providers - No More `.Provider`

```tsx
// Before
<MyContext.Provider value={value}>{children}</MyContext.Provider>

// React 19+
<MyContext value={value}>{children}</MyContext>
```

#### Ref as Prop - No More `forwardRef`

```tsx
// Before
const Button = forwardRef((props, ref) => <button ref={ref} {...props} />);

// React 19+
const Button = ({ ref, ...props }) => <button ref={ref} {...props} />;
```

### Document Metadata Support

Place `<title>`, `<meta>`, `<link>` directly in components:

```tsx
function BlogPost({ title, description }) {
  return (
    <>
      <title>{title} | My Blog</title>
      <meta name="description" content={description} />
      <meta property="og:title" content={title} />
      <article>{content}</article>
    </>
  );
}
```

React automatically "hoists" these to `<head>`.

### Enhanced Ref Callbacks

Ref callbacks can now return cleanup functions:

```tsx
const buttonRef = useCallback((element: HTMLButtonElement | null) => {
  if (!element) return; // cleanup on unmount

  const handler = () => console.log("Clicked");
  element.addEventListener("click", handler);

  return () => element.removeEventListener("click", handler);
}, []);
```

### Improved Hydration

- Better handling of third-party script DOM mutations
- Enhanced error messages with detailed diffs
- Consolidated error logging

### New Error Callbacks

```tsx
createRoot(document.getElementById("root")!, {
  onCaughtError: (error, errorInfo) => {
    // Errors caught by Error Boundaries
    console.error("Caught:", error, errorInfo);
  },
  onUncaughtError: (error, errorInfo) => {
    // Errors NOT caught by Error Boundaries
    console.error("Uncaught:", error, errorInfo);
  },
});
```

### Custom Elements Support

Full support for Web Components with proper attribute and event handling.

## Next.js 16 (Released October 2025)

### Major Changes

#### Turbopack - Now Default & Stable

Turbopack is now the default bundler for both `next dev` and `next build`:

```bash
# Turbopack is now default - no flags needed
next dev
next build
```

**Performance improvements:**

- 5-10x faster Fast Refresh
- Significantly faster builds
- Production-ready stability

#### Cache Components (New Programming Model)

**Cache Components** replace Partial Prerendering (PPR) with a more explicit caching model:

```tsx
// next.config.js - Enable Cache Components
export default {
  cacheComponents: true, // Opt-in feature
};
```

**Key characteristics:**

- More explicit and flexible than implicit App Router caching
- Requires opt-in via config flag
- Component-level caching control
- Supersedes experimental PPR from Next.js 15

#### `proxy.ts` Replaces `middleware.ts`

Middleware has been renamed to **proxy**:

```tsx
// Before: middleware.ts
export function middleware(request: NextRequest) {
  // logic
}

// After: proxy.ts
export function proxy(request: NextRequest) {
  // Same logic, just renamed
}
```

**Migration:**

```bash
# Automated codemod available
npx @next/codemod@canary middleware-to-proxy
```

**What changed:**

- File renamed: `middleware.ts` → `proxy.ts`
- Export renamed: `middleware` → `proxy`
- Logic remains identical
- Runs on Node.js runtime

#### Async Route Parameters (Breaking Change)

Route parameters are now async:

```tsx
// Before Next.js 16
export default async function Page({ params, searchParams }) {
  const id = params.id;
  const query = searchParams.q;
}

// Next.js 16+
export default async function Page({ params, searchParams }) {
  const id = await params.id; // Now async!
  const query = await searchParams.q; // Now async!
}
```

**This is a breaking change** requiring migration of components using params/searchParams.

#### React 19.2 Integration

Full compatibility and optimization for React 19.2 features.

#### Deprecated APIs Removed

- Various `unstable_` APIs promoted to stable
- Old middleware convention fully removed
- Legacy caching patterns removed

### Next.js 15 Features (Still Relevant)

#### App Router (Default)

File-system based router with Server Components:

```
app/
  layout.tsx      # Root layout
  page.tsx        # Home page
  blog/
    layout.tsx    # Blog section layout
    [slug]/       # Dynamic route
      page.tsx    # Blog post page
```

#### Server Actions (Stable)

Direct server-side mutations from client components:

```tsx
// app/actions.ts
"use server";

export async function createTodo(formData: FormData) {
  const title = formData.get("title");
  await db.todo.create({ data: { title } });
}

// app/page.tsx
import { createTodo } from "./actions";

export default function Page() {
  return (
    <form action={createTodo}>
      <input name="title" />
      <button type="submit">Add</button>
    </form>
  );
}
```

#### Server Components (Default)

All components in `app/` are Server Components by default:

```tsx
// Server Component - no 'use client' needed
async function Dashboard() {
  const user = await getCurrentUser();
  const posts = await db.post.findMany();

  return <div>Welcome {user.name}</div>;
}
```

Add `'use client'` directive only for:

- Event handlers (`onClick`, etc.)
- React hooks (`useState`, `useEffect`, etc.)
- Browser APIs

#### Improved Caching

More predictable and granular caching:

- Better defaults for data fetching
- Explicit cache control via `revalidatePath`/`revalidateTag`
- `fetch` requests cached by default

```tsx
// Cache for 1 hour
const data = await fetch("https://api.example.com/data", {
  next: { revalidate: 3600 },
});

// Invalidate on demand
revalidatePath("/blog");
revalidateTag("posts");
```

#### `after()` API

Post-response operations:

```tsx
import { after } from "next/server";

export default function handler() {
  after(() => {
    // Runs after response is sent to client
    analytics.track();
  });
  return <Response />;
}
```

## Best Practices (2025-2026)

### Server-First Mental Model

1. **Default to Server Components** - Only use Client Components for interactivity
2. **Leverage Server Functions** - Replace API routes for mutations
3. **Stream with Suspense** - Progressive loading for better UX
4. **Push state to edges** - Client components only where necessary

### Form Handling Pattern

```tsx
// Server Action
"use server";
async function submitContact(prevState, formData) {
  const email = formData.get("email");
  await db.contact.create({ data: { email } });
  return { success: true };
}

// Client Component
("use client");
import { useActionState } from "react";
import { submitContact } from "./actions";

export default function ContactForm() {
  const [state, formAction, isPending] = useActionState(submitForm, null);

  return (
    <form action={formAction}>
      <input name="email" disabled={isPending} />
      <button disabled={isPending}>
        {isPending ? "Sending..." : "Submit"}
      </button>
      {state?.success && <p>Thanks!</p>}
    </form>
  );
}
```

### Optimistic UI Pattern

```tsx
"use client";
import { useOptimistic } from "react";
import { toggleLike } from "./actions";

function LikeButton({ postId, initialLiked }) {
  const [optimisticLiked, addOptimistic] = useOptimistic(
    initialLiked,
    (state) => !state
  );

  return (
    <button
      formAction={async () => {
        addOptimistic();
        await toggleLike(postId);
      }}
    >
      {optimisticLiked ? "Unlike" : "Like"}
    </button>
  );
}
```

### Server Component Data Fetching

```tsx
// Simple, direct database access
async function BlogList() {
  const posts = await db.post.findMany({
    orderBy: { createdAt: "desc" },
  });

  return (
    <div>
      {posts.map((post) => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.excerpt}</p>
        </article>
      ))}
    </div>
  );
}
```

### Streaming with Suspense

```tsx
import { Suspense } from "react";

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<StatsSkeleton />}>
        <Stats />
      </Suspense>
      <Suspense fallback={<PostsSkeleton />}>
        <RecentPosts />
      </Suspense>
    </div>
  );
}
```

## Migration Guides

### Next.js 15 → 16

1. **Update async params:**

   ```tsx
   // Add await to all params/searchParams access
   const id = await params.id;
   ```

2. **Rename middleware to proxy:**

   ```bash
   npx @next/codemod@canary middleware-to-proxy
   ```

3. **Enable Turbopack** (already default, but verify):

   ```bash
   next dev --turbo  # Should be default now
   ```

4. **Consider Cache Components:**
   ```js
   // next.config.js
   export default {
     cacheComponents: true, // Opt-in for new caching model
   };
   ```

### React 18 → 19

1. **Update forms to use Actions**
2. **Simplify components** - Remove `forwardRef`, update Context syntax
3. **Remove manual memoization** where React Compiler is active
4. **Add error callbacks** to `createRoot`
5. **Migrate to native metadata** instead of third-party libraries

### Pages Router → App Router

| Pages Router            | App Router                                      |
| ----------------------- | ----------------------------------------------- |
| `pages/index.js`        | `app/page.tsx`                                  |
| `getServerSideProps`    | async Server Component                          |
| `getStaticProps`        | async Server Component + `generateStaticParams` |
| `getStaticPaths`        | `generateStaticParams`                          |
| `_app.js`               | `app/layout.tsx`                                |
| `_document.js`          | `app/layout.tsx`                                |
| API routes `pages/api/` | Route handlers `app/api/`                       |

## Common Patterns

### Document Metadata by Route

```tsx
// app/blog/[slug]/page.tsx
export async function generateMetadata({ params }) {
  const post = await getPost(params.slug);
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      images: [post.ogImage],
    },
  };
}
```

### Loading States

```tsx
// app/blog/loading.tsx
export default function Loading() {
  return <BlogListSkeleton />;
}

// Or inline Suspense
export default function BlogPage() {
  return (
    <Suspense fallback={<BlogListSkeleton />}>
      <BlogList />
    </Suspense>
  );
}
```

### Error Handling

```tsx
// app/blog/error.tsx
"use client";

export default function Error({ error, reset }) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

## Resources

### Official Documentation

- [React 19 Official Blog](https://react.dev/blog/2024/12/05/react-19)
- [React 19.2 Release](https://react.dev/blog/2025/10/01/react-19-2)
- [React Versions](https://react.dev/versions)
- [Next.js 16 Official Blog](https://nextjs.org/blog/next-16)
- [Next.js 16 Upgrade Guide](https://nextjs.org/docs/app/guides/upgrading/version-16)
- [Cache Components Documentation](https://nextjs.org/docs/app/getting-started/cache-components)
- [Proxy Migration Guide](https://nextjs.org/docs/messages/middleware-to-proxy)

### React References

- [useActionState Reference](https://react.dev/reference/react/useActionState)
- [useOptimistic Reference](https://react.dev/reference/react/useOptimistic)
- [useFormStatus Reference](https://react.dev/reference/react/useFormStatus)
- [use Reference](https://react.dev/reference/react/use)
- [Server Components Reference](https://react.dev/reference/rsc/server-components)
- [Server Functions Reference](https://react.dev/reference/rsc/server-functions)

### Guides & Tutorials

- [freeCodeCamp React 19 Hooks Guide](https://www.freecodecamp.org/news/react-19-new-hooks-explained-with-examples/)
- [React Server Components Guide (Josh Comeau)](https://www.joshwcomeau.com/react/server-components/)
- [Vercel PPR Blog](https://vercel.com/blog/partial-prerendering-with-next-js-creating-a-new-default-rendering-model)
