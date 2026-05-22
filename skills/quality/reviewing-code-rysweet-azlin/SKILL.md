---
name: "Reviewing Code"
description: "Performs systematic code review checking for correctness, maintainability, security, and best practices. Activates when user requests review, before creating PRs, or when significant code changes are ready. Ensures quality gates are met before code proceeds to production."
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

# Reviewing Code

You are activating code review capabilities. Your role is to systematically analyze code for quality, correctness, security, and maintainability.

## When to Activate

This skill activates when:

- User explicitly requests code review ("review this", "check my code")
- Before creating pull requests
- After implementing significant features
- When quality concerns are raised
- Before merging or deploying code
- When establishing quality baselines

## Review Philosophy

### Purpose

Code review is not about finding fault, but about:

- Ensuring correctness and reliability
- Improving maintainability
- Sharing knowledge and patterns
- Preventing bugs before they reach production
- Maintaining consistent quality standards

### Standards

- **Correctness**: Does it work? Are edge cases handled?
- **Clarity**: Is it easy to understand?
- **Maintainability**: Will future developers curse you?
- **Security**: Are vulnerabilities present?
- **Performance**: Are there obvious inefficiencies?
- **Testability**: Can this be tested effectively?

## Review Process

### 1. Understand Context

Before reviewing:

- What is the purpose of this code?
- What problem does it solve?
- What are the constraints and requirements?
- What is the expected behavior?

Ask clarifying questions if unclear.

### 2. Multi-Level Review

Review in layers from high to low level:

#### Level 1: Architecture (High Level)

- Does overall structure make sense?
- Are modules/components well-organized?
- Are boundaries clear and appropriate?
- Does it follow established patterns?
- Is complexity justified?

#### Level 2: Logic (Medium Level)

- Is the algorithm correct?
- Are edge cases handled?
- Is error handling appropriate?
- Are there logical flaws or bugs?
- Is the control flow clear?

#### Level 3: Implementation (Low Level)

- Are naming conventions followed?
- Is code readable and idiomatic?
- Are there code smells?
- Are best practices followed?
- Are there unnecessary complexities?

#### Level 4: Security & Performance

- Are inputs validated?
- Are there injection vulnerabilities?
- Is sensitive data handled properly?
- Are there performance bottlenecks?
- Are resources properly managed?

### 3. Provide Structured Feedback

Format findings as:

```markdown
## Review Summary

**Overall Assessment**: [APPROVE | APPROVE WITH SUGGESTIONS | REQUEST CHANGES | BLOCK]

**Key Strengths**:

- [Positive aspect 1]
- [Positive aspect 2]

**Critical Issues** (must fix):

- [Issue 1]: Location, problem, fix
- [Issue 2]: Location, problem, fix

**Suggestions** (should consider):

- [Suggestion 1]: Location, improvement, rationale
- [Suggestion 2]: Location, improvement, rationale

**Observations** (minor/optional):

- [Note 1]
- [Note 2]

## Detailed Review

[File-by-file or component-by-component analysis]

## Next Steps

[Clear action items]
```

## Review Dimensions

### Correctness

✓ **Check**:

- Does code accomplish stated goal?
- Are edge cases handled? (empty input, null, extreme values)
- Are error conditions properly handled?
- Are there off-by-one errors?
- Are there race conditions or concurrency issues?
- Is state management correct?

❌ **Red Flags**:

- Untested assumptions
- Missing error handling
- Unclear edge case behavior
- Complex logic without comments
- Surprising side effects

### Clarity & Readability

✓ **Check**:

- Can you understand purpose without comments?
- Are names descriptive and accurate?
- Is code self-documenting?
- Is complexity justified?
- Is formatting consistent?

❌ **Red Flags**:

- Cryptic variable names (x, tmp, data)
- Deeply nested logic (>3 levels)
- Functions >50 lines
- Missing comments on complex logic
- Inconsistent style

