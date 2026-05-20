---
name: better-auth
description: Provides Better Auth authentication integration patterns for NestJS backend and Next.js frontend with Drizzle ORM and PostgreSQL. Use when implementing authentication - Setting up Better Auth with NestJS backend, Integrating Next.js App Router frontend, Configuring Drizzle ORM schema with PostgreSQL, Implementing social login (GitHub, Google, etc.), Adding plugins (2FA, Organization, SSO, Magic Link, Passkey), Email/password authentication with session management, Creating protected routes and middleware
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Better Auth Integration Guide

## Overview

Better Auth is a comprehensive authentication framework for TypeScript that provides type-safe authentication with support for multiple providers, 2FA, SSO, organizations, and more. This skill covers complete integration patterns for NestJS backend with Drizzle ORM and PostgreSQL, plus Next.js App Router frontend integration.

## When to Use

- Setting up Better Auth with NestJS backend
- Integrating Next.js App Router frontend with Better Auth
- Configuring Drizzle ORM schema with PostgreSQL for authentication
- Implementing social login (GitHub, Google, Facebook, Microsoft, etc.)
- Adding Multi-Factor Authentication (MFA/2FA) with TOTP
- Implementing passkey (WebAuthn) passwordless authentication
- Managing trusted devices for streamlined authentication
- Using backup codes for 2FA account recovery
- Adding authentication plugins (2FA, Organization, SSO, Magic Link, Passkey)
- Email/password authentication with secure session management
- Creating protected routes and authentication middleware
- Implementing role-based access control (RBAC)
- Building multi-tenant applications with organizations

## Quick Start

### Installation

```bash
# Backend (NestJS)
npm install better-auth @auth/drizzle-adapter
npm install drizzle-orm pg
npm install -D drizzle-kit

# Frontend (Next.js)
npm install better-auth
```

### Basic Setup

1. Configure Better Auth instance (backend)
2. Set up Drizzle schema with Better Auth tables
3. Create auth module in NestJS
4. Configure Next.js auth client
5. Set up middleware for protected routes

See References/ for detailed setup instructions.

## Architecture

### Backend (NestJS)

```
src/
├── auth/
│   ├── auth.module.ts           # Auth module configuration
│   ├── auth.controller.ts       # Auth HTTP endpoints
│   ├── auth.service.ts          # Business logic
│   ├── auth.guard.ts            # Route protection
│   └── schema.ts                # Drizzle auth schema
├── database/
│   ├── database.module.ts       # Database module
│   └── database.service.ts      # Drizzle connection
└── main.ts
```

### Frontend (Next.js)

```
app/
├── (auth)/
│   ├── sign-in/
│   │   └── page.tsx            # Sign in page
│   └── sign-up/
│       └── page.tsx            # Sign up page
├── (dashboard)/
│   ├── dashboard/
│   │   └── page.tsx            # Protected page
│   └── layout.tsx              # With auth check
├── api/
│   └── auth/
│       └── [...auth]/route.ts  # Auth API route
├── layout.tsx                   # Root layout
└── middleware.ts                # Auth middleware
lib/
├── auth.ts                      # Better Auth client
└── utils.ts
```

## Instructions

### Phase 1: Database Setup

1. **Install Dependencies**
   ```bash
   npm install drizzle-orm pg @auth/drizzle-adapter better-auth
   npm install -D drizzle-kit
   ```

2. **Configure Drizzle**
   - Create `drizzle.config.ts`
   - Set up database connection
   - Define schema with Better Auth tables

3. **Generate and Run Migrations**
   ```bash
   npx drizzle-kit generate
   npx drizzle-kit migrate
   ```

### Phase 2: Backend Setup (NestJS)

1. **Create Database Module**
   - Set up Drizzle connection
   - Provide database service

2. **Configure Better Auth**
   - Create auth instance with Drizzle adapter
   - Configure providers (GitHub, Google, etc.)
   - Set up session management

3. **Create Auth Module**
   - Auth controller with endpoints
   - Auth service with business logic
   - Auth guard for protection

### Phase 3: Frontend Setup (Next.js)

1. **Configure Auth Client**
   - Set up Better Auth client
   - Configure server actions

2. **Create Auth Pages**
   - Sign in page
   - Sign up page
   - Error handling

3. **Add Middleware**
   - Protect routes
   - Handle redirects

