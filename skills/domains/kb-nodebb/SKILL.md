---
name: kb-nodebb
description: >
  Background knowledge about NodeBB, the modern open-source forum software
  built on Node.js with native ActivityPub federation (core feature since
  v4.0.0, January 2025). Covers the three actor types (Person user at
  /u/username, Group category at /category/<cid> implementing FEP-1b12
  Group Federation with Announce relay pattern, Application instance
  actor), the two-level content hierarchy (category as audience → topic
  as context → post), how topics map to resolvable OrderedCollection
  contexts per FEP-7888 and posts are Note/Article objects, extensive
  FEP support (12 implemented: FEP-1b12 Group Federation, FEP-7888
  context property, FEP-f228 Backfilling Conversations, FEP-4f05 Soft
  Deletion, FEP-9098 Custom emojis, FEP-b2b8 Long-form Text, FEP-fe34
  Origin-based security, FEP-ae0c Relay Protocols, FEP-11dd Context
  Ownership, FEP-f15d Context Relocation, FEP-fb2a Actor metadata,
  FEP-0151 NodeInfo), the tech stack (Node.js/WebSocket/Socket.IO/
  MongoDB or Redis or PostgreSQL, GPL-3.0), content discovery (follow-
  based, URL paste to search, Uncategorized catch-all with auto-pruning,
  no relay support), per-category federation control with domain
  allow/deny lists, content pruning (30 days remote content, 7 days
  remote users), cross-posting between categories (v4.8.0+), hooks-based
  plugin system (filter/action/static/response hooks), and comparison
  with Discourse (core AP vs plugin AP). Load when the user asks about
  NodeBB; implementing a NodeBB-compatible ActivityPub server; how
  NodeBB categories federate as Group actors; NodeBB's context and
  audience properties; FEP-7888 conversational contexts in NodeBB;
  federating with NodeBB instances; how forum software works in the
  Fediverse; NodeBB's content pruning of remote data; NodeBB vs
  Discourse federation; or building software that interoperates with
  NodeBB forums.
user-invocable: false
---

# NodeBB — Complete Reference

## Overview

NodeBB is a modern, open-source forum software built on **Node.js**
with native WebSocket real-time updates. Founded in **2014** by Julian
Lam, Andrew Rodrigues, and Barış Soner Üşaklı in Toronto, Canada.
Licensed GPL-3.0.

Starting with **v4.0.0** (released January 20, 2025), NodeBB includes
**ActivityPub federation as a core feature** — not a plugin. This makes
NodeBB the first major traditional forum software to ship ActivityPub
in its core. The implementation was funded by the **NLNet Foundation**
(NGI Zero Core fund, approved August 2023).

NodeBB organizes content as **forum topics** (not ephemeral posts).
Content is presented chronologically with active topics "bumped" to the
top when receiving replies. This is fundamentally different from
microblogging platforms — NodeBB brings the structured discussion forum
paradigm into the Fediverse.

---

## 1. Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Node.js |
| Real-time | WebSockets (Socket.IO) |
| Database | MongoDB (default), Redis, or PostgreSQL |
| Frontend | Server-rendered templates + client-side JS |
| License | GPL-3.0 |

### Database Architecture

NodeBB provides a unified database abstraction layer (hashes, sets,
sorted sets, lists) that works identically across all three backends.
Data is stored as key-value objects (e.g., `user:<uid>`).

**Multi-database support:** Sessions can be separated into a different
database instance (e.g., Redis for sessions, MongoDB for data). Redis
pub-sub is used for inter-process communication regardless of primary
database, enabling horizontal scaling across multiple Node.js processes.

### Plugin System

Hooks-based architecture with four hook types:

| Type | Behavior |
|------|----------|
| Filters | Take input, modify, return changed value |
| Actions | Execute side effects, return nothing |
| Static | Like actions but NodeBB waits for completion |
| Response | Return HTTP responses |

Plugins can mount API routes at `/api/v3/plugins`. Widget system
supports template-and-location based widget areas. Large npm-based
plugin ecosystem (SSO, media embedding, advertising, emoji, push
notifications, rich-text, galleries, etc.).

---

## 2. ActivityPub Implementation

### Why Core, Not Plugin

ActivityPub required extensive architectural changes that couldn't be
accomplished via a plugin. It was built directly into the NodeBB core.

### Configuration

- **Global toggle:** `ACP > Settings > Federation (ActivityPub)`
- **New v4 installs:** federation enabled by default, all categories
  federate
