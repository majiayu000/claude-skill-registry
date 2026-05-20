---
name: kb-peertube
description: >
  Background knowledge about PeerTube, the decentralized video streaming
  platform. Load when the user asks about implementing a PeerTube-
  compatible ActivityPub server, federating with PeerTube instances,
  PeerTube's two-tier actor model (Person actors own Group channel
  actors, Application instance actor), PeerTube's attributedTo
  requirement (videos must reference a Group actor which references an
  owning Person actor), PeerTube's supported ActivityPub activities
  (Accept, Announce, ApproveReply via FEP-5624, Create, Delete, Dislike,
  Flag, Follow, Like, Reject, Undo, Update, View), PeerTube's object
  types (Video with live streaming and comment policy extensions, Note
  for comments, CacheFile for video redundancy/mirroring, Playlist,
  PlaylistElement, WatchAction), PeerTube's JSON-LD context namespaces
  (joinpeertube.org/ns#, schema.org, join-lemmy.org/ns#), PeerTube's
  Video object extensions (isLiveBroadcast, liveSaveReplay, permanentLive,
  latencyMode, commentsPolicy, canReply, downloadEnabled, sensitive,
  waitTranscoding, state, embedUrl), the CacheFile redundancy system
  (WebSeed injection, Create{CacheFile}, Undo{CacheFile}), PeerTube's
  Dislike activity (non-standard in the Fediverse), cross-platform
  federation with Mastodon (comments as replies, favourites as thumbs up,
  asymmetrical instance following), PeerTube's P2P video delivery (HLS
  with WebRTC), live streaming (RTMP/RTMPS ingestion, HLS output,
  permanent streams, replay saving), remote runners for transcoding,
  the plugin system, or PeerTube's technical stack (TypeScript, Node.js,
  Express, PostgreSQL, Redis, Angular, FFmpeg). Also load when reviewing
  or writing code that needs to interoperate with PeerTube instances,
  implement PeerTube's channel model, handle PeerTube Video objects, or
  process CacheFile activities.
user-invocable: false
---

# PeerTube — Complete Reference

## Overview

PeerTube is a free, open-source, decentralized video streaming platform
— the Fediverse's alternative to YouTube. Created by Chocobozzz and
supported by the French non-profit Framasoft since October 2017, it
federates via ActivityPub. As of October 2025, it has approximately
1,906 active instances, 815,000 registered users, and 1.56 million
hosted videos. Licensed under AGPL-3.0.

PeerTube federations are **asymmetrical** — one instance can follow
another to display their videos without the other having to reciprocate.
This is fundamentally different from Mastodon's symmetrical user-follow
model.

---

## 1. Technical Stack

| Layer | Technology |
|---|---|
| Backend language | TypeScript (Node.js) |
| Backend framework | Express |
| Database | PostgreSQL 12+ (with `pg_trgm` and `unaccent` extensions) |
| Cache / Queue | Redis (BullMQ for job queues) |
| ORM | Sequelize |
| Video processing | FFmpeg (LTS 4.3+) |
| OAuth | Built-in OAuth 2.0 |
| Web server | Nginx (official configs provided) |
| Package manager | pnpm |
| Frontend framework | Angular (TypeScript) |
| Playback | VideoJS, hls.js, P2P Media Loader |
| Frontend build | Webpack |
| Frontend CSS | SASS / Bootstrap |
| Mobile | Official app (iOS + Android, December 2024) |
| License | AGPL-3.0 |
| Runtime | Node.js LTS 20.19+ (excl. v21) or v22.12+ (excl. v23) |

### Server Components

- **REST API** — handles client requests and video operations
- **RTMP server** — accepts live streaming input (port 1935/TCP,
  1936/TCP for RTMPS)
- **ActivityPub implementation** — federation between instances
- **Socket.io server** — real-time client notifications
- **Task scheduler** — processes transcoding and ActivityPub delivery
  jobs via BullMQ

---

## 2. Actor Model

PeerTube uses a **two-tier actor model** that is central to how it
federates video content:

- **Person** — represents user accounts
- **Group** — represents video channels, owned by Person actors
- **Application** — platform-level instance actor for federation and
  anonymous activities

A single Person can own multiple Group (channel) actors.

