---
name: implementing-code
description: >
  Implements code changes and creates commits.
  Triggered when: implementation tasks, code changes, feature additions, bug fixes.
allowed-tools: Read, Write, Edit, Bash(git:*), Glob, Grep
---

# Task Input

- **Purpose**: What to achieve
- **Deliverable**: Completion criteria

# Implementation Flow

1. Investigate related code (Glob, Grep, Read)
2. Implement following existing patterns
3. Commit changes

# Commit Convention

Check CLAUDE.md for project-specific rules.

Default format (Conventional Commits):
```
<type>: <description>
```

| type | usage |
|------|-------|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation |
| refactor | Refactoring |
| test | Tests |
| chore | Other |

# Commit Execution

```bash
git add <files>
git commit -m "<type>: <description>"
```

# Parallel Execution

When running in parallel with other tasks:
- Do NOT edit the same files
- Report conflicts to manager

# Completion Report

- Changed files
- Implementation summary
- Commit hash
