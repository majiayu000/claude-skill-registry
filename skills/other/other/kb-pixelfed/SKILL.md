---
name: kb-pixelfed
description: >
  Background knowledge about Pixelfed, the decentralized photo and video
  sharing platform. Load when the user asks about implementing a Pixelfed-
  compatible ActivityPub server, federating with Pixelfed instances,
  Pixelfed's actor model (Person actors, Application instance actor),
  Pixelfed's supported ActivityPub activities (Accept, Add, Announce,
  Create, Delete, Flag, Follow, Like, Reject, Undo, Update, View,
  Story:Reaction, Story:Reply), Pixelfed's non-standard extensions
  (capabilities object for announce/like/reply permissions, commentsEnabled
  boolean, Stories with Bearcap URIs, location geo-tagging with Place
  objects, blurhash on attachments, federated Groups via FEP-400e and
  FEP-1b12), Pixelfed's JSON-LD context namespaces (pixelfed.org/ns#,
  joinmastodon.org/ns#), Pixelfed's Mastodon API compatibility layer,
  cross-platform federation quirks (text-only posts hidden, album limits,
  Stories not federating outside Pixelfed, comment count inaccuracies),
  Pixelfed configuration environment variables (ACTIVITY_PUB, AP_REMOTE_FOLLOW,
  MAX_PHOTO_SIZE, MAX_ALBUM_LENGTH, STORIES_ENABLED, OAUTH_ENABLED),
  or Pixelfed's
  technical stack (PHP, Laravel, Vue.js, Redis). Also load when reviewing
  or writing code that needs to interoperate with Pixelfed instances or
  implement Pixelfed-specific extensions.
user-invocable: false
---

# Pixelfed — Complete Reference

## Overview

Pixelfed is a free, open-source, decentralized photo and video sharing
platform — the Fediverse's answer to Instagram. Created by Daniel
Supernault ("dansup") and launched December 25, 2018, it federates via
ActivityPub. As of mid-2025, it has approximately 900,000 registered
users across roughly 1,800 servers with 96+ million media items shared.
Licensed under AGPL-3.0.

Pixelfed **only displays posts with images or video** — text-only posts
from other Fediverse platforms are hidden. This is a fundamental design
decision, not a bug.

---

## 1. Technical Stack

| Layer | Technology |
|---|---|
| Backend language | PHP |
| Backend framework | Laravel (currently v12) |
| Database | MySQL 8.0 or PostgreSQL 13 |
| Cache / Queue | Redis |
| Queue management | Laravel Horizon |
| OAuth | Laravel Passport |
| Frontend framework | Vue.js 2.6.14 |
| Frontend state | Vuex |
| CSS | Bootstrap |
| Build | Webpack via Laravel Mix |
| Mobile | React Native (iOS + Android) |
| Storage | Local filesystem or S3/Object Storage |
| License | AGPL-3.0 |
| Runtime | PHP 8.3+ (supports 8.4, 8.5), Node.js for assets |

---

## 2. Actor Model

