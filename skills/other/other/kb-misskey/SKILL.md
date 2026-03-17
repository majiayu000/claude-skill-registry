---
name: kb-misskey
description: >
  Background knowledge about Misskey, the Japanese-origin federated
  microblogging platform (created 2014 by syuilo). Covers Misskey's
  ActivityPub extensions (custom namespace https://misskey-hub.net/ns#
  with _misskey_content, _misskey_quote, _misskey_reaction for emoji
  reactions on Like activities, _misskey_votes, _misskey_talk for chat,
  isCat boolean, _misskey_followedMessage, _misskey_requireSigninToViewContents,
  _misskey_makeNotesFollowersOnlyBefore, _misskey_makeNotesHiddenBefore,
  _misskey_license), MFM (Misskey Flavored Markdown) proprietary markup
  with animations/colors/effects, emoji reactions as primary engagement
  mechanism (Unicode + custom emoji, federated via Like with _misskey_reaction),
  the Drive file management system, Antennas (custom filtered feeds),
  Deck UI, Channels, Pages, Clips, Plugins, Themes, Widgets, isCat mode,
  the tech stack (Node.js/TypeScript/NestJS/PostgreSQL/Redis/Vue.js 3/Vite,
  AGPL-3.0), REST API (POST-based) and WebSocket streaming API, Note
  visibility levels (public/home/followers/specified), the extensive fork
  ecosystem (Sharkey active soft fork, Cherrypick, Firefish/Calckey
  discontinued, Iceshrimp.NET C# rewrite, FoundKey EOL, Catodon
  discontinued, Meiskey), Misskey vs Mastodon comparison, and federation
  interoperability quirks. Load when the user asks about Misskey;
  implementing a Misskey-compatible ActivityPub server; Misskey's
  ActivityPub extensions and custom namespace; how emoji reactions
  federate from Misskey; the _misskey_reaction or _misskey_quote
  properties; MFM markup language; federating with Misskey instances;
  the Misskey fork ecosystem (Sharkey, Firefish, Iceshrimp, FoundKey);
  how Misskey differs from Mastodon; Misskey's Drive or Antenna features;
  or building software that interoperates with Misskey-family platforms.
user-invocable: false
---

# Misskey — Complete Reference

## Overview

Misskey is a free, open-source, decentralized microblogging platform —
a feature-rich Japanese-origin Fediverse platform that predates many
others. Created by **syuilo** (Eiji Shinoda) in **2014** as a
BBS-style forum, it adopted **ActivityPub in 2018**. The name comes
from the song "Brain Diver" by the band May'n. Licensed AGPL-3.0.

Misskey is explicitly **not a Mastodon fork** — it is "a project
completely different from Mastodon or other alike projects." Its
cultural DNA reflects Japanese social media preferences: emoji reactions
as the primary engagement mechanism (not simple likes), rich visual
formatting (MFM), integrated file management (Drive), and playful
features like `isCat` mode and the mascot Ai (藍). Community members
are called "Misskists."

As of late 2024: ~918,550 registered accounts, ~25,782 active users,
1,096+ instances. The flagship instance **misskey.io** is reportedly
the second largest instance in the entire Fediverse. MisskeyHQ exists
as a company entity, funded by donations and software licensing.

---

## 1. Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Node.js with TypeScript |
| Framework | NestJS (dependency injection) |
| Database | PostgreSQL (TypeORM) |
| Cache / Queue | Redis (ioredis) / BullMQ |
| Frontend | Vue.js 3 (Composition API, TypeScript) |
| Build tool | Vite |
| License | AGPL-3.0 |

### Resource Footprint

Small instances: ~848 MB RAM with CPU bursts. A $10/month VPS suffices
for small communities; $20/month for 15–50 users.

### Repository

https://github.com/misskey-dev/misskey

---

## 2. ActivityPub Extensions

Misskey uses the JSON-LD namespace `https://misskey-hub.net/ns#`
(prefix `misskey`). This is the most extensive set of custom ActivityPub
extensions in the Fediverse ecosystem.

### Extension Reference

