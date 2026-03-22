---
name: "Remix Testing"
description: "Testing patterns for Remix applications covering loader testing, action testing, route testing, form submission testing, and nested route integration testing."
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [remix, loaders, actions, forms, nested-routes, error-boundaries, defer, streaming, sessions, msw]
testingTypes: [unit, integration, e2e]
frameworks: [vitest, playwright, jest]
languages: [typescript, javascript]
domains: [web, api]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, gemini-cli, amp]
---

# Remix Testing

You are an expert QA engineer specializing in Remix application testing patterns. When the user asks you to write, review, debug, or set up tests for Remix applications -- including loaders, actions, routes, forms, error boundaries, deferred data, sessions, and cookies -- follow these detailed instructions. You understand Remix's server-first architecture, nested routing, progressive enhancement, and the boundary between server and client concerns.

## Core Principles

1. **Loader/Action Isolation** -- Loaders and actions are plain async functions that receive a Request and return a Response. Test them as pure functions without rendering any UI. This is the most valuable layer of Remix testing.
2. **Progressive Enhancement Testing** -- Remix forms work without JavaScript. Test form submissions both with and without client-side JavaScript to ensure progressive enhancement is not broken.
3. **Nested Route Testing** -- Remix's nested routing means parent loaders run in parallel with child loaders. Test that parent and child data loading work correctly together, including error boundary cascading.
4. **Request/Response Fidelity** -- Loaders and actions use standard Web Request and Response objects. Create realistic request objects in tests with proper headers, cookies, and form data.
5. **Error Boundary Coverage** -- Every route should have error boundary tests. Test both expected errors (404, 403) and unexpected errors (thrown exceptions) to verify the correct boundary catches each error.
6. **Session Testing** -- Remix sessions are cookie-based by default. Test session creation, reading, updating, and destruction with proper cookie handling in test requests.
7. **Type-Safe Testing** -- Leverage Remix's TypeScript-first design. Use `LoaderFunctionArgs` and `ActionFunctionArgs` types in tests to ensure request construction matches the real runtime.

## When to Use This Skill

- When testing Remix loader functions that fetch and return data
- When testing Remix action functions that handle form submissions
- When testing route modules as complete units (loader + action + component)
- When testing form submissions with and without JavaScript
- When testing nested route data flow and error boundary cascading
- When testing deferred data loading with `defer` and `Await`
- When testing session and cookie management
- When writing Playwright E2E tests for full Remix application flows

## Project Structure

```
project-root/
├── app/
│   ├── routes/
│   │   ├── _index.tsx                  # Homepage route
│   │   ├── login.tsx                   # Login route (action + loader)
│   │   ├── dashboard.tsx               # Dashboard layout route
│   │   ├── dashboard._index.tsx        # Dashboard index
│   │   ├── dashboard.posts.tsx         # Posts list route
│   │   ├── dashboard.posts.$id.tsx     # Post detail route
│   │   ├── dashboard.posts.new.tsx     # Create post route
│   │   ├── dashboard.settings.tsx      # Settings route
│   │   └── api.posts.tsx               # Resource route (API)
│   ├── components/
│   │   ├── PostForm.tsx                # Post form component
│   │   ├── PostCard.tsx                # Post card component
│   │   └── ErrorFallback.tsx           # Error boundary component
│   ├── lib/
│   │   ├── db.server.ts                # Database client (server-only)
│   │   ├── auth.server.ts              # Auth utilities (server-only)
│   │   ├── session.server.ts           # Session management
│   │   └── validation.ts               # Form validation schemas
│   ├── root.tsx                        # Root route
│   └── entry.server.tsx                # Server entry
│
├── tests/
│   ├── setup/
│   │   ├── test-utils.tsx              # Test wrapper utilities
│   │   ├── request-helpers.ts          # Request construction helpers
│   │   ├── session-helpers.ts          # Session test helpers
│   │   ├── msw-handlers.ts            # MSW handlers
│   │   └── msw-server.ts             # MSW server setup
│   ├── unit/
│   │   ├── loaders/
│   │   │   ├── index.test.ts           # Homepage loader tests
│   │   │   ├── login.test.ts           # Login loader tests
│   │   │   ├── dashboard.test.ts       # Dashboard loader tests
│   │   │   └── posts.test.ts           # Posts loader tests
│   │   ├── actions/
│   │   │   ├── login.test.ts           # Login action tests
│   │   │   ├── create-post.test.ts     # Create post action tests
│   │   │   └── settings.test.ts        # Settings action tests
│   │   └── validation/
│   │       └── forms.test.ts           # Form validation tests
│   ├── integration/
│   │   ├── routes/
│   │   │   ├── login.test.tsx          # Login route integration
│   │   │   ├── dashboard.test.tsx      # Dashboard route integration
│   │   │   └── posts.test.tsx          # Posts route integration
│   │   ├── error-boundaries.test.tsx   # Error boundary tests
│   │   ├── sessions.test.ts           # Session management tests
│   │   └── nested-routes.test.tsx     # Nested route tests
│   ├── e2e/
│   │   ├── auth.spec.ts               # Auth flow E2E
│   │   ├── posts.spec.ts              # Post CRUD E2E
│   │   ├── forms.spec.ts              # Form submission E2E
│   │   └── navigation.spec.ts         # Navigation E2E
│   └── vitest.config.ts
│
├── playwright.config.ts
├── vite.config.ts
└── package.json
```

## Source Code

