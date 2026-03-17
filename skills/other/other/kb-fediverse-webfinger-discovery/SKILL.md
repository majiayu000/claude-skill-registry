---
name: kb-fediverse-webfinger-discovery
description: >
  Background knowledge about reverse WebFinger discovery — finding a
  WebFinger address from an ActivityPub actor — based on FEP-2c59 (DRAFT
  status). Covers the `webfinger` property on actors, the forward vs
  reverse discovery problem, why `preferredUsername` is insufficient for
  reverse lookups, domain mismatch use cases, validation requirements
  (no-redirect string comparison), security considerations, JSON-LD
  context registration, the community debate around alternative approaches
  (`alsoKnownAs`, `aliases`, property naming), Mastodon's current reverse
  discovery algorithm and its limitations, and the W3C SWICG
  acknowledgment of the problem. Load when the user asks about reverse
  WebFinger discovery; how to get a WebFinger address from an actor URL;
  the `webfinger` property on ActivityPub actors; why `preferredUsername`
  is not enough for constructing WebFinger handles; domain mismatch
  between actor URL and WebFinger address; FEP-2c59; or how Mastodon
  resolves actor URLs back to `user@domain` handles.
user-invocable: false
---

# Reverse WebFinger Discovery (FEP-2c59) — Complete Reference

## Overview

WebFinger (RFC 7033) is the standard mechanism for discovering an
ActivityPub actor from a human-friendly address like `user@domain.example`.
The **forward direction** (WebFinger to actor) is well-defined. The
**reverse direction** (actor to WebFinger address) is not — and this causes
real problems across the Fediverse.

FEP-2c59 (authored by Evan Prodromou, received 2024-01-04, **status DRAFT**)
proposes adding a `webfinger` property to ActivityPub actor objects to solve
the reverse discovery problem explicitly.

## The Problem: Reverse Discovery Is Broken

### Forward Discovery (Well-Defined)

Converting `user@domain` to an actor URL is straightforward:

1. Construct the query: `https://domain/.well-known/webfinger?resource=acct:user@domain`
2. Parse the JRD (JSON Resource Descriptor) response
3. Extract the `href` from the link with `rel="self"` and an ActivityPub media type

### Reverse Discovery (Problematic)

Going the other direction — from an actor URL back to a `user@domain`
handle — has no standard mechanism. Current implementations reconstruct it
by extracting `preferredUsername` from the actor and combining it with the
hostname from the actor's `id` URL:

```
actor.preferredUsername + "@" + hostname(actor.id)
```

This approach has three fundamental problems:

1. **`preferredUsername` is optional** — it is not a required property in the
   ActivityPub specification, so it may be absent entirely.

2. **Domain mismatch** — organizations may want WebFinger addresses on a
   different domain than where their ActivityPub server runs. For example,
   `alice@company.tld` while the AP server is at `social.company.tld`. The
   current approach constructs `alice@social.company.tld` instead.

3. **Semantic overload** — `preferredUsername` serves double duty as both a
   display name preference and the WebFinger handle component, preventing it
   from serving either purpose cleanly.

The W3C Social Web Incubator Community Group (SWICG) acknowledged this
explicitly in their "ActivityPub and WebFinger" report:

> "Back-linking an actor to a WebFinger address could be more explicit.
> Current use of `preferredUsername` is not ideal for constructing WebFinger
> addresses, and it also does not allow for expressing actual 'preferred
> usernames'."

## The Solution: The `webfinger` Property

FEP-2c59 proposes that actors SHOULD include a `webfinger` property
containing their canonical WebFinger address.

### Wire Format

