---
name: clerk
description: Auto-activates when user mentions Clerk, authentication, user management, or auth flows. Expert in Clerk authentication including Next.js integration, user management, and session handling.
category: auth
---

# Clerk Authentication Skill

Comprehensive guide for implementing Clerk authentication and user management in Next.js applications with App Router support.

## 1. Setup & Configuration

### Installation

```bash
# Install Clerk for Next.js
bun add @clerk/nextjs

# Install themes (optional)
bun add @clerk/themes
```

### Environment Variables

Create `.env.local` with your Clerk keys:

```bash
# Required - Get from Clerk Dashboard
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...

# Optional - Custom redirect URLs
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/onboarding
```

### Root Layout Setup (App Router)

✅ **Good: Proper ClerkProvider setup**

```typescript
// app/layout.tsx
import { ClerkProvider } from '@clerk/nextjs';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'My App',
  description: 'Secure app with Clerk',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  );
}
```

❌ **Bad: Missing ClerkProvider or incorrect placement**

```typescript
// app/layout.tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        {/* Missing ClerkProvider - auth won't work */}
        {children}
      </body>
    </html>
  );
}
```

### ClerkProvider with Localization

✅ **Good: Custom localization**

```typescript
// app/layout.tsx
import { ClerkProvider } from '@clerk/nextjs';
import { frFR } from '@clerk/localizations';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider localization={frFR}>
      <html lang="fr">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  );
}
```

### Middleware Configuration

Create `middleware.ts` in project root:

✅ **Good: Basic middleware setup**

```typescript
// middleware.ts
import { clerkMiddleware } from '@clerk/nextjs/server';

export default clerkMiddleware();

export const config = {
  matcher: [
    // Skip Next.js internals and static files
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    // Always run for API routes
    '/(api|trpc)(.*)',
  ],
};
```

✅ **Good: Middleware with public routes**

```typescript
// middleware.ts
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';

const isPublicRoute = createRouteMatcher([
  '/',
  '/sign-in(.*)',
  '/sign-up(.*)',
  '/api/webhooks(.*)',
]);

export default clerkMiddleware(async (auth, req) => {
  if (!isPublicRoute(req)) {
    await auth.protect();
  }
});

export const config = {
  matcher: [
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    '/(api|trpc)(.*)',
  ],
};
```

❌ **Bad: Missing matcher config**

```typescript
// middleware.ts
import { clerkMiddleware } from '@clerk/nextjs/server';

// Missing config.matcher - middleware won't run correctly
export default clerkMiddleware();
```

### Clerk Dashboard Configuration

1. **Sign-In Settings**:
   - Email address (required)
   - Phone number (optional)
   - Username (optional)

2. **Social Connections**:
   - Google OAuth
   - GitHub OAuth
   - Discord, LinkedIn, etc.

3. **Multi-Factor Authentication**:
   - SMS code
   - Authenticator app (TOTP)
   - Backup codes

4. **Session Configuration**:
   - Session lifetime: 7 days (default)
   - Inactive period: 10 minutes (default)

---

## 2. Authentication Methods

### Email/Password Authentication

✅ **Good: Using prebuilt components**

```typescript
// app/sign-up/[[...sign-up]]/page.tsx
import { SignUp } from '@clerk/nextjs';

export default function SignUpPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <SignUp />
    </div>
  );
}
```

```typescript
// app/sign-in/[[...sign-in]]/page.tsx
import { SignIn } from '@clerk/nextjs';

export default function SignInPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <SignIn />
    </div>
  );
}
```

✅ **Good: Custom email/password flow with Clerk Elements**

```typescript
'use client';

import { useSignUp } from '@clerk/nextjs';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function CustomSignUp() {
  const { isLoaded, signUp, setActive } = useSignUp();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [pendingVerification, setPendingVerification] = useState(false);
  const [code, setCode] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!isLoaded) return;

    try {
      await signUp.create({
        emailAddress: email,
        password,
      });

      // Send verification email
      await signUp.prepareEmailAddressVerification({
        strategy: 'email_code',
      });

      setPendingVerification(true);
    } catch (err: any) {
      console.error('Error:', JSON.stringify(err, null, 2));
    }
  };

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!isLoaded) return;

    try {
      const completeSignUp = await signUp.attemptEmailAddressVerification({
        code,
      });

      if (completeSignUp.status === 'complete') {
        await setActive({ session: completeSignUp.createdSessionId });
        router.push('/dashboard');
      }
    } catch (err: any) {
      console.error('Error:', JSON.stringify(err, null, 2));
    }
  };

  if (pendingVerification) {
    return (
      <form onSubmit={handleVerify}>
        <input
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Enter verification code"
        />
        <button type="submit">Verify Email</button>
      </form>
    );
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        type="email"
        placeholder="Email"
      />
      <input
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        type="password"
        placeholder="Password"
      />
      <button type="submit">Sign Up</button>
    </form>
  );
}
```

❌ **Bad: Weak password validation**

```typescript
// Don't rely on client-side only validation
const handleSubmit = async () => {
  if (password.length < 6) {
    alert('Password too short');
    return;
  }
  // Clerk handles strong password validation automatically
};
```

### OAuth Authentication (Social Login)

✅ **Good: Google OAuth setup**

```typescript
'use client';

import { useSignIn } from '@clerk/nextjs';

export default function OAuthButtons() {
  const { signIn, isLoaded } = useSignIn();

  if (!isLoaded) return null;

  const signInWithGoogle = () => {
    signIn.authenticateWithRedirect({
      strategy: 'oauth_google',
      redirectUrl: '/sso-callback',
      redirectUrlComplete: '/dashboard',
    });
  };

  const signInWithGitHub = () => {
    signIn.authenticateWithRedirect({
      strategy: 'oauth_github',
      redirectUrl: '/sso-callback',
      redirectUrlComplete: '/dashboard',
    });
  };

  return (
    <div>
      <button onClick={signInWithGoogle}>
        Continue with Google
      </button>
      <button onClick={signInWithGitHub}>
        Continue with GitHub
      </button>
    </div>
  );
}
```

