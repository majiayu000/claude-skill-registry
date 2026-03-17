---
name: kb-piefed
description: >
  Background knowledge about PieFed, the federated link aggregation and
  discussion platform (Python-based Reddit/Lemmy alternative in the
  Threadiverse). Covers PieFed's tech stack (Python/Flask, PostgreSQL,
  Celery/Redis, htmx, Jinja2, AGPL-3.0), the Lemmy-compatible
  ActivityPub implementation (Community as Group, Post as Page, Comment
  as Note, Like/Dislike voting, Announce relay pattern, ChatMessage for
  DMs), the unique Feed actor type (FEP-1d80 for federated multi-
  community collections), private/anonymous voting via proxy user
  profiles, additional activity types (EmojiReact, PollVote,
  ChooseAnswer for Q&A mode, Event objects with startTime/endTime),
  the 95%-Lemmy-compatible REST API (/api/alpha/ with Swagger docs,
  enabling Voyager/Interstellar/Blorp/Summit mobile apps), custom
  JSON-LD extensions (genAI, nsfl, flair, postingWarning,
  interactionPolicy, lemmy:tagsForPosts compatibility), the
  federation architecture (Celery async processing, Redis dedup with
  90s TTL, RSA-SHA256 HTTP signatures, LD signature fallback, batched
  federation between PieFed instances, retry queue), moderation tools
  (reputation/attitude tracking, 3000+ domain blocklist, AI content
  labeling, 4chan screenshot detection, authoritarian inoculation,
  web of trust, community-level downvote controls), content types
  (link/text/image/video posts, polls, events, wikis, emoji reactions,
  quote posts, cross-post deduplication with merged comments, scheduled
  posts), community features (local-only communities, private
  communities, NSFW/NSFL/genAI flags, moderator recruitment via
  newModsWanted, post flair via tagsForPosts), and interoperability
  with Lemmy, Mastodon (mention-to-follow, poll interop, quote-boost),
  PeerTube (channel following, embedded player), and Mbin/Kbin
  (accepts both attributedTo and moderators for mod lists). Load when
  the user asks about PieFed federation; implementing a PieFed-
  compatible ActivityPub server; how PieFed communities work; PieFed's
  voting system and private votes; PieFed's Feed actor; PieFed's API
  and mobile app compatibility; interoperating with PieFed instances;
  PieFed's moderation features; PieFed vs Lemmy differences; or the
  Threadiverse ecosystem.
user-invocable: false
---

# PieFed — Complete Reference

## Overview

PieFed is a free, open-source, federated link aggregation and discussion
platform — a Python-based alternative to Reddit and Lemmy in the
Fediverse "Threadiverse." Created by Rimu Atkinson (Christchurch, New
Zealand) with the first code published July 28, 2023 and the flagship
instance (piefed.social) launched January 4, 2024. Licensed AGPL-3.0.

PieFed federates via ActivityPub using the same Group/Page/Note model as
Lemmy, making it fully interoperable with Lemmy, Mbin, and the wider
Fediverse. Its distinguishing features are: **cross-post deduplication**
with merged comments, **federated Feeds** (multi-community collections
via a custom `Feed` actor type), **private/anonymous voting** via proxy
user profiles, **trust & safety as a first-class design concern**
(reputation tracking, 3,000+ pre-blocked disinformation domains, AI
content filtering), and a **deliberately simple Python/Flask codebase**
designed for contributor accessibility.

The name "PieFed" is a portmanteau of "Python" and "Federation." The
repository is named "pyfedi" and hosted on Codeberg (not GitHub). As of
early 2026: 75+ instances, ~2,000 MAU, 82,571 lines of code, 62
contributors. "Very High Activity" on Open Hub.

---

