---
name: ca-watch
description: Watch a PR's CI to completion — diagnose on red, notify and offer the merge on green. Never auto-merges.
argument-hint: "<PR number | url | branch>"
---

# /ca-watch — PR CI babysitter

Watch a pull request's checks to completion without babysitting them by hand. The
wait happens server-side, so it costs nothing while CI runs; arbiter wakes once, on
the verdict — diagnoses a red, or offers you the merge on a green. Arbiter never
pulls the merge trigger.

## Precondition

Requires the GitHub CLI authenticated (`gh auth status`). If `gh` is absent or
unauthenticated, report the precondition failure naming `gh` and STOP — do not start
a phantom watcher.

## Flow

1. **Resolve the PR** from `$ARGUMENTS` (number, URL, or branch; default to the
   current branch's PR).
2. **Watch to completion** — run the watch as a **detached background task** built on
   the server-side block:
   ```
   gh pr checks <PR> --watch
   ```
   This blocks until every check finishes and then exits non-zero on failure. It is
   NOT a polling loop — there is no interval-based wake-up. Arbiter is re-invoked once
   when the watch process exits.
3. **On red** — retrieve the failing job's logs (`gh run view --log-failed` /
   `gh pr checks`) and act at the configured depth. Resolve that depth with the
   canonical resolver rather than reading the env var by hand (so the accepted
   values can't drift):
   ```
   python3 "<plugin-root>/hooks/babysit.py" --root "<project-root>" || python "<plugin-root>/hooks/babysit.py" --root "<project-root>"
   ```
   It prints one JSON line; act at its `on_red` value (`CODEARBITER_BABYSIT_ONRED`,
   default `propose`):
   - **`propose`** — name the likely cause and propose a concrete fix. Do NOT edit
     any tracked file; applying the fix routes through `/ca-fix` or `/ca-feature`.
   - **`branch`** — additionally open a `spike/fix-*` branch carrying the proposed
     change for review. That branch is a spike: it can never PR or merge. The default
     branch is left untouched.
4. **On green** — notify the user and present a merge **offer** (the `gh pr merge`
   command, ready to run). The watcher itself NEVER merges. If the PR targets the
   default branch, the merge routes through the merge-to-default hard gate — the offer
   cannot bypass it.

## On/off

A global flag, `CODEARBITER_BABYSIT` (default **off**, mirrors `CODEARBITER_PRUNE`),
governs auto-attachment: when on, `/ca-pr` auto-attaches a watcher to the PR it
opens. `/ca-watch <PR>` works ad-hoc regardless of the flag. The flag is never set on
the user's behalf — enabling it is the user's explicit choice. Both the command and
the flag are dormant in a repo without `arbiter: enabled`.

## When NOT to use

- Open the PR first → `/ca-pr`.
- Apply a fix for a diagnosed red → `/ca-fix` (or `/ca-feature`).
- Review a diff without watching CI → `/ca-review`.

## Hard gate

- MUST NOT auto-merge. Green → notify + offer only; the watcher never invokes
  `gh pr merge`.
- A merge into the default branch MUST route through the merge-to-default hard gate —
  the green offer cannot and does not bypass it.
- MUST NOT implement a polling loop that re-invokes the model on a timer — the watch
  is the server-side `gh pr checks --watch` block.
- MUST surface a missing/unauthenticated `gh` as a precondition failure, not a silent
  no-op.
- At depth `propose` MUST NOT edit any tracked file; at depth `branch` the proposed
  change lands only on an unmergeable `spike/fix-*` branch.