✅ **Good: SSO callback handler**

```typescript
// app/sso-callback/page.tsx
'use client';

import { AuthenticateWithRedirectCallback } from '@clerk/nextjs';

export default function SSOCallback() {
  return <AuthenticateWithRedirectCallback />;
}
```

✅ **Good: OAuth with additional scopes**

```typescript
'use client';

import { useSignIn } from '@clerk/nextjs';

export default function GoogleCalendarAuth() {
  const { signIn } = useSignIn();

  const signInWithCalendar = () => {
    signIn?.authenticateWithRedirect({
      strategy: 'oauth_google',
      redirectUrl: '/sso-callback',
      redirectUrlComplete: '/calendar',
      additionalScopes: ['https://www.googleapis.com/auth/calendar'],
    });
  };

  return (
    <button onClick={signInWithCalendar}>
      Connect Google Calendar
    </button>
  );
}
```

### Magic Links (Passwordless)

✅ **Good: Email magic link authentication**

```typescript
'use client';

import { useSignIn } from '@clerk/nextjs';
import { useState } from 'react';

export default function MagicLinkSignIn() {
  const { signIn, isLoaded } = useSignIn();
  const [email, setEmail] = useState('');
  const [emailSent, setEmailSent] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!isLoaded) return;

    try {
      const result = await signIn.create({
        identifier: email,
      });

      const emailLink = result.supportedFirstFactors.find(
        (factor) => factor.strategy === 'email_link'
      );

      if (emailLink) {
        await signIn.prepareFirstFactor({
          strategy: 'email_link',
          emailAddressId: emailLink.emailAddressId,
          redirectUrl: '/verify-magic-link',
        });

        setEmailSent(true);
      }
    } catch (err) {
      console.error('Error:', err);
    }
  };

  if (emailSent) {
    return <p>Check your email for a magic link!</p>;
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Enter your email"
      />
      <button type="submit">Send Magic Link</button>
    </form>
  );
}
```

✅ **Good: Magic link verification page**

```typescript
// app/verify-magic-link/page.tsx
'use client';

import { useSignIn } from '@clerk/nextjs';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function VerifyMagicLink() {
  const { signIn, setActive } = useSignIn();
  const router = useRouter();

  useEffect(() => {
    const verify = async () => {
      try {
        const result = await signIn?.attemptFirstFactor({
          strategy: 'email_link',
        });

        if (result?.status === 'complete') {
          await setActive?.({ session: result.createdSessionId });
          router.push('/dashboard');
        }
      } catch (err) {
        console.error('Error verifying:', err);
      }
    };

    verify();
  }, [signIn, setActive, router]);

  return <div>Verifying your magic link...</div>;
}
```

### Phone (SMS) Authentication

✅ **Good: Phone number sign-up**

```typescript
'use client';

import { useSignUp } from '@clerk/nextjs';
import { useState } from 'react';

export default function PhoneSignUp() {
  const { signUp, isLoaded, setActive } = useSignUp();
  const [phone, setPhone] = useState('');
  const [code, setCode] = useState('');
  const [verifying, setVerifying] = useState(false);

  const handleSendCode = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!isLoaded) return;

    try {
      await signUp.create({
        phoneNumber: phone,
      });

      await signUp.preparePhoneNumberVerification();
      setVerifying(true);
    } catch (err) {
      console.error('Error:', err);
    }
  };

  const handleVerifyCode = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!isLoaded) return;

    try {
      const result = await signUp.attemptPhoneNumberVerification({
        code,
      });

      if (result.status === 'complete') {
        await setActive({ session: result.createdSessionId });
      }
    } catch (err) {
      console.error('Error:', err);
    }
  };

  if (verifying) {
    return (
      <form onSubmit={handleVerifyCode}>
        <input
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Enter SMS code"
        />
        <button type="submit">Verify</button>
      </form>
    );
  }

  return (
    <form onSubmit={handleSendCode}>
      <input
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
        placeholder="+1234567890"
      />
      <button type="submit">Send SMS Code</button>
    </form>
  );
}
```

### Multi-Factor Authentication (MFA)

✅ **Good: Enable MFA with TOTP**

```typescript
'use client';

import { useUser } from '@clerk/nextjs';
import { useState } from 'react';

export default function EnableMFA() {
  const { user } = useUser();
  const [qrCode, setQrCode] = useState('');
  const [code, setCode] = useState('');

  const startMFAEnrollment = async () => {
    try {
      const mfaFactor = await user?.createTOTP();
      setQrCode(mfaFactor?.uri || '');
    } catch (err) {
      console.error('Error creating TOTP:', err);
    }
  };

  const verifyMFA = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const totpFactor = user?.totpList?.[0];
      await totpFactor?.attemptVerification({ code });
    } catch (err) {
      console.error('Error verifying TOTP:', err);
    }
  };

  if (qrCode) {
    return (
      <div>
        <img src={qrCode} alt="QR Code" />
        <form onSubmit={verifyMFA}>
          <input
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="Enter code from authenticator app"
          />
          <button type="submit">Verify</button>
        </form>
      </div>
    );
  }

  return (
    <button onClick={startMFAEnrollment}>
      Enable Two-Factor Authentication
    </button>
  );
}
```

✅ **Good: MFA sign-in flow**

