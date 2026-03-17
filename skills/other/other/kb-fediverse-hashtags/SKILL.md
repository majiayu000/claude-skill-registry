---
name: kb-fediverse-hashtags
description: >
  Background knowledge about how hashtags work on the Fediverse, including
  at the ActivityPub wire-format level. Load when the user asks about
  implementing hashtags, detecting hashtag support in a codebase, how
  hashtag federation works, why hashtag search returns incomplete results,
  how to follow hashtags, the Hashtag type in ActivityPub, the tag property
  on Note objects, case sensitivity in hashtag handling, featured hashtags,
  hashtag relays, or any question about tags in a federated social network
  context. Also load when reviewing or writing code that processes ActivityPub
  objects and needs to handle the tag array.
user-invocable: false
---

# Fediverse Hashtags — Complete Reference

## Overview

Hashtags on the Fediverse work differently from centralised platforms. Because
there is no global index, what a user sees under a hashtag is determined by
what their *particular server* has observed — not a complete picture of the
whole network.

---

## 1. The ActivityPub Wire Format

### The `Hashtag` type

`Hashtag` is **not** a standard ActivityStreams 2.0 type. It was introduced by
Mastodon and placed in the `as:` namespace (`https://www.w3.org/ns/activitystreams#Hashtag`),
even though it was never formally added to the ActivityStreams context document.
It has since been formalised in the **ActivityPub Miscellaneous Terms** extension
(`https://purl.archive.org/miscellany`), but most implementations still declare
it via the `as:` namespace for compatibility.

The `Hashtag` type is a subtype of `Link`, not of `Object`. This matters:
it should not have an `id` property in strict JSON-LD terms, though some
implementations add one anyway.

### Declaring `Hashtag` in `@context`

There are two common patterns in the wild:

**Pattern A — inline in `@context` (Mastodon, Pixelfed style):**
```json
"@context": [
  "https://www.w3.org/ns/activitystreams",
  {
    "Hashtag": "as:Hashtag"
  }
]
```

**Pattern B — via the Miscellany extension:**
```json
"@context": [
  "https://www.w3.org/ns/activitystreams",
  "https://purl.archive.org/miscellany"
]
```

Both resolve to the same URI. Pattern A is more common in existing
implementations. Pattern B is the more formally correct approach.

### Attaching a hashtag to a `Note`

Hashtags are expressed in the `tag` array of an object (usually a `Note`).
Each entry is a `Hashtag` object with:

- `type`: `"Hashtag"` (required)
- `href`: URL of a page listing content with this tag (required — this is
  what makes it a `Link` subtype)
- `name`: the hashtag string, conventionally including the `#` prefix

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    { "Hashtag": "as:Hashtag" }
  ],
  "id": "https://example.com/notes/1",
  "type": "Note",
  "attributedTo": "https://example.com/users/alice",
  "content": "<p>Watching the eclipse! <a href='https://example.com/tags/eclipse2024' class='mention hashtag' rel='tag'>#<span>eclipse2024</span></a></p>",
  "tag": [
    {
      "type": "Hashtag",
      "href": "https://example.com/tags/eclipse2024",
      "name": "#eclipse2024"
    }
  ]
}
```

### The `tag` array can hold multiple types

The `tag` array is shared by `Hashtag`, `Mention`, and `Emoji` entries.
Implementations must check `type` to differentiate them:

```json
"tag": [
  { "type": "Mention",  "href": "https://other.example/users/bob", "name": "@bob@other.example" },
  { "type": "Hashtag",  "href": "https://example.com/tags/cats",   "name": "#cats" },
  { "type": "Emoji",    "id":   "https://example.com/emoji/42",    "name": ":blobcat:" }
]
```

### The dual representation problem

Hashtags appear in **two places** in an ActivityPub object, and both must be
consistent:

1. **`tag` array** — the structured metadata, used by receiving servers to
   index the post under that tag
2. **`content` field** — the HTML body, where hashtags appear as `<a>` links
   with `rel="tag"` and `class="mention hashtag"`

If the `tag` array entry is missing, receiving servers may not index the post
under that hashtag at all, even if the `#word` appears visibly in the content.
If the `content` link is missing or malformed, the hashtag may not be
clickable or display correctly.

---

## 2. Case Sensitivity

Case handling is one of the most inconsistent areas of Fediverse hashtag
implementation.

**The `name` field vs. the `href` field:**
- The `href` (and the path used in URLs like `/tags/eclipse2024`) is
  typically **lowercased**
- The `name` field may preserve the original capitalisation the author typed
  (`"#Eclipse2024"`) or may be lowercased

**Mastodon's behaviour:**
- Stores tags lowercased internally
- The `name` field in the outgoing ActivityPub object reflects the *database
  canonical form*, not necessarily what the author typed
- `href` is always lowercase

**CamelCase for accessibility:**
Users are encouraged to write hashtags in CamelCase (`#DogsAtPollingStations`
rather than `#dogsatpollingstations`) because screen readers can parse
individual words from CamelCase. This is a widely-promoted Fediverse
convention, not a technical requirement.

**Interoperability implication:**
When processing incoming `Hashtag` objects, implementations should normalise
the tag name to lowercase before indexing or comparing, since `#Cats`, `#cats`,
and `#CATS` all refer to the same tag.

---

## 3. Featured Hashtags

