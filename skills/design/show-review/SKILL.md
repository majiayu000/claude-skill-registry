---
name: show-review
description: 'Use when the answer is a walk through the diff rather than a review report: the user says "walk me through this review", "walk me through this PR", "show-review", or "review this interactively". Emits one finding per turn as an ephemeral visual and a Keep/Skip/Discuss question. A written sectioned report goes to review; a GitHub PR sectioned report goes to pr-review; showing a topic without reviewing it goes to show-me.'
argument-hint: "Which diff should we walk?"
---

Walk the change as a sequence of one-finding visuals. Skip the preamble. Keep prose to the line or two the visual needs.

## Scope

Named files, a PR number (`gh pr diff`), the working tree, or the branch against its base. An empty change-set is `0 findings.` then stop. Binary, lockfile, and generated paths are not findings.

## A turn

This message is one finding. Highest remaining first. Remaining titles stay unsaid. A count, if you have one, belongs on the first turn only, in the same message as that finding.

Rank in place by reachable impact: ship-blocker and wrong-on-plausible-input first, degraded uncommon path next, no-behavioral-impact last. Nits take this same Keep/Skip path, Skip first. A line that is not a defect is not a finding. Read enough of the change-set to name the current highest finding; do not write a findings list.

1. The smallest view that carries the defect.
2. One or two lines: what is wrong, the reachable impact, `file:line`.
3. One single-select: Keep / Skip / Discuss. `(Recommended)` on the first option.

```diff
 on(save)
-  write content
+  if content is unchanged
+    return cached result
+  write new content
```

Unchanged content returns a stale cache when another process wrote. `cache.ts:40`

Keep (Recommended) / Skip / Discuss?

Print the visual in the message body next to the two lines, not in the question-tool preview. Use the harness question tool when it exists (labels only); otherwise number the three options. The next message is the answer. A turn is done when Keep or Skip is in hand.

Recommended first: Keep for a named reachable failure; Skip for a no-behavioral-impact nit.

Discuss is one round, then Keep / Skip only. A new defect raised in Discuss waits until this finding has Keep or Skip.

After eight behavioral turns, one single-select: skip the rest (Recommended) / continue. Skip the rest counts unseen findings as skipped. Keep the rest counts them as kept. Either phrase, on any turn, closes the walk.

An empty remaining list goes to Close.

## Pick the view

Pick the view the way `show-me` does: its shapes, a diff matched to the view it changes, mermaid or nomnoml for a diagram. The point is the defect.

| The defect is | View |
|---|---|
| a change against a shape that already exists | focused diff |
| logic or an algorithm | pseudocode |
| what calls what at runtime | call tree |
| UI structure or a module boundary | component tree |
| file responsibility | shallow file tree |
| interaction or data flow between parts | diagram |
| new code, or a missing shape | whole block |

One view is the common case. Cut every line the defect does not turn on.

## Close

The queue is empty, or the rest is skipped. One-line tally: kept, skipped, how many were discussed. If kept is empty, stop. Otherwise one single-select: Stop (Recommended) / apply kept with `fix` / grill kept with `review-fix-grill-loop`. Close is done when that answer is in hand. The walk does not patch.

## Boundaries

- Nothing here lands on disk. Every view is chat output.
- A written sectioned report goes to `review`.
- A GitHub PR sectioned report goes to `pr-review`.
- A topic shown without reviewing it goes to `show-me`.
- A grill-until-clean pass without a visual walk goes to `review-fix-grill-loop`.
