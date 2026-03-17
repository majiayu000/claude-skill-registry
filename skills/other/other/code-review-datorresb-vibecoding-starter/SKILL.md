---
name: code-review
description: Systematic code review guidance covering correctness, maintainability, security, and performance. Activates for PR reviews and code quality checks.
---

# Code Review Skill

## Core Principle

**Review code through multiple dimensions with constructive, actionable feedback.**

Code review is not just about finding bugs. It's about improving overall quality, sharing knowledge, and maintaining consistency across the codebase. Every review should make the code better while respecting the author's effort and intent.

**Effective reviews are:**
- Specific (point to exact lines, suggest alternatives)
- Constructive (explain why, not just what's wrong)
- Prioritized (critical issues first, nits last)
- Actionable (clear path to resolution)

---

## Review Dimensions

**Review code across five dimensions:**

### 1. Correctness
- Does the code do what it's supposed to do?
- Are edge cases handled?
- Are there logical errors or off-by-one bugs?
- Do tests adequately cover the functionality?
- Are error conditions properly handled?

### 2. Maintainability
- Is the code readable and understandable?
- Are variable/function names clear and descriptive?
- Is the code properly documented?
- Is complexity kept to a minimum?
- Are there repeated patterns that should be abstracted?

### 3. Security
- Are inputs validated and sanitized?
- Are secrets/credentials properly managed?
- Are there SQL injection or XSS vulnerabilities?
- Is authentication/authorization properly implemented?
- Are dependencies up-to-date and vulnerability-free?

### 4. Performance
- Are there obvious performance bottlenecks?
- Are expensive operations (DB queries, API calls) minimized?
- Is caching used appropriately?
- Are data structures chosen efficiently?
- Will this scale with increased load?

### 5. Testing
- Are there adequate tests for new functionality?
- Do tests cover edge cases and error conditions?
- Are tests maintainable and not brittle?
- Is test coverage sufficient for the risk level?
- Are integration points properly tested?

---

## Severity Classification

**Use consistent severity levels to prioritize issues:**

### CRITICAL (Must Fix)
- Security vulnerabilities
- Data corruption or loss risks
- Breaking changes without migration path
- Crashes or exceptions in common paths
- Legal/compliance violations

**Action:** Block merge until resolved.

### MAJOR (Should Fix)
- Significant performance degradation
- Missing error handling for likely failures
- Violations of established patterns/standards
- Insufficient test coverage for complex logic
- Accessibility violations

**Action:** Request changes, consider blocking merge.

### MINOR (Nice to Fix)
- Code duplication or complexity
- Missing documentation for public APIs
- Inconsistent naming or formatting
- Suboptimal algorithm choices
- Missing logging for debugging

**Action:** Request changes, but allow merge if time-constrained.

### NIT (Cosmetic)
- Whitespace or formatting inconsistencies
- Subjective naming preferences
- Comment typos or grammar
- Style guide deviations (if auto-fixable)

**Action:** Suggest but don't block. Consider auto-formatting tools.

---

## Feedback Patterns

**How you phrase feedback matters as much as what you say.**

### Constructive Phrasing

**Good:**
```
MAJOR: This database query runs inside a loop (lines 45-52), which could cause
N+1 query problems with large datasets. Consider moving the query outside the
loop and fetching all records at once:

// Suggested approach:
const userIds = items.map(item => item.userId);
const users = await User.findAll({ where: { id: userIds } });
```

**Bad:**
```
This is slow and inefficient.
```

**Why it matters:** The good example explains the issue, shows the impact, and provides a concrete solution. The bad example is vague and unhelpful.

### Ask Questions Instead of Making Demands

**Good:**
```
MINOR: I notice we're using a different error handling pattern here than in
the rest of the module. Is there a reason for the inconsistency, or should
we standardize on the try/catch pattern used elsewhere?
```

**Bad:**
```
Use the standard error handling pattern.
```

**Why it matters:** The good approach assumes the author may have a reason and invites discussion. The bad approach is prescriptive and may miss important context.

### Highlight What's Good

**Good:**
```
Nice work on the comprehensive error handling in this function. The specific
error messages will make debugging much easier.

MINOR: Consider extracting the validation logic (lines 23-35) into a separate
function to make this more testable.
```

**Bad:**
```
Extract the validation logic into a separate function.
```

**Why it matters:** Positive reinforcement encourages good practices and makes critical feedback easier to receive.

### Provide Context and Examples

**Good:**
```
MAJOR: This function modifies the input array in-place (line 67), which could
cause unexpected behavior for callers who don't expect mutation.

Example of potential bug:
const originalData = [1, 2, 3];
processData(originalData);
console.log(originalData); // [2, 4, 6] - caller didn't expect this!

Consider returning a new array instead:
return data.map(x => x * 2);
```

**Bad:**
```
Don't mutate the input.
```

**Why it matters:** Showing the potential problem with an example makes the issue concrete and demonstrates why the change matters.

---

## Language-Specific Checklists

### Python

**Correctness:**
- [ ] Proper exception handling (specific exceptions, not bare `except:`)
- [ ] Edge cases for None, empty collections, zero/negative numbers
- [ ] Type hints for function signatures (Python 3.5+)
- [ ] Context managers used for file/resource handling

**Maintainability:**
- [ ] PEP 8 style compliance (or project style guide)
- [ ] Docstrings for public functions/classes
- [ ] Functions are focused and < 50 lines
- [ ] List comprehensions for simple cases, explicit loops for complex logic

**Security:**
- [ ] SQL parameterization (no string concatenation for queries)
- [ ] Input validation for user-provided data
- [ ] No `eval()` or `exec()` with user input
- [ ] Secrets in environment variables, not code

**Performance:**
- [ ] Generators for large datasets
- [ ] Appropriate data structures (set for membership, dict for lookups)
- [ ] No redundant list/dict copies
- [ ] Database query optimization (select specific columns, limit results)

### JavaScript/TypeScript

**Correctness:**
- [ ] Proper async/await or promise handling
- [ ] No race conditions in async operations
- [ ] Proper error handling in promises (`.catch()` or try/catch)
- [ ] TypeScript types for function signatures (TS only)

**Maintainability:**
- [ ] ESLint/Prettier compliant (or project style guide)
- [ ] JSDoc comments for exported functions
- [ ] Functions are pure when possible (no side effects)
- [ ] Meaningful variable names (no single-letter except loop counters)

**Security:**
- [ ] Input sanitization for DOM manipulation
- [ ] No `eval()` or `Function()` with user input
- [ ] CSRF protection for state-changing operations
- [ ] XSS prevention (proper escaping, Content Security Policy)

**Performance:**
- [ ] Debouncing/throttling for frequent event handlers
- [ ] Memoization for expensive computations
- [ ] Lazy loading for large datasets
- [ ] No unnecessary re-renders (React: useMemo, useCallback)

### Go

**Correctness:**
- [ ] Error handling for all error returns
- [ ] Proper context handling for timeouts/cancellation
- [ ] Goroutine cleanup (no goroutine leaks)
- [ ] Race condition checks (`go test -race`)

**Maintainability:**
- [ ] `gofmt` formatting
- [ ] Exported functions have comments
- [ ] Interfaces are small and focused
- [ ] Error messages are descriptive

**Security:**
- [ ] SQL parameterization with prepared statements
- [ ] Input validation before use
- [ ] TLS configuration for network services
- [ ] No hardcoded secrets

**Performance:**
- [ ] Appropriate buffer sizes for channels
- [ ] Sync.Pool for frequently allocated objects
- [ ] Profiling for hot paths (if applicable)
- [ ] Efficient string building (strings.Builder)

### Rust

**Correctness:**
- [ ] Proper error propagation (`?` operator or explicit handling)
- [ ] Lifetime annotations where needed
- [ ] Thread safety (Send/Sync trait compliance)
- [ ] Unsafe code justified and documented

**Maintainability:**
- [ ] `cargo fmt` formatting
- [ ] Documentation comments for public items
- [ ] Descriptive type names and variants
- [ ] Pattern matching exhaustiveness

**Security:**
- [ ] No unsafe code without documentation/justification
- [ ] Input validation before unsafe operations
- [ ] Dependency audit (`cargo audit`)

**Performance:**
- [ ] Appropriate collection types (Vec, HashMap, BTreeMap)
- [ ] Avoiding unnecessary clones
- [ ] Iterator chains instead of intermediate collections
- [ ] `cargo bench` for performance-critical code

---

## Integration with Git Hygiene Skill

**Code review happens at different stages:**

### Pre-Commit (Self-Review)

Before committing code:

```bash
# 1. Review your own diff
git diff --staged

# 2. Run automated checks
npm test && npm run lint  # JavaScript
pytest && black --check . # Python
cargo test && cargo clippy # Rust

# 3. Self-review checklist
- Does this code do what I intended?
- Are there edge cases I missed?
- Is this code readable to someone else?
- Are there adequate tests?
- Did I remove debug code and TODOs?

# 4. Commit with descriptive message
git commit -m "[task-X] Brief description"
```

### Pull Request Review

When reviewing others' code:

1. **Read the PR description** - Understand the context and goals
2. **Check CI status** - Ensure tests pass before reviewing
3. **Review commits** - Check git-hygiene skill compliance (task references, atomic commits)
4. **Review code changes** - Use review dimensions above
5. **Test locally if needed** - For complex changes, checkout and test
6. **Provide feedback** - Use severity classification and constructive phrasing
7. **Approve or request changes** - Based on severity of issues

### Post-Merge Review (Team Norms)

After merge (for continuous improvement):

- Review team metrics (test coverage, performance, bug rates)
- Identify patterns (common mistakes, knowledge gaps)
- Update skill guidance or coding standards
- Share learnings in team documentation

---

## Review Checklist

**Before approving a pull request:**

### Functional Review
- [ ] Code solves the stated problem
- [ ] Edge cases are handled
- [ ] Error conditions are properly managed
- [ ] Tests verify the functionality
- [ ] No obvious bugs or logical errors

### Code Quality
- [ ] Code is readable and self-documenting
- [ ] Naming is clear and consistent
- [ ] Complexity is minimized
- [ ] No code duplication (DRY principle)
- [ ] Follows project style guide and conventions

### Security Review
- [ ] Inputs are validated
- [ ] No hardcoded secrets or credentials
- [ ] Authentication/authorization is correct
- [ ] Dependencies are up-to-date
- [ ] No known vulnerability patterns

### Performance Review
- [ ] No obvious performance issues
- [ ] Database queries are optimized
- [ ] Caching is used appropriately
- [ ] Resource usage is reasonable
- [ ] Will scale with expected load

### Testing Review
- [ ] New functionality has tests
- [ ] Tests cover edge cases
- [ ] Tests are maintainable
- [ ] Coverage meets project standards
- [ ] Integration tests for cross-component changes

### Documentation Review
- [ ] Public APIs are documented
- [ ] Complex logic has explanatory comments
- [ ] README updated if needed
- [ ] Migration guide for breaking changes
- [ ] CHANGELOG updated (if applicable)

### Git Hygiene (see git-hygiene skill)
- [ ] Commits reference task IDs
- [ ] Commit messages are descriptive
- [ ] No unrelated changes included
- [ ] No secrets committed
- [ ] Clean commit history (atomic, logical)

---

## Common Pitfalls

### What NOT to Do in Code Reviews

**DON'T:**
- Bikeshed (argue about trivial style issues)
- Make it personal ("you always do this")
- Review too quickly (rushing leads to missed issues)
- Focus only on negatives (acknowledge good work)
- Block on nits (use auto-formatters instead)
- Review too slowly (delays block team progress)
- Ignore context (understand the problem being solved)
- Rewrite in your own style (respect different approaches)

**DO:**
- Focus on high-impact issues first
- Explain the "why" behind feedback
- Suggest alternatives with examples
- Ask questions when intent is unclear
- Use automated tools for style/formatting
- Review promptly (within 1 business day)
- Consider the broader context
- Accept multiple valid approaches

### When to Escalate

**Escalate to team discussion when:**
- Architectural decisions affect multiple components
- Security concerns require expert review
- Performance impact is unclear
- Pattern violates established standards but author has rationale
- Disagreement about approach can't be resolved

**How to escalate:**
1. Document the issue and perspectives
2. Tag relevant experts or team leads
3. Schedule synchronous discussion if needed
4. Document decision in PR or team documentation
5. Update coding standards if needed

---

## Examples: Good vs Bad Reviews

### Example 1: Database Query Issue

**Bad Review:**
```
This is inefficient.
```

**Good Review:**
```
MAJOR: This query runs inside a loop (lines 45-52), creating an N+1 query
problem. With 1000 items, this will run 1000 separate queries instead of 1.

Impact: Page load time increases from ~200ms to ~5s with typical data volumes.

Suggested fix:
// Before (N+1 queries):
for (const item of items) {
  const user = await User.findById(item.userId);
  item.userName = user.name;
}

// After (single query):
const userIds = items.map(item => item.userId);
const users = await User.findAll({ where: { id: userIds } });
const userMap = Object.fromEntries(users.map(u => [u.id, u]));
items.forEach(item => item.userName = userMap[item.userId].name);
```

### Example 2: Error Handling

**Bad Review:**
```
Add error handling.
```

**Good Review:**
```
MAJOR: This async function doesn't handle errors (lines 23-30). If the API
call fails, the promise will be rejected and potentially cause an unhandled
rejection crash.

Consider wrapping in try/catch:
async function fetchUserData(userId) {
  try {
    const response = await api.getUser(userId);
    return response.data;
  } catch (error) {
    logger.error('Failed to fetch user data', { userId, error });
    throw new UserFetchError('Unable to retrieve user data', { cause: error });
  }
}

This allows callers to handle the error appropriately.
```

### Example 3: Code Duplication

**Bad Review:**
```
DRY violation.
```

**Good Review:**
```
MINOR: I notice the validation logic is duplicated between createUser() and
updateUser() (lines 45-52 and lines 78-85). Consider extracting to a shared
function:

function validateUserInput(data) {
  if (!data.email || !isValidEmail(data.email)) {
    throw new ValidationError('Invalid email');
  }
  if (!data.name || data.name.length < 2) {
    throw new ValidationError('Name must be at least 2 characters');
  }
  return true;
}

This makes the validation logic easier to maintain and test in isolation.
```

### Example 4: Security Issue

**Bad Review:**
```
Security problem here.
```

**Good Review:**
```
CRITICAL: User input is concatenated directly into SQL query (line 34),
creating a SQL injection vulnerability.

Vulnerable code:
const query = `SELECT * FROM users WHERE email = '${userEmail}'`;

Exploit example:
userEmail = "' OR '1'='1'; --"
// This returns all users instead of filtering by email

Fix with parameterized query:
const query = 'SELECT * FROM users WHERE email = ?';
const users = await db.query(query, [userEmail]);

This ensures user input is properly escaped and cannot modify the query structure.
```

### Example 5: Positive Feedback with Suggestion

**Bad Review:**
```
Line 67: Extract this to a helper.
```

**Good Review:**
```
Nice work on the comprehensive input validation! The descriptive error messages
will make debugging much easier for API consumers.

MINOR: The validation logic (lines 60-75) might be useful in other endpoints.
Consider extracting to a shared validator module:

// validators/userInput.js
export function validateUserCreation(data) {
  const errors = [];
  if (!data.email || !isValidEmail(data.email)) {
    errors.push({ field: 'email', message: 'Invalid email format' });
  }
  // ... rest of validation
  return errors;
}

This would make it easier to maintain consistent validation across endpoints.
```

---

## Integration with Backlog Workflow

**Code review integrates with task management:**

### During Task Execution
- Self-review before marking task complete
- Use review checklist to verify quality
- Ensure all acceptance criteria met

### During Pull Request
- Reference task ID in PR description
- Link commits to tasks (git-hygiene skill)
- Update task notes with PR status

### After Merge
- Update task with commit hash (git-hygiene skill)
- Mark task complete in backlog
- Document learnings for future tasks

**Example workflow:**

```bash
# 1. Complete task implementation
# 2. Self-review using checklist above
git diff --staged
npm test && npm run lint

# 3. Commit with task reference
git commit -m "[task-42] Add user authentication

Implements JWT-based auth with refresh tokens. All security best practices
followed (bcrypt for passwords, secure token storage, CSRF protection)."

# 4. Push and create PR
git push -u origin feature/task-42-auth
gh pr create --title "[task-42] Add user authentication" --body "..."

# 5. Team reviews PR using code-review skill
# 6. Address feedback, push updates
# 7. After approval and merge, update task
task_edit(
  id="task-42",
  status="Done",
  notesAppend=["PR #123 merged, commit abc123"]
)
```

---

**Remember:** Code review is a collaborative process focused on improving quality and sharing knowledge. Approach reviews with curiosity and respect, prioritize high-impact issues, and make feedback actionable. Good reviews make code better and teams stronger.
