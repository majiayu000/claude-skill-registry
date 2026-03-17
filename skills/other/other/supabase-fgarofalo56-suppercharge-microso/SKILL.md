---
name: supabase
description: Build applications with Supabase for auth, real-time subscriptions, edge functions, and PostgreSQL with Row Level Security. Use when building full-stack apps with Supabase, implementing authentication, or adding real-time features.
---

# Supabase Skill

> Backend-as-a-Service with PostgreSQL, authentication, real-time subscriptions, storage, and edge functions.

## Quick Reference

| Feature            | Use Case                                           |
| ------------------ | -------------------------------------------------- |
| **Auth**           | User authentication with email, OAuth, magic links |
| **Database**       | PostgreSQL with Row Level Security (RLS)           |
| **Realtime**       | Live subscriptions to database changes             |
| **Storage**        | File uploads with access control                   |
| **Edge Functions** | Serverless TypeScript functions (Deno)             |

---

## Client Setup

### Installation

```bash
npm install @supabase/supabase-js
```

### Basic Client (TypeScript)

```typescript
// lib/supabase.ts
import { createClient } from "@supabase/supabase-js";
import type { Database } from "./database.types";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export const supabase = createClient<Database>(supabaseUrl, supabaseAnonKey);
```

### Next.js App Router Setup

```typescript
// lib/supabase/client.ts
import { createBrowserClient } from "@supabase/ssr";
import type { Database } from "@/types/database.types";

export function createClient() {
  return createBrowserClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  );
}
```

```typescript
// lib/supabase/server.ts
import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";
import type { Database } from "@/types/database.types";

export async function createClient() {
  const cookieStore = await cookies();

  return createServerClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options),
            );
          } catch {
            // Called from Server Component - ignore
          }
        },
      },
    },
  );
}
```

### React Context Provider

```typescript
// providers/supabase-provider.tsx
'use client';

import { createContext, useContext, useState } from 'react';
import { createClient } from '@/lib/supabase/client';
import type { SupabaseClient } from '@supabase/supabase-js';
import type { Database } from '@/types/database.types';

type SupabaseContext = {
  supabase: SupabaseClient<Database>;
};

const Context = createContext<SupabaseContext | undefined>(undefined);

export function SupabaseProvider({ children }: { children: React.ReactNode }) {
  const [supabase] = useState(() => createClient());

  return (
    <Context.Provider value={{ supabase }}>
      {children}
    </Context.Provider>
  );
}

export function useSupabase() {
  const context = useContext(Context);
  if (!context) {
    throw new Error('useSupabase must be used within SupabaseProvider');
  }
  return context;
}
```

---

## Authentication

### Email/Password Authentication

```typescript
// Sign up
const { data, error } = await supabase.auth.signUp({
  email: "user@example.com",
  password: "secure-password",
  options: {
    data: {
      full_name: "John Doe",
      avatar_url: "https://example.com/avatar.png",
    },
  },
});

// Sign in
const { data, error } = await supabase.auth.signInWithPassword({
  email: "user@example.com",
  password: "secure-password",
});

// Sign out
await supabase.auth.signOut();
```

### OAuth Providers

```typescript
// Google OAuth
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: "google",
  options: {
    redirectTo: `${window.location.origin}/auth/callback`,
    queryParams: {
      access_type: "offline",
      prompt: "consent",
    },
  },
});

// GitHub OAuth
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: "github",
  options: {
    redirectTo: `${window.location.origin}/auth/callback`,
    scopes: "read:user user:email",
  },
});
```

### Magic Link (Passwordless)

```typescript
// Send magic link
const { data, error } = await supabase.auth.signInWithOtp({
  email: "user@example.com",
  options: {
    emailRedirectTo: `${window.location.origin}/auth/callback`,
  },
});

// Phone OTP
const { data, error } = await supabase.auth.signInWithOtp({
  phone: "+1234567890",
});

// Verify OTP
const { data, error } = await supabase.auth.verifyOtp({
  phone: "+1234567890",
  token: "123456",
  type: "sms",
});
```

### Auth State Management

```typescript
// Get current session
const {
  data: { session },
} = await supabase.auth.getSession();

// Get current user
const {
  data: { user },
} = await supabase.auth.getUser();

// Listen to auth state changes
const {
  data: { subscription },
} = supabase.auth.onAuthStateChange((event, session) => {
  console.log("Auth event:", event);
  console.log("Session:", session);

  if (event === "SIGNED_IN") {
    // Handle sign in
  } else if (event === "SIGNED_OUT") {
    // Handle sign out
  } else if (event === "TOKEN_REFRESHED") {
    // Handle token refresh
  }
});

// Cleanup
subscription.unsubscribe();
```