| Property | On | Description |
|----------|-----|-------------|
| `_misskey_content` | Note | **Deprecated.** MFM source text (equivalent to `source` property) |
| `_misskey_summary` | Actor | Actor summary in MFM format |
| `_misskey_quote` | Note | ID of quoted note. Compatible with `fedibird:quoteUri` and `as:quoteUrl` |
| `_misskey_reaction` | Like | Emoji reaction type. Unicode emoji or `:name:` custom emoji string |
| `_misskey_votes` | Question option | Vote count (equivalent to `replies.totalItems`) |
| `_misskey_talk` | Note | Boolean `true` marks note as a chat message |
| `isCat` | Actor | Boolean — actor identifies as a cat (triggers visual effects) |
| `_misskey_followedMessage` | Actor | Custom message on follow notification (since 2024.9.0-alpha.11) |
| `_misskey_requireSigninToViewContents` | Actor | Forbids display to non-signed-in viewers |
| `_misskey_makeNotesFollowersOnlyBefore` | Actor | Restricts past notes to followers only. Value: Unix epoch ms (negative = relative) |
| `_misskey_makeNotesHiddenBefore` | Actor | Hides past notes from all except author. Same value format |
| `_misskey_license` | Emoji | License metadata. Properties: `freeText` (string or null) |

### Emoji Reactions Wire Format

Misskey's emoji reactions are the most significant interoperability
concern. When a user reacts with an emoji, Misskey sends a `Like`
activity with `_misskey_reaction` set to the emoji:

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    "https://w3id.org/security/v1",
    {
      "misskey": "https://misskey-hub.net/ns#",
      "_misskey_reaction": "misskey:_misskey_reaction"
    }
  ],
  "type": "Like",
  "id": "https://misskey.example/likes/abc123",
  "actor": "https://misskey.example/users/alice",
  "object": "https://remote.example/notes/xyz",
  "_misskey_reaction": "👍",
  "content": "👍"
}
```

For **custom emoji** reactions:

```json
{
  "type": "Like",
  "_misskey_reaction": ":blobcat:",
  "content": ":blobcat:",
  "tag": [
    {
      "type": "Emoji",
      "id": "https://misskey.example/emojis/blobcat",
      "name": ":blobcat:",
      "icon": {
        "type": "Image",
        "url": "https://misskey.example/files/blobcat.png"
      }
    }
  ]
}
```

**Interoperability:** Platforms that do not understand `_misskey_reaction`
will treat these as standard `Like` activities (favourites). Custom emoji
reactions are only visible to other Misskey-family software. The `content`
field is also set to the reaction value as a fallback.

### Quote Posts Wire Format

```json
{
  "type": "Note",
  "id": "https://misskey.example/notes/abc123",
  "content": "<p>My thoughts on this</p>",
  "_misskey_quote": "https://remote.example/notes/original",
  "quoteUrl": "https://remote.example/notes/original"
}
```

Both `_misskey_quote` and `quoteUrl` are set for compatibility. Also
recognized: `https://fedibird.com/ns#quoteUri`.

---

## 3. MFM (Misskey Flavored Markdown)

Proprietary markup language usable in notes, content warnings,
usernames, and bios. General syntax:
`$[name.attribute1,attribute2=value content]`

### Text Formatting

- Bold: `**text**`
- Small: `<small>text</small>`
- Center: `<center>text</center>`
- Quotes: `> text`
- Ruby: `$[ruby text reading]`
- Links: `[label](url)`
- Code: backticks (inline), triple backticks with language (blocks, 200+
  languages via Shiki)

### Visual Effects

| Syntax | Effect |
|--------|--------|
| `$[flip text]` | Horizontal/vertical flip |
| `$[font.serif text]` | Font change (serif, monospace, cursive, fantasy) |
| `$[blur text]` | Blur until hover |
| `$[fg.color=hex text]` | Foreground color |
| `$[bg.color=hex text]` | Background color |
| `$[border.style=solid,width=4 text]` | Border (solid, dotted, dashed, double, groove, ridge, inset, outset) |
| `$[position.x=0.8,y=0.5 text]` | Position shifting |
| `$[rotate.deg=30 text]` | Rotation |
| `$[scale.x=4,y=2 text]` | Scaling (also `$[x2]`, `$[x3]`, `$[x4]`) |

### Animations

| Syntax | Effect |
|--------|--------|
| `$[jelly text]` | Jiggles |
| `$[tada text]` | Celebration |
| `$[jump text]` | Bouncing |
| `$[bounce text]` | Elasticity |
| `$[spin text]` | Rotation (modifiers: `.left`, `.alternate`, `.x`, `.y`) |
| `$[shake text]` | Vibration |
| `$[twitch text]` | Random twitching |
| `$[rainbow text]` | Color cycling |
| `$[sparkle text]` | Shimmer |

All animations support `.speed=5s` for timing control.

**Federation note:** MFM is rendered as HTML when federating via
ActivityPub. The `_misskey_content` (deprecated) and `source` properties
carry the original MFM source. Non-Misskey platforms see plain HTML with
animations and effects stripped.