### Phase 4: Advanced Features

1. **Social Providers**
   - Configure OAuth apps
   - Add provider callbacks

2. **Plugins**
   - Two-Factor Authentication (2FA)
   - Organizations
   - SSO
   - Magic Links
   - Passkeys

## Examples

### Example 1: Complete NestJS Auth Setup

**Input:** Developer needs to set up Better Auth in a new NestJS project with PostgreSQL.

**Process:**
```typescript
// 1. Create auth instance
export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: "pg",
    schema: { ...schema }
  }),
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    }
  }
});

// 2. Create auth controller
@Controller('auth')
export class AuthController {
  @All('*')
  async handleAuth(@Req() req: Request, @Res() res: Response) {
    return auth.handler(req);
  }
}
```

**Output:** Fully functional auth endpoints at `/auth/*` with GitHub OAuth support.

### Example 2: Next.js Middleware for Route Protection

**Input:** Protect dashboard routes in Next.js App Router.

**Process:**
```typescript
// middleware.ts
import { auth } from '@/lib/auth';

export default auth((req) => {
  if (!req.auth && req.nextUrl.pathname.startsWith('/dashboard')) {
    const newUrl = new URL('/sign-in', req.nextUrl.origin);
    return Response.redirect(newUrl);
  }
});

export const config = {
  matcher: ['/dashboard/:path*', '/api/protected/:path*']
};
```

**Output:** Unauthenticated users are redirected to `/sign-in` when accessing `/dashboard/*`.

### Example 3: Server Component with Session

**Input:** Display user data in a Next.js Server Component.

**Process:**
```typescript
// app/dashboard/page.tsx
import { auth } from '@/lib/auth';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const session = await auth();

  if (!session) {
    redirect('/sign-in');
  }

  return (
    <div>
      <h1>Welcome, {session.user.name}</h1>
      <p>Email: {session.user.email}</p>
    </div>
  );
}
```

**Output:** Renders user information only for authenticated users, redirects others to sign-in.

### Example 4: Adding Two-Factor Authentication

**Input:** Enable 2FA for enhanced account security.

**Process:**
```typescript
// Enable 2FA plugin
export const auth = betterAuth({
  plugins: [
    twoFactor({
      issuer: 'MyApp',
      otpOptions: {
        digits: 6,
        period: 30
      }
    })
  ]
});

// Client-side enable 2FA
const { data, error } = await authClient.twoFactor.enable({
  password: 'user-password'
});
```

**Output:** Users can enable TOTP-based 2FA and verify with authenticator apps.

### Example 5: TOTP Verification with Trusted Device

**Input:** User has enabled 2FA and wants to sign in, marking the device as trusted.

**Process:**
```typescript
// Server-side: Configure 2FA with OTP sending
export const auth = betterAuth({
  plugins: [
    twoFactor({
      issuer: 'MyApp',
      otpOptions: {
        async sendOTP({ user, otp }, ctx) {
          // Send OTP via email, SMS, or other method
          await sendEmail({
            to: user.email,
            subject: 'Your verification code',
            body: `Code: ${otp}`
          });
        }
      }
    })
  ]
});

// Client-side: Verify TOTP and trust device
const verify2FA = async (code: string) => {
  const { data, error } = await authClient.twoFactor.verifyTotp({
    code,
    trustDevice: true  // Device trusted for 30 days
  });

  if (data) {
    // Redirect to dashboard
    router.push('/dashboard');
  }
};
```

**Output:** User is authenticated, device is trusted for 30 days (no 2FA prompt on next sign-ins).

### Example 6: Passkey Authentication Setup

**Input:** Enable passkey (WebAuthn) authentication for passwordless login.

**Process:**
```typescript
// Server-side: Configure passkey plugin
import { passkey } from '@better-auth/passkey';

export const auth = betterAuth({
  plugins: [
    passkey({
      rpID: 'example.com',      // Relying Party ID (your domain)
      rpName: 'My App',         // Display name
      advanced: {
        webAuthnChallengeCookie: 'my-app-passkey'
      }
    })
  ]
});

// Client-side: Register passkey
const registerPasskey = async () => {
  const { data, error } = await authClient.passkey.register({
    name: 'My Device'
  });

  if (data) {
    console.log('Passkey registered successfully');
  }
};

// Client-side: Sign in with passkey
const signInWithPasskey = async () => {
  await authClient.signIn.passkey({
    autoFill: true,  // Enable conditional UI
    fetchOptions: {
      onSuccess() {
        router.push('/dashboard');
      }
    }
  });
};
```

