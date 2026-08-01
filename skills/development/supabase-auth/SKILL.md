---
name: supabase-auth
description: 'Apply when implementing authentication: sign up, sign in, OAuth providers,
  session management, and protected routes.'
---

---
name: supabase-auth
description: Apply when implementing authentication: sign up, sign in, OAuth providers, session management, and protected routes.
version: 1.1.0
tokens: ~750
confidence: high
sources:
  - https://supabase.com/docs/guides/auth
  - https://supabase.com/docs/reference/javascript/auth-signinwithpassword
  - https://supabase.com/docs/guides/auth/server-side/nextjs
last_validated: 2025-12-10
next_review: 2025-12-24
tags: [supabase, auth, authentication, security]
---

## When to Use

Apply when implementing authentication: sign up, sign in, OAuth providers, session management, and protected routes.

## Patterns

### Pattern 1: Email/Password Auth
```typescript
// Source: https://supabase.com/docs/reference/javascript/auth-signinwithpassword
// Sign up
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'securepassword',
  options: {
    data: { full_name: 'John Doe' }, // Custom user metadata
  },
});

// Sign in
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'securepassword',
});

// Sign out
await supabase.auth.signOut();
```

### Pattern 2: OAuth Provider
```typescript
// Source: https://supabase.com/docs/guides/auth/social-login
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google', // or 'github', 'discord', etc.
  options: {
    redirectTo: `${window.location.origin}/auth/callback`,
  },
});

// In /auth/callback/route.ts (Next.js)
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get('code');

  if (code) {
    const supabase = createServerClient();
    await supabase.auth.exchangeCodeForSession(code);
  }

  return NextResponse.redirect(new URL('/', request.url));
}
```

### Pattern 3: Auth State Hook
```typescript
// Source: https://supabase.com/docs/guides/auth
import { useEffect, useState } from 'react';
import { User } from '@supabase/supabase-js';

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
      setLoading(false);
    });

    // Listen for changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => setUser(session?.user ?? null)
    );

    return () => subscription.unsubscribe();
  }, []);

  return { user, loading };
}
```

### Pattern 4: Protected Route (Next.js Middleware) - @supabase/ssr
```typescript
// Source: https://supabase.com/docs/guides/auth/server-side/nextjs
// IMPORTANT: Use @supabase/ssr, NOT deprecated @supabase/auth-helpers-nextjs
// middleware.ts
import { createServerClient } from '@supabase/ssr';
import { NextResponse, type NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({ request });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) =>
            request.cookies.set(name, value)
          );
          response = NextResponse.next({ request });
          cookiesToSet.forEach(({ name, value, options }) =>
            response.cookies.set(name, value, options)
          );
        },
      },
    }
  );

  // CRITICAL: Use getUser() (not getSession()) in middleware for security
  const { data: { user } } = await supabase.auth.getUser();

  if (!user && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return response;
}

export const config = { matcher: ['/dashboard/:path*'] };
```

### Pattern 5: Password Reset
```typescript
// Source: https://supabase.com/docs/reference/javascript/auth-resetpasswordforemail
// Request reset
await supabase.auth.resetPasswordForEmail(email, {
  redirectTo: `${origin}/auth/reset-password`,
});

// Update password (after clicking email link)
await supabase.auth.updateUser({ password: newPassword });
```

## Anti-Patterns

- **Using deprecated @supabase/auth-helpers-nextjs** - Migrate to @supabase/ssr
- **Using getSession() in middleware** - Use getUser() for security
- **Storing password in state** - Clear after auth call
- **No loading state** - Show spinner during auth checks
- **Ignoring errors** - Always handle and display auth errors

## Verification Checklist

- [ ] Using @supabase/ssr (NOT auth-helpers-nextjs)
- [ ] Middleware uses getUser() (NOT getSession())
- [ ] onAuthStateChange listener with cleanup
- [ ] OAuth callback route configured
- [ ] Error messages shown to user
- [ ] Loading states during auth operations
