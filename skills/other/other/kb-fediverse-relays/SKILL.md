---
name: kb-fediverse-relays
description: >
  Background knowledge about how relays work on the Fediverse, including
  at the ActivityPub wire-format level. Load when the user asks about
  implementing a relay, subscribing to a relay, the relay subscription
  handshake (Follow/Accept to the Public collection), the two relay
  protocols (Mastodon relay protocol vs LitePub/Pleroma relay protocol),
  the /inbox vs /actor subscription endpoints, how relays re-broadcast
  activities using Announce, message forwarding vs message relaying, relay
  actor types, relay software (pub-relay, Activity-Relay, aode-relay,
  buzzrelay), topic-based or hashtag-filtered relays (FediBuzz), resource
  impact of relays, relay moderation, or why the federated timeline is
  empty on a new instance. Also load when reviewing or writing code that
  implements relay functionality, subscribes to a relay, or processes
  relayed activities.
user-invocable: false
---

# Fediverse Relays — Complete Reference

## Overview

A relay is a service-type ActivityPub actor that re-broadcasts public
content between subscribed servers. It solves a core discovery problem:
without relays, a new or small instance only sees content from accounts
its users explicitly follow, leaving the federated timeline empty and
hashtag search incomplete.

Relays function as "a commons of public content" — participating servers
send their public posts to the relay, and the relay distributes them to
all other subscribers. This is an admin-level operation, not something
individual users control.

There is no separate relay specification. Relay behaviour is an
application of the core ActivityPub spec, primarily using the `Announce`
activity type and the standard `Follow`/`Accept` subscription flow.

---

## 1. The Relay Actor

A relay is represented as an ActivityPub actor, typically with
`"type": "Application"` or `"type": "Service"`. It exposes the standard
endpoints needed for federation:

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    "https://w3id.org/security/v1"
  ],
  "type": "Application",
  "id": "https://relay.example.com/actor",
  "inbox": "https://relay.example.com/inbox",
  "publicKey": {
    "id": "https://relay.example.com/actor#main-key",
    "owner": "https://relay.example.com/actor",
    "publicKeyPem": "-----BEGIN PUBLIC KEY-----\nMIIB...\n-----END PUBLIC KEY-----"
  },
  "url": "https://relay.example.com/actor",
  "endpoints": {
    "sharedInbox": "https://relay.example.com/inbox"
  }
}
```

Key points:
- The relay actor's `inbox` is where subscribing servers send activities
- The `publicKey` is used for HTTP Signature verification
- Most relay implementations also expose `/.well-known/webfinger`,
  `/.well-known/nodeinfo`, and `/nodeinfo/2.0` for discovery

---

## 2. The Subscription Handshake

### Subscribing — Follow the Public collection

A server subscribes to a relay by sending a `Follow` activity where the
`object` is the special public collection URI:

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://instance.example/activities/relay-follow-1",
  "type": "Follow",
  "actor": "https://instance.example/actor",
  "object": "https://www.w3.org/ns/activitystreams#Public"
}
```

Requirements:
- The `object` field **must** be exactly
  `"https://www.w3.org/ns/activitystreams#Public"` — this is what
  distinguishes a relay subscription from a normal user follow
- The `actor` must resolve to an object with both `inbox` and
  `endpoints.sharedInbox` properties
- The request must be signed with a valid HTTP Signature

### Acceptance

On successful subscription, the relay responds with an `Accept`:

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://relay.example.com/activities/accept-1",
  "type": "Accept",
  "actor": "https://relay.example.com/actor",
  "object": {
    "type": "Follow",
    "actor": "https://instance.example/actor",
    "object": "https://www.w3.org/ns/activitystreams#Public"
  }
}
```

Some relays require manual approval before sending the `Accept`. The
subscribing server should handle an indefinite pending state gracefully.

### Unsubscribing — Undo Follow

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://instance.example/activities/undo-relay-follow-1",
  "type": "Undo",
  "actor": "https://instance.example/actor",
  "object": {
    "type": "Follow",
    "actor": "https://instance.example/actor",
    "object": "https://www.w3.org/ns/activitystreams#Public"
  }
}
```

---

## 3. The Two Relay Protocols

Two protocols exist in the wild. They differ in how a server addresses
the relay when subscribing, but the underlying ActivityPub mechanics
are the same.

