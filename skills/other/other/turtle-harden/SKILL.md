---
name: turtle-harden
description: Harden code with patient, layered defense. The turtle carries its shell — bone-deep protection grown from within, not strapped on. Use when building new features to ensure they're secure by design, or when auditing existing code for deep vulnerabilities that slip through standard reviews.
---

# Turtle Harden 🐢

The turtle doesn't rush. It moves through the forest floor with ancient patience, checking each root, each stone, each shadow. Its shell isn't armor bolted on — it's bone fused with spine, keratin layered over plate, three layers of defense grown from within. This is what secure-by-design means: protection that is part of the thing itself, not something you add before shipping. Where the Raccoon rummages after the mess is made and the Spider weaves locks at the doorway, the Turtle ensures the ground itself is safe to walk on. Defense in depth. Every layer. Every time.

## When to Activate

- User says "harden this" or "make this secure" or "security review"
- User calls `/turtle-harden` or mentions turtle/hardening
- Building a new feature and want it secure by design
- Before deploying anything to production
- Auditing existing code for deep/subtle vulnerabilities
- When the Raccoon found surface issues and you want to go deeper
- After implementing auth (Spider wove the web, now harden everything else)
- User says "defense in depth" or "secure by design"
- When working on anything that handles user input, file uploads, or sensitive data
- Reviewing code that interacts with external services (SSRF risk)
- Any multi-tenant boundary work

**IMPORTANT:** The Turtle is thorough by nature. Do not skip phases. Do not rush. A shell with gaps protects nothing.

**Pair with:** `raccoon-audit` for secret scanning first, `spider-weave` for auth implementation, `beaver-build` for writing security regression tests

---

## The Hardening

```
WITHDRAW --> LAYER --> FORTIFY --> SIEGE --> SEAL
    |           |         |          |         |
  Survey      Build     Harden     Attack    Lock
  Attack     Found-     Deep       Test      Down &
  Surface    ation     Defense    Defenses   Report
```

### Phase 1: WITHDRAW

_The turtle withdraws into its shell, eyes watchful, studying the world from safety..._

Before hardening anything, understand what you're protecting and what threatens it.

**Identify the Scope:**

- What code/feature/system is being reviewed?
- Is this new code (secure-by-design) or existing code (audit)?
- What is the threat model? (public-facing? internal? multi-tenant?)

**Map the Attack Surface:**

```
ENTRY POINTS (Where data comes in):
[ ] URL parameters and query strings
[ ] Form submissions and POST bodies
[ ] HTTP headers (Host, Referer, X-Forwarded-*, custom headers)
[ ] Cookies
[ ] File uploads
[ ] WebSocket messages
[ ] postMessage from iframes/popups
[ ] URL fragments (client-side)
[ ] API request bodies (JSON, XML, multipart)
[ ] Webhooks from external services
[ ] Database reads (second-order injection)
[ ] Environment variables / config files

EXIT POINTS (Where data goes out):
[ ] HTML responses (XSS surface)
[ ] HTTP response headers
[ ] JSON API responses (data leakage)
[ ] Database writes (injection surface)
[ ] External API calls (SSRF surface)
[ ] Email content
[ ] Log files (sensitive data leakage)
[ ] Error messages (information disclosure)
[ ] Redirects (open redirect surface)
```

**Catalog Data Flows:**
For each piece of sensitive data (credentials, PII, tokens, payment info):

1. Where does it enter the system?
2. Where is it stored?
3. Where is it transmitted?
4. Where is it displayed/output?
5. When is it deleted?

**Tech Stack Assessment:**
Check for known vulnerability patterns in the stack:

- SvelteKit: Layout bypass, server-only module leaks, CSP nonce handling
- Cloudflare Workers: Secret storage, subrequest limits, V8 isolate boundaries
- TypeScript/JavaScript: Prototype pollution, type coercion, eval patterns
- D1/SQLite: SQL injection, parameter binding, tenant isolation

**Output:** Complete attack surface map with entry points, exit points, data flows, and tech-specific risks

---

### Phase 2: LAYER

_Layer by layer, the shell grows stronger. Keratin over bone, bone over spine..._

Apply the foundational defenses. These are non-negotiable — every piece of code must have these layers.

**2A. Input Validation & Sanitization**

Every entry point identified in Phase 1 must be validated:

```
VALIDATION CHECKLIST:
[ ] All user input is validated SERVER-SIDE (client-side is UX only)
[ ] Validation uses ALLOWLISTS, not blocklists
[ ] Strict type constraints enforced (string, number, boolean — never trust incoming types)
[ ] Length limits enforced on all string inputs
[ ] Range limits enforced on all numeric inputs
[ ] Format validation for structured data (email, URL, date, UUID)
[ ] Runtime schema validation at API boundaries (Zod, Valibot, or equivalent)
[ ] Invalid input is REJECTED with an error, not silently "fixed" or coerced
[ ] Null bytes, control characters, and Unicode normalization handled
[ ] Content-Type header validated on all incoming requests
```

**SvelteKit pattern:**

```typescript
// +page.server.ts or +server.ts
import { z } from "zod";

const CreatePostSchema = z.object({
  title: z.string().min(1).max(200).trim(),
  content: z.string().min(1).max(50000),
  slug: z
    .string()
    .regex(/^[a-z0-9-]+$/)
    .max(100),
});

export const actions = {
  default: async ({ request, locals }) => {
    const formData = await request.formData();
    const result = CreatePostSchema.safeParse({
      title: formData.get("title"),
      content: formData.get("content"),
      slug: formData.get("slug"),
    });

    if (!result.success) {
      return fail(400, { errors: result.error.flatten() });
    }

    // result.data is now typed and validated
  },
};
```