### Person Actor (Account)

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    "https://w3id.org/security/v1",
    {"pt": "https://joinpeertube.org/ns#"}
  ],
  "type": "Person",
  "id": "https://peertube.example/accounts/alice",
  "preferredUsername": "alice",
  "name": "Alice",
  "summary": "<p>Bio text</p>",
  "inbox": "https://peertube.example/accounts/alice/inbox",
  "outbox": "https://peertube.example/accounts/alice/outbox",
  "following": "https://peertube.example/accounts/alice/following",
  "followers": "https://peertube.example/accounts/alice/followers",
  "publicKey": {
    "id": "https://peertube.example/accounts/alice#main-key",
    "owner": "https://peertube.example/accounts/alice",
    "publicKeyPem": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
  },
  "endpoints": {
    "sharedInbox": "https://peertube.example/inbox"
  }
}
```

### Group Actor (Video Channel)

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    "https://w3id.org/security/v1",
    {"pt": "https://joinpeertube.org/ns#"}
  ],
  "type": "Group",
  "id": "https://peertube.example/video-channels/alice_channel",
  "preferredUsername": "alice_channel",
  "name": "Alice's Channel",
  "summary": "<p>Channel description</p>",
  "inbox": "https://peertube.example/video-channels/alice_channel/inbox",
  "outbox": "https://peertube.example/video-channels/alice_channel/outbox",
  "following": "https://peertube.example/video-channels/alice_channel/following",
  "followers": "https://peertube.example/video-channels/alice_channel/followers",
  "attributedTo": [
    {
      "type": "Person",
      "id": "https://peertube.example/accounts/alice"
    }
  ],
  "publicKey": {
    "id": "https://peertube.example/video-channels/alice_channel#main-key",
    "owner": "https://peertube.example/video-channels/alice_channel",
    "publicKeyPem": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
  },
  "endpoints": {
    "sharedInbox": "https://peertube.example/inbox"
  }
}
```

Key points:
- The Group actor's `attributedTo` points to the owning Person actor
- Users follow **channels** (Group), not accounts (Person) directly
- Both Person and Group actors are discoverable via WebFinger
- The shared inbox path is `/inbox`
- The Application instance actor handles platform-level federation and
  anonymous GET request signing

### Interoperability with Non-Channel Platforms

For platforms that don't have a channel concept, PeerTube recommends:
1. Simulate a Group actor representing the account, or
2. Put the Person actor as a Group actor in `attributedTo` owned by a
   global Person actor

Without a Group actor in `attributedTo`, PeerTube cannot properly
federate the video.

---

## 3. Supported Activities

| Activity | Description |
|---|---|
| `Accept` | Approves follow requests |
| `Announce` | Channel announces a video (primary video distribution mechanism) |
| `ApproveReply` | Comment moderation approval (v6.2+, implements FEP-5624) |
| `Create` | Creates Video, Note (comment), CacheFile, Playlist |
| `Delete` | Removes Video, Note, Person, Group, Playlist, CacheFile |
| `Dislike` | Thumbs down on a video (non-standard — most Fediverse software only has Like) |
| `Flag` | Federated report functionality |
| `Follow` | Subscribe to a channel or instance |
| `Like` | Thumbs up on a video |
| `Reject` | Denies follow requests |
| `Undo` | Reverses Follow, Announce, Like, Dislike, CacheFile |
| `Update` | Modifies Video, Note, Person, Group, Playlist, CacheFile |
| `View` | View count tracking |

### How Video Publishing Works

When a user uploads a video:
1. The Person actor sends a `Create{Video}` activity
2. The Group (channel) actor sends an `Announce{Video}` to its followers
3. Followers of the channel receive the video via the Announce

This two-step flow is how PeerTube distributes videos — the channel
`Announce` is the primary distribution mechanism.

---

## 4. Object Types

### Video Object

