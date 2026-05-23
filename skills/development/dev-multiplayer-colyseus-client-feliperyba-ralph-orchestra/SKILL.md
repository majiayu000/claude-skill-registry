---
name: dev-multiplayer-colyseus-client
description: Colyseus client SDK for React, connection methods, room events, and messaging. Use when connecting to multiplayer server.
category: multiplayer
---

# Colyseus Client SDK

Connect to Colyseus server from React applications with colyseus.js.

## When to Use

Use when:
- Connecting to game server from client
- Handling room state changes
- Sending/receiving messages
- Managing room lifecycle

## Basic Connection

```typescript
import { Client, Room } from 'colyseus.js';

const client = new Client('ws://localhost:2567');

async function joinGame() {
  try {
    const room = await client.joinOrCreate('game_room', {});

    room.onStateChange((state) => {
      console.log('New state:', state);
    });

    room.onMessage('game_event', (data) => {
      console.log('Received:', data);
    });

    room.onLeave((code) => {
      console.log('Left room:', code);
    });
  } catch (e) {
    console.error('Join error:', e);
  }
}
```

## Connection Methods

```typescript
// Join existing or create new
const room = await client.joinOrCreate('room_name', { options: 'value' });

// Create new (fails if exists)
const room = await client.create('room_name', { options: 'value' });

// Join existing only (fails if full/not found)
const room = await client.join('room_name', { options: 'value' });

// Join by specific room ID
const room = await client.joinById('room_id_here', { options: 'value' });

// Reconnect to previous room
const room = await client.reconnect(reconnectionToken);

// Consume seat reservation
const room = await client.consumeSeatReservation(reservation);
```

## React Integration

```tsx
import { useEffect, useRef, useState } from 'react';
import { Client, Room } from 'colyseus.js';

const client = new Client('ws://localhost:2567');

function GameRoom() {
  const roomRef = useRef<Room>();
  const [isConnecting, setIsConnecting] = useState(true);
  const [players, setPlayers] = useState([]);

  useEffect(() => {
    const req = client.joinOrCreate('my_room', {});

    req.then((room) => {
      roomRef.current = room;
      setIsConnecting(false);

      room.onStateChange((state) => setPlayers(state.players.toJSON()));
    });

    return () => {
      req.then((room) => room.leave());
    };
  }, []);

  return (
    <div>
      {isConnecting ? 'Connecting...' :
        players.map((player) => (
          <div key={player.id}>{player.name}</div>
        ))
      }
    </div>
  );
}
```

## Room Methods

```typescript
// Properties
room.state        // Current room state (Schema instance)
room.sessionId    // Unique client identifier
room.id           // Room identifier (shareable)
room.name         // Room handler name

// Send message to server
room.send('message_type', { data: 'value' });

// Send raw bytes
room.sendBytes(0, [0x01, 0x02, 0x03]);

// Leave room
room.leave();              // Consented leave
room.leave(false);         // Forced leave

// Remove all listeners
room.removeAllListeners();
```

## Room Events

```typescript
// Message events
room.onMessage('message_type', (data) => {
  console.log('Received:', data);
});

// State change events
room.onStateChange((state) => {
  console.log('State updated:', state.toJSON());
});

// One-time state change (first state only)
room.onStateChange.once((state) => {
  console.log('Initial state:', state);
});

// Leave event
room.onLeave((code) => {
  console.log('Left room with code:', code);
  // 1000 = normal shutdown
  // 4000-4999 = custom codes
});

// Error event
room.onError((code, message) => {
  console.error('Room error:', code, message);
});
```

## HTTP Requests

```typescript
// GET request
client.http.get('/api/endpoint').then(response => {
  console.log(response.data);
});

// POST request
client.http.post('/api/endpoint', { body: 'data' }).then(response => {
  console.log(response.data);
});

// PUT request
client.http.put('/api/endpoint', { body: 'data' }).then(response => {
  console.log(response.data);
});

// DELETE request
client.http.delete('/api/endpoint').then(response => {
  console.log(response.data);
});
```

## React Context Provider Pattern

```tsx
// RoomContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { Client, Room } from 'colyseus.js';

interface RoomContextType {
  room: Room | null;
  state: any;
  isConnected: boolean;
  join: () => void;
}

export const RoomContext = createContext<RoomContextType>({} as RoomContextType);

export function useRoom() {
  return useContext(RoomContext);
}

export function RoomProvider({ children }: { children: React.ReactNode }) {
  const [room, setRoom] = useState<Room | null>(null);
  const [state, setState] = useState<any>(null);
  const [isConnected, setIsConnected] = useState(false);

  const join = async () => {
    try {
      const client = new Client('ws://localhost:2567');
      const joinedRoom = await client.joinOrCreate('game_room');

      setRoom(joinedRoom);
      setIsConnected(true);

      joinedRoom.onStateChange((newState) => {
        setState(newState.toJSON());
      });

      joinedRoom.onLeave(() => {
        setIsConnected(false);
        setRoom(null);
      });
    } catch (e) {
      console.error('Failed to join:', e);
    }
  };

  return (
    <RoomContext.Provider value={{ room, state, isConnected, join }}>
      {children}
    </RoomContext.Provider>
  );
}
```