**2B. Output Encoding**

Every exit point must encode data for its context:

```
ENCODING CHECKLIST:
[ ] HTML context: HTML entity encoding (< > & " ')
[ ] JavaScript context: JavaScript encoding (\xHH)
[ ] URL context: Percent encoding (%HH)
[ ] CSS context: CSS encoding (\HHHHHH)
[ ] JSON API responses: Proper serialization (no raw HTML in JSON values)
[ ] SVG context: Full sanitization (strip scripts, event handlers, foreignObject)
[ ] Rich text output uses DOMPurify or equivalent with strict allowlist
[ ] innerHTML / @html (Svelte) NEVER used with unsanitized user input
```

**SvelteKit pattern:**

```svelte
<!-- DANGEROUS: Never do this with user input -->
{@html userContent}

<!-- SAFE: Svelte auto-escapes by default -->
{userContent}

<!-- SAFE: If you MUST render HTML, sanitize first -->
{@html DOMPurify.sanitize(userContent, { ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'] })}
```

**2C. Parameterized Queries**

```
DATABASE CHECKLIST:
[ ] ALL database queries use parameterized statements / prepared statements
[ ] ZERO string concatenation in SQL queries
[ ] Table and column names validated against alphanumeric pattern (never from user input)
[ ] Use the typed query helpers from database.ts where available
[ ] Each independent query has its own try/catch (no cascading failures)
[ ] Independent queries run in parallel with Promise.all()
```

**Pattern:**

```typescript
// NEVER: String concatenation
const results = await db
  .prepare(`SELECT * FROM posts WHERE slug = '${slug}'`)
  .all();

// ALWAYS: Parameterized
const results = await db
  .prepare("SELECT * FROM posts WHERE slug = ?")
  .bind(slug)
  .all();

// BEST: Typed query helper
const post = await findById<Post>(db, "posts", postId);
```

**2D. Type Safety & Secure Defaults**

```
TYPE SAFETY CHECKLIST:
[ ] TypeScript strict mode enabled ("strict": true)
[ ] strictNullChecks enabled
[ ] No use of 'any' type (use 'unknown' with type guards)
[ ] No eval(), new Function(), setTimeout(string), setInterval(string)
[ ] No dynamic import() with user-controlled paths
[ ] Object.create(null) for dictionaries (no prototype chain)
[ ] Map/Set instead of plain objects where appropriate
[ ] Explicit return types on security-critical functions
```

**2E. Error Handling (Signpost Standard)**

Every error MUST use a Signpost error code. No bare `throw new Error()` or `throw error(500, ...)`.

```
ERROR HANDLING CHECKLIST (SIGNPOST):
[ ] All errors use a Signpost code from the appropriate catalog
    (API_ERRORS, ARBOR_ERRORS, SITE_ERRORS, AUTH_ERRORS, PLANT_ERRORS)
[ ] logGroveError() called for all server-side errors (never console.error alone)
[ ] API routes return buildErrorJson() — never ad-hoc JSON error shapes
[ ] Page loads use throwGroveError() for expected errors (renders in +error.svelte)
[ ] userMessage is warm, clear, and contains NO technical details
[ ] adminMessage is detailed and actionable (for logs/dashboards only)
[ ] Error category is correct: "user" (they can fix), "admin" (config), "bug" (investigate)
[ ] Client-side actions show toast.success() or toast.error() feedback
[ ] Production error pages show GENERIC userMessage only (no stack traces)
[ ] Different errors produce the SAME response for auth (no user enumeration)
    "Invalid credentials" — never "user not found" vs "wrong password"
[ ] adminMessage never reaches the client (information disclosure prevention)
[ ] try/catch blocks don't silently swallow errors — at minimum logGroveError()
```

See `AgentUsage/error_handling.md` for the complete Signpost reference.

**Output:** Foundational defenses applied to all entry and exit points

---

### Phase 3: FORTIFY

_Each plate of the shell interlocks with the next. No gaps. No seams. No way through..._

Apply deep, layered hardening. These are the defenses that make the difference between "has authentication" and "is actually secure."

**3A. HTTP Security Headers**

Every response must include these headers:

```
REQUIRED HEADERS:
[ ] Content-Security-Policy        — Strict nonce-based or hash-based policy
[ ] Strict-Transport-Security      — max-age=31536000; includeSubDomains; preload
[ ] X-Content-Type-Options         — nosniff
[ ] X-Frame-Options                — DENY (or SAMEORIGIN if framing needed)
[ ] Referrer-Policy                — strict-origin-when-cross-origin (or no-referrer)
[ ] Permissions-Policy             — Disable unused: camera=(), microphone=(), geolocation=()
[ ] Cross-Origin-Opener-Policy     — same-origin
[ ] Cross-Origin-Embedder-Policy   — require-corp (if using SharedArrayBuffer)
[ ] Cross-Origin-Resource-Policy   — same-origin or same-site

REMOVE / DISABLE:
[ ] X-Powered-By                   — Remove entirely (leaks framework info)
[ ] Server                         — Remove or genericize (leaks server software)
[ ] X-XSS-Protection              — Set to 0 if present (deprecated, can cause issues)
```

**SvelteKit pattern (hooks.server.ts):**

```typescript
export const handle: Handle = async ({ event, resolve }) => {
  const response = await resolve(event);

  response.headers.set("X-Frame-Options", "DENY");
  response.headers.set("X-Content-Type-Options", "nosniff");
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  response.headers.set(
    "Permissions-Policy",
    "camera=(), microphone=(), geolocation=(), payment=()",
  );
  response.headers.delete("X-Powered-By");

  return response;
};
```

