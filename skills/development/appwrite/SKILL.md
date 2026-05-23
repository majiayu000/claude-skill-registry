---
name: appwrite
description: >-
  Build backends with Appwrite — open-source Backend-as-a-Service. Use when a
  user asks to set up user authentication, manage a database without writing
  backend code, handle file storage and uploads, add realtime subscriptions, set
  up cloud functions, build a mobile or web app backend, replace Firebase with
  an open-source alternative, or self-host a BaaS platform. Covers auth,
  databases, storage, functions, realtime, and SDK integration for web, mobile,
  and server-side.
license: Apache-2.0
compatibility: 'Docker (self-hosted) or Appwrite Cloud'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: development
  tags:
    - appwrite
    - baas
    - backend
    - auth
    - database
    - storage
    - serverless
---

# Appwrite

## Overview

Appwrite is an open-source Backend-as-a-Service (BaaS) providing authentication, databases, file storage, cloud functions, and realtime subscriptions — all through a single self-hosted Docker deployment. It's the open-source alternative to Firebase, with SDKs for web (JavaScript), mobile (Flutter, Swift, Kotlin), and server-side (Node.js, Python, PHP). This skill covers self-hosting setup, authentication, database operations, file storage, serverless functions, and realtime subscriptions.

## Instructions

### Step 1: Self-Hosted Deployment

```bash
# One-command Docker setup
docker run -it --rm \
  --volume /var/run/docker.sock:/var/run/docker.sock \
  --volume "$(pwd)/appwrite:/usr/src/code/appwrite:rw" \
  --entrypoint="install" \
  appwrite/appwrite:latest

# Or with Docker Compose (production)
curl -o docker-compose.yml https://appwrite.io/install/compose
curl -o .env https://appwrite.io/install/env
docker compose up -d

# Console: http://localhost/console
# Create your first project in the console UI
```

### Step 2: Authentication

```javascript
// lib/appwrite.js — Client SDK setup and authentication
import { Client, Account, ID } from 'appwrite'

const client = new Client()
  .setEndpoint('http://localhost/v1')    // Appwrite API endpoint
  .setProject('your-project-id')         // from console

const account = new Account(client)

// Sign up
async function signUp(email, password, name) {
  const user = await account.create(ID.unique(), email, password, name)
  // Auto-login after signup
  await account.createEmailPasswordSession(email, password)
  return user
}

// Login
async function login(email, password) {
  return await account.createEmailPasswordSession(email, password)
}

// OAuth login (Google, GitHub, Apple, etc.)
account.createOAuth2Session('google', 'http://localhost:3000/callback', 'http://localhost:3000/login')

// Get current user
async function getCurrentUser() {
  try {
    return await account.get()
  } catch {
    return null    // not logged in
  }
}

// Logout
async function logout() {
  await account.deleteSession('current')
}
```

### Step 3: Database Operations

```javascript
// lib/database.js — CRUD operations with Appwrite Databases
import { Client, Databases, ID, Query } from 'appwrite'

const client = new Client()
  .setEndpoint('http://localhost/v1')
  .setProject('your-project-id')

const databases = new Databases(client)

const DB_ID = 'main'
const COLLECTION_ID = 'posts'

// Create document
async function createPost(title, content, authorId) {
  return await databases.createDocument(DB_ID, COLLECTION_ID, ID.unique(), {
    title,
    content,
    author_id: authorId,
    status: 'draft',
    created_at: new Date().toISOString(),
  })
}

// List with filters and pagination
async function listPublishedPosts(page = 1, limit = 10) {
  return await databases.listDocuments(DB_ID, COLLECTION_ID, [
    Query.equal('status', 'published'),
    Query.orderDesc('created_at'),
    Query.limit(limit),
    Query.offset((page - 1) * limit),
  ])
}

// Update
async function publishPost(postId) {
  return await databases.updateDocument(DB_ID, COLLECTION_ID, postId, {
    status: 'published',
    published_at: new Date().toISOString(),
  })
}

// Delete
async function deletePost(postId) {
  await databases.deleteDocument(DB_ID, COLLECTION_ID, postId)
}
```

### Step 4: File Storage

