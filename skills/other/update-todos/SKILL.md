---
name: update-todos
description: 'Re-sync a stale task list against what actually landed: mark real completions with proof, drop overtaken items, add discovered blockers, re-order what moved. Use when the user says "update the todos", "re-sync the task list", or the plan and the tree have drifted apart. To deepen a list that is too coarse rather than stale, use sophisticate-todos.'
metadata:
  short-description: 'Re-derive the task list from current reality'
---

# update-todos

A task list drifts the moment work starts. Items get done sideways, get overtaken by a design change, or turn out to be blocked on something nobody saw. A list that no longer matches the tree is worse than no list, because it is trusted.

This skill is temporal: it reconciles the list against what actually happened. For a list that is accurate but too coarse to execute, use `sophisticate-todos` instead.

## Reconcile

Three-way comparison: the list as written, the tree as it stands, and what the conversation established.

Classify every existing item exactly once:

| Class | Meaning |
|---|---|
| `landed` | Done, with proof |
| `still-open` | Unchanged, still required |
| `overtaken` | A design change made it unnecessary |
| `blocked` | Cannot proceed until something external clears |
| `newly-discovered` | Not on the list; found during the work |

A `landed` claim requires proof: the test, the command output, or the `path:line` that demonstrates it. An unproven completion stays `still-open`. Someone saying an item is done is not proof; it is the claim under test.

**Completion criterion:** every pre-existing item carries exactly one classification, and every `landed` cites its proof.

## Apply

Write the reconciled list back through the `todo` tool.

An `overtaken` item is dropped with a one-line reason recorded in the report, never deleted silently. A dropped item with no recorded reason is indistinguishable from an item you forgot.

**Completion criterion:** the written list contains no item whose classification contradicts its recorded state.

## Report

Emit the delta only: what changed classification, and why.

**Completion criterion:** the report accounts for every item whose state moved, and says nothing about items that did not move.
