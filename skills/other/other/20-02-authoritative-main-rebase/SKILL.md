---
name: 20-02-authoritative-main-rebase
description: Execute a rebase onto main when main changes are authoritative and conflict-free, without merging.
---

# 20.02 Authoritative-Main Rebase (Execute)

⛔ **ONLY RUN THIS AFTER HUMAN CONFIRMED WITH `[R]`**

## Instructions:

When you are 100% sure a rebase would not drop changes from existing main (main changes generally are authoritative- **if in any way you are not 100% sure ask hooman**) then **rebase** - **DO NOT MERGE YET**

If you have a very complicated rebase- an advised strategy is to create a new temporary worktree in `.worktrees/` to avoid conflict hell.

## ⛔ STOP HERE — WAIT FOR HUMAN

Report the rebase result. Do NOT proceed to merge (20.03).
The human must explicitly say `[M]` before you merge.
