---
name: aif-commit
description: Create conventional commit messages by analyzing staged changes. Generates semantic commit messages following the Conventional Commits specification. Use when user says "commit", "save changes", or "create commit".
argument-hint: "[scope or context]"
allowed-tools: Bash(git *)
disable-model-invocation: true
---

# Conventional Commit Generator

Generate commit messages following the [Conventional Commits](https://www.conventionalcommits.org/) specification.

## Workflow

1. **Analyze Changes**
   - Run `git status` to see staged files
   - Run `git diff --cached` to see staged changes
   - If nothing staged, show warning and suggest staging

2. **Determine Commit Type**
   - `feat`: New feature
   - `fix`: Bug fix
   - `docs`: Documentation only
   - `style`: Code style (formatting, semicolons)
   - `refactor`: Code change that neither fixes a bug nor adds a feature
   - `perf`: Performance improvement
   - `test`: Adding or modifying tests
   - `build`: Build system or dependencies
   - `ci`: CI configuration
   - `chore`: Maintenance tasks

3. **Identify Scope**
   - From file paths (e.g., `src/auth/` → `auth`)
   - From argument if provided
   - Optional - omit if changes span multiple areas

4. **Generate Message**
   - Keep subject line under 72 characters
   - Use imperative mood ("add" not "added")
   - Don't capitalize first letter after type
   - No period at end of subject

## Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Examples

**Simple feature:**
```
feat(auth): add password reset functionality
```

**Bug fix with body:**
```
fix(api): handle null response from payment gateway

The payment API can return null when the gateway times out.
Added null check and retry logic.

Fixes #123
```

**Breaking change:**
```
feat(api)!: change response format for user endpoint

BREAKING CHANGE: user endpoint now returns nested profile object
```

## Behavior

When invoked:

1. Check for staged changes
2. Analyze the diff content
3. Propose a commit message
4. Ask for confirmation or modifications
5. Execute `git commit` with the message
6. After a successful commit, offer to push:
   - Show branch/ahead status: `git status -sb`
   - If the branch has no upstream, use: `git push -u origin <branch>`
   - Otherwise: `git push`
   - User choice:
     - [ ] Push now
     - [ ] Skip push

If argument provided (e.g., `/aif-commit auth`):
- Use it as the scope
- Or as context for the commit message

## Important

- Never commit secrets or credentials
- Review large diffs carefully before committing
- If staged changes contain unrelated work (e.g., a feature + a bugfix, or changes to independent modules), suggest splitting into separate commits:
  1. Show which files/hunks belong to which commit
  2. Ask for confirmation
  3. Unstage all: `git reset HEAD`
  4. Stage and commit each group separately using `git add <files>` + `git commit`
  5. Offer to push only after all commits are done
- Add Co-Authored-By for pair programming if mentioned
