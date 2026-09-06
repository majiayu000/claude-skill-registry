---
name: reflect
description: 'Use when a completed task needs reflection on invoked skills to propose and apply approved improvements. Not for remote, credential, publish, deploy, or irreversible changes.'
disable-model-invocation: true
---

# Reflect

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Reflect on a completed task to improve invoked skills. |
| Authority | Human-gated: explicit invocation required before any mutation; every other write is reversible local, with version control as the rollback. |
| Side effect | Edits approved skills and may file backlog items. |
| Done | Approved improvements applied and rejections explained. |

## Refusals

- Edits without explicit human approval: rejected. Every "apply now" or "apply on approval" proposal requires explicit human sign-off before any file change.
- Analysis beyond the named skills: rejected. Do not widen the analysis beyond the invoked skills the human supplied.
- **Remote, credential, publish, deploy, or irreversible changes**: rejected.

## Inputs

The human must supply:
- The completed task context (what was attempted, what happened, what remains).
- The list of invoked skill slugs or names.

Optional: evidence of failure patterns, specific lines or sections to target, or scope constraints.

## Procedure

1. Collect context. Gather the task context and the list of invoked skills from the human. Identify which skill files are reachable in the workspace. **Done when**: the task context and skill list are gathered and reachable files are identified.
2. Analyze. Examine the invoked skills for failure patterns, missing coverage, unclear scope, or improvement opportunities. Do not widen the analysis beyond the named skills. **Done when**: each skill has been examined and findings are listed.
3. Propose. Present each finding as a discrete improvement proposal. Label each as "apply now", "apply on approval", or "backlog item". Keep proposals scoped to one skill. **Done when**: every finding is presented as a labeled proposal.
4. Get approval. For every "apply now" or "apply on approval" proposal, obtain explicit human approval before making any file change. **Done when**: every proposal has an approval decision recorded.
5. Execute. Apply approved edits to the skill files. File any approved backlog items. Report every applied change and every rejected or deferred proposal. **Done when**: all approved edits are applied and all rejections are recorded.

## Failure and recovery

- Analysis failure: if the skill files cannot be read or the task context is insufficient, stop and report the reason.
- No improvement found: state that finding and end without mutation.
- Approval withheld: record the reason and continue with remaining proposals.
- Application failure: if an approved edit cannot be applied after human sign-off, attempt to roll back any partial change and report the blocked state. Do not declare success when the done predicate does not hold.

## Output

A reflection report with each analyzed skill and findings, each approved change and its result, each rejected or deferred proposal and the reason, and any filed backlog items, ordered as listed, ending with a statement that the done predicate holds or the specific outstanding block.