- **Upgrades from v3:** federation disabled by default (opt-in)
- **Per-category control:** the "fediverse" pseudo-user is granted
  viewing/posting privileges on a per-category basis
- **Domain filtering:** allow-list or deny-list modes

### Development Timeline

| Date | Milestone |
|------|-----------|
| Mid-2023 | Julian conceives inter-NodeBB communication idea |
| Aug 2023 | NLNet Foundation funding approved |
| Jun 2024 | v4.0.0-alpha |
| Sep 2024 | v4.0.0-beta.1 |
| Nov 2024 | RC1 |
| Jan 20, 2025 | **v4.0.0 stable** |
| 2025–2026 | Continued releases through v4.9.0+ |

---

## 3. Actor Types

| Actor | Type | Path | Purpose |
|-------|------|------|---------|
| User | `Person` | `/u/username` | Individual user accounts |
| Category | `Group` | `/category/<cid>` | Forum categories, Group Federation |
| Instance | `Application` | (instance-level) | Server-level actor |

### Category as Group Actor (FEP-1b12)

Each category identifies itself as a `Group` actor. Categories:

- Maintain follow relationships with other actors and remote users
- Can follow other `Group` actors from different forums
- Federate content via the **Announce relay pattern**
- Have a unique handle — a "slugified" version of the category name
  (e.g., "Category About Cats" → `category-about-cats`)

When a user posts content (new topic or reply), the category wraps it
in an `Announce` activity and distributes to all followers:

```
User creates post → Create{Note} sent to Category
Category wraps → Announce{Create{Note}} sent to all followers
Remote instances receive → display post in corresponding category
```

This is the same pattern used by Lemmy communities and Kbin/Mbin
magazines. Remote users can follow a NodeBB category the same way they
follow a Lemmy community.

### The Uncategorized Pseudo-Category

Serves as a catch-all for manually discovered remote content (via URL
paste into search). Content lands here automatically before admins move
it to appropriate local categories. The Uncategorized category does
**NOT** use the Announce pattern and has automated pruning.

---

## 4. Content Model and Conversational Context

### Two-Level Hierarchy

NodeBB maps forum structure to ActivityPub using a two-level hierarchy:

```
Category (audience) → Topic (context) → Post
     Group actor        OrderedCollection    Note/Article
```

Every post carries both properties:
- **`audience`** → points to the category (`Group` actor)
- **`context`** → points to the topic (resolvable URL returning an
  `OrderedCollection` per FEP-7888)

### Object Types

| NodeBB Concept | AP Object | Notes |
|---------------|-----------|-------|
| Topic | `context` (OrderedCollection) | Resolvable collection of posts |
| Post / Reply | `Note` or `Article` | Within a context, with `inReplyTo` for threading |
| Category | `Group` actor | Uses `audience` property |

NodeBB builds topics from incoming ActivityPub activities (`Create`,
`Question`, `Listen`) and objects (`Note`, `Article`).

### Context Resolution (FEP-7888)

When NodeBB encounters an object with a `context` property:

1. **Primary: Resolvable context** — resolves the URL to retrieve a
   `Collection`, parses all objects, organizes them into a single topic.
   Supports synchronization headers for freshness verification.

2. **Fallback: Reply chain traversal** — traverses `inReplyTo` chain
   upward to the root node, organizes chain objects into a topic.

Reply chain traversal has limitations:
- If any object in the chain becomes unresolvable, the chain breaks
- Only follows the direct reply path, missing sibling branches

### Outboxes

User and category outboxes (v4.10.0+) return paginated
`OrderedCollection` containing activities (`Create`, `Like`, etc.)
with `first`, `last`, `prev`, `next` navigation.

---

## 5. FEP Support

NodeBB evaluates FEPs using four positions (mirroring Mozilla's
Specification Positions): positive, neutral, defer, negative.

### Implemented

| FEP | Title |
|-----|-------|
| FEP-0151 | NodeInfo in Fediverse Software |
| FEP-11dd | Context Ownership and Inheritance |
| FEP-1b12 | Group Federation |
| FEP-4f05 | Soft Deletion |
| FEP-7888 | Demystifying the context property |
| FEP-9098 | Custom emojis |
| FEP-ae0c | Fediverse Relay Protocols (Mastodon and LitePub) |
| FEP-b2b8 | Long-form Text |
| FEP-f15d | Context Relocation and Removal |
| FEP-f228 | Backfilling Conversations |
| FEP-fb2a | Actor metadata |
| FEP-fe34 | Origin-based security model |

