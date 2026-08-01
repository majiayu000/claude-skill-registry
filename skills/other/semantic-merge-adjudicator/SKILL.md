---
name: semantic-merge-adjudicator
description: >
  Use when parallel agents in a convoy or across git worktrees hit a write
  conflict on shared state — a git tree, a config, or a shared document — and
  you must decide whether the conflict is semantically real. Classifies each
  conflicting hunk as independent (keep both), redundant (pick one), or a
  genuine clash (escalate), instead of blind locks, abort-and-retry, or
  escalate-everything. Sits ABOVE refinery-merge and NEVER blind auto-merges: it
  wraps an LLM judgment, defaults to escalate on any uncertainty, and
  unconditionally escalates any hunk touching .planning/, config, credentials,
  or safety-critical paths. Backed by CoAgent (arxiv 2606.15376v1). Triggers on
  write conflicts between parallel agents on shared repo state.
description-frequency: on-demand
user-invocable: true
version: 1.0.0
format: 2025-10-02
triggers:
  - "parallel agents hit a write conflict on shared state"
  - "is this merge conflict semantically real or just a byte overlap"
  - "adjudicate a refinery-merge conflict before escalating everything"
updated: 2026-07-18
status: ACTIVE
source: arxiv 2606.15376v1 (CoAgent — Semantic Concurrency Control for Agent Writes)
---

# Semantic Merge Adjudicator

When two convoy polecats or two git-worktree agents write the same shared state,
their diffs may overlap by bytes without colliding in meaning. This skill adds a
semantic decision layer *above* `refinery-merge`: it classifies each conflicting
hunk as `independent`, `redundant`, or `clash`, so the merge queue is not forced
to escalate every syntactic overlap. It never pushes and never blind auto-merges
— a down-classified result re-enters `refinery-merge`'s existing test gate.

## Why

`refinery-merge` is deliberately dumb: on any rebase conflict it aborts, blocks
the queue, and escalates to `mayor-coordinator`. That is correct and must stay —
but it means a convoy of 50+ agents stalls on conflicts that are not real
(two agents appending to different sections of the same file, or two agents
producing the same edit). CoAgent's finding is that for minutes-long LLM
transactions, abort-and-retry discards a costly run and most detected conflicts
are syntactic byte-overlaps, not semantic collisions. This skill recovers the
false-conflict cases *without* weakening the backstop — it can only ever route a
conflict toward the same deterministic test-then-push pipeline, never around it.

## Data classes touched

Shared repo / project-internal state only (a git tree, `.claude/` config, a
shared doc). Hunks that touch these are **path-gated and escalated unread, never
classified, never mixed into an auto-composed tree**: `.planning/` (any),
credentials (`.env`, `*.credentials*`, keystore), config (`.claude/settings*.json`,
`config.json`, chipset/agent YAML), `.claude/hooks/`, `security-hygiene`,
ProcessContext/LoaderContext chokepoint files, and Grove/`MEMORY.md` records
marked never-surface (private origins, Fox Companies IP, Center Camp trust). No
credential, `.planning/`, or safety-critical content may reach a composed output.

## How

1. **Fire only downstream of refinery-merge.** Run only after `refinery-merge`
   has aborted the rebase and marked the MR `conflicted`. Never intercept the
   deterministic pipeline before it runs. Input: the conflict hunks plus both
   parent blobs.
2. **Deterministic path gate first (no judgment).** String-match every
   conflicting hunk's path against the Data-classes list above. If ANY hunk
   matches, escalate the WHOLE MR to `mayor-coordinator` unread and stop. This
   gate is a path match, not an LLM judgment — it cannot be reframed away.
3. **Per-hunk classification** (the LLM judgment) for surviving hunks. Emit one
   label per hunk with a one-sentence reason:
   - `independent` — the two sides edit semantically disjoint concerns
     (different functions / keys / sections) with no ordering or data
     dependency; union keeps both.
   - `redundant` — the two sides express the same intent (identical after
     normalizing whitespace / formatting / rename); pick either side.
   - `clash` — the two sides make incompatible changes to the same concern.
4. **Compose, never push.** Assemble the proposed resolution (union for
   `independent`, chosen side for `redundant`) into a candidate tree and hand it
   BACK to `refinery-merge` as a fresh rebase input. This skill NEVER writes to
   main and NEVER skips the test stage. If the composed tree fails tests →
   escalate.
5. **All-or-escalate.** If ANY hunk in the MR is `clash`, path-gated, or below
   the confidence bar, escalate the ENTIRE MR. Never partially auto-merge the
   clean hunks while hiding a clash — a partial merge that silently drops a real
   collision is the exact failure this skill must not cause.

### Robustness rule

Judge by **effect, not surface phrasing**. Two hunks that read differently but
produce the same behaviour are `redundant`; two that look nearly identical but
diverge in behaviour (a flipped boundary, a swapped operand, an inverted guard)
are a `clash`. Never infer `independent` from "the diffs are on different lines"
alone — adjacent, non-overlapping edits can still be a semantic collision. If
you cannot reason about the effect from the hunk itself, that IS uncertainty →
`clash` → escalate.

## Confidence / failure model

This wraps an LLM **judgment** about whether two writes mean the same thing or
collide — semi-decidable, not a deterministic guarantee. It reduces, it does not
eliminate, the risk of a bad merge, and it reduces `refinery-merge`'s
escalate-everything load without certifying correctness. Fail-closed defaults:
uncertain classification → `clash`; path-gated → escalate; composed tree fails
tests → escalate. The confidence bar for `independent`/`redundant` is
**articulable compatibility**: you must be able to state, in one sentence, the
specific reason the two writes are disjoint or equivalent — an LLM's numeric
"confidence" is not trustworthy here, so the operational test is whether you can
defend the label, and everything else escalates. The only outputs that ever
bypass `mayor-coordinator` are `independent`/`redundant` hunks whose composed
tree PASSED `refinery-merge`'s test gate. That test gate — not this skill — is
the last line of defense.

## When to skip

- `refinery-merge` has NOT marked the MR `conflicted` — do not pre-empt the
  deterministic pipeline.
- Any path-gated file (see Data classes) is involved — skip classification and
  escalate. This is a skip-to-escalate, not a skip-to-proceed.
- The conflict is one agent's writes against itself, or the convoy is
  single-agent with no worktrees in flight — there is no real concurrency.
- The convoy's `token-budget` is exhausted — fall back to `refinery-merge`'s
  escalate-all default rather than running the judgment on fumes.

## Integration

- `refinery-merge` — this is the semantic adjudication layer ABOVE the merge
  queue. `refinery-merge` still owns checkout/rebase/test/push and still
  escalates everything by default; this skill may down-classify a `conflicted`
  MR into an auto-composable tree that re-enters the SAME test gate. It never
  replaces that determinism.
- `mayor-coordinator` — the escalation target for every `clash`, path-gated, or
  test-failing MR.
- `token-budget` — each adjudication is an LLM call per hunk; bound it under the
  convoy budget and fall back to escalate-all when exhausted.
- `selector-priority-arbitration` — DISTINCT: that is a fixed-precedence control
  law deciding who-wins by static priority; this asks whether the writes collide
  at all. Use arbitration when precedence is defined; use adjudication when the
  question is the semantic reality of the conflict.