**Output:** Users can register and authenticate with passkeys (biometric, PIN, or security key).

### Example 7: Passkey Conditional UI (Autofill)

**Input:** Implement passkey autofill in sign-in form for seamless authentication.

**Process:**
```tsx
// Component with conditional UI support
'use client';

import { useEffect } from 'react';
import { authClient } from '@/lib/auth/client';

export default function SignInPage() {
  useEffect(() => {
    // Check for conditional mediation support
    if (!PublicKeyCredential.isConditionalMediationAvailable ||
        !PublicKeyCredential.isConditionalMediationAvailable()) {
      return;
    }

    // Enable passkey autofill
    void authClient.signIn.passkey({ autoFill: true });
  }, []);

  return (
    <form>
      <label htmlFor="email">Email:</label>
      <input
        type="email"
        name="email"
        autoComplete="username webauthn"
      />
      <label htmlFor="password">Password:</label>
      <input
        type="password"
        name="password"
        autoComplete="current-password webauthn"
      />
      <button type="submit">Sign In</button>
    </form>
  );
}
```

**Output:** Browser automatically suggests passkeys when user focuses on input fields.

### Example 8: Backup Codes for 2FA Recovery

**Input:** User needs backup codes to recover account if authenticator app is lost.

**Process:**
```typescript
// Enable 2FA - backup codes are generated automatically
const enable2FA = async (password: string) => {
  const { data, error } = await authClient.twoFactor.enable({
    password
  });

  if (data) {
    // IMPORTANT: Display backup codes to user immediately
    console.log('Backup codes (save these securely):');
    data.backupCodes.forEach((code: string) => {
      console.log(code);
    });

    // Show TOTP URI as QR code
    const qrCodeUrl = data.totpURI;
    displayQRCode(qrCodeUrl);
  }
};

// Recover with backup code
const recoverWithBackupCode = async (code: string) => {
  const { data, error } = await authClient.twoFactor.verifyBackupCode({
    code
  });

  if (data) {
    // Allow user to disable 2FA or set up new authenticator
    router.push('/settings/2fa');
  }
};
```

**Output:** User receives single-use backup codes for account recovery.

## Common Patterns

### Protected Route Pattern

```typescript
// NestJS Guard
@Controller('dashboard')
@UseGuards(AuthGuard)
export class DashboardController {
  @Get()
  getDashboard(@Request() req) {
    return req.user;
  }
}
```

```typescript
// Next.js Server Component
import { auth } from '@/lib/auth';
import { redirect } from 'next/navigation';

export default async function Dashboard() {
  const session = await auth();
  if (!session) {
    redirect('/sign-in');
  }
  return <div>Welcome {session.user.name}</div>;
}
```

### Session Management Pattern

```typescript
// Get session in API route
const session = await auth.api.getSession({
  headers: await headers()
});

// Get session in Server Component
const session = await auth();

// Get session in Client Component
'use client';
import { useSession } from '@/lib/auth/client';
const { data: session } = useSession();
```

## Best Practices

1. **Environment Variables**: Always use environment variables for sensitive data (secrets, database URLs, OAuth credentials)

2. **Secret Generation**: Use strong, unique secrets for Better Auth. Generate with `openssl rand -base64 32`

3. **HTTPS Required**: OAuth callbacks require HTTPS in production. Use `ngrok` or similar for local testing

4. **Session Security**: Configure appropriate session expiration times based on your security requirements

5. **Database Indexing**: Add indexes on frequently queried fields (email, userId) for performance

6. **Error Handling**: Implement proper error handling for auth failures without revealing sensitive information

7. **Rate Limiting**: Add rate limiting to auth endpoints to prevent brute force attacks

8. **CSRF Protection**: Better Auth includes CSRF protection. Always use the provided methods for state changes

9. **Type Safety**: Leverage TypeScript types from Better Auth for full type safety across frontend and backend

10. **Testing**: Test auth flows thoroughly including success cases, error cases, and edge conditions

## Constraints and Warnings

### Security Notes

