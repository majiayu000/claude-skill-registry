---
version: 1.2.0
name: dev-security-frontend
description: >
  Security checklist for Angular/TypeScript frontend. Covers XSS prevention,
  client-side validation, secure authentication patterns, CSRF handling,
  content security policy, and sensitive data in bundles.
  Invoked via /dev-security (unified entry point) — not directly.
disable-model-invocation: true
user-invocable: false
context: fork
argument-hint: "[--checklist | --scan | --full]"
---

# Security Review — Frontend (Angular)

Security checklist for Angular/TypeScript frontend code.

> **Reference:** [OWASP Top 10:2025](https://owasp.org/Top10/2025/)

## Angular Version Notes

This checklist targets **Angular 21+ with zoneless change detection** (no zone.js). All components
are **standalone** (no NgModules). Guards and interceptors use **functional** patterns.

Zoneless mode (`provideExperimentalZonelessChangeDetection()`) does not change the security model,
but be aware that async operations (timers, fetch, WebSocket) no longer automatically trigger
change detection. If you manually schedule work outside Angular's awareness, ensure sensitive
state is still cleaned up properly — Angular won't "accidentally" flush it via a zone turn.

## When to Activate

- Handling user input or form submissions
- Implementing authentication flows (login, token storage)
- Rendering user-generated content
- Before deploying to production
- Adding third-party scripts or integrations

## 1. No Secrets in Bundles

Angular bundles are public — everything in them is visible to users.

```typescript
// environment.ts — URLs are OK, secrets are NOT
export const environment = {
  apiUrl: 'https://api.example.com',  // OK — just a URL
  // apiKey: 'sk-xxx'                 // NEVER — visible in bundle
};
```

**Checklist:**
- [ ] No API keys, tokens, or passwords in `environment.ts` or any `.ts` file
- [ ] No secrets in `angular.json` or build configurations
- [ ] Production source maps disabled (`"sourceMap": false`)
- [ ] No secrets in git history (`git log -p -S "apikey"`)

## 2. XSS Prevention

Angular sanitizes by default. Watch for bypasses:

```typescript
// Angular sanitizes automatically in templates
// {{ userInput }} is safe — Angular escapes it

// DANGEROUS — bypasses sanitization
this.domSanitizer.bypassSecurityTrustHtml(userInput); // Only if you MUST render HTML

// If you must render user HTML, sanitize server-side first
```

### innerHTML vs interpolation
```typescript
// SAFE — Angular escapes
<p>{{ userInput }}</p>

// RISKY — Angular sanitizes but be careful
<div [innerHTML]="userInput"></div>

// DANGEROUS — bypasses all protection
<div [innerHTML]="sanitizer.bypassSecurityTrustHtml(userInput)"></div>
```

**Checklist:**
- [ ] Never use `bypassSecurityTrust*` with user input
- [ ] Prefer `{{ interpolation }}` over `[innerHTML]`
- [ ] If `[innerHTML]` is needed, sanitize server-side first
- [ ] No `eval()`, `new Function()`, or dynamic script injection

## 3. Client-Side Validation

Client-side validation is for UX, not security. The server must always re-validate.

### Template-Driven Forms with ngModel

```typescript
@Component({
  standalone: true,
  imports: [FormsModule],
  template: `
    <form #orderForm="ngForm" (ngSubmit)="onSubmit()">
      <input
        type="email"
        [(ngModel)]="email"
        name="email"
        required
        email
        maxlength="200"
        #emailField="ngModel"
      />
      @if (emailField.invalid && emailField.touched) {
        <span class="error">Valid email required</span>
      }

      <input
        type="number"
        [(ngModel)]="quantity"
        name="quantity"
        required
        min="1"
        max="1000"
        #qtyField="ngModel"
      />

      <button type="submit" [disabled]="orderForm.invalid">Submit</button>
    </form>
  `
})
export class OrderFormComponent {
  email = '';
  quantity = 1;

  onSubmit() {
    // Client validation passed — server will validate again
  }
}
```

**Security note on `[(ngModel)]`:** Two-way binding itself is not a vulnerability, but avoid
binding user input directly into `[innerHTML]`, URL parameters, or script contexts. Always
treat model values as untrusted when passing them beyond the template.

**Checklist:**
- [ ] Template-driven forms with appropriate validators on all inputs
- [ ] Max length on text inputs (prevent payload bloat)
- [ ] Number ranges validated (min/max)
- [ ] Form submission disabled when invalid
- [ ] Remember: this is UX only — server validates again

## 4. Authentication Patterns

For code examples (cookie sessions, OAuth2 PKCE, functional guards, HTTP interceptors), see [auth-patterns.md](auth-patterns.md).

**Checklist:**
- [ ] Session cookies use `__Host-` prefix (Secure, HttpOnly, SameSite=Strict)
- [ ] OAuth2 flows use PKCE with S256 challenge method
- [ ] `code_verifier` in memory or `sessionStorage` only (not `localStorage`)
- [ ] Tokens stay server-side — client receives session cookie only
- [ ] Functional route guards (`CanActivateFn`) on all protected pages
- [ ] Functional HTTP interceptor handles 401 redirect and 429 rate limiting
- [ ] Clear auth state on logout (including in-memory signal state)

## 5. CSRF Protection

Angular's `HttpClient` handles CSRF automatically when cookies are configured:

```typescript
// Angular reads XSRF-TOKEN cookie and sends X-XSRF-TOKEN header automatically
// Server must set the XSRF-TOKEN cookie and validate the header

// If you need custom configuration:
provideHttpClient(
  withXsrfConfiguration({
    cookieName: 'XSRF-TOKEN',
    headerName: 'X-XSRF-TOKEN'
  })
)
```

**Checklist:**
- [ ] XSRF cookie/header configured
- [ ] Server validates anti-forgery tokens
- [ ] SameSite=Strict on auth cookies (server-side)

## 6. Content Security Policy

CSP headers are set server-side but affect the frontend:

```
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'
```

**Frontend implications:**
- [ ] No inline `<script>` tags (use Angular components)
- [ ] No `eval()` or `new Function()`
- [ ] External scripts loaded only from whitelisted domains
- [ ] Fonts and images from trusted CDNs only

## 7. Signal-Based State Security

Angular signals replace many RxJS patterns for state management. They avoid subscription leak
risks but introduce their own considerations:

```typescript
@Component({
  standalone: true,
  template: `
    <!-- SAFE — display name is not sensitive -->
    <p>Welcome, {{ displayName() }}</p>

    <!-- DANGEROUS — never expose tokens or secrets in templates -->
    <!-- <p>Token: {{ authToken() }}</p> -->
  `
})
export class DashboardComponent {
  private readonly authService = inject(AuthService);

  // OK — non-sensitive derived state
  displayName = computed(() => this.authService.user()?.name ?? 'Guest');

  // WRONG — sensitive data in a signal that could appear in templates or DevTools
  // authToken = computed(() => this.authService.session()?.token);

  // If you need sensitive data, keep it in a private method, not a signal
  private getToken(): string | null {
    return this.authService.session()?.token ?? null;
  }
}
```

**Checklist:**
- [ ] Signals exposed in templates contain no sensitive data (tokens, PII, secrets)
- [ ] `computed()` values that derive from auth state only expose safe projections
- [ ] Sensitive data accessed via private methods, not public signals
- [ ] Angular DevTools can inspect signals — assume they are visible

## 8. Dependency Security

```bash
# Check for vulnerable packages
npm audit

# Auto-fix safe updates
npm audit fix

# Check what's outdated
npm outdated
```

**Checklist:**
- [ ] `npm audit` clean (or only low-severity dev dependencies)
- [ ] No `console.log` or `debugger` in production code
- [ ] Third-party packages from trusted sources
- [ ] Lock file (`package-lock.json`) committed

## 9. Sensitive Data in the Client

```typescript
@Component({
  standalone: true,
  template: `
    @if (error) {
      <p class="error">{{ error }}</p>
    }
  `
})
export class LoginComponent {
  private readonly authService = inject(AuthService);
  error = '';

  onLoginFailed(response: HttpErrorResponse) {
    // WRONG — exposing server details
    // this.error = `Failed to authenticate: ${response.error.details}`;

    // CORRECT — generic error
    this.error = 'Authentication failed. Please try again.';
  }
}
```

**Checklist:**
- [ ] No sensitive data in console.log statements
- [ ] Error messages generic for users
- [ ] No PII stored in localStorage/sessionStorage
- [ ] Browser dev tools don't reveal sensitive state

## 10. Service Worker Security

Angular Service Worker caches assets for offline use. Misconfigured caching can leak sensitive data or serve stale auth state. For `ngsw-config.json` data group examples, see [auth-patterns.md](auth-patterns.md#service-worker--ngsw-configjson-data-groups).

**Checklist:**
- [ ] Auth endpoints use `freshness` strategy with short/zero maxAge
- [ ] No sensitive data (PII, tokens) in cached data groups
- [ ] `ngsw-config.json` reviewed — no accidental wildcard caching of API responses
- [ ] Service Worker update strategy tested — stale versions don't serve outdated auth
- [ ] SW cache cleared on logout (call `SwUpdate` or `registration.unregister()` if needed)

## 11. Supply Chain Security (OWASP A03:2025)

npm supply chain attacks target packages, build scripts, and transitive dependencies.

**Checklist:**
- [ ] `npm audit` clean (or only low-severity dev dependencies)
- [ ] Lock file (`package-lock.json`) committed — never deleted or regenerated without review
- [ ] No `postinstall` scripts in dependencies that download external code
- [ ] Third-party packages from trusted sources with active maintenance
- [ ] No wildcard (`*`) or overly broad version ranges in `package.json`
- [ ] Review `npm ls` for unexpected transitive dependencies
- [ ] Subresource Integrity (SRI) on any CDN-loaded scripts

## 12. Exceptional Condition Handling (OWASP A10:2025)

Unhandled errors in the frontend can freeze the UI, leak state, or expose debug info.

**Checklist:**
- [ ] Global error handler (`ErrorHandler`) catches unhandled exceptions
- [ ] HTTP errors handled in interceptor — 401 redirects, 429 rate-limit UX, 5xx retry/fallback
- [ ] Observable chains have `catchError` — no unhandled observable errors
- [ ] Signal-based async operations handle error states (not just loading/success)
- [ ] Network failures show user-friendly messages (not raw errors)
- [ ] No `console.error` stack traces visible in production

## Pre-Deployment Checklist

### OWASP Top 10:2025 Coverage
- [ ] **A01 Broken Access Control**: Route guards on all protected pages, role-based guards
- [ ] **A02 Security Misconfiguration**: Source maps disabled, CSP headers, no debug in prod
- [ ] **A03 Supply Chain**: `npm audit` clean, lock file committed, SRI on CDN scripts
- [ ] **A04 Cryptographic Failures**: No secrets in bundles, tokens server-side only
- [ ] **A05 Injection**: No `bypassSecurityTrust*` with user input, no `eval()`, no `innerHTML` with user data
- [ ] **A06 Insecure Design**: Forms validated, error states handled gracefully
- [ ] **A07 Authentication Failures**: `__Host-` cookies, OAuth2+PKCE, functional guards + interceptors
- [ ] **A08 Integrity Failures**: XSRF tokens configured, Service Worker update strategy
- [ ] **A09 Logging & Alerting**: No sensitive data in console, structured error reporting
- [ ] **A10 Exceptional Conditions**: Global error handler, HTTP interceptor, Observable error handling

### Stack-Specific
- [ ] **Signals**: No sensitive data in public signals or `computed()` values
- [ ] **Service Worker**: Auth endpoints not cached, SW config reviewed
- [ ] **Build**: Production build with AOT compilation

## Flags

| Flag | Behavior |
|------|----------|
| `--checklist` | Print the pre-deployment checklist only |
| `--scan` | Run automated scans (`npm audit`, console.log grep, secret grep, Aspire runtime errors) |
| `--full` | Full review: checklist + scans + runtime checks + code review of changed files |

## Aspire Runtime Security Checks (--scan / --full)

If the Aspire AppHost is running, the `--scan` and `--full` flags include runtime security checks:

**Step 1 — Check for runtime console errors:**
```
mcp__aspire__list_console_logs  resourceName: "site"
```
Look for:
- `console.error` or `console.warn` output that leaks internal state
- Angular error messages that expose component internals or stack traces
- Failed network requests visible in console (CORS, auth, 500s)

**Step 2 — Check API logs for frontend-triggered security issues:**
```
mcp__aspire__list_structured_logs  resourceName: "api"
```
Filter for errors from frontend requests:
- `401`/`403` responses that indicate auth misconfiguration
- CORS rejections from the frontend origin
- Missing CSRF tokens on state-changing requests

Skip if Aspire is not running.
