---
name: kb-fediverse-federation-md
description: >
  Background knowledge about FEP-67ff FEDERATION.md, the convention for
  documenting federation behavior in Fediverse projects. Covers the
  specification requirements (valid Markdown, repository root location),
  suggested template sections (protocols, FEPs, ActivityPub details),
  machine-readable discovery via NodeInfo 2.1 software.repository, the
  companion FEP-c893 (DOAP JSON-LD for automated capability discovery),
  the origin story (Darius Kazemi's 2020 proposal, WriteFreely as first
  adopter), the interoperability documentation gap FEDERATION.md solves,
  real-world examples from Mastodon and WordPress, and the 40+
  implementations that have adopted it. Load when the user asks about
  FEDERATION.md; how to document federation behavior; FEP-67ff; what
  protocols or FEPs a project supports; how to create interoperability
  documentation for a Fediverse project; how other projects document
  their ActivityPub implementation; or machine-readable federation
  capability discovery with DOAP.
user-invocable: false
---

# FEDERATION.md (FEP-67ff) — Complete Reference

## Overview

FEDERATION.md is a convention for documenting how a project implements
federation protocols. Formalized as FEP-67ff (authored by silverpill,
status FINAL, finalized 2024-09-22), it provides a standardized location
and format for interoperability documentation — analogous to README.md for
project description or CONTRIBUTING.md for contributor guidelines.

The convention originated in January 2020 when Darius Kazemi (creator of
gath.io) proposed a standard documentation file after struggling to
understand how other servers handled federation. It grew organically to
12+ implementations before silverpill formalized it as a FEP in April 2023.
Over 40 projects have now adopted it, including Mastodon, Pixelfed, Lemmy,
WordPress ActivityPub, GoToSocial, and PeerTube.

---

## 1. Specification Requirements (RFC 2119)

Only two hard requirements:

1. It **MUST** be a valid Markdown document
2. It **MUST** be located in the root of a project's code repository (or,
   if documentation is located elsewhere, contain a link to that location)

Soft requirements (SHOULD):

- It **SHOULD** enumerate implemented federation protocols and standards
- It **SHOULD** list supported Fediverse Enhancement Proposals (FEPs)

The file "can have arbitrary structure and content" — the spec deliberately
avoids mandating a rigid format, allowing each project to document what
matters most for its federation behavior.

---

## 2. Suggested Template

The specification provides a reference template with these sections:

### Supported Federation Protocols and Standards

List the protocols the project implements:

```markdown
## Supported federation protocols and standards

- [ActivityPub](https://www.w3.org/TR/activitypub/) (Server-to-Server)
- [WebFinger](https://webfinger.net/)
- [HTTP Signatures](https://datatracker.ietf.org/doc/html/draft-cavage-http-signatures)
- [NodeInfo](https://nodeinfo.diaspora.software/)
```

### Supported FEPs

List adopted Fediverse Enhancement Proposals:

```markdown
## Supported FEPs

- [FEP-67ff: FEDERATION.md](https://codeberg.org/fediverse/fep/src/branch/main/fep/67ff/fep-67ff.md)
- [FEP-f1d5: NodeInfo in Fediverse Software](https://codeberg.org/fediverse/fep/src/branch/main/fep/f1d5/fep-f1d5.md)
```

### ActivityPub-Specific Documentation

Detailed sections covering:
- Profiles / actors
- Posts / objects
- Addressing and delivery
- Content limits
- Non-standard extensions
- Known interoperability quirks

---

## 3. The Problem FEDERATION.md Solves

ActivityPub is a protocol specification that leaves many implementation
details up to individual servers. Different implementations make different
choices about:

- Which Activity types they handle (some ignore Like, some ignore Announce)
- How they represent custom content (BookWyrm reviews, Lemmy votes,
  Pixelfed photos)
- What non-standard extensions they require (Mastodon's HTTP Signature
  requirements)
- How they handle edge cases (username changes, content limits, private
  posts)

Before FEDERATION.md, the only way to understand another implementation's
behavior was to read their source code, reverse-engineer through testing,
or ask on forums. This was particularly painful because the Fediverse has
dozens of implementations in different programming languages.

FEDERATION.md provides a single, predictable file location where developers
can find all federation-relevant documentation. By placing it at the
repository root as a Markdown file, it follows established open-source
conventions (like README.md, CONTRIBUTING.md, LICENSE) and is immediately
accessible via any code hosting platform.

---

## 4. Real-World Examples

### Mastodon's FEDERATION.md

Mastodon's file documents:

- **Protocols**: ActivityPub (S2S), WebFinger, HTTP Signatures, NodeInfo
- **FEPs**: FEP-67ff, FEP-f1d5, FEP-8fcf, FEP-5feb, FEP-044f, and others
- **Detailed sections**: profiles/actors, posts, addressing, content limits,
  non-standard extensions
- Notes that Mastodon "largely follows the ActivityPub server-to-server
  specification but makes use of some non-standard extensions, some of which
  are required for interacting with Mastodon at all"

### WordPress ActivityPub Plugin's FEDERATION.md

Documents support for:

- ActivityPub S2S, WebFinger, HTTP Signatures, NodeInfo
- Various FEPs including FEP-67ff itself and FEP-3b86 (Activity Intents)
- Notes that it "largely follows ActivityPub's server-to-server
  specification, but makes use of some non-standard extensions"

Both files follow a similar structure — protocols section, FEPs section,
then detailed ActivityPub documentation — but neither uses a rigid template.
They adapted the convention to their needs.

---

## 5. Machine-Readable Discovery

### Via NodeInfo 2.1

FEDERATION.md files can potentially be discovered automatically via
NodeInfo 2.1's `software.repository` field, which points to the project's
source code repository. A crawler could follow this link and look for
FEDERATION.md at the repository root.

```json
{
  "software": {
    "name": "mastodon",
    "version": "4.3.0",
    "repository": "https://github.com/mastodon/mastodon"
  }
}
```

From this, a tool can construct:
`https://github.com/mastodon/mastodon/blob/main/FEDERATION.md`

### Limitation

This approach requires the `software.repository` field (added in NodeInfo
2.1) and depends on the repository being publicly accessible. Many
instances run forks or customized versions where the repository URL may
not point to the right FEDERATION.md.

---

## 6. The DOAP Companion: FEP-c893

FEP-c893 (by AvidSeeker, status DRAFT, received July 2024) proposes a
`doap.jsonld` file as a machine-readable companion to FEDERATION.md.

### What DOAP Provides

A JSON-LD file using the DOAP (Description of a Project) vocabulary:

```json
{
  "@context": {
    "doap": "http://usefulinc.com/ns/doap#",
    "foaf": "http://xmlns.com/foaf/0.1/"
  },
  "@type": "doap:Project",
  "doap:name": "Example Server",
  "doap:homepage": "https://example.com",
  "doap:description": {
    "@language": "en",
    "@value": "A federated social media server"
  },
  "doap:implements": [
    "https://www.w3.org/TR/activitypub/",
    "https://webfinger.net/"
  ],
  "doap:supportedFEPs": [
    "https://codeberg.org/fediverse/fep/src/branch/main/fep/67ff/fep-67ff.md"
  ],
  "doap:maintainer": {
    "@type": "foaf:Person",
    "foaf:name": "Alice Developer"
  }
}
```

### Key Fields

| Field | Purpose |
|-------|---------|
| `doap:name` | Project name |
| `doap:homepage` | Project website |
| `doap:description` | Multilingual description |
| `doap:repository` | Repository URLs |
| `doap:release` | Version and date information |
| `doap:implements` | Federation protocols supported |
| `doap:supportedFEPs` | Adopted FEPs |
| `doap:maintainer` | Project maintainers |

### Relationship to FEP-67ff

FEP-c893 is the machine-readable counterpart to FEP-67ff's human-readable
FEDERATION.md. Together they provide both developer documentation and
automated capability discovery. This pairing was inspired by XMPP's
XEP-0453, which uses the same DOAP vocabulary for capability reporting.

---

## 7. Writing a FEDERATION.md

### Step-by-Step Guide

1. **Create the file** at the root of your project repository

2. **List supported protocols**:
   - ActivityPub (specify Server-to-Server, Client-to-Server, or both)
   - WebFinger
   - HTTP Signatures (specify draft version)
   - NodeInfo (specify schema version)
   - Any other protocols (Diaspora, Zot, OStatus, etc.)

3. **List supported FEPs** with links to the FEP specifications

4. **Document ActivityPub behavior** — this is the most valuable section:
   - What Activity types your server sends and accepts
   - What Object types your server creates and understands
   - How inbox processing works for each Activity type
   - Non-standard extensions or properties your server uses
   - Known interoperability issues with specific implementations

5. **Document addressing and delivery**:
   - How public/followers-only/direct addressing works
   - Shared inbox support
   - Relay support

6. **Note known limitations**:
   - Activity types that are silently ignored
   - Content types that receive degraded display
   - Extension requirements for full interoperability

