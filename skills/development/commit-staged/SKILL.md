---
name: commit-staged
description: Generate descriptive commit messages by analyzing git diffs, very fast and context pollution safe. Use on any request to commit staged changes.
model: haiku
user-invocable: true
context: fork
allowed-tools: Bash(git:*), Read, Glob, Grep, Bash(grep:*), Bash(find:*), Bash(fdfind:*), Bash(prek:*), Bash(uv run prek:*), Bash(uv run pre-commit:*), Bash(pre-commit:*)
argument-hint: "[notes or comments to account for in the commit message]"
---

Analyze these staged changes and generate commit message, then commit the changes:
!`uv run prek run >/dev/null 2>&1 || git add -u`
!`git --no-pager status`
!`git --no-pager diff --cached`
!`git --no-pager diff --cached --stat`

<user_notes>
$ARGUMENTS
</user_notes>

## Commit message format

Follow conventional commits format (no footer, except for breaking change footer):

```text
<type>(<scope>): <description>

[optional body]
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, missing semicolons)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

**Feature commit:**

```text
feat(auth): add JWT authentication

Implement JWT-based authentication system with:
- Login endpoint with token generation
- Token validation middleware
- Refresh token support
```

**Bug fix:**

```text
fix(api): handle null values in user profile

Prevent crashes when user profile fields are null.
Add null checks before accessing nested properties.
```

**Refactor:**

```text
refactor(database): simplify query builder

Extract common query patterns into reusable functions.
Reduce code duplication in database layer.
```

## Commit message guidelines

**DO:**

- Use imperative mood ("add feature" not "added feature")
- Keep first line under 50 characters
- Capitalize first letter
- No period at end of summary
- Explain WHY not just WHAT in body

**DON'T:**

- Use vague messages like "update" or "fix stuff"
- Include technical implementation details in summary
- Write paragraphs in summary line
- Use past tense

## Multi-file commits

When committing multiple related changes:

```text
refactor(core): restructure authentication module

- Move auth logic from controllers to service layer
- Extract validation into separate validators
- Update tests to use new structure
- Add integration tests for auth flow

Breaking change: Auth service now requires config object
```

## Scope Rules

**Scope MUST identify WHERE in the codebase, NOT what type of change.**

The scope is a module, component, or directory name - never a description of the change itself.

### Determining Scope

1. **Single module/directory**: Use that module name

   - Changes to `src/auth/*.py` → `auth`
   - Changes to `plugins/gitlab-skill/` → `gitlab-skill`

2. **Multiple files in same area**: Use the common parent

   - Changes to `skills/python3-dev/assets/*.py` → `assets` or `python3-dev`

3. **Cross-cutting changes**: Use the primary affected area OR omit scope

   - Config + code changes → use primary area: `feat(auth): add OAuth support`
   - Truly scattered changes → omit: `chore: update dependencies across modules`

4. **Root config files**: Use the config type
   - `pyproject.toml` linting rules → `lint` or `ruff`
   - `pyproject.toml` dependencies → `deps`
   - `.github/workflows/` → `ci`

### Scope Anti-Patterns

**NEVER use these as scopes** - they describe WHAT, not WHERE:

| ❌ Wrong   | ✅ Correct                     | Why                                     |
| ---------- | ------------------------------ | --------------------------------------- |
| `docs`     | `readme`, `api-docs`, `skills` | "docs" is a change type, not a location |
| `tests`    | `auth-tests`, `api`            | Be specific about what's being tested   |
| `types`    | `models`, `api`                | Types belong to a module                |
| `refactor` | (use as type, not scope)       | "refactor" is a type, not a location    |
| `bugfix`   | (use `fix` as type)            | "bugfix" is a type, not a location      |

### Scope Examples

**By domain:**

- `feat(auth): add JWT authentication`
- `fix(payments): handle currency conversion`
- `refactor(users): extract validation logic`

**By layer:**

- `feat(api): add user profile endpoint`
- `fix(db): resolve connection pool leak`
- `chore(ci): update Node version to 20`

**By plugin/skill:**

- `feat(gitlab-skill): add MR approval support`
- `fix(python3-dev): correct shebang detection`
- `docs(commit-staged): clarify scope selection`

## Breaking changes

Indicate breaking changes clearly:

```text
feat(api)!: restructure API response format

BREAKING CHANGE: All API responses now follow JSON:API spec

Previous format:
{ "data": {...}, "status": "ok" }

New format:
{ "data": {...}, "meta": {...} }

Migration guide: Update client code to handle new response structure
```

## Template workflow

1. **Review changes**: `git diff --staged`
2. **Identify type**: Is it feat, fix, refactor, etc.?
3. **Determine scope**: What part of the codebase?
4. **Write summary**: Brief, imperative description
5. **Add body**: Explain why and what impact
6. **Note breaking changes**: If applicable

## Interactive commit helper

Use `git add -p` for selective staging:

```bash
# Stage changes interactively
git add -p

# Review what's staged
git diff --staged

# Commit with message
git commit -m "type(scope): description"
```

## Amending commits

Fix the last commit message:

```bash
# Amend commit message only
git commit --amend

# Amend and add more changes
git add forgotten-file.js
git commit --amend --no-edit
```

## Best practices

1. **Atomic commits** - One logical change per commit
2. **Test before commit** - Ensure code works
3. **Reference issues** - Include issue numbers if applicable
4. **Keep it focused** - Don't mix unrelated changes
5. **Write for humans** - Future you will read this

## Commit message checklist

- [ ] Type is appropriate (feat/fix/docs/etc.)
- [ ] Scope identifies WHERE (module/directory), NOT what type of change
- [ ] Scope is NOT a banned word: `docs`, `tests`, `types`, `refactor`, `bugfix`
- [ ] Summary is under 50 characters
- [ ] Summary uses imperative mood
- [ ] Body explains WHY not just WHAT
- [ ] Breaking changes are clearly marked
- [ ] Related issue numbers are included

Finally, you will commit the changes with the generated commit message, without using `--no-verify`:

```sh
git commit -m "<commit-message>"
```

If you are blocked by a pre-commit or prek hook, you should stop, and announce your intended commit message, and that it was blocked, and requires a linting-agent to be run against the issues found.
