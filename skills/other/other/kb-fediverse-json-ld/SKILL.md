---
name: kb-fediverse-json-ld
description: >
  Background knowledge about how JSON-LD works on the Fediverse and in
  ActivityPub, including the difference between @id and id, @type and type
  (keyword aliasing via @context), the many forms a value can take (string,
  object with @value, object with @id, array, language-tagged value), the
  four JSON-LD document forms (compacted, expanded, flattened, framed),
  how @context works and when it is optional, why most Fediverse
  implementations treat JSON-LD as plain JSON and what breaks when they
  do, the content vs contentMap language map pattern, the functional vs
  non-functional property distinction, content type negotiation
  (application/activity+json vs application/ld+json), LD Signatures and
  JSON-LD canonicalization, Mastodon's @context structure and known bugs,
  and defensive parsing strategies. Load when the user asks about JSON-LD
  in ActivityPub, why @id and id are equivalent, how to handle value form
  variability, how to construct or interpret a @context, why a property
  can be a string or an array, how expansion or compaction works, how to
  add extensions to ActivityPub, content type headers for ActivityPub
  requests, or when reviewing or writing code that parses, produces, or
  transforms ActivityPub JSON-LD documents.
user-invocable: false
---

# Fediverse JSON-LD — Complete Reference

## Overview

ActivityPub and ActivityStreams 2.0 use JSON-LD as their data format.
JSON-LD (JSON for Linking Data) is a W3C standard that extends JSON with
semantic meaning by mapping property names to IRIs via a `@context`.

In practice, most Fediverse implementations **do not** perform full
JSON-LD processing. They treat ActivityPub messages as plain JSON,
looking up properties by their short names and ignoring the `@context`.
This mostly works but creates real interoperability problems around value
form variability, extensions, and namespace collisions.

Understanding both what JSON-LD specifies and what implementations
actually do is essential for building software that federates correctly.

---

## 1. `@id` vs `id`, `@type` vs `type` — Keyword Aliasing

### The ActivityStreams aliases

The ActivityStreams 2.0 context (`https://www.w3.org/ns/activitystreams`)
defines these aliases:

```json
{
  "id": "@id",
  "type": "@type"
}
```

This means `"id"` and `"@id"` are **semantically identical** in any
document using the ActivityStreams context, as are `"type"` and `"@type"`.
Both of these are valid and mean the same thing:

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "@id": "https://example.com/users/alice",
  "@type": "Person"
}
```

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://example.com/users/alice",
  "type": "Person"
}
```

The Fediverse overwhelmingly uses the **aliased forms** (`id`, `type`).
The `@`-prefixed forms are rarely seen in practice but are semantically
equivalent.

### Rules of keyword aliasing

- Any JSON-LD keyword can be aliased **except `@context` itself**
- An alias is defined in `@context` as `"myAlias": "@keyword"`
- The alias and the keyword are interchangeable in the document
- After JSON-LD expansion, aliases revert to their `@`-prefixed forms

### When implementing

Accept both forms. When producing documents, use the aliased forms
(`id`, `type`) for maximum compatibility with Fediverse software.

---

## 2. The `@context` — What It Does and When It's Optional

### Purpose

The `@context` maps short property names (terms) to full IRIs. It tells
a JSON-LD processor what each property means semantically:

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "type": "Note",
  "content": "Hello, world!"
}
```

Here, `@context` maps `"content"` to
`https://www.w3.org/ns/activitystreams#content` and `"Note"` to
`https://www.w3.org/ns/activitystreams#Note`.

### Three forms `@context` can take

**A single URL string:**
```json
"@context": "https://www.w3.org/ns/activitystreams"
```

**An inline object with term definitions:**
```json
"@context": {
  "@vocab": "https://www.w3.org/ns/activitystreams#",
  "toot": "http://joinmastodon.org/ns#"
}
```

**An array mixing URLs and objects:**
```json
"@context": [
  "https://www.w3.org/ns/activitystreams",
  "https://w3id.org/security/v1",
  {
    "toot": "http://joinmastodon.org/ns#",
    "Emoji": "toot:Emoji",
    "featured": "toot:featured"
  }
]
```

### When `@context` is optional

From a strict JSON-LD perspective, `@context` is **required** for any
JSON-LD processing — without it, expansion cannot occur.

However, ActivityStreams 2.0 was deliberately designed so that it
"conforms to a subset of JSON-LD syntax constraints but does not require
JSON-LD processing." Implementations that treat messages as plain JSON
can ignore `@context` and access properties by their short names.

