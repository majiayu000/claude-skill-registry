---
name: "Google Cloud Platform & APIs"
description: "Deploy Node.js applications on Google Cloud with Cloud Run, Cloud Firestore, and Google APIs. Implement OAuth2 authentication and manage service accounts. Apply when building serverless applications, integrating Google services, or deploying to GCP."
allowed-tools: Read, Write, Edit, Bash
version: 1.1.0
compatibility: Claude Opus 4.5, Claude Code v2.x
updated: 2026-01-24
---

# Google Cloud Platform & APIs

Systematic GCP deployment for Node.js applications with serverless architecture and Google API integration.

## Overview

This Skill enforces:
- Cloud Run for serverless deployments
- Cloud Firestore for document storage
- Realtime Database for real-time data
- OAuth 2.0 authentication (user and service accounts)
- Service account management
- Google APIs integration
- Auto-scaling and cost optimization
- Security and access control

Apply when deploying to GCP, integrating Google services, or building serverless applications.

## Google Cloud Setup

### Create GCP Project

```bash
# Create project
gcloud projects create my-project --name="My Project"

# Set as active project
gcloud config set project my-project

# Enable services
gcloud services enable run.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudtasks.googleapis.com
```

## Cloud Run Deployment

### Deploy Node.js Application

```bash
# Build and deploy
gcloud run deploy my-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars NODE_ENV=production

# Check deployment
gcloud run services list
gcloud run services describe my-app --region us-central1
```

### Dockerfile for Cloud Run

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
```

### app.js Configuration

```ts
import express from 'express';

const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.send('Hello from Cloud Run!');
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

## Firestore Database

### Initialize Firestore

```ts
// lib/firestore.ts
import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
  apiKey: process.env.FIREBASE_API_KEY,
  authDomain: process.env.FIREBASE_AUTH_DOMAIN,
  projectId: process.env.FIREBASE_PROJECT_ID,
  storageBucket: process.env.FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.FIREBASE_APP_ID
};

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
```

### CRUD Operations

```ts
import {
  collection,
  addDoc,
  getDocs,
  doc,
  getDoc,
  updateDoc,
  deleteDoc,
  query,
  where
} from 'firebase/firestore';

// CREATE
async function createUser(userData: { email: string; name: string }) {
  const docRef = await addDoc(collection(db, 'users'), {
    email: userData.email,
    name: userData.name,
    createdAt: new Date()
  });
  return docRef.id;
}

// READ (single document)
async function getUser(userId: string) {
  const docRef = doc(db, 'users', userId);
  const docSnap = await getDoc(docRef);

  if (docSnap.exists()) {
    return docSnap.data();
  } else {
    throw new Error('User not found');
  }
}

// READ (collection with query)
async function getUsersByEmail(email: string) {
  const q = query(
    collection(db, 'users'),
    where('email', '==', email)
  );
  const querySnapshot = await getDocs(q);

  const users: any[] = [];
  querySnapshot.forEach(doc => {
    users.push({ id: doc.id, ...doc.data() });
  });
  return users;
}

// UPDATE
async function updateUser(userId: string, updates: any) {
  const userRef = doc(db, 'users', userId);
  await updateDoc(userRef, {
    ...updates,
    updatedAt: new Date()
  });
}

// DELETE
async function deleteUser(userId: string) {
  await deleteDoc(doc(db, 'users', userId));
}
```

## Realtime Database

### Firebase Realtime Setup

```ts
// lib/realtime-db.ts
import { initializeApp } from 'firebase/app';
import { getDatabase, ref, onValue, set, update, remove } from 'firebase/database';

const app = initializeApp(firebaseConfig);
export const realtimeDb = getDatabase(app);

// Real-time listener
function subscribeToPresence(userId: string, callback: (data: any) => void) {
  const presenceRef = ref(realtimeDb, `presence/${userId}`);
  const unsubscribe = onValue(presenceRef, snapshot => {
    callback(snapshot.val());
  });

  return unsubscribe;
}

// Write data
async function setUserStatus(userId: string, status: string) {
  const statusRef = ref(realtimeDb, `status/${userId}`);
  await set(statusRef, {
    status,
    lastUpdated: new Date().toISOString()
  });
}
```

