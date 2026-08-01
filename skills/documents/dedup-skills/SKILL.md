---
name: dedup-skills
description: 'Ledger-first dedup of a skills/ or prompt-directory tree. Use when the user asks to dedup skills, find rules repeated across or within skill files, or check whether skills contradict each other.'
---

# Dedup skills

Produce a **ledger** of two defect classes across every markdown file in the target tree (default `skills/`): **repetition** — the same rule stated verbatim or near-verbatim in two or more places, cross-file or within one file — and **self-conflict** — opposing directives (must vs never) on the same subject. Report first, always: this skill edits nothing; edits happen only after the user approves ledger rows.

Two duplications are legitimate and are never findings: a short self-contained rule repeated where it is needed (duplication of one short rule beats a pointer chain), and replication carrying a sync-lineage note that names its counterpart. The finding is the *undocumented, long-form* repeat — and the conflict.

## Step 1 — Vendored set

Read the tree's LICENSES/NOTICE/attribution file in full before scanning. Vendored or license-covered paths are annotate-only: findings inside them are reported with a vendored annotation, never proposed for deletion, and the attribution file itself is excluded from the scan (registry, not prompt content).

Done when: every vendored path is enumerated, before any scan runs.

## Step 2 — Cluster pass

Mechanical script over all markdown in the tree. Strip YAML frontmatter first — frontmatter is load-bearing routing data and never a dedup target, so it never enters the scan. Segment into paragraphs (skip fenced code), normalize tokens, and cluster near-identical spans so that **every member of a cluster verifies against its cluster center** — chained transitive grouping pollutes clusters with sub-threshold members. A **cluster** is a span appearing in ≥2 locations cross-file or ≥2 times in one file. Threshold is verbatim/near-verbatim only (≈0.85 token-shingle Jaccard as guidance, not a rule).

Done when: every file is scanned and the cluster list carries file:line locations plus a snippet per cluster.

## Step 3 — Conflict pass

Index directive-modal sentences (must / always / required vs never / do not / forbidden), with sentence-level line attribution — not the enclosing paragraph's first line. Pair sentences with opposing modals on overlapping content words into conflict candidates, each carrying both sentences, both file:line locations, and the overlap score. Before trusting the live result, verify the detector can fail end-to-end: point the scanner's root at a fixture tree containing one markdown file with a known opposing pair, run the full discovery → frontmatter-strip → pairing path, and confirm the pair is flagged. A zero-candidate live result is then a real outcome, not a dead detector.

Done when: the candidate list is emitted and the fixture pair was flagged.

## Step 4 — Judgment pass

Classify every finding from both sets — repetition clusters and conflict candidates are separate, complete sets — exactly once:

- `repeat` — real repetition, all copies live, no sync-lineage note. Remedy: **shorten in place** — every copy stays where it is, compressed to its load-bearing core; no pointer consolidation, no copy deleted. Recommending a sync-lineage annotation is allowed; consolidation is not.
- `conflict` — genuine opposing directives on one subject. Quote both sides verbatim from source (read each cited line in context before confirming). **No default winner**: the ledger proposes no resolution; the user resolves each conflict at apply time.
- `intentional-keep` — documented replication (sync-lineage note, byte-duplicated-by-design header), vendored self-contained relocation, template mirroring its exemplar, or a short self-contained rule. State the reason.
- `not-a-finding` — false positive (opposing modals on different subjects, scoped exceptions such as rules governing different states or routes, coincidental overlap, template scaffolding). Discharge with a one-line reason.

Done when: zero unclassified findings in either set and the finding set is MECE.

## Step 5 — Ledger

Write the ledger: totals per classification, repeat findings grouped into families with per-copy locations and shorten-in-place proposals, conflicts with both sides quoted, discharge reasons for everything else, and the verification performed (spot-checked cluster count, conflict-pass falsifiability). Deliver it without editing the tree. Apply is a separate, later pass gated on per-row (or per-family) user approval.

Done when: the ledger is delivered and the tree is untouched.
