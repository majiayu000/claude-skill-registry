---
name: pusher
description: Implements real-time features with Pusher Channels for WebSocket-based pub/sub messaging. Use when adding live updates, notifications, chat, presence indicators, or collaborative features.
---

# Pusher Channels

Real-time WebSocket infrastructure for pub/sub messaging. Supports public, private, presence, and encrypted channels.

## Quick Start

### Client Setup

```bash
npm install pusher-js
```

```javascript
import Pusher from 'pusher-js';

const pusher = new Pusher('YOUR_APP_KEY', {
  cluster: 'us2',  // your cluster
});

// Subscribe to a channel
const channel = pusher.subscribe('my-channel');

// Bind to an event
channel.bind('my-event', (data) => {
  console.log('Received:', data);
});
```

### Server Setup (Node.js)

```bash
npm install pusher
```

```javascript
import Pusher from 'pusher';

const pusher = new Pusher({
  appId: 'YOUR_APP_ID',
  key: 'YOUR_APP_KEY',
  secret: 'YOUR_APP_SECRET',
  cluster: 'us2',
  useTLS: true
});

// Trigger an event
await pusher.trigger('my-channel', 'my-event', {
  message: 'Hello from server!'
});
```

## Channel Types

### Public Channels

Anyone can subscribe. No authentication required.

```javascript
// Client
const channel = pusher.subscribe('news-updates');

channel.bind('new-article', (data) => {
  console.log('New article:', data.title);
});
```

### Private Channels

Require authentication. Prefix with `private-`.

```javascript
// Client
const privateChannel = pusher.subscribe('private-user-123');

privateChannel.bind('notification', (data) => {
  console.log('Private notification:', data);
});
```

```javascript
// Server - Auth endpoint (e.g., /pusher/auth)
app.post('/pusher/auth', (req, res) => {
  const socketId = req.body.socket_id;
  const channel = req.body.channel_name;

  // Verify user has access to this channel
  if (!userCanAccess(req.user, channel)) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  const auth = pusher.authorizeChannel(socketId, channel);
  res.json(auth);
});
```

### Presence Channels

Track who's online. Prefix with `presence-`.

```javascript
// Client
const presenceChannel = pusher.subscribe('presence-room-1');

// Current members
presenceChannel.bind('pusher:subscription_succeeded', (members) => {
  console.log('Member count:', members.count);
  members.each((member) => {
    console.log('Member:', member.id, member.info);
  });
});

// New member joined
presenceChannel.bind('pusher:member_added', (member) => {
  console.log('Joined:', member.info.name);
});

// Member left
presenceChannel.bind('pusher:member_removed', (member) => {
  console.log('Left:', member.info.name);
});
```

```javascript
// Server - Auth endpoint for presence
app.post('/pusher/auth', (req, res) => {
  const socketId = req.body.socket_id;
  const channel = req.body.channel_name;

  const presenceData = {
    user_id: req.user.id,
    user_info: {
      name: req.user.name,
      avatar: req.user.avatar
    }
  };

  const auth = pusher.authorizeChannel(socketId, channel, presenceData);
  res.json(auth);
});
```

### Encrypted Channels

End-to-end encryption. Prefix with `private-encrypted-`.

```javascript
// Client - need to enable encryption
const pusher = new Pusher('APP_KEY', {
  cluster: 'us2',
  channelAuthorization: {
    endpoint: '/pusher/auth'
  }
});

const encrypted = pusher.subscribe('private-encrypted-secret');
encrypted.bind('message', (data) => {
  // Data is automatically decrypted
  console.log('Decrypted:', data);
});
```

## Client Configuration

```javascript
const pusher = new Pusher('APP_KEY', {
  cluster: 'us2',

  // Authentication
  channelAuthorization: {
    endpoint: '/pusher/auth',
    transport: 'ajax',  // or 'jsonp'
    headers: {
      'Authorization': 'Bearer ' + token
    }
  },

  // Connection options
  forceTLS: true,
  enabledTransports: ['ws', 'wss'],

  // Auto-reconnect (enabled by default)
  activityTimeout: 120000,
  pongTimeout: 30000
});
```

## Connection State

```javascript
pusher.connection.bind('connected', () => {
  console.log('Connected! Socket ID:', pusher.connection.socket_id);
});

pusher.connection.bind('disconnected', () => {
  console.log('Disconnected');
});

pusher.connection.bind('error', (err) => {
  console.error('Connection error:', err);
});

pusher.connection.bind('state_change', (states) => {
  console.log('State changed from', states.previous, 'to', states.current);
});

// States: initialized, connecting, connected, unavailable, failed, disconnected
```

## Client Events

Trigger events from client (private/presence channels only).

```javascript
// Enable on dashboard first
const channel = pusher.subscribe('private-chat-room');

// Trigger from client (prefix with 'client-')
channel.trigger('client-typing', {
  user: 'Alice',
  typing: true
});

// Listen for client events
channel.bind('client-typing', (data) => {
  console.log(data.user, 'is typing...');
});
```

## Server SDK (Node.js)

### Trigger Events

```javascript
// Single channel
await pusher.trigger('my-channel', 'event-name', { data: 'value' });

// Multiple channels (max 100)
await pusher.trigger(['channel-1', 'channel-2'], 'event-name', { data: 'value' });

// Exclude a socket (don't send to sender)
await pusher.trigger('my-channel', 'event-name', { data: 'value' }, {
  socket_id: 'exclude-socket-id'
});
```