**3B. Content Security Policy (CSP)**

```
CSP CHECKLIST:
[ ] CSP delivered via HTTP header (not <meta> tag alone)
[ ] Uses nonce-based or hash-based approach (strict CSP)
[ ] default-src set to 'self' or more restrictive
[ ] script-src does NOT contain 'unsafe-inline' (use nonces instead)
[ ] script-src does NOT contain 'unsafe-eval'
[ ] No wildcard * sources (except possibly subdomains of owned domains)
[ ] object-src set to 'none'
[ ] base-uri set to 'self' or 'none'
[ ] frame-ancestors set to 'none' (unless framing is intentional)
[ ] form-action restricted to trusted origins
[ ] style-src is restrictive (CSS injection is a real exfiltration vector)
[ ] Nonces are cryptographically random and regenerated per response
[ ] report-uri or report-to configured for violation monitoring
[ ] Tested in Report-Only mode before enforcement
```

**SvelteKit CSP config (svelte.config.js):**

```javascript
kit: {
  csp: {
    mode: 'auto', // Adds nonces automatically
    directives: {
      'default-src': ['self'],
      'script-src': ['self', 'nonce'],
      'style-src': ['self', 'unsafe-inline'], // Svelte needs this, unfortunately
      'img-src': ['self', 'data:', 'https://cdn.grove.place'],
      'font-src': ['self'],
      'object-src': ['none'],
      'base-uri': ['self'],
      'frame-ancestors': ['none'],
      'form-action': ['self'],
    }
  }
}
```

**3C. CORS Configuration**

```
CORS CHECKLIST:
[ ] Access-Control-Allow-Origin is NEVER set to * in production
[ ] Origin is validated against an EXACT allowlist (no regex that can be bypassed)
[ ] Origin is NEVER reflected verbatim from the request
[ ] null origin is NOT allowed (exploitable via sandboxed iframes)
[ ] Access-Control-Allow-Credentials is only true when necessary
[ ] Access-Control-Allow-Methods restricted to actually needed methods
[ ] Access-Control-Allow-Headers restricted to actually needed headers
[ ] Access-Control-Max-Age set to limit preflight caching
[ ] CORS is configured per-endpoint, not globally
```

**Bad CORS (common mistake):**

```typescript
// DANGEROUS: Reflects any origin
response.headers.set(
  "Access-Control-Allow-Origin",
  request.headers.get("Origin"),
);

// DANGEROUS: Allows all origins with credentials
response.headers.set("Access-Control-Allow-Origin", "*");
```

**Safe CORS:**

```typescript
const ALLOWED_ORIGINS = new Set([
  "https://grove.place",
  "https://meadow.grove.place",
]);

const origin = request.headers.get("Origin");
if (origin && ALLOWED_ORIGINS.has(origin)) {
  response.headers.set("Access-Control-Allow-Origin", origin);
  response.headers.set("Vary", "Origin");
}
```

**3D. Session & Cookie Security**

```
SESSION CHECKLIST:
[ ] Session IDs generated with crypto.getRandomValues() or equivalent CSPRNG
[ ] Session IDs are at least 128 bits (32 hex chars)
[ ] Session ID regenerated after successful authentication (prevent fixation)
[ ] Session ID regenerated after privilege escalation
[ ] Idle timeout enforced (15-30 min for sensitive apps)
[ ] Absolute session timeout enforced (even active sessions expire)
[ ] Logout fully invalidates session server-side (not just clearing cookie)
[ ] Sessions are NEVER transmitted via URL parameters
[ ] Concurrent session limits enforced where appropriate

COOKIE CHECKLIST:
[ ] HttpOnly flag set (prevents JavaScript access)
[ ] Secure flag set (HTTPS-only transmission)
[ ] SameSite=Strict or SameSite=Lax (CSRF defense layer)
[ ] Path scoped as narrowly as possible
[ ] Domain scoped as narrowly as possible
[ ] Reasonable expiration (not years)
[ ] __Host- prefix used where possible (strictest cookie scope)
```

**3E. CSRF Protection**

```
CSRF CHECKLIST:
[ ] Anti-CSRF tokens on ALL state-changing requests
[ ] CSRF tokens are per-session and cryptographically random
[ ] CSRF tokens validated server-side on every state-changing request
[ ] SameSite cookie attribute set as additional defense layer
[ ] State-changing operations use POST/PUT/DELETE, never GET
[ ] SvelteKit form actions have built-in CSRF — verify it's not disabled
[ ] For multi-tenant proxy setup: csrf.trustedOrigins configured correctly
[ ] Origin header validated on non-form API endpoints
```

**Grove-specific CSRF (svelte.config.js):**

```javascript
kit: {
  csrf: {
    checkOrigin: true,
    trustedOrigins: [
      'https://grove.place',
      'https://*.grove.place',
      'http://localhost:5173',
    ],
  },
}
```

**3F. Rate Limiting**

```
RATE LIMITING CHECKLIST:
[ ] Authentication endpoints rate-limited (5-10 attempts per 15 min)
[ ] Password reset rate-limited (3 attempts per hour)
[ ] API endpoints rate-limited per-user/per-IP
[ ] File upload endpoints rate-limited
[ ] Search/expensive query endpoints rate-limited
[ ] Rate limit headers returned (X-RateLimit-Remaining, Retry-After)
[ ] Rate limits applied BEFORE expensive operations (not after)
[ ] Different limits for authenticated vs unauthenticated requests
[ ] Cloudflare rate limiting rules configured for edge enforcement
```

**3G. Authentication Hardening**

