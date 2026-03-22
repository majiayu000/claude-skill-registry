---
name: fix-ci
description: "(ePost) Fix CI pipeline failures"
user-invokable: true
context: fork
agent: epost-debugger
metadata:
  argument-hint: "[CI failure description or log URL]"
  connections:
    extends: [fix]
---

# Fix CI Pipeline Failures

Direct CI fix — skip auto-detection, go straight to CI debugging.

<issue>$ARGUMENTS</issue>

## Process

1. **Examine CI logs** — identify the failing step and error output
2. **Identify failure point** — parse error messages, exit codes, build output
3. **Reproduce locally** — run the same commands/tests that failed in CI
4. **Fix** — apply the minimal correct fix
5. **Verify** — re-run the failing command locally to confirm fix
6. **Test** — run full test suite to catch regressions

## Rules

- Fix root causes, not symptoms
- Do not disable or skip failing CI checks
- If CI config needs changes, explain why
