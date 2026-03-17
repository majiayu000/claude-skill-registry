---
name: Code Review Culture
description: Building a positive code review culture that catches bugs, shares knowledge, maintains code quality, and builds team trust through effective review practices.
---

# Code Review Culture

> **Current Level:** Intermediate  
> **Domain:** Team Collaboration / Code Quality

---

## Overview

Code review culture is essential for maintaining code quality, sharing knowledge, and building team trust. Effective code review practices catch bugs before production, ensure consistent standards, help onboard new team members, and foster collaborative improvement.

## Why Code Review Matters

| Benefit | Impact |
|---------|---------|
| **Catch Bugs Before Production** | Reduce defects in production |
| **Knowledge Sharing** | Team learns from each other |
| **Maintain Code Quality** | Consistent code standards |
| **Onboard New Team Members** | Learn codebase through reviews |
| **Build Team Trust** | Collaborative improvement |

---

## Core Concepts

### Code Review Objectives

#### Correctness

```javascript
// Does it work?
function calculateTotal(items) {
    return items.reduce((sum, item) => sum + item.price, 0);
}

// Review: Check edge cases (empty array, null items)
function calculateTotal(items) {
    if (!items || items.length === 0) return 0;
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

### Quality

```javascript
// Is it well-written?
// Bad: Complex, hard to understand
function d(a){return a.reduce((b,c)=>b+c.p,0)}

