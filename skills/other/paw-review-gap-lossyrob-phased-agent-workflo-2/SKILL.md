---
name: paw-review-gap
description: Systematically identifies gaps in correctness, safety, testing, and maintainability, categorizing findings by severity.
---

# Gap Analysis Activity Skill

Systematically identify gaps and issues across correctness, safety, testing, and maintainability dimensions, categorizing findings as Must/Should/Could based on evidence.

> **Reference**: Follow Core Review Principles from `paw-review-workflow` skill.

## Responsibilities

- Identify correctness issues (logic errors, edge cases, error handling)
- Find safety and security gaps (input validation, permission checks)
- Assess test coverage quantitatively (if reports available) and qualitatively (always)
- Evaluate maintainability (code duplication, pattern adherence, documentation)
- Categorize all findings as Must/Should/Could with evidence
- Recognize positive observations (mentoring value)
- Produce comprehensive GapAnalysis.md artifact

## Non-Responsibilities

- System-wide impact analysis (handled by paw-review-impact)
- Generating review comments (Output stage skills)
- Workflow orchestration (handled by workflow skill)

## Prerequisites

Verify these artifacts exist at `.paw/reviews/<identifier>/`:
- Phase 1: `ReviewContext.md`, `CodeResearch.md`, `DerivedSpec.md`
- Phase 2: `ImpactAnalysis.md`

If any artifact is missing, report the blocker and do not proceed.

## Step 1: Correctness Analysis

Identify logic and implementation errors:

### Logic Anomalies

- Incorrect conditional logic (wrong operators, inverted conditions)
- Off-by-one errors in loops or array access
- Race conditions or concurrency issues
- State management inconsistencies

### Edge Case Handling

- Missing null/undefined checks
- Empty array/object handling gaps
- Boundary value issues (min/max, zero, negative)
- String edge cases (empty, very long, special characters)

### Error Handling Gaps

- Missing try/catch blocks for operations that can fail
- Error swallowing without logging
- Unchecked promise rejections
- Missing error propagation

### State Transitions

- Invalid state transitions allowed
- Missing state validation
- Inconsistent state updates

### Cross-Repository Consistency

When reviewing PRs across multiple repositories, also check:

**Version Consistency:**
- Package versions compatible across repos (no conflicting dependency ranges)
- Shared type definitions match (same version of `@types/` packages)
- API version expectations aligned

**Coordinated Changes:**
- API changes in one repo have corresponding consumer updates in other repos
- Schema changes propagated to all consumers
- Missing coordinated updates flagged as gaps

**Timing Dependencies:**
- Deployment order matters (provider must deploy before consumer)
- Feature flag coordination required
- Database migration sequences across repos

**Detection:**
Cross-repo consistency applies when:
- Multiple artifact directories exist (`.paw/reviews/PR-<number>-<repo-slug>/`)
- ReviewContext.md contains `related_prs` entries
- ImpactAnalysis.md contains Cross-Repository Dependencies section

**Output:**
Add "Cross-Repository Gaps" subsection in GapAnalysis.md with coordinated change issues.

### Output

Correctness findings with file:line references, issue descriptions, and evidence

## Step 2: Safety & Security Analysis

Find security vulnerabilities and risks:

### Input Validation

- User input reaching sensitive operations without validation
- Missing sanitization of user-provided data
- Type coercion vulnerabilities
- Length/size checks missing

### Permission & Authorization

- Missing permission checks on operations
- Auth middleware bypassed
- Role-based access control gaps
- Resource ownership checks missing

### Data Exposure

- Sensitive data logged or returned in responses
- PII handling without protection
- Secrets in code or configuration
- Overly broad data access

### Injection Risks

- SQL injection (raw queries with user input)
- XSS (unescaped user content)
- Command injection
- Path traversal

### Cryptography

- Weak algorithms or key sizes
- Missing encryption for sensitive data
- Insecure random number generation
- Certificate validation disabled

### Output

Safety/security findings with severity, file:line references, and concrete risks

## Step 3: Testing Analysis

Assess test coverage and quality:

### Quantitative Coverage (if available)

- Look for `coverage/summary.json`, `lcov.info`, `coverage.xml` in repo
- Parse JSON: `coverage.summary.total.lines.pct`, `branches.pct`, `functions.pct`
- Parse LCOV: `LF`, `LH` (lines found/hit), `BRF`, `BRH` (branches)
- If absent: Note unavailable and proceed with qualitative

### Qualitative Coverage

**Depth Assessment:**
- Do tests verify edge cases (null, empty, boundary values)?
- Are error paths tested (exceptions, failures)?
- Are different code branches exercised?
- Do tests verify boundary conditions?