The address may be plain or use the `acct:` prefix:

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    "https://purl.archive.org/socialweb/webfinger"
  ],
  "type": "Person",
  "id": "https://social.example/users/alice",
  "preferredUsername": "alice",
  "webfinger": "alice@example.org"
}
```

Or with the `acct:` prefix:

```json
{
  "webfinger": "acct:alice@example.org"
}
```

Both forms are valid. The property is **functional** — at most one value per
actor.

### JSON-LD Context

The `webfinger` property is registered under:

```
https://purl.archive.org/socialweb/webfinger
```

Include this URL in the actor's `@context` array for proper JSON-LD
processing.

## Domain Mismatch Use Case

The motivating scenario for FEP-2c59:

An organization hosts its ActivityPub server at `social.company.tld` but
wants employees to have addresses like `alice@company.tld`. Today this works
via WebFinger redirects — `company.tld/.well-known/webfinger` redirects
queries to `social.company.tld/.well-known/webfinger`.

But Mastodon's reverse discovery constructs `alice@social.company.tld` (from
the actor URL hostname), not `alice@company.tld` (the intended address).

With FEP-2c59:

```json
{
  "type": "Person",
  "id": "https://social.company.tld/users/alice",
  "preferredUsername": "alice",
  "webfinger": "alice@company.tld"
}
```

The intended address is stated explicitly — no guessing required.

## Validation Requirements

When an implementation encounters a `webfinger` property, it MUST validate
the claim:

1. Perform a WebFinger lookup on the stated address
2. The JRD response MUST contain a `self` link whose `href` matches the
   actor's `id` URL **exactly**
3. **No redirects allowed** — the match must be a direct string comparison

### Why No Redirects

RFC 7033 (WebFinger) makes HTTP redirects mandatory to support. FEP-2c59
deliberately prohibits redirects during validation to simplify confirmation
to a string comparison. This was a point of contention in the community
discussion, with mro arguing it violates RFC 7033 semantics. Evan Prodromou
maintained that forbidding redirects makes validation unambiguous.

### Validation Example

Given an actor with `"webfinger": "alice@company.tld"` and
`"id": "https://social.company.tld/users/alice"`:

1. Query `https://company.tld/.well-known/webfinger?resource=acct:alice@company.tld`
2. Expect a JRD with a link:
   ```json
   {
     "subject": "acct:alice@company.tld",
     "links": [
       {
         "rel": "self",
         "type": "application/activity+json",
         "href": "https://social.company.tld/users/alice"
       }
     ]
   }
   ```
3. Confirm `href` equals the actor's `id` — validation passes

## Security Considerations

The `webfinger` property should only be trusted when:

- It comes from dereferencing the actor's `id` URL directly (i.e., you
  fetched the actor document from its authoritative origin)
- It is delivered with the actor's HTTP Signature via ActivityPub

A third party could spoof the `webfinger` property otherwise. For example,
if actor A delivers an activity containing actor B's profile with a modified
`webfinger` value, the recipient should not trust that claim without
independent verification.

Always validate the `webfinger` claim by performing the forward WebFinger
lookup and confirming the `self` link matches.

## Mastodon's Current Reverse Discovery

Mastodon does not implement FEP-2c59. It uses the `preferredUsername` +
hostname approach:

1. Extract `preferredUsername` and the hostname from the actor's `id` URL
2. Construct `acct:preferredUsername@hostname`
3. Perform a WebFinger lookup to verify the address resolves back to the
   same actor
4. If the JRD `subject` differs from the requested resource, follow up with
   another WebFinger request to the canonical subject

### Mastodon Username Rules

- Alphanumeric characters and underscores allowed anywhere
- Dots and dashes only in the middle (not at start or end)
- Case-insensitive
- Regex: `[a-z0-9_]+([a-z0-9_.-]+[a-z0-9_]+)?`

### When Mastodon's Approach Breaks

- `preferredUsername` is absent from the actor
- The WebFinger domain differs from the actor URL domain
- The actor URL uses subdomains or non-standard paths
- `preferredUsername` contains characters not valid in WebFinger handles

## Community Debate: Alternative Approaches

The SocialHub discussion revealed several alternative proposals:

### `alsoKnownAs` (stevebate)

