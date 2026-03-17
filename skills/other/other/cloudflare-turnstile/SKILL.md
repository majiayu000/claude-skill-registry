---
name: cloudflare-turnstile
description: |
  Add bot protection with Turnstile (CAPTCHA alternative). Use when: protecting forms, securing login/signup, preventing spam, migrating from reCAPTCHA, integrating with React/Next.js/Hono, implementing E2E tests, or debugging CSP errors, token validation failures, Chrome/Edge first-load issues, multiple widget rendering bugs, timeout-or-duplicate errors, or error codes 100*/106010/300*/600*.
user-invocable: true
---

# Cloudflare Turnstile

**Status**: Production Ready ✅
**Last Updated**: 2026-01-21
**Dependencies**: None (optional: @marsidev/react-turnstile for React)
**Latest Versions**: @marsidev/react-turnstile@1.4.1, turnstile-types@1.2.3

**Recent Updates (2025)**:
- **December 2025**: @marsidev/react-turnstile v1.4.1 fixes race condition in script loading
- **August 2025**: v1.3.0 adds `rerenderOnCallbackChange` prop for React closure issues
- **March 2025**: Upgraded Turnstile Analytics with TopN statistics (7 dimensions: hostnames, browsers, countries, user agents, ASNs, OS, source IPs), anomaly detection, enhanced bot behavior monitoring
- **January 2025**: Brief remoteip validation enforcement (resolved, but highlights importance of correct IP passing)
- **2025**: WCAG 2.1 AA compliance, Free plan (20 widgets, 7-day analytics), Enterprise features (unlimited widgets, ephemeral IDs, any hostname support, 30-day analytics, offlabel branding)

---

## Quick Start (5 Minutes)

```bash
# 1. Create widget: https://dash.cloudflare.com/?to=/:account/turnstile
#    Copy sitekey (public) and secret key (private)

# 2. Add widget to frontend
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
<form>
  <div class="cf-turnstile" data-sitekey="YOUR_SITE_KEY"></div>
  <button type="submit">Submit</button>
</form>

# 3. Validate token server-side (Cloudflare Workers)
const formData = await request.formData()
const token = formData.get('cf-turnstile-response')

const verifyFormData = new FormData()
verifyFormData.append('secret', env.TURNSTILE_SECRET_KEY)
verifyFormData.append('response', token)
verifyFormData.append('remoteip', request.headers.get('CF-Connecting-IP'))  // REQUIRED - see Critical Rules

const result = await fetch(
  'https://challenges.cloudflare.com/turnstile/v0/siteverify',
  { method: 'POST', body: verifyFormData }
)

const outcome = await result.json()
if (!outcome.success) return new Response('Invalid', { status: 401 })
```

**CRITICAL:**
- Token expires in 5 minutes, single-use only
- ALWAYS validate server-side (Siteverify API required)
- Never proxy/cache api.js (must load from Cloudflare CDN)
- Use different widgets for dev/staging/production

## Rendering Modes

**Implicit** (auto-render on page load):
```html
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
<div class="cf-turnstile" data-sitekey="YOUR_SITE_KEY" data-callback="onSuccess"></div>
```

**Explicit** (programmatic control for SPAs):
```typescript
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit"></script>
const widgetId = turnstile.render('#container', { sitekey: 'YOUR_SITE_KEY' })
turnstile.reset(widgetId)   // Reset widget
turnstile.getResponse(widgetId)  // Get token
```

**React** (using @marsidev/react-turnstile):
```tsx
import { Turnstile } from '@marsidev/react-turnstile'
<Turnstile siteKey={TURNSTILE_SITE_KEY} onSuccess={setToken} />
```

---

## Critical Rules

### Always Do

✅ **Call Siteverify API** - Server-side validation is mandatory
✅ **Use HTTPS** - Never validate over HTTP
✅ **Protect secret keys** - Never expose in frontend code
✅ **Handle token expiration** - Tokens expire after 5 minutes
✅ **Implement error callbacks** - Handle failures gracefully
✅ **Use dummy keys for testing** - Test sitekey: `1x00000000000000000000AA`
✅ **Set reasonable timeouts** - Don't wait indefinitely for validation
✅ **Validate action/hostname** - Check additional fields when specified
✅ **Rotate keys periodically** - Use dashboard or API to rotate secrets
✅ **Monitor analytics** - Track solve rates and failures
✅ **Always pass client IP to Siteverify** - Use `CF-Connecting-IP` header (Workers) or `X-Forwarded-For` (Node.js). Cloudflare briefly enforced strict remoteip validation in Jan 2025, causing widespread failures for sites not passing correct IP

