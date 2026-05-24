---
name: git-semantic-commits
description: Format Git commit messages following Conventional Commits specification with semantic versioning support for proper commit type detection and versioning
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers, maintainers
  workflow: commit-formatting
---

## What I do

I provide Git commit message formatting following the Conventional Commits specification with semantic versioning support:

1. **Format Commit Messages**: Enforce Conventional Commits format: `<type>(<scope>): <subject>`
2. **Detect Commit Type**: Identify commit type from content: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert
3. **Support Scopes**: Add optional scope to identify affected component/package: `feat(api):`, `fix(ui):`
4. **Detect Breaking Changes**: Identify breaking changes via `!` after type/scope or `BREAKING CHANGE:` in footer
5. **Provide Versioning Guidance**: Explain versioning implications (MAJOR.MINOR.PATCH) based on commit type
6. **Validate Messages**: Check commit messages follow Conventional Commits specification
7. **Generate Templates**: Provide commit message templates for each type
8. **Support Body and Footer**: Include detailed body and footers (BREAKING CHANGE, Closes, etc.)

## When to use me

Use this framework when:
- You need to format Git commit messages following semantic conventions
- You're creating a workflow that generates commits
- You need to detect commit type for versioning or changelog generation
- You want consistent commit message formatting across your team
- You're integrating with automated versioning tools (semantic-release, etc.)
- You need to support automated changelog generation
- You're creating PRs and want proper title formatting

This is a **framework skill** - it provides commit message formatting that other skills use.

## Conventional Commits Specification

### Format Structure

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Format Rules
- **type**: One of the allowed types (see below)
- **scope**: Optional, identifies affected component/package
- **subject**: Short description, imperative mood, no period at end
- **body**: Detailed description, can be multiple lines
- **footer**: Metadata (BREAKING CHANGE, Closes, etc.)

### Example Complete Format

```
feat(auth): add OAuth2 support for third-party providers

Implement OAuth2 authentication flow with support for Google and GitHub.
Add token refresh mechanism and error handling.

BREAKING CHANGE: The authentication API has been updated and is not backward compatible.
```

## Commit Types and Their Meanings

### 1. feat (Feature)
**Description**: A new feature

**Versioning Impact**: MINOR version increment

**Examples**:
```
feat: add user authentication
feat(api): add OAuth2 support
feat(ui): implement dark mode toggle
feat(components): add dropdown menu component
```

**Keywords**: add, implement, create, new, support, introduce, build, develop

### 2. fix (Bug Fix)
**Description**: A bug fix

**Versioning Impact**: PATCH version increment

**Examples**:
```
fix: resolve login timeout issue
fix(api): correct user ID parsing
fix(ui): prevent button double-click
fix: handle null pointer exception in data loader
```

**Keywords**: fix, error, bug, issue, problem, broken, crash, fail, incorrect, wrong

### 3. docs (Documentation)
**Description**: Documentation only changes

**Versioning Impact**: No version change (unless breaking changes in docs)

**Examples**:
```
docs: add API reference for authentication module
docs(readme): update installation instructions
docs: correct typo in contributing guide
docs: add migration guide from v1.0 to v2.0
```

**Keywords**: document, readme, docs, guide, explain, tutorial, wiki, comment, manual

### 4. style (Style)
**Description**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.)

**Versioning Impact**: No version change

**Examples**:
```
style: format code with Prettier
style: remove trailing whitespace
style: convert tabs to spaces
style: sort imports alphabetically
```

**Keywords**: format, style, whitespace, formatting, lint, prettier, eslint

### 5. refactor (Refactor)
**Description**: A code change that neither fixes a bug nor adds a feature

**Versioning Impact**: No version change

**Examples**:
```
refactor: simplify authentication flow
refactor(api): extract user service into separate module
refactor: replace promise chains with async/await
refactor: consolidate duplicate validation logic
```

**Keywords**: refactor, simplify, extract, consolidate, improve, optimize, restructure

### 6. test (Test)
**Description**: Adding missing tests or correcting existing tests

**Versioning Impact**: No version change

**Examples**:
```
test: add unit tests for authentication module
test: fix broken integration test
test: increase test coverage to 80%
test: add E2E tests for login flow
```

**Keywords**: test, spec, coverage, unit test, integration test, E2E, jest, pytest

### 7. chore (Chore)
**Description**: Changes to the build process or auxiliary tools and libraries such as documentation generation

**Versioning Impact**: No version change

**Examples**:
```
chore: upgrade dependencies to latest versions
chore: update linting rules
chore: remove unused dependencies
chore: update CI configuration
```

**Keywords**: chore, build, ci, dependencies, deps, config, tools

### 8. perf (Performance)
**Description**: A code change that improves performance

