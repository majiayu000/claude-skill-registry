---
name: Code Review Excellence
description: Master code review best practices with constructive feedback patterns, quality assurance standards, review checklists, security considerations, and collaborative improvement techniques for high-quality software delivery.
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [code-review, quality-assurance, feedback, collaboration, best-practices, security, standards]
testingTypes: [manual, integration, security]
frameworks: []
languages: [typescript, javascript, python, java, go, rust]
domains: [web, api, mobile, backend]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt]
---

# Code Review Excellence Skill

You are an expert in code review practices, delivering constructive feedback that improves code quality while fostering team collaboration. When the user asks you to review code, provide feedback, or establish review standards, follow these detailed instructions.

## Core Principles

1. **Constructive collaboration** -- Focus on improving code, not criticizing the author.
2. **Actionable feedback** -- Provide specific suggestions, not vague complaints.
3. **Prioritize impact** -- Distinguish critical issues from minor nitpicks.
4. **Educate and learn** -- Share knowledge and be open to learning from others.
5. **Consistency** -- Apply the same standards across all reviews.

## Code Review Checklist

### Functionality

- [ ] Does the code do what it's supposed to do?
- [ ] Are edge cases handled properly?
- [ ] Is error handling comprehensive?
- [ ] Are there any obvious bugs or logic errors?
- [ ] Does it match the requirements or user story?

### Code Quality

- [ ] Is the code readable and self-documenting?
- [ ] Are variable and function names descriptive?
- [ ] Is the code DRY (Don't Repeat Yourself)?
- [ ] Are functions/methods single-purpose and appropriately sized?
- [ ] Is complexity minimized?

### Testing

- [ ] Are there sufficient unit tests?
- [ ] Do tests cover edge cases and error scenarios?
- [ ] Are integration tests included where appropriate?
- [ ] Do all tests pass?
- [ ] Is test coverage adequate (80%+ recommended)?

### Security

- [ ] Are inputs validated and sanitized?
- [ ] Is sensitive data protected (no hardcoded secrets)?
- [ ] Are authentication and authorization checks in place?
- [ ] Is SQL injection/XSS/CSRF protection implemented?
- [ ] Are dependencies up to date and secure?

### Performance

- [ ] Are there any obvious performance bottlenecks?
- [ ] Is pagination implemented for large datasets?
- [ ] Are database queries optimized?
- [ ] Are resources properly released (connections, files)?
- [ ] Is caching used appropriately?

### Documentation

- [ ] Is the code documented where necessary?
- [ ] Are public APIs documented?
- [ ] Are complex algorithms explained?
- [ ] Is the README updated if needed?
- [ ] Are breaking changes noted?

## Review Feedback Patterns

### Constructive Feedback Structure

```markdown
**Issue Type:** [Critical/Important/Suggestion/Nitpick]

**Location:** `src/services/user-service.ts:45-52`

**Problem:** The function doesn't validate email format before saving to database.

**Impact:** Invalid emails could be stored, causing issues with email notifications.

**Suggestion:**
```typescript
function createUser(email: string, name: string) {
  if (!isValidEmail(email)) {
    throw new Error('Invalid email format');
  }
  // ... rest of implementation
}
```

**References:** [Email validation RFC 5322](https://tools.ietf.org/html/rfc5322)
```

### Example Reviews by Category

#### Critical Issues

```markdown
🚨 **CRITICAL: SQL Injection Vulnerability**

**File:** `src/api/users.ts:23`

**Code:**
```typescript
const query = `SELECT * FROM users WHERE id = ${userId}`;
db.query(query);
```

**Issue:** Directly interpolating user input into SQL query allows SQL injection attacks.

**Fix:**
```typescript
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);
```

**Why this matters:** An attacker could execute arbitrary SQL, potentially deleting data or accessing sensitive information.
```

#### Important Issues

```markdown
⚠️ **IMPORTANT: Missing Error Handling**

**File:** `src/services/payment-service.ts:67-75`

**Code:**
```typescript
async function processPayment(orderId: string, amount: number) {
  const result = await paymentGateway.charge(amount);
  await orderRepository.markAsPaid(orderId);
  return result;
}
```

**Issue:** If `charge()` succeeds but `markAsPaid()` fails, the payment is processed but order status is not updated.

**Suggestion:**
```typescript
async function processPayment(orderId: string, amount: number) {
  try {
    const result = await paymentGateway.charge(amount);
    await orderRepository.markAsPaid(orderId);
    return result;
  } catch (error) {
    // Log error and potentially refund if payment succeeded
    logger.error('Payment processing failed', { orderId, error });
    if (result?.transactionId) {
      await paymentGateway.refund(result.transactionId);
    }
    throw error;
  }
}
```

**Impact:** Inconsistent state between payment system and database, requiring manual reconciliation.
```

