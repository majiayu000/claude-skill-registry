---
name: prism
description: 'Use when one reviewer angle is insufficient or the user suspects a direction is tunnel-visioned or inherited its framing. Modes: artifact, direction. Not for source or remote-system changes.'
---

# Prism

## Contract

| Field | Bound contract |
|---|---|
| Trigger | One reviewer angle is insufficient, the user asks to "prism this" or review from different angles, one read may be an artifact of how the question was framed, or the user suspects the current direction of work is tunnel-visioned or inherited its framing. |
| Authority | Read-only. No writes; nothing to roll back. No remote mutation. |
| Side effect | A divergence-first report in chat only; create or change no files; bounded fresh zero-context sub-reads are spawned only as inputs to classification. |
| Done | Bait is stripped from the target; every read carries exactly one classification label (artifact mode: divergent-incompatible, divergent-compatible, convergent; direction mode adds ambiguous); shared-root clustering is complete; cluster order follows the mode, with direction mode listing ambiguous clusters first; convergence is labeled reassurance with no consensus wording; one decisive resolving question is stated. |

## Inputs

- Mode: artifact or direction; default artifact. Direction applies when the user asks whether a current direction of work (plan, approach, or framing) is tunnel-visioned or inherited its framing; artifact applies when a concrete artifact is reviewed.
- Target: the artifact to review, or the direction of work to stress-test. Required.
- Lenses or viewpoints: review lenses for artifact mode; distinct viewpoints for direction mode (opposing assumption, adjacent domain, historical failure mode, resource constraint, user-population segment). Optional; if omitted, derive them from the target's genuinely distinct failure modes.
- Context: background material that may inform the reads but must not constrain them to a single frame. Optional.
- Decision: a decision the review must inform. Optional.
- Read count: between 2 and 5; default 3. Optional. The same model is allowed across reads: this checks framing blind spots, not cross-model truth.

## Procedure

1. Read the target end to end before selecting lenses. In direction mode the target is the direction statement; read it with its surrounding context. Treat supplied context as evidence only when it is available and attributable; do not invent missing facts. Done when: the target is read completely and no fact is invented.
2. Select two to five lenses, each representing a distinct failure mode. Mode artifact: merge proposed lenses that test the same failure mode; let the artifact determine the count rather than defaulting to a fixed number. Mode direction: pick distinct viewpoints such as opposing assumption, adjacent domain, historical failure mode, resource constraint, or user-population segment; no read may copy or restate another. Done when: each lens targets a distinct failure mode and duplicates are merged.
3. Strip the framing. Remove the session's own examples, suggested answers, preferred naming, and framing-specific wording down to the underlying goal, constraints, and known facts. Mode artifact: restate the bare review question in neutral terms that do not carry the session's loaded vocabulary; if a term is load-bearing, keep its denotation but drop the framing that points at one answer. Mode direction: strip bait from the direction statement, removing leading, suggestive, and conclusory language; restate what is being attempted and why, preserving the decision's substance without its rhetorical frame. Done when: the bare question or direction statement is restated in neutral terms with loaded framing or bait removed.
4. Fan out 2 to 5 fresh zero-context reads of the stripped question or direction, default 3, each evaluated independently through one lens. The same model is allowed. Done when: 2 to 5 fresh reads are dispatched, each through a distinct lens.
5. Normalize verdicts. For each lens give exactly one verdict (`pass`, `fail`, or `unclear`) and the single most load-bearing reason supported by the target or supplied context. Do not average or flatten conflicting verdicts. Done when: every lens has one verdict and one load-bearing reason.
6. Classify each perspective. Assign exactly one label: `divergent-incompatible` (challenges a premise the direction depends on, or identifies a framing flaw, hidden assumption, or outcome that contradicts the intent), `divergent-compatible` (adds, reframes, or proposes a meaningfully different path or emphasis without discarding the direction), `convergent` (independently arrives at the same framing or verdict), or `ambiguous` (cannot be classified with confidence; include a one-sentence explanation). Do not force-fit a label. Done when: every perspective carries exactly one classification label.
7. Cluster by shared root before reporting. Group reads that share the same underlying assumption, evidence source, or structural concern; name the root and put the instances under it as evidence. Reads with no shared root form single-member clusters. Done when: every read is assigned to a cluster with its root labeled.
8. Report divergence-first. Mode artifact: incompatible divergence, then compatible divergence, then convergence. Mode direction: ambiguous clusters first, then incompatible, then compatible, then convergent; within each cluster, order by relevance to the core claim. Label convergence as reassurance, never proof; in direction mode note that convergent reads confirm the framing was inherited, not chosen. Use no consensus, agreement, majority, or weight wording when describing the reads collectively; if such wording appears, rewrite the sentence with per-read or per-cluster attribution. No majority vote, no averaging, no "verified." Done when: the report is emitted in the mode's order with convergence labeled as reassurance and no consensus wording present.
9. Name one decisive resolving question whose answer would resolve the deepest disagreement. For full convergence, state the shared verdict and mark the resolving question as `none (no lens conflict)`. Done when: the decisive question is stated, or `none (no lens conflict)` with the shared verdict.
10. Check that every selected lens appears once, every verdict has evidence, every perspective is classified, and the grouping follows from the verdicts. Return the report only in chat. Done when: every lens appears once, every verdict has evidence, every perspective is classified, and the grouping follows from the verdicts.

