---
name: ably
description: Implements real-time pub/sub messaging with Ably's edge infrastructure. Use when building real-time features requiring enterprise reliability, presence, message history, and global low-latency delivery.
---

# Ably Pub/Sub

Enterprise-grade real-time messaging platform with global edge network. Supports pub/sub, presence, message history, and push notifications.

## Quick Start

```bash
npm install ably
```

### Client (Realtime)

```javascript
import * as Ably from 'ably';

const ably = new Ably.Realtime({
  key: 'YOUR_API_KEY',  // Use token auth in production
  clientId: 'user-123'
});

// Wait for connection
await ably.connection.once('connected');

// Get a channel
const channel = ably.channels.get('my-channel');

// Subscribe to messages
await channel.subscribe('greeting', (message) => {
  console.log('Received:', message.data);
});

// Publish a message
await channel.publish('greeting', 'Hello World!');
```

### Server (REST)

```javascript
import * as Ably from 'ably';

const ably = new Ably.Rest({ key: 'YOUR_API_KEY' });

// Publish without maintaining connection
const channel = ably.channels.get('notifications');
await channel.publish('alert', { message: 'Server notification' });
```

## Authentication

### Token Auth (Recommended for Production)

```javascript
// Client with auth endpoint
const ably = new Ably.Realtime({
  authUrl: '/api/ably-token',
  clientId: 'user-123'
});

// Server endpoint (Next.js example)
// app/api/ably-token/route.ts
import * as Ably from 'ably';

export async function GET(req: Request) {
  const ably = new Ably.Rest({ key: process.env.ABLY_API_KEY });

  const tokenParams = {
    clientId: 'user-123',  // Get from session
    capability: { '*': ['publish', 'subscribe', 'presence'] }
  };

  const tokenRequest = await ably.auth.createTokenRequest(tokenParams);
  return Response.json(tokenRequest);
}
```

### Token Capabilities

```javascript
const tokenParams = {
  clientId: 'user-123',
  capability: {
    'public-*': ['subscribe'],           // Subscribe to public channels
    'private-user-123': ['*'],            // Full access to own channel
    'chat-room-*': ['publish', 'subscribe', 'presence']
  }
};
```

## Channels

### Subscribe & Publish

```javascript
const channel = ably.channels.get('chat');

// Subscribe to all messages
await channel.subscribe((message) => {
  console.log(message.name, message.data);
});

// Subscribe to specific event
await channel.subscribe('message', (message) => {
  console.log('Chat message:', message.data);
});

// Publish
await channel.publish('message', {
  text: 'Hello!',
  author: 'Alice'
});

// Publish multiple
await channel.publish([
  { name: 'message', data: 'First' },
  { name: 'message', data: 'Second' }
]);

// Unsubscribe
channel.unsubscribe('message', myHandler);
channel.unsubscribe();  // All handlers
```

### Channel States

```javascript
channel.on('attached', () => console.log('Channel attached'));
channel.on('detached', () => console.log('Channel detached'));
channel.on('failed', (err) => console.error('Channel failed:', err));

// Check state
console.log(channel.state);  // initialized, attaching, attached, detaching, detached, failed
```

## Presence

Track who's online in a channel.

```javascript
const channel = ably.channels.get('room-1');

// Enter presence
await channel.presence.enter({ status: 'online', name: 'Alice' });

// Update presence data
await channel.presence.update({ status: 'away' });

// Leave presence
await channel.presence.leave();

// Get current members
const members = await channel.presence.get();
members.forEach((member) => {
  console.log(member.clientId, member.data);
});

// Subscribe to presence events
await channel.presence.subscribe('enter', (member) => {
  console.log(member.clientId, 'entered');
});

await channel.presence.subscribe('leave', (member) => {
  console.log(member.clientId, 'left');
});

await channel.presence.subscribe('update', (member) => {
  console.log(member.clientId, 'updated:', member.data);
});

// Subscribe to all presence events
await channel.presence.subscribe((member) => {
  console.log(member.action, member.clientId, member.data);
});
```

## Message History

```javascript
const channel = ably.channels.get('chat');

// Get last 100 messages
const history = await channel.history({ limit: 100 });

history.items.forEach((message) => {
  console.log(message.timestamp, message.name, message.data);
});

// Paginate through history
let page = await channel.history({ limit: 50 });

while (page) {
  page.items.forEach(console.log);
  page = await page.next();  // null when no more pages
}

// Get messages from specific time
const history = await channel.history({
  start: Date.now() - 60000,  // Last minute
  direction: 'forwards'
});
```

## Connection Management

```javascript
// Connection events
ably.connection.on('connected', () => {
  console.log('Connected!');
});

ably.connection.on('disconnected', () => {
  console.log('Disconnected - will auto-reconnect');
});

ably.connection.on('suspended', () => {
  console.log('Connection suspended');
});

ably.connection.on('failed', (err) => {
  console.error('Connection failed:', err);
});

// Connection state
console.log(ably.connection.state);
// States: initialized, connecting, connected, disconnected, suspended, closing, closed, failed

// Manual control
ably.connection.close();
ably.connection.connect();

// Get connection ID
console.log(ably.connection.id);
```

