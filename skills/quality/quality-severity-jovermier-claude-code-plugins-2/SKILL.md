---
name: quality-severity
description: This skill should be used when classifying issues, findings, or code review problems with severity levels. Triggers on requests like "classify severity", "what is P1/P2/P3", "determine issue priority".
updated: 2026-01-12
---

# Quality Gate Severity Levels

## Core Philosophy

Severity classification enables prioritized triage of issues, ensuring critical problems block deployments while less severe issues are tracked appropriately.

## Key Sections

### Severity Levels

#### P1 (Critical) - Blocks Merge

**Definition:** Issues that must be fixed before merging. These cause immediate harm or break core functionality.

**Types:**
- **Security vulnerabilities**
  - OWASP Top 10 violations (SQL injection, XSS, CSRF, etc.)
  - Hardcoded secrets or credentials
  - Authentication/authorization bypasses
  - Insecure data transmission

- **Data corruption risks**
  - Unhandled database constraints
  - Race conditions causing data loss
  - Missing transaction boundaries
  - Improper data validation

- **Breaking changes**
  - API contract violations
  - Backward-incompatible changes
  - Deprecated method usage without migration

- **System failures**
  - Unhandled exceptions causing crashes
  - Memory leaks leading to OOM
  - Deadlock conditions
  - Critical performance degradation (>10x slowdown)

**Action:** Fix immediately, block merge, create P1 todo

#### P2 (Important) - Should Fix

**Definition:** Issues that significantly impact code quality but don't block merging. Should be addressed promptly.

**Types:**
- **Performance issues**
  - N+1 query problems
  - Missing indexes
  - Inefficient algorithms (O(n²) where O(n) possible)
  - Unnecessary expensive operations

- **Architectural concerns**
  - Violation of SOLID principles
  - Tight coupling between components
  - Missing abstractions for repeated patterns
  - Inappropriate layering violations

- **Code clarity problems**
  - Confusing variable/function names
  - Complex nested logic (5+ levels)
  - Magic numbers/strings
  - Missing or misleading comments

- **Maintainability risks**
  - Large functions/methods (>100 lines)
  - Duplicate code (DRY violations)
  - Missing error handling for edge cases
  - Untested or untestable code paths

**Action:** Create P2 todo, aim to fix in same iteration

#### P3 (Nice-to-Have) - Enhancement

**Definition:** Improvements that would be beneficial but aren't urgent. Can be deferred to tech debt time.

**Types:**
- **Code cleanup**
  - Minor style inconsistencies
  - Unused imports/variables
  - Redundant null checks (type-safe cases)

- **Optimization opportunities**
  - Micro-optimizations with minimal impact
  - Caching opportunities for rarely-used data
  - Minor algorithmic improvements

- **Documentation improvements**
  - Adding JSDoc/Python docstrings
  - Improving inline comments
  - Updating README examples

- **Style consistency**
  - Formatting alignment
  - Naming convention adherence
  - Import organization

**Action:** Track in backlog, address during tech debt sprint

### Classification Framework

```
1. Does this cause immediate harm or data loss?
   YES → P1

2. Does this significantly impact performance, security, or maintainability?
   YES → P2

3. Is this a minor improvement or polish?
   YES → P3
```

### Quick Reference Table

| Category | P1 Examples | P2 Examples | P3 Examples |
|----------|-------------|-------------|-------------|
| **Security** | SQL injection, exposed secrets | Missing rate limiting | Weak password suggestions |
| **Performance** | 10x slowdown, OOM | N+1 queries, missing indexes | Micro-optimizations |
| **Data** | Corruption, loss | Race conditions | Unused columns |
| **Architecture** | Breaking changes | SOLID violations | Minor refactors |
| **Code Quality** | Crashes, unhandled errors | Complex logic, duplication | Style, formatting |
| **Testing** | No tests for critical paths | Missing edge cases | Untested utility functions |

## Usage Examples

**Example 1: Classifying a security issue**
> User: "What severity is hardcoded API keys in the code?"

> Assistant: This is **P1 (Critical)** because it exposes secrets that could be exploited. Action required: Immediately remove and rotate keys, block merge until fixed.

**Example 2: Classifying a performance issue**
> User: "We have N+1 queries in the user list endpoint"

> Attorney: This is **P2 (Important)**. While it doesn't block the merge, it will cause significant performance issues at scale. Create a P2 todo to fix with eager loading or data loader.

**Example 3: Classifying a style issue**
> User: "Inconsistent spacing in function parameters"

> Attorney: This is **P3 (Nice-to-Have)**. It's a minor style issue that should be fixed via linting tools. Track for tech debt cleanup.

## Output Format

When reporting issues, use this format:

```markdown
### Issue #[number]: [Title]
**Severity:** P1 (Critical) | P2 (Important) | P3 (Nice-to-Have)
**Category:** Security | Performance | Architecture | Code Quality
**File:** [path/to/file.ts]
**Lines:** [line numbers]

**Problem:**
[Clear description of the issue]

**Impact:**
[What happens if this isn't fixed]

**Fix:**
[Specific steps to resolve]

**Related:** [Link to documentation or similar issues]
```

## Success Criteria
- [ ] All issues classified with P1/P2/P3
- [ ] P1 issues block merge
- [ ] P2 issues tracked in todos
- [ ] P3 issues documented in backlog

## Integration Points

- **Code Review:** Apply severity to all findings
- **Triage Workflow:** Create todos based on severity
- **PR Templates:** Include severity in review comments
- **Quality Gates:** Block on P1, warn on P2, track P3