### Auth Hook (React)

```typescript
// hooks/useAuth.ts
import { useEffect, useState } from "react";
import { useSupabase } from "@/providers/supabase-provider";
import type { User, Session } from "@supabase/supabase-js";

export function useAuth() {
  const { supabase } = useSupabase();
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setUser(session?.user ?? null);
      setLoading(false);
    });

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
      setUser(session?.user ?? null);
    });

    return () => subscription.unsubscribe();
  }, [supabase]);

  return { user, session, loading };
}
```

---

## Database Operations

### CRUD Operations

```typescript
// SELECT - Fetch all
const { data, error } = await supabase.from("posts").select("*");

// SELECT - With relations
const { data, error } = await supabase.from("posts").select(`
    id,
    title,
    content,
    created_at,
    author:users(id, name, avatar_url),
    comments(id, content, created_at)
  `);

// SELECT - With filters
const { data, error } = await supabase
  .from("posts")
  .select("*")
  .eq("status", "published")
  .gte("created_at", "2024-01-01")
  .order("created_at", { ascending: false })
  .limit(10);

// INSERT
const { data, error } = await supabase
  .from("posts")
  .insert({
    title: "New Post",
    content: "Post content here",
    user_id: user.id,
  })
  .select()
  .single();

// UPDATE
const { data, error } = await supabase
  .from("posts")
  .update({ title: "Updated Title" })
  .eq("id", postId)
  .select()
  .single();

// UPSERT
const { data, error } = await supabase
  .from("user_settings")
  .upsert({
    user_id: user.id,
    theme: "dark",
    notifications: true,
  })
  .select()
  .single();

// DELETE
const { error } = await supabase.from("posts").delete().eq("id", postId);
```

### Advanced Queries

```typescript
// Full-text search
const { data, error } = await supabase
  .from("posts")
  .select("*")
  .textSearch("title", "typescript react", {
    type: "websearch",
    config: "english",
  });

// Count
const { count, error } = await supabase
  .from("posts")
  .select("*", { count: "exact", head: true })
  .eq("user_id", userId);

// Pagination
const { data, error } = await supabase.from("posts").select("*").range(0, 9); // First 10 items

// OR conditions
const { data, error } = await supabase
  .from("posts")
  .select("*")
  .or("status.eq.published,status.eq.draft");

// Filter by JSON column
const { data, error } = await supabase
  .from("products")
  .select("*")
  .contains("metadata", { featured: true });
```

---

## Row Level Security (RLS)

### Enable RLS

```sql
-- Enable RLS on table
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Force RLS for table owner too
ALTER TABLE posts FORCE ROW LEVEL SECURITY;
```

### Common RLS Policies

```sql
-- Users can read all published posts
CREATE POLICY "Public posts are viewable by everyone"
ON posts FOR SELECT
USING (status = 'published');

-- Users can only read their own drafts
CREATE POLICY "Users can view own drafts"
ON posts FOR SELECT
USING (auth.uid() = user_id AND status = 'draft');

-- Users can insert their own posts
CREATE POLICY "Users can create own posts"
ON posts FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Users can update their own posts
CREATE POLICY "Users can update own posts"
ON posts FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Users can delete their own posts
CREATE POLICY "Users can delete own posts"
ON posts FOR DELETE
USING (auth.uid() = user_id);
```

### Role-Based Access

```sql
-- Create profiles table with role
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  role TEXT DEFAULT 'user' CHECK (role IN ('user', 'admin', 'moderator'))
);

-- Helper function to get user role
CREATE OR REPLACE FUNCTION get_user_role()
RETURNS TEXT AS $$
  SELECT role FROM profiles WHERE id = auth.uid();
$$ LANGUAGE SQL SECURITY DEFINER;

-- Admins can do everything
CREATE POLICY "Admins have full access"
ON posts FOR ALL
USING (get_user_role() = 'admin');

-- Moderators can update any post
CREATE POLICY "Moderators can update posts"
ON posts FOR UPDATE
USING (get_user_role() = 'moderator');
```

---

## Real-time Subscriptions

### Subscribe to Changes

