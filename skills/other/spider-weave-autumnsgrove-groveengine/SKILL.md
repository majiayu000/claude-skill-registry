---
name: spider-weave
description: Weave authentication webs with patient precision. Spin the threads, connect the strands, secure the knots, and bind the system. Use when integrating auth, setting up OAuth, or securing routes.
---

# Spider Weave 🕷️

The spider doesn't rush. It spins one thread at a time, anchoring each carefully before moving to the next. The web grows organically—radial strands first, then the spiral, each connection tested for strength. When complete, the web catches what matters while letting the wind pass through. Authentication woven this way is strong, resilient, and beautiful in its structure.

## When to Activate

- User asks to "add auth" or "set up authentication"
- User says "protect this route" or "add login"
- User calls `/spider-weave` or mentions spider/auth
- Integrating OAuth (Google, GitHub, etc.)
- Setting up session management
- Protecting API routes
- Adding role-based access control (RBAC)
- Implementing PKCE flow
- Connecting to Heartwood (GroveAuth)

**Pair with:** `raccoon-audit` for security review, `beaver-build` for auth testing

---

## The Weave

```
SPIN → CONNECT → SECURE → TEST → BIND
  ↓       ↓        ↓        ↓        ↓
Create  Link    Harden   Verify   Lock In
Threads Strands  Knots    Web     Security
```

### Phase 1: SPIN

*The spider spins the first thread, anchoring it carefully...*

Create the foundational auth structure:

**Choose the Auth Pattern:**

| Pattern | Best For | Complexity |
|---------|----------|------------|
| **Session-based** | Traditional web apps | Medium |
| **JWT** | Stateless APIs, SPAs | Medium |
| **OAuth 2.0** | Third-party login | High |
| **PKCE** | Mobile/SPA OAuth | High |
| **API Keys** | Service-to-service | Low |

**For Grove/Heartwood Integration:**
```typescript
// PKCE flow setup
import { generatePKCE } from '$lib/auth/pkce';

const { codeVerifier, codeChallenge } = await generatePKCE();

// Store verifier (cookie or session)
cookies.set('pkce_verifier', codeVerifier, {
  httpOnly: true,
  secure: true,
  sameSite: 'lax',
  maxAge: 600 // 10 minutes
});

// Redirect to Heartwood
const authUrl = new URL('https://heartwood.grove.place/oauth/authorize');
authUrl.searchParams.set('client_id', CLIENT_ID);
authUrl.searchParams.set('code_challenge', codeChallenge);
authUrl.searchParams.set('code_challenge_method', 'S256');
authUrl.searchParams.set('redirect_uri', REDIRECT_URI);
authUrl.searchParams.set('state', generateState());
```

**Core Auth Files Structure:**
```
src/lib/auth/
├── index.ts           # Main exports
├── types.ts           # Auth-related types
├── session.ts         # Session management
├── middleware.ts      # Route protection
├── pkce.ts           # PKCE utilities
└── client.ts         # Heartwood/OAuth client
```

**Database Schema:**
```typescript
// Users table (linked to Heartwood)
export const users = sqliteTable('users', {
  id: integer('id').primaryKey(),
  heartwoodId: text('heartwood_id').unique(),
  email: text('email').unique(),
  displayName: text('display_name'),
  avatarUrl: text('avatar_url'),
  role: text('role').default('user'), // admin, user, guest
  createdAt: integer('created_at', { mode: 'timestamp' }).notNull(),
});

// Sessions (if using session-based auth)
export const sessions = sqliteTable('sessions', {
  id: text('id').primaryKey(),
  userId: integer('user_id').references(() => users.id),
  expiresAt: integer('expires_at', { mode: 'timestamp' }).notNull(),
});
```

**Environment Variables:**
```bash
# OAuth/Heartwood
HEARTWOOD_CLIENT_ID=
HEARTWOOD_CLIENT_SECRET=
HEARTWOOD_AUTHORIZE_URL=https://heartwood.grove.place/oauth/authorize
HEARTWOOD_TOKEN_URL=https://heartwood.grove.place/oauth/token
HEARTWOOD_USERINFO_URL=https://heartwood.grove.place/oauth/userinfo

# App
AUTH_REDIRECT_URI=http://localhost:5173/auth/callback
SESSION_SECRET=generate_with_openssl_rand_hex_32
```

**Output:** Auth infrastructure created, dependencies installed, schema defined

---

### Phase 2: CONNECT

*Thread connects to thread, the web taking shape...*

Link the auth system together:

**OAuth Flow Implementation:**