**Versioning Impact**: PATCH or MINOR (if significant improvement)

**Examples**:
```
perf: optimize database queries
perf: reduce initial bundle size by 30%
perf: implement lazy loading for images
perf: cache API responses in localStorage
```

**Keywords**: performance, optimize, speed, faster, improve performance, cache, lazy load

### 9. ci (Continuous Integration)
**Description**: Changes to CI configuration files and scripts

**Versioning Impact**: No version change

**Examples**:
```
ci: add GitHub Actions workflow for deployment
ci: fix failing CI build
ci: upgrade Node.js version in CI
ci: add code coverage reporting
```

**Keywords**: ci, continuous integration, github actions, jenkins, circleci, build

### 10. build (Build)
**Description**: Changes that affect the build system or external dependencies

**Versioning Impact**: PATCH (if dependency changes affect functionality)

**Examples**:
```
build: upgrade webpack to version 5
build: add TypeScript compilation step
build: update Dockerfile for production
build: configure bundler for ES modules
```

**Keywords**: build, webpack, babel, typescript, bundler, docker, makefile

### 11. revert (Revert)
**Description**: Reverts a previous commit

**Versioning Impact**: Depends on what's being reverted

**Examples**:
```
revert: feat(api): add OAuth2 support

This reverts commit abc123def456.
```

**Keywords**: revert, undo, rollback, revert commit

## Scope Usage

### Purpose
Scope provides context about which part of the codebase is affected.

### Common Scopes
- `api` - API changes
- `ui` - User interface changes
- `components` - Component library changes
- `auth` - Authentication/authorization
- `db` - Database changes
- `config` - Configuration changes
- `deps` - Dependency changes
- `docs` - Documentation changes
- `tests` - Test changes
- `build` - Build system changes

### Scope Examples

```
feat(api): add user registration endpoint
fix(ui): resolve mobile layout issue
refactor(auth): simplify token validation
test(components): add unit tests for Button
chore(deps): upgrade React to v18
docs(readme): update installation instructions
```

### Scope Guidelines
- Use lowercase for scope names
- Keep scope names short and consistent
- Don't use scope if change affects multiple areas
- Establish project-specific scope conventions

## Breaking Changes

### Breaking Change Indicators

A breaking change can be indicated in two ways:

**Option 1: Exclamation mark (!) after type/scope**
```
feat(api)!: change authentication endpoint URL structure
```

**Option 2: BREAKING CHANGE: in footer**
```
feat(api): add new authentication flow

BREAKING CHANGE: The authentication API has been updated and is not backward compatible. Update your clients accordingly.
```

### Breaking Change Examples

```
feat(api)!: remove deprecated endpoints

BREAKING CHANGE: /api/v1/users is no longer supported. Use /api/v2/users instead.

fix(ui)!: change component API for Button

The Button component now requires a `label` prop instead of children. This is a breaking change.

refactor(core)!: restructure data models

BREAKING CHANGE: Data models have been restructured. Migration script is required for existing databases.
```

### Versioning Impact
Breaking changes trigger MAJOR version increment (e.g., 1.2.3 → 2.0.0)

## Versioning Implications

### Semantic Versioning (SemVer)
Format: `MAJOR.MINOR.PATCH` (e.g., 1.2.3)

| Commit Type | Version Increment | Example |
|------------|-------------------|----------|
| feat | MINOR | 1.2.3 → 1.3.0 |
| fix | PATCH | 1.2.3 → 1.2.4 |
| docs | None | 1.2.3 → 1.2.3 |
| style | None | 1.2.3 → 1.2.3 |
| refactor | None | 1.2.3 → 1.2.3 |
| test | None | 1.2.3 → 1.2.3 |
| chore | None | 1.2.3 → 1.2.3 |
| perf | PATCH/MINOR | 1.2.3 → 1.2.4 or 1.3.0 |
| ci | None | 1.2.3 → 1.2.3 |
| build | PATCH (if functional) | 1.2.3 → 1.2.4 |
| revert | Depends | 1.2.3 → varies |
| BREAKING CHANGE | MAJOR | 1.2.3 → 2.0.0 |

### Changelog Generation

Proper semantic commits enable automated changelog generation:

```markdown
## [1.3.0] - 2024-01-15

### Added
- feat(api): add user registration endpoint
- feat(ui): implement dark mode toggle

### Fixed
- fix(auth): resolve token refresh issue
- fix(ui): prevent button double-click

### Changed
- refactor(core): simplify data models

## [1.2.4] - 2024-01-10

### Fixed
- fix(api): correct user ID parsing
```

## Commit Message Templates

### Template for Each Type

```
feat(<scope>): <subject>

<body>

BREAKING CHANGE: <description>
```

