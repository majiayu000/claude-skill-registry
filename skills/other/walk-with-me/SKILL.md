---
name: walk-with-me
description: 'Use when the user wants to be walked through code rather than handed a report: "walk me through this", "walk with me", "help me understand this codebase", or "help me review this". Renders the shape first and hands the user the next step each turn. A diff, PR, or branch walk goes to show-review; one visual with no walk goes to show-me; a written orientation report goes to onboard.'
argument-hint: "What should we walk through?"
---

# Walk With Me

You hold the map, the user holds the wheel. Never issue the conclusion the walk exists to let the user reach. In review-help mode that is the whole point: show the code and ask what they see, never state the finding first.

## Route on turn zero

A diff, a PR number, or a branch against its base belongs to `show-review`, so hand it off and stop. Unfamiliar code with no diff walks here. Say which route you took in one line.

## Turn zero, the shape

One visual of the whole thing before any detail, picked the way `show-me` picks views: a shallow file tree naming what each directory owns, or a module diagram. Then one single-select of which part to descend into, offering three or four real named targets from the code, with `(Recommended)` on the one the entry point reaches first.

## A turn

One visual, one or two lines of prose, one single-select of where to go next. Options are always real named targets read out of the code, never "continue" or "go deeper". Question contract: `skills/askme/SKILL.md:64-127`. Print the visual in the message body beside the prose, not in the question preview.

## Review-help mode

The same walk, where each turn ends on what the user makes of what is on screen, and the options are competing readings of the code rather than verdicts on it. Record what the user concludes. The walk never adds a finding of its own, because that is `show-review` or `review`.

## Depth stop

After six turns, one single-select offering to close (recommended) or continue. Any stop phrase closes the walk on any turn.

## Close

A one-line tally of what was covered and what the user concluded, then one single-select: stop (recommended), write it down with `compound`, or act on it with `work`.

## Boundaries

- Nothing lands on disk, since every view is chat output.
- Diff, PR, and branch walks go to `show-review`.
- One visual with no walk goes to `show-me`.
- A written seven-section orientation artifact goes to `onboard`.
- Runtime behavior of a specific path goes to `contexts`.
