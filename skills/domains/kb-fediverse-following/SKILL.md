---
name: kb-fediverse-following
description: >
  Background knowledge about how following works on the Fediverse, including
  at the ActivityPub wire-format level. Load when the user asks about
  implementing follows, the Follow/Accept/Reject/Undo activity flow, locked
  vs unlocked accounts, the followers and following collections, shared
  inboxes, delivery of posts to followers, how follower-only posts work,
  account migration with the Move activity, the manuallyApprovesFollowers
  flag, pending follow requests, or unfollowing. Also load when reviewing or
  writing code that handles any of these activity types, or when debugging
  federation issues related to follows not working correctly.
user-invocable: false
---

# Fediverse Following — Complete Reference

## Overview

Following on the Fediverse is a formal ActivityPub handshake, not a simple
database write. It involves activity delivery between servers, an explicit
approval step, and ongoing delivery of content. Understanding all the steps
— and what can go wrong — is essential for correct implementation.

---

## 1. The Actor Object

Before any following can happen, each user is represented as an **actor** —
a JSON-LD object served at a stable URL. The actor contains the endpoints
and collections needed for the follow flow:

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "type": "Person",
  "id": "https://example.com/users/alice",
  "preferredUsername": "alice",
  "inbox": "https://example.com/users/alice/inbox",
  "outbox": "https://example.com/users/alice/outbox",
  "followers": "https://example.com/users/alice/followers",
  "following": "https://example.com/users/alice/following",
  "manuallyApprovesFollowers": false
}
```

Key properties for following:

- **`inbox`** — the URL where activities are POSTed to reach this actor
- **`followers`** — an `OrderedCollection` of actors who follow this actor
- **`following`** — an `OrderedCollection` of actors this actor follows
- **`manuallyApprovesFollowers`** — `false` = open/unlocked account (auto-accepts);
  `true` = locked account (requires manual approval). Defined in the
  ActivityPub Miscellaneous Terms as `as:manuallyApprovesFollowers`.

---

## 2. The Follow Handshake — Step by Step

Following is a **four-message exchange** in the general case. For unlocked
accounts it collapses to three (the Accept is sent automatically).

### Step 1: Alice sends a `Follow` activity

Alice's server POSTs a `Follow` activity to Bob's inbox:

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://alice.example/activities/follow-1",
  "type": "Follow",
  "actor": "https://alice.example/users/alice",
  "object": "https://bob.example/users/bob"
}
```

- The `object` is the actor being followed (Bob)
- The `actor` is the one initiating the follow (Alice)
- The `id` should be a unique, dereferenceable URI on Alice's server
  (though in practice many implementations use non-dereferenceable UUIDs)
- At this point, Alice's server may add Bob to Alice's `following` collection
  tentatively, or wait until the `Accept` arrives — implementations differ

### Step 2: Bob's server receives the `Follow`

On receiving the `Follow` in Bob's inbox, Bob's server:

1. Validates the HTTP Signature on the request (to confirm it came from
   Alice's server)
2. Checks whether Bob has `manuallyApprovesFollowers: true` or `false`
3. Either queues a follow request for Bob to approve (locked account), or
   automatically proceeds to send an `Accept`

At this stage the follow is **pending** — Alice is not yet in Bob's
`followers` collection.

### Step 3: Bob's server sends an `Accept` (or `Reject`)

**For unlocked accounts** — `Accept` is sent automatically:

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://bob.example/activities/accept-1",
  "type": "Accept",
  "actor": "https://bob.example/users/bob",
  "object": {
    "type": "Follow",
    "actor": "https://alice.example/users/alice",
    "object": "https://bob.example/users/bob"
  }
}
```

The `object` of the `Accept` is the original `Follow` activity (or just its
`id` URI — either form is acceptable).

**For locked accounts** — Bob manually approves or denies. If denied, a
`Reject` is sent with the same structure:

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://bob.example/activities/reject-1",
  "type": "Reject",
  "actor": "https://bob.example/users/bob",
  "object": "https://alice.example/activities/follow-1"
}
```