### Session Management

```typescript
// app/lib/session.server.ts
import { createCookieSessionStorage, redirect } from '@remix-run/node';

const sessionSecret = process.env.SESSION_SECRET;
if (!sessionSecret) throw new Error('SESSION_SECRET must be set');

const storage = createCookieSessionStorage({
  cookie: {
    name: '__session',
    httpOnly: true,
    maxAge: 60 * 60 * 24 * 30, // 30 days
    path: '/',
    sameSite: 'lax',
    secrets: [sessionSecret],
    secure: process.env.NODE_ENV === 'production',
  },
});

export async function createUserSession(userId: string, redirectTo: string) {
  const session = await storage.getSession();
  session.set('userId', userId);
  return redirect(redirectTo, {
    headers: {
      'Set-Cookie': await storage.commitSession(session),
    },
  });
}

export async function getUserSession(request: Request) {
  return storage.getSession(request.headers.get('Cookie'));
}

export async function getUserId(request: Request): Promise<string | null> {
  const session = await getUserSession(request);
  const userId = session.get('userId');
  if (!userId || typeof userId !== 'string') return null;
  return userId;
}

export async function requireUserId(request: Request): Promise<string> {
  const userId = await getUserId(request);
  if (!userId) {
    throw redirect('/login');
  }
  return userId;
}

export async function destroySession(request: Request) {
  const session = await getUserSession(request);
  return redirect('/login', {
    headers: {
      'Set-Cookie': await storage.destroySession(session),
    },
  });
}
```

### Login Route

```typescript
// app/routes/login.tsx
import type { LoaderFunctionArgs, ActionFunctionArgs } from '@remix-run/node';
import { json, redirect } from '@remix-run/node';
import { useActionData, useLoaderData, Form, useNavigation } from '@remix-run/react';
import { getUserId, createUserSession } from '~/lib/session.server';
import { validateLogin } from '~/lib/auth.server';
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  redirectTo: z.string().optional().default('/dashboard'),
});

export async function loader({ request }: LoaderFunctionArgs) {
  const userId = await getUserId(request);
  if (userId) return redirect('/dashboard');

  const url = new URL(request.url);
  const redirectTo = url.searchParams.get('redirectTo') || '/dashboard';

  return json({ redirectTo });
}

export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  const rawData = Object.fromEntries(formData);

  const result = loginSchema.safeParse(rawData);
  if (!result.success) {
    return json(
      { errors: result.error.flatten().fieldErrors, values: rawData },
      { status: 400 },
    );
  }

  const { email, password, redirectTo } = result.data;

  const user = await validateLogin(email, password);
  if (!user) {
    return json(
      {
        errors: { email: ['Invalid email or password'], password: [] },
        values: { email, redirectTo },
      },
      { status: 401 },
    );
  }

  return createUserSession(user.id, redirectTo);
}

export default function LoginRoute() {
  const { redirectTo } = useLoaderData<typeof loader>();
  const actionData = useActionData<typeof action>();
  const navigation = useNavigation();
  const isSubmitting = navigation.state === 'submitting';

  return (
    <div className="login-container">
      <h1>Login</h1>
      <Form method="post">
        <input type="hidden" name="redirectTo" value={redirectTo} />

        <div>
          <label htmlFor="email">Email</label>
          <input
            id="email"
            name="email"
            type="email"
            defaultValue={actionData?.values?.email as string}
            aria-invalid={!!actionData?.errors?.email}
            aria-errormessage="email-error"
          />
          {actionData?.errors?.email && (
            <p id="email-error" className="error">
              {actionData.errors.email[0]}
            </p>
          )}
        </div>

        <div>
          <label htmlFor="password">Password</label>
          <input
            id="password"
            name="password"
            type="password"
            aria-invalid={!!actionData?.errors?.password}
            aria-errormessage="password-error"
          />
          {actionData?.errors?.password && (
            <p id="password-error" className="error">
              {actionData.errors.password[0]}
            </p>
          )}
        </div>

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Logging in...' : 'Log in'}
        </button>
      </Form>
    </div>
  );
}

export function ErrorBoundary() {
  return (
    <div className="error-container">
      <h1>Login Error</h1>
      <p>Something went wrong. Please try again.</p>
    </div>
  );
}
```

### Posts Routes

```typescript
// app/routes/dashboard.posts.tsx
import type { LoaderFunctionArgs } from '@remix-run/node';
import { json } from '@remix-run/node';
import { useLoaderData, Outlet, Link } from '@remix-run/react';
import { requireUserId } from '~/lib/session.server';
import { getPosts } from '~/lib/db.server';

export async function loader({ request }: LoaderFunctionArgs) {
  const userId = await requireUserId(request);
  const url = new URL(request.url);
  const page = Number(url.searchParams.get('page') || '1');
  const search = url.searchParams.get('search') || '';

  const { posts, total } = await getPosts({ userId, page, search, limit: 10 });

  return json({ posts, total, page, search });
}

export default function PostsRoute() {
  const { posts, total, page, search } = useLoaderData<typeof loader>();

  return (
    <div>
      <div className="posts-header">
        <h2>Posts ({total})</h2>
        <Link to="new" className="btn-primary">
          New Post
        </Link>
      </div>
      <div className="posts-list">
        {posts.map((post) => (
          <Link key={post.id} to={post.id} className="post-card">
            <h3>{post.title}</h3>
            <p>{post.excerpt}</p>
            <span className={`badge ${post.published ? 'published' : 'draft'}`}>
              {post.published ? 'Published' : 'Draft'}
            </span>
          </Link>
        ))}
      </div>
      <Outlet />
    </div>
  );
}
```

