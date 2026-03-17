---
name: code-review-assistant
description: Conduct comprehensive code reviews identifying bugs, security issues, performance problems, code quality concerns, and best practice violations. Use when reviewing pull requests, examining code changes, evaluating new code, assessing code quality, or providing feedback on implementations. Analyzes code for correctness, security vulnerabilities, performance bottlenecks, maintainability issues, test coverage, documentation quality, and adherence to coding standards. Produces structured markdown reviews with categorized findings, severity ratings, specific examples, and actionable recommendations. Triggers when users ask to review code, check pull requests, evaluate implementations, find bugs, or assess code quality.
---

# Code Review Assistant

## Overview

Perform thorough, constructive code reviews that identify issues, suggest improvements, and ensure code quality, security, and maintainability.

## Review Categories

Examine code across these dimensions:

### 1. 🐛 Correctness & Bugs
- Logic errors
- Edge case handling
- Null/undefined checks
- Type mismatches
- Off-by-one errors
- Race conditions

### 2. 🔒 Security
- Input validation
- SQL injection risks
- XSS vulnerabilities
- Authentication/authorization flaws
- Sensitive data exposure
- Insecure dependencies

### 3. ⚡ Performance
- Algorithm efficiency (O(n) complexity)
- Memory leaks
- Unnecessary computations
- Database query optimization
- Caching opportunities

### 4. 🏗️ Code Quality
- Readability and clarity
- Naming conventions
- Code duplication (DRY principle)
- Function/method length
- Complexity (cyclomatic)
- SOLID principles

### 5. ✅ Testing
- Test coverage
- Edge case testing
- Unit vs integration tests
- Test quality and clarity
- Mock usage appropriateness

### 6. 📚 Documentation
- Code comments quality
- API documentation
- Function/method docstrings
- Complex logic explanation
- README updates

## Review Workflow

### Step 1: Understand Context

**Gather information:**
- What's the purpose of this code?
- What problem does it solve?
- What's the scope of changes?
- Are there related files to consider?

**For PRs:**
```bash
# View PR diff
gh pr diff <PR-NUMBER>

# View PR description
gh pr view <PR-NUMBER>

# See changed files
git diff --name-only main..HEAD
```

### Step 2: Read the Code

**First pass - high level:**
- Overall structure and organization
- Naming consistency
- Code patterns used
- Separation of concerns

**Second pass - detailed:**
- Line-by-line logic verification
- Edge cases and error handling
- Performance considerations
- Security implications

### Step 3: Identify Issues

Categorize findings by severity:

**🔴 Critical:** Must fix before merge
- Security vulnerabilities
- Data loss risks
- System crashes
- Breaking changes

**🟡 Important:** Should fix before merge
- Logic bugs
- Performance issues
- Poor error handling
- Missing tests for critical paths

**🔵 Minor:** Nice to have
- Code style inconsistencies
- Missing comments
- Minor optimizations
- Naming improvements

**💡 Suggestion:** Optional improvements
- Refactoring opportunities
- Alternative approaches
- Future considerations

### Step 4: Provide Feedback

Structure feedback constructively:

**For each issue:**
1. **Location:** File and line number
2. **Issue:** What's wrong
3. **Impact:** Why it matters
4. **Recommendation:** How to fix
5. **Example:** Code suggestion if helpful

**Tone guidelines:**
- Be specific and objective
- Focus on code, not the person
- Explain the "why" behind suggestions
- Acknowledge good practices
- Ask questions for clarification when unsure

## Review Template

```markdown
# Code Review: [PR Title / Code Description]

## Summary
- **Files Reviewed:** X files, Y lines changed
- **Overall Assessment:** [Approve/Request Changes/Comment]
- **Critical Issues:** N
- **Important Issues:** M
- **Minor Issues:** K

---

## 🔴 Critical Issues

### Issue 1: [Title]
**Location:** `path/to/file.py:42`

**Problem:**
[Clear description of the issue]

**Impact:**
[Why this is critical - security, data loss, crashes, etc.]

**Recommendation:**
[Specific fix needed]

**Example:**
```python
# Current (problematic)
user_input = request.GET['id']
query = f"SELECT * FROM users WHERE id = {user_input}"