```typescript
'use client';

import { useSignIn } from '@clerk/nextjs';
import { useState } from 'react';

export default function MFASignIn() {
  const { signIn, isLoaded, setActive } = useSignIn();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [totpCode, setTotpCode] = useState('');
  const [needsTOTP, setNeedsTOTP] = useState(false);

  const handleFirstStep = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!isLoaded) return;

    try {
      const result = await signIn.create({
        identifier: email,
        password,
      });

      if (result.status === 'needs_second_factor') {
        setNeedsTOTP(true);
      } else if (result.status === 'complete') {
        await setActive({ session: result.createdSessionId });
      }
    } catch (err) {
      console.error('Error:', err);
    }
  };

  const handleTOTPVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!isLoaded) return;

    try {
      const result = await signIn.attemptSecondFactor({
        strategy: 'totp',
        code: totpCode,
      });

      if (result.status === 'complete') {
        await setActive({ session: result.createdSessionId });
      }
    } catch (err) {
      console.error('Error:', err);
    }
  };

  if (needsTOTP) {
    return (
      <form onSubmit={handleTOTPVerify}>
        <input
          value={totpCode}
          onChange={(e) => setTotpCode(e.target.value)}
          placeholder="6-digit code"
        />
        <button type="submit">Verify</button>
      </form>
    );
  }

  return (
    <form onSubmit={handleFirstStep}>
      <input
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        type="email"
        placeholder="Email"
      />
      <input
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        type="password"
        placeholder="Password"
      />
      <button type="submit">Sign In</button>
    </form>
  );
}
```

❌ **Bad: Storing MFA backup codes insecurely**

```typescript
// Don't store backup codes in localStorage or state
const backupCodes = user?.backupCodes;
localStorage.setItem('backupCodes', JSON.stringify(backupCodes)); // ❌ Insecure
```

---

## 3. User Management

### User Object Structure

Clerk's user object contains comprehensive user information:

```typescript
interface ClerkUser {
  id: string;
  firstName: string | null;
  lastName: string | null;
  fullName: string | null;
  username: string | null;
  primaryEmailAddress: EmailAddress | null;
  emailAddresses: EmailAddress[];
  primaryPhoneNumber: PhoneNumber | null;
  phoneNumbers: PhoneNumber[];
  profileImageUrl: string;
  imageUrl: string;
  hasImage: boolean;
  publicMetadata: Record<string, any>;
  privateMetadata: Record<string, any>;
  unsafeMetadata: Record<string, any>;
  externalAccounts: ExternalAccount[];
  createdAt: Date;
  updatedAt: Date;
  lastSignInAt: Date | null;
}
```

### Accessing User Data

✅ **Good: Client-side user access**

```typescript
'use client';

import { useUser } from '@clerk/nextjs';

export default function UserProfile() {
  const { isLoaded, isSignedIn, user } = useUser();

  if (!isLoaded) {
    return <div>Loading...</div>;
  }

  if (!isSignedIn) {
    return <div>Please sign in</div>;
  }

  return (
    <div>
      <img src={user.imageUrl} alt="Profile" />
      <h1>{user.fullName}</h1>
      <p>{user.primaryEmailAddress?.emailAddress}</p>
    </div>
  );
}
```

✅ **Good: Server-side user access**

```typescript
// app/dashboard/page.tsx
import { auth, currentUser } from '@clerk/nextjs/server';

export default async function DashboardPage() {
  const { userId } = await auth();
  const user = await currentUser();

  if (!userId) {
    return <div>Not authenticated</div>;
  }

  return (
    <div>
      <h1>Welcome, {user?.firstName}!</h1>
      <p>User ID: {userId}</p>
    </div>
  );
}
```

### Public Metadata vs Private Metadata

✅ **Good: Metadata organization**

```typescript
// Public metadata - accessible on frontend, in session token
type PublicMetadata = {
  role: 'admin' | 'user' | 'moderator';
  subscriptionTier: 'free' | 'pro' | 'enterprise';
  onboardingComplete: boolean;
};

// Private metadata - backend only, sensitive data
type PrivateMetadata = {
  stripeCustomerId: string;
  internalNotes: string;
  lastPaymentDate: string;
};

// Unsafe metadata - read/write on frontend (use sparingly)
type UnsafeMetadata = {
  theme: 'light' | 'dark';
  notificationPreferences: {
    email: boolean;
    push: boolean;
  };
};
```

✅ **Good: Setting metadata (backend)**

```typescript
// app/api/users/[userId]/route.ts
import { clerkClient } from '@clerk/nextjs/server';
import { NextRequest, NextResponse } from 'next/server';

export async function PATCH(
  req: NextRequest,
  { params }: { params: { userId: string } }
) {
  const { role } = await req.json();

  await clerkClient().users.updateUser(params.userId, {
    publicMetadata: {
      role,
    },
  });

  return NextResponse.json({ success: true });
}
```

✅ **Good: Updating unsafe metadata (client-side)**

```typescript
'use client';

import { useUser } from '@clerk/nextjs';

export default function ThemeToggle() {
  const { user } = useUser();

  const toggleTheme = async () => {
    const currentTheme = user?.unsafeMetadata?.theme || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';

    await user?.update({
      unsafeMetadata: {
        ...user.unsafeMetadata,
        theme: newTheme,
      },
    });
  };

  return (
    <button onClick={toggleTheme}>
      Toggle Theme
    </button>
  );
}
```

❌ **Bad: Storing sensitive data in public metadata**

```typescript
// ❌ Don't expose sensitive data in publicMetadata
await clerkClient().users.updateUser(userId, {
  publicMetadata: {
    creditCardNumber: '4242424242424242', // ❌ Exposed in session token!
    ssn: '123-45-6789', // ❌ Never store PII here
  },
});

// ✅ Use privateMetadata instead
await clerkClient().users.updateUser(userId, {
  privateMetadata: {
    stripePaymentMethodId: 'pm_123',
    encryptedSSN: encryptSSN('123-45-6789'),
  },
});
```

### User Profile Updates

✅ **Good: Updating user profile**