In practice: the `@context` MUST be present in outgoing documents (other
implementations may need it), but your own code may not need to process
it if you only handle standard ActivityPub vocabulary.

---

## 3. The Many Forms a Value Can Take

This is the most practically important aspect of JSON-LD for Fediverse
implementers. Due to JSON-LD's data model, a single property value can
appear in many different forms — all semantically equivalent.

### Literal values

A plain string:
```json
"content": "Hello, world!"
```

A value object (explicit):
```json
"content": {"@value": "Hello, world!"}
```

A language-tagged value:
```json
"content": {"@value": "Hello, world!", "@language": "en"}
```

A typed value:
```json
"content": {"@value": "42", "@type": "http://www.w3.org/2001/XMLSchema#integer"}
```

### IRI references

As a string:
```json
"attributedTo": "https://example.com/users/alice"
```

As a node object:
```json
"attributedTo": {"id": "https://example.com/users/alice"}
```

Or with the `@` prefix:
```json
"attributedTo": {"@id": "https://example.com/users/alice"}
```

### Embedded objects

```json
"attributedTo": {
  "type": "Person",
  "id": "https://example.com/users/alice",
  "name": "Alice"
}
```

### Arrays

Any of the above can also appear inside an array:
```json
"tag": [
  {"type": "Hashtag", "name": "#cats"},
  {"type": "Mention", "href": "https://example.com/users/bob"}
]
```

Or as a single-element array:
```json
"inReplyTo": ["https://example.com/notes/1"]
```

### Mixed arrays

An array can contain a mix of strings and objects:
```json
"attributedTo": [
  "https://example.com/users/alice",
  {"@id": "https://example.com/users/bob"}
]
```

### Why this happens

JSON-LD compaction collapses single-element arrays to scalars. JSON-LD
expansion wraps all values in arrays and all strings in `@value` objects.
Different implementations may send data in different stages of this
pipeline, producing different surface representations of the same data.

---

## 4. Functional vs Non-Functional Properties

In the ActivityStreams vocabulary, some properties are marked as
**functional** — they can only have a single value. Non-functional
properties can have multiple values, meaning they may legally appear as
arrays.

After JSON-LD compaction, a non-functional property with one value is
collapsed to a scalar. But the array form is equally valid. This is the
root cause of bugs like Mastodon's `inReplyTo` crash (#25588) — the code
assumed `inReplyTo` would always be a string, but it arrived as an array.

**Rule:** Any property not explicitly marked functional in the
ActivityStreams vocabulary can appear as either a single value or an
array. Handle both.

---

## 5. Expansion and Compaction

These are the two key JSON-LD transformations. Understanding them
explains why the same data looks different from different servers.

### Expansion

Transforms a compacted document into a canonical, unambiguous form:

1. All property names become full IRIs
2. All values are wrapped in arrays
3. String/number values become `{"@value": ...}` objects
4. IRI references become `{"@id": ...}` objects
5. `@type` values become full IRIs inside an array
6. `@id` stays as a string (the only property that does NOT become an
   array)
7. The `@context` is removed — its information has been applied

**Compacted:**
```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://example.com/notes/1",
  "type": "Note",
  "content": "Hello",
  "attributedTo": "https://example.com/users/alice"
}
```

**Expanded:**
```json
[
  {
    "@id": "https://example.com/notes/1",
    "@type": ["https://www.w3.org/ns/activitystreams#Note"],
    "https://www.w3.org/ns/activitystreams#content": [
      {"@value": "Hello"}
    ],
    "https://www.w3.org/ns/activitystreams#attributedTo": [
      {"@id": "https://example.com/users/alice"}
    ]
  }
]
```

### Compaction

The reverse of expansion — applies a `@context` to:
- Shorten full IRIs back to short terms
- Collapse single-element arrays to scalar values
- Simplify `{"@value": "Hello"}` back to `"Hello"`

### Recommended processing workflow

1. **Expand** incoming documents to normalize them
2. **Process** the expanded data — all values are in predictable arrays
3. **Compact** before sending responses — make output human-readable

This approach dramatically simplifies parsing code because after
expansion, every property has a consistent structure.

---

## 6. The Four Document Forms

JSON-LD documents can appear in four forms:

### Compacted

Human-readable. Short property names from `@context`. Single-element
arrays collapsed to scalars. This is what ActivityPub implementations
typically produce and consume.

### Expanded

Canonical. Full IRI property names. All values in arrays. No `@context`.
Unambiguous but verbose. Used internally for processing.

### Flattened