```typescript
// app/routes/dashboard.posts.new.tsx
import type { ActionFunctionArgs } from '@remix-run/node';
import { json, redirect } from '@remix-run/node';
import { useActionData, Form, useNavigation } from '@remix-run/react';
import { requireUserId } from '~/lib/session.server';
import { createPost } from '~/lib/db.server';
import { z } from 'zod';

const postSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200, 'Title too long'),
  content: z.string().min(10, 'Content must be at least 10 characters'),
  published: z.coerce.boolean().optional().default(false),
});

export async function action({ request }: ActionFunctionArgs) {
  const userId = await requireUserId(request);
  const formData = await request.formData();
  const rawData = Object.fromEntries(formData);

  const result = postSchema.safeParse(rawData);
  if (!result.success) {
    return json(
      { errors: result.error.flatten().fieldErrors, values: rawData },
      { status: 400 },
    );
  }

  const post = await createPost({
    ...result.data,
    authorId: userId,
  });

  return redirect(`/dashboard/posts/${post.id}`);
}

export default function NewPostRoute() {
  const actionData = useActionData<typeof action>();
  const navigation = useNavigation();
  const isSubmitting = navigation.state === 'submitting';

  return (
    <div>
      <h2>Create New Post</h2>
      <Form method="post">
        <div>
          <label htmlFor="title">Title</label>
          <input
            id="title"
            name="title"
            defaultValue={actionData?.values?.title as string}
            aria-invalid={!!actionData?.errors?.title}
          />
          {actionData?.errors?.title && (
            <p className="error">{actionData.errors.title[0]}</p>
          )}
        </div>

        <div>
          <label htmlFor="content">Content</label>
          <textarea
            id="content"
            name="content"
            rows={10}
            defaultValue={actionData?.values?.content as string}
            aria-invalid={!!actionData?.errors?.content}
          />
          {actionData?.errors?.content && (
            <p className="error">{actionData.errors.content[0]}</p>
          )}
        </div>

        <div>
          <label>
            <input type="checkbox" name="published" value="true" />
            Publish immediately
          </label>
        </div>

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Creating...' : 'Create Post'}
        </button>
      </Form>
    </div>
  );
}
```

### Deferred Data Route

```typescript
// app/routes/dashboard._index.tsx
import type { LoaderFunctionArgs } from '@remix-run/node';
import { defer } from '@remix-run/node';
import { useLoaderData, Await } from '@remix-run/react';
import { Suspense } from 'react';
import { requireUserId } from '~/lib/session.server';
import { getQuickStats, getRecentActivity, getAnalytics } from '~/lib/db.server';

export async function loader({ request }: LoaderFunctionArgs) {
  const userId = await requireUserId(request);

  // Quick stats load fast -- don't defer
  const stats = await getQuickStats(userId);

  // These are slow -- defer them
  const recentActivity = getRecentActivity(userId);
  const analytics = getAnalytics(userId);

  return defer({
    stats,
    recentActivity,
    analytics,
  });
}

export default function DashboardIndex() {
  const { stats, recentActivity, analytics } = useLoaderData<typeof loader>();

  return (
    <div>
      <h1>Dashboard</h1>

      {/* Stats render immediately */}
      <div data-testid="stats">
        <p>Total Posts: {stats.totalPosts}</p>
        <p>Total Views: {stats.totalViews}</p>
      </div>

      {/* Recent activity streams in */}
      <Suspense fallback={<p data-testid="activity-loading">Loading activity...</p>}>
        <Await resolve={recentActivity}>
          {(activity) => (
            <div data-testid="recent-activity">
              {activity.map((item: any) => (
                <p key={item.id}>{item.description}</p>
              ))}
            </div>
          )}
        </Await>
      </Suspense>

      {/* Analytics streams in */}
      <Suspense fallback={<p data-testid="analytics-loading">Loading analytics...</p>}>
        <Await resolve={analytics} errorElement={<p>Failed to load analytics</p>}>
          {(data) => (
            <div data-testid="analytics">
              <p>Page views this week: {data.pageViews}</p>
            </div>
          )}
        </Await>
      </Suspense>
    </div>
  );
}
```

## Test Infrastructure

### Request Helpers

