---
name: kb-kbin
description: >
  Background knowledge about Kbin and its active community fork Mbin,
  the decentralized content aggregator and microblogging platform for
  the Fediverse (Reddit + Mastodon hybrid). Covers the dual content
  model (threads/link aggregation via Page objects + microblogging via
  Note objects in a single platform), magazines as Group actors with
  Announce relay (same pattern as Lemmy communities), the three actor
  types (Application instance actor at /i/actor, Person user at
  /u/username, Group magazine at /m/name), supported activities (Follow,
  Like, Announce, Create, Update, Delete, Block, Flag, Lock, Add,
  Remove), the critical detail that downvotes do NOT federate, content
  object mapping (threads as Page, microblogs as Note, comments as Note
  with inReplyTo, private messages as ChatMessage), the tech stack
  (PHP 8.2+/Symfony/PostgreSQL/RabbitMQ/Redis, AGPL-3.0), the REST API
  with OAuth2 and Swagger docs at /api/docs, the Mbin fork history
  (Kbin discontinued after creator Ernest Wisniewski's absences, Mbin
  forked October 2023 with C4 governance, improved federation/performance/
  scaling), Kbin vs Lemmy comparison (Kbin has microblogging + threads
  while Lemmy is threads only, Kbin has stronger Mastodon integration,
  Lemmy federates downvotes while Kbin does not), the Threadiverse
  ecosystem context (Lemmy, Mbin, PieFed, Sublinks), voting/reputation
  system (reputation is cosmetic only), and federation interoperability
  details. Load when the user asks about Kbin or Mbin; implementing a
  Kbin/Mbin-compatible ActivityPub server; how Kbin magazines federate
  as Group actors; how Kbin combines link aggregation and microblogging;
  why Kbin downvotes don't federate; the Kbin to Mbin transition; how
  Kbin/Mbin differs from Lemmy; interoperating with Kbin/Mbin instances;
  the Threadiverse; or building software that federates with Kbin/Mbin.
user-invocable: false
---

# Kbin / Mbin — Complete Reference

## Overview

Kbin (stylized /kbin) was a decentralized content aggregator and
microblogging platform for the Fediverse — a Reddit + Mastodon hybrid.
Created by **Ernest Wiśniewski** (Polish developer) with development
becoming serious in early 2023, the flagship instance kbin.social
launched in **April 2023**. The project received **NLnet funding**
(NGI0 Entrust Fund, December 2022).

Kbin is now **discontinued**. Its active community fork **Mbin**
(founded October 2023 by Melroy van den Berg) continues development
with significant improvements to federation, performance, and
governance. When this document says "Kbin/Mbin," the information
applies to both; Mbin-specific features are noted.

Kbin's key differentiator from Lemmy: it combines **two content models
in one platform** — Reddit-style link aggregation (threads organized
into magazines) and Mastodon-style microblogging (short-form posts).
This dual nature enables stronger integration with microblogging
platforms like Mastodon.

Licensed AGPL-3.0. Built with PHP/Symfony/PostgreSQL.

---

## 1. Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | PHP 8.2+ |
| Framework | Symfony |
| Database | PostgreSQL |
| Message queue | RabbitMQ |
| Cache | Redis / KeyDB / Valkey |
| Real-time | Mercure (optional) |
| Frontend | Twig templates, SCSS, JavaScript |
| Image processing | GD or ImageMagick |
| Web server | Nginx, Apache, or Caddy |
| Deployment | Docker / Docker Compose |
| License | AGPL-3.0 |

### Language Breakdown

- PHP: 86.3%
- Twig: 9.4%
- SCSS: 2.5%
- JavaScript: 1.6%

### Development Tools

- PHPUnit (testing), PHPStan (static analysis), Psalm (security
  scanning), Composer (dependencies), API Platform (API generation)

---

## 2. Content Model

### Magazines

The primary organizational unit — equivalent to subreddits (Reddit),
communities (Lemmy), or topics (PieFed). Any registered user can create
a magazine and automatically becomes its owner with administrative tools
including moderator appointment.

### Content Types

