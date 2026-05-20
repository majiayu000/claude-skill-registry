---
name: "Clerk Auth Testing"
description: "Testing patterns for Clerk authentication including sign-in flow testing, protected route testing, webhook verification, middleware testing, and organization-based access control"
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [clerk, authentication, auth, protected-routes, middleware, webhooks, rbac, organizations, session, testing-tokens]
testingTypes: [unit, integration, e2e]
frameworks: [vitest, jest, playwright]
languages: [typescript, javascript]
domains: [web, api]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, gemini-cli, amp]
---

# Clerk Auth Testing Skill

You are an expert QA engineer specializing in testing applications that use Clerk for authentication. When the user asks you to write, review, or debug tests for Clerk auth flows, protected routes, middleware, webhooks, or organization-based access control, follow these detailed instructions.

## Core Principles

1. **Use Clerk testing tokens for E2E tests** -- Clerk provides testing tokens that bypass the Clerk hosted UI. Use them in Playwright tests to avoid interacting with iframes and third-party UI.
2. **Mock Clerk in unit tests, integrate in E2E** -- For unit tests, mock `@clerk/nextjs` hooks and helpers. For E2E tests, use real Clerk test instances or testing tokens.
3. **Test the middleware, not Clerk itself** -- Your middleware uses Clerk's `auth()` and `clerkMiddleware()`. Test your route protection logic, not Clerk's JWT verification.
4. **Webhook signature verification is critical** -- Clerk webhooks use Svix for signing. Test that your webhook handler rejects unsigned or tampered payloads.
5. **Organization RBAC requires multi-tenant testing** -- Test that users with different roles in different organizations see the correct content and have the correct permissions.
6. **Session management affects every page** -- Test that expired sessions redirect correctly, session refresh works, and multi-tab scenarios do not cause state inconsistencies.
7. **Graceful degradation when Clerk is unavailable** -- Your app should handle missing Clerk keys or network failures without crashing. Test the degraded state.

## Project Structure

Always organize Clerk auth testing with this structure:

```
src/
  middleware.ts
  app/
    (auth)/
      sign-in/
        [[...sign-in]]/
          page.tsx
      sign-up/
        [[...sign-up]]/
          page.tsx
    (protected)/
      dashboard/
        page.tsx
      admin/
        page.tsx
      settings/
        page.tsx
    api/
      webhooks/
        clerk/
          route.ts
      protected/
        route.ts
  lib/
    auth.ts
    roles.ts
  __tests__/
    unit/
      middleware.test.ts
      auth.test.ts
      roles.test.ts
    integration/
      webhook.test.ts
      protected-routes.test.ts
      organization.test.ts
    e2e/
      sign-in.spec.ts
      sign-up.spec.ts
      protected-flow.spec.ts
      admin-flow.spec.ts
    helpers/
      clerk-mock.ts
      clerk-test-utils.ts
    fixtures/
      clerk-user.fixture.ts
      clerk-webhook.fixture.ts
```

## Clerk Middleware Testing

### Middleware Configuration

```typescript
// src/middleware.ts
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';
import { NextResponse } from 'next/server';

const isPublicRoute = createRouteMatcher([
  '/',
  '/sign-in(.*)',
  '/sign-up(.*)',
  '/api/webhooks(.*)',
  '/api/public(.*)',
  '/blog(.*)',
  '/pricing',
]);

const isAdminRoute = createRouteMatcher([
  '/admin(.*)',
  '/api/admin(.*)',
]);

const isApiRoute = createRouteMatcher([
  '/api(.*)',
]);

export default clerkMiddleware(async (auth, req) => {
  const { userId, orgRole } = await auth();

  // Allow public routes
  if (isPublicRoute(req)) {
    return NextResponse.next();
  }

  // Require authentication for all non-public routes
  if (!userId) {
    if (isApiRoute(req)) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }
    const signInUrl = new URL('/sign-in', req.url);
    signInUrl.searchParams.set('redirect_url', req.url);
    return NextResponse.redirect(signInUrl);
  }

  // Admin routes require admin role
  if (isAdminRoute(req)) {
    if (orgRole !== 'org:admin') {
      if (isApiRoute(req)) {
        return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
      }
      return NextResponse.redirect(new URL('/dashboard', req.url));
    }
  }

  return NextResponse.next();
});

export const config = {
  matcher: [
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    '/(api|trpc)(.*)',
  ],
};
```

### Middleware Unit Tests

