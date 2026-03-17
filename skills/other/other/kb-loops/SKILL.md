---
name: kb-loops
description: >
  Background knowledge about Loops, the federated short-form video sharing
  platform (TikTok/Vine alternative for the Fediverse). Covers the key
  federation design decision of using Note objects with video attachments
  instead of Video objects for maximum cross-platform compatibility, the
  instance actor and shared inbox implementation, HTTP Signatures with
  SHA-256 digests, WebFinger discovery, the graph-walking comment
  validator (rejects top-level Notes, creates Comment and CommentReply
  objects), cross-platform interactions (follow, comment, like, Announce
  across Mastodon/Pixelfed/PeerTube), the tech stack (Laravel/PHP,
  Vue 3, Tailwind, Expo/React Native mobile), features (vertical swipe
  feed, For You algorithm, duets, 3-minute videos, playlists, threaded
  comments), the relationship to Pixelfed and creator Daniel Supernault,
  federation beta status, and comparison with PeerTube (Note vs Video
  object types, short-form vs long-form). Load when the user asks about
  Loops; how short-form video federates in the Fediverse; why Loops
  uses Note instead of Video objects; how to federate with Loops
  instances; the Fediverse TikTok alternative; how video content works
  in ActivityPub with Note attachments; Loops federation protocol
  details; or comparing Loops with PeerTube.
user-invocable: false
---

# Loops — Complete Reference

## Overview

Loops is a federated, open-source short-form video sharing platform —
the Fediverse equivalent of TikTok/Vine. Its tagline is "Short videos.
Your community. Your rules." Created by **Daniel Supernault** (aka
Dansup), the Canadian developer also behind **Pixelfed** (the Fediverse
Instagram alternative). Branded as "Loops by Pixelfed," it is a separate
platform under the Pixelfed project umbrella.

Built on **Laravel (PHP), Vue 3, and Tailwind CSS** with a custom
ActivityPub implementation. Licensed AGPL-3.0. ActivityPub federation
entered beta on October 14, 2025. As of March 2026, the latest release
is v1.0.0-beta.10.

---

## 1. Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | PHP / Laravel |
| Frontend | Vue 3 + TypeScript |
| CSS | Tailwind CSS |
| Build tool | Vite |
| Mobile app | React Native (Expo) |
| Deployment | Docker / Docker Compose |
| CDN | Fastly (Fast Forward program) |
| License | AGPL-3.0 |

### Repositories

| Repository | URL |
|-----------|-----|
| Server | https://github.com/joinloops/loops-server |
| Mobile app | https://github.com/joinloops/loops-expo |
| API docs | https://docs.joinloops.org/ |

---

## 2. The Key Design Decision: Note, Not Video

The most important technical decision in Loops' federation: **Loops uses
`Note` objects with video attachments instead of `Video` objects** for
maximum cross-platform compatibility.

From Daniel Supernault:

> "The fediverse is optimized for notes. Mastodon, Pleroma, Misskey —
> they all handle notes beautifully. By wrapping video content as notes
> with video attachments, loops federate seamlessly across the entire
> fediverse without requiring special handling."

> "This pragmatic approach means loops show up properly everywhere, not
> just on platforms that specifically understand video objects. It's about
> meeting the fediverse where it is, not where we wish it would be."

### What Gets Federated

When a loop is posted, the federation sends:

- A `Note` object with rich video attachments
- Multiple video encodings for different devices (where supported)
- Generated thumbnails and preview images (where supported)
- Captions and content warnings
- All standard interaction capabilities (Like, Announce, Reply)

### Why Not Video Objects?

PeerTube uses `Video` objects, which provide richer video-specific
metadata. However, many Fediverse platforms (especially microblogging
platforms like Mastodon, Misskey, Pleroma) either don't handle `Video`
objects at all or display them with degraded UX. By using `Note` — the
type every Fediverse platform handles natively — Loops videos appear
correctly in timelines across the entire Fediverse without special
handling.

### Comparison

| Approach | Used by | Pros | Cons |
|----------|---------|------|------|
| `Note` + video attachment | Loops | Universal compatibility; shows up in all timelines | Less video-specific metadata |
| `Video` object | PeerTube | Rich metadata (duration, resolution, chapters) | Many platforms ignore or poorly display `Video` type |

---

## 3. Federation Implementation

### Instance Actor and Shared Inbox

Every Loops instance has a server-level actor that handles:
- Server-to-server authentication
- Instance metadata exchange
- Account deletions and relay subscriptions

A **shared inbox** is implemented for optimized delivery — remote
instances send activities once to the shared inbox rather than per-
follower, reducing network overhead as instances grow.

### HTTP Signatures

Request signing with:
- SHA-256 digests
- Date header parsing (handling format variations across servers)
- Non-standard port number handling
- Every federated request is cryptographically signed

### WebFinger Discovery

Standard WebFinger discovery for both individual users and the instance
actor, enabling seamless follow operations across the Fediverse.

### Federation-Aware Comments

Loops implements a **graph-walking validator** that traces reply chains:

- **Top-level `Note` objects from remote servers are rejected** — Loops
  is for videos only, not microblog posts
- Replies to videos create `Comment` objects
- Replies to comments become `CommentReply` objects with correct parent
  relationships
