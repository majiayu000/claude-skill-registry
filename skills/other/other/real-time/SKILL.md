---
name: NestJS Real-Time
description: WebSocket and SSE selection strategies and scaling.
metadata:
  labels: [nestjs, websockets, sse, socket.io]
  triggers:
    files: ['**/*.gateway.ts', '**/*.controller.ts']
    keywords: [WebSocketGateway, SubscribeMessage, Sse, Socket.io]
---

# Real-Time & WebSockets

## **Priority: P1 (OPERATIONAL)**

WebSocket and real-time communication patterns with NestJS.

- **WebSockets (Bi-directional)**: Use for Chat, Multiplayer Games, Collaborative Editing.
  - _High Complexity_: Requires custom scaling (Redis Adapter) and sticky sessions (sometimes).
- **Server-Sent Events (SSE) (Uni-directional)**: Use for Notifications, Live Feeds, Tickers, CI Log streaming.
  - _Low Complexity_: Standard HTTP. Works with standard Load Balancers. Easy to secure.
  - _NestJS_: Use `@Sse('route')` returning `Observable<MessageEvent>`.
- **Long Polling**: Use **only** as a fallback or for extremely low-frequency updates (e.g., job status check every 10m).
  - _Impact_: High header overhead. Blocks threads if not handled carefully.

## WebSockets Implementation

- **Socket.io**: Default choice. Features "Rooms", "Namespaces", and automatic reconnection. Heavy protocol.
- **Fastify/WS**: Use `ws` adapter if performance is critical (e.g., high-frequency trading updates) and you don't need "Rooms" logic.

## Scaling (Critical)

- **WebSockets**: In K8s, a client connects to Pod A. If Pod B emits an event, the client won't receive it.
  - **Solution**: **Redis Adapter** (`@socket.io/redis-adapter`). Every pod publishes to Redis; Redis distributes to all other pods.
- **SSE**: Stateless. No special adapter needed, but be aware of **Connection Limits** (6 concurrent connections per domain in HTTP/1.1; virtually unlimited in HTTP/2).
  - **Rule**: Must use **HTTP/2** for SSE at scale.

## Security

- **Handshake Auth**: Standard HTTP Guards don't trigger on Ws connection efficiently.
  - **Pattern**: Validate JWT during the `handleConnection()` lifecycle method. Disconnect immediately if invalid.
- **Rate Limiting**: Sockets are expensive. Apply strict throttling on "Message" events to prevent flooding.

## Architecture

- **Gateway != Service**: The `WebSocketGateway` should **only** handle client comms (Join Room, Ack message).
  - **Rule**: Delegate business logic to a Service or Command Bus.
- **Events**: Use `AsyncApi` or `SocketApi` decorators (from community packages) to document WS events similarly to OpenAPI.
