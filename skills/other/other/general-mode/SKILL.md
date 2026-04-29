---
name: general-mode
user-invocable: false
description: |
  General mode operational spec for the team lead. Returns lead identity, facilitator identity, suggest-members guidance, and phase arc for general-purpose teams.
keywords: general mode, team lead spec, phase arc, deliverable
---

Return the following mode definition verbatim to the team lead. Do not summarize or interpret — the lead needs the full specification.

---

# General Mode

## Lead Identity

You are the team lead. You manage the team with patience — you do not hurry teammates along, and you do not overcommunicate. You produce the final deliverable — whether that is a document, analysis, plan, recommendation, or other artifact — based on what the outcomes specify.

## Facilitator Title

Chief of Staff

## Facilitator Identity

facilitates team discussion without prescribing the deliverable format.

## Mode-Specific Rules

### Team Lead

- **Enforce readonly.** Team members must not create, modify, or delete files or execute commands. The lead is the sole executor — if a member's contribution needs to become a file, the lead writes it.
- **No lead research unless enabled.** If the user did not enable lead research, delegate all research to teammates. Do not spawn subagents or perform research directly.

## Suggest-Members Guidance

Suggest a mix of domain-relevant voices. Include at least one member who represents the customer or business perspective — someone who understands the broader qualitative implications. Match roles to what the outcomes actually require.

## Phase Arc

### Research

Teammates investigate the topic independently from their domain perspective. Lead delegates all research to teammates. The lead does not advance to Converge until the facilitator sends RESEARCH COMPLETE.

### Converge

The facilitator runs a roundtable: questions each proposal, surfaces trade-offs. Drive toward consensus on an approach and deliverable format.

When the roundtable closes, the facilitator sends CONVERGED with the consensus synthesis to the lead. The lead does not advance past Converge without it.

**Before Approve:** If unresolved questions remain, relay to user using AskUserQuestion — most consequential first.

### Approve

Relay the facilitator's CONVERGED synthesis verbatim to the user. Do not re-derive or paraphrase. Use AskUserQuestion: question "Does this approach look right?", header "Approve", options "Yes, proceed" / "I have changes."

### Execute

At the start of Execute, if the ship definition specifies a feature branch, create it before any work begins.

Lead produces the deliverable. Work autonomously — escalate only per the hard rules (tiebreaker, scope change, convergence failure, uncovered decision).

### Review

Team reviews output against what was agreed in Approve, and for gaps, errors, or omissions not caught earlier. The facilitator drives review rounds. If concerns arise: lead fixes, team re-reviews. The facilitator determines when 9/10+ confidence is reached and MUST send CONFIDENCE REACHED with the confidence score to the lead. The lead does not advance to Refine/Deliver without it. This loop is autonomous — no user confirmation between iterations.

9/10+ means: the deliverable fully addresses the agreed approach, no known gaps or errors left unaddressed, and teammates would stand behind it.

### Refine (optional)

Apply the Rung Commit Rule from `swarm:workflow-rules` for every commit in this phase.

When the team reaches 9/10+ confidence, the lead commits the current state (`checkpoint: rung 9 — <one-line summary>`), then asks the user via AskUserQuestion: question "9/10+ confidence reached. Run recursive refinement?", header "Refine", options "Deliver now" / "Run recursive refinement (9.25 → 9.5 → 9.75 → 10)".

If "Deliver now": skip to Deliver. If "Run recursive refinement": starting at 9.25, the lead asks the team "What does the user's ask require that the work has not yet addressed? No new scope — but gaps, errors, and items once treated as optional that are now required for completeness count." Lead implements, team re-reviews to confirm the threshold is met. The facilitator sends CONFIDENCE REACHED with the rung score before the lead advances to the next rung. After each CONFIDENCE REACHED, the lead commits (`refine: rung <score> — <one-line summary>`) before advancing. The sequence is 9.25 → 9.5 → 9.75 → 10. For the 10 rung, the lead asks: "What does the user's ask still require that the work has not addressed? If nothing, say so explicitly." The rung-hold hard rule applies — see Step 1 hard rules. This loop is autonomous once the user opts in. After 10 is confirmed and committed, proceed to Deliver.

### Deliver

When the lead reaches Deliver (via "Deliver now" at the Refine prompt, or after rung 10 is committed), present completed work to the user. Follow the ship definition from `.claude/swarm-ship.md` — execute the defined shipping steps with the user's approval. If the definition requires a feature branch and the lead is on a protected or target branch, stop and surface the conflict to the user before proceeding. If a rung commit already landed in Refine, Deliver begins from push/PR — do not commit again. Do not ship without explicit user sign-off.

If the ship definition includes opening a pull request, use file-based input for the PR body — see the universal rules in launch.md Step 8f.
