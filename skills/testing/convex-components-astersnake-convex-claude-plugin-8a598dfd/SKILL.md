---
name: convex-components
description: Convex Components - Presence, ProseMirror/BlockNote collaborative editing,
  and Resend email integration
---

---
name: convex-components
description: Convex Components - Presence, ProseMirror/BlockNote collaborative editing, and Resend email integration
globs:
  - "convex/**/*.ts"
  - "convex/convex.config.ts"
  - "**/*.tsx"
triggers:
  - presence
  - prosemirror
  - blocknote
  - resend
  - email
  - collaborative
  - real-time editing
  - facepile
  - convex.config.ts
  - defineApp
  - components
  - @convex-dev/presence
  - @convex-dev/prosemirror-sync
  - @convex-dev/resend
---

# Convex Components Overview

Convex Components package up code and data in a sandbox that allows you to confidently and quickly add new features to your backend.

## Key Principles

- Components are like mini self-contained Convex backends
- Installing them is always safe - they can't read your app's tables or call your app's functions unless you pass them in explicitly
- Each component is installed as its own independent library from NPM
- You need to add a `convex/convex.config.ts` file that includes the component
- ALWAYS prefer using a component for a feature than writing the code yourself
- You do NOT need to deploy a component to use it - you can use it after installation
- You can use multiple components in the same project

## Supported Components

1. **proseMirror** - A collaborative text editor component
2. **presence** - A component for managing presence functionality (live-updating list of users in a "room")
3. **resend** - A component for sending emails

---

# Presence Component

A Convex component for managing presence functionality - a live-updating list of users in a "room" including their status for when they were last online.

## Why Use This Component

It can be tricky to implement presence efficiently without polling and without re-running queries every time a user sends a heartbeat message. This component implements presence via Convex scheduled functions such that clients only receive updates when a user joins or leaves the room.

## Installation

```bash
npm install @convex-dev/presence
```

## Configuration

Add the component to your Convex app in `convex/convex.config.ts`:

```typescript
import { defineApp } from "convex/server";
import presence from "@convex-dev/presence/convex.config";

const app = defineApp();
app.use(presence);
export default app;
```

## Backend Setup

Create `convex/presence.ts`:

```typescript
import { mutation, query } from "./_generated/server";
import { components } from "./_generated/api";
import { v } from "convex/values";
import { Presence } from "@convex-dev/presence";
import { getAuthUserId } from "@convex-dev/auth/server";
import { Id } from "./_generated/dataModel";

export const presence = new Presence(components.presence);

export const getUserId = query({
  args: {},
  returns: v.union(v.string(), v.null()),
  handler: async (ctx) => {
    return await getAuthUserId(ctx);
  },
});

export const heartbeat = mutation({
  args: {
    roomId: v.string(),
    userId: v.string(),
    sessionId: v.string(),
    interval: v.number(),
  },
  returns: v.string(),
  handler: async (ctx, { roomId, userId, sessionId, interval }) => {
    const authUserId = await getAuthUserId(ctx);
    if (!authUserId) {
      throw new Error("Not authenticated");
    }
    return await presence.heartbeat(ctx, roomId, authUserId, sessionId, interval);
  },
});

export const list = query({
  args: { roomToken: v.string() },
  handler: async (ctx, { roomToken }) => {
    const presenceList = await presence.list(ctx, roomToken);
    const listWithUserInfo = await Promise.all(
      presenceList.map(async (entry) => {
        const user = await ctx.db.get(entry.userId as Id<"users">);
        if (!user) {
          return entry;
        }
        return {
          ...entry,
          name: user?.name,
          image: user?.image,
        };
      })
    );
    return listWithUserInfo;
  },
});

export const disconnect = mutation({
  args: { sessionToken: v.string() },
  returns: v.null(),
  handler: async (ctx, { sessionToken }) => {
    await presence.disconnect(ctx, sessionToken);
    return null;
  },
});
```

## React Component Usage

```tsx
// src/App.tsx
import { useQuery } from "convex/react";
import { api } from "../convex/_generated/api";
import usePresence from "@convex-dev/presence/react";
import FacePile from "@convex-dev/presence/facepile";

export default function App(): React.ReactElement {
  const userId = useQuery(api.presence.getUserId);

  return (
    <main>
      {userId && <PresenceIndicator userId={userId} />}
    </main>
  );
}

function PresenceIndicator({ userId }: { userId: string }) {
  const presenceState = usePresence(api.presence, "my-chat-room", userId);
  return <FacePile presenceState={presenceState ?? []} />;
}
```

