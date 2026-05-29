---
name: kb-mbin
description: >
  Background knowledge about Mbin, the federated content aggregator and
  microblogging platform (active community fork of Kbin). Covers the hybrid
  dual content model (threads as Page + microblogs as Note in one platform),
  magazines as Group actors with Announce relay, the three actor types
  (Application instance actor at /i/actor, Person user at /u/username, Group
  magazine at /m/name), the full activity reference (Create, Update, Delete,
  Like, Dislike, Announce, Follow, Accept, Block, Flag, Lock, Add, Remove),
  the voting system (Like for upvotes, Dislike for downvotes with historical
  federation issues, Announce for boosts — boosts and votes are separate
  unlike Lemmy), the hybrid thread+microblog model and why it enables
  superior Mastodon integration, the tech stack (PHP 8.3+/Symfony 7.4/
  PostgreSQL/RabbitMQ/Redis, AGPL-3.0), the async message processing
  architecture (Symfony Messenger with 15 inbox + 15 outbox message types),
  the REST API with OAuth2 and Swagger docs, the Mbin fork history (forked
  from Kbin October 2023 by Melroy van den Berg after creator Ernest
  Wisniewski's prolonged absences, C4 collective governance), codebase
  structure (106 entity classes, 33 src directories), deployment model
  (Docker or bare metal, 4+ vCPU/6GB+ RAM), moderation tools (magazine-level
  and instance-level bans, CLI admin commands, federated ban propagation),
  Mbin vs Lemmy comparison (Mbin has microblogging + user-following + separate
  boost/vote, Lemmy has more apps and users), and federation interoperability
  details including the @context with ostatus/toot/pt/lemmy namespaces. Load
  when the user asks about Mbin specifically; implementing an Mbin-compatible
  ActivityPub server; how Mbin's hybrid thread+microblog model works; how
  Mbin magazines federate as Group actors; how Mbin voting and boosting work;
  Mbin's async message processing architecture; the Mbin fork from Kbin and
  C4 governance; Mbin deployment and administration; Mbin moderation and CLI
  commands; how Mbin differs from Lemmy or Kbin; interoperating with Mbin
  instances; or building software that federates with Mbin.
user-invocable: false
---

# Mbin — Complete Reference

## Overview

Mbin is a federated content aggregator and microblogging platform for the
Fediverse — a Reddit + Mastodon hybrid. It is the **active community fork
of Kbin**, created by **Melroy van den Berg** on **October 21, 2023**
(first release v1.0.0 on October 30, 2023) after Kbin's sole developer
Ernest Wisniewski became unable to maintain the project.

Mbin's key differentiator is its **hybrid dual content model**: it combines
Reddit-style link aggregation (threads organized into magazines) and
Mastodon-style microblogging (short-form posts) in a single platform. This
enables significantly better Mastodon integration than Lemmy or PieFed.

Governed under the **Collective Code Construction Contract (C4)** — no
single maintainer, consensus-based on Matrix, any maintainer can merge PRs.
35 releases, 4,477 commits, 30+ contributors as of early 2026. Licensed
AGPL-3.0. Built with PHP 8.3+/Symfony 7.4/PostgreSQL.

---

## 1. Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | PHP 8.3+ (8.4 recommended) |
| Framework | Symfony 7.4.x |
| ORM | Doctrine 2.19.6 |
| Database | PostgreSQL (14–18) |
| Message queue | RabbitMQ (with optional AMQProxy for connection pooling) |
| Cache | Redis / Valkey / KeyDB |
| Real-time | Mercure (optional, server-sent events) |
| Frontend | Twig templates (9.4%), SCSS (2.5%), JavaScript (1.6%) |
| Bundler | Webpack |
| Web server | Nginx, Apache, or Caddy |
| Image processing | GD with blurhash support |
| Object storage | Local filesystem or S3 (AWS, MinIO, Ceph) |
| Deployment | Docker (Debian Trixie base) or bare metal |
| License | AGPL-3.0 |
| Documentation | Docusaurus (docs.joinmbin.org) |

### Language Breakdown

- PHP: 86.3%
- Twig: 9.4%
- SCSS: 2.5%
- JavaScript: 1.6%

### Key Dependencies

- Symfony 7.4 (framework-bundle, security-bundle, twig-bundle, messenger)
- Doctrine ORM + Migrations
- OAuth2 providers: Facebook, GitHub, Google, Keycloak, Discord, Azure
- TOTP-based two-factor authentication
- AWS S3 SDK, blurhash, web push notifications, JWT via phpseclib
- swagger-php for API documentation
- PHPUnit + Paratest (parallel testing), PHPStan (static analysis)

---

## 2. Content Model

### Magazines

The primary organizational unit — equivalent to subreddits (Reddit),
communities (Lemmy), or topics (PieFed). Any registered user can create
a magazine and automatically becomes its owner. Magazines are represented
as **ActivityPub Group actors** at `/m/name`.

### The Hybrid Dual Content Model

This is Mbin's defining feature. Two content types coexist within each
magazine:

| Type | Description | AP Object | Entity Class |
|------|-------------|-----------|-------------|
| Thread (Entry) | Links, articles, discussion posts with titles | `Page` | `Entry` + `EntryComment` |
| Microblog (Post) | Short-form posts (like Mastodon) | `Note` | `Post` + `PostComment` |
| Comment | Replies to threads or microblogs | `Note` (with `inReplyTo`) | `EntryComment` or `PostComment` |
| Private message | Direct messages between users | `ChatMessage` | — |

**Why this matters for federation:** Lemmy and PieFed only see Mastodon
posts that users intentionally tag to appear on the Threadiverse. Mbin's
microblog section can follow Mastodon users directly, display their posts
in the microblog view, and federate mentions bidirectionally. This makes
Mbin the strongest Threadiverse bridge to the microblogging Fediverse.

### Navigation Structure

The UI reflects the hybrid model with tabs: Combined, Threads, Microblog,
People, Magazines. The combined view (v1.9.0+) shows threads and microblogs
together as the default homepage.

### Voting and Boosting

- **Upvote** — federated as `Like` activity (equivalent to Mastodon favourite)
- **Downvote** — federated as `Dislike` activity (historically had federation
  issues inherited from Kbin)
- **Boost** — federated as `Announce` activity (separate from voting)

**Critical difference from Lemmy:** In Mbin, boosting and voting are
**separate functions**. In Lemmy, upvoting a post effectively boosts it.
In Mbin, you can upvote without boosting and vice versa.

- Upvotes and boosts are **public** (visible to everyone)
- Downvotes are **NOT public** (to prevent harassment)
- Boosting elevates a post to the top of "Active" list and adds points
  for the "Hot" section

**Entity classes:** Vote, EntryVote, EntryCommentVote, PostVote,
PostCommentVote. Favourites are separate: Favourite, EntryFavourite,
EntryCommentFavourite, PostFavourite, PostCommentFavourite.

---

## 3. ActivityPub Implementation

### Actor Types

| Actor | Type | Path | Purpose |
|-------|------|------|---------|
| Instance | `Application` | `/i/actor` and `/` | Server-level actor, signs requests, inbox/outbox |
| User | `Person` | `/u/username` | Individual accounts with followers/following, discoverable/indexable flags |
| Magazine | `Group` | `/m/name` | Community container, announces user activities, moderator attribution |

### JSON-LD Context

All payloads include a `@context` resolving to `https://instance.example/contexts`
which maps multiple namespaces:

- ActivityStreams (`https://www.w3.org/ns/activitystreams`)
- W3C Security vocabulary
- ostatus
- schema.org
- toot (Mastodon extensions)
- pt (PeerTube extensions)
- lemmy (Lemmy extensions)

### Discovery Protocols

| Protocol | Endpoint | Source File |
|----------|----------|------------|
| WebFinger | `/.well-known/webfinger` | `WebFingerController.php` + `Service/ActivityPub/Webfinger/` |
| NodeInfo | `/.well-known/nodeinfo` | `NodeInfoController.php` |
| Host-Meta | `/.well-known/host-meta` | `HostMetaController.php` |

### Shared Inbox

`/f/inbox` for instance-wide activity delivery.

### HTTP Signatures

- Implementation: `src/Service/ActivityPub/HttpSignature.php`
- Validation: `src/Service/ActivityPub/SignatureValidator.php`
- Key generation: `src/Service/ActivityPub/KeysGenerator.php`
- Private key rotation via CLI: `mbin:user:private-keys:rotate`
- After rotation, other instances take up to 24 hours to update stored keys

---

## 4. ActivityPub Object Types and Wire Format

### Thread (Page)

```json
{
  "type": "Page",
  "id": "https://instance.example/m/magazine/t/12345",
  "attributedTo": "https://instance.example/u/alice",
  "to": ["https://www.w3.org/ns/activitystreams#Public"],
  "cc": ["https://instance.example/m/magazine/followers"],
  "audience": "https://instance.example/m/magazine",
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
  "commentsEnabled": true,
  "tag": [
    {"type": "Hashtag", "name": "#fediverse", "href": "https://instance.example/tag/fediverse"}
  ]
}
```

### Microblog (Note)

```json
{
  "type": "Note",
  "id": "https://instance.example/m/magazine/p/67890",
  "attributedTo": "https://instance.example/u/alice",
  "to": ["https://www.w3.org/ns/activitystreams#Public"],
  "cc": ["https://instance.example/m/magazine/followers"],
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

### Comment (Note with inReplyTo)

```json
{
  "type": "Note",
  "id": "https://instance.example/m/magazine/t/12345/-/comment/99",
  "attributedTo": "https://instance.example/u/bob",
  "inReplyTo": "https://instance.example/m/magazine/t/12345",
  "to": ["https://www.w3.org/ns/activitystreams#Public"],
  "cc": ["https://instance.example/m/magazine/followers"],
  "content": "<p>Reply text</p>",
  "source": {
    "content": "Reply text",
    "mediaType": "text/markdown"
  },
  "tag": [
    {"type": "Mention", "href": "https://instance.example/u/alice", "name": "@alice"}
  ]
}
```

### Vote (Like/Dislike)

```json
{
  "type": "Like",
  "id": "https://instance.example/u/alice/like/456",
  "actor": "https://instance.example/u/alice",
  "object": "https://other.example/m/magazine/t/12345",
  "to": ["https://other.example/m/magazine"]
}
```

Like activities use the magazine ID in the `to` field (changed in v1.9.1
from using the followers collection).

### Collection Endpoints

| Collection | Type | Description |
|------------|------|-------------|
| Outbox | `OrderedCollection` | Create activities, paginated with `first` |
| Followers | `OrderedCollection` | Users: individual refs; Magazines: counts only |
| Following | `OrderedCollection` | Users only |
| Moderators | `OrderedCollection` | Non-paginated list of moderator URIs |
| Featured | `OrderedCollection` | Non-paginated pinned threads |

---

## 5. Activity Reference

### Content Activities

| Activity | Purpose |
|----------|---------|
| `Create` | Create threads, microblogs, comments, messages |
| `Update` | Edit content or account profiles |
| `Delete` | Remove content/accounts, replaced with `Tombstone`; optional `removeData` flag |
| `Lock` | Disable comments on threads/microblogs |

### Social Activities

| Activity | Purpose |
|----------|---------|
| `Follow` | Subscribe to user or magazine |
| `Accept` / `Reject` | Follow request responses (auto-sent on Follow receipt) |
| `Undo` | Reverse Follow, Like, Dislike, or Announce |
| `Like` | Upvote |
| `Dislike` | Downvote |
| `Announce` | Boost/reshare; also magazine relay wrapping |

### Moderation Activities

| Activity | Purpose |
|----------|---------|
| `Block` | Ban user from magazine or instance (optional expiration) |
| `Flag` | Report content (distributed only to instances hosting magazine moderators) |
| `Add` / `Remove` | Moderator assignment and thread pinning to target collections |

### Magazine Announcements

Magazines `Announce` user activities to followers. The full set of
announced activities: Create, Update, Add, Remove, Announce, Delete,
Like, Dislike, Flag, Lock. Flag announcements are restricted to instances
hosting the magazine's moderators.

```
User creates thread → Create{Page} sent to Magazine
Magazine wraps      → Announce{Create{Page}} sent to all followers
Remote instances    → Receive Announce → display thread in magazine
```

---

## 6. Async Message Processing Architecture

Mbin uses **Symfony Messenger** with **RabbitMQ** (Redis fallback) for
asynchronous processing of all federation messages.

### Incoming Inbox Message Types (15)

ActivityMessage, AddMessage, AnnounceMessage, BlockMessage,
ChainActivityMessage, CreateMessage, DeleteMessage, DislikeMessage,
EntryPinMessage, FlagMessage, FollowMessage, LikeMessage, LockMessage,
RemoveMessage, UpdateMessage

### Outgoing Outbox Message Types (15)

AddMessage, AnnounceLikeMessage, AnnounceMessage, BlockMessage,
CreateMessage, DeleteMessage, DeliverMessage, EntryPinMessage,
FlagMessage, FollowMessage, GenericAnnounceMessage, LikeMessage,
LockMessage, RemoveMessage, UpdateMessage

### Worker Configuration

```
php bin/console messenger:consume scheduler_default old async \
  outbox deliver inbox resolve receive failed --time-limit=3600
```

Recommended: 6 Supervisor worker processes, running as `www-data`.

### AMQProxy

Optional AMQP connection pooling proxy (port 5673) that reduces TCP
connection overhead by reusing RabbitMQ channels.

---

## 7. Magazine (Group) Federation Details

Magazines are the core organizational unit and federate identically to
Lemmy communities: as Group actors using the Announce relay pattern.

### Magazine Features

- Any user can create a magazine and becomes its owner
- Owners appoint moderators with `Add`/`Remove` to `/moderators` collection
- **Custom CSS** per magazine (local display only, does not federate)
- **Magazine banners** compatible with Lemmy community banners (v1.9.0+)
- **Magazine tags** — moderators set hashtags that route matching microblogs
  into the magazine
- **Pinned content** via `featured` collection
- **Discoverable** flag controls search visibility
- **Indexable** flag controls robots.txt advisory

### Magazine Rules Deprecation

The magazine rules field is **deprecated** — rules cannot be properly
federated to other servers. The workaround appends rules to the magazine
description with a `### Rules` header.

### Entity Classes

Magazine, MagazineBan, MagazineBlock, MagazineLog (15+ specialized
subclasses), MagazineOwnershipRequest, MagazineSubscription,
MagazineSubscriptionRequest, Moderator, ModeratorRequest

---

## 8. REST API

REST API with Swagger/OpenAPI documentation generated via swagger-php.

### Authentication

OAuth2 with RSA key pair:
- Private key: `openssl genrsa -des3 -out ./config/oauth2/private.pem 4096`
- Environment variables: `OAUTH_PRIVATE_KEY`, `OAUTH_PUBLIC_KEY`,
  `OAUTH_ENCRYPTION_KEY`
- External SSO via Facebook, GitHub, Google, Keycloak, Discord, Azure

### API Resource Groups (12)

Bookmark, Combined, Domain, Entry, Instance, Magazine, Message,
Notification, OAuth2, Post, Search, User

### Key Endpoints

- `/api/instance/settings` — instance configuration
- `/api/instance/ban`, `/api/instance/unban` — instance-level bans
- Thread and microblog locking endpoints (v1.9.1+)
- Entry/post CRUD with image upload support

---

## 9. Moderation Tools

### Magazine-Level

- Owners appoint moderators
- Moderators can: pin/unpin threads, ban/unban users, lock/unlock content,
  delete/restore content, add/remove other moderators
- Public moderation logs with type filtering (v1.9.0+)
- Moderator assignments federate via `Add`/`Remove` activities

### Instance-Level

- Global moderators view, approve, or deny account signups
  (`MBIN_NEW_USERS_NEED_APPROVAL`, default: false)
- Federation allow list (`MBIN_USE_FEDERATION_ALLOW_LIST`, default: false)
- Instance-wide user blocking via `Block` activities
- Federated bans — both incoming and outgoing (v1.9.0+)

### CLI Admin Commands

| Command | Purpose |
|---------|---------|
| `mbin:user:create` | Create users with optional admin/moderator privileges |
| `mbin:user:admin` | Grant/revoke admin privileges |
| `mbin:user:delete` | Delete user and notify fediverse |
| `mbin:user:moderator` | Grant/revoke global moderator |
| `mbin:user:verify` | Activate/deactivate users (bypasses email verification) |
| `mbin:user:password` | Reset passwords |
| `mbin:user:private-keys:rotate` | Rotate federation authentication keys |
| `mbin:magazine:create` | Create/remove/purge magazines |
| `mbin:messages:remove_and_ban` | Search DMs, ban senders, remove messages |
| `mbin:check:duplicates-users-magazines` | Find/remove duplicate accounts |
| `mbin:ap:actor:update` | Update remote users and avatars |
| `mbin:ap:import` | Import ActivityPub resources by URL |

### Anti-Abuse

- Anubis DDoS protection integration (v1.9.0+)
- robots.txt blocks for vote, boost, report, crosspost, and search paths
- Per-user and per-magazine discoverable/indexable settings

---

## 10. Deployment

### Hardware Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| vCPU | 4 cores (≥2GHz) | 12 cores |
| RAM | 6 GB | 32 GB |
| Storage | 40 GB | — |

### Docker Deployment

- Pre-built image: `ghcr.io/mbinorg/mbin`
- Base image: Debian Trixie, Node.js v24
- Built-in Caddy web server for automatic HTTPS
- Services: PHP app, Messenger worker, PostgreSQL, RabbitMQ, Valkey, Caddy
- Volumes: caddy_config, caddy_data, media, messenger_logs, oauth,
  php_logs, postgres, rabbitmq_data, rabbitmq_logs

### Bare Metal

- OS: Debian 12+ or Ubuntu 22.04 LTS+
- PHP-FPM: pm.max_children=70, pm.start_servers=10
- PHP config: max_execution_time=60, upload_max_filesize=12M, memory_limit=512M
- OPCache: opcache.memory_consumption=512, opcache.jit=1255, preload enabled
- Node.js 22+ required for frontend asset building
- Supervisor for worker process management
- Installation root: `/var/www/mbin`

---

## 11. Codebase Structure

### Top-Level `src/` Directories (33)

```
ActivityPub/           Command/              Controller/
DTO/                   DataFixtures/         DoctrineExtensions/
Document/              Entity/ (106 classes) Enums/
Event/                 EventListener/        EventSubscriber/
Exception/             Factory/              Feed/
Form/                  Kernel.php            Markdown/
Message/               MessageHandler/       Middleware/
PageView/              Pagination/           Payloads/
Provider/              Repository/           Scheduler/
Schema/                Security/             Service/ (48 items)
Twig/                  Utils/                Validator/
```

### ActivityPub Controllers (14 files + 2 subdirectories)

ContextsController, EntryCommentController, EntryController,
HostMetaController, InstanceController, InstanceOutboxController,
MessageController, NodeInfoController, ObjectController,
PostCommentController, PostController, ReportController,
SharedInboxController, WebFingerController + Magazine/ + User/

### Service Layer Key Classes

ActivityPubManager, ApHttpClient, HttpSignature, KeysGenerator,
SignatureValidator, Note, Page, MarkdownConverter, DeliverManager,
EntryManager, PostManager, MagazineManager, UserManager, VoteManager,
FavouriteManager, BookmarkManager, ReportManager, ReputationManager,
TagManager, MentionManager, SearchManager, FeedManager, ImageManager

---

## 12. Mbin vs Lemmy

| Aspect | Mbin | Lemmy |
|--------|------|-------|
| Language | PHP 8.3+ (Symfony) | Rust (Actix-web) |
| Content types | Threads **+ Microblogs** | Threads only |
| Communities | "Magazines" (Group) | "Communities" (Group) |
| AP objects | `Page` (threads) + `Note` (microblogs) | `Page` only |
| Mastodon integration | Strong — microblog section shows Mastodon content | Limited |
| User following | Yes — can follow individual accounts | No — communities only |
| Boost vs vote | **Separate** functions | Combined (upvote = boost) |
| Downvote federation | `Dislike` (historical issues) | `Dislike` (reliable) |
| Mention federation | Strong (bidirectional with Mastodon) | Weaker |
| Third-party apps | Limited (Interstellar) | Many (Boost, Thunder, Voyager) |
| Governance | C4 collective, multiple maintainers | 2 primary developers |
| Maturity | Newer (Oct 2023) | Older (Feb 2019) |

### Interoperability

Both use `Group` actors for communities/magazines and `Page` objects for
threads. They federate with each other: Lemmy communities appear as
magazines in Mbin and vice versa.

Key friction points:
- Mbin microblog `Note` posts appear as comments in Lemmy (Lemmy only
  understands `Page` for top-level posts)
- Lemmy combines upvoting and boosting; Mbin treats them separately
- Magazine banners are compatible with Lemmy community banners (v1.9.0+)
- Mbin's `@context` includes the lemmy namespace for compatibility

---

## 13. History and Governance

### Kbin Background

Kbin was created by **Ernest Wisniewski** (Polish developer), with
development starting January 2021 and kbin.social launching April 2023.
During the Reddit API crisis (June 2023), kbin.social grew from ~300 to
30,000+ users in one week, eventually reaching 123,000+.

Ernest experienced compounding personal crises (divorce, surgery,
full-time job) and began disappearing for weeks to months. Pull requests
on Codeberg sat unmerged. kbin.social went offline permanently.

### The Fork

**Melroy van den Berg** (Dutch software engineer, DevOps architect)
announced the Mbin fork on October 21, 2023. His stated motivation:
*"I saw the project slowly dying over the past months, and I couldn't
let this happen."*

The name "Mbin" = "M" (Melroy) + "bin" (from kbin). Melroy acknowledged:
"I know, I wasn't creative."

Within one week, the community had already shipped GUI improvements,
backend fixes, security patches, and documentation. After ~8-10 months,
Mbin stopped porting Kbin code entirely — all subsequent development is
original work.

### C4 Governance

The **Collective Code Construction Contract** (from ZeroMQ/Pieter Hintjens):
- No single-maintainer bottleneck — multiple contributors hold org owner rights
- All maintainers peer-review each other's code
- PRs merged by any maintainer after consensus on Matrix
- "Bad actors" removed by public discussion and majority agreement
- Deliberately prevents the single-point-of-failure that killed Kbin

### Release Timeline

| Version | Date | Key Changes |
|---------|------|-------------|
| v1.0.0 | Oct 30, 2023 | First release |
| v1.7.0 | mid 2024 | PeerTube support, DMs, push notifications |
| v1.8.4 | Sep 7, 2024 | Security patch, dead instance handling |
| v1.9.0 | Dec 14, 2024 | Combined homepage, magazine banners, federated bans, Symfony 7 |
| v1.9.1 | Feb 9, 2025 | Thread/microblog locking, RSS improvements, faster search |

---

## 14. Instances and Ecosystem

~18 instances, ~8,172 total users, ~750 monthly active users.

| Instance | URL | Users | MAU |
|----------|-----|-------|-----|
| Fedia | fedia.io | 6,036 | 488 |
| kbin.earth | kbin.earth | 770 | 131 |
| the/brain/bin | thebrainbin.org | 245 | 34 |
| GehirnEimer | gehirneimer.de | 136 | 28 |

Fedia.io dominates with ~74% of all users (concentration risk).

### Mobile Apps

**Interstellar** is the primary mobile client (Android, iOS, Linux,
Windows) — functional but limited compared to Lemmy-specific apps. The
Threadiverse primer recommends Mbin only for desktop browsing.

A unified TypeScript client (`github.com/aeharding/threadiverse`) is in
development for Lemmy, PieFed, and Mbin.

---

## 15. Common Implementation Mistakes

1. **Sending `Note` objects to a magazine expecting thread display** —
   Mbin uses `Page` for threads (entries) and `Note` for microblogs.
   A `Note` sent to a magazine appears in the microblog section, not as
   a thread. Use `Page` with a `name` (title) for thread-style posts.

2. **Ignoring the separate boost/vote model** — Unlike Lemmy where
   upvoting boosts, Mbin treats `Like` (upvote) and `Announce` (boost)
   as independent actions. Implement both if you want full interoperability.

3. **Expecting downvotes to always federate** — Mbin sends `Dislike`
   activities but historically had federation issues inherited from Kbin.
   Downvotes are not publicly visible on Mbin. Do not assume reliable
   `Dislike` delivery from older Mbin versions.

4. **Not including the magazine in activity recipients** — Activities
   targeting a magazine must include the magazine Group actor in `to` or
   `cc`. The magazine must receive the activity to `Announce` it to
   followers.

5. **Assuming `ChatMessage` is standard** — Mbin uses a custom
   `ChatMessage` type for private messages, not `Note` with direct
   addressing. Other platforms may not understand this type.

6. **Ignoring `source` with markdown** — All content preserves original
   markdown in the `source` field alongside HTML in `content`. Prefer
   rendering from `source` if you want accurate markdown.

7. **Not handling both `Page` and `Note` from the same magazine** — A
   single magazine may produce both `Page` (threads) and `Note`
   (microblogs) objects. Consuming software must handle both types from
   the same Group actor.

8. **Expecting `Like` activities to use followers collection in `to`** —
   As of v1.9.1, Like/Dislike activities use the magazine ID in the `to`
   field instead of the followers collection.

9. **Treating magazine rules as a reliable field** — The rules field is
   deprecated and cannot federate. Rules are embedded in the magazine
   description under a `### Rules` header instead.

10. **Not accepting `application/json` content type** — Mbin accepts
    both `application/activity+json` and plain `application/json` on all
    ActivityPub endpoints, and may send requests with `application/json`.
    Strict content-type checking will break interoperability.