Use the existing `alsoKnownAs` property with `acct:` URIs instead of adding
a new property. Evan Prodromou objected because Mastodon uses `alsoKnownAs`
for its `Move` (account migration) function — adding WebFinger addresses to
it could interfere with migration semantics.

### `aliases` from XRD/JRD (erincandescent)

Use the `aliases` array concept from WebFinger's JRD format:

```json
{
  "aliases": ["acct:bob@example.com"]
}
```

Advantages cited:
- Aligns WebFinger XRD/JRD values directly with ActivityStreams
- Semantics are already understood because everyone implements WebFinger
- Enables future extensibility for emerging identifier schemes (e.g., DIDs)
- More capable than a dedicated `webfinger` field

### Property Naming (trwnh)

Suggested renaming `webfinger` to `webfingerAcct` or `acct` for semantic
clarity, since the property specifically holds an `acct:` URI, not a generic
WebFinger resource.

## Related Specifications

| Specification | Relationship |
|--------------|-------------|
| RFC 7033 (WebFinger) | The underlying protocol; defines the `/.well-known/webfinger` endpoint and JRD format |
| RFC 7565 (`acct:` URI) | Defines the `acct:user@host` URI scheme used in WebFinger queries |
| FEP-d556 | Complementary proposal for **server-level** actor discovery via WebFinger (vs FEP-2c59's user-level focus) |
| W3C SWICG "ActivityPub and WebFinger" report | Acknowledges the reverse discovery problem; does not reference FEP-2c59 by name |

## Implementation Guidance

### If You Are Building a New ActivityPub Server

1. Include the `webfinger` property on all actor objects
2. Add `https://purl.archive.org/socialweb/webfinger` to the `@context`
3. Set the value to the canonical `user@domain` address (with or without
   `acct:` prefix)
4. Ensure your WebFinger endpoint returns a JRD with a `self` link pointing
   to the actor's `id` URL

### If You Are Consuming ActivityPub Actors

1. Check for the `webfinger` property first
2. If present, validate it by performing a forward WebFinger lookup and
   confirming the `self` link matches the actor's `id`
3. If absent, fall back to the `preferredUsername` + hostname approach
4. Always verify any constructed address via forward WebFinger lookup

### Defensive Parsing

- Accept both `"user@domain"` and `"acct:user@domain"` formats
- Strip the `acct:` prefix before display (users expect `user@domain`)
- Do not assume `preferredUsername` exists — it is optional
- Do not assume the WebFinger domain matches the actor URL domain

## Known Issues and Open Questions

1. **DRAFT status** — FEP-2c59 has not reached FINAL status; no
   implementations are listed in the FEP itself
2. **No-redirect controversy** — the prohibition on redirects during
   validation conflicts with RFC 7033's mandatory redirect support
3. **Property naming unresolved** — whether `webfinger`, `webfingerAcct`,
   or `acct` is the best name remains debated
4. **`aliases` alternative** — the community has not reached consensus on
   whether a dedicated property or the `aliases` approach is preferable
5. **Mastodon adoption unknown** — Mastodon has not indicated plans to
   adopt FEP-2c59
6. **JSON-LD context availability** — the
   `https://purl.archive.org/socialweb/webfinger` context document's
   long-term availability is not guaranteed

## WebFinger Protocol Quick Reference

For implementors who need a refresher on the underlying WebFinger protocol:

- **Endpoint**: `GET /.well-known/webfinger?resource=acct:user@domain`
- **Response**: JRD (JSON Resource Descriptor) with `subject`, optional
  `aliases`, and `links` array
- **Key link relation**: `rel="self"` with `type="application/activity+json"`
  (or `application/ld+json; profile="https://www.w3.org/ns/activitystreams"`)
  points to the ActivityPub actor URL
- **Standard**: RFC 7033 (IETF, 2013)
- **Not part of ActivityPub** — WebFinger is a convention the Fediverse
  adopted; the W3C ActivityPub spec does not mention it