```typescript
// tests/setup/request-helpers.ts
/**
 * Create a GET request with optional URL params and headers.
 */
export function createGetRequest(
  url: string,
  options: {
    headers?: Record<string, string>;
    cookie?: string;
  } = {},
): Request {
  const headers = new Headers(options.headers);
  if (options.cookie) {
    headers.set('Cookie', options.cookie);
  }
  return new Request(url, { method: 'GET', headers });
}

/**
 * Create a POST request with form data.
 */
export function createFormRequest(
  url: string,
  data: Record<string, string>,
  options: {
    headers?: Record<string, string>;
    cookie?: string;
  } = {},
): Request {
  const formData = new URLSearchParams();
  for (const [key, value] of Object.entries(data)) {
    formData.append(key, value);
  }

  const headers = new Headers({
    'Content-Type': 'application/x-www-form-urlencoded',
    ...options.headers,
  });
  if (options.cookie) {
    headers.set('Cookie', options.cookie);
  }

  return new Request(url, {
    method: 'POST',
    headers,
    body: formData.toString(),
  });
}

/**
 * Create a multipart form request (for file uploads).
 */
export function createMultipartRequest(
  url: string,
  data: Record<string, string | File>,
  options: { cookie?: string } = {},
): Request {
  const formData = new FormData();
  for (const [key, value] of Object.entries(data)) {
    formData.append(key, value);
  }

  const headers = new Headers();
  if (options.cookie) {
    headers.set('Cookie', options.cookie);
  }

  return new Request(url, {
    method: 'POST',
    headers,
    body: formData,
  });
}

/**
 * Extract JSON body from a Remix json() response.
 */
export async function getResponseJson<T>(response: Response): Promise<T> {
  return response.json() as Promise<T>;
}

/**
 * Extract redirect location from a redirect response.
 */
export function getRedirectLocation(response: Response): string | null {
  if (response.status < 300 || response.status >= 400) return null;
  return response.headers.get('Location');
}

/**
 * Extract Set-Cookie header from response.
 */
export function getSetCookie(response: Response): string | null {
  return response.headers.get('Set-Cookie');
}
```

### Session Test Helpers

```typescript
// tests/setup/session-helpers.ts
import { createCookieSessionStorage } from '@remix-run/node';

const TEST_SESSION_SECRET = 'test-secret-for-testing-only';

const testStorage = createCookieSessionStorage({
  cookie: {
    name: '__session',
    httpOnly: true,
    path: '/',
    sameSite: 'lax',
    secrets: [TEST_SESSION_SECRET],
    secure: false,
  },
});

/**
 * Create a session cookie string for authenticated test requests.
 */
export async function createSessionCookie(userId: string): Promise<string> {
  const session = await testStorage.getSession();
  session.set('userId', userId);
  return testStorage.commitSession(session);
}

/**
 * Create a request with an authenticated session.
 */
export async function createAuthenticatedRequest(
  url: string,
  userId: string,
  options: {
    method?: string;
    body?: BodyInit;
    headers?: Record<string, string>;
  } = {},
): Promise<Request> {
  const cookie = await createSessionCookie(userId);
  const headers = new Headers(options.headers);
  headers.set('Cookie', cookie);

  return new Request(url, {
    method: options.method || 'GET',
    headers,
    body: options.body,
  });
}

/**
 * Parse a session from a Set-Cookie header.
 */
export async function parseSessionFromCookie(setCookie: string) {
  return testStorage.getSession(setCookie);
}
```

### Test Utilities

```typescript
// tests/setup/test-utils.tsx
import React from 'react';
import { render } from '@testing-library/react';
import { createRemixStub } from '@remix-run/testing';

/**
 * Create a Remix stub for route testing.
 * This renders the route component with its loader/action data.
 */
export function renderRemixRoute(
  routes: Parameters<typeof createRemixStub>[0],
  initialEntries?: string[],
) {
  const RemixStub = createRemixStub(routes);
  return render(
    <RemixStub initialEntries={initialEntries || ['/']} />,
  );
}
```

## Unit Tests

### Loader Tests

```typescript
// tests/unit/loaders/login.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { loader } from '../../../app/routes/login';
import { createGetRequest } from '../../setup/request-helpers';

// Mock session utilities
vi.mock('~/lib/session.server', () => ({
  getUserId: vi.fn(),
}));

import { getUserId } from '~/lib/session.server';

describe('Login Loader', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should return redirectTo from search params', async () => {
    vi.mocked(getUserId).mockResolvedValue(null);

    const request = createGetRequest('http://localhost/login?redirectTo=/settings');
    const response = await loader({
      request,
      params: {},
      context: {},
    });

    const data = await response.json();
    expect(data.redirectTo).toBe('/settings');
  });

  it('should default redirectTo to /dashboard', async () => {
    vi.mocked(getUserId).mockResolvedValue(null);

    const request = createGetRequest('http://localhost/login');
    const response = await loader({
      request,
      params: {},
      context: {},
    });

    const data = await response.json();
    expect(data.redirectTo).toBe('/dashboard');
  });

  it('should redirect authenticated users to /dashboard', async () => {
    vi.mocked(getUserId).mockResolvedValue('user-123');

    const request = createGetRequest('http://localhost/login');
    const response = await loader({
      request,
      params: {},
      context: {},
    });

    expect(response.status).toBe(302);
    expect(response.headers.get('Location')).toBe('/dashboard');
  });
});
```

