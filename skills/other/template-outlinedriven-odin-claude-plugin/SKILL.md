---
name: "{skill_name}"
description: >-
  Personal taste skill — 5 evidence-derived anchors ({anchor_names}) for prose,
  code, design, and decisions. Two modes: audit judges an artifact against the
  two-sided charter; anchor loads the taste register before producing. Trigger
  with "{trigger_phrase}", "taste-test", "is this slop?", or "overkill?".
# auto-invoke: explicitly permitted — generated taste skills auto-invoke like the generic taste skill
---

# {skill_name}

{skill_name} is a personal taste skill. It encodes observed taste through 5 evidence-derived anchors, each with a load-bearing concept, canonical exemplar, and two-sided failure boundary.

## Posture

{posture_statement}

Conviction with restraint. The anchors are the positive frame; the two-sided charter is the negative space. Side A blocks slop/default convergence. Side B blocks overkill/compensatory excess. Both sides fail by refusing to commit.

## Modes [LOAD-BEARING]

Two modes share the auto-clarity exception.

### Mode-selection

Auto-detect from invoking-context phrasing, with slash-arg override:

- "is this slop?", "overkill?", "taste-test", "audit this", "review for taste", "what's wrong with this" -> **audit**.
- "shape this before writing", "load taste", "anchor mode", "before I write" -> **anchor**.
- Anything else -> **audit** by default.
- Explicit override: `/{skill_name} audit`, `/{skill_name} anchor`. Override always wins.

### audit mode

Walk the 5 anchors against the artifact in hand. For each anchor: verdict (`pass` / `warn` / `fail`), Side A or Side B citation when violated, and concrete fix. Surface tensions when anchors imply conflicting fixes; do not auto-pick a hidden precedence. Close with top-3 ranked fixes.

### anchor mode

Load the 5 anchors and two-sided charter as imperatives for subsequent responses. Persistence is best-effort: applies until the user signals "stop taste" or "normal mode" OR context is compacted, whichever comes first. Re-invoke anchor mode if drift is observed.

## Two-sided charter

**Side A — slop:** {side_a_summary}

**Side B — overkill:** {side_b_summary}

See `references/charter.md` for the full charter.

## Anchors

| Anchor | Influence | Concept |
|---|---|---|
| {anchor_1_name} | {anchor_1_influence} | {anchor_1_concept_short} |
| {anchor_2_name} | {anchor_2_influence} | {anchor_2_concept_short} |
| {anchor_3_name} | {anchor_3_influence} | {anchor_3_concept_short} |
| {anchor_4_name} | {anchor_4_influence} | {anchor_4_concept_short} |
| {anchor_5_name} | {anchor_5_influence} | {anchor_5_concept_short} |

Depth and canonical exemplars per anchor: see `references/anchors.md`.

## Audit output shape

An audit produces:

1. The artifact, quoted tersely when short or identified by path/section when long.
2. 5-anchor verdict table: anchor | verdict | Side A or Side B citation if violated | concrete fix.
3. Tensions between anchors, only when a fix conflicts.
4. Top-3 ranked fixes, most load-bearing first.
5. Revised artifact when requested or when the fix is small enough to show directly.

## Anchor mode output shape

When anchor mode activates, emit:

```text
/{skill_name} anchor active.
Anchors: {anchor_names}.
Side A blocks: {side_a_blocks_short}.
Side B blocks: {side_b_blocks_short}.
Persistence: best-effort. Stop with "stop taste" or "normal mode". May reset on context compaction.
```

## Auto-clarity exception

Suspend the taste register temporarily for:

- Destructive or irreversible operation confirmations.
- Security or data-loss warnings.
- Multi-step procedures where order or atomicity matters and taste register would obscure structure.
- Direct clarification requests.

Resume the register once the high-stakes section ends.
