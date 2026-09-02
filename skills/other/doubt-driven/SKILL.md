---
name: doubt-driven
description: 'Use when a non-trivial decision sits under uncertainty and correctness matters more than speed. Returns fresh-context adversarial findings with classified reconciliation and a stop condition. Not for patch review — use review; not for plan attacks — use advocate.'
---

# Doubt-driven development

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Non-trivial decision under uncertainty; correctness matters more than speed; a claim not checkable by the type system or compiler; before committing non-trivial code |
| Authority | Read-only. No file, VCS, credential, paid, published, deployed, or remote mutation |
| Side effect | Chat output: fresh-context adversarial review findings and reconciliation |
| Done | Every non-trivial decision named as a CLAIM and fresh-context reviewed; findings classified; a stop condition met |

## Inputs

- Artifact (required): the unit under scrutiny: a code diff, function, decision proposal, or assertion plus its supporting evidence.
- Contract (required): the constraint the artifact must satisfy.

## Procedure

1. **CLAIM.** Name the non-trivial decision compactly as `CLAIM: "<statement>"` plus `WHY THIS MATTERS: <consequence>`. A decision that cannot be stated that compactly is a vibe, not a decision; surface it before scrutinizing. Done when: the decision is stated as a compact CLAIM with its consequence.
2. **EXTRACT.** Isolate the smallest reviewable unit: the artifact and the contract, without the reviewer's reasoning. Passing conclusions to the reviewer invites validation of those conclusions. Decompose a 500-line PR first; the unit must fit one read. Done when: the smallest reviewable unit is isolated and fits one read.
3. **DOUBT.** Spawn a fresh-context subagent with isolated context using this adversarial prompt verbatim so it overrides any default balanced response shape:

   ```
   Adversarial review. Find what is wrong with this artifact.
   Assume the author is overconfident. Look for:
   - Unstated assumptions
   - Edge cases not handled
   - Hidden coupling or shared state
   - Ways the contract could be violated
   - Existing conventions this might break
   - Failure modes under unexpected input

   Do NOT validate. Do NOT summarize. Find issues, or state
   explicitly that none could be found after thorough examination.

   ARTIFACT: <paste artifact>
   CONTRACT: <paste contract>
   ```

   Pass ARTIFACT + CONTRACT only. Do NOT pass the CLAIM: handing the reviewer a conclusion biases it toward agreement. If a reviewer's default shape cannot be overridden to issues-only, fall back to a generic subagent with the adversarial prompt. Done when: a fresh-context review is spawned passing ARTIFACT + CONTRACT only.

4. **RECONCILE.** Re-read the artifact against each finding before classifying it. Rubber-stamping the reviewer fails just as surely as ignoring it. Classify each finding in this precedence order, first match wins: (a) **contract misread**: the CONTRACT was unclear or incomplete, fix it and re-classify next cycle; (b) **valid + actionable**: real issue, change the artifact and re-loop; (c) **valid trade-off**: real but fixing costs more than accepting, document the trade-off; (d) **noise**: correct under context the reviewer lacked, note it and consider adding that context to the contract. Done when: every finding is classified with first-match-wins precedence.
5. **STOP.** Stop when the next iteration returns only trivial or already-considered findings, or 3 cycles are completed (escalate to the user, do not grind a fourth alone), or the user explicitly says to ship. If 3 cycles still surface substantive issues, the artifact may not be ready; surface this to the user. Three unresolved cycles is information about the artifact, not a reason to keep looping. If 3 cycles is obviously insufficient because the artifact is large, the artifact is too big: return to Step 2 and decompose; do not lift the bound. Done when: a stop condition is met (trivial findings, 3 cycles, user says ship, or escalation).

**Nested-subagent fallback.** This skill runs in the main session, where Step 3 can spawn a fresh-context reviewer. Do not run it from inside a subagent, where spawning another subagent is blocked. If that happens, surface to the user that doubt-driven cannot run nested and let the main session handle it. As a last resort only, a degraded self-questioning fallback exists: rewrite ARTIFACT + CONTRACT as a fresh self-prompt with a hard mental separator from the prior reasoning and walk Steps 1–5. This is not fresh-context review, so flag the result as degraded.

**Doubt theater.** Across 2 or more cycles where the reviewer surfaced substantive findings, zero findings classified as actionable means the reviewer is validating, not doubting. Stop and escalate.

## Failure and recovery
- CLAIM not writable: the decision is still a vibe; return to Step 1, do not proceed to review.
- Reviewer received the CLAIM or reasoning: biased review; re-spawn passing ARTIFACT + CONTRACT only.
- Nested subagent blocks fresh-context spawn: surface to the user; use the degraded self-questioning fallback only as a last resort and flag the result degraded.
- Doubt theater (2+ substantive cycles, zero actionable classifications): stop and escalate to the user.
- 3 unresolved cycles: surface that the artifact may not be ready; do not grind a fourth alone.
- Partial-result rule: a stopped cycle with every finding classified is a valid partial result; unclassified or rubber-stamped findings are not.
- Non-mutation rule: read-only; no file, VCS, credential, paid, published, deployed, or remote mutation. Re-loop changes are recommendations in chat output, not applied edits.

## Output
A report listing each CLAIM, the fresh-context review findings, the classification of each finding (contract misread / valid + actionable / valid trade-off / noise), and the stop condition met — with actionable findings carrying a recommended artifact change stated as a recommendation, not an applied edit.
