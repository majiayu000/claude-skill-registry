---
name: spider-weave
description: Weave authentication webs with patient precision. Spin the threads, connect the strands, secure the knots, and bind the system. Use when integrating auth, setting up OAuth, or securing routes.
---

# Spider Weave

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
SPIN --> CONNECT --> SECURE --> TEST --> BIND
  |         |          |          |        |
Create    Link       Harden    Verify   Lock In
Threads  Strands     Knots      Web    Security
```

### Phase 1: SPIN

*The spider spins the first thread, anchoring it carefully in the corner of the frame...*

Create the foundational auth structure. Choose a pattern, scaffold the files, define the schema, and wire environment variables before writing a line of logic.

- Choose the auth pattern: Session, JWT, OAuth 2.0, PKCE, or API Keys — based on app type and user needs
- Scaffold `src/lib/auth/` with `index.ts`, `types.ts`, `session.ts`, `middleware.ts`, `pkce.ts`, `client.ts`
- Define the users and sessions tables in the database schema
- Set required environment variables: client IDs, secrets, authorize/token/userinfo URLs, redirect URI, session secret

**Reference:** Load `references/oauth-pkce-flow.md` for PKCE setup code, database schema, env var list, and the full file structure

---

### Phase 2: CONNECT

*Thread connects to thread, the web taking shape across the frame...*

Link the auth system together: implement the OAuth login redirect, the callback handler, user upsert, and session creation. Then wire up the client-side auth store.

- Implement the login route: generate PKCE verifier + challenge, set cookies, redirect to provider
- Implement the callback route: verify state, exchange code for tokens, fetch userinfo, upsert user, create session, clean up PKCE cookies
- Build session creation (`createSession`), validation (`validateSession`), and invalidation (`invalidateSession`)
- Set up the client-side `auth` store with `loadUser()` for reactive auth state in Svelte

**Reference:** Load `references/oauth-pkce-flow.md` for the complete login and callback route implementations, and `references/session-management.md` for session functions and the auth store

---

### Phase 3: SECURE

*The spider tests each knot, tightening what holds loose, cutting what doesn't belong...*

Harden the authentication system before trusting it with users. Add route protection, security headers, CSRF validation, and rate limiting.

- Implement `requireAuth()` middleware that validates sessions in `hooks.server.ts`
- Implement `requireRole(allowedRoles)` for RBAC — 403 on unauthorized access
- Set security headers on every response: `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Content-Security-Policy`
- Add CSRF origin validation for state-changing endpoints
- Add rate limiting: 5 attempts per 15 minutes per IP on auth endpoints

**Reference:** Load `references/route-protection.md` for middleware code and RBAC patterns, and `references/security-headers.md` for headers, CSRF, rate limiting, and Cloudflare edge rules

---

### Phase 4: TEST

*The spider plucks the strands, verifying each vibrates true at the right frequency...*

Test authentication thoroughly across the happy path, security edge cases, and failure modes. Automated tests catch regressions; security tests verify the knots hold.

- Test the full OAuth flow: redirects with PKCE challenge, callback handling, session creation
- Test route protection: unauthenticated redirect, authenticated access, role enforcement
- Test security properties: CSRF state rejection, secure cookie attributes, session fixation prevention
- Cover failure modes: expired sessions, invalid codes, denied OAuth permissions

**Reference:** Load `references/oauth-pkce-flow.md` for OAuth flow tests and `references/route-protection.md` for route protection test suite

---

### Phase 5: BIND

*The web is complete, every strand bound tight, the whole stronger than the sum of its threads...*

Finalize and lock in the authentication. Polish the user experience, configure monitoring, and produce the completion report.

- Verify the integration checklist: login, logout, protected routes, session expiry, error handling, rate limiting, CSRF, headers, cookies
- Add login UI loading and error states with proper `aria-busy` and `role="alert"` attributes
- Configure auth event logging (userId, provider, IP — never tokens or passwords)
- Alert on suspicious activity (10+ failed attempts from same identifier)
- Generate the completion report: provider, flow type, files created, security features confirmed, test counts

**Reference:** Load `references/session-management.md` for the full integration checklist, login UI snippet, monitoring patterns, and completion report template. Load `references/heartwood-integration.md` for Grove-specific logout flow and role assignment.

---

## Reference Routing Table

| Phase | Reference | Load When |
|-------|-----------|-----------|
| SPIN | `references/oauth-pkce-flow.md` | Always — foundation code lives here |
| CONNECT | `references/oauth-pkce-flow.md` + `references/session-management.md` | Implementing login/callback/session |
| SECURE | `references/route-protection.md` + `references/security-headers.md` | Adding middleware, headers, rate limiting |
| TEST | `references/oauth-pkce-flow.md` + `references/route-protection.md` | Writing auth and route tests |
| BIND | `references/session-management.md` + `references/heartwood-integration.md` | Finalizing, logging, reporting |
| Grove/Heartwood | `references/heartwood-integration.md` | Any Grove ecosystem integration |

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
- Reflect `redirect_uri` or `next` parameters without validation (open redirect)
- Assign admin roles via OAuth claims (manual DB assignment only)

---

## Example Weave

**User:** "Add GitHub OAuth login"

**Spider flow:**

1. **SPIN** — "Create OAuth app in GitHub, generate client credentials, set up PKCE utilities, create auth endpoints structure"

2. **CONNECT** — "Implement /auth/github/login redirect, /auth/github/callback handler, user upsert logic, session creation"

3. **SECURE** — "Add CSRF state validation, secure cookie settings, rate limiting on auth endpoints, role assignment for new users"

4. **TEST** — "Test OAuth flow, callback handling, session creation, protected route access, error cases (denied permissions)"

5. **BIND** — "Add login button to UI, error state handling, loading states, documentation, monitoring"

---

## Quick Decision Guide

| Situation | Approach |
|-----------|----------|
| Simple app, internal users | Session-based auth |
| Public app, social login | OAuth 2.0 + PKCE |
| API for mobile/SPA | JWT with refresh tokens |
| Service-to-service | API keys with IP allowlist |
| Grove ecosystem | Heartwood integration (load `references/heartwood-integration.md`) |

---

## Integration with Other Skills

**Before Weaving:**
- `eagle-architect` — For auth system design decisions
- `swan-design` — For auth flow specifications

**During Weaving:**
- `elephant-build` — For multi-file auth implementation
- `raccoon-audit` — For security review

**After Weaving:**
- `beaver-build` — For auth testing
- `turtle-harden` — For defense-in-depth hardening beyond the web
- `deer-sense` — For accessibility audit of login UI

---

*A well-woven web catches intruders while letting friends pass through.*
