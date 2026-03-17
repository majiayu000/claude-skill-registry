---
name: websocket-hub-patterns
model: standard
description: Horizontally-scalable WebSocket hub pattern with lazy Redis subscriptions, connection registry, and graceful shutdown. Use when building real-time WebSocket servers that scale across multiple instances. Triggers on WebSocket hub, WebSocket scaling, connection registry, Redis WebSocket, real-time gateway, horizontal scaling.
---

# WebSocket Hub Patterns

Production patterns for horizontally-scalable WebSocket connections with Redis-backed coordination.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install websocket-hub-patterns
```


---

## When to Use

- Real-time bidirectional communication
- Chat applications, collaborative editing
- Live dashboards with client interactions
- Need horizontal scaling across multiple gateway instances

---

## Hub Structure

```go
type Hub struct {
    // Local state
    connections   map[*Connection]bool
    subscriptions map[string]map[*Connection]bool // channel -> connections

    // Channels
    register   chan *Connection
    unregister chan *Connection
    broadcast  chan *Event

    // Redis for scaling
    redisClient  *redis.Client
    redisSubs    map[string]*goredis.PubSub
    redisSubLock sync.Mutex

    // Optional: Distributed registry
    connRegistry *ConnectionRegistry
    instanceID   string

    // Shutdown
    done chan struct{}
    wg   sync.WaitGroup
}
```

---

## Hub Main Loop

```go
func (h *Hub) Run() {
    for {
        select {
        case <-h.done:
            return

        case conn := <-h.register:
            h.connections[conn] = true
            if h.connRegistry != nil {
                h.connRegistry.RegisterConnection(ctx, conn.ID(), info)
            }

        case conn := <-h.unregister:
            if _, ok := h.connections[conn]; ok {
                if h.connRegistry != nil {
                    h.connRegistry.UnregisterConnection(ctx, conn.ID())
                }
                h.removeConnection(conn)
            }

        case event := <-h.broadcast:
            h.broadcastToChannel(event)
        }
    }
}
```

---

## Lazy Redis Subscriptions

Subscribe to Redis only when first local subscriber joins:

```go
func (h *Hub) subscribeToChannel(conn *Connection, channel string) error {
    // Add to local subscriptions
    if h.subscriptions[channel] == nil {
        h.subscriptions[channel] = make(map[*Connection]bool)
    }
    h.subscriptions[channel][conn] = true

    // Lazy: Only subscribe to Redis on first subscriber
    h.redisSubLock.Lock()
    defer h.redisSubLock.Unlock()

    if _, exists := h.redisSubs[channel]; !exists {
        pubsub := h.redisClient.Subscribe(context.Background(), channel)
        h.redisSubs[channel] = pubsub
        go h.forwardRedisMessages(channel, pubsub)
    }

    return nil
}

func (h *Hub) unsubscribeFromChannel(conn *Connection, channel string) {
    if subs, ok := h.subscriptions[channel]; ok {
        delete(subs, conn)

        // Cleanup when no local subscribers
        if len(subs) == 0 {
            delete(h.subscriptions, channel)
            h.closeRedisSubscription(channel)
        }
    }
}
```

---

## Redis Message Forwarding

```go
func (h *Hub) forwardRedisMessages(channel string, pubsub *goredis.PubSub) {
    ch := pubsub.Channel()
    for {
        select {
        case <-h.done:
            return
        case msg, ok := <-ch:
            if !ok {
                return
            }
            h.broadcast <- &Event{
                Channel: channel,
                Data:    []byte(msg.Payload),
            }
        }
    }
}

func (h *Hub) broadcastToChannel(event *Event) {
    subs := h.subscriptions[event.Channel]
    for conn := range subs {
        select {
        case conn.send <- event.Data:
            // Sent
        default:
            // Buffer full - close slow client
            h.removeConnection(conn)
        }
    }
}
```

---

## Connection Write Pump

```go
func (c *Connection) writePump() {
    ticker := time.NewTicker(54 * time.Second) // Ping interval
    defer func() {
        ticker.Stop()
        c.conn.Close()
    }()

    for {
        select {
        case message, ok := <-c.send:
            c.conn.SetWriteDeadline(time.Now().Add(10 * time.Second))
            if !ok {
                c.conn.WriteMessage(websocket.CloseMessage, []byte{})
                return
            }
            c.conn.WriteMessage(websocket.TextMessage, message)

            // Batch drain queue
            for i := 0; i < len(c.send); i++ {
                c.conn.WriteMessage(websocket.TextMessage, <-c.send)
            }

        case <-ticker.C:
            if err := c.conn.WriteMessage(websocket.PingMessage, nil); err != nil {
                return
            }
        }
    }
}
```

---

## Connection Registry for Horizontal Scaling

```go
type ConnectionRegistry struct {
    client     *redis.Client
    instanceID string
}

func (r *ConnectionRegistry) RegisterConnection(ctx context.Context, connID string, info ConnectionInfo) error {
    info.InstanceID = r.instanceID
    data, _ := json.Marshal(info)
    return r.client.Set(ctx, "ws:conn:"+connID, data, 2*time.Minute).Err()
}

func (r *ConnectionRegistry) HeartbeatInstance(ctx context.Context, connectionCount int) error {
    info := InstanceInfo{
        InstanceID:  r.instanceID,
        Connections: connectionCount,
    }
    data, _ := json.Marshal(info)
    return r.client.Set(ctx, "ws:instance:"+r.instanceID, data, 30*time.Second).Err()
}
```

---

## Graceful Shutdown

```go
func (h *Hub) Shutdown() {
    close(h.done)

    // Close all Redis subscriptions
    h.redisSubLock.Lock()
    for channel, pubsub := range h.redisSubs {
        pubsub.Close()
        delete(h.redisSubs, channel)
    }
    h.redisSubLock.Unlock()

    // Close all connections
    for conn := range h.connections {
        conn.Close()
    }

    h.wg.Wait()
}
```

---

## Decision Tree

| Situation | Approach |
|-----------|----------|
| Single instance | Skip ConnectionRegistry |
| Multi-instance | Enable ConnectionRegistry |
| No subscribers to channel | Lazy unsubscribe from Redis |
| Slow client | Close on buffer overflow |
| Need message history | Use Redis Streams + Pub/Sub |

---

## Related Skills

- **Meta-skill:** [ai/skills/meta/realtime-dashboard/](../../meta/realtime-dashboard/) — Complete realtime dashboard guide
- [dual-stream-architecture](../dual-stream-architecture/) — Event publishing
- [resilient-connections](../resilient-connections/) — Connection resilience

---

## NEVER Do

- **NEVER block on conn.send** — Use select with default to detect overflow
- **NEVER skip graceful shutdown** — Clients need close frames
- **NEVER share pubsub across channels** — Each channel needs own subscription
- **NEVER forget instance heartbeat** — Dead instances leave orphaned connections
- **NEVER send without ping/pong** — Load balancers close "idle" connections