```typescript
'use client';

import { useUser } from '@clerk/nextjs';
import { useState } from 'react';

export default function EditProfile() {
  const { user } = useUser();
  const [firstName, setFirstName] = useState(user?.firstName || '');
  const [lastName, setLastName] = useState(user?.lastName || '');

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await user?.update({
        firstName,
        lastName,
      });
      alert('Profile updated!');
    } catch (err) {
      console.error('Error updating profile:', err);
    }
  };

  return (
    <form onSubmit={handleUpdate}>
      <input
        value={firstName}
        onChange={(e) => setFirstName(e.target.value)}
        placeholder="First Name"
      />
      <input
        value={lastName}
        onChange={(e) => setLastName(e.target.value)}
        placeholder="Last Name"
      />
      <button type="submit">Update Profile</button>
    </form>
  );
}
```

✅ **Good: Uploading profile image**

```typescript
'use client';

import { useUser } from '@clerk/nextjs';

export default function ProfileImageUpload() {
  const { user } = useUser();

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      await user?.setProfileImage({ file });
      alert('Profile image updated!');
    } catch (err) {
      console.error('Error uploading image:', err);
    }
  };

  return (
    <div>
      <img src={user?.imageUrl} alt="Profile" />
      <input
        type="file"
        accept="image/*"
        onChange={handleImageUpload}
      />
    </div>
  );
}
```

### User Deletion

✅ **Good: User account deletion**

```typescript
'use client';

import { useUser } from '@clerk/nextjs';
import { useRouter } from 'next/navigation';

export default function DeleteAccount() {
  const { user } = useUser();
  const router = useRouter();

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete your account?')) {
      return;
    }

    try {
      await user?.delete();
      router.push('/');
    } catch (err) {
      console.error('Error deleting account:', err);
    }
  };

  return (
    <button onClick={handleDelete} className="text-red-600">
      Delete Account
    </button>
  );
}
```

✅ **Good: Backend user deletion (admin)**

```typescript
// app/api/admin/users/[userId]/route.ts
import { clerkClient } from '@clerk/nextjs/server';
import { NextResponse } from 'next/server';
import { auth } from '@clerk/nextjs/server';

export async function DELETE(
  req: Request,
  { params }: { params: { userId: string } }
) {
  const { userId: adminId } = await auth();
  
  if (!adminId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Check if admin (from publicMetadata)
  const admin = await clerkClient().users.getUser(adminId);
  if (admin.publicMetadata.role !== 'admin') {
    return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
  }

  await clerkClient().users.deleteUser(params.userId);
  
  return NextResponse.json({ success: true });
}
```

---

## 4. Middleware & Route Protection

### Basic Middleware Setup

✅ **Good: Default protection with public routes**

```typescript
// middleware.ts
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';

const isPublicRoute = createRouteMatcher([
  '/',
  '/sign-in(.*)',
  '/sign-up(.*)',
  '/about',
  '/contact',
  '/api/webhooks(.*)',
]);

export default clerkMiddleware(async (auth, req) => {
  if (!isPublicRoute(req)) {
    await auth.protect();
  }
});

export const config = {
  matcher: [
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    '/(api|trpc)(.*)',
  ],
};
```

### Role-Based Access Control (RBAC)

✅ **Good: Protect routes by role**

```typescript
// middleware.ts
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';

const isPublicRoute = createRouteMatcher(['/sign-in(.*)', '/sign-up(.*)']);
const isAdminRoute = createRouteMatcher(['/admin(.*)']);
const isModeratorRoute = createRouteMatcher(['/moderator(.*)']);

export default clerkMiddleware(async (auth, req) => {
  const { userId, sessionClaims } = await auth();

  if (isPublicRoute(req)) {
    return;
  }

  if (!userId) {
    return auth.redirectToSignIn();
  }

  const role = sessionClaims?.metadata?.role as string;

  if (isAdminRoute(req) && role !== 'admin') {
    return Response.redirect(new URL('/403', req.url));
  }

  if (isModeratorRoute(req) && !['admin', 'moderator'].includes(role)) {
    return Response.redirect(new URL('/403', req.url));
  }
});
```

✅ **Good: Custom session claims for RBAC**

Configure in Clerk Dashboard → Sessions → Customize session token:

```json
{
  "metadata": {
    "role": "{{user.public_metadata.role}}",
    "orgRole": "{{org.role}}"
  }
}
```

### Server-Side Route Protection

✅ **Good: Using auth().protect() in Server Components**

```typescript
// app/dashboard/page.tsx
import { auth } from '@clerk/nextjs/server';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const { userId } = await auth.protect();

  // User is guaranteed to be authenticated here
  return <div>Dashboard for user: {userId}</div>;
}
```

✅ **Good: Conditional protection with role check**

```typescript
// app/admin/page.tsx
import { auth } from '@clerk/nextjs/server';

export default async function AdminPage() {
  const { userId, sessionClaims } = await auth.protect((has) => {
    return has({ role: 'admin' });
  });

  return <div>Admin Dashboard</div>;
}
```

✅ **Good: Organization-based protection**

```typescript
// app/org/[orgId]/settings/page.tsx
import { auth } from '@clerk/nextjs/server';

export default async function OrgSettingsPage({
  params,
}: {
  params: { orgId: string };
}) {
  await auth.protect((has) => {
    return (
      has({ permission: 'org:settings:manage' }) ||
      has({ role: 'org:admin' })
    );
  });

  return <div>Organization Settings</div>;
}
```

### Redirect Patterns

✅ **Good: Custom redirects after authentication**

```typescript
// app/sign-in/[[...sign-in]]/page.tsx
import { SignIn } from '@clerk/nextjs';

export default function SignInPage() {
  return (
    <SignIn
      afterSignInUrl="/dashboard"
      redirectUrl="/dashboard"
    />
  );
}
```

✅ **Good: Conditional redirects based on metadata**

```typescript
// middleware.ts
import { clerkMiddleware } from '@clerk/nextjs/server';
import { NextResponse } from 'next/server';

export default clerkMiddleware(async (auth, req) => {
  const { userId, sessionClaims } = await auth();

  if (userId && req.nextUrl.pathname === '/sign-in') {
    const onboardingComplete = sessionClaims?.metadata?.onboardingComplete;
    
    if (!onboardingComplete) {
      return NextResponse.redirect(new URL('/onboarding', req.url));
    }
    
    return NextResponse.redirect(new URL('/dashboard', req.url));
  }
});
```