```typescript
// tests/unit/loaders/posts.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { loader } from '../../../app/routes/dashboard.posts';
import { createGetRequest } from '../../setup/request-helpers';

vi.mock('~/lib/session.server', () => ({
  requireUserId: vi.fn(),
}));

vi.mock('~/lib/db.server', () => ({
  getPosts: vi.fn(),
}));

import { requireUserId } from '~/lib/session.server';
import { getPosts } from '~/lib/db.server';

describe('Posts Loader', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(requireUserId).mockResolvedValue('user-123');
  });

  it('should load posts for authenticated user', async () => {
    vi.mocked(getPosts).mockResolvedValue({
      posts: [
        { id: '1', title: 'Post 1', excerpt: 'Excerpt 1', published: true },
        { id: '2', title: 'Post 2', excerpt: 'Excerpt 2', published: false },
      ],
      total: 2,
    });

    const request = createGetRequest('http://localhost/dashboard/posts');
    const response = await loader({ request, params: {}, context: {} });
    const data = await response.json();

    expect(data.posts).toHaveLength(2);
    expect(data.total).toBe(2);
    expect(data.page).toBe(1);
  });

  it('should pass pagination params to getPosts', async () => {
    vi.mocked(getPosts).mockResolvedValue({ posts: [], total: 0 });

    const request = createGetRequest('http://localhost/dashboard/posts?page=3&search=remix');
    await loader({ request, params: {}, context: {} });

    expect(getPosts).toHaveBeenCalledWith({
      userId: 'user-123',
      page: 3,
      search: 'remix',
      limit: 10,
    });
  });

  it('should redirect unauthenticated users', async () => {
    vi.mocked(requireUserId).mockRejectedValue(
      new Response(null, { status: 302, headers: { Location: '/login' } }),
    );

    const request = createGetRequest('http://localhost/dashboard/posts');

    try {
      await loader({ request, params: {}, context: {} });
      expect.unreachable('Should have thrown redirect');
    } catch (response: any) {
      expect(response.status).toBe(302);
      expect(response.headers.get('Location')).toBe('/login');
    }
  });
});
```

### Action Tests

```typescript
// tests/unit/actions/login.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { action } from '../../../app/routes/login';
import { createFormRequest, getResponseJson, getRedirectLocation } from '../../setup/request-helpers';

vi.mock('~/lib/auth.server', () => ({
  validateLogin: vi.fn(),
}));

vi.mock('~/lib/session.server', () => ({
  createUserSession: vi.fn(),
}));

import { validateLogin } from '~/lib/auth.server';
import { createUserSession } from '~/lib/session.server';

describe('Login Action', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should return validation errors for invalid email', async () => {
    const request = createFormRequest('http://localhost/login', {
      email: 'not-an-email',
      password: 'password123',
    });

    const response = await action({ request, params: {}, context: {} });
    const data = await getResponseJson<any>(response);

    expect(response.status).toBe(400);
    expect(data.errors.email).toBeDefined();
    expect(data.errors.email[0]).toContain('email');
  });

  it('should return validation errors for short password', async () => {
    const request = createFormRequest('http://localhost/login', {
      email: 'test@example.com',
      password: 'short',
    });

    const response = await action({ request, params: {}, context: {} });
    const data = await getResponseJson<any>(response);

    expect(response.status).toBe(400);
    expect(data.errors.password).toBeDefined();
  });

  it('should return 401 for invalid credentials', async () => {
    vi.mocked(validateLogin).mockResolvedValue(null);

    const request = createFormRequest('http://localhost/login', {
      email: 'test@example.com',
      password: 'wrongpassword',
    });

    const response = await action({ request, params: {}, context: {} });
    const data = await getResponseJson<any>(response);

    expect(response.status).toBe(401);
    expect(data.errors.email[0]).toContain('Invalid');
  });

  it('should create session and redirect on valid login', async () => {
    vi.mocked(validateLogin).mockResolvedValue({ id: 'user-123', email: 'test@example.com' });
    vi.mocked(createUserSession).mockResolvedValue(
      new Response(null, {
        status: 302,
        headers: { Location: '/dashboard' },
      }),
    );

    const request = createFormRequest('http://localhost/login', {
      email: 'test@example.com',
      password: 'password123',
    });

    const response = await action({ request, params: {}, context: {} });

    expect(createUserSession).toHaveBeenCalledWith('user-123', '/dashboard');
    expect(response.status).toBe(302);
    expect(getRedirectLocation(response)).toBe('/dashboard');
  });

  it('should respect custom redirectTo parameter', async () => {
    vi.mocked(validateLogin).mockResolvedValue({ id: 'user-123', email: 'test@example.com' });
    vi.mocked(createUserSession).mockImplementation(async (_userId, redirectTo) => {
      return new Response(null, {
        status: 302,
        headers: { Location: redirectTo },
      });
    });

    const request = createFormRequest('http://localhost/login', {
      email: 'test@example.com',
      password: 'password123',
      redirectTo: '/settings',
    });

    const response = await action({ request, params: {}, context: {} });

    expect(getRedirectLocation(response)).toBe('/settings');
  });

  it('should preserve email in form values on error', async () => {
    vi.mocked(validateLogin).mockResolvedValue(null);

    const request = createFormRequest('http://localhost/login', {
      email: 'test@example.com',
      password: 'wrongpassword',
    });

    const response = await action({ request, params: {}, context: {} });
    const data = await getResponseJson<any>(response);

    expect(data.values.email).toBe('test@example.com');
  });
});
```

