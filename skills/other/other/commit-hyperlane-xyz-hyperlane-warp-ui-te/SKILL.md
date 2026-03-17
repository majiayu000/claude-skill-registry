---
name: commit
description: Commit changes following project quality gates and best practices. Run before creating any git commit.
---

# Commit Skill

Use this skill when committing changes to ensure quality and correctness.

## Pre-Commit Checklist

Run these in order. **Do not commit if any fail.**

1. **`pnpm prettier`** — Format all source files
2. **`pnpm lint`** — Check for ESLint errors
3. **`pnpm typecheck`** — Verify TypeScript compiles
4. **`pnpm build`** — Ensure production build succeeds (optional for small changes, required before PR)

## Staging Rules

- **Only stage files related to the current task.** Review `git status` carefully.
- **Never stage unrelated files** — markdown notes, scratch files, `.monorepo-tarballs/`, `agent/`, etc. should not be committed unless explicitly requested.
- **Use specific file paths** with `git add`, not `git add .` or `git add -A`.
- **Review `git diff --staged`** before committing to verify only intended changes are included.

## Commit Message Format

- Use conventional commit prefixes: `feat:`, `fix:`, `style:`, `chore:`, `refactor:`, `docs:`, `test:`
- Keep the first line under 72 characters
- Add a blank line then bullet points for multi-change commits
- End with `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>`
- Use a HEREDOC to pass the message to avoid shell escaping issues

## Things to Watch For

- **Secrets**: Never commit `.env`, credentials, or API keys
- **Large files**: Don't commit binaries, build artifacts, or font files (check `.gitignore`)
- **Formatting drift**: If prettier changed files you didn't touch, stage them separately or skip them

## Example Flow

```bash
pnpm prettier
pnpm lint
pnpm typecheck
git status                    # review what changed
git diff                      # verify changes are correct
git add <specific-files>      # only related files
git diff --staged             # double-check staged changes
git commit -m "$(cat <<'EOF'
feat: description of change

- Detail 1
- Detail 2

EOF
)"
```
