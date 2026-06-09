---
name: freeze
description: Scope or freeze which files Claude can edit during debugging, a refactor, or review. Use when edits should stay in specific dirs, or for a read-only investigate lock. Backed by a sentinel + PreToolUse hook.
effort: low
---

# Freeze — scoped edit lock

Toggle a project-local edit lock so Claude can only modify the files you intend
during a focused task (debugging, a tight refactor, a review pass). Enforced by
the `freeze-gate.sh` PreToolUse hook, which denies `Edit`/`Write`/`NotebookEdit`
outside the allow-list. No sentinel = no lock; the hook stays dormant.

The lock lives in `.claude/.freeze` — one allowed path prefix per line,
project-relative. Empty file = freeze everything.

## Usage

`/phx:freeze [args]` — resolve `$ARGUMENTS` and run the matching Bash branch.

| Invocation | Effect |
|------------|--------|
| `/phx:freeze` | Freeze ALL edits — read-only investigation mode |
| `/phx:freeze lib/app_web priv/repo` | Allow edits only under these dirs |
| `/phx:freeze status` | Show current lock state |
| `/phx:freeze off` | Lift the lock (delete the sentinel) |

### Freeze all edits (investigation mode)

```bash
mkdir -p .claude && : > .claude/.freeze
echo "Freeze ON — all edits blocked. Lift with /phx:freeze off"
```

### Scope edits to specific directories

```bash
mkdir -p .claude
printf '%s\n' lib/app_web priv/repo > .claude/.freeze
echo "Freeze ON — edits limited to: lib/app_web priv/repo"
```

Map `$ARGUMENTS` to the dirs the user named. Include any directory you still need
to write to — e.g. add `.claude` if progress/scratchpad logging must continue.

### Show status

```bash
if [ -f .claude/.freeze ]; then
  if [ -s .claude/.freeze ]; then echo "Freeze ON — limited to:"; cat .claude/.freeze
  else echo "Freeze ON — ALL edits blocked"; fi
else echo "Freeze OFF — no edit lock"; fi
```

### Lift the lock

```bash
rm -f .claude/.freeze && echo "Freeze OFF — edits unlocked"
```

## Iron Laws

1. **MANAGE the sentinel via Bash only** (`:>`, `printf`, `rm`) — NEVER via
   Edit/Write. The freeze hook gates Edit/Write and would block you from
   re-scoping or clearing the lock.
2. **NEVER leave a freeze active across unrelated tasks** — it persists until
   `/phx:freeze off`, including into later sessions. Clear it when the task ends.
3. **PATHS ARE PROJECT-RELATIVE PREFIXES, one per line** — `lib/foo` allows
   `lib/foo` and everything under it; it does NOT allow `lib/foobar`.

## Notes

- The hook denies with a reason and tells Claude not to retry, so a frozen edit
  surfaces clearly instead of failing silently.
- Pairs with `/phx:investigate` (freeze all while root-causing) and `/phx:work`
  (scope to the plan's dirs). The lock is advisory tooling, not a security
  boundary — anyone can run `/phx:freeze off`.
