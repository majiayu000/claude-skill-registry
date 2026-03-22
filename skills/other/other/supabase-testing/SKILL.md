---
name: "Supabase Testing"
description: "Testing patterns for Supabase applications covering auth flow testing, Row Level Security policy testing, realtime subscription testing, and edge function testing"
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [supabase, rls, auth, realtime, edge-functions, postgres, storage, migrations, row-level-security, testing]
testingTypes: [unit, integration, e2e]
frameworks: [vitest, jest, playwright]
languages: [typescript, javascript]
domains: [web, api, backend]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, gemini-cli, amp]
---

# Supabase Testing Skill

You are an expert QA engineer specializing in testing Supabase-powered applications. When the user asks you to write, review, or debug tests for Supabase auth, Row Level Security, realtime subscriptions, edge functions, or storage, follow these detailed instructions.

## Core Principles

1. **Local-first testing** -- Always use Supabase CLI (`supabase start`) to run a local Postgres instance with all Supabase features. Never test directly against production.
2. **RLS is your security boundary** -- Row Level Security policies are the most critical code in a Supabase app. Test every policy with multiple user roles and edge cases.
3. **Test auth flows end-to-end** -- Supabase auth involves email confirmation, magic links, OAuth redirects, and JWT tokens. Test the full flow, not just the API call.
4. **Realtime requires connection testing** -- Subscription tests must establish actual WebSocket connections. Mock-only tests miss critical reconnection and conflict scenarios.
5. **Edge functions are isolated** -- Supabase Edge Functions run in Deno. Test them independently with their own test runner before integration testing.
6. **Storage policies mirror RLS** -- Storage bucket policies follow the same RLS pattern. Apply the same testing rigor to file access as to row access.
7. **Migration testing prevents data loss** -- Every schema migration should be tested against a snapshot of production-like data to verify both the up and down paths.

## Project Structure

Always organize Supabase testing with this structure:

```
supabase/
  config.toml
  migrations/
    20240101000000_create_profiles.sql
    20240102000000_add_rls_policies.sql
  functions/
    hello-world/
      index.ts
    send-notification/
      index.ts
  seed.sql
  tests/
    rls/
      profiles.test.ts
      posts.test.ts
      comments.test.ts
    migrations/
      migration.test.ts
src/
  lib/
    supabase/
      client.ts
      server.ts
      middleware.ts
  __tests__/
    unit/
      auth.test.ts
      database.test.ts
    integration/
      auth-flow.test.ts
      realtime.test.ts
      storage.test.ts
    e2e/
      signup-login.spec.ts
      crud-with-rls.spec.ts
    helpers/
      supabase-test-utils.ts
      test-users.ts
      seed-test-data.ts
```

## Supabase Local Setup for Testing

### Configuration

```toml
# supabase/config.toml
[project]
id = "my-project"

[db]
port = 54322

[auth]
site_url = "http://localhost:3000"
enable_signup = true

[auth.email]
enable_confirmations = false  # Disable for testing
double_confirm_changes = false

[auth.external.google]
enabled = false
```

### Test Helper Setup

```typescript
// __tests__/helpers/supabase-test-utils.ts
import { createClient, SupabaseClient } from '@supabase/supabase-js';

const SUPABASE_URL = process.env.SUPABASE_URL || 'http://127.0.0.1:54321';
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...';
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...';

// Anon client (respects RLS)
export function createAnonClient(): SupabaseClient {
  return createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
}

// Service role client (bypasses RLS)
export function createServiceClient(): SupabaseClient {
  return createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);
}

// Authenticated client for a specific user
export async function createAuthenticatedClient(
  email: string,
  password: string
): Promise<SupabaseClient> {
  const client = createAnonClient();
  const { error } = await client.auth.signInWithPassword({ email, password });
  if (error) throw new Error(`Auth failed for ${email}: ${error.message}`);
  return client;
}

// Create a test user and return authenticated client
export async function createTestUser(
  email?: string,
  password?: string,
  metadata?: Record<string, unknown>
): Promise<{ client: SupabaseClient; userId: string; email: string }> {
  const testEmail = email || `test-${Date.now()}-${Math.random().toString(36).slice(2)}@test.com`;
  const testPassword = password || 'TestPassword123!';

  const serviceClient = createServiceClient();

  // Create user via service role (bypasses email confirmation)
  const { data: user, error } = await serviceClient.auth.admin.createUser({
    email: testEmail,
    password: testPassword,
    email_confirm: true,
    user_metadata: metadata || {},
  });

  if (error) throw new Error(`Failed to create test user: ${error.message}`);

  const client = await createAuthenticatedClient(testEmail, testPassword);

  return {
    client,
    userId: user.user.id,
    email: testEmail,
  };
}

// Cleanup test data
export async function cleanupTestUser(userId: string): Promise<void> {
  const serviceClient = createServiceClient();
  await serviceClient.auth.admin.deleteUser(userId);
}

// Reset database to clean state
export async function resetDatabase(): Promise<void> {
  const serviceClient = createServiceClient();

  // Delete all non-system data in reverse dependency order
  await serviceClient.from('comments').delete().neq('id', '00000000-0000-0000-0000-000000000000');
  await serviceClient.from('posts').delete().neq('id', '00000000-0000-0000-0000-000000000000');
  await serviceClient.from('profiles').delete().neq('id', '00000000-0000-0000-0000-000000000000');
}
```