All nodes collected into a single array under `@graph`. Nested objects
replaced with `@id` references. Blank nodes get generated identifiers.
Useful when you need a flat list of all nodes in the document.

### Framed

Data reshaped to match a developer-provided template ("frame").
Extracts specific structures from a graph. Rarely used in the Fediverse.

---

## 7. Language Maps — `content` vs `contentMap`

ActivityStreams defines paired properties for multilingual content:

| Plain | Language map | Purpose |
|---|---|---|
| `content` | `contentMap` | Post body (HTML) |
| `name` | `nameMap` | Display name / title |
| `summary` | `summaryMap` | Content warning text |

### Plain form

```json
"content": "Hello, world!"
```

### Language map form

```json
"contentMap": {
  "en": "Hello, world!",
  "es": "¡Hola, mundo!"
}
```

### The merging problem

In the ActivityStreams context, `content` and `contentMap` map to the
**same IRI** (`https://www.w3.org/ns/activitystreams#content`). The
`contentMap` version has `"@container": "@language"`. When a JSON-LD
processor encounters both `content` and `contentMap` on the same object,
it **merges** them because they resolve to the same IRI — which can
produce unexpected results.

### Mastodon's behavior

Mastodon sends both `content` and `contentMap`, but `contentMap` always
contains only a single language entry duplicating `content`. This is
redundant but harmless.

When consuming, prefer `contentMap` if available (it includes language
information). Fall back to `content` if `contentMap` is absent.

---

## 8. How Fediverse Implementations Handle JSON-LD

### The spectrum

| Approach | Implementations | How it works |
|---|---|---|
| Full JSON-LD processing | GoToSocial | Parses JSON-LD properly; maps IRIs to struct fields |
| Partial JSON-LD | Mastodon, Pleroma/Akkoma | Uses JSON-LD library for LD Signatures / canonicalization; otherwise treats as plain JSON |
| Plain JSON | Most others | Ignores `@context`; looks up properties by short name |

### Why most skip JSON-LD processing

1. **Complexity** — full JSON-LD processing is hard to implement
   correctly. The expansion algorithm alone can take weeks.
2. **Remote context fetching** — JSON-LD may reference remote context
   documents, introducing latency and security risks.
3. **Unnecessary for core vocabulary** — standard ActivityPub property
   names are stable and well-known. JSON-LD processing adds overhead
   without practical benefit for the base vocabulary.
4. **Mastodon compatibility** — most implementations just match
   Mastodon's output format rather than handling arbitrary JSON-LD.

### What breaks when you skip JSON-LD

1. **Extensions** — custom properties from other implementations' own
   `@context` entries may not be understood, or worse, may collide if
   two extensions use the same short name for different things.
