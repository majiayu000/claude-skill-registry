---
name: supabase-email-auth
description: This skill should be used when implementing Supabase email/password authentication in Next.js applications. Automates the complete setup including client/server utilities, login/register pages, auth callback handling, middleware protection, and email configuration. Handles common errors like PKCE flow issues, cookie management, and admin role verification.
---

# Supabase Email Authentication Setup Skill

## Purpose

This skill provides a complete, production-ready implementation of Supabase email/password authentication for Next.js 13+ applications using the App Router. It eliminates the repetitive 1-hour setup process and resolves common authentication errors by providing tested, working code patterns.

The skill includes:
- Client and server-side authentication utilities
- Login and registration pages with proper UI/UX
- OAuth callback handling with PKCE flow
- Password reset functionality
- Admin role-based access control
- Environment variable configuration
- Middleware for route protection

## When to Use This Skill

Use this skill when:
- Starting a new Next.js project that needs Supabase authentication
- Adding email/password auth to an existing Supabase-enabled project
- Migrating from another auth provider to Supabase
- Troubleshooting Supabase auth errors (PKCE, cookies, sessions)
- Implementing admin panels with role-based access
- Setting up password reset flows
- User asks to "implement Supabase auth" or "add login functionality"

## Prerequisites

Before using this skill, ensure:
1. A Supabase project is created at https://supabase.com
2. Next.js 13+ project with App Router (`app/` directory)
3. Dependencies installed:
   ```bash
   npm install @supabase/ssr @supabase/supabase-js
   npm install lucide-react  # For icons in UI
   ```

## Implementation Workflow

### Step 1: Environment Variables Setup

Create or update the `.env.local` file with Supabase credentials.

**Use the reference file:** `references/env-template.md` for the exact environment variable structure.

Key variables needed:
- `NEXT_PUBLIC_SUPABASE_URL` - Project URL from Supabase dashboard
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` - Anon/public key
- `SUPABASE_SERVICE_ROLE_KEY` - Service role key (keep secret!)
- `ADMIN_EMAILS` - Comma-separated list of admin emails (optional)

**Critical:** Never commit `.env.local` to version control. Add it to `.gitignore`.

### Step 2: Create Authentication Utilities

Create the core authentication utilities in the `lib/auth/` directory.

**Files to create:**

1. **`lib/auth/client.ts`** - Client-side auth functions
   - Use template from `references/client-auth-template.md`
   - Handles browser-based auth: sign in, sign up, password reset
   - Creates Supabase browser client using `@supabase/ssr`

2. **`lib/auth/server.ts`** - Server-side auth functions
   - Use template from `references/server-auth-template.md`
   - Handles server component auth checks
   - Implements admin role verification
   - Proper Next.js 13+ cookie handling with `next/headers`

3. **`lib/auth/api-protection.ts`** (Optional)
   - Use template from `references/api-protection-template.md`
   - Helper functions for protecting API routes
   - Validates authentication in API route handlers

4. **`lib/supabase-admin.ts`** - Admin client for bypassing RLS
   - Use template from `references/supabase-admin-template.md`
   - Creates service role client for admin operations
   - Required for checking user roles in database

### Step 3: Create Auth Callback Handler

The auth callback route handles OAuth redirects and PKCE flow completion.

**Create:** `app/auth/callback/route.ts`

**Use template from:** `references/auth-callback-template.md`

This route:
- Exchanges authorization code for session
- Handles PKCE code verifier from cookies
- Redirects to appropriate page based on user role
- Manages password recovery flow
- Validates admin email whitelist

**Critical implementation notes:**
- Must use `@supabase/ssr` `createServerClient` for cookie access
- Code verifier is automatically retrieved from cookies
- Error handling redirects to `/login?error=<error_type>`

### Step 4: Create Login Page

Create a full-featured login page with email/password auth.

**Create:** `app/login/page.tsx`

**Use template from:** `references/login-page-template.md`

Features:
- Email and password inputs with validation
- Error message display
- Loading states
- Auto-redirect if already logged in
- Admin vs regular user detection
- Handles redirect parameter for protected pages
- Optional Google OAuth integration (commented out by default)

**UI/UX considerations:**
- Show clear error messages
- Disable form during submission
- Validate email format client-side
- Minimum 6 character password requirement

### Step 5: Create Registration Page

Create a user registration page with full validation.

**Create:** `app/register/page.tsx`

**Use template from:** `references/register-page-template.md`

Features:
- Full name, email, password, and confirm password fields
- Client-side validation
- Password strength requirements
- Success screen with auto-redirect
- Email format validation
- Already registered error handling

**Note:** Registration creates accounts, but admin access requires email whitelist approval.

### Step 6: Create Password Reset Pages (Optional)

If password reset functionality is needed, create these pages:

1. **`app/forgot-password/page.tsx`**
   - Use template from `references/forgot-password-template.md`
   - Sends password reset email

2. **`app/update-password/page.tsx`**
   - Use template from `references/update-password-template.md`
   - Allows user to set new password after clicking email link

### Step 7: Supabase Dashboard Configuration

Configure Supabase settings in the dashboard:

1. **Email Auth Settings**
   - Navigate to Authentication > Providers > Email
   - Enable Email provider
   - Disable "Confirm email" if you don't want email verification
   - Set Site URL to your production URL
   - Add redirect URLs:
     - `http://localhost:3000/auth/callback` (development)
     - `https://yourdomain.com/auth/callback` (production)