### Partially Implemented

FEP-7458 (Using the replies collection)

### Positive (Not Yet Implemented)

FEP-044f, FEP-8b32, FEP-9967, FEP-c0e0

NodeBB is an active participant in the **SWICG Forum and Threaded
Discussions Task Force**, promoting threaded discussion formats in the
Fediverse.

---

## 6. Content Discovery and Pruning

### Discovery Methods

1. **Follow users/categories** — search for handles
   (e.g., `user@domain.social`)
2. **URL paste** — paste a remote content URL into NodeBB's search bar
   to pull it in; content lands in Uncategorized
3. **Cross-posting (v4.8.0+)** — topics from remote categories can be
   added to local categories

### No Relay Support

NodeBB explicitly does NOT support relays. This is intentional — relays
"do not guarantee the quality of incoming content." The design
prioritizes relationship-based content distribution over algorithmic or
broadcast discovery.

### Content Pruning

NodeBB automatically manages remote content to prevent database bloat:

| Setting | Default | Condition for removal |
|---------|---------|----------------------|
| Remote content retention | 30 days | Topics with no local engagement (votes or replies) |
| Remote user retention | 7 days | Accounts with no posts and no follow relationships |

Both settings are configurable via the admin panel.

---

## 7. NodeBB vs Discourse (Federation)

| Aspect | NodeBB | Discourse |
|--------|--------|-----------|
| Language | Node.js | Ruby on Rails |
| AP integration | **Core feature** (v4+) | Plugin (discourse-activity-pub) |
| AP since | January 2025 | 2023 (plugin) |
| Actor model | Group (categories) | Group (categories) |
| Context support | FEP-7888 (resolvable) | Separate approach |
| FEPs implemented | 12 | Fewer |
| Real-time | Native WebSockets | Long polling / MessageBus |
| Database | MongoDB/Redis/PostgreSQL | PostgreSQL only |
| License | GPL-3.0 | GPL-2.0 |

Both bring threaded forum discussions to the Fediverse, using categories
as Group actors. NodeBB's core integration means tighter coupling with
the ActivityPub protocol and more extensive FEP adoption. Discourse's
plugin approach allows easier opt-in/opt-out but has less deep
integration.

---

## 8. Interoperability Notes for Implementers

1. **Categories are `Group` actors** — follow a NodeBB category by
   sending `Follow` to the Group actor at `/category/<cid>`. The
   category relays all content via `Announce`, identical to Lemmy
   communities. Category handles are slugified names
   (e.g., `general-discussion`).

2. **Posts carry both `context` and `audience`** — `context` points to
   the topic (resolvable `OrderedCollection`), `audience` points to the
   category (`Group` actor). This two-level hierarchy is NodeBB-specific
   and differs from Lemmy's single-level approach.

3. **Topics are resolvable collections** — if your software encounters
   a NodeBB `context` URL, resolve it to get the full topic as an
   `OrderedCollection`. This is the recommended way to backfill
   conversations (per FEP-7888 and FEP-f228).

4. **`Note` and `Article` objects accepted** — NodeBB processes both
   `Note` and `Article` types when building topics. Send whichever is
   appropriate for your content.

5. **No relay federation** — NodeBB will not participate in relay
   subscriptions. Content exchange requires explicit follow
   relationships.

6. **Remote content is pruned** — NodeBB deletes remote content after
   30 days (configurable) if it has no local engagement. If your
   software references old NodeBB content, it may have been pruned from
   remote instances that imported it. Similarly, content your software
   sends to NodeBB will be pruned if no local user engages with it.

7. **Cross-posting** — since v4.8.0, a single topic can appear in
   multiple local categories. This means the same remote content may
   be accessible via different category Group actors on the same
   instance.

8. **Soft deletion (FEP-4f05)** — NodeBB supports soft deletion. When
   content is deleted, a `Delete` activity with a `Tombstone` object
   is sent rather than simply disappearing.

9. **Custom emojis (FEP-9098)** — NodeBB supports federated custom
   emoji. Remote emoji in posts and chats are rendered (since v4.7.0).

10. **Content in Uncategorized has no `audience`** — manually
    discovered content landing in the Uncategorized pseudo-category may
    not have a proper `audience` property pointing to a Group actor.
    This content is not Announced to followers.