## 1. Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend language | Python (3.9+, ~70% of codebase) |
| Web framework | Flask |
| Frontend | htmx + vanilla JavaScript + Bootstrap CSS |
| Template engine | Jinja2 |
| Database | PostgreSQL 17 |
| ORM | SQLAlchemy (Flask-SQLAlchemy) |
| Migrations | Alembic (`flask db upgrade`) |
| Task queue | Celery with Redis broker |
| Cache | Redis 6.2 (optional) |
| Application server | Gunicorn |
| Real-time notifications | FastAPI + Uvicorn (separate service) |
| Linting | Ruff |
| i18n | Babel |
| Deployment | Docker (5-service compose), bare metal, YunoHost |
| License | AGPL-3.0 |

Design philosophy: "Clean, simple code" with "no fancy design patterns
or algorithms." Only requires Python + PostgreSQL; Redis is optional.
Dramatically lighter resource usage than Lemmy — one user reported
server load of ~1 vs Lemmy's ~12 on identical hardware.

---

## 2. ActivityPub Object Type Mapping

| PieFed Concept | ActivityPub Type | Notes |
|----------------|------------------|-------|
| Community | `Group` | Relay actor; Announces content to followers |
| User | `Person` | Creates content, moderates |
| Bot | `Service` | Bot accounts |
| Feed | `Feed` | PieFed extension (FEP-1d80); federated multi-community collection |
| Post | `Page` | Primary post type, mandatory title (`name`) |
| Article | `Article` | Long-form content |
| Link post | `Link` | URL submissions |
| Comment | `Note` | Tree structure via `inReplyTo` |
| Poll | `Question` | `oneOf`/`anyOf` choices, up to 15 options |
| Event | `Event` | `startTime`, `endTime`, `timezone`, `participantCount` |
| Video | `Video` | PeerTube video embeds |
| Direct message | `ChatMessage` | Private user-to-user |

---

## 3. Communities as Group Actors

Communities are `Group` actors with their own inboxes, following the
same Announce relay pattern as Lemmy — all content flows through the
community actor and is wrapped in `Announce` for distribution to
subscribers across instances.

### Community-Specific Attributes

| Attribute | Description |
|-----------|-------------|
| `sensitive` | NSFW flag |
| `nsfl` | Not-safe-for-life flag (separate from NSFW) |
| `genAI` | AI-generated content flag |
| `postingRestrictedToMods` | Only moderators can post |
| `newModsWanted` | Community is seeking moderators |
| `privateMods` | Moderator list is hidden |
| `defaultPostType` | Default content type for new posts |
| `questionAnswer` | StackOverflow-style Q&A mode enabled |
| `moderators` | OrderedCollection of moderators |
| `featured` | Pinned posts collection |
| `tagsForPosts` | Available flair/tag options (Lemmy-compatible) |

### Moderator Attribution

PieFed accepts **both** `attributedTo` (Lemmy/Mbin style) and
`moderators` (Kbin style) for moderator lists, improving cross-platform
compatibility.

### Community Types

- **Federated** (default): Full ActivityPub federation
- **Local-only**: Visible only on the home instance, no federation
- **Private** (v1.6+): Invitation-only, no federation, posts visible
  only to members

---

## 4. Voting — Like, Dislike, and Private Votes

PieFed uses `Like` (upvote) and `Dislike` (downvote) activities, same
as Lemmy. However, PieFed adds a **private/anonymous voting** system
that is unique in the Threadiverse.

### Private Voting Mechanism

Users have **two profiles**: a main profile (for posting) and an
**anonymous proxy profile** (no name, avatar, or bio) used exclusively
for voting. When "Vote privately" is enabled:

- Votes sent to Lemmy/Mbin instances use the anonymous proxy profile
- New accounts have private voting **enabled by default**
- Votes can also be fully local (not federated at all)

### Community-Level Vote Controls

- Moderators can **restrict downvoting** to subscribed members only
- Downvoting can be restricted to "trusted" instances (a third tier
  between full federation and defederation)
- Communities can **disable downvotes entirely**
- "Low quality" communities (e.g., memes) don't award karma for upvotes

