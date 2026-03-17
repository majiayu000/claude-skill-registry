---
name: arcanea-code-review
description: Conduct thorough, constructive code reviews that improve code quality and team knowledge. Focuses on what matters - architecture, logic, security, maintainability - while avoiding bikeshedding.
version: 2.0.0
author: Arcanea
tags: [code-review, quality, collaboration, development]
triggers:
  - review
  - code review
  - PR
  - pull request
  - check my code
---

# The Art of Code Review

> *"A review is not a judgment. It is a gift of attention that makes both the code and the coder stronger."*

---

## The Review Philosophy

### What Code Review IS
```
✓ Knowledge sharing
✓ Quality assurance
✓ Learning opportunity
✓ Documentation check
✓ Collaboration ritual
```

### What Code Review is NOT
```
❌ Gatekeeping
❌ Proving superiority
❌ Stylistic bikeshedding
❌ Blocking progress
❌ Personal criticism
```

---

## The Review Hierarchy

Focus effort where it matters most:

```
╔════════════════════════════════════════════════════════════╗
║                    REVIEW PRIORITY                          ║
╠════════════════════════════════════════════════════════════╣
║                                                             ║
║   🔴 CRITICAL (Block merge)                                ║
║   ├── Security vulnerabilities                             ║
║   ├── Data loss risks                                      ║
║   ├── Breaking changes without migration                   ║
║   └── Logic errors affecting correctness                   ║
║                                                             ║
║   🟠 IMPORTANT (Should fix before merge)                   ║
║   ├── Bugs and edge cases                                  ║
║   ├── Performance issues                                   ║
║   ├── Missing tests for new logic                         ║
║   └── Architectural concerns                               ║
║                                                             ║
║   🟡 SUGGESTIONS (Nice to have)                            ║
║   ├── Readability improvements                             ║
║   ├── Better naming                                        ║
║   ├── Documentation additions                              ║
║   └── Minor refactoring opportunities                      ║
║                                                             ║
║   ⚪ NITPICKS (Optional, don't block)                      ║
║   ├── Style preferences                                    ║
║   ├── Formatting                                           ║
║   └── Subjective choices                                   ║
║                                                             ║
╚════════════════════════════════════════════════════════════╝
```

---

## The Review Checklist

### 1. Security Review
```
□ No hardcoded secrets/credentials
□ Input validation present
□ No SQL injection risks
□ No XSS vulnerabilities
□ Authentication/authorization correct
□ Sensitive data handled properly
□ Dependencies are up to date
□ No debug/admin backdoors
```

### 2. Logic Review
```
□ Code does what it claims to do
□ Edge cases handled
□ Error handling is appropriate
□ Null/undefined handled safely
□ Race conditions considered
□ State management is correct
□ No obvious bugs
```

### 3. Architecture Review
```
□ Follows project patterns
□ Separation of concerns
□ Dependencies flow correctly
□ No circular dependencies
□ Appropriate abstraction level
□ DRY (Don't Repeat Yourself)
□ SOLID principles where applicable
```

### 4. Maintainability Review
```
□ Code is readable
□ Functions are reasonably sized
□ Names are clear and accurate
□ Complex logic is commented
□ No magic numbers/strings
□ Easy to modify in future
□ No unnecessary complexity
```

### 5. Testing Review
```
□ Tests exist for new functionality
□ Tests cover edge cases
□ Tests are readable
□ Tests actually test something
□ No testing implementation details
□ Existing tests still pass
```

### 6. Performance Review
```
□ No obvious performance issues
□ Database queries are efficient
□ No N+1 query problems
□ Appropriate caching
□ Memory usage reasonable
□ No blocking operations on main thread
```

---

## Review Communication

### The Feedback Format
```markdown
**Level**: [Critical/Important/Suggestion/Nitpick]

**What**: [Specific issue]

**Why**: [Impact or concern]

**How**: [Suggested fix or alternative]
```

### Examples

#### Critical Issue
```markdown
🔴 **Critical: SQL Injection Risk**

**Line 45**: `db.query("SELECT * FROM users WHERE id = " + userId)`

This is vulnerable to SQL injection. An attacker could delete data
or access unauthorized information.

**Suggested fix**:
```js
db.query("SELECT * FROM users WHERE id = ?", [userId])
```
```

