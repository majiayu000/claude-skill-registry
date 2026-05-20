---
name: release-change-analyzer
description: Compares HEAD with the latest published version to analyze real changes, group by type, and recommend version bumps. Use before publishing a release to understand what actually changed.
---

# Release Change Analyzer

Analyzes unpublished changes by comparing HEAD with the latest published version. Reads actual diffs instead of just copying commit messages.

## When to Use This Skill

- Before publishing a new release
- Deciding between major/minor/patch version bump
- Writing accurate release notes based on real code changes
- Reviewing what changed since last deployment

## What This Skill Does

### Step 1: Identify Published Version

```bash
# npm
npm view <package-name> version 2>/dev/null || echo "not published"

# PyPI
pip index versions <package-name> 2>/dev/null | head -1

# Or use git tags
git tag --sort=-v:refname | head -1
```

### Step 2: Analyze Real Changes

```bash
# Get actual diff (NOT just commit messages)
git diff v{published-version}..HEAD --stat
git diff v{published-version}..HEAD
```

For each commit, MUST:
1. Read the actual diff to understand WHAT CHANGED
2. Describe the REAL change in plain language
3. Explain WHY it matters (if not obvious)

### Step 3: Group and Report

```markdown
## Unpublished Changes (v{published} -> HEAD)

### Features
| Scope | What Changed |
|-------|--------------|
| auth | Added OAuth2 support with Google and GitHub providers |

### Fixes
| Scope | What Changed |
|-------|--------------|
| api | Fixed race condition in concurrent request handling |

### Refactoring
| Scope | What Changed |
|-------|--------------|
| core | Extracted retry logic from 3 services into shared module |

### Breaking Changes
- Removed deprecated `v1/login` endpoint

### Files Changed
42 files changed, 1205 insertions(+), 387 deletions(-)

### Suggested Version Bump
- **Recommendation**: minor
- **Reason**: New features added, no breaking changes in public API
```

## Version Bump Decision

| Condition | Bump |
|-----------|------|
| Breaking changes in public API | major |
| New features, no breaking changes | minor |
| Bug fixes, refactoring, docs only | patch |

## Anti-Patterns

- Copying commit messages verbatim — read the actual diff
- Describing "what" without "why" — explain impact
- Missing breaking changes — always check public API surface
- Guessing at scope — verify from the diff

## Example

**User**: "What changed since last release?"

**Output**: Reads diff between `v1.2.3` and HEAD, identifies 3 features, 2 fixes, 1 refactor, no breaking changes. Recommends `minor` bump to `v1.3.0`.

**Inspired by:** [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode) get-unpublished-changes command
