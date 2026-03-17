---
name: Development Workflows
description: Modern development process patterns for shipping faster with higher quality
version: 1.0.0
license: MIT
tier: community
---

# Development Workflows

> **Ship faster, with fewer bugs, and less stress**

This skill provides battle-tested workflows for modern software development, from feature inception to production deployment.

## Core Principles

### 1. Small Batches
Smaller changes are easier to review, test, and rollback. Ship often.

### 2. Automation Over Documentation
If you have to remember to do something, automate it instead.

### 3. Fail Fast, Learn Faster
Catch issues early. The cost of a bug increases 10x at each stage.

## Development Lifecycle

### The Feature Flow

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  PLAN    │───▶│  BUILD   │───▶│  VERIFY  │───▶│  SHIP    │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │               │               │               │
     ▼               ▼               ▼               ▼
  - Specs         - Code          - Code review   - Deploy
  - Design        - Tests         - QA testing    - Monitor
  - Tasks         - Docs          - Staging       - Iterate
```

## Feature Development Workflow

### Phase 1: Planning

**Input:** User story or requirement
**Output:** Clear, scoped tasks ready for development

```yaml
Planning Checklist:
  [ ] Requirement clearly understood
  [ ] Scope defined (what's IN and OUT)
  [ ] Technical approach decided
  [ ] Tasks broken down (max 4 hours each)
  [ ] Dependencies identified
  [ ] Acceptance criteria written
  [ ] Edge cases documented
```

**Task Template:**

```markdown
## Task: [Title]

### Context
[Why are we doing this?]

### Requirements
- [ ] Requirement 1
- [ ] Requirement 2

### Technical Approach
[How will we implement this?]

### Acceptance Criteria
- [ ] AC 1
- [ ] AC 2

### Out of Scope
- Not doing X
- Not doing Y

### Dependencies
- Needs API from [other task]
```

### Phase 2: Building

**Input:** Planned tasks
**Output:** Working code with tests

```yaml
Building Workflow:
  1. Create branch:
     git checkout -b feature/description

  2. Implement in small commits:
     - Each commit should build and pass tests
     - Commit messages describe the "why"

  3. Write tests alongside code:
     - Unit tests for logic
     - Integration tests for flows
     - No code without tests

  4. Self-review before PR:
     - Run linter
     - Check for debug code
     - Review diff yourself
```

**Commit Message Format:**

```
type(scope): short description

[optional body]
- What changed
- Why it changed

[optional footer]
Closes #123
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`

### Phase 3: Verification

**Input:** Feature branch with code
**Output:** Verified, approved code

```yaml
Verification Steps:

  Code Review:
    - [ ] Meets requirements
    - [ ] Code is readable
    - [ ] No obvious bugs
    - [ ] Tests are meaningful
    - [ ] No security issues
    - [ ] Performance acceptable

  Automated Testing:
    - [ ] Unit tests pass
    - [ ] Integration tests pass
    - [ ] E2E tests pass (if applicable)
    - [ ] Linting passes
    - [ ] Type checking passes

  QA Testing:
    - [ ] Happy path works
    - [ ] Edge cases handled
    - [ ] Error states work
    - [ ] Cross-browser (if web)
    - [ ] Responsive (if web)
    - [ ] Accessibility checked
```

### Phase 4: Shipping

**Input:** Verified code
**Output:** Feature in production

```yaml
Shipping Workflow:

  Pre-Deploy:
    - [ ] All checks pass
    - [ ] PR approved
    - [ ] No merge conflicts

  Deploy:
    - [ ] Merge to main
    - [ ] Automatic deployment triggers
    - [ ] Watch deployment logs

  Post-Deploy:
    - [ ] Verify in production
    - [ ] Check error monitoring
    - [ ] Confirm metrics normal
    - [ ] Update ticket/task status
```

## Git Workflow

### Branch Strategy (GitHub Flow)

```
main ─────●─────●─────●─────●─────●─────●─────▶
           \       /         \       /
feature/a  ●──●──●            \     /
                               \   /
feature/b                      ●──●──●
```

**Rules:**
- `main` is always deployable
- All work on feature branches
- PRs required for merging to main
- Branches deleted after merge

### Branch Naming

```yaml
Pattern: type/description

Types:
  feature/ - New functionality
  fix/ - Bug fixes
  refactor/ - Code improvements
  docs/ - Documentation
  test/ - Test additions
  chore/ - Maintenance

Examples:
  feature/user-authentication
  fix/login-redirect-loop
  refactor/api-client-cleanup
```

### Pull Request Template

```markdown
## Summary
[Brief description of changes]

## Type of Change
- [ ] Feature (new functionality)
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] Refactor (no functional changes)
- [ ] Documentation
- [ ] Tests

## Changes Made
- Change 1
- Change 2

## Testing Done
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

## Screenshots (if UI changes)
[Add screenshots]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests added for changes
- [ ] Documentation updated
- [ ] No console.logs or debug code
```

## Code Review

### Reviewer Checklist

```yaml
Code Quality:
  - [ ] Code is readable and understandable
  - [ ] Functions/methods are appropriately sized
  - [ ] No code duplication
  - [ ] Names are clear and meaningful
  - [ ] Comments explain "why" not "what"

Correctness:
  - [ ] Logic is correct
  - [ ] Edge cases handled
  - [ ] Error handling appropriate
  - [ ] No race conditions

Security:
  - [ ] No hardcoded secrets
  - [ ] Input validation present
  - [ ] No injection vulnerabilities
  - [ ] Auth/authz properly handled

Performance:
  - [ ] No obvious performance issues
  - [ ] Appropriate data structures
  - [ ] Database queries efficient

