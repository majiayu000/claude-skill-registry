---
name: release
description: Full release workflow - changelog, tests, PR, merge, tag, publish. Use /release [patch|minor|major] or /release (auto-detect).
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task, WebFetch
---

# Release Workflow

You are executing a full release cycle for this project. Follow every step in order. Do NOT skip steps. Do NOT add "Co-Authored-By" to any commit or PR.

## Input

- `$ARGUMENTS` = version bump type: `patch`, `minor`, or `major`
- If empty, auto-detect from commits since last tag using conventional commits:
  - `feat` commits → `minor`
  - `fix`/`refactor`/`docs`/`chore` only → `patch`
  - `BREAKING CHANGE` or `!` in commit → `major`

## Pre-flight checks

Before starting, verify all of these. If any fail, STOP and report:

```bash
# Must be on a feature branch, not main/master
git branch --show-current

# Must have a clean working tree (no uncommitted changes except untracked spike/ files)
git status --porcelain

# Must be authenticated with GitHub
gh auth status

# Must have the remote configured
git remote -v
```

## Step 1: Determine version

```bash
# Get last tag
git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0"

# Get commits since last tag
git log $(git describe --tags --abbrev=0 2>/dev/null || echo "HEAD~50")..HEAD --oneline --no-decorate
```

- Parse current version from `package.json`
- Apply bump type to calculate new version
- Store as `NEW_VERSION` (e.g., `1.8.0`) and `NEW_TAG` (e.g., `v1.8.0`)

## Step 2: Update CHANGELOG.md

Read `CHANGELOG.md` and the [changelog-guide.md](changelog-guide.md) for format rules.

- Move everything under `## [Unreleased]` into a new `## [NEW_VERSION] - YYYY-MM-DD` section
- Categorize commits into: Added, Changed, Improved, Fixed, Removed, Documentation
- Write clear, user-facing descriptions (not raw commit messages)
- Leave `## [Unreleased]` empty for future changes
- Add the new version link at the bottom of the file

## Step 3: Update README.md

Read the current README.md. Only update if:
- There are new features that should be highlighted
- Installation instructions changed
- There are breaking changes that affect usage

If no relevant changes, skip this step and say so.

## Step 4: Bump version in package.json and VS Code extension

```bash
# Bump root package.json (no git tag — we tag manually later)
npm version NEW_VERSION --no-git-tag-version

# Bump VS Code extension version to match
cd vscode-extension && npm version NEW_VERSION --no-git-tag-version && cd ..
```

Both `package.json` files must have the same version so the release workflow publishes both npm and the VS Code Marketplace extension with matching versions.

## Step 5: Run full checks

```bash
pnpm format:fix   # always run first — auto-fixes style, prevents CI failures
pnpm check
```

This runs `typecheck + lint + test`. If ANY check fails:
1. Read the error output carefully
2. Fix the issue
3. Run `pnpm check` again
4. Repeat until all checks pass (max 5 attempts)

If after 5 attempts checks still fail, STOP and report the issue.

## Step 6: Commit

Stage only the relevant files and commit:

```bash
git add CHANGELOG.md README.md package.json pnpm-lock.yaml vscode-extension/package.json
git commit -m "chore(release): bump version to NEW_VERSION"
```

IMPORTANT:
- Do NOT add `Co-Authored-By` to the commit message
- Do NOT use `--no-verify`
- Only stage files that were actually modified

## Step 7: Push branch

```bash
git push origin $(git branch --show-current)
```

## Step 8: Create PR to main

Create a PR using the template from [pr-template.md](pr-template.md).

```bash
gh pr create --base main --title "chore(release): vNEW_VERSION" --body "BODY_FROM_TEMPLATE"
```

IMPORTANT:
- Do NOT add `Co-Authored-By` in the PR body
- Fill in the template with actual changes from the changelog
- Include the version number and key changes

## Step 9: Wait for CI checks

```bash
gh pr checks --watch
```

If any check fails:
1. Read the failure details: `gh pr checks`
2. Get the failing run logs if needed: `gh run view RUN_ID --log-failed`
3. Fix the issue locally
4. Commit the fix: `git commit -m "fix: resolve CI failure in AREA"`
5. Push: `git push`
6. Wait again: `gh pr checks --watch`
7. Repeat until all checks pass (max 5 cycles)

If after 5 cycles checks still fail, STOP and report.

## Step 10: Merge PR to main

```bash
gh pr merge --squash --delete-branch
```

## Step 11: Create and push tag

```bash
git checkout main
git pull origin main
git tag vNEW_VERSION
git push origin vNEW_VERSION
```

This triggers the `release.yml` workflow which:
- Runs tests
- Builds the project
- Publishes to npm
- Creates a GitHub Release

## Step 12: Verify deployment

```bash
# Wait for the release workflow to start
sleep 5
gh run list --workflow=release.yml --limit=1

# Watch the run
gh run watch $(gh run list --workflow=release.yml --limit=1 --json databaseId -q '.[0].databaseId')
```

Once the workflow completes:
- Confirm the GitHub Release was created: `gh release view vNEW_VERSION`
- Confirm npm publish: `npm view @corbat-tech/coco version`

## Final report

Print a summary:

```
## Release vNEW_VERSION complete

- Changelog: updated
- README: updated / no changes needed
- Tests: all passing
- PR: #NUMBER (merged)
- Tag: vNEW_VERSION
- npm: @corbat-tech/coco@NEW_VERSION
- GitHub Release: https://github.com/corbat/corbat-coco/releases/tag/vNEW_VERSION
```