```
AUTH CHECKLIST:
[ ] Passwords hashed with Argon2id (preferred) or bcrypt (cost 12+)
[ ] No MD5, SHA-1, SHA-256, or any unsalted hash for passwords
[ ] Salts auto-generated by hashing algorithm
[ ] Login errors don't reveal whether username or password was wrong
[ ] Account enumeration prevented on registration, login, and password reset
[ ] Password reset tokens are single-use, time-limited, cryptographically random
[ ] MFA available for sensitive operations
[ ] Brute-force protections: rate limiting, progressive delays, account lockout
[ ] OAuth: PKCE flow used (not implicit grant)
[ ] OAuth: State parameter validated (CSRF in OAuth flow)
[ ] OAuth: Redirect URIs are exact-match (no wildcards)
[ ] JWT: Algorithm explicitly whitelisted (reject 'none' algorithm)
[ ] JWT: Signature ALWAYS verified (never just decoded)
[ ] JWT: Short expiry (5-15 min for access tokens)
[ ] JWT: Claims validated (iss, aud, exp, nbf)
[ ] JWT: Stored in HttpOnly cookies, NOT localStorage
[ ] JWT: Different signing keys per environment
```

**3H. Authorization**

```
AUTHORIZATION CHECKLIST:
[ ] Authorization checked server-side on EVERY request
[ ] Object-level authorization: User A cannot access User B's resources (IDOR prevention)
[ ] Function-level authorization: Regular users cannot access admin endpoints
[ ] Property-level authorization: Sensitive fields filtered from responses by role
[ ] Default deny: All access denied unless explicitly granted
[ ] Horizontal escalation tested: Can user A read/write/delete user B's data?
[ ] Vertical escalation tested: Can regular users reach admin functions?
[ ] Authorization enforced in hooks.server.ts, NOT just layout files
    (SvelteKit layouts can be bypassed by parallel loading)
[ ] API routes verify auth BEFORE processing
```

**3I. Multi-Tenant Isolation**

```
MULTI-TENANT CHECKLIST:
[ ] Tenant context resolved at request boundary, BEFORE business logic
[ ] EVERY database query includes tenant scoping (WHERE tenant_id = ?)
[ ] Row-Level Security enforced at database level as secondary layer
[ ] Cross-tenant data access tested: Tenant A cannot reach Tenant B's data
[ ] API responses scoped to authenticated tenant
[ ] Background jobs carry explicit tenant context
[ ] File storage isolated per tenant (separate R2 prefixes or buckets)
[ ] Logs include tenant context for auditability
[ ] Resource limits enforced per tenant (storage, API calls, compute)
[ ] Tenant deletion fully purges ALL associated data
[ ] Cache keys include tenant ID (no cache pollution between tenants)
```

**3J. File Upload Security**

```
FILE UPLOAD CHECKLIST:
[ ] File types validated via ALLOWLIST of extensions AND MIME types
[ ] File content inspected (magic bytes), not just extension or Content-Type
[ ] Uploaded files renamed to server-generated random names (hash + timestamp)
[ ] Original filenames sanitized (remove ../, ..\, null bytes, special chars)
[ ] File size limits enforced (per-file AND per-request)
[ ] Files stored OUTSIDE web root (not publicly accessible by path)
[ ] Files stored on separate host/domain/storage where possible (R2)
[ ] Execute permissions NOT set on uploaded files
[ ] Content-Disposition: attachment set when serving user files
[ ] X-Content-Type-Options: nosniff set when serving user files
[ ] Images re-processed server-side (strip metadata, re-encode)
[ ] SVGs sanitized with DOMPurify (strip scripts, event handlers, foreignObject)
[ ] No user-controlled paths in file operations (path traversal prevention)
```

**3K. Data Protection**

```
DATA PROTECTION CHECKLIST:
[ ] All data in transit uses TLS 1.2+ (TLS 1.0/1.1 and SSLv3 disabled)
[ ] HSTS enabled with max-age of at least 6 months
[ ] Sensitive data at rest encrypted (AES-256-GCM or equivalent)
[ ] Secrets stored in environment variables or secrets vault, never in source code
[ ] .env files in .gitignore and never committed
[ ] PII minimized: only collect/store what's strictly necessary
[ ] Backups encrypted and access-controlled
[ ] Data retention policies defined and enforced
[ ] Logging does NOT capture passwords, tokens, full card numbers, SSNs, or PII
[ ] Database credentials use least-privilege accounts
[ ] Cloudflare Workers secrets stored in Workers Secrets (encrypted at rest)
[ ] Constant-time comparison used for secrets/tokens (crypto.timingSafeEqual)
```

**Output:** Deep, layered defenses applied across all security domains

---

### Phase 4: SIEGE

_Test the shell. Strike it. Push it. Try every angle. What holds is worthy. What breaks is found before the enemy finds it..._

Think like an attacker. This phase checks for the subtle, exotic vulnerabilities that slip through standard reviews. For each category, attempt the attack mentally (or practically if safe to do so) and verify defenses hold.

**4A. Prototype Pollution**

```
CHECK:
[ ] No deep merge/extend operations on user-controlled objects
[ ] Keys like __proto__, constructor, and prototype rejected in object merging
[ ] Object.create(null) used for dictionaries instead of {}
[ ] lodash.merge, jQuery.extend, or similar deep-merge not used with user input
[ ] If deep merge is needed, library is patched/updated for prototype pollution
[ ] Consider Object.freeze(Object.prototype) in sensitive contexts
```

**What to look for:**