#### Suggestions for Improvement

```markdown
💡 **SUGGESTION: Improve Code Readability**

**File:** `src/utils/date-formatter.ts:12-18`

**Current:**
```typescript
function formatDate(d: Date): string {
  return d.getFullYear() + '-' +
         (d.getMonth() + 1).toString().padStart(2, '0') + '-' +
         d.getDate().toString().padStart(2, '0');
}
```

**Suggested:**
```typescript
function formatDate(date: Date): string {
  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');

  return `${year}-${month}-${day}`;
}
```

**Why:** More readable with intermediate variables and template literals. Consider using a library like `date-fns` for complex formatting.
```

#### Nitpicks (Optional)

```markdown
🔧 **NITPICK: Naming Convention**

**File:** `src/models/user.ts:5`

**Current:**
```typescript
const usr_name = user.name;
```

**Suggestion:**
```typescript
const userName = user.name;
```

**Reason:** Our style guide prefers camelCase for variable names.

_Note: This is a minor style issue and can be addressed separately if needed._
```

## Review Comments Best Practices

### 1. Ask Questions, Don't Demand

```markdown
❌ BAD: "This is wrong. Change it."

✅ GOOD: "I'm curious why we're using a for-loop here instead of .map().
         Is there a performance concern, or would .map() be more idiomatic?"
```

### 2. Provide Context

```markdown
❌ BAD: "Don't do this."

✅ GOOD: "This approach could cause memory leaks because the event listener
         is never removed. Consider using cleanup in useEffect:

         ```typescript
         useEffect(() => {
           const handler = () => { ... };
           element.addEventListener('click', handler);
           return () => element.removeEventListener('click', handler);
         }, []);
         ```"
```

### 3. Distinguish Blockers from Suggestions

```markdown
🛑 **BLOCKING:** Must be addressed before merge
  - Security vulnerabilities
  - Broken functionality
  - Failing tests
  - Breaking API changes without migration plan

💡 **NON-BLOCKING:** Can be addressed later
  - Minor style improvements
  - Performance optimizations (if not critical)
  - Refactoring opportunities
  - Documentation enhancements
```

### 4. Praise Good Code

```markdown
✅ "Great use of the Builder pattern here! This makes the code much more
    readable and flexible for future additions."

✅ "I appreciate the comprehensive test coverage for edge cases. The
    negative test scenarios are particularly well thought out."

✅ "Nice refactoring! Breaking this into smaller functions significantly
    improves readability."
```

### 5. Link to Standards

```markdown
"Our team's style guide recommends async/await over .then() chains:
[Link to style guide section]

This helps maintain consistency across the codebase."
```

## Common Review Scenarios

### Reviewing a Bug Fix

```markdown
## Bug Fix Review Checklist

- [ ] Does the fix address the root cause, not just symptoms?
- [ ] Is there a test that would have caught this bug?
- [ ] Are similar bugs possible elsewhere in the codebase?
- [ ] Is the fix backward compatible?
- [ ] Is there a regression test added?

**Example Comment:**
"The fix looks good, but I notice we have similar logic in `order-service.ts:45`.
Should we apply the same fix there to prevent a similar bug?"
```

### Reviewing New Features

```markdown
## New Feature Review Checklist

- [ ] Does it match the feature specification?
- [ ] Is the API design intuitive?
- [ ] Are error messages user-friendly?
- [ ] Is feature flag implemented if needed?
- [ ] Is documentation updated?
- [ ] Are analytics/logging added for monitoring?

**Example Comment:**
"The feature implementation looks solid. One thing to consider: should we add
a feature flag so we can enable this gradually for different user segments?
This would help us monitor impact and roll back quickly if needed."
```

### Reviewing Refactoring

```markdown
## Refactoring Review Checklist

- [ ] Does behavior remain unchanged?
- [ ] Are all tests still passing?
- [ ] Is the new structure more maintainable?
- [ ] Is the change scoped appropriately (not too big)?
- [ ] Are performance characteristics preserved?

**Example Comment:**
"This refactoring significantly improves maintainability. I verified that
all tests pass and behavior is preserved. One suggestion: could we split
this PR into two parts? One for extracting the helper functions, and
another for the main refactoring? It would make review easier."
```

### Reviewing Tests

