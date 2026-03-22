---
name: api-baas-appwrite
description: Appwrite backend-as-a-service — Auth, TablesDB, Storage, Functions, Realtime, permissions model, typed client
---

# Appwrite Patterns

> **Quick Guide:** Use Appwrite as your open-source BaaS for authentication, structured data (TablesDB), file storage, serverless functions, and realtime subscriptions. Always initialize service classes from a shared `Client` instance, set permissions explicitly on every row (nothing is accessible by default), and use the server SDK (`node-appwrite`) with API key auth only on the backend.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST set permissions explicitly on every row and file — Appwrite grants NO access by default, so omitting permissions makes data inaccessible)**

**(You MUST use `node-appwrite` with API key auth on the server and `appwrite` with session auth on the client — NEVER expose API keys in client bundles)**

**(You MUST always check for `AppwriteException` on every SDK call — Appwrite throws exceptions, it does NOT return `{ data, error }` tuples)**

**(You MUST use `ID.unique()` for auto-generated IDs — passing a raw string creates a custom ID, not an auto-generated one)**

**(You MUST use the TablesDB API for new projects — the legacy Databases/collections/documents API is deprecated and receives only security patches)**

</critical_requirements>

---

**Auto-detection:** Appwrite, appwrite, node-appwrite, TablesDB, Account, Databases, Permission, Role, ID.unique, Query.equal, createEmailPasswordSession, realtime.subscribe, Channel.files, Channel.tablesdb, APPWRITE_FUNCTION

**When to use:**

- Setting up an Appwrite client or server SDK with TypeScript
- Implementing authentication (email/password, OAuth, magic URL, phone OTP, anonymous sessions)
- Performing CRUD on TablesDB tables (rows, queries, permissions)
- Uploading and serving files from Storage buckets with access control
- Building serverless functions triggered by events, schedules, or HTTP
- Subscribing to realtime changes on rows, files, or account events
- Managing team memberships and role-based permissions

**Key patterns covered:**

- Client and server SDK initialization with typed service classes
- Auth flows: sign up, sign in, OAuth, magic URL, session management
- TablesDB operations with `Query` class for filtering, pagination, ordering
- Permission model: `Permission.read(Role.any())`, `Role.user()`, `Role.team()`
- Storage: upload, download, preview with image transforms, bucket permissions
- Serverless functions: `export default async ({ req, res, log, error }) => {}`
- Realtime subscriptions via `Channel` helpers and `realtime.subscribe()`

**When NOT to use:**

- Direct database connections or SQL queries (Appwrite is API-only, no raw SQL)
- Complex relational joins across many tables (Appwrite supports relationships but not arbitrary SQL joins)
- Applications requiring server-side realtime (Appwrite Realtime is client SDK only)

**Detailed Resources:**

- For decision frameworks and anti-patterns, see [reference.md](reference.md)

**Client & Queries:**

- [examples/core.md](examples/core.md) — Client setup, TablesDB CRUD, error handling, permissions

**Authentication:**

- [examples/auth.md](examples/auth.md) — Full auth flows, OAuth, magic URL, sessions, teams

**Storage & Functions:**

- [examples/storage.md](examples/storage.md) — File upload, download, previews, bucket permissions
- [examples/functions.md](examples/functions.md) — Serverless functions, triggers, SDK usage inside functions

**Realtime:**

- [examples/realtime.md](examples/realtime.md) — Channel subscriptions, event filtering, cleanup

---

<philosophy>

## Philosophy

Appwrite is an open-source backend-as-a-service providing authentication, databases (TablesDB), file storage, serverless functions, and realtime — all through a unified SDK. It can be self-hosted or used via Appwrite Cloud.

**Core principles:**

1. **Secure by default** — Nothing is accessible without explicit permissions. Every row and file must have permissions set, or it is invisible to all users. This is the opposite of "open by default" — treat it as a mandatory step, not an afterthought.
2. **Service class architecture** — All SDK interactions go through service classes (`Account`, `TablesDB`, `Storage`, `Functions`, `Teams`, `Realtime`) instantiated from a shared `Client`. This pattern is consistent across client and server SDKs.
3. **Two SDK split** — `appwrite` (client) uses session-based auth for browsers. `node-appwrite` (server) uses API key auth for backends. They share the same API shape but different auth mechanisms. Never mix them.
4. **Exceptions, not tuples** — Appwrite throws `AppwriteException` on failure, not `{ data, error }` tuples. Always wrap calls in try/catch.
5. **TablesDB is the future** — Appwrite 1.8 introduced TablesDB (tables/rows/columns) as the modern API. The legacy Databases API (collections/documents/attributes) still works but is deprecated. New features only land in TablesDB.
6. **ID generation** — Use `ID.unique()` for server-generated unique IDs. If you pass a string directly, it becomes a custom ID (which must be globally unique within the table).

