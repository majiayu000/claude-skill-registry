---
name: kb-mastodon
description: >
  Background knowledge about Mastodon, the dominant federated microblogging
  platform and de facto reference implementation for ActivityPub social
  networking. Covers Mastodon's JSON-LD @context structure (three-element
  array: activitystreams, security/v1, inline object defining toot:
  http://joinmastodon.org/ns# with Emoji/discoverable/featured/featuredTags/
  blurhash/votersCount/indexable/memorial/suspended/attributionDomains,
  schema: http://schema.org# with PropertyValue/value, as: with
  Hashtag/manuallyApprovesFollowers/movedTo/sensitive), content-type and
  Accept header requirements (application/activity+json or application/
  ld+json with ActivityStreams profile, content negotiation for actor
  discovery), HTTP signature requirements (RSA-SHA256, Digest header
  mandatory for POST, signed headers include request-target/host/date/
  digest), authorized fetch / secure mode (AUTHORIZED_FETCH env var,
  requires signatures on GET requests too, breaks unsigned federation),
  supported object types (Note and Question first-class, Article/Page/
  Image/Audio/Video/Event converted with content or name + URL appended),
  poll implementation (Question wrapped in Create, oneOf for single-choice
  anyOf for multiple, options as Note with name and replies.totalItems,
  votes as Create of Note matching option name, endTime/closed/votersCount),
  edit/Update handling (since 3.5.0, requires updated timestamp, sends
  Update activity with full object, edit history not yet federated),
  Announce/boost behavior (object field is URI string, receiver fetches
  original, shares collection on statuses), direct message addressing
  (no as:Public, no follower collection, only actor URIs in to, all
  must be Mentioned in tag), visibility calculation (public=as:Public
  in to, unlisted=as:Public in cc, private=followers in to/cc without
  as:Public, limited=actors not all Mentioned, direct=all actors
  Mentioned), custom emoji (tag type Emoji with name shortcode and
  icon Image), HTML sanitization (allowed: a/p/br/span/b/i/em/strong/
  blockquote/pre/code/ul/ol/li/div/audio/video/img/source, strips all
  other elements and attributes, allowed classes: mention/hashtag/
  invisible/ellipsis/h-*/p-*/u-*/dt-*/e-*), character limits (500 default
  for composing but accepts and displays longer remote posts with
  truncation/Read More, hard limit 1MB JSON-LD serialization), thread
  fetching (up to 5 same-server replies fetched on discovery, inReplyTo
  recursive fetch, replies not forwarded upstream, 4.4+ fetch-all-replies
  feature, 4.5 enables by default with AsyncRefresh API), NodeInfo 2.0
  at /.well-known/nodeinfo pointing to /nodeinfo/2.0, Mastodon REST API
  compatibility layer (implemented by Pleroma/Akkoma/GoToSocial/Firefish/
  Sharkey/Pixelfed), recent version changes (4.3: attributionDomains/
  fediverse:creator, like/boost counts in AP objects, summary as HTML;
  4.4: quote post display via FEP-044f, experimental RFC9421 HTTP
  Message Signatures, FASP support; 4.5: quote post authoring, fetch-
  all-replies enabled by default, RFC9421 verification standard,
  AsyncRefresh API), size limits (username 2048, display name 2048
  truncated, profile note 20kB, profile fields 50 max, field name/value
  2047, poll options 500, emoji shortcode 2048, media descriptions
  1500), and common federation gotchas (schema.org incorrect base URI,
  reply propagation gaps, counter inconsistencies across instances,
  Block activity sent server-to-server despite spec being client-only,
  Article type poorly supported, Linked-Data Signatures for public
  posts disabled in secure mode). Load when the user asks about
  Mastodon federation; implementing a Mastodon-compatible ActivityPub
  server; Mastodon's JSON-LD context or toot namespace; how Mastodon
  handles incoming ActivityPub objects; Mastodon content-type or Accept
  headers; Mastodon HTTP signatures or authorized fetch; how Mastodon
  polls work in ActivityPub; how Mastodon edits/Updates federate; how
  Mastodon boosts/Announces work; Mastodon direct messages in
  ActivityPub; Mastodon visibility levels; Mastodon HTML sanitization;
  Mastodon character limits; Mastodon thread fetching; Mastodon
  NodeInfo; the Mastodon client API compatibility; Mastodon custom
  emoji federation; Mastodon 4.3/4.4/4.5 changes; or common gotchas
  when federating with Mastodon.