```typescript
// DANGEROUS: Deep merging user input
const config = deepMerge(defaults, userInput);
// Attacker sends: { "__proto__": { "isAdmin": true } }
// Now ({}).isAdmin === true for ALL objects

// SAFE: Validate keys before merging
function safeMerge(target, source) {
  for (const key of Object.keys(source)) {
    if (key === "__proto__" || key === "constructor" || key === "prototype")
      continue;
    target[key] = source[key];
  }
  return target;
}
```

**4B. Timing Side-Channel Attacks**

```
CHECK:
[ ] Secret/token comparison uses crypto.timingSafeEqual(), not === or ==
[ ] HMAC verification uses constant-time comparison
[ ] Database lookups for auth don't reveal user existence via timing
    (Query for user + verify password even when user doesn't exist)
[ ] API key validation doesn't exit early on mismatch
```

**What to look for:**

```typescript
// DANGEROUS: Early-exit comparison leaks information
if (providedToken === storedToken) { ... }

// SAFE: Constant-time comparison
import { timingSafeEqual } from 'crypto';
const a = Buffer.from(providedToken);
const b = Buffer.from(storedToken);
if (a.length === b.length && timingSafeEqual(a, b)) { ... }
```

**4C. Race Conditions (TOCTOU)**

```
CHECK:
[ ] Single-use tokens (coupons, invites, password resets) use atomic operations
    (SELECT FOR UPDATE, or unique constraint + INSERT, not check-then-act)
[ ] Financial operations use database-level locking or transactions
[ ] Rate limiting uses atomic increment (not read-check-write)
[ ] File operations use exclusive locks where needed
[ ] Idempotency keys used for non-idempotent operations
[ ] State transitions validated atomically (can't skip states)
```

**What to look for:**

```typescript
// DANGEROUS: Check-then-act (race condition)
const coupon = await db.query(
  "SELECT * FROM coupons WHERE code = ? AND used = 0",
  [code],
);
if (coupon) {
  await applyDiscount(coupon);
  await db.query("UPDATE coupons SET used = 1 WHERE code = ?", [code]);
  // Two concurrent requests can both pass the check before either updates!
}

// SAFE: Atomic operation
const result = await db.query(
  "UPDATE coupons SET used = 1 WHERE code = ? AND used = 0 RETURNING *",
  [code],
);
if (result.rows.length > 0) {
  await applyDiscount(result.rows[0]);
}
```

**4D. Regular Expression Denial of Service (ReDoS)**

```
CHECK:
[ ] No user-supplied regex patterns
[ ] Regex patterns reviewed for catastrophic backtracking
    Dangerous patterns: (a+)+, ([a-zA-Z]+)*, (a|aa)+, (.*a){x}
[ ] Input length limited BEFORE regex evaluation
[ ] Consider RE2 or other non-backtracking engine for user-facing patterns
[ ] Email validation uses a simple pattern, not an RFC-complete monster regex
[ ] URL parsing uses URL() constructor, not regex
```

**What to look for:**

```typescript
// DANGEROUS: Catastrophic backtracking
const emailRegex = /^([a-zA-Z0-9]+)*@([a-zA-Z0-9]+)*\.([a-zA-Z]+)*$/;
// Input: "aaaaaaaaaaaaaaaaaaaaaa" causes exponential backtracking

// SAFE: Simple, non-backtracking validation
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
// Or better: use a validation library (Zod's z.string().email())
```

**4E. Server-Side Request Forgery (SSRF)**

```
CHECK:
[ ] Any URL/hostname from user input validated against strict ALLOWLIST
[ ] IP addresses from DNS resolution validated IMMEDIATELY before connection
    (not separately — DNS rebinding sends different IPs on each resolution)
[ ] RFC 1918 addresses blocked: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
[ ] Loopback blocked: 127.0.0.0/8, [::1], localhost (including decimal/octal/hex variants)
[ ] Link-local blocked: 169.254.0.0/16, [fe80::]/10
[ ] Cloud metadata endpoints blocked: 169.254.169.254, metadata.google.internal
[ ] Redirect following disabled (or redirects re-validated at each hop)
[ ] URL parsing is consistent (no parser confusion between validation and request)
[ ] file://, gopher://, dict://, and other non-HTTP schemes rejected
[ ] IMDSv2 used on AWS (requires session token, blocks SSRF to metadata)
```

**4F. CRLF Injection**

```
CHECK:
[ ] CR (\r) and LF (\n) stripped from ALL values used in HTTP headers
[ ] Redirect URLs sanitized (no newlines in Location header)
[ ] Set-Cookie values sanitized
[ ] Custom headers built from user input sanitized
[ ] Log entries sanitized (prevent log injection/forging)
```

**4G. Unicode & Encoding Attacks**

```
CHECK:
[ ] Security filters applied AFTER Unicode normalization (NFC/NFKC), not before
[ ] Homoglyph attacks considered for usernames and display names
    (Cyrillic 'a' U+0430 looks identical to Latin 'a' U+0061)
[ ] Bidirectional text characters stripped from code inputs (Trojan Source)
[ ] Zero-width characters stripped from security-sensitive inputs
[ ] Character set allowlists used where possible
[ ] Case-insensitive comparisons use locale-independent methods
```

**4H. Deserialization**

```
CHECK:
[ ] JSON.parse() used instead of custom deserialization libraries
[ ] No node-serialize, serialize-to-js, funcster, or similar used with untrusted input
[ ] If custom serialization required: strict schema validation with property allowlist
[ ] Cookie values are JSON, not serialized JavaScript objects
[ ] Webhook payloads validated against expected schema before processing
```

**4I. postMessage Security**