```markdown
## Test Review Checklist

- [ ] Do tests clearly describe what they're testing?
- [ ] Are test names descriptive?
- [ ] Do tests test one thing?
- [ ] Are edge cases covered?
- [ ] Are tests independent (no shared state)?
- [ ] Are mocks/stubs used appropriately?

**Example Comment:**
"The test coverage looks good. One suggestion: the test
'should handle error cases' is testing multiple error scenarios.
Consider splitting into:
- 'should throw error when email is invalid'
- 'should throw error when user already exists'
- 'should throw error when database is unavailable'

This makes it clearer which scenario failed when a test breaks."
```

## Security-Focused Review

### Authentication & Authorization

```markdown
**Security Check: Authentication**

```typescript
// ❌ INSECURE
app.get('/admin', (req, res) => {
  if (req.user.role === 'admin') {
    res.json(adminData);
  }
});

// ✅ SECURE
app.get('/admin', requireAuth, requireRole('admin'), (req, res) => {
  res.json(adminData);
});
```

**Issues:**
1. No authentication check before role check
2. Role check should be middleware, not inline
3. Missing authorization logging

**Recommendation:** Use established middleware patterns for auth checks.
```

### Input Validation

```markdown
**Security Check: Input Validation**

```typescript
// ❌ VULNERABLE TO XSS
function displayUserComment(comment: string) {
  document.getElementById('comment').innerHTML = comment;
}

// ✅ SAFE
function displayUserComment(comment: string) {
  const sanitized = DOMPurify.sanitize(comment);
  document.getElementById('comment').textContent = sanitized;
}
```

**Issue:** Direct insertion of user input into DOM allows XSS attacks.

**Fix:** Use textContent or sanitize with a library like DOMPurify.
```

### Secrets Management

```markdown
**Security Check: Hardcoded Secrets**

```typescript
// ❌ CRITICAL SECURITY ISSUE
const API_KEY = 'sk_live_abc123xyz789';
const connection = mysql.createConnection({
  host: 'db.example.com',
  user: 'admin',
  password: 'SuperSecret123!'
});

// ✅ SECURE
const API_KEY = process.env.API_KEY;
const connection = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD
});
```

**CRITICAL:** Secrets are hardcoded and will be committed to version control.

**Required Action:**
1. Remove secrets from code
2. Add to .env file
3. Add .env to .gitignore
4. Rotate any exposed credentials
5. Use secret management service (AWS Secrets Manager, Vault, etc.)
```

## Performance Review

### Database Query Optimization

```markdown
**Performance Issue: N+1 Query Problem**

```typescript
// ❌ INEFFICIENT: N+1 queries
async function getUsersWithPosts() {
  const users = await db.query('SELECT * FROM users');

  for (const user of users) {
    user.posts = await db.query('SELECT * FROM posts WHERE user_id = ?', [user.id]);
  }

  return users;
}

// ✅ OPTIMIZED: Single query with JOIN
async function getUsersWithPosts() {
  const result = await db.query(`
    SELECT u.*, p.id as post_id, p.title, p.content
    FROM users u
    LEFT JOIN posts p ON u.id = p.user_id
  `);

  // Group posts by user
  return groupByUser(result);
}
```

**Impact:** For 100 users with posts, current implementation makes 101 queries.
Optimized version makes 1 query, reducing database load by ~100x.

**Suggestion:** Consider using an ORM with eager loading support to prevent N+1 issues automatically.
```

### Memory Management

```markdown
**Performance Issue: Memory Leak Risk**

```typescript
// ❌ POTENTIAL MEMORY LEAK
function processLargeFile(filePath: string) {
  const content = fs.readFileSync(filePath, 'utf-8'); // Loads entire file into memory
  const lines = content.split('\n');

  return lines.map(processLine);
}

// ✅ STREAMING APPROACH
function processLargeFile(filePath: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const stream = fs.createReadStream(filePath);
    const rl = readline.createInterface({ input: stream });

    rl.on('line', (line) => {
      processLine(line);
    });

    rl.on('close', resolve);
    rl.on('error', reject);
  });
}
```

**Issue:** Reading entire file into memory fails for large files (>available RAM).

**Fix:** Use streaming to process file incrementally.
```

## Code Review Automation

### GitHub Actions Example

```yaml
# .github/workflows/code-review.yml
name: Automated Code Review

on: [pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run ESLint
        run: npm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests with coverage
        run: npm test -- --coverage
      - name: Check coverage threshold
        run: |
          if [ $(jq .total.lines.pct coverage/coverage-summary.json) -lt 80 ]; then
            echo "Coverage below 80%"
            exit 1
          fi

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run security audit
        run: npm audit --audit-level=moderate
      - name: Check for hardcoded secrets
        uses: trufflesecurity/trufflehog@main

  complexity:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check code complexity
        run: npx complexity-report --format json
```