2. **URL Configuration**
   - Go to Authentication > URL Configuration
   - Set Redirect URLs (important for OAuth and password reset):
     ```
     http://localhost:3000/auth/callback
     https://yourdomain.com/auth/callback
     ```

3. **Email Templates** (Optional)
   - Customize email templates in Authentication > Email Templates
   - Update password reset, confirmation emails

4. **Database Setup** (If using role-based auth)
   - Create `app_users` table with columns:
     - `id` (uuid, foreign key to auth.users)
     - `role` (text: 'admin' | 'user')
     - `status` (text: 'active' | 'inactive')
     - `created_at` (timestamp)
   - See `references/database-schema.md` for full schema

### Step 8: Protect Routes with Middleware (Optional)

To automatically redirect unauthenticated users, create middleware.

**Create:** `middleware.ts` (root level)

**Use template from:** `references/middleware-template.md`

Features:
- Automatic auth checking for protected routes
- Refresh session tokens
- Redirect to login with return URL
- Exclude public routes (login, register, etc.)

### Step 9: Testing the Implementation

Follow this testing checklist:

**Registration Flow:**
1. Navigate to `/register`
2. Enter email, password, full name
3. Submit form
4. Verify success message
5. Check Supabase dashboard > Authentication > Users for new user

**Login Flow:**
1. Navigate to `/login`
2. Enter registered email and password
3. Submit form
4. Verify redirect to `/directory` or `/admin-panel` based on role
5. Check that session persists on page refresh

**Password Reset Flow:**
1. Navigate to `/forgot-password`
2. Enter registered email
3. Check email inbox for reset link
4. Click link (should redirect to `/update-password`)
5. Enter new password
6. Verify login works with new password

**Admin Access:**
1. Add test email to `ADMIN_EMAILS` in `.env.local`
2. Login with admin email
3. Verify redirect to `/admin-panel`
4. Test API route protection with `isAdmin()` function

## Common Errors and Solutions

### PKCE Flow Errors

**Error:** "code_verifier not found" or "Invalid PKCE code"

**Solution:**
- Ensure using `@supabase/ssr` package
- Use `createBrowserClient` for client-side
- Use `createServerClient` with proper cookie config for server-side
- Verify callback route implements cookie handlers correctly
- Check that redirect URLs match exactly in Supabase dashboard

### Cookie Issues

**Error:** "Cookies can only be modified in a Server Action or Route Handler"

**Solution:**
- Only call `createServerClient` in Server Components, Route Handlers, or Server Actions
- Use `createBrowserClient` in Client Components
- Add `'use client'` directive to client components
- Wrap cookie operations in try-catch blocks

### Session Not Persisting

**Error:** User logged in but session lost on refresh

**Solution:**
- Verify callback route exchanges code properly
- Check browser cookies are enabled
- Ensure HTTPS in production (cookies may not work on HTTP)
- Verify `sameSite` cookie settings

### Admin Access Not Working

**Error:** Admin users can't access admin panel

**Solution:**
- Check `ADMIN_EMAILS` format (comma-separated, no spaces unless trimmed)
- Verify email matches exactly (case-sensitive)
- If using database roles, ensure `app_users` table exists
- Check `isAdmin()` function is called server-side only

### Email Not Sending

**Error:** Password reset or confirmation emails not arriving

**Solution:**
- Check Supabase email rate limits
- Verify SMTP settings if using custom SMTP
- Check spam folder
- Use Supabase dashboard to resend confirmation
- For production, configure custom SMTP in Supabase

## Customization Options

### OAuth Providers (Google, GitHub, etc.)