## Authentication

```typescript
// Anonymous sign-in
client.auth.signInAnonymously()
  .then((response) => {
    console.log('Authenticated:', response.user);
  })
  .catch((error) => {
    console.error('Auth error:', error);
  });

// Listen to auth changes
client.auth.onChange((authData) => {
  if (authData.token) {
    console.log('User logged in:', authData.user);
  } else {
    console.log('User logged out');
  }
});

// Auth tokens sent automatically with HTTP requests
client.http.get('/profile').then(response => {
  // Authorization header included
});
```

## Best Practices

1. **Leave room on unmount** - Prevent memory leaks
2. **Handle errors** - Network failures are common
3. **Use reconnection tokens** - For seamless reconnection
4. **Send inputs, not positions** - Server-authoritative
5. **Handle state changes** - Use schema callbacks for updates

## Connection Lifecycle Management

**CRITICAL:** Handle all connection states properly for a good UX.

```typescript
// Connection states enum
enum ConnectionState {
  DISCONNECTED = 'disconnected',
  CONNECTING = 'connecting',
  CONNECTED = 'connected',
  RECONNECTING = 'reconnecting',
  ERROR = 'error',
}

// Connection hook with lifecycle
function useColyseusConnection(roomName: string) {
  const [state, setState] = useState<ConnectionState>(ConnectionState.DISCONNECTED);
  const [room, setRoom] = useState<Room | null>(null);
  const [error, setError] = useState<string | null>(null);

  const connect = async () => {
    setState(ConnectionState.CONNECTING);
    setError(null);

    try {
      const client = new Client('ws://localhost:2567');
      const joinedRoom = await client.joinOrCreate(roomName);

      setRoom(joinedRoom);
      setState(ConnectionState.CONNECTED);

      // Handle disconnection
      joinedRoom.onLeave((code) => {
        if (code === 1000) {
          setState(ConnectionState.DISCONNECTED);
        } else {
          setState(ConnectionState.RECONNECTING);
          // Attempt reconnection
          setTimeout(() => connect(), 3000);
        }
      });

      joinedRoom.onError((err) => {
        setError(err.message);
        setState(ConnectionState.ERROR);
      });

    } catch (err) {
      setError(err.message);
      setState(ConnectionState.ERROR);
    }
  };

  const disconnect = () => {
    if (room) {
      room.leave();
      setRoom(null);
      setState(ConnectionState.DISCONNECTED);
    }
  };

  return { state, error, connect, disconnect, room };
}
```

### Reconnection Testing Pattern

**For E2E tests covering disconnect/reconnect cycles:**

```typescript
// E2E test for reconnection
test('handles disconnect and reconnect', async ({ page }) => {
  // 1. Connect to server
  await page.goto('/game');
  await expect(page.getByTestId('connection-status')).toHaveText('Connected');

  // 2. Simulate server disconnect
  await page.evaluate(() => {
    // @ts-ignore - Test utility
    window.__testDisconnectServer();
  });

  // 3. Verify disconnected state
  await expect(page.getByTestId('connection-status')).toHaveText('Disconnected');

  // 4. Wait for auto-reconnect
  await expect(page.getByTestId('connection-status')).toHaveText('Reconnecting', { timeout: 5000 });

  // 5. Verify reconnected
  await expect(page.getByTestId('connection-status')).toHaveText('Connected', { timeout: 10000 });
});
```

### Connection State Monitoring

```typescript
// Browser's online/offline events
useEffect(() => {
  const handleOnline = () => {
    console.log('Browser online - attempt reconnect');
    // Trigger reconnection logic
  };

  const handleOffline = () => {
    console.log('Browser offline - show disconnected');
    setState(ConnectionState.DISCONNECTED);
  };

  window.addEventListener('online', handleOnline);
  window.addEventListener('offline', handleOffline);

  return () => {
    window.removeEventListener('online', handleOnline);
    window.removeEventListener('offline', handleOffline);
  };
}, []);
```

## Common Mistakes

| ❌ Wrong | ✅ Right |
|----------|----------|
| Not leaving room on unmount | Always `room.leave()` in cleanup |
| Using CommonJS imports | Use `import { Client } from 'colyseus.js'` |
| Client sends absolute position | Client sends input (WASD, aim) |
| Ignoring error events | Always handle `onError` |

## Reference

- [Colyseus Client Docs](https://docs.colyseus.io/client)
- [React Integration](https://docs.colyseus.io/getting-started/react)