// Good: Clear, readable
function calculateTotal(items) {
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

### Readability

```javascript
// Can others understand?
// Bad: Unclear variable names
function x(y){return y.map(z=>z*2)}

// Good: Descriptive names
function doubleNumbers(numbers) {
    return numbers.map(number => number * 2);
}
```

### Design

```javascript
// Is the approach sound?
// Bad: Tight coupling
function processOrder(order) {
    saveToDatabase(order);
    sendEmail(order);
    updateInventory(order);
    chargeCreditCard(order);
}

// Good: Separation of concerns
function processOrder(order) {
    const orderService = new OrderService();
    orderService.process(order);
}
```

### Tests

```javascript
// Are there adequate tests?
// Bad: No tests
function calculateTotal(items) {
    return items.reduce((sum, item) => sum + item.price, 0);
}

// Good: With tests
function calculateTotal(items) {
    return items.reduce((sum, item) => sum + item.price, 0);
}

// Tests
describe('calculateTotal', () => {
    it('calculates total correctly', () => {
        const items = [{ price: 10 }, { price: 20 }];
        expect(calculateTotal(items)).toBe(30);
    });
    
    it('handles empty array', () => {
        expect(calculateTotal([])).toBe(0);
    });
});
```

### Security

```javascript
// Are there security vulnerabilities?
// Bad: SQL injection vulnerability
function getUser(id) {
    const query = `SELECT * FROM users WHERE id = ${id}`;
    return db.query(query);
}

// Good: Parameterized query
function getUser(id) {
    const query = 'SELECT * FROM users WHERE id = $1';
    return db.query(query, [id]);
}
```

## Code Review Process

### Step-by-Step Process

```
┌─────────────────────────────────────────────────────────────────┐
│  Code Review Process                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Create PR ──▶ 2. Automated Checks ──▶ 3. Reviewers Assigned ──▶ 4. Reviewers Provide Feedback ──▶ 5. Developer Addresses Feedback ──▶ 6. Approval and Merge │
│                                                                  │
│  └───────────────────────────────────────────────────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

### Step 1: Create PR

```bash
# Create pull request
git checkout -b feature/new-feature
git add .
git commit -m "Add new feature"
git push origin feature/new-feature

# Create PR on GitHub
```

### Step 2: Automated Checks

```yaml
# GitHub Actions workflow
name: CI
on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: npm test
      - name: Run linter
        run: npm run lint
      - name: Run type check
        run: npm run type-check
```

### Step 3: Reviewers Assigned

```javascript
// Assign reviewers automatically
// GitHub: CODEOWNERS file
# Frontend code
*.js @frontend-team
*.jsx @frontend-team

# Backend code
*.py @backend-team
*.go @backend-team

# Database migrations
migrations/ @db-team
```

### Step 4: Reviewers Provide Feedback

```javascript
// Good review comment
// "I noticed that this function doesn't handle the case where `items` is null. 
// Consider adding a null check or using optional chaining."
function calculateTotal(items) {
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

### Step 5: Developer Addresses Feedback

```javascript
// Address feedback
function calculateTotal(items) {
    if (!items) return 0;
    return items.reduce((sum, item) => sum + item.price, 0);
}

// Respond to reviewer
// "Thanks for catching that! I've added a null check."
```

### Step 6: Approval and Merge

```bash
# Merge PR after approval
# GitHub: Click "Merge pull request"
# Or use GitHub CLI
gh pr merge --merge
```

## Review Size

### Small PRs (< 400 lines)

```javascript
// Good: Small, focused PR
function calculateTotal(items) {
    if (!items) return 0;
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

### Large PRs (> 1000 lines)

```javascript
// Bad: Large, hard to review
// Too many changes in one PR
// Break into smaller PRs
```

### Break Up Large PRs

```bash
# Break large PR into smaller ones
# PR 1: Add calculateTotal function
# PR 2: Add tests for calculateTotal
# PR 3: Update UI to use calculateTotal
```

## Review Turnaround Time

### Goal: Review Within 24 Hours

```javascript
// Good: Fast feedback
// Review within 24 hours
// Keeps momentum
```

### Blocked PRs Slow Down Team

```javascript
// Bad: Long delays
// PR sits for days
// Blocks other work
```

## Giving Feedback

### Be Kind and Constructive

```javascript
// Good: Constructive feedback
// "I think we could simplify this by using array methods. 
// What do you think about using reduce() instead of a for loop?"

// Bad: Harsh feedback
// "This is terrible code. Rewrite it."
```

### Explain the "Why"

```javascript
// Good: Explains why
// "I noticed you're using `var` instead of `const`. 
// Using `const` is better because it prevents reassignment 
// and makes the code more predictable."

// Bad: No explanation
// "Use const instead of var."
```

### Suggest Alternatives

```javascript
// Good: Suggests alternatives
// "Instead of using a for loop, we could use map() 
// which is more functional and easier to read."

// Example:
// Before:
const doubled = [];
for (let i = 0; i < numbers.length; i++) {
    doubled.push(numbers[i] * 2);
}

// After:
const doubled = numbers.map(n => n * 2);
```

### Ask Questions Instead of Demanding

```javascript
// Good: Asks questions
// "Have you considered using TypeScript here? 
// It might help catch type errors at compile time."

// Bad: Demands
// "You must use TypeScript here."
```

### Praise Good Work

```javascript
// Good: Praises good work
// "Great job on the tests! They're comprehensive 
// and easy to understand."
```

## Review Comment Types

### Blocking Comments

```javascript
// Must fix before merge
// "This function has a security vulnerability. 
// Please use parameterized queries instead of string interpolation."
function getUser(id) {
    const query = `SELECT * FROM users WHERE id = ${id}`;
    return db.query(query);
}
```

### Non-Blocking Comments

```javascript
// Nice-to-have, not required
// "Consider adding a comment explaining why we're using 
// this particular algorithm."
function calculateTotal(items) {
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

### Question Comments

```javascript
// Asking for clarification
// "I'm not sure why we're using this approach. 
// Could you explain the reasoning?"
function processOrder(order) {
    // Complex logic
}
```

### Praise Comments

```javascript
// Recognizing good work
// "Great job on the error handling! 
// It's comprehensive and user-friendly."
function processOrder(order) {
    try {
        // Process order
    } catch (error) {
        // Handle error gracefully
    }
}
```

## Receiving Feedback

### Don't Take It Personally

```javascript
// It's about the code, not you
// Feedback helps improve code quality
```

### Ask for Clarification

```javascript
// If unclear, ask for clarification
// "Could you explain why you think we should use 
// this approach? I'm not sure I understand."
```

### Discuss Disagreements Respectfully

```javascript
// Good: Respectful discussion
// "I see your point, but I think this approach is 
// better because... What do you think?"

// Bad: Argumentative
// "You're wrong. This is the right way."
```

### Learn from Feedback

```javascript
// Use feedback to improve
// "Thanks for the feedback! I'll keep that in mind 
// for future PRs."
```

## Review Checklist

### Code Works as Intended

```javascript
// [ ] Code works as intended
function calculateTotal(items) {
    if (!items) return 0;
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

### Tests Added/Updated

```javascript
// [ ] Tests added/updated
describe('calculateTotal', () => {
    it('calculates total correctly', () => {
        const items = [{ price: 10 }, { price: 20 }];
        expect(calculateTotal(items)).toBe(30);
    });
});
```

### Edge Cases Handled

```javascript
// [ ] Edge cases handled
function calculateTotal(items) {
    if (!items || items.length === 0) return 0;
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

### Error Handling Present

```javascript
// [ ] Error handling present
function processOrder(order) {
    try {
        // Process order
    } catch (error) {
        // Handle error
        console.error('Error processing order:', error);
        throw new Error('Failed to process order');
    }
}
```

### No Obvious Bugs

```javascript
// [ ] No obvious bugs
function calculateTotal(items) {
    if (!items || items.length === 0) return 0;
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

### Readable and Maintainable

```javascript
// [ ] Readable and maintainable
function calculateTotal(items) {
    if (!items || items.length === 0) return 0;
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

### Follows Style Guide

```javascript
// [ ] Follows style guide
// ESLint rules
// Prettier formatting
```

### No Security Issues

```javascript
// [ ] No security issues
function getUser(id) {
    const query = 'SELECT * FROM users WHERE id = $1';
    return db.query(query, [id]);
}
```

### Documentation Updated

```javascript
// [ ] Documentation updated
/**
 * Calculate the total price of items.
 * @param {Array} items - Array of items with price property
 * @returns {number} Total price
 */
function calculateTotal(items) {
    if (!items || items.length === 0) return 0;
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

## Automated Checks

### Linting

```json
// package.json
{
  "scripts": {
    "lint": "eslint src/",
    "lint:fix": "eslint src/ --fix"
  }
}
```

```javascript
// .eslintrc.js
module.exports = {
    extends: ['eslint:recommended'],
    rules: {
        'no-console': 'warn',
        'no-unused-vars': 'error'
    }
};
```

### Formatting

```json
// package.json
{
  "scripts": {
    "format": "prettier --write src/"
  }
}
```

```javascript
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2
}
```

### Tests

```json
// package.json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  }
}
```

### Type Checking

```json
// package.json
{
  "scripts": {
    "type-check": "tsc --noEmit"
  }
}
```

### Security Scanning

```json
// package.json
{
  "scripts": {
    "security": "npm audit",
    "security:fix": "npm audit fix"
  }
}
```

## Review Tools

### GitHub Pull Requests

```bash
# Create PR
gh pr create --title "Add new feature" --body "Description"

# View PR
gh pr view

# Merge PR
gh pr merge --merge
```

### GitLab Merge Requests

```bash
# Create MR
git push -o merge_request.create

# View MR
gitlab mr show

# Merge MR
gitlab mr merge
```

### Bitbucket Pull Requests

```bash
# Create PR
bitbucket pr create --title "Add new feature" --description "Description"

# View PR
bitbucket pr view

# Merge PR
bitbucket pr merge
```

## Review Best Practices

### Review Promptly

```javascript
// Don't block teammates
// Review within 24 hours
```

### Focus on Important Issues

```javascript
// Don't nitpick
// Focus on important issues
```

### Automate What Can Be Automated

```javascript
// Use linters, formatters, tests
// Don't manually check style
```

### Set Time Limits

```javascript
// Limit review time
// 30 minutes per review
```

### Synchronous Discussion for Complex Topics

```javascript
// Discuss complex topics synchronously
// Video call, pair programming
```

## Common Review Mistakes

### Rubber-Stamping

```javascript
// Bad: Approving without reading
// Don't just click "Approve"
// Actually review the code
```

### Nitpicking

```javascript
// Bad: Focusing on trivial issues
// Don't nitpick style issues
// Let linters handle those
```

### Not Explaining Feedback

```javascript
// Bad: Not explaining feedback
// Always explain why
// Help the author understand
```

### Long Delays

```javascript
// Bad: Long delays
// Review promptly
// Don't block teammates
```

## Self-Review

### Review Your Own Code

```javascript
// Before submitting PR
// Review your own code
// Catch obvious issues
```

### Self-Review Checklist

```javascript
// Self-review checklist
// [ ] Code works as intended
// [ ] Tests added
// [ ] Edge cases handled
// [ ] Error handling present
// [ ] No obvious bugs
// [ ] Readable and maintainable
// [ ] Follows style guide
// [ ] No security issues
// [ ] Documentation updated
```

## Pair Programming as Review

### Real-Time Review

```javascript
// Pair programming
// Real-time review during coding
// Faster feedback
```

### Great for Complex or Risky Changes

```javascript
// Use pair programming for
// Complex features
// Risky changes
// Critical bugs
```

## Review Metrics

### Review Turnaround Time

```javascript
// Measure review turnaround time
// Goal: < 24 hours
```

### Review Thoroughness

```javascript
// Measure review thoroughness
// Comments per PR
// Blocking comments
// Non-blocking comments
```

### Defect Escape Rate

```javascript
// Measure defects in production
// Bugs found after merge
// Goal: < 5% of PRs
```

## Building Review Culture

### Everyone Reviews

```javascript
// Not just seniors
// Everyone reviews
// Juniors, seniors, leads
```

### Code Review Guidelines Document

```markdown
# Code Review Guidelines

## Review Process
1. Create PR
2. Automated checks pass
3. Assign reviewers
4. Reviewers provide feedback
5. Developer addresses feedback
6. Approval and merge

## Review Checklist
- [ ] Code works as intended
- [ ] Tests added/updated
- [ ] Edge cases handled
- [ ] Error handling present
- [ ] No obvious bugs
- [ ] Readable and maintainable
- [ ] Follows style guide
- [ ] No security issues
- [ ] Documentation updated

## Feedback Guidelines
- Be kind and constructive
- Explain the "why"
- Suggest alternatives
- Ask questions instead of demanding
- Praise good work
```

### Regular Feedback on Review Quality

```javascript
// Give feedback on reviews
// Help reviewers improve
```

### Celebrate Good Reviews

```javascript
// Celebrate good reviews
// Recognize thorough reviews
```

## Remote Team Reviews

### Async-First

```javascript
// Written feedback
// Not real-time
```

### Video Call for Complex Discussions

```javascript
// Use video call for
// Complex topics
// Disagreements
```

### Timezone-Aware

```javascript
// Don't block overnight
// Be considerate of timezones
```

## Real Examples

### Good Review Comments

```javascript
// Good: Constructive feedback
// "I noticed that this function doesn't handle the case where `items` is null. 
// Consider adding a null check or using optional chaining."

// Good: Explains why
// "I noticed you're using `var` instead of `const`. 
// Using `const` is better because it prevents reassignment 
// and makes the code more predictable."

// Good: Suggests alternatives
// "Instead of using a for loop, we could use map() 
// which is more functional and easier to read."

// Good: Praises good work
// "Great job on the tests! They're comprehensive 
// and easy to understand."
```

### Bad Review Comments

```javascript
// Bad: Harsh feedback
// "This is terrible code. Rewrite it."

// Bad: No explanation
// "Use const instead of var."

// Bad: Demands
// "You must use TypeScript here."

// Bad: Argumentative
// "You're wrong. This is the right way."
```

## Summary Checklist

### Before Reviewing

- [ ] Understand the context
- [ ] Read the PR description
- [ ] Review the code
- [ ] Run the code locally
- [ ] Check the tests

### During Review

- [ ] Focus on important issues
- [ ] Be kind and constructive
- [ ] Explain the "why"
- [ ] Suggest alternatives
- [ ] Ask questions instead of demanding

### After Review

- [ ] Respond to feedback
- [ ] Make requested changes
- [ ] Update documentation
- [ ] Re-request review
- [ ] Merge when approved
```

---

## Quick Start

### Code Review Checklist

```markdown
# Code Review Checklist

## Functionality
- [ ] Code works as intended
- [ ] Edge cases handled
- [ ] Error handling present

## Code Quality
- [ ] Follows style guide
- [ ] No code duplication
- [ ] Proper naming conventions

## Testing
- [ ] Tests included
- [ ] Tests pass
- [ ] Coverage adequate

## Documentation
- [ ] Comments where needed
- [ ] README updated if needed
- [ ] API docs updated
```

### Review Template

```markdown
## Review Comments

### Critical Issues
- [ ] Issue 1: [Description]
- [ ] Issue 2: [Description]

### Suggestions
- [ ] Suggestion 1: [Description]
- [ ] Suggestion 2: [Description]

### Questions
- [ ] Question 1: [Description]
```

---

## Production Checklist

- [ ] **Review Process**: Clear review process defined
- [ ] **Reviewers**: Appropriate reviewers assigned
- [ ] **Timeline**: Reasonable review timeline (24-48 hours)
- [ ] **Automation**: Automated checks (linting, tests) in CI
- [ ] **Guidelines**: Code review guidelines documented
- [ ] **Culture**: Positive, constructive review culture
- [ ] **Training**: Team trained on review practices
- [ ] **Metrics**: Track review metrics (time, approval rate)
- [ ] **Feedback**: Regular feedback on review quality
- [ ] **Tools**: Appropriate review tools configured
- [ ] **Documentation**: Review decisions documented
- [ ] **Escalation**: Process for resolving disagreements

---

## Anti-patterns

### ❌ Don't: Personal Attacks

```markdown
# ❌ Bad - Personal
"This code is terrible. You should know better."
```

```markdown
# ✅ Good - Constructive
"Consider using a more descriptive variable name here. 
'data' could be 'userProfile' to be clearer."
```

### ❌ Don't: Nitpicking

```markdown
# ❌ Bad - Minor style issue
"Add a space after the comma"
```

```markdown
# ✅ Good - Focus on important issues
"Consider extracting this logic into a separate function 
for better testability and reusability."
```

### ❌ Don't: Blocking Without Explanation

```markdown
# ❌ Bad - No context
"Needs work"
```

```markdown
# ✅ Good - Clear feedback
"This function is doing too much. Consider splitting into:
1. Data fetching
2. Data transformation
3. Data validation

This will improve testability."
```

---

## Integration Points

- **Code Review** (`01-foundations/code-review/`) - Review best practices
- **Git Workflow** (`01-foundations/git-workflow/`) - PR workflow
- **Onboarding** (`27-team-collaboration/onboarding/`) - Review for new members

---

## Further Reading

- [Google Code Review Guide](https://google.github.io/eng-practices/review/)
- [Code Review Best Practices](https://github.com/google/eng-practices/blob/master/review/README.md)