### Best Practices

- **Keep it updated** — outdated documentation is worse than no
  documentation, because it misleads implementers
- **Be specific about non-standard behavior** — if your server requires
  something not in the ActivityPub spec (like Mastodon's HTTP Signature
  requirements), document it prominently
- **Include wire-format examples** — JSON examples of actual activities
  your server sends and expects are more useful than prose descriptions
- **Document what you ignore** — knowing that a server silently drops
  Like activities (like Lemmy does with standard Likes) saves implementers
  debugging time

---

## 8. Origin and History

### Darius Kazemi's 2020 Proposal

In January 2020, Darius Kazemi (creator of gath.io, a federated event
organizing service, and Fellow at the Berkman Klein Center for Internet
& Society) proposed FEDERATION.md on SocialHub. He had been implementing
federation for gath.io and felt implementers needed better documentation
on server behavior.

His original FEDERATION.md had three sections:
1. Federation philosophy
2. Inbox behavior (what the server does when receiving various activities)
3. Web application-triggered activities (what the server sends in response
   to user actions)

### Early Adoption Timeline

| Date | Event |
|------|-------|
| January 5, 2020 | Darius Kazemi proposes FEDERATION.md on SocialHub |
| January 9, 2020 | WriteFreely becomes first adopter |
| February 4, 2020 | Zot (Hubzilla family) adopts |
| February 8, 2020 | Discussed at W3C Social CG meeting |
| March–October 2020 | tavern, Smithereen, Lemmy adopt |
| April 2023 | silverpill proposes FEP-67ff (~12 implementations) |
| September 5, 2023 | FEP-67ff received as DRAFT |
| September 22, 2024 | FEP-67ff achieves FINAL status |
| Present | 40+ implementations |

### Key Observation

The convention grew organically for over 3 years before being formalized
as a FEP. This "convention first, spec second" approach means FEP-67ff
codified existing practice rather than inventing new requirements — a
pattern that contributed to its successful adoption and FINAL status.

---

## 9. Implementations

Over 40 projects have adopted FEDERATION.md, including:

| Project | Category |
|---------|----------|
| Mastodon | Microblogging |
| Pleroma / Akkoma | Microblogging |
| GoToSocial | Microblogging |
| Pixelfed | Photo sharing |
| PeerTube | Video sharing |
| Lemmy | Link aggregation |
| BookWyrm | Book reviews |
| WriteFreely | Long-form writing |
| Friendica | Social networking |
| Hubzilla | Social networking |
| Funkwhale | Music sharing |
| WordPress ActivityPub | Blogging plugin |
| Mitra | Microblogging |
| Smithereen | Social networking |
| Bonfire | Social networking |

---

## 10. Capability Discovery Landscape

FEDERATION.md addresses documentation but not machine-readable discovery.
Several other FEPs tackle the machine-readable side:

| FEP | Approach | Machine-readable? | Status |
|-----|----------|-------------------|--------|
| FEP-67ff | FEDERATION.md documentation | No (human only) | FINAL |
| FEP-c893 | DOAP JSON-LD companion file | Yes | DRAFT |
| FEP-6481 | IRI list in NodeInfo metadata | Yes | WITHDRAWN |
| FEP-9fde | Reverse-FQDN operations in NodeInfo | Yes | DRAFT |
| FEP-eb22 | Type lists in NodeInfo | Yes | DRAFT |
| FEP-844e | Capability URIs on AP actors | Yes | DRAFT |

FEP-67ff is the only capability-related FEP to reach FINAL status. Its
success is partly because it focused on the simplest possible requirement
(a Markdown file) rather than trying to solve machine-readable discovery.

---

## 11. Known Issues

- **No standard structure** — every project formats their FEDERATION.md
  differently, making automated parsing impossible. This is by design
  (the spec explicitly allows arbitrary structure) but limits tooling.
- **Freshness problem** — there is no mechanism to verify whether a
  FEDERATION.md is up-to-date. Some files document features from years ago
  that may have changed.
- **Discovery gap** — finding a project's FEDERATION.md requires knowing
  the repository URL. NodeInfo 2.1's `software.repository` field helps
  but is not universally implemented.
- **No machine-readable companion at scale** — FEP-c893 (DOAP) exists as
  a DRAFT but has limited adoption. The Murmurations protocol was proposed
  as an alternative in 2021 but was not adopted.
- **Fork divergence** — many Fediverse instances run forks or customized
  versions. The upstream FEDERATION.md may not accurately describe a
  particular instance's behavior.
