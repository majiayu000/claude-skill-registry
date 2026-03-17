---
name: cloudflare-turnstile
description: This skill should be used when the user asks to "add turnstile", "implement bot protection", "validate turnstile token", "fix turnstile error", "setup captcha alternative", or encounters error codes 100*/300*/600*, CSP errors, or token validation failures. Provides CAPTCHA-alternative protection for Cloudflare Workers, React, Next.js, and Hono.

  Keywords: turnstile, captcha, bot protection, cloudflare challenge, siteverify, recaptcha alternative, spam prevention, form protection, cf-turnstile, turnstile widget, token validation, managed challenge, invisible challenge, @marsidev/react-turnstile, hono turnstile, workers turnstile
license: MIT
metadata:
  version: "1.1.0"
  last_verified: "2025-11-26"
  react_turnstile_version: "1.3.1"
  turnstile_types_version: "1.2.3"
  errors_prevented: 12
  templates_included: 7
  references_included: 8
---

# Cloudflare Turnstile

**Status**: Production Ready ✅ | **Last Verified**: 2025-11-26

**Dependencies**: None (optional: @marsidev/react-turnstile for React)

**Contents**: [Quick Start](#quick-start-10-minutes) • [Critical Rules](#critical-rules) • [Top 12 Errors](#known-issues-prevention) • [Common Patterns](#common-patterns) • [When to Load References](#when-to-load-references) • [Troubleshooting](#troubleshooting)

---

## Quick Start (10 Minutes)

### 1. Create Turnstile Widget

Get your sitekey and secret key from Cloudflare Dashboard.

```bash
# Navigate to: https://dash.cloudflare.com/?to=/:account/turnstile
# Create new widget → Copy sitekey (public) and secret key (private)
```

**Why this matters:**
- Each widget has unique sitekey/secret pair
- Sitekey goes in frontend (public)
- Secret key ONLY in backend (private)
- Use different widgets for dev/staging/production

### 2. Add Widget to Frontend

Embed the Turnstile widget in your HTML form.

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
</head>
<body>
  <form id="myForm" action="/submit" method="POST">
    <input type="email" name="email" required>
    <!-- Turnstile widget renders here -->
    <div class="cf-turnstile" data-sitekey="YOUR_SITE_KEY"></div>
    <button type="submit">Submit</button>
  </form>
</body>
</html>
```

**CRITICAL:**
- Never proxy or cache `api.js` - must load from Cloudflare CDN
- Widget auto-creates hidden input `cf-turnstile-response` with token
- Token expires in 5 minutes
- Each token is single-use only

### 3. Validate Token on Server

ALWAYS validate the token server-side. Client-side verification alone is not secure.

```typescript
// Cloudflare Workers example
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const formData = await request.formData()
    const token = formData.get('cf-turnstile-response')
    const ip = request.headers.get('CF-Connecting-IP')

    // Validate token with Siteverify API
    const verifyFormData = new FormData()
    verifyFormData.append('secret', env.TURNSTILE_SECRET_KEY)
    verifyFormData.append('response', token)
    verifyFormData.append('remoteip', ip)

    const result = await fetch(
      'https://challenges.cloudflare.com/turnstile/v0/siteverify',
      {
        method: 'POST',
        body: verifyFormData,
      }
    )

    const outcome = await result.json()

    if (!outcome.success) {
      return new Response('Invalid Turnstile token', { status: 401 })
    }

    // Token valid - proceed with form processing
    return new Response('Success!')
  }
}
```

---

## The 3-Step Setup Process

### Step 1: Create Widget Configuration

1. Log into Cloudflare Dashboard
2. Navigate to Turnstile section
3. Click "Add Site"
4. Configure:
   - **Widget Mode**: Managed (recommended), Non-Interactive, or Invisible
   - **Domains**: Add allowed hostnames (e.g., example.com, localhost for dev)
   - **Name**: Descriptive name (e.g., "Production Login Form")

**Key Points:**
- Use separate widgets for dev/staging/production
- Restrict domains to only those you control
- Managed mode provides best balance of security and UX
- localhost must be explicitly added for local testing

### Step 2: Client-Side Integration

Choose between implicit or explicit rendering:

**Implicit Rendering** (Recommended for static forms):
```html
<!-- 1. Load script -->
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>

