---
name: Supabase Developer
description: Build full-stack applications with Supabase (PostgreSQL, Auth, Storage, Real-time, Edge Functions). Use when implementing authentication, database design with RLS, file storage, real-time features, or serverless functions.
version: 1.0.0
category: backend
tags:
  - backend
  - database
  - authentication
  - storage
  - real-time
  - serverless
related_skills:
  - api-designer
  - security-engineer
  - frontend-builder
  - data-engineer
  - performance-optimizer
triggers:
  - supabase-developer
  - supabase developer
  - supabase dev
supports_mcps:
  - supabase-mcp
required_tools:
  - database-query-tool
  - api-caller-tool
required_integrations:
  - supabase
---

# Supabase Developer

**Build production-ready full-stack applications with Supabase.**

Supabase is an open-source Firebase alternative providing PostgreSQL database, authentication, storage, real-time subscriptions, and edge functions. This skill guides you through building secure, scalable applications using Supabase's full feature set.

---

## When to Use This Skill

- **Authentication**: Implementing user signup/login with email, OAuth, magic links, or phone auth
- **Database**: Designing PostgreSQL schemas with Row Level Security (RLS)
- **Storage**: Managing file uploads, downloads, and access control
- **Real-time**: Building live features with subscriptions and broadcasts
- **Edge Functions**: Serverless TypeScript functions at the edge
- **Migrations**: Managing database schema changes
- **Integration**: Connecting Next.js, React, Vue, or other frameworks

---

## Core Supabase Concepts

### 1. Database (PostgreSQL)

Supabase uses PostgreSQL with extensions:

- **PostgREST**: Auto-generates REST API from schema
- **pg_graphql**: Optional GraphQL support
- **Extensions**: pgvector for embeddings, pg_cron for scheduled jobs

### 2. Authentication

Built-in auth with multiple providers:

- Email/password with confirmation
- Magic links (passwordless)
- OAuth (Google, GitHub, etc.)
- Phone/SMS authentication
- SAML SSO (enterprise)

### 3. Row Level Security (RLS)

PostgreSQL policies that enforce data access at the database level:

- User can only read their own data
- Admin can read all data
- Public read, authenticated write

### 4. Storage

S3-compatible object storage with RLS:

- Public and private buckets
- File size and type restrictions
- Image transformations on the fly
- CDN integration

### 5. Real-time

WebSocket-based subscriptions:

