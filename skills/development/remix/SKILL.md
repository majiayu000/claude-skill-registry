---
name: remix
description: Builds full-stack React applications with Remix using loaders, actions, nested routes, and progressive enhancement. Use when creating Remix projects, implementing data loading, form handling, error boundaries, or deploying to various platforms.
---

# Remix

Full-stack React framework with nested routing, server-side data loading, progressive enhancement, and bring-your-own-server flexibility.

## Quick Start

**Create new project:**
```bash
npx create-remix@latest my-app
cd my-app
npm run dev
```

**Manual setup:**
```bash
mkdir my-remix-app && cd my-remix-app
npm init -y
npm i @remix-run/node @remix-run/react @remix-run/serve isbot react react-dom
npm i -D @remix-run/dev vite typescript @types/react @types/react-dom
```

**Essential file structure:**
```
app/
  root.tsx            # Root layout (required)
  routes/
    _index.tsx        # Home page (/)
    about.tsx         # /about
    posts.$slug.tsx   # /posts/:slug
  entry.client.tsx    # Client entry
  entry.server.tsx    # Server entry
vite.config.ts
```

## File-Based Routing

### Route Conventions

| File | Route |
|------|-------|
| `_index.tsx` | `/` (index route) |
| `about.tsx` | `/about` |
| `posts._index.tsx` | `/posts` |
| `posts.$slug.tsx` | `/posts/:slug` |
| `posts.$slug_.edit.tsx` | `/posts/:slug/edit` (escaping nesting) |
| `$.tsx` | Splat (catch-all) |

### Special Characters

| Character | Purpose | Example |
|-----------|---------|---------|
| `.` | Nested URL segment | `posts.new.tsx` -> `/posts/new` |
| `$` | Dynamic segment | `posts.$id.tsx` -> `/posts/:id` |
| `_` | Layout nesting escape | `posts_.$id.tsx` -> no layout |
| `()` | Optional segment | `($lang).about.tsx` |

### Nested Routes

```
app/routes/
  dashboard.tsx           # Layout for /dashboard/*
  dashboard._index.tsx    # /dashboard
  dashboard.settings.tsx  # /dashboard/settings
  dashboard.users.tsx     # /dashboard/users
```

```tsx
// app/routes/dashboard.tsx (Layout)
import { Outlet } from "@remix-run/react";

export default function DashboardLayout() {
  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1">
        <Outlet /> {/* Child routes render here */}
      </main>
    </div>
  );
}
```

## Root Route

```tsx
// app/root.tsx
import {
  Links,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
} from "@remix-run/react";

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <Meta />
        <Links />
      </head>
      <body>
        {children}
        <ScrollRestoration />
        <Scripts />
      </body>
    </html>
  );
}

export default function App() {
  return <Outlet />;
}
```

## Loaders (Data Fetching)

### Basic Loader

```tsx
// app/routes/posts._index.tsx
import { json } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import type { LoaderFunctionArgs } from "@remix-run/node";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const posts = await db.posts.findMany();
  return json({ posts });
};

export default function Posts() {
  const { posts } = useLoaderData<typeof loader>();

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

### With Parameters

```tsx
// app/routes/posts.$slug.tsx
import { json } from "@remix-run/node";
import type { LoaderFunctionArgs } from "@remix-run/node";

export const loader = async ({ params }: LoaderFunctionArgs) => {
  const post = await db.posts.findUnique({
    where: { slug: params.slug },
  });

  if (!post) {
    throw new Response("Not Found", { status: 404 });
  }

  return json({ post });
};
```

### With Search Params

```tsx
export const loader = async ({ request }: LoaderFunctionArgs) => {
  const url = new URL(request.url);
  const query = url.searchParams.get("q") ?? "";
  const page = Number(url.searchParams.get("page")) || 1;

  const posts = await db.posts.findMany({
    where: { title: { contains: query } },
    skip: (page - 1) * 10,
    take: 10,
  });

  return json({ posts, query, page });
};
```

### With Headers

```tsx
export const loader = async ({ request }: LoaderFunctionArgs) => {
  const authHeader = request.headers.get("Authorization");

  // Check auth
  if (!authHeader) {
    throw new Response("Unauthorized", { status: 401 });
  }

  return json({ data: "secret" });
};
```

## Actions (Mutations)

### Basic Form Action

```tsx
// app/routes/posts.new.tsx
import { json, redirect } from "@remix-run/node";
import { Form, useActionData } from "@remix-run/react";
import type { ActionFunctionArgs } from "@remix-run/node";

export const action = async ({ request }: ActionFunctionArgs) => {
  const formData = await request.formData();
  const title = formData.get("title") as string;
  const content = formData.get("content") as string;

  // Validate
  const errors: Record<string, string> = {};
  if (!title) errors.title = "Title is required";
  if (!content) errors.content = "Content is required";

  if (Object.keys(errors).length > 0) {
    return json({ errors }, { status: 400 });
  }

  // Create post
  await db.posts.create({ data: { title, content } });

  return redirect("/posts");
};