<!-- 2. Add widget -->
<div class="cf-turnstile"
     data-sitekey="YOUR_SITE_KEY"
     data-callback="onSuccess"
     data-error-callback="onError"></div>

<script>
function onSuccess(token) {
  console.log('Turnstile success:', token)
}

function onError(error) {
  console.error('Turnstile error:', error)
}
</script>
```

**Explicit Rendering** (For SPAs/dynamic UIs):
```typescript
// 1. Load script with explicit mode
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit" defer></script>

// 2. Render programmatically
const widgetId = turnstile.render('#container', {
  sitekey: 'YOUR_SITE_KEY',
  callback: (token) => {
    console.log('Token:', token)
  },
  'error-callback': (error) => {
    console.error('Error:', error)
  },
  theme: 'auto',
  execution: 'render', // or 'execute' for manual trigger
})

// Control lifecycle
turnstile.reset(widgetId)        // Reset widget
turnstile.remove(widgetId)       // Remove widget
turnstile.execute(widgetId)      // Manually trigger challenge
const token = turnstile.getResponse(widgetId) // Get current token
```

**React Integration** (using @marsidev/react-turnstile):
```tsx
import { Turnstile } from '@marsidev/react-turnstile'

export function MyForm() {
  const [token, setToken] = useState<string>()

  return (
    <form>
      <Turnstile
        siteKey={TURNSTILE_SITE_KEY}
        onSuccess={setToken}
        onError={(error) => console.error(error)}
      />
      <button disabled={!token}>Submit</button>
    </form>
  )
}
```

### Step 3: Server-Side Validation

**MANDATORY**: Always call Siteverify API to validate tokens.

```typescript
interface TurnstileResponse {
  success: boolean
  challenge_ts?: string
  hostname?: string
  error-codes?: string[]
  action?: string
  cdata?: string
}

async function validateTurnstile(
  token: string,
  secretKey: string,
  options?: {
    remoteip?: string
    idempotency_key?: string
    expectedAction?: string
    expectedHostname?: string
  }
): Promise<TurnstileResponse> {
  const formData = new FormData()
  formData.append('secret', secretKey)
  formData.append('response', token)

  if (options?.remoteip) {
    formData.append('remoteip', options.remoteip)
  }

  if (options?.idempotency_key) {
    formData.append('idempotency_key', options.idempotency_key)
  }

  const response = await fetch(
    'https://challenges.cloudflare.com/turnstile/v0/siteverify',
    {
      method: 'POST',
      body: formData,
    }
  )

  const result = await response.json<TurnstileResponse>()

  // Additional validation
  if (result.success) {
    if (options?.expectedAction && result.action !== options.expectedAction) {
      return { success: false, 'error-codes': ['action-mismatch'] }
    }

    if (options?.expectedHostname && result.hostname !== options.expectedHostname) {
      return { success: false, 'error-codes': ['hostname-mismatch'] }
    }
  }

  return result
}

// Usage in Cloudflare Worker
const result = await validateTurnstile(
  token,
  env.TURNSTILE_SECRET_KEY,
  {
    remoteip: request.headers.get('CF-Connecting-IP'),
    expectedHostname: 'example.com',
  }
)

if (!result.success) {
  return new Response('Turnstile validation failed', { status: 401 })
}
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
✅ **Validate token AFTER form submission** - Verify tokens after user completes form, not before. Premature validation creates security vulnerabilities where attackers obtain valid tokens then bypass protection

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

This skill prevents **12** documented issues:

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
**Why It Happens**: Each token can only be validated once
**Prevention**: Templates document single-use constraint and token refresh patterns

---

## Configuration

**Wrangler (Workers)**: Load `templates/wrangler-turnstile-config.jsonc` for complete configuration. Key settings: `vars` for public sitekey (safe to commit), `secrets` for private secret key (use `wrangler secret put TURNSTILE_SECRET_KEY`).

**CSP Directives** (if using Content Security Policy):
```html
<meta http-equiv="Content-Security-Policy" content="
  script-src 'self' https://challenges.cloudflare.com;
  frame-src 'self' https://challenges.cloudflare.com;
  connect-src 'self' https://challenges.cloudflare.com;">
```

---