- Database changes (INSERT, UPDATE, DELETE)
- Broadcast messages to channels
- Presence tracking (who's online)

### 6. Edge Functions

Deno-based serverless functions:

- Deploy globally at the edge
- TypeScript/JavaScript runtime
- Background jobs and webhooks
- Custom API endpoints

---

## 6-Phase Supabase Implementation

### Phase 1: Project Setup & Configuration

**Goal**: Initialize Supabase project and connect to your application

#### 1.1 Create Supabase Project

```bash
# Option A: Web Dashboard
# 1. Go to https://supabase.com
# 2. Create new project
# 3. Save database password securely

# Option B: CLI (recommended for production)
npx supabase init
npx supabase start
```

#### 1.2 Install Client Libraries

```bash
# JavaScript/TypeScript
npm install @supabase/supabase-js

# React helpers (optional)
npm install @supabase/auth-helpers-react @supabase/auth-helpers-nextjs

# For Auth UI components
npm install @supabase/auth-ui-react @supabase/auth-ui-shared
```

#### 1.3 Environment Configuration

```env
# .env.local
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key # Server-side only!
```

#### 1.4 Initialize Client

```typescript
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
```

**Next.js 13+ App Router Pattern:**

```typescript
// lib/supabase/client.ts (Client Components)
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}

// lib/supabase/server.ts (Server Components)
import { createServerClient, type CookieOptions } from '@supabase/ssr'
import { cookies } from 'next/headers'

export function createClient() {
  const cookieStore = cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value
        }
      }
    }
  )
}
```

---

### Phase 2: Authentication Implementation

**Goal**: Secure user authentication with session management

#### 2.1 Authentication Strategies

**Email/Password Authentication:**

```typescript
// Sign up
async function signUp(email: string, password: string) {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      emailRedirectTo: 'https://yourapp.com/auth/callback'
    }
  })

  if (error) throw error
  return data
}

// Sign in
async function signIn(email: string, password: string) {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password
  })

  if (error) throw error
  return data
}

// Sign out
async function signOut() {
  const { error } = await supabase.auth.signOut()
  if (error) throw error
}
```

**OAuth Authentication:**

```typescript
// Google OAuth
async function signInWithGoogle() {
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: {
      redirectTo: 'https://yourapp.com/auth/callback',
      queryParams: {
        access_type: 'offline',
        prompt: 'consent'
      }
    }
  })

  if (error) throw error
  return data
}

// GitHub, Twitter, Discord, etc. - same pattern
```

**Magic Link (Passwordless):**

```typescript
async function signInWithMagicLink(email: string) {
  const { data, error } = await supabase.auth.signInWithOtp({
    email,
    options: {
      emailRedirectTo: 'https://yourapp.com/auth/callback'
    }
  })

  if (error) throw error
  return data
}
```

#### 2.2 Session Management

```typescript
// Get current session
async function getSession() {
  const {
    data: { session },
    error
  } = await supabase.auth.getSession()
  return session
}

// Get current user
async function getUser() {
  const {
    data: { user },
    error
  } = await supabase.auth.getUser()
  return user
}

// Listen to auth changes
supabase.auth.onAuthStateChange((event, session) => {
  console.log(event, session)

  if (event === 'SIGNED_IN') {
    // User signed in
  }
  if (event === 'SIGNED_OUT') {
    // User signed out
  }
  if (event === 'TOKEN_REFRESHED') {
    // Token refreshed
  }
})
```

#### 2.3 Protected Routes (Next.js)

```typescript
// middleware.ts
import { createMiddlewareClient } from '@supabase/auth-helpers-nextjs'
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(req: NextRequest) {
  const res = NextResponse.next()
  const supabase = createMiddlewareClient({ req, res })

  const {
    data: { session }
  } = await supabase.auth.getSession()

  // Protected routes
  if (!session && req.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', req.url))
  }

  return res
}

export const config = {
  matcher: ['/dashboard/:path*', '/profile/:path*']
}
```

---

### Phase 3: Database Design & RLS

**Goal**: Design secure database schema with Row Level Security

#### 3.1 Schema Design

```sql
-- Example: Blog application schema

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Profiles table (extends auth.users)
CREATE TABLE profiles (
  id UUID REFERENCES auth.users(id) PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  full_name TEXT,
  avatar_url TEXT,
  bio TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Posts table
CREATE TABLE posts (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  published BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Comments table
CREATE TABLE comments (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  post_id UUID REFERENCES posts(id) ON DELETE CASCADE NOT NULL,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX posts_user_id_idx ON posts(user_id);
CREATE INDEX posts_created_at_idx ON posts(created_at DESC);
CREATE INDEX comments_post_id_idx ON comments(post_id);
```

#### 3.2 Row Level Security (RLS) Policies

```sql
-- Enable RLS on all tables
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;

-- Profiles: Users can read all, update only their own
CREATE POLICY "Public profiles are viewable by everyone"
  ON profiles FOR SELECT
  USING (true);

CREATE POLICY "Users can insert their own profile"
  ON profiles FOR INSERT
  WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can update their own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id);

-- Posts: Public can read published, users can manage their own
CREATE POLICY "Published posts are viewable by everyone"
  ON posts FOR SELECT
  USING (published = true OR auth.uid() = user_id);

CREATE POLICY "Users can create their own posts"
  ON posts FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own posts"
  ON posts FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own posts"
  ON posts FOR DELETE
  USING (auth.uid() = user_id);

-- Comments: Public can read, users can manage their own
CREATE POLICY "Comments are viewable by everyone"
  ON comments FOR SELECT
  USING (true);

CREATE POLICY "Authenticated users can create comments"
  ON comments FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own comments"
  ON comments FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own comments"
  ON comments FOR DELETE
  USING (auth.uid() = user_id);
```

#### 3.3 Database Functions

```sql
-- Automatic updated_at timestamp
CREATE OR REPLACE FUNCTION handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to tables
CREATE TRIGGER handle_profiles_updated_at
  BEFORE UPDATE ON profiles
  FOR EACH ROW
  EXECUTE FUNCTION handle_updated_at();

CREATE TRIGGER handle_posts_updated_at
  BEFORE UPDATE ON posts
  FOR EACH ROW
  EXECUTE FUNCTION handle_updated_at();

-- Automatic profile creation on signup
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, username, full_name, avatar_url)
  VALUES (
    NEW.id,
    NEW.raw_user_meta_data->>'username',
    NEW.raw_user_meta_data->>'full_name',
    NEW.raw_user_meta_data->>'avatar_url'
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION handle_new_user();
```

#### 3.4 Querying with TypeScript

```typescript
// Insert
const { data, error } = await supabase
  .from('posts')
  .insert({
    title: 'My First Post',
    content: 'Hello World!',
    user_id: userId
  })
  .select()
  .single()

// Select with filters
const { data: posts } = await supabase
  .from('posts')
  .select('*, profiles(*), comments(*)')
  .eq('published', true)
  .order('created_at', { ascending: false })
  .limit(10)

// Update
const { data, error } = await supabase
  .from('posts')
  .update({ published: true })
  .eq('id', postId)
  .select()

// Delete
const { error } = await supabase.from('posts').delete().eq('id', postId)

// Count
const { count } = await supabase.from('posts').select('*', { count: 'exact', head: true })

// Full-text search
const { data } = await supabase.from('posts').select('*').textSearch('content', 'supabase', {
  type: 'websearch',
  config: 'english'
})
```

---

### Phase 4: Storage Implementation

**Goal**: Manage file uploads with access control

#### 4.1 Bucket Configuration

```sql
-- Create storage bucket
INSERT INTO storage.buckets (id, name, public)
VALUES ('avatars', 'avatars', true);

INSERT INTO storage.buckets (id, name, public)
VALUES ('private-docs', 'private-docs', false);
```

#### 4.2 Storage RLS Policies

```sql
-- Avatars: Anyone can read, users can upload their own
CREATE POLICY "Avatar images are publicly accessible"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'avatars');

CREATE POLICY "Users can upload their own avatar"
  ON storage.objects FOR INSERT
  WITH CHECK (
    bucket_id = 'avatars' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY "Users can update their own avatar"
  ON storage.objects FOR UPDATE
  USING (
    bucket_id = 'avatars' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );

-- Private docs: Only owner can access
CREATE POLICY "Users can access their own documents"
  ON storage.objects FOR SELECT
  USING (
    bucket_id = 'private-docs' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY "Users can upload their own documents"
  ON storage.objects FOR INSERT
  WITH CHECK (
    bucket_id = 'private-docs' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );
```

#### 4.3 File Upload/Download

```typescript
// Upload file
async function uploadFile(bucket: string, path: string, file: File) {
  const { data, error } = await supabase.storage.from(bucket).upload(path, file, {
    cacheControl: '3600',
    upsert: false
  })

  if (error) throw error
  return data
}

// Download file
async function downloadFile(bucket: string, path: string) {
  const { data, error } = await supabase.storage.from(bucket).download(path)

  if (error) throw error
  return data
}

// Get public URL
function getPublicUrl(bucket: string, path: string) {
  const { data } = supabase.storage.from(bucket).getPublicUrl(path)

  return data.publicUrl
}

// Get signed URL (private files)
async function getSignedUrl(bucket: string, path: string, expiresIn: number = 3600) {
  const { data, error } = await supabase.storage.from(bucket).createSignedUrl(path, expiresIn)

  if (error) throw error
  return data.signedUrl
}

// Delete file
async function deleteFile(bucket: string, path: string) {
  const { error } = await supabase.storage.from(bucket).remove([path])

  if (error) throw error
}

// List files
async function listFiles(bucket: string, folder: string = '') {
  const { data, error } = await supabase.storage.from(bucket).list(folder, {
    limit: 100,
    offset: 0,
    sortBy: { column: 'created_at', order: 'desc' }
  })

  if (error) throw error
  return data
}
```

#### 4.4 Image Transformations

```typescript
// Get resized image URL
function getTransformedImage(
  bucket: string,
  path: string,
  options: {
    width?: number
    height?: number
    quality?: number
  }
) {
  const { data } = supabase.storage.from(bucket).getPublicUrl(path, {
    transform: {
      width: options.width,
      height: options.height,
      quality: options.quality || 80
    }
  })

  return data.publicUrl
}
```

---

### Phase 5: Real-time Features

**Goal**: Build live, collaborative features

#### 5.1 Database Change Subscriptions

```typescript
// Subscribe to INSERT events
const subscription = supabase
  .channel('posts-channel')
  .on(
    'postgres_changes',
    {
      event: 'INSERT',
      schema: 'public',
      table: 'posts'
    },
    payload => {
      console.log('New post created:', payload.new)
      // Update UI with new post
    }
  )
  .subscribe()

// Subscribe to all events on a table
supabase
  .channel('comments-channel')
  .on(
    'postgres_changes',
    {
      event: '*', // INSERT, UPDATE, DELETE
      schema: 'public',
      table: 'comments'
    },
    payload => {
      console.log('Change detected:', payload)
    }
  )
  .subscribe()

// Subscribe with filters
supabase
  .channel('my-posts-channel')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'posts',
      filter: `user_id=eq.${userId}`
    },
    payload => {
      console.log('My post changed:', payload)
    }
  )
  .subscribe()

// Unsubscribe
subscription.unsubscribe()
```

#### 5.2 Broadcast Messages

```typescript
// Join a room and broadcast messages
const channel = supabase.channel('room-1')

// Send broadcast message
channel.send({
  type: 'broadcast',
  event: 'message',
  payload: { text: 'Hello!', user: 'John' }
})

// Receive broadcast messages
channel
  .on('broadcast', { event: 'message' }, payload => {
    console.log('Message received:', payload)
  })
  .subscribe()
```

#### 5.3 Presence Tracking

```typescript
// Track online users
const channel = supabase.channel('online-users', {
  config: {
    presence: {
      key: userId
    }
  }
})

// Track current user presence
channel
  .on('presence', { event: 'sync' }, () => {
    const state = channel.presenceState()
    console.log('Online users:', state)
  })
  .on('presence', { event: 'join' }, ({ key, newPresences }) => {
    console.log('User joined:', key, newPresences)
  })
  .on('presence', { event: 'leave' }, ({ key, leftPresences }) => {
    console.log('User left:', key, leftPresences)
  })
  .subscribe(async status => {
    if (status === 'SUBSCRIBED') {
      await channel.track({
        user: userId,
        online_at: new Date().toISOString()
      })
    }
  })

// Update presence
await channel.track({ status: 'typing' })

// Stop tracking
await channel.untrack()
```

---

### Phase 6: Edge Functions & Advanced Features

**Goal**: Serverless functions and advanced capabilities

#### 6.1 Edge Functions

```typescript
// supabase/functions/hello/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async req => {
  try {
    // Create Supabase client with service role
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    )

    // Get user from auth header
    const authHeader = req.headers.get('Authorization')!
    const token = authHeader.replace('Bearer ', '')
    const {
      data: { user }
    } = await supabaseClient.auth.getUser(token)

    // Your logic here
    const { data, error } = await supabaseClient.from('posts').select('*').eq('user_id', user?.id)

    if (error) throw error

    return new Response(JSON.stringify({ data }), {
      headers: { 'Content-Type': 'application/json' }
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    })
  }
})
```

**Deploy Edge Function:**

```bash
# Deploy function
supabase functions deploy hello

# Invoke from client
const { data, error } = await supabase.functions.invoke('hello', {
  body: { name: 'World' },
})
```

#### 6.2 Database Webhooks

```sql
-- Send webhook on new post
CREATE OR REPLACE FUNCTION send_post_webhook()
RETURNS TRIGGER AS $$
BEGIN
  PERFORM
    net.http_post(
      url := 'https://your-api.com/webhook',
      headers := '{"Content-Type": "application/json"}'::jsonb,
      body := jsonb_build_object(
        'event', 'new_post',
        'post_id', NEW.id,
        'title', NEW.title
      )
    );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER on_post_created
  AFTER INSERT ON posts
  FOR EACH ROW
  EXECUTE FUNCTION send_post_webhook();
```

#### 6.3 Vector Search (pgvector)

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Add embedding column
ALTER TABLE posts ADD COLUMN embedding vector(1536);

-- Create vector index
CREATE INDEX ON posts USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Search by similarity
SELECT *
FROM posts
ORDER BY embedding <=> '[0.1, 0.2, ...]'::vector
LIMIT 10;
```

```typescript
// Generate and store embeddings
import OpenAI from 'openai'

const openai = new OpenAI()

async function addEmbedding(postId: string, text: string) {
  // Generate embedding
  const response = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: text
  })

  const embedding = response.data[0].embedding

  // Store in Supabase
  await supabase.from('posts').update({ embedding }).eq('id', postId)
}