Pixelfed uses `Person` type actors for user accounts:

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    "https://w3id.org/security/v1",
    {"pixelfed": "http://pixelfed.org/ns#"}
  ],
  "type": "Person",
  "id": "https://pixelfed.example/users/alice",
  "preferredUsername": "alice",
  "name": "Alice",
  "summary": "<p>Bio text</p>",
  "inbox": "https://pixelfed.example/users/alice/inbox",
  "outbox": "https://pixelfed.example/users/alice/outbox",
  "following": "https://pixelfed.example/users/alice/following",
  "followers": "https://pixelfed.example/users/alice/followers",
  "manuallyApprovesFollowers": false,
  "indexable": true,
  "publicKey": {
    "id": "https://pixelfed.example/users/alice#main-key",
    "owner": "https://pixelfed.example/users/alice",
    "publicKeyPem": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
  },
  "icon": {
    "type": "Image",
    "mediaType": "image/jpeg",
    "url": "https://pixelfed.example/storage/avatars/alice.jpg"
  },
  "endpoints": {
    "sharedInbox": "https://pixelfed.example/f/inbox"
  },
  "alsoKnownAs": []
}
```

Key points:
- The shared inbox path is `/f/inbox` (not `/inbox` as with some other
  implementations)
- `manuallyApprovesFollowers` controls locked/private account behaviour
- `indexable` signals whether the account should appear in search indexes
- `alsoKnownAs` is present but account migration between servers is not
  currently supported

### Instance Actor

Pixelfed uses an instance-wide actor with `"type": "Application"` to
sign GET requests to remote instances. This is separate from the
`Person` actors used by regular accounts. The instance actor is used
for authorized fetch (secure mode) — when a remote server requires
signed GET requests, Pixelfed uses this actor's key.

---

## 3. Supported Activities

| Activity | Description |
|---|---|
| `Accept` | Approves follow requests |
| `Add` | Federates Stories (uses Bearcap URIs for access control) |
| `Announce` | Reblogs/boosts |
| `Create` | Creates Note and Question objects |
| `Delete` | Removes Person, Tombstone, and Story objects |
| `Flag` | Federated report functionality |
| `Follow` | Follow request |
| `Like` | Favorites a post |
| `Reject` | Denies follow requests |
| `Undo` | Reverses Announce, Follow, and Like |
| `Update` | Modifies Note (status) and Person (profile) |
| `View` | Story view tracking |
| `Story:Reaction` | Reaction to a Story (Pixelfed-only) |
| `Story:Reply` | Reply to a Story (Pixelfed-only) |

`Story:Reaction` and `Story:Reply` are Pixelfed-specific activity types
that are not understood by other Fediverse software.

---

## 4. Object Types and Post Structure

Pixelfed supports three object types: **Note**, **Image**, and
**Document**.

Posts are represented as `Note` objects:

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    "https://w3id.org/security/v1",
    {"pixelfed": "http://pixelfed.org/ns#"}
  ],
  "type": "Note",
  "id": "https://pixelfed.example/p/alice/123456",
  "attributedTo": "https://pixelfed.example/users/alice",
  "content": "<p>Caption text with #hashtag</p>",
  "summary": null,
  "inReplyTo": null,
  "published": "2025-06-15T12:00:00Z",
  "url": "https://pixelfed.example/p/alice/123456",
  "sensitive": false,
  "to": ["https://www.w3.org/ns/activitystreams#Public"],
  "cc": ["https://pixelfed.example/users/alice/followers"],
  "attachment": [
    {
      "type": "Image",
      "mediaType": "image/jpeg",
      "url": "https://pixelfed.example/storage/m/photo.jpg",
      "name": "Alt text description",
      "blurhash": "LEHV6nWB2yk8pyoJadR*.7kCMdnj"
    }
  ],
  "tag": [
    {
      "type": "Hashtag",
      "href": "https://pixelfed.example/discover/tags/hashtag",
      "name": "#hashtag"
    }
  ],
  "commentsEnabled": true,
  "capabilities": {
    "announce": "https://www.w3.org/ns/activitystreams#Public",
    "like": "https://www.w3.org/ns/activitystreams#Public",
    "reply": "https://www.w3.org/ns/activitystreams#Public"
  }
}
```

Key points:
- `summary` is used for content warnings (null when not set)
- `attachment` contains `Image` objects with optional `blurhash`
- Albums can have up to 20 items (some sources say 12 for photos)
- Captions support up to 2,000 characters (configurable)
- Three visibility levels: public, unlisted, followers-only

---

## 5. Pixelfed-Specific Extensions

### Capabilities

Per-post access control added to `Note` objects:

```json
"capabilities": {
  "announce": "https://www.w3.org/ns/activitystreams#Public",
  "like": "https://www.w3.org/ns/activitystreams#Public",
  "reply": null
}
```

Each capability value is either:
- `"https://www.w3.org/ns/activitystreams#Public"` — allowed for everyone
- `null` — disabled

This controls who can boost, like, or reply to a specific post. Other
Fediverse software generally ignores this extension — they will still
allow their users to interact with the post regardless of these settings.

### commentsEnabled

A boolean property on `Note` objects:

```json
"commentsEnabled": true
```

When `false`, replies are disabled on the post. Like `capabilities`,
this is enforced by Pixelfed but generally ignored by other
implementations.

### Stories

Ephemeral 24-hour content, similar to Instagram Stories:

