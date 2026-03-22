---
name: api-baas-supabase
description: Supabase backend-as-a-service — Auth, Database, Realtime, Storage, Edge Functions, RLS policies, typed client
---

# Supabase Patterns

> **Quick Guide:** Use Supabase as your backend-as-a-service for Postgres database, authentication, realtime subscriptions, file storage, and edge functions. Always use the typed client with `Database` generic, enable RLS on every table, and use `service_role` key only on the server.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST enable Row Level Security (RLS) on EVERY table in an exposed schema — no exceptions)**

**(You MUST use the `Database` generic type with `createClient<Database>()` for type-safe queries)**

**(You MUST NEVER expose the `service_role` key in client-side code — use `anon` key in browsers, `service_role` only on the server)**

**(You MUST use `(select auth.uid())` wrapped in a subquery inside RLS policies for performance)**

**(You MUST handle all Supabase responses with `{ data, error }` destructuring — never assume success)**

</critical_requirements>

---

**Auto-detection:** Supabase, createClient, @supabase/supabase-js, @supabase/ssr, supabase-js, auth.uid(), RLS, row level security, realtime, postgres_changes, supabase.auth, supabase.from, supabase.storage, supabase.functions, supabase.channel, edge function, Deno.serve

**When to use:**

- Setting up a Supabase client with TypeScript type safety
- Implementing authentication (email/password, OAuth, magic links, session management)
- Querying Postgres via the Supabase client (select, insert, update, delete, RPC)
- Writing Row Level Security policies for data access control
- Subscribing to database changes in real time
- Uploading and serving files from Supabase Storage
- Building serverless functions with Supabase Edge Functions (Deno)

**Key patterns covered:**

- Typed client setup with `Database` generic and environment variables
- Auth flows: sign up, sign in, OAuth, magic link, session refresh, `onAuthStateChange`
- Database queries with filters, joins, RPC calls, and error handling
- RLS policies: `USING` vs `WITH CHECK`, `auth.uid()`, role-based access
- Realtime subscriptions via `channel().on('postgres_changes')`
- Storage: upload, signed URLs, public URLs, bucket policies
- Edge Functions: `Deno.serve`, CORS headers, secrets, Supabase client in functions

**When NOT to use:**

- Direct Postgres connections (use a database driver skill instead)
- Complex server-side ORM patterns (use a dedicated ORM skill)
- Non-Supabase authentication providers (use dedicated auth skills)

**Detailed Resources:**

- For decision frameworks and anti-patterns, see [reference.md](reference.md)

**Client & Queries:**

- [examples/core.md](examples/core.md) — Client setup, typed queries, error handling patterns

**Authentication:**

- [examples/auth.md](examples/auth.md) — Full auth flows, OAuth, magic links, session refresh, middleware protection

**Database:**

- [examples/database.md](examples/database.md) — Complex queries, joins, RPC, migrations, type generation

**Storage:**

- [examples/storage.md](examples/storage.md) — File upload, signed URLs, bucket policies, image transforms

**Edge Functions:**

- [examples/edge-functions.md](examples/edge-functions.md) — Deno edge functions, `Deno.serve()`, CORS, secrets

---

<philosophy>

## Philosophy

Supabase is an open-source Firebase alternative built on Postgres. It provides a complete backend through a combination of Postgres extensions, auto-generated REST/GraphQL APIs, authentication, realtime subscriptions, file storage, and edge functions.

**Core principles:**

1. **Postgres at the core** — Every feature is built on Postgres. RLS policies, auth, and realtime all leverage Postgres primitives. Understanding Postgres is understanding Supabase.
2. **Type safety end-to-end** — Generate TypeScript types from your database schema with `supabase gen types`. Pass the `Database` generic to `createClient` for fully typed queries.
3. **Security by default** — RLS must be enabled on every table. The `anon` key is safe for browsers (RLS enforces access). The `service_role` key bypasses RLS and must never leave the server.
4. **Error as values** — Every Supabase method returns `{ data, error }`. Never assume success. Always check `error` before using `data`.
5. **Realtime built in** — Postgres changes stream over WebSockets via channels. No separate pub/sub infrastructure needed.
6. **Edge-first functions** — Edge Functions run Deno at the edge, close to users. Design for short-lived, idempotent operations.

**When to use Supabase:**

- Rapid backend development with Postgres, auth, and storage out of the box
- Projects needing realtime features (chat, notifications, live dashboards)
- Teams wanting to avoid managing separate auth, database, and storage services
- Applications that benefit from Row Level Security for multi-tenant data isolation

**When NOT to use:**

- Complex server-side business logic requiring a full application server (use Edge Functions for simple cases, a dedicated API for complex ones)
- Applications needing an ORM with advanced query building (Supabase query builder is powerful but not a full ORM)
- Offline-first applications requiring complex sync protocols

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Typed Client Setup

Always pass the `Database` generic to `createClient` for full autocomplete on table names, column names, and return types. Use environment variables for URL and keys.

