---
name: api-baas-firebase
description: Firebase backend-as-a-service — Firestore, Authentication, Cloud Functions v2, Storage, Hosting, Admin SDK, security rules, emulator suite
---

# Firebase Patterns

> **Quick Guide:** Use Firebase as your backend-as-a-service for Firestore database, authentication, Cloud Functions, file storage, and hosting. Always use the modular SDK (`firebase/app`, `firebase/firestore`, etc.) for tree-shaking, type Firestore documents with TypeScript interfaces, write security rules for every collection, and use the Admin SDK only on the server.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use the modular Firebase SDK imports (`firebase/app`, `firebase/firestore`, `firebase/auth`) -- NEVER use the deprecated `firebase/compat` namespace API)**

**(You MUST write Firestore security rules for EVERY collection -- a collection without rules is wide open in production)**

**(You MUST NEVER expose Firebase Admin SDK credentials or service account keys in client-side code)**

**(You MUST use Cloud Functions v2 API (`firebase-functions/v2/https`, `firebase-functions/v2/firestore`) -- NOT the deprecated v1 API)**

**(You MUST handle all Firestore operations with error checking -- never assume reads/writes succeed)**

</critical_requirements>

---

**Auto-detection:** Firebase, initializeApp, firebase/app, firebase/firestore, firebase/auth, getFirestore, getAuth, onAuthStateChanged, collection, doc, getDocs, setDoc, updateDoc, deleteDoc, onSnapshot, firebase-admin, firebase-functions, Cloud Functions, Firestore security rules, firebase.json, firebase deploy

**When to use:**

- Initializing Firebase and configuring services (Firestore, Auth, Storage, Functions)
- Implementing authentication (email/password, OAuth, phone, custom tokens)
- Querying and writing Firestore documents (CRUD, real-time listeners, transactions)
- Writing Cloud Functions v2 (HTTP handlers, callable functions, Firestore triggers, scheduled functions)
- Uploading and serving files from Firebase Storage
- Deploying to Firebase Hosting with function rewrites
- Writing Firestore and Storage security rules
- Using the Firebase Admin SDK for server-side operations

**Key patterns covered:**

- Modular SDK setup with `initializeApp` and service getters (`getFirestore`, `getAuth`, `getStorage`)
- Auth flows: sign up, sign in, OAuth, phone auth, `onAuthStateChanged`, session management
- Firestore CRUD with `doc()`, `collection()`, `getDocs()`, `setDoc()`, `updateDoc()`, `deleteDoc()`
- Firestore real-time listeners with `onSnapshot()`
- Firestore queries with `where()`, `orderBy()`, `limit()`, composite indexes
- Cloud Functions v2: `onRequest`, `onCall`, `onDocumentCreated`, `onSchedule`
- Firebase Admin SDK: `initializeApp()`, `getFirestore()`, `getAuth()`, custom tokens, user management
- Security rules: read/write granularity, auth-based access, data validation
- Emulator suite for local development and testing
- Offline persistence with `persistentLocalCache`

**When NOT to use:**

- Complex relational queries needing JOIN operations (use a relational database with an ORM)
- Full server-side ORM patterns (Firestore is a document database, not relational)
- Applications using a non-Firebase authentication provider
- Applications requiring complex server-side business logic beyond Cloud Functions scope

**Examples:**

- [Core Setup & Configuration](examples/core.md) -- App init, emulators, offline persistence
- [Firestore Database](examples/firestore.md) -- CRUD, queries, real-time listeners, transactions
- [Authentication](examples/auth.md) -- Email/password, OAuth, React context pattern
- [Cloud Functions & Admin SDK](examples/functions.md) -- HTTP, callable, triggers, scheduled, Admin SDK
- [Cloud Storage](examples/storage.md) -- Upload with progress, validation, App Check
- [Security Rules](examples/security-rules.md) -- Firestore and Storage rules patterns

---

<philosophy>

## Philosophy

Firebase is Google's Backend-as-a-Service platform providing a complete backend through Firestore (document database), Authentication, Cloud Functions, Storage, Hosting, and more. The modular SDK (v12+) uses tree-shakeable ES module imports for minimal bundle sizes.

**Core principles:**

