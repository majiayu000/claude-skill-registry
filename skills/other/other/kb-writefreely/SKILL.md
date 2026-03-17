---
name: kb-writefreely
description: >
  Background knowledge about WriteFreely, the open-source federated blogging
  platform written in Go (AGPL-3.0) by Matt Baer / Musing Studio. Covers
  the origin story (Write.as anonymous writing platform launched 2014,
  open-sourced as WriteFreely November 2018 after adding ActivityPub), the
  write-only/broadcast federation model (blogs can be followed but cannot
  follow others, no incoming comments/replies displayed, no moderation),
  the actor model (each blog/collection is a Person actor with handle
  @blog@instance.com), the Article vs Note object type distinction
  (double-line break heuristic, notes_only config option), supported
  activities (outbound Create/Update/Delete, inbound Follow/Undo/Like),
  RSA-SHA256 HTTP signatures with per-blog keypairs, the tech stack
  (Go/MySQL or SQLite/single binary deployment/256 MB RAM/Raspberry Pi),
  configuration (single-user vs multi-user modes, federation toggle,
  .ini config file), NodeInfo with WriteFreely-specific metadata, the
  RESTful API (Posts/Collections/Users with token auth, anonymous
  publishing), the Musing Studio ecosystem (Write.as, WriteFreely.host,
  Snap.as, Remark.as, Submit.as, Read.as), Gopher protocol support,
  Web Monetization, email newsletters, custom CSS/JS per blog, OAuth 2.0
  integration, comparison with Plume and Ghost. Load when the user asks
  about WriteFreely; implementing a WriteFreely-compatible ActivityPub
  server; how WriteFreely blogs federate; WriteFreely's Article vs Note
  distinction; WriteFreely's write-only federation model; WriteFreely's
  API; the Write.as and Musing Studio ecosystem; federating with
  WriteFreely instances; long-form blogging in the Fediverse; or
  building software that interoperates with WriteFreely.
user-invocable: false
---

# WriteFreely — Complete Reference

## Overview

WriteFreely is a free, open-source, federated blogging platform written
in **Go**, created by **Matt Baer** and developed under **Musing Studio**
(formerly the Write.as team). Licensed **AGPL-3.0**.

WriteFreely originated from **Write.as**, a privacy-focused anonymous
writing platform launched in late **2014**. After adding ActivityPub
federation support, the codebase was refactored and released as open
source in **November 2018**. It describes itself as "the social media
hater's blogging platform" — deliberately rejecting feeds, alerts, and
engagement metrics in favor of a distraction-free writing environment.

WriteFreely's federation model is **write-only/broadcast**: blogs can
be followed from Mastodon and other ActivityPub platforms, but WriteFreely
cannot follow others, does not display incoming replies or comments, and
has no follower moderation. This is a deliberate design choice — it is a
writing platform, not a social network.

As of early 2026, Write.as has hosted over 600,000 users with 6.6 million
posts. The WriteFreely open-source software powers hundreds of independent
instances across the fediverse.

---

## 1. Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Go (golang) — 64% of codebase |
| Templates | Go Template — 24% |
| Styling | LESS — 6.5% |
| Client-side | JavaScript — 3.8% |
| Database | MySQL/MariaDB 5.6+ or SQLite |
| Rich editor | ProseMirror (WYSIWYG "classic" mode) |
| License | AGPL-3.0 |

### Key Technical Characteristics

- **Single binary deployment** on any platform/architecture Go supports
- **Minimal resources**: runs on servers with 256 MB RAM, including
  Raspberry Pi
