---
name: kb-fediverse-group-federation
description: >
  Background knowledge about how group/forum federation works on the
  Fediverse using FEP-1b12 (FINAL status). Covers the Group actor type,
  the audience property for group identification, the Announce wrapping
  mechanism for content distribution, thread/comment structure (Page for
  top-level posts, Note for replies, inReplyTo chains), group moderation
  via attributedTo collection with Add/Remove activities, the
  Announce(Activity) vs Announce(Object) interop issue, the competing
  FEP-400e approach (Smithereen/Mastodon wall collections), and
  implementations across Lemmy, Friendica, Hubzilla, Lotide, PeerTube,
  Kbin, NodeBB, and Guppe. Load when the user asks about implementing
  groups or forums in ActivityPub; how Group actors work; how to use the
  audience property; how Announce wrapping distributes group content; how
  group moderation works; the difference between FEP-1b12 and FEP-400e;
  how Lemmy communities federate; how to build a forum with ActivityPub;
  or what FEP-1b12 specifies.
user-invocable: false
---

# Fediverse Group Federation (FEP-1b12) — Complete Reference

## Overview

Internet forums — communities where users submit posts and discuss topics —
are implemented in ActivityPub using `Group` actors. FEP-1b12 (authored by
Felix Ableitner / nutomic, received 2022-11-12, **status FINAL** since
2023-02-09) codifies the common patterns already used in production by
Lemmy, Friendica, Hubzilla, Lotide, and PeerTube.

The core mechanism: a `Group` actor receives activities from users, validates
them, wraps them in `Announce` activities, and distributes them to all
followers. The `audience` property on objects identifies which group they
belong to.

---

## 1. The Group Actor

Each forum/community is represented by a `Group` actor with standard
ActivityPub endpoints:

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "type": "Group",
  "id": "https://lemmy.example/c/technology",
  "preferredUsername": "technology",
  "name": "Technology",
  "inbox": "https://lemmy.example/c/technology/inbox",
  "outbox": "https://lemmy.example/c/technology/outbox",
  "followers": "https://lemmy.example/c/technology/followers",
  "attributedTo": "https://lemmy.example/c/technology/moderators"
}
```

The Group actor operates as an **automated actor**:
- It accepts `Follow` requests automatically (for public groups)
- It validates incoming activities and redistributes them
- It is discovered via WebFinger like any other actor

### Following a Group

Users follow a Group using the standard Follow/Accept handshake:

1. User sends `Follow` to the group's inbox
2. Group auto-accepts with an `Accept{Follow}` (public groups SHOULD do this)
3. User is added to the group's `followers` collection
4. From now on, the group distributes content to that user's inbox

Unfollowing uses `Undo{Follow}`, same as unfollowing a person.

---

## 2. The `audience` Property

The `audience` property (defined in ActivityStreams 2.0 but previously unused
in the wild) identifies which group an object belongs to:

```json
{
  "type": "Page",
  "id": "https://lemmy.example/post/123",
  "attributedTo": "https://alice.example/users/alice",
  "name": "Check out this new technology",
  "audience": "https://lemmy.example/c/technology"
}
```

### Why `audience` instead of `to` or `attributedTo`

Before FEP-1b12, implementations placed the group identifier in various
fields:
- **`to`/`cc`** — requires URL resolution to determine if a recipient is a
  Group actor; mixed with other addressees
- **`attributedTo`** — conflicts with the actual author of the post

`audience` solves this cleanly:
- No extension needed (it's already in the ActivityStreams vocabulary)
- Recipients can instantly identify the group without resolving URLs
- Existing implementations that don't understand groups simply ignore it
- Doesn't conflict with delivery addressing (`to`/`cc`) or authorship
  (`attributedTo`)

All objects and activities related to a group SHOULD include `audience`
pointing to the group's id.

---

## 3. Threads and Comments

### Top-level posts

Top-level posts (threads) are typically `Page` objects with a `name`
property serving as the title:

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "type": "Page",
  "id": "https://lemmy.example/post/123",
  "attributedTo": "https://alice.example/users/alice",
  "to": ["https://www.w3.org/ns/activitystreams#Public"],
  "cc": ["https://lemmy.example/c/technology/followers"],
  "name": "Check out this new technology",
  "content": "<p>I found something interesting...</p>",
  "audience": "https://lemmy.example/c/technology"
}
```