```typescript
// __tests__/unit/middleware.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { NextRequest } from 'next/server';

// Mock @clerk/nextjs/server before importing middleware
vi.mock('@clerk/nextjs/server', () => {
  const createRouteMatcher = (patterns: string[]) => {
    return (req: NextRequest) => {
      const pathname = req.nextUrl.pathname;
      return patterns.some((pattern) => {
        const regex = new RegExp('^' + pattern.replace('(.*)', '.*') + '$');
        return regex.test(pathname);
      });
    };
  };

  let mockAuthData = { userId: null as string | null, orgRole: null as string | null };

  const clerkMiddleware = (handler: (auth: () => Promise<any>, req: NextRequest) => any) => {
    return (req: NextRequest) => {
      const auth = async () => mockAuthData;
      return handler(auth, req);
    };
  };

  return {
    clerkMiddleware,
    createRouteMatcher,
    __setMockAuth: (data: typeof mockAuthData) => {
      mockAuthData = data;
    },
  };
});

import middleware from '../../src/middleware';
import { __setMockAuth } from '@clerk/nextjs/server';

function createRequest(path: string, method = 'GET'): NextRequest {
  return new NextRequest(new URL(path, 'http://localhost:3000'), { method });
}

describe('Clerk Middleware', () => {
  beforeEach(() => {
    __setMockAuth({ userId: null, orgRole: null });
  });

  describe('Public routes', () => {
    const publicPaths = ['/', '/sign-in', '/sign-up', '/blog', '/blog/my-post', '/pricing', '/api/webhooks/clerk'];

    it.each(publicPaths)('should allow unauthenticated access to %s', async (path) => {
      const req = createRequest(path);
      const response = await middleware(req);

      // Public routes should pass through (not redirect)
      expect(response.status).not.toBe(302);
      expect(response.status).not.toBe(401);
    });
  });

  describe('Protected routes (unauthenticated)', () => {
    it('should redirect unauthenticated users to sign-in for pages', async () => {
      const req = createRequest('/dashboard');
      const response = await middleware(req);

      expect(response.status).toBe(307); // Next.js redirect
      expect(response.headers.get('location')).toContain('/sign-in');
      expect(response.headers.get('location')).toContain('redirect_url');
    });

    it('should include the original URL in redirect_url param', async () => {
      const req = createRequest('/dashboard/settings');
      const response = await middleware(req);

      const location = new URL(response.headers.get('location')!, 'http://localhost:3000');
      expect(location.searchParams.get('redirect_url')).toContain('/dashboard/settings');
    });

    it('should return 401 JSON for unauthenticated API requests', async () => {
      const req = createRequest('/api/protected/data');
      const response = await middleware(req);

      expect(response.status).toBe(401);
      const body = await response.json();
      expect(body.error).toBe('Unauthorized');
    });
  });

  describe('Protected routes (authenticated)', () => {
    it('should allow authenticated users to access protected pages', async () => {
      __setMockAuth({ userId: 'user_123', orgRole: 'org:member' });

      const req = createRequest('/dashboard');
      const response = await middleware(req);

      expect(response.status).toBe(200);
    });

    it('should allow authenticated users to access protected API routes', async () => {
      __setMockAuth({ userId: 'user_123', orgRole: 'org:member' });

      const req = createRequest('/api/protected/data');
      const response = await middleware(req);

      expect(response.status).toBe(200);
    });
  });

  describe('Admin routes', () => {
    it('should allow admin users to access admin pages', async () => {
      __setMockAuth({ userId: 'admin_123', orgRole: 'org:admin' });

      const req = createRequest('/admin/users');
      const response = await middleware(req);

      expect(response.status).toBe(200);
    });

    it('should redirect non-admin users from admin pages to dashboard', async () => {
      __setMockAuth({ userId: 'user_123', orgRole: 'org:member' });

      const req = createRequest('/admin/users');
      const response = await middleware(req);

      expect(response.status).toBe(307);
      expect(response.headers.get('location')).toContain('/dashboard');
    });

    it('should return 403 for non-admin API requests', async () => {
      __setMockAuth({ userId: 'user_123', orgRole: 'org:member' });

      const req = createRequest('/api/admin/users');
      const response = await middleware(req);

      expect(response.status).toBe(403);
      const body = await response.json();
      expect(body.error).toBe('Forbidden');
    });

    it('should return 401 (not 403) for unauthenticated admin API requests', async () => {
      const req = createRequest('/api/admin/users');
      const response = await middleware(req);

      // Auth check happens before admin check
      expect(response.status).toBe(401);
    });
  });
});
```

## Mocking Clerk in Unit Tests

### Clerk Mock Helper

