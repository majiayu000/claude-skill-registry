---
name: issue-now
description: 'Use when a human asks to compare one closed or stale tracker issue with current reality and mark it done or update it. Don''t use for bulk issue reconciliation or multi-issue sweeps.'
disable-model-invocation: true
---

# Issue now

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A human explicitly asks to compare one closed or stale tracker issue with current reality and mark it done or update it. |
| Authority | Human-only: inspect and propose freely, but require the invoking human's explicit approval of the exact target and consequence before any remote mutation. |
| Side effect | Close, reopen, or update only the single identified tracker issue; do not mutate other issues, pull requests, project fields, milestones, or repository content. |
| Done | After approval and mutation, a fresh tracker read confirms that the issue state and approved content match current reality. |

## Inputs

- Required: one unambiguous tracker issue reference containing the tracker or repository and issue identifier.
- Required before mutation: explicit human approval of the proposed target, exact field or state changes, and their consequence.
- Optional: the human's claim about what is stale or complete, desired wording, and links to relevant current evidence.
- Tracker access sufficient to read the issue is required for comparison; mutation credentials are needed only after approval. Never request credentials in chat or expose credential values.

## Procedure

1. Resolve the supplied reference to exactly one issue. Stop if it is missing, ambiguous, inaccessible, or resolves to a pull request or another tracker object. Done when: one issue is resolved and confirmed not a pull request or other object.
2. Read the issue's current title, body, state, labels, recent discussion, and completion criteria that are available without changing remote state. Done when: the issue's current state and content are captured.
3. Inspect current, directly relevant evidence available from the tracker and referenced project material. Separate observed facts from human claims, and stop rather than infer completion or invent evidence when the comparison cannot be supported. Done when: observed facts and human claims are separated and evidence is gathered or the gap is reported.
4. Compare each material issue claim or completion criterion with that evidence. Classify the issue as complete, still valid as written, stale but actionable, or indeterminate. Done when: the issue has one classification.
5. Derive the semantic-minimum reconciliation for that one issue: close it when the recorded work is demonstrably complete; reopen it when a closed issue remains actionable; otherwise update only the stale fields or text needed to reflect current reality. Preserve accurate history and content. Done when: one reconciliation action is derived that changes the minimum needed.
6. Present a pre-mutation preview naming the issue, its current state, the evidence used, the exact proposed changes, and the consequence. Ask for explicit approval of that preview. Treat silence, general encouragement, or approval of a different proposal as no approval. Done when: the user explicitly approves the exact preview, or the skill stops for lack of approval.
7. If the human changes the proposal, repeat the comparison and preview. Do not widen the operation beyond the identified issue. Done when: the revised preview is approved or the skill stops.
8. After explicit approval, perform only the approved remote mutation on that issue. Do not add unapproved comments, labels, assignments, milestones, or related-item changes. Done when: the approved mutation is performed and the tracker acknowledges it.
9. Read the issue again from the tracker and compare its resulting state and content with the approved preview. Report success only when this fresh read confirms the match. Done when: the fresh read confirms the issue state and content match the approved preview.

## Failure and recovery
- Invalid or ambiguous target: make no mutation and return `blocked` with the missing or conflicting identifier.
- Insufficient evidence: make no mutation and return `indeterminate`, listing the unresolved completion claims and evidence needed.
- Approval absent or mismatched: make no mutation and return `awaiting-approval` with the exact preview that remains unapproved.
- Access or tracker failure before mutation: make no mutation and return `blocked` with the failed operation and tracker error, excluding secrets.
- Mutation rejected: return `failed`; retain the confirmed pre-mutation state and report the tracker error without retrying a broader or different change.
- Mutation accepted but confirmation unavailable or mismatched: return `unconfirmed` with the approved change, the last confirmed state, and the observed mismatch or read failure. Do not claim the done predicate holds and do not attempt a compensating mutation without a new preview and explicit human approval.
- A read-only comparison and preview are valid partial results. No remote state change counts as complete until the post-mutation read confirms it.

## Output

Return the issue reference, evidence-based classification, approved change, mutation result, and freshly observed final state. The terminal classification is exactly one of `confirmed`, `awaiting-approval`, `indeterminate`, `blocked`, `failed`, or `unconfirmed`; only `confirmed` means the issue now matches current reality.