### beforeAuth and afterAuth Patterns

✅ **Good: Rate limiting before auth**

```typescript
// middleware.ts
import { clerkMiddleware } from '@clerk/nextjs/server';
import { NextResponse } from 'next/server';

export default clerkMiddleware(async (auth, req) => {
  // beforeAuth: Run logic before authentication
  const ip = req.headers.get('x-forwarded-for') || 'unknown';
  const isRateLimited = await checkRateLimit(ip);

  if (isRateLimited) {
    return NextResponse.json(
      { error: 'Too many requests' },
      { status: 429 }
    );
  }

  // Authentication happens here
  const { userId } = await auth();

  // afterAuth: Run logic after authentication
  if (userId) {
    await trackUserActivity(userId, req.url);
  }

  return NextResponse.next();
});

async function checkRateLimit(ip: string): Promise<boolean> {
  // Implement rate limiting logic
  return false;
}

async function trackUserActivity(userId: string, url: string) {
  // Track user activity
}
```

❌ **Bad: Missing route protection**

```typescript
// app/dashboard/page.tsx
export default function DashboardPage() {
  // ❌ No auth check - anyone can access
  return <div>Secret dashboard data</div>;
}
```

❌ **Bad: Client-only protection**

```typescript
'use client';

import { useUser } from '@clerk/nextjs';
import { useRouter } from 'next/navigation';

export default function ProtectedPage() {
  const { isSignedIn } = useUser();
  const router = useRouter();

  // ❌ Client-side only - can be bypassed
  if (!isSignedIn) {
    router.push('/sign-in');
    return null;
  }

  return <div>Protected content</div>;
}
// ✅ Always use middleware or server-side auth checks
```

---

## 5. Session Management

### Session Tokens (JWT)

Clerk generates short-lived JWT tokens for each authenticated session.

**Default Claims:**

```typescript
interface SessionClaims {
  azp: string;           // Authorized party (origin)
  exp: number;           // Expiration time
  iat: number;           // Issued at
  iss: string;           // Issuer (Clerk)
  nbf: number;           // Not before
  sid: string;           // Session ID
  sub: string;           // User ID
}
```

### Server-Side Session Access

✅ **Good: Getting session info**

```typescript
// app/api/me/route.ts
import { auth } from '@clerk/nextjs/server';
import { NextResponse } from 'next/server';

export async function GET() {
  const { userId, sessionId, sessionClaims } = await auth();

  if (!userId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  return NextResponse.json({
    userId,
    sessionId,
    claims: sessionClaims,
  });
}
```

✅ **Good: Getting session token**

```typescript
// app/api/external/route.ts
import { auth } from '@clerk/nextjs/server';

export async function GET() {
  const { getToken } = await auth();
  
  const token = await getToken();

  // Use token to authenticate with external API
  const response = await fetch('https://api.example.com/data', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return Response.json(await response.json());
}
```

### Client-Side Session Hooks

✅ **Good: useAuth hook**

```typescript
'use client';

import { useAuth } from '@clerk/nextjs';

export default function SessionInfo() {
  const {
    isLoaded,
    userId,
    sessionId,
    getToken,
    signOut,
  } = useAuth();

  if (!isLoaded) {
    return <div>Loading...</div>;
  }

  const handleAPICall = async () => {
    const token = await getToken();
    
    const response = await fetch('/api/protected', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  };

  return (
    <div>
      <p>User ID: {userId}</p>
      <p>Session ID: {sessionId}</p>
      <button onClick={() => signOut()}>Sign Out</button>
      <button onClick={handleAPICall}>Call API</button>
    </div>
  );
}
```

✅ **Good: useSession hook**

```typescript
'use client';

import { useSession } from '@clerk/nextjs';

export default function SessionDetails() {
  const { session, isLoaded } = useSession();

  if (!isLoaded) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <p>Session ID: {session?.id}</p>
      <p>Created: {session?.createdAt.toLocaleString()}</p>
      <p>Last Active: {session?.lastActiveAt.toLocaleString()}</p>
      <p>Expires: {session?.expireAt.toLocaleString()}</p>
    </div>
  );
}
```

### Session Customization (Custom Claims)

✅ **Good: Adding custom claims to session token**

Configure in Clerk Dashboard → Sessions → Customize session token:

```json
{
  "role": "{{user.public_metadata.role}}",
  "subscription": "{{user.public_metadata.subscriptionTier}}",
  "orgId": "{{org.id}}",
  "orgRole": "{{org_membership.role}}",
  "permissions": "{{org_membership.permissions}}"
}
```

✅ **Good: Accessing custom claims**

```typescript
// app/api/admin/route.ts
import { auth } from '@clerk/nextjs/server';
import { NextResponse } from 'next/server';

export async function GET() {
  const { sessionClaims } = await auth();

  const role = sessionClaims?.role as string;
  const subscription = sessionClaims?.subscription as string;

  if (role !== 'admin') {
    return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
  }

  return NextResponse.json({
    message: 'Admin access granted',
    subscription,
  });
}
```

### Session Lifecycle

✅ **Good: Manual session refresh**

```typescript
'use client';

import { useSession } from '@clerk/nextjs';

export default function RefreshSession() {
  const { session } = useSession();

  const handleRefresh = async () => {
    // Force refresh session token
    await session?.getToken({ skipCache: true });
  };

  return (
    <button onClick={handleRefresh}>
      Refresh Session
    </button>
  );
}
```

✅ **Good: Sign out with redirect**

```typescript
'use client';

import { useClerk } from '@clerk/nextjs';

export default function SignOutButton() {
  const { signOut } = useClerk();

  return (
    <button onClick={() => signOut({ redirectUrl: '/' })}>
      Sign Out
    </button>
  );
}
```

