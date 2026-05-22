---
name: clerk
description: Clerk authentication integration for Astro/Next.js. Use when implementing authentication, handling Clerk middleware, testing with Playwright, or debugging auth issues. Trigger phrases include "Clerk auth", "sign in", "authentication", "middleware", "E2E testing with Clerk".
---

# Clerk Authentication Skill

Comprehensive guide for implementing and testing Clerk authentication, with special focus on Astro SSR integration and Playwright E2E testing.

## Key Concepts

### Clerk Architecture in Astro

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser (Client)                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Clerk Frontend SDK (@clerk/astro)                  │    │
│  │  - Manages client-side session state                │    │
│  │  - Provides <SignIn>, <UserButton> components       │    │
│  │  - Sets localStorage tokens                         │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Server (Astro SSR)                        │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  clerkMiddleware (@clerk/astro/server)              │    │
│  │  - Validates HTTPOnly session cookies               │    │
│  │  - Runs BEFORE any custom middleware logic          │    │
│  │  - Sets Astro.locals.auth()                         │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

**Critical Understanding**: Clerk's middleware validates sessions at the wrapper level BEFORE your callback executes. You cannot bypass authentication inside the middleware callback.

### Session Types

| Session Type | Created By | Server Validated | Use Case |
|--------------|-----------|------------------|----------|
| HTTPOnly Cookie | UI sign-in flow | ✅ Yes | Production, E2E tests |
| Client-side | `@clerk/testing` signIn() | ❌ No | Unit tests only |
| Backend API | `sessions.create()` | ⚠️ Partial | Limited use |

## E2E Testing with Playwright

### The Problem

`@clerk/testing`'s programmatic `clerk.signIn()` creates client-side sessions only. These are NOT recognized by Clerk's server-side middleware in Astro/Next.js SSR applications.

```typescript
// ❌ This creates client-side session only - won't pass middleware
await clerk.signIn({
  page,
  signInParams: { strategy: 'password', identifier: email, password }
});
// User appears logged in (UserButton shows), but server redirects to /sign-in
```

### The Solution: UI-Based Sign-In with Test Emails

Use actual UI sign-in flow with Clerk's `+clerk_test` email feature:

```typescript
// ✅ This creates real server-validated session
// 1. Navigate to sign-in with testing token (bypasses bot detection)
await page.goto(`/sign-in?__clerk_testing_token=${testingToken}`);

// 2. Fill in email (MUST contain +clerk_test)
await page.fill('input[name="identifier"]', 'user+clerk_test@example.com');
await page.click('button:has-text("Continue")');

// 3. Fill in password
await page.fill('input[type="password"]', password);
await page.click('button:has-text("Continue")');

// 4. Handle device verification with magic code
// See: clerk.com/docs/guides/development/testing/test-emails-and-phones
await enterVerificationCode(page, CLERK_TEST_VERIFICATION_CODE);
```

### Test Email Magic Code (CRITICAL for E2E/CI)

> ⚠️ **CRITICAL**: Test user emails MUST contain `+clerk_test` for automated testing to work.
> Without this suffix, Clerk requires real email verification which breaks CI/CD pipelines.

Any email with `+clerk_test` suffix is treated specially by Clerk:
- **No actual email sent** for verification
- **Clerk's magic test code always works** for any verification step
- **Real users unaffected** - normal verification for non-test emails
- **Works in both development and production** Clerk instances

**Valid test email formats:**
- `john+clerk_test@gmail.com` ✅
- `test+clerk_test_admin@example.com` ✅
- `user+clerk_test_member@company.com` ✅

**Invalid for automated testing:**
- `john+admin@gmail.com` ❌ (no `clerk_test` in address)
- `john_clerk_test@gmail.com` ❌ (must use `+` plus-addressing)
- `clerktest@gmail.com` ❌ (must use `+clerk_test` suffix format)

