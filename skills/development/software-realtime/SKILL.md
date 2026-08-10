---
name: software-realtime
description: "Designs real-time and collaborative systems. Use when building chat, live dashboards, collaborative editing, notifications, WebSockets, SSE, or CRDT workflows."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# Real-Time Systems

Use this skill for transport choice, collaborative-state design, presence models, reconnection behavior, and multi-node real-time scaling. It owns SSE, WebSocket, CRDT, and managed real-time decisions, not generic backend APIs or frontend-only state management.

## Quick Reference

| Task | Use |
|------|-----|
| Transport selection | [references/transport-selection.md](references/transport-selection.md) |
| Collaboration, presence, and recovery | [references/collaboration-patterns.md](references/collaboration-patterns.md) |
| Vendor traps and version-pinned gotchas | [references/april-vendor-traps.md](references/april-vendor-traps.md) |
| Edge platforms, CRDT picks, channel limits | [references/edge-realtime.md](references/edge-realtime.md) | PartyKit, Liveblocks v2, Supabase, Socket.IO v4, Yjs/Loro |
| WebSocket smoke test (ping/pong + reconnect) | [scripts/ws_smoke_test.py](scripts/ws_smoke_test.py) | asserts pong < 500 ms and reconnect |
| Source map | [data/sources.json](data/sources.json) |

## When to Use This Skill

- Choose between SSE, WebSocket, managed real-time, or CRDT collaboration.
- Design chat, live dashboards, notifications, presence, or collaborative editing.
- Plan reconnection, backpressure, offline queues, and connection lifecycle.
- Scale WebSocket or collaboration infrastructure across multiple nodes.

## Route Elsewhere

- Request-response APIs or background jobs: use [software-backend](../software-backend/SKILL.md).
- System-level event architecture: use [software-architecture-design](../software-architecture-design/SKILL.md).
- Frontend state-management-only questions: use [software-frontend](../software-frontend/SKILL.md).
- Mobile push-notification delivery: use [software-mobile](../software-mobile/SKILL.md).
- Streaming AI response UX: use [software-ai-integration](../software-ai-integration/SKILL.md).

## Defaults

- Default to SSE for one-way text/event streaming.
- Default to WebSocket for bidirectional interactive flows.
- Default to CRDTs for collaborative editing and keep awareness separate from document state.
- Treat presence as its own data model with throttling and expiry rules.
- Design reconnects, idempotency, and slow-consumer handling before worrying about horizontal scale.

## Workflow

1. Classify the real-time shape: one-way stream, bidirectional messaging, shared collaborative state, or managed service need.
2. Choose the transport or collaboration model before touching implementation detail.
3. Define connection lifecycle, auth handoff, retries, presence semantics, and durability.
4. Add multi-node fan-out and recovery only after the single-node model is sound.
5. Verify current library or vendor behavior before final recommendations when the choice is version-sensitive.

## ASCII Flow

```text
Realtime task
  -> Identify collaboration, feed, presence, notification, or streaming shape
  -> Choose WebSocket, SSE, pub/sub, CDC, or managed realtime layer
  -> Define ordering, presence, auth, recovery, and backpressure
  -> Implement reconnect, replay, dedupe, and observability
  -> Verify provider and runtime behavior
  -> Test disconnects, slow consumers, and duplicate delivery
```

## Core Decisions

### Transport Choice

| Use Case | Transport | Reason |
|----------|-----------|--------|
| Dashboards, feeds, notifications | SSE | One-way, HTTP-native, browser handles reconnect |
| Chat, multiplayer, live cursors, client-originated messages | WebSocket | Bidirectional session required |
| Sub-frame media/game state where occasional loss beats head-of-line blocking | WebTransport | Unreliable + unordered datagrams over QUIC; reached Baseline (all major engines, including Safari 26.4, March 2026) — verify current before committing infra |
| Peer-to-peer audio/video or direct browser-to-browser data | WebRTC (media tracks or data channels) | Only path for sub-second p2p media; needs a TURN/STUN fallback and, for >4-6 peers, an SFU instead of mesh |
| Shared documents / state that must merge under concurrency | CRDT-backed collaboration | Avoids hand-rolled merge logic |
| Team owns connection infra as a core advantage | Custom WebSocket + pub/sub | Full control |
| Team wants to avoid connection layer ops | Managed pub/sub (Ably, Pusher, Supabase Realtime, PartyKit) or serverless WebSocket (AWS API Gateway WebSocket, Azure Web PubSub) | Faster path, vendor limits apply |