user-invocable: false
---

# Mastodon -- Complete Federation Reference

## Overview

Mastodon is a free, open-source, decentralized microblogging platform --
the dominant software in the Fediverse and the de facto reference
implementation for ActivityPub social networking. Created by Eugen Rochko
(Gargron) in 2016. Built in Ruby on Rails with a PostgreSQL database,
Redis for caching/queues, and a React.js frontend. Licensed AGPL-3.0.

Mastodon federates via ActivityPub (server-to-server). Because of its
dominance, Mastodon's specific implementation choices have become de facto
standards that other Fediverse software must accommodate, even when those
choices deviate from or extend the ActivityPub specification.

---

## 1. JSON-LD @context Structure

Mastodon's `@context` is a **three-element JSON array**:

```json
[
  "https://www.w3.org/ns/activitystreams",
  "https://w3id.org/security/v1",
  {
    "manuallyApprovesFollowers": "as:manuallyApprovesFollowers",
    "toot": "http://joinmastodon.org/ns#",
    "featured": { "@id": "toot:featured", "@type": "@id" },
    "featuredTags": { "@id": "toot:featuredTags", "@type": "@id" },
    "alsoKnownAs": { "@id": "as:alsoKnownAs", "@type": "@id" },
    "movedTo": { "@id": "as:movedTo", "@type": "@id" },
    "schema": "http://schema.org#",
    "PropertyValue": "schema:PropertyValue",
    "value": "schema:value",
    "discoverable": "toot:discoverable",
    "suspended": "toot:suspended",
    "memorial": "toot:memorial",
    "indexable": "toot:indexable",
    "attributionDomains": {
      "@id": "toot:attributionDomains",
      "@type": "@id"
    },
    "Hashtag": "as:Hashtag",
    "Emoji": "toot:Emoji",
    "sensitive": "as:sensitive",
    "votersCount": "toot:votersCount",
    "blurhash": "toot:blurhash",
    "focalPoint": { "@container": "@list", "@id": "toot:focalPoint" }
  }
]
```

### Namespace Definitions

| Prefix   | URI                                | Notes |
|----------|------------------------------------|-------|
| `as:`    | `https://www.w3.org/ns/activitystreams#` | Standard ActivityStreams |
| `toot:`  | `http://joinmastodon.org/ns#`      | Mastodon-specific extensions |
| `schema:`| `http://schema.org#`               | **BUG**: should be `https://schema.org/` -- causes issues with strict JSON-LD processors |
| `sec:`   | From `https://w3id.org/security/v1`| Public keys, signatures |

### Key `toot:` Namespace Terms

- `toot:Emoji` -- custom emoji type
- `toot:featured` -- pinned posts collection (`@id`, `@type: @id`)
- `toot:featuredTags` -- featured hashtags collection
- `toot:discoverable` -- boolean, whether to list in directory
- `toot:indexable` -- boolean, consent for search indexing (FEP-5feb)
- `toot:suspended` -- boolean, account suspension status
- `toot:memorial` -- boolean, memorial/deceased account
- `toot:votersCount` -- poll total voter count
- `toot:blurhash` -- BlurHash string for media placeholders
- `toot:focalPoint` -- `[x, y]` coordinates for image cropping
- `toot:attributionDomains` -- domains allowed to use `fediverse:creator` (since 4.3)

### Key `as:` Extended Terms

- `as:Hashtag` -- hashtag tag type
- `as:manuallyApprovesFollowers` -- locked account flag
- `as:movedTo` -- account migration target
- `as:sensitive` -- content warning flag
- `as:alsoKnownAs` -- account aliases for migration

### Key `schema:` Terms

- `schema:PropertyValue` -- profile metadata field type
- `schema:value` -- profile metadata field value

**Gotcha**: The `schema:` prefix maps to `http://schema.org#` (with hash,
no HTTPS). This is technically incorrect per schema.org's own context
(`https://schema.org/`). Strict JSON-LD processors may fail to resolve
these terms. Implementations should accept both forms.

