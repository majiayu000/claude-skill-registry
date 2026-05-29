---
name: pr
description: INVOKE THIS SKILL before creating any PR to ensure compliance with branch naming, changelog requirements, and reviewer assignment.
---

# ActivityPub PR Workflow

## Branch Naming

| Prefix | Use |
|--------|-----|
| `add/{feature}` | New features |
| `update/{feature}` | Iterating on existing features |
| `fix/{bug}` | Bug fixes |
| `try/{idea}` | Experimental ideas |

**Reserved:** `release/{X.Y.Z}` (releases only), `trunk` (main branch).

## Pre-PR Review

Before creating a PR, delegate to the **code-review** agent to review all changes on the branch. Address any critical issues before proceeding.

## PR Creation

**Every PR must:**
- Assign `@me`
- Add `Automattic/fediverse` as reviewer
- Include changelog entry OR "Skip Changelog" label
- Pass CI checks
- Merge cleanly with trunk

```bash
# Create PR (includes required assignment/reviewer)
gh pr create --assignee @me --reviewer Automattic/fediverse
```

**Use the exact template from `.github/PULL_REQUEST_TEMPLATE.md`** — do not create custom formatting.

## Changelog

End all changelog messages with punctuation:
```
✅ Add support for custom post types.
❌ Add support for custom post types
```

Add manually if forgotten:
```bash
composer changelog:add
git add . && git commit -m "Add changelog entry" && git push
```

See [release](../release/SKILL.md) for complete changelog details.

## Workflow

### Create Branch
```bash
git checkout trunk && git pull origin trunk
git checkout -b fix/notification-issue
```

### Pre-Push Checks
```bash
composer lint         # PHP standards (composer lint:fix to auto-fix)
npm run lint:js       # If JS changed
npm run lint:css      # If CSS changed
npm run env-test      # Run tests
npm run build         # If assets changed
```

See [dev](../dev/SKILL.md) for complete commands.

### Keep Branch Updated
```bash
git fetch origin
git rebase origin/trunk
# Resolve conflicts if any
git push --force-with-lease
```

## Special Cases

**Hotfixes:** Branch `fix/critical-issue`, minimal changes, add "Hotfix" label, request expedited review.

**Experimental:** Use `try/` prefix, mark as draft, get early feedback, convert to proper branch type once confirmed.

**Multi-PR features:** Create tracking issue, link all PRs, use consistent naming (`add/feature-part-1`, etc.), merge in order.

## Labels

| Label | Use |
|-------|-----|
| `Bug` | Bug fixes |
| `Enhancement` | New features |
| `Documentation` | Doc updates |
| `Code Quality` | Refactoring, cleanup, etc. |
| `Skip Changelog` | No changelog needed |
| `Needs Review` | Ready for review |
| `In Progress` | Still working |
| `Hotfix` | Urgent fix |

## Reference

See [Pull Request Guide](../../../docs/pull-request.md) for complete workflow details.
