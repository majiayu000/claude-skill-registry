---
name: release
description: Cut a release — version bump, changelog, git tag, and push (Marcus Chen's workflow)
disable-model-invocation: true
---

Create a release: $ARGUMENTS

If no version specified, determine the next version using semantic versioning.

## Step 1 — Pre-release Validation
Run the test and type-check commands (see project config).
Both MUST pass. Never release with failing tests or type errors.

## Step 2 — Determine Version
Follow semantic versioning (MAJOR.MINOR.PATCH):
- **PATCH** (1.0.0 → 1.0.1): Bug fixes, no new features, no breaking changes
- **MINOR** (1.0.0 → 1.1.0): New features, backwards compatible
- **MAJOR** (1.0.0 → 2.0.0): Breaking changes to the API

Check current version in the config file and recent git tags.

## Step 3 — Update Version
Update version in these locations:
1. The config file — version field
2. The env example file — version variable

## Step 4 — Generate Changelog
Run `/changelog` or manually create entry in the changelog file.

## Step 5 — Commit Release
```bash
git add <config file> <env example file> <changelog file>
git commit -m "chore: release v<version>"
```

## Step 6 — Tag
```bash
git tag -a v<version> -m "Release v<version>"
```

## Step 7 — Push
```bash
git push origin main
git push origin v<version>
```

## Step 8 — GitHub Release (optional)
```bash
gh release create v<version> --title "v<version>" --notes-file <changelog file>
```

## Step 9 — Verify
```bash
git log --oneline -3
git tag --sort=-v:refname | head -3
```
Confirm the tag and commit exist.

## Rules
- NEVER release without passing tests and type checks
- NEVER skip the changelog
- NEVER use force-push on release tags
- Version in config file MUST match the git tag