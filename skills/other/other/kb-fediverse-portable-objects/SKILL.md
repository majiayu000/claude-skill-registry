---
name: kb-fediverse-portable-objects
description: >
  Background knowledge about FEP-ef61 Portable Objects and server-independent
  identity in ActivityPub, including the ap:// URI scheme with DIDs as
  authority, the did:key and did:ap:key DID methods, the gateway and resolver
  mechanism (/.well-known/apgateway), the gateways property on portable
  actors, integrity proofs (FEP-8b32 / eddsa-jcs-2022), origin-based
  authentication (FEP-fe34), identity proofs (FEP-c390), media integrity
  via digestMultibase, backward compatibility with HTTP(S) URLs, the
  aliases vs alsoKnownAs property debate, and the relationship to nomadic
  identity (Zot/Nomad/Hubzilla/Streams). Also covers the decentralized
  identity stack (FEP-521a, FEP-8b32, FEP-c390, FEP-ef61) and
  implementations in Streams, Mitra, Forte, and tootik. Load when the user
  asks about portable objects, portable identity, nomadic identity,
  server-independent identifiers, ap:// URIs, DIDs in ActivityPub, account
  migration beyond Move, data portability, what happens when a server shuts
  down, FEP-ef61, or how to make ActivityPub objects survive server changes.
user-invocable: false
---

# Fediverse Portable Objects (FEP-ef61) — Complete Reference

## Overview

Standard ActivityPub ties every object's identity to a specific server URL
(e.g., `https://mastodon.social/users/alice/statuses/12345`). If that server
shuts down, all its objects — posts, profiles, media — become permanently
unreachable. The existing `Move` activity only migrates followers, not posts,
likes, bookmarks, or other data.

FEP-ef61 (authored by silverpill, received 2023-12-06, status DRAFT) solves
this by introducing **server-independent identifiers** for ActivityPub
objects. Instead of HTTPS URLs, objects are identified by `ap://` URIs where
the authority component is a Decentralized Identifier (DID). Objects can be
served by any gateway server, and migration is just a matter of changing
which gateway serves them — the identity stays the same.

The concept descends from **nomadic identity**, pioneered over a decade ago
by Mike Macgirvin in the Zot protocol (Hubzilla) and Nomad protocol
(Streams). FEP-ef61 brings this capability to ActivityPub using W3C
standards: Decentralized Identifiers (DIDs) and Verifiable Credential Data
Integrity.

---

## 1. The `ap` URI Scheme

Portable objects use `ap://` URIs instead of `https://` URLs. The URI
follows RFC 3986 with a DID as the authority:

```
ap://did:key:z6MkrJVnaZkeFzdQyMZu1cgjg7k1pZZ6pvBQ7XJPt4swbTQ2/actor
```

Components:
- **Scheme**: `ap`
- **Authority**: A valid DID (percent-encoding permitted)
- **Path**: Required, treated as opaque
- **Query/Fragment**: Optional

A single DID subject can control multiple actors or objects, differentiated
by the path component. The DID represents the identity; the path represents
a resource owned by that identity (e.g., `/actor`, `/posts/123`).

---

## 2. Decentralized Identifiers (DIDs)

DIDs are a W3C standard (2022) providing globally unique identifiers that
do not depend on any central registry or server. Format:

```
did:<method>:<method-specific-id>
```

### `did:key`

The simplest DID method — encodes the public key directly in the identifier:

```
did:key:z6MkrJVnaZkeFzdQyMZu1cgjg7k1pZZ6pvBQ7XJPt4swbTQ2
```

- The `z` prefix indicates base58-btc Multibase encoding
- No resolution infrastructure needed — the public key IS the identifier
- Implementations MUST support `did:key` with base58-btc

### `did:ap:key`

FEP-ef61 evolved from `did:apkey` to `did:ap:key`, positioning `did:ap` as
a namespace that can support multiple constructions:
- `did:ap:key` — wraps `did:key`
- `did:ap:web` — wraps `did:web`
- `did:ap:pkh` — wraps `did:pkh`