```typescript
// 1. Login route - redirect to provider
// src/routes/auth/login/+server.ts
export const GET: RequestHandler = async () => {
  const { codeVerifier, codeChallenge } = generatePKCE();
  const state = generateState();
  
  // Store PKCE verifier
  cookies.set('pkce_verifier', codeVerifier, { httpOnly: true, secure: true });
  cookies.set('oauth_state', state, { httpOnly: true, secure: true });
  
  const url = new URL(HEARTWOOD_AUTHORIZE_URL);
  url.searchParams.set('client_id', HEARTWOOD_CLIENT_ID);
  url.searchParams.set('code_challenge', codeChallenge);
  url.searchParams.set('code_challenge_method', 'S256');
  url.searchParams.set('redirect_uri', AUTH_REDIRECT_URI);
  url.searchParams.set('state', state);
  
  throw redirect(302, url.toString());
};

// 2. Callback route - handle OAuth response
// src/routes/auth/callback/+server.ts
export const GET: RequestHandler = async ({ url, cookies }) => {
  const code = url.searchParams.get('code');
  const state = url.searchParams.get('state');
  const storedState = cookies.get('oauth_state');
  
  // Verify state (CSRF protection)
  if (state !== storedState) {
    throw error(400, 'Invalid state parameter');
  }
  
  // Exchange code for tokens
  const tokenResponse = await fetch(HEARTWOOD_TOKEN_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      client_id: HEARTWOOD_CLIENT_ID,
      client_secret: HEARTWOOD_CLIENT_SECRET,
      code: code!,
      code_verifier: cookies.get('pkce_verifier')!,
      redirect_uri: AUTH_REDIRECT_URI,
    }),
  });
  
  const tokens = await tokenResponse.json();
  
  // Get user info
  const userResponse = await fetch(HEARTWOOD_USERINFO_URL, {
    headers: { Authorization: `Bearer ${tokens.access_token}` },
  });
  
  const userInfo = await userResponse.json();
  
  // Create/update user in database
  const user = await upsertUser({
    heartwoodId: userInfo.sub,
    email: userInfo.email,
    displayName: userInfo.name,
    avatarUrl: userInfo.picture,
  });
  
  // Create session
  const session = await createSession(user.id);
  
  // Set session cookie
  cookies.set('session', session.id, {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 7, // 7 days
  });
  
  // Clean up PKCE cookies
  cookies.delete('pkce_verifier');
  cookies.delete('oauth_state');
  
  throw redirect(302, '/dashboard');
};
```

**Session Management:**

```typescript
// src/lib/auth/session.ts
export async function createSession(userId: number): Promise<Session> {
  const sessionId = generateSecureId();
  const expiresAt = new Date(Date.now() + SESSION_DURATION);
  
  await db.insert(sessions).values({
    id: sessionId,
    userId,
    expiresAt,
  });
  
  return { id: sessionId, userId, expiresAt };
}

export async function validateSession(sessionId: string): Promise<User | null> {
  const session = await db.query.sessions.findFirst({
    where: eq(sessions.id, sessionId),
    with: { user: true },
  });
  
  if (!session || session.expiresAt < new Date()) {
    return null;
  }
  
  return session.user;
}

export async function invalidateSession(sessionId: string): Promise<void> {
  await db.delete(sessions).where(eq(sessions.id, sessionId));
}
```

**Auth Store (Client-side):**

```typescript
// src/lib/stores/auth.ts
import { writable } from 'svelte/store';

export interface AuthState {
  user: User | null;
  loading: boolean;
}

export const auth = writable<AuthState>({
  user: null,
  loading: true,
});

export async function loadUser() {
  const response = await fetch('/api/auth/me');
  if (response.ok) {
    const user = await response.json();
    auth.set({ user, loading: false });
  } else {
    auth.set({ user: null, loading: false });
  }
}
```

**Output:** OAuth flow connected, session management working, client state ready

---

### Phase 3: SECURE

*The spider tests each knot, ensuring the web holds...*

Harden the authentication system:

**Route Protection:**

```typescript
// src/lib/auth/middleware.ts
export function requireAuth(): Handle {
  return async ({ event, resolve }) => {
    const sessionId = event.cookies.get('session');
    
    if (!sessionId) {
      throw redirect(302, '/auth/login');
    }
    
    const user = await validateSession(sessionId);
    
    if (!user) {
      event.cookies.delete('session');
      throw redirect(302, '/auth/login');
    }
    
    event.locals.user = user;
    return resolve(event);
  };
}

// Role-based protection
export function requireRole(allowedRoles: string[]): Handle {
  return async ({ event, resolve }) => {
    const user = event.locals.user;
    
    if (!user || !allowedRoles.includes(user.role)) {
      throw error(403, 'Forbidden');
    }
    
    return resolve(event);
  };
}
```

**Security Headers:**

```typescript
// src/hooks.server.ts
export const handle: Handle = async ({ event, resolve }) => {
  const response = await resolve(event);
  
  // Security headers
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  response.headers.set(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
  );
  
  return response;
};
```

**CSRF Protection:**