---

## 2. Content-Type and Accept Headers

### For Fetching ActivityPub Resources (GET)

Send the `Accept` header as:
```
Accept: application/activity+json, application/ld+json
```

Mastodon uses HTTP content negotiation. If the `Accept` header does not
include an ActivityPub media type, Mastodon serves the HTML profile page
instead of the JSON-LD representation.

Both of these are valid and equivalent:
- `application/activity+json`
- `application/ld+json; profile="https://www.w3.org/ns/activitystreams"`

### For Sending Activities (POST to inbox)

Set the `Content-Type` header to:
```
Content-Type: application/ld+json; profile="https://www.w3.org/ns/activitystreams"
```

Or equivalently:
```
Content-Type: application/activity+json
```

**Gotcha**: Some HTTP libraries default to `application/json` or
`application/x-www-form-urlencoded`. Always set Content-Type explicitly.
Send the request body as a raw JSON string, not form-encoded.

---

## 3. HTTP Signatures

Mastodon **requires** HTTP Signatures on all incoming POST requests and
optionally on GET requests (when authorized fetch is enabled).

### Algorithm

RSA-SHA256 (RSASSA-PKCS1-v1_5 with SHA-256) using the actor's RSA
private key. The corresponding public key is published in the actor
document under `publicKey`.

### Signature Header Format

```
Signature: keyId="https://example.com/users/alice#main-key",
           headers="(request-target) host date digest",
           signature="<base64-encoded-signature>"
```

### Required Signed Headers

**For GET requests** (when authorized fetch is enabled):
- `(request-target)` -- the HTTP method and path (e.g., `get /users/bob`)
- `host` -- target hostname
- `date` -- RFC 2616 date (must be within clock skew tolerance)

**For POST requests** (always required):
- `(request-target)`
- `host`
- `date`
- `digest` -- **mandatory** for POST; Mastodon will reject POSTs without
  a signed Digest header

### Digest Header

For POST requests, compute the SHA-256 hash of the request body:

```
Digest: SHA-256=<base64-encoded-sha256-hash-of-body>
```

The `digest` header name must appear in the `headers` parameter of the
Signature header.

### Key ID Format

The `keyId` is typically `{actor_uri}#main-key`. Mastodon dereferences
this to fetch the actor document, extracts `publicKey.publicKeyPem`, and
verifies the signature.

---

## 4. Authorized Fetch (Secure Mode)

Enabled by setting `AUTHORIZED_FETCH=true` (or `LIMITED_FEDERATION_MODE=true`)
in the Mastodon environment.

### What Changes

- **All GET requests** to ActivityPub representations of public posts and
  profiles require HTTP signatures (normally these are anonymous)
- **Linked-Data Signatures** are no longer generated for public posts
- Suspended/blocked servers cannot fetch public content because they must
  identify themselves via signature
- Server-level and user-level blocks become more effective

### Limitations

- Uses significantly more server resources (signature verification on every
  request)
- Causes compatibility problems with older software that does not sign GET
  requests
- Does not prevent determined adversaries -- a bad actor can set up a new
  instance to bypass blocks
- Authorized fetch is **circumventable** by design; it is a friction
  mechanism, not a security boundary

### Limited Federation Mode

`LIMITED_FEDERATION_MODE=true` is a superset of authorized fetch. It
additionally restricts federation to **manually approved servers only**.
Administrators must explicitly allowlist each domain.

---

## 5. Supported Object Types

### First-Class Types

| Type       | Mastodon Representation |
|------------|------------------------|
| `Note`     | Regular status/toot    |
| `Question` | Poll status            |

### Converted Types (Best-Effort)

These types are accepted but **not given full treatment**:

| Type    | Handling |
|---------|----------|
| `Article` | Uses `content` (or `name` if no content) as status text; appends `url`; `summary` becomes CW; `icon` becomes thumbnail |
| `Page`    | Same conversion logic as Article |
| `Image`   | Same conversion logic |
| `Audio`   | Same conversion logic |
| `Video`   | Same conversion logic |
| `Event`   | Same conversion logic |

