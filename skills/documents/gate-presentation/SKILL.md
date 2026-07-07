---
name: gate-presentation
user-invocable: false
description: |
  Returns the frozen gate constants — question, header, option labels and descriptions, digest field-list, and preview content — for every catalog gate. Invoked by the team lead at each gate, fresh per render, in the same turn as the render. The transport contract, three renders, partition rule, and authoring rubric live in swarm:workflow-rules.
keywords: gate presentation, catalog, gate constants, question, preview, digest
---

Return the following gate constants verbatim to the team lead. Do not summarize or interpret — these are frozen SHAPE; the Gate Presentation transport contract in `swarm:workflow-rules` governs how they are rendered.

---

# Gate Presentation Catalog

**Setup gate** — launch Step 2; generated workflow step 3.
- question: "How would you like to set up the team?" · header: "Setup"
- options: "Ultra — reliability (Recommended)" / "Auto-configure mode, team, and research. Full team on the stronger model — reliable rule-following." · "Balanced — lower cost" / "Same auto-config, but members run a cheaper model — less reliable rule-following."
- digest: none (no run values). preview: none.

**Team gate** — launch Step 4; generated workflow step 4.
- question: "Does this team look right? Suggested team: [for each member: name — 2–4-word role axis]." · header: "Team"
- options: "Yes, looks good" / "Proceed with this team composition" · "I want to adjust" / "Swap a member, add more members, or remove some"
- digest: the roster as handles — every member's name plus a 2–4-word axis compressed from its identity line (a compression, not the identity line itself).
- preview (same on both options): the full roster as formatted markdown — numbered, every member with its full one-line identity. The full identity lines live here only.

**Plan gate** — launch Step 7; generated workflow step 5; /swarm:refine Step 3.
- question: "Is this plan final, or do you have remaining inputs? [digest]" · header: "Confirm"
- options: "Launch the team" / "Plan is final — start creating the team now" · "I have changes" / launch variant: "Adjust outcomes, mode, members, tier, or research first." — refine variant: "Adjust outcomes first (roster and tier are fixed; the diff base cannot be changed from this prompt)."
- digest, launch variant (delta-forward): ship definition (one line — its first appearance); compressed outcomes line (adjustable here, so decision content); scope line only if the reflection fork kept a pin (Option A: "[their word] specifically"); then handles — name-only roster, cost tier token, mode.
- digest, refine variant: diff base first (the silently-inferred correctness pivot); PR state (URL or `(no open PR detected)`); when the base is the default-branch fallback, inline: `no PR detected — diff base falls back to the repo's default branch (<resolved-default>). Verify before launch.`; compressed outcomes line; scope line only if the reflection fork kept a pin (Option A); branch under review; the one-line diff stat. Fixed fields (mode, tier, roster, phase arc, ship definition) are not decision content here — preview only.
- preview (same on both options): elaboration only, never a restatement of the digest — the outcomes verbatim (numbered, exact confirmed wording), the full roster with identity lines, and (refine variant) the fixed fields and ship definition; plus the closing line `Rules: Active`. Fields the digest carries at their only fidelity (mode and tier tokens in the launch variant; the digest one-liners) do not repeat here.

**Approve gate** — every mode's Approve phase.
- question: "Does this [subject] look right?" — [subject] is fixed by the mode skill: approach (code, general), diagnosis (triage), direction (writing) · header: "Approve"
- options: "Yes, proceed" / "Approve the [subject] — the team proceeds to Execute" · "I have changes" / "Adjust the [subject] before the team proceeds"
- digest: none beyond the question — the synthesis is unsplittable verbatim content; a lead-authored compression would breach the verbatim-relay rule.
- preview (same on both options): the facilitator's CONVERGED synthesis verbatim. The main-window relay still happens per the phase arc (it is the scrollback record and the AFK projection's source); the preview is what makes the synthesis readable inside the modal.
- standalone-sufficiency carve-out: this gate's sufficiency source is the verbatim relay that immediately precedes the modal, not a digest — compressing the synthesis into the question would paraphrase it.
- declared AFK carrier: every re-emission of this gate (an AFK restatement, a pulse re-emission, post-compaction) re-carries the synthesis verbatim. The re-read is uniform and structural, never a reliability judgment (silent compaction drift defeats self-detection — the same premise as the constants' unconditional re-fetch): every re-emission, the first AFK restatement included, re-reads the synthesis from the facilitator's on-disk transcript (the Team Lead disk-read rule) unconditionally. Never reconstruct it from memory; if the disk read itself fails, do not fall back to an in-context copy — surface the failure once, then hold the gate.

**Finish gate** — code-mode Refine (the unified pre-ship gate).
- question: "9/10+ confidence reached. How should the team finish?" · header: "Finish"
- options (thoroughness-descending): "Recursive refinement + independent review (Recommended)" / "Run the 9.25→10 refinement ladder (drives completeness to the full scope of the outcome), then an independent review loop (drives out functional defects via an independent reviewer) after the PR is created." · "Recursive refinement only" / "Run the ladder; no independent review loop." · "Independent review loop only" / "Skip the ladder; run just the independent review loop after the PR is created." · "Ship as is" / "Proceed straight to Deliver with no further review."
- digest: none. preview: none.

**Refine gate** — general-mode and writing-mode Refine.
- question: "9/10+ confidence reached. Run recursive refinement?" · header: "Refine"
- options: "Run recursive refinement (9.25 → 9.5 → 9.75 → 10) (Recommended)" / "Mandatory to 10 once started — rung commits along the way." · "Deliver now" / "Skip the ladder and proceed to Deliver."
- digest: none. preview: none.

**Terminal gate** — Deliver's keep-open/shutdown handshake, after the pulse-delete.
- question: "The work is delivered. Keep the team open or shut it down?" · header: "Team"
- options: "Keep the team open" / "Teammates stay available for follow-up work in this session." · "Shut down the team" / "This answer is the explicit shutdown instruction — the lead runs the shutdown protocol."
- digest: none. preview: none.