| Type | Description | AP Object |
|------|-------------|-----------|
| Thread (link) | External links and articles with titles | `Page` |
| Thread (text) | Self-text discussion posts with titles | `Page` |
| Microblog | Short-form posts (like Mastodon) | `Note` |
| Comment | Replies to threads or microblogs | `Note` (with `inReplyTo`) |
| Private message | Direct messages between users | `ChatMessage` (custom) |

The **dual content model** is what distinguishes Kbin/Mbin from Lemmy.
Threads work like Reddit posts (link or self-text with a title,
displayed in a list). Microblogs work like Mastodon posts (short-form,
displayed in a stream). Both coexist within each magazine.

### Voting

- **Upvote** — positive engagement, federated as `Like` activity
- **Downvote ("Reduce")** — negative engagement, **local only — does
  NOT federate**
- **Boost** — reshare/reblog, federated as `Announce` activity

The non-federation of downvotes is a critical interoperability detail.
Lemmy federates downvotes via `Dislike`; Kbin/Mbin does not send them.
Downvotes from Kbin/Mbin users are only visible on the local instance.

### Reputation

Users accumulate reputation points from boosts and favourites on their
content. Reputation is **cosmetic only** — visible on profile pages but
has no functional effect (does not gate features or permissions).

### Content Organization

- Follow magazines, users, or entire domains
- Block users, magazines, or domains
- Content categorized by tags and labels
- RSS feeds for threads, microblogs, or combined

---

## 3. ActivityPub Implementation

### Actor Types

| Actor | Type | Path | Purpose |
|-------|------|------|---------|
| Instance | `Application` | `/i/actor` | Server-level actor, signs requests, inbox/outbox |
| User | `Person` | `/u/username` | Individual accounts with followers/following |
| Magazine | `Group` | `/m/name` | Community container, announces user activities |

### JSON-LD Context

The `@context` resolves to ActivityStreams, W3C security vocabulary,
and custom namespaces including ostatus, schema.org, Mastodon extensions
(`toot:`), PeerTube extensions, and Lemmy extensions.

### Magazine (Group) Federation

Magazines use the same **Group actor Announce relay** pattern as Lemmy
communities. When a user creates a thread in a magazine, the magazine's
Group actor wraps the activity in an `Announce` and distributes it to
all followers:

```
User creates thread → Create{Page} sent to Magazine
Magazine wraps → Announce{Create{Page}} sent to all followers
Remote instances receive Announce → display thread in magazine
```

This means subscribing to a magazine is a `Follow` sent to the Group
actor. The Group actor then relays all content via `Announce`.

### Activities Reference

