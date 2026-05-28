# Supabase Backend Platform Skill

---
progressive_disclosure:
  entry_point:
    summary: "Open-source Firebase alternative with Postgres, authentication, storage, and realtime"
    when_to_use:
      - "When building full-stack applications"
      - "When auth, database, and storage are required"
      - "When realtime subscriptions are needed"
      - "When using Next.js, React, or Vue"
    quick_start:
      - "Create project on Supabase console"
      - "npm install @supabase/supabase-js"
      - "Initialize client with URL and anon key"
      - "Use auth, database, storage, realtime"
  token_estimate:
    entry: 80-95
    full: 5000-6000
---

## Supabase Fundamentals

### What is Supabase?
Open-source Firebase alternative built on:
- **Postgres Database**: Full SQL database with PostgREST API
- **Authentication**: Built-in auth with multiple providers
- **Storage**: File storage with image transformations
- **Realtime**: WebSocket subscriptions to database changes
- **Edge Functions**: Serverless functions on Deno runtime
- **Row Level Security**: Postgres RLS for data access control

### Project Setup
```bash
# Install Supabase client
npm install @supabase/supabase-js

# Install CLI for local development
npm install -D supabase

# TypeScript types
npm install -D @supabase/supabase-js
```

### Client Initialization
```typescript
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// With TypeScript types
import { Database } from '@/types/supabase'

export const supabase = createClient<Database>(
  supabaseUrl,
  supabaseAnonKey
)
```

## Database Operations

### PostgREST API Basics
Supabase auto-generates REST API from Postgres schema:

```typescript
// SELECT * FROM posts
const { data, error } = await supabase
  .from('posts')
  .select('*')

// SELECT with filters
const { data } = await supabase
  .from('posts')
  .select('*')
  .eq('status', 'published')
  .order('created_at', { ascending: false })
  .limit(10)

// SELECT with joins
const { data } = await supabase
  .from('posts')
  .select(`
    *,
    author:profiles(name, avatar),
    comments(count)
  `)

// INSERT
const { data, error } = await supabase
  .from('posts')
  .insert({ title: 'Hello', content: 'World' })
  .select()
  .single()

// UPDATE
const { data } = await supabase
  .from('posts')
  .update({ status: 'published' })
  .eq('id', postId)
  .select()

// DELETE
const { error } = await supabase
  .from('posts')
  .delete()
  .eq('id', postId)

// UPSERT
const { data } = await supabase
  .from('posts')
  .upsert({ id: 1, title: 'Updated' })
  .select()
```

### Advanced Queries
```typescript
// Full-text search
const { data } = await supabase
  .from('posts')
  .select('*')
  .textSearch('title', 'postgresql', {
    type: 'websearch',
    config: 'english'
  })

// Range queries
const { data } = await supabase
  .from('posts')
  .select('*')
  .gte('created_at', '2024-01-01')
  .lte('created_at', '2024-12-31')

// Array contains
const { data } = await supabase
  .from('posts')
  .select('*')
  .contains('tags', ['postgres', 'supabase'])

// JSON operations
const { data } = await supabase
  .from('users')
  .select('*')
  .eq('metadata->theme', 'dark')

// Count without data
const { count } = await supabase
  .from('posts')
  .select('*', { count: 'exact', head: true })

// Pagination
const pageSize = 10
const page = 2
const { data } = await supabase
  .from('posts')
  .select('*')
  .range(page * pageSize, (page + 1) * pageSize - 1)
```

### Database Functions and RPC
```typescript
// Call Postgres function
const { data, error } = await supabase
  .rpc('get_trending_posts', {
    days: 7,
    min_score: 10
  })

// Example function in SQL
/*
CREATE OR REPLACE FUNCTION get_trending_posts(
  days INTEGER,
  min_score INTEGER
)
RETURNS TABLE (
  id UUID,
  title TEXT,
  score INTEGER
) AS $$
BEGIN
  RETURN QUERY
  SELECT p.id, p.title, COUNT(v.id)::INTEGER as score
  FROM posts p
  LEFT JOIN votes v ON p.id = v.post_id
  WHERE p.created_at > NOW() - INTERVAL '1 day' * days
  GROUP BY p.id
  HAVING COUNT(v.id) >= min_score
  ORDER BY score DESC;
END;
$$ LANGUAGE plpgsql;
*/
```

