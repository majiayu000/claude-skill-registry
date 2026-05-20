---
name: soketi
description: >-
  Configure and integrate Soketi WebSocket server with FTC Metrics for real-time updates.
  Use when setting up WebSocket connections, broadcasting scouting data changes,
  implementing presence channels for team collaboration, or debugging real-time features.
license: MIT
compatibility: [Claude Code]
metadata:
  author: ftcmetrics
  version: "1.0.0"
  category: realtime
---

# Soketi WebSocket Server

Soketi is a Pusher-compatible WebSocket server for real-time communication in FTC Metrics.

## Quick Reference

| Feature | Use Case |
|---------|----------|
| Public Channels | Event-wide updates (match scores) |
| Private Channels | Team-specific scouting data |
| Presence Channels | Track who's online scouting |

## Docker Setup

```yaml
# docker-compose.yml
soketi:
  image: quay.io/soketi/soketi:1.6-16-debian
  container_name: ftcmetrics-soketi
  restart: unless-stopped
  environment:
    SOKETI_DEBUG: "1"
    SOKETI_DEFAULT_APP_ID: ${SOKETI_APP_ID:-ftcmetrics}
    SOKETI_DEFAULT_APP_KEY: ${SOKETI_APP_KEY:-ftcmetrics-key}
    SOKETI_DEFAULT_APP_SECRET: ${SOKETI_APP_SECRET:-ftcmetrics-secret}
  ports:
    - "6001:6001"   # WebSocket connections
    - "9601:9601"   # Prometheus metrics
```

### Environment Variables

```bash
# .env
SOKETI_APP_ID=ftcmetrics
SOKETI_APP_KEY=ftcmetrics-key
SOKETI_APP_SECRET=ftcmetrics-secret
SOKETI_HOST=localhost
SOKETI_PORT=6001
```

### Commands

```bash
docker-compose up -d soketi      # Start Soketi
docker-compose logs -f soketi    # View logs
```

## Client Setup (Frontend)

### Install and Configure

```bash
bun add pusher-js
```

```typescript
// packages/web/src/lib/pusher.ts
import Pusher from "pusher-js";

let pusherInstance: Pusher | null = null;

export function getPusherClient(authToken?: string): Pusher {
  if (!pusherInstance) {
    pusherInstance = new Pusher(process.env.NEXT_PUBLIC_SOKETI_APP_KEY!, {
      wsHost: process.env.NEXT_PUBLIC_SOKETI_HOST || "localhost",
      wsPort: parseInt(process.env.NEXT_PUBLIC_SOKETI_PORT || "6001", 10),
      wssPort: parseInt(process.env.NEXT_PUBLIC_SOKETI_PORT || "6001", 10),
      forceTLS: process.env.NODE_ENV === "production",
      disableStats: true,
      enabledTransports: ["ws", "wss"],
      cluster: "mt1",
      authEndpoint: `${process.env.NEXT_PUBLIC_API_URL}/api/pusher/auth`,
      auth: { headers: { "X-User-Id": authToken || "" } },
    });
  }
  return pusherInstance;
}

export function disconnectPusher(): void {
  if (pusherInstance) {
    pusherInstance.disconnect();
    pusherInstance = null;
  }
}
```

### React Hooks

```typescript
// packages/web/src/hooks/usePusher.ts
"use client";
import { useEffect, useState } from "react";
import { getPusherClient } from "@/lib/pusher";
import type { Channel, PresenceChannel } from "pusher-js";

interface UsePusherOptions {
  channelName: string;
  eventName: string;
  onEvent: (data: unknown) => void;
}

export function usePusher({ channelName, eventName, onEvent }: UsePusherOptions) {
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const pusher = getPusherClient();
    const ch = pusher.subscribe(channelName);
    ch.bind("pusher:subscription_succeeded", () => setIsConnected(true));
    ch.bind(eventName, onEvent);
    return () => {
      ch.unbind(eventName, onEvent);
      pusher.unsubscribe(channelName);
    };
  }, [channelName, eventName, onEvent]);

  return { isConnected };
}

export function usePresenceChannel(channelName: string) {
  const [members, setMembers] = useState<Map<string, unknown>>(new Map());
  const [myId, setMyId] = useState<string | null>(null);

  useEffect(() => {
    const pusher = getPusherClient();
    const channel = pusher.subscribe(channelName) as PresenceChannel;

    channel.bind("pusher:subscription_succeeded", (data: { members: Record<string, unknown>; myID: string }) => {
      setMembers(new Map(Object.entries(data.members)));
      setMyId(data.myID);
    });
    channel.bind("pusher:member_added", (member: { id: string; info: unknown }) => {
      setMembers((prev) => new Map(prev).set(member.id, member.info));
    });
    channel.bind("pusher:member_removed", (member: { id: string }) => {
      setMembers((prev) => { const next = new Map(prev); next.delete(member.id); return next; });
    });

    return () => pusher.unsubscribe(channelName);
  }, [channelName]);

  return { members, myId, memberCount: members.size };
}
```