```
CHECK:
[ ] All postMessage listeners validate event.origin with EXACT string comparison
    (not regex, not includes(), not startsWith())
[ ] postMessage sends specify EXACT target origin (never "*")
[ ] Message data treated as untrusted input (validated/sanitized)
[ ] Null origin not accepted (sandboxed iframes have null origin)
[ ] No sensitive data sent via postMessage to untrusted origins
```

**4J. WebSocket Security**

```
CHECK:
[ ] Origin header validated on every WebSocket handshake
[ ] CSRF tokens used in WebSocket handshake request
[ ] Authentication verified (not relying solely on cookies)
[ ] wss:// used exclusively (never ws://)
[ ] Message size limits enforced
[ ] Rate limiting on WebSocket messages
[ ] All WebSocket message payloads validated (injection prevention)
[ ] Connection limits per user/IP
```

**4K. CSS Injection & Data Exfiltration**

```
CHECK:
[ ] User-controlled CSS is not allowed (no custom <style> injection)
[ ] style-src in CSP restricts CSS sources
[ ] HTML sanitization strips <style> tags and style attributes if not needed
[ ] CSRF tokens not in CSS-selectable attribute values
    (CSS: input[value^="a"]{ background: url(leak.com/a) })
[ ] Sensitive form values use type="password" or autocomplete="off" where appropriate
```

**4L. SVG XSS**

```
CHECK:
[ ] SVG uploads sanitized with DOMPurify (strip <script>, event handlers, <foreignObject>)
[ ] User-uploaded SVGs served with Content-Type: image/svg+xml (not text/html)
[ ] Or: SVGs served with Content-Disposition: attachment
[ ] Consider converting SVGs to PNG on upload for maximum safety
[ ] SVGs in <img> tags are safe (browsers block script execution)
[ ] SVGs used inline via {@html} must be sanitized
```

**4M. HTTP Request Smuggling & Cache Poisoning**

```
CHECK:
[ ] HTTP/2 used end-to-end where possible
[ ] No ambiguous Content-Length / Transfer-Encoding headers
[ ] Cloudflare handles front-end parsing (reduces risk if using CF)
[ ] Cache keys include all security-relevant parameters
[ ] Unkeyed headers (X-Forwarded-Host, X-Forwarded-Scheme) not reflected in responses
[ ] Vary header set appropriately for cached responses
[ ] Cache-Control headers set explicitly (no unintended caching of sensitive responses)
```

**4N. Open Redirects**

```
CHECK:
[ ] Redirect URLs validated against allowlist of permitted destinations
[ ] Relative URLs only (reject absolute URLs from user input)
[ ] Or: Parse URL and verify host matches expected domains
[ ] No javascript: or data: schemes in redirect URLs
[ ] redirect_uri in OAuth flows is exact-match (not prefix-match)
```

**4O. HTTP Verb Tampering**

```
CHECK:
[ ] Every route explicitly defines allowed methods
[ ] 405 Method Not Allowed returned for unexpected methods
[ ] Authorization middleware applies to ALL methods, not just GET/POST
[ ] HEAD requests don't bypass auth checks
[ ] SvelteKit: Only exported handlers (GET, POST, etc.) are accessible
```

**4P. Second-Order Vulnerabilities**

```
CHECK:
[ ] Data retrieved from the database is treated as potentially untrusted
[ ] Stored URLs fetched later go through SSRF validation
[ ] Stored usernames/display names encoded on output (stored XSS prevention)
[ ] Stored values used in SQL queries still use parameterized statements
[ ] Webhook URLs stored by users validated on each use, not just on save
```

**4Q. Supply Chain & Dependency Security**

```
CHECK:
[ ] Lock file (pnpm-lock.yaml) committed and reviewed for unexpected changes
[ ] npm audit / pnpm audit run regularly (and in CI)
[ ] No unnecessary dependencies (each dep is an attack surface)
[ ] Dependency versions pinned (no floating ranges in production)
[ ] postinstall scripts reviewed for new dependencies
[ ] Typosquatting checked (package name matches intended package)
[ ] node_modules never committed to version control
```

**4R. Service Worker Risks**

```
CHECK:
[ ] Service worker scope restricted to minimum necessary paths
[ ] CSP restricts which scripts can register service workers
[ ] Service worker updates are signed or integrity-checked
[ ] A "kill switch" service worker deployment is documented and tested
[ ] Clear-Site-Data header available for emergency deregistration
```

**4S. DNS & Infrastructure**

```
CHECK:
[ ] No dangling DNS records (CNAME to decommissioned services)
[ ] Subdomain takeover risk assessed for all DNS records
[ ] Internal services validate Host header (DNS rebinding defense)
[ ] API keys and tokens in Cloudflare Workers use Workers Secrets (not env vars)
```

**Output:** All exotic attack vectors tested, vulnerabilities identified or confirmed absent

---

### Phase 5: SEAL

_The shell is complete. Every gap sealed. Every plate aligned. The turtle endures..._

Final verification and reporting.

**5A. Defense-in-Depth Compliance**

Verify that security is layered — no single control is the only defense:

```
DEFENSE-IN-DEPTH VERIFICATION:
[ ] Network layer:  TLS enforced, HSTS active, rate limiting at edge (Cloudflare)
[ ] Application layer: Input validation, output encoding, CSP, auth, authz
[ ] Data layer: Encryption at rest, parameterized queries, least-privilege DB access
[ ] Infrastructure layer: Secrets management, isolated environments, secure configuration
[ ] Process layer: Code review, automated scanning, dependency auditing
```

**For each critical function, verify at least 2 layers of defense:**