The `did:ap` resolution algorithm: remove the `:ap` segment and resolve the
remaining DID using its native method.

**Community debate**: bumblefudge argued that nesting DIDs within DIDs
"breaks the spirit" of the DID specification. silverpill defended it as a
legitimate resolution algorithm that the spec doesn't prohibit.

---

## 3. Gateways — How Portable Objects Are Served

Since `ap://` URIs cannot be fetched directly via HTTP, portable objects are
served through **gateway** servers.

### The `gateways` property

Portable actors MUST include a `gateways` property listing HTTP(S) URLs
where the current version of the actor can be fetched:

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    "https://w3id.org/security/data-integrity/v1"
  ],
  "type": "Person",
  "id": "ap://did:key:z6MkrJVnaZkeFzdQyMZu1cgjg7k1pZZ6pvBQ7XJPt4swbTQ2/actor",
  "gateways": [
    "https://server-a.example",
    "https://server-b.example"
  ]
}
```

**Migration**: To move to a new server, update the `gateways` list. The
`ap://` identity stays the same. Old gateways can be removed once migration
is complete.

### Dereferencing via `/.well-known/apgateway`

Clients fetch portable objects through the gateway's well-known endpoint:

```
GET https://server-a.example/.well-known/apgateway/did:key:z6Mk.../actor
```

The URL is constructed by:
1. Taking the `ap://` URI
2. Removing the `ap://` prefix
3. Appending the remainder to the gateway's `/.well-known/apgateway/` path

### Multiple gateways

Multiple gateways provide redundancy — if one server goes down, the object
is still reachable through another. This is the core of how FEP-ef61
prevents data loss from server shutdowns.

---

## 4. Integrity Proofs (FEP-8b32) — Required Dependency

All portable objects MUST include cryptographic integrity proofs so
consumers can verify they weren't tampered with, regardless of which
gateway served them. FEP-8b32 defines how this works:

### Signing process

1. **Canonicalize** the ActivityPub object using JSON Canonicalization
   Scheme (JCS, RFC 8785) for deterministic serialization
2. **Hash** the canonicalized output with SHA-256
3. **Construct** a `DataIntegrityProof` specifying `eddsa-jcs-2022`
   (EdDSA signing with SHA-256 hashing and JCS canonicalization)
4. **Concatenate** the proof hash and document hash
5. **Sign** with EdDSA and encode the 64-byte signature as Multibase

### Verification

1. Extract the `proof` from the object
2. Reconstruct the document hash (without the proof)
3. Reconstruct the proof hash
4. Verify the signature against the public key derived from the DID

### Example proof structure

```json
{
  "proof": {
    "type": "DataIntegrityProof",
    "cryptosuite": "eddsa-jcs-2022",
    "verificationMethod": "did:key:z6MkrJVnaZkeFzdQyMZu1cgjg7k1pZZ6pvBQ7XJPt4swbTQ2",
    "proofPurpose": "assertionMethod",
    "created": "2024-01-15T12:00:00Z",
    "proofValue": "z..."
  }
}
```

This is what makes objects truly portable — anyone can verify the object
came from the claimed identity, regardless of which server delivered it.

---

## 5. Authentication — Origin-Based Security (FEP-fe34)

FEP-ef61 uses an origin-based security model from FEP-fe34. The
**cryptographic origin** (the DID in the `ap://` URI) must match the
signing key. This replaces the traditional model where the HTTPS domain
of the URL is the trust anchor.

For traditional ActivityPub, authentication works like:
- Object ID is `https://server.example/post/123`
- Trust anchor is `server.example` (the domain)
- HTTP Signatures prove the request came from that domain

For portable objects:
- Object ID is `ap://did:key:z6Mk.../post/123`
- Trust anchor is `did:key:z6Mk...` (the cryptographic key)
- Integrity proofs (FEP-8b32) prove the object was created by the key holder
- Any gateway can serve it — the gateway is not the trust anchor

---

