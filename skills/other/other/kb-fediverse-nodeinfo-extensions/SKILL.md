---
name: kb-fediverse-nodeinfo-extensions
description: >
  Background knowledge about capability and extension discovery via
  NodeInfo in the Fediverse. Covers FEP-6481 (WITHDRAWN — specifying
  ActivityPub extension support with NodeInfo metadata.activitypub.extensions
  IRI arrays), its successor FEP-9fde (reverse-FQDN operations map with
  semver versioning), and the broader capability discovery landscape
  including FEP-eb22 (supported ActivityStreams types), FEP-844e
  (capability URIs on application actors), and FEP-67ff (FEDERATION.md).
  Also covers the NodeInfo protocol itself (versions 1.0-2.1, the
  /.well-known/nodeinfo JRD endpoint, the metadata free-form section),
  nightpool's argument against custom types in favor of extending standard
  vocabulary, the XMPP Entity Capabilities precedent (XEP-0115), and
  real-world motivations from Manyfold (f3di 3D model extensions),
  BookWyrm (Review type), and Lemmy (voting vs Like). Load when the user
  asks about how to advertise supported ActivityPub extensions; NodeInfo
  metadata for capability discovery; FEP-6481; FEP-9fde; how servers
  discover what extensions a remote server supports; custom ActivityPub
  types and interoperability; the NodeInfo operations field; how to
  declare support for custom ActivityStreams types; capability negotiation
  between Fediverse servers; or whether to create custom types vs extend
  standard types.
user-invocable: false
---

# Fediverse Extension Discovery via NodeInfo — Complete Reference

## Overview

One of the unsolved problems in the Fediverse is **capability discovery**:
how does a server know what extensions, custom types, or features a remote
server supports? If Manyfold sends a 3D model activity to Mastodon,
Mastodon discards it silently. If Lemmy receives a Like from Mastodon, it
creates unnecessary traffic because Lemmy uses voting, not Like.

Several Fediverse Enhancement Proposals have attempted to solve this by
extending **NodeInfo** — the existing server metadata protocol — with
extension and capability declarations. The most notable was FEP-6481
(authored by James Smith / "Floppy," received 2024-03-12, **WITHDRAWN
2024-10-31**), which proposed a simple IRI list in NodeInfo metadata. It was
withdrawn in favor of FEP-9fde, which takes a broader approach.

This is an active area of development with no FINAL-status solution.

## NodeInfo: The Foundation

NodeInfo is a protocol for servers to publish metadata about themselves. It
originated in the **Diaspora** project (predating ActivityPub) and is
formalized in the Fediverse by FEP-f1d5 (status FINAL, revised as FEP-0151
in 2025).

### Discovery

Servers expose `/.well-known/nodeinfo` containing a JRD document:

```json
{
  "links": [
    {
      "rel": "http://nodeinfo.diaspora.software/ns/schema/2.1",
      "href": "https://example.social/nodeinfo/2.1"
    }
  ]
}
```

### Schema Versions

- **1.0** / **1.1** — initial versions
- **2.0** — significant revision
- **2.1** — current most widely deployed version

### Key Properties

| Property | Description |
|----------|-------------|
| `software` | Name, version, homepage, repository |
| `protocols` | Supported protocols (e.g., `["activitypub"]`) |
| `services` | Inbound and outbound service integrations |
| `openRegistrations` | Whether new accounts can be created |
| `usage` | User counts, local post count |
| `metadata` | **Free-form key-value pairs** — the extension point |

The `metadata` field is deliberately unstructured. The spec says: "Clients
should not rely on any specific key present." This is where extension
discovery proposals place their data.

## FEP-6481: Extension IRI List (WITHDRAWN)

FEP-6481 proposed the simplest approach: an array of IRIs in NodeInfo
metadata declaring which ActivityPub extensions a server supports.

### Wire Format

```json
{
  "version": "2.1",
  "protocols": ["activitypub"],
  "metadata": {
    "activitypub": {
      "extensions": [
        "https://w3id.org/manyfold/3dModel#v1",
        "https://joinbookwyrm.org/ns/activitypub#Review"
      ]
    }
  }
}
```

### Requirements

- Extension identifiers MUST be valid IRIs
- IRIs SHOULD include version information via fragment identifiers (`#v1`)
- Once defined, IRIs cannot change while maintaining compatibility
- Long-term persistent URI services (like w3id.org) are recommended