**Breadth Assessment:**
- Are integration points tested?
- Do tests cover user scenarios end-to-end?
- Are cross-component interactions tested?
- Is there happy path AND sad path coverage?

**Quality Assessment:**
- Do tests verify actual behavior vs trivially pass?
- Are assertions meaningful (not just "doesn't crash")?
- Do tests check side effects and state changes?
- Are tests clear about what they're verifying?

### Test Effectiveness

- Will these tests actually fail when the code is broken?
- Are assertions meaningful or trivially passing?
- Is there risk of false positives (tests fail when code is correct)?
- Do tests verify behavior or just exercise code?

### Test Maintainability

- Tests are code too - are they maintainable?
- Are tests overly complex or fragile?
- Do tests have good names explaining what they verify?

### Test Design

- Are tests separated appropriately between test methods?
- Do tests make simple, clear assertions?
- Are tests testing one thing or too many things?

### Heuristics for Test Quality

- Flag tests with no assertions (or only assert true)
- Note overly complex test setup (may indicate design issue)
- Check if test names clearly describe what's being tested
- Identify tests that would pass even with bugs in code

### Gap Detection

Compare code changes to test changes:
```
changed_files - test_diff_files → potential coverage gap
```

Count new conditionals/branches:
- Each new `if/else` adds branches to cover
- Each new `switch/case` adds cases to test
- Each new loop adds edge cases (empty, one, many)

### Specific Test Gaps

- New functions without corresponding tests
- Modified functions without updated tests
- New error handling paths untested
- New branches/conditions without branch tests

### Output

Test coverage section with:
- Quantitative metrics (if available)
- Qualitative depth/breadth/quality assessment
- Specific coverage gaps with file:line references
- Overall assessment of test adequacy

## Step 4: Maintainability Analysis

Evaluate code quality and long-term maintenance:

### Code Duplication

- Repeated logic that could be extracted
- Copy-pasted code blocks
- Similar patterns across files without shared abstraction

### Pattern Adherence

- Divergence from established patterns (from CodeResearch.md)
- Inconsistent naming conventions
- Architectural patterns violated
- Style guide deviations

### Code Clarity

- Confusing variable/function names
- Complex nested logic without explanation
- Magic numbers or strings without constants
- Unclear control flow

### Documentation Gaps

- Complex algorithms without comments
- Public APIs without documentation
- Unclear function purposes
- Missing usage examples for non-obvious code

### User-Facing Documentation

- Do README files need updates?
- Are API docs updated for public interface changes?
- Do new features have usage documentation?

### Orphaned Documentation

- When code is deleted, is related documentation also removed?
- Are there docs referencing removed code/features?
- Do code comments reference deleted functions?

### Comment Quality Assessment

**WHY vs WHAT:**
- Do comments explain WHY not WHAT?
- Are comments necessary or is code self-explanatory?
- Should code be simplified instead of commented?
- Are comments providing value beyond what code shows?

**Comment Anti-Patterns:**
- Comments explaining what code does (code should be clearer)
- Commented-out code (should be removed, git history preserves it)
- Redundant comments (restating obvious code)
- Outdated comments (contradicting current code)

**Comment Best Practices:**
- Complex algorithms explained (regex, mathematical operations)
- Reasoning behind non-obvious decisions
- Gotchas or surprising behavior warnings
- External context (why workaround needed, ticket references)

**Heuristics:**
- Flag comments that just restate code: `// set x to 5` for `x = 5`
- Flag long comment blocks on simple code (simplify code instead)
- Note when complex code lacks explanatory comments
- Check if comments explain WHY for non-obvious decisions

### Output

Maintainability findings with improvement suggestions, including comment quality assessment

## Step 5: Performance Analysis

Identify inefficient code patterns:

### Algorithmic Inefficiency

- Worse complexity than baseline (O(n²) when O(n) was used before)
- Unnecessary iterations or transformations
- Inefficient data structure choices

### Resource Usage

- Missing indexes for database queries
- Lack of caching for repeated operations
- Unbounded operations (no pagination, no limits)
- Memory leaks or excessive allocations

**Note:** Deep performance analysis was done in Impact Analysis. Here, focus on obvious inefficiencies and code-level improvements.

### Output

Performance gap findings (if any obvious issues exist)

## Step 6: Categorize Findings

Apply Must/Should/Could categorization:

### Must - Correctness/Safety/Security with Concrete Impact