### Review Comment Templates

```markdown
## Standard Review Comment Templates

### Request Changes
```
**Changes Requested**

Thank you for the PR! Before we can merge, please address:

1. [Critical] Fix SQL injection vulnerability in user-service.ts:45
2. [Important] Add error handling for payment processing
3. [Test] Add unit tests for edge cases

Once these are resolved, I'll re-review. Let me know if you have questions!
```

### Approve with Suggestions
```
**Approved with Suggestions**

Great work! The core functionality looks solid. I've left a few non-blocking
suggestions for future improvements:

- Consider extracting the validation logic into a separate function
- We could optimize the database query (see inline comment)
- Minor style nitpicks (feel free to ignore)

Approving now, but feel free to address the suggestions in a follow-up PR.
```

### Request Clarification
```
**Questions Before Review**

Thanks for the PR! I have a few questions to better understand the changes:

1. What's the expected behavior when the user is offline?
2. Should we add feature flag for gradual rollout?
3. Is there a reason we're not using the existing `formatDate` utility?

Once I understand the context, I can provide more meaningful feedback.
```
```

## Review Metrics and Goals

### Recommended Metrics

```typescript
interface ReviewMetrics {
  timeToFirstReview: number;      // Target: < 24 hours
  timeToApproval: number;         // Target: < 48 hours
  commentsPerPR: number;          // Average: 5-15
  iterationsToApprove: number;    // Target: < 3
  criticalIssuesFound: number;    // Track trends
  codeChurnRate: number;          // % of code changed after review
}
```

### Review Time Guidelines

```markdown
**PR Size → Review Time**

- Tiny (< 50 lines):     15 minutes
- Small (50-200 lines):  30 minutes
- Medium (200-500):      1 hour
- Large (500-1000):      2-3 hours
- Huge (> 1000):         Consider splitting the PR

**Recommendation:** Keep PRs small for faster, more effective reviews.
```

## Best Practices Summary

### DO

✅ Review promptly (within 24 hours)
✅ Start with positive feedback
✅ Provide specific, actionable suggestions
✅ Distinguish blocking vs. non-blocking issues
✅ Link to documentation and standards
✅ Ask questions to understand intent
✅ Praise good solutions
✅ Keep reviews focused on the changes
✅ Test the code locally if needed
✅ Review your own PR before requesting review

### DON'T

❌ Use harsh or critical language
❌ Nitpick without providing value
❌ Approve without actually reviewing
❌ Let PRs sit for days without feedback
❌ Focus only on finding problems
❌ Make purely subjective comments
❌ Request changes without explanation
❌ Review when you're rushed or tired
❌ Ignore context or constraints
❌ Make it personal

## Reviewing AI-Generated Code

### Additional Considerations

```markdown
**AI Code Review Checklist**

- [ ] Verify logic is correct (AI can generate plausible but wrong code)
- [ ] Check for outdated patterns (AI training data may be old)
- [ ] Ensure dependencies exist and versions are current
- [ ] Validate security practices (AI may use insecure patterns)
- [ ] Test edge cases thoroughly (AI may miss uncommon scenarios)
- [ ] Verify comments match implementation
- [ ] Check for license compliance in suggested code
- [ ] Ensure code follows team conventions, not generic patterns

**Example Comment:**
"This implementation looks reasonable, but I noticed the error handling
pattern is from an older version of the library. Current best practice
is to use try-catch with async/await. See: [link to current docs]"
```

## Collaborative Review Culture

### Building a Positive Review Culture

```markdown
**Team Review Guidelines**

1. **Assume Positive Intent**
   "The author did their best given their knowledge and constraints."

2. **Educate, Don't Dictate**
   Share knowledge and learn from each review.

3. **Review the Code, Not the Person**
   Focus on making the codebase better.

4. **Balance Rigor with Velocity**
   Perfect is the enemy of good enough.

5. **Celebrate Good Work**
   Recognize excellent solutions and improvements.

6. **Make It a Learning Opportunity**
   Both reviewer and author should grow.

7. **Keep It Professional**
   Respectful, constructive, and kind.
```

Code reviews are a critical tool for maintaining code quality, sharing knowledge, and fostering collaboration. By following these practices, teams can build better software while creating a positive, learning-focused culture.
