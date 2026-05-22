---
name: git-majo
description: |
  Git workflow standards for Mark's projects.
  Trigger when user mentions: "commit", "committing", "git commit",
  "git history", "branches", "branching", "push to remote",
  "create a pull request", "PR", "merge conflict",
  or when performing any git operation.
  Covers commit message format, auto-commit policy, and push behavior.
license: Unlicense OR 0BSD
metadata:
  author: Mark Joshwel <mark@joshwel.co>
  version: "2026.2.2"
---

# Git Workflow Standards (Mark)

## Goal

Enable consistent, traceable git history that tracks LLM prompt count per feature/bug fix while following conventional commits format.

## When to Use This Skill

**Use when:**
- User asks to commit changes
- Creating or managing branches
- Working with git history
- Setting up pull requests
- Any git operation mentioned in prompt

**Do NOT use when:**
- User explicitly says "do not commit"
- Working in a non-git directory (no .git folder)

## Process

1. **Check status**: Run `git status` and `git diff` to see changes
2. **Review conventions**: Check `git log --oneline -10` for existing commit style
3. **Stage changes**: `git add <files>`
4. **Commit**: Use conventional format with original prompt in description
5. **Stop**: Do not push unless explicitly told to

## Constraints

- **ALWAYS commit after every prompt** (unless user says "do not commit")
- **One commit per prompt** (unless prompt asks for multiple)
- **NEVER auto-push** - wait for explicit push instruction
- **Include simplified prompts leading up to the commit** in the commit description (shortened if lengthy)
- **Match existing style** from repository history

## Auto-Commit Policy

**ALWAYS commit after every prompt unless explicitly told NOT to**

This allows tracking how many LLM prompts a feature or bug fix required.

### Commit Workflow

After completing work on a prompt:

```bash
# 1. Check what changed
git status
git diff

# 2. Stage changes
git add <files>

# 3. Commit with descriptive message (see format below)
git commit -m "type(component): description"

# 4. DO NOT push (unless explicitly told to)
```

## Commit Message Format

Use conventional commits format:

```
<type>[(<component>)]: <description>
```

### Types

- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style/formatting (no logic change)
- `refactor` - Code refactoring
- `perf` - Performance improvements
- `test` - Adding or fixing tests
- `chore` - Maintenance tasks, dependencies
- `ci` - CI/CD changes
- `meta` - Repository/meta changes (init, config, etc.)

### Examples

```bash
# Simple changes
git commit -m "meta: init files"
git commit -m "feat(cli): add verbose flag"
git commit -m "fix(parser): handle empty input"

# With component
git commit -m "ci(lint): add basedpyright check"
git commit -m "docs(readme): update installation steps"
git commit -m "refactor(utils): extract helper functions"
```

## Including Prompts Leading Up to the Commit

**Commit description should include the simplified prompts leading up to the commit** (shortened/redacted if lengthy):

```bash
# For short prompts
git commit -m "feat(api): add user authentication endpoint" -m "Prompts: add login with jwt tokens; wire refresh token flow"

# For longer prompts (redact verbose parts)
git commit -m "fix(parser): handle edge case in csv parsing" -m "Prompts: fix issue where empty lines cause crash [diagnostic output redacted]; add regression test"
```

**Redaction guidelines**:
- Keep the core request/intent
- Remove large pasted diagnostic output
- Remove excessive context dumps
- Keep it readable in one line

## Push Policy

**NEVER auto-push unless explicitly told TO do so**

Default behavior: commit locally only.

When told to push:
```bash
# Push current branch
git push

# Push specific branch
git push origin <branch-name>
```

## Commit Frequency

**One commit per prompt** (unless the prompt specifically asks for multiple commits):

```
User: "Add user authentication"
→ Do work
→ git commit -m "feat(auth): add user authentication" -m "Prompt: Add user authentication"

User: "Now add password reset"
→ Do work
→ git commit -m "feat(auth): add password reset" -m "Prompt: add password reset"
```

## Branch Naming

If creating branches:
- `feature/<name>` - New features
- `fix/<name>` - Bug fixes
- `docs/<name>` - Documentation
- `refactor/<name>` - Refactoring

## Checking Past Commits

To understand commit style from history:
```bash
# View recent commits
git log --oneline -20

# View commit with message
git log -1
```

Match the style of existing commits in the repository.

## Testing Skills

After creating or updating this skill:

1. Check the description triggers properly when git operations are mentioned
2. Verify commit format examples render correctly
3. Test that Constraints section is easily scannable
4. Confirm all existing content is preserved

## Integration

This skill extends `dev-standards-majo`. Always ensure `dev-standards-majo` is loaded for:
- AGENTS.md maintenance
- Universal code principles
- Documentation policies

Works alongside:
- `python-majo` — For Python-specific development and commits
- `js-bun-majo` — For JavaScript/Bun development and commits
- `shell-majo` — For shell scripting and commits
- `writing-docs-majo` — For documentation commits
- `task-planning-majo` — For complex multi-step work
- `running-windows-commands-majo` — For git operations on Windows
