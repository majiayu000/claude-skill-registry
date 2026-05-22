---
name: git-flow-release
description: Create a release for this repository by tagging main with calendar versioning (optionally using git-flow if configured); use when the user asks to create a release or bump version.
---

# Release

## Communication

- Communicate with the developer in Japanese.
- Write commit messages and tag messages in English.

## Prerequisites

Before starting the release process, verify:

1. All changes are committed (`git status` should show a clean working tree).
2. You are on the target branch (`main` unless the user specifies otherwise).

This repository does not have mandatory lint/test commands; do not run Node/bun/turbo checks here.

## Version Format

Use calendar-based versioning with `v` prefix for git tags:

- **Git tag**: `vYYYY.MM.DD.N` (e.g., `v2026.02.04.1`)

Components:

- **YYYY**: 4-digit year (e.g., 2026)
- **MM**: 2-digit month (e.g., 02)
- **DD**: 2-digit day (e.g., 04)
- **N**: Daily release number starting from 1, incrementing for each subsequent release on the same day

## Version Determination

1. Determine today's date in `YYYY.MM.DD`:

   ```bash
   today=$(date +%Y.%m.%d)
   ```

2. Check existing tags for today:

   ```bash
   git tag --list "v${today}.*"
   ```

3. Choose the next `N`:
   - If no tags exist for today, use `N=1` → `vYYYY.MM.DD.1`
   - If tags exist for today (e.g., `vYYYY.MM.DD.1`), increment `N` (e.g., `vYYYY.MM.DD.2`)

## Release Workflow (tag-based)

Execute the following steps in order:

1. **Determine version**
   - Decide `YYYY.MM.DD.N` and prepare short release notes (bullet list)

2. **Commit changes (if needed)**

   ```bash
   git add -A
   git commit -m "chore: prepare release vYYYY.MM.DD.N"
   ```

3. **Create annotated tag**

   ```bash
   git tag -a vYYYY.MM.DD.N -m "Release vYYYY.MM.DD.N"
   ```

4. **Push main with tags**

   ```bash
   git push origin main --tags
   ```

5. **(Optional) Create a GitHub Release**

   If `gh` is available and the user requests it:

   ```bash
   gh release create vYYYY.MM.DD.N --generate-notes
   ```

## Git-flow (optional)

Only use this section if git-flow is configured for the repository (a `develop` branch exists and `git flow init` has been run).

1. **Start release**

   ```bash
   git flow release start YYYY.MM.DD.N
   ```

2. **Finish release (macOS/BSD safe path)**

   Always finish without tagging and add the tag manually (avoids getopt errors with `-m`).

   ```bash
   git flow release finish -n YYYY.MM.DD.N
   git switch main
   git tag -a vYYYY.MM.DD.N -m "Release vYYYY.MM.DD.N"
   ```

3. **Push branches and tags**

   ```bash
   git push origin develop
   git push origin main --tags
   ```

## Post-release Report

After completing all steps, report:

- The released version number (e.g., `2026.02.04.1`)
- The tag name created (e.g., `v2026.02.04.1`)
- Confirmation that the tag was pushed
- (If created) Confirmation that the GitHub Release was published

## Error Handling

- If tagging fails because there are no commits yet, create the initial commit first.
- If `git flow` is not installed, inform the user and suggest installing it.
- If merge conflicts occur during `git flow release finish`, stop and report the conflict details.
- If push fails, check remote status and report the issue.