// Semantic search
async function semanticSearch(query: string) {
  // Generate query embedding
  const response = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: query
  })

  const queryEmbedding = response.data[0].embedding

  // Search
  const { data } = await supabase.rpc('match_posts', {
    query_embedding: queryEmbedding,
    match_threshold: 0.7,
    match_count: 10
  })

  return data
}
```

---

## Database Migration Management

### Local Development Workflow

```bash
# Initialize Supabase locally
supabase init
supabase start

# Create new migration
supabase migration new add_posts_table

# Edit migration file in supabase/migrations/

# Apply migrations
supabase db reset

# Generate TypeScript types
supabase gen types typescript --local > types/supabase.ts
```

### Production Deployment

```bash
# Link to remote project
supabase link --project-ref your-project-ref

# Push migrations to production
supabase db push

# Or apply specific migration
supabase db remote commit
```

---

## Security Best Practices

### 1. Never Expose Service Role Key

```typescript
// ❌ WRONG - Never on client side
const supabase = createClient(url, SERVICE_ROLE_KEY)

// ✅ CORRECT - Use anon key on client
const supabase = createClient(url, ANON_KEY)

// ✅ Service role only on server
// app/api/admin/route.ts
const supabase = createClient(url, SERVICE_ROLE_KEY)
```

### 2. Always Use RLS

```sql
-- ❌ WRONG - Table without RLS
CREATE TABLE sensitive_data (
  id UUID PRIMARY KEY,
  secret TEXT
);