```typescript
// __tests__/helpers/test-users.ts
import { createTestUser, cleanupTestUser } from './supabase-test-utils';
import type { SupabaseClient } from '@supabase/supabase-js';

interface TestUserContext {
  client: SupabaseClient;
  userId: string;
  email: string;
}

export class TestUserManager {
  private users: TestUserContext[] = [];

  async createUser(
    role: string = 'user',
    metadata: Record<string, unknown> = {}
  ): Promise<TestUserContext> {
    const user = await createTestUser(undefined, undefined, { role, ...metadata });
    this.users.push(user);
    return user;
  }

  async createAdmin(): Promise<TestUserContext> {
    return this.createUser('admin');
  }

  async createModerator(): Promise<TestUserContext> {
    return this.createUser('moderator');
  }

  async cleanup(): Promise<void> {
    for (const user of this.users) {
      await cleanupTestUser(user.userId).catch(() => {});
    }
    this.users = [];
  }
}
```

## Row Level Security (RLS) Testing

### Schema and Policies

```sql
-- supabase/migrations/20240101000000_create_profiles.sql
CREATE TABLE profiles (
  id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  bio TEXT,
  avatar_url TEXT,
  is_public BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Anyone can view public profiles
CREATE POLICY "Public profiles are viewable by everyone"
  ON profiles FOR SELECT
  USING (is_public = true);

-- Users can view their own profile (even if private)
CREATE POLICY "Users can view own profile"
  ON profiles FOR SELECT
  USING (auth.uid() = id);

-- Users can update only their own profile
CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

-- Users can insert their own profile
CREATE POLICY "Users can insert own profile"
  ON profiles FOR INSERT
  WITH CHECK (auth.uid() = id);

-- Only admins can delete profiles
CREATE POLICY "Admins can delete profiles"
  ON profiles FOR DELETE
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE id = auth.uid()
      AND (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
    )
  );
```

```sql
-- supabase/migrations/20240102000000_create_posts.sql
CREATE TABLE posts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  author_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  published BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Anyone can view published posts
CREATE POLICY "Published posts are viewable by everyone"
  ON posts FOR SELECT
  USING (published = true);

-- Authors can view their own drafts
CREATE POLICY "Authors can view own drafts"
  ON posts FOR SELECT
  USING (auth.uid() = author_id);

-- Authenticated users can create posts
CREATE POLICY "Authenticated users can create posts"
  ON posts FOR INSERT
  WITH CHECK (auth.uid() = author_id);

-- Authors can update their own posts
CREATE POLICY "Authors can update own posts"
  ON posts FOR UPDATE
  USING (auth.uid() = author_id)
  WITH CHECK (auth.uid() = author_id);

-- Authors can delete their own posts
CREATE POLICY "Authors can delete own posts"
  ON posts FOR DELETE
  USING (auth.uid() = author_id);
```

### RLS Policy Tests