export default function NewPost() {
  const actionData = useActionData<typeof action>();

  return (
    <Form method="post">
      <div>
        <label>
          Title
          <input type="text" name="title" />
        </label>
        {actionData?.errors?.title && (
          <p className="error">{actionData.errors.title}</p>
        )}
      </div>

      <div>
        <label>
          Content
          <textarea name="content" />
        </label>
        {actionData?.errors?.content && (
          <p className="error">{actionData.errors.content}</p>
        )}
      </div>

      <button type="submit">Create Post</button>
    </Form>
  );
}
```

### Multiple Actions (Intent Pattern)

```tsx
export const action = async ({ request }: ActionFunctionArgs) => {
  const formData = await request.formData();
  const intent = formData.get("intent");

  switch (intent) {
    case "create":
      return createItem(formData);
    case "update":
      return updateItem(formData);
    case "delete":
      return deleteItem(formData);
    default:
      throw new Response("Invalid intent", { status: 400 });
  }
};

// In component
<Form method="post">
  <input type="hidden" name="id" value={item.id} />
  <button type="submit" name="intent" value="update">Update</button>
  <button type="submit" name="intent" value="delete">Delete</button>
</Form>
```

## Forms

### Form Component

```tsx
import { Form } from "@remix-run/react";

// POST to current route
<Form method="post">
  <input name="email" type="email" />
  <button type="submit">Submit</button>
</Form>

// POST to different route
<Form method="post" action="/subscribe">
  <input name="email" type="email" />
  <button type="submit">Subscribe</button>
</Form>

// GET (search)
<Form method="get" action="/search">
  <input name="q" type="search" />
  <button type="submit">Search</button>
</Form>
```

### Pending States

```tsx
import { Form, useNavigation } from "@remix-run/react";

export default function CreatePost() {
  const navigation = useNavigation();
  const isSubmitting = navigation.state === "submitting";

  return (
    <Form method="post">
      <input name="title" disabled={isSubmitting} />
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Creating..." : "Create"}
      </button>
    </Form>
  );
}
```

### useFetcher (Non-Navigation Mutations)

```tsx
import { useFetcher } from "@remix-run/react";

export function LikeButton({ postId }: { postId: string }) {
  const fetcher = useFetcher();
  const isLiking = fetcher.state === "submitting";

  return (
    <fetcher.Form method="post" action="/api/like">
      <input type="hidden" name="postId" value={postId} />
      <button type="submit" disabled={isLiking}>
        {isLiking ? "..." : "Like"}
      </button>
    </fetcher.Form>
  );
}
```

### Optimistic UI

```tsx
export function TodoItem({ todo }) {
  const fetcher = useFetcher();

  // Optimistic value
  const isCompleted = fetcher.formData
    ? fetcher.formData.get("completed") === "true"
    : todo.completed;

  return (
    <fetcher.Form method="post">
      <input type="hidden" name="id" value={todo.id} />
      <input
        type="checkbox"
        name="completed"
        value="true"
        checked={isCompleted}
        onChange={(e) => fetcher.submit(e.target.form)}
      />
      <span className={isCompleted ? "line-through" : ""}>
        {todo.title}
      </span>
    </fetcher.Form>
  );
}
```

## Error Handling

### Error Boundary

```tsx
// app/routes/posts.$slug.tsx
import { useRouteError, isRouteErrorResponse } from "@remix-run/react";

export function ErrorBoundary() {
  const error = useRouteError();

  if (isRouteErrorResponse(error)) {
    return (
      <div>
        <h1>{error.status} {error.statusText}</h1>
        <p>{error.data}</p>
      </div>
    );
  }

  return (
    <div>
      <h1>Error</h1>
      <p>{error instanceof Error ? error.message : "Unknown error"}</p>
    </div>
  );
}
```

### Throwing Responses

```tsx
export const loader = async ({ params }: LoaderFunctionArgs) => {
  const post = await db.posts.findUnique({ where: { slug: params.slug } });

  if (!post) {
    throw new Response("Post not found", { status: 404 });
  }

  return json({ post });
};
```

## Meta & Links

### Meta Tags

```tsx
import type { MetaFunction } from "@remix-run/node";

// Static meta
export const meta: MetaFunction = () => {
  return [
    { title: "My Page" },
    { name: "description", content: "Page description" },
  ];
};

// Dynamic meta from loader
export const meta: MetaFunction<typeof loader> = ({ data }) => {
  return [
    { title: data?.post.title ?? "Post" },
    { name: "description", content: data?.post.excerpt },
  ];
};
```

### Links (CSS, Fonts)

```tsx
import type { LinksFunction } from "@remix-run/node";
import styles from "~/styles/app.css?url";