❌ **Bad: Caching tokens too long**

```typescript
// ❌ Don't cache tokens indefinitely
const token = await getToken();
localStorage.setItem('token', token); // Tokens expire!

// ✅ Always get fresh tokens
const token = await getToken();
```

---

## 6. Organizations

Organizations enable B2B multi-tenancy, allowing users to collaborate in teams.

### Creating Organizations

✅ **Good: Using prebuilt component**

```typescript
// app/create-organization/page.tsx
import { CreateOrganization } from '@clerk/nextjs';

export default function CreateOrgPage() {
  return (
    <div>
      <h1>Create Your Organization</h1>
      <CreateOrganization afterCreateOrganizationUrl="/org/:id" />
    </div>
  );
}
```

✅ **Good: Programmatic organization creation**

```typescript
'use client';

import { useOrganizationList } from '@clerk/nextjs';
import { useState } from 'react';

export default function CreateOrgForm() {
  const { createOrganization } = useOrganizationList();
  const [name, setName] = useState('');

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const org = await createOrganization?.({ name });
      console.log('Created org:', org);
    } catch (err) {
      console.error('Error creating org:', err);
    }
  };

  return (
    <form onSubmit={handleCreate}>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Organization name"
      />
      <button type="submit">Create Organization</button>
    </form>
  );
}
```

### Organization Roles and Permissions

Default roles:
- `org:admin` - Full organization access
- `org:member` - Basic member access

✅ **Good: Custom organization roles**

Configure in Clerk Dashboard → Organizations → Roles:

```json
{
  "roles": [
    {
      "key": "org:admin",
      "name": "Admin",
      "permissions": ["org:manage", "org:delete", "org:members:manage"]
    },
    {
      "key": "org:billing_manager",
      "name": "Billing Manager",
      "permissions": ["org:billing:manage"]
    },
    {
      "key": "org:member",
      "name": "Member",
      "permissions": ["org:read"]
    }
  ]
}
```

✅ **Good: Checking organization permissions**

```typescript
// app/org/[orgId]/settings/page.tsx
import { auth } from '@clerk/nextjs/server';

export default async function OrgSettingsPage() {
  const { has } = await auth();

  const canManageSettings = has?.({ permission: 'org:manage' });
  const canManageMembers = has?.({ permission: 'org:members:manage' });

  if (!canManageSettings) {
    return <div>Access denied</div>;
  }

  return (
    <div>
      <h1>Organization Settings</h1>
      {canManageMembers && (
        <section>
          <h2>Members</h2>
          {/* Member management UI */}
        </section>
      )}
    </div>
  );
}
```

### Organization Invitations

✅ **Good: Inviting members**

```typescript
'use client';

import { useOrganization } from '@clerk/nextjs';
import { useState } from 'react';

export default function InviteMember() {
  const { organization } = useOrganization();
  const [email, setEmail] = useState('');
  const [role, setRole] = useState<'org:admin' | 'org:member'>('org:member');

  const handleInvite = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await organization?.inviteMember({
        emailAddress: email,
        role,
      });
      alert(`Invited ${email} as ${role}`);
      setEmail('');
    } catch (err) {
      console.error('Error inviting member:', err);
    }
  };

  return (
    <form onSubmit={handleInvite}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email address"
      />
      <select value={role} onChange={(e) => setRole(e.target.value as any)}>
        <option value="org:member">Member</option>
        <option value="org:admin">Admin</option>
      </select>
      <button type="submit">Send Invitation</button>
    </form>
  );
}
```

✅ **Good: Managing invitations**

```typescript
'use client';

import { useOrganization } from '@clerk/nextjs';

export default function PendingInvitations() {
  const { organization, invitationList } = useOrganization({
    invitationList: {},
  });

  const revokeInvitation = async (invitationId: string) => {
    try {
      await organization?.revokeInvitation(invitationId);
    } catch (err) {
      console.error('Error revoking invitation:', err);
    }
  };

  return (
    <ul>
      {invitationList?.data?.map((invitation) => (
        <li key={invitation.id}>
          {invitation.emailAddress} - {invitation.role}
          <button onClick={() => revokeInvitation(invitation.id)}>
            Revoke
          </button>
        </li>
      ))}
    </ul>
  );
}
```

### Organization Switching

✅ **Good: Organization switcher component**

```typescript
// app/components/OrgSwitcher.tsx
import { OrganizationSwitcher } from '@clerk/nextjs';

export default function OrgSwitcher() {
  return (
    <OrganizationSwitcher
      afterCreateOrganizationUrl="/org/:id"
      afterSelectOrganizationUrl="/org/:id"
      afterSelectPersonalUrl="/dashboard"
    />
  );
}
```

✅ **Good: Programmatic organization switching**

```typescript
'use client';

import { useOrganizationList } from '@clerk/nextjs';

export default function OrgList() {
  const { setActive, userMemberships } = useOrganizationList({
    userMemberships: {
      infinite: true,
    },
  });

  const switchOrg = async (orgId: string) => {
    await setActive?.({ organization: orgId });
  };

  return (
    <ul>
      {userMemberships.data?.map((membership) => (
        <li key={membership.organization.id}>
          <button onClick={() => switchOrg(membership.organization.id)}>
            {membership.organization.name}
          </button>
        </li>
      ))}
    </ul>
  );
}
```

### Organization Metadata

✅ **Good: Setting organization metadata**

```typescript
// app/api/organizations/[orgId]/route.ts
import { clerkClient } from '@clerk/nextjs/server';
import { NextRequest, NextResponse } from 'next/server';

export async function PATCH(
  req: NextRequest,
  { params }: { params: { orgId: string } }
) {
  const { subscriptionTier, features } = await req.json();

  await clerkClient().organizations.updateOrganization(params.orgId, {
    publicMetadata: {
      subscriptionTier,
      features,
    },
  });

  return NextResponse.json({ success: true });
}
```

