---
name: builder-role-skill
version: 1.0.0
category: development
complexity: moderate
status: active
created: 2025-12-12
author: claude-command-and-control

description: |
  Professional software implementation skill for building features, components,
  and systems through multi-phase TDD development and incremental delivery.

triggers:
  - "implement feature"
  - "build component"
  - "create implementation"
  - "develop functionality"
  - "code this feature"

dependencies: []

tags:
  - implementation
  - tdd
  - feature-development
  - coding
  - incremental-delivery
---

# Builder Role Skill

## Description

Implement production-quality features, components, and systems using test-driven development, incremental delivery, and professional software engineering practices.

## When to Use This Skill

- Implementing features from architectural specifications
- Building new components or systems
- Converting designs into production code
- Feature development requiring multi-phase implementation
- TDD-based development workflows

## When NOT to Use This Skill

- For system design or architecture (use architect-role-skill)
- For testing and code review (use validator-role-skill)
- For documentation generation (use scribe-role-skill)
- For infrastructure work (use devops-role-skill)

## Prerequisites

- Architecture or design specification available
- Development environment configured
- Test framework in place
- Git repository initialized

---

## Workflow

### Phase 1: Task Decomposition

Break architectural specifications into granular, implementable tasks.

**Step 1.1: Load Planning Documents**
```
Read context files:
- DEVELOPMENT_PLAN.md (or equivalent)
- ARCHITECTURE.md (design specifications)
- TODO.md (task backlog)
- MULTI_AGENT_PLAN.md (if multi-agent workflow)
```

**Step 1.2: Create Implementation Plan**

Generate `IMPLEMENTATION_PLAN.md` with structured task breakdown:

```markdown
# Implementation Plan: [Feature Name]

## Architecture Reference
- Source: [Document] Section [X]
- Components: [List components to build]
- Dependencies: [External/internal dependencies]

## Phase Breakdown

### Phase 1: Foundation
- [ ] Task 1.1: [Specific task]
- [ ] Task 1.2: [Specific task]
- [ ] Task 1.3: Write unit tests for foundation

### Phase 2: Business Logic
- [ ] Task 2.1: [Specific task]
- [ ] Task 2.2: [Specific task]
- [ ] Task 2.3: Write service tests

### Phase 3: Integration
- [ ] Task 3.1: [Specific task]
- [ ] Task 3.2: Write integration tests
- [ ] Task 3.3: Full test suite validation

## Completion Criteria
- All tests passing (coverage >= 80%)
- Code linted with zero errors
- Documentation updated
- Peer review approved
```

**Step 1.3: Validate Plan**
- Ensure tasks are specific and measurable
- Verify dependencies are identified
- Confirm test coverage is planned
- Check phase estimates are realistic

---

### Phase 2: TDD Implementation Loop

For each task in the implementation plan, follow the RED-GREEN-REFACTOR cycle:

**Step 2.1: RED - Write Failing Test**

```javascript
// Example: test/user-service.test.js
describe('UserService', () => {
  test('createUser should validate email format', async () => {
    const userService = new UserService();
    await expect(userService.createUser({
      email: 'invalid-email',
      name: 'John Doe'
    })).rejects.toThrow('Invalid email format');
  });
});
```

Run test to confirm it fails:
```bash
npm test -- --testPathPattern=user-service
# Expected: FAIL - Test should fail initially
```

**Step 2.2: GREEN - Write Minimal Implementation**

```javascript
// Example: src/services/user-service.js
class UserService {
  async createUser(userData) {
    // Minimal code to make test pass
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(userData.email)) {
      throw new Error('Invalid email format');
    }
    // ... rest of implementation
  }
}
```

Run test to confirm it passes:
```bash
npm test -- --testPathPattern=user-service
# Expected: PASS - Test should now pass
```

**Step 2.3: REFACTOR - Improve Code Quality**

1. **Extract reusable functions**:
```javascript
// utils/validators.js
export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Refactored service
import { isValidEmail } from '../utils/validators.js';

class UserService {
  async createUser(userData) {
    if (!isValidEmail(userData.email)) {
      throw new Error('Invalid email format');
    }
    // ... rest of implementation
  }
}
```

2. **Run linter and formatter**:
```bash
npm run lint     # Fix linting issues
npm run format   # Auto-format code
```

3. **Re-run tests**:
```bash
npm test
# Expected: All tests still pass after refactoring
```

