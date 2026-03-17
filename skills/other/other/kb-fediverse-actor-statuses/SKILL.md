---
name: kb-fediverse-actor-statuses
description: >
  Background knowledge about FEP-82f6 Actor statuses, an ActivityPub
  extension for short, non-interactable profile status text. Covers the
  ActorStatus type (content, endTime expiration, attachment for rich
  metadata like now-playing), actor fields (status for current inlined
  status, statusHistory collection), activities (Create to set,
  Remove to clear from profile but keep in history, Delete to remove
  entirely), the sm: JSON-LD namespace from Smithereen, the 100-character
  minimum support requirement, the design philosophy of one FEP = one UX
  pattern with clean compatibility breaks, the Remove vs Delete
  distinction, why Update is forbidden, why the featured collection is
  not reused, and the inspiration from early Facebook "is..." statuses,
  VKontakte taglines, Discord custom statuses, and GitHub profile
  statuses. Load when the user asks about actor statuses; profile status
  text; FEP-82f6; how to add a custom status to an ActivityPub actor;
  short non-interactable profile messages; status expiration; status
  history; the ActorStatus type; or the Smithereen sm: namespace.
user-invocable: false
---

# Fediverse Actor Statuses (FEP-82f6) — Complete Reference

## Overview

FEP-82f6 (authored by Gregory Klyushnikov / grishka, received 2025-05-12,
status DRAFT — finalization expected ~2026-03-18) describes an ActivityPub
extension that allows actors to publish a short status text on their
profile, with optional expiration, structured metadata attachment, and
history.

The feature replicates a well-known UX pattern from centralized platforms:
early Facebook "is..." statuses (2006–2009), VKontakte taglines, Discord
custom statuses, and GitHub profile statuses. These are distinct from
regular posts — they cannot be interacted with (no likes, replies, boosts),
cannot contain media attachments, and have a short character limit.

The proposal originates from **Smithereen**, a federated social network
modeled after VKontakte, which already implements this feature. The JSON-LD
namespace `http://smithereen.software/ns#` (prefix `sm:`) reflects this
origin.

---

## 1. The ActorStatus Object

`ActorStatus` extends the ActivityPub `Object` type. It represents a single
status update.

### Required Fields

| Field | Description |
|-------|-------------|
| `id` | Unique identifier for this status update |
| `attributedTo` | ID of the actor whose status this is |
| `content` | Plain text content of the status |
| `published` | Timestamp when the status was created |

### Optional Fields

| Field | Description |
|-------|-------------|
| `endTime` | Timestamp when the status expires. If present and in the past, implementations MUST NOT display this status |
| `attachment` | Structured metadata about what the actor is doing (e.g., a song, a video game). If present, `content` MUST contain a fallback human-readable plain text representation |

### Example

```json
{
  "type": "ActorStatus",
  "id": "https://example.social/users/1/statuses/1747286633",
  "attributedTo": "https://example.social/users/1",
  "content": "is desperately trying to bring the old internet back",
  "published": "2025-05-15T05:23:53.539Z",
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    {
      "sm": "http://smithereen.software/ns#",
      "ActorStatus": "sm:ActorStatus"
    }
  ]
}
```

### Example with Expiration

```json
{
  "type": "ActorStatus",
  "id": "https://example.social/users/1/statuses/1747300000",
  "attributedTo": "https://example.social/users/1",
  "content": "at a conference until Friday",
  "published": "2025-05-15T09:00:00.000Z",
  "endTime": "2025-05-16T18:00:00.000Z"
}
```

### Example with Attachment (Now-Playing)

```json
{
  "type": "ActorStatus",
  "id": "https://example.social/users/1/statuses/1747350000",
  "attributedTo": "https://example.social/users/1",
  "content": "Radiohead — Everything In Its Right Place",
  "published": "2025-05-15T12:00:00.000Z",
  "attachment": {
    "type": "Audio",
    "name": "Everything In Its Right Place",
    "attributedTo": "Radiohead"
  }
}
```

The `content` field MUST contain a human-readable fallback so servers that
don't understand the structured `attachment` can still display meaningful
text.

---

## 2. Actor Fields

Two OPTIONAL fields are added to actor objects:

### `status`

The current status update. Rules:

- MUST NOT be present if the last status has expired or been cleared
- MUST contain an **inlined** `ActorStatus` object (not a reference/link)
- When present, it is always current and non-expired — consumers can rely
  on this