**When to use Appwrite:**

- Open-source, self-hostable BaaS with full control over your data
- Projects needing auth, database, storage, and functions in one platform
- Teams wanting a self-hostable BaaS with no vendor lock-in
- Applications that benefit from granular document/row-level permissions

**When NOT to use:**

- Complex SQL-heavy applications requiring joins, views, and stored procedures
- Server-side realtime consumers (Appwrite Realtime is client SDK only — no server SDK support)
- Offline-first apps requiring local-first sync (Appwrite has no built-in offline sync)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Client SDK Setup (Browser)

Initialize the Appwrite client with endpoint and project ID. All service classes share a single `Client` instance.

```typescript
// lib/appwrite.ts
import { Client, Account, TablesDB, Storage, Realtime } from "appwrite";

const APPWRITE_ENDPOINT = process.env.APPWRITE_ENDPOINT!;
const APPWRITE_PROJECT_ID = process.env.APPWRITE_PROJECT_ID!;

const client = new Client()
  .setEndpoint(APPWRITE_ENDPOINT)
  .setProject(APPWRITE_PROJECT_ID);

export const account = new Account(client);
export const tablesDB = new TablesDB(client);
export const storage = new Storage(client);
export const realtime = new Realtime(client);
```

**Why good:** Single client instance shared across services, named constants for config, named exports for each service, environment variables keep config out of code

```typescript
// BAD: Hardcoded config, recreating clients
import { Client, Account } from "appwrite";

const account = new Account(
  new Client()
    .setEndpoint("https://cloud.appwrite.io/v1") // Hardcoded
    .setProject("abc123"), // Hardcoded project ID
);
```

**Why bad:** Hardcoded endpoint and project ID, new Client per service wastes resources, no shared config

---

### Pattern 2: Server SDK Setup (Node.js)

The server SDK uses API key authentication — never expose API keys in client code.

```typescript
// lib/appwrite-server.ts
import { Client, TablesDB, Users, Storage } from "node-appwrite";

const APPWRITE_ENDPOINT = process.env.APPWRITE_ENDPOINT!;
const APPWRITE_PROJECT_ID = process.env.APPWRITE_PROJECT_ID!;
const APPWRITE_API_KEY = process.env.APPWRITE_API_KEY!;

const client = new Client()
  .setEndpoint(APPWRITE_ENDPOINT)
  .setProject(APPWRITE_PROJECT_ID)
  .setKey(APPWRITE_API_KEY);

export const tablesDB = new TablesDB(client);
export const users = new Users(client);
export const storage = new Storage(client);
```

**Why good:** `.setKey()` for API key auth (server only), `Users` service for admin user management (not available in client SDK), named constants

**When to use:** API routes, serverless functions, admin scripts, webhooks. NEVER import this module from client-side code.

---

### Pattern 3: Error Handling (AppwriteException)

Appwrite throws `AppwriteException` — it does NOT return `{ data, error }` tuples. Always use try/catch.

```typescript
import { AppwriteException, type Models } from "appwrite";

async function getUser(): Promise<Models.User<Models.Preferences>> {
  try {
    return await account.get();
  } catch (error) {
    if (error instanceof AppwriteException) {
      // error.message — human-readable message
      // error.code — HTTP status code (401, 404, etc.)
      // error.type — machine-readable error type string
      throw new Error(`Appwrite error ${error.code}: ${error.message}`);
    }
    throw error;
  }
}
```

**Why good:** Type-narrowed `AppwriteException` provides `code`, `message`, `type`; re-throws unknown errors; explicit return type using `Models` namespace

```typescript
// BAD: Assuming { data, error } tuple returns
const { data, error } = await account.get(); // WRONG — Appwrite throws, not returns tuples
if (error) {
  /* ... */
}
```

**Why bad:** Appwrite does NOT return error tuples — this code will fail silently because `account.get()` either returns data or throws

---

### Pattern 4: TablesDB Operations (CRUD)

Use `TablesDB` for all database operations. Row IDs are required for create — use `ID.unique()` for auto-generation.

#### Create a Row

