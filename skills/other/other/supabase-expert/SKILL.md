---
name: supabase-expert
description: Expert guide for Supabase integration - database schemas, RLS policies, auth, Edge Functions, and real-time subscriptions. Use when working with Supabase backend features.
---

# Supabase Integration Expert Skill

## Overview

This skill helps you build secure, scalable Supabase integrations. Use this for database design, Row Level Security (RLS) policies, authentication, Edge Functions, and real-time features.

## Core Principles

### 1. Security First
- Always enable RLS on tables with user data
- Use service role key only in secure server contexts
- Use anon key for client-side operations
- Test policies thoroughly

### 2. Type Safety
- Generate TypeScript types from schema
- Use generated types in application
- Keep types in sync with schema changes

### 3. Performance
- Use indexes for frequently queried columns
- Implement pagination for large datasets
- Use select() to limit returned fields
- Cache when appropriate

## Database Schema Design

### Basic Table Creation

```sql
-- Create a table with standard fields
create table public.items (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null,
  user_id uuid references auth.users(id) on delete cascade not null,
  title text not null,
  description text,
  status text default 'draft' check (status in ('draft', 'published', 'archived'))
);

-- Create updated_at trigger
create or replace function public.handle_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger set_updated_at
  before update on public.items
  for each row
  execute function public.handle_updated_at();

-- Create index
create index items_user_id_idx on public.items(user_id);
create index items_status_idx on public.items(status);
```

### Foreign Keys & Relations

```sql
-- One-to-many relationship
create table public.comments (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp with time zone default now() not null,
  item_id uuid references public.items(id) on delete cascade not null,
  user_id uuid references auth.users(id) on delete cascade not null,
  content text not null
);

-- Many-to-many relationship
create table public.item_tags (
  item_id uuid references public.items(id) on delete cascade,
  tag_id uuid references public.tags(id) on delete cascade,
  primary key (item_id, tag_id)
);
```

## Row Level Security (RLS)

### Basic RLS Patterns

```sql
-- Enable RLS
alter table public.items enable row level security;

-- Users can read their own items
create policy "Users can read own items"
  on public.items for select
  using (auth.uid() = user_id);

-- Users can insert their own items
create policy "Users can insert own items"
  on public.items for insert
  with check (auth.uid() = user_id);

-- Users can update their own items
create policy "Users can update own items"
  on public.items for update
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

-- Users can delete their own items
create policy "Users can delete own items"
  on public.items for delete
  using (auth.uid() = user_id);
```

### Advanced RLS Patterns

```sql
-- Public read, authenticated write
create policy "Anyone can read published items"
  on public.items for select
  using (status = 'published');

create policy "Authenticated users can insert"
  on public.items for insert
  to authenticated
  with check (true);

-- Role-based access
create policy "Admins can do everything"
  on public.items for all
  using (
    exists (
      select 1 from public.user_roles
      where user_id = auth.uid()
      and role = 'admin'
    )
  );

-- Shared access
create policy "Users can read shared items"
  on public.items for select
  using (
    auth.uid() = user_id
    or exists (
      select 1 from public.item_shares
      where item_id = items.id
      and shared_with = auth.uid()
    )
  );
```

### Anonymous/Guest Access

```sql
-- Allow anonymous reads
create policy "Anonymous can read public content"
  on public.items for select
  to anon
  using (status = 'published');

-- Allow anonymous inserts (for guest mode)
create policy "Anonymous can create items"
  on public.items for insert
  to anon
  with check (true);
```

## Client Integration

### Setup Client (Next.js)

```typescript
// lib/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}

// lib/supabase/server.ts
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export function createServerClient() {
  const cookieStore = cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value
        },
      },
    }
  )
}
```

### CRUD Operations

```typescript
// Query data
const { data, error } = await supabase
  .from('items')
  .select('*')
  .eq('status', 'published')
  .order('created_at', { ascending: false })
  .limit(10)

// Insert data
const { data, error } = await supabase
  .from('items')
  .insert({ title: 'New Item', user_id: userId })
  .select()
  .single()

// Update data
const { data, error } = await supabase
  .from('items')
  .update({ title: 'Updated Title' })
  .eq('id', itemId)
  .select()
  .single()

// Delete data
const { error } = await supabase
  .from('items')
  .delete()
  .eq('id', itemId)

// Complex joins
const { data, error } = await supabase
  .from('items')
  .select(`
    *,
    comments (
      id,
      content,
      user:user_id (
        email
      )
    )
  `)
  .eq('user_id', userId)
```

### Real-time Subscriptions

```typescript
// Subscribe to changes
const channel = supabase
  .channel('items-changes')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'items',
      filter: `user_id=eq.${userId}`,
    },
    (payload) => {
      console.log('Change received!', payload)
      // Update local state
    }
  )
  .subscribe()

// Cleanup
channel.unsubscribe()
```

## Authentication

### Email/Password Auth

