---
name: skill-git-workflow
description: Create scoped git commits for task operations. Invoke after task status changes or artifact creation.
allowed-tools: Bash(git:*)
# Context loaded on-demand via @-references (see Context Loading section)
---

# Git Workflow Skill

Create properly scoped git commits for task operations.

## Context Loading

Load context on-demand when needed:
- `@.claude/context/core/standards/git-safety.md` - Git safety rules and best practices
- `@.claude/context/index.md` - Full context discovery index

## Trigger Conditions

This skill activates when:
- Task status changes (research, plan, implement complete)
- Artifacts are created
- Task lifecycle operations occur

## Commit Message Formats

### Task Operations

| Operation | Format | CI Triggered |
|-----------|--------|--------------|
| Create task | `task {N}: create {title}` | No |
| Complete research | `task {N}: complete research` | No |
| Create plan | `task {N}: create implementation plan` | No |
| Complete phase | `task {N} phase {P}: {phase_name}` | No |
| Complete task | `task {N}: complete implementation` | No |
| Complete task (with CI) | `task {N}: complete implementation [ci]` | Yes |
| Revise plan | `task {N}: revise plan (v{V})` | No |

### System Operations

| Operation | Format |
|-----------|--------|
| Archive tasks | `todo: archive {N} completed tasks` |
| Error fixes | `errors: create fix plan for {N} errors` |
| Code review | `review: {scope} code review` |
| State sync | `sync: reconcile TODO.md and state.json` |

## Execution Flow

```
1. Receive commit request:
   - operation_type
   - task_number (if applicable)
   - scope (files to include)
   - message_template

2. Stage appropriate files:
   - git add {scope}

3. Create commit:
   - Format message
   - Add co-author
   - Execute commit

4. Verify success:
   - Check exit code
   - Log result

5. Return result
```

## Commit Scope Rules

### Task-Specific Commits
Include only task-related files:
```
specs/TODO.md
specs/state.json
specs/{NNN}_{SLUG}/**
```

### Implementation Commits
Include source files modified:
```
Logos/**/*.lean  (for Lean tasks)
src/**/*         (for general tasks)
```

### Phase Commits
Scope to phase changes only:
```
Files modified in that phase
Updated plan with phase status
```

## Safety Checks

### Before Commit
```
1. git status - verify staged files
2. Check no sensitive files staged (.env, credentials)
3. Verify commit message format
```

### Never Run
- `git push --force`
- `git reset --hard` (without explicit request)
- `git rebase -i`

## Message Template

```
{scope}: {action} {description}

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

## CI Triggering

### Overview

CI is **skipped by default** on push events. To trigger CI, add `[ci]` marker to the commit message.

### trigger_ci Parameter

When creating commits, the `trigger_ci` parameter controls whether CI runs:

| Value | Behavior | Use Case |
|-------|----------|----------|
| `false` (default) | No CI marker added | Routine commits, research, planning |
| `true` | Append `[ci]` to message | Lean changes, implementation completion |

### CI Decision Criteria

Trigger CI (`trigger_ci: true`) when:
- **Lean files modified** (.lean) - Ensures build passes
- **Implementation completed** - Final verification before merge
- **CI configuration changed** (.github/workflows/) - Validate workflow changes
- **Mathlib dependencies updated** (lakefile.lean, lake-manifest.json) - Ensure compatibility
- **Critical bug fixes** - Verify fix works

Skip CI (default) when:
- Documentation changes only (.md files)
- Research/planning artifacts
- Configuration changes (non-CI)
- Routine task management operations

### Commit Message with CI Marker

```
task {N}: complete implementation [ci]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### When CI Always Runs

CI runs regardless of marker on:
- Pull request events (all PRs run CI)
- Manual workflow_dispatch trigger
- Commits with `[ci]` marker

## Execution Commands

### Standard Commit
```bash
git add {files}
git commit -m "$(cat <<'EOF'
{message}

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

### Task Commit
```bash
git add specs/
git commit -m "$(cat <<'EOF'
task {N}: {action}

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

## Return Format

```json
{
  "status": "completed|failed",
  "summary": "Created commit: {short_message}",
  "commit_hash": "abc123",
  "files_committed": [
    "path/to/file1",
    "path/to/file2"
  ],
  "message": "Full commit message",
  "ci_triggered": true|false
}
```

## Error Handling

### Nothing to Commit
```json
{
  "status": "committed",
  "summary": "No changes to commit",
  "commit_hash": null
}
```

### Pre-Commit Hook Failure
```json
{
  "status": "failed",
  "error": "Pre-commit hook failed",
  "recovery": "Fix issues and retry (do not use --no-verify)"
}
```

### Git Error
```json
{
  "status": "failed",
  "error": "Git command failed: {error}",
  "recovery": "Check git status and resolve manually"
}
```

## Non-Blocking Behavior

Git failures should NOT block task operations:
- Log the failure
- Continue with task
- Report to user that commit failed
- Task state is preserved regardless