-- ✅ CORRECT - RLS enabled
CREATE TABLE sensitive_data (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id),
  secret TEXT
);

ALTER TABLE sensitive_data ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can only access their data"
  ON sensitive_data FOR ALL
  USING (auth.uid() = user_id);
```

### 3. Validate Input

```typescript
// ❌ WRONG - No validation
await supabase.from('posts').insert({ title: userInput })

// ✅ CORRECT - Validate first
import { z } from 'zod'

const schema = z.object({
  title: z.string().min(1).max(100),
  content: z.string().min(10).max(10000)
})

const validated = schema.parse(userInput)
await supabase.from('posts').insert(validated)
```

### 4. Rate Limiting

```typescript
// Use Edge Functions for rate limiting
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(url, key)

// Check rate limit
const { count } = await supabase
  .from('api_calls')
  .select('*', { count: 'exact', head: true })
  .eq('user_id', userId)
  .gte('created_at', oneHourAgo)

if (count >= 100) {
  return new Response('Rate limit exceeded', { status: 429 })
}
```

---

## Performance Optimization

### 1. Use Indexes

```sql
-- Add indexes on frequently queried columns
CREATE INDEX posts_user_id_idx ON posts(user_id);
CREATE INDEX posts_created_at_idx ON posts(created_at DESC);

