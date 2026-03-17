---
name: code-review
description: Automated code review analyzing security, performance, maintainability, and test coverage. Activated during code reviews or when conducting analysis.
allowed-tools: ['Read', 'Grep', 'Glob']
---

# AI-Powered Code Review Engine

This skill provides comprehensive automated code review with focus on security, performance, maintainability, and test coverage.

## 🔍 Review Categories

### 1. Security Analysis

**Check for**:
- Authentication/authorization vulnerabilities
- SQL injection risks
- XSS (Cross-Site Scripting) vulnerabilities
- Hardcoded secrets or API keys
- Insecure dependencies
- CSRF protection
- Input validation gaps
- Sensitive data exposure

**Common Vulnerabilities**:

```typescript
// ❌ SQL Injection risk
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ Use parameterized queries
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);

// ❌ XSS vulnerability
element.innerHTML = userInput;

// ✅ Sanitize input
element.textContent = userInput;
// or use a sanitization library

// ❌ Hardcoded secret
const API_KEY = "sk_live_abc123xyz789";

// ✅ Use environment variables
const API_KEY = process.env.API_KEY;
```

### 2. Performance Analysis

**Check for**:
- N+1 query problems
- Inefficient algorithms (O(n²) when O(n) possible)
- Unnecessary re-renders (React)
- Memory leaks
- Blocking operations
- Large bundle sizes
- Unoptimized images
- Missing caching opportunities

**Common Issues**:

```typescript
// ❌ N+1 query problem
for (const user of users) {
  const posts = await db.query('SELECT * FROM posts WHERE user_id = ?', [user.id]);
}

// ✅ Single query with JOIN
const usersWithPosts = await db.query(`
  SELECT users.*, posts.*
  FROM users
  LEFT JOIN posts ON users.id = posts.user_id
`);

// ❌ Unnecessary re-renders
function Component({ data }) {
  const processedData = expensiveOperation(data); // Runs every render
  return <div>{processedData}</div>;
}

// ✅ Memoization
function Component({ data }) {
  const processedData = useMemo(() => expensiveOperation(data), [data]);
  return <div>{processedData}</div>;
}
```

### 3. Maintainability Analysis

**Check for**:
- Code complexity (cyclomatic complexity)
- Long functions (> 50 lines)
- Deeply nested code (> 3 levels)
- Duplicate code
- Unclear variable names
- Missing documentation
- Inconsistent coding style
- God objects/classes

**Metrics**:

```typescript
// ❌ High complexity (complexity: 10+)
function processOrder(order) {
  if (order.type === 'standard') {
    if (order.amount > 100) {
      if (order.customer.isPremium) {
        if (order.items.length > 5) {
          // Deep nesting continues...
        }
      }
    }
  }
}

// ✅ Refactored (complexity: 3)
function processOrder(order) {
  if (!isProcessable(order)) {
    return handleInvalidOrder(order);
  }

  const discount = calculateDiscount(order);
  return applyDiscount(order, discount);
}

function isProcessable(order) {
  return order.type === 'standard' && order.amount > 0;
}
```

### 4. Test Coverage Analysis

**Check for**:
- Overall coverage percentage
- Uncovered critical paths
- Missing edge case tests
- Flaky tests
- Slow tests
- Test quality (assertions vs test length)

**Coverage Goals**:
- Critical code (auth, payment): **95%+**
- Business logic: **80%+**
- Utilities: **70%+**
- UI components: **60%+**

## 📊 Review Output Format