```typescript
// Subscribe to all changes on a table
const channel = supabase
  .channel("posts-changes")
  .on(
    "postgres_changes",
    { event: "*", schema: "public", table: "posts" },
    (payload) => {
      console.log("Change received:", payload);
    },
  )
  .subscribe();

// Subscribe to INSERT only
const channel = supabase
  .channel("new-posts")
  .on(
    "postgres_changes",
    { event: "INSERT", schema: "public", table: "posts" },
    (payload) => {
      console.log("New post:", payload.new);
    },
  )
  .subscribe();

// Subscribe with filter
const channel = supabase
  .channel("user-posts")
  .on(
    "postgres_changes",
    {
      event: "*",
      schema: "public",
      table: "posts",
      filter: `user_id=eq.${userId}`,
    },
    (payload) => {
      console.log("User post changed:", payload);
    },
  )
  .subscribe();

// Cleanup
supabase.removeChannel(channel);
```

### React Hook for Real-time

```typescript
// hooks/useRealtimePosts.ts
import { useEffect, useState } from "react";
import { useSupabase } from "@/providers/supabase-provider";
import type { Post } from "@/types";

export function useRealtimePosts(userId?: string) {
  const { supabase } = useSupabase();
  const [posts, setPosts] = useState<Post[]>([]);

  useEffect(() => {
    // Initial fetch
    const fetchPosts = async () => {
      const query = supabase.from("posts").select("*");
      if (userId) query.eq("user_id", userId);
      const { data } = await query;
      if (data) setPosts(data);
    };

    fetchPosts();

    // Subscribe to changes
    const channel = supabase
      .channel("realtime-posts")
      .on(
        "postgres_changes",
        {
          event: "*",
          schema: "public",
          table: "posts",
          filter: userId ? `user_id=eq.${userId}` : undefined,
        },
        (payload) => {
          if (payload.eventType === "INSERT") {
            setPosts((prev) => [payload.new as Post, ...prev]);
          } else if (payload.eventType === "UPDATE") {
            setPosts((prev) =>
              prev.map((p) =>
                p.id === payload.new.id ? (payload.new as Post) : p,
              ),
            );
          } else if (payload.eventType === "DELETE") {
            setPosts((prev) => prev.filter((p) => p.id !== payload.old.id));
          }
        },
      )
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, [supabase, userId]);

  return posts;
}
```

---

## Storage

### Upload Files

```typescript
// Upload file
const { data, error } = await supabase.storage
  .from("avatars")
  .upload(`${userId}/avatar.png`, file, {
    cacheControl: "3600",
    upsert: true,
    contentType: "image/png",
  });

// Upload from form input
async function uploadFile(event: React.ChangeEvent<HTMLInputElement>) {
  const file = event.target.files?.[0];
  if (!file) return;

  const fileExt = file.name.split(".").pop();
  const fileName = `${Math.random()}.${fileExt}`;
  const filePath = `${userId}/${fileName}`;

  const { data, error } = await supabase.storage
    .from("uploads")
    .upload(filePath, file);

  if (error) throw error;
  return data.path;
}
```

### Get Public URL

```typescript
// Get public URL (for public buckets)
const { data } = supabase.storage
  .from("avatars")
  .getPublicUrl("user123/avatar.png");

console.log(data.publicUrl);

// Create signed URL (for private buckets)
const { data, error } = await supabase.storage
  .from("private-files")
  .createSignedUrl("document.pdf", 3600); // 1 hour expiry

console.log(data?.signedUrl);
```

### Storage Bucket Policies

```sql
-- Allow authenticated users to upload to their folder
CREATE POLICY "Users can upload to own folder"
ON storage.objects FOR INSERT
WITH CHECK (
  bucket_id = 'avatars' AND
  auth.uid()::text = (storage.foldername(name))[1]
);

-- Allow public read access
CREATE POLICY "Public read access"
ON storage.objects FOR SELECT
USING (bucket_id = 'public-assets');

-- Allow users to delete own files
CREATE POLICY "Users can delete own files"
ON storage.objects FOR DELETE
USING (
  bucket_id = 'uploads' AND
  auth.uid()::text = (storage.foldername(name))[1]
);
```

---

## Edge Functions

### Create Edge Function

```bash
# Initialize new function
supabase functions new my-function

# Deploy function
supabase functions deploy my-function
```

### Edge Function Template