| Activity | Purpose |
|----------|---------|
| `Follow` | Subscribe to user or magazine |
| `Accept` / `Reject` | Follow request responses |
| `Create` | Create threads, microblogs, comments |
| `Update` | Edit content |
| `Delete` | Remove content |
| `Like` | Upvote (no `Dislike` — downvotes are local only) |
| `Announce` | Boost/reshare; also magazine relay wrapping |
| `Undo` | Reverse Like, Follow, or Announce |
| `Block` | Ban user (optional expiration timestamp, magazine-level or instance-level) |
| `Flag` | Report content (sent to magazine moderators' instances only) |
| `Add` / `Remove` | Moderator assignment, thread pinning |
| `Lock` | Lock threads/microblogs to prevent responses (Mbin) |

### Content Object Wire Format

**Thread (Page):**

```json
{
  "type": "Page",
  "id": "https://instance.example/m/magazine/t/12345",
  "attributedTo": "https://instance.example/u/alice",
  "to": ["https://www.w3.org/ns/activitystreams#Public"],
  "cc": ["https://instance.example/m/magazine/followers"],
  "name": "Thread title",
  "content": "<p>HTML body</p>",
  "mediaType": "text/html",
  "source": {
    "content": "Markdown body",
    "mediaType": "text/markdown"
  },
  "inReplyTo": null,
  "sensitive": false,
  "stickied": false,
  "commentsEnabled": true
}
```

**Microblog (Note):**

```json
{
  "type": "Note",
  "id": "https://instance.example/m/magazine/p/67890",
  "attributedTo": "https://instance.example/u/alice",
  "to": ["https://www.w3.org/ns/activitystreams#Public"],
  "content": "<p>Short-form post content</p>",
  "source": {
    "content": "Short-form post content",
    "mediaType": "text/markdown"
  },
  "tag": [
    {"type": "Hashtag", "name": "#fediverse"}
  ]
}
```

**Comment (Note with inReplyTo):**

```json
{
  "type": "Note",
  "id": "https://instance.example/m/magazine/t/12345/-/comment/99",
  "attributedTo": "https://instance.example/u/bob",
  "inReplyTo": "https://instance.example/m/magazine/t/12345",
  "content": "<p>Reply text</p>",
  "source": {
    "content": "Reply text",
    "mediaType": "text/markdown"
  }
}
```

### Key Federation Details

- **Downvotes do NOT federate** — only `Like` (upvote) and `Announce`
  (boost) are sent. No `Dislike` activity.
- **Reports (`Flag`)** are sent exclusively to instances housing the
  magazine's moderators.
- **Bans (`Block`)** include optional expiration timestamps and specify
  scope (magazine-level vs instance-level).
- Content includes focal point metadata and blurhash via Mastodon
  extensions.
- Supports **all ActivityPub Actor Types** including `Service` for
  bot/robot accounts.
- Accepts `application/json` headers across all ActivityPub endpoints
  (not just `application/activity+json`).
- All content preserves markdown source alongside HTML rendering.
- Multi-language content mapping supported.

---

## 4. API

REST API with Swagger/OpenAPI documentation at `/api/docs` on each
instance.

### Authentication

OAuth2-based:

1. Register client: `POST /api/client` → returns identifier and secret
2. Request token → returns Bearer token, expiration, refresh token
3. Include `Authorization: Bearer <token>` on requests

### Scopes

| Scope | Access |
|-------|--------|
| `read` | Retrieve threads, view favorites |
| `write` | All modification operations |

---

## 5. Kbin vs Lemmy

| Aspect | Kbin/Mbin | Lemmy |
|--------|-----------|-------|
| Language | PHP (Symfony) | Rust (Actix-web) |
| Content types | Threads **+ Microblogs** | Threads only |
| Communities | "Magazines" | "Communities" |
| AP object (posts) | `Page` (threads) + `Note` (microblogs) | `Page` only |
| Mastodon integration | Strong — microblog section shows Mastodon content | Limited |
| Downvote federation | **No** (local only) | Yes (`Dislike` activity) |
| Mention federation | Better (Mbin) | Weaker |
| PeerTube integration | Direct channel following (Mbin v1.7+) | Limited |
| Third-party apps | Very limited | Many (Jerboa, Thunder, Voyager) |
| Governance | Community-driven (Mbin) | Lemmy team (2 primary devs) |
| Maturity | Newer (2023) | Older (2019) |

### Interoperability

Both use `Group` actors for communities/magazines and `Page` objects
for threads. They federate with each other: Lemmy communities appear
as magazines in Kbin/Mbin and vice versa. Comments federate as `Note`
objects with `inReplyTo`.

Key friction points:
- Lemmy sends `Dislike` for downvotes; Kbin/Mbin ignores them (or had
  historical display issues)
- Kbin/Mbin microblog `Note` posts appear as comments in Lemmy (since
  Lemmy only understands `Page` for top-level posts)
- Mention federation works better from Mbin than from Lemmy

---

## 6. History and the Mbin Fork

### Kbin Timeline

| Date | Event |
|------|-------|
| Dec 2022 | NLnet grant funding begins |
| Early 2023 | Project moves to Codeberg, development accelerates |
| Apr 2023 | kbin.social launches with a few hundred users |
| Jun 2023 | Reddit API crisis — kbin.social grows from 300 to 30,000+ users in one week |
| Jun 2023 | Emergency infrastructure: Fastly caching, Cloudflare, server upgrades |
| Late 2023 | Ernest begins pattern of weeks-to-months-long absences |
| Oct 2023 | Mbin fork created on GitHub |
| 2024 | kbin.social increasingly unstable, Ernest cites medical issues |
| Jun 2024 | Ernest promises instance handover, then goes silent again |
| Sep 2024 | kbin.social effectively ceases operation |
| Present | Kbin discontinued; Mbin is the active continuation |

### Mbin

**Founded:** October 12, 2023, by Melroy van den Berg.

**Governance:** Uses the **Collective Code Construction Contract (C4)**
— no single-maintainer bottleneck. Multiple contributors have owner
rights. Pull requests merged by any maintainer with community consensus
on Matrix.

**Key improvements over Kbin:**
1. Federation compatibility — major fixes to interoperability issues
2. Performance and scaling — database optimizations, reduced background
   request overhead
3. Security — up-to-date dependencies, security-first patching
4. Documentation — hosted at docs.joinmbin.org
5. Thread/microblog locking
6. Discoverability and indexability settings
7. PeerTube channel following (since v1.7)
8. All ActivityPub Actor Types including `Service` for bots
9. Combined thread creation form (unified link/text/photo)

**Current version:** v1.9.1 (February 2026). 35 releases, 4,477
commits, 35+ contributors.

Around 8–10 months after forking, Mbin stopped porting Kbin code
and focused on purely original development.

---

## 7. The Threadiverse Ecosystem

The "Threadiverse" is the link-aggregation / threaded-discussion
portion of the Fediverse. All platforms interoperate via ActivityPub
using `Group` actors for communities and `Page`/`Note` objects for
content.

| Software | Language | Status | Differentiator |
|----------|----------|--------|---------------|
| Lemmy | Rust | Active | Most mature (2019), most users |
| Mbin | PHP | Active | Threads + microblogs combined |
| PieFed | Python | Active | Privacy-focused voting, rapid development |
| Sublinks | Java | In dev | Lemmy-compatible alternative backend |
| Lotide | Rust | Limited | Minimal, lightweight |

---

## 8. Instances

### Kbin Instances

8 tracked, mostly inactive or migrated to Mbin. kbin.social (flagship)
is defunct.

### Mbin Instances

23 tracked, almost all with >98% recent uptime:

- **fedia.io** — one of the largest, migrated from Kbin
- **kbin.run** — created due to kbin.social instability
- **kbin.melroy.org** — run by Mbin founder

---

## 9. Interoperability Notes for Implementers

1. **Threads arrive as `Page` objects** — same as Lemmy. If your
   software handles Lemmy's `Page` posts, Kbin/Mbin threads will work
   the same way. Title is in `name`, body in `content`/`source`.

2. **Microblogs arrive as `Note` objects** — these are short-form posts
   without titles, identical in structure to Mastodon posts. They
   originate from a magazine but look like standard microblog posts.
   Lemmy displays these as comments since it only understands `Page`
   for top-level content.

3. **No `Dislike` activity** — Kbin/Mbin never sends downvotes over
   federation. If you receive a `Like` from a Kbin/Mbin instance, it's
   an upvote. You will never receive a `Dislike`. If your platform
   sends `Dislike` to a Kbin/Mbin instance, it may be ignored or cause
   display issues.

4. **Magazines are `Group` actors** — follow a magazine by sending
   `Follow` to the Group actor at `/m/name`. The magazine relays all
   content via `Announce`, identical to Lemmy communities.

5. **`ChatMessage` for DMs** — Kbin/Mbin uses a custom `ChatMessage`
   type for private messages, not standard `Note` with direct
   addressing. Other platforms may not understand this type.

6. **Accepts `application/json`** — Kbin/Mbin accepts both
   `application/activity+json` and plain `application/json` on all
   ActivityPub endpoints. No need to worry about content-type
   strictness.

7. **Report routing** — `Flag` activities are sent only to instances
   that host the magazine's moderators, not broadcast widely.

8. **Ban expiration** — `Block` activities can include expiration
   timestamps and scope (magazine-level vs instance-level). Handle
   the expiration field if present.

9. **Reputation is cosmetic** — Kbin/Mbin exposes reputation scores
   on user profiles, but these have no functional effect and should
   not be used for trust decisions.

10. **Mastodon content in magazines** — Kbin/Mbin's microblog section
    displays Mastodon posts matching magazine hashtags. This means
    Mastodon `Note` objects may appear alongside native Kbin/Mbin
    content in magazine feeds.
