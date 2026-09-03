---
name: move-to-worktree
description: "After /start-task: park the current clean, pushed feature branch in its own issue-numbered nested worktree (.worktrees/<issue#>) and return the primary checkout to current main, so the next parallel lane can start. Use when the user says to move the branch or task to a worktree or open a parallel lane."
model: inherit
color: cyan
---

# Move-to-Worktree

Companion to `/start-task` for parallel Phase 4 lanes. `/start-task` leaves the
primary checkout *on* the new feature branch; this skill moves that branch into
its own worktree and puts the primary back on the default branch — one
worktree + one branch + one agent session per in-flight issue.

## Run (1 bash call)

```bash
bash {base_directory}/move-to-worktree.sh
```

No arguments — it operates on the branch currently checked out. The script:

1. Hard-stops unless run in the **primary checkout**, on a **task branch**
   (`{type}/{issue#}/{slug}`), with a **clean tree** and its upstream set to
   **`origin/<branch>`** literally (not a fork-style `upstream` remote) — i.e.
   exactly the state `/start-task` leaves behind. Also hard-stops unless
   `.worktrees/` is **gitignored**: the worktree is nested inside the repo, so an
   unignored one gets staged by any `git add -A` as an embedded gitlink, committing
   this lane's HEAD onto another branch. Remedy is one line in `.gitignore`; the
   script never edits it for you.
2. Fetches `origin/<branch>` so the behind-check reflects reality, then pushes any
   local-only commits and checks out the default branch (this must happen *before*
   the worktree is created — git refuses to check out a branch in two places).
3. `git worktree add .worktrees/<issue#> <branch>` — nested inside the repo root,
   never a `../` sibling. The context file `specs/context/<issue#>.md`
   travels with the branch (it's committed). If this step fails, the script returns
   the primary checkout to the feature branch rather than stranding it on the
   default branch with no lane created.
4. Fast-forwards the default branch **after** the lane is parked. A failure here is
   reported as a warning, not an error — the move already succeeded.

Non-zero exit → hard-stop, print stderr verbatim.

## Report

The script's summary block (worktree path, branch), plus: *"Prepare the worktree
as your project requires (install dependencies, configure ports, etc.), then
open a new agent session there and continue the pipeline
(`/plan-architecture` / `/implement` → `/review` → `/commit` → PR with
`Closes #N`)."*

When the PR has squash-merged, `/finish-worktree <issue#>` (run back in the
primary) does the teardown.

## You Must NOT

- Run the underlying git commands yourself — the script owns all mutation.
- Stash, discard, or commit anything to satisfy the clean-tree check — hard-stop instead.
- Edit `.gitignore` yourself to satisfy the gitignore check — report the remedy and stop.
- Move a branch whose upstream is ahead or does not match `origin/<branch>`.
- Create the worktree while the primary is still on the feature branch.
- Install dependencies, write port configuration, or otherwise touch the project's
  toolchain — that's the developer's job once the worktree exists.