**Critical gotcha**: `Article` objects are **not rendered with their full
HTML content** the way `Note` objects are. The content is used to generate
status text, but formatting, structure, and richness are lost. Many
platforms (WordPress, WriteFreely, Ghost) send `Article` objects that
display poorly on Mastodon. Some platforms have switched to sending `Note`
instead for better Mastodon compatibility.

---

## 6. Poll Implementation (Question/Answer)

Mastodon represents polls as `Question` objects (used as an Object type,
**not** as an IntransitiveActivity). Polls are wrapped in `Create`
activities like normal statuses.

### Poll Structure

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://example.com/users/alice/statuses/12345",
  "type": "Question",
  "content": "<p>What is your favorite color?</p>",
  "published": "2024-01-01T00:00:00Z",
  "endTime": "2024-01-02T00:00:00Z",
  "oneOf": [
    {
      "type": "Note",
      "name": "Red",
      "replies": { "type": "Collection", "totalItems": 42 }
    },
    {
      "type": "Note",
      "name": "Blue",
      "replies": { "type": "Collection", "totalItems": 58 }
    }
  ],
  "toot:votersCount": 100
}
```

### Key Properties

- `oneOf` -- array of options for **single-choice** polls
- `anyOf` -- array of options for **multiple-choice** polls
- Each option: `type: "Note"`, `name: "<option text>"`, `replies.totalItems: <vote count>`
- Options have **no `id`** property
- `endTime` -- ISO 8601 timestamp when voting closes
- `closed` -- ISO 8601 timestamp when voting actually closed (may differ from endTime)
- `votersCount` (`toot:votersCount`) -- total number of unique voters

### Voting Mechanism

Votes are sent as `Create` activities where the object is a `Note` with:
- `name` exactly matching the poll option's `name`
- `inReplyTo` pointing to the Question's `id`
- `to` addressing the poll author

For **multiple-choice polls**, Mastodon sends **separate `Create` activities**
for each selected option from the same voter.

### Poll Updates

Poll results are updated via `Update` activities on the `Question` object.
Remote instances can re-fetch the poll to get current vote counts.

---

## 7. Edit / Update Activities

Mastodon has supported editing statuses since **version 3.5.0** (March 2022).

### How It Works

- An `Update` activity is sent with the full updated object as `object`
- The `updated` timestamp on the object signals that this is an edit
  (not a first-time creation)
- Receiving instances check: if a status with that `id` already exists
  locally, the `Update` triggers an edit; otherwise it is treated as a
  new status
- Mastodon's `FetchRemoteStatusService` automatically converts a `Create`
  to an `Update` when the status already exists in the local database

### Edit History

- Edit history is stored locally and viewable on the originating instance
- Edit history is **not federated** in the ActivityPub representation
  (as of early 2026, there is an open issue requesting this: #23292)
- The `StatusEdit` entity in the REST API exposes edit history

### Limitations

- Remote instances only see the latest version of a post
- There is no standard way to fetch previous versions via ActivityPub

---

## 8. Announce (Boost) Activities

### Outgoing Announces

When a user boosts a post, Mastodon sends:

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://example.com/users/alice/statuses/67890/activity",
  "type": "Announce",
  "actor": "https://example.com/users/alice",
  "published": "2024-01-01T12:00:00Z",
  "to": ["https://www.w3.org/ns/activitystreams#Public"],
  "cc": ["https://example.com/users/alice/followers",
          "https://remote.example/users/bob"],
  "object": "https://remote.example/users/bob/statuses/11111"
}
```

**The `object` field is a URI string**, not an inline object. The
receiving instance must dereference (fetch) the URI to get the full
status content.

### Incoming Announces

Mastodon accepts both:
- `object` as a URI string (standard pattern) -- fetches the original
- `object` as an inline full object -- uses the embedded data

When processing an incoming `Announce`, Mastodon uses
`ActivityPub::FetchRemoteStatusService` to retrieve the original status
if needed.

### Boost Counters

Statuses expose a `shares` collection:
- `shares.totalItems` -- number of boosts received
- Since Mastodon 4.3, like and boost counts are exposed in ActivityPub
  Note objects
- Since Mastodon 4.4, favorite and boost counts match remote server
  values when available