export const links: LinksFunction = () => [
  { rel: "stylesheet", href: styles },
  { rel: "preconnect", href: "https://fonts.googleapis.com" },
];
```

## Resource Routes (API)

```tsx
// app/routes/api.posts.tsx
import { json } from "@remix-run/node";
import type { LoaderFunctionArgs, ActionFunctionArgs } from "@remix-run/node";

// GET /api/posts
export const loader = async ({ request }: LoaderFunctionArgs) => {
  const posts = await db.posts.findMany();
  return json(posts);
};

// POST /api/posts
export const action = async ({ request }: ActionFunctionArgs) => {
  const body = await request.json();
  const post = await db.posts.create({ data: body });
  return json(post, { status: 201 });
};
```

## Streaming (Deferred Data)

```tsx
import { defer } from "@remix-run/node";
import { Await, useLoaderData } from "@remix-run/react";
import { Suspense } from "react";

export const loader = async () => {
  // Fast data - awaited
  const criticalData = await getCriticalData();

  // Slow data - deferred
  const slowDataPromise = getSlowData();

  return defer({
    criticalData,
    slowData: slowDataPromise,
  });
};

export default function Page() {
  const { criticalData, slowData } = useLoaderData<typeof loader>();

  return (
    <div>
      <h1>{criticalData.title}</h1>

      <Suspense fallback={<p>Loading...</p>}>
        <Await resolve={slowData}>
          {(data) => <SlowComponent data={data} />}
        </Await>
      </Suspense>
    </div>
  );
}
```

## Sessions & Cookies

```tsx
// app/sessions.server.ts
import { createCookieSessionStorage } from "@remix-run/node";

export const sessionStorage = createCookieSessionStorage({
  cookie: {
    name: "__session",
    httpOnly: true,
    maxAge: 60 * 60 * 24 * 7, // 1 week
    path: "/",
    sameSite: "lax",
    secrets: [process.env.SESSION_SECRET!],
    secure: process.env.NODE_ENV === "production",
  },
});

export const { getSession, commitSession, destroySession } = sessionStorage;
```

```tsx
// Usage in loader/action
import { getSession, commitSession } from "~/sessions.server";

export const action = async ({ request }: ActionFunctionArgs) => {
  const session = await getSession(request.headers.get("Cookie"));
  session.set("userId", user.id);

  return redirect("/dashboard", {
    headers: {
      "Set-Cookie": await commitSession(session),
    },
  });
};

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const session = await getSession(request.headers.get("Cookie"));
  const userId = session.get("userId");

  if (!userId) {
    throw redirect("/login");
  }

  return json({ user: await getUser(userId) });
};
```

## Common Patterns

### Protected Routes

```tsx
// app/utils/auth.server.ts
export async function requireUser(request: Request) {
  const session = await getSession(request.headers.get("Cookie"));
  const userId = session.get("userId");

  if (!userId) {
    throw redirect("/login");
  }

  const user = await db.users.findUnique({ where: { id: userId } });

  if (!user) {
    throw redirect("/login");
  }

  return user;
}

// In route
export const loader = async ({ request }: LoaderFunctionArgs) => {
  const user = await requireUser(request);
  return json({ user });
};
```

### Flash Messages

```tsx
export const action = async ({ request }: ActionFunctionArgs) => {
  const session = await getSession(request.headers.get("Cookie"));
  session.flash("success", "Post created successfully!");

  return redirect("/posts", {
    headers: {
      "Set-Cookie": await commitSession(session),
    },
  });
};

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const session = await getSession(request.headers.get("Cookie"));
  const message = session.get("success");

  return json(
    { message },
    {
      headers: {
        "Set-Cookie": await commitSession(session),
      },
    }
  );
};
```

## Best Practices

1. **Colocate data with UI** - Keep loaders/actions in the same file as components
2. **Use Form over fetch** - Progressive enhancement by default
3. **Throw responses for errors** - Triggers error boundaries
4. **Use resource routes for APIs** - Not everything needs UI
5. **Defer slow data** - Stream non-critical content
6. **Validate on server** - Never trust client data

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Fetching in useEffect | Use loaders instead |
| Using fetch for mutations | Use Form/useFetcher |
| Not handling loading states | Check navigation.state |
| Forgetting error boundaries | Add ErrorBoundary export |
| Client-side state for server data | Use loader + revalidation |

## Reference Files

- [references/routing.md](references/routing.md) - Advanced routing patterns
- [references/data-flow.md](references/data-flow.md) - Loaders, actions, and revalidation
- [references/deployment.md](references/deployment.md) - Deployment to various platforms

## Templates

- [templates/route.tsx](templates/route.tsx) - Standard route template
- [templates/resource-route.ts](templates/resource-route.ts) - API route template
