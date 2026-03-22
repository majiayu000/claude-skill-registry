---
name: kanban-based-development
description: >
  Autonomous, parallel-safe development workflow using kanban-md.
  Use when the user asks to work through tasks, do kanban-based development,
  or when multiple agents need to coordinate work on the same codebase.
  Optimized for explicit handoffs and a "defer to user" protocol when
  human intervention is required.
allowed-tools:
  - Bash(kanban-md *)
  - Bash(kbmd *)
  - Bash(git *)
  - Bash(go *)
  - Bash(golangci-lint *)
  - Bash(awk *)
---
<!-- kanban-md-skill-version: 0.31.0 -->

# Kanban-Based Development

Autonomous, parallel-safe development using `kanban-md` to coordinate work on a shared board.
Claims prevent duplicate work; `review` is the waiting room (handoff, user action, merge, decisions).

## Multi-Agent Environment

**This board is shared.** Multiple agents and humans may be working on it simultaneously. You are NOT the only one reading or modifying tasks. This means:

- Another agent may claim a task between the time you list it and try to pick it.
- Tasks you saw as available a moment ago may no longer be available.

The **claim** mechanic is the coordination primitive. It prevents two agents from working on the same task. **You MUST claim a task before starting any work on it, and you MUST only pick unclaimed tasks.** Violating this causes duplicate work, merge conflicts, and wasted effort.

## Non-Negotiables

- **Claim before you change anything.** No task edits, no code changes.
- **One active task per agent.** Keep at most one task in `in-progress` for your agent session.
- **Never steal a live claim.** If it's claimed, pick something else.
- **Never release someone else’s claim.** Only use `edit --release` for your own work (or when the user explicitly asks).
- **Always leave a handoff.** Before you park a task, write a short update in the body so someone else can continue.
- **Refresh claims to avoid timeout.** If the task might take longer than `claim_timeout`, periodically renew your claim: `kanban-md edit <ID> --claim <agent>`.

## Board Home vs Worktrees (simple rule)

- **Always run `kanban-md` from board home** (the canonical repo directory that owns the shared board).
- **Always do code changes in a task worktree.** Never edit code in board home.
- If the board is git-tracked, **commit board changes on `main` as a separate commit** after the task is merged and moved to `done`.

At the start of the session, determine and remember `<board-home>`:

```bash
cd <the canonical repo directory that owns the shared board>
pwd   # remember this path as <board-home>
```

Recommended: keep two shells (or split panes) open:

- **Board shell** at `<board-home>` for `kanban-md` commands
- **Worktree shell** at the task worktree for code changes

Do not run multiple mutating `kanban-md` commands in parallel against the same board directory.

If you are unsure you’re using the shared board, run `kanban-md board --compact` and confirm the board name/shape is what you expect.

## Defer-to-User Boundary (exceptions)

By default, agents should take tasks all the way to `done` (worktree → commit → merge → done).

Defer to the user (leave the task in `review` with a handoff) only when you need:

- an important product/spec decision with multiple valid options and no clear winner
- credentials/access or external actions (push to remote, releases, deployments, ENV variables, etc.)
- a merge conflict that requires judgment (not just mechanical resolution)
- repeated test/lint failures you can’t resolve

## Agent Identity (for claims)

Each agent session must generate a unique name to identify itself for claims. At the very start of a session, run:

```bash
kanban-md agent-name
```

This produces a name like `quiet-storm` or `frost-maple`. **Remember this name in your context** and use it as a literal string in all claim/release commands for the rest of the session. Do not store it in a file or environment variable — those are not persistent or isolated between agents.

Example: if the generated name is `frost-maple`, use `--claim frost-maple` in every claim command.

## Default Loop (worktree → merge → done)

Use `--compact` for board/list/log output whenever available to keep output short.

Before picking work, ensure board home is on `main`:

```bash
cd <board-home>
git switch main
git status
```

### 1) Pick and claim (atomically)

From board home:

Pick only from startable columns to avoid accidentally re-picking `review` work:

```bash
kanban-md pick --claim <agent> --status todo --move in-progress
```

If `todo` is empty:

```bash
kanban-md pick --claim <agent> --status backlog --move in-progress
```