-- Composite indexes for multi-column queries
CREATE INDEX posts_user_published_idx ON posts(user_id, published);

-- Full-text search indexes
CREATE INDEX posts_content_fts_idx ON posts USING gin(to_tsvector('english', content));
```

### 2. Select Only What You Need

```typescript
// ❌ WRONG - Select everything
const { data } = await supabase.from('posts').select('*')

// ✅ CORRECT - Select specific columns
const { data } = await supabase.from('posts').select('id, title, created_at')
```

### 3. Use Pagination

```typescript
// Offset pagination
const { data } = await supabase.from('posts').select('*').range(0, 9)

// Cursor pagination (better for large datasets)
const { data } = await supabase
  .from('posts')
  .select('*')
  .gt('created_at', lastCreatedAt)
  .order('created_at', { ascending: false })
  .limit(10)
```

### 4. Cache Static Data

```typescript
// Use React Query or SWR
import { useQuery } from '@tanstack/react-query'

function usePosts() {
  return useQuery({
    queryKey: ['posts'],
    queryFn: async () => {
      const { data } = await supabase.from('posts').select('*')
      return data
    },
    staleTime: 5 * 60 * 1000 // 5 minutes
  })
}
```

---

## Testing

### Unit Tests

```typescript
// Mock Supabase client
import { createClient } from '@supabase/supabase-js'

