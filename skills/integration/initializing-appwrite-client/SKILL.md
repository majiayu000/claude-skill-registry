---
name: initializing-appwrite-client
description: Initializes the Appwrite Client using Singleton or Provider patterns for Next.js 15. Use whenever setting up the backend connection.
---

# Appwrite Client Initialization

## When to use this skill
- Setting up the initial SDK connection.
- Creating instances for client components vs. server actions.

## Workflow
- [ ] Query `context7` for the latest singleton pattern.
- [ ] Create `lib/appwrite.ts` for shared client instance.
- [ ] Create `lib/server/appwrite.ts` for server-side SDK (using API Key).

## Code Template (Client Context)
```typescript
import { Client, Account, Databases, Storage } from 'appwrite';

export const client = new Client()
    .setEndpoint(process.env.NEXT_PUBLIC_APPWRITE_ENDPOINT!)
    .setProject(process.env.NEXT_PUBLIC_APPWRITE_PROJECT_ID!);

export const account = new Account(client);
export const databases = new Databases(client);
export const storage = new Storage(client);
```

## Instructions
- **Singleton**: Export single instances of services to avoid multiple connections.
- **Server Side**: Use `node-appwrite` in server actions with the secret API key.
