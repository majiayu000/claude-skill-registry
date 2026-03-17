---
name: kb-fediverse-activity-intents
description: >
  Background knowledge about Activity Intents on the Fediverse, based on
  FEP-3b86 (DRAFT status). Covers how servers publish machine-readable URL
  templates via WebFinger for cross-server social interactions (Follow,
  Like, Announce, Create, etc.), the rel namespace convention
  (https://w3id.org/fep/3b86/*), RFC 6570 URI Templates with parameter
  placeholders, the 28 standard activity intents plus the Object intent,
  the special Create intent for pre-populating new content, workflow
  callbacks (on-success, on-cancel), the remote server interaction flow,
  the fallback chain (Activity Intents → oStatus subscribe → hard-coded
  URLs), security considerations (CSRF, open redirects, interstitial
  pages), the history from oStatus remote follow through Mastodon's
  authorize_interaction endpoint, the Twitter Web Intents inspiration,
  comparison with Fedilinks (FEP-07d7), and implementations across
  Emissary, Forte, Loops, PieFed, streams, and WordPress. Load when the
  user asks about implementing remote interaction buttons; cross-server
  follow/like/share from a remote website; Activity Intents; FEP-3b86;
  how to publish interaction endpoints via WebFinger; the oStatus
  subscribe template; Mastodon's authorize_interaction endpoint; how
  remote follow works; how to let users interact with content using their
  home server account; or how to add Follow/Like/Share buttons for
  Fediverse users on a website.
user-invocable: false
---

# Fediverse Activity Intents (FEP-3b86) — Complete Reference

## Overview

Activity Intents enable cross-server social interactions on the Fediverse.
A server publishes machine-readable URL templates in its WebFinger response,
advertising endpoints where users can perform activities like Follow, Like,
Announce, or Create. Remote websites use these templates to display
interactive buttons that let users act on content using their home server
account — without copy-pasting URLs or leaving the page.

FEP-3b86 (authored by Ben Pate, received 2024-04-19, **status DRAFT**)
formalizes and generalizes the pattern established by the oStatus "remote
follow" mechanism. It is inspired by Twitter Web Intents (2011) and
Facebook's Share Button — centralized URL-based interaction flows — adapted
for a decentralized system where the user's home URL must be discovered
dynamically via WebFinger.

## The Problem: Broken Remote Interactions

Without Activity Intents, cross-server interaction on the Fediverse is
painful. If a user on Server A wants to follow, like, or share content from
Server B, the typical workflow is:

1. Copy the URL of the content or actor
2. Paste it into their own instance's search bar
3. Wait for it to resolve
4. Then interact

The only partially-standardized alternative was the oStatus subscribe
template — a link in WebFinger with
`rel="http://ostatus.org/schema/1.0/subscribe"` pointing to Mastodon's
`/authorize_interaction` endpoint. But this mechanism:

- Only supports **Follow** — no Like, Announce, Create, Reply, etc.
- Is **undocumented** in the ActivityPub context
- Was **reverse-engineered** from Mastodon's behavior, not formally specified
- Uses an **oStatus-specific** rel value from a superseded protocol
- Provides **no callbacks** — no way for the remote server to know when the
  action completes

## How Activity Intents Work

### WebFinger Response Structure

Activity Intent links appear in the standard WebFinger JRD `links` array.
Each link has a `rel` identifying the activity type and a `template`
containing an RFC 6570 URI Template:

```json
{
  "subject": "acct:alice@example.social",
  "links": [
    {
      "rel": "self",
      "type": "application/activity+json",
      "href": "https://example.social/users/alice"
    },
    {
      "rel": "http://ostatus.org/schema/1.0/subscribe",
      "template": "https://example.social/authorize_interaction?uri={uri}"
    },
    {
      "rel": "https://w3id.org/fep/3b86/Follow",
      "template": "https://example.social/authorize_interaction?uri={object}"
    },
    {
      "rel": "https://w3id.org/fep/3b86/Like",
      "template": "https://example.social/intents/like?id={object}"
    },
    {
      "rel": "https://w3id.org/fep/3b86/Announce",
      "template": "https://example.social/intents/announce?id={object}"
    },
    {
      "rel": "https://w3id.org/fep/3b86/Create",
      "template": "https://example.social/share?text={content}"
    }
  ]
}
```

### Link Properties

**`rel`**: Uses the `https://w3id.org/fep/3b86/*` namespace (per FEP-888d's
w3id.org convention) where `*` is the Activity type name from the W3C
Activity Vocabulary. Examples:

- `https://w3id.org/fep/3b86/Follow`
- `https://w3id.org/fep/3b86/Like`
- `https://w3id.org/fep/3b86/Announce`
- `https://w3id.org/fep/3b86/Create`

**`template`**: An RFC 6570 URI Template with parameter placeholders
(e.g., `{object}`, `{content}`). The `template` property (as opposed to
`href`) is standardized in RFC 6415 (Web Host Metadata), not merely an
oStatus invention — though early Fediverse usage inherited it from the
oStatus era.

### Template Parameter Rules

Remote servers MUST:

- Replace all recognized parameter placeholders with appropriate values
- Replace unrecognized placeholders with empty strings
- Percent-encode all substituted values per RFC 3986

All parameter values represent IDs (URLs) of JSON-LD resources, except for
the Create intent's content parameters.

## The 28 Standard Activity Intents

FEP-3b86 defines intents for every W3C Activity Vocabulary type. Most
follow a common pattern with an `{object}` parameter and optional workflow
callbacks:

| Intent | Rel suffix | Primary parameters | Purpose |
|--------|-----------|-------------------|---------|
| Accept | `/Accept` | `{object}` | Accept an offer, invitation, etc. |
| Add | `/Add` | `{object}`, `{target}` | Add object to a collection |
| Announce | `/Announce` | `{object}` | Boost/reshare a document |
| Arrive | `/Arrive` | `{location}` | Mark arrival at a location |
| Block | `/Block` | `{object}` | Block a user or document |
| Create | `/Create` | (see below) | Create new content |
| Delete | `/Delete` | `{object}`, `{origin}` | Delete an object |
| Dislike | `/Dislike` | `{object}` | Dislike a document |
| Flag | `/Flag` | `{object}` | Report inappropriate content |
| Follow | `/Follow` | `{object}` | Follow an actor |
| Ignore | `/Ignore` | `{object}` | Ignore/mute an actor or object |
| Invite | `/Invite` | `{target}`, `{object}` | Invite an actor to an event/group |
| Join | `/Join` | `{object}` | Join a group or event |
| Leave | `/Leave` | `{object}` | Leave a group or event |
| Like | `/Like` | `{object}` | Like a document |
| Listen | `/Listen` | `{object}` | Listen to audio content |
| Move | `/Move` | `{object}`, `{target}`, `{origin}` | Move object between collections |
| Offer | `/Offer` | `{object}`, `{target}` | Offer an object to an actor |
| Question | `/Question` | `{name}` | Start a question/poll |
| Read | `/Read` | `{object}` | Mark as read |
| Reject | `/Reject` | `{object}` | Reject an offer or invitation |
| Remove | `/Remove` | `{object}`, `{target}` | Remove object from collection |
| TentativeAccept | `/TentativeAccept` | `{object}` | Tentatively accept |
| TentativeReject | `/TentativeReject` | `{object}` | Tentatively reject |
| Travel | `/Travel` | `{target}`, `{origin}` | Travel between locations |
| Undo | `/Undo` | `{object}` | Undo a previous activity |
| Update | `/Update` | `{object}` | Update an existing object |
| View | `/View` | `{object}` | Mark as viewed |

All activity intents also accept optional `{on-success}` and `{on-cancel}`
workflow callback parameters.

## The Create Intent (Special Case)

The Create intent is fundamentally different from other intents. Instead of
acting on an existing object via `{object}`, it **pre-populates** a new
document for the user to compose:

| Parameter | Description |
|-----------|-------------|
| `{type}` | Object type (Note, Article, etc.) |
| `{name}` | Name/title to pre-populate |
| `{summary}` | Summary to pre-populate |
| `{content}` | Text content to pre-populate |
| `{inReplyTo}` | ID of object being replied to |
| `{attachment}` | ID of object to attach |
| `{tag}` | ID of tag to reference |
| `{startTime}` | Start time (RFC 3339) |
| `{endTime}` | End time (RFC 3339) |
| `{describes}` | ID of object to describe (for Profile) |

Example — a "Share on Mastodon" button:

```json
{
  "rel": "https://w3id.org/fep/3b86/Create",
  "template": "https://mastodon.social/share?text={content}"
}
```

Example — a "Reply" button on a remote post:

```
https://example.social/share?text={content}&inReplyTo={inReplyTo}
```

## The Object Intent (Non-Activity)

A special intent at `https://w3id.org/fep/3b86/Object` enables users to
open remote objects in their home server — analogous to pasting a URL into
Mastodon's search bar.

This intent does **not** generate any ActivityPub activities and does
**not** support `on-success`/`on-cancel` callbacks.

```json
{
  "rel": "https://w3id.org/fep/3b86/Object",
  "template": "https://server.org/intents/object?objectId={object}"
}
```

The Object intent was added after discussion where silverpill argued that
using the `View` activity verb would incorrectly imply that a `View`
activity would be generated and sent. The custom URI makes it explicit that
the server is just retrieving the object, not creating an activity.

## Workflow Callbacks

Activity Intents support optional callback parameters for post-interaction
flow control:

**`{on-success}`** — action after the user completes the workflow:
- `(close)` — instructs the popup window to close
- A valid URL — redirects the user (with interstitial page)

**`{on-cancel}`** — action if the user cancels:
- Same options as `on-success`

**Critical requirement**: Home servers MUST display an interstitial page
before any URL redirect, showing the destination and requiring user
confirmation. Automatic redirects create open-redirect vulnerabilities.

## Remote Server Interaction Flow

The complete user flow for a remote interaction:

1. User visits a remote server and sees social interaction buttons (Follow,
   Like, Share, etc.)
2. User clicks a button
3. Remote server checks if the user is already recognized (e.g., via cookie)
4. If unrecognized, user enters their Fediverse ID (`@user@server`)
5. Remote server performs a WebFinger query for the user's home server
6. Remote server finds the appropriate Activity Intent link in the response
7. Remote server substitutes parameter values into the URI Template
8. User is redirected to their home server's Activity Intent endpoint
9. Home server shows a confirmation page (CSRF-protected POST form)
10. User confirms; home server executes the activity
11. Home server uses `on-success`/`on-cancel` to redirect back (with
    interstitial) or close the popup

## Fallback Strategy

Remote servers SHOULD implement a fallback chain for servers that don't
publish Activity Intents:

1. **Activity Intents** — use if present in WebFinger response
2. **oStatus subscribe** — fall back to the
   `http://ostatus.org/schema/1.0/subscribe` template (Mastodon's
   `/authorize_interaction` endpoint)
3. **Hard-coded URLs** — fall back to known implementation-specific paths
   (Mastodon's `/share`, Hubzilla's `/rpost`)

## Security Considerations

### CSRF Prevention

- Remote servers MUST only send **GET** requests to home servers
- Home servers MUST NOT change data based on GET requests
- Home servers SHOULD protect intent endpoints with CSRF tokens on POST
  operations
- The GET request loads a confirmation page; the actual mutation happens via
  a CSRF-protected POST form submission

### Open Redirect Mitigation

The `on-success` and `on-cancel` parameters accept arbitrary URLs, creating
a potential open-redirect vulnerability. Required mitigation (per OWASP):

> "Force all redirects to first go through a page notifying users that they
> are going off of your site, with the destination clearly displayed, and
> have them click a link to confirm."

The FEP also references OAuth 2.0 Security Best Current Practice § 4.11
(Open Redirection) as additional guidance. During SocialHub discussion,
thisismissem recommended preregistered redirect URIs (OAuth-style) as a
stronger defense, but this was not adopted into the spec.

## History: From oStatus to Activity Intents

### oStatus Remote Follow (Pre-2017)

The oStatus protocol suite included a subscribe mechanism using WebFinger.
A server published a link with `rel="http://ostatus.org/schema/1.0/subscribe"`
containing a template URL. GNU social used this for remote follows.

### Mastodon's authorize_interaction (2017+)

Mastodon adopted the oStatus subscribe template, exposing its own
`/authorize_interaction?uri={uri}` endpoint. Early versions used a different
format (`/authorize_follow?acct=acct:user@instance`) that didn't comply with
GNU social's expectations (Mastodon issue #2177). This was eventually
standardized within Mastodon but remained Mastodon-specific — other
implementations had to reverse-engineer the behavior.

### Twitter Web Intents (2011)

Twitter released Web Intents in March 2011, providing URL-based flows:

- `https://twitter.com/intent/tweet?text=...`
- `https://twitter.com/intent/retweet?tweet_id=...`
- `https://twitter.com/intent/like?tweet_id=...`
- `https://twitter.com/intent/follow?screen_name=...`

These allowed websites to embed Twitter interaction buttons without
requiring users to leave the site or authorize a new app. FEP-3b86
explicitly cites Twitter Web Intents as a reference and applies the same
pattern to the decentralized Fediverse.

### Earlier Proposal: ActivityPub Extension for Intent (2017)

Akihiko Odaki proposed an `Intent` class for Activity Streams 2.0 in 2017,
enabling delivery of "intents declared at locations different from those
where the activity to be performed." This took a different approach —
defining a new vocabulary type rather than using WebFinger link templates.
It did not gain traction or implementations.

### FEP-3b86 (2024)

Ben Pate synthesized the lessons from oStatus, Twitter Web Intents, and the
Mastodon approach into a formal specification. Key improvements:

- Works for **any** activity type, not just Follow
- Uses **standardized** RFC 6570 URI Templates and RFC 6415 `template`
  property
- Publishes via **WebFinger** — the existing discovery mechanism
- Includes **workflow callbacks** for post-interaction flow
- Has **security guidance** (CSRF, open redirects)
- Is **formally documented** as a Fediverse Enhancement Proposal

## Comparison: Activity Intents vs Fedilinks (FEP-07d7)

| Aspect | Activity Intents (FEP-3b86) | Fedilinks (FEP-07d7) |
|--------|----------------------------|---------------------|
| Approach | Server-side | Client-side (browser) |
| Discovery | WebFinger lookup | `web+ap://` URI scheme |
| Browser changes | None required | Requires protocol handler registration |
| Adoption barrier | Server implements WebFinger links | Needs browser vendor support |
| Works today | Yes, with any browser | No — no AP implementations parse `web+ap://` URIs |
| Scope | All activity types + Object | Object navigation |

Ben Pate's key argument: Activity Intents are "handled by websites
themselves instead of relying on enhancements to browsers," enabling
incremental implementation without waiting for browser vendor adoption.

## Implementation Status

### Home Servers (Publishing Activity Intents)

| Implementation | Intents Published |
|---------------|-------------------|
| Emissary | Create, Follow, Like |
| Forte | Create |
| Loops | Follow |
| PieFed | Create |
| streams | Create |
| WordPress (ActivityPub plugin v7.6.0+) | Create, Follow |

### Client Implementations (Consuming Activity Intents)

| Implementation | Features |
|---------------|----------|
| Emissary | Share/like buttons on remote content |
| Forte | Wall-to-wall post/reply buttons |
| streams | Wall-to-wall functionality |
| Web Intents library | In development |

Mastodon has **not** implemented FEP-3b86. An open feature request exists
(issue #33984) but no developers are assigned.

## Implementation Guidance

### Publishing Activity Intents (Home Server)

1. Add Activity Intent links to your WebFinger JRD response
2. Use the `https://w3id.org/fep/3b86/*` namespace for `rel` values
3. Use RFC 6570 URI Templates in the `template` property
4. At minimum, publish **Follow** and **Create** intents (most useful)
5. Consider also publishing **Like**, **Announce**, and **Object** intents
6. Keep the existing oStatus subscribe link for backward compatibility

Example minimal WebFinger addition:

```json
{
  "links": [
    {
      "rel": "https://w3id.org/fep/3b86/Follow",
      "template": "https://yourserver.example/intents/follow?actor={object}"
    },
    {
      "rel": "https://w3id.org/fep/3b86/Create",
      "template": "https://yourserver.example/compose?text={content}&reply={inReplyTo}"
    }
  ]
}
```

### Implementing Intent Endpoints (Home Server)

1. Intent URLs are loaded via **GET** — display a confirmation page
2. Include a CSRF token in the confirmation form
3. The actual mutation happens via **POST** form submission
4. After completion, handle `on-success`:
   - If `(close)`, close the window (JavaScript `window.close()`)
   - If a URL, show an interstitial page with the destination
5. If the user cancels, handle `on-cancel` the same way
6. If the object is not found, show a 404 page — do NOT auto-redirect to
   `on-cancel` (open-redirect risk)

### Consuming Activity Intents (Remote Server)

1. When a user wants to interact with content, prompt for their Fediverse ID
2. Perform a WebFinger query for their ID
3. Look for the appropriate Activity Intent link in the response
4. If not found, fall back to oStatus subscribe, then hard-coded URLs
5. Substitute parameter values into the URI Template (percent-encode per
   RFC 3986)
6. Redirect the user to the constructed URL
7. Optionally include `on-success` and/or `on-cancel` callback URLs

## Known Issues and Open Questions

1. **DRAFT status** — FEP-3b86 has not reached FINAL; the spec may change
2. **Mastodon adoption unclear** — the largest Fediverse implementation has
   not committed to support
3. **Open redirect debate unresolved** — thisismissem proposed OAuth-style
   preregistered redirect URIs, which would be more secure but add complexity
4. **Limited client adoption** — only 3 implementations consume intents;
   most Fediverse software only displays intents for its own users
5. **No Undo/inverse UI pattern** — the spec defines Undo intent but
   doesn't address how to discover whether a user has already performed an
   action (e.g., already following, already liked)
6. **28 intents may be excessive** — most implementations only publish 1-3
   intents; many defined intents (Arrive, Travel, TentativeAccept) have no
   known implementations