1. **Modular imports for tree-shaking** -- Import only what you need from `firebase/firestore`, `firebase/auth`, etc. The modular SDK can reduce bundle size by 80%+ compared to the legacy namespace API.
2. **Document-oriented data model** -- Firestore stores data as documents in collections. Design your data model around your query patterns, not normalized relations. Denormalization is expected.
3. **Security rules are mandatory** -- Firestore and Storage are directly accessible from clients. Security rules are your only server-side access control. Every collection needs rules.
4. **Cloud Functions v2 on Cloud Run** -- 2nd generation functions run on Cloud Run with better scaling, concurrency, longer timeouts (up to 60 minutes), and traffic splitting. Always use v2 for new projects.
5. **Offline-first with persistence** -- Firestore supports offline persistence via IndexedDB. Enable it with `persistentLocalCache` for apps that must work without connectivity.
6. **Admin SDK for server-side** -- The Firebase Admin SDK bypasses security rules and has full access. Use it only in trusted server environments (Cloud Functions, API servers).

**When to use Firebase:**

- Rapid prototyping and MVPs with auth, database, and storage out of the box
- Real-time applications (chat, live dashboards, collaborative editing) via Firestore listeners
- Mobile and web apps needing offline support with automatic sync
- Projects wanting serverless backend logic with Cloud Functions
- Applications needing simple file storage with security rules

**When NOT to use:**

- Complex relational data with many-to-many relationships and JOINs (use a relational database)
- Applications needing full-text search (Firestore has limited search -- integrate Algolia or Typesense)
- High-write-throughput scenarios exceeding 10,000 writes/second to a single document
- Applications requiring complex server-side transactions spanning multiple services

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Firebase App Initialization (Modular SDK)

Initialize Firebase with the modular SDK for tree-shaking. Each service has its own import path.

```typescript
// lib/firebase.ts
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { getAuth } from "firebase/auth";
import { getStorage } from "firebase/storage";

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
export const auth = getAuth(app);
export const storage = getStorage(app);
```

**Why good:** Modular imports enable tree-shaking, each service initialized from the app instance, named exports

> Full setup with emulators and offline persistence: [examples/core.md](examples/core.md)

---

### Pattern 2: Firestore CRUD Operations

Use modular functions for all Firestore read/write operations. Always type your documents.

```typescript
const POSTS_COLLECTION = "posts";

// Read
const docSnap = await getDoc(doc(db, POSTS_COLLECTION, postId));
if (!docSnap.exists()) throw new Error(`Not found: ${postId}`);

// Create with auto-ID and server timestamp
const docRef = doc(collection(db, POSTS_COLLECTION));
await setDoc(docRef, { ...data, createdAt: serverTimestamp() });

// Update specific fields
await updateDoc(doc(db, POSTS_COLLECTION, postId), {
  ...data,
  updatedAt: serverTimestamp(),
});

// Delete
await deleteDoc(doc(db, POSTS_COLLECTION, postId));
```

**Why good:** Named constants for collection names, existence check before accessing data, `serverTimestamp()` for consistent timestamps, typed input parameters

> Full CRUD service with pagination: [examples/firestore.md](examples/firestore.md)

---

### Pattern 3: Firestore Real-Time Listeners

Subscribe to document and collection changes with `onSnapshot`. Always unsubscribe to prevent memory leaks.

```typescript
function subscribeToPublishedPosts(
  onUpdate: (posts: Post[]) => void,
  onError: (error: Error) => void,
): Unsubscribe {
  const q = query(
    collection(db, POSTS_COLLECTION),
    where("published", "==", true),
    orderBy("createdAt", "desc"),
  );
  return onSnapshot(
    q,
    (snapshot) => {
      onUpdate(
        snapshot.docs.map((doc) => ({ id: doc.id, ...doc.data() }) as Post),
      );
    },
    (error) => {
      onError(new Error(`Listener failed: ${error.message}`));
    },
  );
}

// Always store and call the unsubscribe function
const unsubscribe = subscribeToPublishedPosts(handler, errorHandler);
unsubscribe(); // Cleanup when done
```

**Why good:** Returns `Unsubscribe` for cleanup, separate error callback, typed parameters

> Real-time chat implementation: [examples/firestore.md](examples/firestore.md)

---

### Pattern 4: Firestore Transactions and Batched Writes

Use transactions for atomic read-then-write operations. Use batched writes for multiple writes without reads.

```typescript
// Transaction: atomic read-then-write
await runTransaction(db, async (transaction) => {
  const postSnap = await transaction.get(postRef);
  if (!postSnap.exists()) throw new Error("Not found");
  transaction.update(postRef, { likeCount: increment(1) });
  transaction.set(likeRef, { createdAt: serverTimestamp() });
});

// Batch: multiple writes (up to 500)
const batch = writeBatch(db);
for (const id of postIds.slice(0, MAX_BATCH_SIZE)) {
  batch.delete(doc(db, POSTS_COLLECTION, id));
}
await batch.commit();
```

