---
name: formatting-commit-messages
description: Formats Git commit messages following Conventional Commits conventions. Use when the user asks to commit, write a commit message, format commits, or mentions conventional commits, staged changes, or release notes.
---

# Commit Message Formatter (Conventional Commits)

## When to use this skill

- User asks to commit staged changes
- User wants help writing a commit message
- User mentions "conventional commits" or commit formatting
- User asks for release-ready or changelog-friendly commits
- User wants to ensure commits follow team standards

## Workflow

- [ ] Check for staged changes using `git diff --cached`
- [ ] Analyze the nature of the changes (new feature, bug fix, refactor, etc.)
- [ ] Determine appropriate type prefix
- [ ] Identify scope from affected files/modules
- [ ] Check for breaking changes
- [ ] Generate formatted commit message
- [ ] Present message for user approval
- [ ] Execute commit if approved

## Conventional Commits Format

```
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

### Type Prefixes

| Type       | When to Use                                     |
| ---------- | ----------------------------------------------- |
| `feat`     | New feature for the user                        |
| `fix`      | Bug fix for the user                            |
| `docs`     | Documentation only changes                      |
| `style`    | Formatting, missing semicolons (no code change) |
| `refactor` | Code change that neither fixes nor adds feature |
| `perf`     | Performance improvement                         |
| `test`     | Adding or correcting tests                      |
| `build`    | Changes to build system or dependencies         |
| `ci`       | CI configuration changes                        |
| `chore`    | Other changes that don't modify src or tests    |
| `revert`   | Reverts a previous commit                       |

### Breaking Changes

- Add `!` after type/scope: `feat(api)!: remove deprecated endpoints`
- OR add `BREAKING CHANGE:` footer in the body

## Instructions

### Step 1: Analyze Staged Changes

Run the following to get staged diffs:

```bash
git diff --cached --stat
git diff --cached
```

### Step 2: Determine Commit Type

Analyze the changes to determine the appropriate type:

- New files in `src/` with new functionality → `feat`
- Modified files fixing incorrect behavior → `fix`
- Changes only to `*.md`, `*.txt`, or docs folder → `docs`
- Only whitespace/formatting changes → `style`
- Code restructuring without behavior change → `refactor`
- Performance optimizations → `perf`
- New or updated test files → `test`
- Changes to `package.json`, `webpack.config.*`, `tsconfig.*` → `build`
- Changes to `.github/workflows/`, CI configs → `ci`
- Dependency updates, config tweaks → `chore`

### Step 3: Identify Scope

Derive scope from the primary affected area:

- `src/components/Button.tsx` → scope: `button`
- `src/api/users.ts` → scope: `api` or `users`
- `lib/utils/` → scope: `utils`
- Multiple unrelated areas → omit scope

### Step 4: Detect Breaking Changes

Look for indicators of breaking changes:

- Removed public functions or exports
- Changed function signatures (parameters, return types)
- Renamed public APIs
- Changed default behavior
- Removed configuration options

### Step 5: Compose the Message

**Subject line rules:**

- Use imperative mood: "add" not "added" or "adds"
- No capital letter at start
- No period at the end
- Max 50 characters (hard limit: 72)

**Body (if needed):**

- Wrap at 72 characters
- Explain _what_ and _why_, not _how_
- Separate from subject with blank line

**Footer (if needed):**

- `BREAKING CHANGE: <description>`
- `Fixes #123` or `Closes #456`
- `Reviewed-by: Name <email>`

### Step 6: Present and Commit

Present the formatted message to the user:

```markdown
**Suggested commit message:**

feat(auth): add OAuth2 login support

Implement OAuth2 authentication flow with Google and GitHub providers.
Users can now sign in using their existing accounts.

Closes #142
```

If approved, execute:

```bash
git commit -m "<subject>" -m "<body>" -m "<footer>"
```

Or for simple commits:

```bash
git commit -m "<type>(<scope>): <description>"
```

## Examples

### Simple Feature

```
feat(cart): add quantity selector to cart items
```

### Bug Fix with Issue Reference

```
fix(auth): prevent token refresh race condition

Multiple simultaneous requests could trigger parallel refresh attempts.
Added mutex lock to ensure single refresh execution.

Fixes #287
```

### Breaking Change

```
feat(api)!: migrate to v2 response format

BREAKING CHANGE: API responses now use camelCase keys instead of snake_case.
All clients must update their parsing logic.
```

### Documentation Update

```
docs(readme): add installation instructions for Windows
```

### Refactor

```
refactor(utils): extract date formatting into separate module
```

## Validation

Before committing, verify:

- [ ] Type accurately reflects the change
- [ ] Scope is specific but not overly narrow
- [ ] Subject is in imperative mood
- [ ] Subject is under 50 characters
- [ ] Breaking changes are properly marked
- [ ] Related issues are referenced

## Error Handling

- **No staged changes**: Run `git status` to confirm. Prompt user to stage files first.
- **Commit fails**: Check `git status` for conflicts or hooks blocking commit.
- **Unsure about a command**: Run `git commit --help` for options.

## Resources

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Angular Commit Guidelines](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit)