```typescript
// For state-changing operations
export function validateCSRF(event: RequestEvent): void {
  const origin = event.request.headers.get('origin');
  const host = event.url.host;
  
  if (origin && new URL(origin).host !== host) {
    throw error(403, 'Invalid origin');
  }
}
```

**Rate Limiting:**

```typescript
// src/lib/auth/rate-limit.ts
const attempts = new Map<string, number[]>();

export function checkRateLimit(identifier: string, maxAttempts: number = 5): boolean {
  const now = Date.now();
  const windowStart = now - 15 * 60 * 1000; // 15 minutes
  
  const userAttempts = attempts.get(identifier) || [];
  const recentAttempts = userAttempts.filter(t => t > windowStart);
  
  if (recentAttempts.length >= maxAttempts) {
    return false;
  }
  
  recentAttempts.push(now);
  attempts.set(identifier, recentAttempts);
  return true;
}
```

**Secure Cookie Settings:**

```typescript
// Always use these for auth cookies
{
  httpOnly: true,    // Not accessible via JavaScript
  secure: true,      // HTTPS only in production
  sameSite: 'lax',   // CSRF protection
  maxAge: 604800,    // 7 days
  path: '/',         // Available site-wide
}
```

**Output:** Routes protected, headers set, rate limiting active, security hardened

---

### Phase 4: TEST

*The spider plucks the strands, verifying the web vibrates true...*

Test authentication thoroughly:

**Test Coverage:**

```typescript
// tests/auth/oauth.test.ts
describe('OAuth Flow', () => {
  test('redirects to Heartwood with PKCE', async () => {
    const response = await request(app).get('/auth/login');
    
    expect(response.status).toBe(302);
    expect(response.headers.location).toMatch(/heartwood\.grove\.place/);
    expect(response.headers.location).toMatch(/code_challenge=/);
  });
  
  test('handles callback and creates session', async () => {
    // Mock Heartwood responses
    mockHeartwoodTokenEndpoint({ access_token: 'test-token' });
    mockHeartwoodUserInfo({ sub: '123', email: 'test@example.com' });
    
    const response = await request(app)
      .get('/auth/callback?code=valid-code&state=valid-state')
      .set('Cookie', ['oauth_state=valid-state; pkce_verifier=test-verifier']);
    
    expect(response.status).toBe(302);
    expect(response.headers.location).toBe('/dashboard');
    
    // Verify session created
    const cookies = response.headers['set-cookie'];
    expect(cookies).toMatch(/session=/);
  });
  
  test('rejects invalid state (CSRF protection)', async () => {
    const response = await request(app)
      .get('/auth/callback?code=valid-code&state=wrong-state')
      .set('Cookie', ['oauth_state=correct-state']);
    
    expect(response.status).toBe(400);
  });
});

describe('Route Protection', () => {
  test('redirects unauthenticated users', async () => {
    const response = await request(app).get('/dashboard');
    expect(response.status).toBe(302);
    expect(response.headers.location).toBe('/auth/login');
  });
  
  test('allows authenticated users', async () => {
    const session = await createTestUserAndSession();
    
    const response = await request(app)
      .get('/dashboard')
      .set('Cookie', [`session=${session.id}`]);
    
    expect(response.status).toBe(200);
  });
  
  test('enforces role restrictions', async () => {
    const user = await createTestUser({ role: 'user' });
    const session = await createSession(user.id);
    
    const response = await request(app)
      .get('/admin')
      .set('Cookie', [`session=${session.id}`]);
    
    expect(response.status).toBe(403);
  });
});
```

**Security Testing:**

```typescript
// Test session fixation
test('session ID changes after login', async () => {
  const oldSession = cookies.get('session');
  await completeLoginFlow();
  const newSession = cookies.get('session');
  expect(newSession).not.toBe(oldSession);
});

// Test cookie security
test('auth cookies have secure attributes', async () => {
  const response = await completeLoginFlow();
  const cookies = response.headers['set-cookie'];
  
  expect(cookies).toMatch(/HttpOnly/);
  expect(cookies).toMatch(/SameSite=/);
});
```

**Output:** All auth flows tested, security verified, edge cases covered

---

### Phase 5: BIND

*The web is complete, each strand bound tight, ready to catch what comes...*

Finalize and lock in the authentication:

**Integration Checklist:**

- [ ] Login flow works end-to-end
- [ ] Logout clears session
- [ ] Protected routes redirect unauthenticated users
- [ ] Session expires correctly
- [ ] Token refresh works (if applicable)
- [ ] Error messages don't leak sensitive info
- [ ] Rate limiting prevents brute force
- [ ] CSRF protection active
- [ ] Security headers set
- [ ] Cookies configured securely

**User Experience Polish:**