# Suggested (fixed)
user_input = request.GET.get('id')
if user_input and user_input.isdigit():
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_input,))
```

---

## 🟡 Important Issues

### Issue 2: [Title]
[Same structure as above]

---

## 🔵 Minor Issues

### Issue 3: [Title]
[Shorter format acceptable for minor issues]

---

## 💡 Suggestions

- [Optional improvement 1]
- [Optional improvement 2]

---

## ✅ Positive Observations

- [Good practice 1]
- [Well-implemented feature]

---

## Questions for Author

- [Clarifying question about design decision]
- [Question about intended behavior]

---

## Recommendations

1. Fix all critical issues before merge
2. Address important issues or provide justification
3. Consider minor improvements where feasible
4. Add tests for edge cases X, Y, Z

**Overall:** [Approve with suggestions / Request changes / Needs discussion]
```

## Common Issues by Language

### Python
```python
# ❌ Mutable default argument
def append_to(element, to=[]):  # Bug: to persists across calls
    to.append(element)
    return to

# ✅ Correct
def append_to(element, to=None):
    if to is None:
        to = []
    to.append(element)
    return to

# ❌ Catching bare exceptions
try:
    risky_operation()
except:  # Too broad, masks errors
    pass

# ✅ Specific exception handling
try:
    risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise

# ❌ String concatenation in loops
result = ""
for item in items:
    result += str(item)  # Creates new string each iteration

# ✅ Use join
result = "".join(str(item) for item in items)
```

### JavaScript/TypeScript
```javascript
// ❌ == instead of ===
if (value == null) {  // Loose equality
    // ...
}

// ✅ Strict equality
if (value === null || value === undefined) {
    // ...
}

// ❌ Unhandled promise rejection
fetchData().then(data => process(data));

// ✅ Error handling
fetchData()
    .then(data => process(data))
    .catch(error => console.error('Error:', error));

// ❌ Variable shadowing
const name = "Global";
function greet() {
    const name = "Local";  // Shadows outer name
    console.log(name);
}

// ✅ Distinct names
const globalName = "Global";
function greet() {
    const userName = "User";
    console.log(userName);
}
```

### Java
```java
// ❌ Resource leak
public void readFile(String path) {
    FileInputStream fis = new FileInputStream(path);
    // ... use fis
    // Missing close(), leaks file handle
}

// ✅ Try-with-resources
public void readFile(String path) {
    try (FileInputStream fis = new FileInputStream(path)) {
        // ... use fis
    } // Automatically closed
}

// ❌ Using == for String comparison
if (str == "value") {  // Compares references
    // ...
}

// ✅ Use equals()
if ("value".equals(str)) {  // Compares content, null-safe
    // ...
}
```

## Security Checklist

**Input Validation:**
- ✅ All user inputs validated?
- ✅ Whitelist validation used?
- ✅ Input length limits enforced?
- ✅ Special characters escaped?

**SQL Injection:**
- ✅ Prepared statements/parameterized queries used?
- ✅ No string concatenation for SQL?
- ✅ ORM used correctly?

**XSS Prevention:**
- ✅ Output encoding applied?
- ✅ HTML sanitization for user content?
- ✅ Content Security Policy headers set?

**Authentication/Authorization:**
- ✅ Authentication required for sensitive operations?
- ✅ Authorization checks present?
- ✅ Session management secure?
- ✅ Password hashing used (not plain text)?

**Data Protection:**
- ✅ Sensitive data encrypted at rest?
- ✅ Sensitive data encrypted in transit (HTTPS)?
- ✅ No secrets in code/logs?
- ✅ Proper file permissions set?