jest.mock('@supabase/supabase-js', () => ({
  createClient: jest.fn(() => ({
    from: jest.fn(() => ({
      select: jest.fn(() => ({
        eq: jest.fn(() => ({
          single: jest.fn(() =>
            Promise.resolve({
              data: { id: '1', title: 'Test' },
              error: null
            })
          )
        }))
      }))
    }))
  }))
}))

test('fetches post by id', async () => {
  const post = await getPostById('1')
  expect(post.title).toBe('Test')
})
```

### Integration Tests

```typescript
// Use test database
const testSupabase = createClient(
  process.env.TEST_SUPABASE_URL!,
  process.env.TEST_SUPABASE_ANON_KEY!
)

beforeEach(async () => {
  // Clean database
  await testSupabase.from('posts').delete().neq('id', '00000000-0000-0000-0000-000000000000')
})

test('creates post', async () => {
  const { data, error } = await testSupabase
    .from('posts')
    .insert({ title: 'Test Post', content: 'Content' })
    .select()
    .single()

  expect(error).toBeNull()
  expect(data.title).toBe('Test Post')
})
```

---

## Common Patterns

### 1. Optimistic UI Updates

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query'

function useCreatePost() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async newPost => {
      const { data } = await supabase.from('posts').insert(newPost).select().single()
      return data
    },
    onMutate: async newPost => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['posts'] })

      // Snapshot previous value
      const previousPosts = queryClient.getQueryData(['posts'])

      // Optimistically update
      queryClient.setQueryData(['posts'], old => [...old, newPost])

      return { previousPosts }
    },
    onError: (err, newPost, context) => {
      // Rollback on error
      queryClient.setQueryData(['posts'], context.previousPosts)
    },
    onSettled: () => {
      // Refetch after mutation
      queryClient.invalidateQueries({ queryKey: ['posts'] })
    }
  })
}
```

### 2. Soft Deletes

