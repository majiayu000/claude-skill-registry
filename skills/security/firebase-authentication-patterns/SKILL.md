---
name: firebase-authentication-patterns
description: |
  Firebase Authentication implementation patterns including sign-in/sign-up flows, OAuth providers,
  session management, protected routes, password reset, email verification, and error handling.
  Keywords: "auth", "authentication", "sign-in", "sign-up", "oauth", "session", "protected route"
---

# Firebase Authentication Patterns

## Overview

Firebase Authentication provides backend services for authenticating users with email/password, OAuth providers (Google, GitHub, etc.), and anonymous authentication.

## Authentication Providers

### Email/Password Authentication

**Sign Up**:
```typescript
import { createUserWithEmailAndPassword } from 'firebase/auth';
import { auth } from '@/lib/firebase/client';

export async function signUp(email: string, password: string, displayName: string) {
  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);

    // Update profile with display name
    await updateProfile(userCredential.user, { displayName });

    // Create user document in Firestore
    await setDoc(doc(db, 'users', userCredential.user.uid), {
      email,
      displayName,
      createdAt: serverTimestamp(),
      role: 'user',
    });

    return userCredential.user;
  } catch (error) {
    // Handle Firebase-specific errors
    if (error instanceof FirebaseError) {
      switch (error.code) {
        case 'auth/email-already-in-use':
          throw new Error('Email already registered');
        case 'auth/weak-password':
          throw new Error('Password must be at least 6 characters');
        case 'auth/invalid-email':
          throw new Error('Invalid email address');
        default:
          throw new Error('Sign up failed');
      }
    }
    throw error;
  }
}
```

**Sign In**:
```typescript
import { signInWithEmailAndPassword } from 'firebase/auth';

export async function signIn(email: string, password: string) {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    return userCredential.user;
  } catch (error) {
    if (error instanceof FirebaseError) {
      switch (error.code) {
        case 'auth/user-not-found':
        case 'auth/wrong-password':
          throw new Error('Invalid email or password');
        case 'auth/too-many-requests':
          throw new Error('Too many failed attempts. Try again later.');
        default:
          throw new Error('Sign in failed');
      }
    }
    throw error;
  }
}
```

### OAuth Authentication

**Google Sign-In**:
```typescript
import { signInWithPopup, GoogleAuthProvider } from 'firebase/auth';

export async function signInWithGoogle() {
  const provider = new GoogleAuthProvider();
  provider.addScope('profile');
  provider.addScope('email');

  try {
    const result = await signInWithPopup(auth, provider);
    const user = result.user;

    // Check if user document exists, create if not
    const userDoc = await getDoc(doc(db, 'users', user.uid));
    if (!userDoc.exists()) {
      await setDoc(doc(db, 'users', user.uid), {
        email: user.email,
        displayName: user.displayName,
        photoURL: user.photoURL,
        createdAt: serverTimestamp(),
        role: 'user',
      });
    }

    return user;
  } catch (error) {
    if (error instanceof FirebaseError) {
      switch (error.code) {
        case 'auth/popup-closed-by-user':
          throw new Error('Sign in cancelled');
        case 'auth/popup-blocked':
          throw new Error('Popup blocked. Please allow popups for this site.');
        default:
          throw new Error('Google sign in failed');
      }
    }
    throw error;
  }
}
```

**GitHub Sign-In**:
```typescript
import { GithubAuthProvider } from 'firebase/auth';

export async function signInWithGitHub() {
  const provider = new GithubAuthProvider();
  provider.addScope('read:user');

  return await signInWithPopup(auth, provider);
}
```

### Anonymous Authentication

```typescript
import { signInAnonymously } from 'firebase/auth';

export async function signInAnonymous() {
  const userCredential = await signInAnonymously(auth);
  return userCredential.user;
}
```

## Session Management

### Auth State Listener

```typescript
import { onAuthStateChanged, type User } from 'firebase/auth';

export function onAuthChange(callback: (user: User | null) => void) {
  return onAuthStateChanged(auth, async (user) => {
    if (user) {
      // User is signed in
      // Optionally fetch additional user data from Firestore
      const userDoc = await getDoc(doc(db, 'users', user.uid));
      callback(user);
    } else {
      // User is signed out
      callback(null);
    }
  });
}
```

### React Auth Provider

```typescript
'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { User } from 'firebase/auth';
import { onAuthChange } from '@/lib/firebase/auth';

interface AuthContextType {
  user: User | null;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthChange((user) => {
      setUser(user);
      setLoading(false);

      // Store token in cookie for middleware
      if (user) {
        user.getIdToken().then((token) => {
          document.cookie = `firebase-token=${token}; path=/; secure; samesite=strict; max-age=3600`;
        });
      } else {
        document.cookie = 'firebase-token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT';
      }
    });

    return unsubscribe;
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
```

