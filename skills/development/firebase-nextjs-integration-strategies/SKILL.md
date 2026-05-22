---
name: firebase-nextjs-integration-strategies
version: "1.0"
description: >
  Next.js 14+ App Router integration with Firebase including server/client SDK separation and data fetching patterns.
  PROACTIVELY activate for: (1) setting up dual SDK architecture for client/server, (2) fetching data in Server Components with Admin SDK, (3) implementing real-time listeners in Client Components.
  Triggers: "nextjs firebase", "app router", "server client sdk"
group: data
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Firebase Next.js Integration Strategies

## Overview

Next.js 14+ App Router has a clear server/client boundary. This skill provides patterns for integrating Firebase's dual SDK model (Client SDK + Admin SDK) with Next.js execution environments.

## Dual SDK Architecture

### Client SDK (Client Components, Browser)

**Use For**:
- Client-side authentication (sign-in, sign-up, sign-out)
- Real-time listeners (`onSnapshot`)
- Client-side mutations with optimistic updates
- File uploads to Storage

**Location**: `src/lib/firebase/client.ts`

```typescript
import { initializeApp, getApps } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { getStorage } from 'firebase/storage';

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
};

const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];

export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);
```

### Admin SDK (Server Components, API Routes, Server Actions)

**Use For**:
- Privileged data access in Server Components
- Token verification in middleware
- Server-side mutations
- Bypassing security rules

**Location**: `src/lib/firebase/admin.ts`

```typescript
import 'server-only'; // CRITICAL: Prevents client bundling

import { initializeApp, getApps, cert } from 'firebase-admin/app';
import { getAuth } from 'firebase-admin/auth';
import { getFirestore } from 'firebase-admin/firestore';

const adminConfig = {
  projectId: process.env.FIREBASE_ADMIN_PROJECT_ID,
  credential: cert({
    projectId: process.env.FIREBASE_ADMIN_PROJECT_ID,
    clientEmail: process.env.FIREBASE_ADMIN_CLIENT_EMAIL,
    privateKey: process.env.FIREBASE_ADMIN_PRIVATE_KEY?.replace(/\\n/g, '\n'),
  }),
};

const adminApp = getApps().length === 0 ? initializeApp(adminConfig, 'admin') : getApps()[0];

export const adminAuth = getAuth(adminApp);
export const adminDb = getFirestore(adminApp);
```

## Data Fetching Patterns

### Pattern 1: Server Component (Recommended for Initial Load)

**Advantages**:
- Fast (no client-side fetch)
- SEO-friendly (pre-rendered)
- Secure (uses Admin SDK)
- Cached by Next.js

```typescript
// app/posts/page.tsx
import { adminDb } from '@/lib/firebase/admin';
import { postAdminConverter, type Post } from '@/lib/firebase/schemas/post.schema';

export default async function PostsPage() {
  // Fetch data server-side with Admin SDK
  const postsSnapshot = await adminDb
    .collection('posts')
    .withConverter(postAdminConverter)
    .where('status', '==', 'published')
    .orderBy('createdAt', 'desc')
    .limit(10)
    .get();

  const posts: Post[] = postsSnapshot.docs.map(doc => doc.data());

  return (
    <div>
      {posts.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.content}</p>
        </article>
      ))}
    </div>
  );
}
```

### Pattern 2: Client Component with Real-Time Listener

**Use When**:
- Need real-time updates
- User-specific data (respects security rules)
- Interactive UI

```typescript
// components/CommentsList.tsx
'use client';

import { useEffect, useState } from 'react';
import { collection, query, where, onSnapshot, orderBy } from 'firebase/firestore';
import { db } from '@/lib/firebase/client';
import { commentConverter, type Comment } from '@/lib/firebase/schemas/comment.schema';

export function CommentsList({ postId }: { postId: string }) {
  const [comments, setComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Real-time listener with withConverter
    const q = query(
      collection(db, 'comments'),
      where('postId', '==', postId),
      orderBy('createdAt', 'desc')
    ).withConverter(commentConverter);

    const unsubscribe = onSnapshot(q, (snapshot) => {
      const commentsData = snapshot.docs.map(doc => doc.data());
      setComments(commentsData);
      setLoading(false);
    });

    return unsubscribe; // Cleanup on unmount
  }, [postId]);

  if (loading) return <div>Loading comments...</div>;

  return (
    <div>
      {comments.map(comment => (
        <div key={comment.id}>{comment.content}</div>
      ))}
    </div>
  );
}
```

### Pattern 3: Server Action (Mutations)

**Use For**:
- Form submissions
- User-initiated mutations
- Progressive enhancement

```typescript
// app/actions/createPost.ts
'use server';

import { adminDb } from '@/lib/firebase/admin';
import { PostSchema, postAdminConverter } from '@/lib/firebase/schemas/post.schema';
import { revalidatePath } from 'next/cache';
import { z } from 'zod';

const CreatePostInput = PostSchema.pick({
  title: true,
  content: true,
}).extend({
  authorId: z.string(),
});

export async function createPost(input: z.infer<typeof CreatePostInput>) {
  // Validate input
  const validated = CreatePostInput.parse(input);

  // Create post with Admin SDK
  const postRef = adminDb.collection('posts').doc();
  await postRef.withConverter(postAdminConverter).set({
    ...validated,
    status: 'draft',
    viewCount: 0,
    createdAt: new Date(),
    updatedAt: new Date(),
  });

  // Revalidate posts page cache
  revalidatePath('/posts');

  return { success: true, postId: postRef.id };
}
```

## Decision Tree

**When to use Server Components**:
- Initial page load
- SEO-critical content
- Privileged data access
- Static or slow-changing data

**When to use Client Components**:
- Real-time updates
- User interactions
- Client-side state
- Animations

**When to use Server Actions**:
- Form submissions
- Mutations
- Progressive enhancement

**When to use API Routes**:
- External webhooks
- Complex server logic
- Non-Next.js clients

## Best Practices

**Do**:
- Use Server Components for initial data load (faster, SEO-friendly)
- Use Client Components for real-time updates
- Use Admin SDK in Server Components/Actions (privileged, bypasses rules)
- Use Client SDK in Client Components (respects security rules)
- Verify tokens in middleware
- Store tokens in `HttpOnly` cookies (not localStorage)
- Use `server-only` package for admin files

**Don't**:
- Import Admin SDK in Client Components
- Use Client SDK in Server Components (wrong execution context)
- Skip token verification
- Fetch data client-side when Server Component would work
- Forget to cleanup real-time listeners (`onSnapshot`)

---

**Related Skills**: `firebase-admin-sdk-server-integration`, `firestore-data-modeling-patterns`