**Why good:** Transaction ensures atomicity, `increment()` for safe counters, batch for bulk operations

> Full examples: [examples/firestore.md](examples/firestore.md)

---

### Pattern 5: Authentication Flows

Use Firebase Authentication with the modular SDK. Handle auth state changes with `onAuthStateChanged`.

```typescript
// Sign up / Sign in / Sign out
const credential = await createUserWithEmailAndPassword(auth, email, password);
const credential = await signInWithEmailAndPassword(auth, email, password);
await signOut(auth);

// OAuth
const result = await signInWithPopup(auth, new GoogleAuthProvider());

// Listen to auth state -- register early in app lifecycle
const unsubscribe = onAuthStateChanged(auth, (user) => {
  /* ... */
});

// Get ID token for API calls
const token = await auth.currentUser?.getIdToken(/* forceRefresh */ true);
```

**Why good:** Modular imports, typed `User` return values, `Unsubscribe` for cleanup

> Full auth context with React: [examples/auth.md](examples/auth.md)

---

### Pattern 6: Cloud Functions v2

Write Cloud Functions using the v2 API. Import from `firebase-functions/v2/*` subpackages.

```typescript
// HTTP function
import { onRequest } from "firebase-functions/v2/https";
export const getPosts = onRequest(
  { cors: true, region: "us-central1" },
  async (req, res) => {
    /* ... */
  },
);

// Callable function (with auth)
import { onCall, HttpsError } from "firebase-functions/v2/https";
export const createPost = onCall({ region: "us-central1" }, async (request) => {
  if (!request.auth)
    throw new HttpsError("unauthenticated", "Must be signed in");
  /* ... */
});

// Firestore trigger
import { onDocumentCreated } from "firebase-functions/v2/firestore";
export const onPostCreated = onDocumentCreated(
  { document: "posts/{postId}", region: "us-central1" },
  async (event) => {
    /* ... */
  },
);

// Scheduled function
import { onSchedule } from "firebase-functions/v2/scheduler";
export const cleanup = onSchedule(
  { schedule: "every 24 hours", region: "us-central1" },
  async () => {
    /* ... */
  },
);
```

**Why good:** v2 imports from subpackages, region specified, `HttpsError` for callable error handling

> Full Cloud Functions API: [examples/functions.md](examples/functions.md)

---

### Pattern 7: Firebase Admin SDK (Server-Side)

Use the Admin SDK in Cloud Functions or trusted server environments. Bypasses all security rules.

```typescript
import { initializeApp } from "firebase-admin/app";
import { getFirestore } from "firebase-admin/firestore";
import { getAuth } from "firebase-admin/auth";

initializeApp(); // Default credentials in Cloud Functions
export const adminDb = getFirestore();
export const adminAuth = getAuth();

// Custom claims for role-based access
await adminAuth.setCustomUserClaims(uid, { admin: true });
// Verify client ID tokens
const decoded = await adminAuth.verifyIdToken(idToken);
```

**Why good:** Modular Admin SDK imports, default credentials in Cloud Functions, custom claims for RBAC

> Full Admin SDK patterns: [examples/functions.md](examples/functions.md)

---

### Pattern 8: Firebase Storage

Upload, download, and manage files with Firebase Storage.

```typescript
import { ref, uploadBytesResumable, getDownloadURL } from "firebase/storage";

const storageRef = ref(storage, `avatars/${userId}/avatar.png`);
const uploadTask = uploadBytesResumable(storageRef, file, {
  contentType: file.type,
  customMetadata: { uploadedBy: userId },
});

uploadTask.on("state_changed", (snapshot) => {
  const PERCENT_MULTIPLIER = 100;
  const percent =
    (snapshot.bytesTransferred / snapshot.totalBytes) * PERCENT_MULTIPLIER;
  onProgress(percent);
});
```

**Why good:** Resumable upload with progress, `customMetadata` for audit trail, named constants

> Full upload/download/delete with validation: [examples/storage.md](examples/storage.md)

---

### Pattern 9: Security Rules