```typescript
// tests/unit/actions/create-post.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { action } from '../../../app/routes/dashboard.posts.new';
import { createFormRequest, getResponseJson, getRedirectLocation } from '../../setup/request-helpers';

vi.mock('~/lib/session.server', () => ({
  requireUserId: vi.fn(),
}));

vi.mock('~/lib/db.server', () => ({
  createPost: vi.fn(),
}));

import { requireUserId } from '~/lib/session.server';
import { createPost } from '~/lib/db.server';

describe('Create Post Action', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(requireUserId).mockResolvedValue('user-123');
  });

  it('should create post and redirect to it', async () => {
    vi.mocked(createPost).mockResolvedValue({ id: 'post-456' });

    const request = createFormRequest('http://localhost/dashboard/posts/new', {
      title: 'My New Post',
      content: 'This is the content of my new post.',
    });

    const response = await action({ request, params: {}, context: {} });

    expect(createPost).toHaveBeenCalledWith({
      title: 'My New Post',
      content: 'This is the content of my new post.',
      published: false,
      authorId: 'user-123',
    });
    expect(response.status).toBe(302);
    expect(getRedirectLocation(response)).toBe('/dashboard/posts/post-456');
  });

  it('should return validation errors for empty title', async () => {
    const request = createFormRequest('http://localhost/dashboard/posts/new', {
      title: '',
      content: 'This is content that is long enough.',
    });

    const response = await action({ request, params: {}, context: {} });
    const data = await getResponseJson<any>(response);

    expect(response.status).toBe(400);
    expect(data.errors.title).toBeDefined();
  });

  it('should return validation errors for short content', async () => {
    const request = createFormRequest('http://localhost/dashboard/posts/new', {
      title: 'Valid Title',
      content: 'Short',
    });

    const response = await action({ request, params: {}, context: {} });
    const data = await getResponseJson<any>(response);

    expect(response.status).toBe(400);
    expect(data.errors.content).toBeDefined();
  });

  it('should handle published checkbox', async () => {
    vi.mocked(createPost).mockResolvedValue({ id: 'post-789' });

    const request = createFormRequest('http://localhost/dashboard/posts/new', {
      title: 'Published Post',
      content: 'Content that will be published immediately.',
      published: 'true',
    });

    await action({ request, params: {}, context: {} });

    expect(createPost).toHaveBeenCalledWith(
      expect.objectContaining({ published: true }),
    );
  });
});
```

### Form Validation Tests

```typescript
// tests/unit/validation/forms.test.ts
import { describe, it, expect } from 'vitest';
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  redirectTo: z.string().optional().default('/dashboard'),
});

const postSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200, 'Title too long'),
  content: z.string().min(10, 'Content must be at least 10 characters'),
  published: z.coerce.boolean().optional().default(false),
});

describe('Form Validation Schemas', () => {
  describe('loginSchema', () => {
    it('should accept valid login data', () => {
      const result = loginSchema.safeParse({
        email: 'test@example.com',
        password: 'password123',
      });
      expect(result.success).toBe(true);
    });

    it('should reject invalid email', () => {
      const result = loginSchema.safeParse({
        email: 'not-an-email',
        password: 'password123',
      });
      expect(result.success).toBe(false);
    });

    it('should reject short password', () => {
      const result = loginSchema.safeParse({
        email: 'test@example.com',
        password: '1234567',
      });
      expect(result.success).toBe(false);
    });

    it('should default redirectTo to /dashboard', () => {
      const result = loginSchema.parse({
        email: 'test@example.com',
        password: 'password123',
      });
      expect(result.redirectTo).toBe('/dashboard');
    });
  });

  describe('postSchema', () => {
    it('should accept valid post data', () => {
      const result = postSchema.safeParse({
        title: 'My Post',
        content: 'This is enough content for validation.',
      });
      expect(result.success).toBe(true);
    });

    it('should reject empty title', () => {
      const result = postSchema.safeParse({
        title: '',
        content: 'Valid content here.',
      });
      expect(result.success).toBe(false);
    });

    it('should coerce published string to boolean', () => {
      const result = postSchema.parse({
        title: 'Post',
        content: 'Content that is long enough.',
        published: 'true',
      });
      expect(result.published).toBe(true);
    });

    it('should default published to false', () => {
      const result = postSchema.parse({
        title: 'Post',
        content: 'Content that is long enough.',
      });
      expect(result.published).toBe(false);
    });
  });
});
```

## Integration Tests

### Session Integration Tests

```typescript
// tests/integration/sessions.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createSessionCookie, parseSessionFromCookie } from '../setup/session-helpers';

// Note: These tests use the test session storage, not the production one.
// For true integration tests, test against the real session.server module
// with a test SESSION_SECRET environment variable.

describe('Session Management', () => {
  it('should create a session cookie with userId', async () => {
    const cookie = await createSessionCookie('user-123');
    expect(cookie).toBeDefined();
    expect(cookie).toContain('__session=');
  });

  it('should parse userId from session cookie', async () => {
    const cookie = await createSessionCookie('user-456');
    const session = await parseSessionFromCookie(cookie);

    expect(session.get('userId')).toBe('user-456');
  });

  it('should handle empty session', async () => {
    const session = await parseSessionFromCookie('');
    expect(session.get('userId')).toBeUndefined();
  });

  it('should handle corrupted session cookie', async () => {
    const session = await parseSessionFromCookie('__session=invalid-data');
    expect(session.get('userId')).toBeUndefined();
  });
});
```

### Error Boundary Tests

