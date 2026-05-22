---
name: code-review-skill
description: Comprehensive code review and analysis. AUTO-TRIGGERS when user asks to review, refactor, debug, critique, or analyze code.
keywords:
  - review
  - refactor
  - debug
  - critique
  - analyze code
  - code quality
  - bugs
  - vulnerabilities
  - performance
  - best practices
---

# Code Review Skill

## What This Skill Does

This skill **automatically activates** when you ask Claude to review, refactor, debug, or analyze code. It's a demonstration of the **auto-trigger pattern**—the skill detects your intent and applies specialized code review expertise without you explicitly requesting "code review mode."

## Auto-Trigger Keywords

This skill engages when you mention:
- "review" (code review, peer review, security review)
- "refactor" (improve, restructure, simplify)
- "debug" (find the bug, what's wrong, why doesn't it work)
- "analyze" (code analysis, code smell, technical debt)
- "critique" (code critique, feedback, improvement)
- "vulnerabilities" (security issues, exploits, vulnerabilities)
- "performance" (optimization, slow, inefficient)
- "best practices" (coding standards, conventions, idiomatic)

## Review Workflow

### Step 1: Understand the Context
- Identify the programming language
- Determine the purpose/intent of the code
- Note the specific area of focus (performance, security, clarity, etc.)

### Step 2: Structured Analysis
Review across these dimensions:
1. **Correctness** - Does it do what it's supposed to?
2. **Readability** - Is the code clear and maintainable?
3. **Performance** - Are there inefficiencies?
4. **Security** - Are there vulnerabilities or risks?
5. **Best Practices** - Does it follow language conventions?
6. **Testing** - Is the code testable? Are edge cases handled?

### Step 3: Provide Feedback
- Highlight what works well (positive feedback)
- Point out specific issues with line references
- Suggest concrete improvements
- Explain the "why" behind recommendations

### Step 4: Prioritize Suggestions
- **Critical** - Security issues, bugs, breaking issues
- **Important** - Performance, maintainability, design
- **Nice-to-have** - Style, minor improvements

## Review Scenarios (Examples)

### Example 1: Security Review
**User:** "Review this for vulnerabilities"
```python
import hashlib
password = input("Enter password: ")
hash = hashlib.md5(password.encode()).hexdigest()
```
**Response:** (Auto-triggers code-review-skill)
- Point out: MD5 is cryptographically broken
- Suggest: Use bcrypt, scrypt, or Argon2 instead
- Explain: MD5 is vulnerable to collision attacks

### Example 2: Refactoring Request
**User:** "How can I refactor this to be cleaner?"
```python
if x > 5:
    if y > 10:
        if z < 3:
            print("conditions met")
```
**Response:** (Auto-triggers code-review-skill)
- Suggest: Use logical operators to flatten nesting
- Show: `if x > 5 and y > 10 and z < 3:`
- Explain: Reduces cognitive complexity

### Example 3: Performance Analysis
**User:** "This code is slow, find the bottleneck"
```python
result = []
for item in large_list:
    if item not in result:
        result.append(item)
```
**Response:** (Auto-triggers code-review-skill)
- Identify: O(n²) behavior due to list lookup
- Suggest: Use `set()` for O(1) lookups
- Show: `result = list(set(large_list))`

### Example 4: Bug Hunting
**User:** "Debug this—there's a logic error"
```javascript
for (let i = 0; i <= arr.length; i++) {
    console.log(arr[i]);
}
```
**Response:** (Auto-triggers code-review-skill)
- Spot: Off-by-one error (i <= arr.length)
- Explain: arr[arr.length] is undefined
- Fix: Change `<=` to `<`

## Key Points

- **Auto-trigger is implicit** - Just ask about code quality/bugs, and this skill engages
- **Context-aware** - Adapts to language, domain, and review focus
- **Positive & constructive** - Always acknowledge good practices first
- **Specific feedback** - Reference line numbers and concrete examples
- **Educational** - Explain the "why" behind suggestions

## When This Skill Doesn't Apply

This skill focuses on **code itself**. For other needs, use different tools:
- Architecture design → Use planning/design tools
- Project setup → Use project initialization tools
- Documentation → Use documentation skills
- Testing framework selection → Use research skills

## Review Priorities

**Always check first (if relevant):**
1. Security vulnerabilities
2. Correctness/logic bugs
3. Performance critical paths
4. Maintainability
5. Style/conventions

**Only after above are addressed:**
6. Minor improvements
7. Code style preferences
8. Formatting