**Gotcha**: Boost/like counts are inherently inconsistent across instances.
Only the originating instance knows the true total. Other instances only
see counts from their own users plus what has been federated to them.

---

## 9. Direct Messages (Mentions-Only Visibility)

Mastodon does **not** have a dedicated direct message ActivityPub type.
"Direct messages" are simply `Note` objects with restricted addressing.

### Addressing Rules for Direct Messages

```json
{
  "type": "Note",
  "to": ["https://remote.example/users/bob"],
  "cc": [],
  "tag": [
    {
      "type": "Mention",
      "href": "https://remote.example/users/bob",
      "name": "@bob@remote.example"
    }
  ]
}
```

Requirements:
- **No** `as:Public` (`https://www.w3.org/ns/activitystreams#Public`) in
  `to` or `cc`
- **No** follower collection URI in `to` or `cc`
- **Only** specific actor URIs in `to`
- **All** actors in `to`/`cc` must have a corresponding `Mention` tag

### Visibility Level Calculation

Mastodon calculates visibility from addressing, **not** from an explicit
visibility field:

| Visibility   | `to`                    | `cc`                    | Mention tags |
|-------------|-------------------------|-------------------------|--------------|
| **public**  | `as:Public`             | followers collection    | --           |
| **unlisted**| followers collection    | `as:Public`             | --           |
| **private** | followers collection    | (no `as:Public`)        | --           |
| **limited** | specific actors         | --                      | Not all actors are Mentioned |
| **direct**  | specific actors         | --                      | All actors are Mentioned |

**Gotcha**: The distinction between `limited` and `direct` depends on
whether all addressed actors have corresponding `Mention` tags. If you
address actors in `to` without `Mention` tags, Mastodon treats it as
`limited` (not `direct`).

---

## 10. Custom Emoji Federation

Custom emoji are represented as `Emoji` tags on objects:

```json
{
  "type": "Note",
  "content": "<p>Hello :coolcat:</p>",
  "tag": [
    {
      "id": "https://example.com/emojis/coolcat",
      "type": "Emoji",
      "name": ":coolcat:",
      "icon": {
        "type": "Image",
        "mediaType": "image/png",
        "url": "https://example.com/system/custom_emojis/images/coolcat.png"
      }
    }
  ]
}
```

### Properties

- `type`: `"Emoji"` (from `toot:Emoji`)
- `name`: shortcode including colons (e.g., `:coolcat:`)
- `icon.type`: `"Image"`
- `icon.mediaType`: MIME type (e.g., `image/png`)
- `icon.url`: direct URL to the emoji image

### Behavior

- Mastodon scans `name`, `summary`, and `content` for shortcode substrings
  and links them to the emoji image
- Custom emoji from remote instances are visible in federated posts
- Administrators can see and copy emoji from federated instances
- Emoji **updates and deletions** do not reliably federate
- Custom emoji may not render in display names and bios in all contexts

---

## 11. HTML Sanitization

Mastodon sanitizes all incoming HTML to protect API client developers
from unexpected markup.

### Allowed Elements

```
a, abbr, audio, b, blockquote, br, code, div, em, i, img, li, ol, p,
pre, source, span, strong, ul, video
```

### Allowed CSS Classes

```
mention, hashtag, ellipsis, invisible, h-*, p-*, u-*, dt-*, e-*
```

(Microformats2 classes are preserved.)

### Behavior

- Unsupported elements are **stripped** (content preserved, tags removed)
- Unsupported attributes are **stripped**
- Links (`<a>`) are kept only if the protocol is supported (http, https);
  other protocols are converted to plain text
- Mentions and hashtags are represented as `<a>` tags with `class="mention"`
  or `class="hashtag"`

**Gotcha**: If your platform sends rich HTML (tables, headings, definition
lists, details/summary, etc.), Mastodon will strip all of it. Only the
plain text content inside those elements survives. Design your content to
degrade gracefully.

---

## 12. Character Limits

### Composing Limit

Mastodon's default composing limit is **500 characters**. This is enforced
client-side and in the REST API. Instance administrators can modify this
by changing source code, but it is not a simple configuration option.

### Receiving Limit

