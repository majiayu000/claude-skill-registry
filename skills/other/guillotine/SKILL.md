---
name: guillotine
description: 'Use when dead, duplicate, superseded, or generated residue must leave more than one artifact class of a repo or subsystem, preserving behavior. Not for one enumerated record set: use clean-clean-cut.'
---

# Guillotine

Remove weight the product does not use. Interior cleanup needs proof, not sentiment.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A repository or subsystem needs dead, duplicate, superseded, or generated residue removed across more than one artifact class. |
| Authority | Reversible local: writes only VCS-tracked interior artifacts (edits and deletion); rollback is version control. No remote mutation. No history rewrite, data migration, credential change, or deletion of untracked or critical data. |
| Side effect | VCS-tracked artifacts are deleted or consolidated; live consumers are migrated to the surviving owner; generated surfaces are regenerated. The observable boundary is unchanged. |
| Done | Every removed artifact has a proof of non-necessity, no live route to the old path remains, the observable boundary passes, and the repository gate is green. |

## Inputs

- The subsystem or repository region to purge. Named explicitly or derived from the observed debt surface.
- The observable boundary: the commands, public routes, generated outputs, or user scenarios that must remain unchanged. Required; if no boundary can be named, the skill stops before editing.
- The repository-native gate command that defines "passes". Required, or discoverable in the repo.

## Procedure

1. Name the subsystem and its observable boundary. List the commands, public routes, generated outputs, or user scenarios that must remain unchanged. Done when: the subsystem is named and every boundary element is listed, or the skill stops because no provable boundary exists.
2. Build a candidate ledger. For each code path, document, test, dependency, configuration entry, workflow, or generated file, record its claimed job, live callers or readers, source of truth, and evidence that it is dead, duplicate, superseded, or reproducible. Done when: every candidate has an entry with its job, live consumers, source of truth, and evidence category named.
3. Classify every candidate into one of five categories. Dead: no live caller, route, import, loader, build step, or documented consumer. Duplicate: another artifact owns the same fact or operation and all consumers can move to it. Superseded: the active path covers the required contract and no supported path selects the old one. Generated residue: the repository generator reproduces the required output and does not select this copy. Keep: evidence still names a live job, even when the artifact looks ugly. Done when: every candidate carries exactly one classification and the five categories are exhaustive with no candidate unclassified.
4. Prove the cut from both directions. Search from each candidate to its consumers, then from each required consumer back to its owner. Run a focused behavioral, mutation, build, or generation probe when static references cannot prove necessity. Done when: every candidate has a bidirectional proof: consumer-to-candidate search and candidate-to-consumer search both confirm the classification, or a probe was run that settled the ambiguous case.
5. Stop for approval if the proposed cut reaches an observable API, user command, stored data, history, remote state, untracked file, credential, or critical target. Show the exact consequence and a recoverable alternative. Interior VCS-tracked debt with a proven unchanged boundary does not need a second approval. Done when: every approval-gated target is identified with its consequence and alternative stated, or no target requires approval and the cut proceeds.
6. Cut one dependency-closed slice at a time. Move live consumers to the single surviving owner, then delete the obsolete implementation, tests that protect only obsolete behavior, dependency entries, configuration, workflow steps, and generated copies. Do not leave aliases, shims, dual paths, tombstones, or "deprecated" wrappers. Done when: the slice is cut with all consumers migrated to one owner and no alias, shim, dual path, tombstone, or deprecated wrapper left behind.
7. Regenerate every repository-owned surface affected by the cut. Reject a generator that recreates the removed residue; fix its source selection instead of deleting its output again. Done when: every affected generated surface is regenerated and the generator does not reproduce the removed artifact.
8. Exercise the observable boundary and run the repository-native gate. If behavior changes, restore the smallest failed slice from VCS, correct its ledger classification, and continue with the remaining proven cuts. Done when: every named boundary element passes and the repository gate exits green, or the failed slice is restored and reclassified.
9. Re-run route, import, registration, and source-of-truth searches. Done when: the old path is absent from every search and every required consumer resolves to one live owner.

## Failure and recovery

| Failure | Action |
|---|---|
| A candidate still has a live consumer | Reclassify it as keep or move that consumer inside the same dependency-closed slice. |
| Two artifacts both appear canonical | Stop the cut and establish one owner before deleting either copy. |
| A test fails only because it asserts obsolete internals | Prove the observable contract elsewhere, then delete or rewrite the test. Do not weaken a real boundary test. |
| A dependency looks unused but participates in loading, build, or delivery | Keep it until a real package or artifact probe proves removal safe. |
| Generation recreates removed files | Fix the generator or membership source. Do not hand-delete generated output as the final state. |
| Boundary verification changes | Restore the failed slice from VCS and report the classification error. |
| The cut reaches an approval-gated boundary | Return the exact target, consequence, evidence, and recovery path; wait for explicit authority. |

## Output

Return the candidate ledger with cut or keep verdicts, removed paths grouped by artifact class, surviving owners, observable-boundary evidence, native gate results, and any approval-gated remainder.
