---
id: sh-for-ls
title: for f in $(ls ...) — breaks on filenames with spaces / newlines
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: shell
tags: shell, warning, invariant-guard
---

# for f in $(ls ...) — breaks on filenames with spaces / newlines

`for f in $(ls ...)` breaks on filenames with spaces, tabs, newlines, or globs. The output of `ls` is meant for humans, not programs. Use a glob or `find -print0 | xargs -0`.

## Fix

Use glob `for f in *.txt` or `find ... -print0 | xargs -0`. Never parse `ls`.

## Incorrect

```shell
for f in $(ls *.txt); do
  process "$f"  # breaks on "my file.txt"
done
```

## Correct

```shell
# Glob directly
for f in *.txt; do
  process "$f"
done

# Or, when find is necessary
find . -name '*.txt' -print0 | xargs -0 -n1 process
```

## Escalate to

If this pattern is widespread in the codebase, load **invariant-guard** for the corrective workflow.
