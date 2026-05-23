---
name: push-pr
description: Push branch and create GitHub PR
user-invocable: true
---

# Push Branch and Create Pull Request

## Steps

1. **Get current feature from branch**:

   ```bash
   BRANCH=$(git rev-parse --abbrev-ref HEAD)
   NUM=$(echo "$BRANCH" | grep -oE 'alg-([0-9]+)' | grep -oE '[0-9]+')
   ```

2. **Run verification**:

   ```bash
   npm run type-check --workspaces --if-present
   npm test --workspaces --if-present
   ```

3. **If verification fails**, stop and report errors.
   Do NOT proceed to create a PR with failing checks.

4. **Push branch to remote**:

   ```bash
   git push -u origin $BRANCH
   ```

5. **Generate PR title** using [Conventional Commits](https://www.conventionalcommits.org/):
   - Read `specs/alg-${NUM}-*/spec.md` to understand the feature
   - Generate a title like: `feat(scope): short description`
   - **Types**: `feat` (new feature), `fix` (bug fix), `refactor`, `perf`, `docs`, `chore`
   - **Scope**: optional component name, e.g. `feat(search):`, `fix(auth):`

6. **Create PR with gh CLI** (following `.github/PULL_REQUEST_TEMPLATE.md`):

   ```bash
   gh pr create \
     --title "${TITLE}" \
     --body "## Summary

   Resolves [ALG-${NUM}](https://linear.app/algojuke/issue/ALG-${NUM})

   See [spec.md](specs/alg-${NUM}-*/spec.md) for full specification.

   ## Changes

   $(git log main..HEAD --oneline)

   ## Verification

   - [x] Type check passes
   - [x] Tests pass
   "
   ```

7. **Output the PR URL** for the user.

## Notes

- The PR body uses "Resolves [ALG-XX](url)" to link the Linear issue
- Linear automation will automatically update the issue status to "In Review" when the PR is created
- If the branch already has a PR, `gh pr create` will fail - use `gh pr view` instead
- Always run verification before pushing to catch issues early
