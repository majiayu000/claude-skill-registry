---
name: release-notes
description: Draft release notes and changelog entries from git history or merged PRs between two refs (tags/SHAs/branches), including breaking changes, migrations, and upgrade steps. Use when the user asks for release notes, changelog updates, or a GitHub Release draft.
---

# Release notes

## Goal
Produce accurate, scannable release notes (Markdown) for a specific release range.

## Inputs to ask for (if missing)
- Release version + date (or "unreleased").
- Range to summarize: `from_ref..to_ref` (tags/SHAs/branches). If unknown, ask: "last release tag?" and "target branch/tag?"
- Target audience: end users, developers, internal ops, or all.
- What to include/exclude: internal refactors, dependency bumps, infra-only changes.

## Workflow (checklist)
1) Determine the release range
   - Prefer tags: pick the previous tag and the new tag/HEAD.
   - If no tags: use the last release branch point or a date-based window.
   - Commands to gather candidates:
     - `git tag --sort=-creatordate | Select-Object -First 20`
     - `git log --first-parent --oneline <from_ref>..<to_ref>`
     - If GitHub CLI is available: list merged PRs for the range and use titles for grouping.
2) Collect and categorize changes
   - Start from merge commits (first-parent) to avoid noise.
   - Categorize into: Highlights, Breaking changes, Features, Fixes, Performance, Security, Deprecations, Docs, Dependencies, Infra/ops.
   - Flag anything requiring action: config changes, env vars, DB migrations, API contract changes.
3) Identify breaking changes and upgrade steps
   - Look for: renamed/removed endpoints, changed request/response fields, changed config keys, Java/Kotlin/Node version bumps, DB schema changes.
   - Add explicit "Upgrade" and "Rollback" notes when impact is non-trivial.
4) Write release notes using the template
   - Use short bullets, active voice, and user-facing wording.
   - Prefer "what changed" + "why it matters" over implementation details.
   - Include PR/issue references only if they are stable in your repo hosting.
   - Use `references/release-notes-template.md` to keep structure consistent.
5) Sanity check for omissions and accuracy
   - Diff the range: `git diff --stat <from_ref>..<to_ref>`
   - Scan for config/migrations: `rg -n \"ENV|config|migration|Flyway|Liquibase\" -S`
   - Ensure breaking changes are called out and have upgrade steps.

## Deliverable
Provide:
- Release notes Markdown (ready to paste into a GitHub Release / changelog).
- A short "Risk/notes" section listing any required migrations, config changes, or rollback concerns.