### Reputation Tracking

- **"Attitude" metric**: tracks ratio of downvotes to upvotes per user;
  flags excessive downvoters
- Comments scoring **-10 or below** are auto-collapsed
- Users with negative karma get **red warning icons** next to names
  (double red for severely negative)
- New accounts (first 7 days) display a special indicator

---

## 5. The Feed Actor (FEP-1d80)

PieFed introduces a custom `Feed` actor type — a federated equivalent
of Reddit's multi-reddits. This is defined in **FEP-1d80**.

A Feed is an ActivityPub actor of type `Feed` that aggregates multiple
communities (Group actors) into a single subscribable collection. Feeds
can include communities from any federated instance, PeerTube channels,
and Mastodon accounts.

- Feeds can be **public** (discoverable, subscribable) or **private**
- Feed actors are discoverable via WebFinger
- Users on remote PieFed instances can subscribe to a Feed like any
  other actor
- Feeds are managed via `Add`/`Remove` activities to add/remove
  communities

This is a PieFed-specific extension — Lemmy and Mbin do not support
the `Feed` actor type, though the FEP is open for adoption.

---

## 6. Full Activity Reference

### Incoming Activities

| Activity | Purpose |
|----------|---------|
| `Follow` | Subscribe to community/feed |
| `Accept` / `Reject` | Subscription response |
| `Create` | New post, comment, chat message, poll |
| `Update` | Edit post/comment, update community profile |
| `Delete` | Remove post, comment, PM, feed |
| `Like` | Upvote |
| `Dislike` | Downvote |
| `EmojiReact` | Custom emoji reaction (unicode or `:name:` format) |
| `PollVote` | Vote in a poll |
| `ChooseAnswer` | Mark comment as answer (Q&A mode) |
| `Add` | Add moderator, sticky post, add community to feed |
| `Remove` | Remove moderator, unsticky post, remove from feed |
| `Lock` | Lock post or comment (including children) |
| `Flag` | Report content |
| `Announce` | Boost/share (wraps other activities) |
| `Undo` | Reverse any previous activity |

### Community → Followers

| Activity | Purpose |
|----------|---------|
| `Accept{Follow}` | Automatic response to Follow |
| `Announce{*}` | Rebroadcast received activities to all followers |

Community outboxes serve `Announce(Create(Page))` activities even for
non-local posts, functioning as content relays.

---

## 7. JSON-LD Context and Extensions

### Context

```json
[
  "https://www.w3.org/ns/activitystreams",
  "https://w3id.org/security/v1"
]
```

### Lemmy-Compatible Extensions

| Property | Used on | Description |
|----------|---------|-------------|
| `tagsForPosts` | Group | Available flair/tag options (Lemmy `CommunityTag`) |
| `postingRestrictedToMods` | Group | Restricted posting |
| `language` | Page, Note | Language metadata (`identifier` + `name`) |

### PieFed-Specific Extensions

| Property | Used on | Description |
|----------|---------|-------------|
| `genAI` | Group, Page | AI-generated content flag |
| `nsfl` | Group, Page | Not-safe-for-life flag |
| `flair` | Note | User flair (custom extension on comments) |
| `postingWarning` | Group | Contextual warning above comment form |
| `interactionPolicy` | Page | Interaction restrictions |
| `newModsWanted` | Group | Community seeking moderators |
| `questionAnswer` | Group | Q&A mode enabled |

---

## 8. Federation Architecture

### Activity Processing Flow

1. Parse JSON request body
2. Check federation pause status (normal / overload / permanently closed)
3. Extract actor and validate HTTP signature
4. Deduplicate via Redis (activity IDs stored with 90-second TTL)
5. Route to handler based on activity type
6. Process asynchronously via Celery task

### HTTP Signatures