- **No external dependencies** in SQLite mode
- Built-in HTTP server with TLS support (Let's Encrypt auto-cert)
- Optional Gopher protocol server (since v0.13)
- Go 1.23+ and Node.js 15+ required for development builds

### Database

Two backends supported:

- **MySQL/MariaDB 5.6+**: `CREATE DATABASE writefreely CHARACTER SET
  latin1 COLLATE latin1_swedish_ci;`
- **SQLite**: Built-in, no external database needed

PostgreSQL is **not** supported.

Database tables include: user access tokens, public/private RSA keypairs
per collection (for signing ActivityPub requests), collections (blogs),
posts, remote users, and remote follows.

---

## 2. ActivityPub Implementation

### Actor Model

Each **blog (collection)** is an ActivityPub actor of type `Person`. In
single-user mode, the instance acts as the single blog actor.

The fediverse handle format is `@blog@instance.com` (or
`@username@instance.com` in single-user mode).

Each collection/blog has:
- A public/private RSA keypair for signing requests
- An inbox endpoint for receiving activities
- An outbox endpoint for published content
- A followers collection

### Object Types

WriteFreely federates posts as either `Article` or `Note`:

- **`Article`**: Posts containing a double-line break (paragraph break).
  The default for multi-paragraph blog posts. Includes the post title
  in the `name` property.
- **`Note`**: Posts without paragraph breaks (single-paragraph). Can be
  forced for all posts via `notes_only = true` configuration.

The heuristic: if the post body contains `\n\n` (double newline), it is
sent as `Article`; otherwise as `Note`. This was implemented in v0.13
(merged March 2021).

Since v0.16, posts include `preview`/`summary` fields so microblogging
platforms like Mastodon and Threads show excerpts with links rather than
just a link.

### Activities

WriteFreely supports a deliberately limited set of activities:

**Outbound (WriteFreely sends):**

| Activity | Trigger |
|----------|---------|
| `Create{Article}` or `Create{Note}` | Post published |
| `Update{Article}` or `Update{Note}` | Post edited |
| `Delete` | Post deleted |

**Inbound (WriteFreely receives):**

| Activity | Effect |
|----------|--------|
| `Follow` | Remote user follows a blog |
| `Undo{Follow}` | Remote user unfollows |
| `Like` | Remote user favorites a post (count tracked since v0.16) |

### Write-Only / Broadcast Nature

This is the most critical detail for interoperability:

- Blogs **can be followed** from Mastodon, Pleroma, and other AP platforms
- Posts **are delivered** to followers' timelines
- **No incoming replies/comments**: WriteFreely does not display replies
  from federated users on the blog itself
- **No outgoing follows**: Cannot follow other users from WriteFreely
- **No blocking/managing follows**: No moderation tools for followers
- **No Announce/boost**: WriteFreely does not send or process boosts
- **Mentions as workaround**: Authors can mention their own Mastodon
  account (`@handle@their.instance`) in posts so fediverse replies route
  to their microblogging account

### HTTP Signatures

RSA-SHA256 signatures with per-blog keypairs. Signed headers include:
request target, date, host, and digest. Remote user data stored: actor
ID, inbox URL, shared inbox URL, user handle, and public key.

### Libraries

- **go-fed/activity/streams**: ActivityPub library for Go
- **writefreely/go-nodeinfo**: Fork of NodeInfo with WriteFreely-specific
  metadata

---

## 3. Configuration

WriteFreely uses an `.ini` config file (`config.ini` by default).

### Instance Modes

- **Single-user**: One blog, the instance is the blog actor
- **Multi-user**: Multiple accounts, each with up to 5 blogs (default),
  local timeline/reader, admin dashboard, invitation system

### Key Federation Settings

| Field | Description | Default |
|-------|-------------|---------|
| `federation` | ActivityPub federation toggle | true |
| `notes_only` | Send all posts as Note (not Article) | false |
| `public_stats` | NodeInfo statistics visibility | true |

### Other Notable Settings

| Field | Description | Default |
|-------|-------------|---------|
| `single_user` | Single-blog instance mode | false |
| `editor` | Editor template: pad, bare, classic | pad |
| `open_registration` | Public signup (multi-user) | true |
| `max_blogs` | Blogs per account (multi-user) | 5 |
| `default_visibility` | New blog visibility | unlisted |
| `local_timeline` | Instance reader (multi-user) | true |
| `monetization` | Web Monetization support | true |
| `gopher_port` | Gopher server port (0 = disabled) | 0 |

---

## 4. NodeInfo

WriteFreely implements NodeInfo via `github.com/writefreely/go-nodeinfo`
(v1.2.0, MIT license), a fork with WriteFreely-specific metadata.

### Discovery

`/.well-known/nodeinfo` → points to full NodeInfo URL.

### WriteFreely-Specific Metadata

```json
{
  "metadata": {
    "nodeName": "My Blog",
    "nodeDescription": "A writing community",
    "private": false,
    "software": {
      "homepage": "https://writefreely.org",
      "github": "https://github.com/writefreely/writefreely",
      "follow": "https://writing.exchange/@writefreely"
    },
    "maxBlogs": 5,
    "publicReader": true,
    "invites": true
  },
  "protocols": ["activitypub"],
  "services": {
    "outbound": ["rss2.0"]
  },
  "software": {
    "name": "writefreely",
    "version": "0.16.0"
  }
}
```

---

## 5. API

WriteFreely provides a RESTful API (shared with Write.as) with full
read access and publishing.

### Authentication

Token-based: `Authorization: Token {access_token}` (UUID format).
Anonymous publishing is supported — no auth required for creating posts.

Accepts form data (default) or `application/json`. Returns JSON.

### Core Endpoints

**Posts:**

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | `/api/posts` | Optional | Create post |
| GET | `/api/posts/{id}` | No | Retrieve post |
| POST | `/api/posts/{id}` | Optional | Update post |
| DELETE | `/api/posts/{id}` | Optional | Delete post |
| POST | `/api/posts/claim` | Required | Claim anonymous posts |

**Collections (Blogs):**

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | `/api/collections` | Required | Create collection |
| GET | `/api/collections/{alias}` | No | Get metadata |
| POST | `/api/collections/{alias}/posts` | Required | Publish to blog |
| GET | `/api/collections/{alias}/posts` | No | List posts |
| GET | `/api/collections/{alias}/posts/{slug}` | No | Get single post |

**Users:**

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | `/api/auth/login` | No | Authenticate |
| GET | `/api/me` | Required | Get user info |
| GET | `/api/me/posts` | Required | List user's posts |
| GET | `/api/me/collections` | Required | List user's blogs |

### Data Models

**Post**: id, slug, token (for anonymous updates), title, body
(Markdown), appearance (sans/serif/wrap/mono/code), language, rtl,
created, updated, views, tags, collection.

**Collection**: alias (URL slug), title, description, style_sheet,
script, visibility (0=Unlisted, 1=Public, 2=Private,
4=Password-protected), views, total_posts.

---

## 6. Features

### Writing and Publishing

- Distraction-free Markdown editor with three modes: pad (default),
  bare, classic (WYSIWYG via ProseMirror, since v0.13)
- MathJax formula rendering
- Hashtag organization
- Custom CSS and JavaScript per blog
- Font appearances: serif, sans-serif, monospace, wrapped
- RTL script support, 20+ language localizations
- Draft posts, static pinned pages, post signatures
- RSS feed per blog (automatic)
- SEO best practices encoded by default
- No native image hosting — must embed from external sources (Snap.as
  or other hosts)

### Multi-User Community

- Multiple blogs per account (configurable, default 5)
- Local timeline / reader for shared content
- Privacy levels: public, unlisted, private, password-protected
- Open or closed registration, invitation system
- Admin dashboard with instance stats and user management

### Federation Features

- Fediverse verification badges via rel="me" (since v0.14)
- Like counts visible to blog authors (since v0.16)
- Subscribers page showing fediverse followers
- fediverse:creator tag linking to another profile (since v0.16)
- Mentions via `@handle@their.instance` in post content

### Other Protocols and Integrations

- Gopher protocol server (since v0.13)
- Web Monetization micropayments (since v0.13)
- Email newsletters via Mailgun (since v0.15)
- SMTP for password resets and notifications (since v0.16)
- OAuth 2.0: Generic, Gitea, GitLab, Slack, Write.as

---

## 7. Ecosystem

WriteFreely is part of the **Musing Studio** ecosystem:

| Service | Purpose |
|---------|---------|
| **Write.as** | Hosted blogging platform ($1-10/month) |
| **WriteFreely** | Open-source software (self-hosted) |
| **WriteFreely.host** | Managed WriteFreely community hosting |
| **Snap.as** | Minimalist photo sharing |
| **Remark.as** | Commenting system for Write.as blogs |
| **Submit.as** | Accept writing submissions |
| **Read.as / ReadFreely** | ActivityPub reading client (paused) |

Musing Studio was founded by Matt Baer in 2015. He runs the company
solo. Core values: ad-free, tracking-free, customer-funded (no venture
capital), open web interoperability.

---

## 8. Comparisons

### WriteFreely vs Plume

| Aspect | WriteFreely | Plume |
|--------|------------|-------|
| Language | Go | Rust |
| Federation model | Write-only (broadcast) | Bidirectional (shows replies) |
| Customization | Custom CSS only | Themes, fonts, layouts |
| Maintenance | Actively maintained | Not actively maintained |
| Object types | Article + Note | Article |

### WriteFreely vs Ghost

| Aspect | WriteFreely | Ghost |
|--------|------------|-------|
| Language | Go | Node.js |
| AP integration | Since 2018 (core) | Since 2024 (core) |
| Focus | Minimalist writing | Full-featured CMS |
| Image hosting | None (external only) | Built-in |
| Newsletters | Mailgun integration | Built-in |
| Themes | Custom CSS | Full theme system |
| Resources | 256 MB RAM | 1 GB+ RAM |

---

## 9. Interoperability Notes for Implementers

1. **Blogs are `Person` actors** — each WriteFreely blog (collection)
   presents itself as a `Person` actor with a fediverse handle of
   `@alias@instance.com`. Follow a blog by sending `Follow` to this
   actor.

2. **Write-only federation** — WriteFreely will never send `Follow`,
   `Announce`, `Like`, or reply activities. It only sends `Create`,
   `Update`, and `Delete` for its own posts. If your software expects
   bidirectional interaction, WriteFreely will not reciprocate.

3. **Article vs Note distinction** — multi-paragraph posts arrive as
   `Article` objects (with `name` containing the title), single-paragraph
   posts arrive as `Note` objects (no `name`). If an instance has
   `notes_only = true`, all posts arrive as `Note`. Your software should
   handle both types from WriteFreely.

4. **No incoming comment support** — if your users reply to a WriteFreely
   post, their reply will be delivered to the WriteFreely inbox but will
   **not be displayed** on the blog. The reply exists only on your
   platform. Authors may work around this by mentioning their Mastodon
   account in posts.

5. **Like tracking** — since v0.16, WriteFreely tracks `Like` activities
   and shows a count to the blog author. Sending `Like` to a WriteFreely
   blog will be acknowledged, but `Undo{Like}` handling may vary.

6. **No shared inbox optimization** — WriteFreely stores shared inbox
   URLs from remote actors but primarily uses individual inboxes. Verify
   delivery works with both paths.

7. **Post excerpts on microblogging platforms** — since v0.16, WriteFreely
   includes `preview`/`summary` fields on `Article` objects. Mastodon and
   Threads will show an excerpt with a link rather than just a bare link.
   Older WriteFreely versions may send Articles without summaries.

8. **NodeInfo identifies the software** — look for
   `"name": "writefreely"` in the NodeInfo software block to identify
   WriteFreely instances. The metadata includes WriteFreely-specific
   fields like `maxBlogs`, `publicReader`, and `invites`.

9. **RSS is always available** — every WriteFreely blog has an RSS feed
   regardless of federation settings. If federation is disabled, RSS is
   still the primary syndication method.

10. **No image hosting** — WriteFreely posts reference externally-hosted
    images via Markdown image syntax. If your software processes
    WriteFreely content, images will be URLs to third-party hosts
    (including Snap.as), not to the WriteFreely instance itself.
