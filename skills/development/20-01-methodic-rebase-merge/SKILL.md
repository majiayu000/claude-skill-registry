---
name: 20-01-methodic-rebase-merge
description: Investigate rebase conflicts against local main before executing, plan resolution for each conflict in advance.
---

# 20.01 Methodic Rebase-Merge (Investigate)

⛔ **THIS SKILL IS INVESTIGATE ONLY. DO NOT REBASE. DO NOT PROCEED TO 20.02.**

## Instructions:

ok I need you to pay sharp fucking full attention, no rushing
- **ALWAYS MAKE SURE YOU'RE ON THE RIGHT BRANCH IN THE RIGHT DIRECTORY (CRITICAL)**
- commit everything in worktree
- backup branch from that
- INVESTIGATE what would happen if we rebase on **local main**, and I mean it- need to see the conflicts up front so we're not surprised, we know in advance how to solve it all
	- you make a plan to solve each conflict in advance
	- display that in a way I can read it

If you have a very complicated rebase- an advised strategy is to create a new temporary worktree in `.worktrees/` to avoid conflict hell.

## ⛔ STOP HERE — WAIT FOR HUMAN

Present your investigation and conflict plan. Do NOT proceed to rebase.
The human must explicitly say `[R]` before you run 20.02.

*after any rebase (only when human confirms with [R])*
- run applicable tests
- verify integrity / loss of important details
- are things wired up? or unwired?