```typescript
import { ID, Permission, Role } from "appwrite";

interface Todo {
  title: string;
  completed: boolean;
}

const DATABASE_ID = "main";
const TABLE_ID = "todos";

const row = await tablesDB.createRow<Todo>({
  databaseId: DATABASE_ID,
  tableId: TABLE_ID,
  rowId: ID.unique(),
  data: {
    title: "Buy groceries",
    completed: false,
  },
  permissions: [
    Permission.read(Role.user(userId)),
    Permission.update(Role.user(userId)),
    Permission.delete(Role.user(userId)),
  ],
});
```

#### List Rows with Queries

```typescript
import { Query } from "appwrite";

const PAGE_SIZE = 25;

const result = await tablesDB.listRows<Todo>({
  databaseId: DATABASE_ID,
  tableId: TABLE_ID,
  queries: [
    Query.equal("completed", false),
    Query.orderDesc("$createdAt"),
    Query.limit(PAGE_SIZE),
  ],
});

// result.rows — array of Todo rows
// result.total — total matching count
```

#### Update a Row

```typescript
const updated = await tablesDB.updateRow<Todo>({
  databaseId: DATABASE_ID,
  tableId: TABLE_ID,
  rowId: row.$id,
  data: { completed: true },
});
```

#### Delete a Row

```typescript
await tablesDB.deleteRow({
  databaseId: DATABASE_ID,
  tableId: TABLE_ID,
  rowId: row.$id,
});
```

**Why good:** Named constants for database/table IDs, `ID.unique()` for auto-generated IDs, permissions set explicitly on create, `Query` class for type-safe filtering, generic type parameter for row shape

---

### Pattern 5: Permissions Model

Appwrite grants NO access by default. You must set permissions on every row and file.

#### Permission + Role Syntax

```typescript
import { Permission, Role } from "appwrite";

// Public read, owner full access
const publicReadPermissions = [
  Permission.read(Role.any()),
  Permission.update(Role.user(userId)),
  Permission.delete(Role.user(userId)),
];

// Team access
const teamPermissions = [
  Permission.read(Role.team(teamId)),
  Permission.update(Role.team(teamId, "admin")),
  Permission.delete(Role.team(teamId, "owner")),
];

// Verified users only
const verifiedOnlyPermissions = [Permission.read(Role.users("verified"))];
```

#### Common Role Helpers

```typescript
Role.any(); // Anyone (including guests)
Role.guests(); // Unauthenticated users only
Role.users(); // All authenticated users
Role.users("verified"); // Only verified users
Role.user(userId); // Specific user by ID
Role.team(teamId); // All members of a team
Role.team(teamId, "admin"); // Team members with "admin" role
Role.member(membershipId); // Specific team membership
Role.label("premium"); // Users with "premium" label
```

**Why good:** Explicit permissions on every resource, role helpers are type-safe, team roles enable granular access

```typescript
// BAD: Creating a row without permissions
const row = await tablesDB.createRow({
  databaseId: DATABASE_ID,
  tableId: TABLE_ID,
  rowId: ID.unique(),
  data: { title: "Secret" },
  // NO permissions set — this row is INVISIBLE to everyone!
});
```

**Why bad:** Without permissions, the row exists in the database but NO user can read, update, or delete it (not even the creator) — this is the most common Appwrite mistake

---

### Pattern 6: Authentication Flows

Use the `Account` service for all auth operations.

#### Email/Password Sign Up and Sign In

```typescript
import { ID, type Models } from "appwrite";

// Sign up: create account + create session (two steps)
const user = await account.create({
  userId: ID.unique(),
  email,
  password,
  name,
});
const session = await account.createEmailPasswordSession({ email, password });

// Sign in
const session = await account.createEmailPasswordSession({ email, password });

// Sign out (current device)
await account.deleteSession({ sessionId: "current" });
```

**Why good:** Two-step sign up (create account + create session), object parameters for all SDK calls, `deleteSession({ sessionId: "current" })` for current device only

See [examples/auth.md](examples/auth.md) for full auth flows including OAuth, magic URL, anonymous sessions, teams, and password reset.

---

### Pattern 7: Storage Operations

Upload, download, and preview files with the `Storage` service.