```
🔍 Code Analysis Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Performance
✅ 3 optimization opportunities found
  - UsersList component: Recommend React.memo (line 45)
  - API call results: Add caching (line 128)
  - Array operations: Parallelize with Promise.all (line 201)

🔒 Security
✅ No critical issues detected
⚠️  1 warning
  - Input validation: Add sanitization for user-generated content (line 89)

🛠️ Maintainability
⚠️ 2 method extractions recommended
  - validateUserInput: Complexity 15 → recommend <10 (line 156)
  - processPaymentData: Length 120 lines → recommend <50 (line 234)

✅ Test Coverage
📊 85% (target: 90%)
  - Add 3 error handling test cases
    - Test invalid email format (auth.test.ts)
    - Test network timeout (api.test.ts)
    - Test concurrent updates (user.test.ts)
  - Add 2 edge case tests
    - Test empty array input (utils.test.ts)
    - Test boundary values (validation.test.ts)

📚 Documentation
⚠️ 2 functions missing proper documentation
  - calculateTotalPrice(): Add JSDoc (line 45)
  - formatUserData(): Missing parameter descriptions (line 123)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Priority: 🔴 1 Critical, 🟡 5 High, 🟢 8 Medium
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 🎯 Automated Checks

Execute during review:

1. **Lint errors** - Check for code style violations
2. **Type safety** - Verify TypeScript strict mode compliance
3. **Test execution** - Ensure all tests pass
4. **Code coverage** - Check coverage thresholds
5. **Security scan** - Run security vulnerability checks
6. **Performance profiling** - Identify slow operations

```bash
# Automated checks script
pnpm run lint
pnpm tsc --noEmit
pnpm test -- --coverage
pnpm audit
```

## 💡 Suggestion Priority

### 🔴 Critical (Fix Immediately)
- Security vulnerabilities
- Data loss risks
- Production crashes
- Breaking changes without migration

### 🟡 High (Fix Before Merge)
- Performance issues (>100ms operations)
- Memory leaks
- Incorrect business logic
- Missing error handling

### 🟢 Medium (Address Soon)
- Code complexity issues
- Missing documentation
- Test coverage gaps
- Minor performance optimizations

### 🔵 Low (Nice to Have)
- Style improvements
- Variable naming suggestions
- Additional abstractions
- Micro-optimizations

## 📋 Review Checklist

### Code Quality
- [ ] Functions are small and focused (<50 lines)
- [ ] Variable names are clear and descriptive
- [ ] No magic numbers (use named constants)
- [ ] No commented-out code
- [ ] Consistent code style
- [ ] DRY principle followed

### Security
- [ ] Input validation implemented
- [ ] Output encoding/escaping applied
- [ ] Authentication checked for protected routes
- [ ] Authorization verified for sensitive operations
- [ ] No hardcoded credentials
- [ ] Dependencies are up-to-date and secure

### Performance
- [ ] No N+1 queries
- [ ] Efficient algorithms used
- [ ] Caching implemented where appropriate
- [ ] Database queries optimized
- [ ] Lazy loading considered
- [ ] No memory leaks

### Testing
- [ ] Unit tests written for new code
- [ ] Edge cases covered
- [ ] Integration tests for critical paths
- [ ] Tests are fast (<100ms each)
- [ ] Tests are deterministic (no flaky tests)
- [ ] Mocks used appropriately

### Documentation
- [ ] Public APIs documented
- [ ] Complex logic explained
- [ ] README updated if needed
- [ ] Examples provided
- [ ] Breaking changes noted

## 🚀 Review Workflow

### 1. Automated Analysis

```bash
# Run automated checks
pnpm run lint
pnpm tsc --noEmit
pnpm test -- --coverage
pnpm audit

# Generate coverage report
pnpm test -- --coverage --coverageReporters=html

# Check bundle size
pnpm run build
pnpm run analyze
```

### 2. Manual Review

Focus on:
- **Business logic correctness**
- **Architecture decisions**
- **API design**
- **User experience**
- **Edge cases**

### 3. Provide Feedback

Structure feedback:

```markdown
## Review Comments

### 🔴 Critical Issues
1. **Security**: SQL injection vulnerability in user search (line 45)
   - Use parameterized queries
   - Add input validation

### 🟡 High Priority
1. **Performance**: N+1 query in getUserPosts (line 123)
   - Recommend eager loading with JOIN
   - Estimated improvement: 80% faster

### 🟢 Suggestions
1. **Maintainability**: Extract validation logic (line 200)
   - Create separate validator function
   - Improves testability

### ✅ Positive Feedback
- Clean error handling implementation
- Good test coverage for new features
- Clear commit messages
```

## 🔍 Code Smell Detection

### Common Code Smells

**Long Method** (>50 lines):
```typescript
// Smell: Method too long
function processOrder(order) {
  // 100+ lines of code
}

// Fix: Extract smaller functions
function processOrder(order) {
  validateOrder(order);
  calculateTotal(order);
  applyDiscounts(order);
  finalizeOrder(order);
}
```

**Large Class** (>300 lines):
```typescript
// Smell: God object
class UserManager {
  // 500+ lines handling everything
}

// Fix: Split responsibilities
class UserAuthenticator { }
class UserProfileManager { }
class UserNotificationService { }
```

**Duplicate Code**:
```typescript
// Smell: Copy-paste code
function calculatePriceA(items) {
  let total = 0;
  for (const item of items) {
    total += item.price * item.quantity;
  }
  return total * 1.1; // tax
}

function calculatePriceB(products) {
  let sum = 0;
  for (const product of products) {
    sum += product.price * product.quantity;
  }
  return sum * 1.1; // tax
}

// Fix: Extract common logic
function calculateSubtotal(items) {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

function applyTax(amount) {
  return amount * 1.1;
}

function calculatePrice(items) {
  return applyTax(calculateSubtotal(items));
}
```

## 💎 Best Practices

1. **Be constructive** - Suggest improvements, don't just criticize
2. **Explain why** - Provide context for suggestions
3. **Prioritize issues** - Use severity levels
4. **Acknowledge good code** - Positive feedback is important
5. **Ask questions** - Seek clarification before assumptions
6. **Provide examples** - Show better alternatives
7. **Be timely** - Review promptly
8. **Be respectful** - Remember there's a person behind the code

## 🎓 Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Clean Code Principles](https://github.com/ryanmcdermott/clean-code-javascript)
- [React Performance Optimization](https://react.dev/learn/render-and-commit)
- [TypeScript Best Practices](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html)
