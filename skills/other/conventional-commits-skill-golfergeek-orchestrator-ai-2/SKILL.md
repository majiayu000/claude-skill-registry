---
name: Conventional Commits
description: Conventional Commits specification format. Use when creating commit messages. Format: <type>(<scope>): <description>. Types: feat, fix, chore, docs, test, refactor, style, perf. CRITICAL: All commits must follow conventional commit format.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Conventional Commits Skill

**CRITICAL**: All commits must follow Conventional Commits format: `<type>(<scope>): <description>`

## When to Use This Skill

Use this skill when:
- Creating commit messages
- Formatting commits
- Understanding commit types
- Writing commit descriptions

## Commit Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

## Commit Types

| Type | Purpose | Example |
|------|---------|---------|
| `feat` | New feature | `feat(auth): add user login` |
| `fix` | Bug fix | `fix(api): resolve memory leak` |
| `chore` | Maintenance tasks | `chore(deps): update packages` |
| `docs` | Documentation changes | `docs(readme): update install guide` |
| `test` | Test additions/changes | `test(auth): add unit tests` |
| `refactor` | Code refactoring | `refactor(api): restructure services` |
| `style` | Code style changes | `style: format code with prettier` |
| `perf` | Performance improvements | `perf(api): optimize database query` |
| `ci` | CI/CD changes | `ci: add GitHub Actions workflow` |
| `build` | Build system changes | `build: update webpack config` |

## Scope Guidelines

Scopes identify the affected area:

### API Scopes

```bash
feat(api): add new endpoint
fix(api): resolve endpoint error
refactor(api): restructure controllers
```

### Module Scopes

```bash
feat(auth): add authentication
fix(llm): resolve provider issue
chore(mcp): update MCP tools
```

### Feature Scopes

```bash
feat(agents): add new agent type
fix(webhooks): resolve status tracking
perf(orchestration): optimize execution
```

## Commit Examples

### Simple Commit

```bash
feat(auth): add JWT token authentication
```

### Commit with Body

```bash
feat(auth): add JWT token authentication

Implement JWT token generation and validation.
- Add token generation service
- Add token validation middleware
- Update auth controller
```

### Commit with Footer

```bash
fix(api): resolve memory leak

The service was holding references to completed requests.
Now properly cleans up after request completion.

Closes #123
```

### Breaking Change

```bash
feat(api)!: change authentication endpoint

BREAKING CHANGE: Authentication endpoint moved from /auth/login to /api/auth/login
```

## Common Patterns

### Feature Development

```bash
feat(user-dashboard): add user dashboard component

- Create dashboard Vue component
- Add user stats API endpoint
- Implement real-time updates
```

### Bug Fixes

```bash
fix(login): resolve authentication error

The login was failing due to incorrect token validation.
Fixed by updating token validation logic.

Fixes #456
```

### Chores

```bash
chore(deps): update NestJS to v10

- Update @nestjs/core to 10.0.0
- Update @nestjs/common to 10.0.0
- Resolve breaking changes
```

### Documentation

```bash
docs(api): update API documentation

- Add endpoint documentation
- Update examples
- Fix formatting issues
```

### Tests

```bash
test(auth): add unit tests for auth service

- Test login functionality
- Test token generation
- Test error handling
```

### Refactoring

```bash
refactor(api): restructure service layer

- Extract common service logic
- Improve dependency injection
- Update module structure
```

## ❌ Bad Commit Messages

```bash
❌ fix stuff
❌ update
❌ changes
❌ WIP
❌ asdf
❌ fixed bug
❌ add feature
❌ work in progress
❌ commit
❌ test
```

## ✅ Good Commit Messages

```bash
✅ feat(auth): add user authentication
✅ fix(api): resolve memory leak in service
✅ chore(deps): update dependencies
✅ docs(readme): update installation guide
✅ test(auth): add unit tests for login
✅ refactor(api): restructure service layer
✅ perf(db): optimize query performance
✅ style: format code with prettier
```

## Multi-Line Commit Messages

### Format

```bash
<type>(<scope>): <short description>

<detailed description>

<footer>
```

### Example

```bash
feat(agents): add new API agent type

This commit adds support for API agents that wrap external HTTP services.
API agents use request/response transforms to adapt between Orchestrator AI
format and external service format.

Changes:
- Add API agent runtime dispatch service
- Add request/response transform logic
- Update agent registry to support API agents
- Add API agent validation

Closes #789
```

## Commit Message Guidelines

### ✅ DO

- Use imperative mood ("add" not "added")
- Keep first line under 50 characters
- Use body for detailed explanation
- Reference issues in footer
- Use breaking change notation for breaking changes

### ❌ DON'T

- Don't use past tense ("fixed" use "fix")
- Don't use first person ("I added" use "add")
- Don't write vague messages
- Don't commit unrelated changes together
- Don't use abbreviations

## Commit Message Templates

### Feature Template

```bash
feat(<scope>): <description>

<what was added>

<why it was added>

<how to test>
```

### Fix Template

```bash
fix(<scope>): <description>

<what was broken>

<how it was fixed>

<how to verify fix>

Fixes #<issue-number>
```

### Refactor Template

```bash
refactor(<scope>): <description>

<what was refactored>

<why it was refactored>

<what changed>
```

## Git Commit Commands

### Simple Commit

```bash
git commit -m "feat(auth): add user login"
```

### Multi-Line Commit

```bash
git commit -m "feat(auth): add user login" -m "Implement JWT token authentication with middleware validation"
```

### Commit with Editor

```bash
git commit
# Opens editor for multi-line message
```

## Checklist for Conventional Commits

When creating commits:

- [ ] Commit message follows format: `<type>(<scope>): <description>`
- [ ] Type is correct (`feat`, `fix`, `chore`, etc.)
- [ ] Scope identifies affected area
- [ ] Description is clear and concise
- [ ] Description uses imperative mood
- [ ] Body included if needed for context
- [ ] Footer included if referencing issues
- [ ] Breaking changes marked with `!`

## Related Documentation

- **Git Standards**: See Orchestrator Git Standards Skill
- **GitHub Workflow**: See GitHub Workflow Skill
- **Quality Gates**: See Quality Gates Skill