## Performance Review Points

**Algorithm Complexity:**
- Nested loops: O(n²) or worse?
- Can use more efficient algorithm?
- Unnecessary iterations?

**Database:**
- N+1 query problem?
- Missing indexes?
- Fetching unnecessary data?
- Could use batch operations?

**Caching:**
- Repeated expensive computations?
- Could cache results?
- Cache invalidation handled?

**Memory:**
- Large objects kept in memory?
- Memory leaks possible?
- Could stream instead of load all?

## Code Quality Standards

**Function/Method Size:**
- ✅ Functions under 50 lines (guideline)
- ✅ Single responsibility per function
- ✅ Clear, descriptive names

**Complexity:**
- ✅ Cyclomatic complexity < 10 (guideline)
- ✅ Nesting depth reasonable (< 4 levels)
- ✅ Complex logic well-commented

**DRY (Don't Repeat Yourself):**
- ✅ No code duplication
- ✅ Common logic extracted to functions
- ✅ Constants defined once

**Naming:**
- ✅ Variables: noun phrases (userData, itemCount)
- ✅ Functions: verb phrases (getUserData, calculateTotal)
- ✅ Booleans: question form (isValid, hasPermission)
- ✅ Classes: PascalCase nouns (UserService, DataProcessor)

## Testing Review

**Coverage:**
- ✅ New code has tests?
- ✅ Critical paths tested?
- ✅ Edge cases covered?

**Test Quality:**
- ✅ Tests are independent?
- ✅ Clear test names describing what's tested?
- ✅ Arrange-Act-Assert pattern followed?
- ✅ No test interdependencies?

**Test Types:**
- ✅ Unit tests for business logic?
- ✅ Integration tests for API endpoints?
- ✅ Error cases tested?

## Example Reviews

### Example 1: Security Issue

```markdown
### 🔴 Critical: SQL Injection Vulnerability
**Location:** `api/users.py:45`

**Problem:**
User input is directly interpolated into SQL query without sanitization.

**Impact:**
Attacker could execute arbitrary SQL commands, leading to data breach or data loss.

**Code:**
```python
# Current (VULNERABLE)
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)
```

**Recommendation:**
Use parameterized queries to prevent SQL injection.

**Fix:**
```python
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = %s"
    return db.execute(query, (user_id,))
```
```

### Example 2: Performance Issue

```markdown
### 🟡 Important: N+1 Query Problem
**Location:** `services/order_service.py:78-82`

**Problem:**
Loading users in a loop creates N+1 database queries.

**Impact:**
For 100 orders, this creates 101 queries (1 + 100), severely impacting performance.

**Code:**
```python
# Current (inefficient)
orders = Order.query.all()
for order in orders:
    order.user = User.query.get(order.user_id)  # N queries
```

**Recommendation:**
Use eager loading or a single query with join.

**Fix:**
```python
# Option 1: Eager loading
orders = Order.query.options(joinedload(Order.user)).all()

# Option 2: Separate query
orders = Order.query.all()
user_ids = [o.user_id for o in orders]
users = {u.id: u for u in User.query.filter(User.id.in_(user_ids)).all()}
for order in orders:
    order.user = users[order.user_id]
```
```

## Tips for Effective Reviews

**Be constructive:**
- Explain why, not just what
- Suggest solutions, don't just criticize
- Acknowledge good code

**Be specific:**
- Point to exact lines
- Provide code examples
- Quantify impact when possible

**Prioritize:**
- Fix critical issues first
- Don't nitpick minor style issues
- Focus on what matters

**Ask questions:**
- "Could you explain the reasoning behind...?"
- "Have you considered...?"
- "What happens if...?"

**Provide context:**
- Link to documentation
- Reference coding standards
- Cite security best practices

**Be timely:**
- Review promptly
- Don't block unnecessarily
- Iterate in conversations

This skill provides comprehensive code review guidance. Save it to the current path when ready to package.