PeerTube uses `Video` as the object type (not `Note`). This is an
extended ActivityStreams object with many custom properties:

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    "https://w3id.org/security/v1",
    {"pt": "https://joinpeertube.org/ns#"},
    {"sc": "http://schema.org/"}
  ],
  "type": "Video",
  "id": "https://peertube.example/videos/watch/abc-123",
  "name": "My Video Title",
  "content": "<p>Video description</p>",
  "summary": "Content warning text",
  "sensitive": false,
  "published": "2025-06-15T12:00:00Z",
  "updated": "2025-06-15T13:00:00Z",
  "attributedTo": [
    {
      "type": "Group",
      "id": "https://peertube.example/video-channels/alice_channel"
    },
    {
      "type": "Person",
      "id": "https://peertube.example/accounts/alice"
    }
  ],
  "to": ["https://www.w3.org/ns/activitystreams#Public"],
  "cc": ["https://peertube.example/video-channels/alice_channel/followers"],
  "duration": "PT5M30S",
  "downloadEnabled": true,
  "waitTranscoding": true,
  "state": 1,
  "commentsPolicy": 0,
  "canReply": "https://www.w3.org/ns/activitystreams#Public",
  "isLiveBroadcast": false,
  "url": [
    {
      "type": "Link",
      "mediaType": "text/html",
      "href": "https://peertube.example/videos/watch/abc-123"
    },
    {
      "type": "Link",
      "mediaType": "video/mp4",
      "href": "https://peertube.example/static/streaming-playlists/hls/abc-123/master.m3u8",
      "height": 1080,
      "fps": 30
    }
  ],
  "embedUrl": "https://peertube.example/videos/embed/abc-123",
  "tag": [
    {
      "type": "Hashtag",
      "name": "#technology"
    }
  ]
}
```

Key points about the Video object:
- `attributedTo` **must** contain both a Group (channel) and a Person
  (account) — the Group entry is required for federation
- `name` is the video title (not `summary` as with Mastodon posts)
- `content` is the video description (HTML)
- `summary` is used for content warnings (like Mastodon)
- `duration` uses ISO 8601 duration format (e.g., `PT5M30S`)
- `url` is an array with multiple entries for different formats and
  resolutions (HTML page, MP4 files, HLS playlists)
- If `embedUrl` is absent, the video has embedding restrictions
- `sensitive` and a tag of `type: SensitiveTag` indicate sensitive content

### Video Object Extensions

**Live streaming properties:**
- `isLiveBroadcast` — whether this is a live stream
- `liveSaveReplay` — whether to save the replay after stream ends
- `permanentLive` — persistent stream URL that can be reused
- `latencyMode` — latency configuration for the stream
- `schedules` — array for scheduled broadcast times

**Interaction controls:**
- `commentsPolicy` — comment policy (integer value)
- `canReply` — FEP-5624; when set to the public collection, comments
  require approval via `ApproveReply`
- `downloadEnabled` — boolean controlling whether viewers can download

**State:**
- `waitTranscoding` — whether to wait for transcoding before publishing
- `state` — current video state (integer)

### Note (Comments)

Comments are represented as `Note` objects, compatible with Mastodon
and other text-based platforms:

```json
{
  "type": "Note",
  "id": "https://peertube.example/comments/456",
  "content": "<p>Great video!</p>",
  "inReplyTo": "https://peertube.example/videos/watch/abc-123",
  "attributedTo": "https://peertube.example/accounts/bob",
  "published": "2025-06-15T14:00:00Z",
  "to": ["https://www.w3.org/ns/activitystreams#Public"],
  "cc": ["https://peertube.example/accounts/alice"]
}
```

When a Mastodon user replies to a PeerTube video post, the reply
appears as a comment on the video in PeerTube.

### CacheFile (Redundancy)

A non-standard object type used for PeerTube's video mirroring system:

```json
{
  "type": "CacheFile",
  "object": "https://peertube.example/videos/watch/abc-123",
  "expires": "2025-07-15T12:00:00Z",
  "url": {
    "type": "Link",
    "mediaType": "application/x-mpegURL",
    "href": "https://mirror.example/redundancy/hls/abc-123/master.m3u8"
  }
}
```

### Other Object Types

| Type | Purpose |
|---|---|
| `Playlist` | Non-standard OrderedCollectionPage containing PlaylistElement items |
| `PlaylistElement` | Individual playlist entries with start/stop timestamps |
| `WatchAction` | Schema.org-derived object for aggregated viewer statistics |

---

## 5. Video Redundancy and CacheFile

PeerTube has a built-in redundancy system allowing instances to mirror
videos from other instances, improving resilience and bandwidth sharing.

### How Redundancy Works

1. An admin configures a redundancy strategy (cache trending videos,
   recently uploaded videos, etc.)
2. PeerTube periodically checks for new videos to duplicate
3. When a video is selected, all resolution files are imported and
   stored locally
4. A `Create{CacheFile}` ActivityPub message is sent to federated
   instances
5. The caching instance is injected as a **WebSeed** by instances that
   receive this message — viewers can now download video chunks from
   the mirror
6. When the cache is full, old videos are evicted and new ones selected

### ActivityPub Flow

- `Create{CacheFile}` — sent when a mirror instance begins caching
- `Undo{CacheFile}` — sent when the cached copy is removed

### Redundancy Strategies

- **Most viewed** — cache the most popular videos
- **Recently added** — cache the newest videos
- **Complete mirror** — use `recently-added` with view count set to 0

### Benefits

- If the origin server goes down, the video remains accessible from
  cache instances
- Servers share bandwidth for popular content
- P2P delivery benefits from additional WebSeeds

---

## 6. P2P Video Delivery

PeerTube uses **HLS with WebRTC P2P** for video playback:

- Video chunks are loaded via HTTP from the origin server and any
  mirrors (WebSeeds)
- Simultaneously, chunks are exchanged between viewers via WebRTC
  peer-to-peer connections
- Under optimal conditions (many concurrent viewers), P2P can reduce
  server bandwidth usage by 80-90%
- P2P efficacy diminishes with few concurrent viewers

Up until version 6.0.0, PeerTube also supported WebTorrent for P2P
delivery. WebTorrent was dropped in v6.0 in favour of HLS-only P2P.

### Privacy Consideration

P2P streaming exposes viewer IP addresses to other peers. This is
inherent to how WebRTC works and should be considered when deploying
PeerTube in privacy-sensitive contexts.

---

## 7. Live Streaming

PeerTube supports live streaming (introduced in v3.0, January 2021):

- **RTMP ingestion** — stream via OBS or any RTMP-compatible software
  (port 1935/TCP)
- **RTMPS** — encrypted streaming (port 1936/TCP)
- **Live transcoding** — real-time transcoding to multiple resolutions
- **HLS output** — live streams delivered via HLS with P2P WebRTC
- **Permanent live streams** — persistent stream URLs that can be reused
- **Stream scheduling** — schedule when a stream starts (v7.3+)
- **Live chat** — basic integration (v7.3+)
- **Save replay** — optionally save recordings as VOD after stream ends
- **Federation** — live streams federate to channel followers via
  ActivityPub using Video objects with `isLiveBroadcast: true`

Live transcoding is processed differently from VOD transcoding — it
happens in real-time and can be offloaded to remote runners.

---

## 8. JSON-LD Context

PeerTube uses extended contexts with multiple custom namespaces:

```json
"@context": [
  "https://www.w3.org/ns/activitystreams",
  "https://w3id.org/security/v1",
  {"pt": "https://joinpeertube.org/ns#"},
  {"sc": "http://schema.org/"}
]
```

| Namespace | Prefix | Purpose |
|---|---|---|
| `https://www.w3.org/ns/activitystreams` | — | ActivityStreams 2.0 vocabulary |
| `https://w3id.org/security/v1` | — | W3C Security Vocabulary (publicKey) |
| `https://joinpeertube.org/ns#` | `pt:` | PeerTube-specific properties (commentsPolicy, downloadEnabled, isLiveBroadcast, etc.) |
| `http://schema.org/` | `sc:` | Schema.org vocabulary (WatchAction, etc.) |
| `https://join-lemmy.org/ns#` | `lemmy:` | Lemmy compatibility (postingRestrictedToMods) |

