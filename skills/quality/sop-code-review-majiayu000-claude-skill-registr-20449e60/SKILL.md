---
name: sop-code-review
description: Comprehensive code review workflow coordinating quality, security, performance, and documentation reviewers. 4-hour timeline for thorough multi-agent review.
---

# SOP: Code Review Workflow

Comprehensive code review using specialized reviewers for different quality aspects.

## Timeline: 4 Hours

**Phases**:
1. Automated Checks (30 min)
2. Specialized Reviews (2 hours)
3. Integration Review (1 hour)
4. Final Approval (30 min)

---

## Phase 1: Automated Checks (30 minutes)

### Quick Quality Checks

**Parallel Automated Testing**:

```javascript
// Initialize review swarm
await mcp__ruv-swarm__swarm_init({
  topology: 'star',  // Coordinator pattern for reviews
  maxAgents: 6,
  strategy: 'specialized'
});

// Run all automated checks in parallel
const [lint, tests, coverage, build] = await Promise.all([
  Task("Linter", `
Run linting checks:
- ESLint for JavaScript/TypeScript
- Pylint for Python
- RuboCop for Ruby
- Check for code style violations

Store results: code-review/${prId}/lint-results
`, "reviewer"),

  Task("Test Runner", `
Run test suite:
- Unit tests
- Integration tests
- E2E tests (if applicable)
- All tests must pass

Store results: code-review/${prId}/test-results
`, "tester"),

  Task("Coverage Analyzer", `
Check code coverage:
- Overall coverage > 80%
- New code coverage > 90%
- No critical paths uncovered

Generate coverage report
Store: code-review/${prId}/coverage-report
`, "reviewer"),

  Task("Build Validator", `
Validate build:
- Clean build (no warnings)
- Type checking passes
- No broken dependencies
- Bundle size within limits

Store build results: code-review/${prId}/build-status
`, "reviewer")
]);

// If any automated check fails, stop and request fixes
if (hasFailures([lint, tests, coverage, build])) {
  await Task("Review Coordinator", `
Automated checks failed. Request fixes from author:
${summarizeFailures([lint, tests, coverage, build])}

Store feedback: code-review/${prId}/automated-feedback
`, "pr-manager");
  return; // Stop review until fixed
}
```

**Deliverables**:
- All automated checks passing
- Test results documented
- Coverage report generated

---

## Phase 2: Specialized Reviews (2 hours)

### Parallel Expert Reviews

**Sequential coordination of parallel reviews**:

```javascript
// Spawn specialized reviewers in parallel
const [codeQuality, security, performance, architecture, docs] = await Promise.all([
  Task("Code Quality Reviewer", `
Review for code quality:

**Readability**:
- Clear, descriptive names (variables, functions, classes)
- Appropriate function/method length (< 50 lines)
- Logical code organization
- Minimal cognitive complexity

**Maintainability**:
- DRY principle (no code duplication)
- SOLID principles followed
- Clear separation of concerns
- Proper error handling

**Best Practices**:
- Following language idioms
- Proper use of design patterns
- Appropriate comments (why, not what)
- No code smells (magic numbers, long parameter lists)

Store review: code-review/${prId}/quality-review
Rating: 1-5 stars
`, "code-analyzer"),

  Task("Security Reviewer", `
Review for security issues:

**Authentication & Authorization**:
- Proper authentication checks
- Correct authorization rules
- No privilege escalation risks
- Secure session management

**Data Security**:
- Input validation (prevent injection attacks)
- Output encoding (prevent XSS)
- Sensitive data encryption
- No hardcoded secrets or credentials

**Common Vulnerabilities** (OWASP Top 10):
- SQL Injection prevention
- XSS prevention
- CSRF protection
- Secure dependencies (no known vulnerabilities)

Store review: code-review/${prId}/security-review
Severity: Critical/High/Medium/Low for each finding
`, "security-manager"),

  Task("Performance Reviewer", `
Review for performance issues:

**Algorithmic Efficiency**:
- Appropriate time complexity (no unnecessary O(n²))
- Efficient data structures chosen
- No unnecessary iterations
- Lazy loading where appropriate

**Resource Usage**:
- No memory leaks
- Proper cleanup (connections, files, timers)
- Efficient database queries (avoid N+1)
- Batch operations where possible