```typescript
// tests/integration/error-boundaries.test.tsx
import { describe, it, expect } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderRemixRoute } from '../setup/test-utils';

describe('Error Boundaries', () => {
  it('should render route error boundary on loader error', async () => {
    renderRemixRoute(
      [
        {
          path: '/',
          Component: () => <div>Should not render</div>,
          ErrorBoundary: () => <div data-testid="error">Route Error</div>,
          loader: () => {
            throw new Error('Loader failed');
          },
        },
      ],
      ['/'],
    );

    await waitFor(() => {
      expect(screen.getByTestId('error')).toHaveTextContent('Route Error');
    });
  });

  it('should render parent error boundary when child has none', async () => {
    renderRemixRoute(
      [
        {
          path: '/',
          Component: () => (
            <div>
              <h1>Parent</h1>
              {/* Outlet for child routes */}
            </div>
          ),
          ErrorBoundary: () => <div data-testid="parent-error">Parent Caught Error</div>,
          children: [
            {
              path: 'child',
              Component: () => <div>Child</div>,
              loader: () => {
                throw new Error('Child loader failed');
              },
              // No ErrorBoundary -- bubbles up to parent
            },
          ],
        },
      ],
      ['/child'],
    );

    await waitFor(() => {
      expect(screen.getByTestId('parent-error')).toHaveTextContent('Parent Caught Error');
    });
  });

  it('should render 404 for unknown routes', async () => {
    renderRemixRoute(
      [
        {
          path: '/',
          Component: () => <div>Home</div>,
          ErrorBoundary: () => <div data-testid="not-found">Page Not Found</div>,
        },
      ],
      ['/unknown-route'],
    );

    await waitFor(() => {
      expect(screen.getByTestId('not-found')).toBeInTheDocument();
    });
  });
});
```

### Route Integration Tests

```typescript
// tests/integration/routes/login.test.tsx
import { describe, it, expect } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { renderRemixRoute } from '../../setup/test-utils';

describe('Login Route Integration', () => {
  it('should render login form', async () => {
    renderRemixRoute(
      [
        {
          path: '/login',
          Component: () => (
            <form method="post">
              <label htmlFor="email">Email</label>
              <input id="email" name="email" type="email" />
              <label htmlFor="password">Password</label>
              <input id="password" name="password" type="password" />
              <button type="submit">Log in</button>
            </form>
          ),
          loader: () => ({ redirectTo: '/dashboard' }),
        },
      ],
      ['/login'],
    );

    await waitFor(() => {
      expect(screen.getByLabelText('Email')).toBeInTheDocument();
      expect(screen.getByLabelText('Password')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: 'Log in' })).toBeInTheDocument();
    });
  });

  it('should display validation errors from action', async () => {
    renderRemixRoute(
      [
        {
          path: '/login',
          Component: () => {
            // Simplified component for testing
            return (
              <div>
                <p className="error">Invalid email address</p>
              </div>
            );
          },
          loader: () => ({ redirectTo: '/dashboard' }),
          action: async () => {
            return Response.json(
              { errors: { email: ['Invalid email address'] } },
              { status: 400 },
            );
          },
        },
      ],
      ['/login'],
    );

    await waitFor(() => {
      expect(screen.getByText('Invalid email address')).toBeInTheDocument();
    });
  });
});
```

## E2E Tests

### Auth Flow E2E

```typescript
// tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test('should login with valid credentials', async ({ page }) => {
    await page.goto('/login');

    await page.fill('#email', 'test@example.com');
    await page.fill('#password', 'password123');
    await page.click('button[type="submit"]');

    await page.waitForURL('/dashboard');
    expect(page.url()).toContain('/dashboard');
  });

  test('should show validation errors for invalid input', async ({ page }) => {
    await page.goto('/login');

    await page.fill('#email', 'invalid');
    await page.fill('#password', 'short');
    await page.click('button[type="submit"]');

    await expect(page.locator('.error')).toBeVisible();
  });

  test('should work without JavaScript (progressive enhancement)', async ({ page, context }) => {
    // Disable JavaScript
    await context.route('**/*.js', (route) => route.abort());

    await page.goto('/login');

    await page.fill('#email', 'test@example.com');
    await page.fill('#password', 'password123');
    await page.click('button[type="submit"]');

    // Form should still submit via standard HTML form
    await page.waitForURL('/dashboard');
    expect(page.url()).toContain('/dashboard');
  });

  test('should redirect to requested page after login', async ({ page }) => {
    await page.goto('/login?redirectTo=/settings');

    await page.fill('#email', 'test@example.com');
    await page.fill('#password', 'password123');
    await page.click('button[type="submit"]');

    await page.waitForURL('/settings');
  });

  test('should protect dashboard from unauthenticated access', async ({ page }) => {
    await page.goto('/dashboard');
    await page.waitForURL(/\/login/);
    expect(page.url()).toContain('/login');
  });

  test('should logout and redirect to login', async ({ page }) => {
    // First login
    await page.goto('/login');
    await page.fill('#email', 'test@example.com');
    await page.fill('#password', 'password123');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');

    // Then logout
    await page.click('[data-testid="logout-button"]');
    await page.waitForURL('/login');
  });
});
```

### Post CRUD E2E

```typescript
// tests/e2e/posts.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Post CRUD Operations', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login');
    await page.fill('#email', 'test@example.com');
    await page.fill('#password', 'password123');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');
  });

  test('should create a new post', async ({ page }) => {
    await page.goto('/dashboard/posts/new');

    await page.fill('#title', 'E2E Test Post');
    await page.fill('#content', 'This is a post created by an end-to-end test.');
    await page.click('button[type="submit"]');

    // Should redirect to the new post
    await page.waitForURL(/\/dashboard\/posts\/.+/);
    await expect(page.locator('h1')).toContainText('E2E Test Post');
  });

  test('should display validation errors on form', async ({ page }) => {
    await page.goto('/dashboard/posts/new');

    // Submit empty form
    await page.click('button[type="submit"]');

    await expect(page.locator('.error')).toBeVisible();
  });

  test('should list posts on dashboard', async ({ page }) => {
    await page.goto('/dashboard/posts');

    await expect(page.locator('.posts-list')).toBeVisible();
    const postCards = page.locator('.post-card');
    await expect(postCards.first()).toBeVisible();
  });

  test('should search posts', async ({ page }) => {
    await page.goto('/dashboard/posts?search=test');

    await page.waitForLoadState('networkidle');
    // Results should be filtered
    const postCards = page.locator('.post-card');
    const count = await postCards.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });

  test('should navigate between post list and detail', async ({ page }) => {
    await page.goto('/dashboard/posts');

    // Click first post
    await page.locator('.post-card').first().click();

    // Should navigate to detail view
    await page.waitForURL(/\/dashboard\/posts\/.+/);
    await expect(page.locator('h1')).toBeVisible();

    // Navigate back
    await page.goBack();
    await page.waitForURL('/dashboard/posts');
  });
});
```

