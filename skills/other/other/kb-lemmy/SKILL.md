---
name: kb-lemmy
description: >
  Background knowledge about Lemmy, the federated link aggregation and
  discussion platform (Reddit alternative). Covers Lemmy's fundamental
  architectural decision of Communities as Group actors that automatically
  Announce all content to followers, the ActivityPub object type mappings
  (Post as Page with mandatory title, Comment as Note with inReplyTo tree,
  Community as Group, User as Person, Instance as Application, Private
  Message as ChatMessage), voting via Like/Dislike activities (unique
  first-class downvotes unlike most Fediverse platforms), ranking
  algorithms (Active, Hot, Scaled, Top), the full activity reference
  (Create/Update/Delete for posts and comments, Follow/Accept for
  community subscription, Remove/Block/Lock for moderation, Flag for
  reporting, Announce for community relay), federation modes (allowlist,
  blocklist, open), custom namespace extensions (stickied, distinguished,
  commentsEnabled, postingRestrictedToMods), the Lemmy JSON-LD context
  (join-lemmy.org/context.json), the REST API v3 with JWT auth and
  pictrs image service, known interoperability issues (name vs
  preferredUsername reversal, JSON-LD context errors, Mastodon reply
  propagation failures, vote federation inconsistencies, strict parsing),
  the tech stack (Rust/Actix-web/Diesel/PostgreSQL backend,
  TypeScript/Inferno.js frontend, activitypub-federation-rust library),
  and the Threadiverse ecosystem (Kbin/Mbin, PieFed, Sublinks). Load
  when the user asks about Lemmy federation; implementing a Lemmy-
  compatible ActivityPub server; how Lemmy communities work as Group
  actors; how Lemmy voting federates; Lemmy's Page object type; how
  posts and comments federate in Lemmy; Lemmy's moderation activities;
  interoperating with Lemmy instances; the Lemmy API; or the
  Threadiverse.
user-invocable: false
---

# Lemmy — Complete Reference

## Overview

Lemmy is a self-hosted, federated social link aggregation and discussion
forum — the Fediverse equivalent of Reddit. Created by Dessalines in
February 2019, with Nutomic as co-creator and primary federation
implementer. Built in Rust (Actix-web, Diesel ORM, PostgreSQL) with a
TypeScript/Inferno.js frontend. Licensed AGPL-3.0.

Lemmy federates via ActivityPub. Its fundamental design choice is
representing **communities as Group actors** that automatically relay all
content via `Announce` activities, ensuring cross-instance consistency.
It is the largest platform in the "Threadiverse" — the threaded discussion
subset of the Fediverse.

---

## 1. Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend language | Rust |
| Web framework | Actix-web (actor-model based) |
| ORM | Diesel (type-safe) |
| Database | PostgreSQL (R2D2 connection pooling) |
| Frontend language | TypeScript + CSS |
| Frontend framework | Inferno.js (React-compatible) |
| API client | lemmy-js-client |
| Image service | pictrs |
| Deployment | Docker, Ansible, ARM64/RPi supported |
| License | AGPL-3.0 |
| Federation library | activitypub-federation-rust (standalone reusable crate) |

---

## 2. ActivityPub Object Type Mapping

| Lemmy Concept | ActivityPub Type | Notes |
|---------------|------------------|-------|
| Community | `Group` | Automated relay actor; Announces all content to followers |
| User | `Person` | Creates content, moderates, sends PMs |
| Instance | `Application` | Instance-level actor at root path |
| Post | `Page` | Mandatory title (`name`), optional URL and body |
| Comment | `Note` | Tree structure via `inReplyTo` |
| Private Message | `ChatMessage` | Direct user-to-user, no threading |

### Why Page for Posts?

Lemmy posts have a mandatory title (`name`), distinguishing them from
`Note` (typically untitled) and `Article` (long-form). The `Page` type
aligns with the concept of a web page with a URL, title, and optional
body.

---

## 3. Communities as Group Actors

This is the fundamental architectural decision. Communities are `Group`
actors with their own inboxes. Every post, comment, vote, and moderation
action is received by the community and then **Announced** (wrapped and
forwarded) to all followers across all instances.

