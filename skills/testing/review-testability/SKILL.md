---
name: review-testability
description: Audit code for testability design patterns. Identifies business logic entangled with IO and suggests functional core / imperative shell separation.
context: fork
---

Use the code-testability-reviewer agent to perform a testability audit on: $ARGUMENTS

If no arguments provided, analyze the git diff between the current branch and main/master branch.
