---
name: Requesting Code Review
description: This skill should be used when the user asks to "request code review", "prepare for PR review", "code review checklist", "pre-review validation", "review preparation", or needs guidance on preparing code for peer review.
version: 1.0.0
---

# Requesting Code Review: Pre-Review Preparation

## Overview

Requesting Code Review ensures that code is thoroughly prepared before peer review, maximizing reviewer efficiency and code quality. This systematic approach reduces review cycles and helps catch issues early.

## Pre-Review Checklist

### Self-Review Phase

**Code Quality Validation:**
- [ ] Code follows project style guidelines
- [ ] No debugging code (console.log, print statements) left in
- [ ] No commented-out code blocks
- [ ] All TODO comments are addressed or documented
- [ ] Variable and function names are descriptive
- [ ] Complex logic has explanatory comments

**Functionality Verification:**
- [ ] All acceptance criteria are met
- [ ] Edge cases are handled
- [ ] Error conditions are managed appropriately
- [ ] Feature works as expected in all environments
- [ ] No breaking changes to existing functionality

**Testing Completeness:**
- [ ] Unit tests written for new functionality
- [ ] Integration tests added where appropriate
- [ ] Test coverage meets project standards (≥80%)
- [ ] All tests pass locally
- [ ] No test skipping or ignoring without justification

### Documentation Requirements

**Code Documentation:**
- [ ] Public functions have JSDoc/docstrings
- [ ] Complex algorithms are explained
- [ ] API endpoints are documented
- [ ] Configuration changes are noted
- [ ] Breaking changes are highlighted

**Pull Request Documentation:**
- [ ] Clear, descriptive PR title
- [ ] Comprehensive description explaining changes
- [ ] Screenshots/videos for UI changes
- [ ] Links to related issues/tickets
- [ ] Migration instructions if applicable

### Technical Validation

**Performance Considerations:**
- [ ] No obvious performance regressions
- [ ] Database queries are optimized
- [ ] Large files/datasets handled efficiently
- [ ] Memory usage is reasonable
- [ ] API response times are acceptable

**Security Review:**
- [ ] Input validation implemented
- [ ] Authentication/authorization checked
- [ ] No sensitive data in logs or commits
- [ ] Dependencies are up to date
- [ ] No hardcoded secrets or credentials

## Pull Request Preparation

### Branch Management

```bash
# Ensure branch is up to date
git checkout main
git pull origin main

# Rebase feature branch
git checkout feature/my-feature
git rebase main

# Clean up commit history
git log --oneline -10  # Review commits
git rebase -i HEAD~3   # Interactive rebase if needed
```

### Commit Message Quality

**Good Commit Messages:**
```
feat: add user authentication with JWT tokens

- Implement login/logout endpoints
- Add password hashing with bcrypt
- Include refresh token rotation
- Update user model with auth fields

Closes #123
```

**Bad Commit Messages:**
```
fix bug
updated stuff
WIP
asdf
```

### PR Description Template

```markdown
## Summary
Brief description of what this PR accomplishes.

## Changes
- [ ] New feature X
- [ ] Bug fix for Y
- [ ] Refactor Z component
- [ ] Update documentation

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Performance impact assessed

## Screenshots/Videos
(Include for UI changes)

## Breaking Changes
- None / List any breaking changes

## Deployment Notes
- Any special deployment instructions
- Environment variable changes
- Database migrations required

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## Code Review Request Process

### 1. Pre-Request Validation

Run automated checks before requesting review:

```bash
#!/bin/bash
# scripts/pre-review-check.sh

echo "🔍 Running pre-review validation..."

# Style and formatting
npm run format
npm run lint

# Type checking
npm run type-check

# Tests
npm run test

# Build verification
npm run build

# Security scan
npm audit

echo "✅ Pre-review checks complete!"
```

### 2. Reviewer Selection

**Choose appropriate reviewers based on:**
- **Domain expertise**: Familiar with the code area
- **Availability**: Can review within reasonable timeframe
- **Team distribution**: Spread knowledge across team
- **Code ownership**: Maintain code quality standards

**Typical reviewer matrix:**
- **Senior developer**: Architecture and design review
- **Domain expert**: Business logic validation
- **Security expert**: Security-sensitive changes
- **Tech lead**: Major architectural changes

### 3. Review Request Context

**Provide context in the PR:**
- Why this change is needed
- What alternatives were considered
- Any trade-offs made
- Areas needing special attention
- Timeline expectations

## Review-Ready Indicators

### Green Flags (Ready for Review)
- ✅ All automated checks pass
- ✅ Feature is complete and tested
- ✅ Documentation is updated
- ✅ PR description is comprehensive
- ✅ Self-review completed
- ✅ No known issues remaining

### Red Flags (Not Ready)
- ❌ Automated checks failing
- ❌ WIP or incomplete features
- ❌ Missing or inadequate tests
- ❌ No description or context
- ❌ Known bugs or issues
- ❌ Performance concerns unaddressed

## Common Review Feedback Categories

### Code Quality Issues

**Naming and Clarity:**
```javascript
// ❌ Poor naming
function calc(u, p) {
    return u * p * 1.08;
}

// ✅ Clear naming
function calculateTotalWithTax(unitPrice, quantity) {
    const TAX_RATE = 0.08;
    return unitPrice * quantity * (1 + TAX_RATE);
}
```

**Error Handling:**
```python
# ❌ Poor error handling
def process_user_data(data):
    return data["user"]["email"].lower()

