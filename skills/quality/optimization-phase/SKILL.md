---
name: optimization-phase
description: Validates production readiness through performance benchmarking, accessibility audits, security reviews, and code quality checks. Use after implementation phase completes, before deployment, or when conducting quality gates for features. (project)
---

<objective>
Production readiness validation through systematic quality gates. Ensures features meet performance targets, accessibility standards (WCAG 2.1 AA), security requirements, and code quality thresholds before deployment.

This skill orchestrates the /optimize phase, which runs after /implement and before /preview in the deployment workflow.

Inputs: Implemented code (from /implement), spec.md (success criteria)
Outputs: optimization-report.md, code-review-report.md
Expected duration: 1-2 hours
</objective>

<quick_start>
Execute optimization quality gates systematically:

1. Performance Benchmarking - API p50 <200ms, p95 <500ms, page load <2s
2. Accessibility Audit - WCAG 2.1 AA compliance (if UI feature)
3. Security Review - npm audit, dependency scanning, OWASP top 10
4. Code Quality Review - DRY violations <3, test coverage ≥80%
5. Generate Reports - optimization-report.md + code-review-report.md

Key principle: All blocking quality gates must pass before deployment.
</quick_start>

<prerequisites>
Before beginning optimization:
- Implementation phase completed (all tasks done or blocked)
- All tests passing (CI pipeline green)
- Code committed to feature branch (git status clean)
- spec.md contains performance targets and success criteria

If prerequisites not met, return to /implement phase.
</prerequisites>

<workflow>
<step number="1">
**Performance Benchmarking**

Validate API response times and page load performance against spec.md targets.

**API Performance Testing**:

```bash
# Measure API endpoint response times (10 requests)
for i in {1..10}; do
  curl -w "%{time_total}\n" -o /dev/null -s "http://localhost:3000/api/endpoint"
done | sort -n

# Calculate p50 (median): 5th value
# Calculate p95 (95th percentile): 10th value
```

**Page Load Testing**:

```bash
# Run Lighthouse CI for page load metrics
npm install -g @lhci/cli
lhci autorun --url=http://localhost:3000

# Check metrics:
# - First Contentful Paint (FCP): <1.8s
# - Largest Contentful Paint (LCP): <2.5s
# - Time to Interactive (TTI): <3.8s
```

**Targets from spec.md**:

- API p50 (median): <200ms
- API p95 (95th percentile): <500ms
- Page load (initial): <2 seconds
- Time to Interactive (TTI): <3 seconds

**Blocking**: If performance targets not met, optimization required before deployment.

See resources/performance-benchmarking.md for detailed testing procedures.
</step>

<step number="2">
**Accessibility Audit (UI Features)**

Validate WCAG 2.1 AA compliance for all UI changes.

**Lighthouse CI Audit**:

```bash
# Run Lighthouse accessibility audit
lhci autorun --collect.settings.onlyCategories=accessibility

# Target score: ≥95/100
```

**axe-core Validation**:

```bash
# Install axe-core DevTools extension
# Or use axe CLI:
npm install -g @axe-core/cli
axe http://localhost:3000 --tags wcag2aa
```

**WCAG 2.1 AA Requirements**:

- Color contrast ≥4.5:1 (text), ≥3:1 (UI components)
- Keyboard navigation (all interactive elements accessible)
- Screen reader compatibility (ARIA labels, semantic HTML)
- Focus indicators visible (outline, border, background change)

**Blocking** (if UI feature): All WCAG 2.1 AA violations must be fixed.

**Skip if**: No UI changes in this feature (backend/API only).

See resources/accessibility-audit.md for comprehensive checklist.
</step>

<step number="3">
**Security Review**

Scan for vulnerabilities in dependencies and code.

**Dependency Vulnerability Scan**:

```bash
# npm audit for Node.js projects
npm audit --audit-level=moderate

# Check for critical and high severity vulnerabilities
# Fix: npm audit fix (or manual upgrade)
```

**OWASP Top 10 Checks**:

- SQL Injection: Parameterized queries, no string concatenation
- XSS: Input sanitization, output encoding
- CSRF: CSRF tokens on state-changing endpoints
- Authentication: Secure password hashing (bcrypt), JWT validation
- Sensitive Data Exposure: No secrets in code/logs, HTTPS enforced

**Secret Scanning**:

```bash
# Check for accidentally committed secrets
git secrets --scan

# Or use gitleaks:
gitleaks detect --source . --verbose
```

**Blocking**: Critical and high severity vulnerabilities must be fixed.

See resources/security-review.md for OWASP top 10 checklist.
</step>

