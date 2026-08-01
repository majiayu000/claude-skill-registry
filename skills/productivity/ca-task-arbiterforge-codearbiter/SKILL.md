---
name: ca-task
description: The sanctioned task-board mutator — add a queued task, start one (flips to in-progress and stamps the date, minting a dotted ID on pick-up), or mark an in-progress task done. The only blessed write to open-tasks.md.
argument-hint: "add \"<desc>\" | start <id|\"title\"> | done <id|\"title\">"
---

# /ca-task — task-board writer

The one blessed way to mutate `<project-root>/.codearbiter/open-tasks.md`
(resolves D-1). Hand-editing the board is no longer the only path; this command keeps
every entry schema-conformant and every transition dated. The board LOGIC lives in the
pure `_taskboardlib` transforms; this command runs the thin writer
`<plugin-root>/hooks/taskwrite.py`.

## Verbs

Always put `--` before user text (a desc or title) so a value beginning with `-` is not
parsed as a flag. Interpreter fallback, same shape as the hooks: `python3 … || python …`.

- **add** — append a queued task. ID-less by default; pass `--id <group>.<type>` to mint
  a dotted ID now, `--from <origin>` for a harvest back-ref, `--boundaries a,b` for the
  security/trust boundaries it touches. The description must be nonblank and
  single-line; origin and boundary values must also stay on one line.
  - `python3 "<plugin-root>/hooks/taskwrite.py" add [--id group.type] [--from origin] [--boundaries a,b] -- "<desc>" || python "<plugin-root>/hooks/taskwrite.py" add ... -- "<desc>"`
- **start** — flip a task to in-progress and **stamp the started date** (so it can never
  be a dateless `[~]`). On an ID-less item, pass `--as <group>.<type>` to mint its dotted
  ID at pick-up. `--date YYYY-MM-DD` overrides today.
  - `python3 "<plugin-root>/hooks/taskwrite.py" start [--as group.type] [--date YYYY-MM-DD] -- "<id|title>"`
- **done** — flip an in-progress task to done and stamp the done date (`--date`
  overrides today). A queued task must be `start`ed first.
  - `python3 "<plugin-root>/hooks/taskwrite.py" done [--date YYYY-MM-DD] -- "<id|title>"`

A missing target, an already-matching state, an out-of-order transition, a malformed
add field or `--date`, or an invalid `GROUP.TYPE` namespace is reported and writes
nothing (exit 1).
A queued `done` identifies the task as queued and tells the caller to `start` it first.
**Targeting by title is best-effort:**
prefer the dotted ID, and
note that if two ID-less items share a title, `start`/`done` act on the first — give one
an ID (`/ca-task start --as <group>.<type> -- "<title>"`) to disambiguate.

## When NOT to use

- Promoting workflow follow-ups in bulk → that is the harvest
  (`<plugin-root>/includes/harvest.md`), which calls this writer for you.
- Reading the board / counts → `/ca-status` (read-only).
- Archiving long-settled done items → deferred (D-2); done items stay in-place for now.
- Filing a separate `chore(board)` PR just to flip a task state → task-board transitions
  (`[x]` done-flip, `[~]` start-flip, new `[ ]` add) ride the **work commit** via
  commit-gate, co-located atomically with the code that completes, starts, or spawns the
  task (ADR-0008). A lagging board-only PR is the anti-pattern this design eliminates.

## Hard gate

- MUST write the board only through `taskwrite.py` (the pure transforms), never a
  free-hand Edit that can malform the schema.
- `start` MUST stamp a started date — never leave a dateless `[~]`.
- `done` MUST target an in-progress task — a queued task must go through `start` first.
- MUST NOT delete a task to "complete" it — mark it `done` so the record survives.
