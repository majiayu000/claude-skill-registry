---
name: supabase-setup
slug: supabase-setup
version: 1.0.0
category: core
description: Configure Supabase database, authentication, storage, and realtime features via MCP
triggers:
  - pattern: "supabase|auth|storage|bucket|realtime"
    confidence: 0.7
    examples:
      - "setup supabase for my app"
      - "configure supabase auth"
      - "create storage bucket"
      - "enable realtime subscriptions"
      - "setup supabase database"
mcp_dependencies:
  - server: supabase
    required: true
    capabilities:
      - "query"
      - "schema"
      - "auth"
      - "storage"
---

# Supabase Setup Skill

Automatically configure Supabase database, authentication, storage buckets, and realtime features using the Supabase MCP server. This skill transforms natural language Supabase requirements into complete backend infrastructure with proper security policies.

## Overview

This skill configures:
- **Database Tables** via SQL migrations
- **Row Level Security (RLS)** policies
- **Authentication Providers** (OAuth, Email, etc.)
- **Storage Buckets** for file uploads
- **Realtime Subscriptions** for live data
- **Client/Server Integration** code for Next.js

## When to Use This Skill

Activate this skill when the user requests:
- Supabase project setup
- Database table creation in Supabase
- Authentication configuration
- Storage bucket creation
- Realtime feature enablement
- RLS policy setup
- Client integration code

## Key Features

### 1. Database Table Creation

Generates SQL migrations and executes via MCP:

```sql
-- Create users table
CREATE TABLE users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email text UNIQUE NOT NULL,
  name text NOT NULL,
  avatar_url text,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Create policy: Users can view their own data
CREATE POLICY "Users can view own data"
  ON users
  FOR SELECT
  USING (auth.uid() = id);

-- Create policy: Users can update their own data
CREATE POLICY "Users can update own data"
  ON users
  FOR UPDATE
  USING (auth.uid() = id);
```

### 2. Row Level Security (RLS)

Automatically generates security policies:

```sql
-- Public read access
CREATE POLICY "Public posts are viewable by everyone"
  ON posts
  FOR SELECT
  USING (published = true);

-- Authenticated users can create
CREATE POLICY "Authenticated users can create posts"
  ON posts
  FOR INSERT
  WITH CHECK (auth.role() = 'authenticated');

-- Users can update their own posts
CREATE POLICY "Users can update own posts"
  ON posts
  FOR UPDATE
  USING (auth.uid() = author_id);

-- Users can delete their own posts
CREATE POLICY "Users can delete own posts"
  ON posts
  FOR DELETE
  USING (auth.uid() = author_id);
```

### 3. Authentication Configuration

Configures OAuth providers and generates integration code:

```typescript
// lib/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}

// Sign in with Google
export async function signInWithGoogle() {
  const supabase = createClient()
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: {
      redirectTo: `${location.origin}/auth/callback`,
    },
  })
  return { data, error }
}

// Sign out
export async function signOut() {
  const supabase = createClient()
  const { error } = await supabase.auth.signOut()
  return { error }
}

// Get current session
export async function getSession() {
  const supabase = createClient()
  const { data: { session } } = await supabase.auth.getSession()
  return session
}
```

Server-side authentication:

```typescript
// lib/supabase/server.ts
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) => {
              cookieStore.set(name, value, options)
            })
          } catch (error) {
            // Handle cookie setting errors
          }
        },
      },
    }
  )
}

export async function getUser() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  return user
}
```

Auth callback route:

```typescript
// app/auth/callback/route.ts
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'
import { cookies } from 'next/headers'

export async function GET(request: Request) {
  const requestUrl = new URL(request.url)
  const code = requestUrl.searchParams.get('code')

  if (code) {
    const supabase = await createClient()
    await supabase.auth.exchangeCodeForSession(code)
  }

  return NextResponse.redirect(requestUrl.origin)
}
```

### 4. Storage Buckets

Creates storage buckets for file uploads:

```sql
-- Create storage bucket via MCP
INSERT INTO storage.buckets (id, name, public)
VALUES ('avatars', 'avatars', true);

-- Set storage policies
CREATE POLICY "Avatar images are publicly accessible"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'avatars');

CREATE POLICY "Authenticated users can upload avatars"
  ON storage.objects FOR INSERT
  WITH CHECK (
    bucket_id = 'avatars' AND
    auth.role() = 'authenticated'
  );
```

Upload helper functions:

```typescript
// lib/supabase/storage.ts
import { createClient } from './client'

export async function uploadFile(
  bucket: string,
  path: string,
  file: File
) {
  const supabase = createClient()

  const { data, error } = await supabase.storage
    .from(bucket)
    .upload(path, file, {
      cacheControl: '3600',
      upsert: false,
    })

  if (error) throw error
  return data
}

export async function getPublicUrl(bucket: string, path: string) {
  const supabase = createClient()

  const { data } = supabase.storage
    .from(bucket)
    .getPublicUrl(path)

  return data.publicUrl
}

export async function deleteFile(bucket: string, path: string) {
  const supabase = createClient()

  const { error } = await supabase.storage
    .from(bucket)
    .remove([path])

  if (error) throw error
}
```

### 5. Realtime Subscriptions

Enables realtime features for tables:

```sql
-- Enable realtime for table via MCP
ALTER PUBLICATION supabase_realtime ADD TABLE posts;
```

Subscription client code:

```typescript
// lib/supabase/realtime.ts
import { createClient } from './client'
import { useEffect, useState } from 'react'

export function useRealtimeSubscription<T>(
  table: string,
  filter?: string
) {
  const [data, setData] = useState<T[]>([])
  const supabase = createClient()

  useEffect(() => {
    const channel = supabase
      .channel(`${table}_changes`)
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table,
          filter,
        },
        (payload) => {
          if (payload.eventType === 'INSERT') {
            setData((prev) => [...prev, payload.new as T])
          } else if (payload.eventType === 'UPDATE') {
            setData((prev) =>
              prev.map((item: any) =>
                item.id === payload.new.id ? payload.new : item
              )
            )
          } else if (payload.eventType === 'DELETE') {
            setData((prev) =>
              prev.filter((item: any) => item.id !== payload.old.id)
            )
          }
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [table, filter])

  return data
}

// Usage in component
export function PostsList() {
  const posts = useRealtimeSubscription('posts', 'published=eq.true')

  return (
    <div>
      {posts.map(post => (
        <div key={post.id}>{post.title}</div>
      ))}
    </div>
  )
}
```

## Execution Steps

When this skill is activated:

1. **Parse Supabase Requirements**
   - Extract table definitions
   - Identify auth providers needed
   - Detect storage requirements
   - Determine realtime needs

2. **Generate Database Schema**
   - Create table definitions
   - Add foreign key constraints
   - Generate indexes
   - Enable RLS on tables

3. **Create Security Policies**
   - Generate RLS policies for each table
   - Add authentication-based policies
   - Create public access policies where needed
   - Add storage bucket policies

4. **Configure Authentication**
   - Set up OAuth providers
   - Generate client auth code
   - Generate server auth code
   - Create auth callback routes

5. **Setup Storage Buckets**
   - Create buckets via MCP
   - Configure public/private access
   - Add file size limits
   - Set allowed MIME types
   - Generate upload/download helpers

6. **Enable Realtime Features**
   - Add tables to realtime publication
   - Generate subscription hooks
   - Create realtime client utilities

7. **Generate Integration Code**
   - Create Supabase client utilities
   - Generate TypeScript types
   - Add environment variable setup
   - Create helper functions

8. **Write Output Files**
   - `lib/supabase/client.ts` - Browser client
   - `lib/supabase/server.ts` - Server client
   - `lib/supabase/storage.ts` - Storage utilities
   - `lib/supabase/realtime.ts` - Realtime hooks
   - `app/auth/callback/route.ts` - Auth callback
   - `migrations/{timestamp}_setup.sql` - Database migration
   - `.env.local.example` - Environment variables template

## Usage Examples

### Example 1: Basic Setup

**User Prompt:**
"Setup Supabase with users and posts tables"

**Generated Output:**
- SQL migrations for tables
- RLS policies
- Client/server integration code
- TypeScript types

### Example 2: Auth Configuration

**User Prompt:**
"Configure Supabase auth with Google and GitHub OAuth"

**Generated Output:**
- Auth provider configuration
- Sign in/out functions
- Auth callback route
- Session management utilities

### Example 3: Storage Setup

**User Prompt:**
"Create a storage bucket for user avatars with 5MB limit"

**Generated Output:**
- Avatar bucket creation
- Storage policies
- Upload/delete helper functions
- Public URL getter

### Example 4: Realtime Features

**User Prompt:**
"Enable realtime subscriptions for chat messages"

**Generated Output:**
- Realtime publication setup
- React hooks for subscriptions
- Real-time event handlers

## Security Best Practices

### RLS Policies

Always enable RLS on tables:
```sql
ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;
```

Common policy patterns:
- **Public read:** `USING (published = true)`
- **Owner access:** `USING (auth.uid() = user_id)`
- **Authenticated only:** `WITH CHECK (auth.role() = 'authenticated')`
- **Admin only:** `USING (auth.jwt() ->> 'role' = 'admin')`

### Storage Security

- Use authenticated policies for uploads
- Validate file types and sizes
- Use signed URLs for private content
- Implement virus scanning for uploads

### Authentication

- Always validate sessions server-side
- Use secure, httpOnly cookies
- Implement CSRF protection
- Add rate limiting on auth endpoints

## MCP Integration

This skill **requires** the Supabase MCP server for:

- **Schema Operations:** Create/alter tables, indexes
- **Data Operations:** Insert/update/delete via SQL
- **Auth Configuration:** Setup OAuth providers
- **Storage Management:** Create/configure buckets
- **Realtime Setup:** Enable publication for tables

MCP commands used:
- `execute_sql` - Run SQL migrations
- `create_table` - Create database tables
- `create_policy` - Add RLS policies
- `create_bucket` - Setup storage buckets
- `enable_realtime` - Enable realtime for tables

## Environment Variables

Required `.env.local` variables:

```bash
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# OAuth Providers (if used)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

## TypeScript Types

Auto-generated from database schema:

```typescript
// lib/supabase/types.ts
export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export interface Database {
  public: {
    Tables: {
      users: {
        Row: {
          id: string
          email: string
          name: string
          avatar_url: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          email: string
          name: string
          avatar_url?: string | null
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          email?: string
          name?: string
          avatar_url?: string | null
          created_at?: string
          updated_at?: string
        }
      }
    }
  }
}
```

## Limitations

- Requires Supabase project to be created
- Requires MCP server connection
- PostgreSQL database only
- Environment variables must be configured manually

## Future Enhancements

- Automatic database type generation
- Edge Functions integration
- Database backup configuration
- Performance monitoring setup
- Database migration rollback
- Multi-environment support
- Automated testing for RLS policies

---

**Skill Version:** 1.0.0
**Last Updated:** 2026-01-04
**Maintainer:** Turbocat Agent System