```typescript
// __tests__/integration/rls/profiles.test.ts
import { describe, it, expect, beforeAll, afterAll, beforeEach } from 'vitest';
import {
  createAnonClient,
  createServiceClient,
  resetDatabase,
} from '../../helpers/supabase-test-utils';
import { TestUserManager } from '../../helpers/test-users';

describe('Profiles RLS Policies', () => {
  const users = new TestUserManager();
  let serviceClient: ReturnType<typeof createServiceClient>;

  beforeAll(async () => {
    serviceClient = createServiceClient();
  });

  afterAll(async () => {
    await users.cleanup();
  });

  beforeEach(async () => {
    await resetDatabase();
  });

  describe('SELECT policies', () => {
    it('should allow anyone to view public profiles', async () => {
      const { userId } = await users.createUser();

      // Create a public profile via service role
      await serviceClient.from('profiles').insert({
        id: userId,
        username: 'publicuser',
        bio: 'Public bio',
        is_public: true,
      });

      // Anonymous client should see the profile
      const anonClient = createAnonClient();
      const { data, error } = await anonClient
        .from('profiles')
        .select('*')
        .eq('id', userId)
        .single();

      expect(error).toBeNull();
      expect(data).toBeDefined();
      expect(data!.username).toBe('publicuser');
    });

    it('should hide private profiles from anonymous users', async () => {
      const { userId } = await users.createUser();

      await serviceClient.from('profiles').insert({
        id: userId,
        username: 'privateuser',
        bio: 'Private bio',
        is_public: false,
      });

      const anonClient = createAnonClient();
      const { data } = await anonClient
        .from('profiles')
        .select('*')
        .eq('id', userId);

      expect(data).toEqual([]);
    });

    it('should allow users to view their own private profile', async () => {
      const { client, userId } = await users.createUser();

      await serviceClient.from('profiles').insert({
        id: userId,
        username: 'myprofile',
        bio: 'My private bio',
        is_public: false,
      });

      const { data, error } = await client
        .from('profiles')
        .select('*')
        .eq('id', userId)
        .single();

      expect(error).toBeNull();
      expect(data!.username).toBe('myprofile');
    });

    it('should hide private profiles from other authenticated users', async () => {
      const { userId: ownerId } = await users.createUser();
      const { client: otherClient } = await users.createUser();

      await serviceClient.from('profiles').insert({
        id: ownerId,
        username: 'secretuser',
        is_public: false,
      });

      const { data } = await otherClient
        .from('profiles')
        .select('*')
        .eq('id', ownerId);

      expect(data).toEqual([]);
    });
  });

  describe('INSERT policies', () => {
    it('should allow users to create their own profile', async () => {
      const { client, userId } = await users.createUser();

      const { error } = await client.from('profiles').insert({
        id: userId,
        username: `user-${Date.now()}`,
        bio: 'My bio',
      });

      expect(error).toBeNull();
    });

    it('should prevent users from creating profiles for other users', async () => {
      const { client } = await users.createUser();
      const { userId: otherUserId } = await users.createUser();

      const { error } = await client.from('profiles').insert({
        id: otherUserId,
        username: 'impersonator',
      });

      expect(error).not.toBeNull();
      expect(error!.code).toBe('42501'); // RLS violation
    });

    it('should prevent anonymous users from creating profiles', async () => {
      const anonClient = createAnonClient();

      const { error } = await anonClient.from('profiles').insert({
        id: '550e8400-e29b-41d4-a716-446655440000',
        username: 'anonymous',
      });

      expect(error).not.toBeNull();
    });
  });

  describe('UPDATE policies', () => {
    it('should allow users to update their own profile', async () => {
      const { client, userId } = await users.createUser();

      await serviceClient.from('profiles').insert({
        id: userId,
        username: `user-${Date.now()}`,
        bio: 'Original bio',
      });

      const { error } = await client
        .from('profiles')
        .update({ bio: 'Updated bio' })
        .eq('id', userId);

      expect(error).toBeNull();

      const { data } = await client
        .from('profiles')
        .select('bio')
        .eq('id', userId)
        .single();

      expect(data!.bio).toBe('Updated bio');
    });

    it('should prevent users from updating other profiles', async () => {
      const { userId: ownerId } = await users.createUser();
      const { client: attackerClient } = await users.createUser();

      await serviceClient.from('profiles').insert({
        id: ownerId,
        username: `target-${Date.now()}`,
        bio: 'Original',
      });

      const { data } = await attackerClient
        .from('profiles')
        .update({ bio: 'Hacked!' })
        .eq('id', ownerId)
        .select();

      // RLS silently filters -- no rows affected
      expect(data).toEqual([]);

      // Verify original is unchanged
      const { data: original } = await serviceClient
        .from('profiles')
        .select('bio')
        .eq('id', ownerId)
        .single();

      expect(original!.bio).toBe('Original');
    });
  });

  describe('DELETE policies', () => {
    it('should allow admins to delete profiles', async () => {
      const { client: adminClient } = await users.createAdmin();
      const { userId: targetId } = await users.createUser();

      await serviceClient.from('profiles').insert({
        id: targetId,
        username: `delete-target-${Date.now()}`,
      });

      // Admin needs their own profile for the policy check
      const adminUserId = (await adminClient.auth.getUser()).data.user!.id;
      await serviceClient.from('profiles').insert({
        id: adminUserId,
        username: `admin-${Date.now()}`,
      });

      const { error } = await adminClient
        .from('profiles')
        .delete()
        .eq('id', targetId);

      expect(error).toBeNull();
    });

    it('should prevent non-admin users from deleting profiles', async () => {
      const { client: regularClient } = await users.createUser();
      const { userId: targetId } = await users.createUser();

      await serviceClient.from('profiles').insert({
        id: targetId,
        username: `no-delete-${Date.now()}`,
      });

      const { data } = await regularClient
        .from('profiles')
        .delete()
        .eq('id', targetId)
        .select();

      // Should not delete anything
      expect(data).toEqual([]);
    });
  });
});
```