## Protected Routes

### Next.js Middleware

```typescript
// middleware.ts
import { NextRequest, NextResponse } from 'next/server';
import { adminAuth } from '@/lib/firebase/admin';

export async function middleware(request: NextRequest) {
  const token = request.cookies.get('firebase-token')?.value;

  if (!token) {
    const url = new URL('/login', request.url);
    url.searchParams.set('redirect', request.nextUrl.pathname);
    return NextResponse.redirect(url);
  }

  try {
    await adminAuth.verifyIdToken(token);
    return NextResponse.next();
  } catch (error) {
    const response = NextResponse.redirect(new URL('/login', request.url));
    response.cookies.delete('firebase-token');
    return response;
  }
}

export const config = {
  matcher: ['/dashboard/:path*', '/profile/:path*', '/admin/:path*'],
};
```

### Server Component Auth Check

```typescript
// app/dashboard/page.tsx
import { cookies } from 'next/headers';
import { adminAuth } from '@/lib/firebase/admin';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const token = cookies().get('firebase-token')?.value;

  if (!token) {
    redirect('/login');
  }

  try {
    const decodedToken = await adminAuth.verifyIdToken(token);
    const userId = decodedToken.uid;

    // Fetch user data
    const userDoc = await adminDb.collection('users').doc(userId).get();
    const user = userDoc.data();

    return <div>Welcome, {user.displayName}</div>;
  } catch (error) {
    redirect('/login');
  }
}
```

### Client Component Auth Guard

```typescript
'use client';

import { useAuth } from '@/components/auth/AuthProvider';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export function withAuth<P extends object>(
  Component: React.ComponentType<P>
): React.ComponentType<P> {
  return function AuthGuard(props: P) {
    const { user, loading } = useAuth();
    const router = useRouter();

    useEffect(() => {
      if (!loading && !user) {
        router.push('/login');
      }
    }, [user, loading, router]);

    if (loading) {
      return <div>Loading...</div>;
    }

    if (!user) {
      return null;
    }

    return <Component {...props} />;
  };
}
```

## Password Management

### Password Reset

```typescript
import { sendPasswordResetEmail } from 'firebase/auth';

export async function resetPassword(email: string) {
  try {
    await sendPasswordResetEmail(auth, email, {
      url: `${window.location.origin}/login`,
      handleCodeInApp: false,
    });
    return { success: true };
  } catch (error) {
    if (error instanceof FirebaseError) {
      switch (error.code) {
        case 'auth/user-not-found':
          // Don't reveal if email exists (security best practice)
          return { success: true };
        default:
          throw new Error('Failed to send reset email');
      }
    }
    throw error;
  }
}
```

### Email Verification

```typescript
import { sendEmailVerification } from 'firebase/auth';

export async function sendVerificationEmail() {
  const user = auth.currentUser;
  if (!user) throw new Error('No user signed in');

  await sendEmailVerification(user, {
    url: `${window.location.origin}/dashboard`,
  });
}
```

### Update Password

```typescript
import { updatePassword } from 'firebase/auth';

export async function changePassword(newPassword: string) {
  const user = auth.currentUser;
  if (!user) throw new Error('No user signed in');

  try {
    await updatePassword(user, newPassword);
    return { success: true };
  } catch (error) {
    if (error instanceof FirebaseError && error.code === 'auth/requires-recent-login') {
      throw new Error('Please sign in again to change your password');
    }
    throw error;
  }
}
```

## Error Handling Reference

| Firebase Error Code | User-Friendly Message |
|---------------------|----------------------|
| `auth/email-already-in-use` | Email already registered |
| `auth/weak-password` | Password must be at least 6 characters |
| `auth/invalid-email` | Invalid email address |
| `auth/user-not-found` | Invalid email or password |
| `auth/wrong-password` | Invalid email or password |
| `auth/too-many-requests` | Too many attempts. Try again later. |
| `auth/popup-closed-by-user` | Sign in cancelled |
| `auth/popup-blocked` | Please allow popups |
| `auth/requires-recent-login` | Please sign in again |

## Best Practices

✅ **Do**:
- Store tokens in `HttpOnly` cookies (not localStorage)
- Verify tokens server-side with Admin SDK
- Implement email verification for production
- Use secure password requirements (min 8 chars, complexity)
- Handle all Firebase error codes gracefully
- Create user profile in Firestore after sign-up
- Use middleware for route protection

❌ **Don't**:
- Store tokens in localStorage (XSS risk)
- Trust client-side auth state alone
- Reveal if email exists during password reset
- Allow weak passwords
- Skip email verification in production
- Expose Firebase error codes to users

---

**Related Skills**: `firebase-admin-sdk-server-integration`, `firestore-security-rules-generation`
**Token Estimate**: ~1,300 tokens
