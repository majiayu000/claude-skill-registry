---
name: dev-multiplayer-colyseus-server
description: Colyseus server setup, room handlers, lifecycle events, and scaling. Use when setting up multiplayer server.
category: multiplayer
---

# Colyseus Server Setup

Node.js multiplayer framework - authoritative game server with real-time state sync.

## When to Use

Use when:
- Setting up Colyseus server
- Creating room handlers
- Implementing matchmaking
- Configuring server transport

## Server Setup (ESM Required)

```typescript
// server/index.ts - MUST use ESM
import { Server } from 'colyseus';
import { createServer } from 'http';
import express from 'express';
import { WebSocketTransport } from '@colyseus/ws-transport';
import { GameRoom } from './rooms/GameRoom';

const port = Number(process.env.PORT) || 2567;

const app = express();

// CORS middleware
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }
  next();
});

const httpServer = createServer(app);

const gameServer = new Server({
  transport: new WebSocketTransport({ server: httpServer }),
});

gameServer.define('game_room', GameRoom);
gameServer.listen(port);

console.log(`Colyseus server listening on wss://localhost:${port}`);
```

**CRITICAL**: Server MUST use `"type": "module"` in package.json. Do NOT use CommonJS.

## Room Handler Definition

```typescript
import { Room, Client } from 'colyseus';
import { Schema, type, MapSchema } from '@colyseus/schema';

export class GameRoom extends Room<GameRoomState> {
  onCreate(options: any) {
    this.setState(new GameRoomState());
    console.log(`[GameRoom] Created: ${this.roomId}`);

    // Simulation tick (deltaTime in seconds)
    this.setSimulationInterval((deltaTime) => {
      this.update(deltaTime);
    });

    // One-time event
    this.clock.setTimeout(() => this.endMatch(), 5000);

    // Repeated event
    this.clock.setInterval(() => this.checkCondition(), 100);
  }

  onJoin(client: Client, options: any) {
    const player = new PlayerState();
    player.clientId = client.sessionId;
    this.state.players.set(client.sessionId, player);

    client.send('welcome', { playerId: client.sessionId });
  }

  onLeave(client: Client, consented: boolean) {
    this.state.players.delete(client.sessionId);
  }

  onMessage(client: Client, data: any) {
    switch (data.type) {
      case 'player_input':
        this.handleInput(client, data);
        break;
    }
  }

  onDispose() {
    console.log(`[GameRoom] Disposed: ${this.roomId}`);
  }
}
```

## Message Broadcasting

```typescript
// Broadcast to all clients
this.broadcast('game_event', { data: 'value' });

// Send to specific client
client.send('personal_event', { data: 'value' });

// Send to all except sender
this.broadcast('game_event', { data: 'value' }, [client.sessionId]);
```

## Server Definition Options

```typescript
// Filter rooms by options for matchmaking
gameServer
  .define('battle', BattleRoom)
  .filterBy(['mode', 'map']);

// Sort rooms for matchmaking priority
gameServer
  .define('battle', BattleRoom)
  .sortBy({ clients: -1 });  // Most players first

// Enable realtime listing
gameServer
  .define('battle', BattleRoom)
  .enableRealtimeListing();

// Listen to lifecycle events
gameServer
  .define('chat', ChatRoom)
  .on('create', (room) => console.log('Room created'))
  .on('dispose', (room) => console.log('Room disposed'))
  .on('join', (room, client) => console.log('Client joined'))
  .on('leave', (room, client) => console.log('Client left'));
```

## Transport Configuration

```typescript
import { WebSocketTransport } from '@colyseus/ws-transport';

new WebSocketTransport({
  server,                // HTTP server instance
  pingInterval: 30000,    // Ping interval (ms)
  pingMaxRetries: 3,      // Max retries before disconnect
});

// Development: simulate latency
if (process.env.NODE_ENV !== 'production') {
  gameServer.simulateLatency(200);
}
```

## Scaling with Redis

```typescript
import { Server, RedisPresence, RedisDriver } from 'colyseus';