The `Page` type is exemplary — implementations may use other types. The
key distinction is that top-level posts have a `name` (title) while
replies typically do not.

### Replies (comments)

Replies are `Note` objects with `inReplyTo` linking to the parent:

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "type": "Note",
  "id": "https://bob.example/comment/456",
  "attributedTo": "https://bob.example/users/bob",
  "to": ["https://www.w3.org/ns/activitystreams#Public"],
  "cc": ["https://lemmy.example/c/technology/followers"],
  "inReplyTo": "https://lemmy.example/post/123",
  "content": "<p>Great find! Here is what I think...</p>",
  "audience": "https://lemmy.example/c/technology"
}
```

`inReplyTo` can point to the top-level post (for direct replies) or to
another comment (for nested replies). Lemmy displays comments in a tree
structure.

### `replies` collection

Groups MAY maintain a `replies` collection on the group or on individual
posts, enabling navigation of the thread hierarchy.

---

## 4. The Announce Wrapping Mechanism

This is the core of FEP-1b12 group federation. When a user submits content
to a group, the group wraps it in an `Announce` and distributes it to all
followers.

### Flow

1. Alice creates a post and sends `Create{Page}` to the group's inbox
2. The group validates the activity (checks blocks, permissions)
3. The group wraps it: `Announce{Create{Page}}`
4. The group sends the `Announce` to all follower inboxes

### What the Announce looks like

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "type": "Announce",
  "id": "https://lemmy.example/activities/announce/789",
  "actor": "https://lemmy.example/c/technology",
  "to": ["https://www.w3.org/ns/activitystreams#Public"],
  "cc": ["https://lemmy.example/c/technology/followers"],
  "object": {
    "type": "Create",
    "id": "https://alice.example/activities/create/123",
    "actor": "https://alice.example/users/alice",
    "object": {
      "type": "Page",
      "id": "https://lemmy.example/post/123",
      "attributedTo": "https://alice.example/users/alice",
      "name": "Check out this new technology",
      "audience": "https://lemmy.example/c/technology"
    }
  }
}
```

### What the Announce means

The `Announce` serves as **proof that the group approved the content**.
Recipients can trust that the group validated the activity. After
processing, recipients may optionally discard the `Announce` wrapper and
work with the inner activity directly.

This mechanism supports any activity type — not just `Create`. Comments,
updates, and moderation actions all flow through the same `Announce`
wrapping.

### Validation before Announcing

Groups SHOULD validate incoming activities before wrapping and distributing:
- Check the sending actor/domain is not blocked
- Optionally require the sender to be a follower
- Optionally require moderator approval
- Check the `audience` property matches this group
- Groups MUST NOT forward activities that don't include the group in
  `audience`

---

## 5. Announce(Activity) vs Announce(Object)

FEP-1b12 specifies **Announce(Activity)** — wrapping the full `Create`
activity inside the Announce. However, several major implementations send
**Announce(Object)** — wrapping just the object directly.

| Implementation | Sends | Accepts |
|---|---|---|
| Lemmy | Announce(Activity) + Announce(Object) for Mastodon compat | Both |
| Friendica | Announce(Object) | Both |
| Hubzilla | Announce(Object) | Both |
| NodeBB | Announce(Object) | Both |
| Discourse | — | Both (added Object support for NodeBB compat) |

The FEP author (nutomic) acknowledged not knowing about Announce(Object)
usage when writing the spec. Community consensus is that `Announce(Object)`
should be treated as shorthand for `Announce(Create(Object))`.

**Recommendation for implementors**: When **sending**, Announce(Activity)
is spec-compliant. When **receiving**, accept both forms — treat
Announce(Object) as equivalent to Announce(Create(Object)). The FEP's
FINAL status makes formal amendment difficult, but real-world
interoperability requires handling both.

---

## 6. Group Moderation

Group moderation is an optional feature defined in FEP-1b12, initially
implemented only in Lemmy.

### Moderator list

Moderators are listed in the group's `attributedTo` property, which
resolves to a collection of actor URLs:

