---
name: security-hardener
description: Implement security headers, input validation, and CSRF protection. Use when hardening security, reviewing for vulnerabilities, or before releases.
---

# Security Hardening

## When to Use

- Before production releases
- When handling user input
- Reviewing code for vulnerabilities
- Implementing authentication flows
- Setting up API endpoints

## Quick Reference

### Security Headers (Next.js)

```typescript
// next.config.js
const securityHeaders = [
  {
    key: "X-DNS-Prefetch-Control",
    value: "on",
  },
  {
    key: "Strict-Transport-Security",
    value: "max-age=63072000; includeSubDomains; preload",
  },
  {
    key: "X-Frame-Options",
    value: "SAMEORIGIN",
  },
  {
    key: "X-Content-Type-Options",
    value: "nosniff",
  },
  {
    key: "Referrer-Policy",
    value: "origin-when-cross-origin",
  },
  {
    key: "Permissions-Policy",
    value: "camera=(), microphone=(), geolocation=()",
  },
];

module.exports = {
  async headers() {
    return [
      {
        source: "/:path*",
        headers: securityHeaders,
      },
    ];
  },
};
```

### Content Security Policy

```typescript
// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const nonce = Buffer.from(crypto.randomUUID()).toString("base64");

  const cspHeader = `
    default-src 'self';
    script-src 'self' 'nonce-${nonce}' 'strict-dynamic';
    style-src 'self' 'unsafe-inline';
    img-src 'self' blob: data: https:;
    font-src 'self';
    connect-src 'self' https://*.firebaseio.com https://*.googleapis.com;
    frame-ancestors 'none';
    form-action 'self';
    base-uri 'self';
  `
    .replace(/\s{2,}/g, " ")
    .trim();

  const response = NextResponse.next();
  response.headers.set("Content-Security-Policy", cspHeader);
  response.headers.set("x-nonce", nonce);

  return response;
}
```

### Input Validation with Zod

```typescript
// lib/validation.ts
import { z } from "zod";

// Sanitize string input
const sanitizedString = z
  .string()
  .trim()
  .max(1000)
  .transform((s) => s.replace(/<[^>]*>/g, "")); // Strip HTML

// Email validation
const emailSchema = z.string().email().toLowerCase().max(255);

// ID validation (prevent injection)
const idSchema = z
  .string()
  .regex(/^[a-zA-Z0-9_-]+$/)
  .max(128);

// URL validation
const urlSchema = z
  .string()
  .url()
  .refine((url) => {
    const parsed = new URL(url);
    return ["http:", "https:"].includes(parsed.protocol);
  }, "Invalid protocol");

// Example: Journal entry validation
export const journalEntrySchema = z.object({
  title: sanitizedString.max(200),
  content: sanitizedString.max(50000),
  tags: z.array(z.string().max(50)).max(20),
  mood: z.enum(["happy", "neutral", "sad", "anxious", "excited"]),
  isPrivate: z.boolean().default(false),
});
```

### API Route Protection

```typescript
// app/api/entries/route.ts
import { NextRequest, NextResponse } from "next/server";
import { getServerSession } from "@/lib/auth";
import { rateLimit } from "@/lib/rate-limit";

export async function POST(request: NextRequest) {
  // 1. Rate limiting
  const ip = request.headers.get("x-forwarded-for") || "unknown";
  const { success, remaining } = await rateLimit(ip, 10, "1m");

  if (!success) {
    return NextResponse.json(
      { error: "Too many requests" },
      { status: 429, headers: { "Retry-After": "60" } },
    );
  }

  // 2. Authentication
  const session = await getServerSession();
  if (!session?.user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  // 3. Input validation
  const body = await request.json();
  const result = journalEntrySchema.safeParse(body);

  if (!result.success) {
    return NextResponse.json(
      { error: "Invalid input", details: result.error.flatten() },
      { status: 400 },
    );
  }

  // 4. Authorization check
  if (body.userId !== session.user.id) {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  // 5. Process validated data
  const entry = await createEntry(result.data);
  return NextResponse.json({ data: entry }, { status: 201 });
}
```

### Rate Limiting

```typescript
// lib/rate-limit.ts
const rateLimitMap = new Map<string, { count: number; resetTime: number }>();

export async function rateLimit(
  key: string,
  limit: number,
  window: string,
): Promise<{ success: boolean; remaining: number }> {
  const windowMs = parseWindow(window);
  const now = Date.now();

  const record = rateLimitMap.get(key);

  if (!record || now > record.resetTime) {
    rateLimitMap.set(key, { count: 1, resetTime: now + windowMs });
    return { success: true, remaining: limit - 1 };
  }

  if (record.count >= limit) {
    return { success: false, remaining: 0 };
  }

  record.count++;
  return { success: true, remaining: limit - record.count };
}

function parseWindow(window: string): number {
  const match = window.match(/^(\d+)([smh])$/);
  if (!match) return 60000;

  const [, num, unit] = match;
  const multipliers = { s: 1000, m: 60000, h: 3600000 };
  return parseInt(num) * multipliers[unit as keyof typeof multipliers];
}
```

### XSS Prevention

```typescript
// lib/sanitize.ts

// For displaying user content safely
export function escapeHtml(unsafe: string): string {
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// For URLs in href attributes
export function sanitizeUrl(url: string): string {
  try {
    const parsed = new URL(url);
    if (!["http:", "https:", "mailto:"].includes(parsed.protocol)) {
      return "#";
    }
    return url;
  } catch {
    return "#";
  }
}

// For rendering user-provided HTML content:
// - Use DOMPurify library to sanitize before rendering
// - Prefer text content over HTML when possible
// - Use React's built-in escaping (JSX expressions)
```

## Security Checklist

### Authentication

- [ ] Session tokens are HttpOnly, Secure, SameSite=Strict
- [ ] Passwords hashed with bcrypt (cost factor 12+)
- [ ] Rate limiting on login attempts
- [ ] Account lockout after failed attempts
- [ ] Secure password reset flow

### Authorization

- [ ] Every API route checks authentication
- [ ] Resource ownership verified before operations
- [ ] Role-based access control where needed
- [ ] No sensitive data in URLs

### Input Handling

- [ ] All user input validated with Zod schemas
- [ ] File uploads validated (type, size, content)
- [ ] SQL/NoSQL injection prevented (parameterized queries)
- [ ] XSS prevention (escape output, CSP)

### Data Protection

- [ ] Sensitive data encrypted at rest
- [ ] PII minimized and access logged
- [ ] Secure deletion when required
- [ ] No secrets in client bundles

### Infrastructure

- [ ] HTTPS everywhere (HSTS enabled)
- [ ] Security headers configured
- [ ] Dependencies regularly audited
- [ ] Error messages don't leak internals

## Common Vulnerabilities to Check

| Vulnerability  | Check                          | Fix                     |
| -------------- | ------------------------------ | ----------------------- |
| XSS            | User content rendered unsafely | Escape HTML, use CSP    |
| CSRF           | State-changing GET requests    | Use POST + tokens       |
| Injection      | Raw user input in queries      | Parameterized queries   |
| Auth bypass    | Missing auth checks            | Middleware protection   |
| Data exposure  | Sensitive data in responses    | Filter response fields  |
| Path traversal | User-controlled file paths     | Validate/sanitize paths |

## See Also

- [checklist.md](checklist.md) - Full security checklist
- [headers.md](headers.md) - Security header reference
