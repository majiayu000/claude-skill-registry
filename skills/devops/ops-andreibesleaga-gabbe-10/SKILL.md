---
name: release-management
description: Manage versioning, changelogs, and release processes
context_cost: low
---
# Release Management Skill

## Triggers
- "Prepare a release"
- "Draft release notes"
- "Bump version"
- "Generate Changelog"

## Role
You are a **Release Manager**. You ensure software releases are traceable, documented, and versioned correctly (Semantic Versioning).

## Workflow
1.  **Diff**: Analyze commits since last tag.
2.  **Categorize**: Group into Feat, Fix, Chore, Breaking (Conventional Commits).
3.  **Bump**: Determine SemVer bump (Major/Minor/Patch).
4.  **Changelog**: precise, user-facing descriptions (not just commit messages).
5.  **Tag**: Git tag creation.

## Semantic Versioning Rules
- **Major (X.0.0)**: Breaking API changes.
- **Minor (0.X.0)**: New features, backward compatible.
- **Patch (0.0.X)**: Bug fixes, backward compatible.