---

## 4. Note System

### Visibility Levels

| Level | Description |
|-------|-------------|
| `public` | Visible to everyone, appears on all timelines |
| `home` | Visible to everyone but only appears on home timeline |
| `followers` | Only visible to followers |
| `specified` | Only visible to specified users (direct message) |

### Features

- **Content Warning (CW):** `summary` field hides content behind a
  toggle
- **Renote:** Boost/reblog (Announce activity)
- **Quote Renote:** Boost with added commentary (`_misskey_quote`)
- **Polls:** `Question` activity type with `_misskey_votes` for counts
- **Reactions:** Full emoji reactions (see Section 2)
- **Mentions:** @-mentions across the Fediverse
- **Hashtags:** Standard `Hashtag` tag type

### Timelines

| Timeline | Content |
|----------|---------|
| Home | Notes from followed users |
| Local | All public notes from the instance |
| Social (Hybrid) | Home + Local combined |
| Global | All known public notes including remote |

---

## 5. Unique Features

### Drive

Cloud storage system for managing uploaded files. Files can be organized
into folders and **reused across multiple notes** without re-uploading.
Each file retains metadata (type, size, hash). Drive capacity is
configurable per-user by instance administrators via role policies.

### Antennas

Customizable filtered feeds that collect notes matching set conditions
(keywords, users, file attachments) in real time. Essentially continuous
background searches. Antennas exclude the user's own posts.

### Deck UI

Multi-column layout with side-by-side views for an information-dense
interface. Users can arrange timeline columns, notification panels, and
other widgets freely.

### Channels

Topic-based note collections within an instance. Similar to forums or
discussion threads organized by subject.

### Pages

Static page creation system using MFM and custom emoji, enabling users
to build content beyond notes.

### Other Features

- **Clips** — public/private categorized bookmarks
- **Plugins** — extend web client functionality via AiScript
- **Themes** — full client appearance customization
- **Widgets** — small interactive dashboard displays
- **Webhooks** — external service integration
- **Word mute / Thread mute** — content filtering
- **Charts** — server data visualization
- **Online status** — activity indicators on profile icons
- **Share form** — at `/share` path for social sharing buttons
- **Safe mode** — disables custom CSS, plugins, themes
- **Embeds** — embed notes and timelines on external websites
- **`isCat` mode** — users identify as cats with visual effects in
  supporting clients

---

## 6. API

### REST API

All endpoints use HTTP POST (not GET for reads):

```
POST /api/notes/create
POST /api/notes/show
POST /api/users/show
POST /api/following/create
```

Authentication via access tokens. SDK: `misskey-js` (TypeScript).

### Streaming API

WebSocket-based with channel multiplexing:

```json
{
  "type": "connect",
  "body": {
    "channel": "homeTimeline",
    "id": "arbitrary-unique-id"
  }
}
```

Available channels: `globalTimeline`, `homeTimeline`, `hybridTimeline`,
`localTimeline`, `main`.

Multiple channels can be multiplexed on a single WebSocket connection
using different IDs.

---

## 7. Fork Ecosystem

Misskey has the most extensive fork tree in the Fediverse. All forks
federate with each other and the broader Fediverse.

### Active Forks

| Fork | Type | Key Differentiators |
|------|------|-------------------|
| **Sharkey** | Soft fork (tracks upstream) | Federated note editing with history, Mastodon-compatible API + OAuth2, multi-platform import (Mastodon/Pleroma/Firefish/Twitter/Instagram/Facebook), GDPR data export, "Bubble" timeline, Argon2 hashing, multiple translation services |
| **Cherrypick** | Soft fork | Compatible with Misskey client ecosystem |
| **Meiskey** | v11 fork | Based on older Misskey v11 |

### Discontinued / EOL Forks

| Fork | Status | Notes |
|------|--------|-------|
| **Firefish** (was Calckey) | Discontinued 2024 | Added recommended timeline, account migration, mobile-optimized UI. Lead developer became absent |
| **Iceshrimp** | Transitioning | JS version: security patches only. **Iceshrimp.NET**: complete C# rewrite (beta), Mastodon API support |
| **FoundKey** | End of Life | Hard fork of v12, goal was removing bloat |
| **Catodon** | Discontinued Nov 2025 | Community-driven fork of Iceshrimp, created in reaction to Firefish governance failures |

### Fork Relationship