When processing PeerTube JSON-LD documents, unknown properties from the
`pt:` namespace should be ignored rather than causing errors.

---

## 9. HTTP Signatures and WebFinger

### HTTP Signatures

PeerTube signs ActivityPub messages with **JSON Linked Data Signatures**
using the private key of the account that authored the action. HTTP
Signatures are used for server-to-server authentication.

Each actor (Person, Group, Application) has its own key pair. The
Application instance actor is used for platform-level operations.

### WebFinger

PeerTube supports WebFinger at `/.well-known/webfinger` for actor
discovery. Both Person (account) and Group (channel) actors are
discoverable:

- Account: `acct:alice@peertube.example`
- Channel: `acct:alice_channel@peertube.example`

---

## 10. Cross-Platform Federation

### Mastodon Interoperability

| Action on Mastodon | Result on PeerTube |
|---|---|
| Follow a PeerTube channel | Videos appear in Mastodon home timeline |
| Reply to a PeerTube video post | Appears as a comment on the video |
| Favourite a PeerTube video | Appears as a thumbs up (Like) |
| Boost a PeerTube video | Increases reach on federated timelines |

| Action on PeerTube | Result on Mastodon |
|---|---|
| Upload a video | Appears as a post in followers' timelines |
| Like a Mastodon comment | Standard Like activity |
| Dislike | **Not processed** — Mastodon ignores Dislike activities |