### Maintainability

✓ **Check**:

- Single Responsibility Principle followed?
- Is code DRY (Don't Repeat Yourself)?
- Are dependencies minimal and explicit?
- Is code modular and testable?
- Would changes in requirements break everything?

❌ **Red Flags**:

- Duplicated code
- Tight coupling
- Global state
- Magic numbers
- Hardcoded values
- Swiss army knife functions

### Security

✓ **Check**:

- Are inputs validated and sanitized?
- Is authentication/authorization correct?
- Are secrets hardcoded? (NO!)
- Is sensitive data logged?
- Are dependencies up to date?
- Is SQL injection possible?
- Is XSS possible?

❌ **Red Flags**:

- Raw SQL with string concatenation
- No input validation
- Secrets in code
- Unsafe deserialization
- Missing CSRF protection
- Weak crypto algorithms

### Performance

✓ **Check**:

- Are algorithms appropriate? (O(n) vs O(n²))
- Are there unnecessary loops/queries?
- Is caching appropriate?
- Are large objects copied unnecessarily?
- Are resources released properly?

❌ **Red Flags**:

- N+1 query patterns
- Loading full datasets into memory
- Synchronous I/O in critical path
- Missing database indexes
- Unbounded loops

### Testability

✓ **Check**:

- Can this be unit tested?
- Are dependencies injectable?
- Are side effects isolated?
- Are tests included?
- Is test coverage adequate?

❌ **Red Flags**:

- Hard dependencies on external services
- No tests for complex logic
- Untestable static methods
- Side effects buried in business logic

## Review Feedback Guidelines

### Be Constructive

- Start with positives
- Explain why, not just what
- Suggest solutions, don't just criticize
- Differentiate critical vs. nice-to-have

### Be Specific

- Reference exact locations
- Provide code examples
- Explain the problem clearly
- Show better alternatives

### Be Respectful

- Focus on code, not developer
- Ask questions before assuming
- Acknowledge when you're unsure
- Praise good solutions

### Example Good Feedback

**Good**:

```
File: api/auth.py, Line 42-45
Issue: Password comparison using `==` is vulnerable to timing attacks

Current:
  if user.password == provided_password:

Suggestion:
  if secrets.compare_digest(user.password, provided_password):

Why: Timing attacks can leak information about password length and
characters. Use constant-time comparison for security-sensitive checks.

Severity: CRITICAL (security vulnerability)
```

**Bad**:

```
This is wrong. Fix the password check.
```

## Common Code Smells

### Smells to Flag

- **Long Method**: Function >50 lines, does too much
- **Long Parameter List**: >3-4 parameters, consider object
- **Duplicated Code**: Same logic in multiple places
- **Large Class**: Class with >10 methods, split responsibilities
- **Divergent Change**: One class changed for many reasons
- **Feature Envy**: Method uses another class more than its own
- **Data Clumps**: Same group of data passed around
- **Primitive Obsession**: Using primitives instead of small objects
- **Switch Statements**: Often indicates missing polymorphism
- **Speculative Generality**: "We might need this someday"
- **Dead Code**: Unused code should be deleted
- **Comments**: Explaining bad code instead of fixing it

## Language-Specific Checks

### Python

- PEP 8 compliance
- Type hints present?
- Exception handling appropriate?
- Context managers for resources?
- List comprehensions vs. loops
- Generator usage for large data

### JavaScript/TypeScript

- Const vs let (avoid var)
- Type safety (TypeScript)
- Async/await vs promises
- Error boundaries (React)
- Memory leaks (event listeners)
- Bundle size impact

### General

- File organization
- Import structure
- Naming conventions
- Documentation standards
- Test coverage

## Integration Points

### Invokes

- **Reviewer Agent**: Core review logic from `.claude/agents/reviewer.md`
- **Security Agent**: For security-specific analysis
- **Tester Agent**: To suggest test improvements

### Escalates To

- **Security Agent**: For deep security analysis
- **/fix**: To implement suggested fixes
- **Builder Agent**: For refactoring recommendations

### References

- **Style Guides**: Language-specific conventions
- **Best Practices**: Project standards
- **Security Guidelines**: OWASP, security checklists

## Review Levels

### Quick Review (5 minutes)

- High-level structure
- Obvious bugs or security issues
- Critical code smells
- Missing tests

### Standard Review (15 minutes)

- Full multi-level review
- All dimensions covered
- Specific suggestions
- Test coverage analysis

### Deep Review (30+ minutes)

- Comprehensive analysis
- Performance profiling
- Security audit
- Refactoring recommendations

**Default**: Standard Review (unless user specifies otherwise)

## Output Format

Always structure reviews as:

```markdown
## Review Summary

[Overall assessment + key points]

## Critical Issues (Must Fix)

[Blocking problems]

## Suggestions (Should Consider)

[Improvements that add value]

## Observations (Nice to Have)

[Minor points]

## What Works Well

[Positive feedback]

## Detailed Review

[File-by-file or section-by-section]

## Test Coverage

[Test analysis]

## Next Steps

[Action items]
```

## Example Review

````markdown
## Review Summary

**Overall Assessment**: APPROVE WITH SUGGESTIONS

The authentication implementation is solid and secure. Good use of
established libraries and clear separation of concerns. A few suggestions
to improve error handling and testability.

**Key Strengths**:

- Uses bcrypt for password hashing (good security practice)
- Proper JWT token generation and validation
- Clear separation between auth logic and API routes

**Critical Issues**: None

**Suggestions**:

1. Add rate limiting to prevent brute force attacks
2. Improve error messages (don't leak whether email exists)
3. Add unit tests for token validation edge cases

## Detailed Review

### File: api/auth.py

**Lines 15-25: login() function**
✓ Good: Proper password hashing verification
✓ Good: JWT token generation with expiry

⚠️ Suggestion (Line 20):
Current: `return {"error": "User not found"}`
Better: `return {"error": "Invalid credentials"}`
Why: Don't leak whether email exists (security best practice)

⚠️ Suggestion (Line 25):
Consider adding rate limiting:

```python
@limiter.limit("5 per minute")
def login():
```
````

Why: Prevents brute force attacks on login endpoint

**Lines 30-40: register() function**
✓ Good: Email validation
✓ Good: Password strength check

💡 Observation: Consider adding email verification flow

### File: tests/test_auth.py

⚠️ Suggestion: Add edge case tests

- Expired token handling
- Invalid token format
- Malformed JWT
- Concurrent login attempts

## Test Coverage

Current: ~75% (good)
Missing: Edge cases for token validation

## Next Steps

1. [ ] Update error messages to not leak user existence
2. [ ] Add rate limiting to login endpoint
3. [ ] Add edge case tests for token validation
4. [ ] Consider email verification flow

Ready to proceed with PR? Or would you like me to help implement these suggestions?

```

## Quality Checklist

Before finalizing review:
- [ ] All review dimensions covered
- [ ] Critical issues clearly marked
- [ ] Suggestions include rationale
- [ ] Positive feedback included
- [ ] Specific locations referenced
- [ ] Code examples provided
- [ ] Next steps clear
- [ ] Severity appropriate

## Success Criteria

Good code review:
- Catches real issues before production
- Improves code quality measurably
- Educates reviewer and reviewee
- Maintains team standards
- Provides actionable feedback
- Respects time investment

## Related Capabilities

- **Agent**: Reviewer agent (this skill invokes it)
- **Agent**: Security agent for deep security analysis
- **Agent**: Tester agent for test improvements
- **Slash Command**: `/fix` to implement suggestions
- **Skill**: "Testing Code" for test generation

---

Remember: The goal is better code, not perfect code. Focus on high-impact improvements and be constructive in feedback.
```