**Step 2.4: Commit Progress**

```bash
git add .
git commit -m "feat(user): add email validation to user creation

- Implement email format validation
- Add unit tests for validation
- Extract reusable validator utility

Tests: 12 passing, coverage 85%
Refs: #[issue-number]"
```

---

### Phase 3: Phase Integration

After completing all tasks in a phase:

**Step 3.1: Run Full Test Suite**

```bash
# Run all tests
npm test

# Check coverage
npm run coverage
# Ensure coverage >= 80%

# Run linter
npm run lint
# Zero errors required
```

**Step 3.2: Update Progress Tracking**

Mark phase complete in planning documents:
- `IMPLEMENTATION_PLAN.md` - Check off phase tasks
- `TODO.md` - Update task status
- `MULTI_AGENT_PLAN.md` - Update coordination status (if applicable)

**Step 3.3: Create Phase Commit**

```bash
git add .
git commit -m "feat([feature-name]): Complete Phase [N] - [Phase Name]

Phase [N] Summary:
- ✅ Task 1 completed
- ✅ Task 2 completed
- ✅ Task 3 completed

Tests: [X] passing, coverage [Y%]
Phase: [N] of [Total]
Next: Phase [N+1]"
```

---

### Phase 4: Final Integration & Handoff

After all phases complete:

**Step 4.1: Integration Testing**

```bash
# Merge feature branch to develop
git checkout develop
git merge --no-ff feature/[feature-name]

# Run full test suite including integration tests
npm run test:integration

# Verify all tests pass
```

**Step 4.2: Create Pull Request**

```bash
gh pr create \
  --title "feat: [Feature Name]" \
  --body-file PR_DESCRIPTION.md \
  --label "ready-for-review"
```

**PR Description Template**:
```markdown
## Feature: [Name]

### Summary
[1-2 sentence description]

### Implementation Details
- Component 1: [Description]
- Component 2: [Description]

### Test Coverage
- Unit tests: [X] tests, [Y%] coverage
- Integration tests: [Z] scenarios

### Breaking Changes
- [None / List breaking changes]

### Migration Guide
[If breaking changes, provide migration steps]

### Checklist
- [ ] All tests passing
- [ ] Coverage >= 80%
- [ ] Linting passes
- [ ] Documentation updated
- [ ] No known bugs
```

**Step 4.3: Handoff to Validator**

If using multi-agent workflow, create handoff document:

```markdown
---
TO: Validator Agent (or use validator-role-skill)
FEATURE: [Feature Name]
PR: #[PR number]
IMPLEMENTATION_PLAN: IMPLEMENTATION_PLAN.md
TEST_COVERAGE: [X%]

IMPLEMENTATION_NOTES:
  - [Key implementation detail 1]
  - [Any concerns or trade-offs]
  - [Areas needing special attention]

VALIDATION_REQUESTS:
  - [ ] Unit test review
  - [ ] Integration test verification
  - [ ] Code quality assessment
  - [ ] Security review (if handling sensitive data)
---
```

---

## Specialized Workflows

### Workflow A: Bug Fix Implementation

**When to Use**: Fixing defects in existing code

**Step A.1: Bug Analysis**
```markdown
# Bug Fix Plan: [Bug ID]

## Problem Description
[What is broken, symptoms, reproduction steps]

## Root Cause Analysis
[Why it's broken - technical explanation]

## Proposed Solution
[How to fix it - specific approach]

## Affected Components
[List files/modules requiring changes]

## Regression Risk
[What could potentially break]

## Testing Strategy
[How to verify fix + prevent regression]
```

**Step A.2: Test-Driven Fix**

1. **Write failing test that reproduces bug**:
```javascript
test('Bug #123: division by zero should throw error', () => {
  const calculator = new Calculator();
  expect(() => calculator.divide(10, 0))
    .toThrow('Cannot divide by zero');
});
```

2. **Implement minimal fix**:
```javascript
divide(a, b) {
  if (b === 0) {
    throw new Error('Cannot divide by zero');
  }
  return a / b;
}
```

3. **Verify test passes**
4. **Run full test suite** (check for regressions)
5. **Commit with "fix:" prefix**

**Step A.3: Verification**

```bash
# Run affected component tests
npm test -- --testPathPattern=[component]

# Run full suite
npm test

# Manual verification if UI/UX involved
[Steps to manually verify fix]
```

