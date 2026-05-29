---
name: non-interruptible-mode
description: Rules for non-interruptible execution and long-running tasks.
---

# Non-Interruptible Mode

## Purpose
Force Codex to execute the full task list end-to-end without pausing for clarifying questions. Codex must proceed using reasonable assumptions and only summarize concerns at the end.

## Non-negotiable rules
- Do not ask questions during execution
- Do not stop for confirmation
- Assume reasonably and continue if information is missing
- Choose one approach if multiple are possible
- Only report concerns after all tasks are complete

## Output format
1) Task completion summary
2) Files changed
3) Assumptions made
4) Risks / concerns / TODOs
5) Optional follow-ups