**Optimization Opportunities**:
- Caching potential
- Parallelization opportunities
- Database index needs
- API call optimization

Store review: code-review/${prId}/performance-review
Impact: High/Medium/Low for each finding
`, "perf-analyzer"),

  Task("Architecture Reviewer", `
Review for architectural consistency:

**Design Patterns**:
- Follows established patterns in codebase
- Appropriate abstraction level
- Proper dependency injection
- Clean architecture principles

**Integration**:
- Fits well with existing code
- No unexpected side effects
- Backward compatibility maintained
- API contracts respected

**Scalability**:
- Design supports future growth
- No hardcoded limits
- Stateless where possible
- Horizontally scalable

Store review: code-review/${prId}/architecture-review
Concerns: Blocker/Major/Minor for each finding
`, "system-architect"),

  Task("Documentation Reviewer", `
Review documentation:

**Code Documentation**:
- Public APIs documented (JSDoc/docstring)
- Complex logic explained
- Non-obvious behavior noted
- Examples provided where helpful

**External Documentation**:
- README updated (if needed)
- API docs updated (if API changed)
- Migration guide (if breaking changes)
- Changelog updated

**Tests as Documentation**:
- Test names are descriptive
- Test coverage demonstrates usage
- Edge cases documented in tests

Store review: code-review/${prId}/docs-review
Completeness: 0-100%
`, "api-docs")
]);

// Aggregate all reviews
await Task("Review Aggregator", `
Aggregate specialized reviews:
- Quality: ${codeQuality}
- Security: ${security}
- Performance: ${performance}
- Architecture: ${architecture}
- Documentation: ${docs}

Identify:
- Blocking issues (must fix before merge)
- High-priority suggestions
- Nice-to-have improvements

Generate summary
Store: code-review/${prId}/aggregated-review
`, "reviewer");
```

**Deliverables**:
- 5 specialized reviews completed
- Issues categorized by severity
- Aggregated review summary

---

## Phase 3: Integration Review (1 hour)

### End-to-End Impact Assessment

**Sequential Analysis**:

```javascript
// Step 1: Integration Testing
await Task("Integration Tester", `
Test integration with existing system:
- Does this change break any existing functionality?
- Are all integration tests passing?
- Does it play well with related modules?
- Any unexpected side effects?

Run integration test suite
Store results: code-review/${prId}/integration-tests
`, "tester");

// Step 2: Deployment Impact
await Task("DevOps Reviewer", `
Assess deployment impact:
- Infrastructure changes needed?
- Database migrations required?
- Configuration updates needed?
- Backward compatibility maintained?
- Rollback plan clear?

Store assessment: code-review/${prId}/deployment-impact
`, "cicd-engineer");

// Step 3: User Impact
await Task("Product Reviewer", `
Assess user impact:
- Does this change improve user experience?
- Are there any user-facing changes?
- Is UX/UI consistent with design system?
- Are analytics/tracking updated?

Store assessment: code-review/${prId}/user-impact
`, "planner");

// Step 4: Risk Assessment
await Task("Risk Analyzer", `
Overall risk assessment:
- What's the blast radius of this change?
- What's the worst-case failure scenario?
- Do we have rollback procedures?
- Should this be feature-flagged?
- Monitoring and alerting adequate?

Store risk assessment: code-review/${prId}/risk-analysis
Recommendation: Approve/Conditional/Reject
`, "reviewer");
```

**Deliverables**:
- Integration test results
- Deployment impact assessment
- User impact assessment
- Risk analysis

---

## Phase 4: Final Approval (30 minutes)

### Review Summary & Decision

**Sequential Finalization**:

```javascript
// Step 1: Generate Final Summary
await Task("Review Coordinator", `
Generate final review summary:

**Automated Checks**: ✅ All passing
**Quality Review**: ${qualityScore}/5
**Security Review**: ${securityIssues} issues (${criticalCount} critical)
**Performance Review**: ${perfIssues} issues (${highImpactCount} high-impact)
**Architecture Review**: ${archConcerns} concerns (${blockerCount} blockers)
**Documentation Review**: ${docsCompleteness}% complete
**Integration Tests**: ${integrationStatus}
**Deployment Impact**: ${deploymentImpact}
**User Impact**: ${userImpact}
**Risk Level**: ${riskLevel}

**Blocking Issues**:
${listBlockingIssues()}

**Recommendations**:
${generateRecommendations()}

