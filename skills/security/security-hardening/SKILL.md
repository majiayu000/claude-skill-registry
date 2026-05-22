---
name: security-hardening
description: Security best practices for Shopify Apps. Covers OWASP Top 10, authentication, data protection, webhook verification, and secure coding patterns for Remix applications.
---

# Security Hardening for Shopify Apps

This skill covers essential security practices for building secure Shopify apps. Security is non-negotiable when handling merchant data, customer PII, and payment information.

## Why Security Matters for Shopify Apps

- **Merchant Trust**: Apps handle sensitive business data
- **Customer PII**: Access to customer names, emails, addresses
- **Payment Data**: Some apps process or display financial information
- **App Store Requirements**: Shopify reviews apps for security compliance
- **Legal Liability**: GDPR, CCPA, and data protection regulations apply

## 1. Authentication & Authorization

### Session Management

```typescript
// app/routes/app.tsx - Secure session handling
import { authenticate } from '~/shopify.server';

export async function loader({ request }: LoaderFunctionArgs) {
  // ALWAYS authenticate every request
  const { admin, session } = await authenticate.admin(request);

  // Session contains sensitive data - never expose to client
  return json({
    shop: session.shop,
    // DON'T return: accessToken, session object directly
  });
}
```

### Route Protection Pattern

```typescript
// app/lib/auth.server.ts
import { authenticate } from '~/shopify.server';
import { redirect } from '@remix-run/node';

export async function requireAuth(request: Request) {
  try {
    return await authenticate.admin(request);
  } catch (error) {
    // Log for monitoring, don't expose details
    console.error('Authentication failed:', error);
    throw redirect('/auth/login');
  }
}

// Protect all app routes
// app/routes/app._index.tsx
export async function loader({ request }: LoaderFunctionArgs) {
  const { admin, session } = await requireAuth(request);
  // ... rest of loader
}
```

### API Route Protection

```typescript
// app/routes/api.products.tsx
import { json, type ActionFunctionArgs } from '@remix-run/node';
import { authenticate } from '~/shopify.server';

export async function action({ request }: ActionFunctionArgs) {
  // ALWAYS authenticate API routes
  const { admin, session } = await authenticate.admin(request);

  // Validate request method
  if (request.method !== 'POST') {
    return json({ error: 'Method not allowed' }, { status: 405 });
  }

  // ... handle request
}

// Block unauthenticated GET requests
export async function loader({ request }: LoaderFunctionArgs) {
  await authenticate.admin(request);
  return json({ error: 'Use POST' }, { status: 405 });
}
```

## 2. Webhook Security

### HMAC Verification (Critical)

```typescript
// app/routes/webhooks.tsx
import crypto from 'crypto';
import { json, type ActionFunctionArgs } from '@remix-run/node';

export async function action({ request }: ActionFunctionArgs) {
  // Get raw body for HMAC verification
  const { topic, session, admin, payload } = await authenticate.webhook(request)

  // Process webhook...
  return json({ success: true });
}
```


## 2. Input Validation & Sanitization

### Never Trust User Input

```typescript
// app/lib/validation.server.ts
import { z } from 'zod';
import DOMPurify from 'isomorphic-dompurify';

// Sanitize HTML content
export function sanitizeHtml(dirty: string): string {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
    ALLOWED_ATTR: ['href'],
  });
}

// Validate Shopify GID format
export const shopifyGidSchema = z
  .string()
  .regex(
    /^gid:\/\/shopify\/[A-Za-z]+\/\d+$/,
    'Invalid Shopify GID format'
  );

// Validate and sanitize product input
export const productInputSchema = z.object({
  title: z
    .string()
    .min(1)
    .max(255)
    .transform(val => val.trim()),

  description: z
    .string()
    .max(5000)
    .transform(sanitizeHtml)
    .optional(),

  vendor: z
    .string()
    .max(255)
    .transform(val => val.trim())
    .optional(),

  tags: z
    .array(z.string().max(50).transform(val => val.trim()))
    .max(100)
    .optional(),
});
```

### SQL Injection Prevention

```typescript
// ALWAYS use parameterized queries with Prisma
// app/services/product.server.ts

// GOOD - Parameterized query (Prisma handles escaping)
export async function findProducts(shop: string, search: string) {
  return db.product.findMany({
    where: {
      shop,
      title: {
        contains: search, // Prisma escapes this automatically
        mode: 'insensitive',
      },
    },
  });
}

// BAD - Never do this!
// const products = await db.$queryRaw`
//   SELECT * FROM products WHERE title LIKE '%${search}%'
// `;