```json
{
  "type": "Person",
  "id": "https://example.social/users/1",
  "name": "Alice",
  "status": {
    "type": "ActorStatus",
    "id": "https://example.social/users/1/statuses/1747286633",
    "attributedTo": "https://example.social/users/1",
    "content": "is desperately trying to bring the old internet back",
    "published": "2025-05-15T05:23:53.539Z"
  }
}
```

### `statusHistory`

A collection of all past status updates. Behavior:

- If present, implementations MAY provide a UI to view the actor's status
  history (similar to early Facebook's status timeline)
- If absent, implementations SHOULD NOT store past status updates and
  MUST NOT expose them in the UI
- The presence or absence of this collection signals to remote servers
  whether the actor supports status history

---

## 3. Activities

### Create — Set a New Status

Send `Create{ActorStatus}` to followers.

```json
{
  "type": "Create",
  "actor": "https://example.social/users/1",
  "object": {
    "type": "ActorStatus",
    "id": "https://example.social/users/1/statuses/1747286633",
    "attributedTo": "https://example.social/users/1",
    "content": "is desperately trying to bring the old internet back",
    "published": "2025-05-15T05:23:53.539Z"
  },
  "to": "https://example.social/users/1/followers"
}
```

Upon receiving:
- Update the actor's current status
- If the actor has `statusHistory`, add the new status to it
- If the actor does NOT have `statusHistory`, the previous status is
  considered deleted (as if `Delete`d)

After sending, the `status` field on the actor object MUST be updated.
An `Update{Actor}` MUST NOT be sent — the `Create` already implicitly
updates the status field on remote servers.

### Remove — Clear Status from Profile

Send `Remove{ActorStatus}` to followers.

```json
{
  "type": "Remove",
  "actor": "https://example.social/users/1",
  "object": "https://example.social/users/1/statuses/1747286633",
  "to": "https://example.social/users/1/followers"
}
```

Upon receiving:
- If the `object` ID matches the actor's current status, clear it
- If the actor has `statusHistory`, the status **stays in history**
- The actor's `status` field becomes absent

### Delete — Completely Remove a Status

Send `Delete{ActorStatus}` to followers.

```json
{
  "type": "Delete",
  "actor": "https://example.social/users/1",
  "object": "https://example.social/users/1/statuses/1747286633",
  "to": "https://example.social/users/1/followers"
}
```

Upon receiving:
- Remove the status from `statusHistory` as well as clearing from profile
- If the actor has no `statusHistory`, this is identical to `Remove`

### No Update Allowed

Once published, a status object **cannot be `Update`d**. This is a
deliberate design decision — if the user wants a different status, they
create a new one.

### No Interactions

Statuses cannot be interacted with. Implementations:
- SHOULD NOT send any activities (Like, Announce, etc.) referring to
  statuses as their `object` from non-owner actors
- MUST either ignore such activities (return 2xx) or reject them (return
  4xx)

---

## 4. Remove vs Delete Semantics

The spec makes a deliberate distinction:

| Activity | Profile | History | Use case |
|----------|---------|---------|----------|
| `Remove` | Cleared | Kept (if `statusHistory` exists) | "I'm done with this status, but it's part of my history" |
| `Delete` | Cleared | Removed | "I want this status to no longer exist anywhere" |
| `Remove` (no history) | Cleared | N/A | Identical to Delete when `statusHistory` is absent |

This mirrors the Facebook/VK pattern where statuses accumulate in a
timeline. Users can either move past them (they become history) or delete
them entirely.

---

## 5. JSON-LD Context

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    {
      "sm": "http://smithereen.software/ns#",
      "ActorStatus": "sm:ActorStatus",
      "status": {
        "@type": "@id",
        "@id": "sm:status"
      },
      "statusHistory": {
        "@type": "@id",
        "@id": "sm:statusHistory"
      }
    }
  ]
}
```

The namespace `http://smithereen.software/ns#` originates from the
Smithereen project. `ActorStatus` is equivalent to
`http://smithereen.software/ns#ActorStatus` — they are the same type
expressed with and without the namespace prefix.

---

## 6. Character Limit

- Implementations MUST support statuses of up to **100 characters or
  emoji**
- Implementations MAY allow longer statuses, but they MAY be truncated
  on the receiving side depending on display and storage constraints
- RECOMMENDED: apply a 100-character limit in the user-facing text input,
  but be more permissive when processing status updates from other servers

---

## 7. Comparison with Centralized Platform Statuses