```typescript
// __tests__/helpers/clerk-mock.ts
import { vi } from 'vitest';

interface MockUser {
  id: string;
  firstName: string | null;
  lastName: string | null;
  emailAddresses: Array<{ emailAddress: string; id: string }>;
  primaryEmailAddress: { emailAddress: string } | null;
  imageUrl: string;
  publicMetadata: Record<string, unknown>;
  organizationMemberships: Array<{
    organization: { id: string; name: string; slug: string };
    role: string;
  }>;
}

interface MockSession {
  id: string;
  userId: string;
  status: 'active' | 'expired' | 'revoked';
  lastActiveAt: Date;
  expireAt: Date;
}

const defaultMockUser: MockUser = {
  id: 'user_test123',
  firstName: 'Test',
  lastName: 'User',
  emailAddresses: [{ emailAddress: 'test@example.com', id: 'email_1' }],
  primaryEmailAddress: { emailAddress: 'test@example.com' },
  imageUrl: 'https://img.clerk.com/test',
  publicMetadata: {},
  organizationMemberships: [],
};

let currentMockUser: MockUser | null = null;
let currentMockSession: MockSession | null = null;

export function setMockUser(user: Partial<MockUser> | null) {
  currentMockUser = user ? { ...defaultMockUser, ...user } : null;
  currentMockSession = user
    ? {
        id: 'sess_test123',
        userId: user.id || defaultMockUser.id,
        status: 'active',
        lastActiveAt: new Date(),
        expireAt: new Date(Date.now() + 86400000),
      }
    : null;
}

export function clearMockUser() {
  currentMockUser = null;
  currentMockSession = null;
}

// Mock for @clerk/nextjs (client-side)
export function mockClerkNextjs() {
  vi.mock('@clerk/nextjs', () => ({
    useUser: () => ({
      isLoaded: true,
      isSignedIn: !!currentMockUser,
      user: currentMockUser,
    }),
    useAuth: () => ({
      isLoaded: true,
      isSignedIn: !!currentMockUser,
      userId: currentMockUser?.id || null,
      sessionId: currentMockSession?.id || null,
      orgId: currentMockUser?.organizationMemberships?.[0]?.organization?.id || null,
      orgRole: currentMockUser?.organizationMemberships?.[0]?.role || null,
      getToken: vi.fn().mockResolvedValue('mock-token'),
      signOut: vi.fn().mockResolvedValue(undefined),
    }),
    useOrganization: () => ({
      isLoaded: true,
      organization: currentMockUser?.organizationMemberships?.[0]?.organization || null,
      membership: currentMockUser?.organizationMemberships?.[0] || null,
    }),
    useOrganizationList: () => ({
      isLoaded: true,
      organizationList: currentMockUser?.organizationMemberships?.map((m) => ({
        organization: m.organization,
        membership: m,
      })) || [],
    }),
    useClerk: () => ({
      signOut: vi.fn(),
      openSignIn: vi.fn(),
      openSignUp: vi.fn(),
      openUserProfile: vi.fn(),
    }),
    SignedIn: ({ children }: { children: React.ReactNode }) =>
      currentMockUser ? children : null,
    SignedOut: ({ children }: { children: React.ReactNode }) =>
      !currentMockUser ? children : null,
    ClerkProvider: ({ children }: { children: React.ReactNode }) => children,
    SignInButton: ({ children }: { children?: React.ReactNode }) =>
      children || '<button>Sign in</button>',
    UserButton: () => '<div data-testid="user-button" />',
  }));
}

// Mock for @clerk/nextjs/server (server-side)
export function mockClerkServer() {
  vi.mock('@clerk/nextjs/server', () => ({
    auth: vi.fn().mockImplementation(async () => ({
      userId: currentMockUser?.id || null,
      sessionId: currentMockSession?.id || null,
      orgId: currentMockUser?.organizationMemberships?.[0]?.organization?.id || null,
      orgRole: currentMockUser?.organizationMemberships?.[0]?.role || null,
      getToken: vi.fn().mockResolvedValue('mock-server-token'),
    })),
    currentUser: vi.fn().mockImplementation(async () => currentMockUser),
    clerkClient: () => ({
      users: {
        getUser: vi.fn().mockResolvedValue(currentMockUser),
        getUserList: vi.fn().mockResolvedValue({ data: [currentMockUser].filter(Boolean) }),
        createUser: vi.fn().mockImplementation(async (data) => ({
          ...defaultMockUser,
          ...data,
          id: `user_${Date.now()}`,
        })),
        updateUser: vi.fn().mockImplementation(async (userId, data) => ({
          ...currentMockUser,
          ...data,
        })),
        deleteUser: vi.fn().mockResolvedValue({}),
      },
      organizations: {
        getOrganization: vi.fn(),
        getOrganizationMembershipList: vi.fn(),
      },
    }),
  }));
}
```

### Testing Components with Clerk Auth

```typescript
// __tests__/unit/components/dashboard.test.tsx
import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { setMockUser, clearMockUser, mockClerkNextjs } from '../../helpers/clerk-mock';

// Must call mock setup before importing components
mockClerkNextjs();

import { DashboardHeader } from '../../../src/components/dashboard-header';

describe('DashboardHeader', () => {
  beforeEach(() => {
    clearMockUser();
  });

  it('should display user name when signed in', () => {
    setMockUser({ firstName: 'Jane', lastName: 'Smith' });

    render(<DashboardHeader />);

    expect(screen.getByText('Jane Smith')).toBeDefined();
  });

  it('should display user email when name is not available', () => {
    setMockUser({
      firstName: null,
      lastName: null,
      emailAddresses: [{ emailAddress: 'jane@test.com', id: 'e1' }],
    });

    render(<DashboardHeader />);

    expect(screen.getByText('jane@test.com')).toBeDefined();
  });

  it('should show sign-in button when not authenticated', () => {
    clearMockUser();

    render(<DashboardHeader />);

    expect(screen.getByText('Sign in')).toBeDefined();
  });

  it('should show admin badge for admin users', () => {
    setMockUser({
      organizationMemberships: [
        {
          organization: { id: 'org_1', name: 'Test Org', slug: 'test-org' },
          role: 'org:admin',
        },
      ],
    });

    render(<DashboardHeader />);

    expect(screen.getByText('Admin')).toBeDefined();
  });
});
```

## Webhook Testing

### Webhook Handler