### Posts RLS Tests

```typescript
// __tests__/integration/rls/posts.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import {
  createAnonClient,
  createServiceClient,
} from '../../helpers/supabase-test-utils';
import { TestUserManager } from '../../helpers/test-users';

describe('Posts RLS Policies', () => {
  const users = new TestUserManager();
  let serviceClient: ReturnType<typeof createServiceClient>;

  beforeAll(() => {
    serviceClient = createServiceClient();
  });

  afterAll(async () => {
    await users.cleanup();
  });

  it('should allow anyone to see published posts', async () => {
    const { userId } = await users.createUser();

    await serviceClient.from('profiles').insert({
      id: userId,
      username: `author-${Date.now()}`,
    });

    await serviceClient.from('posts').insert({
      author_id: userId,
      title: 'Published Post',
      content: 'This is public',
      published: true,
    });

    const anonClient = createAnonClient();
    const { data } = await anonClient
      .from('posts')
      .select('*')
      .eq('published', true);

    expect(data!.length).toBeGreaterThan(0);
    expect(data!.some((p) => p.title === 'Published Post')).toBe(true);
  });

  it('should hide draft posts from anonymous users', async () => {
    const { userId } = await users.createUser();

    await serviceClient.from('profiles').insert({
      id: userId,
      username: `draft-author-${Date.now()}`,
    });

    const { data: insertedPost } = await serviceClient.from('posts').insert({
      author_id: userId,
      title: 'Secret Draft',
      content: 'Not published',
      published: false,
    }).select().single();

    const anonClient = createAnonClient();
    const { data } = await anonClient
      .from('posts')
      .select('*')
      .eq('id', insertedPost!.id);

    expect(data).toEqual([]);
  });

  it('should allow authors to see their own drafts', async () => {
    const { client, userId } = await users.createUser();

    await serviceClient.from('profiles').insert({
      id: userId,
      username: `my-draft-author-${Date.now()}`,
    });

    await serviceClient.from('posts').insert({
      author_id: userId,
      title: 'My Draft',
      content: 'Work in progress',
      published: false,
    });

    const { data } = await client
      .from('posts')
      .select('*')
      .eq('author_id', userId)
      .eq('published', false);

    expect(data!.length).toBeGreaterThan(0);
    expect(data![0].title).toBe('My Draft');
  });

  it('should prevent users from creating posts as another author', async () => {
    const { client } = await users.createUser();
    const { userId: otherUserId } = await users.createUser();

    const { error } = await client.from('posts').insert({
      author_id: otherUserId,
      title: 'Impersonation Post',
      content: 'Not my account',
    });

    expect(error).not.toBeNull();
  });

  it('should prevent users from updating other authors posts', async () => {
    const { userId: authorId } = await users.createUser();
    const { client: attackerClient } = await users.createUser();

    await serviceClient.from('profiles').insert({
      id: authorId,
      username: `update-target-${Date.now()}`,
    });

    const { data: post } = await serviceClient.from('posts').insert({
      author_id: authorId,
      title: 'Original Title',
      content: 'Original content',
      published: true,
    }).select().single();

    const { data } = await attackerClient
      .from('posts')
      .update({ title: 'Hacked Title' })
      .eq('id', post!.id)
      .select();

    expect(data).toEqual([]);
  });
});
```

## Auth Flow Testing

