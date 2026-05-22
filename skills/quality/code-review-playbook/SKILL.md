---
name: code-review-playbook
description: Use this skill when conducting or improving code reviews. Provides structured review processes, conventional comments patterns, language-specific checklists, and feedback templates. Use when reviewing PRs or standardizing review practices.
version: 2.0.0
author: AI Agent Hub
tags: [code-review, quality, collaboration, best-practices]
context: fork
agent: code-quality-reviewer
user-invocable: false
---

# Code Review Playbook
This skill provides a comprehensive framework for effective code reviews that improve code quality, share knowledge, and foster collaboration. Whether you're a reviewer giving feedback or an author preparing code for review, this playbook ensures reviews are thorough, consistent, and constructive.

## Overview
- Reviewing pull requests or merge requests
- Preparing code for review (self-review)
- Establishing code review standards for teams
- Training new developers on review best practices
- Resolving disagreements about code quality
- Improving review processes and efficiency

## Code Review Philosophy

### Purpose of Code Reviews

Code reviews serve multiple purposes:

1. **Quality Assurance**: Catch bugs, logic errors, and edge cases
2. **Knowledge Sharing**: Spread domain knowledge across the team
3. **Consistency**: Ensure codebase follows conventions and patterns
4. **Mentorship**: Help developers improve their skills
5. **Collective Ownership**: Build shared responsibility for code
6. **Documentation**: Create discussion history for future reference

### Principles

**Be Kind and Respectful:**
- Review the code, not the person
- Assume positive intent
- Praise good solutions
- Frame feedback constructively

**Be Specific and Actionable:**
- Point to specific lines of code
- Explain *why* something should change
- Suggest concrete improvements
- Provide examples when helpful

**Balance Speed with Thoroughness:**
- Aim for timely feedback (< 24 hours)
- Don't rush critical reviews
- Use automation for routine checks
- Focus human review on logic and design

**Distinguish Must-Fix from Nice-to-Have:**
- Use conventional comments to indicate severity
- Block merges only for critical issues
- Allow authors to defer minor improvements
- Capture deferred work in follow-up tickets

---

## Conventional Comments

A standardized format for review comments that makes intent clear.

### Format

```
<label> [decorations]: <subject>

[discussion]
```

### Labels

| Label | Meaning | Blocks Merge? |
|-------|---------|---------------|
| **praise** | Highlight something positive | No |
| **nitpick** | Minor, optional suggestion | No |
| **suggestion** | Propose an improvement | No |
| **issue** | Problem that should be addressed | Usually |
| **question** | Request clarification | No |
| **thought** | Idea to consider | No |
| **chore** | Routine task (formatting, deps) | No |
| **note** | Informational comment | No |
| **todo** | Follow-up work needed | Maybe |
| **security** | Security concern | **Yes** |
| **bug** | Potential bug | **Yes** |
| **breaking** | Breaking change | **Yes** |

### Decorations

Optional modifiers in square brackets:

| Decoration | Meaning |
|------------|---------|
| **[blocking]** | Must be addressed before merge |
| **[non-blocking]** | Optional, can be deferred |
| **[if-minor]** | Only if it's a quick fix |

### Examples

```typescript
// ✅ Good: Clear, specific, actionable

praise: Excellent use of TypeScript generics here!

This makes the function much more reusable while maintaining type safety.

---

nitpick [non-blocking]: Consider using const instead of let

This variable is never reassigned, so `const` would be more appropriate:
```typescript
const MAX_RETRIES = 3;
```

---

issue: Missing error handling for API call

If the API returns a 500 error, this will crash the application.
Add a try/catch block:
```typescript
try {
  const data = await fetchUser(userId);
  // ...
} catch (error) {
  logger.error('Failed to fetch user', { userId, error });
  throw new UserNotFoundError(userId);
}
```

---

question: Why use a Map instead of an object here?

Is there a specific reason for this data structure choice?
If it's for performance, could you add a comment explaining?

---

security [blocking]: API endpoint is not authenticated

The `/api/admin/users` endpoint is missing authentication middleware.
This allows unauthenticated access to sensitive user data.

Add the auth middleware:
```typescript
router.get('/api/admin/users', requireAdmin, getUsers);
```

---

suggestion [if-minor]: Extract magic number to named constant

Consider extracting this value:
```typescript
const CACHE_TTL_SECONDS = 3600;
cache.set(key, value, CACHE_TTL_SECONDS);
```
```

