---
name: kb-fediverse-liking
description: >
  Background knowledge about how the Like activity works on the Fediverse and
  in ActivityPub, including the Like/Undo{Like} flow, the `likes` and `liked`
  collections, delivery model, the Dislike type (exists in ActivityStreams but
  is unused in ActivityPub), emoji reactions (EmojiReact / FEP-c0e0 vs the
  Misskey _misskey_reaction approach), stale like counts on remote posts, and
  implementation differences across Mastodon, Misskey/Calckey/Firefish,
  Pleroma/Akkoma, and PeerTube. Load when the user asks about implementing
  likes, favourites, or reactions; why like counts are wrong on remote posts;
  how to send or receive a Like activity; how to undo a like; how emoji
  reactions differ from likes; or what EmojiReact is.
user-invocable: false
---

# Fediverse Liking — Complete Reference

## Overview

"Liking" a post is modelled by the ActivityPub `Like` activity, defined in
the ActivityStreams 2.0 vocabulary and given server-side effects in the
ActivityPub specification. It is a binary state — either an actor has liked
an object or they haven't. There is no built-in rating scale.

Platforms surface likes under different names: Mastodon calls them
**favourites** (shown with a star ★), other platforms use hearts ♥ or thumbs
up 👍. The underlying ActivityPub type is always `Like` regardless of the
UI label.

---

## 1. The Like Activity

### Minimal structure

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://alice.example/likes/abc123",
  "type": "Like",
  "actor": "https://alice.example/users/alice",
  "object": "https://bob.example/users/bob/statuses/456",
  "to": ["https://www.w3.org/ns/activitystreams#Public"],
  "cc": ["https://bob.example/users/bob"]
}
```

Key fields:
- `id` — required; a stable, dereferenceable URL on the actor's server.
  Needed so the activity can later be referenced inside an `Undo`.
- `actor` — the actor who is liking.
- `object` — the object being liked (a URL is sufficient; the full object
  need not be embedded).
- `to`/`cc` — addressing. Conventions vary; common practice is to address
  the Public collection and `cc` the author of the object.

The `Like` activity SHOULD have an `id` because it will need to be
referenced as the `object` of a future `Undo{Like}`. Omitting it makes
undoing the like ambiguous.

---

## 2. The Two Collections

### `likes` — on the object

An object (Note, Article, Video, etc.) MAY expose a `likes` property linking
to an `OrderedCollection` of `Like` activities received for that object:

```json
{
  "id": "https://bob.example/users/bob/statuses/456",
  "type": "Note",
  "likes": "https://bob.example/users/bob/statuses/456/likes",
  ...
}
```

This collection is maintained by the **author's server**. It contains one
`Like` activity per liking actor (unique by actor id). The count of items in
this collection is what platforms display as the "like count."

The collection MAY be hidden (its items not publicly enumerated) while still
exposing a `totalItems` count. This is common practice — servers often expose
the count but not the list of who liked the post.

### `liked` — on the actor

An actor MAY expose a `liked` property linking to an `OrderedCollection` of
objects that actor has liked:

```json
{
  "id": "https://alice.example/users/alice",
  "type": "Person",
  "liked": "https://alice.example/users/alice/liked",
  ...
}
```

This collection is maintained by the **actor's server** and contains the
objects (by id), not the Like activities themselves. It is unique by object
id — an actor cannot like the same object twice. It is often private or
semi-private.

---

## 3. Client-to-Server Flow (C2S)

When a client (app) submits a Like to the actor's outbox:

1. Server checks the object exists.
2. Server checks the object is not already in the actor's `liked` collection.
3. Server checks the actor has permission to view the object (is an
   addressee of the object or its `Create` activity).
4. Server checks the actor is not blocked by the object's responsible actor.
5. If all checks pass:
   - Add the object to the actor's `liked` collection.
   - If the object is **local**: add the `Like` activity to the object's
     `likes` collection directly.
   - If the object is **remote**: deliver the `Like` activity to the inbox
     of the actor responsible for the object (typically `attributedTo` or
     `actor` on the object).

---

## 4. Server-to-Server Flow (S2S)

When a remote server delivers a `Like` to your inbox:

1. Check the `object` exists on the local server. If it doesn't (e.g. it's
   on a third server), the `Like` can be treated as having no side effects
   and quietly ignored.
2. Check no `Like` from this actor already exists in the object's `likes`
   collection (deduplicate by actor id).
3. Check the responsible actor for the object has not blocked the liking
   actor.
4. Check the liking actor has permission to view the object.
5. If all checks pass: add the `Like` activity to the object's `likes`
   collection and update the displayed count.

---

## 5. Undoing a Like — `Undo{Like}`

Unlinking a like is done with an `Undo` activity wrapping the original `Like`:

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://alice.example/likes/abc123/undo",
  "type": "Undo",
  "actor": "https://alice.example/users/alice",
  "object": {
    "id": "https://alice.example/likes/abc123",
    "type": "Like",
    "actor": "https://alice.example/users/alice",
    "object": "https://bob.example/users/bob/statuses/456"
  }
}
```