### Mastodon Relay Protocol

- The subscribing server uses the relay's **inbox endpoint IRI** —
  e.g. `https://relay.example.com/inbox`
- Uses HTTP Signatures for verification
- Uses the standard `Follow`/`Accept` flow described above
- Subscription is performed at the server admin level only

### LitePub / Pleroma Relay Protocol

- The subscribing server uses the relay's **actor document IRI** —
  e.g. `https://relay.example.com/actor`
- The inbox is derived automatically from the actor document
- Allows any actor to communicate with relays, not just admin-controlled
  instance actors
- LitePub is a set of conventions extending ActivityPub

### Which endpoint to use

| Platform | Subscription Endpoint |
|---|---|
| Mastodon | `/inbox` |
| Misskey and forks | `/inbox` |
| Pleroma / Akkoma | `/actor` |
| snac | `/actor` |

Both endpoints are typically served by the same relay software. A relay
that supports both protocols will accept subscriptions at either
endpoint.

---

## 4. How Relays Process Activities

Once a server is subscribed, it sends all its public activities to the
relay's inbox. The relay then distributes them to all other subscribers
using one of two mechanisms:

### Message relaying (Announce wrapping)

For `Create` and `Announce` activities, the relay wraps the object in a
new `Announce` activity attributed to the relay actor:

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://relay.example.com/announces/789",
  "type": "Announce",
  "actor": "https://relay.example.com/actor",
  "object": "https://instance.example/users/alice/statuses/123",
  "to": ["https://www.w3.org/ns/activitystreams#Public"],
  "cc": []
}
```

This is the primary distribution mechanism. The receiving server sees an
`Announce` from the relay and fetches the original object if needed.

### Message forwarding (direct re-delivery)

For `Update`, `Delete`, `Like`, `Undo`, `Move`, `Add`, and `Remove`
activities, the relay POSTs the activity directly to all subscribers
**unmodified** — it does not wrap it in an `Announce`.

This is necessary because wrapping these activity types in `Announce`
would change their semantics (e.g. an `Announce{Delete}` does not mean
the same thing as a `Delete`).

### LD-Signatures and forwarding

Activities that carry valid linked-data signatures can be forwarded
directly (the recipient can verify the original author's signature).
Activities that lack LD-signatures must be wrapped in `Announce` instead,
because the relay cannot prove the activity's origin otherwise.

### Filtering rules

Most relay implementations apply these filters:
- Only activities addressed to `https://www.w3.org/ns/activitystreams#Public`
  (in `to` or `cc`) are accepted
- Activities older than ~30 minutes are skipped
- Duplicate activity IDs are rejected to prevent reprocessing

---

## 5. Relay Endpoints

A typical relay exposes these HTTP endpoints:

| Endpoint | Method | Purpose |
|---|---|---|
| `/actor` | GET | Returns the relay's ActivityPub actor document |
| `/inbox` | POST | Receives activities from subscribers |
| `/.well-known/webfinger` | GET | WebFinger discovery |
| `/.well-known/nodeinfo` | GET | NodeInfo discovery document |
| `/nodeinfo/2.0` | GET | NodeInfo schema (software name, version, stats) |

Some implementations also expose:
- `/stats` — relay statistics (subscriber count, activity throughput)

---

## 6. Types of Relays

### General-purpose relays

Broadcast **all** public content from all subscribed servers. Maximum
content discovery, but high resource cost. A general relay with a few
large, active servers subscribed will generate significantly more traffic
than one with many small servers.

### Geographic / community relays

Restricted to servers in a specific region or community. Reduces volume
while keeping content culturally relevant. Examples include relays
limited to Australian/New Zealand instances or Canadian instances.

### Topic-based / selective relays (FediBuzz model)

FediBuzz (relay.fedi.buzz) takes a fundamentally different approach.
Instead of receiving activities from subscribers, it connects to
Mastodon's Streaming API and allows per-subscriber customisation:

- **Follow specific hashtags** — only relay posts matching chosen tags
  (supports smart matching: following `#dd` captures `#dd1302` etc.)
- **Follow specific instances** — only relay posts from chosen servers
- **Language filtering** — only relay posts in chosen languages

