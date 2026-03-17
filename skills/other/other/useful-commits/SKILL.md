---
name: Useful Commits
description: This skill should be used when the user asks to "review this commit message", "validate my commit", "improve this commit message", "explain conventional commits", "teach me commit message best practices", "write a commit", or requests guidance on git commit formatting. Provides strict Conventional Commits formatting with Angular convention to produce concise, informative commit messages following industry best practices.
version: 0.1.0
---

# Useful Commits

## Purpose

Guide the creation of concise, conventional commit messages that follow the Conventional Commits specification with Angular convention. Enforce strict formatting rules to prevent verbose, unclear commit messages. Focus on communicating what changed and why it changed, not stylistic flourishes.

## Conventional Commits Structure

Follow this exact format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Components

**Type** (required): Describes the category of change
**Scope** (optional): Specifies what part of the codebase changed
**Description** (required): Brief summary of the change
**Body** (optional): Detailed explanation of what and why
**Footer** (optional): Breaking changes, issue references, git trailers

## Allowed Types (Angular Convention)

Use exactly these types, no others:

- `feat` - New feature for the user
- `fix` - Bug fix for the user
- `docs` - Documentation only changes
- `style` - Code style changes (formatting, missing semicolons, etc.) that don't affect code meaning
- `refactor` - Code change that neither fixes a bug nor adds a feature
- `perf` - Code change that improves performance
- `test` - Adding or correcting tests
- `build` - Changes to build system or external dependencies
- `ci` - Changes to CI configuration files and scripts
- `chore` - Other changes that don't modify src or test files

## Critical Formatting Rules

### Subject Line (type + scope + description)

**Character limit**: Maximum 70 characters including type and scope
**Mood**: Use imperative mood (command form: "add", "fix", "update", not "added", "fixes", "updating")
**Capitalization**: Do not capitalize the first letter of description
**Punctuation**: Do not end with a period
**Format**: `type(scope): description` or `type: description`

**Examples:**
```
feat(auth): add JWT token refresh mechanism
fix: prevent race condition in event handlers
docs: update API documentation for v2 endpoints
```

**Anti-patterns:**
```
feat: Added new feature.        ❌ Capitalized, ends with period
Fix bug                         ❌ Not lowercase type, missing colon
refactor: Refactored code       ❌ Not imperative mood, capitalized
feat(Auth): adds feature        ❌ Capitalized scope, present tense
```

### Body

**Line wrapping**: Wrap at 90 characters
**Maximum length**: 700 characters total (excluding footers/git trailers)
**Capitalization**: Do capitalize the first letter of sentences in body
**Blank line**: Separate subject from body with one blank line
**Content**: Explain what and why, not how
**Bullet points**: Maximum 8 bullet points if using bullets
**Paragraph structure**: Keep succinct, prefer bullets for lists

**Purpose**: Answer these questions:
- Why have I made these changes?
- What effect have my changes made?
- Why was the change needed?
- What are the changes in reference to?

### Footers (Git Trailers)

**Format**: `FOOTER-TOKEN: footer value` or `FOOTER-TOKEN #value`

**Common footers:**
- `BREAKING CHANGE: description` - For breaking changes
- `Refs: #123` - Reference to issue
- `Co-Authored-By: Name <email>` - Co-authors

**Not counted** toward 700 character body limit

## Scope Guidelines

Use scopes sparingly and consistently:

**Consistency**: Once established, always use the same scope name
- Good: `feat(auth):`, `fix(auth):`, `refactor(auth):`
- Bad: `feat(auth):`, `fix(authorization):`, `refactor(auths):`

**Lowercase only**: Scopes must be lowercase
- Good: `feat(api):`
- Bad: `feat(API):`

**Concept-focused**: Use the concept/component name, not filenames
- Good: `fix(auth):`, `feat(api):`, `refactor(ui):`
- Bad: `fix(auth-service.ts):`, `feat(api/v2/handlers):`, `refactor(components/button):`

**Multiple scopes**: Comma-separated if change affects multiple areas
- Example: `refactor(core,api): consolidate error handling`
- Note: Counts toward 70 character subject limit

**Omit when unclear**: If scope is unclear or change is global, omit it
- Good: `chore: update dependencies`

For detailed scope patterns, see **`references/scopes.md`**

## Breaking Changes

Always include breaking change notation unless explicitly told "this is prerelease, don't worry about breaking changes"

**Format**: Both are required
1. Add "!" after type/scope: `feat!:` or `feat(api)!:`
2. Add `BREAKING CHANGE:` footer with description