```typescript
// __tests__/integration/auth-flow.test.ts
import { describe, it, expect, afterAll } from 'vitest';
import { createAnonClient, createServiceClient } from '../helpers/supabase-test-utils';

describe('Supabase Auth Flows', () => {
  const createdUserIds: string[] = [];

  afterAll(async () => {
    const serviceClient = createServiceClient();
    for (const id of createdUserIds) {
      await serviceClient.auth.admin.deleteUser(id).catch(() => {});
    }
  });

  describe('Email/Password Sign Up', () => {
    it('should sign up a new user with email and password', async () => {
      const client = createAnonClient();
      const email = `signup-${Date.now()}@test.com`;

      const { data, error } = await client.auth.signUp({
        email,
        password: 'TestPassword123!',
      });

      expect(error).toBeNull();
      expect(data.user).toBeDefined();
      expect(data.user!.email).toBe(email);
      createdUserIds.push(data.user!.id);
    });

    it('should reject signup with weak password', async () => {
      const client = createAnonClient();

      const { error } = await client.auth.signUp({
        email: `weak-${Date.now()}@test.com`,
        password: '123',
      });

      expect(error).not.toBeNull();
    });

    it('should reject duplicate email signup', async () => {
      const client = createAnonClient();
      const email = `dup-${Date.now()}@test.com`;

      // First signup
      const { data } = await client.auth.signUp({
        email,
        password: 'TestPassword123!',
      });
      createdUserIds.push(data.user!.id);

      // Second signup with same email
      const { data: dup, error } = await client.auth.signUp({
        email,
        password: 'AnotherPassword123!',
      });

      // Supabase returns a fake user for security (no error), but no session
      expect(dup.session).toBeNull();
    });
  });

  describe('Email/Password Sign In', () => {
    it('should sign in with correct credentials', async () => {
      const serviceClient = createServiceClient();
      const email = `signin-${Date.now()}@test.com`;

      const { data: created } = await serviceClient.auth.admin.createUser({
        email,
        password: 'TestPassword123!',
        email_confirm: true,
      });
      createdUserIds.push(created.user.id);

      const client = createAnonClient();
      const { data, error } = await client.auth.signInWithPassword({
        email,
        password: 'TestPassword123!',
      });

      expect(error).toBeNull();
      expect(data.session).toBeDefined();
      expect(data.session!.access_token).toBeDefined();
      expect(data.user!.email).toBe(email);
    });

    it('should reject incorrect password', async () => {
      const serviceClient = createServiceClient();
      const email = `wrongpw-${Date.now()}@test.com`;

      const { data: created } = await serviceClient.auth.admin.createUser({
        email,
        password: 'CorrectPassword123!',
        email_confirm: true,
      });
      createdUserIds.push(created.user.id);

      const client = createAnonClient();
      const { error } = await client.auth.signInWithPassword({
        email,
        password: 'WrongPassword123!',
      });

      expect(error).not.toBeNull();
      expect(error!.message).toContain('Invalid login credentials');
    });

    it('should reject non-existent email', async () => {
      const client = createAnonClient();

      const { error } = await client.auth.signInWithPassword({
        email: 'doesnotexist@test.com',
        password: 'TestPassword123!',
      });

      expect(error).not.toBeNull();
    });
  });

  describe('Session Management', () => {
    it('should return a valid session after sign in', async () => {
      const serviceClient = createServiceClient();
      const email = `session-${Date.now()}@test.com`;

      const { data: created } = await serviceClient.auth.admin.createUser({
        email,
        password: 'TestPassword123!',
        email_confirm: true,
      });
      createdUserIds.push(created.user.id);

      const client = createAnonClient();
      await client.auth.signInWithPassword({ email, password: 'TestPassword123!' });

      const { data: sessionData } = await client.auth.getSession();
      expect(sessionData.session).not.toBeNull();
      expect(sessionData.session!.expires_at).toBeDefined();
    });

    it('should sign out and invalidate session', async () => {
      const serviceClient = createServiceClient();
      const email = `signout-${Date.now()}@test.com`;

      const { data: created } = await serviceClient.auth.admin.createUser({
        email,
        password: 'TestPassword123!',
        email_confirm: true,
      });
      createdUserIds.push(created.user.id);

      const client = createAnonClient();
      await client.auth.signInWithPassword({ email, password: 'TestPassword123!' });

      const { error } = await client.auth.signOut();
      expect(error).toBeNull();

      const { data } = await client.auth.getSession();
      expect(data.session).toBeNull();
    });
  });

  describe('User Metadata', () => {
    it('should store and retrieve user metadata', async () => {
      const serviceClient = createServiceClient();
      const email = `meta-${Date.now()}@test.com`;

      const { data: created } = await serviceClient.auth.admin.createUser({
        email,
        password: 'TestPassword123!',
        email_confirm: true,
        user_metadata: { role: 'editor', displayName: 'Test Editor' },
      });
      createdUserIds.push(created.user.id);

      const client = createAnonClient();
      await client.auth.signInWithPassword({ email, password: 'TestPassword123!' });

      const { data } = await client.auth.getUser();
      expect(data.user!.user_metadata.role).toBe('editor');
      expect(data.user!.user_metadata.displayName).toBe('Test Editor');
    });

    it('should update user metadata', async () => {
      const serviceClient = createServiceClient();
      const email = `update-meta-${Date.now()}@test.com`;

      const { data: created } = await serviceClient.auth.admin.createUser({
        email,
        password: 'TestPassword123!',
        email_confirm: true,
        user_metadata: { displayName: 'Original' },
      });
      createdUserIds.push(created.user.id);

      const client = createAnonClient();
      await client.auth.signInWithPassword({ email, password: 'TestPassword123!' });

      await client.auth.updateUser({
        data: { displayName: 'Updated' },
      });

      const { data } = await client.auth.getUser();
      expect(data.user!.user_metadata.displayName).toBe('Updated');
    });
  });
});
```

## Realtime Subscription Testing

