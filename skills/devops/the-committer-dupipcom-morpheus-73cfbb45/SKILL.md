---
name: the-committer
description: Creates well-structured git commits with conventional commit messages and proper attribution.
license: HPL3-ECO-NC-ND-A 2026
---

Task: Stage changes, create commits with conventional commit messages, and prepare for code review.

Role: You're a release engineer ensuring clean, well-documented commit history.

## Commit Workflow

1. **Review changes**
   ```bash
   git status
   git diff
   ```

2. **Group related changes** into logical commits

3. **Stage files**
   ```bash
   git add <files>
   # Or for all changes
   git add -A
   ```

4. **Create commit** with conventional message

5. **Verify commit**
   ```bash
   git log -1
   git show --stat
   ```

## Conventional Commit Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring, no feature change |
| `perf` | Performance improvement |
| `test` | Adding/fixing tests |
| `chore` | Build, config, dependencies |
| `security` | Security improvements |

### Scopes (optional)

- `api` - API routes
- `ui` - User interface
- `auth` - Authentication
- `db` - Database/schema
- `tasks` - Task management
- `i18n` - Internationalization

### Examples

```bash
# Feature
git commit -m "$(cat <<'EOF'
feat(tasks): add task completion tracking

- Track completion count per task
- Store completer information
- Calculate earnings on completion

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# Bug fix
git commit -m "$(cat <<'EOF'
fix(api): return 404 for missing resources

Previously returned 500 error for missing resources.
Now correctly returns 404 with descriptive message.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# Refactor
git commit -m "$(cat <<'EOF'
refactor(api): extract tasklist service layer

Split 2700-line route.ts into service modules:
- taskListCrudService.ts
- completionService.ts
- taskStatusService.ts

No functional changes.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

## Rules

- One logical change per commit
- Keep commits atomic and focused
- Write descriptive but concise messages
- Reference issues when applicable: `Fixes #123`
- Never commit secrets or sensitive data
- Don't commit generated files (node_modules, .next)
- Always include Co-Authored-By for AI assistance

## Pre-Commit Checklist

- [ ] Changes are logically grouped
- [ ] No unrelated changes included
- [ ] No debug code left in
- [ ] No console.logs in production code
- [ ] No secrets or PII
- [ ] Commit message follows convention
- [ ] Co-Authored-By attribution included

## Files to Never Commit

- `.env.local` (secrets)
- `node_modules/`
- `.next/`
- `generated/prisma/` (regenerated on build)
- `*.log`
- `.DS_Store`

## Branch Naming

```
feature/add-task-completion
fix/missing-auth-check
refactor/split-tasklist-service
chore/update-dependencies
```

## Creating PRs

After commits are ready:
```bash
git push -u origin <branch-name>
gh pr create --title "feat: description" --body "..."
```
