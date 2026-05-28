---
name: supabase-ts
description: Production-ready Supabase integration patterns for Next.js/React/TypeScript applications. Use when working with Supabase for (1) SSR authentication with @supabase/ssr, (2) Database operations and migrations, (3) Row Level Security (RLS) policies, (4) Storage buckets and file uploads, (5) Realtime channels and presence, (6) Edge Functions with Deno, (7) pgvector embeddings and semantic search, (8) Vercel deployment and connection pooling, (9) CLI operations (type generation, migrations). Triggers on Supabase client setup, auth patterns, RLS policies, storage uploads, realtime subscriptions, Edge Functions, vector search, or Vercel+Supabase deployment.
---

# Supabase TypeScript

Production patterns for Supabase in Next.js/React/Vercel applications with TypeScript and Zod v4.

## Quick Reference

### Server Client (Next.js App Router)

```typescript
// src/lib/supabase/server.ts
import "server-only";
import { cookies } from "next/headers";
import { createServerClient } from "@supabase/ssr";
import type { Database } from "./database.types";

export async function createServerSupabase() {
  const cookieStore = await cookies();
  return createServerClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll: () => cookieStore.getAll(),
        setAll: (cookiesToSet) => {
          cookiesToSet.forEach(({ name, value, options }) => {
            cookieStore.set(name, value, options);
          });
        },
      },
    }
  );
}
```

### Browser Client (React)

```typescript
// src/lib/supabase/client.ts
import { createBrowserClient } from "@supabase/ssr";
import type { Database } from "./database.types";

let client: ReturnType<typeof createBrowserClient<Database>> | null = null;

export function getBrowserClient() {
  if (client) return client;
  if (typeof window === "undefined") return null;

  client = createBrowserClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
  return client;
}
```

### Middleware Client

```typescript
// middleware.ts
import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";

export async function middleware(request: NextRequest) {
  const response = NextResponse.next({ request });
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll: () => request.cookies.getAll(),
        setAll: (cookiesToSet) => {
          cookiesToSet.forEach(({ name, value, options }) => {
            response.cookies.set(name, value, options);
          });
        },
      },
    }
  );

  const { data: { user } } = await supabase.auth.getUser();
  if (!user && request.nextUrl.pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }
  return response;
}
```

## Decision Framework

| Context | Client | Why |
|---------|--------|-----|
| Server Component | `createServerSupabase()` | Async cookies, server-only |
| Route Handler | `createServerSupabase()` | SSR context with cookies |
| Middleware | Inline `createServerClient` | Edge runtime, request/response cookies |
| Client Component | `getBrowserClient()` | Singleton, SSR-safe (null check) |
| Server Action | `createServerSupabase()` | Server context |

## Core Patterns

### Auth: Always Use getUser()

```typescript
// CORRECT: Validates JWT with auth server
const { data: { user } } = await supabase.auth.getUser();

// WRONG: Only reads from cookie, can be spoofed
const { data: { session } } = await supabase.auth.getSession();
```

### RLS: Use Subquery Wrapper

```sql
-- CORRECT: Subquery prevents multiple auth.uid() calls
create policy "Users view own data"
on public.items for select
to authenticated
using ((select auth.uid()) = user_id);

-- WRONG: Direct call, inefficient
using (auth.uid() = user_id);
```

### Realtime: Prefer Broadcast

```typescript
// Broadcast: Low latency, no DB polling
const channel = supabase.channel("room:123", { config: { private: true } });
channel.send({ type: "broadcast", event: "cursor", payload: { x, y } });

// postgres_changes: Higher latency, DB trigger required
channel.on("postgres_changes", { event: "*", schema: "public", table: "messages" }, handler);
```

### Storage: Signed URLs for Private Files

```typescript
// Public bucket: Direct URL
const { data } = supabase.storage.from("public-bucket").getPublicUrl("file.jpg");

// Private bucket: Time-limited signed URL
const { data } = await supabase.storage
  .from("private-bucket")
  .createSignedUrl("file.jpg", 3600); // 1 hour
```

## Zod v4 Integration