## Server Setup (Hono API)

### Install and Configure

```bash
cd packages/api && bun add pusher
```

```typescript
// packages/api/src/lib/pusher.ts
import Pusher from "pusher";

let pusherInstance: Pusher | null = null;

export function getPusherServer(): Pusher {
  if (!pusherInstance) {
    pusherInstance = new Pusher({
      appId: process.env.SOKETI_APP_ID!,
      key: process.env.SOKETI_APP_KEY!,
      secret: process.env.SOKETI_APP_SECRET!,
      host: process.env.SOKETI_HOST || "localhost",
      port: process.env.SOKETI_PORT || "6001",
      useTLS: process.env.NODE_ENV === "production",
    });
  }
  return pusherInstance;
}

export async function broadcastToChannel(channel: string, event: string, data: unknown): Promise<void> {
  await getPusherServer().trigger(channel, event, data);
}

export async function broadcastToMultipleChannels(channels: string[], event: string, data: unknown): Promise<void> {
  const pusher = getPusherServer();
  for (let i = 0; i < channels.length; i += 100) {
    await pusher.trigger(channels.slice(i, i + 100), event, data);
  }
}
```

### Auth Endpoint

```typescript
// packages/api/src/routes/pusher-auth.ts
import { Hono } from "hono";
import { getPusherServer } from "../lib/pusher";
import { prisma } from "@ftcmetrics/db";

const pusherAuth = new Hono();

pusherAuth.post("/auth", async (c) => {
  const userId = c.req.header("X-User-Id");
  if (!userId) return c.json({ error: "Unauthorized" }, 403);

  const body = await c.req.parseBody();
  const socketId = body.socket_id as string;
  const channelName = body.channel_name as string;
  if (!socketId || !channelName) return c.json({ error: "Missing params" }, 400);

  const pusher = getPusherServer();

  // Presence channels
  if (channelName.startsWith("presence-")) {
    const user = await prisma.user.findUnique({
      where: { id: userId },
      select: { id: true, name: true, image: true },
    });
    if (!user) return c.json({ error: "User not found" }, 404);

    const hasAccess = await verifyChannelAccess(userId, channelName);
    if (!hasAccess) return c.json({ error: "Access denied" }, 403);

    const authResponse = pusher.authorizeChannel(socketId, channelName, {
      user_id: user.id,
      user_info: { name: user.name, image: user.image },
    });
    return c.json(authResponse);
  }

  // Private channels
  if (channelName.startsWith("private-")) {
    const hasAccess = await verifyChannelAccess(userId, channelName);
    if (!hasAccess) return c.json({ error: "Access denied" }, 403);
    return c.json(pusher.authorizeChannel(socketId, channelName));
  }

  return c.json({ error: "Invalid channel type" }, 400);
});

async function verifyChannelAccess(userId: string, channelName: string): Promise<boolean> {
  const teamMatch = channelName.match(/^(private|presence)-team-(.+)$/);
  if (teamMatch) {
    const membership = await prisma.teamMember.findUnique({
      where: { userId_teamId: { userId, teamId: teamMatch[2] } },
    });
    return !!membership;
  }
  // Event channels: allow authenticated users
  if (channelName.match(/^(private|presence)-event-/)) return true;
  return false;
}

export default pusherAuth;
```