const gameServer = new Server({
  presence: new RedisPresence(),  // Multi-process communication
  driver: new RedisDriver(),       // Room storage across processes
});
```

## Best Practices

1. **Always use ESM** - `"type": "module"` in package.json
2. **Validate all inputs** - Never trust client data
3. **Rate limit actions** - Prevent spam exploits
4. **Log room lifecycle** - For debugging
5. **Use Schema for state** - Efficient binary serialization

## Common Mistakes

| ❌ Wrong | ✅ Right |
|----------|----------|
| `require/module.exports` | `import/export` with `"type": "module"` |
| Server using `colyseus.js` | Server uses `colyseus` package |
| Trusting client positions | Validate all inputs server-side |

## Reference

- [Colyseus Server Docs](https://docs.colyseus.io/server)
- [Room Handlers](https://docs.colyseus.io/server/room/)

---

## Room Lifecycle Best Practices (Updated 2026-01-28)

From arch-003 retrospective - proven patterns for Colyseus room implementation.

### Lifecycle Event Order

```
onCreate (once) → onAuth (per client) → onJoin (per client) → onMessage (loop)
→ onLeave (per client) → onDispose (once, when no clients)
```

### onCreate Implementation Pattern

```typescript
import { Room, Client } from 'colyseus';
import { MyRoomState } from '../schema/MyRoomState';

export class MyRoom extends Room<MyRoomState> {
  maxClients = 64;  // Set on class for 64-player FFA

  onCreate(options: any) {
    // 1. Initialize state
    this.setState(new MyRoomState());

    // 2. Set patch rate (20Hz = 50ms for multiplayer games)
    this.setPatchRate(50);  // 50ms = 20 ticks/sec

    // 3. Set up simulation interval (optional game loop)
    this.setSimulationInterval((deltaTime) => {
      this.gameLoop(deltaTime);
    });

    // 4. Register message handlers
    this.onMessage('input', (client, data) => {
      this.handlePlayerInput(client, data);
    });

    console.log(`[Room ${this.roomId}] Created with options:`, options);
  }

  onAuth(client: Client, options: any): boolean | Promise<any> {
    // Return true to allow, false/error to reject
    // Can return Promise for async validation
    return true;
  }

  onJoin(client: Client, options: any) {
    console.log(`[Room ${this.roomId}] Client joined: ${client.sessionId}`);

    // Create player state
    const player = new PlayerState();
    player.sessionId = client.sessionId;
    this.state.players.set(client.sessionId, player);

    // Send welcome message
    client.send('welcome', { sessionId: client.sessionId });
  }

  onLeave(client: Client, consented: boolean) {
    console.log(`[Room ${this.roomId}] Client left: ${client.sessionId} (consented: ${consented})`);

    // Remove player from state
    this.state.players.delete(client.sessionId);
  }

  onDispose() {
    console.log(`[Room ${this.roomId}] Disposed`);
  }

  private gameLoop(deltaTime: number) {
    // Game logic here
  }
}
```

### Room Configuration Best Practices

| Configuration | Value | Purpose |
|--------------|-------|---------|
| `maxClients` | 64 | FFA mode capacity |
| `patchRate` | 50ms | 20Hz state sync for multiplayer |
| `autoDispose` | true | Cleanup when empty (default) |
| `setSimulationInterval` | 16.6ms | 60Hz game loop (optional) |

### Message Handler Pattern

```typescript
// Specific message type
this.onMessage('move', (client, data) => {
  const player = this.state.players.get(client.sessionId);
  if (player) {
    player.x = data.x;
    player.y = data.y;
  }
});

// Catch-all for other messages
this.onMessage('*', (client, type, data) => {
  console.log(`Unhandled message: ${type}`, data);
});
```

**Sources:**
- https://docs.colyseus.io/colyseus/server/room/
- **Learned from arch-003 retrospective (2026-01-28)**
