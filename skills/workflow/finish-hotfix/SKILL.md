---
name: finish-hotfix
allowed-tools: Bash(git:*), Read, Write
description: Complete and merge hotfix branch
model: haiku
argument-hint: [version]
user-invocable: true
---

## Phase 1: Identify Version

**Goal**: Determine hotfix version from current branch or argument.

**Actions**:
1. If `$ARGUMENTS` provided, use it as version
2. Otherwise, extract from current branch: `git branch --show-current` (strip `hotfix/` prefix)

## Phase 2: Pre-finish Checks

**Goal**: Run tests before finishing.

**Actions**:
1. Identify test commands (check package.json, Makefile, etc.)
2. Run tests if available; exit if tests fail

## Phase 3: Update Changelog

**Goal**: Generate changelog from commits.

**Actions**:
1. Get previous tag: `git tag --sort=-v:refname | head -1`
2. Collect commits per `${CLAUDE_PLUGIN_ROOT}/references/changelog-generation.md`
3. Update CHANGELOG.md per `${CLAUDE_PLUGIN_ROOT}/examples/changelog.md`
4. Commit: `chore: update changelog for v$VERSION` with `Co-Authored-By` footer

## Phase 4: Finish Hotfix

**Goal**: Complete hotfix using git-flow-next CLI.

**Actions**:
1. Run `git flow hotfix finish $VERSION -m "Release v$VERSION"`
2. Push all: `git push origin main develop --tags`
