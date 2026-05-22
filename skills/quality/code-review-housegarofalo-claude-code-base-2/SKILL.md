---
name: code-review
description: Thorough code review practices and checklists. Covers security review, performance analysis, maintainability assessment, and constructive feedback. Use when reviewing PRs, auditing code quality, or establishing review standards.
---

# Code Review Skill

## Triggers

Use this skill when you see:
- review, code review, PR review
- audit, quality check, security review
- feedback, suggestions, improvements

## Instructions

### Review Philosophy

**Goals of Code Review:**
1. Catch bugs before production
2. Improve code quality
3. Share knowledge across team
4. Maintain consistency
5. Document decisions

**Mindset:**
- Be constructive, not critical
- Assume good intent
- Focus on the code, not the person
- Ask questions to understand
- Acknowledge good work

### Review Checklist

#### 1. Correctness

- [ ] Does the code do what it's supposed to do?
- [ ] Are edge cases handled?
- [ ] Are error conditions handled gracefully?
- [ ] Do the tests cover the requirements?
- [ ] Are there any logic errors?

#### 2. Security

- [ ] No hardcoded secrets or credentials
- [ ] Input validation on all user inputs
- [ ] SQL queries use parameterized statements
- [ ] Authentication/authorization checked
- [ ] Sensitive data properly encrypted
- [ ] No exposure of sensitive info in logs
- [ ] CSRF/XSS protections in place
- [ ] Dependencies checked for vulnerabilities

#### 3. Performance

- [ ] No N+1 query problems
- [ ] Appropriate indexing for queries
- [ ] No unnecessary loops or iterations
- [ ] Large datasets paginated
- [ ] Caching used where appropriate
- [ ] No memory leaks
- [ ] Async operations where beneficial

#### 4. Maintainability

- [ ] Code is readable and self-documenting
- [ ] Functions/methods have single responsibility
- [ ] No excessive complexity (cyclomatic)
- [ ] Magic numbers/strings extracted to constants
- [ ] Dead code removed
- [ ] Consistent naming conventions
- [ ] Appropriate comments for complex logic

#### 5. Testing

- [ ] Unit tests for new functionality
- [ ] Edge cases tested
- [ ] Error paths tested
- [ ] Tests are readable and maintainable
- [ ] No flaky tests
- [ ] Integration tests where appropriate
- [ ] Test coverage adequate

#### 6. Architecture

- [ ] Follows established patterns
- [ ] Proper separation of concerns
- [ ] Dependencies flow correctly
- [ ] No circular dependencies
- [ ] API contracts maintained
- [ ] Breaking changes documented

### Review Process

#### Before Reviewing

```markdown
1. Understand the context
   - Read the PR description
   - Check linked issues/tickets
   - Understand the requirements

2. Get the big picture
   - Look at files changed
   - Identify the scope
   - Note architectural changes

3. Run the code (if possible)
   - Check out the branch
   - Run tests locally
   - Try the feature manually
```

#### During Review

```markdown
1. First pass: Overview
   - Skim all changes
   - Note major concerns
   - Identify areas needing deep review

2. Second pass: Details
   - Review each file carefully
   - Check logic and edge cases
   - Verify test coverage

3. Third pass: Integration
   - Consider system impact
   - Check for breaking changes
   - Verify documentation
```

### Giving Feedback

#### Feedback Categories

**Blocking (Must Fix)**
```
[BLOCKING] SQL injection vulnerability in user input handling.

The query directly interpolates user input:
```python
query = f"SELECT * FROM users WHERE id = {user_id}"
```

This should use parameterized queries:
```python
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```
```

**Suggestion (Should Consider)**
```
[SUGGESTION] Consider extracting this to a separate function.

This block handles three distinct concerns. Separating them would improve:
- Testability
- Reusability
- Readability

Something like:
```python
def validate_input(data): ...
def transform_data(data): ...
def persist_data(data): ...
```
```

**Nitpick (Take It or Leave It)**
```
[NIT] Consider using a more descriptive variable name.

`x` could be `user_count` for clarity.
```

**Praise (Acknowledgment)**
```
[PRAISE] Great use of the strategy pattern here! This makes it easy to add new payment providers.
```

**Question (Clarification)**
```
[QUESTION] What happens if `response` is null here?

I don't see null handling - is this guaranteed by the caller?
```

### Common Issues by Language

#### Python
```python
# Missing type hints
def process(data):  # -> def process(data: dict) -> bool:

# Mutable default arguments
def func(items=[]):  # -> def func(items=None): items = items or []

# Not using context managers
f = open('file.txt')  # -> with open('file.txt') as f:

# Catching too broad exceptions
except Exception:  # -> except SpecificError:

# String concatenation in loops
result = ""
for item in items:
    result += str(item)  # Use ''.join() instead
```

#### TypeScript/JavaScript
```typescript
// Missing null checks
user.name.toLowerCase();  // -> user?.name?.toLowerCase()

// Using any
function process(data: any)  // -> proper typing

// Not awaiting promises
async function fetch() {
    fetchData();  // -> await fetchData()
}

// == instead of ===
if (value == null)  // -> if (value === null)

// Missing error handling in async
try { await riskyOp(); } catch (e) { }  // -> handle error
```

#### SQL
```sql
-- Missing indexes for WHERE clauses
SELECT * FROM orders WHERE customer_id = 123;
-- Ensure customer_id is indexed

-- SELECT * in production
SELECT * FROM users;  -- -> SELECT id, name, email FROM users

-- No LIMIT on potentially large results
SELECT * FROM logs;  -- -> SELECT * FROM logs LIMIT 1000

-- String concatenation (SQL injection)
"SELECT * FROM users WHERE name = '" + name + "'"
-- -> Parameterized query
```

### Review Response Template

```markdown
## Summary
[1-2 sentence overview of the changes and your assessment]

## Blocking Issues
[List any issues that must be fixed before merge]

## Suggestions
[Recommended improvements, not blocking]

## Questions
[Clarifications needed]

## Positive Notes
[What was done well]

## Decision
- [ ] Approved
- [ ] Request Changes
- [ ] Need Discussion
```

### Best Practices

1. **Review Promptly**: Don't let PRs sit for days
2. **Limit Review Size**: 400 lines max per review session
3. **Use Checklists**: Consistent review quality
4. **Be Specific**: Point to exact lines with fixes
5. **Explain Why**: Not just what's wrong, but why
6. **Offer Solutions**: Don't just criticize
7. **Follow Up**: Check that feedback was addressed
8. **Learn from Reviews**: Each review is a learning opportunity
