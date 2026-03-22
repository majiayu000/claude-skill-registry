---
name: code-review-quality
description: "Conduct context-driven code reviews focusing on quality, testability, and maintainability. Use when reviewing code, providing feedback, or establishing review practices."
category: development-practices
priority: high
tokenEstimate: 900
agents: [qe-quality-analyzer, qe-security-scanner, qe-performance-tester, qe-coverage-analyzer]
implementation_status: optimized
optimization_version: 1.0
last_optimized: 2025-12-02
dependencies: []
quick_reference_card: true
tags: [code-review, feedback, quality, testability, maintainability, pr-review]
trust_tier: 2
validation:
  schema_path: schemas/output.json
  validator_path: scripts/validate-config.json

---

# Code Review Quality

<default_to_action>
When reviewing code or establishing review practices:
1. PRIORITIZE feedback: 🔴 Blocker (must fix) → 🟡 Major → 🟢 Minor → 💡 Suggestion
2. FOCUS on: Bugs, security, testability, maintainability (not style preferences)
3. ASK questions over commands: "Have you considered...?" > "Change this to..."
4. PROVIDE context: Why this matters, not just what to change
5. LIMIT scope: Review < 400 lines at a time for effectiveness

**Quick Review Checklist:**
- Logic: Does it work correctly? Edge cases handled?
- Security: Input validation? Auth checks? Injection risks?
- Testability: Can this be tested? Is it tested?
- Maintainability: Clear naming? Single responsibility? DRY?
- Performance: O(n²) loops? N+1 queries? Memory leaks?

**Critical Success Factors:**
- Review the code, not the person
- Catching bugs > nitpicking style
- Fast feedback (< 24h) > thorough feedback
</default_to_action>

## Quick Reference Card

### When to Use
- PR code reviews
- Pair programming feedback
- Establishing team review standards
- Mentoring developers

### Feedback Priority Levels
| Level | Icon | Meaning | Action |
|-------|------|---------|--------|
| Blocker | 🔴 | Bug/security/crash | Must fix before merge |
| Major | 🟡 | Logic issue/test gap | Should fix before merge |
| Minor | 🟢 | Style/naming | Nice to fix |
| Suggestion | 💡 | Alternative approach | Consider for future |

### Review Scope Limits
| Lines Changed | Recommendation |
|---------------|----------------|
| < 200 | Single review session |
| 200-400 | Review in chunks |
| > 400 | Request PR split |

### What to Focus On
| ✅ Review | ❌ Skip |
|-----------|---------|
| Logic correctness | Formatting (use linter) |
| Security risks | Naming preferences |
| Test coverage | Architecture debates |
| Performance issues | Style opinions |
| Error handling | Trivial changes |

---

## Feedback Templates

### Blocker (Must Fix)
```markdown
🔴 **BLOCKER: SQL Injection Risk**

This query is vulnerable to SQL injection:
```javascript
db.query(`SELECT * FROM users WHERE id = ${userId}`)
```

**Fix:** Use parameterized queries:
```javascript
db.query('SELECT * FROM users WHERE id = ?', [userId])
```

**Why:** User input directly in SQL allows attackers to execute arbitrary queries.
```

### Major (Should Fix)
```markdown
🟡 **MAJOR: Missing Error Handling**

What happens if `fetchUser()` throws? The error bubbles up unhandled.

**Suggestion:** Add try/catch with appropriate error response:
```javascript
try {
  const user = await fetchUser(id);
  return user;
} catch (error) {
  logger.error('Failed to fetch user', { id, error });
  throw new NotFoundError('User not found');
}
```
```

### Minor (Nice to Fix)
```markdown
🟢 **minor:** Variable name could be clearer

`d` doesn't convey meaning. Consider `daysSinceLastLogin`.
```

### Suggestion (Consider)
```markdown
💡 **suggestion:** Consider extracting this to a helper

This validation logic appears in 3 places. A `validateEmail()` helper would reduce duplication. Not blocking, but might be worth a follow-up PR.
```

---

## Review Questions to Ask

### Logic
- What happens when X is null/empty/negative?
- Is there a race condition here?
- What if the API call fails?

### Security
- Is user input validated/sanitized?
- Are auth checks in place?
- Any secrets or PII exposed?

### Testability
- How would you test this?
- Are dependencies injectable?
- Is there a test for the happy path? Edge cases?

### Maintainability
- Will the next developer understand this?
- Is this doing too many things?
- Is there duplication we could reduce?

## Minimum Findings Enforcement
Reviews must meet a minimum weighted finding score of 3.0 (CRITICAL=3, HIGH=2, MEDIUM=1, LOW=0.5, INFORMATIONAL=0.25). If the initial review falls short, run the qe-devils-advocate agent as a meta-reviewer to find additional observations. Every review should have at least 3 actionable observations.

---

## Agent-Assisted Reviews

```typescript
// Comprehensive code review
await Task("Code Review", {
  prNumber: 123,
  checks: ['security', 'performance', 'testability', 'maintainability'],
  feedbackLevels: ['blocker', 'major', 'minor'],
  autoApprove: { maxBlockers: 0, maxMajor: 2 }
}, "qe-quality-analyzer");

// Security-focused review
await Task("Security Review", {
  prFiles: changedFiles,
  scanTypes: ['injection', 'auth', 'secrets', 'dependencies']
}, "qe-security-scanner");

// Test coverage review
await Task("Coverage Review", {
  prNumber: 123,
  requireNewTests: true,
  minCoverageDelta: 0
}, "qe-coverage-analyzer");
```

---

## Agent Coordination Hints

### Memory Namespace
```
aqe/code-review/
├── review-history/*     - Past review decisions
├── patterns/*           - Common issues by team/repo
├── feedback-templates/* - Reusable feedback
└── metrics/*            - Review turnaround time
```

### Fleet Coordination
```typescript
const reviewFleet = await FleetManager.coordinate({
  strategy: 'code-review',
  agents: [
    'qe-quality-analyzer',    // Logic, maintainability
    'qe-security-scanner',    // Security risks
    'qe-performance-tester',  // Performance issues
    'qe-coverage-analyzer'    // Test coverage
  ],
  topology: 'parallel'
});
```

---

## Review Etiquette

| ✅ Do | ❌ Don't |
|-------|---------|
| "Have you considered...?" | "This is wrong" |
| Explain why it matters | Just say "fix this" |
| Acknowledge good code | Only point out negatives |
| Suggest, don't demand | Be condescending |
| Review < 400 lines | Review 2000 lines at once |

---

## Related Skills
- [agentic-quality-engineering](../agentic-quality-engineering/) - Agent coordination
- [security-testing](../security-testing/) - Security review depth
- [refactoring-patterns](../refactoring-patterns/) - Maintainability patterns

---

## Remember

**Prioritize feedback:** 🔴 Blocker → 🟡 Major → 🟢 Minor → 💡 Suggestion. Focus on bugs and security, not style. Ask questions, don't command. Review < 400 lines at a time. Fast feedback (< 24h) beats thorough feedback.

**With Agents:** Agents automate security, performance, and coverage checks, freeing human reviewers to focus on logic and design. Use agents for consistent, fast initial review.
