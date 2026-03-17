---
name: check-pr
description: When you submit a PR (or push a change to a branch that already has a PR), wait for CI checks to perform, and process them.
---

Repeat the following loop until the PR is fully approved and CI is green:

1. **Check for conflicts** - Pull the latest `main` branch from origin and check that there is no conflict with the current branch. If there are any, fix them and push, and restart the loop
2. **Check CI status** - Poll GitHub Actions until all checks complete, wait if needed.
3. **If CI failed** - Investigate the failure, implement the minimal fix, push, and restart the loop
4. **Check reviews** - Look for comments from both human reviewers and agent reviewers
5. **If changes requested** - Implement the requested changes (only what's needed), push, and restart the loop

Before each push, verify you're not introducing more changes than required.
After each push, post a comment summarizing what you changed so reviewers (human and agent) can track your work

Keep iterating until:

- There are no conflict and the branch is up to date
- All CI checks pass
- All reviewer comments are addressed