## usePresence Hook Signature

```typescript
export default function usePresence(
  presence: PresenceAPI,
  roomId: string,
  userId: string,
  interval: number = 10000,
  convexUrl?: string
): PresenceState[] | undefined
```

## Best Practice

ALWAYS use the `FacePile` UI component included with this package unless the user explicitly requests a custom presence UI. You can copy the code and use the `usePresence` hook directly to implement your own styling.

---

# ProseMirror/BlockNote Component

A Convex Component that syncs a ProseMirror document between clients via a Tiptap extension (also works with BlockNote).

## Features

- Collaborative editing that syncs to the cloud
- Users can edit the same document in multiple tabs or devices
- Data lives in your Convex database alongside the rest of your app's data

## Installation

```bash
npm install @convex-dev/prosemirror-sync
```

## Configuration

Create `convex/convex.config.ts`:

```typescript
import { defineApp } from 'convex/server';
import prosemirrorSync from '@convex-dev/prosemirror-sync/convex.config';

const app = defineApp();
app.use(prosemirrorSync);

export default app;
```

**IMPORTANT:** You do NOT need to add component tables to your `schema.ts`. The component tables are only read and written to from the component functions.

## Backend Setup

Create `convex/prosemirror.ts`:

```typescript
import { components } from './_generated/api';
import { ProsemirrorSync } from '@convex-dev/prosemirror-sync';
import { DataModel } from "./_generated/dataModel";
import { GenericQueryCtx, GenericMutationCtx } from 'convex/server';
import { getAuthUserId } from "@convex-dev/auth/server";

const prosemirrorSync = new ProsemirrorSync(components.prosemirrorSync);

// Optional: Define permission checks
async function checkPermissions(ctx: GenericQueryCtx<DataModel>, id: string) {
  const userId = await getAuthUserId(ctx);
  if (!userId) {
    throw new Error("Unauthorized");
  }
  // Add your own authorization logic here
}

export const {
  getSnapshot,
  submitSnapshot,
  latestVersion,
  getSteps,
  submitSteps
} = prosemirrorSync.syncApi<DataModel>({
  checkRead: checkPermissions,
  checkWrite: checkPermissions,
  onSnapshot: async (ctx, id, snapshot, version) => {
    // Optional: Called when a new snapshot is available
    console.log(`Document ${id} updated to version ${version}`);
  },
});
```

**IMPORTANT:** Do NOT use any other component functions outside the functions exposed by `prosemirrorSync.syncApi`.

## React Component with BlockNote

```tsx
// src/MyComponent.tsx
import { useBlockNoteSync } from '@convex-dev/prosemirror-sync/blocknote';
import '@blocknote/core/fonts/inter.css';
import { BlockNoteView } from '@blocknote/mantine';
import '@blocknote/mantine/style.css';
import { api } from '../convex/_generated/api';
import { BlockNoteEditor } from '@blocknote/core';

function MyComponent({ id }: { id: string }) {
  const sync = useBlockNoteSync<BlockNoteEditor>(api.prosemirror, id);

  return sync.isLoading ? (
    <p>Loading...</p>
  ) : sync.editor ? (
    <BlockNoteView editor={sync.editor} />
  ) : (
    <button onClick={() => sync.create({ type: 'doc', content: [] })}>
      Create document
    </button>
  );
}

// IMPORTANT: Wrapper to re-render when id changes
export function MyComponentWrapper({ id }: { id: string }) {
  return <MyComponent key={id} id={id} />;
}
```

## sync.create Content Format

The `sync.create` function accepts an argument with `JSONContent` type. Do NOT pass it a string - it must be an object:

```typescript
export type JSONContent = {
  type?: string;
  attrs?: Record<string, any>;
  content?: JSONContent[];
  marks?: {
    type: string;
    attrs?: Record<string, any>;
    [key: string]: any;
  }[];
  text?: string;
  [key: string]: any;
};
```

Empty document example:
```typescript
sync.create({ type: 'doc', content: [] })
```

## Snapshot Debounce

The snapshot debounce interval is set to one second by default. You can specify a different interval with the `snapshotDebounceMs` option when calling `useBlockNoteSync`.