```typescript
// __tests__/integration/realtime.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { createServiceClient } from '../helpers/supabase-test-utils';
import { TestUserManager } from '../helpers/test-users';
import type { RealtimeChannel } from '@supabase/supabase-js';

describe('Supabase Realtime Subscriptions', () => {
  const users = new TestUserManager();
  let serviceClient: ReturnType<typeof createServiceClient>;
  const channels: RealtimeChannel[] = [];

  beforeAll(() => {
    serviceClient = createServiceClient();
  });

  afterAll(async () => {
    // Unsubscribe all channels
    for (const channel of channels) {
      await channel.unsubscribe();
    }
    await users.cleanup();
  });

  it('should receive INSERT events on subscribed table', async () => {
    const { client, userId } = await users.createUser();

    await serviceClient.from('profiles').insert({
      id: userId,
      username: `realtime-${Date.now()}`,
    });

    const receivedEvents: any[] = [];

    const channel = client
      .channel('posts-inserts')
      .on(
        'postgres_changes',
        { event: 'INSERT', schema: 'public', table: 'posts' },
        (payload) => receivedEvents.push(payload)
      )
      .subscribe();

    channels.push(channel);

    // Wait for subscription to be established
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Insert a post via service client
    await serviceClient.from('posts').insert({
      author_id: userId,
      title: 'Realtime Test Post',
      content: 'Testing realtime',
      published: true,
    });

    // Wait for the event to arrive
    await new Promise((resolve) => setTimeout(resolve, 2000));

    expect(receivedEvents.length).toBeGreaterThan(0);
    expect(receivedEvents[0].new.title).toBe('Realtime Test Post');
    expect(receivedEvents[0].eventType).toBe('INSERT');
  });

  it('should receive UPDATE events', async () => {
    const { client, userId } = await users.createUser();

    await serviceClient.from('profiles').insert({
      id: userId,
      username: `rt-update-${Date.now()}`,
    });

    const { data: post } = await serviceClient.from('posts').insert({
      author_id: userId,
      title: 'Before Update',
      content: 'Original',
      published: true,
    }).select().single();

    const updateEvents: any[] = [];

    const channel = client
      .channel('posts-updates')
      .on(
        'postgres_changes',
        { event: 'UPDATE', schema: 'public', table: 'posts', filter: `id=eq.${post!.id}` },
        (payload) => updateEvents.push(payload)
      )
      .subscribe();

    channels.push(channel);

    await new Promise((resolve) => setTimeout(resolve, 1000));

    await serviceClient
      .from('posts')
      .update({ title: 'After Update' })
      .eq('id', post!.id);

    await new Promise((resolve) => setTimeout(resolve, 2000));

    expect(updateEvents.length).toBeGreaterThan(0);
    expect(updateEvents[0].new.title).toBe('After Update');
    expect(updateEvents[0].old.title).toBe('Before Update');
  });

  it('should receive DELETE events', async () => {
    const { client, userId } = await users.createUser();

    await serviceClient.from('profiles').insert({
      id: userId,
      username: `rt-delete-${Date.now()}`,
    });

    const { data: post } = await serviceClient.from('posts').insert({
      author_id: userId,
      title: 'To Be Deleted',
      content: 'Bye',
      published: true,
    }).select().single();

    const deleteEvents: any[] = [];

    const channel = client
      .channel('posts-deletes')
      .on(
        'postgres_changes',
        { event: 'DELETE', schema: 'public', table: 'posts' },
        (payload) => deleteEvents.push(payload)
      )
      .subscribe();

    channels.push(channel);

    await new Promise((resolve) => setTimeout(resolve, 1000));

    await serviceClient.from('posts').delete().eq('id', post!.id);

    await new Promise((resolve) => setTimeout(resolve, 2000));

    expect(deleteEvents.length).toBeGreaterThan(0);
    expect(deleteEvents[0].old.id).toBe(post!.id);
  });

  it('should handle channel disconnection gracefully', async () => {
    const { client } = await users.createUser();

    const channel = client
      .channel('disconnect-test')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'posts' }, () => {})
      .subscribe();

    channels.push(channel);

    await new Promise((resolve) => setTimeout(resolve, 500));

    // Unsubscribe
    const status = await channel.unsubscribe();
    expect(status).toBe('ok');
  });
});
```

## Storage Bucket Testing