```svelte
<!-- Login button states -->
<script>
  let loading = $state(false);
  let error = $state('');
</script>

{#if error}
  <div role="alert" class="error">
    {error}
  </div>
{/if}

<button 
  on:click={handleLogin} 
  disabled={loading}
  aria-busy={loading}
>
  {#if loading}
    <span class="spinner" aria-hidden="true" />
    Connecting...
  {:else}
    Sign in with Heartwood
  {/if}
</button>
```

**Monitoring & Logging:**

```typescript
// Log auth events (without sensitive data)
logger.info('User authenticated', {
  userId: user.id,
  provider: 'heartwood',
  ip: event.getClientAddress(),
});

// Alert on suspicious activity
if (failedAttempts > 10) {
  logger.warn('Potential brute force attack', {
    identifier,
    attempts: failedAttempts,
  });
}
```

**Documentation:**

```markdown
## Authentication System

### Architecture
- OAuth 2.0 with PKCE for secure token exchange
- Session-based auth for web app
- Heartwood (GroveAuth) as identity provider

### Flow
1. User clicks "Sign in" → Redirect to Heartwood
2. User authenticates with Heartwood
3. Heartwood redirects back with auth code
4. App exchanges code for tokens
5. App creates session, sets cookie
6. User is authenticated

### Protected Routes
Add to `src/routes/protected/+page.server.ts`:
```typescript
export const load = async ({ locals }) => {
  if (!locals.user) {
    throw redirect(302, '/auth/login');
  }
  return { user: locals.user };
};
```

### Environment Variables
See `.env.example` for required variables.
```

**Completion Report:**

```markdown
## 🕷️ SPIDER WEAVE COMPLETE

### Auth System Integrated
- Provider: Heartwood (GroveAuth)
- Flow: OAuth 2.0 + PKCE
- Session: Cookie-based, 7-day expiry

### Files Created
- `src/lib/auth/` (6 files)
- `src/routes/auth/login/+server.ts`
- `src/routes/auth/callback/+server.ts`
- `src/routes/auth/logout/+server.ts`
- `src/lib/stores/auth.ts`

### Security Features
- ✅ PKCE for OAuth
- ✅ CSRF protection
- ✅ Rate limiting (5 attempts / 15 min)
- ✅ Secure cookie attributes
- ✅ Security headers
- ✅ Role-based access control

### Tests
- 15 unit tests
- 8 integration tests
- 100% pass rate

*The web is woven. The system is secure.* 🕷️
```

**Output:** Auth system complete, tested, documented, monitoring in place

---

## Spider Rules

### Patience
Weave one thread at a time. Don't rush to connect everything at once. Each strand must be secure before adding the next.

### Precision
Small mistakes in auth have big consequences. Verify every redirect, check every token, validate every session.

### Completeness
A web with holes catches nothing. Test the error paths, the edge cases, the failure modes. Security is only as strong as the weakest strand.

### Communication
Use weaving metaphors:
- "Spinning the threads..." (creating foundations)
- "Connecting the strands..." (linking components)
- "Testing the knots..." (security hardening)
- "The web holds..." (verification complete)

---

## Anti-Patterns

**The spider does NOT:**
- Store passwords in plain text (ever)
- Skip PKCE in OAuth flows
- Trust user input without validation
- Leave default secrets in configuration
- Ignore session expiration
- Log sensitive data (tokens, passwords)

---

## Example Weave

**User:** "Add GitHub OAuth login"

**Spider flow:**

1. 🕷️ **SPIN** — "Create OAuth app in GitHub, generate client credentials, set up PKCE utilities, create auth endpoints structure"

2. 🕷️ **CONNECT** — "Implement /auth/github/login redirect, /auth/github/callback handler, user upsert logic, session creation"

3. 🕷️ **SECURE** — "Add CSRF state validation, secure cookie settings, rate limiting on auth endpoints, role assignment for new users"

4. 🕷️ **TEST** — "Test OAuth flow, callback handling, session creation, protected route access, error cases (denied permissions)"

5. 🕷️ **BIND** — "Add login button to UI, error state handling, loading states, documentation, monitoring"

---

## Quick Decision Guide

| Situation | Approach |
|-----------|----------|
| Simple app, internal users | Session-based auth |
| Public app, social login | OAuth 2.0 + PKCE |
| API for mobile/SPA | JWT with refresh tokens |
| Service-to-service | API keys with IP allowlist |
| Grove ecosystem | Heartwood integration |

---

## Integration with Other Skills

**Before Weaving:**
- `eagle-architect` — For auth system design
- `swan-design` — For auth flow specifications

**During Weaving:**
- `elephant-build` — For multi-file auth implementation
- `raccoon-audit` — For security review

**After Weaving:**
- `beaver-build` — For auth testing
- `deer-sense` — For accessibility audit of login UI

---

*A well-woven web catches intruders while letting friends pass through.* 🕷️