### Batch Events

```javascript
await pusher.triggerBatch([
  { channel: 'channel-1', name: 'event-1', data: { msg: 'Hello' } },
  { channel: 'channel-2', name: 'event-2', data: { msg: 'World' } }
]);
```

### Query Channel State

```javascript
// Get channel info
const info = await pusher.get({ path: '/channels/presence-room-1' });

// Get users in presence channel
const users = await pusher.get({
  path: '/channels/presence-room-1/users'
});

// Get all channels
const channels = await pusher.get({ path: '/channels' });
```

## React Integration

```jsx
import Pusher from 'pusher-js';
import { useEffect, useState, createContext, useContext } from 'react';

// Create context
const PusherContext = createContext(null);

export function PusherProvider({ children }) {
  const [pusher] = useState(() =>
    new Pusher('APP_KEY', { cluster: 'us2' })
  );

  useEffect(() => {
    return () => pusher.disconnect();
  }, []);

  return (
    <PusherContext.Provider value={pusher}>
      {children}
    </PusherContext.Provider>
  );
}

// Hook to subscribe to channel
export function useChannel(channelName) {
  const pusher = useContext(PusherContext);
  const [channel, setChannel] = useState(null);

  useEffect(() => {
    const ch = pusher.subscribe(channelName);
    setChannel(ch);

    return () => {
      pusher.unsubscribe(channelName);
    };
  }, [channelName]);

  return channel;
}

// Hook to bind to events
export function useEvent(channel, eventName, callback) {
  useEffect(() => {
    if (!channel) return;

    channel.bind(eventName, callback);
    return () => channel.unbind(eventName, callback);
  }, [channel, eventName, callback]);
}

// Usage
function ChatRoom({ roomId }) {
  const [messages, setMessages] = useState([]);
  const channel = useChannel(`private-room-${roomId}`);

  useEvent(channel, 'new-message', (data) => {
    setMessages((prev) => [...prev, data]);
  });

  return (
    <div>
      {messages.map((msg, i) => (
        <div key={i}>{msg.text}</div>
      ))}
    </div>
  );
}
```

## Next.js API Route

```typescript
// app/api/pusher/auth/route.ts
import Pusher from 'pusher';
import { getServerSession } from 'next-auth';

const pusher = new Pusher({
  appId: process.env.PUSHER_APP_ID!,
  key: process.env.NEXT_PUBLIC_PUSHER_KEY!,
  secret: process.env.PUSHER_SECRET!,
  cluster: process.env.NEXT_PUBLIC_PUSHER_CLUSTER!,
  useTLS: true
});

export async function POST(req: Request) {
  const session = await getServerSession();
  if (!session) {
    return new Response('Unauthorized', { status: 401 });
  }

  const data = await req.formData();
  const socketId = data.get('socket_id') as string;
  const channel = data.get('channel_name') as string;

  // For presence channels
  if (channel.startsWith('presence-')) {
    const presenceData = {
      user_id: session.user.id,
      user_info: {
        name: session.user.name,
        image: session.user.image
      }
    };
    const auth = pusher.authorizeChannel(socketId, channel, presenceData);
    return Response.json(auth);
  }

  // For private channels
  const auth = pusher.authorizeChannel(socketId, channel);
  return Response.json(auth);
}
```

## Common Patterns

### Live Notifications

```javascript
// Client
const userChannel = pusher.subscribe(`private-user-${userId}`);

userChannel.bind('notification', (notification) => {
  showToast(notification.message);
  updateNotificationCount();
});
```

```javascript
// Server
async function sendNotification(userId, notification) {
  await pusher.trigger(`private-user-${userId}`, 'notification', {
    id: notification.id,
    message: notification.message,
    createdAt: new Date().toISOString()
  });
}
```

### Typing Indicators

```javascript
// Client
let typingTimeout;

function handleInput() {
  channel.trigger('client-typing', { userId: myUserId });

  clearTimeout(typingTimeout);
  typingTimeout = setTimeout(() => {
    channel.trigger('client-stopped-typing', { userId: myUserId });
  }, 1000);
}

channel.bind('client-typing', ({ userId }) => {
  showTypingIndicator(userId);
});

channel.bind('client-stopped-typing', ({ userId }) => {
  hideTypingIndicator(userId);
});
```

### Online Users List

```javascript
const presenceChannel = pusher.subscribe('presence-app');
const [onlineUsers, setOnlineUsers] = useState([]);

presenceChannel.bind('pusher:subscription_succeeded', (members) => {
  const users = [];
  members.each((member) => users.push(member.info));
  setOnlineUsers(users);
});

presenceChannel.bind('pusher:member_added', (member) => {
  setOnlineUsers((prev) => [...prev, member.info]);
});

presenceChannel.bind('pusher:member_removed', (member) => {
  setOnlineUsers((prev) => prev.filter((u) => u.id !== member.id));
});
```

## Debug Mode

```javascript
Pusher.logToConsole = true;  // Enable in development

const pusher = new Pusher('APP_KEY', {
  cluster: 'us2'
});
```

## Limits

- Max 100 channels per trigger
- Max 10KB per message
- Max 100 presence members per channel
- Max 200 connections per app (free tier)