❌ **Bad: Not checking organization membership**

```typescript
// ❌ Anyone can access organization data
export default async function OrgDashboard({
  params,
}: {
  params: { orgId: string };
}) {
  // No membership check!
  return <div>Org: {params.orgId}</div>;
}

// ✅ Always verify membership
export default async function OrgDashboard({
  params,
}: {
  params: { orgId: string };
}) {
  const { orgId } = await auth();
  
  if (orgId !== params.orgId) {
    return <div>Access denied</div>;
  }
  
  return <div>Org: {params.orgId}</div>;
}
```

---

## 7. Webhooks

Clerk webhooks notify your application of events (user creation, updates, deletions, etc.).

### Webhook Events

Common events:
- `user.created`
- `user.updated`
- `user.deleted`
- `session.created`
- `session.ended`
- `organization.created`
- `organization.updated`
- `organizationMembership.created`
- `organizationMembership.deleted`

### Webhook Setup

1. **Configure endpoint** in Clerk Dashboard → Webhooks
2. **Add endpoint URL**: `https://yourdomain.com/api/webhooks/clerk`
3. **Subscribe to events**: Select events to receive
4. **Copy signing secret**: `whsec_...`

### Webhook Handler

✅ **Good: Svix signature verification**

```typescript
// app/api/webhooks/clerk/route.ts
import { Webhook } from 'svix';
import { headers } from 'next/headers';
import { WebhookEvent } from '@clerk/nextjs/server';

export async function POST(req: Request) {
  const WEBHOOK_SECRET = process.env.CLERK_WEBHOOK_SECRET;

  if (!WEBHOOK_SECRET) {
    throw new Error('CLERK_WEBHOOK_SECRET is not set');
  }

  // Get headers
  const headerPayload = await headers();
  const svix_id = headerPayload.get('svix-id');
  const svix_timestamp = headerPayload.get('svix-timestamp');
  const svix_signature = headerPayload.get('svix-signature');

  if (!svix_id || !svix_timestamp || !svix_signature) {
    return new Response('Missing svix headers', { status: 400 });
  }

  // Get body
  const payload = await req.json();
  const body = JSON.stringify(payload);

  // Verify webhook
  const wh = new Webhook(WEBHOOK_SECRET);
  let evt: WebhookEvent;

  try {
    evt = wh.verify(body, {
      'svix-id': svix_id,
      'svix-timestamp': svix_timestamp,
      'svix-signature': svix_signature,
    }) as WebhookEvent;
  } catch (err) {
    console.error('Webhook verification failed:', err);
    return new Response('Verification failed', { status: 400 });
  }

  // Handle event
  const { id } = evt.data;
  const eventType = evt.type;

  console.log(`Webhook ${eventType} for ${id}`);

  return new Response('Webhook received', { status: 200 });
}
```

### Syncing Users to Database

✅ **Good: User created webhook**

```typescript
// app/api/webhooks/clerk/route.ts
import { Webhook } from 'svix';
import { headers } from 'next/headers';
import { WebhookEvent } from '@clerk/nextjs/server';
import { db } from '@/lib/db';

export async function POST(req: Request) {
  const WEBHOOK_SECRET = process.env.CLERK_WEBHOOK_SECRET!;
  const headerPayload = await headers();
  const svix_id = headerPayload.get('svix-id')!;
  const svix_timestamp = headerPayload.get('svix-timestamp')!;
  const svix_signature = headerPayload.get('svix-signature')!;

  const payload = await req.json();
  const body = JSON.stringify(payload);

  const wh = new Webhook(WEBHOOK_SECRET);
  const evt = wh.verify(body, {
    'svix-id': svix_id,
    'svix-timestamp': svix_timestamp,
    'svix-signature': svix_signature,
  }) as WebhookEvent;

  switch (evt.type) {
    case 'user.created':
      await db.user.create({
        data: {
          clerkId: evt.data.id,
          email: evt.data.email_addresses[0]?.email_address,
          firstName: evt.data.first_name,
          lastName: evt.data.last_name,
          imageUrl: evt.data.image_url,
        },
      });
      break;

    case 'user.updated':
      await db.user.update({
        where: { clerkId: evt.data.id },
        data: {
          email: evt.data.email_addresses[0]?.email_address,
          firstName: evt.data.first_name,
          lastName: evt.data.last_name,
          imageUrl: evt.data.image_url,
        },
      });
      break;

    case 'user.deleted':
      await db.user.delete({
        where: { clerkId: evt.data.id! },
      });
      break;
  }

  return new Response('Webhook processed', { status: 200 });
}
```

✅ **Good: Organization webhooks**

```typescript
switch (evt.type) {
  case 'organization.created':
    await db.organization.create({
      data: {
        clerkId: evt.data.id,
        name: evt.data.name,
        slug: evt.data.slug,
        imageUrl: evt.data.image_url,
      },
    });
    break;

  case 'organizationMembership.created':
    await db.organizationMember.create({
      data: {
        organizationId: evt.data.organization.id,
        userId: evt.data.public_user_data.user_id,
        role: evt.data.role,
      },
    });
    break;

  case 'organizationMembership.deleted':
    await db.organizationMember.delete({
      where: {
        organizationId_userId: {
          organizationId: evt.data.organization.id,
          userId: evt.data.public_user_data.user_id,
        },
      },
    });
    break;
}
```

❌ **Bad: No webhook verification**

```typescript
// ❌ DANGEROUS: No signature verification
export async function POST(req: Request) {
  const payload = await req.json();
  
  // Anyone can send fake webhooks!
  await db.user.create({ data: payload.data });
  
  return new Response('OK');
}

// ✅ Always verify with Svix
```

❌ **Bad: Blocking webhook processing**

