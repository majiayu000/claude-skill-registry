---
name: bknd-client-setup
description: Use when setting up Bknd SDK in a frontend application. Covers Api class initialization, token storage, auth state handling, React integration with BkndBrowserApp and useApp hook, framework-specific setup (Vite, Next.js, standalone), and TypeScript type registration.
---

# Client Setup

Set up the Bknd TypeScript SDK in your frontend application.

## Prerequisites

- Bknd backend running (local or deployed)
- Frontend project initialized (React, Vue, vanilla JS, etc.)
- `bknd` package installed: `npm install bknd`

## When to Use UI Mode

Not applicable - client setup is code-only.

## When to Use Code Mode

- Always - SDK setup requires code configuration
- Choose approach based on architecture:
  - **Standalone API client** - Connecting to separate Bknd backend
  - **Embedded (BkndBrowserApp)** - Bknd runs in browser (Vite/React)
  - **Framework adapter** - Next.js, Astro, etc.

## Approach 1: Standalone API Client

Use when connecting to a separate Bknd backend server.

### Step 1: Basic Setup

```typescript
import { Api } from "bknd";

const api = new Api({
  host: "https://api.example.com",  // Your Bknd backend URL
});

// Make requests
const { ok, data } = await api.data.readMany("posts");
```

### Step 2: Add Token Persistence

Store auth tokens across page refreshes:

```typescript
import { Api } from "bknd";

const api = new Api({
  host: "https://api.example.com",
  storage: localStorage,  // Persists token as "auth" key
});
```

Custom storage key:

```typescript
const api = new Api({
  host: "https://api.example.com",
  storage: localStorage,
  key: "myapp_auth",  // Custom key instead of "auth"
});
```

### Step 3: Handle Auth State Changes

React to login/logout events:

```typescript
const api = new Api({
  host: "https://api.example.com",
  storage: localStorage,
  onAuthStateChange: (state) => {
    console.log("Auth state:", state);
    // state.user - current user or undefined
    // state.token - JWT or undefined
    // state.verified - whether token was verified with server
  },
});
```

### Step 4: Cookie-Based Auth (SSR)

For server-side rendering with cookies:

```typescript
const api = new Api({
  host: "https://api.example.com",
  credentials: "include",  // Send cookies cross-origin
});
```

### Step 5: Full Configuration

```typescript
import { Api } from "bknd";

const api = new Api({
  // Required
  host: "https://api.example.com",

  // Auth persistence
  storage: localStorage,
  key: "auth",

  // Auth events
  onAuthStateChange: (state) => {
    if (state.user) {
      console.log("Logged in:", state.user.email);
    } else {
      console.log("Logged out");
    }
  },

  // Request options
  credentials: "include",  // For cookies
  verbose: true,           // Log requests (dev only)

  // Data API defaults
  data: {
    defaultQuery: { limit: 20 },
  },
});

export { api };
```

## Approach 2: React with BkndBrowserApp (Embedded)

Use when Bknd runs entirely in the browser (Vite + React).

### Step 1: Define Schema

```typescript
// bknd.config.ts
import { boolean, em, entity, text } from "bknd";

export const schema = em({
  todos: entity("todos", {
    title: text(),
    done: boolean(),
  }),
});

// Type registration for autocomplete
type Database = (typeof schema)["DB"];
declare module "bknd" {
  interface DB extends Database {}
}
```

### Step 2: Configure BkndBrowserApp

```tsx
// App.tsx
import { BkndBrowserApp, type BrowserBkndConfig } from "bknd/adapter/browser";
import { schema } from "./bknd.config";

const config = {
  config: {
    data: schema.toJSON(),
    auth: {
      enabled: true,
      jwt: {
        secret: "your-secret-key",  // Use env var in production
      },
    },
  },
  options: {
    seed: async (ctx) => {
      // Initial data (runs once on empty DB)
      await ctx.em.mutator("todos").insertMany([
        { title: "Learn bknd", done: false },
      ]);
    },
  },
} satisfies BrowserBkndConfig;

export default function App() {
  return (
    <BkndBrowserApp {...config}>
      <YourRoutes />
    </BkndBrowserApp>
  );
}
```

### Step 3: Use the useApp Hook