```sql
-- Add deleted_at column
ALTER TABLE posts ADD COLUMN deleted_at TIMESTAMP WITH TIME ZONE;

-- Update RLS to exclude deleted
CREATE POLICY "Only show non-deleted posts"
  ON posts FOR SELECT
  USING (deleted_at IS NULL);

-- Soft delete function
CREATE OR REPLACE FUNCTION soft_delete_post(post_id UUID)
RETURNS void AS $$
BEGIN
  UPDATE posts
  SET deleted_at = NOW()
  WHERE id = post_id AND user_id = auth.uid();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### 3. Audit Logs

```sql
-- Create audit log table
CREATE TABLE audit_logs (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  table_name TEXT NOT NULL,
  record_id UUID NOT NULL,
  action TEXT NOT NULL,
  old_data JSONB,
  new_data JSONB,
  user_id UUID REFERENCES auth.users(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Audit trigger function
CREATE OR REPLACE FUNCTION audit_trigger()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO audit_logs (table_name, record_id, action, old_data, new_data, user_id)
  VALUES (
    TG_TABLE_NAME,
    COALESCE(NEW.id, OLD.id),
    TG_OP,
    CASE WHEN TG_OP = 'DELETE' THEN row_to_json(OLD) ELSE NULL END,
    CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN row_to_json(NEW) ELSE NULL END,
    auth.uid()
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Apply to tables
CREATE TRIGGER audit_posts
  AFTER INSERT OR UPDATE OR DELETE ON posts
  FOR EACH ROW
  EXECUTE FUNCTION audit_trigger();
```

---

## Troubleshooting

### Issue: RLS Policies Not Working

**Symptom**: Can't query data even with correct policies

**Solution**:

```sql
-- Check if RLS is enabled
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public';

-- Check policies
SELECT * FROM pg_policies WHERE tablename = 'your_table';

-- Test policy as user
SET LOCAL ROLE authenticated;
SET LOCAL request.jwt.claims.sub TO 'user-uuid';
SELECT * FROM your_table;
```

### Issue: "JWT expired" Errors

**Solution**:

```typescript
// Auto-refresh tokens
supabase.auth.onAuthStateChange((event, session) => {
  if (event === 'TOKEN_REFRESHED') {
    // Token refreshed automatically
  }
})

// Manual refresh
const { data, error } = await supabase.auth.refreshSession()
```

### Issue: Storage Upload Fails

**Solution**:

```typescript
// Check file size (default: 50MB)
// Check MIME type restrictions
// Verify bucket exists
const { data: buckets } = await supabase.storage.listBuckets()

// Check RLS policies on storage.objects
```

### Issue: Real-time Not Working

**Solution**:

```sql
-- Enable replication for table
ALTER PUBLICATION supabase_realtime ADD TABLE posts;

-- Check if table is in publication
SELECT * FROM pg_publication_tables WHERE pubname = 'supabase_realtime';
```

---

## Quick Reference

### Essential Commands

```bash
# Local development
supabase init
supabase start
supabase stop
supabase status

# Migrations
supabase migration new migration_name
supabase db reset
supabase db push

# Type generation
supabase gen types typescript --local > types/supabase.ts

# Edge Functions
supabase functions new function_name
supabase functions serve
supabase functions deploy function_name

# Link to remote
supabase link --project-ref your-ref
```

### Common Queries

```typescript
// CRUD operations
const { data } = await supabase.from('table').select('*')
const { data } = await supabase.from('table').insert({ ... })
const { data } = await supabase.from('table').update({ ... }).eq('id', id)
const { data } = await supabase.from('table').delete().eq('id', id)

// Filters
.eq('column', value)
.neq('column', value)
.gt('column', value)
.gte('column', value)
.lt('column', value)
.lte('column', value)
.like('column', '%pattern%')
.ilike('column', '%pattern%')
.is('column', null)
.in('column', [1, 2, 3])
.contains('array_column', ['value'])
.textSearch('column', 'query')

// Modifiers
.order('column', { ascending: false })
.limit(10)
.range(0, 9)
.single()
.maybeSingle()
```

---

## Integration Examples

### Next.js 13+ App Router

See Phase 1 for client/server setup patterns.

### React + Vite

```typescript
// src/lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

export const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_ANON_KEY
)

// src/hooks/useAuth.ts
export function useAuth() {
  const [user, setUser] = useState(null)

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null)
    })

    const {
      data: { subscription }
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null)
    })

    return () => subscription.unsubscribe()
  }, [])

  return { user }
}
```

---

## Summary

This skill covers the complete Supabase development lifecycle:

1. ✅ **Setup**: Project initialization and client configuration
2. ✅ **Auth**: Multiple authentication strategies with session management
3. ✅ **Database**: PostgreSQL schema design with Row Level Security
4. ✅ **Storage**: File management with access control
5. ✅ **Real-time**: Live subscriptions, broadcasts, and presence
6. ✅ **Edge Functions**: Serverless TypeScript functions
7. ✅ **Security**: Best practices for production applications
8. ✅ **Performance**: Optimization strategies for scale
9. ✅ **Testing**: Unit and integration testing patterns
10. ✅ **Migration**: Database change management

**Key Takeaway**: Supabase provides a complete backend platform with PostgreSQL at its core. Row Level Security is your primary security layer—design RLS policies carefully to ensure data is secure by default.

For complex scenarios, combine this skill with:

- **api-designer** for custom API endpoints
- **security-engineer** for advanced security reviews
- **performance-optimizer** for scaling large applications
- **data-engineer** for complex data pipelines
