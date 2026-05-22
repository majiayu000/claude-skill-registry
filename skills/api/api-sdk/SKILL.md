---
name: api-sdk
description: Use when working with the TypeScript SDK for making API calls to Bknd, handling authentication, and managing data operations from client or server code. Covers Api class initialization, CRUD operations, auth methods, and module-specific APIs.
---

# TypeScript SDK

The Bknd TypeScript SDK provides a type-safe, promise-based client for interacting with Bknd's REST API. Use it for both client-side browser applications and server-side code.

## What You'll Learn

- Initialize the Api class with different auth strategies
- Perform CRUD operations on entities
- Handle authentication and token management
- Access media and system APIs
- Use type safety with auto-generated DB types

## Quick Start

```typescript
import { Api } from "bknd";

const api = new Api({ host: "https://api.example.com" });

// Read data
const posts = await api.data.readMany("posts", { limit: 10 });

// Login with password
await api.auth.login("password", { email: "user@example.com", password: "pass" });
```

## Api Class

The `Api` class is the main entry point for all SDK operations.

### Constructor Options

```typescript
const api = new Api({
  host: string,           // API base URL (default: http://localhost)
  headers?: Headers,      // Custom headers
  storage?: Storage,      // For token persistence (see below)
  key?: string,           // Token storage key (default: "auth")
  token?: string,         // Direct JWT token
  user?: SafeUser | null, // User object (server-side)
  request?: Request,      // Extract from Hono/Next.js request
  credentials?: "include" | "same-origin" | "omit",
  onAuthStateChange?: (state: AuthState) => void,
  fetcher?: ApiFetcher,   // Custom fetch implementation
  verbose?: boolean,
  // Module-specific options
  data?: Partial<DataApiOptions>,
  auth?: Partial<AuthApiOptions>,
  media?: Partial<MediaApiOptions>,
});
```

### Storage Interface

For client-side token persistence, provide a storage object:

```typescript
const api = new Api({
  host: "https://api.example.com",
  storage: {
    getItem: (key) => localStorage.getItem(key),
    setItem: (key, value) => localStorage.setItem(key, value),
    removeItem: (key) => localStorage.removeItem(key),
  },
  onAuthStateChange: (state) => {
    console.log("Auth state:", state);
  },
});
```

### Initialization Patterns

**Client-side with localStorage:**
```typescript
const api = new Api({
  host: "https://api.example.com",
  storage: {
    getItem: (key) => localStorage.getItem(key),
    setItem: (key, value) => localStorage.setItem(key, value),
    removeItem: (key) => localStorage.removeItem(key),
  },
});
```

**Server-side with Request (Next.js/Hono):**
```typescript
const api = new Api({
  request: req, // Automatically extracts token from cookies/headers
});
```

**Direct Token:**
```typescript
const api = new Api({
  host: "https://api.example.com",
  token: "your-jwt-token",
});
```

**User Object (server-side, no token):**
```typescript
const api = new Api({
  host: "https://api.example.com",
  user: { id: 1, email: "user@example.com" },
  verified: true,
});
```

## Data API

Accessed via `api.data`. Provides CRUD operations on entities.

### Read Operations

```typescript
// Read single entity
const post = await api.data.readOne("posts", 1);

// Read many with query
const posts = await api.data.readMany("posts", {
  limit: 10,
  offset: 0,
  sort: "-created_at",
  where: { published: true },
  with: ["author", "comments"],
});

// Read one by filter
const post = await api.data.readOneBy("posts", {
  where: { slug: "hello-world" },
});

// Read related entities
const comments = await api.data.readManyByReference("posts", 1, "comments", {
  limit: 20,
});
```

### Create Operations

```typescript
// Create single
const newPost = await api.data.createOne("posts", {
  title: "Hello",
  content: "World",
  author_id: 1,
});

// Create many
const newPosts = await api.data.createMany("posts", [
  { title: "First", author_id: 1 },
  { title: "Second", author_id: 2 },
]);
```

### Update Operations

```typescript
// Update single
const updated = await api.data.updateOne("posts", 1, {
  title: "Updated title",
});

// Update many
await api.data.updateMany("posts", { published: false }, {
  published: true,
});
```

### Delete Operations

```typescript
// Delete single
await api.data.deleteOne("posts", 1);

// Delete many
await api.data.deleteMany("posts", { archived: true });
```

### Utility Methods

```typescript
// Count records
const { count } = await api.data.count("posts", { published: true });

// Check existence
const { exists } = await api.data.exists("posts", { slug: "hello-world" });
```

