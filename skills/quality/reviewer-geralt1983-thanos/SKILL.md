---
name: Code Reviewer
description: Code review, PR analysis, and quality feedback. USE WHEN user mentions review, PR, pull request, code quality, best practices, feedback, suggestions, improvements, code smell, or asks to look at code for issues.
---

# Code Reviewer Skill

AI-powered code review guidance for analyzing code changes, identifying issues, suggesting improvements, and ensuring best practices with focus on maintainability, correctness, and team standards.

## What This Skill Does

This skill provides expert-level code review guidance including identifying bugs, security issues, performance problems, style violations, and opportunities for improvement. It combines code review best practices with constructive, actionable feedback.

**Key Capabilities:**
- **Bug Detection**: Logic errors, edge cases, null handling, race conditions
- **Security Analysis**: Vulnerability scanning, injection risks, auth issues
- **Performance Review**: Inefficiencies, N+1 queries, memory concerns
- **Style Consistency**: Naming conventions, formatting, idiomatic code
- **Maintainability**: Complexity, readability, documentation gaps
- **PR Best Practices**: Commit hygiene, change scope, description quality

## Core Principles

### The Constructive Review Mindset
- **Assume Positive Intent**: The author is trying their best
- **Ask, Don't Tell**: Frame suggestions as questions when possible
- **Explain Why**: Context helps the author learn and decide
- **Praise Good Work**: Acknowledge patterns done well
- **Pick Your Battles**: Not everything needs to be perfect

### Review Priority Hierarchy
1. **Correctness** - Does it work? Will it break things?
2. **Security** - Are there vulnerabilities or data risks?
3. **Performance** - Are there obvious performance issues?
4. **Maintainability** - Can others understand and modify it?
5. **Style** - Does it follow team conventions?

## Code Review Workflow

### 1. Understand Context
```
Before reviewing code:
├── Read the PR description/ticket
├── Understand the goal (what problem is being solved?)
├── Check the scope (is this the right size change?)
├── Review related changes (tests included?)
└── Check target branch (main, feature, hotfix?)
```

### 2. First Pass - Big Picture
```
High-level review:
├── Architecture (does this fit the existing patterns?)
├── Design (is this the right approach?)
├── Completeness (are all cases handled?)
├── Tests (are changes adequately tested?)
└── Breaking Changes (will this break existing code?)
```

### 3. Detailed Review
```
Line-by-line analysis:
├── Logic (correct algorithms, edge cases)
├── Security (input validation, auth checks)
├── Error Handling (exceptions, edge cases)
├── Performance (loops, queries, memory)
├── Naming (clear, consistent, meaningful)
├── Comments (necessary, accurate, helpful)
└── Style (formatting, conventions)
```

### 4. Provide Feedback
Generate feedback that is:
- Specific (point to exact lines)
- Actionable (say what to change)
- Educational (explain why it matters)
- Prioritized (must-fix vs nice-to-have)

## Review Comment Categories

### Comment Severity Levels
| Level | Prefix | Meaning | Example |
|-------|--------|---------|---------|
| **Blocking** | 🔴 | Must fix before merge | Security vulnerability |
| **Major** | 🟠 | Should fix, discuss if not | Bug, missing test |
| **Minor** | 🟡 | Nice to have | Style improvement |
| **Nitpick** | ⚪ | Optional, FYI | Preference, suggestion |
| **Praise** | 🟢 | Good job! | Clean pattern |

### Comment Types
```
🔴 Bug: This will throw NullPointerException when user is null
🟠 Test: Missing test for the error case on line 45
🟡 Style: Consider extracting this to a helper function
⚪ Nit: Typo in variable name "recieve" → "receive"
🟢 Nice: Great use of the Strategy pattern here!
❓ Question: What happens if the queue is empty?
```

## Common Issues to Look For

### Logic Issues
| Issue | Look For | Example |
|-------|----------|---------|
| **Off-by-one** | Loops, array indices | `i <= length` vs `i < length` |
| **Null/undefined** | Optional values, API responses | Missing null checks |
| **Type confusion** | Type coercion, casting | String vs number comparison |
| **Boundary conditions** | Empty arrays, zero values | `items.length > 0` checks |
| **State management** | Shared state, async updates | Race conditions |

### Security Issues
| Issue | Look For | Example |
|-------|----------|---------|
| **Injection** | User input in queries/commands | SQL, command injection |
| **Auth bypass** | Missing permission checks | Direct object reference |
| **Data exposure** | Logging, error messages | Passwords in logs |
| **XSS** | User content rendered as HTML | Unsanitized output |
| **CSRF** | State-changing GET requests | Missing CSRF tokens |

### Performance Issues
| Issue | Look For | Example |
|-------|----------|---------|
| **N+1 queries** | Loops with DB calls | Fetch in loop |
| **Unbounded growth** | Collections without limits | Memory leaks |
| **Unnecessary work** | Redundant calculations | Computing in loop |
| **Missing caching** | Repeated expensive ops | Re-fetching static data |
| **Blocking operations** | Sync in async context | Blocking I/O |

