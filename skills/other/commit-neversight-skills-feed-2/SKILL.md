---
name: commit
description: Generates git commit messages following Conventional Commits 1.0.0 specification with semantic types (feat, fix, etc.), optional scope, and breaking change annotations. Use when committing code changes or creating commit messages. Triggers on phrases like 'commit', 'commit and push', 'make a commit', 'git commit', or when commit is part of a compound action (e.g., 'bump version and commit').
---

# Conventional Commit Generator

## Workflow

1. Run `git status` and `git diff HEAD` to analyze changes
2. Stage files: user-specified only, or `git add -A` for all
3. Commit using HEREDOC format:

   ```bash
   git commit -m "$(cat <<'EOF'
   <type>(<scope>): <description>
   EOF
   )"
   ```

4. Output: `<hash> <subject>`

**DO NOT:** Modify code, push (unless asked), amend without request

## Format

```text
<type>[scope][!]: <description>
```

**Types:** `feat`, `fix`, `perf`, `refactor`, `style`, `test`, `docs`, `build`, `ci`, `revert`, `chore`

**Subject:** Imperative mood ("Add" not "Added"), capitalize first letter, no period, ~50 chars (max 72)

**Scope:** Optional noun for affected area (e.g., `auth`, `api`, `parser`)

**Breaking changes:** Add *exclamation mark* before colon: `feat(api)!: Remove deprecated endpoints`

**Issue references:** Use footer: `Closes #123` or `Fixes #456`

## Body (when needed)

Add body for non-trivial changes. Explain *what* and *why*, not *how*. Wrap at 72 chars.