- This enables nested conversations that work across platforms

This validator is important for interoperability: when a Mastodon user
replies to a loop, the reply is accepted as a Comment. But if a Mastodon
user tries to create a top-level post that arrives at a Loops instance,
it is rejected.

### What Works in Federation Beta

| Feature | Status |
|---------|--------|
| Follow any ActivityPub user | Working |
| Be followed from Mastodon/Pixelfed/etc | Working |
| Cross-platform comments | Working |
| Cross-platform likes | Working |
| Share/Announce to followers | Working |
| Federated notifications | Working |
| Multi-instance video distribution | Working |
| Account migration with follower transfer | Planned |

### Federation Configuration

Federation is **opt-in** during beta for self-hosted instances:
- Enable in instance settings
- HTTPS required
- Configure domain properly
- Allocate storage for remote media caching
- Documented in FEDERATION.md in the repository

---

## 4. Features

### Available Now

- Vertical swipe short-video feed
- **Following feed** (chronological) and **For You feed** (algorithmic,
  powered by engagement/hashtags/social graph)
- Videos up to **3 minutes** (originally 30 seconds, extended over time)
- In-app camera with multi-lens switching and caption editor
- **Duets** (collaborative video creation)
- Nested/threaded comments with @mentions across the Fediverse
- Like, share, boost/repost
- Hashtag browsing and trending topics
- Profile and video search
- Pinned videos (up to 3)
- Playlists & Collections
- Favourites (private bookmarks)
- Sound library
- Full ActivityPub federation (beta)
- Native iOS and Android apps
- Admin dashboard
- Public API with OpenAPI documentation

### Roadmap (2026)

| Quarter | Features |
|---------|----------|
| Q1 | Advanced moderation, push notifications, multi-account, stitches |
| Q2 | Creator analytics, AR filters, collaborative moderation, accessibility |
| Q3 | Embeddable player, account migration, live streaming, video editor |
| Q4 | Challenges, monetization options |

---

## 5. Loops vs PeerTube

| Aspect | Loops | PeerTube |
|--------|-------|----------|
| Focus | Short-form vertical video (TikTok/Vine) | Long-form video (YouTube) |
| Video length | Up to 3 minutes | No practical limit |
| UI | Mobile-first vertical swipe | Web-first video library |
| Discovery | For You algorithmic feed + hashtags | Federated search, channels |
| AP object type | `Note` with video attachments | `Video` |
| Tech stack | Laravel (PHP) + Vue.js | Node.js + Angular |
| P2P delivery | No | Yes (WebRTC) |
| Live streaming | Planned Q3 2026 | Yes |
| Maturity | Beta (v1.0.0-beta.10) | Stable (v6+, since 2018) |

Loops and PeerTube are complementary, not competing — they target
fundamentally different video use cases. PeerTube is for long-form
content hosting (channels, playlists, educational videos). Loops is for
short-form social video (trends, creativity, casual sharing).

---

## 6. Interoperability Notes for Implementers

1. **Loops videos arrive as `Note` objects** — if your software handles
   `Note` with video attachments, Loops content will display correctly in
   timelines. No special `Video` type handling needed.

2. **Replying to a Loop** — send a standard `Note` reply with `inReplyTo`
   pointing to the loop's `Note` ID. Loops will accept it as a Comment.

3. **Top-level Notes are rejected** — Loops only accepts video content
   for top-level posts. If a Mastodon user mentions a Loops user in a
   standalone post (not a reply), Loops will not ingest it as a post.

4. **Like and Announce work normally** — standard `Like` and `Announce`
   activities targeting a loop's `Note` ID work as expected.

5. **Video stays on origin server** — when a loop federates, remote
   instances receive the `Note` metadata but the video file is served
   from the original Loops instance. This reduces storage requirements
   for remote instances but depends on the origin server's availability.

6. **Multiple encodings** — Loops may include multiple video file
   attachments (different resolutions/encodings) in the `Note` object.
   Consumers should select the appropriate encoding for their display
   context.

---

## 7. API

Loops provides a full public REST API (OpenAPI spec v1.0.0):

- OAuth authentication with 2FA support
- Video upload and management
- Duets
- Playlists and collections
- Explore/trending endpoints
- For You feed with impression tracking
- Full-text search
- Privacy controls
- 25+ language support
- AI content detection flags
- Alt text and content sensitivity marking

Documentation: https://docs.joinloops.org/

---

## 8. Known Considerations

- **Beta federation**: ActivityPub support is in beta (since October
  2025). Some edge cases with remote platforms may still need work.
- **Opt-in federation**: Self-hosted instances must explicitly enable
  federation in settings during the beta period.
- **Video bandwidth**: Short-form video demands significant bandwidth
  and storage. Instance operators should plan for CDN/object storage
  costs. Loops benefits from Fastly Fast Forward sponsorship for its
  premiere instance.
- **No monetization yet**: Creator monetization features are planned for
  Q4 2026. This may affect creator adoption in the near term.
- **Recommendation algorithm limitations**: The "For You" feed uses
  engagement, hashtags, and social graph signals, but federated privacy
  constraints limit the data available compared to centralized platforms
  like TikTok.