This dramatically reduces resource consumption compared to general
relays. The trade-off is that it requires API access to source instances
rather than using the standard relay subscription model.

---

## 7. Building a Relay — Implementation Guide

### Minimum viable relay

A minimal relay implementation must:

1. **Serve an actor document** at a stable URL with a valid `publicKey`,
   `inbox`, and `endpoints.sharedInbox`
2. **Accept `Follow` activities** where the `object` is
   `as:Public` — validate HTTP Signatures, store the subscriber, and
   respond with `Accept`
3. **Accept `Undo{Follow}`** — remove the subscriber
4. **Accept incoming activities** at the inbox — validate that they are
   addressed to Public, then distribute to all subscribers
5. **Distribute activities** — for each subscriber, POST the activity
   (or an `Announce` wrapping it) to the subscriber's `sharedInbox`
6. **Sign all outgoing requests** with HTTP Signatures using the relay
   actor's private key

### Activity types to handle

| Incoming activity | Relay action |
|---|---|
| `Follow` (object = `as:Public`) | Store subscriber; send `Accept` |
| `Undo{Follow}` | Remove subscriber |
| `Create` | Wrap in `Announce`; deliver to all subscribers |
| `Announce` | Wrap in `Announce` or forward; deliver to all subscribers |
| `Update` | Forward directly to all subscribers |
| `Delete` | Forward directly to all subscribers |
| `Like` | Forward directly to all subscribers |
| `Undo` (other than Follow) | Forward directly to all subscribers |
| `Move` | Forward directly to all subscribers |
| `Add` / `Remove` | Forward directly to all subscribers |

### Delivery optimisation

- Always use `sharedInbox` when available — sending one request per
  subscribing server instead of one per actor
- Use a job queue for async delivery — a relay with 100 subscribers
  means 100 outgoing HTTP requests per incoming activity
- Implement retry logic with exponential backoff for failed deliveries
- Cache resolved actors and their public keys (typical TTL: ~2 days)
- Skip delivery to servers that have been consistently unreachable

### HTTP Signatures

The relay must verify incoming HTTP Signatures and sign all outgoing
requests. See the HTTP Signatures knowledge base for full details.

Notable relay-specific concern: when forwarding an activity, the relay
signs the outgoing request with its own key. The `keyId` in the
`Signature` header is the relay actor's key, not the original author's.
This is why some implementations extract the actor from the `keyId`
rather than from the activity's `actor` field — they may differ when a
relay forwards content.

---

## 8. Subscribing to a Relay — Admin Guide

### Mastodon

1. Log in with admin credentials
2. Navigate to **Preferences > Administration > Relays**
3. Select **"Setup A Relay Connection"**
4. Enter the relay URL with the `/inbox` suffix
   (e.g. `https://relay.example.com/inbox`)
5. Click **"Save And Enable"**
6. Wait for approval if the relay requires it

### Pleroma / Akkoma

Use the CLI:
```
mix pleroma.relay follow https://relay.example.com/actor
```
or:
```
pleroma_ctl relay follow https://relay.example.com/actor
```

### Misskey and forks

Use the admin panel to add a relay with the `/inbox` endpoint.

### snac

Use the `/actor` endpoint:
```
https://relay.example.com/actor
```

---

## 9. Resource Impact and Trade-offs

### What relays cost

Subscribing to a relay increases:
- **Bandwidth** — every public post from every server on the relay is
  delivered to your inbox
- **Storage** — all relayed posts are stored locally (unless your
  software has a retention policy)
- **Processing** — each incoming activity must be validated, stored,
  and indexed
- **Moderation burden** — relayed content may include posts that violate
  your server's rules

### Sizing guidelines

- A general relay with a few large, very active servers will produce
  significantly more traffic than one with many small servers
- Topic-based relays (FediBuzz) are much lighter because they filter
  content before delivery
- Monitor disk usage and database size after subscribing — some admins
  report rapid growth

### When relays are most useful

- **New instances** with few users and an empty federated timeline
- **Small instances** that want better hashtag search coverage
- **Niche instances** that want to connect with related communities

### When relays may not be appropriate

- **Large instances** that already have strong organic federation
- **Resource-constrained servers** that cannot handle the additional load
- **Heavily moderated servers** where unfiltered relay content creates
  moderation overhead

---