```json
{
  "type": "Group",
  "id": "https://lemmy.example/c/technology",
  "attributedTo": "https://lemmy.example/c/technology/moderators"
}
```

The moderators collection:

```json
{
  "type": "OrderedCollection",
  "id": "https://lemmy.example/c/technology/moderators",
  "orderedItems": [
    "https://alice.example/users/alice",
    "https://bob.example/users/bob"
  ]
}
```

### Adding and removing moderators

Moderator changes use `Add` and `Remove` activities:

```json
{
  "type": "Add",
  "actor": "https://alice.example/users/alice",
  "object": "https://charlie.example/users/charlie",
  "target": "https://lemmy.example/c/technology/moderators"
}
```

The actor performing the Add/Remove MUST already appear in the
`attributedTo` collection (i.e., must already be a moderator).

### Content moderation

Moderators remove content using `Remove` activities (not `Delete` — the
ActivityPub spec implies `Delete` should only come from the object's
author):

```json
{
  "type": "Remove",
  "actor": "https://alice.example/users/alice",
  "object": "https://lemmy.example/post/123",
  "target": "https://lemmy.example/c/technology"
}
```

### Distribution of moderation actions

Moderation activities MUST also be wrapped in `Announce` by the group and
distributed to all followers, so moderation takes effect across all
federated instances.

Server administrators can also send moderation activities. The group must
wrap these in `Announce` for distribution.

---

## 7. Interoperability with Non-Group-Aware Software

A key design goal of FEP-1b12 is backward compatibility with software
that doesn't understand groups (e.g., Mastodon).

### How it works

When a group sends `Announce{Create{Note}}` to a Mastodon user who follows
the group, Mastodon sees it as a regular boost/reblog. The user sees the
content in their timeline attributed to the original author, with the
group shown as the booster. This is imperfect but functional.

### Known issues

- **Mastodon reply routing**: Mastodon sends replies only to mentioned
  actors, not to the group. The group never receives the reply and cannot
  redistribute it to other followers. This breaks cross-instance comment
  threading.
- **Vote/Like counts**: Likes sent to the post author's inbox are processed
  locally but not announced by the group to followers, causing count
  discrepancies across instances.
- **Hubzilla workaround**: Hubzilla historically made the forum owner
  appear as the post author since "Mastodon will reject or ignore any
  messages from people you don't follow."
