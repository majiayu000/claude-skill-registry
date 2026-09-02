---
name: offense
description: 'Use when a human says "overhaul", "rebuild this subsystem", or "rewrite it from scratch" and the broken structure must be demolished and re-derived from its contracts. Deletes rather than deprecates, collapses special cases into the general case, and migrates every caller in one change. Not for thin-slice features — use incremental-implementation; not for root-cause bug repair — use strike-the-root.'
---

# Offense

Radical codebase overhaul, invoked by a human only. Demolish-and-re-derive: rewrite subsystems from their contracts instead of patching, delete rather than deprecate, collapse special cases into the general case, and migrate every caller in the same change. The stance is offensive — tear the broken structure out and re-derive it clean — not defensive patching that leaves the old shape half alive.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A human invokes an overhaul: "overhaul", "rebuild this subsystem", "rewrite it from scratch", or equivalent. Never self-initiated. |
| Authority | Modify only the invoked scope, an exact disclosed set of repository paths governed by version control. Create atomic commits and use version control to recover from an invalid increment. Stop and ask before removing any observable surface consumers depend on. |
| Side effect | Atomic compilable commits that demolish the old structure and re-derive it from its contracts; the general case absorbs every special case; every caller migrates in the same change; no shim, alias, deprecated path, or feature flag survives the cutover. |
| Done | The invoked scope is rebuilt from its contracts, every caller is migrated, no special-case branch or deprecated path remains, the feature works end to end, and the applicable verifier is green. |

## Inputs

Supply the invoked scope (the subsystem, module set, or surface to overhaul), the contracts that govern it, and the permitted path set. Supply required verification commands when the repository does not define them. An implementation plan or known invariants are optional; derive them from the existing contracts when absent, but do not invent requirements.

## Procedure

1. **Bound the invoked scope.** List the exact repository paths in the overhaul and the observable surfaces it exposes (public APIs, CLI flags, config keys, file formats, wire shapes). Stop and ask before removing any observable surface consumers depend on; never silently narrow scope. Done when: the exact path set and observable surfaces are listed, and removal of any consumer-facing surface is explicitly approved.
2. **Re-derive the contract.** Read the existing implementation and extract the contract the subsystem should have held — its invariants, trust boundaries, and the general case that absorbs every special case. Discard the old structure's accidents; keep only the contract. Done when: the contract is written with invariants, trust boundaries, and the general case named.
3. **Partition into atomic increments.** Each increment must preserve the named invariants, compile, and leave applicable existing behavior verifiable. Order increments so the contract is re-derived before callers migrate onto it. Done when: the work is partitioned into increments that each compile and preserve invariants.
4. **Demolish and re-derive.** Implement the general case directly from the contract. Encode invariants in types or construction where practical; otherwise validate at the boundary and return or raise the repository's explicit error form. Delete the old structure rather than deprecating it; collapse every special-case branch into the general rule; do not leave a shim, alias, deprecated path, or feature flag for the old shape. Done when: the general case is implemented, the old structure is deleted, and no special-case branch, shim, alias, or dark flag remains.
5. **Migrate every caller in the same change.** Update every callsite to the new contract in the same change that introduces it; never leave a caller on a removed surface. If a caller cannot migrate within the disclosed path set, stop and ask — do not widen scope implicitly and do not leave a half-migrated state. Done when: every caller is migrated and no reference to a removed surface remains.
6. **Verify each increment.** After each increment, run the narrowest applicable compile and behavioral checks that exercise its changed contract. If they pass, commit that one logical change with a descriptive message. Revalidate all named invariants affected by the next increment before continuing. Done when: each increment is checked, committed, and its invariants revalidated for the next increment.
7. **Exercise end to end and run the final verifier.** Confirm the changed-path set is exactly the disclosed set, that no special-case branch, shim, alias, deprecated path, or uncommitted partial increment remains, and that the feature works end to end. Done when: end-to-end behavior is exercised, the final verifier is green, and the changed-path set matches the disclosed set with no remnants.

## Failure and recovery

Classify failure as invariant violation, verification failure, unavailable verification, scope breach, consumer-surface conflict, or non-convergence. On an invariant violation, fail before mutation when possible and report the violated invariant. On verification failure, stop; restore only the current atomic increment to the last green commit while preserving earlier green commits. On unavailable verification or a required path outside the disclosed set, make no further changes and return `blocked` with the missing check or exact additional path. On a consumer-surface conflict — a caller outside the disclosed set depends on a surface slated for removal — stop and ask before proceeding; never silently break a consumer. If repeated attempts preserve neither the contract nor the done predicate, return `non-converged` with the last green commit, failed increment, and verifier evidence. Never report success from a partial result; never leave a shim, alias, or deprecated path to force convergence.

## Output

Return the ordered atomic commit identifiers, the exact changed paths, the re-derived contract with its named invariants and how each is enforced, the observable surfaces removed and the consumer-surface approvals obtained, verification commands with observed results, and the end-to-end outcome. Terminal classification: `complete`, `blocked`, or `non-converged`; `complete` requires the bound done predicate — every caller migrated, no special-case branch or deprecated path remaining, and the verifier green.