```typescript
import { ID, Permission, Role } from "appwrite";

const BUCKET_ID = "user-uploads";
const PREVIEW_WIDTH = 400;
const PREVIEW_HEIGHT = 300;

// Upload with permissions
await storage.createFile({
  bucketId: BUCKET_ID,
  fileId: ID.unique(),
  file,
  permissions: [
    Permission.read(Role.user(userId)),
    Permission.update(Role.user(userId)),
  ],
});

// Image preview with transforms
const url = storage.getFilePreview({
  bucketId: BUCKET_ID,
  fileId,
  width: PREVIEW_WIDTH,
  height: PREVIEW_HEIGHT,
});

// Download URL
const downloadUrl = storage.getFileDownload({ bucketId: BUCKET_ID, fileId });
```

**Why good:** Object parameters for all SDK calls, named constants, `ID.unique()` for file IDs, permissions set on upload

See [examples/storage.md](examples/storage.md) for full upload, preview, download, and file management patterns.

---

### Pattern 8: Realtime Subscriptions

Subscribe to changes using the `Realtime` service with `Channel` helpers.

```typescript
import { Realtime, Channel } from "appwrite";

const DATABASE_ID = "main";
const TABLE_ID = "messages";

// Subscribe to all changes on a table
const subscription = await realtime.subscribe(
  Channel.tablesdb(DATABASE_ID).table(TABLE_ID),
  (response) => {
    if (response.events.includes("tablesdb.*.tables.*.rows.*.create")) {
      console.log("New row:", response.payload);
    }
    if (response.events.includes("tablesdb.*.tables.*.rows.*.update")) {
      console.log("Updated row:", response.payload);
    }
    if (response.events.includes("tablesdb.*.tables.*.rows.*.delete")) {
      console.log("Deleted row:", response.payload);
    }
  },
);

// IMPORTANT: Always unsubscribe when done
await subscription.close();
```

#### Subscribe to Files

```typescript
const fileSubscription = await realtime.subscribe(
  Channel.files(),
  (response) => {
    if (response.events.includes("buckets.*.files.*.create")) {
      console.log("New file uploaded:", response.payload);
    }
  },
);
```

#### Subscribe to Account Changes

```typescript
const accountSub = await realtime.subscribe(Channel.account(), (response) => {
  console.log("Account event:", response.events);
});
```

**Why good:** `Channel` helpers provide type-safe channel construction, event string matching for filtering, explicit cleanup with `subscription.close()`, separate subscriptions per concern

**When to use:** Chat apps, live dashboards, collaborative editing, notification feeds. Avoid for high-frequency data streams.

</patterns>

---

<decision_framework>

## Decision Framework

### Client SDK vs Server SDK

```
Where is the code running?
+-  Browser / Client-side -> `appwrite` package, session auth
+-  Server / API route -> `node-appwrite` package, API key auth
+-  Serverless function -> `node-appwrite` package, dynamic key from `req.headers['x-appwrite-key']`
    +-- NEVER expose API keys in client bundles
```

### TablesDB vs Legacy Databases

```
Which API should I use?
+-  New project -> TablesDB (tables, rows, columns)
+-  Existing project with collections -> Legacy Databases still works (deprecated, security patches only)
+-  Migrating -> Adopt TablesDB for new tables, migrate existing gradually
```

### Auth Method Selection

```
What auth flow does the user need?
+-  Email + Password -> account.create({ ... }) + account.createEmailPasswordSession({ ... })
+-  Social login (GitHub, Google, etc.) -> account.createOAuth2Session({ provider: OAuthProvider.Github, ... })
+-  Passwordless email -> account.createMagicURLToken({ ... })
+-  Phone + SMS -> account.createPhoneToken({ ... })
+-  Guest / anonymous -> account.createAnonymousSession()
+-  Existing JWT -> client.setJWT()
```

### Permissions Strategy

```
Who should access this resource?
+-  Public (anyone) -> Permission.read(Role.any())
+-  Owner only -> Permission.read(Role.user(userId))
+-  Team members -> Permission.read(Role.team(teamId))
+-  Team role (e.g. admins) -> Permission.read(Role.team(teamId, "admin"))
+-  Verified users -> Permission.read(Role.users("verified"))
+-  Labeled users -> Permission.read(Role.label("premium"))
```

### Storage: Public vs Private