// If you MUST use raw queries, use Prisma.sql
export async function rawSearch(shop: string, search: string) {
  return db.$queryRaw`
    SELECT * FROM products
    WHERE shop = ${shop}
    AND title ILIKE ${`%${search}%`}
  `; // Prisma.sql handles escaping
}
```

### Command Injection Prevention

```typescript
// app/services/export.server.ts
import { execFile } from 'child_process';
import { promisify } from 'util';

const execFileAsync = promisify(execFile);

// GOOD - Use execFile with arguments array
export async function generatePdf(templatePath: string, outputPath: string) {
  // Validate paths
  if (!templatePath.startsWith('/app/templates/')) {
    throw new Error('Invalid template path');
  }

  // execFile doesn't use shell, so command injection is not possible
  await execFileAsync('wkhtmltopdf', [
    '--quiet',
    templatePath,
    outputPath,
  ]);
}

// BAD - Never use exec with user input
// exec(`wkhtmltopdf ${templatePath} ${outputPath}`); // VULNERABLE!
```

## 4. XSS Prevention

### React/Remix Built-in Protection

```typescript
// React automatically escapes content - this is SAFE
function ProductTitle({ title }: { title: string }) {
  return <h1>{title}</h1>; // Escaped automatically
}

// DANGER - dangerouslySetInnerHTML
function ProductDescription({ html }: { html: string }) {
  // Only use with sanitized content!
  const sanitized = DOMPurify.sanitize(html);

  return (
    <div
      dangerouslySetInnerHTML={{ __html: sanitized }}
    />
  );
}
```

### Content Security Policy

```typescript
// app/entry.server.tsx
import { renderToString } from 'react-dom/server';
import { RemixServer } from '@remix-run/react';

export default async function handleRequest(
  request: Request,
  responseStatusCode: number,
  responseHeaders: Headers,
  remixContext: EntryContext
) {
  const markup = renderToString(
    <RemixServer context={remixContext} url={request.url} />
  );

  // Set security headers
  responseHeaders.set('Content-Type', 'text/html');
  responseHeaders.set(
    'Content-Security-Policy',
    [
      "default-src 'self'",
      "script-src 'self' https://cdn.shopify.com",
      "style-src 'self' 'unsafe-inline' https://cdn.shopify.com",
      "img-src 'self' data: https://cdn.shopify.com https://*.shopifycdn.com",
      "connect-src 'self' https://*.shopify.com",
      "frame-ancestors https://*.myshopify.com https://admin.shopify.com",
    ].join('; ')
  );

  return new Response('<!DOCTYPE html>' + markup, {
    status: responseStatusCode,
    headers: responseHeaders,
  });
}
```

## 5. Data Protection

### Environment Variables Security

```typescript
// .env - NEVER commit this file
SHOPIFY_API_KEY=your_api_key
SHOPIFY_API_SECRET=your_api_secret
DATABASE_URL=postgresql://user:pass@host:5432/db
ENCRYPTION_KEY=your_32_byte_encryption_key

// app/lib/env.server.ts
import { z } from 'zod';

const envSchema = z.object({
  SHOPIFY_API_KEY: z.string().min(1),
  SHOPIFY_API_SECRET: z.string().min(1),
  DATABASE_URL: z.string().url(),
  ENCRYPTION_KEY: z.string().length(32),
  NODE_ENV: z.enum(['development', 'production', 'test']),
});

// Validate at startup
export const env = envSchema.parse(process.env);

// NEVER log secrets
console.log('Starting app with API key:', env.SHOPIFY_API_KEY.slice(0, 4) + '...');
```

### Encrypting Sensitive Data

```typescript
// app/lib/encryption.server.ts
import crypto from 'crypto';

const ALGORITHM = 'aes-256-gcm';
const IV_LENGTH = 16;
const AUTH_TAG_LENGTH = 16;
const ENCRYPTION_KEY = Buffer.from(process.env.ENCRYPTION_KEY!, 'hex');