# ✅ Proper error handling
def process_user_data(data):
    try:
        user = data.get("user")
        if not user:
            raise ValueError("User data is required")

        email = user.get("email")
        if not email:
            raise ValueError("User email is required")

        return email.lower()
    except (KeyError, TypeError, AttributeError) as e:
        raise ValueError(f"Invalid user data format: {e}")
```

### Architecture and Design

**Single Responsibility Principle:**
```python
# ❌ Too many responsibilities
class UserManager:
    def create_user(self, data):
        # Validate data
        # Hash password
        # Send email
        # Log activity
        # Update analytics
        pass

# ✅ Separated concerns
class UserCreator:
    def __init__(self, validator, hasher, emailer, logger, analytics):
        self.validator = validator
        self.hasher = hasher
        self.emailer = emailer
        self.logger = logger
        self.analytics = analytics

    def create_user(self, data):
        validated_data = self.validator.validate(data)
        user = self._create_user_record(validated_data)
        self.emailer.send_welcome_email(user)
        self.logger.log_user_creation(user)
        self.analytics.track_user_signup(user)
        return user
```

### Testing and Coverage

**Test Quality:**
```javascript
// ❌ Poor test
test('user test', () => {
    const result = something();
    expect(result).toBeTruthy();
});

// ✅ Good test
describe('UserService.createUser', () => {
    it('should create user with valid data and return user object', async () => {
        // Arrange
        const userData = {
            email: 'test@example.com',
            password: 'SecurePass123!',
            name: 'Test User'
        };

        // Act
        const result = await userService.createUser(userData);

        // Assert
        expect(result).toMatchObject({
            id: expect.any(String),
            email: 'test@example.com',
            name: 'Test User'
        });
        expect(result.password).toBeUndefined();
    });
});
```

## Advanced Review Techniques

### Checklist-Driven Reviews

Create specific checklists for different types of changes:

**API Changes Checklist:**
- [ ] Backwards compatibility maintained
- [ ] Input validation implemented
- [ ] Error responses standardized
- [ ] Rate limiting considered
- [ ] Documentation updated
- [ ] Versioning strategy followed

**Database Changes Checklist:**
- [ ] Migration is reversible
- [ ] Performance impact assessed
- [ ] Indexes added where needed
- [ ] Data integrity constraints
- [ ] Backup strategy considered

**Security Changes Checklist:**
- [ ] Authentication requirements met
- [ ] Authorization checks implemented
- [ ] Input sanitization applied
- [ ] Audit logging included
- [ ] Security headers configured

### Automated Review Tools

**Setup GitHub Actions for automated review:**
```yaml
name: Automated Review

on: [pull_request]

jobs:
  automated-review:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Run ESLint
      run: npx eslint src/ --format @microsoft/eslint-formatter-sarif --output-file eslint-results.sarif

    - name: Upload ESLint results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: eslint-results.sarif

    - name: Run security scan
      uses: securecodewarrior/github-action-add-sarif@v1
      with:
        sarif-file: security-scan-results.sarif
```

## Review Etiquette and Communication

### Requesting Reviews

**Good review requests:**
```
@reviewer Hi! Could you please review this PR when you have time?

It adds user authentication to the API. I'd especially appreciate feedback on:
- The security approach in auth.js
- The error handling strategy
- Whether the tests cover the edge cases adequately

No rush - sometime this week would be great. Thanks!
```

**Poor review requests:**
```
@reviewer review pls
```

### Responding to Feedback

**Constructive response:**
```
Thanks for the feedback! You're right about the error handling. I've:

1. Added proper try-catch blocks in lines 45-52
2. Standardized error response format
3. Added tests for error scenarios

The performance concern is valid - I've optimized the query and added an index.
Let me know if you'd like me to explain the approach.
```

**Defensive response (avoid):**
```
This works fine. The performance is not that bad.
```

## Metrics and Improvement

### Review Quality Metrics

**Track these metrics to improve the review process:**
- Average time from PR creation to first review
- Number of review cycles per PR
- Percentage of PRs with issues found in production
- Reviewer participation and distribution
- Time to merge after approval

### Continuous Improvement

**Regular retrospectives on review process:**
- What types of issues are commonly missed?
- Are reviews taking too long?
- Do reviewers need training in specific areas?
- Are automated tools catching the right issues?
- Is the review checklist comprehensive?

## Additional Resources

### Reference Files
For detailed review patterns and standards, consult:
- **`references/review-standards.md`** - Detailed code review standards and guidelines
- **`references/feedback-patterns.md`** - Effective feedback communication patterns
- **`references/pr-templates.md`** - Pull request templates for different change types

### Example Files
Working review examples in `examples/`:
- **`examples/pr-description-examples.md`** - Good and bad PR description examples
- **`examples/review-comments.md`** - Effective review comment examples
- **`examples/self-review-checklist.md`** - Comprehensive self-review checklist

### Scripts
Review preparation scripts in `scripts/`:
- **`scripts/pre-review-check.sh`** - Automated pre-review validation
- **`scripts/generate-pr-template.sh`** - Generate PR template based on changes
- **`scripts/review-metrics.py`** - Generate review process metrics

## Tools and Integration

### IDE Integration
- **VS Code**: GitLens extension for better Git history
- **IntelliJ**: Built-in code review tools
- **Vim**: Fugitive plugin for Git integration

### Review Platforms
- **GitHub**: Built-in review tools with suggestions
- **GitLab**: Merge request reviews with approval rules
- **Bitbucket**: Pull request reviews with automatic merging
- **Azure DevOps**: Pull request policies and branch protection

Use this systematic approach to prepare high-quality code reviews that maximize team collaboration and code quality while minimizing reviewer burden and review cycles.