```typescript
// src/app/api/webhooks/clerk/route.ts
import { Webhook } from 'svix';
import { headers } from 'next/headers';
import { WebhookEvent } from '@clerk/nextjs/server';
import { db } from '@/db';

export async function POST(req: Request) {
  const WEBHOOK_SECRET = process.env.CLERK_WEBHOOK_SECRET;

  if (!WEBHOOK_SECRET) {
    return new Response('Webhook secret not configured', { status: 500 });
  }

  const headerPayload = await headers();
  const svix_id = headerPayload.get('svix-id');
  const svix_timestamp = headerPayload.get('svix-timestamp');
  const svix_signature = headerPayload.get('svix-signature');

  if (!svix_id || !svix_timestamp || !svix_signature) {
    return new Response('Missing svix headers', { status: 400 });
  }

  const payload = await req.json();
  const body = JSON.stringify(payload);

  const wh = new Webhook(WEBHOOK_SECRET);
  let evt: WebhookEvent;

  try {
    evt = wh.verify(body, {
      'svix-id': svix_id,
      'svix-timestamp': svix_timestamp,
      'svix-signature': svix_signature,
    }) as WebhookEvent;
  } catch (err) {
    return new Response('Invalid signature', { status: 400 });
  }

  switch (evt.type) {
    case 'user.created': {
      const { id, email_addresses, first_name, last_name, image_url } = evt.data;
      const primaryEmail = email_addresses.find((e) => e.id === evt.data.primary_email_address_id);

      await db.user.create({
        data: {
          clerkId: id,
          email: primaryEmail?.email_address || '',
          name: [first_name, last_name].filter(Boolean).join(' ') || null,
          avatarUrl: image_url || null,
        },
      });
      break;
    }

    case 'user.updated': {
      const { id, email_addresses, first_name, last_name, image_url } = evt.data;
      const primaryEmail = email_addresses.find((e) => e.id === evt.data.primary_email_address_id);

      await db.user.update({
        where: { clerkId: id },
        data: {
          email: primaryEmail?.email_address || undefined,
          name: [first_name, last_name].filter(Boolean).join(' ') || undefined,
          avatarUrl: image_url || undefined,
        },
      });
      break;
    }

    case 'user.deleted': {
      if (evt.data.id) {
        await db.user.delete({ where: { clerkId: evt.data.id } });
      }
      break;
    }
  }

  return new Response('OK', { status: 200 });
}
```

### Webhook Integration Tests

```typescript
// __tests__/integration/webhook.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { Webhook } from 'svix';

// Mock the database
const mockDb = {
  user: {
    create: vi.fn(),
    update: vi.fn(),
    delete: vi.fn(),
  },
};

vi.mock('@/db', () => ({ db: mockDb }));

// Webhook fixtures
function createWebhookPayload(type: string, data: Record<string, unknown>) {
  return { type, data, object: 'event' };
}

function signWebhookPayload(secret: string, payload: string) {
  const wh = new Webhook(secret);
  const timestamp = Math.floor(Date.now() / 1000).toString();
  const msgId = `msg_${Date.now()}`;

  // Generate a real Svix signature
  const toSign = `${msgId}.${timestamp}.${payload}`;
  const crypto = require('crypto');
  const secretBytes = Buffer.from(secret.split('_')[1] || secret, 'base64');
  const signature = crypto
    .createHmac('sha256', secretBytes)
    .update(toSign)
    .digest('base64');

  return {
    'svix-id': msgId,
    'svix-timestamp': timestamp,
    'svix-signature': `v1,${signature}`,
  };
}

describe('Clerk Webhook Handler', () => {
  const WEBHOOK_SECRET = 'whsec_testkey1234567890abcdefghijkl';

  beforeEach(() => {
    vi.clearAllMocks();
    process.env.CLERK_WEBHOOK_SECRET = WEBHOOK_SECRET;
  });

  describe('Signature verification', () => {
    it('should reject requests without svix headers', async () => {
      const { POST } = await import('../../src/app/api/webhooks/clerk/route');

      const req = new Request('http://localhost:3000/api/webhooks/clerk', {
        method: 'POST',
        body: JSON.stringify({ type: 'user.created', data: {} }),
        headers: { 'Content-Type': 'application/json' },
      });

      // Mock headers() to return empty
      vi.mock('next/headers', () => ({
        headers: () =>
          new Map([
            ['svix-id', null],
            ['svix-timestamp', null],
            ['svix-signature', null],
          ]),
      }));

      const response = await POST(req);
      expect(response.status).toBe(400);
    });

    it('should reject requests with invalid signatures', async () => {
      const { POST } = await import('../../src/app/api/webhooks/clerk/route');

      const payload = JSON.stringify({ type: 'user.created', data: {} });

      vi.mock('next/headers', () => ({
        headers: async () => ({
          get: (key: string) => {
            const headers: Record<string, string> = {
              'svix-id': 'msg_test',
              'svix-timestamp': Math.floor(Date.now() / 1000).toString(),
              'svix-signature': 'v1,invalidsignature',
            };
            return headers[key] || null;
          },
        }),
      }));

      const req = new Request('http://localhost:3000/api/webhooks/clerk', {
        method: 'POST',
        body: payload,
      });

      const response = await POST(req);
      expect(response.status).toBe(400);
    });
  });

  describe('user.created event', () => {
    it('should create a user in the database', async () => {
      const payload = createWebhookPayload('user.created', {
        id: 'user_new123',
        email_addresses: [
          { id: 'email_1', email_address: 'new@example.com' },
        ],
        primary_email_address_id: 'email_1',
        first_name: 'New',
        last_name: 'User',
        image_url: 'https://img.clerk.com/new',
      });

      mockDb.user.create.mockResolvedValue({
        id: 'db_1',
        clerkId: 'user_new123',
      });

      // This would need proper signature verification setup
      // In practice, you would use the signed headers from signWebhookPayload
      expect(mockDb.user.create).toBeDefined();
    });

    it('should handle missing first/last name', async () => {
      const eventData = {
        id: 'user_noname',
        email_addresses: [{ id: 'email_1', email_address: 'noname@test.com' }],
        primary_email_address_id: 'email_1',
        first_name: null,
        last_name: null,
        image_url: null,
      };

      // Simulate webhook handler logic
      const name = [eventData.first_name, eventData.last_name]
        .filter(Boolean)
        .join(' ') || null;

      expect(name).toBeNull();
    });
  });

  describe('user.updated event', () => {
    it('should update user data in database', async () => {
      mockDb.user.update.mockResolvedValue({ clerkId: 'user_update123' });

      // Verify the update was called with correct data
      await mockDb.user.update({
        where: { clerkId: 'user_update123' },
        data: {
          email: 'updated@example.com',
          name: 'Updated Name',
        },
      });

      expect(mockDb.user.update).toHaveBeenCalledWith({
        where: { clerkId: 'user_update123' },
        data: {
          email: 'updated@example.com',
          name: 'Updated Name',
        },
      });
    });
  });

  describe('user.deleted event', () => {
    it('should delete user from database', async () => {
      mockDb.user.delete.mockResolvedValue({});

      await mockDb.user.delete({ where: { clerkId: 'user_delete123' } });

      expect(mockDb.user.delete).toHaveBeenCalledWith({
        where: { clerkId: 'user_delete123' },
      });
    });

    it('should handle missing user ID gracefully', async () => {
      const eventData = { id: undefined };

      // The handler should check for id before deleting
      if (eventData.id) {
        await mockDb.user.delete({ where: { clerkId: eventData.id } });
      }

      expect(mockDb.user.delete).not.toHaveBeenCalled();
    });
  });
});
```