**Overall Decision**: ${decision} (Approve/Request Changes/Reject)

Store final summary: code-review/${prId}/final-summary
`, "pr-manager");

// Step 2: Author Notification
await Task("Notification Agent", `
Notify PR author:
- Review complete
- Summary of findings
- Action items (if any)
- Next steps

Send notification
Store: code-review/${prId}/author-notification
`, "pr-manager");

// Step 3: Decision Actions
if (decision === 'Approve') {
  await Task("Merge Coordinator", `
Approved for merge:
- Add "approved" label
- Update PR status
- Queue for merge (if auto-merge enabled)
- Notify relevant teams

Store: code-review/${prId}/merge-approval
`, "pr-manager");
} else if (decision === 'Request Changes') {
  await Task("Feedback Coordinator", `
Request changes:
- Create detailed feedback comment
- Label as "changes-requested"
- Assign back to author
- Schedule follow-up review

Store: code-review/${prId}/change-request
`, "pr-manager");
} else {
  await Task("Rejection Handler", `
Reject PR:
- Create detailed explanation
- Suggest alternative approaches
- Label as "rejected"
- Close PR (or request fundamental rework)

Store: code-review/${prId}/rejection
`, "pr-manager");
}
```

**Deliverables**:
- Final review summary
- Author notification
- Decision and next steps

---

## Success Criteria

### Review Quality
- **Coverage**: All aspects reviewed (quality, security, performance, architecture, docs)
- **Consistency**: Reviews follow established guidelines
- **Actionability**: All feedback is specific and actionable
- **Timeliness**: Reviews completed within 4 hours

### Code Quality Gates
- **Automated Tests**: 100% passing
- **Code Coverage**: > 80% overall, > 90% for new code
- **Linting**: 0 violations
- **Security**: 0 critical issues, 0 high-severity issues
- **Performance**: No high-impact performance regressions
- **Documentation**: 100% of public APIs documented

### Process Metrics
- **Review Turnaround**: < 4 hours (business hours)
- **Author Satisfaction**: > 4/5 (feedback is helpful)
- **Defect Escape Rate**: < 1% (issues found in production that should have been caught)

---

## Review Guidelines

### What Reviewers Should Focus On

**DO Review**:
- Logic correctness
- Edge case handling
- Error handling robustness
- Security vulnerabilities
- Performance implications
- Code clarity and maintainability
- Test coverage and quality
- API design and contracts
- Documentation completeness

**DON'T Nitpick**:
- Personal style preferences (use automated linting)
- Minor variable naming (unless truly confusing)
- Trivial formatting (use automated formatting)
- Subjective "better" ways (unless significantly better)

### Giving Feedback

**Effective Feedback**:
- ✅ "This function has O(n²) complexity. Consider using a hash map for O(n)."
- ✅ "This input isn't validated. Add validation to prevent SQL injection."
- ✅ "This error isn't logged. Add error logging for debugging."

**Ineffective Feedback**:
- ❌ "I don't like this."
- ❌ "This could be better."
- ❌ "Change this." (without explanation)

**Tone**:
- Be respectful and constructive
- Assume good intent
- Ask questions rather than make demands
- Suggest, don't dictate (unless security/critical issue)

---

## Agent Coordination Summary

**Total Agents Used**: 12-15
**Execution Pattern**: Star topology (coordinator with specialists)
**Timeline**: 4 hours
**Memory Namespaces**: code-review/{pr-id}/*

**Key Agents**:
1. reviewer - Lint, build, coordination
2. tester - Test execution, integration testing
3. code-analyzer - Code quality review
4. security-manager - Security review
5. perf-analyzer - Performance review
6. system-architect - Architecture review
7. api-docs - Documentation review
8. cicd-engineer - Deployment impact
9. planner - Product/user impact
10. pr-manager - Review coordination, notifications

---

## Usage

```javascript
// Invoke this SOP skill for a PR
Skill("sop-code-review")

// Or execute with specific PR
Task("Code Review Orchestrator", `
Execute comprehensive code review for PR #${prNumber}
Repository: ${repoName}
Author: ${authorName}
Changes: ${changesSummary}
`, "pr-manager")
```

---

**Status**: Production-ready SOP
**Complexity**: Medium (12-15 agents, 4 hours)
**Pattern**: Star topology with specialized reviewers
