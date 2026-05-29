---
name: tools-email
description: Email delivery using Resend API. Use this skill when implementing email verification flows, password reset, transactional emails, configuring DNS (SPF/DKIM/DMARC), setting up the Resend MCP server, or following email best practices for deliverability. Includes Next.js 16 proxy patterns, OAuth vs password user handling, and token security patterns.
---

# Email Resend Skill

This skill provides workflows, best practices, and code patterns for sending transactional emails using [Resend](https://resend.com).

## Overview

Resend is a modern email API designed for developers. It provides:
- Simple REST API and SDKs
- React Email integration for beautiful templates
- Built-in analytics and deliverability monitoring
- MCP server for AI-assisted email workflows

## Prerequisites

### 1. Resend Account Setup

1. Sign up at [resend.com](https://resend.com)
2. Generate an API key in the dashboard
3. Add to your environment:

```bash
# .env.local
RESEND_API_KEY=re_xxxxx
RESEND_FROM_EMAIL="App Name <noreply@yourdomain.com>"
```

### 2. Domain Verification

Before sending from your domain, you must verify it:

1. Go to Resend Dashboard → Domains → Add Domain
2. Add these DNS records at your provider:

| Type | Name | Value | Purpose |
|------|------|-------|---------|
| TXT | `@` or domain | `v=spf1 include:_spf.resend.com ~all` | SPF |
| CNAME | `resend._domainkey` | Provided by Resend | DKIM |
| TXT | `_dmarc` | `v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com` | DMARC |

3. Wait for verification (usually 5-60 minutes)

### 3. MCP Server Setup (Optional - for Cursor AI)

To use Resend directly from Cursor's AI:

1. Clone and build the MCP server:
```bash
cd ~/Desktop/Code
git clone https://github.com/resend/mcp-send-email.git mcp-send-email
cd mcp-send-email && npm install && npm run build
```

2. Get the **absolute path** (this is critical):
```bash
realpath ~/Desktop/Code/mcp-send-email/build/index.js
# Output: /Users/YOUR_USERNAME/Desktop/Code/mcp-send-email/build/index.js
```

3. Add to your `.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "resend": {
      "type": "command",
      "command": "node /Users/YOUR_USERNAME/Desktop/Code/mcp-send-email/build/index.js --key=re_xxxxx --sender=noreply@yourdomain.com"
    }
  }
}
```

> **Common Gotcha**: The path must be absolute and correct. `~/Code/` vs `~/Desktop/Code/` will cause `MODULE_NOT_FOUND` errors. Always verify with `realpath`.

## Code Patterns

### Basic Resend Client (TypeScript)

```typescript
// lib/email/index.ts
import { Resend } from 'resend'

const resend = new Resend(process.env.RESEND_API_KEY)

const FROM_EMAIL = process.env.RESEND_FROM_EMAIL || 'App <noreply@example.com>'
const APP_URL = process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'

export interface SendEmailOptions {
  to: string
  subject: string
  html: string
  text?: string
  replyTo?: string
}

export async function sendEmail(options: SendEmailOptions) {
  const { data, error } = await resend.emails.send({
    from: FROM_EMAIL,
    to: options.to,
    subject: options.subject,
    html: options.html,
    text: options.text,
    replyTo: options.replyTo,
  })

  if (error) {
    console.error('[Email] Failed to send:', error)
    throw new Error(`Failed to send email: ${error.message}`)
  }

  return data
}
```

### Verification Email

```typescript
export async function sendVerificationEmail(email: string, token: string) {
  const verifyUrl = `${APP_URL}/verify-email?token=${token}`
  
  return sendEmail({
    to: email,
    subject: 'Verify your email address',
    html: `
      <h2>Welcome!</h2>
      <p>Please verify your email address by clicking the button below:</p>
      <a href="${verifyUrl}" style="
        display: inline-block;
        background: #000;
        color: #fff;
        padding: 12px 24px;
        text-decoration: none;
        border-radius: 6px;
        margin: 16px 0;
      ">Verify Email</a>
      <p>Or copy this link: ${verifyUrl}</p>
      <p>This link expires in 24 hours.</p>
      <p style="color: #666; font-size: 12px;">
        If you didn't create an account, you can ignore this email.
      </p>
    `,
    text: `Verify your email: ${verifyUrl}`,
  })
}
```

### Password Reset Email

```typescript
export async function sendPasswordResetEmail(email: string, token: string) {
  const resetUrl = `${APP_URL}/reset-password?token=${token}`
  
  return sendEmail({
    to: email,
    subject: 'Reset your password',
    html: `
      <h2>Password Reset Request</h2>
      <p>We received a request to reset your password. Click below to choose a new one:</p>
      <a href="${resetUrl}" style="
        display: inline-block;
        background: #000;
        color: #fff;
        padding: 12px 24px;
        text-decoration: none;
        border-radius: 6px;
        margin: 16px 0;
      ">Reset Password</a>
      <p>Or copy this link: ${resetUrl}</p>
      <p>This link expires in 1 hour.</p>
      <p style="color: #666; font-size: 12px;">
        If you didn't request this, you can safely ignore this email.
      </p>
    `,
    text: `Reset your password: ${resetUrl}`,
  })
}
```

### Welcome Email (after verification)

```typescript
export async function sendWelcomeEmail(email: string, name?: string) {
  return sendEmail({
    to: email,
    subject: 'Welcome to App Name!',
    html: `
      <h2>Welcome${name ? `, ${name}` : ''}!</h2>
      <p>Your email has been verified and your account is ready.</p>
      <p>Here are some things you can do:</p>
      <ul>
        <li>Complete your profile</li>
        <li>Explore features</li>
        <li>Check out the documentation</li>
      </ul>
      <a href="${APP_URL}" style="
        display: inline-block;
        background: #000;
        color: #fff;
        padding: 12px 24px;
        text-decoration: none;
        border-radius: 6px;
        margin: 16px 0;
      ">Get Started</a>
    `,
    text: `Welcome! Your account is ready. Get started at ${APP_URL}`,
  })
}
```

## Database Schema

Add these tables for email verification and password reset:

```sql
-- Add to users table
ALTER TABLE users ADD COLUMN email_verified_at TEXT;

-- Email verification tokens (one-time use)
CREATE TABLE email_verification_tokens (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token_hash TEXT NOT NULL UNIQUE,  -- SHA-256 hash, never store raw
  expires_at TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Password reset tokens (one-time use)
CREATE TABLE password_reset_tokens (
  id TEXT PRIMARY KEY,
  email TEXT NOT NULL,  -- Use email, not user_id (user might not exist)
  token_hash TEXT NOT NULL UNIQUE,
  expires_at TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_verification_tokens_hash ON email_verification_tokens(token_hash);
CREATE INDEX idx_reset_tokens_hash ON password_reset_tokens(token_hash);
```

## Token Generation Pattern

Use secure, URL-safe tokens for verification and reset links:

```typescript
// lib/auth/tokens.ts
import { sha256 } from 'oslo/crypto'
import { encodeBase64url, encodeHex } from 'oslo/encoding'

// Token valid for 24 hours
const VERIFICATION_TOKEN_EXPIRY = 24 * 60 * 60 * 1000
// Reset token valid for 1 hour  
const RESET_TOKEN_EXPIRY = 60 * 60 * 1000

/**
 * Generate a cryptographically secure token
 */
export function generateToken(): string {
  const bytes = new Uint8Array(32)
  crypto.getRandomValues(bytes)
  return encodeBase64url(bytes)
}

/**
 * Hash a token for database storage
 * Never store raw tokens - always hash them
 */
export async function hashToken(token: string): Promise<string> {
  return encodeHex(await sha256(new TextEncoder().encode(token)))
}
```

### Token Security Rules

1. **Never store raw tokens** - Always hash with SHA-256 before storing
2. **One-time use** - Delete token after successful validation
3. **Delete existing tokens** - When creating new token, delete any existing ones for that user/email
4. **Short expiry for reset** - Password reset tokens should expire in 1 hour max
5. **Longer expiry for verification** - Email verification can be 24-48 hours

## Rate Limiting

Prevent email abuse with rate limiting:

```typescript
// Per-email rate limits
const EMAIL_RATE_LIMITS = {
  verification: { max: 3, window: 60 * 60 * 1000 },    // 3 per hour
  passwordReset: { max: 3, window: 60 * 60 * 1000 },   // 3 per hour
  general: { max: 10, window: 24 * 60 * 60 * 1000 },   // 10 per day
}
```

## Resend API Limits

| Plan | Emails/day | Emails/month | Rate limit |
|------|------------|--------------|------------|
| Free | 100 | 3,000 | 2/second |
| Pro | 5,000+ | Based on plan | 10/second |

## OAuth vs Password Users

When implementing email verification, handle OAuth and password users differently:

```typescript
// OAuth users (Google, Apple, etc.) - pre-verified
const user = createUser({
  // ...
  email_verified_at: new Date().toISOString(), // Trust OAuth provider
})

// Password users - require verification
const user = createUser({
  // ...
  email_verified_at: null, // Must verify via email
})
```

### Verification Flow by Auth Type

| Auth Type | Email Verified? | Verification Required? |
|-----------|----------------|----------------------|
| Google OAuth | Yes (by Google) | No |
| Apple OAuth | Yes (by Apple) | No |
| Email/Password | No | Yes - block until verified |
| Magic Link | Yes (implicit) | No |

### Handling Unverified Login Attempts

```typescript
// In login API
if (!user.email_verified_at) {
  return NextResponse.json({
    error: 'Please verify your email before signing in.',
    code: 'EMAIL_NOT_VERIFIED',
    requiresVerification: true,
  }, { status: 403 })
}
```

### Re-signup for Unverified Users

If a user tries to sign up with an email that exists but isn't verified, resend the verification:

```typescript
const existingUser = getUserByEmail(email)
if (existingUser && !existingUser.email_verified_at) {
  // Resend verification instead of returning error
  const { token } = await createVerificationToken(existingUser.id)
  await sendVerificationEmail(email, token)
  return { requiresVerification: true }
}
```

## Next.js Integration

### Next.js 16+ (proxy.ts)

> **Breaking Change**: Next.js 16 replaced `middleware.ts` with `proxy.ts`

For protected routes, use `proxy.ts` for fast redirects only:

```typescript
// src/proxy.ts
export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl
  
  // Allow auth routes
  if (['/login', '/verify-email', '/forgot-password', '/reset-password']
      .some(r => pathname.startsWith(r))) {
    return NextResponse.next()
  }
  
  // Let API routes handle their own auth
  return NextResponse.next()
}
```

**Important**: Don't do heavy auth validation in proxy. Check `email_verified_at` in your API routes and server components instead.

### Next.js 16 and earlier

Use `middleware.ts` with the same logic, but export as `middleware` instead of `proxy`.

## Best Practices

### Subject Lines
- Keep under 60 characters
- Be specific and action-oriented
- Avoid spam triggers (see references/deliverability.md)

### Email Copy
- Front-load important information
- Use clear CTAs
- Always include plain text fallback
- Keep emails focused on one purpose

### Transactional vs Marketing
- **Transactional**: Triggered by user action (verification, reset, receipts)
- **Marketing**: Promotional content (newsletters, announcements)
- Keep them separate - different sending reputations

### Error Handling
- Log all email failures
- Have fallback mechanisms (show token in UI for dev)
- Don't block user actions on email failures

### Verification Strategies

| Strategy | UX | Security | Use Case |
|----------|----|---------|----|
| Block until verified | Friction | High | Financial, healthcare |
| Soft verification (banner) | Smooth | Medium | Social, content apps |
| No verification | Seamless | Low | Low-risk apps |

## Implementation Checklist

### Email Verification Flow

- [ ] Add `email_verified_at` column to users table
- [ ] Create `email_verification_tokens` table
- [ ] Install `resend` and `oslo` packages
- [ ] Create email service (`lib/email/index.ts`)
- [ ] Create token utilities (`lib/auth/tokens.ts`)
- [ ] Modify signup to send verification email
- [ ] Create `/api/auth/verify-email` endpoint
- [ ] Create `/api/auth/resend-verification` endpoint (rate limited)
- [ ] Create `/verify-email` page with resend UI
- [ ] Update login to check `email_verified_at`
- [ ] Handle OAuth users as pre-verified

### Password Reset Flow

- [ ] Create `password_reset_tokens` table
- [ ] Create `/api/auth/forgot-password` endpoint
- [ ] Create `/api/auth/reset-password` endpoint
- [ ] Create `/forgot-password` page
- [ ] Create `/reset-password` page
- [ ] Add "Forgot password?" link to login page

### Environment Variables

```bash
RESEND_API_KEY=re_xxxxx
RESEND_FROM_EMAIL="App Name <noreply@yourdomain.com>"
NEXT_PUBLIC_APP_URL=https://yourapp.com
```

## References

- [Deliverability Guide](references/deliverability.md) - DNS, spam prevention, reputation
- [Email Templates](references/templates.md) - Copy best practices, compliance
- [React Email Patterns](references/react-email.md) - Component-based email templates

## Common Issues & Troubleshooting

### MCP Server "MODULE_NOT_FOUND"

**Cause**: Wrong path in `.cursor/mcp.json`

**Fix**: Use absolute path, verify with `realpath`:
```bash
realpath ~/Desktop/Code/mcp-send-email/build/index.js
```

### Emails Going to Spam

1. Verify DNS records (SPF, DKIM, DMARC) are correct
2. Check sender domain matches authenticated domain
3. Review email content for spam trigger words
4. Test with [mail-tester.com](https://mail-tester.com)

### Token Validation Failing

1. Ensure you're hashing the token before lookup
2. Check token hasn't expired
3. Verify token wasn't already consumed (one-time use)
4. Check for URL encoding issues in the token

### OAuth Users Can't Reset Password

OAuth-only users don't have passwords. Check for `password_hash`:
```typescript
if (!user.password_hash) {
  return { error: 'This account uses social login.' }
}
```

### Next.js 16 Proxy Not Working

1. File must be `src/proxy.ts` (not `middleware.ts`)
2. Export must be `proxy` (not `middleware`)
3. Proxy runs on Node.js runtime, not Edge

## Dependencies

Install the Resend SDK:

```bash
npm install resend
```

For token hashing (recommended):

```bash
npm install oslo
```

For React Email templates (optional):

```bash
npm install @react-email/components react-email
```