## Authentication

### Email/Password Authentication
```typescript
// Sign up
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'secure-password',
  options: {
    data: {
      name: 'John Doe',
      avatar_url: 'https://...'
    }
  }
})

// Sign in
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'secure-password'
})

// Sign out
const { error } = await supabase.auth.signOut()

// Get current user
const { data: { user } } = await supabase.auth.getUser()

// Get session
const { data: { session } } = await supabase.auth.getSession()
```

### OAuth Providers
```typescript
// Sign in with OAuth
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'github',
  options: {
    redirectTo: 'http://localhost:3000/auth/callback',
    scopes: 'repo user'
  }
})

// Available providers
// github, google, gitlab, bitbucket, azure, discord, facebook,
// linkedin, notion, slack, spotify, twitch, twitter, apple
```

### Magic Links
```typescript
// Send magic link
const { data, error } = await supabase.auth.signInWithOtp({
  email: 'user@example.com',
  options: {
    emailRedirectTo: 'http://localhost:3000/auth/callback'
  }
})

// Verify OTP
const { data, error } = await supabase.auth.verifyOtp({
  email: 'user@example.com',
  token: '123456',
  type: 'email'
})
```

### Phone Authentication
```typescript
// Sign in with phone
const { data, error } = await supabase.auth.signInWithOtp({
  phone: '+1234567890'
})

// Verify phone OTP
const { data, error } = await supabase.auth.verifyOtp({
  phone: '+1234567890',
  token: '123456',
  type: 'sms'
})
```

### Auth State Management
```typescript
// Listen to auth changes
supabase.auth.onAuthStateChange((event, session) => {
  if (event === 'SIGNED_IN') {
    console.log('User signed in:', session?.user)
  }
  if (event === 'SIGNED_OUT') {
    console.log('User signed out')
  }
  if (event === 'TOKEN_REFRESHED') {
    console.log('Token refreshed')
  }
})

// Update user metadata
const { data, error } = await supabase.auth.updateUser({
  data: { theme: 'dark' }
})

// Change password
const { data, error } = await supabase.auth.updateUser({
  password: 'new-password'
})
```

## Row Level Security (RLS)

### RLS Fundamentals
Postgres Row Level Security controls data access at the database level:

```sql
-- Enable RLS on table
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Policy: Users can read all published posts
CREATE POLICY "Public posts are viewable by everyone"
ON posts FOR SELECT
USING (status = 'published');

-- Policy: Users can only update their own posts
CREATE POLICY "Users can update own posts"
ON posts FOR UPDATE
USING (auth.uid() = author_id);

-- Policy: Authenticated users can insert posts
CREATE POLICY "Authenticated users can create posts"
ON posts FOR INSERT
WITH CHECK (auth.uid() = author_id);

-- Policy: Users can delete their own posts
CREATE POLICY "Users can delete own posts"
ON posts FOR DELETE
USING (auth.uid() = author_id);
```

### Common RLS Patterns
```sql
-- Public read, authenticated write
CREATE POLICY "Anyone can view posts"
ON posts FOR SELECT
USING (true);

CREATE POLICY "Authenticated users can create posts"
ON posts FOR INSERT
WITH CHECK (auth.uid() IS NOT NULL);

-- Organization-based access
CREATE POLICY "Users can view org data"
ON documents FOR SELECT
USING (
  organization_id IN (
    SELECT organization_id
    FROM memberships
    WHERE user_id = auth.uid()
  )
);

-- Role-based access
CREATE POLICY "Admins can do anything"
ON posts FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM user_roles
    WHERE user_id = auth.uid()
    AND role = 'admin'
  )
);

-- Time-based access
CREATE POLICY "View published or scheduled posts"
ON posts FOR SELECT
USING (
  status = 'published'
  OR (status = 'scheduled' AND publish_at <= NOW())
);
```