### Community Object

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    "https://join-lemmy.org/context.json"
  ],
  "id": "https://enterprise.lemmy.ml/c/main",
  "type": "Group",
  "preferredUsername": "main",
  "name": "The Main Community",
  "summary": "<p>Welcome to the main community!</p>",
  "inbox": "https://enterprise.lemmy.ml/c/main/inbox",
  "outbox": "https://enterprise.lemmy.ml/c/main/outbox",
  "followers": "https://enterprise.lemmy.ml/c/main/followers",
  "featured": "https://enterprise.lemmy.ml/c/main/featured",
  "attributedTo": ["https://enterprise.lemmy.ml/u/picard"],
  "publicKey": {
    "id": "https://enterprise.lemmy.ml/c/main#main-key",
    "owner": "https://enterprise.lemmy.ml/c/main",
    "publicKeyPem": "..."
  }
}
```

### Key Fields

| Field | Description |
|-------|-------------|
| `preferredUsername` | Machine-readable community name |
| `name` | Human-readable display name |
| `summary` | Description / rules (HTML) |
| `icon` / `image` | Avatar / banner |
| `outbox` | Limited to 20 latest posts |
| `followers` | Count only (no individual references — privacy) |
| `attributedTo` | Creators and moderators |
| `featured` | Pinned posts collection |
| `postingRestrictedToMods` | Whether only mods can post |

### The Announce Relay Pattern

```
User on Instance A              Community on Instance B         Instance C subscriber
       |                               |                              |
       |--- Create{Page} -----------> |                              |
       |                               |--- Announce{Create{Page}} ->|
       |                               |                              |
