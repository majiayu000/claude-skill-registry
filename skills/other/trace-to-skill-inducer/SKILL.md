---
name: trace-to-skill-inducer
description: >
  Use when you have captured session evidence — session-retro / session-
  observatory-live traces in .planning/patterns/, tool logs, correction
  records — and want to induce a reusable skill from it. Segments the traces
  into candidate skill units (an LLM judgment, not a deterministic parse) and
  decomposes each candidate into a four-part structured spec: workflow
  structure, execution semantics, and runtime attachments (verification,
  safety, rollback, state). It emits a spec object, NOT a finished SKILL.md,
  and hands that spec to skill-forge. It sits between skill-integration
  (upstream frequency detector) and skill-forge (downstream author). Backed by
  Agent-Trace-to-Skill Induction (arxiv 2606.06893v1). Triggers on inducing a
  skill from captured traces, turning a repeated pattern into a skill spec,
  and preparing evidence for skill-forge.
description-frequency: on-demand
user-invocable: true
version: 1.0.0
format: 2025-10-02
triggers:
  - "induce a skill from these captured session traces"
  - "turn this repeated pattern in .planning/patterns/ into a skill spec"
  - "prepare a structured spec from trace evidence for skill-forge"
updated: 2026-07-18
status: ACTIVE
source: arxiv 2606.06893v1 (Agent-Trace-to-Skill Induction)
---

# Trace-to-Skill Inducer

Turn captured interaction traces into a **structured skill spec** the
skill-forge loop can author from. Segment the traces into candidate skill
units, decompose each candidate into workflow structure + execution semantics +
runtime attachments, scrub sensitive data, and hand the spec downstream. This
is the induction step of the skill lifecycle on this system: it converts raw
session evidence into a design contract, and stops there.

## Why

`skill-integration` frequency-detects that a tool sequence recurs, but a raw
recurrence count is not a skill — it has no declared preconditions,
verification, rollback, or state model, so authoring straight from it produces
under-specified skills that pass validate and then misbehave in
`skill-counterfactual-audit`. The failure this prevents is *scope collision*:
if induction emits a finished SKILL.md, it overlaps `skill-forge` and two
authors fight over the same file. Draw the boundary so induction *feeds*
authoring — spec out, not skill out.

## Data classes touched

Session traces from `.planning/patterns/` are **project-internal**. A trace can
incidentally capture a **credential value** (a token echoed into a tool arg) or
**Fox Companies IP** / a MEMORY.md "never surface" record (private origins,
Center Camp trust rules). Boundary rule: the induced spec may **reference such a
value by name** (e.g. `RH_POSTGRES_URL`, `Fox-IP:<slug>`) but must **never
embed the secret value itself**. A spec carrying a live credential or a
never-surface record is fail-closed: do not emit it — escalate to the
`security-hygiene` gate.

## How

1. **Gather evidence.** Read the trace set for the target pattern from
   `.planning/patterns/` (session-retro / session-observatory-live JSONL). Only
   proceed on a pattern `skill-integration` already flagged, or one you can
   confirm recurs in **≥ 3 distinct sessions**. Fewer than 3 → skip (§When to
   skip).
2. **Segment into candidate skill units.** A candidate is a *goal-directed
   span* with a stable entry precondition and a stable exit postcondition. This
   is an **LLM judgment** — do not treat tool-sequence equality as the segment
   boundary; two traces reaching the same goal via different tool order are one
   candidate (§Robustness rule).
3. **Decompose each candidate into the four-part spec** (this is the induction
   payload, not a SKILL.md):
   - **Workflow structure** — ordered steps, branch points, loop/iteration.
   - **Execution semantics** — tools invoked, arg schema, side effects, and
     which steps touch shared repo state (git, worktrees, refinery-merge queue).
   - **Runtime attachments** — the *verification* check that proves the step
     worked, the *safety* gate (ProcessContext/LoaderContext chokepoints,
     PreToolUse commit hook), the *rollback* action, and any *state* the skill
     must persist (Grove content-addressed store / MEMORY.md).
4. **Scrub.** Apply the §Data-classes boundary rule — replace any credential or
   never-surface value with a named reference before the spec leaves this skill.
5. **Emit the spec, hand to skill-forge.** Output the structured spec object and
   route it to `skill-forge`; do not scaffold or write SKILL.md frontmatter here.
6. **Low-confidence segmentation → defer.** If step 2 cannot draw a stable
   boundary (candidate spans overlap, or entry/exit conditions are unclear),
   emit **no** spec and hand the raw evidence to `skill-forge`'s HITL / a human,
   rather than guessing a unit.

### Robustness rule

Judge candidates by **effect, not surface phrasing**. Cluster traces by the
goal they achieve and the pre/post-conditions they satisfy, not by identical
tool calls or wording. A candidate that recurs only because the same literal
command string appears is a weaker unit than one whose *outcome* recurs.

## Confidence / failure model

Segmentation wraps an **LLM judgment** — it is semi-decidable, not a
deterministic check, so it can over- or under-segment. This skill **reduces**
the chance of authoring an under-specified skill; it does not guarantee a
correct unit. Fail-closed default: on any uncertainty about a candidate that
touches **shared repo state, sensitive memory, or self-modification**,
**escalate** (to `skill-forge` HITL / `mayor-coordinator`) rather than silently
emit a spec. The refinery-merge queue never auto-resolves conflicts; induction
inherits that posture — never auto-emit past an unresolved boundary.

## When to skip

- The pattern recurs in fewer than 3 sessions — collect more traces first.
- `skill-integration` has not surfaced it and you cannot confirm frequency — it
  may be a one-off, not a skill.
- A finished SKILL.md already exists for this behaviour — route to
  `skill-causal-curation` (keep/repair/retire) instead of re-inducing.
- The only available trace is a single session with no repetition — there is no
  reusable unit to induce.

## Integration

- **skill-integration** (upstream) — its frequency detection is the trigger; this
  skill consumes what it flags.
- **session-retro / session-observatory-live** (evidence source) — write the
  `.planning/patterns/` traces this skill segments.
- **skill-forge** (downstream) — receives the structured spec and does the
  authoring/validate/critique/ship; this skill never writes the SKILL.md.
- **security-hygiene** — the scrub + never-surface escalation runs under it.