### RLS Helper Functions
```sql
-- Get current user ID
SELECT auth.uid();

-- Get current user JWT
SELECT auth.jwt();

-- Get specific claim
SELECT auth.jwt()->>'email';

-- Custom claims
SELECT auth.jwt()->'app_metadata'->>'role';
```

## Storage

### File Upload
```typescript
// Upload file
const { data, error } = await supabase.storage
  .from('avatars')
  .upload('public/avatar1.png', file, {
    cacheControl: '3600',
    upsert: false
  })

// Upload with progress
const { data, error } = await supabase.storage
  .from('avatars')
  .upload('public/avatar1.png', file, {
    onUploadProgress: (progress) => {
      console.log(`${progress.loaded}/${progress.total}`)
    }
  })

// Upload from URL
const { data, error } = await supabase.storage
  .from('avatars')
  .uploadToSignedUrl('path', token, file)
```

### File Operations
```typescript
// Download file
const { data, error } = await supabase.storage
  .from('avatars')
  .download('public/avatar1.png')

// Get public URL
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('public/avatar1.png')

// Create signed URL (temporary access)
const { data, error } = await supabase.storage
  .from('avatars')
  .createSignedUrl('private/document.pdf', 3600) // 1 hour

// List files
const { data, error } = await supabase.storage
  .from('avatars')
  .list('public', {
    limit: 100,
    offset: 0,
    sortBy: { column: 'name', order: 'asc' }
  })

// Delete file
const { data, error } = await supabase.storage
  .from('avatars')
  .remove(['public/avatar1.png'])

// Move file
const { data, error } = await supabase.storage
  .from('avatars')
  .move('public/avatar1.png', 'public/avatar2.png')
```

### Image Transformations
```typescript
// Transform image
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('avatar1.png', {
    transform: {
      width: 200,
      height: 200,
      resize: 'cover',
      quality: 80
    }
  })

// Available transformations
// width, height, resize (cover|contain|fill),
// quality (1-100), format (origin|jpeg|png|webp)
```

### Storage RLS
```sql
-- Enable RLS on storage
CREATE POLICY "Avatar images are publicly accessible"
ON storage.objects FOR SELECT
USING (bucket_id = 'avatars' AND (storage.foldername(name))[1] = 'public');

CREATE POLICY "Users can upload their own avatar"
ON storage.objects FOR INSERT
WITH CHECK (
  bucket_id = 'avatars'
  AND (storage.foldername(name))[1] = auth.uid()::text
);

CREATE POLICY "Users can delete their own avatar"
ON storage.objects FOR DELETE
USING (
  bucket_id = 'avatars'
  AND (storage.foldername(name))[1] = auth.uid()::text
);
```

## Realtime Subscriptions

### Database Changes
```typescript
// Subscribe to inserts
const channel = supabase
  .channel('posts-insert')
  .on(
    'postgres_changes',
    {
      event: 'INSERT',
      schema: 'public',
      table: 'posts'
    },
    (payload) => {
      console.log('New post:', payload.new)
    }
  )
  .subscribe()

// Subscribe to updates
const channel = supabase
  .channel('posts-update')
  .on(
    'postgres_changes',
    {
      event: 'UPDATE',
      schema: 'public',
      table: 'posts',
      filter: 'id=eq.1'
    },
    (payload) => {
      console.log('Updated:', payload.new)
      console.log('Previous:', payload.old)
    }
  )
  .subscribe()

// Subscribe to all changes
const channel = supabase
  .channel('posts-all')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'posts'
    },
    (payload) => {
      console.log('Change:', payload)
    }
  )
  .subscribe()

// Unsubscribe
supabase.removeChannel(channel)
```