### Filled Examples

**Feature:**
```
feat(auth): add OAuth2 support for third-party providers

Implement OAuth2 authentication flow with support for Google and GitHub.
Add token refresh mechanism and error handling for expired tokens.
```

**Bug Fix:**
```
fix(api): resolve login timeout issue

Increase timeout duration from 30s to 60s to handle slow networks.
Add retry logic for failed authentication attempts.
```

**Documentation:**
```
docs(readme): update installation instructions

Update Node.js version requirement to v16 or later.
Add troubleshooting section for common installation issues.
```

**Performance:**
```
perf(api): optimize database queries

Add database indexes for frequently queried fields.
Reduce query execution time by 40%.
```

**Breaking Change:**
```
feat(api)!: change authentication endpoint URL structure

BREAKING CHANGE: The authentication API has been restructured.
Old: /api/auth/login
New: /api/v2/auth/login
Update your API clients accordingly.
```

## Commit Message Validation

### Validation Rules

1. **Type Check**: Must be one of: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert
2. **Format Check**: Must match pattern: `<type>(<scope>): <subject>`
3. **Subject Check**: Must be in imperative mood, no period at end
4. **Subject Length**: Should be under 72 characters
5. **Body Format**: Each line should be under 72 characters
6. **Breaking Change**: Must be clearly indicated

### Validation Script

```bash
#!/bin/bash
# Validate commit message follows Conventional Commits

COMMIT_MSG_FILE=$1
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

# Valid types
TYPES="feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert"

# Check format
if [[ ! $COMMIT_MSG =~ ^($TYPES)(\(.+\))?:\ .+ ]]; then
  echo "❌ Commit message doesn't follow Conventional Commits format"
  echo "Expected: <type>(<scope>): <subject>"
  echo "Allowed types: $TYPES"
  exit 1
fi

# Extract subject
SUBJECT=$(echo "$COMMIT_MSG" | sed 's/.*: //')

# Check subject length
if [ ${#SUBJECT} -gt 72 ]; then
  echo "❌ Subject is too long (max 72 characters)"
  echo "Current length: ${#SUBJECT}"
  exit 1
fi

# Check for period at end
if [[ $SUBJECT =~ \.$ ]]; then
  echo "❌ Subject should not end with a period"
  exit 1
fi

# Check breaking change indicator
if [[ $COMMIT_MSG =~ :\! ]]; then
  echo "✓ Breaking change detected (using !)"
fi

if grep -q "BREAKING CHANGE:" "$COMMIT_MSG_FILE"; then
  echo "✓ Breaking change detected (using footer)"
fi

echo "✅ Commit message is valid"
exit 0
```

### Git Hook Integration

```bash
# Add to .git/hooks/commit-msg
#!/bin/bash
# Path to validation script
COMMIT_MSG_FILE=$1
# Run validation
/path/to/validate-commit-msg.sh "$COMMIT_MSG_FILE"
# Exit with validation result
```

## Detection Logic

### Detecting Commit Type

```bash
#!/bin/bash
# Detect commit type from message

COMMIT_MSG="$1"

# Extract type and scope
if [[ $COMMIT_MSG =~ ^([a-z]+)(\(([a-z]+)\))?: ]]; then
  TYPE="${BASH_REMATCH[1]}"
  SCOPE="${BASH_REMATCH[2]}"
else
  TYPE="unknown"
  SCOPE=""
fi

# Determine versioning impact
case $TYPE in
  feat)
    VERSION_IMPACT="MINOR"
    ;;
  fix|perf)
    VERSION_IMPACT="PATCH"
    ;;
  *)
    VERSION_IMPACT="NONE"
    ;;
esac

echo "Type: $TYPE"
echo "Scope: $SCOPE"
echo "Version Impact: $VERSION_IMPACT"

# Check for breaking change
if [[ $COMMIT_MSG =~ :\! ]] || grep -q "BREAKING CHANGE:" <<< "$COMMIT_MSG"; then
  VERSION_IMPACT="MAJOR"
  echo "Breaking change detected!"
fi
```

## Best Practices

### Subject Guidelines
- Use imperative mood: "add" not "added" or "adds"
- Keep it short: Under 72 characters
- No period at the end
- Be specific: "fix login bug" not "fix bug"
- Use lowercase for type and scope

### Body Guidelines
- Explain what and why, not how
- Use bullet points for multiple items
- Wrap lines at 72 characters
- Reference issues: "Closes #123"

### Footer Guidelines
- **BREAKING CHANGE**: Describe what changed and how to migrate
- **Closes #123**: Reference closed issues
- **Reviewed-by @user**: Acknowledge reviewers
- **Authored-by @user**: Acknowledge original author (for cherry-picks)