## Google OAuth 2.0 (User Authentication)

### Setup OAuth Credentials

1. Go to Google Cloud Console → APIs & Services → Credentials
2. Create OAuth 2.0 Client ID
3. Set authorized redirect URIs

### OAuth Implementation

```ts
// lib/google-oauth.ts
import { google } from 'googleapis';
import session from 'express-session';

const oauth2Client = new google.auth.OAuth2(
  process.env.GOOGLE_CLIENT_ID,
  process.env.GOOGLE_CLIENT_SECRET,
  process.env.GOOGLE_REDIRECT_URL
);

// Route: Start OAuth flow
app.get('/auth/google', (req, res) => {
  const scopes = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
  ];

  const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: scopes,
    include_granted_scopes: true
  });

  res.redirect(authUrl);
});

// Route: OAuth callback
app.get('/auth/callback', async (req, res) => {
  const { code } = req.query;

  try {
    const { tokens } = await oauth2Client.getToken(code as string);
    oauth2Client.setCredentials(tokens);

    // Use tokens to get user info
    const oauth2 = google.oauth2({
      auth: oauth2Client,
      version: 'v2'
    });

    const userinfo = await oauth2.userinfo.get();

    req.session.user = userinfo.data;
    req.session.tokens = tokens;

    res.redirect('/dashboard');
  } catch (error) {
    console.error('OAuth error:', error);
    res.status(500).send('Authentication failed');
  }
});

// Middleware: Check authentication
export function requireAuth(req: any, res: any, next: any) {
  if (!req.session.user) {
    return res.redirect('/auth/google');
  }
  next();
}
```

## Google Service Accounts (Server-to-Server)

### Create Service Account

```bash
# Create service account
gcloud iam service-accounts create my-service-account \
  --display-name="My Service Account"

# Create key file
gcloud iam service-accounts keys create key.json \
  --iam-account=my-service-account@my-project.iam.gserviceaccount.com

# Grant permissions
gcloud projects add-iam-policy-binding my-project \
  --member="serviceAccount:my-service-account@my-project.iam.gserviceaccount.com" \
  --role="roles/editor"
```

### Use Service Account

```ts
// lib/service-account.ts
import { google } from 'googleapis';

const serviceAccount = require('./key.json');

const auth = new google.auth.GoogleAuth({
  keyFile: './key.json',
  scopes: [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/calendar'
  ]
});

const drive = google.drive({ version: 'v3', auth });
const calendar = google.calendar({ version: 'v3', auth });

// Example: List Google Drive files
export async function listDriveFiles() {
  const res = await drive.files.list({
    pageSize: 10,
    fields: 'files(id, name)'
  });

  return res.data.files;
}

// Example: Create calendar event
export async function createCalendarEvent(calendarId: string, event: any) {
  const res = await calendar.events.insert({
    calendarId,
    requestBody: {
      summary: event.title,
      description: event.description,
      start: { dateTime: event.startTime },
      end: { dateTime: event.endTime }
    }
  });

  return res.data;
}
```

## Google APIs Examples

### Gmail API

```ts
// Send email
export async function sendEmail(to: string, subject: string, body: string) {
  const message = [
    `To: ${to}`,
    `Subject: ${subject}`,
    '',
    body
  ].join('\n');

  const encodedMessage = Buffer.from(message)
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_');

  const res = await gmail.users.messages.send({
    userId: 'me',
    requestBody: {
      raw: encodedMessage
    }
  });

  return res.data;
}
```

### Sheets API