**Get the verification code**: See [Clerk's Test Emails Documentation](https://clerk.com/docs/guides/development/testing/test-emails-and-phones) for the magic verification code that works with `+clerk_test` emails.

> 💡 **CI/CD Tip**: Store test user emails in environment variables/secrets. Ensure all contain `+clerk_test`:
> ```
> TEST_ADMIN_EMAIL=user+clerk_test_admin@gmail.com
> TEST_MEMBER_EMAIL=user+clerk_test_member@gmail.com
> ```

### Testing Token

Get a testing token to bypass bot detection:

```typescript
import { createClerkClient } from '@clerk/backend';

const clerkClient = createClerkClient({
  secretKey: process.env.CLERK_SECRET_KEY,
});

const token = await clerkClient.testingTokens.createTestingToken();
// Use as: /sign-in?__clerk_testing_token=${token.token}
```

### Complete E2E Auth Setup

```typescript
// tests/e2e/global-setup.ts
import { createClerkClient } from '@clerk/backend';

const clerkClient = createClerkClient({
  secretKey: process.env.CLERK_SECRET_KEY,
});

async function authenticateUser(page, email, password, storagePath) {
  // 1. Get testing token
  const { token } = await clerkClient.testingTokens.createTestingToken();

  // 2. Navigate with token
  await page.goto(`/sign-in?__clerk_testing_token=${token}`);

  // 3. Fill email (must have +clerk_test)
  await page.fill('input[name="identifier"]', email);
  await page.click('button:has-text("Continue")');

  // 4. Fill password
  await page.fill('input[type="password"]', password);
  await page.click('button:has-text("Continue")');

  // 5. Handle device verification (code from Clerk docs)
  // See: clerk.com/docs/guides/development/testing/test-emails-and-phones
  await page.waitForTimeout(2000);
  if (page.url().includes('factor-two')) {
    const code = process.env.CLERK_TEST_CODE; // From Clerk docs
    const inputs = page.locator('input[inputmode="numeric"]');
    for (let i = 0; i < 6; i++) {
      await inputs.nth(i).fill(code[i]);
    }
  }

  // 6. Wait for redirect and save session
  await page.waitForURL(url => !url.includes('/sign-in'));
  await page.context().storageState({ path: storagePath });
}
```

## Middleware Configuration

### Basic Protected Routes

```typescript
// src/middleware.ts
import { clerkMiddleware, createRouteMatcher } from "@clerk/astro/server";

const isPublicRoute = createRouteMatcher([
  "/",
  "/sign-in(.*)",
  "/sign-up(.*)",
  "/api/webhooks/(.*)",
]);

export const onRequest = clerkMiddleware((auth, context) => {
  const { userId } = auth();

  if (isPublicRoute(context.request)) {
    return; // Allow public routes
  }

  if (!userId) {
    return auth().redirectToSignIn();
  }
});
```

### Role-Based Access

```typescript
// Check role inside middleware callback
export const onRequest = clerkMiddleware(async (auth, context) => {
  const { userId } = auth();

  if (!userId) {
    return auth().redirectToSignIn();
  }

  // Check admin routes
  if (context.request.url.includes('/admin')) {
    const member = await memberQueries.findByClerkId(userId);
    if (member?.role !== 'admin') {
      return context.redirect('/unauthorized');
    }
  }
});
```

## Common Patterns

### Get Current User in Astro Pages

```typescript
// src/pages/dashboard.astro
---
const auth = Astro.locals.auth();
const { userId, sessionClaims } = auth;

if (!userId) {
  return Astro.redirect('/sign-in');
}

// Get user data from your database
const member = await memberQueries.findByClerkId(userId);
---
```

### Client-Side Auth Check

```typescript
// For pre-rendered pages that need client-side auth
<script>
  function checkAuth() {
    if (window.Clerk?.loaded && !window.Clerk.user) {
      window.Clerk.redirectToSignIn({ redirectUrl: window.location.href });
    }
  }

  // Poll until Clerk loads
  const interval = setInterval(() => {
    if (window.Clerk?.loaded) {
      clearInterval(interval);
      checkAuth();
    }
  }, 100);
</script>
```

### Webhook Handling

```typescript
// src/pages/api/webhooks/clerk.ts
import { Webhook } from 'svix';

export const POST: APIRoute = async ({ request }) => {
  const payload = await request.text();
  const headers = Object.fromEntries(request.headers);

  const wh = new Webhook(process.env.CLERK_WEBHOOK_SECRET);
  const event = wh.verify(payload, headers);

  switch (event.type) {
    case 'user.created':
      // Create member record
      break;
    case 'user.updated':
      // Sync user data
      break;
  }

  return new Response('OK', { status: 200 });
};
```

## Troubleshooting

### "Session not recognized by server"

**Cause**: Using `@clerk/testing` programmatic sign-in which only creates client-side sessions.

**Fix**: Use UI-based sign-in flow with testing tokens:
```typescript
await page.goto(`/sign-in?__clerk_testing_token=${token}`);
// Then fill in the actual form
```

### "Bot traffic detected"

**Cause**: Clerk's bot protection blocking automated requests.

**Fix**: Include testing token in URL:
```typescript
const token = await clerkClient.testingTokens.createTestingToken();
await page.goto(`/sign-in?__clerk_testing_token=${token.token}`);
```

### "Device verification required"

**Cause**: Clerk requires email verification from new devices.

**Fix**: Use `+clerk_test` email suffix with Clerk's magic test code:
```typescript
// Email MUST contain +clerk_test for magic code to work
const email = 'user+clerk_test_admin@gmail.com';
// Get the code from: clerk.com/docs/guides/development/testing/test-emails-and-phones
```

**Common mistake**: Using emails like `user+admin@gmail.com` without `clerk_test` - the magic code won't work!

### "redirectToSignIn not working"

**Cause**: Page is pre-rendered (SSG) so server-side redirect doesn't work.

**Fix**: Use client-side redirect:
```typescript
// In page frontmatter
export const prerender = true; // or remove for SSR

// In client script
if (!window.Clerk?.user) {
  window.Clerk?.redirectToSignIn();
}
```

### Middleware Not Running

**Cause**: Route might be pre-rendered or middleware configuration issue.

**Fix**: Ensure SSR mode for protected routes:
```typescript
// astro.config.mjs
export default defineConfig({
  output: 'server', // or 'hybrid'
});
```

## CI/CD Integration

### GitHub Actions Setup

```yaml
# .github/workflows/e2e-auth.yml
- name: Run authenticated E2E tests
  env:
    CLERK_SECRET_KEY: ${{ secrets.TEST_CLERK_SECRET_KEY }}
    # CRITICAL: Emails MUST contain +clerk_test
    TEST_ADMIN_EMAIL: ${{ secrets.TEST_ADMIN_EMAIL }}
    TEST_ADMIN_PASSWORD: ${{ secrets.TEST_ADMIN_PASSWORD }}
  run: npx playwright test
```

### Secret Configuration Checklist

1. ✅ Create test users in Clerk with `+clerk_test` emails
2. ✅ Set passwords for test users (Clerk Dashboard → Users)
3. ✅ Store email/password pairs as GitHub Secrets
4. ✅ Verify emails contain `+clerk_test` substring
5. ✅ Test locally before pushing to CI

### Syncing Local to CI

If your local `.env` works but CI fails, sync your secrets:

```bash
# Script to update GitHub Secrets from .env
source .env
gh secret set TEST_ADMIN_EMAIL --body "$TEST_ADMIN_EMAIL"
gh secret set TEST_ADMIN_PASSWORD --body "$TEST_ADMIN_PASSWORD"
# Repeat for other test users...
```

### Common CI Failure: "Verification code failed"

**Symptom**: Local tests pass, CI tests fail at device verification step.

**Root Cause**: GitHub Secrets have emails WITHOUT `+clerk_test`:
```
# ❌ Wrong - magic code won't work
TEST_ADMIN_EMAIL=user+admin@gmail.com

# ✅ Correct - magic code will work
TEST_ADMIN_EMAIL=user+clerk_test_admin@gmail.com
```

**Fix**: Update GitHub Secrets with correctly formatted emails.

## Environment Variables

```env
# Required for Clerk
PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_xxx
CLERK_SECRET_KEY=sk_test_xxx
CLERK_WEBHOOK_SECRET=whsec_xxx

# For E2E testing - MUST contain +clerk_test
TEST_ADMIN_EMAIL=user+clerk_test_admin@gmail.com
TEST_ADMIN_PASSWORD=xxx
TEST_MEMBER_EMAIL=user+clerk_test_member@gmail.com
TEST_MEMBER_PASSWORD=xxx
```

## Package Reference

| Package | Purpose |
|---------|---------|
| `@clerk/astro` | Astro integration (components, middleware) |
| `@clerk/backend` | Server-side operations (testing tokens, user management) |
| `@clerk/testing` | Test utilities (limited - client-side only) |
| `svix` | Webhook signature verification |

## References

- [Clerk Astro Integration](https://clerk.com/docs/reference/astro)
- [Clerk Testing with Playwright](https://clerk.com/docs/testing/playwright)
- [Test Emails and Phones](https://clerk.com/docs/guides/development/testing/test-emails-and-phones)
- [Testing Tokens](https://clerk.com/docs/testing/overview#testing-tokens)
- [Clerk Middleware](https://clerk.com/docs/reference/astro/clerk-middleware)

---

*Last updated: December 22, 2025*
*Added: CI/CD integration patterns and +clerk_test email requirements*