```typescript
// ❌ Long-running operations block webhook
export async function POST(req: Request) {
  // Verify webhook...
  
  // This takes too long - webhook will timeout
  await sendWelcomeEmail(evt.data.id);
  await generateReport(evt.data.id);
  await updateAnalytics(evt.data.id);
  
  return new Response('OK');
}

// ✅ Queue background jobs instead
export async function POST(req: Request) {
  // Verify webhook...
  
  // Queue jobs for async processing
  await queue.add('welcome-email', { userId: evt.data.id });
  
  return new Response('OK', { status: 200 });
}
```

---

## 8. UI Components

Clerk provides prebuilt components for rapid integration.

### SignIn Component

```typescript
import { SignIn } from '@clerk/nextjs';

export default function SignInPage() {
  return <SignIn />;
}
```

### SignUp Component

```typescript
import { SignUp } from '@clerk/nextjs';

export default function SignUpPage() {
  return <SignUp />;
}
```

### UserButton Component

```typescript
import { UserButton } from '@clerk/nextjs';

export default function Header() {
  return (
    <header>
      <nav>
        <UserButton afterSignOutUrl="/" />
      </nav>
    </header>
  );
}
```

### Component Customization

✅ **Good: Custom appearance**

```typescript
import { SignIn } from '@clerk/nextjs';

export default function CustomSignIn() {
  return (
    <SignIn
      appearance={{
        elements: {
          formButtonPrimary: 'bg-blue-600 hover:bg-blue-700',
          card: 'shadow-lg',
          headerTitle: 'text-2xl font-bold',
        },
        variables: {
          colorPrimary: '#3b82f6',
          colorText: '#1f2937',
        },
      }}
    />
  );
}
```

✅ **Good: Using themes**

```typescript
import { SignIn } from '@clerk/nextjs';
import { dark } from '@clerk/themes';

export default function ThemedSignIn() {
  return (
    <SignIn
      appearance={{
        baseTheme: dark,
      }}
    />
  );
}
```

✅ **Good: UserButton with custom menu items**

```typescript
import { UserButton } from '@clerk/nextjs';

export default function Header() {
  return (
    <UserButton>
      <UserButton.MenuItems>
        <UserButton.Link
          label="Dashboard"
          labelIcon={<DashboardIcon />}
          href="/dashboard"
        />
        <UserButton.Link
          label="Settings"
          labelIcon={<SettingsIcon />}
          href="/settings"
        />
      </UserButton.MenuItems>
    </UserButton>
  );
}
```

❌ **Bad: Hardcoding theme in layout**

```typescript
// ❌ Won't respond to theme changes
export default function Layout() {
  return (
    <ClerkProvider
      appearance={{
        baseTheme: dark, // Fixed to dark mode
      }}
    >
      {children}
    </ClerkProvider>
  );
}

// ✅ Apply theme at component level
'use client';
import { useTheme } from 'next-themes';
import { SignIn } from '@clerk/nextjs';
import { dark } from '@clerk/themes';

export default function ThemedSignIn() {
  const { theme } = useTheme();
  
  return (
    <SignIn
      appearance={{
        baseTheme: theme === 'dark' ? dark : undefined,
      }}
    />
  );
}
```

---

## Best Practices

### Environment Variables Security

✅ **Good: Use environment variables**

```bash
# .env.local
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_...
CLERK_SECRET_KEY=sk_live_...
CLERK_WEBHOOK_SECRET=whsec_...
```

❌ **Bad: Hardcoding keys**

```typescript
// ❌ Never hardcode keys
const clerkPublishableKey = 'pk_live_abc123...';
```

### TypeScript Types

✅ **Good: Type safety with custom metadata**

```typescript
// types/clerk.ts
declare global {
  interface CustomJwtSessionClaims {
    metadata: {
      role?: 'admin' | 'user' | 'moderator';
      onboardingComplete?: boolean;
    };
  }
}

export interface UserPublicMetadata {
  role: 'admin' | 'user' | 'moderator';
  subscriptionTier: 'free' | 'pro' | 'enterprise';
}

export interface UserPrivateMetadata {
  stripeCustomerId: string;
}
```

### Performance Optimization

✅ **Good: Selective data fetching**

```typescript
'use client';

import { useOrganization } from '@clerk/nextjs';

export default function OrgMembers() {
  // Only fetch what you need
  const { membershipList } = useOrganization({
    membershipList: {
      limit: 10,
      offset: 0,
    },
  });

  return (
    <ul>
      {membershipList?.data?.map((membership) => (
        <li key={membership.id}>
          {membership.publicUserData.firstName}
        </li>
      ))}
    </ul>
  );
}
```

### Error Handling

✅ **Good: Comprehensive error handling**

```typescript
'use client';

import { useSignIn } from '@clerk/nextjs';
import { isClerkAPIResponseError } from '@clerk/nextjs/errors';

export default function SignInForm() {
  const { signIn } = useSignIn();

  const handleSignIn = async (email: string, password: string) => {
    try {
      await signIn?.create({
        identifier: email,
        password,
      });
    } catch (err) {
      if (isClerkAPIResponseError(err)) {
        console.error('Clerk error:', err.errors);
        
        err.errors.forEach((error) => {
          if (error.code === 'form_password_incorrect') {
            alert('Incorrect password');
          }
        });
      }
    }
  };
}
```

---

## Summary

Clerk provides comprehensive authentication and user management for Next.js applications:

1. **Setup**: Install `@clerk/nextjs`, configure environment variables, wrap app with `ClerkProvider`
2. **Authentication**: Support for email/password, OAuth, magic links, SMS, and MFA
3. **User Management**: Rich user object with metadata (public/private/unsafe)
4. **Middleware**: Route protection with role-based access control
5. **Sessions**: JWT-based sessions with customizable claims
6. **Organizations**: B2B multi-tenancy with roles and permissions
7. **Webhooks**: Real-time event notifications with Svix verification
8. **UI Components**: Prebuilt, customizable components for rapid development

Use environment variables for all sensitive data, implement proper server-side protection, and leverage Clerk's comprehensive feature set for production-ready authentication.