| Function             | Layer 1               | Layer 2            | Layer 3             |
| -------------------- | --------------------- | ------------------ | ------------------- |
| Prevent XSS          | Output encoding       | CSP nonce-based    | Input validation    |
| Prevent CSRF         | SameSite cookies      | CSRF tokens        | Origin validation   |
| Prevent SQLi         | Parameterized queries | Input validation   | Least-privilege DB  |
| Prevent auth bypass  | Session validation    | Rate limiting      | Brute-force lockout |
| Prevent data leakage | Encryption in transit | Encryption at rest | Access control      |
| Tenant isolation     | App-level scoping     | DB-level RLS       | Cache key isolation |

**5B. Logging & Monitoring Verification**

```
LOGGING CHECKLIST:
[ ] Authentication events logged (login, logout, failed attempts, lockouts)
[ ] Authorization failures logged
[ ] Input validation failures logged (potential attack indicator)
[ ] Admin and privileged actions logged
[ ] Logs include: timestamp, user identity, IP, action, resource, result
[ ] Logs do NOT contain: passwords, tokens, session IDs, PII
[ ] Logs protected from tampering (centralized, append-only)
[ ] Alerting configured for: brute force, mass data access, error rate spikes
```

**5C. Build Verification (MANDATORY)**

**Before generating the hardening report, verify the hardened code still builds and passes all checks:**

```bash
# Sync dependencies
pnpm install

# Verify ONLY the packages the turtle touched — lint, check, test, build
gw ci --affected --fail-fast --diagnose
```

**If verification fails:** Hardening introduced a regression. Read the diagnostics, fix the issue (type errors from stricter validation, test failures from tighter security, etc.), re-run verification. The turtle does not seal a broken shell.

**5D. Security-Specific Scan**

```bash
# Check for secrets in code
grep -r "sk-live\|sk-test\|AKIA\|ghp_\|password\s*=" --include="*.{ts,js,json}" .

# Check for dangerous patterns
grep -r "eval(\|innerHTML\|dangerouslySetInnerHTML\|__proto__" --include="*.{ts,js,svelte}" .

# Check for disabled security
grep -r "nocheck\|no-verify\|unsafe-inline\|unsafe-eval" --include="*.{ts,js,json}" .

# Audit dependencies
pnpm audit
```

**5D. Generate Hardening Report**

```markdown
## TURTLE HARDENING REPORT

### Scope

- **Target:** [Feature/system/files reviewed]
- **Mode:** [Secure-by-design review / Existing code audit]
- **Threat model:** [Public-facing / Internal / Multi-tenant]

### Defense Layers Applied

| Layer                    | Status              | Notes                     |
| ------------------------ | ------------------- | ------------------------- |
| Input Validation         | [PASS/FAIL/PARTIAL] | [Details]                 |
| Output Encoding          | [PASS/FAIL/PARTIAL] | [Details]                 |
| SQL Injection Prevention | [PASS/FAIL/PARTIAL] | [Details]                 |
| Security Headers         | [PASS/FAIL/PARTIAL] | [Details]                 |
| CSP                      | [PASS/FAIL/PARTIAL] | [Details]                 |
| CORS                     | [PASS/FAIL/PARTIAL] | [Details]                 |
| Session Security         | [PASS/FAIL/PARTIAL] | [Details]                 |
| CSRF Protection          | [PASS/FAIL/PARTIAL] | [Details]                 |
| Rate Limiting            | [PASS/FAIL/PARTIAL] | [Details]                 |
| Auth Hardening           | [PASS/FAIL/PARTIAL] | [Details]                 |
| Authorization            | [PASS/FAIL/PARTIAL] | [Details]                 |
| Multi-Tenant Isolation   | [PASS/FAIL/PARTIAL] | [N/A if not multi-tenant] |
| File Upload Security     | [PASS/FAIL/PARTIAL] | [N/A if no uploads]       |
| Data Protection          | [PASS/FAIL/PARTIAL] | [Details]                 |

### Exotic Attack Vectors Tested

| Vector               | Status            | Notes |
| -------------------- | ----------------- | ----- |
| Prototype Pollution  | [CLEAR/FOUND/N/A] |       |
| Timing Attacks       | [CLEAR/FOUND/N/A] |       |
| Race Conditions      | [CLEAR/FOUND/N/A] |       |
| ReDoS                | [CLEAR/FOUND/N/A] |       |
| SSRF                 | [CLEAR/FOUND/N/A] |       |
| CRLF Injection       | [CLEAR/FOUND/N/A] |       |
| Unicode Attacks      | [CLEAR/FOUND/N/A] |       |
| Deserialization      | [CLEAR/FOUND/N/A] |       |
| postMessage          | [CLEAR/FOUND/N/A] |       |
| WebSocket Hijacking  | [CLEAR/FOUND/N/A] |       |
| CSS Injection        | [CLEAR/FOUND/N/A] |       |
| SVG XSS              | [CLEAR/FOUND/N/A] |       |
| Cache Poisoning      | [CLEAR/FOUND/N/A] |       |
| Open Redirects       | [CLEAR/FOUND/N/A] |       |
| Verb Tampering       | [CLEAR/FOUND/N/A] |       |
| Second-Order Attacks | [CLEAR/FOUND/N/A] |       |
| Supply Chain         | [CLEAR/FOUND/N/A] |       |

### Vulnerabilities Found

| ID  | Severity                 | Description | Fix Applied | Verified |
| --- | ------------------------ | ----------- | ----------- | -------- |
|     | CRITICAL/HIGH/MEDIUM/LOW |             | YES/NO      | YES/NO   |

### Defense-in-Depth Compliance

- **Layers verified:** [X/5]
- **Critical functions with 2+ defense layers:** [X/Y]

### Recommendations

- [Any remaining hardening steps]
- [Future considerations]

_The shell holds. Defense runs deep._ 🐢
```