```typescript
// supabase/functions/my-function/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type",
};

serve(async (req) => {
  // Handle CORS preflight
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    // Create Supabase client with user's JWT
    const supabase = createClient(
      Deno.env.get("SUPABASE_URL") ?? "",
      Deno.env.get("SUPABASE_ANON_KEY") ?? "",
      {
        global: {
          headers: { Authorization: req.headers.get("Authorization")! },
        },
      },
    );

    // Get authenticated user
    const {
      data: { user },
      error: authError,
    } = await supabase.auth.getUser();
    if (authError || !user) {
      return new Response(JSON.stringify({ error: "Unauthorized" }), {
        status: 401,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // Parse request body
    const { name } = await req.json();

    // Your logic here
    const result = { message: `Hello, ${name}!`, userId: user.id };

    return new Response(JSON.stringify(result), {
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

### Invoke Edge Function

```typescript
const { data, error } = await supabase.functions.invoke("my-function", {
  body: { name: "World" },
});
```

---

## Type Generation

### Generate Types from Schema

```bash
# Login to Supabase CLI
supabase login

# Generate types
supabase gen types typescript --project-id your-project-id > types/database.types.ts

# Or from local database
supabase gen types typescript --local > types/database.types.ts
```

### Using Generated Types

```typescript
// types/database.types.ts (generated)
export type Database = {
  public: {
    Tables: {
      posts: {
        Row: {
          id: string;
          title: string;
          content: string;
          user_id: string;
          created_at: string;
        };
        Insert: {
          id?: string;
          title: string;
          content: string;
          user_id: string;
          created_at?: string;
        };
        Update: {
          id?: string;
          title?: string;
          content?: string;
          user_id?: string;
          created_at?: string;
        };
      };
    };
  };
};

// Helper types
export type Post = Database["public"]["Tables"]["posts"]["Row"];
export type PostInsert = Database["public"]["Tables"]["posts"]["Insert"];
export type PostUpdate = Database["public"]["Tables"]["posts"]["Update"];
```

---

## Local Development

### Supabase CLI Setup

```bash
# Install CLI
npm install supabase --save-dev

# Initialize project
npx supabase init

# Start local Supabase
npx supabase start

# Stop local Supabase
npx supabase stop
```

### Database Migrations

```bash
# Create migration
npx supabase migration new create_posts_table

# Apply migrations locally
npx supabase db reset

# Push to remote
npx supabase db push
```

### Migration Example

```sql
-- supabase/migrations/20240101000000_create_posts_table.sql
CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  content TEXT,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'published')),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can CRUD own posts"
ON posts FOR ALL
USING (auth.uid() = user_id);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER posts_updated_at
  BEFORE UPDATE ON posts
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();
```

---

## Best Practices

### Security

| Practice                          | Implementation                             |
| --------------------------------- | ------------------------------------------ |
| Always enable RLS                 | `ALTER TABLE x ENABLE ROW LEVEL SECURITY`  |
| Use service role only server-side | Never expose `service_role` key            |
| Validate on server                | Edge Functions for sensitive operations    |
| Secure file uploads               | Storage policies with user folder patterns |

### Performance

| Practice                   | Implementation                                  |
| -------------------------- | ----------------------------------------------- |
| Select only needed columns | `.select('id, title')` not `.select('*')`       |
| Use indexes                | `CREATE INDEX idx_posts_user ON posts(user_id)` |
| Paginate large datasets    | `.range(0, 9)` or cursor pagination             |
| Cache with SWR/React Query | Reduce database calls                           |

### Error Handling

```typescript
async function safeQuery<T>(
  queryFn: () => Promise<{ data: T | null; error: Error | null }>,
): Promise<T> {
  const { data, error } = await queryFn();

  if (error) {
    console.error("Supabase error:", error);
    throw new Error(error.message);
  }

  if (!data) {
    throw new Error("No data returned");
  }

  return data;
}

// Usage
const post = await safeQuery(() =>
  supabase.from("posts").select("*").eq("id", id).single(),
);
```

---

## Environment Variables

```env
# .env.local
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key

# Server-side only (never expose)
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

---

## Common Patterns

### Middleware Auth Check (Next.js)

```typescript
// middleware.ts
import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({ request });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value),
          );
          response = NextResponse.next({ request });
          cookiesToSet.forEach(({ name, value, options }) =>
            response.cookies.set(name, value, options),
          );
        },
      },
    },
  );

  const {
    data: { user },
  } = await supabase.auth.getUser();

  // Protect routes
  if (!user && request.nextUrl.pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return response;
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
```