- **Mastodon's own groups**: Mastodon's pending groups PR (#19059) uses
  FEP-400e instead, which is incompatible with FEP-1b12. A Mastodon
  developer (Claire) argued that FEP-1b12's compatibility with
  non-group-aware software is actually a problem because it prevents
  enforcing group-specific interaction semantics (like preventing
  reblogging of group posts).

---

## 8. FEP-1b12 vs FEP-400e (Publicly Appendable Collections)

Two incompatible approaches to groups exist in the fediverse:

| | FEP-1b12 | FEP-400e |
|---|---|---|
| Mechanism | Group wraps activities in `Announce` | Actors send `Add` to group's `wall` collection |
| Group identification | `audience` property | `wall` property on Group actor |
| Content distribution | Group sends `Announce` to followers | Group sends `Add` to followers |
| Detection | Check for `Group` type + `audience` usage | Check for `wall` property on actor |
| Status | FINAL | — |
| Adoption | Lemmy, Friendica, Hubzilla, Lotide, PeerTube, Kbin, NodeBB | Smithereen (~25 MAU), Mastodon (pending PR) |

FEP-1b12 is the de-facto standard used by the vast majority of group
implementations. FEP-400e is currently only implemented by Smithereen and
proposed for Mastodon.

There is no way to detect which approach a `Group` actor uses from the
actor document alone without checking for the presence of a `wall`
property. trwnh noted there is "nothing actually special about the Group
type" in ActivityStreams 2.0 — the behavior must be inferred.

---

## 9. Implementation Matrix

| Platform | Group Type | audience | Announce wrapping | Moderation | Notes |
|---|---|---|---|---|---|
| Lemmy | Community = `Group` | Yes (since 0.17.0) | Announce(Activity) + Announce(Object) | Full (attributedTo) | Reference implementation |
| Friendica | Forum = `Group` | Yes | Announce(Object) | Yes | Federated forums since 2019.03 |
| Hubzilla | Forum = `Group` | Yes | Announce(Object) | Yes | Workaround for Mastodon compat |
| Lotide | Community = `Group` | Yes | Yes | — | — |
| PeerTube | Channel = `Group` | Yes | Yes | — | Video-oriented |
| Kbin/Mbin | Magazine = `Group` | Yes | Yes | Yes | Lemmy-compatible |
| NodeBB | Category = `Group` | Yes (deviation) | Announce(Object) | — | Categories only; `audience` at 2nd-order parent |
| Guppe | Auto-group = `Group` | No | Announce(Object) | No | ~200 lines; simplest possible group (boost bot) |
| Mastodon | Pending | No | No (uses FEP-400e) | — | PR #19059; incompatible with FEP-1b12 |

---

## 10. Creating a Post in a Group — Complete Flow

This section traces the full lifecycle of a group post.

### Step 1: User creates a post

Alice writes a post for the Technology community and sends it to the
group's inbox:

```json
{
  "type": "Create",
  "actor": "https://alice.example/users/alice",
  "to": ["https://www.w3.org/ns/activitystreams#Public"],
  "cc": ["https://lemmy.example/c/technology"],
  "object": {
    "type": "Page",
    "attributedTo": "https://alice.example/users/alice",
    "name": "Check out this new technology",
    "content": "<p>I found something interesting...</p>",
    "audience": "https://lemmy.example/c/technology"
  }
}
```

### Step 2: Group validates

The group checks:
- Alice is not blocked
- The domain is not blocked
- `audience` matches this group
- (Optional) Alice is a follower
- (Optional) Moderator approval required

### Step 3: Group announces

The group wraps and distributes:

```json
{
  "type": "Announce",
  "actor": "https://lemmy.example/c/technology",
  "to": ["https://www.w3.org/ns/activitystreams#Public"],
  "cc": ["https://lemmy.example/c/technology/followers"],
  "object": {
    "type": "Create",
    "actor": "https://alice.example/users/alice",
    "object": { ... }
  }
}
```

### Step 4: Followers receive

Bob (on a different server) receives the `Announce` in his inbox. His
server:
1. Verifies the `Announce` came from the group (HTTP Signature check)
2. Extracts the inner `Create{Page}`
3. Displays the post in the Technology community feed
4. The `Announce` wrapper serves as proof the group approved this content

### Step 5: Bob replies

Bob sends a reply (`Create{Note}` with `inReplyTo`) to the group's inbox.
The group validates and announces it to all followers.

---

## 11. Discovery

Groups are discoverable via WebFinger. Lemmy uses the `!` prefix
convention for communities:

```
GET /.well-known/webfinger?resource=acct:technology@lemmy.example
```

The response includes a `self` link with `type: Group` in properties:

```json
{
  "rel": "self",
  "type": "application/activity+json",
  "href": "https://lemmy.example/c/technology",
  "properties": {
    "https://www.w3.org/ns/activitystreams#type": "Group"
  }
}
```

The `!` prefix is a Lemmy UI convention, not a protocol requirement.
NodeBB uses `@` prefix like regular actors. The WebFinger response's
`type: Group` property is the canonical way to detect a group.

---

## 12. Known Issues and Pitfalls

- **Mastodon reply routing**: Mastodon doesn't include the group in
  replies, so the group can't redistribute them. This is the biggest
  cross-platform interop issue.
- **Announce(Object) non-compliance**: Hubzilla, Friendica, and NodeBB
  send Announce(Object) which is technically non-compliant. Consumers
  must accept both forms.
- **Vote count discrepancies**: Likes/dislikes sent to post author instead
  of group are not redistributed, causing different counts on different
  instances.
- **No `<h1>` in Page titles**: The title goes in `name`, not in HTML
  content.
- **Delete vs Remove**: Use `Remove` for moderation actions, not `Delete`.
  `Delete` implies the actor is the author of the object.
- **Private groups**: FEP-1b12 explicitly removed private groups from
  scope. Lemmy and Friendica implement them independently by restricting
  activity visibility to followers only and verifying member lists.
- **Group detection**: There is no reliable way to distinguish a FEP-1b12
  group from a FEP-400e group from the actor document alone without
  checking for a `wall` property.