---

### Workflow B: Refactoring Implementation

**When to Use**: Improving code structure without changing behavior

**Step B.1: Refactoring Justification**

```markdown
# Refactoring Proposal: [Component Name]

## Current Problems
- [Problem 1: e.g., Code duplication]
- [Problem 2: e.g., Poor naming]
- [Problem 3: e.g., High complexity]

## Proposed Improvements
- [Improvement 1: Extract common logic]
- [Improvement 2: Rename variables for clarity]
- [Improvement 3: Split large function]

## Risk Assessment
- Breaking changes: [Yes/No]
- Current test coverage: [X%]
- Effort estimate: [Hours]
- Architect approval required: [Yes/No]
```

**Step B.2: Safety-First Refactoring**

1. **Ensure comprehensive test coverage FIRST**
   - If coverage < 80%, write tests before refactoring
   - Tests act as safety net

2. **Make incremental changes**
   - One refactoring at a time
   - Commit after each logical change
   - Run tests after EVERY change

3. **Never break public APIs** without version bump
   - Internal refactoring OK
   - Public API changes require coordination

4. **Document breaking changes** clearly
   - Update CHANGELOG.md
   - Provide migration guide
   - Notify stakeholders

---

## Code Quality Standards

### File-Level Requirements

Every file must have:
- [ ] File-level docstring/comment explaining purpose
- [ ] Appropriate imports/dependencies
- [ ] Consistent formatting (via auto-formatter)
- [ ] Error handling for failure modes
- [ ] Input validation where applicable

### Function-Level Requirements

Every function must have:
- [ ] Clear, descriptive name (verb for actions)
- [ ] Docstring/comment (purpose, params, returns)
- [ ] Type hints/annotations (if language supports)
- [ ] Single responsibility principle
- [ ] Unit test coverage

**Example (TypeScript)**:
```typescript
/**
 * Validates user email format and domain
 * @param email - Email address to validate
 * @returns true if valid, false otherwise
 * @throws ValidationError if email is null/undefined
 */
function validateUserEmail(email: string): boolean {
  if (!email) {
    throw new ValidationError('Email is required');
  }
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```

### Class-Level Requirements

Every class must have:
- [ ] Class-level docstring
- [ ] Well-defined public interface
- [ ] Private methods clearly marked
- [ ] Constructor documentation
- [ ] Test coverage of public methods

---

## Commit Message Standards

Use Conventional Commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semi-colons, etc.
- `refactor`: Code restructuring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Example**:
```
feat(auth): add JWT token refresh mechanism

- Implement refresh token endpoint
- Add token expiration validation
- Update authentication middleware
- Add unit tests for refresh flow

Tests: 45 passing, coverage 92%
Closes: #123
```

---

## Quality Assurance Checklists

### Before Each Commit
- [ ] Code compiles/runs without errors
- [ ] All tests pass
- [ ] Linter passes with zero errors
- [ ] Code formatted with project formatter
- [ ] No commented-out code blocks
- [ ] No debug logging statements
- [ ] Commit message follows convention

### Before Phase Completion
- [ ] Phase tasks all complete
- [ ] Test coverage meets threshold (80%+)
- [ ] Documentation updated
- [ ] IMPLEMENTATION_PLAN.md updated
- [ ] No known bugs or issues
- [ ] Performance acceptable

### Before PR Creation
- [ ] All phases complete
- [ ] Integration tests pass
- [ ] No merge conflicts with target branch
- [ ] PR description complete and accurate
- [ ] Breaking changes documented
- [ ] Migration guide provided (if needed)

---

## Collaboration Patterns

### With Architect (or architect-role-skill)
- Request clarification on unclear specifications
- Propose alternative implementations when issues discovered
- Report architectural concerns immediately
- Never deviate from architecture without approval

### With Validator (or validator-role-skill)
- Provide comprehensive test instructions
- Document known limitations or edge cases
- Request specific security reviews when handling sensitive data
- Respond promptly to code review feedback

### With Scribe (or scribe-role-skill)
- Update inline documentation as code changes
- Flag complex algorithms needing detailed explanation
- Provide API usage examples
- Document breaking changes

### With DevOps (or devops-role-skill)
- Communicate new dependencies or environment requirements
- Provide database migration scripts
- Document configuration changes
- Alert to performance-critical changes

---

## Error Handling Protocols