### Presence (Track Online Users)
```typescript
// Track presence
const channel = supabase.channel('room-1')

// Track current user
channel
  .on('presence', { event: 'sync' }, () => {
    const state = channel.presenceState()
    console.log('Online users:', state)
  })
  .on('presence', { event: 'join' }, ({ key, newPresences }) => {
    console.log('User joined:', newPresences)
  })
  .on('presence', { event: 'leave' }, ({ key, leftPresences }) => {
    console.log('User left:', leftPresences)
  })
  .subscribe(async (status) => {
    if (status === 'SUBSCRIBED') {
      await channel.track({
        user_id: userId,
        online_at: new Date().toISOString()
      })
    }
  })

// Untrack
await channel.untrack()
```

### Broadcast (Send Messages)
```typescript
// Broadcast messages
const channel = supabase.channel('chat-room')

channel
  .on('broadcast', { event: 'message' }, (payload) => {
    console.log('Message:', payload)
  })
  .subscribe()

// Send message
await channel.send({
  type: 'broadcast',
  event: 'message',
  payload: { text: 'Hello', user: 'John' }
})
```

## Edge Functions

### Edge Function Basics
Serverless functions on Deno runtime:

```bash
# Create function
supabase functions new my-function

# Serve locally
supabase functions serve

# Deploy
supabase functions deploy my-function
```

### Edge Function Example
```typescript
// supabase/functions/my-function/index.ts
import { serve } from 'https://deno.land/std@0.177.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  try {
    // Get auth header
    const authHeader = req.headers.get('Authorization')!

    // Create Supabase client
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      { global: { headers: { Authorization: authHeader } } }
    )

    // Verify user
    const { data: { user }, error } = await supabase.auth.getUser()
    if (error) throw error

    // Process request
    const { data } = await supabase
      .from('posts')
      .select('*')
      .eq('author_id', user.id)

    return new Response(
      JSON.stringify({ data }),
      { headers: { 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    )
  }
})
```

### Invoke Edge Function
```typescript
// From client
const { data, error } = await supabase.functions.invoke('my-function', {
  body: { name: 'John' }
})

// With auth
const { data, error } = await supabase.functions.invoke('my-function', {
  headers: {
    Authorization: `Bearer ${session.access_token}`
  },
  body: { name: 'John' }
})
```

## Next.js Integration

### App Router Setup
```typescript
// lib/supabase/client.ts (Client Component)
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}

// lib/supabase/server.ts (Server Component)
import { createServerClient, type CookieOptions } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value
        },
        set(name: string, value: string, options: CookieOptions) {
          cookieStore.set({ name, value, ...options })
        },
        remove(name: string, options: CookieOptions) {
          cookieStore.set({ name, value: '', ...options })
        },
      },
    }
  )
}

// lib/supabase/middleware.ts (Middleware)
import { createServerClient, type CookieOptions } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function updateSession(request: NextRequest) {
  let response = NextResponse.next({
    request: {
      headers: request.headers,
    },
  })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value
        },
        set(name: string, value: string, options: CookieOptions) {
          request.cookies.set({ name, value, ...options })
          response = NextResponse.next({
            request: { headers: request.headers },
          })
          response.cookies.set({ name, value, ...options })
        },
        remove(name: string, options: CookieOptions) {
          request.cookies.set({ name, value: '', ...options })
          response = NextResponse.next({
            request: { headers: request.headers },
          })
          response.cookies.set({ name, value: '', ...options })
        },
      },
    }
  )

  await supabase.auth.getUser()
  return response
}
```

### Middleware
```typescript
// middleware.ts
import { updateSession } from '@/lib/supabase/middleware'

export async function middleware(request: NextRequest) {
  return await updateSession(request)
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
```

### Server Component
```typescript
// app/posts/page.tsx
import { createClient } from '@/lib/supabase/server'

export default async function PostsPage() {
  const supabase = await createClient()

  const { data: posts } = await supabase
    .from('posts')
    .select('*')
    .order('created_at', { ascending: false })

  return (
    <div>
      {posts?.map((post) => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.content}</p>
        </article>
      ))}
    </div>
  )
}
```