| Platform | Feature | Interactable? | Media? | Limit | History? |
|----------|---------|---------------|--------|-------|----------|
| Early Facebook (2006–2009) | "is..." status | No | No | Very short | Yes |
| VKontakte | Status/tagline | No | No | Short | Yes |
| Discord | Custom status | No | Emoji only | 128 chars | No |
| GitHub | Custom status | No | Emoji only | Short | No |
| Slack | Custom status | No | Emoji only | 100 chars | No |
| FEP-82f6 | ActorStatus | No | Attachment metadata | 100+ chars | Optional |

No existing Fediverse platform has a standardized actor status feature.
Smithereen is the only known implementation.

---

## 8. Design Philosophy

The author's design philosophy is distinctive and worth understanding for
implementers:

### One FEP = One UX Pattern

"This FEP serves one particular UX use case and **only that**. Nothing
less, nothing more." The proposal does not try to be a general-purpose
mechanism. It captures a specific, well-understood UI pattern.

### Clean Compatibility Break

"A clean compatibility break with all preexisting software is an explicit
goal." Rather than reusing existing mechanisms (like the `featured`
collection) for partial backward compatibility, the proposal introduces
a new type that servers either understand or don't. This avoids ambiguous
degradation where a status might misleadingly appear as a pinned post.

### UI-to-Protocol Mapping

"I simply translated the actions that the user can take in the UI to AP
activities, one-to-one." Each user action maps directly to one Activity
type:

| User action | Activity |
|-------------|----------|
| Set status | `Create{ActorStatus}` |
| Clear status | `Remove{ActorStatus}` |
| Delete status | `Delete{ActorStatus}` |

No side effects, no indirect mechanisms (like using `Update` with
`endTime` changes to clear a status).

---

## 9. Why Certain Alternatives Were Rejected

### Why Not Use the `featured` Collection?

silverpill suggested placing `ActorStatus` in `featured` for partial
compatibility. Rejected because:
- Mixing different object types in one collection causes database and UI
  complexity
- A clean break is preferred over a status misleadingly appearing as a
  pinned post
- `featured` has different semantics (showcase content vs. current state)

### Why No `Update` Activity?

silverpill proposed `Update{ActorStatus}` setting `endTime` to a past
date to clear statuses. Rejected because:
- It replaces an obvious action (`Remove`) with a non-obvious one
  (`Update` with a side effect)
- It opens the door to restoring expired statuses by resetting `endTime`
  to a future date
- The `Remove` activity directly and transparently maps to the user
  action of clearing a status

### Why No Interactions?

SorteKanin asked why statuses can't have likes, replies, images, or long
text. Rejected because adding these features would make statuses overlap
with regular posts (`Note` objects) and lose the distinct UX identity that
makes them useful.

---

## 10. Implementation Guidance

### Sending a Status Update

1. Create an `ActorStatus` object with `id`, `attributedTo`, `content`,
   `published`, and optionally `endTime` and/or `attachment`
2. Send `Create{ActorStatus}` to the actor's followers
3. Update the actor's `status` field with the new status
4. Do NOT send `Update{Actor}` — the `Create` implicitly updates remote
   copies

### Receiving a Status Update

1. On `Create{ActorStatus}`: update the actor's displayed status. If you
   track history and the actor has `statusHistory`, add to it. If no
   `statusHistory`, discard the previous status.
2. On `Remove{ActorStatus}`: if the object ID matches the current status,
   clear it. Keep in history if applicable.
3. On `Delete{ActorStatus}`: clear from profile AND remove from history.
4. Ignore any other activities (Like, Announce, etc.) targeting statuses.

### Displaying Statuses

- Show on the actor's profile page
- Optionally show next to the actor's name in feeds, comments, etc.
- If `endTime` is present and in the past, do NOT display
- If `statusHistory` is available, optionally provide a UI to browse it

### Handling the Attachment Field

The `attachment` field carries structured metadata (e.g., a song, a game).
If you can render it richly (album art, game icon), do so. If not, the
`content` field already contains a plain text fallback — just display that.

---

## 11. Known Issues and Considerations

- **Single implementation**: Smithereen is the only known implementation.
  The `sm:` namespace reflects this single-origin status. Adoption by
  other platforms would validate the design.
- **No standard attachment types**: The spec does not define specific
  attachment schemas for now-playing, gaming, etc. Implementers must
  define their own structured formats or wait for community conventions.
- **Expiration timing**: Implementations must actively check `endTime`
  and stop displaying expired statuses. There is no push notification
  for expiration — it's poll-based on the `endTime` value.
- **No `Update`**: If a user makes a typo in their status, they must
  create a new one rather than editing. This is intentional but may
  surprise users accustomed to editing posts.
- **History privacy**: The `statusHistory` collection is visible to
  "anyone who can see the actor itself." There is no mechanism for
  private or followers-only status history.