## 6. Identity Proofs (FEP-c390)

FEP-c390 links ActivityPub actor profiles to their canonical DID identities.
Actors embed `VerifiableIdentityStatement` objects in their `attachment`
array, cryptographically proving the relationship between the HTTPS actor
URL and the DID:

```json
{
  "type": "Person",
  "id": "https://server.example/users/alice",
  "attachment": [
    {
      "type": "VerifiableIdentityStatement",
      "subject": "did:key:z6MkrJVnaZkeFzdQyMZu1cgjg7k1pZZ6pvBQ7XJPt4swbTQ2",
      "proof": {
        "type": "DataIntegrityProof",
        "cryptosuite": "eddsa-jcs-2022",
        "verificationMethod": "did:key:z6MkrJVnaZkeFzdQyMZu1cgjg7k1pZZ6pvBQ7XJPt4swbTQ2",
        "proofPurpose": "assertionMethod",
        "proofValue": "z..."
      }
    }
  ]
}
```

This enables a bridge between the traditional HTTPS-based ActivityPub world
and the portable `ap://` world.

---

## 7. Public Key Representation (FEP-521a)

FEP-521a modernises how public keys are represented on actors. Instead of
the legacy `publicKey` + PEM encoding pattern, it uses:

- **`assertionMethod`** property (from Verifiable Credential Data Integrity)
- **Multibase** encoding with `publicKeyMultibase`
- Single-character prefix: `z` = base58-btc (recommended), `u` = base64-url

This replaces verbose PEM encoding and eliminates the need for ASN.1 DER
parsing libraries.

---

## 8. Media Integrity

External resources (images, video, audio) attached to portable objects
MUST include `digestMultibase` properties containing SHA-256 hashes:

```json
{
  "type": "Image",
  "url": "https://server.example/media/photo.jpg",
  "digestMultibase": "zQm..."
}
```

This allows:
- Verification that media hasn't been tampered with
- Content-addressed retrieval through any gateway
- Hashlinks as resource URIs for integrity verification

---

## 9. Backward Compatibility

FEP-ef61 addresses the practical challenge that most existing ActivityPub
software only understands HTTPS URLs.

### Gateway-based HTTP(S) URLs

Publishers construct backward-compatible URLs using the **first gateway**
in the `gateways` list:

```
https://server-a.example/.well-known/apgateway/did:key:z6Mk.../actor
```

Existing software can fetch this URL normally. Software that understands
`ap://` URIs strips the gateway prefix and reconstructs the canonical
`ap://` form.

### The `aliases` property

Portable objects may include an `aliases` property listing alternative
identifiers (including HTTPS URLs) for the same resource.

**Note**: silverpill chose `aliases` instead of `alsoKnownAs` because of a
semantic conflict. In the DID specification, `alsoKnownAs` means "different
identifiers for the same resource." In Mastodon's usage, it means "different
subjects with the same controller" (for account migration). trwnh documented
that while DID WG and SWICG agreed in 2021 to use `as:alsoKnownAs`,
Mastodon's pre-existing usage created incompatible semantics. The `aliases`
property may be extracted into a separate FEP (FEP-d2da, pre-draft).

---

## 10. The Full Decentralized Identity Stack

These FEPs work together to enable portable objects:

| FEP | Name | Role |
|---|---|---|
| FEP-521a | Public Key Representation | Multibase key encoding on actors |
| FEP-8b32 | Object Integrity Proofs | Cryptographic signing of objects (eddsa-jcs-2022) |
| FEP-c390 | Identity Proofs | Linking HTTPS actors to DIDs via VerifiableIdentityStatement |
| FEP-fe34 | (unnamed) | Origin-based security model |
| FEP-ef61 | Portable Objects | Server-independent `ap://` identifiers with gateway resolution |

The dependency chain: FEP-ef61 requires FEP-8b32 (integrity proofs) and
FEP-fe34 (origin-based auth). FEP-8b32 requires FEP-521a (key
representation). FEP-c390 bridges traditional and portable identity.

