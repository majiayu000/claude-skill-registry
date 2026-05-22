---
name: workers-security
description: Cloudflare Workers security with authentication, CORS, rate limiting, input validation. Use for securing APIs, JWT/API keys, or encountering auth failures, CORS errors, XSS/injection vulnerabilities.
---

# Cloudflare Workers Security

Comprehensive security patterns for protecting Workers and APIs.

## Quick Security Checklist

```typescript
// 1. Validate all input
const validated = schema.parse(await request.json());

// 2. Authenticate requests
const user = await verifyToken(request.headers.get('Authorization'));
if (!user) return new Response('Unauthorized', { status: 401 });

// 3. Rate limit
const limited = await rateLimiter.check(clientIP);
if (!limited.allowed) return new Response('Too Many Requests', { status: 429 });

// 4. Add security headers
response.headers.set('X-Content-Type-Options', 'nosniff');
response.headers.set('X-Frame-Options', 'DENY');

// 5. Use HTTPS-only cookies
headers.set('Set-Cookie', 'session=xxx; Secure; HttpOnly; SameSite=Strict');
```

## Critical Rules

1. **Never trust client input** - Validate and sanitize everything
2. **Use secure secrets** - Store in Wrangler secrets, never in code
3. **Implement rate limiting** - Protect against abuse
4. **Set security headers** - Prevent common attacks
5. **Use CORS properly** - Don't use `*` in production

## Top 10 Security Errors

| Vulnerability | Symptom | Prevention |
|---------------|---------|------------|
| Missing auth | Unauthorized access | Verify tokens on every request |
| SQL injection | Data breach | Use parameterized queries with D1 |
| XSS | Script injection | Sanitize output, set CSP |
| CORS misconfiguration | Blocked requests or open access | Configure specific origins |
| Secrets in code | Exposed credentials | Use `wrangler secret` |
| Missing rate limits | DoS vulnerability | Implement per-IP limits |
| Weak tokens | Session hijacking | Use crypto.subtle for signing |
| Missing HTTPS | Data interception | Enforce HTTPS redirects |
| Insecure headers | Clickjacking, MIME attacks | Set security headers |
| Excessive permissions | Blast radius | Principle of least privilege |

## Authentication Patterns

### JWT Verification

```typescript
async function verifyJWT(token: string, secret: string): Promise<{ valid: boolean; payload?: unknown }> {
  try {
    const [headerB64, payloadB64, signatureB64] = token.split('.');

    // Verify signature
    const key = await crypto.subtle.importKey(
      'raw',
      new TextEncoder().encode(secret),
      { name: 'HMAC', hash: 'SHA-256' },
      false,
      ['verify']
    );

    const signature = Uint8Array.from(atob(signatureB64.replace(/-/g, '+').replace(/_/g, '/')), c => c.charCodeAt(0));
    const data = new TextEncoder().encode(`${headerB64}.${payloadB64}`);

    const valid = await crypto.subtle.verify('HMAC', key, signature, data);
    if (!valid) return { valid: false };

    // Decode payload
    const payload = JSON.parse(atob(payloadB64.replace(/-/g, '+').replace(/_/g, '/')));

    // Check expiration
    if (payload.exp && Date.now() / 1000 > payload.exp) {
      return { valid: false };
    }

    return { valid: true, payload };
  } catch {
    return { valid: false };
  }
}
```

### API Key Validation

```typescript
async function validateApiKey(
  request: Request,
  env: Env
): Promise<{ valid: boolean; clientId?: string }> {
  const apiKey = request.headers.get('X-API-Key');
  if (!apiKey) return { valid: false };

  // Hash the key for lookup (never store plain keys)
  const keyHash = await sha256(apiKey);

  // Lookup in KV or D1
  const client = await env.KV.get(`apikey:${keyHash}`, 'json');
  if (!client) return { valid: false };

  return { valid: true, clientId: client.id };
}

async function sha256(str: string): Promise<string> {
  const buffer = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(str));
  return [...new Uint8Array(buffer)].map(b => b.toString(16).padStart(2, '0')).join('');
}
```

## Input Validation

### With Zod

```typescript
import { z } from 'zod';

const UserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().min(0).max(150).optional(),
});

async function handleCreate(request: Request): Promise<Response> {
  try {
    const body = await request.json();
    const user = UserSchema.parse(body);

    // Safe to use validated data
    return Response.json({ success: true, user });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return Response.json({ error: 'Validation failed', details: error.errors }, { status: 400 });
    }
    throw error;
  }
}
```

## Security Headers

```typescript
function addSecurityHeaders(response: Response): Response {
  const headers = new Headers(response.headers);

  // Prevent MIME type sniffing
  headers.set('X-Content-Type-Options', 'nosniff');

  // Prevent clickjacking
  headers.set('X-Frame-Options', 'DENY');

  // XSS protection
  headers.set('X-XSS-Protection', '1; mode=block');

  // Content Security Policy
  headers.set('Content-Security-Policy', "default-src 'self'; script-src 'self'");

  // HSTS
  headers.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');

  // Referrer policy
  headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');

  return new Response(response.body, { status: response.status, headers });
}
```

## CORS Configuration

```typescript
const ALLOWED_ORIGINS = ['https://app.example.com', 'https://admin.example.com'];

function handleCORS(request: Request, response: Response): Response {
  const origin = request.headers.get('Origin');

  if (!origin || !ALLOWED_ORIGINS.includes(origin)) {
    return response; // No CORS headers
  }

  const headers = new Headers(response.headers);
  headers.set('Access-Control-Allow-Origin', origin);
  headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  headers.set('Access-Control-Allow-Credentials', 'true');
  headers.set('Access-Control-Max-Age', '86400');

  return new Response(response.body, { status: response.status, headers });
}
```

## When to Load References

Load specific references based on the task:

- **Implementing authentication?** → Load `references/authentication.md`
- **CORS issues?** → Load `references/cors-security.md`
- **Validating input?** → Load `references/input-validation.md`
- **Managing secrets?** → Load `references/secrets-management.md`
- **Rate limiting?** → Load `references/rate-limiting.md`
- **Security headers?** → Load `references/security-headers.md`

## Templates

| Template | Purpose | Use When |
|----------|---------|----------|
| `templates/auth-middleware.ts` | JWT/API key auth | Adding authentication |
| `templates/cors-handler.ts` | CORS middleware | Handling cross-origin |
| `templates/rate-limiter.ts` | Rate limiting | Preventing abuse |
| `templates/secure-worker.ts` | Full secure setup | Starting secure project |

## Scripts

| Script | Purpose | Command |
|--------|---------|---------|
| `scripts/security-audit.sh` | Audit security | `./security-audit.sh <url>` |

## Resources

- Security: https://developers.cloudflare.com/workers/platform/security/
- WAF: https://developers.cloudflare.com/waf/
- Rate Limiting: https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/