### Maintainability Issues
| Issue | Look For | Example |
|-------|----------|---------|
| **Long methods** | > 50 lines | Extract helper functions |
| **Deep nesting** | > 3 levels of indentation | Guard clauses, extraction |
| **Magic numbers** | Hardcoded values | Use named constants |
| **Poor naming** | Single letters, abbreviations | Descriptive names |
| **Missing docs** | Public APIs without docs | Add JSDoc/docstrings |

## Effective Feedback Templates

### Suggesting Alternatives
```markdown
**Instead of:**
```python
result = []
for item in items:
    if item.active:
        result.append(item.name)
```

**Consider:**
```python
result = [item.name for item in items if item.active]
```

This is more Pythonic and expresses the intent more clearly.
```

### Asking Questions
```markdown
❓ I'm curious about the choice to use recursion here. 
Given that the input could be deeply nested (up to 1000 levels),
would an iterative approach with an explicit stack be safer 
to avoid potential stack overflow?
```

### Explaining Concerns
```markdown
🟠 **Concern: Race Condition Risk**

Lines 45-50 read the counter, increment it, and write back.
If two requests hit this simultaneously, they could both read 
the same value, leading to a lost update.

**Suggestion:** Use atomic operations or database transactions:
```python
Counter.objects.filter(id=1).update(value=F('value') + 1)
```
```

### Praising Good Work
```markdown
🟢 **Nice pattern here!** 

Using the factory method makes this extensible without modifying 
existing code. I like that you also included the type hints - 
makes the intent crystal clear.
```

## PR Best Practices Guide

### Good PR Characteristics
- **Small and Focused**: One logical change per PR
- **Descriptive Title**: Summarizes what the change does
- **Clear Description**: Why, what, and how
- **Self-Reviewed**: Author reviewed before requesting
- **Tests Included**: New/changed code has tests
- **Passing CI**: All checks green before review

### PR Review Checklist
- [ ] **Title clear?** Does it summarize the change?
- [ ] **Description complete?** Context, testing, rollback?
- [ ] **Right size?** < 400 lines is ideal
- [ ] **Tests passing?** CI all green?
- [ ] **Tests adequate?** New behavior covered?
- [ ] **No debug code?** Console.logs, print statements removed?
- [ ] **Dependencies updated?** Lock files included?
- [ ] **Documentation updated?** README, API docs?

## Language-Specific Review Points

### Python
```python
# Check for:
- Type hints on public functions
- Docstrings on public classes/methods
- No mutable default arguments (def foo(items=[]))
- Context managers for resources (with open(...))
- List comprehensions over map/filter when cleaner
- f-strings for formatting (not % or .format)
```

### JavaScript/TypeScript
```typescript
// Check for:
- Proper async/await usage (not mixing with .then())
- Null coalescing (??) vs OR (||) for defaults
- Optional chaining (?.) for nested access
- const over let, avoid var
- Arrow functions where appropriate
- TypeScript: strict types, no any
```

### Java
```java
// Check for:
- Proper null handling (Optional, @Nullable)
- Try-with-resources for AutoCloseable
- Immutable objects where possible
- Builder pattern for complex constructors
- Stream API over imperative loops when clearer
- Proper equals/hashCode implementation
```

### Go
```go
// Check for:
- Error handling (not _ for errors)
- Defer for cleanup
- Context propagation
- Proper goroutine lifecycle
- Interface compliance (compile-time checks)
- Effective naming (short but clear)
```

## When to Use This Skill

**Trigger Phrases:**
- "Review this code..."
- "What do you think about..."
- "Can you check this PR..."
- "Is this approach correct?"
- "Any suggestions for improvement?"
- "What issues do you see?"
- "How can I make this better?"
- "Does this look right?"

**Example Requests:**
1. "Review this function for potential bugs"
2. "What security issues do you see in this API?"
3. "Is this the right way to structure this?"
4. "Does this follow best practices?"
5. "Help me review this PR before merging"
6. "What would you improve about this code?"

## Review Quality Checklist

Before submitting review feedback:

- [ ] **Constructive?** Would I want to receive this feedback?
- [ ] **Specific?** Did I point to exact lines/issues?
- [ ] **Actionable?** Is it clear what to change?
- [ ] **Prioritized?** Are blocking issues clearly marked?
- [ ] **Complete?** Did I cover correctness, security, tests?
- [ ] **Balanced?** Did I acknowledge what was done well?
- [ ] **Respectful?** Is the tone collaborative?

## Integration with Other Skills

- **Architect**: Architecture review during design phase
- **Tester**: Test coverage and quality review
- **Troubleshooter**: Reviewing fixes for bugs
- **Refactorer**: Post-merge improvement suggestions

---

*Skill designed for Thanos + Antigravity integration*