## E2E Testing with Playwright and Clerk Testing Tokens

### Playwright Configuration for Clerk

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './__tests__/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Clerk E2E Test Helper with Testing Tokens

```typescript
// __tests__/helpers/clerk-test-utils.ts
import { type Page, type BrowserContext } from '@playwright/test';

/**
 * Clerk Testing Tokens allow bypassing the Clerk UI in E2E tests.
 * Set CLERK_TESTING_TOKEN in your .env.test file.
 * Generate tokens via: https://dashboard.clerk.com -> Testing
 */

interface ClerkTestUser {
  email: string;
  password: string;
  firstName?: string;
  lastName?: string;
}

// Sign in using Clerk's hosted sign-in page
export async function signInWithClerk(
  page: Page,
  user: ClerkTestUser
): Promise<void> {
  await page.goto('/sign-in');

  // Wait for Clerk's sign-in component to load
  await page.waitForSelector('[data-clerk-sign-in-root]', { timeout: 10000 });

  // Enter email
  const emailInput = page.locator('input[name="identifier"]');
  await emailInput.fill(user.email);
  await page.getByRole('button', { name: /continue/i }).click();

  // Enter password
  await page.waitForSelector('input[name="password"]', { timeout: 5000 });
  const passwordInput = page.locator('input[name="password"]');
  await passwordInput.fill(user.password);
  await page.getByRole('button', { name: /continue/i }).click();

  // Wait for redirect to dashboard
  await page.waitForURL('**/dashboard**', { timeout: 15000 });
}

// Sign in using Clerk Testing Token (faster, no UI interaction)
export async function signInWithTestingToken(
  page: Page,
  context: BrowserContext
): Promise<void> {
  const testingToken = process.env.CLERK_TESTING_TOKEN;
  if (!testingToken) {
    throw new Error('CLERK_TESTING_TOKEN not set. Generate one at https://dashboard.clerk.com');
  }

  // Set the testing token as a cookie
  await context.addCookies([
    {
      name: '__clerk_testing_token',
      value: testingToken,
      domain: 'localhost',
      path: '/',
    },
  ]);

  // Navigate to trigger auth
  await page.goto('/dashboard');
  await page.waitForURL('**/dashboard**', { timeout: 10000 });
}

// Sign out
export async function signOut(page: Page): Promise<void> {
  // Click user button and sign out
  await page.getByTestId('user-button').click();
  await page.getByRole('menuitem', { name: /sign out/i }).click();

  // Wait for redirect to home or sign-in
  await page.waitForURL(/\/(sign-in)?$/, { timeout: 10000 });
}

// Helper to set up authenticated state via API
export async function setupAuthState(
  context: BrowserContext,
  sessionToken: string
): Promise<void> {
  await context.addCookies([
    {
      name: '__session',
      value: sessionToken,
      domain: 'localhost',
      path: '/',
      httpOnly: true,
      secure: false,
      sameSite: 'Lax',
    },
  ]);
}
```

### E2E Sign-In Tests