## 10. Moderation and Security

### Content moderation gaps

Current relay implementations provide minimal moderation capabilities.
A relay typically re-broadcasts everything it receives without content
filtering. The subscribing server's own moderation tools (domain blocks,
keyword filters) still apply to relayed content, but the volume can make
moderation more difficult.

**Recommendation:** Verify a relay's content and subscriber list before
subscribing. Check whether the relay operator maintains a blocklist.

### No boost notifications

When a relay `Announce`s a post, the original author does **not** receive
a notification. The relay actor is the one performing the `Announce`, and
implementations treat relay announces differently from user boosts.

### Domain blocking

Some relay implementations (notably aode-relay) support domain
blocklisting and allowlisting:
- **Blocklist mode:** accept all subscribers except blocked domains
- **Allowlist mode (restricted):** only accept explicitly approved domains

### API token concerns

Some relay services (e.g. FediBuzz) request API tokens from subscribing
instances. This grants broader access than necessary — potentially
including followers-only and mentioned-only posts, which contradicts the
relay principle of only handling public content. Evaluate what access a
relay service requests before providing credentials.

---

## 11. Standardisation Efforts

### Current state

There is no formal relay specification. The relay concept emerged
organically from Mastodon's implementation and was independently
implemented by Pleroma using the LitePub protocol. This has led to
protocol fragmentation.

### FEP-a974

A Fediverse Enhancement Proposal (FEP-a974) exists to formalise relay
behaviour, addressing:
- Standard subscription and unsubscription flows
- Activity acceptance criteria
- Relay actor type definitions
- Terminology standardisation

### SocialHub discussions

The SocialHub ActivityPub forum has extensive ongoing discussion about
relay standardisation, including debates about:
- What to call servers that publish to and consume from relays
- Whether relays should have moderation capabilities
- How to handle the two competing subscription protocols

---

## 12. Existing Relay Software

| Software | Language | Protocol Support | Key Feature |
|---|---|---|---|
| pub-relay | Crystal | Mastodon + LitePub | Rigorous HTTP Signature verification; LD-signature-aware forwarding |
| Activity-Relay | Go | Mastodon + LitePub | Redis-backed job queue; CLI admin; YAML config |
| ActivityRelay (Pleroma) | Python | LitePub | Mature (14 releases); configurable DB backends |
| aode-relay | Rust | Mastodon + LitePub | Lightweight; blocklist/allowlist; Prometheus metrics; Telegram admin bot |
| buzzrelay (FediBuzz) | Rust | Follow-only | Streaming API approach; hashtag/instance/language filtering; PostgreSQL |

All are licensed under AGPLv3.

### Notable differences

- **pub-relay** is the closest to a reference implementation for the
  Mastodon relay protocol
- **Activity-Relay** requires Redis and has the most structured
  architecture (API server + job worker + control utility)
- **aode-relay** is the most feature-rich for moderation (blocklist,
  allowlist, restricted mode)
- **buzzrelay** is architecturally different — it connects to Mastodon's
  Streaming API rather than receiving activities at an inbox

---

## 13. Common Implementation Mistakes

- **Wrong `object` in the `Follow`**: subscribing with the relay actor's
  id as the `object` instead of `as:Public` — the relay will treat this
  as a normal follow, not a relay subscription
- **Missing `sharedInbox`**: if the subscribing server's actor does not
  expose `endpoints.sharedInbox`, the relay may not be able to deliver
  activities
- **Not handling both subscription protocols**: if building a relay,
  accept subscriptions at both `/inbox` and `/actor` to support all
  platforms
- **Wrapping `Delete` in `Announce`**: forwarding a `Delete` as
  `Announce{Delete}` changes its semantics — `Delete` should be
  forwarded directly
- **Not filtering non-public activities**: relays must only process
  activities addressed to `as:Public` — relaying non-public content
  violates user privacy
- **No deduplication**: without tracking processed activity IDs, the
  same activity can be relayed multiple times if it arrives through
  different paths
- **Not signing outgoing requests**: all deliveries from the relay must
  be signed with the relay actor's key, or receiving servers will reject
  them
- **Ignoring the `/actor` endpoint**: serving only `/inbox` and not
  an actor document at `/actor` breaks Pleroma/Akkoma/snac subscription