### Never Do

❌ **Skip server validation** - Client-side only = security vulnerability
❌ **Proxy api.js script** - Must load from Cloudflare CDN
❌ **Reuse tokens** - Each token is single-use only
❌ **Use GET requests** - Siteverify only accepts POST
❌ **Expose secret key** - Keep secrets in backend environment only
❌ **Trust client-side validation** - Tokens can be forged
❌ **Cache api.js** - Future updates will break your integration
❌ **Use production keys in tests** - Use dummy keys instead
❌ **Ignore error callbacks** - Always handle failures

---

## Known Issues Prevention

This skill prevents **15** documented issues:

### Issue #1: Missing Server-Side Validation
**Error**: Zero token validation in Turnstile Analytics dashboard
**Source**: https://developers.cloudflare.com/turnstile/get-started/
**Why It Happens**: Developers only implement client-side widget, skip Siteverify call
**Prevention**: All templates include mandatory server-side validation with Siteverify API

### Issue #2: Token Expiration (5 Minutes)
**Error**: `success: false` for valid tokens submitted after delay
**Source**: https://developers.cloudflare.com/turnstile/get-started/server-side-validation
**Why It Happens**: Tokens expire 300 seconds after generation
**Prevention**: Templates document TTL and implement token refresh on expiration

### Issue #3: Secret Key Exposed in Frontend
**Error**: Security bypass - attackers can validate their own tokens
**Source**: https://developers.cloudflare.com/turnstile/get-started/server-side-validation
**Why It Happens**: Secret key hardcoded in JavaScript or visible in source
**Prevention**: All templates show backend-only validation with environment variables

### Issue #4: GET Request to Siteverify
**Error**: API returns 405 Method Not Allowed
**Source**: https://developers.cloudflare.com/turnstile/migration/recaptcha
**Why It Happens**: reCAPTCHA supports GET, Turnstile requires POST
**Prevention**: Templates use POST with FormData or JSON body

### Issue #5: Content Security Policy Blocking
**Error**: Error 200500 - "Loading error: The iframe could not be loaded"
**Source**: https://developers.cloudflare.com/turnstile/troubleshooting/client-side-errors/error-codes
**Why It Happens**: CSP blocks challenges.cloudflare.com iframe
**Prevention**: Skill includes CSP configuration reference and check-csp.sh script

### Issue #6: Widget Crash (Error 300030)
**Error**: Generic client execution error for legitimate users
**Source**: https://community.cloudflare.com/t/turnstile-is-frequently-generating-300x-errors/700903
**Why It Happens**: Unknown - appears to be Cloudflare-side issue (2025)
**Prevention**: Templates implement error callbacks, retry logic, and fallback handling

### Issue #7: Configuration Error (Error 600010)
**Error**: Widget fails with "configuration error"
**Source**: https://community.cloudflare.com/t/repeated-cloudflare-turnstile-error-600010/644578
**Why It Happens**: Missing or deleted hostname in widget configuration
**Prevention**: Templates document hostname allowlist requirement and verification steps

### Issue #8: Safari 18 / macOS 15 "Hide IP" Issue
**Error**: Error 300010 when Safari's "Hide IP address" is enabled
**Source**: https://community.cloudflare.com/t/turnstile-is-frequently-generating-300x-errors/700903
**Why It Happens**: Privacy settings interfere with challenge signals
**Prevention**: Error handling reference documents Safari workaround (disable Hide IP)

### Issue #9: Brave Browser Confetti Animation Failure
**Error**: Verification fails during success animation
**Source**: https://github.com/brave/brave-browser/issues/45608 (April 2025)
**Why It Happens**: Brave shields block animation scripts
**Prevention**: Templates handle success before animation completes

