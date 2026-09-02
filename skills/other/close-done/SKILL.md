---
name: close-done
description: 'Use when the user wants to batch-close resolved or outdated tracker items. Fetches item metadata, filters by evidence-backed criteria, and presents a prepared batch for the user to close manually. The agent never closes tracker items itself. Not for individual item closure or items still under active work.'
disable-model-invocation: true
---

# Close done

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User wants to batch-close resolved or outdated tracker items. |
| Authority | Read-only preparation. The agent fetches, classifies, and presents the batch. The user performs every remote closure. The agent never executes a close call on the tracker. |
| Side effect | A prepared batch list presented to the user. No tracker item is mutated by this skill. |
| Done | A prepared batch list is presented to the user for manual closure, with each item classified as resolved or outdated and backed by evidence. |

## Inputs

- The candidate tracker items, supplied as numbers, URLs, a filter, or a query the agent can resolve against the configured tracker.
- Optional: a reason or resolution note the user will attach when closing.
- Tracker host and credentials are those already configured in the environment; the agent does not create or modify credentials.

## Classification criteria

An item qualifies for the batch only when it meets one of these evidence-backed criteria:

- Resolved: the item's tracker state is closed-done or merged, or the item references a merged pull request, commit, or deployment that addresses it. Evidence: the tracker state field, a linked PR/commit with a merged status, or a resolution comment from the assignee.
- Outdated: the item has had no activity for a period the user defines (default 90 days), and no open PR or branch references it. Evidence: the last-activity timestamp and the absence of linked open work.

Items that do not meet either criterion are excluded. List each excluded item with the reason it failed the criteria.

## Procedure

1. Resolve the supplied references or filter against the tracker read-only and fetch each item's number, title, current state, last activity timestamp, and linked PRs or branches. Done when: every supplied item is resolved with its metadata or the failing item is named.
2. Classify each item as resolved or outdated using the criteria above. Drop items that are neither and list them as excluded with the reason. Done when: every item has a classification with its evidence or an exclusion reason.
3. Prepare the final batch list: every item proposed for close with its number, title, current state, classification (resolved or outdated), and the evidence supporting it. Done when: the full batch is listed and no mutation has occurred.
4. Present the batch to the user for manual closure. State that the agent will not close any item and that the user must perform the closure on the tracker. Include the optional resolution note for the user to attach. Done when: the batch is presented and the user has the closure instructions.

## Failure and recovery

- Tracker query fails (auth, network, rate limit): stop, report the failing item and error. Retry only the read query, never a close.
- Unresolvable items (deleted, permission-denied, malformed reference): report which items could not be resolved and proceed with the rest.
- An item's state changed between fetch and presentation: re-fetch and re-classify that item before presenting.
- If no items qualify for the batch, report an empty batch with the excluded items and their reasons.
- The agent never closes, labels, or mutates any tracker item. If the user asks the agent to close items directly, state that this skill prepares the batch only and the user must perform the closure.

## Output

A batch report listing each item proposed for close (number, title, current state, classification, evidence), excluded items with reasons, and the optional resolution note for the user to attach. The report includes the tracker URL or instructions for the user to perform the closure manually.