```typescript
// __tests__/integration/storage.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { createServiceClient } from '../helpers/supabase-test-utils';
import { TestUserManager } from '../helpers/test-users';

describe('Supabase Storage', () => {
  const users = new TestUserManager();
  let serviceClient: ReturnType<typeof createServiceClient>;

  beforeAll(async () => {
    serviceClient = createServiceClient();

    // Ensure test bucket exists
    await serviceClient.storage.createBucket('avatars', {
      public: false,
      fileSizeLimit: 1024 * 1024, // 1MB
      allowedMimeTypes: ['image/png', 'image/jpeg', 'image/webp'],
    }).catch(() => {}); // Ignore if already exists
  });

  afterAll(async () => {
    await users.cleanup();
  });

  it('should allow authenticated users to upload to their folder', async () => {
    const { client, userId } = await users.createUser();

    const file = new Blob(['fake image data'], { type: 'image/png' });

    const { data, error } = await client.storage
      .from('avatars')
      .upload(`${userId}/avatar.png`, file, {
        contentType: 'image/png',
      });

    expect(error).toBeNull();
    expect(data!.path).toBe(`${userId}/avatar.png`);
  });

  it('should prevent users from uploading to other user folders', async () => {
    const { client } = await users.createUser();
    const { userId: otherUserId } = await users.createUser();

    const file = new Blob(['fake data'], { type: 'image/png' });

    const { error } = await client.storage
      .from('avatars')
      .upload(`${otherUserId}/malicious.png`, file, {
        contentType: 'image/png',
      });

    expect(error).not.toBeNull();
  });

  it('should enforce file size limits', async () => {
    const { client, userId } = await users.createUser();

    // Create a file larger than 1MB limit
    const largeFile = new Blob([new ArrayBuffer(2 * 1024 * 1024)], { type: 'image/png' });

    const { error } = await client.storage
      .from('avatars')
      .upload(`${userId}/too-large.png`, largeFile);

    expect(error).not.toBeNull();
  });

  it('should enforce allowed MIME types', async () => {
    const { client, userId } = await users.createUser();

    const file = new Blob(['not an image'], { type: 'application/pdf' });

    const { error } = await client.storage
      .from('avatars')
      .upload(`${userId}/doc.pdf`, file, {
        contentType: 'application/pdf',
      });

    expect(error).not.toBeNull();
  });

  it('should generate signed URLs for private files', async () => {
    const { client, userId } = await users.createUser();

    const file = new Blob(['test data'], { type: 'image/png' });
    await client.storage
      .from('avatars')
      .upload(`${userId}/signed-test.png`, file, { contentType: 'image/png' });

    const { data, error } = await client.storage
      .from('avatars')
      .createSignedUrl(`${userId}/signed-test.png`, 60);

    expect(error).toBeNull();
    expect(data!.signedUrl).toContain('token=');
  });
});
```

## Edge Function Testing

```typescript
// supabase/functions/hello-world/index.ts
import { serve } from 'https://deno.land/std@0.177.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

serve(async (req) => {
  try {
    const { name } = await req.json();

    if (!name) {
      return new Response(
        JSON.stringify({ error: 'Name is required' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Verify auth
    const authHeader = req.headers.get('Authorization');
    if (!authHeader) {
      return new Response(
        JSON.stringify({ error: 'Unauthorized' }),
        { status: 401, headers: { 'Content-Type': 'application/json' } }
      );
    }

    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_ANON_KEY')!,
      { global: { headers: { Authorization: authHeader } } }
    );

    const { data: { user } } = await supabase.auth.getUser();

    return new Response(
      JSON.stringify({ message: `Hello ${name}!`, userId: user?.id }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ error: 'Internal error' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
});
```

```typescript
// __tests__/integration/edge-functions.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { createTestUser, cleanupTestUser } from '../helpers/supabase-test-utils';

const FUNCTIONS_URL = 'http://127.0.0.1:54321/functions/v1';

describe('Edge Function: hello-world', () => {
  let accessToken: string;
  let userId: string;

  beforeAll(async () => {
    const user = await createTestUser();
    userId = user.userId;

    const { data } = await user.client.auth.getSession();
    accessToken = data.session!.access_token;
  });

  afterAll(async () => {
    await cleanupTestUser(userId);
  });

  it('should return greeting with user info', async () => {
    const response = await fetch(`${FUNCTIONS_URL}/hello-world`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify({ name: 'World' }),
    });

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.message).toBe('Hello World!');
    expect(data.userId).toBe(userId);
  });

  it('should return 400 when name is missing', async () => {
    const response = await fetch(`${FUNCTIONS_URL}/hello-world`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify({}),
    });

    expect(response.status).toBe(400);
    const data = await response.json();
    expect(data.error).toBe('Name is required');
  });

  it('should return 401 without auth header', async () => {
    const response = await fetch(`${FUNCTIONS_URL}/hello-world`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'World' }),
    });

    expect(response.status).toBe(401);
  });
});
```

## Database Migration Testing