### Issue #10: Next.js + Jest Incompatibility
**Error**: @marsidev/react-turnstile breaks Jest tests
**Source**: https://github.com/marsidev/react-turnstile/issues/112 (Oct 2025)
**Why It Happens**: Module resolution issues with Jest
**Prevention**: Testing guide includes Jest mocking patterns and dummy sitekey usage

### Issue #11: localhost Not in Allowlist
**Error**: Error 110200 - "Unknown domain: Domain not allowed"
**Source**: https://developers.cloudflare.com/turnstile/troubleshooting/client-side-errors/error-codes
**Why It Happens**: Production widget used in development without localhost in allowlist
**Prevention**: Templates use dummy test keys for dev, document localhost allowlist requirement

### Issue #12: Token Reuse Attempt
**Error**: `success: false` with "token already spent" error
**Source**: https://developers.cloudflare.com/turnstile/troubleshooting/testing
**Why It Happens**: Each token can only be validated once. Turnstile tokens are single-use - after validation (success OR failure), the token is consumed and cannot be revalidated. Developers must explicitly call `turnstile.reset()` to generate a new token for subsequent submissions.
**Prevention**: Templates document single-use constraint and token refresh patterns

```typescript
// CRITICAL: Reset widget after validation to get new token
const turnstileRef = useRef(null)

async function handleSubmit(e) {
  e.preventDefault()
  const token = formData.get('cf-turnstile-response')

  const result = await fetch('/api/submit', {
    method: 'POST',
    body: JSON.stringify({ token })
  })

  // Reset widget regardless of success/failure
  // Token is consumed either way
  if (turnstileRef.current) {
    turnstile.reset(turnstileRef.current)
  }
}

<Turnstile
  ref={turnstileRef}
  siteKey={TURNSTILE_SITE_KEY}
  onSuccess={setToken}
/>
```