```typescript
export const supabase = createClient<Database>(SUPABASE_URL, SUPABASE_ANON_KEY);
```

Without the generic, typos in table/column names are not caught at compile time. See [examples/core.md](examples/core.md) for browser, server, and admin client setup patterns.

---

### Pattern 2: Error Handling with { data, error }

Every Supabase method returns `{ data, error }`. Always destructure and check `error` before using `data`. Never use non-null assertions on `data`.

```typescript
const { data, error } = await supabase
  .from("profiles")
  .select("id, username")
  .eq("id", userId)
  .single();
if (error) throw new Error(`Failed to fetch profile: ${error.message}`);
```

See [examples/core.md](examples/core.md) for the reusable error handler pattern and common mistakes.

---

### Pattern 3: Authentication Flows

Supabase Auth supports email/password (`signInWithPassword`), OAuth (`signInWithOAuth`), magic links (`signInWithOtp`), and phone OTP. Register `onAuthStateChange` early in the app lifecycle and always clean up with `subscription.unsubscribe()`.

Key gotcha: Do NOT call Supabase methods directly inside `onAuthStateChange` — use `setTimeout(..., 0)` to defer.

See [examples/auth.md](examples/auth.md) for sign up, sign in, OAuth, magic link, session management, middleware protection, and password reset patterns.

---

### Pattern 4: Database Queries

Use the query builder for type-safe CRUD with filters, joins, ordering, and pagination. Always add `.select()` after `.insert()` or `.update()` to return the affected row.

```typescript
const { data, error } = await supabase
  .from("posts")
  .select("id, title, author:profiles(username)")
  .eq("published", true)
  .order("created_at", { ascending: false })
  .range(0, PAGE_SIZE - 1);
```

See [examples/database.md](examples/database.md) for complex queries, upserts, RPC calls, conditional filters, counting, and migrations.

---

### Pattern 5: Row Level Security (RLS) Policies

RLS is the primary security mechanism. Enable it on every table, write separate policies per operation (not `FOR ALL`), and wrap `auth.uid()` in a subquery for performance.

```sql
alter table public.posts enable row level security;

create policy "posts_select" on public.posts for select to authenticated
using ( published = true or (select auth.uid()) = author_id );
```

Never trust `user_metadata` from JWT for access control — it is user-modifiable. See [examples/database.md](examples/database.md) for full CRUD policies, team-based access, and anti-patterns.

---

### Pattern 6: Realtime Subscriptions

Subscribe to database changes via `channel().on('postgres_changes', ...)`. Always unsubscribe on cleanup. DELETE events cannot be filtered — all deletes are received. UPDATE/DELETE payloads need `replica identity full` for old record data.

```typescript
const channel = supabase
  .channel("room-messages")
  .on(
    "postgres_changes",
    {
      event: "INSERT",
      schema: "public",
      table: "messages",
      filter: `room_id=eq.${roomId}`,
    },
    (payload) => {
      /* handle */
    },
  )
  .subscribe();
```

Use for chat, live dashboards, notifications. Avoid for high-frequency data (> 100 updates/sec).

---

### Pattern 7: Storage Operations

Upload files with `supabase.storage.from(bucket).upload()`. Use `getPublicUrl()` for public buckets, `createSignedUrl()` for private buckets with time-limited access. Storage access control uses RLS on `storage.objects`.

See [examples/storage.md](examples/storage.md) for upload, signed URLs, public URLs, image transforms, bucket policies, and signed upload URLs.

---

### Pattern 8: Edge Functions

Use `Deno.serve()` (not the deprecated `serve` import). Import supabase-js with `npm:` prefix: `import { createClient } from "npm:@supabase/supabase-js@2"`. Handle CORS on every response. Use `Deno.env.get()` for secrets. Forward user JWT for RLS enforcement.

See [examples/edge-functions.md](examples/edge-functions.md) for basic functions, authenticated access, shared utilities, webhooks, multi-route "fat functions", and background processing with `EdgeRuntime.waitUntil()`.

</patterns>

---

<decision_framework>

## Decision Framework

### Which Supabase Key to Use

```
Where is the code running?
├─ Browser / Client-side → anon key (RLS enforced)
├─ Server / API route → anon key + user JWT (RLS enforced per user)
└─ Admin / Migration script → service_role key (bypasses RLS)
    └─ NEVER expose service_role in client bundles
```

### Auth Method Selection

```
What auth flow does the user need?
├─ Email + Password → signInWithPassword
├─ Social login (GitHub, Google, etc.) → signInWithOAuth
├─ Passwordless email → signInWithOtp (magic link)
├─ Phone + SMS → signInWithOtp (phone)
└─ SSO / SAML → signInWithSSO (enterprise)
```

### Realtime vs Polling

