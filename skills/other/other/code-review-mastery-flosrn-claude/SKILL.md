---
name: code-review-mastery
description: Complete code review lifecycle - WHAT to check + HOW to interact + verification gates. ALWAYS use when the user says "code review", "review this PR", "check my code", "audit this", "revue de code", "vérifier le code", "analyser ce PR", "revoir mon code", or when reviewing PRs, receiving feedback, requesting reviews, conducting code audits, or before making completion claims. Covers security (OWASP), clean code (SOLID), metrics, feedback patterns, and verification gates.
---

# Code Review Mastery

Complete code review lifecycle: WHAT to check, HOW to interact, and WHEN to verify.

## Overview

Code review is a three-part discipline:

1. **WHAT to Review** - Security, logic, clean code, metrics
2. **HOW to Interact** - Receiving feedback, requesting reviews, giving feedback
3. **VERIFICATION** - Evidence before any completion claims

## Quick Start

### Giving a Review

**Priority order**: Security > Correctness > Maintainability > Performance

```
1. SECURITY: Input validation, auth checks, secrets exposure
2. LOGIC: Edge cases, error handling, null checks
3. ARCHITECTURE: Single responsibility, proper abstractions
4. TESTS: Coverage for new functionality
```

**Skip** (automate instead): Formatting, naming conventions, linting violations

### Receiving Feedback

```
READ → UNDERSTAND → VERIFY → EVALUATE → RESPOND → IMPLEMENT
```

- No performative agreement ("You're absolutely right!")
- Verify against codebase before implementing
- Push back if technically wrong

### Before Claiming Done

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

Run the command. Read the output. THEN claim the result.

---

## Part 1: What to Review

### Security (Critical)

**Must check in every review:**
- No hardcoded credentials (search: `password.*=.*['"]`, `api[_-]?key.*=`)
- Input validation on all user data
- Parameterized queries (no string concatenation for SQL)
- Authorization checks on every endpoint
- No `eval()`, `exec()`, dangerous functions

**Reference**: [references/security-checklist.md](references/security-checklist.md)

### Logic (Critical)

**Verify correctness:**
- Business logic matches requirements
- Edge cases handled (null, empty, boundary values)
- Error handling present and appropriate
- Race conditions in async code
- Resource cleanup (connections, file handles)

### Clean Code (High)

**Check for code smells:**
- Large functions (>50 lines) - violate Single Responsibility
- Deep nesting (>3 levels) - extract to functions
- Long parameter lists (>3 params) - use objects
- Duplicated code - extract to shared functions
- Magic numbers/strings - use named constants

**Reference**: [references/clean-code-principles.md](references/clean-code-principles.md)

### Metrics (Medium)

**Targets:**
| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Cognitive complexity | <15/fn | 15-25 | >25 |
| Function size | <20 lines | 30-50 | >50 |
| Parameters | ≤3 | 4 | >5 |
| Nesting depth | ≤2 | 3 | >3 |

**Reference**: [references/code-quality-metrics.md](references/code-quality-metrics.md)

---

## Part 2: How to Interact

### Giving Feedback

**Structure**: What + Why + How

```
✓ "[BLOCKING] SQL injection at line 34. Query uses string concatenation
   with user input. Fix: Use parameterized query:
   db.query('SELECT * FROM users WHERE id = ?', [userId])"

✗ "This query looks unsafe."
```

**Priority Labels:**
| Label | Meaning | Blocks Merge? |
|-------|---------|---------------|
| `[BLOCKING]` | Must fix - security, bugs | Yes |
| `[CRITICAL]` | Strongly recommended | Discuss |
| `[SUGGESTION]` | Would improve code | No |
| `[NIT]` | Minor preference | No |

**Reference**: [references/feedback-patterns.md](references/feedback-patterns.md)

### Receiving Feedback

**The Response Pattern:**
```
1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
```

**Forbidden responses:**
- "You're absolutely right!" (performative)
- "Great point!" (performative)
- "Let me implement that now" (before verification)

**When feedback is unclear:**
```
STOP - do not implement anything yet
ASK for clarification on ALL unclear items
```

**When feedback is wrong:**
Push back with technical reasoning, not defensiveness.

**Reference**: [references/code-review-reception.md](references/code-review-reception.md)

### Requesting Review

**When to request:**
- After each task in subagent-driven development
- After completing major features
- Before merge to main

**How:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)
HEAD_SHA=$(git rev-parse HEAD)
```

Then dispatch code-reviewer subagent via Task tool.

**Reference**: [references/requesting-code-review.md](references/requesting-code-review.md)

---

## Part 3: Verification Gates

### The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

### The Gate Function

```
1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
5. ONLY THEN: Make the claim
```

### Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test output: 0 failures | Previous run, "should pass" |
| Build succeeds | Build exit 0 | Linter passing |
| Bug fixed | Original symptom passes | Code changed |
| Requirements met | Line-by-line checklist | Tests passing |

### Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification
- About to commit without running tests
- ANY wording implying success without evidence

**Reference**: [references/verification-before-completion.md](references/verification-before-completion.md)

---

## Anti-Patterns

### Nitpicking
**Problem**: Excessive minor comments bury critical issues
**Solution**: Automate style with linters; focus humans on logic/security

### Vague Criticism
**Problem**: "This is wrong" without explanation
**Solution**: Always include What + Why + How

### Blocking on Preferences
**Problem**: Blocking merge for subjective style
**Solution**: Reserve blocking for security/correctness only

### Performative Agreement
**Problem**: "You're absolutely right!" without verification
**Solution**: Verify first, then implement

---

## Decision Tree

```
SITUATION?
│
├─ Reviewing someone's code
│  ├─ Security issue? → [BLOCKING] with fix
│  ├─ Logic bug? → [BLOCKING] with test case
│  ├─ Code smell? → [SUGGESTION] with explanation
│  └─ Style preference? → Skip or automate
│
├─ Received feedback
│  ├─ Unclear items? → STOP, ask for clarification first
│  ├─ From trusted source? → Understand, then implement
│  └─ From external reviewer? → Verify technically before implementing
│
├─ Completed work
│  └─ Major feature/task? → Request code-reviewer subagent review
│
└─ About to claim status
   ├─ Have fresh verification? → State claim WITH evidence
   └─ No fresh verification? → RUN command first
```

---

## Reference Guides

- **Security**: [references/security-checklist.md](references/security-checklist.md) - OWASP Top 10, auth, input validation
- **Clean Code**: [references/clean-code-principles.md](references/clean-code-principles.md) - SOLID, naming, functions, smells
- **Feedback**: [references/feedback-patterns.md](references/feedback-patterns.md) - Valuable vs wasteful patterns
- **Metrics**: [references/code-quality-metrics.md](references/code-quality-metrics.md) - Complexity, maintainability
- **Reception**: [references/code-review-reception.md](references/code-review-reception.md) - How to receive feedback
- **Requesting**: [references/requesting-code-review.md](references/requesting-code-review.md) - How to request reviews
- **Verification**: [references/verification-before-completion.md](references/verification-before-completion.md) - Evidence gates

---

## Success Criteria

A good code review:
- Identifies security vulnerabilities (if any)
- Catches logic errors and edge cases
- Flags maintainability issues with specific fixes
- Uses priority labels ([BLOCKING] vs [SUGGESTION])
- Provides actionable feedback (What + Why + How)
- Avoids nitpicks on style/formatting
- Verifies claims with evidence before completion