## Failure and recovery

- Missing or unreadable target: stop and return `blocked`, naming the artifact or access needed; do not substitute a guessed target.
- Framing cannot be stripped: in artifact mode, report that the framing cannot be separated and stop; do not fan out a still-loaded question. In direction mode, proceed with the original statement and note which bait elements could not be removed.
- Fewer than two distinct lenses or reads: return `blocked: independent lenses unavailable`, report the single read with its classification, and explain why a multi-lens verdict would be false precision; do not pad with variations of the same viewpoint.
- Insufficient evidence: use `unclear` for the affected lens or `ambiguous` for the affected read and name the missing evidence; do not convert uncertainty into a firm label.
- Read refuses or returns empty: report the refusal as a divergence lead rather than retrying with re-primed prompts.
- Consensus language detected in output: rewrite the affected sentence; replace phrasing that implies the reads collectively agree or disagree with per-read or per-cluster attribution.
- Partial result: return every read obtained with its classification. Never fabricate a read, invent a classification, or upgrade convergence to proof.
- Unresolved disagreement: return the conflicting verdicts and the single resolving question as a valid partial result; do not claim convergence.

All failures preserve the read-only boundary: there is no mutation to roll back.

## Output

Return a chat report with sections in this order: Stripped target, Lenses, Verdicts, Divergences, Convergence, Decisive question, Status.

| Section | Content |
|---|---|
| Stripped target | The bare review question (artifact mode) or the stripped direction statement (direction mode). |
| Lenses | Each selected lens or viewpoint and the failure mode it targets. |
| Verdicts | Per lens: the normalized verdict (`pass` / `fail` / `unclear`), the load-bearing reason, and the classification (`divergent-incompatible` / `divergent-compatible` / `convergent` / `ambiguous`). |
| Divergences | Roots with their divergent perspectives clustered underneath. Artifact mode: incompatible divergence first, then compatible. Direction mode: ambiguous clusters first, then incompatible, then compatible, then convergent. |
| Convergence | Convergent perspectives described as reassurance, never proof; direction mode notes the framing was inherited, not chosen. |
| Decisive question | The single question whose answer would resolve the deepest disagreement, or `none (no lens conflict)` with the shared verdict. |
| Status | `complete` when all lenses evaluated and all perspectives classified; `partial` when some reads were obtained but not all; `blocked` when the target is missing, independent lenses are unavailable, or artifact-mode framing cannot be stripped. |