```typescript
// supabase/tests/migrations/migration.test.ts
import { describe, it, expect, beforeAll } from 'vitest';
import { createServiceClient } from '../../__tests__/helpers/supabase-test-utils';

describe('Database Migration Verification', () => {
  let serviceClient: ReturnType<typeof createServiceClient>;

  beforeAll(() => {
    serviceClient = createServiceClient();
  });

  it('should have profiles table with correct columns', async () => {
    const { data, error } = await serviceClient.rpc('get_table_columns', {
      p_table: 'profiles',
    });

    // Alternatively, query information_schema directly
    const { data: columns } = await serviceClient
      .from('information_schema.columns' as any)
      .select('column_name, data_type, is_nullable')
      .eq('table_name', 'profiles')
      .eq('table_schema', 'public');

    const columnNames = columns!.map((c: any) => c.column_name);

    expect(columnNames).toContain('id');
    expect(columnNames).toContain('username');
    expect(columnNames).toContain('bio');
    expect(columnNames).toContain('avatar_url');
    expect(columnNames).toContain('is_public');
    expect(columnNames).toContain('created_at');
  });

  it('should have RLS enabled on all tables', async () => {
    const { data: tables } = await serviceClient.rpc('check_rls_enabled');

    // All public tables should have RLS enabled
    const publicTables = ['profiles', 'posts', 'comments'];
    for (const table of publicTables) {
      const tableInfo = tables?.find((t: any) => t.tablename === table);
      expect(tableInfo?.rowsecurity, `RLS not enabled on ${table}`).toBe(true);
    }
  });

  it('should have correct foreign key relationships', async () => {
    // Verify posts.author_id references profiles.id
    const { data: fks } = await serviceClient
      .from('information_schema.referential_constraints' as any)
      .select('constraint_name')
      .eq('constraint_schema', 'public');

    expect(fks!.length).toBeGreaterThan(0);
  });
});
```

## Best Practices

1. **Always use `supabase start` for local testing** -- Never test against production or staging Supabase instances. Local testing is fast, isolated, and free.
2. **Test every RLS policy with at least 3 roles** -- For each policy, test as the resource owner, a different authenticated user, and an anonymous user.
3. **Use the service role client for test setup only** -- Create test data with the service role client, but run actual tests with anon or authenticated clients to verify RLS.
4. **Clean up test users after each suite** -- Use a TestUserManager that tracks created users and deletes them in afterAll to prevent test database bloat.
5. **Disable email confirmation for test environments** -- Set `enable_confirmations = false` in the local config to avoid needing to handle email verification in tests.
6. **Test RLS with both SELECT and the actual operation** -- A user may be able to SELECT a row but not UPDATE or DELETE it. Test each operation independently.
7. **Verify RLS failures are silent, not errors** -- Supabase RLS violations on UPDATE/DELETE return empty results, not errors. Assert on the returned data being empty.
8. **Test realtime with proper timeouts** -- Realtime events have latency. Use adequate waits (1-2 seconds) between subscribing and expecting events.
9. **Use unique identifiers in test data** -- Include timestamps or random strings in test usernames and emails to prevent collisions between parallel test runs.
10. **Test storage policies separately from application logic** -- Storage bucket policies are independent of table RLS. Write dedicated storage tests.

## Anti-Patterns to Avoid

1. **Testing against production Supabase** -- Production testing creates real data, costs money, and risks exposing test users. Always use local instances.
2. **Using the service role client in application tests** -- The service role bypasses RLS entirely. If your tests use it for data access, they cannot verify security policies.
3. **Not testing RLS at all** -- Many teams skip RLS testing because it requires user management. This is the most critical security boundary in a Supabase app.
4. **Sharing test users between test files** -- Parallel test execution with shared users causes race conditions. Each test file should create its own users.
5. **Testing only SELECT policies** -- INSERT, UPDATE, and DELETE policies have different USING and WITH CHECK clauses. Test each operation type.
6. **Ignoring the difference between USING and WITH CHECK** -- USING filters rows you can see, WITH CHECK validates the new row on INSERT/UPDATE. Both need testing.
7. **Hardcoding Supabase keys in test files** -- Use environment variables or read from the local Supabase config. Hardcoded keys get committed to version control.
8. **Not testing auth edge cases** -- Token expiry, session refresh, and concurrent sessions are common sources of production bugs. Test these flows.
9. **Skipping migration rollback tests** -- Only testing the `up` migration is not enough. Verify that `down` migrations cleanly reverse schema changes.
10. **Testing realtime without actually subscribing** -- Mocking the realtime client misses connection issues, reconnection logic, and message ordering problems.

## Running Tests

- Start local Supabase: `supabase start`
- Run all tests: `pnpm vitest run`
- Run RLS tests: `pnpm vitest run __tests__/integration/rls`
- Run auth tests: `pnpm vitest run __tests__/integration/auth-flow.test.ts`
- Run realtime tests: `pnpm vitest run __tests__/integration/realtime.test.ts`
- Run edge function tests: `supabase functions serve && pnpm vitest run __tests__/integration/edge-functions.test.ts`
- Reset local database: `supabase db reset`
- View local Supabase dashboard: `open http://127.0.0.1:54323`
- Stop local Supabase: `supabase stop`
