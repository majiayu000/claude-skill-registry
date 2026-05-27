---
name: breaking-changes
description: Detect breaking changes in Claude Code updates by comparing current API surface against changelog. Maps impacts to specific plugin files.
argument-hint: "[version]"
user-invocable: true
---

# Breaking Changes Detection Skill

## Overview

Compares Claude Code API changes against our plugin ecosystem to detect compatibility issues.

## API Surface File

The `api-surface.md` reference contains our current known API:
- Hook types and their matchers
- Agent frontmatter fields
- Plugin manifest schema
- Skill SKILL.md format
- Script CLI flags used

## Detection Workflow

1. **Load** current api-surface.md
2. **Fetch** latest Claude Code API docs
3. **Diff** for added/changed/removed APIs
4. **Grep** our plugins for each changed API
5. **Report** with file:line impact mapping

## Impact Assessment

| Change Type | Severity | Example |
|-------------|----------|---------|
| Removed API | BREAKING | Hook type deleted |
| Changed schema | BREAKING | Frontmatter field renamed |
| New required field | BREAKING | Mandatory new param |
| Deprecated API | DEPRECATED | Old hook still works |
| New optional API | NEW | New hook type added |

## References

- [API Surface](references/api-surface.md)
- [Migration Guide Template](references/templates/migration-guide.md)