This is atomic — if another agent claims the task between your list and claim, `pick` handles it safely. No need to list/choose/claim manually.

By default, `pick` prints the picked task details (including body), so a separate `show` is not required. Use `--no-body` only when you want the one-line confirmation.

### 2) Create a worktree (default)

Create a worktree for the task branch from board home:

```bash
git worktree add ../kanban-md-task-<ID> -b task/<ID>-<kebab-description>
cd ../kanban-md-task-<ID>
```

Skip a worktree only for truly non-conflicting work (e.g., board-only changes or writing an untracked research report). If you touch tracked code/config, use a worktree.

### 3) Implement, test, commit (in the worktree)

Implement the smallest change that satisfies the task.

- Bugs: write a failing test first (TDD), then fix.
- Run the appropriate checks for the change (common defaults):
  - `go test ./...`
  - `golangci-lint run ./...`

Commit in the worktree when green:

```bash
git add <files>
git commit -m "feat: <description>"
```

### Progress notes (recommended)

While a task is `in-progress`, leave short timestamped notes in the task body from **board home** (especially after major steps or before/after running tests). This makes handoffs and reviews much faster.

```bash
kanban-md edit <ID> --append-body "Implemented X/Y/Z, now running tests." --timestamp --claim <agent>
```

The `--append-body` (`-a`) flag appends text to the existing body without replacing it. The `--timestamp` (`-t`) flag prefixes a timestamp line like `[[2026-02-10]] Mon 15:04`.

### 4) Merge to main (from board home)

Switch back to board home and merge your task branch:

```bash
cd <board-home>
git switch main
git status
```

If `git status` shows unexpected changes outside the board directory (usually `kanban/`) or a git operation in progress, do not proceed. Park the task in `review` and move on.

Merge and re-run tests on main:

```bash
git merge task/<ID>-<kebab-description>
go test ./...
golangci-lint run ./...
```

If you cannot merge right now (e.g., another merge/rebase is in progress), do **not** force. Park the task in `review`, leave a note (branch name + what’s left), and pick the next task.

To park a “ready to merge” task:

From board home:

```bash
kanban-md handoff <ID> --claim <agent> --note "Ready to merge: task/<ID>-…; remaining: …" --timestamp --release
```

### 5) Mark done (only after merge)

Only after the merge is on main and checks pass:

From board home:

```bash
kanban-md edit <ID> --release
kanban-md move <ID> done
```

### 6) Commit board changes (only if board is git-tracked)

From board home:

```bash
git add kanban/config.yml kanban/tasks/
git commit -m "chore(board): update task #<ID>"
```

### 7) Optional cleanup

```bash
git worktree remove --force ../kanban-md-task-<ID>
git branch -d task/<ID>-<kebab-description>
```

## Blocked / Needs User Input (the “review and move on” rule)

If you cannot continue without the user (decision, access, environment, or anything outside your control):

From board home:

```bash
kanban-md handoff <ID> --claim <agent> \
  --block "Waiting on user: <what you need>" \
  --note "## Handoff
- Current state:
- Branch (if any):
- Open questions (A/B):
- Next step:" \
  --timestamp --release
```

In your handoff note, include:

- The exact question(s) for the user (prefer A/B options)
- What you already tried and what happened
- The minimal next step after the user responds

Then pick the next task. Do not idle.

## Resuming a parked task

When the user answers and you need to continue, re-claim and move back to `in-progress`:

From board home:

```bash
kanban-md edit <ID> --claim <agent>
kanban-md edit <ID> --unblock --claim <agent>   # if it was blocked
kanban-md move <ID> in-progress --claim <agent>
```

## Status meanings (keep the board honest)

| Status | Meaning |
|---|---|
| `in-progress` | Actively being worked by an agent right now |
| `review` | Waiting state: ready to merge, or waiting on user/decision/unblock |
| `done` | Merged to main (and checks pass) |

## When there is nothing to pick

If `pick` returns "no unblocked, unclaimed tasks found":

- Check blocked work: `kanban-md list --compact --blocked`
- Check waiting work: `kanban-md list --compact --status review`
- If everything is waiting on the user, ask targeted questions and stop (don't thrash the board).