Mastodon **accepts and displays** posts longer than 500 characters from
remote instances. The ActivityPub protocol has no character limit.

- Long posts are displayed with automatic truncation and a **"Read More"**
  link in the web UI
- Most Mastodon-compatible mobile clients also truncate with "Read More"
- The post content is stored in full -- no data is lost

### Hard Size Limits (FEDERATION.md)

| Property                  | Limit     | Behavior if exceeded |
|--------------------------|-----------|---------------------|
| JSON-LD serialization     | 1 MB      | Activity rejected   |
| Username                  | 2048 chars| Actor rejected      |
| Display name              | 2048 chars| Truncated           |
| Profile note (bio)        | 20 kB     | Truncated           |
| Profile fields            | 50 fields | List truncated      |
| Field name/value          | 2047 chars| Truncated           |
| Poll options              | 500       | List truncated      |
| Custom emoji shortcode    | 2048 chars| Rejected            |
| Media descriptions (alt)  | 1500 chars| Truncated           |
| Account aliases           | 256       | List truncated      |
| Attribution domains       | 256       | List truncated      |

---

## 13. Thread Fetching and Reply Dereferencing

### inReplyTo Resolution

When Mastodon encounters a status with an `inReplyTo` pointing to an
unknown URI, it **fetches the parent status** from the remote server.
This works recursively up the reply chain to build the thread context.

### Same-Server Reply Fetching

Upon discovering a remote status, Mastodon fetches **up to 5 replies from
the same server** as the original post. This helps fill in thread context
but is limited in scope.

### Reply Distribution Problem

Replies are sent to the parent post's instance but are **not forwarded
through follower networks** automatically. This creates a fundamental
gap:

- If A posts, B replies, and C replies to B: A's instance may never see
  C's reply unless C explicitly mentions A
- Each instance has an incomplete view of any conversation
- Reply counts, like counts, and boost counts differ across instances

### Fetch All Replies (4.4+)

Mastodon 4.4 introduced a "fetch all replies" feature (disabled by
default). When triggered:
- Paginates through the first layer of `replies` collections from the
  source server
- Collects reply URIs
- Launches background workers to fetch them

### Mastodon 4.5 Improvements

- Fetch all replies is **enabled by default**
- Automatically checks for missing replies on page load and every 15 min
- New **AsyncRefresh API**: the `/api/v1/statuses/:id/context` endpoint
  returns a `Mastodon-Async-Refresh` HTTP header when background fetch
  jobs are pending, allowing clients to poll for completion

---

## 14. NodeInfo Implementation

### Discovery Endpoint

```
GET /.well-known/nodeinfo
```

Response:
```json
{
  "links": [
    {
      "rel": "http://nodeinfo.diaspora.software/ns/schema/2.0",
      "href": "https://mastodon.example/nodeinfo/2.0"
    }
  ]
}
```

### NodeInfo 2.0 Response

```
GET /nodeinfo/2.0
```

```json
{
  "version": "2.0",
  "software": {
    "name": "mastodon",
    "version": "4.5.0"
  },
  "protocols": ["activitypub"],
  "services": {
    "outbound": [],
    "inbound": []
  },
  "usage": {
    "users": {
      "total": 12345,
      "activeMonth": 5678,
      "activeHalfyear": 9012
    },
    "localPosts": 678901
  },
  "openRegistrations": true,
  "metadata": {
    "nodeName": "Example Mastodon",
    "nodeDescription": "A Mastodon instance"
  }
}
```

**Note**: `software.name` is always lowercase `"mastodon"`. Use this to
detect Mastodon instances programmatically.

---

## 15. Mastodon REST API Compatibility Layer

Mastodon's REST API has become a de facto standard. Many Fediverse
platforms implement it (partially or fully) to allow Mastodon client
apps to work with them:

| Platform         | Mastodon API Support |
|-----------------|---------------------|
| **Pleroma**     | Near-complete, with Pleroma-specific extensions |
| **Akkoma**      | Near-complete (Pleroma fork), with additional extensions |
| **GoToSocial**  | Well-implemented, works with major Mastodon apps |
| **Firefish**    | Partial support (now discontinued) |
| **Sharkey**     | Partial support (Misskey fork) |
| **Pixelfed**    | Partial support for photo-related endpoints |
| **Friendica**   | Partial support |

