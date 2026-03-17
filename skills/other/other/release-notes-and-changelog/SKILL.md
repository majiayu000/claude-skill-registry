---
name: release-notes-and-changelog
description: Generate release notes from git history
version: 1.1.0
tags: [release, documentation, changelog]
owner: documentation
status: active
---

# Release Notes & Changelog Skill

## Overview

Generate user-facing release notes from commit history.

## Usage

```
/release-notes-and-changelog
```

## Identity
**Role**: Product Owner / Documentarian
**Objective**: Transform raw git commits into user-facing release notes.

## Workflow

### 1. Data Collection
**Command**: `git log <last-tag>..HEAD --pretty=format:"%s"`
**Filter**:
- Include: `feat`, `fix`, `perf`.
- Exclude: `chore`, `ci`, `test`, `refactor` (unless breaking).

### 2. Categorization
Group by Type:
- 🚀 **New Features** (`feat`)
- 🐛 **Bug Fixes** (`fix`)
- ⚡ **Performance** (`perf`)
- ⚠️ **Breaking Changes** (commits with `BREAKING CHANGE:` footer).

### 3. Formatting
**Output File**: `CHANGELOG.md` or `RELEASE_NOTES.md`.
**Format**:
```markdown
## [Version] - Date

### 🚀 Features
- **scope**: description (hash)

### 🐛 Fixes
- **scope**: description (hash)
```

## Constraints
- **Cleanliness**: Remove PR numbers or tech jargon if targeted at end-users.
- **Accuracy**: Do not hallucinate features not continuously in the log.

## Tools
- Can use `conventional-changelog` CLI if available.
- Otherwise, parse manually with LLM.

## Outputs

- Release notes and changelog entries grouped by change type.

## Related Skills

- `/codebase-visualizer` - Diagrammatic summaries for releases