```ts
// Write to Google Sheet
export async function writeToSheet(spreadsheetId: string, values: any[]) {
  const res = await sheets.spreadsheets.values.append({
    spreadsheetId,
    range: 'Sheet1!A1',
    valueInputOption: 'RAW',
    requestBody: { values }
  });

  return res.data;
}

// Read from Google Sheet
export async function readFromSheet(spreadsheetId: string) {
  const res = await sheets.spreadsheets.values.get({
    spreadsheetId,
    range: 'Sheet1'
  });

  return res.data.values;
}
```

## Environment Variables

### .env Configuration

```bash
# Google Cloud
GCP_PROJECT_ID=my-project
GCP_REGION=us-central1

# Firebase
FIREBASE_API_KEY=xxx
FIREBASE_AUTH_DOMAIN=xxx.firebaseapp.com
FIREBASE_PROJECT_ID=my-project
FIREBASE_STORAGE_BUCKET=xxx.appspot.com
FIREBASE_MESSAGING_SENDER_ID=xxx
FIREBASE_APP_ID=xxx

# OAuth
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxx
GOOGLE_REDIRECT_URL=http://localhost:3000/auth/callback

# Service Account
GOOGLE_APPLICATION_CREDENTIALS=./key.json
```

## Deployment with CI/CD

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_SERVICE_ACCOUNT_KEY }}

      - name: Deploy to Cloud Run
        uses: google-github-actions/deploy-cloudrun@v1
        with:
          service: my-app
          region: us-central1
          image: gcr.io/${{ secrets.GCP_PROJECT_ID }}/my-app
          env_vars: |
            NODE_ENV=production
            FIREBASE_PROJECT_ID=${{ secrets.GCP_PROJECT_ID }}
```

## Anti-Patterns

```ts
// ❌ BAD: Hardcoded credentials
const oauth2Client = new google.auth.OAuth2(
  'hardcoded-client-id',
  'hardcoded-secret',
  'http://localhost:3000/callback'
);

// ✅ GOOD: Use environment variables
const oauth2Client = new google.auth.OAuth2(
  process.env.GOOGLE_CLIENT_ID,
  process.env.GOOGLE_CLIENT_SECRET,
  process.env.GOOGLE_REDIRECT_URL
);

// ❌ BAD: No error handling
const tokens = await oauth2Client.getToken(code);
// Crashes if getToken fails

// ✅ GOOD: Error handling
try {
  const { tokens } = await oauth2Client.getToken(code);
  oauth2Client.setCredentials(tokens);
} catch (error) {
  console.error('OAuth error:', error);
  res.status(500).send('Authentication failed');
}

// ❌ BAD: Querying all documents
const allUsers = await getDocs(collection(db, 'users'));

// ✅ GOOD: Filter with where clause
const q = query(collection(db, 'users'), where('active', '==', true));
const activeUsers = await getDocs(q);
```

## Verification Before Production

- [ ] Service account created with appropriate permissions
- [ ] OAuth credentials configured with redirect URIs
- [ ] Firestore indexes created for queries
- [ ] Environment variables configured
- [ ] HTTPS enabled for OAuth callback
- [ ] Error handling for API calls
- [ ] Rate limiting configured
- [ ] Cloud Run health checks configured
- [ ] CI/CD pipeline set up
- [ ] Secrets managed securely (not in code)

## Integration with Project Standards

Enforces security and deployment best practices:
- S-5: Secrets in environment variables
- No hardcoded credentials
- Service account least-privilege access
- OAuth2 standard compliance

## Resources

- Google Cloud Run: https://cloud.google.com/run/docs
- Firebase: https://firebase.google.com/docs
- Google APIs: https://developers.google.com/apis-explorer
- OAuth 2.0: https://developers.google.com/identity/protocols/oauth2
---

**Last Updated:** January 24, 2026
**Compatibility:** Claude Opus 4.5, Claude Code v2.x
**Status:** Production Ready

> **January 2026 Update:** This skill is compatible with Claude Opus 4.5 and Claude Code v2.x. For complex tasks, use the `effort: high` parameter for thorough analysis.