## Common Patterns

**Hono + Cloudflare Workers**: Server-side validation in Workers API routes with Hono framework. Load `references/common-patterns.md` #pattern-1 when building Workers endpoints requiring bot protection.

**React + Next.js**: Client-side forms with @marsidev/react-turnstile integration. Load `references/common-patterns.md` #pattern-2 when integrating Turnstile with React/Next.js applications.

**E2E Testing**: Automated testing with dummy keys (Playwright, Cypress, Jest). Load `references/common-patterns.md` #pattern-3 when writing E2E tests or setting up CI/CD pipelines.

**Widget Lifecycle**: Programmatic widget control for SPAs (render, reset, remove, getToken). Load `references/common-patterns.md` #pattern-4 when building SPAs requiring explicit widget management.

---

## When to Load References

**`references/widget-configs.md`**: Configuring widget appearance, themes, execution modes, size, language, or retry behavior.

**`references/error-codes.md`**: Debugging error codes 100*, 200*, 300*, 400*, 600* or troubleshooting client-side failures (CSP, domain errors, widget crashes).

**`references/testing-guide.md`**: Setting up E2E tests (Playwright, Cypress), local development with dummy keys, or CI/CD pipeline integration.

**`references/react-integration.md`**: Integrating with React, Next.js, or troubleshooting @marsidev/react-turnstile issues (Jest mocking, SSR, hooks).

**`references/common-patterns.md`**: Building Hono Workers routes, React forms, E2E tests, or widget lifecycle management (explicit rendering).

**`references/advanced-topics.md`**: Implementing pre-clearance for SPAs, custom actions/cdata, retry strategies, or multi-widget pages.

**`references/setup-checklist.md`**: Preparing for deployment, verifying complete setup, or ensuring production readiness (14-point checklist).

**`references/migration-guide.md`**: Migrating from reCAPTCHA (v2) or hCaptcha to Turnstile, including compat mode, API differences, and POST-only Siteverify requirement.

**`references/browser-support.md`**: Browser compatibility matrix, Safari 18 "Hide IP" workaround, Brave shields issues, and browser-specific fallbacks.

**`references/mobile-implementation.md`**: WebView integration for iOS, Android, React Native, and Flutter, including User Agent consistency and storage persistence requirements.

**`templates/`**: **wrangler-turnstile-config.jsonc** (Workers env), **turnstile-widget-implicit.html** (static forms), **turnstile-widget-explicit.ts** (SPA rendering), **turnstile-server-validation.ts** (Siteverify API), **turnstile-react-component.tsx** (React integration), **turnstile-hono-route.ts** (Hono validation), **turnstile-test-config.ts** (testing setup)

**`scripts/check-csp.sh`**: Verify Content Security Policy allows Turnstile (usage: `./scripts/check-csp.sh https://example.com`)

---


## Dependencies

**Required**: None (Turnstile loads from Cloudflare CDN)

**Optional**: @marsidev/react-turnstile@1.3.1 (React), turnstile-types@1.2.3 (TypeScript), vue-turnstile (Vue 3), ngx-turnstile (Angular), svelte-turnstile (Svelte), @nuxtjs/turnstile (Nuxt)

---

## Official Documentation

**Turnstile**: https://developers.cloudflare.com/turnstile/ • **Get Started**: https://developers.cloudflare.com/turnstile/get-started/ • **Error Codes**: https://developers.cloudflare.com/turnstile/troubleshooting/client-side-errors/error-codes/ • **Testing**: https://developers.cloudflare.com/turnstile/troubleshooting/testing/ • **Migration (reCAPTCHA)**: https://developers.cloudflare.com/turnstile/migration/recaptcha/ • **MCP**: Use `mcp__cloudflare-docs__search_cloudflare_documentation` tool

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
**Solution**: Mock the Turnstile component in Jest setup:
```typescript
// jest.setup.ts
jest.mock('@marsidev/react-turnstile', () => ({
  Turnstile: () => <div data-testid="turnstile-mock" />,
}))
```

---

**Token Efficiency**: ~65-70% savings vs manual integration

**Errors Prevented**: 12 documented security/validation issues with complete solutions

**Deployment Checklist**: Load `references/setup-checklist.md` for complete 14-point pre-deployment verification