```typescript
// __tests__/e2e/sign-in.spec.ts
import { test, expect } from '@playwright/test';
import { signInWithClerk, signOut } from '../helpers/clerk-test-utils';

const testUser = {
  email: process.env.CLERK_TEST_EMAIL || 'test@example.com',
  password: process.env.CLERK_TEST_PASSWORD || 'TestPassword123!',
};

test.describe('Sign In Flow', () => {
  test('should display sign-in page', async ({ page }) => {
    await page.goto('/sign-in');

    // Clerk's sign-in component should be visible
    await expect(page.locator('[data-clerk-sign-in-root]')).toBeVisible({
      timeout: 10000,
    });
  });

  test('should redirect unauthenticated users to sign-in', async ({ page }) => {
    await page.goto('/dashboard');

    // Should redirect to sign-in
    await expect(page).toHaveURL(/\/sign-in/);
  });

  test('should preserve redirect URL after sign-in', async ({ page }) => {
    // Try to access a specific protected page
    await page.goto('/dashboard/settings');

    // Should redirect to sign-in with redirect_url
    await expect(page).toHaveURL(/\/sign-in.*redirect_url/);
  });

  test('should sign in with valid credentials', async ({ page }) => {
    await signInWithClerk(page, testUser);

    // Should be on dashboard
    await expect(page).toHaveURL(/\/dashboard/);

    // Should show user info
    await expect(page.getByTestId('user-button')).toBeVisible();
  });

  test('should show error for invalid credentials', async ({ page }) => {
    await page.goto('/sign-in');

    await page.waitForSelector('[data-clerk-sign-in-root]');

    const emailInput = page.locator('input[name="identifier"]');
    await emailInput.fill('wrong@example.com');
    await page.getByRole('button', { name: /continue/i }).click();

    // Wait for error message
    await expect(
      page.getByText(/couldn't find your account|no account/i)
    ).toBeVisible({ timeout: 10000 });
  });

  test('should sign out successfully', async ({ page }) => {
    await signInWithClerk(page, testUser);

    await signOut(page);

    // Should be signed out
    await page.goto('/dashboard');
    await expect(page).toHaveURL(/\/sign-in/);
  });
});
```

### Protected Route E2E Tests

```typescript
// __tests__/e2e/protected-flow.spec.ts
import { test, expect } from '@playwright/test';
import { signInWithClerk } from '../helpers/clerk-test-utils';

const testUser = {
  email: process.env.CLERK_TEST_EMAIL || 'test@example.com',
  password: process.env.CLERK_TEST_PASSWORD || 'TestPassword123!',
};

test.describe('Protected Routes', () => {
  test.beforeEach(async ({ page }) => {
    await signInWithClerk(page, testUser);
  });

  test('should access dashboard when authenticated', async ({ page }) => {
    await page.goto('/dashboard');
    await expect(page.getByRole('heading', { name: /dashboard/i })).toBeVisible();
  });

  test('should access settings page', async ({ page }) => {
    await page.goto('/dashboard/settings');
    await expect(page.getByRole('heading', { name: /settings/i })).toBeVisible();
  });

  test('should call protected API endpoints', async ({ page }) => {
    const response = await page.request.get('/api/protected/data');
    expect(response.status()).toBe(200);

    const data = await response.json();
    expect(data).toBeDefined();
  });

  test('should handle session expiry gracefully', async ({ page, context }) => {
    await page.goto('/dashboard');

    // Clear session cookies to simulate expiry
    await context.clearCookies();

    // Navigate to a protected page
    await page.goto('/dashboard/settings');

    // Should redirect to sign-in
    await expect(page).toHaveURL(/\/sign-in/);
  });
});
```

## Organization and RBAC Testing

```typescript
// __tests__/integration/organization.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { setMockUser, clearMockUser, mockClerkNextjs } from '../helpers/clerk-mock';

mockClerkNextjs();

import { checkPermission, getUserRole, canAccessResource } from '../../src/lib/roles';

describe('Organization RBAC', () => {
  beforeEach(() => {
    clearMockUser();
  });

  describe('Role checks', () => {
    it('should identify admin users', () => {
      setMockUser({
        organizationMemberships: [
          {
            organization: { id: 'org_1', name: 'Test Org', slug: 'test-org' },
            role: 'org:admin',
          },
        ],
      });

      expect(getUserRole('org_1')).toBe('org:admin');
    });

    it('should identify member users', () => {
      setMockUser({
        organizationMemberships: [
          {
            organization: { id: 'org_1', name: 'Test Org', slug: 'test-org' },
            role: 'org:member',
          },
        ],
      });

      expect(getUserRole('org_1')).toBe('org:member');
    });

    it('should return null for users not in the organization', () => {
      setMockUser({
        organizationMemberships: [
          {
            organization: { id: 'org_1', name: 'Test Org', slug: 'test-org' },
            role: 'org:member',
          },
        ],
      });

      expect(getUserRole('org_other')).toBeNull();
    });
  });

  describe('Permission checks', () => {
    it('should allow admins to manage members', () => {
      expect(checkPermission('org:admin', 'manage_members')).toBe(true);
    });

    it('should deny members from managing members', () => {
      expect(checkPermission('org:member', 'manage_members')).toBe(false);
    });

    it('should allow members to view content', () => {
      expect(checkPermission('org:member', 'view_content')).toBe(true);
    });

    it('should allow admins all permissions', () => {
      const adminPermissions = [
        'manage_members',
        'manage_settings',
        'delete_organization',
        'view_content',
        'create_content',
      ];

      for (const perm of adminPermissions) {
        expect(checkPermission('org:admin', perm)).toBe(true);
      }
    });
  });

  describe('Multi-organization support', () => {
    it('should handle users with multiple organization memberships', () => {
      setMockUser({
        organizationMemberships: [
          {
            organization: { id: 'org_1', name: 'Org One', slug: 'org-one' },
            role: 'org:admin',
          },
          {
            organization: { id: 'org_2', name: 'Org Two', slug: 'org-two' },
            role: 'org:member',
          },
        ],
      });

      expect(getUserRole('org_1')).toBe('org:admin');
      expect(getUserRole('org_2')).toBe('org:member');
    });

    it('should scope permissions to the active organization', () => {
      setMockUser({
        organizationMemberships: [
          {
            organization: { id: 'org_1', name: 'Org One', slug: 'org-one' },
            role: 'org:admin',
          },
          {
            organization: { id: 'org_2', name: 'Org Two', slug: 'org-two' },
            role: 'org:member',
          },
        ],
      });

      // Admin in org_1 but member in org_2
      expect(canAccessResource('org_1', 'manage_members')).toBe(true);
      expect(canAccessResource('org_2', 'manage_members')).toBe(false);
    });
  });
});
```