### When Stuck on Implementation
1. Document the problem in IMPLEMENTATION_PLAN.md
2. Research similar patterns in codebase (use grep/search)
3. Consult external documentation
4. Use researcher-role-skill if needed for deep investigation
5. Escalate to architect-role-skill if architectural change needed

### When Tests Fail
1. Analyze test failure output
2. Debug with focused console logging
3. Isolate failing component
4. Fix or update test as appropriate
5. **Never skip or disable tests** to make them pass

### When Dependencies Conflict
1. Document the conflict
2. Research resolution in package documentation
3. Test resolution in isolated environment
4. Update dependency management files
5. Notify DevOps (or use devops-role-skill) of environment changes

---

## Performance Considerations

### Code Efficiency Guidelines
- Optimize only when profiling shows bottleneck
- Prefer clarity over premature optimization
- Use appropriate data structures (arrays vs objects vs sets)
- Avoid N+1 queries (use eager loading, joins)
- Cache expensive computations
- Consider pagination for large datasets

### Resource Management
- Close file handles and connections
- Manage memory in long-running processes
- Use connection pooling for databases
- Implement timeouts for external API calls
- Log resource usage in development

---

## Security Implementation Standards

### Input Validation
- Validate ALL user input
- Sanitize before database queries
- Use parameterized queries (NEVER string concatenation)
- Validate file uploads (type, size, content)
- Implement rate limiting where appropriate

**Example (SQL Injection Prevention)**:
```javascript
// ❌ WRONG - Vulnerable to SQL injection
const query = `SELECT * FROM users WHERE email = '${userEmail}'`;

// ✅ CORRECT - Parameterized query
const query = 'SELECT * FROM users WHERE email = ?';
db.execute(query, [userEmail]);
```

### Authentication & Authorization
- Never store passwords in plain text
- Use established libraries for crypto operations
- Validate authorization on every request
- Implement proper session management
- Log authentication events

### Data Protection
- Encrypt sensitive data at rest
- Use HTTPS for data in transit
- Redact sensitive info from logs
- Implement proper access controls
- Follow principle of least privilege

---

## Examples

### Example 1: Simple Feature Implementation

**Task**: Add user registration endpoint

```markdown
## Phase 1: Foundation
1. Write test for user model validation
2. Create user model with email, password fields
3. Add email format validation
4. Add password strength validation

## Phase 2: Business Logic
1. Write test for registration service
2. Implement registration service
3. Add duplicate email check
4. Hash password before storage

## Phase 3: API Integration
1. Write integration test for /register endpoint
2. Create POST /register endpoint
3. Add input validation middleware
4. Add error handling

Result: Feature complete in 3 phases with 95% test coverage
```

### Example 2: Bug Fix

**Task**: Fix user login timeout issue

```markdown
## Bug Analysis
- Problem: Login hangs after 30 seconds
- Root cause: Database query missing index on email column
- Solution: Add database index

## Implementation
1. Write test that times login query
2. Add migration script for index
3. Run migration
4. Verify test passes
5. Measure performance improvement (30s → 50ms)
```

### Example 3: Refactoring

**Task**: Extract duplicate validation logic

```markdown
## Current Problem
- Email validation duplicated in 5 files
- Password validation duplicated in 3 files

## Solution
1. Ensure all 5 files have tests (add if missing)
2. Extract common validation to utils/validators.js
3. Update imports in all 5 files
4. Run tests after each file update
5. Remove old validation code
6. Final test run - all pass

Result: Code duplication eliminated, tests still pass
```

---

## Resources

### Templates
- `resources/IMPLEMENTATION_PLAN_template.md` - Implementation plan template
- `resources/commit_message_guide.md` - Commit message examples
- `resources/tdd_workflow.md` - TDD cycle reference

### Scripts
- `scripts/run_tests.sh` - Test execution script
- `scripts/validate_commit.py` - Pre-commit validation
- `scripts/phase_checker.sh` - Phase completion validator

---

## References

- [Agent Skills vs. Multi-Agent](../../docs/best-practices/09-Agent-Skills-vs-Multi-Agent.md)
- [Test-Driven Development Skill](../test-driven-development/) (if available)
- [Git Worktrees Skill](../using-git-worktrees/SKILL.md)

---

**Version**: 1.0.0
**Last Updated**: December 12, 2025
**Status**: ✅ Active
**Maintained By**: Claude Command and Control Project