```typescript
// Sign up
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'password123',
  options: {
    data: {
      display_name: 'User Name',
    },
  },
})

// Sign in
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'password123',
})

// Sign out
const { error } = await supabase.auth.signOut()

// Get current user
const { data: { user } } = await supabase.auth.getUser()
```

### OAuth Providers

```typescript
// Google OAuth
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: `${window.location.origin}/auth/callback`,
  },
})

// Handle callback
// app/auth/callback/route.ts
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const code = searchParams.get('code')

  if (code) {
    const supabase = createServerClient()
    await supabase.auth.exchangeCodeForSession(code)
  }

  return NextResponse.redirect(new URL('/dashboard', request.url))
}
```

### Auth Middleware

```typescript
// middleware.ts
import { createServerClient } from '@supabase/ssr'
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  const response = NextResponse.next()

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value
        },
        set(name: string, value: string, options: any) {
          response.cookies.set(name, value, options)
        },
        remove(name: string, options: any) {
          response.cookies.set(name, '', { ...options, maxAge: 0 })
        },
      },
    }
  )

  const { data: { user } } = await supabase.auth.getUser()

  // Redirect to login if not authenticated
  if (!user && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return response
}

export const config = {
  matcher: ['/dashboard/:path*'],
}
```

## Edge Functions

### Basic Edge Function

```typescript
// supabase/functions/hello/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  try {
    // Get Supabase client
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      {
        auth: {
          autoRefreshToken: false,
          persistSession: false,
        },
      }
    )

    // Get user from auth header
    const authHeader = req.headers.get('Authorization')
    const token = authHeader?.replace('Bearer ', '')
    const { data: { user } } = await supabase.auth.getUser(token)

    if (!user) {
      return new Response(
        JSON.stringify({ error: 'Unauthorized' }),
        { status: 401, headers: { 'Content-Type': 'application/json' } }
      )
    }

    // Your logic here
    const { data, error } = await supabase
      .from('items')
      .select('*')
      .eq('user_id', user.id)

    return new Response(
      JSON.stringify({ data }),
      { headers: { 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    )
  }
})
```

## Type Generation

```bash
# Generate TypeScript types
npx supabase gen types typescript --project-id your-project-id > types/supabase.ts

# Use in code
import { Database } from '@/types/supabase'

type Item = Database['public']['Tables']['items']['Row']
type ItemInsert = Database['public']['Tables']['items']['Insert']
type ItemUpdate = Database['public']['Tables']['items']['Update']
```

## Common Patterns

### Soft Deletes

```sql
alter table public.items add column deleted_at timestamp with time zone;

create policy "Users cannot see deleted items"
  on public.items for select
  using (deleted_at is null);

-- Soft delete function
create or replace function soft_delete_item(item_id uuid)
returns void as $$
begin
  update public.items
  set deleted_at = now()
  where id = item_id;
end;
$$ language plpgsql security definer;
```

### Audit Logs

```sql
create table public.audit_logs (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp with time zone default now() not null,
  user_id uuid references auth.users(id),
  table_name text not null,
  record_id uuid not null,
  action text not null,
  changes jsonb
);

-- Trigger function
create or replace function public.audit_trigger()
returns trigger as $$
begin
  insert into public.audit_logs (user_id, table_name, record_id, action, changes)
  values (
    auth.uid(),
    TG_TABLE_NAME,
    NEW.id,
    TG_OP,
    to_jsonb(NEW) - to_jsonb(OLD)
  );
  return NEW;
end;
$$ language plpgsql security definer;
```

## Troubleshooting

### Common Issues

1. **401 Errors**: Check RLS policies, ensure user is authenticated
2. **403 Errors**: RLS policy blocking operation
3. **Row not found**: Policy may be filtering it out
4. **Connection issues**: Check URL and API keys
5. **Type mismatches**: Regenerate types after schema changes

### Debugging RLS

```sql
-- Test as specific user
set request.jwt.claims = '{"sub": "user-uuid-here"}';

-- Check what policies apply
select * from pg_policies where tablename = 'items';

-- Disable RLS temporarily (for testing only!)
alter table public.items disable row level security;
```

## Best Practices Checklist

- [ ] Enable RLS on all tables with user data
- [ ] Create indexes for foreign keys and frequently queried columns
- [ ] Use UUID for primary keys
- [ ] Add created_at and updated_at timestamps
- [ ] Implement soft deletes for important data
- [ ] Use check constraints for enum-like fields
- [ ] Generate and use TypeScript types
- [ ] Test RLS policies thoroughly
- [ ] Use service role key only server-side
- [ ] Implement proper error handling
- [ ] Add audit logs for sensitive operations
- [ ] Use transactions for multi-step operations

## When to Use This Skill

Invoke this skill when:
- Designing database schemas
- Creating or debugging RLS policies
- Setting up authentication
- Building Edge Functions
- Implementing real-time features
- Troubleshooting Supabase issues
- Optimizing database queries
- Setting up type generation