```

All content activities (Create, Update, Delete, Like, Dislike, Remove,
Lock) flow through the community Group actor, which wraps each in an
`Announce` and broadcasts to all followers. This is how cross-instance
consistency is maintained.

---

## 4. Post (Page) Object

```json
{
  "type": "Page",
  "id": "https://enterprise.lemmy.ml/post/123",
  "attributedTo": "https://enterprise.lemmy.ml/u/riker",
  "to": [
    "https://www.w3.org/ns/activitystreams#Public",
    "https://ds9.lemmy.ml/c/main"
  ],
  "audience": "https://ds9.lemmy.ml/c/main",
  "name": "An interesting link",
  "content": "<p>Check this out!</p>",
  "source": {
    "content": "Check this out!",
    "mediaType": "text/markdown"
  },
  "attachment": [],
  "image": {},
  "commentsEnabled": true,
  "sensitive": false,
  "stickied": false,
  "published": "2024-01-15T12:00:00.000Z"
}
```

| Field | Description |
|-------|-------------|
| `name` | Title (mandatory — distinguishes Post from Comment) |
| `content` | Body text (HTML-rendered) |
| `source` | Original markdown with `mediaType: "text/markdown"` |
| `audience` | Target community (for routing) |
| `attachment` | Links/images array |
| `image` | Thumbnail |
| `commentsEnabled` | Post lock status (custom extension) |
| `sensitive` | NSFW flag |
| `stickied` | Pinned status (custom extension) |
| `language` | Language metadata (`identifier` + `name`) |

---

## 5. Comment (Note) Object

```json
{
  "type": "Note",
  "id": "https://enterprise.lemmy.ml/comment/95",
  "attributedTo": "https://enterprise.lemmy.ml/u/picard",
  "to": "https://enterprise.lemmy.ml/c/main",
  "content": "I agree with this take.",
  "source": {
    "content": "I agree with this take.",
    "mediaType": "text/markdown"
  },
  "inReplyTo": [
    "https://enterprise.lemmy.ml/post/38",
    "https://voyager.lemmy.ml/comment/73"
  ],
  "tag": [
    {
      "type": "Mention",
      "href": "https://voyager.lemmy.ml/u/janeway",
      "name": "@janeway@voyager.lemmy.ml"
    }
  ],
  "distinguished": false,
  "published": "2024-01-15T13:00:00.000Z"
}
```

| Field | Description |
|-------|-------------|
| `inReplyTo` | Parent post and/or parent comment (builds tree) |
| `tag` | `Mention` objects for user references |
| `distinguished` | Mod-highlighted comment (custom extension) |

---

## 6. Voting — Like and Dislike

Lemmy uses both `Like` (upvote) and `Dislike` (downvote) as first-class
ActivityPub activities. This is **unique** among major Fediverse platforms
— most only support `Like`.

### Upvote

```json
{
  "type": "Like",
  "actor": "https://enterprise.lemmy.ml/u/picard",
  "object": "https://enterprise.lemmy.ml/post/123",
  "audience": "https://ds9.lemmy.ml/c/main"
}
```

### Downvote

```json
{
  "type": "Dislike",
  "actor": "https://enterprise.lemmy.ml/u/worf",
  "object": "https://enterprise.lemmy.ml/post/123",
  "audience": "https://ds9.lemmy.ml/c/main"
}
```

### Undo Vote

```json
{
  "type": "Undo",
  "actor": "https://enterprise.lemmy.ml/u/picard",
  "object": {
    "type": "Like",
    "actor": "https://enterprise.lemmy.ml/u/picard",
    "object": "https://enterprise.lemmy.ml/post/123"
  }
}
```

All votes include `audience` for community routing and are wrapped in
`Announce` by the community actor.

**Privacy note**: Every instance that subscribes to the community receives
all vote activities — instance admins can see who voted on what.

### Ranking Algorithms

| Algorithm | Description |
|-----------|-------------|
| Active (default) | Score + latest comment time with decay |
| Hot | Score + post publication time with decay |
| Scaled | Hot with boost for less active communities |
| New / Old | Chronological |
| Most Comments | Comment count |
| New Comments | Forum-style bump on new reply |
| Top (Day/Week/Month/Year/All) | Score within time window |

Score = upvotes minus downvotes.

---

## 7. Full Activity Reference

### User → Community

| Activity | Purpose |
|----------|---------|
| `Follow` | Subscribe to community |
| `Undo{Follow}` | Unsubscribe |
| `Create{Page}` | New post |
| `Create{Note}` | New comment |
| `Update{Page}` | Edit post |
| `Update{Note}` | Edit comment |
| `Like` | Upvote |
| `Dislike` | Downvote |
| `Undo{Like}` / `Undo{Dislike}` | Remove vote |
| `Delete` | Delete own content |
| `Undo{Delete}` | Restore deleted content |
| `Flag` | Report content (with `summary` reason) |

### Community → Followers

| Activity | Purpose |
|----------|---------|
| `Accept{Follow}` | Automatic response to Follow |
| `Announce{*}` | Rebroadcast any received activity to all followers |

### Moderation

| Activity | Purpose |
|----------|---------|
| `Remove` | Remove content (with `summary` reason) |
| `Block` | Ban user (with `target` scope, optional `removeData`, `expires`, `summary`) |
| `Lock` | Prevent new comments on post |
| `Add` to `/moderators` | Add moderator |
| `Remove` from `/moderators` | Remove moderator |
| `Add` to `/featured` | Pin post |
| `Remove` from `/featured` | Unpin post |

### User → User

| Activity | Purpose |
|----------|---------|
| `Create{ChatMessage}` | Send private message |
| `Update{ChatMessage}` | Edit private message |
| `Delete{ChatMessage}` | Delete private message |

### Instance-Level

- Instance actor (type `Application`) at root path
- Admins can remove any content instance-wide
- `Delete` on user actor with `removeData: true` for account deletion

All activities are signed with RSA keys (key ID: `{actor-url}#main-key`).

---

## 8. JSON-LD Context and Custom Extensions

### Required Context

```json
[
  "https://join-lemmy.org/context.json",
  "https://www.w3.org/ns/activitystreams"
]
```

### Namespace Prefixes

```json
{
  "lemmy": "https://join-lemmy.org/ns#",
  "litepub": "http://litepub.social/ns#",
  "pt": "https://joinpeertube.org/ns#",
  "sc": "http://schema.org/"
}
```

### Custom Properties

| Property | Namespace | Used on | Description |
|----------|-----------|---------|-------------|
| `stickied` | lemmy | Page | Pinned post |
| `distinguished` | lemmy | Note | Mod-highlighted comment |
| `commentsEnabled` | lemmy | Page | Post lock status |
| `postingRestrictedToMods` | lemmy | Group | Restricted posting |
| `moderators` | lemmy | Group | Moderator collection |
| `language` | lemmy | Page, Note | Language metadata |
| `sensitive` | as | Page | NSFW flag |
| `matrixUserId` | lemmy | Person | Matrix chat ID |

**Important**: Lemmy parses ActivityPub objects as plain JSON, not as
JSON-LD. The `@context` is included for other software's benefit but
Lemmy does not perform JSON-LD expansion or compaction.

---

## 9. Federation Modes and Fetching

### Federation Modes

