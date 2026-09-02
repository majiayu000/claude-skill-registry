---
name: goal-init
description: 'Use when a durable effort needs an approved, checkable success predicate before work starts; writes the goal, verifier, budget, and run-log scaffold. Not for requirement-to-evidence contract ledgers. Never remote, credential, publish, deploy, or irreversible.'
---

# Goal init

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A durable effort needs an approved, checkable success predicate before work starts. |
| Authority | Reversible-local: write only the named goal scaffold artifacts under the goal directory. Rollback is deleting that directory before any effort binds. |
| Side effect | Writes the goal scaffold artifacts (goal statement, budget, run log, verifier); performs no implementation work and binds no effort. |
| Done | Exactly one approved success predicate exists with its verifier and budget recorded, ready for an effort to bind it. |

## Inputs

A human-supplied goal description stating the desired end state in operational terms. The success predicate extracted from it must be checkable: a verifier can return pass or fail without human judgment of the outcome. Optional: a budget ceiling (time, token, or step limit) and a verifier method. If the human cannot state a checkable predicate, stop.

## Procedure

1. Receive the human-supplied goal description. Bound scope before any mutation: this skill writes only scaffold artifacts, performs no implementation work, and binds no effort. Done when: the goal description is received, and scope is bounded to scaffold artifacts only — no implementation work and no effort binding.
2. Validate the goal at its trust boundary. Confirm the human states exactly one checkable success predicate. A predicate is checkable when a verifier can return pass or fail without human judgment of the outcome. If zero or more than one predicate is present, or the predicate is not checkable, stop and report without writing. Done when: exactly one checkable success predicate is confirmed (a verifier can return pass or fail without human judgment), or the run stops with a stated count or checkability failure and no write.
3. Write the goal statement artifact recording the approved success predicate. Done when: the goal statement artifact exists on disk and records the approved success predicate.
4. Write the verifier artifact recording how the predicate is checked, such that the check returns pass or fail. Done when: the verifier artifact exists on disk and records the check method that returns pass or fail.
5. Write the budget artifact recording the effort ceiling (time, token, or step limit). If the human supplied none, record an explicit unbounded marker and flag it for human approval. Done when: the budget artifact exists on disk recording the effort ceiling, or an explicit unbounded marker with a human-approval flag.
6. Write the run-log artifact as an empty log ready for an effort to append execution records. Done when: the run-log artifact exists on disk as an empty log ready for execution records.
7. Confirm the done predicate: exactly one approved success predicate exists with its verifier and budget recorded. Done when: the scaffold directory contains exactly four artifacts (goal statement, verifier, budget, run log), and exactly one approved checkable success predicate is recorded across them.

## Failure and recovery
- Uncheckable predicate: stop, write nothing, report that the predicate cannot be verified.
- Multiple or zero predicates: stop, write nothing, report the count found.
- Missing budget: write the scaffold with an explicit unbounded marker and flag it for human approval; do not fail, because the predicate and verifier are still valid.
- Partial write failure: delete the scaffold directory written so far as rollback and report the blocked state; never leave a partial scaffold that an effort could bind.
- Blocked or non-converged result: report "blocked: goal scaffold not approved" with the specific reason; no effort is bound.

## Output
A goal scaffold directory containing four artifacts (goal statement, verifier, budget, run log) with exactly one approved, checkable success predicate recorded, ready for an effort to bind.