---

## 11. Relationship to Nomadic Identity (Zot/Nomad)

FEP-ef61 is the ActivityPub equivalent of nomadic identity, which was
pioneered over a decade ago:

| | Zot/Nomad (Hubzilla/Streams) | FEP-ef61 (ActivityPub) |
|---|---|---|
| Identity model | Channel-based, server-independent | DID-based, server-independent |
| Object IDs | Server-independent | `ap://` URIs with DID authority |
| Multi-homing | Native (clone channels across servers) | Via `gateways` property |
| Integrity | Protocol-level | FEP-8b32 Data Integrity proofs |
| Migration | Seamless (nomadic) | Update gateways list |
| Adoption | Hubzilla, Streams only | Growing (Streams, Mitra, Forte, tootik) |

Mike Macgirvin (creator of Zot/Nomad/Hubzilla/Streams) implemented FEP-ef61
in Streams, making it the first platform to support nomadic identity over
ActivityPub. Streams and Mitra are collaborating on the first cross-platform
implementation.

silverpill prefers the terms "cryptographic identity" or "key-based identity"
over "nomadic identity" — the key insight being that "the combination of
cryptographic identity and cryptographic integrity proofs makes objects
portable."

---

## 12. Implementation Matrix

| Platform | FEP-ef61 Support | Details |
|---|---|---|
| Streams | Full | First to implement; built by Mike Macgirvin (Zot/Nomad creator) |
| Mitra | Gateway | Gateway config (disabled by default), resolver endpoint, portable inboxes/outboxes with DID signatures, portable Like activities |
| Forte | Noted | Listed as implementation |
| tootik | Noted | Listed as implementation |
| fep-ae97-client | Client | Client-side implementation |
| Fedify | Requested | Feature request (issue #288); FEP-8b32 dependency already available |
| Hollo | Requested | Feature request (issue #211) |
| Mastodon | None | No current support or announced plans |

---

## 13. Comparison with Other Portability Approaches

### `Move` activity (current Mastodon approach)

The `Move` activity only migrates followers. Posts, likes, bookmarks,
lists, and media remain on the old server. If the old server shuts down,
all that data is lost. There is no standard for cross-implementation
migration.

### LOLA (Linked Open Local Authority)

LOLA is a separate specification from the W3C Social Web Incubator
Community Group focused on data export/import for migration. It addresses
the practical need to move accounts in response to moderation decisions,
server shutdowns, or policy changes. LOLA and FEP-ef61 are complementary:
LOLA focuses on data portability (moving data between servers), while
FEP-ef61 focuses on identity portability (objects that don't need to move
because they were never tied to a server).

### Domain-based resolution

An alternative approach where users control a domain that maps to their
actual host (similar to DNS). Simpler than DIDs but still ties identity to
domain ownership, which has its own costs and failure modes.

---

## 14. Known Issues and Open Questions

- **Retrofitting existing objects**: Existing ActivityPub objects already
  have HTTPS URLs as identifiers. There is no practical way to convert them
  to `ap://` URIs retroactively across the entire network.
- **`did:ap` method registry**: The `did:ap:key` syntax (nesting DID
  methods) is controversial. Whether `did:ap` can be registered as a
  formal DID method is debated.
- **`aliases` vs `alsoKnownAs`**: The property naming conflict between DID
  and Mastodon semantics is unresolved. FEP-d2da (pre-draft) proposes
  extracting `aliases` into its own FEP.
- **Mastodon adoption**: Mastodon has not signalled plans to support
  portable objects, and its dominant market position means most fediverse
  users cannot benefit from FEP-ef61 yet.
- **Complexity**: The full stack (FEP-521a + FEP-8b32 + FEP-c390 +
  FEP-fe34 + FEP-ef61) is substantially more complex to implement than
  traditional HTTP Signatures + HTTPS URLs.
- **Gateway trust**: While integrity proofs ensure objects aren't tampered
  with, gateway availability and censorship resistance are separate
  concerns not fully addressed by the FEP.
