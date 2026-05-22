---
name: firebase-admin-sdk-server-integration
description: |
  Server-side Firebase Admin SDK patterns for Next.js 14+, including secure initialization, custom claims,
  server-only protection, token verification, privileged operations, and environment separation.
  Keywords: "admin sdk", "server-only", "custom claims", "verify token", "server", "privileged"
---

# Firebase Admin SDK Server Integration

## Overview

The Firebase Admin SDK provides privileged server-side access to Firebase services, bypassing security rules. It must be used exclusively in server environments (Server Components, API Routes, Server Actions).

## Critical Security Pattern: server-only Package

**MANDATORY**: All Admin SDK files MUST import `server-only` to prevent client-side bundling.

```typescript
// lib/firebase/admin.ts
import 'server-only'; // CRITICAL: First import, prevents client bundling

import { initializeApp, getApps, cert } from 'firebase-admin/app';
```

**Why**: Without `server-only`, service account credentials could leak into the client bundle, exposing your entire Firebase project.

## Secure Admin SDK Initialization

```typescript
// lib/firebase/admin.ts
import 'server-only';

import { initializeApp, getApps, cert, type App } from 'firebase-admin/app';
import { getAuth, type Auth } from 'firebase-admin/auth';
import { getFirestore, type Firestore } from 'firebase-admin/firestore';
import { getStorage, type Storage } from 'firebase-admin/storage';

/**
 * Initialize Firebase Admin SDK with service account credentials
 * ONLY use in server-side code
 */
const adminConfig = {
  projectId: process.env.FIREBASE_ADMIN_PROJECT_ID,
  credential: cert({
    projectId: process.env.FIREBASE_ADMIN_PROJECT_ID,
    clientEmail: process.env.FIREBASE_ADMIN_CLIENT_EMAIL,
    // Firebase private keys contain \n characters that need to be unescaped
    privateKey: process.env.FIREBASE_ADMIN_PRIVATE_KEY?.replace(/\\n/g, '\n'),
  }),
};

// Validate environment variables
if (
  !process.env.FIREBASE_ADMIN_PROJECT_ID ||
  !process.env.FIREBASE_ADMIN_CLIENT_EMAIL ||
  !process.env.FIREBASE_ADMIN_PRIVATE_KEY
) {
  throw new Error(
    'Missing Firebase Admin SDK environment variables. Ensure .env.local is configured.'
  );
}

// Singleton pattern (prevent multiple initializations)
let adminApp: App;
if (getApps().length === 0) {
  adminApp = initializeApp(adminConfig, 'admin');
} else {
  adminApp = getApps()[0];
}

/**
 * Admin Authentication
 * Use for: token verification, custom claims, user management
 */
export const adminAuth: Auth = getAuth(adminApp);

/**
 * Admin Firestore
 * Use for: privileged data access, bypassing security rules
 */
export const adminDb: Firestore = getFirestore(adminApp);

/**
 * Admin Storage
 * Use for: signed URLs, server-side file operations
 */
export const adminStorage: Storage = getStorage(adminApp);

export { adminApp };
```

## Environment Variables

**`.env.local`** (Server-only variables):
```bash
# Firebase Admin SDK Credentials (NEVER commit these!)
FIREBASE_ADMIN_PROJECT_ID=your-project-id
FIREBASE_ADMIN_CLIENT_EMAIL=firebase-adminsdk-xxxxx@your-project-id.iam.gserviceaccount.com
FIREBASE_ADMIN_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYourPrivateKeyHere\n-----END PRIVATE KEY-----\n"
```

**Get Credentials**:
1. Firebase Console → Project Settings → Service Accounts
2. Click "Generate New Private Key"
3. Download JSON file
4. Extract values into `.env.local`

## Token Verification

### Middleware Pattern

```typescript
// middleware.ts
import { NextRequest, NextResponse } from 'next/server';
import { adminAuth } from '@/lib/firebase/admin';

export async function middleware(request: NextRequest) {
  const token = request.cookies.get('firebase-token')?.value;

  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  try {
    // Verify token signature and expiration
    const decodedToken = await adminAuth.verifyIdToken(token);

    // Add user info to request headers for Server Components
    const requestHeaders = new Headers(request.headers);
    requestHeaders.set('x-user-id', decodedToken.uid);
    requestHeaders.set('x-user-email', decodedToken.email || '');

    return NextResponse.next({
      request: { headers: requestHeaders },
    });
  } catch (error) {
    // Invalid or expired token
    const response = NextResponse.redirect(new URL('/login', request.url));
    response.cookies.delete('firebase-token');
    return response;
  }
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/protected/:path*'],
};
```

### Server Component Pattern

```typescript
// app/dashboard/page.tsx
import { cookies, headers } from 'next/headers';
import { adminAuth, adminDb } from '@/lib/firebase/admin';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  // Get user ID from middleware headers
  const userId = headers().get('x-user-id');

  if (!userId) {
    redirect('/login');
  }

  // Fetch user data with Admin SDK (bypasses security rules)
  const userDoc = await adminDb.collection('users').doc(userId).get();
  const user = userDoc.data();

  return <div>Welcome, {user?.displayName}</div>;
}
```

### API Route Pattern

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { adminAuth, adminDb } from '@/lib/firebase/admin';