**Important spec note:** Servers MAY choose to not send a `Reject` at all
(e.g. to protect a user's privacy — not rejecting leaks the fact that the
account exists). This means the follow request may be silently ignored,
leaving Alice's server in an indefinite pending state. Implementations
should handle this gracefully.

### Step 4: Alice's server receives the `Accept`

On receiving the `Accept`:

- Alice's server adds Bob to Alice's `following` collection
- Bob's server adds Alice to Bob's `followers` collection
- The follow relationship is now **active**

From this point on, when Bob creates a post addressed to his followers,
his server will deliver it to Alice's inbox.

---

## 3. Unfollowing — The `Undo Follow`

To unfollow, Alice sends an `Undo` activity wrapping the original `Follow`:

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://alice.example/activities/undo-follow-1",
  "type": "Undo",
  "actor": "https://alice.example/users/alice",
  "object": {
    "type": "Follow",
    "actor": "https://alice.example/users/alice",
    "object": "https://bob.example/users/bob"
  }
}
```

This is POSTed to Bob's inbox. On receipt, Bob's server removes Alice from
Bob's `followers` collection. Alice's server removes Bob from Alice's
`following` collection.

The spec requires that the `Undo` and the activity being undone have the
**same actor**. You cannot undo another actor's Follow.

---

## 4. The `followers` and `following` Collections

Both are `OrderedCollection` objects. They may be paginated with
`OrderedCollectionPage`. The actor object contains their URLs; fetching
those URLs with `Accept: application/activity+json` returns the collection.

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://bob.example/users/bob/followers",
  "type": "OrderedCollection",
  "totalItems": 412,
  "first": "https://bob.example/users/bob/followers?page=1"
}
```

Implementations may choose to hide the actual members of these collections
for privacy (returning `totalItems` but an empty `items` array, or omitting
`first`/`next` page links). This is valid and common.

---

## 5. How Content is Delivered to Followers

When Bob creates a public post, his server must deliver it to all his
followers. This is where the follow relationship does its work.

### Addressing

A public post addressed to followers is typically addressed as:

```json
{
  "to": ["https://www.w3.org/ns/activitystreams#Public"],
  "cc": ["https://bob.example/users/bob/followers"]
}
```

A followers-only post omits the public audience:

```json
{
  "to": ["https://bob.example/users/bob/followers"],
  "cc": []
}
```

### Delivery mechanics

Bob's server must POST the `Create` activity to the `inbox` of every actor
in Bob's `followers` collection. For followers on many different servers,
this can mean hundreds of HTTP POST requests.

### Shared inbox optimisation

To avoid sending N requests to the same server (when multiple followers are
on the same instance), the actor object may declare a `sharedInbox`:

```json
{
  "endpoints": {
    "sharedInbox": "https://alice.example/inbox"
  }
}
```

When a `sharedInbox` is available, the sending server can POST **once** to
that shared inbox instead of once per follower on that instance. The
receiving server then fans out internally to all relevant local followers.
Mastodon always provides a shared inbox. Using it is optional but strongly
recommended for performance.

---

## 6. Visibility Levels and the `to`/`cc` Fields

The follow relationship determines what appears in a follower's Home
timeline. The `to` and `cc` fields on activities determine visibility:

| Visibility | `to` | `cc` |
|---|---|---|
| Public | `as:Public` | followers collection |
| Unlisted | followers collection | `as:Public` |
| Followers-only | followers collection | (empty) |
| Direct (mention-only) | mentioned actors | (empty) |

The special URI `https://www.w3.org/ns/activitystreams#Public` (often
written as `as:Public`) signals that the post is publicly accessible.

Posts addressed to followers-only are only delivered to followers' inboxes,
not crawlable publicly. A server receiving such a post should only show it
to users who follow the author.