### Client Component
```typescript
// app/components/new-post.tsx
'use client'

import { useState } from 'react'
import { createClient } from '@/lib/supabase/client'

export function NewPost() {
  const [title, setTitle] = useState('')
  const supabase = createClient()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return

    const { error } = await supabase
      .from('posts')
      .insert({ title, author_id: user.id })

    if (!error) {
      setTitle('')
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Post title"
      />
      <button>Create</button>
    </form>
  )
}
```

### Server Actions
```typescript
// app/actions/posts.ts
'use server'

import { revalidatePath } from 'next/cache'
import { createClient } from '@/lib/supabase/server'

export async function createPost(formData: FormData) {
  const supabase = await createClient()

  const { data: { user } } = await supabase.auth.getUser()
  if (!user) {
    return { error: 'Not authenticated' }
  }

  const title = formData.get('title') as string

  const { error } = await supabase
    .from('posts')
    .insert({ title, author_id: user.id })

  if (error) {
    return { error: error.message }
  }

  revalidatePath('/posts')
  return { success: true }
}
```

## TypeScript Type Generation

### Generate Types from Database
```bash
# Install CLI
npm install -D supabase

# Login
npx supabase login

# Link project
npx supabase link --project-ref your-project-ref

# Generate types
npx supabase gen types typescript --project-id your-project-ref > types/supabase.ts

# Or from local database
npx supabase gen types typescript --local > types/supabase.ts
```

### Use Generated Types
```typescript
// types/supabase.ts (generated)
export type Database = {
  public: {
    Tables: {
      posts: {
        Row: {
          id: string
          title: string
          content: string | null
          author_id: string
          created_at: string
        }
        Insert: {
          id?: string
          title: string
          content?: string | null
          author_id: string
          created_at?: string
        }
        Update: {
          id?: string
          title?: string
          content?: string | null
          author_id?: string
          created_at?: string
        }
      }
    }
  }
}

// Usage
import { createClient } from '@supabase/supabase-js'
import { Database } from '@/types/supabase'

const supabase = createClient<Database>(url, key)

// Type-safe queries
const { data } = await supabase
  .from('posts') // TypeScript knows this table exists
  .select('title, content') // Autocomplete for columns
  .single()

// data is typed as { title: string; content: string | null }
```

## Supabase CLI and Local Development

### Setup Local Development
```bash
# Initialize Supabase
npx supabase init

# Start local Supabase (Postgres, Auth, Storage, etc.)
npx supabase start

# Stop
npx supabase stop

# Reset database
npx supabase db reset

# Status
npx supabase status
```

### Database Migrations
```bash
# Create migration
npx supabase migration new create_posts_table

# Edit migration file
# supabase/migrations/20240101000000_create_posts_table.sql

# Apply migrations
npx supabase db push

# Pull remote schema
npx supabase db pull

# Diff local vs remote
npx supabase db diff
```

### Migration Example
```sql
-- supabase/migrations/20240101000000_create_posts_table.sql
CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  content TEXT,
  author_id UUID NOT NULL REFERENCES auth.users(id),
  status TEXT NOT NULL DEFAULT 'draft',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Anyone can view published posts"
ON posts FOR SELECT
USING (status = 'published');

CREATE POLICY "Users can create their own posts"
ON posts FOR INSERT
WITH CHECK (auth.uid() = author_id);

CREATE POLICY "Users can update their own posts"
ON posts FOR UPDATE
USING (auth.uid() = author_id);

-- Indexes
CREATE INDEX posts_author_id_idx ON posts(author_id);
CREATE INDEX posts_status_idx ON posts(status);

-- Trigger for updated_at
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON posts
FOR EACH ROW
EXECUTE FUNCTION moddatetime(updated_at);
```

## Security Best Practices