### API Discovery Challenge

Different platforms support different subsets of the Mastodon API and add
their own extensions. There is no standardized way to discover which
endpoints a server supports. Client libraries like **Megalodon** abstract
over platform differences.

---

## 16. Recent Version Changes (4.x Series)

### Mastodon 4.3 (October 2024)

Federation-relevant changes:
- **`attributionDomains`**: new `toot:` property for `fediverse:creator`
  author attribution on external articles
- **Like and boost counts** now exposed in ActivityPub Note objects
- **`summary` field** in non-Note objects treated as HTML (was plain text)
- **Grouped notifications** in REST API
- **Numeric actor IDs**: new users get numeric-based ActivityPub URIs
  (preparation for future account renaming)

### Mastodon 4.4 (July 2025)

Federation-relevant changes:
- **Quote post display**: incoming quote posts per FEP-044f rendered in
  web UI; new `quote` attribute on Status entity
- **RFC 9421 HTTP Message Signatures**: experimental support for
  verification of incoming signatures (behind feature flag)
- **FASP (Fediverse Auxiliary Service Providers)**: initial support for
  shared decentralized services (behind feature flag)
- **Fetch all replies**: new backend feature to fetch missing remote
  replies (disabled by default)
- **Remote counts**: favorite/boost counts match remote server values

### Mastodon 4.5 (November 2025)

Federation-relevant changes:
- **Quote post authoring**: users can compose quote posts; `quoted_status_id`
  API parameter; new quote states (`blocked_account`, `blocked_domain`,
  `muted_account`)
- **Fetch all replies enabled by default**: automatic background fetching
  of missing conversation participants
- **AsyncRefresh API**: `Mastodon-Async-Refresh` HTTP header for async
  background job status on context endpoint
- **RFC 9421 standard**: experimental flag removed; incoming HTTP Message
  Signatures now verified by default

### Supported FEPs

- **FEP-67ff**: FEDERATION.md
- **FEP-f1d5**: NodeInfo in Fediverse Software
- **FEP-8fcf**: Followers collection synchronization
- **FEP-5feb**: Search indexing consent (`toot:indexable`)
- **FEP-044f**: Consent-respecting quote posts
- **FEP-3b86**: Activity Intents (Follow, Announce, Like, Object intents)

---

## 17. Common Federation Gotchas

### JSON-LD Issues

1. **schema.org base URI bug**: Mastodon maps `schema:` to
   `http://schema.org#` instead of `https://schema.org/`. Strict JSON-LD
   processors will fail. Workaround: accept both forms.

2. **Context order matters**: Some implementations are sensitive to the
   order of items in the `@context` array. Match Mastodon's order when
   possible.

3. **Unknown properties ignored**: Mastodon silently ignores JSON-LD
   properties it does not understand. Your custom extensions will not
   cause errors but will not be processed.

### Reply Propagation

4. **Incomplete threads**: Mastodon instances have fundamentally
   incomplete views of conversations. Replies are not forwarded upstream.
   Only the instance where a post originated has the full picture.

5. **Counter inconsistency**: Like counts, boost counts, and reply counts
   differ across instances. Never assume these numbers are authoritative
   on any instance except the originating one.

### Content Handling

6. **Article objects degraded**: Mastodon does not render `Article`
   objects with full fidelity. Long-form content platforms should consider
   sending `Note` for Mastodon compatibility or accept that their content
   will be reduced to plain text + URL.

7. **HTML stripped aggressively**: Tables, headings, definition lists,
   details/summary, horizontal rules, and other block-level elements are
   stripped. Only a minimal subset of HTML survives.

8. **Hashtag/mention encoding**: When a mention is present, hashtags in
   the Note activity can sometimes be replaced with mentions during
   federation delivery (the object itself retains correct tags when
   fetched directly).

### Protocol Behavior

9. **Block activity sent S2S**: Mastodon sends `Block` activities
   server-to-server when a user blocks a remote account, even though the
   ActivityPub spec defines Block for client-to-server only. Your
   implementation should handle incoming Block activities gracefully.