export function encrypt(plaintext: string): string {
  const iv = crypto.randomBytes(IV_LENGTH);
  const cipher = crypto.createCipheriv(ALGORITHM, ENCRYPTION_KEY, iv);

  let encrypted = cipher.update(plaintext, 'utf8', 'hex');
  encrypted += cipher.final('hex');

  const authTag = cipher.getAuthTag();

  // Return iv:authTag:encrypted
  return `${iv.toString('hex')}:${authTag.toString('hex')}:${encrypted}`;
}

export function decrypt(ciphertext: string): string {
  const [ivHex, authTagHex, encrypted] = ciphertext.split(':');

  const iv = Buffer.from(ivHex, 'hex');
  const authTag = Buffer.from(authTagHex, 'hex');

  const decipher = crypto.createDecipheriv(ALGORITHM, ENCRYPTION_KEY, iv);
  decipher.setAuthTag(authTag);

  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');

  return decrypted;
}

// Usage: Encrypt sensitive metafield values
export async function storeSecureMetafield(
  admin: AdminApiClient,
  ownerId: string,
  key: string,
  value: string
) {
  const encryptedValue = encrypt(value);

  return admin.graphql(`
    mutation metafieldsSet($metafields: [MetafieldsSetInput!]!) {
      metafieldsSet(metafields: $metafields) {
        metafields { id }
        userErrors { field message }
      }
    }
  `, {
    variables: {
      metafields: [{
        ownerId,
        namespace: 'app_secure',
        key,
        value: encryptedValue,
        type: 'single_line_text_field',
      }],
    },
  });
}
```

### Data Retention & Deletion

```typescript
// app/services/gdpr.server.ts
import { db } from '~/db.server';
import { encrypt, decrypt } from '~/lib/encryption.server';

// Handle customers/data_request webhook
export async function handleDataRequest(shop: string, customerId: string) {
  const customerData = await db.customerData.findMany({
    where: { shop, customerId },
  });

  // Decrypt sensitive fields before returning
  return customerData.map(record => ({
    ...record,
    email: record.encryptedEmail ? decrypt(record.encryptedEmail) : null,
    phone: record.encryptedPhone ? decrypt(record.encryptedPhone) : null,
  }));
}

// Handle customers/redact webhook
export async function handleCustomerRedact(shop: string, customerId: string) {
  // Delete all customer data
  await db.customerData.deleteMany({
    where: { shop, customerId },
  });

  // Log for compliance
  await db.auditLog.create({
    data: {
      shop,
      action: 'customer_redact',
      targetId: customerId,
      timestamp: new Date(),
    },
  });
}

// Handle shop/redact webhook (app uninstall + 48h)
export async function handleShopRedact(shop: string) {
  // Delete ALL shop data
  await db.$transaction([
    db.product.deleteMany({ where: { shop } }),
    db.order.deleteMany({ where: { shop } }),
    db.customer.deleteMany({ where: { shop } }),
    db.session.deleteMany({ where: { shop } }),
    db.settings.deleteMany({ where: { shop } }),
  ]);

  console.log(`Shop data redacted: ${shop}`);
}
```

## 6. Rate Limiting & DoS Prevention

### Request Rate Limiting

```typescript
// app/lib/rate-limit.server.ts
import { LRUCache } from 'lru-cache';

interface RateLimitEntry {
  count: number;
  resetAt: number;
}

const cache = new LRUCache<string, RateLimitEntry>({
  max: 10000, // Max entries
  ttl: 60000, // 1 minute TTL
});

interface RateLimitOptions {
  maxRequests: number;
  windowMs: number;
}

export function rateLimit(
  identifier: string,
  options: RateLimitOptions = { maxRequests: 100, windowMs: 60000 }
): { allowed: boolean; remaining: number; resetAt: number } {
  const now = Date.now();
  const entry = cache.get(identifier);

  if (!entry || now > entry.resetAt) {
    // New window
    const newEntry = {
      count: 1,
      resetAt: now + options.windowMs,
    };
    cache.set(identifier, newEntry);
    return {
      allowed: true,
      remaining: options.maxRequests - 1,
      resetAt: newEntry.resetAt,
    };
  }

  if (entry.count >= options.maxRequests) {
    return {
      allowed: false,
      remaining: 0,
      resetAt: entry.resetAt,
    };
  }

  entry.count++;
  cache.set(identifier, entry);

  return {
    allowed: true,
    remaining: options.maxRequests - entry.count,
    resetAt: entry.resetAt,
  };
}