---

## 7. Locked Accounts and Pending Requests

When `manuallyApprovesFollowers` is `true`:

- Incoming `Follow` activities are queued, not immediately accepted
- The follower sees a "pending" state in the UI
- The followed user sees a follow request notification
- They can `Accept` (sending an `Accept` activity) or `Reject` (sending a
  `Reject` activity, or silently ignoring it)
- Until accepted, the follower does NOT receive the account's posts

There is no standard way for a server to query whether a pending follow
request has been accepted or rejected — implementations typically rely on
eventually receiving an `Accept` or `Reject`, or timing out.

---

## 8. Account Migration — The `Move` Activity

ActivityPub does not natively support moving an account between servers,
but a convention has emerged (led by Mastodon) using the `Move` activity
and the `alsoKnownAs` / `movedTo` properties.

### The process

1. **New account declares `alsoKnownAs`** pointing to the old account:
   ```json
   {
     "type": "Person",
     "id": "https://new.example/users/alice",
     "alsoKnownAs": ["https://old.example/users/alice"]
   }
   ```

2. **Old account sends a `Move` activity** to all its followers:
   ```json
   {
     "@context": "https://www.w3.org/ns/activitystreams",
     "type": "Move",
     "actor": "https://old.example/users/alice",
     "object": "https://old.example/users/alice",
     "target": "https://new.example/users/alice"
   }
   ```

3. **Receiving servers** (i.e. servers that have followers of the old account)
   automatically re-issue a `Follow` from each of those followers to the new
   account, effectively migrating the follower list.

### Important limitations

- Only **followers** are migrated — not posts, likes, bookmarks, or lists
- The old account's posts remain on the old server (or disappear if the
  server is shut down)
- Not all implementations support `Move` — GotoSocial notably lacked support
  for a time
- The `alsoKnownAs` must be set on the **new** account *before* the `Move`
  is sent from the old account, or receiving servers may reject it

---

## 9. Common Implementation Mistakes

- **Not waiting for `Accept` before adding to `following`**: Adding the
  followee to `following` before the `Accept` arrives means the collection
  is inaccurate for locked accounts
- **Not handling silent `Reject`**: If a locked account never sends a
  `Reject`, the pending state must time out gracefully
- **Not validating HTTP Signatures** on incoming `Follow` activities:
  anyone could POST a fake `Follow` to your inbox
- **Sending `Accept` to the wrong URL**: The `Accept` must be delivered to
  the `inbox` of the Follow's `actor`, not the `object`
- **Not using `sharedInbox`**: Sending one request per follower per instance
  instead of using `sharedInbox` causes serious performance problems at scale
- **Forgetting to handle `Undo Follow`**: When Alice unfollows Bob, Bob's
  server must remove Alice from the `followers` collection, or Alice will
  keep receiving Bob's posts
- **Exposing full followers list without privacy consideration**: Some
  users expect their followers/following lists to be private; implementations
  should support hiding collection members while still providing `totalItems`

---

## 10. Summary: The Minimum a Correct Implementation Must Do

| Direction | Activity | Required action |
|---|---|---|
| Outgoing follow | Send `Follow` to target's `inbox` | Add to local pending state |
| Incoming `Accept` | Receive in own `inbox` | Move from pending → active; add to `following` |
| Incoming `Reject` (or silence) | Receive in own `inbox` (or timeout) | Remove from pending |
| Incoming `Follow` | Receive in own `inbox` | Queue or auto-accept; send `Accept`/`Reject` |
| Outgoing `Accept` | Send to follower's `inbox` | Add follower to `followers` collection |
| Outgoing unfollow | Send `Undo{Follow}` to target's `inbox` | Remove from `following` |
| Incoming `Undo Follow` | Receive in own `inbox` | Remove actor from `followers` collection |
| Delivering posts | POST `Create` to each follower's `inbox` (or `sharedInbox`) | — |
