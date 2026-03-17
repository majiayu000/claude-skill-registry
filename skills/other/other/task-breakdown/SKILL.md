---
name: task-breakdown
description: Break down high-level plans into specific tasks with file paths,
  line numbers, and verification steps. Creates execution-ready implementation
  plans.
---

# Task Breakdown Skill

## Purpose
Transform architecture plans into atomic, executable tasks with clear verification criteria.

## When to Use
- After architecture plan is approved
- Converting design to implementation steps
- Creating detailed work breakdown
- Estimating implementation effort

## Task Template
Use [templates/task-template.md](templates/task-template.md) for consistent task format.

## Task Criteria

### Atomic Tasks Must Be:
1. **Single-concern**: One logical change per task
2. **Verifiable**: Clear success criteria
3. **Bounded**: Defined start and end
4. **Estimated**: Size/complexity indicated
5. **Ordered**: Dependencies explicit

### Task Size Guidelines

| Size | Description | Typical Scope |
|------|-------------|---------------|
| **XS** | Single line change | Typo fix, constant update, config tweak |
| **S** | Single function | Add/modify one function, simple test |
| **M** | Single file | Multiple functions in one file |
| **L** | Multiple files, one concern | Feature spanning 2-4 files |
| **XL** | Too large - split further | Break into smaller tasks |

**Rule**: If a task is XL, it must be broken down further.

## File Operation Types

### CREATE
Create new file from scratch.
```markdown
| Action | File | Details |
|--------|------|---------|
| CREATE | `src/services/auth.ts` | New auth service, follow UserService pattern |
```

Include:
- Full file path
- Template or pattern to follow
- Key exports/functions to include

### MODIFY
Change existing file.
```markdown
| Action | File | Details |
|--------|------|---------|
| MODIFY | `src/routes/index.ts` | Lines 45-60, add auth routes |
```

Include:
- File path
- Line range
- Description of change
- Before/after state

### DELETE
Remove file or code.
```markdown
| Action | File | Details |
|--------|------|---------|
| DELETE | `src/old/legacy-auth.ts` | Remove deprecated auth system |
```

Include:
- File path
- Reason for deletion
- Confirmation of no dependencies

### MOVE
Relocate file.
```markdown
| Action | File | Details |
|--------|------|---------|
| MOVE | `src/auth.ts` → `src/services/auth.ts` | Reorganize to services directory |
```

Include:
- Source and destination paths
- Import updates needed
- Git history preservation note

## Verification Approaches

| Type | Command | Use Case |
|------|---------|----------|
| Type Check | `npm run typecheck` | TypeScript changes |
| Lint | `npm run lint` | Style/format compliance |
| Unit Test | `npm test -- [pattern]` | Logic verification |
| Integration Test | `npm run test:integration` | Component interaction |
| E2E Test | `npm run e2e` | Full workflow |
| Build | `npm run build` | Compilation verification |
| Manual | [Specific instructions] | UI/UX, visual changes |

### Framework-Specific Commands

**Node.js/TypeScript:**
```bash
npm run typecheck
npm run lint
npm test -- --testPathPattern=auth
```

**Python:**
```bash
python -m pytest tests/test_auth.py
python -m mypy src/auth.py
python -m flake8 src/auth.py
```

**Go:**
```bash
go test ./auth/...
go vet ./auth/...
golint ./auth/...
```

## Dependency Types

### Hard Dependency
Must complete before next task starts.
```markdown
**Dependencies:** Task 1.1 (hard) - Needs auth service to exist
```

### Soft Dependency
Should complete first but can proceed if needed.
```markdown
**Dependencies:** Task 1.2 (soft) - Ideally after tests written
```

### None
Independent task, can run in parallel.
```markdown
**Dependencies:** None
```

## Commit Message Conventions

Follow conventional commits format:
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code change without feature/fix
- `docs`: Documentation only
- `test`: Adding tests
- `chore`: Maintenance tasks

### Examples
```
feat(auth): implement JWT token service

- Add token generation with configurable expiry
- Add token validation with signature verification
- Integrate with user service for claims

Closes #123
```

## Priority Levels

| Priority | Meaning | When to Use |
|----------|---------|-------------|
| **P1** | Critical | Blocking other work, core functionality |
| **P2** | High | Important, should be done soon |
| **P3** | Medium | Standard priority |
| **P4** | Low | Nice to have, can defer |

## Phase Organization

Group tasks into logical phases:
1. **Foundation**: Core infrastructure, shared utilities
2. **Core Features**: Main functionality
3. **Integration**: Connecting components
4. **Testing**: Test implementation
5. **Documentation**: Docs and cleanup

## Output Quality Checklist

Before finalizing implementation plan:
- [ ] All tasks are appropriately sized (no XL tasks)
- [ ] File paths are complete and accurate
- [ ] Line numbers included for modifications
- [ ] Current and expected state shown for changes
- [ ] Verification commands are runnable
- [ ] Commit messages follow project conventions
- [ ] Dependencies clearly marked
- [ ] Phases organized logically
- [ ] All architecture components covered
- [ ] No orphan tasks (everything connects)

## Output Location
Save implementation plans to: `docs/plans/implementation-{session}.md`

## Integration with Workflow

1. **Architecture document** provides component design
2. **Task breakdown** creates executable tasks (this skill)
3. **Implementation** follows tasks exactly
4. **Validation** verifies each task's success criteria