| Aspect | Detail |
|--------|--------|
| Algorithm | RSA-SHA256 (also accepts `hs2019`) |
| Key size | 2048-bit RSA |
| Signed headers | `(request-target)`, `Host`, `Date`, `Digest`, `Content-Type`, `Accept` |
| Date tolerance | 3,600 seconds (1 hour) |
| Fallback | LD signatures via URDNA2015 normalization |
| Key cache | Up to 1,000 entries |

### Reliability

- Failed deliveries enter a retry queue with retries over several days
- **Batched federation** between PieFed instances reduces load
- Redis-based locking minimizes database deadlocks
- Federation can be **paused** during overload conditions

### Key Endpoints

| Path | Purpose |
|------|---------|
| `/.well-known/webfinger` | User, community, and feed discovery |
| `/.well-known/nodeinfo` | NodeInfo schema links |
| `/nodeinfo/2.0`, `/nodeinfo/2.1` | Server stats and protocol info |
| `/u/<actor>` | User actor (content-negotiated JSON/HTML) |
| `/c/<actor>` | Community actor |
| `/inbox` | Shared inbox |
| `/site_inbox` | Site-level inbox |
| `/api/v1/instance` | Mastodon-compatible instance info |

---

## 9. REST API

PieFed's API is intentionally **"95% the same as the Lemmy API"** to
enable reuse of Lemmy's mobile app ecosystem.

| Aspect | Detail |
|--------|--------|
| Base path | `/api/alpha/` |
| Documentation | Swagger at `/api/alpha/swagger` |
| Total endpoints | 100+ |
| Rate limiting | Applied to creation endpoints |

### Compatible Mobile Apps

Voyager, Interstellar (Android/iOS/Linux/Windows), Blorp (iOS),
Summit, with Boost and Photon in development.

### Endpoint Categories

- **Site** (5): instance info, configuration
- **Communities** (17): CRUD, flair, bans, moderation
- **Feeds** (3): create, edit, list
- **Posts** (18): CRUD, polls, flair, voting
- **Comments** (13): CRUD, answer marking
- **Private messages** (8): send, read, delete
- **Users** (20): profiles, notifications, flair, bans
- **Search** (4): content discovery
- **Images** (4): upload, manage
- **Admin** (2): site management

### Notable Unique Endpoints (beyond Lemmy)

- `/post/poll_vote` — poll voting
- `/comment/mark_as_answer` — Q&A answer selection
- `/feed/*` — Feed (multi-reddit) management
- `/community/flair/*` — flair management
- `/user/set_flair` — user flair

---

## 10. Moderation and Trust & Safety

PieFed was designed with safety as a first-class concern, drawing
inspiration from the Mastodon Covenant and "nudge theory."

### Reputation System

- **Karma tracking** with sortable low-karma account lists
- **"Attitude" metric**: percentage of downvotes vs upvotes per user
- **Visual indicators**: red icons for negative karma, double-red for
  severe, special icon for accounts < 7 days old
- **Auto-collapse** for comments at -10 or below

### Content Filtering

- **3,000+ pre-loaded domain blocklist** (disinformation, conspiracy,
  fake news sites)
- **4chan screenshot detection** via image recognition (auto-reported)
- **AI content labeling**: posts/communities tagged as AI-generated;
  users can hide all AI content like NSFW
- **NSFW and NSFL as separate flags**
- **Keyword filtering**: user-configurable
- **Bot content filter**: single checkbox

### Admin Tools

- Ban / Ban + Purge on user profiles
- IP-based ban evasion detection
- Username keyword filtering (blocks e.g. "1488")
- **Web of trust**: follow another instance's blocklist automatically
- Registration approval queue
- **"Authoritarian Inoculation"** feature with default blocks on known
  extremist instances

### Community-Level Moderation

- Per-community downvote policies
- Comment and post locking
- Post approval workflow (optional pre-publication review)
- Contextual warnings above comment forms
- Searchable moderation log
- Federated community bans
- `newModsWanted` flag for moderator recruitment

