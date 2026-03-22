---
name: changesets
description: >-
  Assists with managing versioning and changelogs in JavaScript/TypeScript monorepos using
  Changesets. Use when automating semantic versioning, generating changelogs from PRs,
  coordinating multi-package releases, or publishing to npm. Trigger words: changesets,
  versioning, changelog, npm publish, monorepo release, semver.
license: Apache-2.0
compatibility: "Requires Node.js 16+"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: development
  tags: ["changesets", "versioning", "changelog", "monorepo", "npm"]
---

# Changesets

## Overview

Changesets is a versioning and changelog management tool for JavaScript/TypeScript monorepos. Developers add changeset files describing their changes, then CI consumes them to bump package versions, generate changelogs, and publish to npm with coordinated releases across interdependent packages.

## Instructions

- When adding a change, run `npx changeset`, select affected packages, choose the semver bump type (patch, minor, major), write a user-facing description, and commit the generated `.changeset/xxx.md` file with the PR.
- When releasing versions, run `npx changeset version` to consume pending changesets, bump `package.json` versions, update `CHANGELOG.md` per package, and handle dependency bumps automatically.
- When publishing, run `npx changeset publish` to publish changed packages to npm, create git tags, and skip unchanged packages.
- When automating with CI, use `changesets/action` in GitHub Actions to automatically create a "Version Packages" PR and publish on merge.
- When coordinating packages, use `linked` for packages that must share the same version (CLI + SDK) and `fixed` for monorepo-wide versioning.
- When testing pre-releases, use snapshot releases (`--snapshot preview`) for CI testing or pre-release mode (`changeset pre enter next`) for `-next.0` versions.

## Examples

### Example 1: Set up automated releases for a monorepo

**User request:** "Configure Changesets for automated versioning and publishing in my Turborepo monorepo"

**Actions:**
1. Install `@changesets/cli` and run `npx changeset init` to create `.changeset/config.json`
2. Configure `@changesets/changelog-github` for PR links and author attribution
3. Add `changesets/action` to GitHub Actions for automatic "Version Packages" PR creation
4. Set up CI check that requires a changeset file on PRs affecting published packages

**Output:** A monorepo with automated versioning, changelog generation, and npm publishing triggered by merging the version PR.

### Example 2: Coordinate a breaking change across multiple packages

**User request:** "Release a major version bump for our core package and patch bumps for all dependents"

**Actions:**
1. Run `npx changeset` and select the core package with `major` bump
2. Write a description of the breaking change for the changelog
3. Run `npx changeset version` which bumps the core package and patches all dependents
4. Review the generated changelogs and version bumps, then merge

**Output:** A coordinated release with a major bump on the core package and automatic patch bumps on all dependent packages.

## Guidelines

- Require changesets on every PR that affects published packages and enforce with a CI check.
- Write changeset descriptions for users, not developers: "Fixed button hover state" not "Refactored CSS modules."
- Use `linked` for packages that must stay in sync, such as CLI and SDK pairs.
- Use snapshot releases for testing PRs since they publish `0.0.0-timestamp` versions for CI testing.
- Use `@changesets/changelog-github` for open-source projects to include PR links and author attribution.
- Keep `.changeset/config.json` in the repo root as project configuration.
