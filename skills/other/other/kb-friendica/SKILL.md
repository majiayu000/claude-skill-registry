---
name: kb-friendica
description: >
  Background knowledge about Friendica, the federated social networking
  platform (Facebook alternative). Covers Friendica's history and lineage
  (Mistpark 2010, Friendika, Friendica, the Red Matrix/Hubzilla fork),
  its multi-protocol architecture (ActivityPub, DFRN, Diaspora protocol
  simultaneously), the DFRN protocol (Distributed Friends and Relations
  Network — Atom/ActivityStreams XML with public-key crypto handshake,
  dfrn_notify/dfrn_poll/dfrn_request endpoints), the ActivityPub
  implementation (Receiver/Processor/Transmitter classes, APDelivery
  workers, Mastodon-compatible API), the Diaspora protocol integration
  (reverse-engineered PHP implementation), the addon/plugin system
  (hook-based with 100+ hooks, Smarty3 templates, module intercept),
  cross-network connectors (Bluesky bidirectional, Tumblr, GNU Social,
  email IMAP/SMTP, RSS/Atom, WordPress/LiveJournal/Dreamwidth post-only),
  privacy controls (ACLs, Circles/Groups, multiple profiles, per-post
  permissions), content model (200,000-char posts, BBCode, photo albums,
  events, forums, polls), the database schema (97 tables, hub-and-spoke
  post model with post/post-user/post-content/post-media separation),
  the 8-layer architecture (Client/Frontend/Application/Business Logic/
  Content Processing/Federation/Data/Background Worker), the tech stack
  (PHP, MySQL/MariaDB/PostgreSQL, Apache/Nginx, Smarty3, Composer,
  AGPL-3.0), supported FEPs (group federation, OpenWebAuth, long-form
  text, FEP-67ff), federation interoperability quirks (bridge role
  between protocol ecosystems, OStatus dropped in 2024.12), and the
  relationship to Mike Macgirvin's later projects (Hubzilla, Zot/Nomad
  protocol, Streams, Forte). Load when the user asks about Friendica
  federation; implementing a Friendica-compatible ActivityPub server;
  the DFRN protocol; how Friendica bridges multiple protocol ecosystems;
  Friendica's addon system; Friendica's privacy model; interoperating
  with Friendica instances; Friendica's Mastodon API compatibility; the
  Friendica-to-Hubzilla lineage; or cross-posting from Friendica to
  Bluesky, Tumblr, Diaspora, or other networks.
user-invocable: false
---

# Friendica — Complete Reference

## Overview

Friendica is a free, open-source, decentralized social networking platform
— the Fediverse's answer to Facebook. Created by Mike Macgirvin (former
Netscape/AOL/Sun messaging engineer) in July 2010 under the original name
"Mistpark," it is one of the oldest continuously active Fediverse projects,
predating Mastodon by six years. Licensed AGPL-3.0.

Friendica's defining characteristic is its **multi-protocol bridge role**.
It simultaneously speaks ActivityPub, the Diaspora protocol, and its native
DFRN protocol, and connects (via addons) to Bluesky, Tumblr, GNU Social,
email (IMAP/SMTP), and RSS/Atom feeds. Fedi.Tips calls it "a sort of Swiss
Army knife of the Fediverse." Where Mastodon is a Twitter replacement
(microblogging), Friendica is a Facebook replacement (full social networking)
with Circles/Groups, photo albums, events, forums, 200,000-character posts,
and fine-grained ACL-based privacy controls.

Current maintainers are Tobias Diekershoff (FSFE) and Michael Vogel. As of
2025: ~220 active instances, ~20,800 registered users, ~2.8 million
statuses, 27,000+ commits from 250+ contributors.

---

## 1. History and Lineage