### API Key Management
```typescript
// NEVER expose service_role key in client
// Use anon key for client-side
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY! // Public
)

// Service role key only on server
const supabaseAdmin = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!, // Secret, bypasses RLS
  { auth: { persistSession: false } }
)
```

### RLS Best Practices
```sql
-- Always enable RLS
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Default deny (no policy = no access)
-- Explicitly grant access with policies

-- Test policies as different users
SET request.jwt.claims.sub = 'user-id';
SELECT * FROM posts; -- Test as this user

-- Disable RLS only for admin operations
-- Use service_role key from server, never client
```

### Input Validation
```typescript
// Validate on client and server
function validatePost(data: unknown) {
  const schema = z.object({
    title: z.string().min(1).max(200),
    content: z.string().max(10000).optional()
  })

  return schema.parse(data)
}

// Server-side validation in Edge Function
serve(async (req) => {
  const body = await req.json()

  try {
    const validated = validatePost(body)
    // Process validated data
  } catch (error) {
    return new Response(
      JSON.stringify({ error: 'Invalid input' }),
      { status: 400 }
    )
  }
})
```

### Environment Variables
```bash
# .env.local
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ... # Public
SUPABASE_SERVICE_ROLE_KEY=eyJ... # Secret, server-only

# Production: Use environment variables in hosting platform
# Never commit .env files to git
```

## Production Deployment

### Database Optimization
```sql
-- Add indexes for common queries
CREATE INDEX posts_created_at_idx ON posts(created_at DESC);
CREATE INDEX posts_author_status_idx ON posts(author_id, status);

-- Optimize full-text search
CREATE INDEX posts_title_search_idx ON posts
USING GIN (to_tsvector('english', title));

-- Analyze query performance
EXPLAIN ANALYZE
SELECT * FROM posts WHERE author_id = 'xxx';

-- Vacuum and analyze
VACUUM ANALYZE posts;
```

### Connection Pooling
```typescript
// Use connection pooling for serverless
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(url, key, {
  db: {
    schema: 'public',
  },
  auth: {
    persistSession: true,
    autoRefreshToken: true,
  },
  global: {
    headers: { 'x-my-custom-header': 'my-value' },
  },
})

// Configure pool in Supabase dashboard
// Settings > Database > Connection pooling
```

### Monitoring
```typescript
// Enable query logging
const supabase = createClient(url, key, {
  global: {
    fetch: async (url, options) => {
      console.log('Query:', url)
      return fetch(url, options)
    }
  }
})

// Monitor in Supabase Dashboard
// - Database performance
// - API usage
// - Storage usage
// - Auth activity
```

### Backup Strategy
```bash
# Automatic backups (Pro plan+)
# Daily backups with point-in-time recovery

# Manual backup
pg_dump -h db.xxx.supabase.co -U postgres -d postgres > backup.sql

# Restore
psql -h db.xxx.supabase.co -U postgres -d postgres < backup.sql
```

## Supabase vs Firebase

### Similarities
- Backend-as-a-Service platform
- Authentication with multiple providers
- Realtime data synchronization
- File storage
- Serverless functions
- Generous free tier

### Key Differences

**Database**
- Supabase: PostgreSQL (SQL, full control)
- Firebase: Firestore (NoSQL, limited queries)

**Queries**
- Supabase: Full SQL, joins, aggregations
- Firebase: Limited filtering, no joins

**Security**
- Supabase: Row Level Security (Postgres native)
- Firebase: Security Rules (custom syntax)

**Open Source**
- Supabase: Fully open source, self-hostable
- Firebase: Proprietary, Google-hosted only

**Pricing**
- Supabase: Compute-based, predictable
- Firebase: Usage-based, can spike

**Ecosystem**
- Supabase: Postgres ecosystem (extensions, tools)
- Firebase: Google Cloud Platform integration