```typescript
import { z } from "zod";

// Use top-level string helpers (Zod v4)
const UserSchema = z.strictObject({
  id: z.uuid(),
  email: z.email(),
  created_at: z.iso.datetime(),
  metadata: z.looseObject({
    avatar_url: z.url().optional(),
  }),
});

// Unified error option (Zod v4)
const InsertSchema = z.strictObject({
  title: z.string().min(1, { error: "Title required" }),
  user_id: z.uuid({ error: "Invalid user ID" }),
});

// Parse Supabase response
const { data, error } = await supabase.from("items").select("*");
if (error) throw error;
const parsed = z.array(ItemSchema).parse(data);
```

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| `getSession()` for auth validation | Use `getUser()` - validates JWT |
| `auth.uid()` directly in RLS | Wrap in `(select auth.uid())` |
| Module-scope Supabase client | Create inside request handler |
| Service role key on client | Server-only, never expose |
| `postgres_changes` for chat | Use broadcast channels |
| Caching auth responses (`'use cache'`) | Keep auth routes dynamic |

## CLI Quick Reference

```bash
# Setup
supabase login
supabase link --project-ref <ref>

# Type generation
supabase gen types typescript --project-id <ref> --schema public > database.types.ts

# Migrations
supabase migration new <name>
supabase db push        # Push local migrations to remote
supabase db pull        # Pull remote schema to local
supabase db diff        # Show schema differences
supabase db reset       # Reset local database

# Edge Functions
supabase functions serve           # Local development
supabase functions deploy <name>   # Deploy to production
```

## Reference Documentation

Navigate to detailed guides based on task:

### Core Setup & Operations
- **[CLI Mastery](references/cli-mastery.md)**: Complete CLI workflow, type generation, migrations
- **[Database](references/database.md)**: Migrations, pgvector, functions, extensions
- **[Vercel Deployment](references/vercel-deployment.md)**: Integration, pooling, env vars

### Authentication & Security
- **[Auth SSR](references/auth-ssr.md)**: @supabase/ssr setup, PKCE, OAuth, middleware
- **[RLS Cookbook](references/rls-cookbook.md)**: Policy patterns, team access, storage RLS

### Data & Features
- **[Storage](references/storage.md)**: Buckets, uploads, transformations, signed URLs
- **[Realtime](references/realtime.md)**: Broadcast, presence, authorization
- **[AI Vectors](references/ai-vectors.md)**: pgvector, embeddings, semantic search
- **[Edge Functions](references/edge-functions.md)**: Deno runtime, deployment, CORS

## Templates

### Migration Template

```sql
-- supabase/migrations/YYYYMMDDHHmmss_description.sql

-- Enable required extensions
create extension if not exists "uuid-ossp";

-- Create table with RLS
create table public.items (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid not null references auth.users(id) on delete cascade,
  title text not null,
  created_at timestamptz not null default now()
);

-- Enable RLS (mandatory)
alter table public.items enable row level security;

-- Policies
create policy "Users view own items"
on public.items for select
to authenticated
using ((select auth.uid()) = user_id);

create policy "Users insert own items"
on public.items for insert
to authenticated
with check ((select auth.uid()) = user_id);

-- Indexes
create index items_user_id_idx on public.items(user_id);

comment on table public.items is 'User items with RLS';
```

### Edge Function Template

```typescript
// supabase/functions/my-function/index.ts
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const authHeader = req.headers.get("Authorization");
    const supabase = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_ANON_KEY")!,
      { global: { headers: { Authorization: authHeader! } } }
    );

    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
      return new Response(JSON.stringify({ error: "Unauthorized" }), {
        status: 401,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const body = await req.json();
    // Process request...

    return new Response(JSON.stringify({ success: true }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
```

### GitHub Actions Type Generation

```yaml
# .github/workflows/supabase-types.yml
name: Generate Supabase Types
on:
  push:
    paths: ["supabase/migrations/**"]
    branches: [main]

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: supabase/setup-cli@v1
      - run: |
          supabase gen types typescript \
            --project-id ${{ secrets.SUPABASE_PROJECT_REF }} \
            --schema public \
            > src/lib/supabase/database.types.ts
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}
      - uses: peter-evans/create-pull-request@v5
        with:
          commit-message: "chore: update database types"
          title: "Update Supabase Database Types"
          branch: update-db-types
```