#### Important Suggestion
```markdown
🟠 **Important: Missing Error Handling**

**Line 78**: `const data = await fetchUser(id)`

If fetchUser throws, this will crash the request handler and
return a 500 to the user.

**Suggested fix**:
```js
try {
  const data = await fetchUser(id);
} catch (error) {
  logger.error('Failed to fetch user', { id, error });
  return res.status(404).json({ error: 'User not found' });
}
```
```

#### Suggestion
```markdown
🟡 **Suggestion: Naming Clarity**

**Line 32**: `const d = new Date()`

Single-letter variable names reduce readability.

**Consider**: `const createdAt = new Date()`
```

#### Nitpick
```markdown
⚪ **Nitpick** (optional, non-blocking)

**Line 15**: Would prefer `const` over `let` here since it's never reassigned.
```

### Tone Guidelines
```
AVOID:
- "You should..."
- "This is wrong"
- "Why would you..."
- "Obviously..."

PREFER:
- "Consider..."
- "What if we..."
- "I wonder if..."
- "One option might be..."

Questions often work better than commands:
"Could this throw if the user doesn't exist?"
vs
"This will crash when user doesn't exist!"
```

---

## Review Strategies

### The First Pass: Overview
```
1. Read the PR description
2. Understand the goal
3. Scan all files changed
4. Get the big picture
```

### The Second Pass: Detail
```
1. Read each file carefully
2. Check logic flow
3. Look for bugs and issues
4. Note questions
```

### The Third Pass: Context
```
1. Check how it fits with existing code
2. Consider future implications
3. Look for missing tests
4. Consider edge cases
```

### Large PR Strategy
```
If PR is too big to review effectively:

1. Request it be split into smaller PRs
2. Focus on highest-risk files first
3. Review in multiple sessions
4. Trust tests for mechanical changes
```

---

## Common Review Scenarios

### The Refactoring PR
```
Key questions:
- Does behavior remain identical?
- Are there tests proving behavior is preserved?
- Is the new structure actually better?
- Is this the right time for this refactor?
```

### The Bug Fix PR
```
Key questions:
- Does it actually fix the bug?
- Is there a test that would have caught this?
- Could this fix break something else?
- Is the root cause addressed?
```

### The New Feature PR
```
Key questions:
- Does it meet requirements?
- Is it complete or partial?
- Are there edge cases?
- Is it testable and tested?
- Does it fit the architecture?
```

### The Dependencies Update PR
```
Key questions:
- Is this update necessary?
- Are there breaking changes?
- Have changelogs been reviewed?
- Do tests still pass?
- Any security advisories?
```

---

## Self-Review Checklist

Before requesting review, check:

```
□ Code compiles/passes linter
□ Tests pass
□ Changes match PR description
□ No debug code left in
□ No commented-out code
□ No unrelated changes
□ Commit messages are clear
□ Documentation updated if needed
□ PR is reasonably sized
□ Ready for someone else to read
```

---

## Being a Good Reviewer

### Timeliness
```
Review within 24 hours if possible.
Blocked authors = blocked productivity.
If you can't review, say so.
```

### Completeness
```
Review thoroughly the first time.
Multiple rounds of "one more thing" is frustrating.
Group all feedback in one review.
```

### Approachability
```
Praise what's good, not just what's wrong.
"Nice approach to this problem"
"Clean solution for the edge case"
Genuine appreciation builds trust.
```

### Ownership
```
Reviews aren't about winning.
The goal is better code AND better coders.
Be willing to be wrong.
Defer to author on judgment calls.
```

---

## Quick Reference

### Review Comment Prefixes
```
🔴 CRITICAL: - Must fix before merge
🟠 IMPORTANT: - Should fix before merge
🟡 SUGGESTION: - Improvement idea
⚪ NIT: - Take it or leave it
❓ QUESTION: - Need clarification
💭 THOUGHT: - Something to consider
👍 NICE: - Positive feedback
```

### The 10-Minute Review
```
If you only have 10 minutes:
1. Read PR description (1 min)
2. Scan file changes (2 min)
3. Check highest-risk code (5 min)
4. Verify tests exist (2 min)

Flag if needs deeper review.
```

### Review Red Flags
```
- Very large diffs (>500 lines)
- No tests for new logic
- Commented-out code
- TODOs without tickets
- Copy-pasted code blocks
- Complex nested logic
- Magic numbers/strings
- Ignored error handling
- Hardcoded values
- Console.log/print statements
```

---

*"Review the code, not the coder. The goal is software we're all proud of."*
