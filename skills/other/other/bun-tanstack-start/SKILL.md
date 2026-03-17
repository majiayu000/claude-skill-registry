---
name: Bun TanStack Start
description: TanStack Start full-stack React framework with Bun runtime. Use for TanStack Router, server functions, vinxi, or encountering SSR, build, preset errors.
---

# Bun TanStack Start

Run TanStack Start (full-stack React framework) with Bun.

## Quick Start

```bash
# Create new TanStack Start project
bunx create-tanstack-start@latest my-app
cd my-app

# Install dependencies
bun install

# Development
bun run dev

# Build
bun run build

# Preview
bun run start
```

## Project Setup

### package.json

```json
{
  "scripts": {
    "dev": "vinxi dev",
    "build": "vinxi build",
    "start": "vinxi start"
  },
  "dependencies": {
    "@tanstack/react-router": "^1.139.0",
    "@tanstack/start": "^1.120.0",
    "react": "^19.2.0",
    "react-dom": "^19.2.0",
    "vinxi": "^0.5.10"
  }
}
```

### app.config.ts

```typescript
import { defineConfig } from "@tanstack/start/config";

export default defineConfig({
  server: {
    preset: "bun",
  },
});
```

## File-Based Routing

```
app/
├── routes/
│   ├── __root.tsx       # Root layout
│   ├── index.tsx        # /
│   ├── about.tsx        # /about
│   ├── users/
│   │   ├── index.tsx    # /users
│   │   └── $userId.tsx  # /users/:userId
│   └── api/
│       └── users.ts     # /api/users
└── client.tsx
```

## Route Components

### Basic Route

```tsx
// app/routes/index.tsx
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  component: Home,
});

function Home() {
  return <h1>Welcome Home</h1>;
}
```

### Route with Loader

```tsx
// app/routes/users/index.tsx
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/users/")({
  loader: async () => {
    const response = await fetch("/api/users");
    return response.json();
  },
  component: Users,
});

function Users() {
  const users = Route.useLoaderData();

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### Dynamic Routes

```tsx
// app/routes/users/$userId.tsx
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/users/$userId")({
  loader: async ({ params }) => {
    const response = await fetch(`/api/users/${params.userId}`);
    return response.json();
  },
  component: UserDetail,
});

function UserDetail() {
  const user = Route.useLoaderData();
  const { userId } = Route.useParams();

  return (
    <div>
      <h1>{user.name}</h1>
      <p>User ID: {userId}</p>
    </div>
  );
}
```

## Server Functions

### Define Server Function

```tsx
// app/routes/users/index.tsx
import { createFileRoute } from "@tanstack/react-router";
import { createServerFn } from "@tanstack/start";
import { Database } from "bun:sqlite";

const getUsers = createServerFn("GET", async () => {
  const db = new Database("data.sqlite");
  const users = db.query("SELECT * FROM users").all();
  db.close();
  return users;
});

const createUser = createServerFn("POST", async (name: string) => {
  const db = new Database("data.sqlite");
  db.run("INSERT INTO users (name) VALUES (?)", [name]);
  db.close();
  return { success: true };
});

export const Route = createFileRoute("/users/")({
  loader: () => getUsers(),
  component: Users,
});

function Users() {
  const users = Route.useLoaderData();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const name = formData.get("name") as string;
    await createUser(name);
    // Refetch or update state
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input name="name" placeholder="Name" />
        <button type="submit">Add User</button>
      </form>
      <ul>
        {users.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Server Function with Context

```tsx
import { createServerFn } from "@tanstack/start";
import { getWebRequest } from "@tanstack/start/server";

const getSession = createServerFn("GET", async () => {
  const request = getWebRequest();
  const cookies = request.headers.get("Cookie");
  // Parse and validate session
  return { userId: "123", role: "admin" };
});

const protectedAction = createServerFn("POST", async (data: any) => {
  const session = await getSession();

  if (session.role !== "admin") {
    throw new Error("Unauthorized");
  }

  // Perform action
  return { success: true };
});
```

## API Routes

```typescript
// app/routes/api/users.ts
import { createAPIFileRoute } from "@tanstack/start/api";
import { Database } from "bun:sqlite";

export const Route = createAPIFileRoute("/api/users")({
  GET: async ({ request }) => {
    const db = new Database("data.sqlite");
    const users = db.query("SELECT * FROM users").all();
    db.close();

    return Response.json(users);
  },

  POST: async ({ request }) => {
    const { name } = await request.json();

    const db = new Database("data.sqlite");
    db.run("INSERT INTO users (name) VALUES (?)", [name]);
    db.close();

    return Response.json({ success: true });
  },
});
```

## Root Layout

```tsx
// app/routes/__root.tsx
import { createRootRoute, Link, Outlet } from "@tanstack/react-router";

export const Route = createRootRoute({
  component: Root,
});

function Root() {
  return (
    <html>
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>My App</title>
      </head>
      <body>
        <nav>
          <Link to="/">Home</Link>
          <Link to="/users">Users</Link>
          <Link to="/about">About</Link>
        </nav>
        <main>
          <Outlet />
        </main>
      </body>
    </html>
  );
}
```

## Error Handling

```tsx
// app/routes/users/$userId.tsx
export const Route = createFileRoute("/users/$userId")({
  loader: async ({ params }) => {
    const response = await fetch(`/api/users/${params.userId}`);
    if (!response.ok) {
      throw new Error("User not found");
    }
    return response.json();
  },
  errorComponent: ({ error }) => (
    <div>
      <h1>Error</h1>
      <p>{error.message}</p>
    </div>
  ),
  pendingComponent: () => <div>Loading...</div>,
  component: UserDetail,
});
```

## Search Params

```tsx
// app/routes/users/index.tsx
import { createFileRoute } from "@tanstack/react-router";
import { z } from "zod";

const searchSchema = z.object({
  page: z.number().default(1),
  limit: z.number().default(10),
  search: z.string().optional(),
});

export const Route = createFileRoute("/users/")({
  validateSearch: searchSchema,
  loader: async ({ search }) => {
    const { page, limit, search: query } = search;
    // Fetch with pagination
    return fetchUsers({ page, limit, query });
  },
  component: Users,
});
```

## Deployment

### Build for Bun

```bash
NITRO_PRESET=bun bun run build
bun .output/server/index.mjs
```

### Docker

```dockerfile
FROM oven/bun:1 AS builder

WORKDIR /app
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile

COPY . .
RUN bun run build

FROM oven/bun:1

WORKDIR /app
COPY --from=builder /app/.output ./output

EXPOSE 3000

CMD ["bun", ".output/server/index.mjs"]
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot find bun:sqlite` | Wrong preset | Set `server.preset: "bun"` |
| `Server function failed` | Network error | Check function definition |
| `Route not found` | File naming | Check route file location |
| `Hydration mismatch` | Server/client diff | Check loader data |

## When to Load References

Load `references/router-api.md` when:
- Advanced routing patterns
- Route guards
- Nested layouts

Load `references/forms.md` when:
- Form handling
- Mutations
- Optimistic updates