```
How fresh must the data be?
├─ Instant (< 1 second) → Realtime subscription (postgres_changes)
├─ Near-instant (1-5 seconds) → Realtime subscription
├─ Periodic (> 5 seconds ok) → Polling with setInterval
└─ On-demand (user refresh) → Re-fetch on action
    └─ High-frequency updates (> 100/sec)?
        ├─ YES → Polling or batch (Realtime has per-subscriber checks)
        └─ NO → Realtime is fine
```

### Storage: Public vs Private Buckets

```
Who should access the files?
├─ Anyone (public assets, avatars) → Public bucket + getPublicUrl()
├─ Authenticated users only → Private bucket + createSignedUrl()
├─ Specific users (own files) → Private bucket + RLS on storage.objects
└─ Server-only processing → service_role key for upload/download
```

### Edge Functions vs Client Queries

```
Does the operation need server-side logic?
├─ Simple CRUD → Client query with RLS (no edge function needed)
├─ Multi-step / transactional → Edge function or Postgres function (RPC)
├─ Third-party API call → Edge function
├─ Webhook receiver → Edge function
└─ Heavy computation → Edge function with EdgeRuntime.waitUntil() for background work
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Missing RLS on tables** — Any table without RLS in an exposed schema is completely open to the public. In January 2025, 170+ apps were found with exposed databases due to missing RLS (CVE-2025-48757).
- **service_role key in client code** — The service_role key bypasses all RLS. Exposing it in browser bundles gives every user full admin database access.
- **Ignoring `{ data, error }` returns** — Accessing `data` without checking `error` leads to runtime crashes when operations fail.
- **Using `auth.jwt() ->> 'user_metadata'` in RLS policies** — `user_metadata` is modifiable by authenticated users via `updateUser()`. Never use it for access control decisions.

**Medium Priority Issues:**

- **Using `FOR ALL` in RLS policies** — Separate into `SELECT`, `INSERT`, `UPDATE`, `DELETE` policies for clarity and auditability.
- **Bare `auth.uid()` in policies without subquery** — Wrap in `(select auth.uid())` for up to 94-99% performance improvement per Supabase benchmarks.
- **Not specifying `to authenticated` or `to anon` in policies** — Without a role, policies apply to all roles, which may expose data unintentionally.
- **Using `select("*")` everywhere** — Fetches all columns including sensitive data. Select only the columns you need.
- **Deprecated `serve` import in Edge Functions** — `import { serve } from "https://deno.land/std/http/server.ts"` is deprecated. Use `Deno.serve()`.

**Common Mistakes:**

- **Not adding `.select()` after `.insert()` or `.update()`** — Without `.select()`, these methods return no data (only `null`).
- **Missing CORS headers in Edge Functions** — Browser requests fail without proper CORS headers and OPTIONS handling.
- **Not unsubscribing from Realtime channels** — Leaks WebSocket connections and can cause memory issues.
- **Using bare specifiers in Edge Functions** — `import { createClient } from "@supabase/supabase-js"` fails in Deno. Use `npm:@supabase/supabase-js@2`.
- **Using `getSession()` to verify auth** — `getSession()` reads from local storage and can be tampered with. Use `getUser()` for secure server-side verification.

**Gotchas & Edge Cases:**

- **Realtime DELETE events cannot be filtered** — All deletes for a subscribed table are received regardless of filter.
- **Realtime requires `replica identity full` for old record data** — By default, UPDATE and DELETE payloads only include the new record. Set `alter table X replica identity full` to access `payload.old`.
- **RLS policies are not applied to Realtime DELETE events** — Be cautious about what information DELETE events expose.
- **`onAuthStateChange` fires on tab focus** — `SIGNED_IN` events fire when a browser tab regains focus, not just on actual sign-in.
- **Do NOT call Supabase methods inside `onAuthStateChange` callback** — This can cause deadlocks. Use `setTimeout(..., 0)` to defer.
- **Signed URLs expire** — `createSignedUrl()` URLs expire after the specified duration. Signed upload URLs expire after 2 hours.
- **Public bucket URLs bypass RLS** — Files in public buckets are accessible to anyone with the URL, regardless of policies.
- **Edge Function cold starts** — First invocation after idle period has additional latency. Design "fat functions" (fewer, larger functions) to minimize cold starts.
- **Edge Functions: file writes only on `/tmp`** — The `/tmp` directory is the only writable path in edge functions.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST enable Row Level Security (RLS) on EVERY table in an exposed schema — no exceptions)**

**(You MUST use the `Database` generic type with `createClient<Database>()` for type-safe queries)**

**(You MUST NEVER expose the `service_role` key in client-side code — use `anon` key in browsers, `service_role` only on the server)**

**(You MUST use `(select auth.uid())` wrapped in a subquery inside RLS policies for performance)**

**(You MUST handle all Supabase responses with `{ data, error }` destructuring — never assume success)**

**Failure to follow these rules will create security vulnerabilities, type-unsafe queries, and silent runtime failures.**

</critical_reminders>