- Federated **only between Pixelfed instances** — not visible on
  Mastodon, Pleroma, or other platforms
- Use **Bearcap URIs** for access control (recipients must present a
  token to access the content)
- Require `STORIES_ENABLED=true` in server configuration
- Support activities: `Add`, `Delete`, `View`, `Story:Reaction`,
  `Story:Reply`
- Transform to `StoryReaction` and `StoryView` internal models

### Location Geo-tagging

Posts can include a `Place` object for location data:

```json
"location": {
  "type": "Place",
  "name": "Paris, France",
  "longitude": 2.3522,
  "latitude": 48.8566,
  "country": "France"
}
```

### Blurhash

Pixelfed includes `blurhash` on image attachments for compact preview
placeholders. This uses the `toot:blurhash` property from Mastodon's
namespace (`http://joinmastodon.org/ns#`). The blurhash is a short
string that encodes a blurred preview of the image, useful for showing
a placeholder while the full image loads.

### Federated Groups

Pixelfed supports federated Groups via FEP-400e and FEP-1b12 extensions.
Group actors use `"type": "Group"` with standard inbox/outbox
collections.

---

## 6. JSON-LD Context

Pixelfed uses a multi-context approach with four namespaces:

```json
"@context": [
  "https://www.w3.org/ns/activitystreams",
  "https://w3id.org/security/v1",
  {"pixelfed": "http://pixelfed.org/ns#"},
  {"toot": "http://joinmastodon.org/ns#"}
]
```

| Namespace | Purpose |
|---|---|
| `https://www.w3.org/ns/activitystreams` | ActivityStreams 2.0 vocabulary |
| `https://w3id.org/security/v1` | W3C Security Vocabulary (publicKey) |
| `http://pixelfed.org/ns#` | Pixelfed-specific properties (capabilities, commentsEnabled) |
| `http://joinmastodon.org/ns#` | Mastodon compatibility (blurhash, indexable) |

When processing Pixelfed JSON-LD documents, unknown properties from the
`pixelfed:` and `toot:` namespaces should be ignored rather than causing
errors.

---

## 7. HTTP Signatures and WebFinger

### HTTP Signatures

- Pixelfed signs **every** POST and GET request
- All incoming POST requests **must** be signed
- GET requests **may** require signatures (configurable — this is
  "authorized fetch" or "secure mode")
- The instance `Application` actor's key is used for signing GET requests
- Individual `Person` actor keys are used for signing POST requests
  (activities from that user)

### WebFinger

Pixelfed requires each ActivityPub actor to uniquely map to an `acct:`
URI resolvable via WebFinger at `/.well-known/webfinger`. Standard
WebFinger resolution applies.

---

## 8. Collections

Three primary user collections using the `OrderedCollection` pattern:

| Collection | Path | Content |
|---|---|---|
| Following | `/users/{username}/following` | Accounts this user follows |
| Followers | `/users/{username}/followers` | Accounts following this user |
| Outbox | `/users/{username}/outbox` | User's published statuses |

`totalItems` may return `0` if the collection is hidden per user
privacy preference. This is intentional, not a bug — do not assume an
empty collection means the user has no followers/following.

---

## 9. Mastodon API Compatibility

Pixelfed implements a subset of the Mastodon REST API, allowing
Mastodon client apps to work with Pixelfed instances.

### Working endpoints

- Account endpoints (verify_credentials, update_credentials,
  relationships, search)
- Status endpoints (create, view, delete, favourite, boost)
- Timeline endpoints (home, public, hashtag)
- Notification endpoints
- OAuth 2.0 authentication (requires `OAUTH_ENABLED=true`)

### Known compatibility gaps

- **OOB OAuth redirect** (`urn:ietf:wg:oauth:2.0:oob`) is not
  supported — apps relying on this flow will fail
- **Authorization code grant type** has reported issues
- Some public API endpoints incorrectly require OAuth tokens
- Pixelfed-specific features (Stories, Collections, capabilities) are
  **not accessible** via the Mastodon API — only through Pixelfed's
  own API

---

## 10. Federation Interoperability

### Cross-platform behaviour

