---
name: finish-release
allowed-tools: Bash(git:*), Bash(gh:*), Read, Write
description: Complete and merge release branch
model: haiku
argument-hint: [version]
user-invocable: true
---

## Phase 1: Identify Version

**Goal**: Determine release version from current branch or argument.

**Actions**:
1. If `$ARGUMENTS` provided, use it as version
2. Otherwise, extract from current branch: `git branch --show-current` (strip `release/` prefix)

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

## Phase 4: Finish Release

**Goal**: Complete release using git-flow-next CLI.

**Actions**:
1. Run `git flow release finish $VERSION -m "Release v$VERSION"`
2. Push all: `git push origin main develop --tags`

## Phase 5: GitHub Release

**Goal**: Create GitHub release.

**Actions**:
1. Extract changelog for this version from CHANGELOG.md
2. Run `gh release create v$VERSION --title "v$VERSION" --notes "<changelog>"`
