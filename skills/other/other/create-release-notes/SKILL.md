---
name: create-release-notes
description: Generate user-facing release notes when the user asks to write release notes, document a release, summarize changes for users, or prepare a changelog between versions
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash, Write
argument-hint: "[version range, e.g., v1.1.0...v1.2.0, or target version]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: release, changelog, docs
---

# Create Release Notes

## Overview

Generate clear, user-facing release notes from git history and PR descriptions between two versions. Translate technical changes into language that users and stakeholders understand, grouped by impact category with breaking changes prominently highlighted.

## Workflow

1. **Read project context** — Check `.chalk/docs/` for:
   - Previous release notes (to match tone, format, and conventions)
   - Product docs (to understand user-facing terminology)
   - Architecture docs (to map technical changes to user-facing features)

2. **Determine the version range** — From `$ARGUMENTS`:
   - If two versions are provided (e.g., `v1.1.0...v1.2.0`), use that range
   - If only a target version is provided, find the previous tag: `git tag --sort=-v:refname | head -5`
   - If no versions given, use the latest tag to HEAD: `git log <latest-tag>..HEAD`
   - Run `git log --oneline --no-merges <from>..<to>` to list all commits

3. **Gather change details** — For each commit in the range:
   - Read the commit message (subject and body)
   - If a PR number is referenced, read the PR description for richer context
   - Identify the type of change: feature, improvement, bugfix, breaking change, deprecation, internal/chore
   - Skip purely internal changes (CI config, dev tooling) unless they affect the user

4. **Classify changes** — Group each change into one of these categories:
   - **Breaking Changes**: API contract changes, removed features, changed defaults, required migration steps
   - **New Features**: Entirely new capabilities that did not exist before
   - **Improvements**: Enhancements to existing features (performance, UX, expanded functionality)
   - **Bug Fixes**: Corrections to incorrect behavior
   - **Deprecations**: Features or APIs that still work but will be removed in a future version
   - **Security**: Vulnerability patches and security improvements

5. **Translate to user-facing language** — For each change:
   - Replace technical jargon with user-facing terms ("refactored the query builder" becomes "improved search performance")
   - Focus on the benefit to the user, not the implementation detail
   - Keep each entry to 1-2 sentences
   - Use active voice and present tense ("Adds dark mode support" not "Dark mode support has been added")
   - If the change is not user-facing, omit it from the notes (or group under "Internal" if the audience includes developers)

6. **Write breaking changes section** — For each breaking change:
   - Clearly state what changed and why
   - Provide before/after examples
   - Include step-by-step migration instructions
   - Note the minimum version required for the migration
   - If an automated migration tool exists, reference it

7. **Determine the next file number** — List files in `.chalk/docs/product/` matching `*_release_notes*`. Find the highest number and increment by 1.

8. **Write the release notes** — Save to `.chalk/docs/product/<n>_release_notes_<version>.md`.

9. **Confirm** — Present a summary: version, number of changes by category, any breaking changes that need attention.

## Filename Convention

```
<number>_release_notes_<version>.md
```

Examples:
- `3_release_notes_v1_2_0.md`
- `8_release_notes_v2_0_0.md`

## Release Notes Format

```markdown
# Release Notes: <version>

**Release date**: <YYYY-MM-DD>
**Previous version**: <version>

## Highlights

<1-3 sentences summarizing the most important changes in this release. What should users be excited about or aware of?>

## Breaking Changes

> **Action required**: The following changes may require updates to your code or configuration.

### <Change title>

<What changed and why.>

**Before (<previous version>)**:
```<language>
<old code or configuration>
```

**After (<this version>)**:
```<language>
<new code or configuration>
```

**Migration steps**:
1. <Step-by-step migration instruction>
2. <Next step>

## New Features

- **<Feature name>** — <1-2 sentence description of what it does and why it matters to the user>
- **<Feature name>** — <description>

## Improvements

- **<Improvement area>** — <What got better and how it benefits the user>
- **<Improvement area>** — <description>

## Bug Fixes

- Fixed an issue where <user-visible symptom>
- Fixed <specific scenario> that caused <user-visible problem>

## Deprecations

- **<Deprecated feature>** — <What is deprecated, what to use instead, when it will be removed>

## Security

- Patched <brief, non-exploitable description> (severity: <level>)

---

**Full changelog**: `git log <from>..<to>`
```

## Translation Guidelines

### Technical to User-Facing

| Technical Description | User-Facing Description |
|----------------------|------------------------|
| Refactored database query to use index scan | Improved search performance by up to 3x |
| Added Redis caching layer for user sessions | Faster page loads for returning users |
| Migrated from REST to GraphQL for the dashboard API | Dashboard now loads only the data you need, reducing load times |
| Fixed N+1 query in order listing endpoint | Order history page now loads significantly faster |
| Updated React from 17 to 18 | Improved UI responsiveness and reduced memory usage |
| Added rate limiting middleware | API now handles traffic spikes more reliably |
| Fixed race condition in checkout flow | Resolved rare issue where duplicate orders could be created |

### Tone and Style

- **Do**: Use plain language, focus on benefits, be specific about improvements
- **Do**: "Search results now load 50% faster" (specific, measurable)
- **Do not**: "Optimized the Elasticsearch query aggregation pipeline" (technical jargon)
- **Do not**: "Various bug fixes and improvements" (vague, unhelpful)
- **Do**: Use consistent verb tense (present tense: "Adds...", "Fixes...", "Improves...")
- **Do not**: Mix tenses ("Added...", "Fixes...", "Will improve...")

### Audience Considerations

| Audience | Include | Exclude |
|----------|---------|---------|
| End users | Features, bug fixes, UX improvements | Internal refactors, CI changes, dev tooling |
| Developers (API consumers) | Breaking changes, API additions, deprecations | UI changes, internal architecture |
| Internal team | Everything | Nothing, but still translate jargon |

## Anti-patterns

- **Internal jargon** — "Refactored the middleware pipeline" means nothing to users. Translate every entry into language your audience understands. If you cannot explain the user benefit, the change might not belong in release notes.
- **Just listing commits** — Copy-pasting `git log` output is not release notes. Commits are written for developers reviewing code, not for users understanding what changed. Synthesize, group, and translate.
- **Not highlighting breaking changes** — Burying a breaking change in a list of bug fixes causes users to miss it, leading to broken integrations and angry support tickets. Breaking changes get their own section, at the top, with migration instructions.
- **Missing migration instructions** — Saying "the API changed" without showing before/after examples and step-by-step migration is not actionable. Users need to know exactly what to change in their code.
- **Vague entries** — "Various improvements" and "bug fixes" tell the user nothing. If it is worth mentioning, be specific. If it is not worth being specific about, omit it.
- **Including internal changes** — CI pipeline updates, dev dependency bumps, and code formatting changes are not user-facing. Including them adds noise and makes real changes harder to find.
- **No highlights section** — Users scan release notes quickly. Without a highlights section, the most important changes get buried. Lead with what matters most.
- **Inconsistent categorization** — A performance improvement listed under "Bug Fixes" or a new feature listed under "Improvements" confuses users. Use the categories consistently and correctly.
