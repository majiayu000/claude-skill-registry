---
id: sh-unquoted-var
title: Unquoted $var — word splitting and glob expansion
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: shell
tags: shell, warning, invariant-guard
---

# Unquoted $var — word splitting and glob expansion

An unquoted `$var` is subject to word splitting (on `$IFS`) and glob expansion. A path with a space, a tab, or a `*` will silently do the wrong thing.

## Fix

Quote: `"$var"`. Use `"${arr[@]}"` for arrays. Required even for paths you trust.

## Incorrect

```shell
if [ -d $dir ]; then echo yes; fi
# If $dir = "/tmp/with space", expands to: [ -d /tmp/with space ] — syntax error
```

## Correct

```shell
if [ -d "$dir" ]; then echo yes; fi
# Always quote. For arrays: "${arr[@]}".
```

## Escalate to

If this pattern is widespread in the codebase, load **invariant-guard** for the corrective workflow.