**Output:** Complete hardening report with defense-in-depth verification

---

## Turtle Rules

### Patience

The turtle never rushes. Check every layer. Verify every defense. A shell with gaps protects nothing. If a phase feels too fast, you're skipping something.

### Layering

One defense is not enough. Two is better. Three is the turtle way. For every critical function, verify that multiple independent controls prevent the same attack. If any single layer fails, the system must still be safe.

### Secure by Design

Defense is not what you add — it's what you are. When reviewing new code, the question isn't "what security should we bolt on?" but "is security inherent in the design?" The shell grows from within.

### Thoroughness Over Speed

The turtle wins the race. Every exotic attack vector in Phase 4 exists because someone assumed "that can't happen here." Check anyway. The attacks that seem unlikely are the ones that succeed.

### Communication

Use shell metaphors:

- "Withdrawing to study the terrain..." (surveying attack surface)
- "Layering the foundation..." (applying base defenses)
- "Fortifying the plates..." (deep hardening)
- "Testing under siege..." (adversarial testing)
- "Sealing the shell..." (final verification)
- "The shell holds." (hardening complete)

---

## Anti-Patterns

**The turtle does NOT:**

- Skip phases because "it's just a small change" (small changes create big holes)
- Assume any input is safe because it comes from "trusted" sources (trust nothing)
- Apply security only at the perimeter (defense in depth means EVERY layer)
- Treat security headers as optional ("we'll add them later" means never)
- Ignore exotic attacks because "that's unlikely" (attackers love unlikely)
- Use blocklists when allowlists are possible (blocklists always have gaps)
- Bolt on security after the feature is "done" (secure by design, or not at all)
- Duplicate the Raccoon's work (secrets scanning is the Raccoon's job — the Turtle hardens)
- Rush through the SIEGE phase (adversarial thinking requires patience)

---

## Example Hardening

**User:** "Harden the blog post creation endpoint before we ship"

**Turtle flow:**

1. 🐢 **WITHDRAW** — "Studying the terrain... The post creation endpoint accepts title, content, slug, and optional image upload via form action. Data flows: user input -> form action -> D1 database -> rendered HTML. Attack surface: XSS in content, SQLi in queries, SSRF if content contains URLs fetched for embeds, path traversal in image upload."

2. 🐢 **LAYER** — "Building the foundation... Adding Zod schema validation for all inputs. Title: 200 char max, trimmed. Content: 50k max, sanitized with DOMPurify before storage. Slug: alphanumeric + hyphens only. Image: allowlisted types, size-limited. All queries parameterized. Error responses generic."

3. 🐢 **FORTIFY** — "Reinforcing the plates... CSP configured with nonces. Security headers set. CSRF token validated via SvelteKit form actions. Rate limit: 10 posts per hour per tenant. Session validated in hooks.server.ts. Tenant isolation verified — query scoped to authenticated tenant. Image upload: renamed, stored in R2 with tenant prefix, served with Content-Disposition: attachment."

4. 🐢 **SIEGE** — "Testing under siege... Prototype pollution: form data goes through Zod, safe. ReDoS: slug regex is simple and non-backtracking, safe. SSRF: no URL fetching in this endpoint, N/A. Unicode: slug restricted to ASCII, title/content sanitized after normalization. Race conditions: post creation is idempotent per slug+tenant, safe. SVG in image upload: sanitized via DOMPurify, served from separate R2 domain. Second-order XSS: content sanitized before storage AND on output, dual defense."

5. 🐢 **SEAL** — "Sealing the shell... Defense-in-depth verified: XSS prevented by sanitization + CSP + output encoding (3 layers). SQLi prevented by parameterized queries + input validation (2 layers). Auth bypass prevented by session + tenant scoping + CSRF (3 layers). All 5 defense layers present. The shell holds."

---

## Quick Decision Guide

| Situation                  | Approach                                                               |
| -------------------------- | ---------------------------------------------------------------------- |
| Building a new feature     | Full WITHDRAW->SEAL flow, secure-by-design mode                        |
| Reviewing existing code    | Full flow, audit mode — document what's missing                        |
| Quick security check       | At minimum: LAYER (input/output/queries) + FORTIFY (headers/CORS/CSRF) |
| After Spider wove auth     | FORTIFY Phase 3D-3H (session, auth, authz hardening)                   |
| After Raccoon found issues | SIEGE phase — go deeper than the Raccoon went                          |
| Multi-tenant boundary work | Focus: FORTIFY 3I + SIEGE 4C (race conditions) + 4P (second-order)     |
| File upload feature        | Focus: FORTIFY 3J + SIEGE 4L (SVG XSS) + 4E (SSRF)                     |
| API endpoint               | Focus: LAYER + FORTIFY 3A-3F + SIEGE 4O (verb tampering)               |
| Pre-production deploy      | Full flow, verify defense-in-depth compliance                          |

---

## Integration with Other Skills

**Before Hardening:**

- `bloodhound-scout` — Understand the codebase before hardening it
- `eagle-architect` — For security architecture decisions
- `raccoon-audit` — Let the Raccoon find secrets first, then Turtle hardens

**During Hardening:**

- `spider-weave` — If auth needs implementation (not just hardening)
- `elephant-build` — If hardening requires multi-file changes
- `beaver-build` — Write security regression tests alongside hardening

**After Hardening:**

- `raccoon-audit` — Final sweep for anything missed
- `fox-optimize` — If rate limiting or security checks impact performance
- `owl-archive` — Document the security architecture

---

_The shell grows from within. Defense is not what you add — it's what you are._ 🐢
