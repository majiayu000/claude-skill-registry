---
name: windows-protocols
description: Local Microsoft Open Specifications corpus navigator for Windows protocols. Use this skill when the user asks protocol-level questions, needs message/structure details, wants section-by-section summaries, or needs cross-references across related specifications.
---

# Windows Protocols Corpus Navigator

## Overview

- The markdown corpus is already extracted locally, next to `SKILL.md`.
- Use local files only. Do not use network lookup for this skill.
- Do not run download or setup commands as part of normal usage.

This skill is optimized for structure-first navigation of Microsoft Open Specifications markdown and evidence-grounded answers.

## Corpus Layout

- `README.md` — index with three sections: Overview Documents (domain maps), Technical Documents (full spec list), and Reference Documents. Overview Documents are at the top; use them for topical discovery.
- `LEGAL.md` — legal and redistribution notice.
- `<PROTOCOL-ID>/` — protocol directories (Overview, Technical, or Reference), directly under this folder.
- `<PROTOCOL-ID>/<PROTOCOL-ID>.md` — primary markdown spec content.
- `<PROTOCOL-ID>/media/` — extracted figures and image assets referenced by the markdown.

## Corpus Document Types

- **Overview Documents** — Domain maps that group related protocols under a topic (file access, authentication, storage, remote desktop, etc.). Each describes system capabilities, lists member protocols with their roles, and contains many links to specifications. Use as the primary entry point for topical discovery.
- **Technical Documents** — Individual protocol specifications with full wire-format, message syntax, and behavior details.
- **Reference Documents** — Supplemental references (error codes, shared types, etc.).

## Protocol Clusters by Domain

When using Overview documents for discovery, expect these cluster themes:

- **Authentication**: Kerberos, NTLM, SPNEGO — core for file access, RDP, Group Policy.
- **File Access**: SMB/CIFS family, DFS, WebDAV, shared types (FSCC, FSA).
- **Remote Desktop**: Base + graphics pipeline, gateway, virtual channels (clipboard, devices, transport).
- **Storage**: Disk/volume management, shadow copies, EFS, backup, removable media.
- **Group Policy**: Core protocol + extensions; depends on AD and file access.
- **Network Access Protection**: SoH/SoHR over PEAP; DHCP/VPN/TSGU/IPsec enforcement.
- **Content Caching**: Peer discovery, retrieval, hosted cache; integrates with SMB/HTTP.
- **File Services Management**: FSRM, remote VSS, classification.
- **Rights Management**: Publish/consume protected content.
- **Virtual Storage**: Remote shared virtual disks over SMB.

## Protocol Naming and Scope

- `MS-...` documents are Microsoft protocol specifications (wire formats, behavior, state machines, structures).
- Families share prefixes (for example `MS-RDP*`, `MS-AD*`, `MS-MQ*`).

When a user asks a broad question, start from family prefixes and narrow to specific protocol IDs.

## When to Use / When Not to Use

Use this skill when the user asks for:

- Protocol semantics, message flow, field definitions, or sequencing rules.
- Cross-reference analysis between related specs.
- Security semantics and product-behavior distinctions in Open Specifications docs.

Do not use this skill as the primary source for:

- API usage tutorials, SDK how-to steps, or implementation quickstarts.
- Product configuration guidance not grounded in protocol specs.

If a required protocol is missing from root-level `MS-*` directories, state that explicitly and ask the user for the exact protocol ID or a narrower feature scope.

## Navigation Strategy

- **Domain/topic questions** (file access, authentication, storage, remote desktop, etc.): Start with the corresponding Overview document from README. Use it as a map to identify which specifications to read. Follow its links into those specs.
- **Protocol-ID questions**: Go directly to the spec if the ID is known.
- **Principle**: Overview documents are the primary entry point for topical discovery. README provides the index of Overview docs and the full protocol list, but does not contain the semantic mapping (topic → protocols) found in Overviews.
- **Anti-pattern**: Do not rely on README keyword search alone. A shallow grep of README may return protocol IDs from unrelated domains; overview documents provide the curated topic-to-protocol mapping.

## Navigation Workflow