### Why It Was Created

James Smith ("Floppy") created **Manyfold**, a federated 3D model manager
that extends ActivityPub with the `f3di` namespace
(`http://purl.org/f3di/ns#`). When Manyfold sends activities with custom 3D
model types, servers like Mastodon silently discard them. There was no way
to discover in advance whether a remote server would understand the custom
types.

### Why It Was Withdrawn

Floppy withdrew FEP-6481 on 2024-10-31 in favor of **FEP-9fde** (by
nikclayton), which covers the same use case with broader scope. FEP-9fde
can express everything FEP-6481 proposed while also addressing client APIs,
federation features, and arbitrary server operations.

### Community Objections

**nightpool's strong objection**: "I strongly, strongly object to this
FEP." The argument:

- ActivityStreams 2.0 is designed to be extensible via JSON-LD — add extra
  properties to standard types (Note, Article, etc.) and servers that don't
  understand them simply ignore the extra fields
- Custom types (BookWyrm's `Review`, Manyfold's 3D model types) break
  graceful degradation because standard servers discard unrecognized types
  entirely
- Capability-based routing (sending different formats to different servers)
  fragments the ecosystem, increases complexity, and multiplies the testing
  surface

**stevebate's concerns**: the definition of "extension" was too vague;
fragment-based URI versioning (`#v1`) doesn't work with HTTP (fragments
aren't sent to servers); dereferenceable URIs should use path or query
parameter versioning instead.

**nutomic's reinterpretation**: saw it as a traffic filtering mechanism —
Lemmy could use it to tell servers "don't send me Like activities, I use
voting."

## FEP-9fde: Operations Map (Successor)

FEP-9fde (by nikclayton, DRAFT) extends NodeInfo with a standardized
`operations` property using reverse-FQDN identifiers and semantic
versioning.

### Wire Format

```json
{
  "operations": {
    "org.joinmastodon.api.statuses.post": ["1.0.0", "1.1.0", "2.0.0"],
    "app.manyfold.activitypub.accept.3dmodel": ["1.0.0"],
    "io.github.glitch-soc.api.statuses.bookmark": ["1.0.0"]
  }
}
```

### Key Differences from FEP-6481

| Aspect | FEP-6481 | FEP-9fde |
|--------|----------|----------|
| Scope | ActivityPub extensions only | Any server operation |
| Identifiers | IRIs with fragment versioning | Reverse-FQDN strings |
| Versioning | Fragment identifiers (`#v1`) | Semver arrays (`["1.0.0"]`) |
| Location | `metadata.activitypub.extensions` | `operations` property |
| Granularity | Per-extension | Per-operation |
| Status | WITHDRAWN | DRAFT |

### Design Rationale

FEP-9fde explicitly rejects several alternatives:
- **OpenAPI definitions** — too complex for clients
- **Hardcoded version mappings** — maintenance burden and version-locking
- **Capabilities flags** — combinatorial explosion as features interact
- **IRI identifiers** — case-sensitivity issues; reverse-FQDN avoids this

## The Broader Capability Discovery Landscape

Multiple proposals address the same fundamental problem:

### FEP-eb22: Supported ActivityStreams Types

Lists which Activity and Object types a server handles:

```json
{
  "activities": ["Create", "Update", "Delete", "Like", "Announce"],
  "objects": ["Note", "Article"],
  "properties": {}
}
```

Focuses on describing the standard ActivityStreams vocabulary a server
supports, rather than arbitrary extensions or operations.

### FEP-844e: Capability Discovery via Actors

Instead of using NodeInfo, attaches capability information to the
ActivityPub **application actor** itself. Based on FEP-aaa3 (listing
implemented specifications on the application actor). This keeps capability
data within the ActivityPub protocol rather than relying on the external
NodeInfo protocol.

### FEP-67ff: FEDERATION.md

A human-readable approach: servers include a `FEDERATION.md` file
documenting their federation behavior. Status FINAL. This solves the
documentation problem but not machine-readable discovery.

### Comparison

