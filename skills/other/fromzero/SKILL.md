---
name: fromzero
description: 'Use when replacing a greenfield attempt with a clean pad of verified requirements. Not for rebuilding from primitives: use from-first-principle. Requires a committed, VCS-recoverable attempt.'
disable-model-invocation: true
---

# Fromzero

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user wants to replace a greenfield attempt with a clean pad carrying only proven requirements. |
| Authority | Human-gated: requires explicit human invocation before acting; otherwise reversible local: writes only VCS-tracked targets (show the exact set before mutation); rollback is version control. No remote mutation. |
| Side effect | A new greenfield attempt on a clean pad; the old attempt remains recoverable through VCS. |
| Done | A new greenfield attempt exists carrying only verified requirement statements, and the old attempt is reachable in VCS history. |

## Not for

- Rebuilding a design from primitives: use from-first-principle.
- Continuing an existing attempt with fixes: this replaces, it does not patch.
- Operating without a committed, VCS-recoverable current attempt: the old attempt must survive in history.

## Inputs

- The current greenfield attempt, which must be under version control and committed.
- A list of proven requirements. A requirement is proven only when it has been verified (tested, accepted, or otherwise demonstrated). Speculative or unverified scope is not proven.

## Procedure

1. Verify the current attempt is committed and recoverable through version control. If any uncommitted or untracked work exists, stop and require the human to commit or discard it first. Done when: the working tree is clean and the attempt is in VCS history.

2. Filter requirements to verified only. Carry only requirements that have been verified; discard unproven, speculative, or accumulated scope. Done when: the proven-requirements set is listed and each entry is verified.

3. Branch from the recoverable commit to clear the working surface. Before any mutation, list the exact set of VCS-tracked targets the clearance will delete (the tracked files of the old attempt) and show that set; the mutation is a branch creation followed by the clearance of exactly those listed targets. The old attempt survives in VCS history while the working surface is cleared on the new branch. Do not use an unspecified reset alternative. Done when: the exact target set was shown before mutating, the working surface is clear on the new branch, and the old attempt is reachable in VCS.

4. Write the requirement list into the new pad. Write only the proven requirements as statements. Do not reintroduce discarded scope. Done when: the new pad contains only verified requirement statements.

## Failure and recovery

- Current attempt not committed or not VCS-tracked: stop before mutation; require the human to commit. No files change.
- Unverified requirements mixed: stop; do not carry unproven scope into the new attempt.
- Non-mutation fallback: when any precondition fails, no target is changed. Report the blocked precondition and the exact recovery step the human must perform. Do not substitute an unspecified reset alternative.
- Partial-result rule: never leave a half-replaced pad. The old attempt must be recoverable through VCS before any working-surface mutation begins.

## Output

A new greenfield attempt on a clean pad carrying only verified requirement statements, with the old attempt recoverable through VCS history.
