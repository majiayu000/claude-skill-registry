---
name: hotfix
description: Quick patch release for urgent fixes. Use /hotfix or /hotfix "description of the fix".
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Hotfix Release

Streamlined release workflow for urgent patch fixes. Skips README updates and uses abbreviated changelog entries.

## Input

- `$ARGUMENTS` = optional description of what was fixed (used in changelog and commit)

## Pre-flight

```bash
git branch --show-current
git status --porcelain
gh auth status
```

- Must NOT be on main/master
- Working tree must be clean (all fix commits already made)
- If working tree is dirty, STOP and ask user to commit pending changes first

## Step 1: Version bump (always patch)

```bash
# Current version
node -e "console.log(require('./package.json').version)"
```

Calculate new patch version (e.g., 1.7.0 → 1.7.1).

```bash
npm version patch --no-git-tag-version
```

## Step 2: Quick changelog update

Read CHANGELOG.md. Add a minimal entry under a new version section:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Fixed
- **Description of the fix** (from $ARGUMENTS or from recent commit messages)
```

## Step 3: Run checks

```bash
pnpm check
```

If checks fail, fix and retry (max 3 attempts). This is a hotfix - speed matters but quality is non-negotiable.

## Step 4: Commit and push

```bash
git add CHANGELOG.md package.json pnpm-lock.yaml
git commit -m "chore(release): hotfix vX.Y.Z"
git push origin $(git branch --show-current)
```

Do NOT add `Co-Authored-By`.

## Step 5: Create PR

```bash
gh pr create --base main --title "hotfix: vX.Y.Z" --body "## Hotfix vX.Y.Z

### Fixed
- DESCRIPTION

### Checklist
- [x] Fix verified locally
- [x] Tests passing
- [ ] CI passing
"
```

## Step 6: Wait for CI and merge

```bash
gh pr checks --watch
```

If checks pass:
```bash
gh pr merge --squash --delete-branch
```

If checks fail, fix → commit → push → retry (max 3 cycles).

## Step 7: Tag and push

```bash
git checkout main
git pull origin main
git tag vX.Y.Z
git push origin vX.Y.Z
```

## Final report

```
## Hotfix vX.Y.Z released

- Fix: DESCRIPTION
- PR: #NUMBER (merged)
- Tag: vX.Y.Z
- npm publish: triggered (release.yml)
```