| Date | Event |
|------|-------|
| July 2010 | Mike Macgirvin creates **Mistpark** in Australia, motivated by "Quit Facebook Day" privacy concerns |
| Mid-2010 | Within first month: federation with StatusNet (OStatus), RSS, email integration |
| Late 2010 | Renamed to **Friendika** |
| July 2011 | Zot protocol first named (Macgirvin's next-gen protocol design) |
| Sep 2011 | Macgirvin forks as "Free-Friendika" (MIT license) |
| Oct 2011 | Name changed to **Friendica** |
| Jan 2012 | First "Friendica" release (v2.37) |
| 2012 | Diaspora protocol reverse-engineered from scratch (~6 months) |
| May 2012 | Macgirvin departs, forks into **Red** / **Friendica Red** (MIT) |
| 2012-2013 | Red becomes **Red Matrix** |
| May 2015 | Red Matrix renamed to **Hubzilla** |
| Dec 2018 | **ActivityPub** support shipped |
| May 2023 | Initial Bluesky connector |
| Dec 2023 | Bidirectional Bluesky; Circles and Channels introduced |
| Jan 2025 | v2024.12: **OStatus dropped**, Prometheus metrics, FEP-67ff |
| Jan 2026 | v2026.01 "Blutwurz": reworked hook system, media embedding overhaul |

### The Fork Lineage

```
Mistpark (2010)
  └─> Friendika (2010) ─> Friendica (2011, AGPL-3.0)
  └─> Free-Friendika (2011, MIT)
        └─> Red / Friendica Red (2012)
              └─> Red Matrix (2013)
                    └─> Hubzilla (2015, Zot protocol)
                          └─> Osada, Zap, Roadhouse (2018-2022)
                                └─> Streams (2021-present, Nomad protocol)
                                      └─> Forte (2024, ActivityPub-only)
```

### Founding Motivation

Macgirvin left Facebook in early 2010 and found no decentralized alternative
with both Facebook-like interactivity and privacy. StatusNet's OStatus had
"absolutely nothing in the way of privacy." He created the DFRN protocol to
address four gaps:

1. No protocol for friend connections
2. No privacy support in social protocols
3. No cross-server wall posting
4. Private media required sending copies to all recipients

---

## 2. Technology Stack

| Layer | Technology |
|-------|-----------|
| Backend language | PHP (7.4+, 8.x recommended, supports 8.5) |
| Database | MariaDB (recommended), MySQL, PostgreSQL 9.6+ |
| Web server | Apache (mod-rewrite) or Nginx |
| Template engine | Smarty3 |
| Dependency management | Composer |
| DI container | Dice |
| Themes | frio (default), vier, quattro |
| License | AGPL-3.0 |
| Hardware minimum | 2 GB RAM |
| Required PHP extensions | Curl, GD, GMP, PDO, mbstring, Intl, MySQLi, OpenSSL, POSIX |

### Entry Points

- **Web**: `index.php` → `App::processRequest()`
- **CLI**: `bin/console.php` → `App::processConsole()`
- **Worker**: `bin/console.php worker` (or legacy `bin/worker.php`)

### Configuration Hierarchy (increasing priority)

1. `static/defaults.config.php` — system defaults
2. `static/settings.config.php` — admin-configurable defaults
3. `config/local.config.php` — instance-specific overrides
4. `config` database table — runtime settings (highest)

---

## 3. Federation Protocols

Friendica is unique in speaking **multiple federation protocols
simultaneously**, acting as a bridge between otherwise-separate ecosystems.

### Currently Supported

| Protocol | Purpose | Since |
|----------|---------|-------|
| **ActivityPub** | Federation with Mastodon, Pleroma, Pixelfed, PeerTube, Lemmy, etc. | Dec 2018 |
| **Diaspora protocol** | Federation with Diaspora pods, Hubzilla | 2012 |
| **DFRN** | Native Friendica-to-Friendica federation | July 2010 |
| **WebFinger** | User discovery | — |
| **HTTP Signatures** | Request authentication for ActivityPub | — |
| **NodeInfo** | Server metadata discovery | — |
| **Salmon** | Message exchange for replies and mentions | — |

### Dropped

| Protocol | Dropped | Reason |
|----------|---------|--------|
| **OStatus** (PubSubHubbub + Atom) | v2024.12 | Too few active OStatus-only servers |

### Supported FEPs

Nine FEPs including: group federation (Lemmy/Kbin compatible), OpenWebAuth
(Hubzilla login), long-form text (partial), application actor identification,
object links, and FEP-67ff (FEDERATION.md).

---

## 4. The DFRN Protocol

**Distributed Friends and Relations Network** — Friendica's native protocol
for Friendica-to-Friendica federation. Creates an authenticated pipe between
users using public-key cryptography.

### Message Format

- Atom Syndication Protocol wrapper with ActivityStreams 1.0, threading,
  and media extensions
- Content in BBCode internally
- Specification: `spec/dfrn2.pdf` in the Friendica repository

### Key Concepts

- Distinguishes **author** (content creator) from **owner** (profile host)
- Communication boundary is the individual's profile page
- "Friends of friends" are visible, but direct contact required for
  communication with third parties

### Endpoints

| Endpoint | Purpose |
|----------|---------|
| `dfrn_request` | Friend/contact requests |
| `dfrn_notify` | Delivery (push) |
| `dfrn_poll` | Feed retrieval (pull) |

### Handshake

1. Remote site POSTs to `dfrn_poll` with `type=profile-check`
2. Includes duplex direction, relationship `dfrn_id`, and a random number
   encrypted with the site's DFRN public key
3. Original site decodes `dfrn_id`, verifies relationship, decodes challenge,
   matches `sec` string

### Delivery Model

- **Public messages**: dual path — BBCode to DFRN clients + HTML conversion
  with PubSubHubbub notification
- **Private messages**: direct delivery via `dfrn_notify` to recipients only;
  public hubs remain uninformed
- **Polling**: `src/Worker/OnePoll.php` with configurable intervals (up to
  5-minute checks)
- **Retry**: failed deliveries are queued for automatic retry

---

## 5. ActivityPub Implementation

### Architecture

Three main classes in `src/Protocol/ActivityPub/`:

| Class | Role |
|-------|------|
| **Receiver** | HTTP Signature verification, activity validation, JSON decoding |
| **Processor** | Activity type handling (Create, Update, Delete, Like, Announce) |
| **Transmitter** | JSON-LD generation for outbound activities |

Delivery: `Worker/Notifier` calculates recipients by protocol, spawning
`APDelivery` workers for ActivityPub contacts.

### Supported Features

- Follow/unfollow accounts
- Public and non-public messaging
- Posting, commenting, liking, unliking, deletion
- Bidirectional comment distribution (thread-based and per-posting models)
- Thread completion (prevents conversation fragmentation)
- Failed delivery retry queuing
- Sends Follow for root post IDs to request inclusion in receiver collections

### Known Limitations

- No native direct messages via ActivityPub (workaround: non-public post
  restricted to single recipient)
- No account migration between nodes via ActivityPub

### Mastodon-Compatible API

Extensive coverage:

- **Accounts**: verify_credentials, follow/unfollow/block/unblock/mute/unmute,
  followers, following, relationships, search
- **Statuses**: create/get/delete, favourite/unfavourite, reblog/unreblog,
  bookmark, pin/unpin, context
- **Timelines**: home, public, tag, list, direct
- **Notifications**: list, get, clear, dismiss
- **Other**: conversations, lists, media, search v1/v2, instance info,
  follow requests, emojis, directory, polls, push subscriptions

**Not implemented**: profile updates via API, familiar followers, trending,
poll voting, streaming, admin functions, domain blocks

Compatible clients: Tusky, Fedilab, Sengi, Twidere, AndStatus, Bitlbee,
Raccoon for Friendica.

---

## 6. Cross-Network Connectivity

### Built-in (no addon needed)

| Network | Protocol |
|---------|----------|
| Mastodon, Pleroma, Pixelfed, PeerTube, Lemmy, Kbin, Misskey | ActivityPub |
| Diaspora, Hubzilla, Socialhome | Diaspora protocol |
| Other Friendica nodes | DFRN |
| Email | IMAP4rev1 / ESMTP (bidirectional) |
| Any website/blog | RSS/Atom feed import |

### Addon Connectors (bidirectional)

| Network | Notes |
|---------|-------|
| **Bluesky** | No API key needed; bidirectional since v2023.12 |
| **pump.io** | Posting, relaying, reading |
| **GNU Social** | Via statusnet addon |

### Addon Connectors (post-only)

Tumblr, WordPress (XMLRPC), LiveJournal, Dreamwidth, InsaneJournal,
Libertree, Blogger, Buffer

### Deprecated

- **Twitter** — removed due to API changes under Musk
- **Facebook/Google+** — removed when APIs shut down

---

## 7. Privacy and Access Control

Friendica's privacy model is significantly more granular than most Fediverse
platforms:

- **Posts default to private** (configurable by admin to default public)
- **Access Control Lists (ACLs)** on every post via lock icon UI
- **Circles** (formerly Groups) for organizing contacts into permission sets
- **Per-post overrides**: select specific individuals or Circles to
  allow/deny
- **Multiple profiles**: different profiles for different audiences (family,
  friends, public)
- Anonymous profile viewing can be disabled
- Post deletion triggers removal notifications to all recipients
- Content expiration with automated removal from remote Friendica servers

### Cross-Network Limitation

Privacy only fully works **within Friendica's native protocols**. Posts
shared via ActivityPub or other protocols lose fine-grained ACL enforcement
— the receiving server controls display. Private photo sharing only works
reliably between Friendica members.

**Once published, post permissions CANNOT be changed.**

---

## 8. Content Model

### Post Capabilities

| Feature | Details |
|---------|---------|
| Maximum length | 200,000 characters |
| Markup | BBCode (bold, italic, headings h1-h6, code blocks, tables, spoilers, lists) |
| Media | Images (with alt text, dimensions), video (YouTube/Vimeo/generic), audio, OEmbed |
| Albums | Photo albums with tagging and per-album privacy |
| Events | Date, time, location, RSVP |
| Forums | Public and private, federated |
| Polls | Limited (not supported via Diaspora protocol) |
| Notes | Private notebook (notes to self) |
| Maps | By address, coordinates, or post location |
| Abstract/summary | Per-network overrides (e.g., `[abstract=twit]` for Twitter-length) |

### Object Types

Friendica represents posts as ActivityPub `Note` objects when federating
via ActivityPub. Internally, content is stored in BBCode and converted to
HTML or ActivityPub JSON as needed for each protocol.

---

## 9. Database Schema

**97 tables**, utf8mb4 charset. Schema version tracked by
`DB_UPDATE_VERSION`.

### Hub-and-Spoke Content Model

| Table | Purpose |
|-------|---------|
| `item-uri` | URI registry for deduplication |
| `post` | Protocol-agnostic metadata (author-id, owner-id, created) |
| `post-user` | Per-user states (starred, hidden, visibility) |
| `post-content` | Body text |
| `post-media` | Attachments with MIME types |
| `post-thread` / `post-thread-user` | Thread structure |
| `post-history` | Edit history |
| `post-delivery` / `post-delivery-data` | Delivery tracking |
| `post-tag` / `post-category` | Tags and categories |
| `post-question` / `post-question-option` | Polls |
| `delayed-post` | Scheduled posts |

A single post can be visible to multiple users with different permission
levels without duplicating content — the `post-user` table stores per-user
state separately from `post-content`.

### Contact Tables

| Table | Purpose |
|-------|---------|
| `contact` | Both local and remote actors |
| `apcontact` | ActivityPub-specific contact data |
| `fcontact` | Diaspora-specific contact data |
| `contact-relation` | Relationship graph |
| `user-contact` | Per-user contact settings |

### Relationship Constants

`NOTHING=0`, `FOLLOWER=1`, `SHARING=2`, `FRIEND=3`, `SELF=4`

### Server/Federation Tables

`gserver` (known servers), `endpoint` (AP endpoints), `inbox-status`
(AP inbox tracking), `diaspora-interaction` (signed Diaspora interactions)

---

## 10. Architecture

### 8-Layer Model

1. **Client Layer** — browsers, mobile apps (Raccoon, Fedilab), third-party
   clients via Mastodon API
2. **Frontend Layer** — theme system (frio/vier/quattro), JavaScript,
   localization
3. **Application Layer** — Router with 600+ routes
   (`static/routes.config.php`), modules, API endpoints
4. **Business Logic Layer** — Model classes: `Item`, `Contact`, `User`
5. **Content Processing Layer** — BBCode formatting, media processing, URL
   parsing
6. **Federation Layer** — `Friendica\Protocol\ActivityPub`,
   `Friendica\Protocol\Diaspora`, `Friendica\Protocol\DFRN`
7. **Data Layer** — Database abstraction (`DBA`), schema management
   (`DBStructure`)
8. **Background Processing** — Worker queue with priority levels

### Worker Queue

| Priority | Value |
|----------|-------|
| CRITICAL | 10 |
| HIGH | 20 |
| MEDIUM | 30 |
| LOW | 40 |
| NEGLIGIBLE | 50 |

Tasks enqueued via `Worker::add()` into `workerqueue` table. Default 10
parallel instances. `Worker/Notifier` routes deliveries to protocol-specific
workers (`APDelivery`, `Delivery`).

### Namespaces

`Friendica\Module`, `Friendica\Model`, `Friendica\Protocol`,
`Friendica\Worker`, `Friendica\Core`, `Friendica\Database`, `Friendica\Util`

### Dependency Injection

Dice DI container. Services accessed via static `DI` class: `DI::dba()`,
`DI::config()`, `DI::logger()`, `DI::session()`, `DI::baseUrl()`,
`DI::l10n()`.

---

## 11. Addon/Plugin System

Hook-based architecture with 100+ hooks. Addons live in `addon/` directory,
each in its own subdirectory.

### Required Functions

```php
function <addon>_install() {
    \Friendica\Core\Hook::register($hookname, $file, $function);
}
function <addon>_uninstall() { }
```

### Callback Signature

```php
function <addon>_<hookname>(App $a, &$b) { }
```

`$a` is the Friendica App class; `$b` is hook-specific data passed by
reference.

### Major Hook Categories

| Category | Hooks |
|----------|-------|
| Content | `post_local`, `post_local_end`, `post_remote`, `display_item`, `prepare_body` |
| Auth | `authenticate`, `logged_in`, `register_post` |
| Profile | `profile_post`, `profile_edit`, `profile_sidebar` |
| Contacts | `follow`, `unfollow`, `revoke_follow`, `block`, `unblock` |
| Settings | `addon_settings`, `connector_settings` |
| System | `init_1`, `load_config`, `route_collection` |
| Federation | `probe_detect`, `item_by_link` |

### Module Intercept

Addons can act as full page modules by defining:

```php
function <addon>_module() {}      // signals module capability
function <addon>_content(App $a) {} // returns HTML
```

### Notable Addons

- **Cross-posting**: bluesky, tumblr, diaspora, discourse, wppost,
  ljpost, dwpost
- **Storage**: s3_storage, webdav_storage
- **Auth**: ldapauth, saml, keycloakpassword
- **Privacy**: securemail (GPG-encrypted notifications)
- **Filters**: advancedcontentfilter, langfilter, nsfw, superblock

---

## 12. Installation and Deployment

### Methods

1. **Git clone**: `git clone -b stable` + `composer install --no-dev` +
   web installer
2. **CLI**: `bin/console autoinstall` with config file or env vars
3. **Docker**: `docker pull friendica` (official image)
4. **YunoHost**: app package available

### Critical Requirements

- Cron every 5-10 minutes: `bin/worker.php` (or daemon mode)
- HTTPS/TLS mandatory
- Must be at top-level domain or subdomain (not directory path) for
  Diaspora federation
- Domain **cannot be changed** after installation

### Scaling

- Nginx preferred over Apache (~2x capacity)
- Database tuning via mysqltuner.pl
- PHP-FPM for faster processing
- Configurable worker queue parallelism (default 10)
- Extended poller intervals (30-60 min) for large instances

---

## 13. Federation Interoperability

### Friendica as Protocol Bridge

Friendica's unique value is connecting users across protocol boundaries:

```
Mastodon user ←─ActivityPub─→ Friendica ←─Diaspora protocol─→ Diaspora pod
                                  ↕
                              DFRN native
                                  ↕
                           Bluesky (addon)
                                  ↕
                         RSS/Atom/Email/Tumblr
```

A Friendica user can follow a Mastodon account, a Diaspora contact, a
Bluesky account, and an RSS feed — all in the same timeline.

### vs. Mastodon

| Feature | Friendica | Mastodon |
|---------|-----------|----------|
| Post length | 200,000 chars | 500 chars |
| Protocols | AP + Diaspora + DFRN + addons | AP only |
| Contact groups | Circles with ACLs | Lists (no ACLs) |
| RSS reader | Built-in | No |
| Photo albums | Yes | No |
| Events/calendar | Yes | No |
| Quote posts | Yes (early pioneer) | Added later |
| Forums | Yes (public + private) | No |
| BBCode | Yes | No |

### Known Issues

- Friendica's rich content (BBCode formatting, long posts) may be
  truncated or stripped by Mastodon's HTML filtering
- Privacy ACLs only enforceable within Friendica — remote servers
  control their own display
- Private photos only reliable between Friendica members
- Comment counts may be inaccurate on remote instances due to
  incomplete thread federation

---

## 14. Governance and Community

- **No corporation, foundation, or board** — informal volunteer governance
- **Core maintainers**: Tobias Diekershoff (FSFE), Michael Vogel
- **Communication**: Friendica forums (dogfooding the platform)
- **Code**: GitHub + self-hosted Gitea at git.friendi.ca
- **Mascot**: Flaxy O'Hare (rabbit, CC0)
- **Release cadence**: quarterly stable releases, year.month versioning
- **No direct donations accepted** — covers server costs only

---

## 15. Common Implementation Mistakes

- **Assuming Friendica only speaks ActivityPub**: Friendica may deliver
  content via DFRN or Diaspora protocol depending on the contact type —
  inspect the contact's protocol, not just the server software
- **Not handling long posts**: Friendica posts can be up to 200,000
  characters — truncate gracefully rather than rejecting
- **Ignoring BBCode in content**: Friendica's native format is BBCode,
  converted to HTML for ActivityPub — the HTML may contain richer
  formatting than typical Mastodon posts
- **Expecting Mastodon API parity**: Friendica's Mastodon API has gaps
  (no streaming, no admin API, no poll voting) — test against a real
  Friendica instance
- **Not supporting the `Application` instance actor**: Friendica uses an
  instance-level actor for some federation tasks — verify keys from
  `Application` actors, not just `Person`
- **Dropping unknown properties**: Friendica posts may include properties
  from DFRN or Diaspora context — ignore unknown properties rather than
  rejecting the entire object
- **Assuming public-by-default**: Friendica defaults to private posts
  (admin-configurable) — a Friendica instance may send fewer public
  posts than expected
