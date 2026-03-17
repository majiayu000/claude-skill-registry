---
name: develop
description: General principles for exploring, developing, editing, and refactoring code. Use for codebase analysis, implementation tasks, and code quality improvements.
---

# Develop Skill

## Core Principles
- **Clean Code**: Follow readable, maintainable patterns.
- **Fail Early**: Never catch unexpected exceptions silently; let them bubble up.
- **Simplicity**: Prefer the simplest working solution.

## Planning
For non-trivial changes:
- Present a plan with **at least 3 clarifying questions** (and proposed answers).
- **Wait for explicit approval** before implementation.
- For complex strategy, use the `plan` skill.

## Implementation & Git
### Git Safety
- **Permission First**: Always ask before initializing repos or switching branches.
- **Atomic Commits**: Group related changes logically.

### Code Quality
- **Focus on WHY**: Document intent, not mechanics.
- **Edge Cases**: Consider and test error scenarios.
- **Existing Style**: Match existing patterns and formatting.

## Language-Specific References
When working with specific languages, consult the following references:
- **Python**: Refer to `references/python.md`.

## File Operations
- **Prefer `edit_file`**: Use for targeted changes; avoid rewriting full files.
- **Verification**: Always verify changes after editing.
- **Tools**: Use `fd` and `rg` for exploration; standard shell tools for navigation.