A snapshot won't be sent until:
- The document has been idle for the debounce interval
- The current user was the last to make a change

---

# Resend Email Component (Beta)

The official way to integrate the Resend email service with your Convex project.

## Features

- **Queueing**: Send as many emails as you want, as fast as you want—they'll all be delivered eventually
- **Batching**: Automatically batches large groups of emails and sends them efficiently
- **Durable execution**: Uses Convex workpools to ensure emails are eventually delivered
- **Idempotency**: Manages Resend idempotency keys to guarantee emails are delivered exactly once
- **Rate limiting**: Honors API rate limits established by Resend

## Installation

```bash
npm install @convex-dev/resend
```

## Prerequisites

1. Get a Resend account at https://resend.com
2. Register a domain at https://resend.com/domains
3. Get an API key at https://resend.com/api-keys
4. Add environment variables:
   - `RESEND_API_KEY`
   - `RESEND_DOMAIN`

## Configuration

Create or update `convex/convex.config.ts`:

```typescript
import { defineApp } from "convex/server";
import resend from "@convex-dev/resend/convex.config";

const app = defineApp();
app.use(resend);

export default app;
```

## Backend Setup

Create `convex/sendEmails.ts`:

```typescript
import { components, internal } from "./_generated/api";
import { Resend, vEmailId, vEmailEvent } from "@convex-dev/resend";
import { internalMutation } from "./_generated/server";
import { v } from "convex/values";

export const resend: Resend = new Resend(components.resend, {
  // Set testMode: false to send to real addresses (default is true)
  testMode: true,
  onEmailEvent: internal.sendEmails.handleEmailEvent,
});

export const sendTestEmail = internalMutation({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    await resend.sendEmail(
      ctx,
      `Me <test@${process.env.RESEND_DOMAIN}>`,
      "Resend <delivered@resend.dev>",
      "Hi there",
      "This is a test email"
    );
    return null;
  },
});

// Handle email status events (requires webhook setup)
export const handleEmailEvent = internalMutation({
  args: {
    id: vEmailId,
    event: vEmailEvent,
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    console.log("Email event:", args.id, args.event);
    // Handle the event (delivered, bounced, etc.)
    return null;
  },
});
```

## Webhook Setup (Required for Status Updates)

Add to `convex/http.ts`:

```typescript
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";
import { resend } from "./sendEmails";

const http = httpRouter();

http.route({
  path: "/resend-webhook",
  method: "POST",
  handler: httpAction(async (ctx, req) => {
    return await resend.handleResendEventWebhook(ctx, req);
  }),
});

export default http;
```

Your webhook URL will be: `https://<deployment-name>.convex.site/resend-webhook`

Configure the webhook in Resend dashboard:
1. Navigate to webhooks
2. Create a new webhook with your URL
3. Enable all `email.*` events
4. Copy the webhook secret
5. Add `RESEND_WEBHOOK_SECRET` environment variable

## ResendOptions

```typescript
const resend = new Resend(components.resend, {
  // Provide API key instead of environment variable
  apiKey: "your-api-key",

  // Provide webhook secret instead of environment variable
  webhookSecret: "your-webhook-secret",

  // Only allow delivery to test addresses (default: true)
  // Set to false for production
  testMode: false,

  // Your email event callback
  onEmailEvent: internal.sendEmails.handleEmailEvent,
});
```

## Tracking and Managing Emails

```typescript
// sendEmail returns an EmailId
const emailId = await resend.sendEmail(ctx, from, to, subject, body);

// Check status
const status = await resend.status(ctx, emailId);

// Cancel email (only if not yet sent)
await resend.cancelEmail(ctx, emailId);
```

## Data Retention

This component retains "finalized" (delivered, cancelled, bounced) emails for seven days to allow status checks. Then, a background job clears those emails and their bodies to reclaim database space.

---

# Using Multiple Components

You can use multiple components in the same `convex.config.ts`:

```typescript
import { defineApp } from "convex/server";
import presence from "@convex-dev/presence/convex.config";
import prosemirrorSync from "@convex-dev/prosemirror-sync/convex.config";
import resend from "@convex-dev/resend/convex.config";

const app = defineApp();
app.use(presence);
app.use(prosemirrorSync);
app.use(resend);

export default app;
```

Component functions are accessed via `components.<component_name>.<function>` imported from `./_generated/api`:

```typescript
import { components } from "./_generated/api";
```