- Null pointer / undefined access that will crash
- Unchecked user input reaching SQL queries or file operations
- Permission bypass allowing unauthorized actions
- Auth weakening exposing sensitive operations
- Data corruption risk (race condition, bad state transition)
- Critical logic errors breaking core functionality

**Evidence Required:** Concrete impact (not just "could cause issues")

### Should - Quality/Completeness Improvements

- Missing tests for new code paths (but no critical path untested)
- Missing error handling for expected failures
- Code needing refactor or documentation for clarity
- Breaking changes needing migration plan (from ImpactAnalysis.md)
- Performance degradation in non-critical paths
- Pattern violations reducing maintainability
- Over-engineering (solving future vs current problems, unnecessary abstractions)

**Rationale Required:** Why this improves robustness or quality

### Over-engineering Detection

- Is code more generic than current requirements need?
- Are abstractions solving problems that don't exist yet?
- Is developer building for speculative future use cases?
- Are there configuration options that aren't actually needed?
- Is complexity added "just in case" vs for actual requirements?

**Guiding Principle:** Solve the problem that needs to be solved now, not the problem that might need to be solved in the future.

**Heuristics:**
- Flag generic interfaces with only one implementation
- Note parameterization beyond current use cases
- Identify "pluggable" architectures without multiple plugins
- Check for abstraction layers without clear current need

**Categorization:** Should (adds maintenance burden) or Could (suggest simplifying)

### Could - Optional Enhancements

- Code duplication that could be extracted (but not causing bugs)
- Naming improvements for marginal clarity gains
- Additional edge case tests beyond common scenarios
- Documentation enhancements for non-critical code
- Style consistency improvements

**Benefit Required:** Clear benefit stated (not just "nice to have")

### Categorization Rules

- **Don't inflate:** Style issues are not Must without concrete impact
- **Evidence-based:** Every Must/Should needs file:line + rationale
- **Informed by baseline:** Compare to patterns in CodeResearch.md
- **Severity != Category:** High-severity Should is not auto-promoted to Must

## Step 7: Identify Positive Observations

Recognize what the developer did well (mentoring value):

### Good Practices to Commend

- Well-designed code that's easy to understand
- Comprehensive test coverage (especially edge cases)
- Clear, meaningful naming
- Proper error handling and validation
- Good performance considerations
- Following established patterns well
- Clear documentation and comments
- Thoughtful architectural decisions

### Recognition Guidelines

- Be specific about what was done well (not generic praise)
- Highlight practices that should be emulated
- Note when developer addressed difficult problems elegantly
- Recognize attention to edge cases, testing, or maintainability
- Acknowledge when feedback from previous reviews was incorporated

### Output

Positive observations to include in GapAnalysis.md before critical findings

## Step 8: Style & Conventions Analysis

Evaluate adherence to style guidelines:

### Style Guide Compliance

- Is code following project style guide? (language-specific)
- Are there style violations that should be fixed?
- Are style preferences (vs requirements) marked as "Nit:"?

### Mixed Changes Anti-pattern

- Are style changes mixed with functional changes?
- Should formatting/style be in separate commit/PR?
- Note: "Makes it hard to see what is being changed"

### Style vs Preference