**WebTransport reality check (verify current before recommending it as default):** it is a genuine third option now, not just "emerging" — but adopting it still means every CDN, corporate proxy, and load balancer in the request path must support HTTP/3/QUIC, and server-side library maturity lags WebSocket's. Default to WebSocket unless the product specifically needs unreliable/unordered delivery (game state, live media metadata) or multiplexed independent streams without head-of-line blocking. Do not migrate an existing working WebSocket system to WebTransport for its own sake.

### Collaboration and Presence

- Use CRDTs (Yjs, Loro) over hand-rolled merge semantics; merge bugs are subtle and rare.
- Keep awareness data (cursors, typing, online status) in a separate `provider.awareness` object, not in the durable document.
- Throttle presence updates to at most every 50–100ms; cursor movement generates too many small events.
- Plan storage, sync, and recovery as a single design decision — retrofitting recovery after storage is built is expensive.

### Connection Management

- Reconnect backoff: initial 1s, double each attempt, cap at 30s, add ±20% jitter.
- Auth: browser WebSocket auth uses query params or first-message auth, not custom HTTP headers (the handshake follows HTTP but upgrade straps away standard auth headers).
- Heartbeat: send a keepalive every 25–30s to prevent proxy timeout; detect silence on the server to expire ghost connections.
- Slow consumers: bound server-side outbound queues; drop or backpressure rather than growing buffers to OOM.
- Offline queues: assign stable `op_id` to each outbound message for idempotent replay; cap queue size and surface an error if exceeded.

**Heartbeat interval budget (re-derive from your own proxy/LB idle timeout, never reuse this number):** if the tightest intermediary idle timeout in the path (LB, corporate proxy, CDN) is 60s, send heartbeats at ≤ half that (≤30s) so at least one heartbeat lands before the timeout fires even under jitter; set server-side dead-connection detection at 2–3× the heartbeat interval (60–90s here) so one dropped heartbeat frame does not trigger a false disconnect.

