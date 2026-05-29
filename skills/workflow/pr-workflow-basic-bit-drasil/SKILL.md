---
name: pr-workflow
description: Land changes via PRs with CI + AI review loops (issue -> branch/worktree -> PR).
compatibility: opencode
---

## Reference

- Canonical workflow: `docs/dev/pr-workflow.md`
- PR template: `.github/pull_request_template.md`
- Worktrees: `docs/dev/worktrees.md`

## Quick local gate

```bash
npm ci
npm run format:check
npm run check
```

## Merge readiness

- Required checks pass.
- PR review threads are resolved (or explicitly addressed).

## Notes

- Never paste secrets into PRs.
- If build fails due to missing Prisma client types, run `npm run prisma:generate`.