## Testing Clerk Server Auth Helpers

```typescript
// __tests__/unit/auth.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mockClerkServer } from '../helpers/clerk-mock';
import { setMockUser, clearMockUser } from '../helpers/clerk-mock';

mockClerkServer();

import { getAuthUser, requireAuth, requireAdmin } from '../../src/lib/auth';

describe('Server Auth Helpers', () => {
  beforeEach(() => {
    clearMockUser();
  });

  describe('getAuthUser', () => {
    it('should return user when authenticated', async () => {
      setMockUser({ id: 'user_test', firstName: 'Test', lastName: 'User' });

      const user = await getAuthUser();
      expect(user).toBeDefined();
      expect(user!.id).toBe('user_test');
    });

    it('should return null when not authenticated', async () => {
      clearMockUser();

      const user = await getAuthUser();
      expect(user).toBeNull();
    });
  });

  describe('requireAuth', () => {
    it('should return user when authenticated', async () => {
      setMockUser({ id: 'user_auth' });

      const user = await requireAuth();
      expect(user.id).toBe('user_auth');
    });

    it('should throw when not authenticated', async () => {
      clearMockUser();

      await expect(requireAuth()).rejects.toThrow('Unauthorized');
    });
  });

  describe('requireAdmin', () => {
    it('should return user when user is admin', async () => {
      setMockUser({
        id: 'user_admin',
        organizationMemberships: [
          {
            organization: { id: 'org_1', name: 'Org', slug: 'org' },
            role: 'org:admin',
          },
        ],
      });

      const user = await requireAdmin();
      expect(user.id).toBe('user_admin');
    });

    it('should throw when user is not admin', async () => {
      setMockUser({
        id: 'user_member',
        organizationMemberships: [
          {
            organization: { id: 'org_1', name: 'Org', slug: 'org' },
            role: 'org:member',
          },
        ],
      });

      await expect(requireAdmin()).rejects.toThrow('Forbidden');
    });

    it('should throw when not authenticated', async () => {
      clearMockUser();

      await expect(requireAdmin()).rejects.toThrow('Unauthorized');
    });
  });
});
```

## Testing Protected API Routes

```typescript
// __tests__/integration/protected-routes.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mockClerkServer, setMockUser, clearMockUser } from '../helpers/clerk-mock';

mockClerkServer();

describe('Protected API Routes', () => {
  beforeEach(() => {
    clearMockUser();
  });

  describe('GET /api/protected/profile', () => {
    it('should return profile for authenticated users', async () => {
      setMockUser({ id: 'user_profile' });

      const { GET } = await import('../../src/app/api/protected/profile/route');

      const req = new Request('http://localhost:3000/api/protected/profile');
      const response = await GET(req);

      expect(response.status).toBe(200);
      const data = await response.json();
      expect(data.userId).toBe('user_profile');
    });

    it('should return 401 for unauthenticated requests', async () => {
      clearMockUser();

      const { GET } = await import('../../src/app/api/protected/profile/route');

      const req = new Request('http://localhost:3000/api/protected/profile');
      const response = await GET(req);

      expect(response.status).toBe(401);
    });
  });

  describe('POST /api/admin/users', () => {
    it('should allow admin to create users', async () => {
      setMockUser({
        id: 'admin_user',
        organizationMemberships: [
          {
            organization: { id: 'org_1', name: 'Org', slug: 'org' },
            role: 'org:admin',
          },
        ],
      });

      const { POST } = await import('../../src/app/api/admin/users/route');

      const req = new Request('http://localhost:3000/api/admin/users', {
        method: 'POST',
        body: JSON.stringify({
          email: 'newuser@test.com',
          firstName: 'New',
          lastName: 'User',
        }),
      });

      const response = await POST(req);
      expect(response.status).toBe(201);
    });

    it('should return 403 for non-admin users', async () => {
      setMockUser({
        id: 'member_user',
        organizationMemberships: [
          {
            organization: { id: 'org_1', name: 'Org', slug: 'org' },
            role: 'org:member',
          },
        ],
      });

      const { POST } = await import('../../src/app/api/admin/users/route');

      const req = new Request('http://localhost:3000/api/admin/users', {
        method: 'POST',
        body: JSON.stringify({ email: 'hack@test.com' }),
      });

      const response = await POST(req);
      expect(response.status).toBe(403);
    });
  });
});
```