Firestore and Storage security rules are your primary access control mechanism.

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    function isAuthenticated() { return request.auth != null; }
    function isOwner(userId) { return request.auth.uid == userId; }

    match /posts/{postId} {
      allow read: if resource.data.published == true
                  || isOwner(resource.data.authorId);
      allow create: if isAuthenticated()
                    && request.resource.data.authorId == request.auth.uid;
      allow update: if isOwner(resource.data.authorId);
      allow delete: if isOwner(resource.data.authorId);
    }
  }
}
```

**Why good:** Helper functions, granular CRUD permissions, ownership checks, data validation

> Full Firestore + Storage rules: [examples/security-rules.md](examples/security-rules.md)

</patterns>

---

<performance>

## Performance Optimization

### Query Performance

- **Use composite indexes** -- Compound queries (multiple `where` + `orderBy`) need composite indexes. Deploy via `firestore.indexes.json` or let Firestore error messages guide you with auto-generated index links.
- **Limit result sets** -- Always use `limit()` to cap query results. Unbounded queries fetch all matching documents.
- **Paginate with cursors** -- Use `startAfter()` with the last document snapshot for efficient pagination instead of `offset()`.
- **Select specific fields** -- Use `select()` in Admin SDK queries to fetch only needed fields (client SDK always fetches full documents).

### Bundle Size

- **Use `initializeAuth` for granular control** -- `getAuth()` enables all auth methods by default. Use `initializeAuth()` with only the providers you need for smaller bundles.
- **Use `firebase/firestore/lite`** -- If you don't need real-time listeners, import from `firebase/firestore/lite` for a smaller Firestore bundle (no `onSnapshot`).

### Cloud Functions

- **Minimize cold starts** -- Use `onInit()` for lazy initialization. Keep function dependencies small. Consider "fat functions" (one entry point routing to handlers) over many small functions.
- **Set appropriate memory/timeout** -- Configure `memory` and `timeoutSeconds` in function options instead of using defaults.
- **Use global variables for reusable connections** -- Initialize Admin SDK and database connections outside the function handler so they persist across invocations.

</performance>

---

<decision_framework>

## Decision Framework

### Firestore vs Realtime Database

```
What does your app need?
+-- Complex queries (where, orderBy, compound) --> Firestore
+-- Simple key-value lookups with low latency --> Realtime Database
+-- Offline support with rich queries --> Firestore
+-- Presence system (online/offline status) --> Realtime Database
+-- Multi-region availability --> Firestore
+-- Very frequent small updates (typing indicators) --> Realtime Database
+-- For most new projects --> Firestore (recommended default)
```

### Auth Method Selection

```
What auth flow does the user need?
+-- Email + Password --> createUserWithEmailAndPassword / signInWithEmailAndPassword
+-- Social login (Google, GitHub, etc.) --> signInWithPopup / signInWithRedirect
+-- Phone + SMS --> signInWithPhoneNumber (requires reCAPTCHA)
+-- Email link (passwordless) --> sendSignInLinkToEmail
+-- Custom backend auth --> Admin SDK createCustomToken + client signInWithCustomToken
+-- Anonymous (guest) --> signInAnonymously (upgrade later with linkWithCredential)
```

### Cloud Functions: onRequest vs onCall

```
Who is calling the function?
+-- External webhooks, third-party services --> onRequest (raw HTTP)
+-- Your own client app (web/mobile) --> onCall (automatic auth, input validation)
+-- Firestore document changes --> onDocumentCreated / onDocumentUpdated / onDocumentDeleted
+-- Scheduled/cron tasks --> onSchedule
+-- Authentication events --> onUserCreated / onUserDeleted (from firebase-functions/v2/identity)
```

### Client SDK vs Admin SDK

```
Where is the code running?
+-- Browser / Client-side --> Client SDK (firebase) -- security rules enforced
+-- Cloud Functions --> Admin SDK (firebase-admin) -- bypasses security rules
+-- API server / backend --> Admin SDK (firebase-admin) -- use service account
+-- NEVER use Admin SDK in client code --> It bypasses all security
```

### Storage: When to Use Firebase Storage

```
What kind of files?
+-- User-generated content (avatars, uploads) --> Firebase Storage with security rules
+-- Public static assets (CSS, images) --> Firebase Hosting (faster CDN)
+-- Large files with progress tracking --> Firebase Storage with uploadBytesResumable
+-- Server-generated files (reports, exports) --> Firebase Storage via Admin SDK
```

</decision_framework>

---

<integration>

## Integration Guide

**Firebase ecosystem integration:**

- **Firebase Hosting + Cloud Functions**: Rewrite rules in `firebase.json` route requests to functions
- **App Check**: Protect your backend resources from abuse by verifying requests come from your app (`initializeAppCheck` with reCAPTCHA Enterprise)
- **Firebase Extensions**: Pre-built Cloud Functions for common tasks (payments, image resizing, email sending)

**Client framework integration:**

- Use `onAuthStateChanged` in your framework's lifecycle (e.g., context provider, composable, store) to track auth state
- Firestore `onSnapshot` listeners require cleanup when components unmount -- use your framework's cleanup mechanism
- Wrap Firestore reads in your data fetching solution's query functions for caching and real-time invalidation

**Replaces / Conflicts with:**

- **Supabase**: Alternative BaaS -- don't use both for the same purpose
- **AWS Amplify**: Alternative BaaS -- pick one platform
- **Custom auth providers**: Firebase Auth can replace third-party auth, or vice versa -- don't mix auth providers

</integration>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Wide-open security rules in production** -- The default test-mode rules (`allow read, write: if true`) give everyone full access to your entire database. This is the single most common Firebase security vulnerability.
- **Admin SDK credentials in client code** -- Service account keys or Admin SDK imports in browser bundles give attackers full bypass of all security rules.
- **Using the compat/namespace API** -- `firebase/compat/*` imports prevent tree-shaking, bundling the entire SDK. The compat layer will be removed in a future major version.
- **Not handling auth state changes** -- Calling Firestore without waiting for `onAuthStateChanged` can result in unauthenticated requests that fail silently against security rules.

**Medium Priority Issues:**

- **Using v1 Cloud Functions API** -- v1 (`functions.https.onRequest`) lacks concurrency, traffic splitting, and longer timeouts. All new functions should use v2 (`firebase-functions/v2/https`).
- **Not unsubscribing from `onSnapshot`** -- Leaked listeners keep WebSocket connections open, consume bandwidth, and cause memory leaks.
- **Unbounded queries** -- Queries without `limit()` can fetch thousands of documents, causing performance issues and high read costs.
- **Monotonically increasing document IDs** -- Sequential IDs like `user1`, `user2` create hotspots. Use Firestore auto-generated IDs or UUIDs.
- **Using `functions.config()`** -- Deprecated and will fail after March 2027. Use Cloud Secret Manager (`defineSecret()`) or environment variables.

**Common Mistakes:**

- **Not adding `.select()` after Admin SDK queries** -- Without `select()`, all document fields are returned, increasing data transfer.
- **Calling `getFirestore()` on every operation** -- Initialize once and reuse the instance. Each call creates overhead.
- **Missing composite indexes** -- Compound queries fail at runtime if the required composite index doesn't exist. Check error messages for the auto-generated index creation link.
- **Deploying without testing security rules** -- Use the emulator to test rules before deploying. Use `firebase emulators:exec "npm test"` in CI.
- **Using `enableIndexedDbPersistence`** -- Deprecated. Use `initializeFirestore` with `persistentLocalCache` instead.

**Gotchas & Edge Cases:**

- **Firestore queries are "all or nothing" with security rules** -- If a query could potentially return documents the user isn't allowed to read, the entire query fails (not just the unauthorized documents).
- **Firestore limits** -- 1 MB max document size, 20,000 fields per document, 500 writes per batch, 1 write per second per document sustained.
- **Security rules propagation delay** -- Rule updates take up to 1 minute to affect new queries, and up to 10 minutes for active listeners.
- **`serverTimestamp()` returns `null` in `onSnapshot` pending writes** -- Until the server confirms the write, the timestamp field is `null` locally. Handle this with `{ serverTimestamps: 'estimate' }` in snapshot options.
- **Firebase Hosting has a 60-second timeout** -- Even if your Cloud Function has a longer timeout, requests through Hosting rewrites timeout at 60 seconds.
- **`onAuthStateChanged` fires on page load** -- It fires with `null` initially, then with the user if a session exists. Always handle the initial `null` state.
- **Firestore `in` queries are limited to 30 values** -- `where("field", "in", array)` supports a maximum of 30 elements in the array (increased from 10 in recent versions).
- **Cloud Functions cold starts** -- First invocation after idle has additional latency. Use `onInit()` for lazy initialization and keep dependencies minimal.
- **Admin SDK `initializeApp()` should be called once** -- Multiple calls throw an error unless you provide a unique app name. Guard with a try-catch or check `getApps().length`.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use the modular Firebase SDK imports (`firebase/app`, `firebase/firestore`, `firebase/auth`) -- NEVER use the deprecated `firebase/compat` namespace API)**

**(You MUST write Firestore security rules for EVERY collection -- a collection without rules is wide open in production)**

**(You MUST NEVER expose Firebase Admin SDK credentials or service account keys in client-side code)**

**(You MUST use Cloud Functions v2 API (`firebase-functions/v2/https`, `firebase-functions/v2/firestore`) -- NOT the deprecated v1 API)**

**(You MUST handle all Firestore operations with error checking -- never assume reads/writes succeed)**

**Failure to follow these rules will create security vulnerabilities, bloated bundles, deprecated code paths, and silent runtime failures.**

</critical_reminders>