```tsx
import { useApp } from "bknd/adapter/browser";

function TodoList() {
  const { api, app, user, isLoading } = useApp();

  if (isLoading) return <div>Loading...</div>;

  // api - Api instance for data/auth/media
  // app - Full App instance
  // user - Current user or null
  // isLoading - True while initializing

  const [todos, setTodos] = useState([]);

  useEffect(() => {
    api.data.readMany("todos").then(({ data }) => setTodos(data));
  }, [api]);

  return (
    <ul>
      {todos.map((todo) => (
        <li key={todo.id}>{todo.title}</li>
      ))}
    </ul>
  );
}
```

## Approach 3: React Standalone (External Backend)

Use when React connects to a separate Bknd server.

### Step 1: Create API Instance

```typescript
// lib/api.ts
import { Api } from "bknd";

export const api = new Api({
  host: import.meta.env.VITE_BKND_URL || "http://localhost:7654",
  storage: localStorage,
});
```

### Step 2: Create React Context

```tsx
// context/BkndContext.tsx
import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { Api, type TApiUser } from "bknd";
import { api } from "../lib/api";

type BkndContextType = {
  api: Api;
  user: TApiUser | null;
  isLoading: boolean;
};

const BkndContext = createContext<BkndContextType | null>(null);

export function BkndProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<TApiUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Listen for auth changes
    api.options.onAuthStateChange = (state) => {
      setUser(state.user ?? null);
    };

    // Verify existing token on mount
    api.verifyAuth().finally(() => {
      setUser(api.getUser());
      setIsLoading(false);
    });

    return () => {
      api.options.onAuthStateChange = undefined;
    };
  }, []);

  return (
    <BkndContext.Provider value={{ api, user, isLoading }}>
      {children}
    </BkndContext.Provider>
  );
}

export function useBknd() {
  const ctx = useContext(BkndContext);
  if (!ctx) throw new Error("useBknd must be used within BkndProvider");
  return ctx;
}
```

### Step 3: Wrap App

```tsx
// main.tsx
import { BkndProvider } from "./context/BkndContext";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <BkndProvider>
    <App />
  </BkndProvider>
);
```

### Step 4: Use in Components

```tsx
function Profile() {
  const { api, user, isLoading } = useBknd();

  if (isLoading) return <div>Loading...</div>;
  if (!user) return <div>Not logged in</div>;

  return <div>Hello, {user.email}</div>;
}
```

## Approach 4: Next.js Integration

### Step 1: Create API Utility

```typescript
// lib/bknd.ts
import { Api } from "bknd";

// Client-side singleton
let clientApi: Api | null = null;

export function getClientApi() {
  if (typeof window === "undefined") {
    throw new Error("getClientApi can only be used client-side");
  }

  if (!clientApi) {
    clientApi = new Api({
      host: process.env.NEXT_PUBLIC_BKND_URL!,
      storage: localStorage,
    });
  }

  return clientApi;
}

// Server-side (per-request)
export function getServerApi(request?: Request) {
  return new Api({
    host: process.env.BKND_URL!,
    request,  // Extracts token from cookies/headers
  });
}
```

### Step 2: Client Component

```tsx
"use client";

import { useEffect, useState } from "react";
import { getClientApi } from "@/lib/bknd";

export function PostList() {
  const [posts, setPosts] = useState([]);
  const api = getClientApi();

  useEffect(() => {
    api.data.readMany("posts").then(({ data }) => setPosts(data));
  }, []);

  return <ul>{posts.map((p) => <li key={p.id}>{p.title}</li>)}</ul>;
}
```

### Step 3: Server Component

```tsx
// app/posts/page.tsx
import { getServerApi } from "@/lib/bknd";

export default async function PostsPage() {
  const api = getServerApi();
  const { data: posts } = await api.data.readMany("posts");

  return <ul>{posts.map((p) => <li key={p.id}>{p.title}</li>)}</ul>;
}
```

## TypeScript Type Registration

Get autocomplete for entity names and fields:

```typescript
// types/bknd.d.ts
import { em, entity, text, number } from "bknd";

// Define your schema
const schema = em({
  posts: entity("posts", {
    title: text(),
    views: number(),
  }),
  users: entity("users", {
    email: text(),
    name: text(),
  }),
});

// Register types globally
type Database = (typeof schema)["DB"];
declare module "bknd" {
  interface DB extends Database {}
}
```