// Usage in routes
export async function action({ request }: ActionFunctionArgs) {
  const { session } = await authenticate.admin(request);

  const { allowed, remaining, resetAt } = rateLimit(session.shop, {
    maxRequests: 50,
    windowMs: 60000,
  });

  if (!allowed) {
    return json(
      { error: 'Too many requests' },
      {
        status: 429,
        headers: {
          'Retry-After': String(Math.ceil((resetAt - Date.now()) / 1000)),
          'X-RateLimit-Remaining': '0',
        },
      }
    );
  }

  // Process request...
}
```

## 7. Secure Headers

```typescript
// app/lib/security-headers.server.ts
export const securityHeaders = {
  // Prevent clickjacking (Shopify embedded apps need specific frame-ancestors)
  'X-Frame-Options': 'DENY', // For non-embedded pages

  // Prevent MIME type sniffing
  'X-Content-Type-Options': 'nosniff',

  // XSS Protection (legacy, but still useful)
  'X-XSS-Protection': '1; mode=block',

  // Referrer policy
  'Referrer-Policy': 'strict-origin-when-cross-origin',

  // Permissions policy
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',

  // HSTS (only in production)
  ...(process.env.NODE_ENV === 'production' && {
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
  }),
};

// Apply in entry.server.tsx
Object.entries(securityHeaders).forEach(([key, value]) => {
  responseHeaders.set(key, value);
});
```

## 8. Logging & Monitoring

### Secure Logging Practices

```typescript
// app/lib/logger.server.ts
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  redact: {
    // Never log these fields
    paths: [
      'accessToken',
      'password',
      'secret',
      'apiKey',
      'authorization',
      '*.accessToken',
      '*.password',
      'headers.authorization',
      'headers.x-shopify-access-token',
    ],
    censor: '[REDACTED]',
  },
});

export { logger };

// Usage
logger.info({ shop: session.shop, action: 'product_created' }, 'Product created');

// DON'T do this
// logger.info({ session }); // May leak accessToken!
```

### Security Event Logging

```typescript
// app/lib/security-events.server.ts
import { logger } from './logger.server';
import { db } from '~/db.server';

export async function logSecurityEvent(
  event: {
    type: 'auth_failure' | 'rate_limit' | 'suspicious_activity' | 'data_access';
    shop?: string;
    ip?: string;
    userAgent?: string;
    details: Record<string, unknown>;
  }
) {
  // Log to application logs
  logger.warn({ event }, `Security event: ${event.type}`);

  // Store in database for audit trail
  await db.securityEvent.create({
    data: {
      type: event.type,
      shop: event.shop,
      ip: event.ip,
      userAgent: event.userAgent,
      details: JSON.stringify(event.details),
      timestamp: new Date(),
    },
  });

  // Alert on critical events (integrate with your alerting system)
  if (event.type === 'suspicious_activity') {
    // Send alert to Slack, PagerDuty, etc.
  }
}
```

## 9. Security Checklist

### Before Deployment

- [ ] All routes authenticated with `authenticate.admin()`
- [ ] Webhook HMAC verification implemented
- [ ] Input validation on all user inputs (Zod schemas)
- [ ] No secrets in code or logs
- [ ] Environment variables validated at startup
- [ ] Rate limiting on API endpoints
- [ ] Security headers configured
- [ ] CSP configured for embedded app
- [ ] GDPR webhooks implemented (data_request, redact)

### Regular Audits

- [ ] Dependency audit: `npm audit`
- [ ] Check for outdated packages: `npm outdated`
- [ ] Review access logs for anomalies
- [ ] Test webhook verification
- [ ] Verify encryption keys are rotated periodically
- [ ] Review and remove unused API scopes

### Shopify-Specific

- [ ] Only request necessary API scopes
- [ ] Implement app proxy authentication if used
- [ ] Handle `app/uninstalled` webhook to clean up data
- [ ] Implement session token verification for App Bridge
- [ ] Test with Shopify's security review checklist

## Anti-Patterns to Avoid

- **DON'T** store access tokens in localStorage or cookies
- **DON'T** log full request/response bodies
- **DON'T** use `eval()` or `Function()` constructor
- **DON'T** trust client-side validation alone
- **DON'T** hardcode secrets in source code
- **DON'T** disable HTTPS in production
- **DON'T** ignore security warnings from `npm audit`
- **DON'T** use outdated dependencies with known vulnerabilities
