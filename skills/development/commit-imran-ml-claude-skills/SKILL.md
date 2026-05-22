---
name: commit
description: |
  Use this skill when the user wants to create a git commit, stage files,
  write a commit message, or finalize their work with a git commit.
  Also invoked by phrases like "commit my changes", "save to git", "git commit".
argument-hint: "[message or scope]"
allowed-tools: "Bash, Read, Glob"
---

# Smart Git Commit

Review staged and unstaged changes, then create a well-formatted git commit.

## Steps

1. Run `git status` to see what's changed
2. Run `git diff` and `git diff --cached` to understand the changes
3. Run `git log --oneline -5` to match the project's commit style
4. Stage relevant files with `git add <files>` (never use `git add .` blindly)
5. Write a commit message following **Conventional Commits**:
   - `feat:` — new feature
   - `fix:` — bug fix
   - `docs:` — documentation
   - `refactor:` — code restructuring (no behavior change)
   - `test:` — adding/updating tests
   - `chore:` — tooling, deps, config
   - `perf:` — performance improvement
   - `style:` — formatting, no logic change
6. Create the commit

## Rules

- Keep subject line under 72 characters
- Use imperative mood: "add feature" not "added feature"
- If the user provided `$ARGUMENTS`, use it as context or scope
- Never commit `.env`, secrets, or `settings.local.json`
- Warn the user before committing any sensitive-looking file

## Example Messages

```
feat(auth): add OAuth2 login with GitHub
fix(api): handle null response from payment gateway
docs: update README with MCP setup instructions
refactor(db): extract query builder into separate module
```

$ARGUMENTS
