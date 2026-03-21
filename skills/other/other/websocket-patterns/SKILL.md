---
name: websocket-patterns
description: Connection management, room patterns, reconnection strategies, message buffering, and binary protocol design.
---

# WebSocket Patterns

Production WebSocket patterns for real-time applications.

## Connection Management

```typescript
import { WebSocketServer, WebSocket } from 'ws'

interface Client {
  id: string
  ws: WebSocket
  rooms: Set<string>
  lastPing: number
  metadata: Record<string, unknown>
}

class ConnectionManager {
  private clients = new Map<string, Client>()
  private heartbeatInterval: NodeJS.Timeout

  constructor(private wss: WebSocketServer) {
    this.heartbeatInterval = setInterval(() => this.checkHeartbeats(), 30_000)

    wss.on('connection', (ws, req) => {
      const clientId = crypto.randomUUID()
      const client: Client = {
        id: clientId,
        ws,
        rooms: new Set(),
        lastPing: Date.now(),
        metadata: { ip: req.socket.remoteAddress }
      }
      this.clients.set(clientId, client)

      ws.on('pong', () => { client.lastPing = Date.now() })
      ws.on('close', () => this.removeClient(clientId))
      ws.on('error', () => this.removeClient(clientId))

      this.send(client, { type: 'connected', clientId })
    })
  }

  private checkHeartbeats(): void {
    const staleThreshold = Date.now() - 45_000
    for (const [id, client] of this.clients) {
      if (client.lastPing < staleThreshold) {
        client.ws.terminate()
        this.removeClient(id)
      } else {
        client.ws.ping()
      }
    }
  }

  private removeClient(id: string): void {
    const client = this.clients.get(id)
    if (!client) return
    for (const room of client.rooms) {
      this.leaveRoom(id, room)
    }
    this.clients.delete(id)
  }

  send(client: Client, data: unknown): void {
    if (client.ws.readyState === WebSocket.OPEN) {
      client.ws.send(JSON.stringify(data))
    }
  }

  destroy(): void {
    clearInterval(this.heartbeatInterval)
  }
}
```

## Room Pattern

```typescript
class RoomManager {
  private rooms = new Map<string, Set<string>>()

  joinRoom(clientId: string, room: string): void {
    if (!this.rooms.has(room)) {
      this.rooms.set(room, new Set())
    }
    this.rooms.get(room)!.add(clientId)
  }

  leaveRoom(clientId: string, room: string): void {
    const members = this.rooms.get(room)
    if (!members) return
    members.delete(clientId)
    if (members.size === 0) this.rooms.delete(room)
  }

  broadcast(room: string, data: unknown, excludeId?: string): void {
    const members = this.rooms.get(room)
    if (!members) return
    const payload = JSON.stringify(data)
    for (const id of members) {
      if (id === excludeId) continue
      const client = this.clients.get(id)
      if (client?.ws.readyState === WebSocket.OPEN) {
        client.ws.send(payload)
      }
    }
  }

  getRoomSize(room: string): number {
    return this.rooms.get(room)?.size ?? 0
  }
}
```

## Client-Side Reconnection

```typescript
class ReconnectingWebSocket {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectDelay = 30_000
  private messageBuffer: unknown[] = []
  private handlers = new Map<string, Function[]>()

  constructor(private url: string) {
    this.connect()
  }

  private connect(): void {
    this.ws = new WebSocket(this.url)

    this.ws.onopen = () => {
      this.reconnectAttempts = 0
      this.flushBuffer()
      this.emit('connected')
    }

    this.ws.onclose = (event) => {
      if (event.code === 1000) return  // Normal closure, no reconnect
      this.scheduleReconnect()
    }

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data as string)
      this.emit(data.type, data)
    }

    this.ws.onerror = () => {
      this.ws?.close()
    }
  }

  private scheduleReconnect(): void {
    // Exponential backoff with jitter
    const baseDelay = Math.min(1000 * 2 ** this.reconnectAttempts, this.maxReconnectDelay)
    const jitter = baseDelay * 0.3 * Math.random()
    const delay = baseDelay + jitter

    this.reconnectAttempts++
    setTimeout(() => this.connect(), delay)
  }

  send(data: unknown): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data))
    } else {
      // Buffer messages while disconnected (max 100)
      if (this.messageBuffer.length < 100) {
        this.messageBuffer.push(data)
      }
    }
  }

  private flushBuffer(): void {
    const buffered = [...this.messageBuffer]
    this.messageBuffer = []
    for (const msg of buffered) {
      this.send(msg)
    }
  }

  on(event: string, handler: Function): void {
    if (!this.handlers.has(event)) this.handlers.set(event, [])
    this.handlers.get(event)!.push(handler)
  }

  private emit(event: string, ...args: unknown[]): void {
    for (const handler of this.handlers.get(event) ?? []) {
      handler(...args)
    }
  }
}
```

## Message Protocol Design

```typescript
// Typed message envelope
interface WsMessage<T = unknown> {
  type: string
  id: string          // For request-response correlation
  timestamp: number
  payload: T
}

// Request-response over WebSocket
class WsRpc {
  private pending = new Map<string, { resolve: Function; timer: NodeJS.Timeout }>()

  async request<T>(type: string, payload: unknown, timeoutMs = 5000): Promise<T> {
    const id = crypto.randomUUID()
    const msg: WsMessage = { type, id, timestamp: Date.now(), payload }

    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id)
        reject(new Error(`RPC timeout: ${type}`))
      }, timeoutMs)

      this.pending.set(id, { resolve, timer })
      this.ws.send(JSON.stringify(msg))
    })
  }

  handleResponse(msg: WsMessage): void {
    const entry = this.pending.get(msg.id)
    if (!entry) return
    clearTimeout(entry.timer)
    this.pending.delete(msg.id)
    entry.resolve(msg.payload)
  }
}
```

## Checklist

- [ ] Heartbeat/ping-pong every 30s, terminate stale connections at 45s
- [ ] Exponential backoff with jitter for client reconnection (1s-30s)
- [ ] Message buffer during disconnection (cap at 100 messages)
- [ ] Auth token validation on initial handshake (not in messages)
- [ ] Room-based broadcasting for scoped message delivery
- [ ] Rate limit per client (max messages/second)
- [ ] Message size limit (max 1MB per frame)
- [ ] Graceful shutdown: close code 1001, drain messages before exit

## Anti-Patterns

- No heartbeat: zombie connections consuming resources
- Reconnecting without backoff: hammering server on outage
- Unbounded message buffer: memory leak during long disconnections
- Auth in every message: use connection-level auth, not per-message
- Broadcasting to all clients when only a room subset needs the update
- Synchronous JSON.parse in hot path: use worker threads for heavy payloads
