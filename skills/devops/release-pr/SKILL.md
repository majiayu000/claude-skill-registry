---
name: release-pr
description: Create a release from merged feature changes. Bumps version, creates tag, pushes to main. Use after merge-back is complete and reviewed.
disable-model-invocation: true
allowed-tools:
  - Bash
---

# Release PR

Creates a release from merged feature changes: bumps version, creates tag, and pushes to main.

## What it does

1. **Validates** you're on a `merge/*` branch
2. **Analyzes** commits to auto-detect version bump (major/minor/patch)
3. **Bumps** version in `package.json` (if present)
4. **Merges** the merge branch into `main`
5. **Creates** a git tag (e.g., `v1.7.0`)
6. **Pushes** main and the tag to the remote

## Usage

```
/release-pr [patch|minor|major]
```

If no bump type is specified, it auto-detects based on conventional commits:
- `feat:` commits -> **minor** bump
- `fix:` commits -> **patch** bump
- `BREAKING CHANGE` or `!:` -> **major** bump

## How to execute

**Must be run from the ORIGINAL project directory while on a `merge/*` branch.**

```bash
bash .claude/skills/release-pr/scripts/release-pr.sh [patch|minor|major]
```

## Important

- The version bump auto-detection uses conventional commit prefixes
- The tag is pushed to the remote, which may trigger CI/CD pipelines
- No `Co-Authored-By` headers are added to any commit
- Review the merge branch changes carefully before running this
- Requires `gh` CLI to be installed for PR creation
- You can override the auto-detected bump type by passing `patch`, `minor`, or `major`