---

## Review Process

### 1. Before Reviewing

**Check Context:**
- Read the PR/MR description
- Understand the purpose and scope
- Review linked tickets or issues
- Check CI/CD pipeline status

**Verify Automated Checks:**
- [ ] Tests are passing
- [ ] Linting has no errors
- [ ] Type checking passes
- [ ] Code coverage meets targets
- [ ] No merge conflicts

**Set Aside Time:**
- Small PR (< 200 lines): 15-30 minutes
- Medium PR (200-500 lines): 30-60 minutes
- Large PR (> 500 lines): 1-2 hours (or ask to split)

### 2. During Review

**Follow a Pattern:**

1. **High-Level Review** (5-10 minutes)
   - Read PR description and understand intent
   - Skim all changed files to get overview
   - Verify approach makes sense architecturally
   - Check that changes align with stated purpose

2. **Detailed Review** (20-45 minutes)
   - Line-by-line code review
   - Check logic, edge cases, error handling
   - Verify tests cover new code
   - Look for security vulnerabilities
   - Ensure code follows team conventions

3. **Testing Considerations** (5-10 minutes)
   - Are tests comprehensive?
   - Do tests test the right things?
   - Are edge cases covered?
   - Is test data realistic?

4. **Documentation Check** (5 minutes)
   - Are complex sections commented?
   - Is public API documented?
   - Are breaking changes noted?
   - Is README updated if needed?

### 3. After Reviewing

**Provide Clear Decision:**
- ✅ **Approve**: Code is ready to merge
- 💬 **Comment**: Feedback provided, no action required
- 🔄 **Request Changes**: Issues must be addressed before merge

**Respond to Author:**
- Answer questions promptly
- Re-review after changes made
- Approve when issues resolved
- Thank author for addressing feedback

---

## Review Checklists

### General Code Quality

- [ ] **Readability**: Code is easy to understand
- [ ] **Naming**: Variables and functions have clear, descriptive names
- [ ] **Comments**: Complex logic is explained
- [ ] **Formatting**: Code follows team style guide
- [ ] **DRY**: No unnecessary duplication
- [ ] **SOLID Principles**: Code follows SOLID where applicable
- [ ] **Function Size**: Functions are focused and < 50 lines
- [ ] **Cyclomatic Complexity**: Functions have complexity < 10

### Security

- [ ] **Authentication**: Protected endpoints require auth
- [ ] **Authorization**: Users can only access their own data
- [ ] **Input Sanitization**: SQL injection, XSS prevented
- [ ] **Secrets Management**: No hardcoded credentials or API keys
- [ ] **Encryption**: Sensitive data encrypted at rest and in transit
- [ ] **Rate Limiting**: Endpoints protected from abuse

---

## Quick Start Guide

**For Reviewers:**
1. Read PR description and understand intent
2. Check that automated checks pass
3. Do high-level review (architecture, approach)
4. Do detailed review (logic, edge cases, tests)
5. Use conventional comments for clear communication
6. Provide decision: Approve, Comment, or Request Changes

**For Authors:**
1. Write clear PR description
2. Perform self-review before requesting review
3. Ensure all automated checks pass
4. Keep PR focused and reasonably sized (< 400 lines)
5. Respond to feedback promptly and respectfully
6. Make requested changes or explain reasoning

---

**Skill Version**: 2.0.0
**Last Updated**: 2026-01-08
**Maintained by**: AI Agent Hub Team

## Related Skills

- `test-standards-enforcer` - Enforce testing best practices during code review
- `security-scanning` - Automated security checks to complement manual review
- `unit-testing` - Unit test patterns to verify during review
- `a11y-testing` - Accessibility testing requirements for UI code reviews

## Capability Details

### review-process
**Keywords:** code review, pr review, review process, feedback
**Solves:**
- How to review PRs
- Conventional comments format
- Review best practices

### quality-checks
**Keywords:** readability, solid, dry, complexity, naming
**Solves:**
- Check code quality
- SOLID principles review
- Cyclomatic complexity

### security-review
**Keywords:** security, authentication, authorization, injection, xss
**Solves:**
- Security review checklist
- Find vulnerabilities
- Auth validation

### language-specific
**Keywords:** typescript, python, type hints, async await, pep8
**Solves:**
- TypeScript review
- Python review
- Language-specific patterns

### pr-template
**Keywords:** pr template, pull request, description
**Solves:**
- PR description format
- Review checklist