| Feature | Pixelfed to Mastodon | Mastodon to Pixelfed |
|---|---|---|
| Photo posts | Appear as image posts with text | Appear normally if image attached |
| Text-only posts | N/A (Pixelfed requires media) | **Not displayed** on Pixelfed |
| Album posts (>4 images) | Only first 4 images shown | N/A (Mastodon max 4) |
| Stories | Not visible | N/A |
| Boosts | Appear as boosts | Appear as boosts |
| Likes/Favourites | Federate normally | Federate normally |
| Replies | Federate, but display may be incomplete | Federate normally |
| Content warnings | Show as content warnings | Show as content warnings |

### Known federation issues

- Pixelfed does not display older posts created before federation with
  a particular instance began
- Comment counts may be inaccurate (showing N comments but not all
  visible) due to incomplete federation of reply threads
- Nested reply threading can be incomplete across platforms
- Profile photo updates sometimes fail to federate properly
- The `capabilities` extension is not respected by other platforms —
  a post with `"reply": null` can still receive replies from Mastodon
  users

---

## 11. Configuration Reference

### Federation

| Variable | Description |
|---|---|
| `ACTIVITY_PUB` | Enable/disable federation entirely |
| `AP_REMOTE_FOLLOW` | Allow/prevent remote following |

### Media

| Variable | Default | Description |
|---|---|---|
| `MAX_PHOTO_SIZE` | 15000 (KB) | Per-file size limit (15 MB) |
| `MAX_ACCOUNT_SIZE` | 1000000 (KB) | Per-user total storage (1 GB) |
| `MAX_ALBUM_LENGTH` | 4 | Items per post |
| `IMAGE_QUALITY` | 80 | JPEG quality 1-100 |
| `PF_OPTIMIZE_IMAGES` | — | Automatic image optimization |
| `PF_OPTIMIZE_VIDEOS` | — | Automatic video optimization |
| `PF_ENABLE_CLOUD` | — | S3/Object Storage support |

### Accounts

| Variable | Default | Description |
|---|---|---|
| `MAX_CAPTION_LENGTH` | 500 | Caption character limit |
| `MAX_BIO_LENGTH` | 125 | Bio character limit |
| `MAX_NAME_LENGTH` | 30 | Display name limit |
| `OPEN_REGISTRATION` | true | New account creation |
| `PF_MAX_USERS` | 1000 | User registration cap |
| `ENFORCE_EMAIL_VERIFICATION` | — | Email confirmation required |

### Features

| Variable | Default | Description |
|---|---|---|
| `STORIES_ENABLED` | false | Stories functionality |
| `OAUTH_ENABLED` | — | Third-party app authentication |
| `INSTANCE_DISCOVER_PUBLIC` | — | Public explore feature access |
| `INSTANCE_PUBLIC_HASHTAGS` | — | Anonymous hashtag feed browsing |

---

## 12. Common Implementation Mistakes

- **Ignoring the `capabilities` extension**: when federating with
  Pixelfed, be aware that `capabilities` exists — even if you choose
  not to enforce it, you should not strip it when forwarding posts
  between instances
- **Sending text-only posts to Pixelfed**: Pixelfed silently drops
  posts without media attachments — there is no error response, the
  post simply does not appear
- **Assuming Mastodon API parity**: Pixelfed's Mastodon API
  implementation has gaps (no OOB OAuth, some endpoints require tokens
  when they should not) — test against a real Pixelfed instance
- **Not handling `commentsEnabled: false`**: if your software creates
  replies, check this field before sending a reply to a Pixelfed post —
  while Pixelfed cannot prevent your server from delivering the reply,
  respecting this field is good federation citizenship
- **Expecting Stories to federate universally**: Stories only work
  between Pixelfed instances — do not implement Story support expecting
  cross-platform compatibility
- **Treating `totalItems: 0` as empty**: Pixelfed returns `0` for
  hidden collections — a followers count of 0 does not mean the account
  has no followers
- **Wrong shared inbox path**: Pixelfed uses `/f/inbox` as the shared
  inbox, not `/inbox` — always read the `endpoints.sharedInbox` value
  from the actor document rather than guessing
- **Not handling the Application instance actor**: Pixelfed uses a
  separate `Application`-type actor for GET request signing — if your
  server requires signed fetches, be prepared to resolve and verify
  keys from actors with `"type": "Application"`, not just `"Person"`