Mastodon allows users to pin hashtags to their profile. This is implemented
as an extra `featuredTags` property on the actor object pointing to a
`Collection` of `Hashtag` objects:

```json
{
  "id": "https://mastodon.example/@alice",
  "type": "Person",
  "featuredTags": "https://mastodon.example/@alice/collections/tags"
}
```

The `featuredTags` term is defined in the Mastodon namespace:
`http://joinmastodon.org/ns#featuredTags`.

---

## 4. How Hashtag Federation Works (and Why It's Incomplete)

This is the most important and most misunderstood aspect of Fediverse hashtags.

### There is no global hashtag index

Unlike centralised platforms, no server has a complete view of all posts
under a hashtag across the entire network. A server only indexes posts it
has *received*.

A server receives a post if:
- A local user follows the author
- A local user has boosted/replied to the post (pulling it into a thread)
- The server subscribes to a relay that delivered the post
- The post was explicitly fetched (e.g., by pasting a URL into the search bar)

### Following a hashtag is a local filter

When a user on Mastodon "follows" a hashtag, it is **not** a network-level
subscription. It is a client-side filter on the server's federated timeline.
The server does not send any ActivityPub messages to announce this follow.
Posts under that hashtag only appear in the user's timeline if the server
would have received them anyway.

Following hashtags does not cause the server to go out and fetch posts from
other servers that use that hashtag. This is a common point of confusion.

### Relays expand the picture

Relays are ActivityPub actors that re-broadcast public posts from many servers
to subscribers. A server admin can subscribe to a relay to increase the
volume of posts the server receives. Some relays (like FediBuzz) allow
filtering by hashtag, so a server can subscribe to receive only posts
tagged with specific hashtags. This is an admin-level operation, not
something individual users can do.

### The RSS workaround

Most Fediverse servers expose a public RSS feed for each hashtag timeline:
```
https://{server}/tags/{tagname}.rss
```
This can be used to subscribe to a hashtag's timeline on a specific server
via any feed reader.

Some Fediverse servers instead expose a public Atom feed for each hashtag timeline:
```
https://{server}/tags/{tagname}.atom
```

---

## 5. Hashtag URLs and Tag Pages

The `href` in a `Hashtag` object points to a human-readable page showing
posts with that tag. The URL convention varies by platform:

| Platform | Tag page URL pattern |
|---|---|
| Mastodon | `/tags/{tagname}` |
| Pixelfed | `/discover/tags/{tagname}` |
| Misskey / Calckey | `/tags/{tagname}` |
| PeerTube | `/search/videos?tagsOneOf={tagname}` |
| Pleroma / Akkoma | `/tag/{tagname}` |

The `href` should always link to the originating server's tag page, not to
any other server's.

---

## 6. Hashtag as an Actor (Experimental)

The W3C ActivityPub Primer describes an experimental approach where a
`Hashtag` object is given `inbox` and `outbox` properties, making it a
followable actor. This would allow true network-level hashtag subscription
via ActivityPub's follow mechanism:

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    "https://purl.archive.org/miscellany"
  ],
  "type": "Hashtag",
  "id": "https://example.org/hashtag/cats",
  "href": "https://example.org/tags/cats",
  "name": "#cats",
  "inbox": "https://example.org/hashtag/cats/inbox",
  "outbox": "https://example.org/hashtag/cats/outbox"
}
```

This is **not widely implemented** and has known problems: `Hashtag` is a
`Link` subtype, making `id` and `inbox`/`outbox` properties unusual; and
many implementations only allow standard AS2 actor types (`Person`,
`Organization`, `Service`, etc.) to be followed.

---

## 7. Common Implementation Mistakes

- **Missing `tag` array entry**: including `#hashtag` in `content` HTML but
  omitting the structured `Hashtag` entry in `tag` — receiving servers may
  not index it
- **Wrong `href` host**: pointing `href` at a different server's tag page
  rather than the originating server's
- **Including `#` in `href`**: the `href` URL path should not contain `#`,
  which is a URL fragment character — use `/tags/cats` not `/tags/#cats`
- **Omitting `name` prefix**: some implementations send `"name": "cats"`
  without the `#` — conventions vary, but including `#` is more common and
  matches Mastodon's behaviour
- **Case mismatch**: `href` is lowercase but `name` has mixed case — this
  is acceptable but can cause confusion; be consistent
- **Not including `Hashtag` in `@context`**: sending `"type": "Hashtag"`
  without declaring it in `@context` means strict JSON-LD parsers will
  reject or ignore it

---

## 8. Summary: What a Correct Implementation Looks Like

A server that correctly implements hashtags should:

1. Parse incoming `tag` arrays, identify entries with `type: "Hashtag"`,
   and index the post under the normalised (lowercased) tag name
2. When creating a post with hashtags, populate both the `tag` array
   (structured metadata) and the `content` HTML (linked `#tag` anchors)
3. Declare `Hashtag` in the `@context` of outgoing objects
4. Expose a tag timeline page at a stable URL (typically `/tags/{name}`)
5. Set the `href` of each `Hashtag` entry to point to that tag timeline page
6. Optionally expose an RSS feed at `/tags/{name}.rss`
7. Optionally expose an Atom feed at `/tags/{name}.atom`
8. Accept incoming posts and index them under their hashtags so local users
   can search and follow those tags
