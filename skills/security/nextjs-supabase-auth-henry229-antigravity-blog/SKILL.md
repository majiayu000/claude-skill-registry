---
name: nextjs-supabase-auth
description: Production-ready authentication system for Next.js 15 + Supabase. Use when setting up auth, login, signup, OAuth, Google login, password reset, or user authentication.
---

# Next.js Supabase Auth Template

Production-ready authentication system for Next.js 15 + Supabase projects.

## Features

✅ **Security Hardened**
- PKCE Flow for OAuth
- RLS policies with least-privilege
- SQL Injection protection (search_path)
- Token validation with error handling

✅ **Complete Auth Flow**
- Email/Password signup & login
- Google OAuth
- Email confirmation
- Password reset
- Auto profile creation

✅ **Template Ready**
- Centralized config (`auth.config.ts`)
- Environment validation
- Type-safe configuration
- Reusable across projects

✅ **UI Components (shadcn/ui)**
- LoginForm
- SignupForm
- ForgotPasswordForm
- ResetPasswordForm
- GoogleLoginButton

## Profile Schema

Assumes `public.profiles` table with:
- `user_id` (uuid, FK to auth.users)
- `email` (text)
- `first_name` (text)
- `last_name` (text)
- `mobile` (text, nullable)
- `role` (text, default: 'user')

## Usage

```
/nextjs-supabase-auth
```

This will:
1. Copy all auth files to your project
2. Create configuration files
3. Generate database migrations
4. Provide setup instructions

## What You Need to Configure

After installation:

1. **Environment Variables** (`.env.local`):
   ```bash
   NEXT_PUBLIC_SUPABASE_URL=your-project-url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
   NEXT_PUBLIC_SITE_URL=http://localhost:3000
   ```

2. **Auth Config** (`lib/auth.config.ts`):
   ```typescript
   redirects: {
     afterLogin: '/dashboard',  // ← Change to your dashboard path
     // ...
   }
   ```

3. **Apply Migrations**:
   - Run migrations in `supabase/migrations/`
   - Or use Supabase Dashboard

4. **Enable OAuth** (optional):
   - Configure Google OAuth in Supabase Dashboard
   - Add callback URL: `{SITE_URL}/auth/callback`

## Files Installed

```
app/
├── actions/auth.ts              # Server actions
└── auth/
    ├── callback/route.ts        # OAuth & email callback
    ├── login/page.tsx
    ├── signup/page.tsx
    ├── forgot-password/page.tsx
    ├── reset-password/page.tsx
    └── verify-email/page.tsx

components/auth/
├── LoginForm.tsx
├── SignupForm.tsx
├── ForgotPasswordForm.tsx
├── ResetPasswordForm.tsx
└── GoogleLoginButton.tsx

lib/
├── auth.config.ts               # Auth configuration
├── env.ts                       # Environment validation
└── supabase/
    ├── client.ts                # Browser client
    ├── server.ts                # Server client
    └── middleware.ts            # Route protection

middleware.ts                    # Next.js middleware

supabase/migrations/
└── fix_function_search_path.sql # Security patch
```

## Dependencies Required

```bash
npm install @supabase/supabase-js @supabase/ssr
npm install lucide-react          # Icons
```

shadcn/ui components needed:
- button
- input
- label
- card

## Security Notes

✅ PKCE flow enabled for OAuth
✅ RLS policies protect user data
✅ SQL injection protection on all functions
✅ Token validation with error handling
✅ Environment variables validated on startup

## Customization

**Change redirect paths**: Edit `lib/auth.config.ts`
**Change profile fields**: Edit `app/actions/auth.ts` signup function
**Change UI text**: Edit component files in `components/auth/`
**Add i18n**: Extend `auth.config.ts` with text config

## Support

Issues? Check:
1. Environment variables are set correctly
2. Supabase project is configured
3. Migrations are applied
4. OAuth providers are enabled (if using)

## Version

Created: 2025-01-11
Compatible with:
- Next.js 15+
- React 19+
- Supabase (latest)
- shadcn/ui