### Consistency
- Use consistent scope names across project
- Follow project-specific commit conventions
- Keep commit messages atomic (one change per commit)
- Write self-explanatory commit messages

### Examples of Good Commits

```
feat(auth): add JWT token refresh mechanism

Implement automatic token refresh when access token expires.
Add retry logic for failed refresh attempts.

Closes #456
```

```
fix(ui): prevent form submission on invalid input

Disable submit button when form has validation errors.
Add visual feedback for invalid fields.
```

```
refactor(api): extract user service into separate module

Move user-related API calls from auth service to dedicated user service.
Improve code organization and testability.
```

## Common Issues

### Type Not in Allowed List

**Issue**: Commit type is not recognized

**Solution**: Use one of the allowed types: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert

### Subject Too Long

**Issue**: Subject exceeds 72 characters

**Solution**: Shorten subject or move details to body

```
Bad:
fix: resolve the timeout issue that occurs when the user tries to authenticate with an invalid token that has expired (95 chars)

Good:
fix: resolve auth timeout for expired tokens (41 chars)
```

### Subject Ends with Period

**Issue**: Subject has a period at the end

**Solution**: Remove the period

```
Bad:
feat: add user authentication.

Good:
feat: add user authentication
```

### Breaking Change Not Clearly Indicated

**Issue**: Breaking change not properly marked

**Solution**: Use `!` after type/scope or add `BREAKING CHANGE:` footer

```
Bad:
feat(api): change authentication endpoint URL (is this breaking?)

Good:
feat(api)!: change authentication endpoint URL structure

BREAKING CHANGE: /api/auth/login is now /api/v2/auth/login
```

### Missing Issue Reference

**Issue**: Commit doesn't reference related issue

**Solution**: Add issue reference in footer

```
Bad:
fix: resolve login issue

Good:
fix: resolve login timeout issue

Closes #123
```

## Integration with Other Skills

### Skills That Should Use git-semantic-commits

- **git-issue-creator**: Format commit messages for PLAN.md commits
- **ticket-branch-workflow**: Format commit messages for PLAN.md commits
- **git-pr-creator**: Format PR titles using semantic format
- **nextjs-pr-workflow**: Format commit messages for Next.js projects
- **pr-creation-workflow**: Format PR titles and descriptions
- **jira-git-workflow**: Format commit messages for JIRA tickets

### Usage Example

```bash
# Generate commit message using git-semantic-commits
COMMIT_MSG=$(git-semantic-commits --type feat --scope api --subject "add user registration")

# Add body
COMMIT_MSG="${COMMIT_MSG}

Implement user registration with email verification.
Add rate limiting to prevent abuse."

# Commit with formatted message
git commit -m "$COMMIT_MSG"
```

## Automation Tools

### Commitizen

CLI tool for enforcing Conventional Commits:

```bash
# Install commitizen
npm install -g commitizen

# Use git cz instead of git commit
git add .
git cz

# Interactive prompts guide you through commit message format
```

### Commitlint

Lint commit messages to enforce format:

```bash
# Install commitlint
npm install -g @commitlint/cli @commitlint/config-conventional

# Configure commitlint
echo "module.exports = {extends: ['@commitlint/config-conventional']}" > commitlint.config.js

# Lint commit messages
echo "feat: add new feature" | commitlint
```

### Semantic Release

Automated versioning based on commit messages:

```bash
# Install semantic-release
npm install -g semantic-release

# Configure .releaserc
cat > .releaserc <<EOF
{
  "branches": ["main", "master"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/npm",
    "@semantic-release/github"
  ]
}
EOF

# Run semantic-release (automatic on CI)
npx semantic-release
```

## Verification Commands

After formatting a commit message:

```bash
# Validate commit message format
echo "feat(api): add user registration" | commitlint

# Check subject length
echo "feat(api): add user registration" | awk '{print length($0)}'

# Extract type from commit message
git log -1 --pretty=%s | grep -oE '^[a-z]+'

# List all commit types in repository
git log --pretty=%s | grep -oE '^[a-z]+' | sort | uniq -c | sort -rn
```

## Related Skills

- **git-issue-labeler**: For labeling GitHub issues with semantic labels
- **git-issue-creator**: For creating GitHub issues with proper commit references
- **ticket-branch-workflow**: For ticket-to-branch workflows with semantic commits
- **pr-creation-workflow**: For creating PRs with semantic titles
- **nextjs-pr-workflow**: For Next.js-specific workflows with semantic commits

## References

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Commitizen](https://commitizen-tools.github.io/commitizen/)
- [Commitlint](https://commitlint.js.org/)
- [Semantic Release](https://semantic-release.gitbook.io/semantic-release/)
