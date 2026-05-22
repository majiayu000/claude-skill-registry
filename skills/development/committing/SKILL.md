---
name: 'committing'
description: 'Creates well-structured git commits following conventional commit format. Use when committing changes, preparing commits, or when asked to commit code.'
---

# Git Committing

## Commit Message Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

## Types

| Type       | Description                     |
| ---------- | ------------------------------- |
| `feat`     | New feature                     |
| `fix`      | Bug fix                         |
| `docs`     | Documentation only              |
| `style`    | Formatting, no code change      |
| `refactor` | Code change without fix/feature |
| `perf`     | Performance improvement         |
| `test`     | Adding or fixing tests          |
| `chore`    | Build, CI, tooling changes      |

## Rules

1. **Subject line**: Under 50 characters, imperative mood ("add" not "added")
2. **Body**: Wrap at 72 characters, explain "why" not "what"
3. **Scope**: Optional, indicates affected area (e.g., `parser`, `api`, `ui`)
4. **Breaking changes**: Add `!` after type or `BREAKING CHANGE:` in footer

## Workflow

1. Run `git status` to see changes
2. Run `git diff` to review modifications
3. Check recent commits with `git log --oneline -5` for style consistency
4. Stage specific files (avoid `git add -A`)
5. Write commit message using HEREDOC:

   ```bash
   git commit -m "$(cat <<'EOF'
   type(scope): subject

   Body explaining why this change was made.
   EOF
   )"
   ```

6. Verify with `git status`

## Safety

- Never commit secrets, credentials, or .env files
- Never use `--no-verify` unless explicitly requested
- Never amend commits that have been pushed
- Create NEW commits after hook failures, don't amend