### Form Submission E2E

```typescript
// tests/e2e/forms.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Form Submissions', () => {
  test('should show loading state during form submission', async ({ page }) => {
    await page.goto('/login');

    await page.fill('#email', 'test@example.com');
    await page.fill('#password', 'password123');

    // Start submission and check for loading state
    const submitButton = page.getByRole('button', { name: 'Log in' });
    await submitButton.click();

    // Button should show loading text briefly
    // Note: This may be too fast to catch without network throttling
    await page.waitForURL('/dashboard');
  });

  test('should handle form resubmission after error', async ({ page }) => {
    await page.goto('/login');

    // First attempt with wrong password
    await page.fill('#email', 'test@example.com');
    await page.fill('#password', 'wrong');
    await page.click('button[type="submit"]');

    await expect(page.locator('.error')).toBeVisible();

    // Second attempt with correct password
    await page.fill('#password', 'password123');
    await page.click('button[type="submit"]');

    await page.waitForURL('/dashboard');
  });

  test('should preserve form values after validation error', async ({ page }) => {
    await page.goto('/dashboard/posts/new');

    await page.fill('#title', 'Valid Title');
    await page.fill('#content', 'Short'); // Too short
    await page.click('button[type="submit"]');

    // Title should still be filled
    const titleValue = await page.inputValue('#title');
    expect(titleValue).toBe('Valid Title');
  });
});
```

## Vitest Configuration

```typescript
// tests/vitest.config.ts
import { defineConfig } from 'vitest/config';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [tsconfigPaths()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./tests/setup/vitest-setup.ts'],
    include: ['tests/**/*.test.{ts,tsx}'],
    exclude: ['tests/e2e/**'],
    coverage: {
      provider: 'v8',
      include: ['app/routes/**', 'app/lib/**'],
    },
  },
});
```

## Best Practices

1. **Test loaders and actions as standalone functions** -- they receive a Request and return a Response. This is the highest-value test layer in Remix because it validates server logic without rendering UI.
2. **Use standard Web Request/Response in tests** -- Remix uses Web standard APIs. Create real Request objects with proper headers, cookies, and form data rather than mocking framework internals.
3. **Test progressive enhancement** -- run critical E2E tests with JavaScript disabled to verify that forms submit correctly via standard HTML form behavior.
4. **Test redirect responses explicitly** -- loaders and actions frequently redirect. Assert both the status code (302/303) and the Location header value.
5. **Mock server-only modules at the module level** -- use `vi.mock('~/lib/db.server')` to replace database calls. Remix's `.server.ts` convention makes it clear which modules need mocking.
6. **Test error boundary cascading** -- verify that errors in child routes bubble up to the nearest parent error boundary. Test both the child and parent boundary behavior.
7. **Use createRemixStub for route integration tests** -- Remix provides `createRemixStub` for rendering routes with their loaders and actions in a test environment.
8. **Test session cookie round-trips** -- verify that session creation produces a valid cookie, and that cookie parsing recovers the session data correctly.
9. **Test form data with URLSearchParams** -- Remix forms submit as `application/x-www-form-urlencoded`. Use `URLSearchParams` to construct form data in test requests.
10. **Test deferred data with Suspense boundaries** -- verify that deferred data shows loading fallbacks initially and resolves to the correct content.

## Anti-Patterns

1. **Mocking the Remix runtime** -- never mock `useLoaderData`, `useActionData`, or `Form`. Test through the real Remix APIs to catch integration issues.
2. **Testing UI without testing loaders** -- rendering components with hardcoded data skips the most important part of Remix: the server data flow. Always test loaders first.
3. **Using fake Request objects** -- creating plain objects `{ url: '...', method: 'GET' }` instead of real `new Request()` instances misses header, cookie, and body parsing behavior.
4. **Ignoring redirect responses in action tests** -- successful actions often redirect. Treating redirects as errors or ignoring them misses the primary success path.
5. **Not testing form validation at the schema level** -- Zod schemas are the first line of defense. Test them independently before testing the action that uses them.
6. **Sharing session state between tests** -- each test should create its own session cookie. Shared sessions cause order-dependent test failures.
7. **Only testing with JavaScript enabled** -- Remix's progressive enhancement is a core feature. If you only test the JavaScript-enhanced path, you miss HTML form submission bugs.
8. **Not testing the action's response status codes** -- a 400 validation error and a 401 auth error should be distinguishable. Always assert response.status.
9. **Testing route components in isolation from their loaders** -- Remix components are designed to consume loader data. Testing them with mock props bypasses the data contract.
10. **Ignoring defer/Await error boundaries** -- deferred data can reject. Test that the `errorElement` on `<Await>` renders correctly when the promise rejects.
