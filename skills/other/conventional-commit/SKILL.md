---
name: conventional-commit
description: Creates git commits following the Conventional Commits specification (v1.0.0). Use this when the user asks to create a commit, make a commit, or when creating commits as part of a workflow. Follows the format type(scope)!: description with proper commit types and breaking change indicators.
allowed-tools: Bash, Read, Grep, Glob
---

# Conventional Commits Skill

This skill helps create git commits following the [Conventional Commits specification v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

## Instructions

When creating a commit using Conventional Commits, follow these steps:

1. **Analyze the changes**:
   - Run `git status` to see staged and unstaged files
   - Run `git diff` to review the actual changes
   - Understand what type of change this represents

2. **Determine the commit type**:
   - `feat`: A new feature (correlates with MINOR in SemVer)
   - `fix`: A bug fix (correlates with PATCH in SemVer)
   - `docs`: Documentation only changes
   - `style`: Changes that don't affect code meaning (formatting, whitespace)
   - `refactor`: Code change that neither fixes a bug nor adds a feature
   - `perf`: Performance improvement
   - `test`: Adding or correcting tests
   - `build`: Changes to build system or external dependencies
   - `ci`: Changes to CI configuration files and scripts
   - `chore`: Other changes that don't modify src or test files

3. **Determine the scope** (optional but recommended):
   - The scope should be a noun describing a section of the codebase
   - Examples: `api`, `parser`, `auth`, `ui`, `database`
   - Use parentheses: `feat(api):`

4. **Check for breaking changes**:
   - If the change introduces breaking changes, add `!` before the colon
   - Example: `feat(api)!:` or `feat!:`
   - MUST also include `BREAKING CHANGE:` footer with description

5. **Construct the commit message**:

   ```
   <type>[optional scope][!]: <description>

   [optional body]

   [optional footer(s)]
   ```

6. **Follow these rules**:
   - Description should be lowercase and concise
   - Description should complete the sentence "This commit will..."
   - Body should provide additional context (wrap at 72 characters)
   - Footers follow git trailer format: `Token: value` or `Token #value`
   - `BREAKING CHANGE:` footer must be uppercase
   - Each footer should be on its own line

7. **Create the commit**:
   - Use a heredoc for proper formatting:

   ```bash
   git commit -m "$(cat <<'EOF'
   type(scope): description

   Optional body explaining the changes in more detail.
   This can span multiple lines.

   BREAKING CHANGE: description of breaking change
   Fixes: #123
   EOF
   )"
   ```

## Commit Message Format

### Header

```
<type>[optional scope][!]: <description>
```

- **type**: Required. One of the types listed above
- **scope**: Optional. A noun describing the affected section
- **!**: Optional. Indicates a breaking change
- **description**: Required. Brief summary in present tense

### Body

- Optional
- Provides additional context about the changes
- Separated from header by one blank line
- Can contain multiple paragraphs

### Footers

- Optional
- Separated from body (or header if no body) by one blank line
- Follow git trailer format
- Common footers:
  - `BREAKING CHANGE: <description>` (for breaking changes)
  - `Fixes: #<issue-number>`
  - `Refs: #<issue-number>`
  - `Reviewed-by: <name>`
  - `Co-authored-by: <name> <email>`

## Examples

### Simple feature

```
feat(auth): add OAuth2 login support
```

### Bug fix with scope

```
fix(parser): handle null values in JSON response
```

### Breaking change with body and footer

```
feat(api)!: redesign user authentication endpoints

The authentication flow has been completely redesigned to use
JWT tokens instead of session cookies. This provides better
scalability and supports mobile clients.

BREAKING CHANGE: POST /auth/login now returns a JWT token in the response body instead of setting a session cookie. Clients must include the token in the Authorization header for subsequent requests.
Refs: #456
```

### Documentation update

```
docs(readme): update installation instructions
```

### Performance improvement

```
perf(database): optimize query for user search

Replaced N+1 query pattern with a single JOIN query,
reducing database calls from ~100 to 1 for typical searches.

Closes: #789
```

### Multiple footers

```
fix(ui): prevent memory leak in dashboard component

The chart component was not properly cleaning up event listeners
when unmounted, causing memory leaks in long-running sessions.

Fixes: #123
Reviewed-by: Jane Doe
Co-authored-by: John Smith <john@example.com>
```

### Chore with no scope

```
chore: update dependencies to latest versions
```

### Breaking change with scope

```
refactor(database)!: migrate from MongoDB to PostgreSQL

BREAKING CHANGE: All database queries must be updated to use PostgreSQL syntax. The connection string format has changed.
```

## Best Practices

1. **Be consistent**: Use the same type names and scope naming conventions across your project
2. **Keep descriptions short**: Aim for 50-72 characters in the description
3. **Use imperative mood**: "add feature" not "added feature" or "adds feature"
4. **Scope should be specific**: Use well-defined, consistent scope names
5. **Breaking changes need both**: Use both `!` and `BREAKING CHANGE:` footer for clarity
6. **One concern per commit**: Don't mix multiple types (e.g., feat + fix) in one commit
7. **Body explains "why"**: Use the body to explain why the change was made, not what was changed
8. **Reference issues**: Use footers to link commits to issues/tickets

## Integration with SemVer

Conventional Commits work with Semantic Versioning:

- `fix:` type commits = PATCH release (0.0.X)
- `feat:` type commits = MINOR release (0.X.0)
- `BREAKING CHANGE:` (any type with !) = MAJOR release (X.0.0)

## Common Patterns

### Multiple files in different areas

If changes span multiple areas, consider:

1. Making separate commits for each area
2. Using a more general scope or no scope
3. Using the most significant change as the type

### Reverting commits

```
revert: feat(api): add OAuth2 login support

This reverts commit abc123def456.
```

### Work in progress (avoid in main branches)

```
wip(feature): partial implementation of new dashboard
```

## Tools and Automation

This specification enables:

- Automatic changelog generation
- Automatic semantic versioning
- Better git log filtering (`git log --grep="^feat"`)
- Automated release notes

## Notes

- Conventional Commits is a **specification**, not a strict rule - adapt to your team's needs
- Some teams use additional types like `wip`, `hotfix`, or `release`
- The specification is designed to work with automated tools but is human-readable
- If using commitlint or similar tools, ensure your commits match their configuration