export async function GET(request: NextRequest) {
  // Verify authentication
  const token = request.cookies.get('firebase-token')?.value;

  if (!token) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  try {
    const decodedToken = await adminAuth.verifyIdToken(token);

    // Fetch data with Admin SDK
    const usersSnapshot = await adminDb.collection('users').limit(10).get();
    const users = usersSnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));

    return NextResponse.json({ users });
  } catch (error) {
    return NextResponse.json({ error: 'Invalid token' }, { status: 401 });
  }
}
```

## Custom Claims (RBAC)

### Set Custom Claims (Server-Side Only)

```typescript
// app/api/admin/set-role/route.ts
import 'server-only';
import { adminAuth } from '@/lib/firebase/admin';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  // Verify requester is admin
  const token = request.cookies.get('firebase-token')?.value;
  if (!token) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const decodedToken = await adminAuth.verifyIdToken(token);
  if (decodedToken.role !== 'admin') {
    return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
  }

  // Set custom claim
  const { uid, role } = await request.json();
  await adminAuth.setCustomUserClaims(uid, { role });

  return NextResponse.json({ success: true });
}
```

### Read Custom Claims (Client-Side)

```typescript
'use client';

import { auth } from '@/lib/firebase/client';
import { useEffect, useState } from 'react';

export function useUserRole() {
  const [role, setRole] = useState<string | null>(null);

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged(async (user) => {
      if (user) {
        const idTokenResult = await user.getIdTokenResult();
        setRole(idTokenResult.claims.role as string || 'user');
      } else {
        setRole(null);
      }
    });

    return unsubscribe;
  }, []);

  return role;
}
```

**IMPORTANT**: After setting custom claims, client must force token refresh:

```typescript
// Client-side after role is changed
await auth.currentUser?.getIdToken(true); // Force refresh
```

## Privileged Operations

### User Management

```typescript
// Create user server-side
export async function createUser(email: string, password: string, displayName: string) {
  const userRecord = await adminAuth.createUser({
    email,
    password,
    displayName,
    emailVerified: false,
  });

  // Create Firestore profile
  await adminDb.collection('users').doc(userRecord.uid).set({
    email,
    displayName,
    createdAt: new Date(),
    role: 'user',
  });

  return userRecord;
}

// Delete user and all data
export async function deleteUser(uid: string) {
  // Delete user data from Firestore
  await adminDb.collection('users').doc(uid).delete();

  // Delete Firebase Auth user
  await adminAuth.deleteUser(uid);
}

// List all users (paginated)
export async function listUsers(maxResults = 100, pageToken?: string) {
  const listUsersResult = await adminAuth.listUsers(maxResults, pageToken);
  return {
    users: listUsersResult.users,
    nextPageToken: listUsersResult.pageToken,
  };
}
```

### Bypass Security Rules

```typescript
// Read data regardless of security rules
export async function adminGetPost(postId: string) {
  const postDoc = await adminDb.collection('posts').doc(postId).get();
  return postDoc.data();
}

// Write data bypassing rules
export async function adminUpdatePost(postId: string, updates: Partial<Post>) {
  await adminDb.collection('posts').doc(postId).update(updates);
}
```

### Generate Signed URLs (Storage)

```typescript
import { getStorage } from 'firebase-admin/storage';

export async function generateSignedUrl(filePath: string) {
  const bucket = getStorage().bucket();
  const file = bucket.file(filePath);

  const [url] = await file.getSignedUrl({
    action: 'read',
    expires: Date.now() + 60 * 60 * 1000, // 1 hour
  });

  return url;
}
```

## Environment Separation

### Server Component (Admin SDK)

```typescript
// app/users/page.tsx
import { adminDb } from '@/lib/firebase/admin';

export default async function UsersPage() {
  // Runs on server, uses Admin SDK
  const usersSnapshot = await adminDb.collection('users').get();
  const users = usersSnapshot.docs.map(doc => doc.data());

  return <div>{/* Render users */}</div>;
}
```

### Client Component (Client SDK)

```typescript
// components/UserProfile.tsx
'use client';

import { db } from '@/lib/firebase/client'; // Client SDK
import { doc, getDoc } from 'firebase/firestore';

export function UserProfile({ userId }: { userId: string }) {
  // Runs on client, uses Client SDK, respects security rules
  useEffect(() => {
    async function fetchUser() {
      const userDoc = await getDoc(doc(db, 'users', userId));
      setUser(userDoc.data());
    }
    fetchUser();
  }, [userId]);

  return <div>{user?.name}</div>;
}
```

## Anti-Patterns

❌ **Importing Admin SDK in Client Component**:
```typescript
'use client';
import { adminDb } from '@/lib/firebase/admin'; // ERROR: Leaks credentials!
```

✅ **Use Server Actions Instead**:
```typescript
// app/actions/getUser.ts
'use server';
import { adminDb } from '@/lib/firebase/admin';

export async function getUser(userId: string) {
  const userDoc = await adminDb.collection('users').doc(userId).get();
  return userDoc.data();
}

// Client component
'use client';
import { getUser } from '@/app/actions/getUser';
```

❌ **Hardcoding Credentials**:
```typescript
const adminConfig = {
  privateKey: "-----BEGIN PRIVATE KEY-----\n...", // NEVER!
};
```

✅ **Use Environment Variables**:
```typescript
const adminConfig = {
  privateKey: process.env.FIREBASE_ADMIN_PRIVATE_KEY?.replace(/\\n/g, '\n'),
};
```

## Best Practices

✅ **Do**:
- Always import `'server-only'` first in admin files
- Store credentials in server-side environment variables
- Validate environment variables on startup
- Use middleware for token verification
- Force token refresh after custom claims change
- Use Admin SDK for server-side data fetching

❌ **Don't**:
- Import Admin SDK in client components
- Commit `.env.local` to version control
- Share service account keys
- Skip token verification
- Use Admin SDK for client-side operations

---

**Related Skills**: `firebase-authentication-patterns`, `firebase-nextjs-integration-strategies`
**Token Estimate**: ~1,300 tokens
