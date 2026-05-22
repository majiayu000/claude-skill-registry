---
name: solidstart-routing
description: "SolidStart file-based routing: routes directory structure, dynamic routes, nested layouts, route groups, app.tsx setup with FileRoutes component."
metadata:
  globs:
    - "src/routes/**/*"
    - "src/app.tsx"
    - "src/entry-*.tsx"
---

# SolidStart File-Based Routing

## Project Structure

```
public/              # Static assets
src/
├── routes/          # File-based routing
├── entry-client.tsx # Client entry
├── entry-server.tsx # Server entry
├── app.tsx          # Root component
```

## Basic Routes

Routes created by files in `src/routes/`. Each file must default export a component.

- `routes/index.tsx` → `/`
- `routes/about.tsx` → `/about`
- `routes/blog.tsx` → `/blog`

```tsx
// routes/index.tsx
export default function Index() {
  return <div>Home</div>;
}
```

## Dynamic Routes

- `routes/users/[id].tsx` → `/users/:id`
- `routes/posts/[[slug]].tsx` → `/posts/:slug?` (optional)
- `routes/docs/[...path].tsx` → `/docs/*` (catch-all)

```tsx
// routes/users/[id].tsx
import { useParams } from "@solidjs/router";

export default function UserProfile() {
  const params = useParams();
  return <div>User {params.id}</div>;
}
```

## Nested Routes

Create directories for nested routes:

- `routes/blog/article-1.tsx` → `/blog/article-1`

```tsx
// routes/blog/article-1.tsx
export default function Article() {
  return <article>Content</article>;
}
```

## Nested Layouts

Create layout file with same name as directory:

```tsx
// routes/blog.tsx - layout
import { RouteSectionProps } from "@solidjs/router";

export default function BlogLayout(props: RouteSectionProps) {
  return (
    <div>
      <nav><h1>Blog</h1></nav>
      <main>{props.children}</main>
    </div>
  );
}

// routes/blog/article-1.tsx - nested route
export default function Article() {
  return <article>Content</article>;
}
```

## Route Groups

Use parentheses for organization (don't affect URL):

```
routes/
├── (auth)/
│   ├── login.tsx     → /login
│   └── signup.tsx    → /signup
└── (marketing)/
    ├── about.tsx     → /about
    └── contact.tsx   → /contact
```

## Index File Naming

Rename index files with parentheses for clarity:

- `routes/blog/(blog).tsx` → `/blog` (instead of `routes/blog/index.tsx`)

## Escaping Nested Routes

Use parentheses to escape nested structure:

```
routes/
├── users.tsx              # Layout
├── users/
│   ├── index.tsx          # /users
│   └── projects.tsx       # /users/projects
└── users(details)/
    └── [id].tsx           # /users/:id (separate layout)
```

## Route Configuration

Export `route` object for preloading:

```tsx
import type { RouteDefinition } from "@solidjs/router";

export const route = {
  preload({ params }) {
    return getData(params.id);
  }
} satisfies RouteDefinition;

export default function Page() {
  return <div>Content</div>;
}
```

## App Setup

### app.tsx

```tsx
import { Suspense } from "solid-js";
import { Router } from "@solidjs/router";
import { FileRoutes } from "@solidjs/start/router";

export default function App() {
  return (
    <Router root={(props) => <Suspense>{props.children}</Suspense>}>
      <FileRoutes />
    </Router>
  );
}
```

**Critical:** Always wrap router root with `<Suspense>` - routes are lazy-loaded.

### Entry Points

**entry-client.tsx**:
```tsx
import { mount, StartClient } from "@solidjs/start/client";
mount(() => <StartClient />, document.getElementById("app")!);
```

**entry-server.tsx**:
```tsx
import { StartServer, createHandler } from "@solidjs/start/server";
export default createHandler(StartServer);
```