<step number="4">
**Code Quality Review**

Validate code follows DRY/KISS principles and test coverage standards.

**Test Coverage Check**:

```bash
# Run coverage report
npm run test:coverage

# Target: ≥80% coverage (unit + integration)
```

**DRY Violations Check**:

```bash
# Manual review for code duplication
# Or use jsinspect (JavaScript):
npm install -g jsinspect
jsinspect src/

# Target: <3 instances of code duplication
```

**KISS Principle Validation**:

- Functions ≤50 lines (complex functions split)
- Cyclomatic complexity <10 (no deeply nested logic)
- No premature optimization (YAGNI principle)

**Code Review Checklist**:

- [ ] No magic numbers (constants extracted)
- [ ] Descriptive variable/function names
- [ ] Error handling present (try/catch, error boundaries)
- [ ] No commented-out code (dead code removed)
- [ ] Consistent code style (linter passing)

**Blocking if**: Test coverage <80% OR >5 DRY violations OR critical complexity issues.

See resources/code-quality-review.md for complete checklist.
</step>

<step number="5">
**Generate Reports**

Create optimization-report.md and code-review-report.md.

**optimization-report.md format**:

```markdown
# Optimization Report: [Feature Name]

**Date**: 2025-11-19
**Feature**: specs/NNN-slug

## Performance Results

### API Performance

- GET /api/users: p50=145ms ✅, p95=320ms ✅
- POST /api/orders: p50=230ms ❌, p95=580ms ❌ (exceeds p95 target)

### Page Load Performance

- Homepage: LCP=1.9s ✅, TTI=2.8s ✅
- Dashboard: LCP=3.2s ❌ (exceeds target)

## Accessibility Audit (WCAG 2.1 AA)

- Lighthouse score: 98/100 ✅
- axe-core violations: 0 ✅

## Security Review

- npm audit: 0 critical, 0 high ✅
- OWASP top 10: All checks passed ✅
- Secret scanning: No secrets detected ✅

## Code Quality

- Test coverage: 85% ✅
- DRY violations: 2 ✅
- Complexity: All functions <10 ✅

## Blocking Issues

- POST /api/orders p95 exceeds target (580ms vs 500ms)
- Dashboard LCP exceeds target (3.2s vs 2.5s)

## Recommendations

- Add caching to /api/orders endpoint (reduce p95 to <500ms)
- Lazy load dashboard widgets (reduce LCP to <2.5s)
```

**code-review-report.md format**:

```markdown
# Code Review Report: [Feature Name]

**Date**: 2025-11-19
**Reviewer**: optimization-phase skill

## Summary

- Files reviewed: 15
- Issues found: 7 (3 critical, 4 minor)

## Critical Issues

1. [src/api/orders.ts:45] Missing input validation on order.total
2. [src/components/Dashboard.tsx:89] Potential memory leak (event listener not removed)
3. [src/services/AuthService.ts:23] Password logged in plaintext (security risk)

## Minor Issues

1. [src/utils/formatDate.ts:12] Magic number 1000 should be constant
2. [src/components/UserCard.tsx:34] Unused import (React.Fragment)

## Recommendations

- Fix all critical issues before deployment
- Consider refactoring Dashboard.tsx (180 lines, split into smaller components)
```

Update state.yaml: `optimization.status = completed`

See resources/report-generation.md for report templates.
</step>
</workflow>

<validation>
After optimization phase, verify:

- All blocking quality gates passed (performance, accessibility, security, code quality)
- optimization-report.md generated with all sections completed
- code-review-report.md generated with issues documented
- Critical issues fixed (blocking deployment)
- Minor issues documented (can defer or fix)
- state.yaml updated (optimization.status = completed)

If blocking issues found, return to /implement to fix, then re-run /optimize.
</validation>

<quality_gates>
<gate name="pre_flight" blocking="true">
**Pre-Flight Validation** (Must pass)

Environment checks:

- [ ] Environment variables configured (.env.production exists)
- [ ] Production build succeeds (npm run build passes)
- [ ] No TypeScript/lint errors (npm run type-check passes)
- [ ] All tests passing (npm test green)

If any check fails, fix before proceeding to quality gates.
</gate>

<gate name="performance" blocking="true">
**Performance Gate** (Must meet targets)

API performance:

- [ ] p50 (median) <200ms
- [ ] p95 (95th percentile) <500ms

Page load performance:

- [ ] Initial load <2 seconds
- [ ] Time to Interactive <3 seconds

If targets not met, profile and optimize before deployment.
</gate>