```javascript
// lib/storage.js — Upload and manage files
import { Client, Storage, ID } from 'appwrite'

const storage = new Storage(new Client()
  .setEndpoint('http://localhost/v1')
  .setProject('your-project-id'))

const BUCKET_ID = 'uploads'

// Upload file
async function uploadFile(file) {
  /**
   * Upload a file to Appwrite storage.
   * Args:
   *   file: File object from <input type="file"> or drag-and-drop
   */
  return await storage.createFile(BUCKET_ID, ID.unique(), file)
}

// Get file URL (with transformations for images)
function getFilePreview(fileId, width = 400, height = 300) {
  return storage.getFilePreview(BUCKET_ID, fileId, width, height)
}

// Download file
function getFileDownload(fileId) {
  return storage.getFileDownload(BUCKET_ID, fileId)
}

// Delete file
async function deleteFile(fileId) {
  await storage.deleteFile(BUCKET_ID, fileId)
}
```

### Step 5: Cloud Functions

```javascript
// functions/on-order-created/src/main.js — Serverless function triggered by database event
// Deploy via Appwrite CLI: appwrite deploy function

import { Client, Databases, Users } from 'node-appwrite'

export default async ({ req, res, log, error }) => {
  const client = new Client()
    .setEndpoint(process.env.APPWRITE_ENDPOINT)
    .setProject(process.env.APPWRITE_PROJECT)
    .setKey(process.env.APPWRITE_API_KEY)

  const payload = JSON.parse(req.body)
  const order = payload.$id ? payload : payload.data

  log(`New order: ${order.$id}, total: ${order.total}`)

  // Send notification, update inventory, etc.
  const users = new Users(client)
  const user = await users.get(order.user_id)
  log(`Order by: ${user.email}`)

  return res.json({ success: true, orderId: order.$id })
}
```

### Step 6: Realtime Subscriptions

```javascript
// hooks/useRealtime.js — Subscribe to live database changes
import { Client } from 'appwrite'

const client = new Client()
  .setEndpoint('http://localhost/v1')
  .setProject('your-project-id')

// Subscribe to changes in a collection
const unsubscribe = client.subscribe(
  'databases.main.collections.messages.documents',
  (response) => {
    // Fires on create, update, delete
    const event = response.events[0]
    const document = response.payload

    if (event.includes('.create')) {
      console.log('New message:', document)
    } else if (event.includes('.update')) {
      console.log('Updated:', document)
    } else if (event.includes('.delete')) {
      console.log('Deleted:', document.$id)
    }
  }
)

// Cleanup
// unsubscribe()
```

## Examples

### Example 1: Build a full-stack app with auth, database, and file uploads
**User prompt:** "I want to build a recipe sharing app. Users sign up, post recipes with photos, and browse others' recipes. Use an open-source backend I can self-host."

The agent will:
1. Deploy Appwrite with Docker Compose.
2. Set up authentication with email/password and Google OAuth.
3. Create database collections: recipes (title, ingredients, steps, author, image_id), users.
4. Configure file storage bucket for recipe photos with size limits.
5. Build a Next.js frontend using the Appwrite Web SDK.
6. Set permissions so users can only edit their own recipes but read all published ones.

### Example 2: Replace Firebase with a self-hosted alternative
**User prompt:** "We're using Firebase but want to self-host for data sovereignty. Migrate our auth, Firestore, and storage to something open-source."

The agent will:
1. Deploy Appwrite on the target server.
2. Export users from Firebase Auth, import to Appwrite.
3. Map Firestore collections to Appwrite database collections.
4. Migrate storage files using the Appwrite Server SDK.
5. Update frontend code to use Appwrite SDK (similar API surface to Firebase).

## Guidelines

- Appwrite runs as a set of Docker containers (API, worker, database, cache, etc.). It needs ~2GB RAM minimum for comfortable operation. Use Docker Compose for managing the full stack.
- Configure database indexes in the Appwrite console for fields you filter or sort on — queries on unindexed fields will be slow at scale.
- Use Appwrite's permission system (`read("any")`, `write("user:USER_ID")`) to control document access. Default is owner-only — explicitly set permissions for public content.
- Server SDKs (Node.js, Python) use API keys and bypass permissions — use them for admin operations, cron jobs, and cloud functions. Client SDKs enforce user permissions.
- Appwrite handles auth tokens, session management, and OAuth flows internally. You don't need to manage JWTs or refresh tokens manually.
