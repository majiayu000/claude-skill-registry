---
name: localsetup-automatic-versioning
description: Use and maintain automatic versioning from conventional commits; VERSION as source of truth; sync to READMEs and docs. Use when working on version bumps, release workflow, or when the user asks about versioning or conventional commits.
metadata:
  version: "1.1"
---

# Automatic versioning (framework)

**Purpose:** The framework uses semantic versioning with VERSION as source of truth. Use this skill when implementing, explaining, or changing versioning behavior so it stays consistent and framework-appropriate.

## Source of truth

- **VERSION** (repo root): single line, semantic version `MAJOR.MINOR.PATCH` (e.g. `2.0.0`). This is the only canonical version value.
- **Displayed version** must stay in sync: README and framework README show `**Version:** X.Y.Z`; framework docs use YAML front matter `version: X.Y` (major.minor). The repository maintainers keep these in sync when they run the publish workflow.

## Conventional Commits → bump type

- **MAJOR:** `BREAKING CHANGE:` in body, or type followed by `!` (e.g. `feat!: new API`).
- **MINOR:** `feat:` (new feature).
- **PATCH:** `fix:`, `docs:`, `chore:`, `style:`, `refactor:`, `perf:`, `test:`, `ci:`, `build:`; any other message defaults to PATCH.
- **No bump:** Merge commits (message starts with `Merge `).

## In this repo (public framework)

Version bump and doc sync are performed by the repository maintainers. Contributors do not need to run any scripts. If you are working in a repo that has the maintainer publish workflow (e.g. the framework maintainer repo), run the publish workflow from that context as documented there.

## Reference

- Versioning doc: docs/VERSIONING.md (slim) or _localsetup/docs/VERSIONING.md in a deployed copy.