### Issue #13: Error 106010 - Chrome/Edge First-Load Failure
**Error**: `106010` - "Generic parameter error" on first widget load in Chrome/Edge browsers
**Source**: [Cloudflare Error Codes](https://developers.cloudflare.com/turnstile/troubleshooting/client-side-errors/error-codes/), [Community Report](https://community.cloudflare.com/t/turnstile-inconsistent-errors/856678)
**Why It Happens**: Unknown browser-specific issue affecting Chrome and Edge on first page load. Console shows 400 error to `https://challenges.cloudflare.com/cdn-cgi/challenge-platform`. Firefox is not affected. Subsequent page reloads work correctly.
**Prevention**: Implement error callback with auto-retry logic

```typescript
turnstile.render('#container', {
  sitekey: SITE_KEY,
  retry: 'auto',
  'retry-interval': 8000,
  'error-callback': (errorCode) => {
    if (errorCode === '106010') {
      console.warn('Chrome/Edge first-load issue (106010), auto-retrying...')
      // Auto-retry will handle it
    }
  }
})
```

**Workaround**: Widget works correctly after page reload. Auto-retry setting resolves in most cases. Test in Incognito mode to rule out browser extensions. Review CSP rules to ensure Cloudflare Turnstile endpoints are allowed.

### Issue #14: Multiple Widgets Visual Status Stuck (Community-sourced)
**Error**: Widget displays "Pending..." status even after successful token generation
**Source**: [GitHub Issue #119](https://github.com/marsidev/react-turnstile/issues/119)
**Why It Happens**: CSS repaint issue when rendering multiple `<Turnstile/>` components on a single page. Only reproducible on full HD desktop screens. Token IS successfully generated (validation works), but visual status doesn't update. Hovering over widget triggers repaint and shows correct status.
**Prevention**: Force CSS repaint in success callback

```tsx
<Turnstile
  siteKey={KEY}
  onSuccess={(token) => {
    setToken(token)
    // Force repaint by toggling display
    const widget = document.querySelector('.cf-turnstile')
    if (widget) {
      widget.style.display = 'none'
      setTimeout(() => widget.style.display = 'block', 0)
    }
  }}
/>
```

**Note**: This is a visual-only issue, not a validation failure. The token is correctly generated and functional.

### Issue #15: Jest Compatibility with @marsidev/react-turnstile (Updated Dec 2025)
**Error**: `Jest encountered an unexpected token` when importing @marsidev/react-turnstile
**Source**: [GitHub Issue #114](https://github.com/marsidev/react-turnstile/issues/114), [GitHub Issue #112](https://github.com/marsidev/react-turnstile/issues/112)
**Why It Happens**: ESM module resolution issues with Jest 30.2.0 (latest as of Dec 2025). Issue #112 closed as "not planned" by maintainer. Jest users are stuck; Vitest migration works.
**Prevention**: Mock the Turnstile component in Jest setup OR migrate to Vitest

```typescript
// Option 1: Jest mocking (jest.setup.ts)
jest.mock('@marsidev/react-turnstile', () => ({
  Turnstile: () => <div data-testid="turnstile-mock" />,
}))

// Option 2: transformIgnorePatterns in jest.config.js
module.exports = {
  transformIgnorePatterns: [
    'node_modules/(?!(@marsidev/react-turnstile)/)'
  ]
}

// Option 3 (Recommended): Migrate to Vitest
// Vitest handles ESM modules correctly without mocking
```

**Status**: Maintainer closed issue as "not planned". Recommend migrating to Vitest for new projects.

## Configuration

**wrangler.jsonc:**
```jsonc
{
  "vars": { "TURNSTILE_SITE_KEY": "1x00000000000000000000AA" },
  "secrets": ["TURNSTILE_SECRET_KEY"]  // Run: wrangler secret put TURNSTILE_SECRET_KEY
}
```

**Required CSP:**
```html
<meta http-equiv="Content-Security-Policy" content="
  script-src 'self' https://challenges.cloudflare.com;
  frame-src 'self' https://challenges.cloudflare.com;
">
```

---

## Common Patterns

### Pattern 1: Hono + Cloudflare Workers

```typescript
import { Hono } from 'hono'

type Bindings = {
  TURNSTILE_SECRET_KEY: string
  TURNSTILE_SITE_KEY: string
}

const app = new Hono<{ Bindings: Bindings }>()

app.post('/api/login', async (c) => {
  const body = await c.req.formData()
  const token = body.get('cf-turnstile-response')

  if (!token) {
    return c.text('Missing Turnstile token', 400)
  }

  // Validate token
  const verifyFormData = new FormData()
  verifyFormData.append('secret', c.env.TURNSTILE_SECRET_KEY)
  verifyFormData.append('response', token.toString())
  verifyFormData.append('remoteip', c.req.header('CF-Connecting-IP') || '')  // CRITICAL - always pass client IP

  const verifyResult = await fetch(
    'https://challenges.cloudflare.com/turnstile/v0/siteverify',
    {
      method: 'POST',
      body: verifyFormData,
    }
  )

  const outcome = await verifyResult.json<{ success: boolean }>()

  if (!outcome.success) {
    return c.text('Invalid Turnstile token', 401)
  }

  // Process login
  return c.json({ message: 'Login successful' })
})

export default app
```

**When to use**: API routes in Cloudflare Workers with Hono framework

### Pattern 2: React + Next.js App Router

```tsx
'use client'

import { Turnstile } from '@marsidev/react-turnstile'
import { useState } from 'react'

export function ContactForm() {
  const [token, setToken] = useState<string>()
  const [error, setError] = useState<string>()

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()

    if (!token) {
      setError('Please complete the challenge')
      return
    }

    const formData = new FormData(e.currentTarget)
    formData.append('cf-turnstile-response', token)

    const response = await fetch('/api/contact', {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      setError('Submission failed')
      return
    }

    // Success
  }

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" type="email" required />
      <textarea name="message" required />

      <Turnstile
        siteKey={process.env.NEXT_PUBLIC_TURNSTILE_SITE_KEY!}
        onSuccess={setToken}
        onError={() => setError('Challenge failed')}
        onExpire={() => setToken(undefined)}
      />

      {error && <div className="error">{error}</div>}

      <button type="submit" disabled={!token}>
        Submit
      </button>
    </form>
  )
}
```

**When to use**: Client-side forms in Next.js with React hooks

---

## Testing Keys

**Dummy Sitekeys (client):**
- Always pass: `1x00000000000000000000AA`
- Always block: `2x00000000000000000000AB`
- Force interactive: `3x00000000000000000000FF`

**Dummy Secret Keys (server):**
- Always pass: `1x0000000000000000000000000000000AA`
- Always fail: `2x0000000000000000000000000000000AA`
- Token already spent: `3x0000000000000000000000000000000AA`

---

## Bundled Resources

**Scripts:** `check-csp.sh` - Verify CSP allows Turnstile

**References:**
- `widget-configs.md` - All configuration options
- `error-codes.md` - Error code troubleshooting (100*/200*/300*/400*/600*)
- `testing-guide.md` - Testing strategies, dummy keys
- `react-integration.md` - React/Next.js patterns

**Templates:** Complete examples for Hono, React, implicit/explicit rendering, validation

---

## Advanced Features

**Pre-Clearance (SPAs):** Issue cookie that persists across page navigations
```typescript
turnstile.render('#container', {
  sitekey: SITE_KEY,
  callback: async (token) => {
    await fetch('/api/pre-clearance', { method: 'POST', body: JSON.stringify({ token }) })
  }
})
```

**Custom Actions & Data:** Track challenge types, pass custom data (max 255 chars)
```typescript
turnstile.render('#container', {
  action: 'login',  // Track in analytics
  cdata: JSON.stringify({ userId: '123' }),  // Custom payload
})
```

**Error Handling:** Use `retry: 'auto'` and `error-callback` for resilience
```typescript
turnstile.render('#container', {
  retry: 'auto',
  'retry-interval': 8000,  // ms between retries
  'error-callback': (error) => { /* handle or show fallback */ }
})
```

---

## Dependencies

**Required:** None (loads from CDN)
**React:** @marsidev/react-turnstile@1.4.1 (Cloudflare-recommended), turnstile-types@1.2.3
**Other:** vue-turnstile, ngx-turnstile, svelte-turnstile, @nuxtjs/turnstile

---

## Official Documentation

- https://developers.cloudflare.com/turnstile/
- Use `mcp__cloudflare-docs__search_cloudflare_documentation` tool

---

## Troubleshooting

### Problem: Error 110200 - "Unknown domain"
**Solution**: Add your domain (including localhost for dev) to widget's allowed domains in Cloudflare Dashboard. For local dev, use dummy test sitekey `1x00000000000000000000AA` instead.

### Problem: Error 300030 - Widget crashes for legitimate users
**Solution**: Implement error callback with retry logic. This is a known Cloudflare-side issue (2025). Fallback to alternative verification if retries fail.

### Problem: Tokens always return `success: false`
**Solution**:
1. Check token hasn't expired (5 min TTL)
2. Verify secret key is correct
3. Ensure token hasn't been validated before (single-use)
4. Check hostname matches widget configuration

### Problem: CSP blocking iframe (Error 200500)
**Solution**: Add CSP directives:
```html
<meta http-equiv="Content-Security-Policy" content="
  frame-src https://challenges.cloudflare.com;
  script-src https://challenges.cloudflare.com;
">
```

### Problem: Safari 18 "Hide IP" causing Error 300010
**Solution**: Document in error message that users should disable Safari's "Hide IP address" setting (Safari → Settings → Privacy → Hide IP address → Off)

### Problem: Next.js + Jest tests failing with @marsidev/react-turnstile
**Solution**: Mock the Turnstile component in Jest setup (or migrate to Vitest, which handles ESM modules correctly):
```typescript
// Option 1: Jest mocking (jest.setup.ts)
jest.mock('@marsidev/react-turnstile', () => ({
  Turnstile: () => <div data-testid="turnstile-mock" />,
}))

// Option 2: Migrate to Vitest (recommended for new projects)
// Vitest handles ESM modules without mocking required
```

**Note**: This issue persists in Jest 30.2.0 (Dec 2025). Maintainer closed as "not planned". See Issue #15 for full details.

---

**Errors Prevented**: 15 documented issues (Safari 18 Hide IP, Brave confetti, Next.js Jest, CSP blocking, token reuse, expiration, hostname allowlist, widget crash 300030, config error 600010, missing validation, GET request, secret exposure, Chrome/Edge 106010, multiple widgets rendering, token regeneration pattern)
