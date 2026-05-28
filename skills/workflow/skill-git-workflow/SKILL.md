---
name: skill-git-workflow
description: Create scoped git commits for task operations. Invoke after task status changes or artifact creation.
allowed-tools: Bash(git:*)
context:
  - core/standards/git-safety.md
  - core/standards/git-integration.md
---

# Git Workflow Skill

Create properly scoped git commits for task operations.

## Trigger Conditions

This skill activates when:
- Task status changes (research, plan, implement complete)
- Artifacts are created
- Task lifecycle operations occur

## Commit Message Formats

### Task Operations

| Operation | Format |
|-----------|--------|
| Create task | `task {N}: create {title}` |
| Complete research | `task {N}: complete research` |
| Create plan | `task {N}: create implementation plan` |
| Complete phase | `task {N} phase {P}: {phase_name}` |
| Complete task | `task {N}: complete implementation` |
| Revise plan | `task {N}: revise plan (v{V})` |

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
.claude/specs/TODO.md
.claude/specs/state.json
.claude/specs/{N}_{SLUG}/**
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
git add .claude/specs/
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
  "message": "Full commit message"
}
```

## Error Handling

### Nothing to Commit
```json
{
  "status": "completed",
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