**Example:**
```
feat(api)!: change authentication response format

Modify login endpoint to return token object instead of plain string.
This provides additional metadata (expiry, refresh token) for clients.

BREAKING CHANGE: AuthService.login() now returns {token: string,
expiresIn: number} instead of just the token string. Update all
clients to access response.token instead of using response directly.
```

For complete breaking change patterns, see **`references/breaking-changes.md`**

## Prohibited Content

**Never include:**
- References to local spec files: `./specs/**/*.md`, `SPECS-123`, `[#DOC-456]`
- GitHub issue numbers are allowed: `Refs: #123`, `Fixes #456`

**Reasoning**: Local spec IDs are internal context that won't be meaningful to future readers or other contributors

## Writing Good Commit Messages

### Include What Changed + Why

Don't assume the reader understands the context. They may not have access to the story or ticket.

**Bad:**
```
fix: add margin
```

**Good:**
```
fix: add margin to nav items to prevent overlapping the logo

Navigation items were rendering too close to the logo on smaller
screens, causing visual overlap. Add 16px margin to create proper
spacing.
```

### Don't Expect Code to Be Self-Explanatory

What seems obvious now won't be obvious in 6 months. Explain the reasoning.

**Bad:**
```
refactor: update user component
```

**Good:**
```
refactor: extract user validation logic to separate service

Move validation logic from UserComponent to UserValidationService
to enable reuse across registration and profile edit flows. This
eliminates duplicated validation code and ensures consistent rules.
```

### Make It Clear Why the Change Was Needed

State the problem being solved, not just what was done.

**Bad:**
```
perf: add caching
```

**Good:**
```
perf: cache user preferences to reduce database queries

User preferences were being fetched on every page load, causing
unnecessary database queries. Implement in-memory cache with 5-minute
TTL to reduce database load by ~80%.
```

### Write Like a News Article

**Headline (subject)**: Sum up what happened and what is important
**Details (body)**: Provide further details in organized fashion

Think: "If I'm debugging this in production at 2am, what would I need to know?"

### Check for Logical Separation

If it's difficult to summarize the commit within 700 characters or 8 bullet points, the commit likely includes several logical changes and should be split.

**Use `git add -p`** to stage changes interactively and create multiple focused commits instead of one large commit.

## Quick Examples

### Good Commits

```
feat(auth): add JWT token refresh mechanism

Implement automatic token refresh when tokens expire within 5 minutes
of API calls. This prevents users from being logged out during active
sessions. Refresh happens transparently in the background.
```

```
fix: prevent race condition in event handlers

Add mutex lock around event processing to ensure handlers execute
sequentially. Rapid events could trigger handlers out of order,
causing inconsistent state updates.

Fixes #234
```

```
docs: update authentication flow documentation

Add sequence diagrams for OAuth flow and clarify token refresh
behavior. Previous documentation was missing the refresh token
exchange step.
```

```
perf(api): optimize database queries for user dashboard

Replace N+1 query pattern with batch loading using dataloader.
Dashboard load time reduced from 2.3s to 0.4s for users with
many projects.
```

### Bad Commits (with explanations)

```
feat: Added new feature to the app.
```
**Problems**: Capitalized, ends with period, vague description, past tense

```
Fix bug in auth
```
**Problems**: Not lowercase type, missing colon, vague

```
refactor(Auth): Refactoring the authentication system to make it better and more secure and maintainable.
```
**Problems**: Capitalized scope, not imperative, capitalized description, too verbose without specifics

```
update user validation per SPECS-234
```
**Problems**: Missing type, references local spec file (prohibited)

## Additional Resources

### Reference Files

For comprehensive guidance, consult:
- **`references/scopes.md`** - Detailed scope usage patterns and consistency guidelines
- **`references/breaking-changes.md`** - Complete breaking change notation and pre-release handling
- **`references/conventional-commits-spec.md`** - Full Conventional Commits specification
- **`references/writing-guide.md`** - Extended philosophy on writing meaningful commit messages

### Examples

See **`examples/good-bad-commits.md`** for real-world examples comparing good and bad commit messages across different scenarios.

## Workflow Integration

When creating commits:

1. Review staged changes with `git diff --staged`
2. Identify the primary type (feat, fix, refactor, etc.)
3. Determine if scope is clear and consistent
4. Draft subject line (imperative mood, lowercase, no period)
5. Check subject line length (≤70 chars including type and scope)
6. If body needed, explain what and why (not how)
7. Wrap body at 90 characters, keep under 700 characters
8. Add breaking change notation if applicable
9. Verify no local spec references
10. Double-check imperative mood and capitalization rules

Apply these rules strictly to every commit message without exception.