---

## 11. Content Types

| Type | Details |
|------|---------|
| Link posts | URL submissions |
| Text posts | Markdown body |
| Image posts | With alt text; width control via `![alt :: width=300px](url)` |
| Video posts | Direct upload (v1.5+, admin-configurable) |
| Polls | `Question` with `oneOf`/`anyOf`, up to 15 options, Mastodon-compatible |
| Events | Time, timezone, location, participant count |
| PeerTube videos | Embedded player, auto-import from channels |
| Cross-posts | Deduplicated with consolidated comment views |
| Scheduled posts | With timezone support |
| Wiki pages | Per-community editable wikis |
| Emoji reactions | Unicode and custom (`:piefed:`), federated as Likes for Lemmy compat |
| Quote posts | v1.6+, Mastodon quote-boost interop |
| StackOverflow Q&A | Comments markable as answers via `ChooseAnswer` |
| Spoilers | Flair-based with image blurring + inline spoiler text |

---

## 12. Interoperability

### Lemmy

- Fully compatible: Group communities, Page posts, Note comments,
  Like/Dislike votes, Announce relay
- API is 95% Lemmy-compatible (mobile apps work)
- Shared extensions: `tagsForPosts`, `CommunityTag`
- **Limitation**: polls and events cannot be posted TO Lemmy communities
  (prevented in PieFed's code to avoid errors)
- Community outboxes follow Lemmy's `Announce(Create(Page))` pattern

### Mastodon

- Users follow PieFed communities by **mentioning** them
- First paragraph becomes post title; rest becomes body
- Works: hashtags, images, alt text, videos, NSFW, polls, markdown,
  mentions, comments, editing, likes, boosts
- Poll voting is **bidirectional**
- Quote-boost interop (v1.6+)
- `/api/v1/instance` Mastodon-compatible endpoint

### PeerTube

- Channels can be followed directly from PieFed
- Videos arrive with embedded player
- New channels auto-import 10 recent videos
- Posts restricted to channel owners

### Mbin / Kbin

- Full community federation
- PieFed accepts Kbin's `moderators` property alongside Lemmy's
  `attributedTo`

### Known Limitations

- "Discoverability between PieFed and other parts of the Fediverse is
  limited"
- Markdown variants differ slightly from Lemmy's
- Remote Mastodon `Announce` activities without full inlined objects
  are logged but skipped

---

## 13. Installation and Deployment

### Bare Metal

```
git clone https://codeberg.org/rimu/pyfedi.git
python -m venv venv && source venv/bin/activate
pip install wheel && pip install -r requirements.txt
cp env.sample .env  # configure SECRET_KEY, DATABASE_URL, etc.
flask db upgrade && flask init-db
gunicorn -b 0.0.0.0:5000 pyfedi:app
```

Setup reported to take "within half an hour."

### Docker (5 services)

| Service | Purpose |
|---------|---------|
| `db` | PostgreSQL 17 |
| `redis` | Redis 6.2 |
| `celery` | Celery worker for async federation tasks |
| `app` | Flask/Gunicorn web app (port 8030) |
| `piefed_notifs` | FastAPI/Uvicorn real-time notifications (port 8040) |

### Other Options

- **YunoHost**: available in app store (v1.4+)
- **Managed hosting**: fedihost.co (beta), Elest.io
- **S3 storage**: Cloudflare R2, Wasabi, Backblaze B2 for media and
  post archival

### Scaling (piefed.social reference: 8-core, 16GB, ~1000 MAU)

- PostgreSQL: `shared_buffers=6GB`, `effective_cache_size=9GB`,
  `max_connections=300`
- DB pool: `POOL_SIZE=30`, `MAX_OVERFLOW=70`
- Nginx caching recommended (RAM-backed `/dev/shm/nginx`)
- Post archival to S3 reduces database size over time

---

## 14. Codebase Structure

```
pyfedi/
├── app/
│   ├── activitypub/        # Federation (routes, signatures, util, actor)
│   ├── admin/              # Admin panel
│   ├── api/alpha/          # Lemmy-compatible REST API
│   ├── auth/               # Authentication
│   ├── chat/               # Real-time chat
│   ├── community/          # Community management
│   ├── feed/               # Feed (multi-reddit) management
│   ├── post/               # Post handling
│   ├── search/             # Search
│   ├── shared/tasks/       # Celery async tasks (adds, blocks, deletes,
│   │                       #   flags, follows, groups, likes, locks,
│   │                       #   notes, pages, removes, users, maintenance)
│   ├── plugins/            # Plugin system
│   ├── tag/                # Hashtag management
│   ├── models.py           # All DB models (209KB single file)
│   ├── inoculation.py      # Anti-propaganda feature
│   └── constants.py
├── migrations/             # Alembic migrations
├── tests/
├── docs/                   # Developer docs, AP examples, ERD
├── compose.yaml            # Docker Compose (5 services)
├── pyfedi.py               # Entry point
├── FEDERATION.md           # Federation documentation
└── CONTRIBUTING.md
```

Key namespaces: `app.activitypub`, `app.api.alpha`, `app.community`,
`app.post`, `app.feed`, `app.shared.tasks`

---

## 15. PieFed vs Lemmy — Key Differences for Implementers

| Aspect | PieFed | Lemmy |
|--------|--------|-------|
| Language | Python/Flask | Rust/Actix-web |
| Resource usage | ~1 load avg | ~12 load avg (same hardware) |
| `Feed` actor type | Yes (FEP-1d80) | No |
| Private voting | Proxy user profiles | All votes public/federated |
| Cross-post dedup | Merged comment views | Separate posts |
| AI content flag | `genAI` property | No |
| NSFL flag | Separate from NSFW | No (NSFW only) |
| `EmojiReact` | Yes (federated as Likes to Lemmy) | No |
| `ChooseAnswer` | Yes (Q&A mode) | No |
| `Event` objects | Yes | No |
| `PollVote` | Yes (Mastodon-compatible) | No native polls |
| Flair federation | `flair` on Note + `tagsForPosts` | `tagsForPosts` only |
| API path | `/api/alpha/` | `/api/v3/` |
| API compatibility | 95% Lemmy-compatible | — |
| JSON-LD processing | Plain JSON (no expansion) | Plain JSON (no expansion) |

---

## 16. Common Implementation Mistakes

1. **Assuming PieFed is a Lemmy fork**: PieFed is a completely separate
   Python codebase, not a Rust fork — protocol-compatible but
   architecturally different

2. **Not handling the `Feed` actor type**: PieFed federates `Feed`
   actors via WebFinger; other software should treat unknown actor types
   gracefully rather than erroring

3. **Expecting public votes**: PieFed defaults to private voting — vote
   activities may come from anonymous proxy profiles or not at all.
   Do not assume vote counts match federated Like/Dislike activities

4. **Ignoring `genAI` and `nsfl` properties**: PieFed adds these to
   Group and Page objects — unknown properties should be ignored, not
   cause parsing errors

5. **Sending polls/events to PieFed communities hosted on Lemmy**:
   PieFed prevents posting polls and events to remote Lemmy communities
   because Lemmy doesn't support them — but if you federate these object
   types to PieFed-hosted communities, they will work

6. **Not handling `EmojiReact`**: PieFed sends `EmojiReact` activities
   for emoji reactions — these federate as `Like` activities to Lemmy
   for compatibility, but other implementations may receive the raw
   `EmojiReact` type

7. **Assuming all communities federate**: PieFed supports local-only
   and private communities that are invisible to federation

8. **Not supporting `ChooseAnswer`**: In Q&A mode communities, PieFed
   sends `ChooseAnswer` activities to mark accepted answers — unknown
   activity types should be ignored gracefully