## Auth API

Accessed via `api.auth`. Handles authentication and session management.

```typescript
// Login with strategy
const res = await api.auth.login("password", {
  email: "user@example.com",
  password: "password",
});

// Register
const res = await api.auth.register("password", {
  email: "user@example.com",
  password: "password",
});

// Get current user
const { user } = await api.auth.me();

// Logout
await api.auth.logout(); // Clears token from storage

// Get available strategies
const { strategies } = await api.auth.strategies();

// Custom action (OAuth, etc.)
const actionRes = await api.auth.action("google", "callback", {
  code: "...",
  state: "...",
});
```

## Media API

Accessed via `api.media`. Handles file uploads and management.

```typescript
// Get upload info for direct upload
const { url, headers } = await api.media.getUploadInfo("uploads/image.jpg");

// Upload directly (returns URL)
const { url } = await api.media.upload(file);

// Delete file
await api.media.deleteFile("uploads/image.jpg");
```

## System API

Accessed via `api.system`. System-level operations.

```typescript
// Health check
await api.system.health();

// Get schema
const schema = await api.system.schema();
```

## Auth State Management

Track authentication state throughout your application.

```typescript
// Get current auth state
const state = api.getAuthState();
// { token?: string, user?: SafeUser, verified: boolean }

// Check if authenticated
if (api.isAuthenticated()) {
  const user = api.getUser();
}

// Verify token with server
const verifiedState = await api.getVerifiedAuthState();

// Manually update token
api.updateToken("new-jwt-token");
```

### Auth State Callback

```typescript
const api = new Api({
  host: "https://api.example.com",
  onAuthStateChange: (state) => {
    if (state.user) {
      console.log("Logged in as:", state.user.email);
    } else {
      console.log("Logged out");
    }
  },
});
```

## Type Safety

Import auto-generated types from `"bknd"` for full type safety.

```typescript
import type { DB, RepoQueryIn, SafeUser } from "bknd";
import { Api } from "bknd";

const api = new Api({ host: "https://api.example.com" });

// Entity types are auto-generated
type Post = DB["posts"];

// Query types are inferred
const query: RepoQueryIn = {
  limit: 10,
  where: { published: true },
};

// API methods return typed results
const posts = await api.data.readMany("posts", query);
// posts is RepositoryResultJSON<Selectable<DB["posts"]>[]>
```

## Error Handling

All API methods return a response object. Check `ok` before accessing data.

```typescript
const res = await api.data.readOne("posts", 1);

if (!res.ok) {
  console.error("Error:", res.body);
  return;
}

console.log("Post:", res.body);
```

## Module-Specific Options

Configure individual modules with custom options.

```typescript
const api = new Api({
  host: "https://api.example.com",
  data: {
    queryLengthLimit: 2000,
    defaultQuery: { limit: 20 },
  },
  auth: {
    basepath: "/api/custom-auth",
    credentials: "include",
  },
});
```

## Common Patterns

### Fetch with Auto-Auth

```typescript
const api = new Api({
  host: "https://api.example.com",
  storage: localStorage,
});

// Login first
await api.auth.login("password", { email: "user@example.com", password: "pass" });

// Subsequent requests automatically include the token
const posts = await api.data.readMany("posts");
```

### Server-Side Protected Request

```typescript
// In Next.js server component or Hono middleware
const api = new Api({ request: req });

if (!api.isAuthenticated()) {
  return new Response("Unauthorized", { status: 401 });
}

const user = api.getUser();
const posts = await api.data.readMany("posts", { author_id: user.id });
```

### Custom Fetcher

```typescript
const api = new Api({
  host: "https://api.example.com",
  fetcher: async (input, init) => {
    console.log("Request:", input, init);
    const response = await fetch(input, init);
    console.log("Response:", response.status);
    return response;
  },
});
```

## DOs and DON'Ts

**DO:**
- Use `api.data.readMany()` for most read operations with query parameters
- Provide `storage` option for client-side token persistence
- Use `api.getAuthState()` to check authentication status
- Import types from `"bknd"` for type safety

**DON'T:**
- Forget to handle errors by checking `res.ok`
- Use `readOneBy` for single entity lookups by ID (use `readOne` instead)
- Manually set headers for authentication (SDK handles this)
- Mix token and user object in same Api instance

## See Also

- [React SDK](/skills/react-sdk) - React hooks built on TypeScript SDK
- [Query System](/skills/query) - Advanced query syntax
- [Auth](/skills/auth) - Authentication configuration