The `object` of the `Undo` is the original `Like` activity, identified by
its `id`. This is why the original `Like` must have had a stable `id`.

The `object` may be embedded (as above) or referenced by id alone —
implementations should accept both.

**Validation on receiving an Undo{Like}:**
- The `Like` activity must exist (in the `likes` collection).
- The actor of the `Undo` must be the same as the actor of the `Like`.
- The `object` of the `Like` must be local.

**If valid:** remove the `Like` from the object's `likes` collection and
decrement the displayed count.

---

## 6. Delivery Target

The `Like` is delivered to the **inbox of the actor responsible for the
object**, not to the liking actor's followers and not to the public. The
"responsible actor" is typically the `attributedTo` field on the object.

This means:
- Likes are **not** broadcast to followers (unlike boosts/announces).
- Like counts on remote posts are only known by the post's origin server.
- A server only knows about a Like on a remote post if it happened to
  receive the notification through some other path (e.g. a local user
  is the author, or the remote server proactively forwarded it).

---

## 7. The `Dislike` Type

ActivityStreams 2.0 defines a `Dislike` activity type. **It is not used in
standard ActivityPub.** The W3C ActivityPub primer explicitly states this.

Exception: **PeerTube** supports both `Like` and `Dislike` for videos,
federating them to update video `likes` and `dislikes` counts. PeerTube
exposes both as named collections on the video object. This is a PeerTube
extension and not interoperable with Mastodon-lineage software.

Do not implement or depend on `Dislike` unless you are specifically building
PeerTube-compatible software.

---

## 8. Multiple Likes for the Same Object

The ActivityPub spec does not address what happens if an actor sends multiple
`Like` activities for the same object. In practice:

- Both `liked` (actor side) and `likes` (object side) are treated as unique
  by the relevant id (object id and actor id respectively).
- Originating servers should avoid sending duplicate `Like` activities.
- Receiving servers should silently ignore all but the first `Like` from the
  same actor for the same object.

---

## 9. Emoji Reactions

Emoji reactions are a popular extension to the basic Like model. They allow
reacting with a specific emoji instead of (or in addition to) a plain like.
There is no single standard — two incompatible approaches exist in the wild.

### 9.1 EmojiReact — Pleroma/Akkoma style (FEP-c0e0)

Pleroma introduced `EmojiReact` as a new activity type in the LitePub
namespace. This has since been formalised in **FEP-c0e0**, which is the
emerging community standard.

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    {
      "toot": "http://joinmastodon.org/ns#",
      "EmojiReact": "http://litepub.social/ns#EmojiReact"
    }
  ],
  "id": "https://alice.example/reactions/xyz",
  "type": "EmojiReact",
  "actor": "https://alice.example/users/alice",
  "object": "https://bob.example/users/bob/statuses/456",
  "content": "👍"
}
```

For a **custom emoji** (not a Unicode emoji), the `tag` property is added:

```json
{
  "type": "EmojiReact",
  "actor": "https://alice.example/users/alice",
  "object": "https://bob.example/...",
  "content": ":blobcat:",
  "tag": [{
    "type": "Emoji",
    "name": ":blobcat:",
    "icon": {
      "type": "Image",
      "url": "https://alice.example/emoji/blobcat.png"
    }
  }]
}
```

**Akkoma/Pleroma behaviour:**
- A user MAY react multiple times with **different** emoji to the same post.
- A user MAY NOT react more than once with the **same** emoji.
- `EmojiReact` is distinct from `Like` — a user can both `Like` and
  `EmojiReact` to the same post; they are separate.
- Duplicate reactions (same actor, same emoji) MUST be silently ignored.
- Unicode emoji: `tag` MAY be omitted.
- Custom emoji: `content` contains the shortcode with colons (`:blobcat:`);
  `tag` contains the `Emoji` object with the image URL.

**Undo:** wrapped in `Undo{EmojiReact}` the same way as `Undo{Like}`.

### 9.2 Misskey-style reactions (overloaded Like)

Misskey (and its forks: Calckey, Firefish, Catodon) does NOT use a separate
activity type. Instead it sends a standard `Like` activity with an additional
non-standard `_misskey_reaction` property carrying the emoji string:

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "type": "Like",
  "actor": "https://misskey.example/users/alice",
  "object": "https://bob.example/users/bob/statuses/456",
  "_misskey_reaction": "👍"
}
```