Now `api.data.readMany("posts")` returns typed `Post[]`.

## Api Class Methods Reference

```typescript
// Auth state
api.getUser()           // Current user or null
api.isAuthenticated()   // Has valid token
api.isAuthVerified()    // Token verified with server
api.verifyAuth()        // Verify token (async)
api.getAuthState()      // { token, user, verified }

// Module APIs
api.data.readMany(...)  // CRUD operations
api.auth.login(...)     // Authentication
api.media.upload(...)   // File uploads
api.system.health()     // System checks

// Token management
api.updateToken(token)  // Manually set token
api.token_transport     // "header" | "cookie" | "none"
```

## Environment Variables

```bash
# .env.local (Next.js)
NEXT_PUBLIC_BKND_URL=http://localhost:7654
BKND_URL=http://localhost:7654

# .env (Vite)
VITE_BKND_URL=http://localhost:7654
```

## Common Pitfalls

### Token Not Persisting

**Problem:** User logged out after refresh

**Fix:** Provide storage option:

```typescript
// WRONG - no persistence
const api = new Api({ host: "..." });

// CORRECT
const api = new Api({
  host: "...",
  storage: localStorage,
});
```

### CORS Errors

**Problem:** Browser blocks requests to backend

**Fix:** Configure CORS on backend:

```typescript
// bknd.config.ts (server)
const app = new App({
  server: {
    cors: {
      origin: ["http://localhost:3000"],
      credentials: true,
    },
  },
});
```

### Auth State Not Updating

**Problem:** UI doesn't reflect login/logout

**Fix:** Use `onAuthStateChange`:

```typescript
const api = new Api({
  host: "...",
  onAuthStateChange: (state) => {
    // Update your UI state here
    setUser(state.user ?? null);
  },
});
```

### SSR Hydration Mismatch

**Problem:** Server/client render different content

**Fix:** Check auth on client only:

```tsx
function AuthStatus() {
  const [user, setUser] = useState(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    setUser(api.getUser());
  }, []);

  if (!mounted) return null;  // Avoid hydration mismatch

  return user ? <span>{user.email}</span> : <span>Guest</span>;
}
```

### Using Wrong Import Path

**Problem:** Import errors

**Fix:** Use correct subpath:

```typescript
// Standalone API
import { Api } from "bknd";

// React browser adapter
import { BkndBrowserApp, useApp } from "bknd/adapter/browser";

// Next.js adapter
import type { NextjsBkndConfig } from "bknd/adapter/nextjs";
```

### Multiple Api Instances

**Problem:** Auth state inconsistent across app

**Fix:** Use singleton pattern:

```typescript
// lib/api.ts
let api: Api | null = null;

export function getApi() {
  if (!api) {
    api = new Api({ host: "...", storage: localStorage });
  }
  return api;
}
```

## Verification

Test your setup:

```typescript
import { api } from "./lib/api";

async function test() {
  // 1. Check connection
  const { ok } = await api.data.readMany("posts", { limit: 1 });
  console.log("API connected:", ok);

  // 2. Check auth
  console.log("Authenticated:", api.isAuthenticated());
  console.log("User:", api.getUser());

  // 3. Test login
  const { ok: loginOk } = await api.auth.login("password", {
    email: "test@example.com",
    password: "password123",
  });
  console.log("Login:", loginOk);
}
```

## DOs and DON'Ts

**DO:**
- Use `storage: localStorage` for token persistence
- Handle `onAuthStateChange` for reactive UI
- Use singleton pattern for Api instance
- Call `verifyAuth()` on app startup
- Use environment variables for host URL

**DON'T:**
- Create multiple Api instances
- Forget to configure CORS on backend
- Use Api directly in SSR without request context
- Hardcode backend URLs
- Ignore auth state changes in UI

## Related Skills

- **bknd-api-discovery** - Explore available endpoints
- **bknd-login-flow** - Implement authentication
- **bknd-crud-read** - Query data with SDK
- **bknd-session-handling** - Manage user sessions
- **bknd-local-setup** - Set up local backend