### Migration Considerations
```typescript
// Firestore collection query
const snapshot = await db
  .collection('posts')
  .where('status', '==', 'published')
  .orderBy('createdAt', 'desc')
  .limit(10)
  .get()

// Equivalent Supabase query
const { data } = await supabase
  .from('posts')
  .select('*')
  .eq('status', 'published')
  .order('created_at', { ascending: false })
  .limit(10)

// Complex queries easier in Supabase
const { data } = await supabase
  .from('posts')
  .select(`
    *,
    author:profiles!inner(name),
    comments(count)
  `)
  .gte('created_at', startDate)
  .lte('created_at', endDate)
  .order('created_at', { ascending: false })
// Firebase would require multiple queries + client-side joins
```

## Advanced Patterns

### Optimistic Updates
```typescript
'use client'

import { useState, useOptimistic } from 'react'
import { createClient } from '@/lib/supabase/client'

export function PostList({ initialPosts }: { initialPosts: Post[] }) {
  const [posts, setPosts] = useState(initialPosts)
  const [optimisticPosts, addOptimisticPost] = useOptimistic(
    posts,
    (state, newPost: Post) => [...state, newPost]
  )

  const supabase = createClient()

  const createPost = async (title: string) => {
    const tempPost = {
      id: crypto.randomUUID(),
      title,
      created_at: new Date().toISOString()
    }

    addOptimisticPost(tempPost)

    const { data } = await supabase
      .from('posts')
      .insert({ title })
      .select()
      .single()

    if (data) {
      setPosts([...posts, data])
    }
  }

  return (
    <div>
      {optimisticPosts.map((post) => (
        <div key={post.id}>{post.title}</div>
      ))}
    </div>
  )
}
```

### Infinite Scroll
```typescript
'use client'

import { useState, useEffect } from 'react'
import { createClient } from '@/lib/supabase/client'

const PAGE_SIZE = 20

export function InfinitePostList() {
  const [posts, setPosts] = useState<Post[]>([])
  const [page, setPage] = useState(0)
  const [hasMore, setHasMore] = useState(true)

  const supabase = createClient()

  useEffect(() => {
    const loadMore = async () => {
      const { data } = await supabase
        .from('posts')
        .select('*')
        .range(page * PAGE_SIZE, (page + 1) * PAGE_SIZE - 1)
        .order('created_at', { ascending: false })

      if (data) {
        setPosts([...posts, ...data])
        setHasMore(data.length === PAGE_SIZE)
      }
    }

    loadMore()
  }, [page])

  return (
    <div>
      {posts.map((post) => (
        <div key={post.id}>{post.title}</div>
      ))}
      {hasMore && (
        <button onClick={() => setPage(page + 1)}>
          Load More
        </button>
      )}
    </div>
  )
}
```

### Debounced Search
```typescript
'use client'

import { useState, useEffect } from 'react'
import { createClient } from '@/lib/supabase/client'
import { useDebounce } from '@/hooks/use-debounce'

export function SearchPosts() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<Post[]>([])
  const debouncedQuery = useDebounce(query, 300)

  const supabase = createClient()

  useEffect(() => {
    if (!debouncedQuery) {
      setResults([])
      return
    }

    const search = async () => {
      const { data } = await supabase
        .from('posts')
        .select('*')
        .textSearch('title', debouncedQuery)
        .limit(10)

      if (data) setResults(data)
    }

    search()
  }, [debouncedQuery])

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search posts..."
      />
      {results.map((post) => (
        <div key={post.id}>{post.title}</div>
      ))}
    </div>
  )
}
```

---

## Summary

Supabase provides a complete backend platform with:
- **Postgres Database** with REST and GraphQL APIs
- **Built-in Authentication** with multiple providers
- **Row Level Security** for granular access control
- **File Storage** with image transformations
- **Realtime Subscriptions** for live updates
- **Edge Functions** for serverless compute
- **Next.js Integration** with Server and Client Components
- **TypeScript Support** with auto-generated types
- **Local Development** with Supabase CLI
- **Production Ready** with monitoring and backups

Use Supabase when a full-featured backend with the power of Postgres, built-in auth, and realtime capabilities is needed, all with excellent TypeScript and Next.js integration.