2. **Value form variability** — an implementation expecting a string
   will crash on an array (Mastodon `inReplyTo` bug #25588).
3. **Namespace differences** — different implementations may use
   different short names for the same concept.

---

## 9. The `@context` in the Wild

### Mastodon's `@context`

Mastodon sends a multi-entry context array:

```json
"@context": [
  "https://www.w3.org/ns/activitystreams",
  "https://w3id.org/security/v1",
  {
    "toot": "http://joinmastodon.org/ns#",
    "Emoji": "toot:Emoji",
    "featured": "toot:featured",
    "featuredTags": "toot:featuredTags",
    "discoverable": "toot:discoverable",
    "manuallyApprovesFollowers": "as:manuallyApprovesFollowers",
    "schema": "http://schema.org#",
    "PropertyValue": "schema:PropertyValue",
    "value": "schema:value"
  }
]
```

### Known `@context` bugs

**Mastodon's `schema` mapping:** Mastodon maps `"schema"` to
`"http://schema.org#"` (note: HTTP, not HTTPS, and `#` instead of `/`).
The correct URI for schema.org is `"https://schema.org/"`. This means
JSON-LD processors using the correct schema.org context will fail to
process Mastodon profile fields (`PropertyValue`, `value`).

**ActivityStreams cyclical alias:** The ActivityStreams context defines
`"as": "https://www.w3.org/ns/activitystreams#"`, which creates a
cyclical reference (the context is itself at that namespace URL). Strict
JSON-LD processors may reject this.

### Adding extensions via `@context`

To add custom properties, add entries to the inline `@context` object:

```json
"@context": [
  "https://www.w3.org/ns/activitystreams",
  {
    "myExtension": "https://myserver.example/ns#",
    "customField": "myExtension:customField"
  }
]
```

Implementations that perform JSON-LD processing will resolve
`"customField"` to the full IRI
`"https://myserver.example/ns#customField"`. Implementations that ignore
`@context` will just look for `"customField"` by name.

---

## 10. Content Types

Three MIME types are associated with ActivityPub / JSON-LD:

| MIME Type | Purpose |
|---|---|
| `application/ld+json; profile="https://www.w3.org/ns/activitystreams"` | Full JSON-LD with ActivityStreams profile (MUST accept per spec) |
| `application/activity+json` | ActivityStreams-specific (SHOULD accept per spec) |
| `application/json` | Generic JSON (JSON-LD is valid JSON) |

### When sending

Use `Content-Type: application/activity+json` for outgoing activities
and responses.

### When fetching

Include both ActivityPub types in the `Accept` header:
```
Accept: application/activity+json, application/ld+json; profile="https://www.w3.org/ns/activitystreams"
```

---

## 11. JSON-LD and LD Signatures

JSON-LD processing is **required** for Linked Data Signatures, even in
implementations that otherwise ignore JSON-LD. The process:

1. Convert the JSON-LD document to canonical form using the URDNA2015
   (or similar) canonicalization algorithm
2. Hash the canonical form with SHA-256
3. Sign the hash with the actor's private key

This is used for activity forwarding (proving the original author) and
by some relays for message verification.

### Security: remote context loading

JSON-LD libraries may make HTTP requests to arbitrary domains when
loading remote `@context` documents. Implementations **must** use a
custom document loader that restricts context fetching to a known set of
URLs. At minimum, allow:

- `https://www.w3.org/ns/activitystreams`
- `https://w3id.org/security/v1`
- `https://w3id.org/identity/v1`

Block all other remote context loads to prevent SSRF and information
leakage.

### Signature type mismatch

Mastodon's LD Signature implementation uses `RsaSignature2017`. The
specification finalized as `RsaSignature2018`. HTTP Message Signatures
(RFC 9421) are gradually replacing LD Signatures for most use cases.

---

## 12. Defensive Parsing — What Correct Implementations Must Do

### For any property value, handle all forms

```
value := parseProperty(obj, "attributedTo")

// value could be:
//   "https://example.com/users/alice"              (string)
//   {"@id": "https://example.com/users/alice"}     (node ref)
//   {"id": "https://example.com/users/alice", ...} (embedded object)
//   ["https://example.com/users/alice"]             (array)
//   [{"@id": "..."}, "https://..."]                 (mixed array)
//   null / missing                                  (absent)
```

### Normalization strategy

1. If the value is a string, treat as-is (plain value or IRI depending
   on the property definition)
2. If the value is an object with `@id` or `id`, extract the IRI
3. If the value is an object with `@value`, extract the literal value
4. If the value is an array, apply the above rules to each element
5. If the value is null or missing, treat as absent
6. Never assume a property will always be a specific form

### Properties that commonly vary in form

| Property | May appear as |
|---|---|
| `inReplyTo` | string, array, object, null |
| `to` / `cc` | string, array |
| `tag` | object, array of objects |
| `attachment` | object, array of objects |
| `attributedTo` | string, object, array |
| `icon` / `image` | string, object, array |
| `url` | string, object, array |

---

## 13. Common Implementation Mistakes

- **Assuming `id` and `@id` are different properties**: they are
  aliases in the ActivityStreams context — identical semantically.
  Accept both, produce `id`
- **Assuming a property is always a string**: any non-functional
  property can arrive as an array. Any IRI-valued property can arrive
  as `{"@id": "..."}` instead of a plain string
- **Not including `@context` in outgoing documents**: even if your
  implementation ignores it, others may need it. Always include at
  least `"@context": "https://www.w3.org/ns/activitystreams"`
- **Fetching remote contexts without restrictions**: JSON-LD libraries
  will load arbitrary URLs unless constrained by a custom document
  loader — this is both a performance and security risk
- **Using `@id` and `@type` in outgoing documents**: use the aliased
  forms (`id`, `type`) for compatibility with implementations that
  match on property name without JSON-LD processing
- **Ignoring `contentMap`**: if present, it carries language
  information that `content` alone does not. Prefer `contentMap` when
  available
- **Not handling the `@context` array form**: `@context` can be a
  string, object, or array — don't assume a specific shape if you
  need to inspect it
- **Hardcoding Mastodon's `@context`**: other implementations send
  different contexts. If you must inspect `@context`, handle variation
- **Treating `content` and `contentMap` as independent**: in JSON-LD
  they map to the same IRI and will merge during expansion — be aware
  of this if you perform JSON-LD processing