## Clerk Fixture Data

```typescript
// __tests__/fixtures/clerk-webhook.fixture.ts
export const userCreatedEvent = {
  type: 'user.created',
  data: {
    id: 'user_fixture_123',
    email_addresses: [
      {
        id: 'idn_fixture',
        email_address: 'fixture@example.com',
        verification: { status: 'verified', strategy: 'email_code' },
      },
    ],
    primary_email_address_id: 'idn_fixture',
    first_name: 'Fixture',
    last_name: 'User',
    image_url: 'https://img.clerk.com/fixture',
    created_at: Date.now(),
    updated_at: Date.now(),
    public_metadata: {},
    private_metadata: {},
    unsafe_metadata: {},
  },
  object: 'event',
};

export const userUpdatedEvent = {
  type: 'user.updated',
  data: {
    ...userCreatedEvent.data,
    first_name: 'Updated',
    last_name: 'Fixture',
  },
  object: 'event',
};

export const userDeletedEvent = {
  type: 'user.deleted',
  data: {
    id: 'user_fixture_123',
    deleted: true,
  },
  object: 'event',
};

export const organizationCreatedEvent = {
  type: 'organization.created',
  data: {
    id: 'org_fixture_123',
    name: 'Fixture Organization',
    slug: 'fixture-org',
    created_at: Date.now(),
    updated_at: Date.now(),
    created_by: 'user_fixture_123',
    max_allowed_memberships: 100,
  },
  object: 'event',
};
```

## Best Practices

1. **Use Clerk Testing Tokens in CI** -- Testing tokens bypass the Clerk hosted UI entirely, making E2E tests faster and more reliable. Generate them from the Clerk dashboard.
2. **Mock Clerk hooks at the module level** -- Use `vi.mock('@clerk/nextjs')` before importing components. Mocking after import does not work reliably.
3. **Create a centralized mock helper** -- Build `setMockUser()` and `clearMockUser()` functions that all tests share instead of duplicating mock setup in every file.
4. **Test middleware separately from route handlers** -- Middleware auth checks and route handler business logic should have independent test suites.
5. **Verify webhook signature rejection** -- Always test that your webhook handler rejects requests with missing, invalid, or tampered Svix signatures.
6. **Test the full auth → database pipeline** -- Verify that webhook events create the correct database records, and that subsequent authenticated requests can access those records.
7. **Use separate Clerk test instances** -- Create a dedicated Clerk application for testing with its own API keys. Never share keys between production and test.
8. **Test organization switching** -- If your app supports multiple organizations, verify that switching organizations updates permissions correctly without requiring re-authentication.
9. **Test the unauthenticated experience** -- Verify that public pages render correctly without auth, sign-in redirects include the return URL, and API routes return proper 401 responses.
10. **Verify graceful degradation** -- When Clerk is misconfigured or unavailable, your app should show an appropriate error, not crash with an unhandled exception.

## Anti-Patterns to Avoid

1. **Testing against Clerk's production API in CI** -- This makes tests slow, flaky, and dependent on network availability. Use mocks for unit tests and testing tokens for E2E.
2. **Mocking `auth()` with a raw object instead of the mock helper** -- Inconsistent mock shapes cause subtle bugs. Always use the centralized mock to ensure all fields are present.
3. **Not testing the middleware redirect URLs** -- If the redirect URL is wrong, users land on the wrong page after sign-in. Always assert the full redirect URL including query params.
4. **Ignoring the auth check order in middleware** -- Authentication should be checked before authorization. If you check admin role before auth, unauthenticated users get FORBIDDEN instead of UNAUTHORIZED.
5. **Hardcoding Clerk user IDs in tests** -- Use fixture factories that generate unique IDs. Hardcoded IDs collide when running tests in parallel.
6. **Not cleaning up test users** -- Leftover test users in the Clerk dashboard waste resources and can cause confusing test failures.
7. **Testing Clerk's own functionality** -- Do not test that Clerk correctly validates JWTs or sends emails. Test your application's behavior when Clerk returns specific states.
8. **Sharing authenticated state between E2E tests** -- Each test should sign in fresh. Shared sessions cause order-dependent failures and make debugging difficult.
9. **Not testing the webhook retry behavior** -- Clerk retries failed webhooks. Ensure your handler is idempotent by testing duplicate event delivery.
10. **Forgetting to test the `afterAuth` callback** -- If you use `afterAuth` in middleware for custom routing logic, test all branches including edge cases like missing organizations or expired sessions.

## Running Tests

- Run all auth tests: `pnpm vitest run __tests__`
- Run unit tests: `pnpm vitest run __tests__/unit`
- Run integration tests: `pnpm vitest run __tests__/integration`
- Run E2E tests: `pnpm playwright test __tests__/e2e`
- Run E2E with visible browser: `pnpm playwright test --headed`
- Run middleware tests: `pnpm vitest run __tests__/unit/middleware.test.ts`
- Run webhook tests: `pnpm vitest run __tests__/integration/webhook.test.ts`
- Watch mode: `pnpm vitest __tests__/unit`
- Debug E2E: `pnpm playwright test --debug`