```
Misskey (syuilo, 2014–)
├── Sharkey (soft fork, ACTIVE)
├── Cherrypick (soft fork, ACTIVE)
├── Meiskey (v11 fork, ACTIVE)
├── FoundKey (v12 hard fork, EOL)
└── Calckey (2022) → Firefish (2023, DISCONTINUED)
    ├── Iceshrimp → Iceshrimp.NET (C# rewrite)
    └── Catodon (DISCONTINUED)
```

**Pattern:** Forks emerge from (a) feature gaps upstream won't fill,
(b) governance/communication issues, or (c) architectural changes
(Iceshrimp.NET's language rewrite).

---

## 8. Misskey vs Mastodon

| Aspect | Misskey | Mastodon |
|--------|---------|----------|
| Origin | Japan (2014) | Germany (2016) |
| Character limit | Configurable per instance | 500 default |
| Reactions | Full emoji reactions (custom + Unicode) | Favourites only |
| File management | Built-in Drive | No persistent storage |
| Markup | MFM (animations, colors, effects) | Limited Markdown |
| Channels | Topic-based communities | No |
| Antennas | Custom filtered feeds | No equivalent |
| Resource usage | Lighter than Mastodon | Heavier |
| Mobile apps | Limited (PWA, third-party) | Official iOS/Android + many third-party |
| Post editing | Not in core (Sharkey has it) | Supported |
| User base | ~918k (mostly Japanese) | ~7.6M total |

---

## 9. Interoperability Notes for Implementers

1. **Emoji reactions arrive as `Like` activities** — check for
   `_misskey_reaction` to distinguish a specific emoji reaction from a
   generic favourite. If absent, treat as a standard Like. The `content`
   field also contains the reaction value.

2. **Custom emoji in reactions** — when `_misskey_reaction` contains a
   `:name:` string, the `tag` array includes an `Emoji` object with
   the image URL. Display the custom emoji image if available, fall back
   to treating it as a Like.

3. **Quote posts** — Misskey sends `_misskey_quote` and `quoteUrl` on
   Note objects. Also check for `fedibird:quoteUri` (Fedibird/Mastodon
   compatibility). Display as an embedded quote if your platform supports
   it.

4. **MFM content** — notes from Misskey contain HTML in `content` (with
   MFM effects stripped) and optionally MFM source in the `source`
   property. Use the HTML for display; the MFM source is only useful if
   you want to re-render with a MFM parser (library: `mfm-js`).

5. **`isCat` property on actors** — a boolean extension. Misskey-family
   clients show cat ears and modify text display for cat-mode users.
   Safe to ignore but do not strip when forwarding actor documents.

6. **Chat messages** — notes with `_misskey_talk: true` are Misskey chat
   messages. They federate as normal Notes to non-Misskey platforms.
   Display as regular posts if your platform has no chat feature.

7. **All API endpoints use POST** — unlike Mastodon's REST conventions,
   Misskey uses POST for everything including reads. If implementing a
   Misskey-compatible API, every endpoint must accept POST.

8. **Visibility level "home"** — Misskey has a fourth visibility level
   (`home`) where notes are visible to everyone but excluded from the
   local and global timelines. This maps to ActivityPub `to: followers,
   cc: Public` (the inverse of Mastodon's "unlisted"). Handle carefully
   when federating.

9. **Poll vote counts** — Misskey includes `_misskey_votes` on poll
   options. This is equivalent to `replies.totalItems` but may be more
   reliably present. Prefer `_misskey_votes` when available.

10. **Note content restrictions** — the `_misskey_makeNotesFollowersOnlyBefore`
    and `_misskey_makeNotesHiddenBefore` properties on actors signal that
    historical content has access restrictions. Respect these when
    fetching older notes from Misskey actors.

---

## 10. Known Considerations

- **No post editing** in core Misskey — users must delete and redraft.
  The Sharkey fork adds federated note editing with version history.
- **Cannot follow hashtags** — use Antennas (keyword-filtered feeds)
  instead.
- **No official mobile apps** — third-party options include SocialHub
  (iOS) and Milktea (Android). The web client supports PWA.
- **Antennas exclude personal posts** from their results.
- **Mute functionality gaps** regarding mentions.
- **No MRF equivalent** for regex-based content filtering (unlike
  Pleroma/Akkoma).
- **November 2025 announcement** about potentially replacing ActivityPub
  with "Misskey's own low-overhead federation system" — details unclear,
  impact on interoperability unknown.
- **Geographic registration restrictions** on misskey.io — initially
  blocked Europeans (GDPR concerns), later restricted to Japanese users,
  Korea allowed since February 2026.
- **Recent security fixes** — CVE-2026-28431, CVE-2026-28432,
  CVE-2026-28433 patched in version 2026.3.1.