| Mode | Description |
|------|-------------|
| Allowlist | Only connect to specified instances |
| Blocklist | Block specific instances, open to all others |
| Open (default) | Connect to any instance |

### Cascading Fetch Behavior

- **Community fetch**: Also fetches most recent posts (not comments/votes)
- **Post fetch**: Also fetches community and author
- **Comment fetch**: Also fetches all parent comments, the post, authors,
  and the community

This ensures referential integrity across the federated network.

---

## 10. REST API

| Aspect | Details |
|--------|---------|
| Version | v3 (`/api/v3/...`) |
| Auth | JWT (cookies or `Authorization` header since 0.19.0) |
| Image service | pictrs — upload, resize, format conversion |
| Feeds | RSS/Atom at `/feeds/` paths |
| Rate limiting | IP-based (Docker: requires `X-Forwarded-For` header) |
| Client library | lemmy-js-client (official TypeScript) |
| OpenAPI spec | Unofficial: `mv-gh.github.io/lemmy_openapi_spec/` |

---

## 11. Interoperability Issues

### name vs preferredUsername (Historical)

Lemmy initially reversed these: `name` for usernames, `preferredUsername`
for display names. This is the opposite of the ActivityPub spec and
Mastodon. Nutomic acknowledged it as "completely counterintuitive."

### JSON-LD Context Errors

Lemmy's `@context` had incorrect declarations:
- `"stickied": "as:stickied"` — falsely implied `stickied` is in the
  ActivityStreams namespace
- `"pt"` prefix expanded to Lemmy's domain instead of PeerTube's

Nutomic admitted: "the truth is that I don't really understand how
[@context] works."

### Mastodon Reply Propagation

Replies from Mastodon can fail to reach all Lemmy instances because
Mastodon doesn't include the community inbox in its recipient lists. The
community Group actor must be in the recipient list to Announce the reply.

### Mastodon Vote Federation

Mastodon's `Like` targets personal inboxes, not shared inboxes. Lemmy
processes the vote locally but does not Announce it, causing vote count
inconsistencies across instances.

### Strict Parsing

Lemmy is "really inflexible when it comes to incoming activities." Arrays
vs single values, or object IDs vs full inlined objects, can cause
parsing errors. The Lemmy protocol is described as "a strict subset of
the ActivityPub Protocol."

---

## 12. The Threadiverse Ecosystem

"Threadiverse" refers to Reddit-style threaded discussion platforms in
the Fediverse. All federate with each other via ActivityPub.

| Platform | Language | Terminology | Notes |
|----------|----------|-------------|-------|
| Lemmy | Rust | Communities | Largest, most mature |
| Mbin | PHP (fork of Kbin) | Magazines | Also supports microblogs (Mastodon-style) |
| PieFed | Python | Topics | Rapid development, approaching feature-parity |
| Sublinks | Java | — | Drop-in Lemmy replacement (alpha) |

Users on any Threadiverse platform can see and interact with content
from any other, including subscribing to Lemmy communities from Mbin
or PieFed.

---

## 13. Known Quirks for Implementers

1. **Posts use `Page`, not `Note`** — if your server sends `Note` objects
   to a Lemmy community, they will be treated as comments, not posts.
   Posts require `Page` type with a `name` (title).

2. **Community must be in recipients** — activities targeting a Lemmy
   community must include the community in `to` or `cc`. Sending only to
   the post author's inbox will not distribute the activity.

3. **`audience` field** — Lemmy uses the `audience` property to route
   activities to the correct community. Include it for reliable delivery.

4. **`Dislike` is real** — unlike most Fediverse platforms, Lemmy uses
   `Dislike` as a distinct activity type for downvotes, not `Undo{Like}`.

5. **`source` with markdown** — Lemmy preserves original markdown in the
   `source` field with `mediaType: "text/markdown"`. The `content` field
   contains the HTML-rendered version.

6. **Outbox is limited** — community outbox only contains the 20 most
   recent posts. Comments and votes are not included.

7. **Followers collection is opaque** — returns only a total count, not
   individual follower references (for privacy).

8. **No JSON-LD processing** — Lemmy parses JSON directly. Do not rely on
   JSON-LD compaction/expansion when interoperating with Lemmy.

9. **`ChatMessage` for PMs** — Lemmy uses the non-standard `ChatMessage`
   type for private messages rather than `Note` with direct addressing.
