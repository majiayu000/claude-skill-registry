---
name: firebase
description: Firebase Firestore, Auth, Storage, real-time listeners, security rules
---

# Firebase Skill

*Load with: base.md + security.md*

Firebase/Firestore patterns for web and mobile applications with real-time data, offline support, and security rules.

**Sources:** [Firebase Docs](https://firebase.google.com/docs) | [Firestore Best Practices](https://firebase.google.com/docs/firestore/best-practices) | [Security Rules](https://firebase.google.com/docs/rules)

---

## Core Principle

**Denormalize with purpose, secure with rules, scale horizontally.**

Firestore is a document database - embrace denormalization for read efficiency. Security rules are your server-side validation. Design for your access patterns.

---

## Firebase Stack

| Service | Purpose |
|---------|---------|
| **Firestore** | NoSQL document database with real-time sync |
| **Authentication** | User auth, OAuth, anonymous sessions |
| **Storage** | File uploads with security rules |
| **Functions** | Serverless backend (Node.js) |
| **Hosting** | Static site + CDN |
| **Extensions** | Pre-built solutions (Stripe, Algolia, etc.) |

---

## Project Setup

### Install Firebase CLI
```bash
# Install globally
npm install -g firebase-tools

# Login
firebase login

# Initialize in project
firebase init
```

### Initialize with Emulators
```bash
firebase init emulators

# Start local development
firebase emulators:start
```

### Project Structure
```
project/
├── firebase.json           # Firebase config
├── firestore.rules         # Security rules
├── firestore.indexes.json  # Composite indexes
├── storage.rules           # Storage security rules
└── functions/              # Cloud Functions
    ├── src/
    ├── package.json
    └── tsconfig.json
```

---

## Firestore Data Modeling

### Document Structure
```typescript
// Good: Flat documents with all needed data
interface Post {
  id: string;
  title: string;
  content: string;
  authorId: string;
  authorName: string;      // Denormalized for display
  authorAvatar: string;    // Denormalized
  tags: string[];
  likeCount: number;       // Aggregated counter
  createdAt: Timestamp;
  updatedAt: Timestamp;
}

// Collection: posts/{postId}
```

### When to Use Subcollections
```typescript
// Use subcollections for:
// 1. Unbounded lists (comments, messages)
// 2. Data with different access patterns
// 3. Data that grows independently

// posts/{postId}/comments/{commentId}
interface Comment {
  id: string;
  text: string;
  authorId: string;
  authorName: string;
  createdAt: Timestamp;
}
```

### Data Model Patterns

```typescript
// Pattern 1: Embedded data (bounded, always needed)
interface User {
  id: string;
  email: string;
  profile: {
    displayName: string;
    bio: string;
    avatar: string;
  };
  settings: {
    notifications: boolean;
    theme: 'light' | 'dark';
  };
}

// Pattern 2: Reference with denormalization
interface Order {
  id: string;
  userId: string;
  userEmail: string;  // Denormalized for display
  items: OrderItem[]; // Embedded (bounded)
  total: number;
  status: 'pending' | 'paid' | 'shipped';
}

// Pattern 3: Aggregation documents
// Keep counters in parent document
interface Channel {
  id: string;
  name: string;
  memberCount: number;  // Updated via Cloud Function
  messageCount: number;
}
```

---

## TypeScript SDK (Modular v9+)

### Initialize Firebase
```typescript
// lib/firebase.ts
import { initializeApp, getApps } from 'firebase/app';
import { getFirestore, connectFirestoreEmulator } from 'firebase/firestore';
import { getAuth, connectAuthEmulator } from 'firebase/auth';
import { getStorage, connectStorageEmulator } from 'firebase/storage';

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID
};

// Initialize only once
const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];

export const db = getFirestore(app);
export const auth = getAuth(app);
export const storage = getStorage(app);

// Connect to emulators in development
if (process.env.NODE_ENV === 'development') {
  connectFirestoreEmulator(db, 'localhost', 8080);
  connectAuthEmulator(auth, 'http://localhost:9099');
  connectStorageEmulator(storage, 'localhost', 9199);
}
```

### CRUD Operations
```typescript
import {
  collection,
  doc,
  getDoc,
  getDocs,
  addDoc,
  setDoc,
  updateDoc,
  deleteDoc,
  query,
  where,
  orderBy,
  limit,
  startAfter,
  serverTimestamp,
  Timestamp
} from 'firebase/firestore';
import { db } from './firebase';

// Create
async function createPost(data: Omit<Post, 'id' | 'createdAt' | 'updatedAt'>) {
  const docRef = await addDoc(collection(db, 'posts'), {
    ...data,
    createdAt: serverTimestamp(),
    updatedAt: serverTimestamp()
  });
  return docRef.id;
}

// Read single document
async function getPost(postId: string): Promise<Post | null> {
  const docSnap = await getDoc(doc(db, 'posts', postId));
  if (!docSnap.exists()) return null;
  return { id: docSnap.id, ...docSnap.data() } as Post;
}

// Query with filters
async function getPostsByAuthor(authorId: string, pageSize = 10) {
  const q = query(
    collection(db, 'posts'),
    where('authorId', '==', authorId),
    orderBy('createdAt', 'desc'),
    limit(pageSize)
  );
  const snapshot = await getDocs(q);
  return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() } as Post));
}

// Pagination
async function getNextPage(lastDoc: Post, pageSize = 10) {
  const q = query(
    collection(db, 'posts'),
    orderBy('createdAt', 'desc'),
    startAfter(lastDoc.createdAt),
    limit(pageSize)
  );
  const snapshot = await getDocs(q);
  return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() } as Post));
}

// Update
async function updatePost(postId: string, data: Partial<Post>) {
  await updateDoc(doc(db, 'posts', postId), {
    ...data,
    updatedAt: serverTimestamp()
  });
}

// Delete
async function deletePost(postId: string) {
  await deleteDoc(doc(db, 'posts', postId));
}
```

### Real-time Listeners
```typescript
import { onSnapshot, QuerySnapshot, DocumentSnapshot } from 'firebase/firestore';

// Listen to single document
function subscribeToPost(
  postId: string,
  onData: (post: Post | null) => void,
  onError: (error: Error) => void
) {
  return onSnapshot(
    doc(db, 'posts', postId),
    (snapshot: DocumentSnapshot) => {
      if (!snapshot.exists()) {
        onData(null);
        return;
      }
      onData({ id: snapshot.id, ...snapshot.data() } as Post);
    },
    onError
  );
}

// Listen to collection with query
function subscribeToPosts(
  authorId: string,
  onData: (posts: Post[]) => void,
  onError: (error: Error) => void
) {
  const q = query(
    collection(db, 'posts'),
    where('authorId', '==', authorId),
    orderBy('createdAt', 'desc')
  );

  return onSnapshot(
    q,
    (snapshot: QuerySnapshot) => {
      const posts = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      } as Post));
      onData(posts);
    },
    onError
  );
}

// React hook example
function usePost(postId: string) {
  const [post, setPost] = useState<Post | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const unsubscribe = subscribeToPost(
      postId,
      (data) => {
        setPost(data);
        setLoading(false);
      },
      (err) => {
        setError(err);
        setLoading(false);
      }
    );
    return unsubscribe;
  }, [postId]);

  return { post, loading, error };
}
```

### Offline Persistence (Web)
```typescript
import { enableIndexedDbPersistence, enableMultiTabIndexedDbPersistence } from 'firebase/firestore';

// Enable offline persistence (call once at startup)
async function enableOffline() {
  try {
    // Single tab
    await enableIndexedDbPersistence(db);

    // OR multi-tab (recommended)
    await enableMultiTabIndexedDbPersistence(db);
  } catch (err: any) {
    if (err.code === 'failed-precondition') {
      // Multiple tabs open, only works in one
      console.warn('Persistence only available in one tab');
    } else if (err.code === 'unimplemented') {
      // Browser doesn't support
      console.warn('Persistence not supported');
    }
  }
}

// Check if data is from cache
onSnapshot(docRef, (snapshot) => {
  const source = snapshot.metadata.fromCache ? 'cache' : 'server';
  console.log(`Data from ${source}`);

  if (snapshot.metadata.hasPendingWrites) {
    console.log('Local changes pending sync');
  }
});
```

---

## Security Rules

### Basic Rules Structure
```javascript
// firestore.rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // Helper functions
    function isAuthenticated() {
      return request.auth != null;
    }

    function isOwner(userId) {
      return request.auth.uid == userId;
    }

    function isAdmin() {
      return request.auth.token.admin == true;
    }

    // Posts collection
    match /posts/{postId} {
      // Anyone can read published posts
      allow read: if resource.data.status == 'published';

      // Only authenticated users can create
      allow create: if isAuthenticated()
        && request.resource.data.authorId == request.auth.uid
        && request.resource.data.keys().hasAll(['title', 'content', 'authorId']);

      // Only author can update
      allow update: if isOwner(resource.data.authorId)
        && request.resource.data.authorId == resource.data.authorId; // Can't change author

      // Only author or admin can delete
      allow delete: if isOwner(resource.data.authorId) || isAdmin();

      // Comments subcollection
      match /comments/{commentId} {
        allow read: if true;
        allow create: if isAuthenticated();
        allow update, delete: if isOwner(resource.data.authorId);
      }
    }

    // User profiles
    match /users/{userId} {
      allow read: if true;
      allow create: if isAuthenticated() && isOwner(userId);
      allow update: if isOwner(userId);
      allow delete: if false; // Never allow delete
    }

    // Private user data
    match /users/{userId}/private/{document=**} {
      allow read, write: if isOwner(userId);
    }
  }
}
```

### Data Validation in Rules
```javascript
match /posts/{postId} {
  function isValidPost() {
    let data = request.resource.data;
    return data.title is string
      && data.title.size() >= 3
      && data.title.size() <= 100
      && data.content is string
      && data.content.size() <= 50000
      && data.tags is list
      && data.tags.size() <= 5;
  }

  allow create: if isAuthenticated() && isValidPost();
  allow update: if isOwner(resource.data.authorId) && isValidPost();
}
```

### Test Rules Locally
```bash
# Install emulators
firebase emulators:start

# Run rules tests
npm test
```

```typescript
// tests/firestore.rules.test.ts
import { assertFails, assertSucceeds, initializeTestEnvironment } from '@firebase/rules-unit-testing';

describe('Firestore Rules', () => {
  let testEnv: RulesTestEnvironment;

  beforeAll(async () => {
    testEnv = await initializeTestEnvironment({
      projectId: 'test-project',
      firestore: { rules: fs.readFileSync('firestore.rules', 'utf8') }
    });
  });

  test('unauthenticated users cannot write', async () => {
    const unauthedDb = testEnv.unauthenticatedContext().firestore();
    await assertFails(
      setDoc(doc(unauthedDb, 'posts/test'), { title: 'Test' })
    );
  });

  test('users can only update own posts', async () => {
    const aliceDb = testEnv.authenticatedContext('alice').firestore();
    const bobDb = testEnv.authenticatedContext('bob').firestore();

    // Create as Alice
    await assertSucceeds(
      setDoc(doc(aliceDb, 'posts/test'), { title: 'Test', authorId: 'alice' })
    );

    // Bob cannot update
    await assertFails(
      updateDoc(doc(bobDb, 'posts/test'), { title: 'Hacked' })
    );
  });
});
```

---

## Authentication

### Email/Password Auth
```typescript
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  User
} from 'firebase/auth';
import { auth } from './firebase';

// Sign up
async function signUp(email: string, password: string) {
  const credential = await createUserWithEmailAndPassword(auth, email, password);
  return credential.user;
}

// Sign in
async function signIn(email: string, password: string) {
  const credential = await signInWithEmailAndPassword(auth, email, password);
  return credential.user;
}

// Sign out
async function logout() {
  await signOut(auth);
}

// Auth state listener
function onAuthChange(callback: (user: User | null) => void) {
  return onAuthStateChanged(auth, callback);
}
```

### OAuth Providers
```typescript
import {
  GoogleAuthProvider,
  signInWithPopup,
  signInWithRedirect
} from 'firebase/auth';

const googleProvider = new GoogleAuthProvider();

async function signInWithGoogle() {
  try {
    const result = await signInWithPopup(auth, googleProvider);
    return result.user;
  } catch (error) {
    // Handle errors
    throw error;
  }
}
```

---

## Cloud Functions

### Basic HTTP Function
```typescript
// functions/src/index.ts
import { onRequest } from 'firebase-functions/v2/https';
import { onDocumentCreated } from 'firebase-functions/v2/firestore';
import { initializeApp } from 'firebase-admin/app';
import { getFirestore } from 'firebase-admin/firestore';

initializeApp();
const db = getFirestore();

// HTTP endpoint
export const helloWorld = onRequest((request, response) => {
  response.json({ message: 'Hello from Firebase!' });
});

// Firestore trigger
export const onPostCreated = onDocumentCreated('posts/{postId}', async (event) => {
  const snapshot = event.data;
  if (!snapshot) return;

  const post = snapshot.data();

  // Update author's post count
  await db.doc(`users/${post.authorId}`).update({
    postCount: FieldValue.increment(1)
  });
});
```

### Callable Functions
```typescript
// Backend
import { onCall, HttpsError } from 'firebase-functions/v2/https';

export const createPost = onCall(async (request) => {
  // Auth check
  if (!request.auth) {
    throw new HttpsError('unauthenticated', 'Must be logged in');
  }

  const { title, content } = request.data;

  // Validation
  if (!title || title.length < 3) {
    throw new HttpsError('invalid-argument', 'Title must be at least 3 characters');
  }

  // Create post
  const postRef = await db.collection('posts').add({
    title,
    content,
    authorId: request.auth.uid,
    createdAt: FieldValue.serverTimestamp()
  });

  return { postId: postRef.id };
});

// Frontend
import { getFunctions, httpsCallable } from 'firebase/functions';

const functions = getFunctions();
const createPostFn = httpsCallable(functions, 'createPost');

async function createPost(title: string, content: string) {
  const result = await createPostFn({ title, content });
  return result.data as { postId: string };
}
```

---

## Batch Operations & Transactions

### Batch Writes
```typescript
import { writeBatch, doc } from 'firebase/firestore';

async function batchUpdate(updates: { id: string; data: any }[]) {
  const batch = writeBatch(db);

  updates.forEach(({ id, data }) => {
    batch.update(doc(db, 'posts', id), data);
  });

  await batch.commit(); // Atomic
}
```

### Transactions
```typescript
import { runTransaction, doc, increment } from 'firebase/firestore';

async function likePost(postId: string, userId: string) {
  await runTransaction(db, async (transaction) => {
    const postRef = doc(db, 'posts', postId);
    const likeRef = doc(db, 'posts', postId, 'likes', userId);

    const postSnap = await transaction.get(postRef);
    if (!postSnap.exists()) throw new Error('Post not found');

    const likeSnap = await transaction.get(likeRef);
    if (likeSnap.exists()) throw new Error('Already liked');

    transaction.set(likeRef, { createdAt: serverTimestamp() });
    transaction.update(postRef, { likeCount: increment(1) });
  });
}
```

---

## Indexes

### Composite Indexes
```json
// firestore.indexes.json
{
  "indexes": [
    {
      "collectionGroup": "posts",
      "queryScope": "COLLECTION",
      "fields": [
        { "fieldPath": "authorId", "order": "ASCENDING" },
        { "fieldPath": "createdAt", "order": "DESCENDING" }
      ]
    },
    {
      "collectionGroup": "posts",
      "queryScope": "COLLECTION",
      "fields": [
        { "fieldPath": "tags", "arrayConfig": "CONTAINS" },
        { "fieldPath": "createdAt", "order": "DESCENDING" }
      ]
    }
  ]
}
```

```bash
# Deploy indexes
firebase deploy --only firestore:indexes
```

---

## CLI Quick Reference

```bash
# Project setup
firebase login                       # Authenticate
firebase init                        # Initialize project
firebase projects:list               # List projects

# Emulators
firebase emulators:start             # Start all emulators
firebase emulators:start --only firestore,auth  # Specific emulators

# Deploy
firebase deploy                      # Deploy everything
firebase deploy --only firestore     # Deploy rules + indexes
firebase deploy --only functions     # Deploy functions
firebase deploy --only hosting       # Deploy hosting

# Functions
cd functions && npm run build        # Build TypeScript
firebase functions:log               # View logs
```

---

## Anti-Patterns

- **No security rules** - Always write rules, never use test mode in production
- **Deep nesting** - Keep documents flat, max 2-3 levels
- **Large documents** - Max 1MB, split if larger
- **Unbounded arrays** - Use subcollections for lists that grow
- **No offline handling** - Enable persistence for mobile/PWA
- **Reading all fields** - Use field masks or Firestore Lite
- **Ignoring indexes** - Check console for missing index errors
- **No emulator testing** - Always test rules before deploy