**Connection memory sizing (re-derive from your own runtime's measured per-connection footprint):** per-connection memory is socket buffers + per-connection application state (auth context, subscriptions, outbound queue). Example only: a Node.js process with ~40 KB average overhead per idle WebSocket connection (socket buffers + framing + app state — measure this on your stack, it varies by runtime and TLS termination point) supports roughly 2 GB ÷ 40 KB ≈ 50,000 idle connections per instance before OS file-descriptor or memory limits become the binding constraint — check `ulimit -n` and kernel ephemeral-port/conntrack limits separately, since those often cap lower than the memory math suggests.

### Scaling

- WebSocket fleets: shared pub/sub (Redis, NATS) plus sticky-session-aware load balancing (or stateless room routing).
- Presence and room membership: must work across nodes — do not store room state only in process memory.
- Deployments: plan graceful client reconnect on rolling restarts, not just health-check wiring.
- Sticky sessions are a load-balancer contract, not a WebSocket protocol feature: pick IP-hash or cookie-based affinity, and confirm the LB supports **connection draining** (finish in-flight connections before removal) before every deploy — without it, rolling restarts hard-kill live sessions instead of letting clients reconnect gracefully.
- Broker choice for fan-out is a durability decision, not just throughput: Redis Pub/Sub is fire-and-forget (sub-ms, but a disconnected consumer loses messages — fine for presence/cursors); Redis Streams adds consumer groups and replay at modest cost; Kafka is the right default once you need per-partition ordering, retention/replay across many consumer groups, or fan-out beyond what one Redis node's CPU/network can push. Do not reach for Kafka to fan out ephemeral presence pings — that is Redis Pub/Sub or Streams territory.

**Fan-out math (re-derive per system — do not reuse this example's numbers):** for N connected clients each needing every message at rate M msg/s, naive per-connection publish costs N × M outbound sends/s from the fan-out tier. Example: 20,000 WebSocket clients in one room, each needing 2 updates/s → the fan-out tier must sustain 20,000 × 2 = 40,000 sends/s just for that room, before framing/serialization overhead. A single Redis Pub/Sub node topping out in the low hundreds-of-thousands of ops/s can absorb this for one room but not for hundreds of similarly sized rooms concurrently — shard by room key across multiple Redis instances or move to Kafka partitions once aggregate demand approaches the broker's measured ceiling (benchmark, do not assume a published number holds for your message size and TLS overhead).

## Output Modes

Default to one of these:

- Transport decision memo:
  SSE, WebSocket, managed service, or CRDT with tradeoffs.
- Realtime architecture brief:
  rooms, presence, persistence, reconnect, and scale path.
- Collaboration plan:
  document model, awareness, sync transport, and recovery notes.

## Known Traps

| Trap | Consequence | Fix |
|------|-------------|-----|
| Auth only on initial handshake; reconnect path undefined | Reconnect after token expiry fails silently | Handle token refresh in reconnect loop |
| Treating presence/typing signals as durable truth | Stale cursors on reconnect; unbounded storage growth | Ephemeral TTL store (Redis `SETEX`); expiry at 2× heartbeat interval |
| Offline queues without stable `op_id` and dedupe policy | Duplicate state on replay | Assign `op_id` before queuing; server deduplicates idempotently |
| Scaling to multi-node before single-node protocol is stable | Fan-out bugs are hard to reproduce across nodes | Validate room semantics on a single node first |
| Choosing WebSocket by habit for one-way server push | Unnecessary bidirectional session overhead | Evaluate SSE; if client never sends messages, SSE is cheaper |
| Adopting WebTransport because it reached Baseline, without checking the request path | Corporate proxies, some CDNs, and older mobile carrier networks still block or downgrade UDP/QUIC; connection silently falls back or fails | Test on the actual target network mix (corporate VPN, carrier NAT); keep a WebSocket fallback path for at least one release cycle |
| Sizing a WebSocket fleet from a published per-connection memory or DO connection-count figure without measuring on your own runtime | Instance falls over well below the "documented" ceiling because TLS termination point, message size, and per-connection app state differ from the vendor's benchmark | Load test at target CCU with production-representative payloads before trusting any vendor capacity number |

## Anti-Patterns

| Anti-Pattern | Problem | Better Default |
|--------------|---------|----------------|
| WebSocket for server-to-client-only feeds | Bidirectional overhead, sticky LB required | SSE: HTTP-native, browser handles reconnect |
| Persisting awareness data (cursors, typing) in durable document state | Unbounded storage growth; stale cursors on reconnect | `provider.awareness` object only; TTL store for presence |
| Missing heartbeat / reconnect logic | Silent drops on idle paths; duplicate replays | Heartbeat every 25–30s; reconnect with `op_id` dedupe |
| Multi-node scale before single-node protocol is stable | Fan-out bugs are hard to reproduce | Validate room, ack, recovery on one node first |
| Trusting vendor marketing pages as architecture proof | Hidden CCU limits, per-room single-thread constraints | Read changelogs, test at target CCU; see [references/april-vendor-traps.md](references/april-vendor-traps.md) |

## Scenarios

Five numbered scenarios covering the most common real-time design moments. Each lists the shortest path using patterns above.

### S1 — Presence channel for online users with stale-cleanup

1. Model presence as ephemeral key-value entries keyed by `user_id`; include a `last_seen` timestamp on each heartbeat.
2. Publish presence updates at most every 5 seconds; throttle high-frequency ping loops on the client.
3. On server, expire any entry where `last_seen` is older than 2× the heartbeat interval.
4. Broadcast presence diffs (join/leave/update) to room subscribers, not the full member list.
5. On reconnect, re-publish the client's own presence before subscribing to the room's current snapshot.
6. Keep presence data in a fast TTL store (Redis `SETEX`) separate from durable document state.

### S2 — Reconnect with exponential backoff + queued ops

1. On disconnect, enter a reconnect loop: initial delay 1s, double each attempt, cap at 30s, add ±20% jitter.
2. Queue outbound operations locally while offline; assign each a stable `op_id` for deduplication on replay.
3. On reconnect, re-authenticate (token refresh if needed), then replay the queue in order.
4. The server deduplicates by `op_id`; idempotent apply means safe replay without double-writes.
5. If the queue exceeds a size limit, surface an error to the user rather than dropping silently.
6. Emit connection-state events (`connecting`, `connected`, `disconnected`) so the UI can show status.

### S3 — Yjs CRDT collaborative doc sync with awareness

1. Initialize a `Y.Doc` per document; connect via a WebSocket provider (`y-websocket` or `PartyKit`).
2. Persist document updates to durable storage (Postgres, Supabase) using the binary `Y.encodeStateAsUpdate` format.
3. Keep awareness data (cursors, selection, name) in a separate `provider.awareness` object; never write it to the doc.
4. Throttle awareness broadcasts to at most 50ms; rapid cursor movement generates too many small updates.
5. On client reconnect, call `Y.applyUpdate` with the server state before broadcasting local pending updates.
6. Test concurrent edits from two clients with network partition; confirm the doc converges after reconnect.

### S4 — SSE vs WebSocket choice for a one-way live dashboard

1. Confirm the dashboard receives server-pushed updates and never sends user input back to the server.
2. Choose SSE: HTTP/1.1 compatible, reconnect handled by the browser natively, no upgrade handshake needed.
3. Implement the server endpoint as a streaming HTTP response with `Content-Type: text/event-stream`.
4. Include `id:` fields on each event so the browser resumes from the last received event after reconnect.
5. Add a server-side heartbeat comment (`: keepalive`) every 25 seconds to prevent proxy timeout.
6. Reject WebSocket if the only requirement is server-to-client push; SSE is simpler and operationally cheaper.

### S5 — PartyKit room sharding for >5k concurrent users

1. Verify the default single-Durable-Object-per-room limit; one room instance handles a bounded connection count.
2. Shard large rooms by assigning users to sub-rooms (e.g., `room:{id}:shard:{n}`) based on `user_id % shard_count`.
3. Broadcast cross-shard events via a coordinator object that fans out to all shard instances.
4. Keep presence and room membership aggregated at the coordinator level, not replicated per shard.
5. Test shard rebalancing behavior when a shard instance restarts; clients should reconnect to the same shard.
6. Monitor per-shard connection count via PartyKit metrics; auto-scale shard count before hitting the ceiling.

## Navigation

- Core references: [references/transport-selection.md](references/transport-selection.md), [references/collaboration-patterns.md](references/collaboration-patterns.md), [references/april-vendor-traps.md](references/april-vendor-traps.md)
- Source map: [data/sources.json](data/sources.json)
- Scripts: [scripts/check_ws_smoke.py](scripts/check_ws_smoke.py)
- Related skills: [software-backend](../software-backend/SKILL.md), [software-baas-platforms](../software-baas-platforms/SKILL.md), [software-frontend](../software-frontend/SKILL.md), [software-architecture-design](../software-architecture-design/SKILL.md), [software-mobile](../software-mobile/SKILL.md), [qa-resilience](../qa-resilience/SKILL.md), [software-security-appsec](../software-security-appsec/SKILL.md)
- [references/distributed-systems-applied.md](references/distributed-systems-applied.md) — CAP/PACELC, consensus, idempotency, quorums applied to real-time and collaborative systems.

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- Verify current library, managed-service, and protocol behavior before presenting version-sensitive recommendations as current fact.
- Prefer official documentation, changelogs, and release notes over blog summaries.
- If live verification is unavailable, mark vendor-specific claims as unverified.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.

