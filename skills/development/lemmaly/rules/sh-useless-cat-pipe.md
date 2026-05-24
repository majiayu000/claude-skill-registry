---
id: sh-useless-cat-pipe
title: cat file | cmd — useless use of cat (UUOC)
severity: info
impact: MEDIUM
impactDescription: Suboptimal; flag when n is large or on a hot path
language: shell
tags: shell, info
---

# cat file | cmd — useless use of cat (UUOC)

`cat file | cmd` reads the file and pipes through `cat` just to feed `cmd`. Every command that takes a file argument can read it directly — one fewer process, clearer intent.

## Fix

Run the command on the file directly: `grep ... file` instead of `cat file | grep ...`.

## Incorrect

```shell
cat access.log | grep "500"
```

## Correct

```shell
grep "500" access.log

# Or stdin redirection if the command takes only stdin:
cmd < access.log
```
