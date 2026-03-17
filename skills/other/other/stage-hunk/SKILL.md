---
name: stage-hunk
description: "Stage or unstage specific hunks from a changed file in a git repo without interactive prompts. Use this skill whenever you need to partially stage or unstage hunks — for example, committing only the bug fix hunk but not the refactor, or unstaging something that was staged by mistake. Common phrases: 'commit only the X changes', 'stage that hunk', 'don't include the Y part', 'unstage the refactor'."
model: haiku
context: fork
allowed-tools: Bash(git diff *), Bash(*/stage-hunk.sh *), Bash(*/stage-hunk.sh --unstage *), Bash(*/stage-hunk.sh --list-hunks *)
---

You stage or unstage specific hunks from a file. You do NOT commit.

## Arguments

- `$ARGUMENTS[0]` — file path with changes (unstaged or staged)
- `$ARGUMENTS[1]` — plain-language description of which changes to stage/unstage, or line numbers if known

## Steps

1. List the available hunks:
   ```
   <skill-dir>/scripts/stage-hunk.sh --list-hunks $ARGUMENTS[0]
   <skill-dir>/scripts/stage-hunk.sh --list-hunks --staged $ARGUMENTS[0]
   ```
   Use `--staged` when unstaging. Prints each hunk with index, line range, and preview.
2. Match the description (`$ARGUMENTS[1]`) to the listed hunks.
3. Call the script with the hunk numbers from the list (plain integers, space-separated):
   ```
   <skill-dir>/scripts/stage-hunk.sh $ARGUMENTS[0] 2
   <skill-dir>/scripts/stage-hunk.sh $ARGUMENTS[0] 1 3 5
   <skill-dir>/scripts/stage-hunk.sh --unstage $ARGUMENTS[0] 1
   ```
4. Report what was staged/unstaged.

If `--list-hunks` output is insufficient to match the description,
try `git diff -U10 -- $ARGUMENTS[0]` for more context. If you still
can't match, report back with a summary so the caller can clarify.

