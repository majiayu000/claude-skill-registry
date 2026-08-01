---
name: memory-hubness-gate
description: >
  Use at write time to vector/embedding memory — Grove content-addressed
  insertion, chroma/pgvector upserts, memory-consolidation promoting session
  traces to MEMORY.md, or embedding externally-ingested content. Scores each
  candidate record against a fixed panel of sentinel queries and quarantines any
  record that would become the nearest neighbor of too many unrelated queries —
  a hub — whether from adversarial poisoning or accidental over-generality.
  This is the memory-record-side sibling of skill-injection-guardian (file-side)
  and the write-side complement of memory-use-warrant (read-side). Quarantine,
  never silently drop; a human reviews. Backed by the admission-time hubness
  gate (arxiv 2606.19692v1). Triggers on inserting into vector memory,
  consolidating memory, and embedding stranger content.
description-frequency: on-demand
user-invocable: true
version: 1.0.0
format: 2025-10-02
triggers:
  - "screen a record before inserting it into vector or embedding memory"
  - "gate memory-consolidation against hub-like poisoning"
  - "embed externally-ingested stranger content into the Grove store"
updated: 2026-07-18
status: ACTIVE
source: arxiv 2606.19692v1 (Admission-Time Defense Against Hubness Poisoning of Vector Memory)
---

# Memory Hubness Gate

Guard the write path of vector/embedding memory against **hubness poisoning**: a
record whose embedding sits near many unrelated query regions, so once inserted
it becomes the nearest neighbor of queries it should never match. This skill
makes the agent score every candidate write against a sentinel panel and
quarantine hub-like candidates *before* they earn a place in the index — the
memory-record-side sibling of `skill-injection-guardian`, which guards files.

## Why

In this repo, writes into the Grove content-addressed store, chroma, and pgvector
are cheap and frequent — `memory-consolidation` promotes session-retro traces to
`MEMORY.md`, tool outputs and fetched passages get embedded, and self-authored
notes append freely. Every one of those is a trust decision, not a free
operation. Hubness is the high-dimensional geometry phenomenon where a few points
dominate everyone's k-nearest-neighbor lists. An attacker can craft a STRANGER
document that reads innocuous but embeds as a hub; the same failure appears
accidentally when an over-general summary is written and then hijacks unrelated
recalls. Read-side hardening guards what comes back; only admission screening
guards what goes in.

## Data classes touched

- **memory records** (public / project-internal). Every embedded write is in scope.
- **STRANGER** (externally-ingested: fetched passages, web tool outputs,
  community content — the `sc-learn` untrusted familiarity class) is the untrusted
  class. It may enter memory only through this gate and must not reach the live
  index without passing.
- **never-surface clusters** (private origins, Fox Companies IP, credentials,
  Center Camp trust rules). Boundary rule: a new record must NOT become the top-k
  neighbor of a sentinel that guards a never-surface cluster — that is poisoning
  that would route unrelated queries toward sensitive space. Any such candidate is
  quarantined regardless of other scores.

## How

1. **Panel.** Maintain a fixed bank of ≥50 sentinel queries spanning ≥8 unrelated
   topic clusters that this memory serves, and include one guard sentinel per
   never-surface cluster above.
2. **Familiarity.** Classify the candidate HOME (self-authored: session-retro
   traces, consolidation output, repo-authored notes) vs STRANGER
   (externally-ingested). STRANGER gets full scrutiny; HOME a lighter check.
3. **Fan-in.** Embed the candidate. For each sentinel, mark a hit if the candidate
   would land in the sentinel's top-5 nearest neighbors OR cosine ≥ 0.55. Count
   the number of DISTINCT unrelated clusters it hits — the hub fan-in.
4. **Verdict.** Quarantine if fan-in spans ≥3 distinct unrelated clusters (HOME) or
   ≥2 (STRANGER); or if it hits any never-surface guard sentinel; or if the
   embedding cannot be computed. Otherwise admit.
5. **Quarantine, never drop.** Move the record to a quarantine store outside the
   live index, attached to the sentinels it dominated and its fan-in evidence. A
   human reviews. If the write was inside a convoy or the refinery-merge queue,
   escalate via `mayor-coordinator` rather than blocking silently.

### Robustness rule

Judge by *geometric effect* — measured neighbor-domination over unrelated clusters
— not by whether the record's text reads benign. A crafted hub is written to look
innocuous. Do not admit on surface phrasing; admit only on measured low fan-in.

## Confidence / failure model

This wraps a JUDGMENT over an embedding probe, not a deterministic guarantee. The
sentinel panel is finite: a hub tuned to query regions absent from the panel slips
through, so a passed record is *lower risk*, not *clean*. It reduces, does not
eliminate, poisoning — the read-side gate (`memory-use-warrant`) stays the
backstop. Default on any uncertainty — ambiguous fan-in, embedding failure, an
unclassifiable familiarity — is **quarantine (fail-closed)**, never silent admit.

## When to skip

- Reading or recalling existing memory — that is `memory-use-warrant`'s read-side gate.
- A HOME write that is a deterministic content-addressed dedup of an already-admitted
  record (identical hash) — no new geometry enters the index.
- Purely structural/metadata writes that carry no embedding vector.

## Integration

- `skill-injection-guardian` — file-side sibling; this is the record-side sibling.
  Together with `memory-use-warrant` (read-side) they form a write/read
  memory-integrity family: guardian screens files, this screens writes, warrant
  screens reads.
- `memory-consolidation` — the primary place this gate runs, on the promote step.
- `security-hygiene` — the umbrella; this is its vector-memory-poisoning procedure.
- Grove content-addressed store / chroma / pgvector — the write path wrapped.
- `mayor-coordinator` — escalation target when a quarantine fires inside a convoy.