Mount in `packages/api/src/index.ts`:
```typescript
import pusherAuth from "./routes/pusher-auth";
app.route("/api/pusher", pusherAuth);
```

## Channel Patterns

| Channel | Purpose | Type |
|---------|---------|------|
| `event-{eventCode}` | Public event updates | Public |
| `private-team-{teamId}` | Team scouting data | Private |
| `presence-team-{teamId}` | Team members online | Presence |
| `match-{eventCode}-{matchNumber}` | Live match updates | Public |

## Broadcasting from Routes

```typescript
// packages/api/src/routes/scouting.ts
import { broadcastToChannel } from "../lib/pusher";

scouting.post("/entries", async (c) => {
  // ... create entry ...
  const entry = await prisma.scoutingEntry.create({ ... });

  // Broadcast to team
  await broadcastToChannel(`private-team-${scoutingTeamId}`, "scouting:entry-created", {
    entry, scoutedTeamNumber, matchNumber,
  });

  // Broadcast to event
  await broadcastToChannel(`event-${eventCode}`, "scouting:new-entry", {
    scoutedTeamNumber, matchNumber,
  });

  return c.json({ success: true, data: entry });
});
```

## Frontend Components

### Live Scouting Feed

```tsx
"use client";
import { useCallback, useState } from "react";
import { usePusher } from "@/hooks/usePusher";

export function ScoutingFeed({ teamId }: { teamId: string }) {
  const [entries, setEntries] = useState<Array<{ id: string; scoutedTeamNumber: number; matchNumber: number; totalScore: number }>>([]);

  const handleNewEntry = useCallback((data: unknown) => {
    const { entry } = data as { entry: typeof entries[0] };
    setEntries((prev) => [entry, ...prev].slice(0, 50));
  }, []);

  const { isConnected } = usePusher({
    channelName: `private-team-${teamId}`,
    eventName: "scouting:entry-created",
    onEvent: handleNewEntry,
  });

  return (
    <div>
      <span className={`w-2 h-2 rounded-full ${isConnected ? "bg-green-500" : "bg-red-500"}`} />
      <ul>{entries.map((e) => <li key={e.id}>Team {e.scoutedTeamNumber} - Match {e.matchNumber}: {e.totalScore}pts</li>)}</ul>
    </div>
  );
}
```

### Team Presence

```tsx
"use client";
import { usePresenceChannel } from "@/hooks/usePusher";

export function TeamPresence({ teamId }: { teamId: string }) {
  const { members, memberCount } = usePresenceChannel(`presence-team-${teamId}`);

  return (
    <div>
      <h3>Online ({memberCount})</h3>
      {Array.from(members.entries()).map(([id, info]) => (
        <span key={id}>{(info as { name: string }).name}</span>
      ))}
    </div>
  );
}
```

## Event Types

```typescript
// packages/shared/src/websocket-events.ts
export const WebSocketEvents = {
  SCOUTING_ENTRY_CREATED: "scouting:entry-created",
  SCOUTING_ENTRY_UPDATED: "scouting:entry-updated",
  SCOUTING_NOTE_ADDED: "scouting:note-added",
  MATCH_STARTED: "match:started",
  MATCH_COMPLETED: "match:completed",
  EPA_UPDATED: "analytics:epa-updated",
  MEMBER_JOINED: "team:member-joined",
  MEMBER_LEFT: "team:member-left",
} as const;
```

## Debugging

```typescript
Pusher.logToConsole = true; // Enable client-side debug
```

```bash
curl http://localhost:6001          # Health check
curl http://localhost:9601/metrics  # Prometheus metrics
```

| Issue | Solution |
|-------|----------|
| Connection refused | Run `docker-compose ps` to check Soketi |
| Auth failures | Verify X-User-Id header |
| Events not received | Check channel name matches |

## Production

- Enable `forceTLS: true` for wss://
- Use Redis adapter for multi-instance scaling
- Configure `SOKETI_MAX_REQUESTS_PER_SECOND`
- Scrape `/metrics` with Prometheus

## References

- [Soketi Docs](https://docs.soketi.app/)
- [Pusher Protocol](https://pusher.com/docs/channels/library_auth_reference/pusher-websockets-protocol/)
- [pusher-js](https://github.com/pusher/pusher-js)