- **Never commit secrets**: Add `.env` to `.gitignore` and never commit OAuth secrets or database credentials
- **Validate redirect URLs**: Always validate OAuth redirect URLs to prevent open redirects
- **Hash passwords**: Better Auth handles password hashing automatically. Never implement your own
- **Session storage**: For production, use Redis or another scalable session store
- **HTTPS Only**: Always use HTTPS for authentication in production
- **OAuth Secrets**: Keep OAuth client secrets secure. Rotate them periodically
- **Email Verification**: Always implement email verification for password-based auth

### Known Limitations

- Better Auth requires Node.js 18+ for Next.js App Router support
- Some OAuth providers require specific redirect URL formats
- Passkeys require HTTPS and compatible browsers
- Organization features require additional database tables

## Version Requirements

### Backend Dependencies

```json
{
  "dependencies": {
    "better-auth": "^1.2.0",
    "@auth/drizzle-adapter": "^1.0.0",
    "drizzle-orm": "^0.35.0",
    "pg": "^8.12.0",
    "@nestjs/common": "^10.0.0",
    "@nestjs/core": "^10.0.0",
    "@nestjs/config": "^3.0.0"
  },
  "devDependencies": {
    "drizzle-kit": "^0.24.0",
    "@types/pg": "^8.11.0"
  }
}
```

### Frontend Dependencies

```json
{
  "dependencies": {
    "better-auth": "^1.2.0",
    "next": "^15.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  }
}
```

### Database

- PostgreSQL 14+ recommended
- For local development: Docker PostgreSQL or Postgres.app

## Troubleshooting

### 1. "Session not found" errors

**Problem**: Session data is not being persisted or retrieved correctly.

**Solution**:
- Verify database connection is working
- Check session table exists and has data
- Ensure `BETTER_AUTH_SECRET` is set consistently
- Verify cookie domain settings match your application domain

### 2. OAuth callback fails with "Invalid state"

**Problem**: OAuth state mismatch during callback.

**Solution**:
- Clear cookies and try again
- Ensure `BETTER_AUTH_URL` is set correctly in environment
- Check that redirect URI in OAuth app matches exactly
- Verify no reverse proxy is modifying callbacks

### 3. TypeScript type errors with auth()

**Problem**: Type inference not working correctly.

**Solution**:
- Ensure TypeScript 5+ is installed
- Use `npx better-auth typegen` to generate types
- Restart TypeScript server in your IDE
- Check that `better-auth` versions match on frontend and backend

### 4. Migration fails with "table already exists"

**Problem**: Drizzle migration conflicts.

**Solution**:
- Drop existing tables and re-run migration
- Or use `drizzle-kit push` for development
- For production, write manual migration to handle existing tables

### 5. CORS errors from frontend to backend

**Problem**: Frontend cannot communicate with backend auth endpoints.

**Solution**:
- Configure CORS in NestJS backend
- Add frontend origin to allowed origins
- Ensure credentials are included: `credentials: 'include'`

### 6. Social provider returns "redirect_uri_mismatch"

**Problem**: OAuth app configuration mismatch.

**Solution**:
- Update OAuth app with exact callback URL
- Include both http://localhost and production URLs
- For ngrok/local testing, update OAuth app each time URL changes

## Resources

### Documentation

- [Better Auth Documentation](https://www.better-auth.com)
- [Drizzle ORM Documentation](https://orm.drizzle.team)
- [NestJS Documentation](https://docs.nestjs.com)
- [Next.js App Router Documentation](https://nextjs.org/docs/app)

### Reference Implementations

- See `references/nestjs-setup.md` for complete NestJS setup
- See `references/nextjs-setup.md` for complete Next.js setup
- See `references/plugins.md` for plugin configuration
- See `assets/` for example code files

### Environment Variables

See `Assets/env.example` for all required environment variables.

## Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Better Auth
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000

# OAuth Providers
AUTH_GITHUB_CLIENT_ID=your-github-client-id
AUTH_GITHUB_CLIENT_SECRET=your-github-client-secret

AUTH_GOOGLE_CLIENT_ID=your-google-client-id
AUTH_GOOGLE_CLIENT_SECRET=your-google-client-secret

# Email (for magic links and verification)
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your-smtp-user
SMTP_PASSWORD=your-smtp-password
SMTP_FROM=noreply@example.com

# Session (optional, for Redis)
REDIS_URL=redis://localhost:6379
```