To add Google OAuth:
1. Enable Google provider in Supabase dashboard
2. Configure OAuth credentials (Client ID, Secret)
3. Uncomment Google sign-in code in `references/login-page-template.md`
4. Add `signInWithGoogle()` function import from `lib/auth/client.ts`

### Custom Role Systems

To extend beyond admin/user roles:
1. Create `app_users` table with role column
2. Modify `isAdmin()` to check specific roles
3. Create role-specific middleware helpers
4. Add role checks in protected routes

### Email Customization

Customize email templates in Supabase dashboard:
- Magic link templates
- Password reset templates
- Confirmation emails
- Add your branding

### UI Theming

The provided templates use a purple gradient theme. To customize:
- Update Tailwind classes in login/register pages
- Modify color schemes in templates
- Replace Lucide icons with your preferred icon library
- Adjust form layouts and spacing

## Advanced Features

### Session Management

**Refresh tokens automatically:**
- `@supabase/ssr` handles refresh automatically
- No manual refresh needed in most cases
- Tokens refresh on authenticated requests

**Manual session refresh:**
```typescript
const { data, error } = await supabase.auth.refreshSession();
```

**Sign out from all devices:**
```typescript
const { error } = await supabase.auth.signOut({ scope: 'global' });
```

### Multi-tenancy

For multi-tenant apps:
1. Add `organization_id` to `app_users` table
2. Filter queries by organization
3. Implement organization-based RLS policies
4. Add organization context to session

### Social Auth (Google, GitHub, etc.)

1. Enable provider in Supabase dashboard
2. Configure OAuth credentials
3. Add provider button to login page
4. Use `signInWithOAuth()` in client.ts
5. Handle callback in `app/auth/callback/route.ts`

## File Structure Reference

After implementation, your project structure should include:

```
your-project/
├── .env.local (environment variables)
├── middleware.ts (optional - route protection)
├── app/
│   ├── login/
│   │   └── page.tsx
│   ├── register/
│   │   └── page.tsx
│   ├── forgot-password/
│   │   └── page.tsx (optional)
│   ├── update-password/
│   │   └── page.tsx (optional)
│   └── auth/
│       └── callback/
│           └── route.ts
└── lib/
    ├── auth/
    │   ├── client.ts
    │   ├── server.ts
    │   └── api-protection.ts (optional)
    └── supabase-admin.ts
```

## Best Practices

1. **Security:**
   - Never expose service role key to client
   - Always validate on server-side
   - Use RLS policies in Supabase
   - Sanitize user inputs
   - Use HTTPS in production

2. **Error Handling:**
   - Show user-friendly error messages
   - Log detailed errors server-side
   - Handle all auth error cases
   - Provide clear next steps for users

3. **Performance:**
   - Cache admin status checks
   - Use Server Components for auth checks
   - Minimize client-side auth calls
   - Lazy load auth-related components

4. **User Experience:**
   - Show loading states
   - Provide clear feedback
   - Auto-redirect after actions
   - Remember redirect intentions
   - Clear error messages

5. **Testing:**
   - Test all auth flows
   - Test error cases
   - Test admin vs regular user paths
   - Test password reset
   - Test session persistence

## Quick Reference

**Sign up user:**
```typescript
import { signUpWithPassword } from '@/lib/auth/client';
const { data, error } = await signUpWithPassword(email, password, fullName);
```

**Sign in user:**
```typescript
import { signInWithPassword } from '@/lib/auth/client';
const { data, error } = await signInWithPassword(email, password);
```

**Get current user (client):**
```typescript
import { getUser } from '@/lib/auth/client';
const { user, error } = await getUser();
```

**Get current user (server):**
```typescript
import { getUser } from '@/lib/auth/server';
const { user, error } = await getUser();
```

**Check if admin (server):**
```typescript
import { isAdmin } from '@/lib/auth/server';
const admin = await isAdmin();
```

**Sign out:**
```typescript
import { signOut } from '@/lib/auth/client';
const { error } = await signOut();
```

**Reset password:**
```typescript
import { resetPassword } from '@/lib/auth/client';
const { data, error } = await resetPassword(email);
```

**Update password:**
```typescript
import { updatePassword } from '@/lib/auth/client';
const { data, error } = await updatePassword(newPassword);
```

## Support and Resources

- **Supabase Auth Docs:** https://supabase.com/docs/guides/auth
- **@supabase/ssr Docs:** https://supabase.com/docs/guides/auth/server-side/nextjs
- **Next.js App Router:** https://nextjs.org/docs/app
- **Common Issues:** Check `references/troubleshooting.md`