- Style guide requirements = Must/Should fix
- Personal preferences = "Nit:" (don't block on these)
- When no rule exists: maintain consistency with existing code

### Heuristics

- Check for common style violations (indentation, naming conventions)
- Identify large formatting changes mixed with logic changes
- Note when new code diverges from style guide
- Suggest extracting pure refactoring to separate PR if large

### Output

Style findings categorized as:
- Must/Should: Style guide violations
- Nit: Stylistic preferences that would improve code but aren't mandatory

## Step 9: Generate GapAnalysis.md

Create comprehensive gap analysis artifact at `.paw/reviews/<identifier>/GapAnalysis.md`:

```markdown
---
date: <timestamp>
git_commit: <head SHA>
branch: <head branch>
repository: <repo>
topic: "Gap Analysis for <PR Title or Branch>"
tags: [review, gaps, findings]
status: complete
---

# Gap Analysis for <PR Title or Branch>

## Summary

**Must Address**: X findings (correctness, safety, security)
**Should Address**: Y findings (quality, completeness)
**Could Consider**: Z findings (optional improvements)

<Brief overview of scope and key concerns>

---

## Positive Observations

<List of things developer did well, with specific examples>

- ✅ **Excellent test coverage**: Added comprehensive edge case tests for null, empty, and boundary conditions in `module.test.ts`
- ✅ **Clear error handling**: Proper validation with helpful error messages in `validator.ts:45-60`
- ✅ **Good performance consideration**: Used efficient algorithm avoiding nested loops in `processor.ts:123`
- ✅ **Well-designed architecture**: Clean separation of concerns in new module structure
- ✅ **Clear naming**: Functions and variables have descriptive, meaningful names

---

## Must Address (Correctness/Safety/Security)

### Finding M1: <Clear, Specific Title>
**File**: `path/to/file.ext:123-130`
**Category**: Correctness | Safety | Security
**Evidence**: <Exact code reference showing the issue>
**Issue**: <Clear description of what's wrong>
**Impact**: <What could go wrong - concrete consequences>
**Suggestion**: <Specific fix or approach to resolve>
**Related**: <IDs of related findings, if any>

### Finding M2: <Title>
[... same structure ...]

---

## Should Address (Quality/Completeness)

### Finding S1: <Title>
**File**: `path/to/file.ext:456-460`
**Category**: Testing | Maintainability | Performance
**Evidence**: <Code reference>
**Issue**: <What's missing or could be better>
**Rationale**: <Why this matters for code quality or robustness>
**Suggestion**: <Recommended improvement>
**Related**: <IDs of related findings, if any>

### Finding S2: <Title>
[... same structure ...]

---

## Could Consider (Optional Improvements)

### Finding C1: <Title>
**File**: `path/to/file.ext:789-795`
**Category**: Maintainability | Testing | Documentation
**Observation**: <What could be enhanced>
**Benefit**: <How this would help (clarity, future changes, etc.)>
**Suggestion**: <Optional enhancement approach>

### Finding C2: <Title>
[... same structure ...]

---

## Test Coverage Assessment

### Quantitative Metrics

**Note:** Coverage report <available|not available>

<If available:>
- Line Coverage: X%
- Branch Coverage: Y%
- Function Coverage: Z%

<If not available:>
Quantitative metrics not available. Qualitative analysis below.

### Qualitative Analysis

**Depth:**
<Do tests verify edge cases, error paths, boundary conditions?>

**Breadth:**
<Do tests cover integration points, user scenarios, cross-component interactions?>

**Quality:**
<Do tests verify behavior vs trivially pass? Are assertions meaningful?>

### Specific Coverage Gaps

<List uncovered code paths or missing test scenarios with file:line references>

**Overall Test Assessment:** Adequate | Needs Improvement | Critical Gaps

---

## Scope Assessment

**Total Findings:** X Must + Y Should + Z Could = Total
**Critical Issues:** <count of Must findings>
**Quality Improvements:** <count of Should findings>
**Baseline Comparison:** <Are patterns from CodeResearch.md followed?>
```

## Guardrails

### Evidence-Based Categorization

- Every finding must have file:line + concrete evidence
- Must findings require demonstrable impact, not hypothetical
- Don't inflate severity without justification

### Not Inflated

- Style preferences are Could, not Must
- Lack of tests for non-critical code is Should, not Must
- Naming issues are Could unless causing real confusion

### Informed by Baseline

- Use CodeResearch.md to judge pattern consistency
- Compare to established conventions in codebase
- Note when new code diverges from existing patterns

### Coverage Context

- Always note when coverage reports unavailable
- Qualitative analysis still valuable without metrics
- Don't penalize for missing coverage tooling

### Batching Preview

- Identify related findings that share root causes
- Note where multiple findings could be addressed together
- This helps Output stage batch feedback efficiently

## Validation Checklist

Before completing, verify:
- [ ] All findings have file:line references with evidence
- [ ] Must findings have concrete impact statements (not speculation)
- [ ] Should findings have clear rationale for why they matter
- [ ] Could findings have stated benefits
- [ ] Positive observations identified and documented
- [ ] Test coverage assessed (quantitatively if available, qualitatively always)
- [ ] Test effectiveness and maintainability evaluated
- [ ] Comment quality assessed (WHY vs WHAT, necessity)
- [ ] Over-engineering detection applied
- [ ] Style guide adherence checked with "Nit:" labeling for preferences
- [ ] User-facing documentation completeness verified
- [ ] Orphaned documentation identified
- [ ] Categorization not inflated (style issues not promoted to Must)
- [ ] Baseline patterns from CodeResearch.md considered
- [ ] Related findings identified for batching
- [ ] GapAnalysis.md artifact generated with all required sections

## Completion Response

```
Activity complete.
Artifact saved: .paw/reviews/<identifier>/GapAnalysis.md
Status: Success

Key findings:
- Positive observations: X good practices identified
- Must-address: Y correctness/safety/security findings
- Should-address: Z quality/completeness findings
- Could-consider: W optional improvements
- Test coverage: [Adequate | Needs Improvement | Critical Gaps]
```