<gate name="accessibility" blocking="conditional">
**Accessibility Gate** (Blocking if UI feature)

WCAG 2.1 AA compliance:

- [ ] Lighthouse accessibility score ≥95/100
- [ ] axe-core violations: 0 (WCAG 2.1 AA)
- [ ] Keyboard navigation functional
- [ ] Screen reader compatible

Skip if: Backend/API feature with no UI changes.
</gate>

<gate name="security" blocking="true">
**Security Gate** (Must be clean)

Vulnerability scanning:

- [ ] npm audit: 0 critical, 0 high severity
- [ ] OWASP top 10 checks passed
- [ ] No secrets in code/logs (gitleaks clean)

If critical/high vulnerabilities found, fix or accept risk (document).
</gate>

<gate name="code_quality" blocking="conditional">
**Code Quality Gate** (Blocking if critical)

Quality standards:

- [ ] Test coverage ≥80% (unit + integration)
- [ ] DRY violations <3 instances
- [ ] Cyclomatic complexity <10 (all functions)

Blocking if: Coverage <80% OR >5 DRY violations OR complexity >15.
</gate>
</quality_gates>

<anti_patterns>
<pitfall name="skipping_accessibility">
**❌ Don't**: Skip accessibility audit for "simple" UI changes
**✅ Do**: Always run WCAG 2.1 AA validation for ANY UI modification

**Why**: Even small UI changes can introduce accessibility violations (color contrast, keyboard nav, screen readers). WCAG compliance is non-negotiable for production.

**Example** (bad):

```
"This is just a button color change, no need for accessibility audit"
[Ships button with insufficient color contrast, fails WCAG 2.1 AA]
```

**Example** (good):

```
"Button color changed from blue to green"
→ Run Lighthouse accessibility audit
→ Check color contrast ratio (4.5:1 minimum)
→ Verify keyboard focus indicator visible
→ Deploy with confidence
```

</pitfall>

<pitfall name="ignoring_performance_regressions">
**❌ Don't**: "Performance is good enough" without measuring
**✅ Do**: Always benchmark against documented targets in spec.md

**Why**: Performance regressions accumulate over time. Without benchmarking, small slowdowns compound into major UX issues.

**Example** (bad):

```
"Dashboard feels fast to me, ship it"
[Reality: LCP=5s, users complain about slow load]
```

**Example** (good):

```
Run Lighthouse: LCP=3.2s (target: 2.5s)
Identify bottleneck: Large uncompressed image
Fix: Lazy load + WebP format
Re-test: LCP=1.8s ✅
Deploy
```

</pitfall>

<pitfall name="deferring_critical_security">
**❌ Don't**: Defer critical security vulnerabilities "for later"
**✅ Do**: Block deployment until critical/high vulnerabilities fixed

**Why**: Security vulnerabilities in production are exploited quickly. Deferring fixes creates risk.

**Example** (bad):

```
npm audit: 2 critical, 5 high vulnerabilities
"We'll fix these in the next sprint"
[Ships vulnerable dependencies, gets hacked]
```

**Example** (good):

```
npm audit: 2 critical, 5 high vulnerabilities
BLOCK deployment
Run: npm audit fix
Or: Manually upgrade vulnerable dependencies
Re-test: 0 critical, 0 high
Deploy safely
```

</pitfall>

<pitfall name="accepting_low_coverage">
**❌ Don't**: Accept <80% test coverage with "we'll add tests later"
**✅ Do**: Block deployment if coverage below threshold

**Why**: Low coverage = high risk of bugs in production. "Later" rarely happens.

**Example** (bad):

```
Test coverage: 45%
"Core functionality is tested, ship it"
[Untested edge cases cause production bugs]
```

**Example** (good):

```
Test coverage: 45% ❌
BLOCK deployment
Write missing tests (focus on critical paths)
Re-run: 82% ✅
Deploy with confidence
```

</pitfall>

<pitfall name="manual_optimization_only">
**❌ Don't**: Rely only on manual code review for optimization
**✅ Do**: Use automated tools (Lighthouse, npm audit, coverage reports)

**Why**: Manual reviews miss issues that automated tools catch instantly.

**Example** (bad):

```
"I reviewed the code, looks good"
[Ships with 12 accessibility violations, 8 security issues]
```

**Example** (good):

```
Lighthouse: 15 accessibility violations
npm audit: 8 vulnerabilities
Coverage: 67%
Fix all blocking issues
Re-run all tools
Deploy when green
```

</pitfall>
</anti_patterns>

<best_practices>
<practice name="automate_quality_gates">
Automate quality gates in CI pipeline:

```yaml
# .github/workflows/optimize.yml
- run: npm run test:coverage
  # Fail if <80%
- run: npm audit --audit-level=high
  # Fail if critical/high vulnerabilities
- run: lhci autorun
  # Fail if performance/accessibility targets not met
```

Result: Quality gates enforced automatically, no human error
</practice>

<practice name="performance_budgets">
Set performance budgets in spec.md success criteria:

```markdown
## Success Criteria

**Performance**:

- API p50 <200ms, p95 <500ms
- Page load <2s, TTI <3s
- Lighthouse performance score ≥90/100
```

Result: Clear, measurable targets validated during /optimize
</practice>

<practice name="accessibility_first">
Test accessibility early and often:

- During /implement (run axe-core locally)
- During /optimize (full WCAG 2.1 AA audit)
- In CI pipeline (automated Lighthouse checks)

Result: Accessibility violations caught early, cheaper to fix
</practice>

<practice name="security_as_blocker">
Treat critical/high security vulnerabilities as deployment blockers:

- Never defer critical vulnerabilities
- Fix or accept risk (with documented justification)
- Re-scan after fixes to verify clean

Result: No vulnerable code in production
</practice>

<practice name="comprehensive_reports">
Generate detailed optimization-report.md and code-review-report.md:

- Document all metrics (performance, security, accessibility, quality)
- List blocking issues clearly
- Provide actionable recommendations
- Track improvements over time

Result: Audit trail for deployment decisions, learning from past optimizations
</practice>
</best_practices>

<success_criteria>
Optimization phase complete when:

- [ ] All blocking quality gates passed (pre-flight, performance, security, code quality)
- [ ] Accessibility gate passed (if UI feature)
- [ ] optimization-report.md generated with all results
- [ ] code-review-report.md generated with issues documented
- [ ] Critical issues fixed (blocking deployment)
- [ ] Minor issues documented (can defer)
- [ ] state.yaml updated (optimization.status = completed)
- [ ] Ready to proceed to /preview (manual UI/UX testing)

If blocking issues remain, return to /implement to fix, then re-run /optimize.
</success_criteria>

<quality_standards>
**Good optimization**:

- All quality gates automated (CI pipeline enforcement)
- Performance targets met (benchmarked against spec.md)
- Accessibility validated (WCAG 2.1 AA compliance)
- Security clean (0 critical/high vulnerabilities)
- High test coverage (≥80%)
- Comprehensive reports (optimization-report.md + code-review-report.md)

**Bad optimization**:

- Manual-only review (no automated tools)
- Performance not measured (subjective "feels fast")
- Accessibility skipped (ships with violations)
- Security vulnerabilities deferred (critical issues in production)
- Low test coverage (<80%, high bug risk)
- No documentation (no optimization-report.md)
  </quality_standards>

<troubleshooting>
**Issue**: Performance targets not met (p95 >500ms)
**Solution**: Profile endpoint, add caching, optimize database queries, lazy load resources

**Issue**: Accessibility violations detected (WCAG 2.1 AA)
**Solution**: Fix color contrast, add ARIA labels, ensure keyboard navigation, test with screen reader

**Issue**: Critical security vulnerabilities found
**Solution**: Run npm audit fix, manually upgrade dependencies, re-scan until clean

**Issue**: Test coverage below 80%
**Solution**: Write missing tests (focus on critical paths), use test-architect for complex features

**Issue**: DRY violations >3 instances
**Solution**: Extract duplicated code to shared utilities, refactor into reusable functions

**Issue**: Lighthouse performance score <90
**Solution**: Optimize images (WebP, lazy loading), minify JS/CSS, enable compression, use CDN
</troubleshooting>

<reference_guides>
Quality gates (blocking):

- Performance Benchmarking (resources/performance-benchmarking.md) - API p50/p95, page load targets
- Accessibility Audit (resources/accessibility-audit.md) - WCAG 2.1 AA compliance, Lighthouse CI
- Security Review (resources/security-review.md) - npm audit, OWASP top 10, secret scanning

Code quality (blocking if critical):

- Code Quality Review (resources/code-quality-review.md) - DRY, KISS, test coverage
- Code Review Checklist (resources/code-review-checklist.md) - Pre-commit validation

Documentation:

- Report Generation (resources/report-generation.md) - optimization-report.md templates
- Common Mistakes (resources/common-mistakes.md) - Anti-patterns to avoid
- Examples (examples.md) - Good vs bad optimization examples

Next phase:
After optimization completes → /preview (manual UI/UX testing)
</reference_guides>