1. For topical questions: Identify the domain from the question, match to an Overview document in README, read it to obtain linked member specs, then follow links into those specs.
2. For known protocol IDs: Validate in `README.md` and directory names (`<PROTOCOL-ID>/`), then open the spec.
3. Start from the spec TOC (`<summary>` blocks and numbered entries) before deep reading.
4. Read sections in this order by intent: orientation/versioning, message or structure syntax, behavior and sequencing, security and product behavior notes.
5. Cross-check base vs extension specs when requirements may be split.
6. Answer with explicit protocol IDs and exact section headings; separate confirmed facts from inference.

## Link-Following

- Overview documents contain References sections (often 1.3) and extensive inline links to member specifications. Follow these links rather than guessing paths.
- The link graph (Overview → spec → related spec) is the intended navigation structure.
- When a spec references another spec for types, extensions, or dependencies, follow that link to reach the authoritative source.
- Continue following links until the relevant information is found; do not stop at the first document that mentions the topic.

## Canonical Spec Structure (Corpus-Guided)

The corpus is highly consistent. The most common top-level sequence is:

- `1 Introduction`
- `2 Messages`
- `3 Protocol Details`
- `4 Protocol Examples`
- `5 Security`

Common `1.x` orientation subsections include:

- `1.1 Glossary`, `1.2 References`, `1.3 Overview`
- `1.4 Relationship to Other Protocols`
- `1.5 Prerequisites/Preconditions`
- `1.7 Versioning and Capability Negotiation`

Common `3.x.y` behavioral subsections include:

- `Abstract Data Model`
- `Timers`
- `Initialization`
- `Higher-Layer Triggered Events`
- `Message Processing Events and Sequencing Rules`
- `Timer Events`
- `Other Local Events`

Use these sections as the default reading spine unless the document is an outlier.

## Section-First Reading Playbook

Prioritize sections by question type:

- “What is this protocol / where does it fit?” -> `1.3`, `1.4`, `1.7`
- “How is data encoded / what are fields?” -> `2.2` (`Message Syntax`, `Common Data Types`, structures)
- “What is the runtime behavior / state machine?” -> `3.x` details and `3.x.y` sequencing sections
- “What security guarantees or knobs exist?” -> `5.*` security sections
- “Implementation differences by product/version?” -> `Appendix ... Product Behavior` and change tracking sections

When structure spans multiple specs, resolve in this order:

1. Base/core protocol semantics.
2. Extension-specific modifications.
3. Shared type dependencies (for example `MS-DTYP`).

## Outlier Handling

Not all specs use the exact canonical headings. Handle these common variants:

- `2 Structures`, `2 Attributes`, `2 Data Types`, `2 Message Transport` instead of `2 Messages`.
- `3 Structure Examples`, `3 Details`, or algorithm-specific section names.
- `4 Security` or `4 Security Considerations` when numbering shifts.
- Appendix variants such as `Full IDL`, `Full WSDL`, `Full XML Schema`, `Full JSON Schema`.
- Change tracking may appear as section `7`, `8`, `9`, or higher.

Rule: match by semantic intent first, section number second.

## Quick Discovery Patterns

- When the protocol ID is unknown: Identify the domain first from question keywords, then open the matching Overview document before picking specs. Use its Protocol Summary or References section to obtain the correct spec list.
- Do not select specs from README's flat Technical Documents list without consulting an Overview when the domain is ambiguous.
- When the user provides a specific protocol ID: Go directly to that spec.
- For extension behavior: Verify whether requirements are in a base protocol or an extension; Overview docs and spec cross-references help clarify dependencies.
- For ambiguous acronyms: List 2–4 likely protocols (via Overview docs) and ask the user to choose before deep analysis.

## Answer Contract (Semi-Structured)

Default answer shape:

1. `Protocols consulted`: list exact IDs.
2. `Sections used`: list exact section titles (and numbers when available).
3. `Findings`: concise facts tied to those sections.
4. `Inference / uncertainty`: explicit separation from confirmed text.

Evidence policy:

- For non-obvious, contested, or security-sensitive claims, include section-grounded evidence.
- For straightforward facts, concise section references are enough.
- If two specs disagree, report both and identify likely version/context scope.

## Working Style

- Prefer section-grounded answers over high-level paraphrase.
- Include the exact protocol IDs used for the answer.
- If the corpus does not clearly answer a point, state uncertainty explicitly.
- Never present inferred behavior as normative requirement text.