| FEP | Approach | Machine-readable? | Status |
|-----|----------|-------------------|--------|
| FEP-6481 | IRI list in NodeInfo metadata | Yes | WITHDRAWN |
| FEP-9fde | Reverse-FQDN operations in NodeInfo | Yes | DRAFT |
| FEP-eb22 | Type lists in NodeInfo | Yes | DRAFT |
| FEP-844e | Capability URIs on AP actors | Yes | DRAFT |
| FEP-67ff | FEDERATION.md documentation | No (human only) | FINAL |

## The Custom Types Debate

A fundamental philosophical question underlies all extension discovery
proposals: **should implementations create custom ActivityStreams types at
all?**

### The Case Against Custom Types (nightpool)

ActivityStreams 2.0 supports graceful degradation through JSON-LD:

- Add custom properties to standard types (`Note`, `Article`, etc.)
- Servers that understand the extensions use the extra data
- Servers that don't understand simply ignore unknown properties
- No capability discovery needed — everything is a standard type

Example: instead of a custom `Review` type, a BookWyrm review could be a
`Note` with additional `rating` and `reviewSubject` properties. Mastodon
would display it as a regular Note; BookWyrm would display it as a rich
review.

### The Case For Custom Types (Manyfold, BookWyrm)

Some extensions are fundamentally different from standard content:

- A 3D model is not meaningfully a "Note" — displaying it as plain text
  loses all value
- Domain-specific actions (accepting a 3D model upload) have no standard
  ActivityPub equivalent
- The receiving server needs to know it's getting specialized content to
  provide any useful experience

### The Practical Compromise

Manyfold's approach combines both:

1. Send standard activities with custom types to servers that declare
   support
2. Post "Compatibility Notes" (standard Note objects with
   `f3di:compatibilityNote: true`) describing the activity in text for
   servers that don't understand the custom types

This ensures content appears in all feeds while providing rich experiences
where supported.

## XMPP Precedent

The capability discovery problem is not new. XMPP solved it over two
decades ago with:

- **XEP-0115 (Entity Capabilities)**: servers and clients advertise
  supported features using a hash of their capability set. Efficient
  discovery without enumerating every feature on every connection.
- **XEP-0453 (DOAP)**: uses structured project descriptions (Description
  of a Project) to communicate capabilities.

These mature solutions demonstrate that capability discovery is solvable
but requires community consensus — something the Fediverse has not yet
achieved.

## Implementation Guidance

### If You Need Extension Discovery Today

1. **Use FEDERATION.md** (FEP-67ff, FINAL) to document your extensions
   in human-readable form
2. **Add NodeInfo metadata** for machine-readable discovery — use the
   FEP-9fde `operations` format if your framework supports it, or add
   custom metadata keys as a stopgap
3. **Always provide fallback content** — post standard Note/Article types
   alongside or instead of custom types for maximum compatibility
4. **Don't rely on capability routing** for critical functionality — the
   receiving server may not implement discovery

### If You Are Extending ActivityPub

Consider nightpool's argument carefully:

1. **Prefer extending standard types** with additional properties over
   creating entirely new types
2. If you must create custom types, also send **compatibility objects**
   (standard types with a text description) for servers that don't
   understand your extensions
3. Define a **JSON-LD context** for your extensions so they are properly
   namespaced
4. Register your extensions with a persistent IRI (w3id.org recommended)

### Checking Remote Server Capabilities

```
GET /.well-known/nodeinfo → follow link → check metadata/operations
```

But remember: most servers don't declare extension support yet. Absence
of a declaration does not necessarily mean absence of support.

## Known Issues and Open Questions

1. **No FINAL solution** — all machine-readable capability discovery
   proposals remain DRAFT or WITHDRAWN
2. **NodeInfo vs actor-based** — unresolved debate about whether capability
   data belongs in NodeInfo (server-level, protocol-agnostic) or on
   ActivityPub actors (protocol-native)
3. **Granularity tension** — FEP-9fde's per-operation approach can be
   verbose (Claire noted bookmarks alone require four operations);
   FEP-6481's per-extension approach may be too coarse
4. **Custom types vs extended standard types** — the community hasn't
   reached consensus on the right extensibility pattern
5. **Mastodon's alternative** — Mastodon introduced `api_versions` as a
   lighter-weight capability signal, potentially diverging from FEP-based
   approaches
6. **No implementations at scale** — FEP-9fde and FEP-eb22 lack widespread
   adoption; only Manyfold actively uses NodeInfo for extension declaration