### Dislike (Non-Standard)

PeerTube supports the `Dislike` activity (thumbs down), which is
non-standard in the broader Fediverse. Most Fediverse software only
implements `Like`. Mastodon does not send or process `Dislike`
activities, so dislikes from PeerTube are silently ignored by Mastodon
and most other platforms.

### Comment Approval (FEP-5624)

PeerTube v6.2+ supports comment moderation via the `ApproveReply`
activity (implementing FEP-5624). When a video has `canReply` set to
the public collection, comments from remote instances require approval
before becoming visible. The origin PeerTube instance sends an
`ApproveReply` activity back to the commenter's instance when approved.

### Asymmetrical Instance Following

PeerTube instances can follow other PeerTube instances to display their
videos without the followed instance needing to reciprocate. This is
an admin-level operation used for content discovery.

---

## 11. Plugin System and Remote Runners

### Plugin System

- Plugins are installed via NPM in a dedicated directory
- The server `require`s the module and calls its `register()` function
- **Hooks** fire on application events (video creation, page
  initialization, transcoding, etc.)
- **Themes** operate as client-only plugins with CSS injection
- Plugins can add custom API routes, settings pages, and client-side
  components

### Remote Runners

PeerTube can offload heavy processing to remote machines:

- Remote runners register with the instance using registration tokens
- They poll the REST API for pending jobs
- Supported tasks: VOD transcoding, Studio transcoding, Live
  transcoding, Automatic transcription
- When remote runners are enabled for a task, PeerTube stops processing
  that task locally
- The runner posts the job result back to PeerTube

**Known limitation:** Server-side transcoding plugins are disabled when
remote runners are enabled for transcoding tasks.

---

## 12. Common Implementation Mistakes

- **Missing Group actor in `attributedTo`**: PeerTube requires videos
  to have an `attributedTo` field containing a Group actor — without
  it, the video cannot be properly federated. If your platform does not
  have channels, simulate a Group actor or use the Person actor in the
  Group role
- **Treating PeerTube videos as Note objects**: PeerTube uses `Video`
  as the object type, not `Note` — code that only handles `Note` will
  miss all PeerTube content. Implement handling for `type: "Video"` in
  your ActivityPub processor
- **Ignoring the two-tier `attributedTo`**: PeerTube's `attributedTo`
  contains both a Group (channel) and a Person (account) — if you only
  read the first entry, you may attribute the video to the channel
  instead of the person, or vice versa
- **Not handling `Dislike` gracefully**: PeerTube sends `Dislike`
  activities that most Fediverse software does not understand — your
  implementation should ignore unknown activity types rather than
  erroring
- **Assuming video URL is a single string**: PeerTube's `url` field is
  an array with multiple entries for different formats (HTML page, MP4
  at various resolutions, HLS playlists) — pick the appropriate entry
  based on `mediaType`
- **Not handling `CacheFile`**: if you receive a `Create{CacheFile}`
  activity, it means a remote instance is mirroring one of your videos
  — you should add the mirror as a WebSeed for that video, not reject
  the activity as unknown
- **Expecting symmetrical follows**: PeerTube instance-level follows
  are asymmetrical — following an instance does not mean they follow
  you back. Don't assume mutual federation.
- **Ignoring `embedUrl` absence**: if a PeerTube Video object lacks
  `embedUrl`, the video has embedding restrictions — do not attempt to
  generate an embed URL by guessing the pattern
- **Not supporting `ApproveReply`**: if your users comment on PeerTube
  videos with comment approval enabled, the comment won't be visible
  until the PeerTube instance sends back an `ApproveReply` — handle
  this pending state in your UI rather than showing it as posted
