---
name: "supabase-nextjs-integration"
description: "Use this skill whenever the user wants to set up, refactor, or optimize Supabase usage in a Next.js (App Router) + TypeScript project, including auth, database, storage, RLS-safe patterns, edge functions, and secure client/server integration."
---

# Supabase + Next.js App Router Integration Skill

## Purpose

You are a specialized assistant for **integrating Supabase with Next.js App Router** in a secure,
idiomatic, and scalable way.

Use this skill to:

- Set up Supabase in a **Next.js App Router + TypeScript** project
- Configure **environment variables & secrets** safely
- Create **Supabase clients** for:
  - Server Components
  - Route Handlers
  - Server Actions
  - Client Components (ONLY with anon keys)
- Implement **Auth** flows (email/password, OAuth, magic links, password reset)
- Use **Row Level Security (RLS)** safely and correctly
- Integrate **database**, **storage**, and **edge functions**
- Choose between **Edge runtime** and **Node runtime** for Supabase usage
- Structure the project so all Supabase usage is consistent and easily testable

Do **not** use this skill for non-Next.js projects or when Supabase is not part of the stack.

If `CLAUDE.md` exists, follow its conventions for env vars, directory structure, and security rules
(e.g. “never use service_role in app”, “always go through specific route handlers”).

---

## When To Apply This Skill

Trigger this skill when the user asks for any of the following (or similar):

- “Set up Supabase in this Next.js app.”
- “Use Supabase auth (login, signup, magic links) in my Next.js frontend.”
- “Wire RLS-protected tables to my Next.js pages/components.”
- “Securely call Supabase from server actions / route handlers.”
- “Use Edge Functions from my Next.js app.”
- “Fix Supabase auth/session handling in App Router.”
- “Use Supabase for database + storage + auth in my Next app.”

Avoid applying this skill when:

- The question is purely about UI & components with no data/auth.
- The project does not use or plan to use Supabase.

---

## High-Level Architecture

When integrating Supabase with Next.js App Router, follow this architecture:

- **Environment variables**
  - `NEXT_PUBLIC_SUPABASE_URL`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
  - `SUPABASE_SERVICE_ROLE_KEY` (server-only, NEVER sent to client)
  - Any other Supabase-related secrets (e.g. JWT secret, webhook secrets)

- **Supabase client modules** (example paths):
  - `src/lib/supabase/client.ts` → **browser/client-side** usage (anon key)
  - `src/lib/supabase/server.ts` → **server-side** usage with cookies & auth helpers
  - `src/lib/supabase/admin.ts` → **server-only admin** usage (service_role, if really needed)

- **Auth integration**
  - Use Supabase auth for sessions and user identity.
  - Implement auth-aware **Server Components**, **layouts**, and **middleware** as needed.
  - Never expose `service_role` to the browser; use row-level security (RLS) to protect data.

- **Edge vs Node runtime**
  - Use **Edge runtime** (`runtime = "edge"`) when you want low-latency Supabase access and your
    libraries are Edge-compatible.
  - Use **Node runtime** (`runtime = "nodejs"`) for heavier operations or incompatible libs.

- **Edge Functions**
  - Implement Supabase Edge Functions for server-side logic that should run close to the data
    and call them from your Next.js app via `fetch`.

---

## Environment & Secrets

Always configure Supabase secrets like this:

```env
# .env.local (never committed)
NEXT_PUBLIC_SUPABASE_URL="https://YOUR_PROJECT_ID.supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="public-anon-key"
SUPABASE_SERVICE_ROLE_KEY="service-role-key" # SERVER ONLY – never exposed client-side
```

Guidelines:

- `NEXT_PUBLIC_*` env vars are visible to the browser; only use **public/anon keys** there.
- `SUPABASE_SERVICE_ROLE_KEY` must **never** be used in code that can run on the client.
- When in doubt, use **server components and route handlers** to keep secrets safe.

---

## Supabase Client Setup

### 1. Client-side Supabase (browser / anon-only)

Use this for strictly client-side features that need Supabase and are safe with anon keys
(e.g. some public reads, optional real-time features).

```ts
// src/lib/supabase/client.ts
import { createBrowserClient } from "@supabase/ssr";

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
```

Usage in client components:

```tsx
"use client";

import { useEffect, useState } from "react";
import { createClient } from "@/lib/supabase/client";

export function ProfileWidget() {
  const [profile, setProfile] = useState<any>(null);

  useEffect(() => {
    const supabase = createClient();

    supabase
      .from("profiles")
      .select("*")
      .limit(1)
      .then(({ data }) => setProfile(data?.[0] ?? null));
  }, []);

  // render...
}
```

Use this skill to **warn when something should really be fetched server-side instead**.

### 2. Server-side Supabase (App Router aware)

Use this in **Server Components**, **Route Handlers**, and **Server Actions** when you need
session-aware Supabase access.

```ts
// src/lib/supabase/server.ts
import { cookies } from "next/headers";
import { createServerClient } from "@supabase/ssr";

export function createServerSupabaseClient() {
  const cookieStore = cookies();

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value;
        },
      },
    }
  );
}
```

Usage in a server component:

```tsx
// app/dashboard/page.tsx
import { createServerSupabaseClient } from "@/lib/supabase/server";

export default async function DashboardPage() {
  const supabase = createServerSupabaseClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    // handle redirect to login, etc.
  }

  const { data: items } = await supabase.from("items").select("*").order("created_at", { ascending: false });

  return <DashboardView user={user} items={items ?? []} />;
}
```

### 3. Admin / Service-role Supabase (server-only)

Use **sparingly**, only for back-office or system tasks that require bypassing RLS.

```ts
// src/lib/supabase/admin.ts
import { createClient } from "@supabase/supabase-js";

export const adminSupabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!,
  {
    auth: { persistSession: false },
  }
);
```

**Never import `adminSupabase` in client components.**

---

## Auth Flows (Next.js + Supabase)

### Sign Up / Sign In (Server Actions)

Use server actions or route handlers to handle auth operations:

```ts
// app/(auth)/actions.ts
"use server";

import { redirect } from "next/navigation";
import { createServerSupabaseClient } from "@/lib/supabase/server";

export async function signInWithEmail(formData: FormData) {
  const email = String(formData.get("email") ?? "");
  const password = String(formData.get("password") ?? "");

  const supabase = createServerSupabaseClient();
  const { error } = await supabase.auth.signInWithPassword({ email, password });

  if (error) {
    // handle error (return structured error)
    return { error: error.message };
  }

  redirect("/dashboard");
}
```

Use this skill to:

- Keep auth flows entirely server-side where possible.
- Avoid exposing unnecessary auth logic to the client.
- Ensure proper redirects and error handling.

### Magic Links / OAuth

- Use Supabase auth methods for magic links and OAuth providers.
- Handle redirect URLs and `next` parameters carefully, avoiding open redirects.

---

## RLS (Row Level Security) Best Practices

- Enable RLS on all tables that store user data.
- Define policies based on Supabase's `auth.uid()`:

  Example policy pattern:

  ```sql
  create policy "Users can see their own rows"
  on profiles
  for select using (
    auth.uid() = user_id
  );
  ```

Use this skill to:

- Encourage RLS for all user-related tables.
- Avoid relying on `service_role` for regular app operations.
- Ensure queries are written with RLS in mind (e.g. filter by `user_id` instead of trusting client input).

---

## Edge Functions

Supabase Edge Functions are great for:

- High-performance APIs close to your database
- Work that should remain within Supabase infrastructure

Use this skill to:

- Suggest separation of complex logic into Edge Functions.
- Show patterns for calling Edge Functions from Next.js via `fetch`:

  ```ts
  const res = await fetch("https://YOUR_PROJECT_ID.supabase.co/functions/v1/my-fn", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`, // if needed
    },
    body: JSON.stringify(payload),
  });
  ```

- Keep security & auth in mind when calling these functions.

---

## Step-by-Step Workflow

When this skill is active, follow this workflow:

### 1. Detect current state

- Check if Supabase is already set up:
  - Are env vars present?
  - Are `@supabase/*` dependencies installed?
  - Are there any existing Supabase client helper files?

- If not present → propose a clean setup with minimal, well-structured helpers.

### 2. Define goals

- Ask (or infer) what the user wants:
  - Auth? Database? Storage? Edge Functions?
  - RLS on which tables?
  - Public vs authenticated routes?

### 3. Set up or refactor client modules

- Create or refine:
  - `lib/supabase/client.ts`
  - `lib/supabase/server.ts`
  - `lib/supabase/admin.ts` (if needed)
- Ensure no server-only keys are referenced in browser code.

### 4. Implement auth flows

- For login, signup, logout, password reset, etc.:
  - Use server actions or route handlers.
  - Maintain a clean separation between UI and auth logic.
  - Ensure redirects work correctly in App Router.

### 5. Wire Supabase into routes/layouts

- Use server components for auth-aware pages and layouts.
- Use RLS-friendly queries (no trusting user IDs from the client).
- Use Suspense/loading states where relevant.

### 6. Integrate storage & other features

- Provide helpers for uploading/downloading from Supabase storage.
- Ensure signed URL usage when appropriate.

### 7. Use Edge Functions when appropriate

- Offload complex or latency-sensitive logic.
- Ensure correct authentication from Next.js to Edge Functions.

### 8. Summarize and document

- After setting up or refactoring Supabase integration, summarize:
  - Where Supabase helpers live.
  - How auth flows work.
  - How RLS and security are enforced.
  - How to add new tables/queries safely.

- Optionally update `README.md` or create `SUPABASE.md` documenting all of the above.

---

## Examples of Prompts That Should Use This Skill

- “Set up Supabase auth and secure dashboard routes in this Next.js app.”
- “Use Supabase with RLS to store user-specific todos and show them in `/dashboard`.”
- “Add a profile page reading from the `profiles` table with proper auth.”
- “Move this client-side Supabase usage into server components and server actions.”
- “Integrate Supabase Edge Functions for heavy data processing and call them from Next.js.”
- “Refactor our Supabase usage to avoid leaking the service_role key and rely on RLS instead.”

For these tasks, rely on this skill to provide **secure, idiomatic Supabase + Next.js App Router integration**, and collaborate with other skills (data fetching, performance, testing, routing) as needed.
