---
name: release-notes
description: Writing clear, comprehensive release notes for software releases
category: Communication Writing
---

# Skill: release-notes

## What I do

I provide expertise in writing clear, comprehensive release notes for software releases. I focus on audience-aware content, categorising changes, and providing migration guides for breaking changes.

## When to use me

- Preparing release notes for a new software version
- Communicating updates, bug fixes, and new features to users
- Documenting breaking changes and providing migration steps
- Updating a changelog or release page on a platform like GitHub

## Core principles

1.  **Audience Awareness** — Distinguish between notes for end-users (what's new) and developers (what changed).
2.  **Categorisation** — Group changes into logical categories (e.g., Features, Fixes, Breaking Changes, Deprecations).
3.  **Conciseness** — Keep descriptions brief and focused on the impact of the change.
4.  **Actionable Migration** — Provide clear, step-by-step instructions for any breaking changes.
5.  **Linking** — Link to relevant documentation, issues, or pull requests for more detail.

## Patterns & examples

### Release Note Template
- **Version & Date**: Clear version number and release date.
- **Summary**: High-level overview of the release.
- **🚀 New Features**: List of new functionality with brief descriptions.
- **🐛 Bug Fixes**: List of resolved issues and their impact.
- **⚠️ Breaking Changes**: Clearly highlighted changes that require user action.
- **Migration Guide**: Specific steps to update existing code or configurations.

### Breaking Change Pattern
"**⚠️ BREAKING CHANGE**: The `getUser` function now returns a Promise instead of a raw object."
- **Why**: To support asynchronous data fetching.
- **How to Fix**: Use `await` or `.then()` when calling `getUser`:
```javascript
const user = await getUser(id);
```

## Anti-patterns to avoid

-   ❌ **Technical Jargon Only** — Writing notes that only the developers who built the feature can understand.
-   ❌ **Missing Breaking Changes** — Failing to highlight changes that will break existing integrations.
-   ❌ **Vague Descriptions** — Using phrases like "various bug fixes" without any detail.
-   ❌ **Inconsistent Versioning** — Changing versioning schemes without explanation.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Communication-Writing/Release Notes.md`

## Related skills

-   `release-management` — For managing the overall release process.
-   `breaking-changes` — For specific guidance on managing backwards compatibility.
-   `documentation-writing` — For general technical clarity.
-   `writing-style` — To maintain a consistent professional voice.
