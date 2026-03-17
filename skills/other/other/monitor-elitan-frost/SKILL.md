---
name: monitor
description: Monitor a PR until CI is 100% green, fixing any failures
---

Monitor this PR and ensure it's 100% green. If any CI checks fail, analyze the failure, fix the issue, and push the fix. Repeat until all checks pass.

Steps:
1. Get current PR status with `gh pr checks`
2. If all green, done
3. If any failing, get the failure logs
4. Analyze and fix the issue
5. Commit and push the fix
6. Sleep 60s between status checks (CI can take a while)
7. Repeat until 100% green

$ARGUMENTS