## React Integration

```jsx
import * as Ably from 'ably';
import { AblyProvider, useChannel, usePresence } from 'ably/react';

// Setup client
const client = new Ably.Realtime({
  authUrl: '/api/ably-token'
});

function App() {
  return (
    <AblyProvider client={client}>
      <ChatRoom />
    </AblyProvider>
  );
}

function ChatRoom() {
  const [messages, setMessages] = useState([]);

  // Subscribe to channel
  const { channel } = useChannel('chat', 'message', (message) => {
    setMessages((prev) => [...prev, message.data]);
  });

  // Presence
  const { presenceData, updateStatus } = usePresence('chat', {
    name: 'Alice',
    status: 'online'
  });

  const sendMessage = () => {
    channel.publish('message', { text: 'Hello!' });
  };

  return (
    <div>
      <div>Online: {presenceData.length}</div>
      {messages.map((msg, i) => (
        <div key={i}>{msg.text}</div>
      ))}
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}
```

### Custom Hooks

```jsx
import { useEffect, useState, useCallback } from 'react';
import * as Ably from 'ably';

const ably = new Ably.Realtime({ authUrl: '/api/ably-token' });

export function useAblyChannel(channelName) {
  const [channel, setChannel] = useState(null);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const ch = ably.channels.get(channelName);
    setChannel(ch);

    ch.subscribe((message) => {
      setMessages((prev) => [...prev, message]);
    });

    return () => {
      ch.unsubscribe();
      ch.detach();
    };
  }, [channelName]);

  const publish = useCallback((name, data) => {
    channel?.publish(name, data);
  }, [channel]);

  return { channel, messages, publish };
}

export function useAblyPresence(channelName, initialData) {
  const [members, setMembers] = useState([]);

  useEffect(() => {
    const channel = ably.channels.get(channelName);

    channel.presence.enter(initialData);

    channel.presence.subscribe((member) => {
      channel.presence.get().then(setMembers);
    });

    channel.presence.get().then(setMembers);

    return () => {
      channel.presence.leave();
      channel.presence.unsubscribe();
    };
  }, [channelName]);

  const updatePresence = useCallback((data) => {
    ably.channels.get(channelName).presence.update(data);
  }, [channelName]);

  return { members, updatePresence };
}
```

## Advanced Features

### Channel Rewind

Get historical messages on subscribe.

```javascript
const channel = ably.channels.get('chat', {
  params: {
    rewind: '2m'  // Last 2 minutes, or '100' for last 100 messages
  }
});

await channel.subscribe((message) => {
  // Includes historical messages
});
```

### Delta Compression

Reduce bandwidth for similar messages.

```javascript
const channel = ably.channels.get('game-state', {
  params: { delta: 'vcdiff' }
});
```

### Push Notifications

```javascript
const channel = ably.channels.get('alerts');

// Subscribe device to push
await channel.push.subscribeDevice();

// Server: Publish with push notification
await channel.publish({
  name: 'alert',
  data: { message: 'Important update!' },
  extras: {
    push: {
      notification: {
        title: 'Alert',
        body: 'Check your app!'
      }
    }
  }
});
```

## Error Handling

```javascript
try {
  await channel.publish('event', data);
} catch (err) {
  if (err.code === 40160) {
    // Invalid credentials
  } else if (err.code === 42910) {
    // Rate limited
  }
  console.error('Ably error:', err.message);
}
```

## Common Patterns

### Chat Application

```javascript
const channel = ably.channels.get('chat-room-1');

// Join room
await channel.presence.enter({ username: 'Alice' });

// Send message
async function sendMessage(text) {
  await channel.publish('message', {
    text,
    author: 'Alice',
    timestamp: Date.now()
  });
}

// Typing indicator
let typingTimeout;
function handleTyping() {
  channel.publish('typing', { user: 'Alice' });
  clearTimeout(typingTimeout);
  typingTimeout = setTimeout(() => {
    channel.publish('stopped-typing', { user: 'Alice' });
  }, 1000);
}
```

### Live Dashboard

```javascript
// Server: Publish metrics
setInterval(async () => {
  await channel.publish('metrics', {
    cpu: getCpuUsage(),
    memory: getMemoryUsage(),
    requests: getRequestCount()
  });
}, 1000);

// Client: Display metrics
channel.subscribe('metrics', (message) => {
  updateDashboard(message.data);
});
```

## REST vs Realtime

| Feature | Realtime | REST |
|---------|----------|------|
| Subscribe | Yes | No |
| Publish | Yes | Yes |
| Presence | Yes | Read only |
| History | Yes | Yes |
| Connection | Persistent | Per-request |
| Use case | Browsers, apps | Servers, scripts |

```javascript
// Use REST for server-side publishing
const rest = new Ably.Rest({ key: 'API_KEY' });
await rest.channels.get('updates').publish('event', data);
```
