---
name: review-for-quality
description: Comprehensive code quality review through expert perspectives (Sandi Metz, Jeremy Evans, Kent Beck, Avdi Grimm, Gary Bernhardt). Updates docs/quality_review.md with findings.
agent: Plan
allowed-tools: Read, Grep, Glob
---

# Code Quality Review

Critically review this Ruby codebase for best-practices, idiom use, and overall quality through the eyes of Ruby experts.

## Expert Perspectives

Analyze the codebase through these 5 perspectives:

1. **Sandi Metz** (POODR principles)
   - Single Responsibility Principle
   - Small, focused methods (< 5 lines ideal)
   - Classes with single purpose
   - DRY principle
   - Clear dependencies
   - High test coverage

2. **Jeremy Evans** (Sequel maintainer)
   - Proper Sequel usage patterns (datasets over raw SQL)
   - Database performance optimization
   - Schema design best practices
   - Connection management
   - Transaction safety
   - Sequel plugins and extensions

3. **Kent Beck** (TDD, Simple Design)
   - Test-first design
   - Simple solutions over complex ones
   - Revealing intent through naming
   - Clear boundaries between components
   - Testability without mocks
   - Command-Query Separation

4. **Avdi Grimm** (Confident Ruby)
   - Confident code (no defensive nil checks everywhere)
   - Tell, don't ask principle
   - Null object pattern
   - Meaningful return values (not nil)
   - Duck typing
   - Result objects over exceptions

5. **Gary Bernhardt** (Boundaries, Fast Tests)
   - Functional core, imperative shell
   - Fast unit tests (no I/O in logic)
   - Clear boundaries between layers
   - Separation of I/O and pure logic
   - Value objects
   - Immutable data structures

## Review Process

1. **Explore the codebase systematically:**
   - `lib/claude_memory/` (all subdirectories)
   - Identify the largest files (> 500 lines)
   - Find code duplication patterns
   - Check architecture and design patterns

2. **Document EVERY issue found** with:
   - Priority: 🔴 Critical / High / 🟡 Medium / Low
   - Specific file:line references
   - Which expert's principle is violated
   - Concrete improvement suggestions with code examples
   - Estimated effort to fix

3. **Track progress:**
   - Compare with previous review date
   - Show metrics (lines of code, god objects, etc.)
   - Identify what's been fixed since last review
   - Highlight new issues that have emerged

4. **Provide actionable recommendations:**
   - High priority items (this week)
   - Medium priority items (next week)
   - Low priority items (later)
   - Quick wins (can do today)

## Output Format

Update `docs/quality_review.md` with:

### Structure:
```
# Code Quality Review - Ruby Best Practices

**Review Date:** [YYYY-MM-DD]
**Previous Review:** [YYYY-MM-DD]

## Executive Summary
[Progress since last review + new critical issues]

## 1. Sandi Metz Perspective
### What's Been Fixed ✅
### Critical Issues 🔴
### Medium Issues 🟡

## 2. Jeremy Evans Perspective
[Same structure]

## 3. Kent Beck Perspective
[Same structure]

## 4. Avdi Grimm Perspective
[Same structure]

## 5. Gary Bernhardt Perspective
[Same structure]

## 6. General Ruby Idioms
[Style and convention issues]

## 7. Positive Observations
[What's working well]

## 8. Priority Refactoring Recommendations
### High Priority (This Week)
### Medium Priority (Next Week)
### Low Priority (Later)

## 9. Conclusion
[Summary + risk assessment + next steps]

## Appendix A: Metrics Comparison
[Table showing progress]

## Appendix B: Quick Wins
[Things that can be done immediately]

## Appendix C: File Size Report
[Largest files identified]
```

## Important Notes

- Be thorough and critical - find real issues to improve
- Every issue needs a specific file:line reference
- Provide code examples for suggested fixes
- Don't just praise - identify concrete problems
- Compare metrics with previous review date
- Estimate effort for each recommendation (days)

## Success Criteria

The review is complete when:
- `docs/quality_review.md` is updated with dated findings
- Every issue has file:line references
- Concrete code examples are provided
- Metrics comparison table is included
- Actionable priorities are listed with time estimates