```
Who should see the files?
+-  Anyone (public assets) -> Set Permission.read(Role.any()) on the file
+-  Owner only (private docs) -> Set Permission.read(Role.user(userId))
+-  Team access -> Set Permission.read(Role.team(teamId))
+-  Server-only -> Use server SDK with API key (bypasses all permissions)
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **No permissions on rows/files** — Appwrite grants ZERO access by default. A row without permissions is completely invisible. This is the number one mistake new Appwrite developers make.
- **API key in client bundle** — The `node-appwrite` server SDK with API key auth must NEVER be imported in browser code. API keys bypass all permissions.
- **Assuming `{ data, error }` return pattern** — Appwrite throws `AppwriteException`, not error tuples. Using destructuring like `const { data, error } = await account.get()` will fail silently.
- **Using legacy Databases API for new projects** — `Databases` (collections/documents) is deprecated as of Appwrite 1.8. Use `TablesDB` (tables/rows) for all new work.
- **Using positional parameters** — As of `appwrite@19.0.0` / `node-appwrite@18.0.0` (September 2025), all SDK methods use object parameters. Positional arguments are deprecated. Use `account.create({ userId, email, password })` not `account.create(userId, email, password)`.
- **Using string literals for OAuth providers** — Use the `OAuthProvider` enum: `OAuthProvider.Github` not `"github"`.

**Medium Priority Issues:**

- **Forgetting `ID.unique()`** — Passing a raw string as a row/file ID creates a custom ID. If you want auto-generated IDs, you must explicitly call `ID.unique()`.
- **Not unsubscribing from Realtime** — Each `realtime.subscribe()` adds to a shared WebSocket. Failing to `subscription.close()` leaks connections and causes duplicate events.
- **Using `Permission.write()` when you mean specific actions** — `Permission.write()` is an alias for create + update + delete combined. Use `Permission.update()` and `Permission.delete()` separately for granular control.
- **Calling `account.create()` without `createEmailPasswordSession()`** — `create()` registers the user but does NOT create a session. The user is not logged in until you call a session method.
- **Server SDK Realtime** — Appwrite Realtime is NOT available through server SDKs. Subscriptions only work with client SDKs.

**Common Mistakes:**

- **OAuth: no code runs after `createOAuth2Session()`** — This method triggers a browser redirect. Any code after the call will not execute.
- **Not setting both success AND failure URLs for OAuth** — If you omit the failure URL, failed auth has no redirect target.
- **Using `Role.users()` when you mean `Role.user(userId)`** — `Role.users()` grants access to ALL authenticated users. `Role.user(userId)` grants access to ONE specific user.
- **Expecting `$createdAt` / `$updatedAt` in queries without `$` prefix** — System fields in Appwrite use `$` prefix: `$id`, `$createdAt`, `$updatedAt`, `$permissions`.

**Gotchas & Edge Cases:**

- **Row security vs table-level permissions** — By default, only table-level permissions apply. To use row-level (document-level) permissions, you must enable "Row Security" in the table settings. When enabled, BOTH table-level AND row-level permissions must pass.
- **`Permission.read(Role.any())` includes guests** — `Role.any()` means everyone, including unauthenticated users. Use `Role.users()` for authenticated-only access.
- **Realtime reconnection creates new WebSocket** — Adding or removing a subscription tears down and recreates the entire WebSocket connection. Batch subscription changes where possible.
- **File preview only works for images** — `storage.getFilePreview()` with width/height transforms only works on image files. For non-images, use `getFileDownload()` or `getFileView()`.
- **`account.get()` throws if no session** — There is no "null user" return. An unauthenticated call throws 401. Wrap in try/catch and return `null` for "no user" state.
- **Max 100 rows per `listRows()` call** — The default and maximum limit is 100. For larger datasets, use cursor-based pagination with `Query.cursorAfter()`.
- **Appwrite function cold starts** — Functions have cold start latency on first invocation after idle. Design "fat functions" (one function handling multiple routes) to reduce cold starts.
- **`Query.search()` requires a full-text index** — The `search` query method only works on columns that have a full-text index configured in the Appwrite console.
- **Labels are server-only** — User labels (`Role.label("premium")`) can only be set via the server SDK `users.updateLabels()`. Clients cannot modify their own labels.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST set permissions explicitly on every row and file — Appwrite grants NO access by default, so omitting permissions makes data inaccessible)**

**(You MUST use `node-appwrite` with API key auth on the server and `appwrite` with session auth on the client — NEVER expose API keys in client bundles)**

**(You MUST always check for `AppwriteException` on every SDK call — Appwrite throws exceptions, it does NOT return `{ data, error }` tuples)**

**(You MUST use `ID.unique()` for auto-generated IDs — passing a raw string creates a custom ID, not an auto-generated one)**

**(You MUST use the TablesDB API for new projects — the legacy Databases/collections/documents API is deprecated and receives only security patches)**

**Failure to follow these rules will create inaccessible data, security vulnerabilities, and silent runtime failures.**

</critical_reminders>