10. **Linked-Data Signatures disabled in secure mode**: When
    `AUTHORIZED_FETCH=true`, Mastodon stops generating LD-Signatures on
    public posts. Implementations that rely on LD-Signatures for relay
    forwarding will break.

11. **Clock skew sensitivity**: HTTP signature verification checks the
    `Date` header. If your server's clock is significantly off, signatures
    will be rejected.

### Performance

12. **Link preview DDoS effect**: Every instance that receives a post
    with a URL will independently fetch the link preview (OpenGraph data).
    A post that goes viral can cause hundreds of concurrent requests to
    the linked website.

13. **Inbox forwarding**: Mastodon does **not** forward activities through
    inboxes the way the AP spec describes. Replies to your posts from
    third-party servers may never reach followers who are not on the
    replier's server.

---

## 18. WebFinger

Mastodon requires WebFinger for user discovery. The endpoint:

```
GET https://example.com/.well-known/webfinger?resource=acct:alice@example.com
```

Must return a JRD document with at minimum:
- `subject`: the `acct:` URI
- `links`: array including a link with `rel: "self"`,
  `type: "application/activity+json"`, and `href` pointing to the actor URI

Mastodon uses `username@domain` as the canonical user identifier. The
WebFinger lookup is fundamental to Mastodon's database design: every
remote actor is stored with a username and domain pair resolved via
WebFinger.

---

## 19. Actor Structure

Mastodon actors are `Person` type (or `Application` for the instance
actor, `Service` for bot/automated accounts). Key properties:

- `preferredUsername` -- the local username (before the @)
- `name` -- display name
- `summary` -- bio (HTML)
- `url` -- profile page URL (HTML)
- `inbox` -- ActivityPub inbox endpoint
- `outbox` -- ActivityPub outbox endpoint
- `followers` -- followers collection URI
- `following` -- following collection URI
- `featured` (`toot:featured`) -- pinned posts collection
- `featuredTags` (`toot:featuredTags`) -- featured hashtags
- `publicKey` -- RSA public key for HTTP signature verification
- `endpoints.sharedInbox` -- shared inbox for efficient delivery
- `icon` -- avatar image
- `image` -- header/banner image
- `attachment` -- array of `schema:PropertyValue` for profile fields
- `discoverable` (`toot:discoverable`) -- directory listing consent
- `indexable` (`toot:indexable`) -- search indexing consent
- `memorial` (`toot:memorial`) -- deceased account flag
- `suspended` (`toot:suspended`) -- suspension flag
- `manuallyApprovesFollowers` -- locked account
- `movedTo` -- migration target actor URI
- `alsoKnownAs` -- array of aliases (for migration verification)
- `attributionDomains` (`toot:attributionDomains`) -- fediverse:creator domains

---

## 20. Supported Activities (Inbox Processing)

| Activity   | Object Type | Mastodon Behavior |
|-----------|-------------|-------------------|
| `Create`  | `Note`      | Creates a new status |
| `Create`  | `Question`  | Creates a poll status |
| `Create`  | Other       | Best-effort conversion to status |
| `Update`  | `Note`/`Question` | Edits status (if `updated` present, since 3.5) |
| `Update`  | `Person`    | Updates remote actor profile |
| `Delete`  | `Note`      | Deletes remote status locally |
| `Delete`  | `Person`    | Removes remote actor and content |
| `Announce` | Status URI | Creates a boost |
| `Like`    | Status URI  | Creates a favorite |
| `Follow`  | Actor URI   | Sends follow request |
| `Accept`  | `Follow`    | Confirms follow relationship |
| `Reject`  | `Follow`    | Rejects follow request |
| `Undo`    | `Follow`    | Unfollows |
| `Undo`    | `Like`      | Removes favorite |
| `Undo`    | `Announce`  | Removes boost |
| `Undo`    | `Block`     | Removes block |
| `Block`   | Actor URI   | Records block (non-standard S2S use) |
| `Flag`    | Actor + objects | Reports content/user to moderators |
| `Move`    | Actor URI   | Triggers account migration |
| `Add`     | Status to `featured` | Pins a status |
| `Remove`  | Status from `featured` | Unpins a status |