Tests:
  - [ ] Tests actually test the feature
  - [ ] Test cases are meaningful
  - [ ] Edge cases covered
```

### Review Comment Levels

```yaml
Levels:
  blocking: "This must be fixed before merge"
    Example: "Security issue: user input not sanitized"

  suggestion: "Consider this improvement"
    Example: "Could extract this into a function"

  question: "Help me understand"
    Example: "Why do we need this null check?"

  nitpick: "Minor preference, optional"
    Example: "nit: could rename to be clearer"

  praise: "Highlight good work"
    Example: "Nice solution to this edge case!"
```

## Testing Strategy

### Test Pyramid

```
                    ╱╲
                   ╱  ╲
                  ╱ E2E╲      Few, slow, expensive
                 ╱──────╲
                ╱        ╲
               ╱Integration╲   Some, medium speed
              ╱────────────╲
             ╱              ╲
            ╱     Unit       ╲  Many, fast, cheap
           ╱──────────────────╲
```

### Test Types

```yaml
Unit Tests:
  What: Individual functions/components in isolation
  Speed: Fast (< 100ms each)
  Coverage: High (80%+ of logic)
  Tools: Jest, Vitest, pytest

Integration Tests:
  What: Multiple units working together
  Speed: Medium (seconds)
  Coverage: Key flows and interfaces
  Tools: Jest, pytest, Supertest

E2E Tests:
  What: Full user journeys
  Speed: Slow (minutes)
  Coverage: Critical paths only
  Tools: Playwright, Cypress
```

### What to Test

```yaml
Always Test:
  - Business logic
  - Complex algorithms
  - State machines
  - API contracts
  - Auth/authz flows
  - Payment flows
  - Data transformations

Don't Over-Test:
  - Simple getters/setters
  - Framework code
  - Third-party libraries
  - UI layout (unless critical)
```

## CI/CD Pipeline

### Standard Pipeline

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  LINT    │──▶│  TEST    │──▶│  BUILD   │──▶│  DEPLOY  │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
     │              │              │              │
     ▼              ▼              ▼              ▼
  ESLint        Unit tests      Bundle        Staging
  TypeScript    Integration     Docker        Production
  Prettier      E2E (subset)    Artifacts
```

### GitHub Actions Example

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run test

  build:
    runs-on: ubuntu-latest
    needs: [lint, test]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run build

  deploy:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    steps:
      - run: echo "Deploy to production"
```

## Debugging Workflow

### Bug Investigation Process

```yaml
1. Reproduce:
   - Get exact steps to reproduce
   - Identify affected environments
   - Note any error messages

2. Isolate:
   - Narrow down affected code area
   - Check recent changes (git blame)
   - Eliminate variables

3. Understand:
   - Add logging/debugging
   - Trace execution path
   - Check assumptions

4. Fix:
   - Make minimal change
   - Verify fix doesn't break else
   - Add regression test

5. Document:
   - Update ticket with findings
   - Consider if docs need update
   - Share learnings if applicable
```

### Debugging Commands

```bash
# Git
git log --oneline -20           # Recent commits
git log -p path/to/file         # File history with diffs
git blame path/to/file          # Who changed what
git bisect start                # Binary search for bug

# Node/JavaScript
DEBUG=* npm run dev             # Enable debug logging
node --inspect script.js        # Chrome DevTools

# Network
curl -v http://api/endpoint     # Verbose HTTP
nc -zv host port                # Test connection

# Process
lsof -i :3000                   # What's using port
ps aux | grep process           # Find process
```

## Environment Management

### Environment Types

```yaml
Local:
  Purpose: Developer machine
  Data: Local/mock data
  Config: .env.local

Development:
  Purpose: Shared dev testing
  Data: Seeded test data
  Config: Automatic from CI

Staging:
  Purpose: Pre-production verification
  Data: Production-like (anonymized)
  Config: Environment variables

Production:
  Purpose: Live users
  Data: Real data
  Config: Secrets manager
```

### Environment Variables

```yaml
# .env.example (committed)
DATABASE_URL=postgresql://localhost:5432/app
API_KEY=your-api-key-here
NEXT_PUBLIC_APP_URL=http://localhost:3000

# .env.local (gitignored)
DATABASE_URL=postgresql://user:pass@localhost:5432/app
API_KEY=actual-api-key
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**Rules:**
- Never commit secrets
- Use `.env.example` as template
- Different values per environment
- Prefix public values appropriately

## Incident Response

### When Things Go Wrong

```yaml
1. Assess:
   - Is production affected?
   - How many users impacted?
   - Is it getting worse?

2. Communicate:
   - Update status page
   - Notify stakeholders
   - Create incident channel

3. Mitigate:
   - Can we rollback?
   - Can we feature flag off?
   - Can we scale up?

4. Fix:
   - Identify root cause
   - Implement fix
   - Deploy carefully

5. Learn:
   - Write post-mortem
   - Identify preventions
   - Update runbooks
```

### Post-Mortem Template

```markdown
# Incident Post-Mortem: [Title]

## Summary
[1-2 sentence description]

## Timeline
- HH:MM - Incident began
- HH:MM - Detected via [how]
- HH:MM - Investigation started
- HH:MM - Root cause identified
- HH:MM - Fix deployed
- HH:MM - Incident resolved

## Impact
- [X] users affected
- [Y] minutes of downtime
- [Z] failed transactions

## Root Cause
[What actually went wrong]

## Resolution
[What we did to fix it]

## Prevention
- [ ] Action item 1
- [ ] Action item 2

## Lessons Learned
[What we learned]
```

---

*"Process exists to enable, not restrict. If a process doesn't help you ship better software, change it."*