**Misskey behaviour:**
- Likes and reactions are equated — reacting replaces any previous reaction.
- Only **one** reaction per post per user is allowed (unlike Pleroma which
  allows multiple different emoji).
- Custom emoji: `_misskey_reaction` contains the shortcode (`:blobcat:@.`
  for local or `:blobcat:@misskey.example` for remote); the emoji image
  is resolved separately.

### 9.3 Interoperability between the two approaches

| | Pleroma/Akkoma (EmojiReact) | Misskey-lineage (Like + `_misskey_reaction`) |
|---|---|---|
| Activity type | `EmojiReact` (new type) | `Like` (standard type, extended) |
| Multiple reactions per post | Yes (different emoji) | No (one per user) |
| Distinct from plain Like | Yes | No |
| Custom emoji in `tag` | Yes | Shortcode in `_misskey_reaction` |
| Standard | FEP-c0e0 (draft) | Proprietary |

Servers that don't understand `EmojiReact` will ignore it (unrecognised
activity types should be treated as unknown and discarded). Servers that
don't understand `_misskey_reaction` will process it as a plain `Like` —
which means Misskey reactions **do** federate as likes to Mastodon and similar
platforms, they just lose the emoji identity.

**Mastodon** currently does not implement either emoji reaction system on the
sending side. It displays incoming Misskey reactions as plain likes. A PR for
Pleroma-style reactions was opened (#13275) but has not been merged.

**FEP-c0e0 is the recommended approach** for new implementations that want
to add emoji reactions, as it uses a distinct activity type, allowing servers
that don't support reactions to simply ignore them without inflating like counts.

---

## 10. Stale Like Counts on Remote Posts

A persistent and well-known limitation: like counts displayed on remote posts
are frequently **stale or incomplete**. This happens because:

1. Likes are delivered only to the post's author's server. They are not
   broadcast to every server that has seen the post.
2. A server that learns about a remote post (e.g. because a local user
   boosted it) receives the post object at that moment in time, including
   its `totalItems` count in the `likes` collection — but that count is a
   snapshot, not a live feed.
3. The receiving server typically does not subscribe to updates of the remote
   `likes` collection. Counts only update if the server re-fetches the object.
4. Some implementations never re-fetch remote objects at all after initial
   discovery.

This is not a bug in the protocol — it is a consequence of decentralisation
combined with the delivery model. Wikipedia's ActivityPub article notes this
explicitly as a known criticism.

**Implications for implementors:**
- Do not claim that like counts shown for remote posts are authoritative.
- If freshness matters, re-fetch the remote object before displaying its count.
- Do not use a remote `likes` collection count as a trust or ranking signal.

---

## 11. The `liked` Collection and Privacy

The `liked` collection on an actor is often kept private or unexposed. The
ActivityPub spec does not require it to be publicly readable. Implementations
vary:

- **Mastodon:** exposes a `liked` URL on the actor but requires authentication
  to read; effectively private.
- **Many others:** expose the collection URL but return an empty collection
  or a 403/404 without auth.

Do not rely on being able to read another server's `liked` collection to
reconstruct what a user has liked. The only reliable signal is receiving a
`Like` activity in your inbox.

---

## 12. Summary of Activity Types

| Activity | Sent to | Effect |
|---|---|---|
| `Like` | Author's inbox | Adds to object's `likes` collection; notification to author |
| `Undo{Like}` | Author's inbox | Removes from `likes` collection |
| `EmojiReact` (FEP-c0e0) | Author's inbox | Adds emoji reaction; ignored by non-supporting servers |
| `Undo{EmojiReact}` | Author's inbox | Removes emoji reaction |
| `Like` + `_misskey_reaction` | Author's inbox | Misskey reaction; treated as plain `Like` by others |
| `Dislike` | Author's inbox | PeerTube only; not used elsewhere |
