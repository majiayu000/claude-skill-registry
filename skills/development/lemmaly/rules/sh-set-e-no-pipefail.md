---
id: sh-set-e-no-pipefail
title: set -e without set -o pipefail — failures inside pipes are masked
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: shell
tags: shell, warning, invariant-guard
---

# set -e without set -o pipefail — failures inside pipes are masked

`set -e` exits on a failed command, but a failure in the middle of a pipe is masked — only the *last* command's exit status counts. `set -o pipefail` fixes it. `set -u` catches unset variables.

## Fix

Use `set -euo pipefail` so the script also fails when an earlier stage in a pipe fails.

## Incorrect

```shell
#!/bin/bash
set -e
some_failing_step | grep needle # if some_failing_step fails, script keeps going
```

## Correct

```shell
#!/bin/bash
set -euo pipefail
some_failing_step | grep needle # any failure in the pipe aborts the script
```

## Escalate to

If this pattern is widespread in the codebase, load **invariant-guard** for the corrective workflow.
