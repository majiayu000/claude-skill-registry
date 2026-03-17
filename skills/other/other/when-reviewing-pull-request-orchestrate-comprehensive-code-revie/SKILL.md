---
name: when-reviewing-pull-request-orchestrate-comprehensive-code-review
type: sop-workflow
description: |
  Use when conducting comprehensive code review for pull requests across multiple quality dimensions.
  Orchestrates 12-15 specialized reviewer agents across 4 phases using star topology coordination.
  Covers automated checks, parallel specialized reviews (quality, security, performance, architecture,
  documentation), integration analysis, and final merge recommendation in a 4-hour workflow.
agents:
  - pr-manager
  - code-analyzer
  - security-manager
  - performance-analyzer
  - system-architect
  - api-documentation-specialist
  - tester
  - qa-engineer
  - devops-engineer
  - style-auditor
  - dependency-analyzer
  - test-coverage-reviewer
  - documentation-reviewer
  - system-integrator
  - code-reviewer
phases: 4
memory_pattern: "code-review/{pr-id}/phase-{N}/{reviewer}/{findings}"
---

# Code Review Orchestration Workflow

Comprehensive code review workflow orchestrating 12-15 specialized reviewers across automated checks, parallel expert reviews, integration analysis, and final approval recommendation. Designed for thorough quality validation across security, performance, architecture, testing, and documentation dimensions in a systematic 4-hour process.

## Overview

This SOP implements a multi-dimensional code review process using star topology coordination where a central PR manager orchestrates specialized reviewers operating in parallel. The workflow emphasizes both thoroughness and efficiency by running automated checks first (gate 1), then parallelizing specialized human-centric reviews, followed by integration impact analysis, and finally synthesizing all findings into actionable recommendations.

The star pattern enables each specialist to focus deeply on their domain while the coordinator ensures comprehensive coverage and prevents conflicting feedback. Memory coordination allows reviewers to reference findings from other specialists, creating a holistic review experience.

## Trigger Conditions

Use this workflow when:
- Reviewing pull requests requiring comprehensive quality validation
- Changes span multiple quality dimensions (code, security, performance, architecture)
- Need systematic review from multiple specialist perspectives
- PR introduces significant functionality or architectural changes
- Merge decision requires evidence-based go/no-go recommendation
- Team wants consistent, repeatable review process
- Code review SLA is within 4 hours (business hours)

## Orchestrated Agents (15 Total)

### Coordination Agent
- **`pr-manager`** - PR coordination, review orchestration, findings aggregation, author notification

### Automated Check Agents (Phase 1)
- **`code-analyzer`** - Linting, static analysis, code complexity metrics
- **`tester`** - Test execution, test suite validation
- **`qa-engineer`** - Coverage analysis, test quality assessment

### Specialized Review Agents (Phase 2)
- **`code-analyzer`** - Code quality, readability, maintainability, DRY, SOLID principles
- **`security-manager`** - Security vulnerabilities, OWASP compliance, secrets scanning, auth/auth
- **`performance-analyzer`** - Performance regressions, algorithmic efficiency, resource optimization
- **`system-architect`** - Architectural consistency, design patterns, scalability, integration fit
- **`api-documentation-specialist`** - Code documentation, API docs, comments, examples
- **`style-auditor`** - Code style consistency, formatting standards
- **`dependency-analyzer`** - Dependency audit, outdated packages, security vulnerabilities
- **`test-coverage-reviewer`** - Coverage metrics, uncovered code paths, edge case testing
- **`documentation-reviewer`** - README updates, changelog, migration guides

### Integration Analysis Agents (Phase 3)
- **`system-integrator`** - Integration impact, breaking changes, backward compatibility
- **`devops-engineer`** - Deployment impact, infrastructure changes, rollback planning
- **`code-reviewer`** - Risk assessment, blast radius analysis

## Workflow Phases

### Phase 1: Automated Checks (30 Minutes, Parallel Gate)

**Duration**: 30 minutes
**Execution Mode**: Parallel automated validation (fast fail-fast gate)
**Agents**: `code-analyzer`, `tester`, `qa-engineer`, `pr-manager`

**Process**:

1. **Initialize Review Swarm**
   ```bash
   PR_ID="$1"  # e.g., "repo-name/pulls/123"
   PR_NUMBER=$(echo $PR_ID | cut -d'/' -f3)

   npx claude-flow hooks pre-task --description "Code review: PR #${PR_NUMBER}"
   npx claude-flow swarm init --topology star --max-agents 15 --strategy specialized
   npx claude-flow agent spawn --type pr-manager
   ```

   **PR Manager** retrieves PR metadata:
   - Changed files and line counts
   - Commit history and messages
   - Branch comparison (base vs head)
   - PR description and labels
   - Author and reviewers assigned

   **Memory Storage**:
   ```bash
   npx claude-flow memory store --key "code-review/${PR_ID}/metadata" \
     --value '{"pr_number": "'"${PR_NUMBER}"'", "files_changed": 15, "lines_added": 342, "lines_deleted": 78}'
   ```

2. **Run Automated Checks in Parallel**
   ```bash
   npx claude-flow task orchestrate --strategy parallel --max-agents 4
   ```

   Spawn all automated check agents concurrently:

   **Linting Check** (Code Analyzer):
   ```bash
   npx claude-flow agent spawn --type code-analyzer --focus "linting"

   # Run linting
   npm run lint  # ESLint for JS/TS
   # or
   pylint src/  # Python
   # or
   rubocop  # Ruby
   ```

   Checks:
   - Code style violations (max line length, indentation)
   - Unused variables and imports
   - Type errors (TypeScript)
   - Deprecated API usage
   - Code complexity warnings

   **Memory Pattern**: `code-review/${PR_ID}/phase-1/code-analyzer/lint-results`

   **Test Execution** (Tester):
   ```bash
   npx claude-flow agent spawn --type tester --focus "test-execution"

   # Run test suite
   npm test  # Jest/Mocha
   # or
   pytest  # Python
   # or
   rspec  # Ruby
   ```

   Validates:
   - All unit tests passing
   - All integration tests passing
   - All E2E tests passing (if applicable)
   - No flaky test failures
   - Test execution time within limits

   **Memory Pattern**: `code-review/${PR_ID}/phase-1/tester/test-results`

   **Coverage Analysis** (QA Engineer):
   ```bash
   npx claude-flow agent spawn --type tester --focus "coverage"

   # Generate coverage report
   npm run test:coverage
   ```

   Checks:
   - Overall coverage > 80%
   - New code coverage > 90%
   - No critical paths uncovered
   - Coverage delta (did coverage decrease?)
   - Untested branches and conditions

   **Memory Pattern**: `code-review/${PR_ID}/phase-1/qa-engineer/coverage-report`

   **Build Validation** (Code Analyzer):
   ```bash
   # Clean build validation
   npm run build
   # or
   python setup.py build
   ```

   Validates:
   - Clean build (no errors, no warnings)
   - Type checking passes (TypeScript, mypy)
   - No broken dependencies
   - Bundle size within limits (for frontend)
   - No circular dependencies

   **Memory Pattern**: `code-review/${PR_ID}/phase-1/code-analyzer/build-status`

3. **Evaluate Gate 1 Results**
   ```bash
   npx claude-flow memory retrieve --pattern "code-review/${PR_ID}/phase-1/*/results"
   ```

   **PR Manager** aggregates automated results:
   - Lint: PASS/FAIL (violations count)
   - Tests: PASS/FAIL (passed/failed/skipped)
   - Coverage: PASS/FAIL (percentage, delta)
   - Build: PASS/FAIL (errors/warnings)

   **Decision Logic**:
   ```javascript
   if (lintFailed || testsFailed || buildFailed) {
     // Request fixes from author
     await notifyAuthor({
       status: 'CHANGES_REQUESTED',
       message: 'Automated checks failed. Please fix before review continues.',
       details: summarizeFailures()
     });

     // Store feedback and stop review
     await memory_store(`code-review/${PR_ID}/phase-1/automated-feedback`);
     return; // Stop review until fixed
   }

   // All automated checks passed, proceed to Phase 2
   await notifyAuthor({
     status: 'IN_REVIEW',
     message: 'Automated checks passed. Proceeding with specialized reviews.'
   });
   ```

**Outputs**:
- Automated check results (pass/fail for each)
- Test execution report
- Coverage report with delta
- Build status

**Success Criteria**:
- [ ] All linting checks passing
- [ ] All tests passing (100% of test suite)
- [ ] Code coverage meets thresholds
- [ ] Build successful with no errors

---

### Phase 2: Specialized Reviews (2 Hours, Parallel Expert Analysis)

**Duration**: 2 hours
**Execution Mode**: Parallel specialized reviews coordinated by PR manager
**Agents**: 10 specialist reviewers

**Process**:

1. **Initialize Specialist Review Swarm**
   ```bash
   npx claude-flow task orchestrate --strategy parallel --max-agents 10 --priority high
   ```

2. **Spawn All Specialist Reviewers Concurrently**

   Each specialist reviews the PR from their domain expertise:

   **Code Quality Review** (Code Analyzer):
   ```bash
   npx claude-flow agent spawn --type code-analyzer --focus "code-quality"
   ```

   Reviews:
   - **Readability**: Clear names, appropriate function length, logical organization, cognitive complexity
   - **Maintainability**: DRY principle, SOLID principles, separation of concerns, error handling
   - **Best Practices**: Language idioms, design patterns, appropriate comments, no code smells

   Rating: 1-5 stars

   **Findings Format**:
   ```json
   {
     "category": "code_quality",
     "findings": [
       {
         "severity": "MEDIUM",
         "file": "src/utils/parser.ts",
         "line": 45,
         "issue": "Function 'parseData' has cognitive complexity of 15 (max 10)",
         "suggestion": "Extract nested conditionals into separate validation functions"
       }
     ],
     "rating": 4,
     "overall_assessment": "Good code quality with minor improvements needed"
   }
   ```

   **Memory Pattern**: `code-review/${PR_ID}/phase-2/code-analyzer/quality-review`

   **Security Review** (Security Manager):
   ```bash
   npx claude-flow agent spawn --type security-manager --focus "security-comprehensive"
   ```

   Reviews:
   - **Authentication & Authorization**: Proper auth checks, no privilege escalation, secure sessions
   - **Data Security**: Input validation (injection prevention), output encoding (XSS prevention), sensitive data encryption, no hardcoded secrets
   - **OWASP Top 10**: SQL Injection, XSS, CSRF, insecure dependencies, security misconfigurations

   Severity: CRITICAL/HIGH/MEDIUM/LOW

   **Findings Format**:
   ```json
   {
     "category": "security",
     "findings": [
       {
         "severity": "HIGH",
         "file": "src/api/users.ts",
         "line": 78,
         "issue": "User input not sanitized before database query (SQL Injection risk)",
         "owasp_category": "A03:2021 – Injection",
         "suggestion": "Use parameterized queries or ORM with proper escaping"
       },
       {
         "severity": "MEDIUM",
         "file": "src/config/secrets.ts",
         "line": 12,
         "issue": "API key appears to be hardcoded (potential secret leak)",
         "suggestion": "Move to environment variables and add to .env.example"
       }
     ],
     "critical_count": 0,
     "high_count": 1,
     "medium_count": 1,
     "overall_assessment": "1 high-severity issue must be fixed before merge"
   }
   ```

   **Memory Pattern**: `code-review/${PR_ID}/phase-2/security-manager/security-review`

   **Performance Review** (Performance Analyzer):
   ```bash
   npx claude-flow agent spawn --type perf-analyzer --focus "performance-optimization"
   ```

   Reviews:
   - **Algorithmic Efficiency**: Time complexity (no unnecessary O(n²)), efficient data structures, no redundant iterations
   - **Resource Usage**: No memory leaks, proper cleanup (connections, files, timers), efficient queries (avoid N+1)
   - **Optimization Opportunities**: Caching potential, parallelization, database indexes, API call reduction

   Impact: HIGH/MEDIUM/LOW

   **Findings Format**:
   ```json
   {
     "category": "performance",
     "findings": [
       {
         "impact": "HIGH",
         "file": "src/services/user-service.ts",
         "line": 125,
         "issue": "N+1 query problem: Loading user roles in loop (1 + N queries)",
         "performance_cost": "10x slower for 100 users",
         "suggestion": "Use eager loading with JOIN or batch query with IN clause"
       }
     ],
     "high_impact_count": 1,
     "estimated_improvement": "10x faster with suggested optimizations",
     "overall_assessment": "Significant performance regression without optimization"
   }
   ```

   **Memory Pattern**: `code-review/${PR_ID}/phase-2/performance-analyzer/performance-review`

   **Architecture Review** (System Architect):
   ```bash
   npx claude-flow agent spawn --type system-architect --focus "architecture-consistency"
   ```

   Reviews:
   - **Design Patterns**: Follows established patterns, appropriate abstraction, dependency injection, clean architecture
   - **Integration**: Fits with existing code, no unexpected side effects, backward compatibility, API contracts respected
   - **Scalability**: Supports future growth, no hardcoded limits, stateless design, horizontally scalable

   Concerns: BLOCKER/MAJOR/MINOR

   **Findings Format**:
   ```json
   {
     "category": "architecture",
     "findings": [
       {
         "concern": "MAJOR",
         "file": "src/services/payment-service.ts",
         "issue": "Payment service directly couples to Stripe SDK (violates adapter pattern)",
         "impact": "Difficult to switch payment providers in future",
         "suggestion": "Create PaymentProvider interface and StripeAdapter implementation"
       }
     ],
     "blocker_count": 0,
     "major_count": 1,
     "overall_assessment": "Architecture mostly consistent with 1 major design concern"
   }
   ```

   **Memory Pattern**: `code-review/${PR_ID}/phase-2/system-architect/architecture-review`

   **Documentation Review** (API Documentation Specialist):
   ```bash
   npx claude-flow agent spawn --type api-docs --focus "documentation-comprehensive"
   ```

   Reviews:
   - **Code Documentation**: Public APIs documented (JSDoc/docstring), complex logic explained, non-obvious behavior noted
   - **External Documentation**: README updated, API docs updated, migration guide (if breaking), changelog updated
   - **Tests as Documentation**: Descriptive test names, test coverage demonstrates usage, edge cases documented

   Completeness: 0-100%

   **Findings Format**:
   ```json
   {
     "category": "documentation",
     "findings": [
       {
         "severity": "MEDIUM",
         "file": "src/api/webhooks.ts",
         "issue": "New webhook endpoint /api/webhooks/stripe missing API documentation",
         "suggestion": "Add JSDoc with parameters, responses, and usage example"
       }
     ],
     "code_doc_coverage": 75,
     "external_doc_updated": false,
     "overall_assessment": "75% complete, missing API docs and changelog update"
   }
   ```

   **Memory Pattern**: `code-review/${PR_ID}/phase-2/api-documentation-specialist/docs-review`

   **Additional Specialist Reviews** (run in parallel):

   - **Style Audit** (Style Auditor): Code style consistency, formatting compliance
   - **Dependency Audit** (Dependency Analyzer): Outdated packages, security vulnerabilities in deps
   - **Test Coverage** (Test Coverage Reviewer): Coverage gaps, missing edge cases
   - **Documentation Completeness** (Documentation Reviewer): README, changelog, migration guides

   Each follows similar format with findings, severity, and recommendations.

3. **Aggregate Specialist Reviews**
   ```bash
   npx claude-flow memory retrieve --pattern "code-review/${PR_ID}/phase-2/*/review"
   npx claude-flow agent spawn --type pr-manager --focus "aggregation"
   ```

   **PR Manager** synthesizes all reviews:
   - Total findings: 15 issues (0 critical, 1 high, 8 medium, 6 low)
   - Quality rating: 4/5 stars
   - Security: 1 high-severity issue
   - Performance: 1 high-impact issue
   - Architecture: 1 major concern
   - Documentation: 75% complete

   Categorize issues:
   - **Blocking Issues** (must fix before merge): High-severity security issue, high-impact performance regression
   - **High-Priority** (should fix): Major architecture concern, medium security issues
   - **Nice-to-Have** (can fix later): Low-severity code quality improvements

   **Memory Storage**:
   ```bash
   npx claude-flow memory store --key "code-review/${PR_ID}/phase-2/aggregated-review" \
     --value "${AGGREGATED_FINDINGS_JSON}"
   ```

**Outputs**:
- 10 specialized review reports
- Aggregated findings with severity prioritization
- Blocking issues list
- Recommendations summary

**Success Criteria**:
- [ ] All specialist reviews completed
- [ ] Findings categorized by severity
- [ ] Blocking issues clearly identified
- [ ] Recommendations actionable and specific

---

### Phase 3: Integration Analysis (1 Hour, Sequential Impact Assessment)

**Duration**: 1 hour
**Execution Mode**: Sequential end-to-end impact analysis
**Agents**: `tester`, `devops-engineer`, `product-manager`, `code-reviewer`

**Process**:

1. **Integration Testing**
   ```bash
   npx claude-flow agent spawn --type tester --focus "integration-impact"
   ```

   **QA Engineer** tests:
   - Does this change break existing functionality?
   - Are all integration tests passing?
   - Does it integrate properly with related modules?
   - Any unexpected side effects or regressions?

   Run integration test suite:
   ```bash
   npm run test:integration
   ```

   **Findings**:
   - Integration tests: 45/45 passing
   - No regressions detected
   - New functionality integrates cleanly

   **Memory Pattern**: `code-review/${PR_ID}/phase-3/tester/integration-tests`

2. **Deployment Impact Assessment**
   ```bash
   npx claude-flow memory retrieve --key "code-review/${PR_ID}/metadata"
   npx claude-flow agent spawn --type cicd-engineer --focus "deployment-impact"
   ```

   **DevOps Engineer** evaluates:
   - Infrastructure changes needed? (new services, scaling)
   - Database migrations required? (schema changes)
   - Configuration updates needed? (env vars, secrets)
   - Backward compatibility maintained? (can rollback safely)
   - Rollback plan clear and tested?

   **Findings**:
   ```json
   {
     "infrastructure_changes": ["Add Redis cache for session storage"],
     "database_migrations": ["Add index on users.email for faster lookups"],
     "config_updates": ["Add REDIS_URL environment variable"],
     "backward_compatible": true,
     "rollback_complexity": "LOW",
     "deployment_risk": "MEDIUM"
   }
   ```

   **Memory Pattern**: `code-review/${PR_ID}/phase-3/devops-engineer/deployment-impact`

3. **User Impact Assessment**
   ```bash
   npx claude-flow agent spawn --type planner --focus "user-impact"
   ```

   **Product Manager** assesses:
   - Does this improve user experience?
   - Any user-facing changes? (UI/UX)
   - Consistent with design system?
   - Analytics/tracking updated?
   - Feature flags needed?

   **Findings**:
   ```json
   {
     "user_facing_changes": ["New export functionality in dashboard"],
     "ux_impact": "POSITIVE",
     "design_system_compliant": true,
     "analytics_updated": false,
     "feature_flag_recommended": true
   }
   ```

   **Memory Pattern**: `code-review/${PR_ID}/phase-3/product-manager/user-impact`

4. **Risk Assessment**
   ```bash
   npx claude-flow memory retrieve --pattern "code-review/${PR_ID}/phase-3/*"
   npx claude-flow agent spawn --type reviewer --focus "risk-analysis"
   ```

   **Code Reviewer** analyzes:
   - What's the blast radius of this change? (how many users/services affected)
   - Worst-case failure scenario? (data loss, downtime, security breach)
   - Do we have rollback procedures? (tested and documented)
   - Should this be feature-flagged? (gradual rollout)
   - Is monitoring and alerting adequate? (can detect issues quickly)

   **Risk Matrix**:
   ```json
   {
     "blast_radius": "MEDIUM (affects 30% of users)",
     "worst_case_scenario": "Temporary export failures (no data loss)",
     "rollback_available": true,
     "rollback_tested": false,
     "feature_flag_needed": true,
     "monitoring_adequate": true,
     "overall_risk": "MEDIUM",
     "recommendation": "CONDITIONAL_APPROVE (add feature flag + test rollback)"
   }
   ```

   **Memory Pattern**: `code-review/${PR_ID}/phase-3/code-reviewer/risk-analysis`

**Outputs**:
- Integration test results
- Deployment impact report
- User impact assessment
- Risk analysis with mitigation recommendations

**Success Criteria**:
- [ ] Integration tests passing
- [ ] Deployment plan documented
- [ ] User impact understood
- [ ] Risk assessment complete with mitigation

---

### Phase 4: Final Approval (30 Minutes, Decision & Notification)

**Duration**: 30 minutes
**Execution Mode**: Sequential synthesis and decision
**Agents**: `pr-manager`

**Process**:

1. **Generate Final Review Summary**
   ```bash
   npx claude-flow memory retrieve --pattern "code-review/${PR_ID}/**"
   npx claude-flow agent spawn --type pr-manager --focus "final-summary"
   ```

   **PR Manager** synthesizes all phases:

   **Summary Report**:
   ```markdown
   # Code Review Summary: PR #${PR_NUMBER}

   ## Automated Checks ✅
   - Linting: ✅ PASS (0 violations)
   - Tests: ✅ PASS (142/142 passing)
   - Coverage: ✅ PASS (93.5%, +2.3% delta)
   - Build: ✅ PASS (clean build, no warnings)

   ## Specialized Reviews
   - **Code Quality**: 4/5 stars (Good quality, minor improvements suggested)
   - **Security**: ⚠️ 1 HIGH issue (SQL injection risk in user query)
   - **Performance**: ⚠️ 1 HIGH impact (N+1 query problem)
   - **Architecture**: ⚠️ 1 MAJOR concern (tight coupling to payment provider)
   - **Documentation**: 75% complete (missing API docs + changelog)

   ## Integration Analysis
   - **Integration Tests**: ✅ All passing (45/45)
   - **Deployment Impact**: MEDIUM risk (requires Redis + DB migration)
   - **User Impact**: POSITIVE (new export feature)
   - **Risk Level**: MEDIUM (feature flag recommended)

   ## Blocking Issues (MUST FIX)
   1. [HIGH/SECURITY] SQL injection risk in src/api/users.ts:78
   2. [HIGH/PERFORMANCE] N+1 query in src/services/user-service.ts:125

   ## High-Priority Recommendations (SHOULD FIX)
   3. [MAJOR/ARCHITECTURE] Decouple payment service from Stripe SDK
   4. [MEDIUM/DOCUMENTATION] Add API documentation for webhook endpoint
   5. [MEDIUM/DEPLOYMENT] Add feature flag for gradual rollout

   ## Overall Decision: ⏸️ REQUEST CHANGES

   **Rationale**: Code is high quality overall, but 2 blocking issues (security + performance) must be addressed before merge. Once fixed, this PR will be ready for production.

   **Next Steps**:
   1. Author fixes blocking issues (estimated 2-4 hours)
   2. Re-run automated checks + security/performance reviews
   3. Once green, approve for merge with feature flag enabled
   ```

   **Memory Storage**:
   ```bash
   npx claude-flow memory store --key "code-review/${PR_ID}/phase-4/final-summary" \
     --value "${FINAL_SUMMARY_MARKDOWN}"
   ```

2. **Determine Decision**

   **Decision Logic**:
   ```javascript
   function determineDecision(aggregatedReview) {
     const { blocking, highPriority, security, performance } = aggregatedReview;

     // REJECT: Fundamental architectural problems or severe quality issues
     if (blocking.length > 5 || security.critical > 0) {
       return {
         decision: 'REJECT',
         message: 'Too many critical issues or fundamental architectural problems. Consider alternative approach.'
       };
     }

     // REQUEST CHANGES: Blocking issues that must be fixed
     if (blocking.length > 0 || security.high > 0 || performance.high > 0) {
       return {
         decision: 'REQUEST_CHANGES',
         message: `${blocking.length} blocking issue(s) must be fixed before merge.`
       };
     }

     // CONDITIONAL APPROVE: High-priority items should be addressed
     if (highPriority.length > 0) {
       return {
         decision: 'CONDITIONAL_APPROVE',
         message: `Approved with ${highPriority.length} recommendations to address before or after merge.`
       };
     }

     // APPROVE: All quality gates passed
     return {
       decision: 'APPROVE',
       message: 'All quality checks passed. Ready to merge.'
     };
   }
   ```

3. **Notify Author**
   ```bash
   npx claude-flow agent spawn --type pr-manager --focus "author-notification"
   ```

   **PR Manager** sends notification:
   - GitHub PR comment with full review summary
   - Label PR appropriately ("changes-requested", "approved", "rejected")
   - Assign back to author (if changes needed)
   - Tag relevant reviewers for specific issues

   **GitHub PR Comment** (example for REQUEST_CHANGES):
   ```markdown
   ## 🔍 Comprehensive Code Review Complete

   Thank you for your contribution! Our automated review system has completed a thorough analysis.

   ### ✅ What Went Well
   - All automated checks passing (tests, coverage, linting)
   - Clean code architecture overall
   - Good test coverage (93.5%)

   ### ⚠️ Issues Requiring Attention

   #### Blocking Issues (Must Fix Before Merge)

   1. **[HIGH/SECURITY]** SQL Injection Risk
      - **File**: `src/api/users.ts:78`
      - **Issue**: User input not sanitized before database query
      - **Fix**: Use parameterized queries or ORM with proper escaping
      - **Priority**: CRITICAL

   2. **[HIGH/PERFORMANCE]** N+1 Query Problem
      - **File**: `src/services/user-service.ts:125`
      - **Issue**: Loading user roles in loop (10x slower for 100 users)
      - **Fix**: Use eager loading with JOIN or batch query
      - **Priority**: HIGH

   #### Recommendations (Should Address)

   3. **[MAJOR/ARCHITECTURE]** Payment Service Coupling
      - Create PaymentProvider interface for future flexibility
      - See: [Architecture Best Practices](link)

   4. **[MEDIUM/DOCUMENTATION]** Missing API Documentation
      - Add JSDoc for webhook endpoint
      - Update changelog with this new feature

   ### 🔄 Next Steps

   1. Address the 2 blocking issues above
   2. Push updates to this PR branch
   3. Automated checks will re-run automatically
   4. We'll re-review security and performance aspects
   5. Once green, we'll approve for merge!

   **Estimated time to fix**: 2-4 hours

   ---
   🤖 Generated by Claude Code Review System | [View Full Report](link)
   ```

   **Memory Storage**:
   ```bash
   npx claude-flow memory store --key "code-review/${PR_ID}/phase-4/author-notification"
   npx claude-flow hooks post-task --task-id "code-review-${PR_ID}" --export-report true
   ```

4. **Execute Decision Actions**

   Based on decision, take appropriate GitHub actions:

   **If APPROVE**:
   ```bash
   # Add approval label
   gh pr edit ${PR_NUMBER} --add-label "approved"

   # Add approval review
   gh pr review ${PR_NUMBER} --approve --body "✅ All quality checks passed. Ready to merge."

   # Queue for merge (if auto-merge enabled)
   gh pr merge ${PR_NUMBER} --auto --squash
   ```

   **If REQUEST_CHANGES**:
   ```bash
   # Add changes-requested label
   gh pr edit ${PR_NUMBER} --add-label "changes-requested" --remove-label "approved"

   # Request changes
   gh pr review ${PR_NUMBER} --request-changes --body "${REVIEW_COMMENT_MARKDOWN}"

   # Assign back to author
   gh pr edit ${PR_NUMBER} --add-assignee ${AUTHOR_USERNAME}

   # Schedule follow-up review
   npx claude-flow memory store --key "code-review/${PR_ID}/follow-up/scheduled" --value "true"
   ```

   **If REJECT**:
   ```bash
   # Add rejected label
   gh pr edit ${PR_NUMBER} --add-label "rejected"

   # Provide detailed explanation
   gh pr review ${PR_NUMBER} --request-changes --body "${DETAILED_REJECTION_REASON}"

   # Suggest alternative approaches
   gh pr comment ${PR_NUMBER} --body "Consider these alternative approaches: ${ALTERNATIVES}"
   ```

5. **Finalize Review Session**
   ```bash
   npx claude-flow hooks session-end --export-metrics true
   npx claude-flow hooks post-task --task-id "pr-${PR_ID}"
   ```

**Outputs**:
- Final review summary (comprehensive report)
- Merge decision (Approve/Request Changes/Reject)
- Author notification (GitHub comment)
- GitHub labels and status updated

**Success Criteria**:
- [ ] Final summary generated and comprehensive
- [ ] Decision clear and justified
- [ ] Author notified with actionable feedback
- [ ] GitHub PR status updated appropriately

---

## Memory Coordination

### Namespace Convention

All review data follows this hierarchical pattern:

```
code-review/{pr-id}/phase-{N}/{reviewer-type}/{findings-type}
```

**Examples**:
- `code-review/repo/pulls/123/metadata`
- `code-review/repo/pulls/123/phase-1/code-analyzer/lint-results`
- `code-review/repo/pulls/123/phase-2/security-manager/security-review`
- `code-review/repo/pulls/123/phase-3/devops-engineer/deployment-impact`
- `code-review/repo/pulls/123/phase-4/final-summary`

### Cross-Phase Data Flow

**Phase 1 → Phase 2**:
```bash
# Phase 2 reviewers check if Phase 1 passed
npx claude-flow memory retrieve --pattern "code-review/${PR_ID}/phase-1/*/results"

# Only proceed if all automated checks passed
if [ "$(jq '.all_passed' < phase1_results.json)" = "true" ]; then
  # Spawn specialist reviewers
  npx claude-flow task orchestrate --strategy parallel
fi
```

**Phase 2 → Phase 3**:
```bash
# Phase 3 integration analysis references specialist findings
npx claude-flow memory retrieve --pattern "code-review/${PR_ID}/phase-2/security-manager/security-review"
npx claude-flow memory retrieve --pattern "code-review/${PR_ID}/phase-2/performance-analyzer/performance-review"

# Risk analysis considers all specialist findings
```

**Phase 3 → Phase 4**:
```bash
# Phase 4 final decision aggregates all prior phases
npx claude-flow memory retrieve --pattern "code-review/${PR_ID}/**"

# Generate comprehensive summary
```

---

## Scripts & Automation

### Pre-Review Initialization

```bash
#!/bin/bash
# Initialize code review workflow

PR_NUMBER="$1"
REPO="$2"  # e.g., "owner/repo"
PR_ID="${REPO}/pulls/${PR_NUMBER}"

# Fetch PR metadata via GitHub API
PR_DATA=$(gh pr view ${PR_NUMBER} --json number,title,author,files,additions,deletions)

# Setup coordination
npx claude-flow hooks pre-task --description "Code review: PR #${PR_NUMBER}"

# Initialize star topology swarm (central coordinator + specialists)
npx claude-flow swarm init --topology star --max-agents 15 --strategy specialized

# Store PR metadata
npx claude-flow memory store --key "code-review/${PR_ID}/metadata" --value "${PR_DATA}"

echo "✅ Code review initialized: PR #${PR_NUMBER}"
```

### Automated Check Gate

```bash
#!/bin/bash
# Execute Phase 1 automated checks (gate)

PR_ID="$1"

echo "🤖 Running automated checks..."

# Run checks in parallel
npx claude-flow task orchestrate --strategy parallel --max-agents 4 << EOF
  lint: npm run lint
  test: npm test
  coverage: npm run test:coverage
  build: npm run build
EOF

# Aggregate results
LINT_STATUS=$(npx claude-flow memory retrieve --key "code-review/${PR_ID}/phase-1/code-analyzer/lint-results" | jq -r '.status')
TEST_STATUS=$(npx claude-flow memory retrieve --key "code-review/${PR_ID}/phase-1/tester/test-results" | jq -r '.status')
COVERAGE_OK=$(npx claude-flow memory retrieve --key "code-review/${PR_ID}/phase-1/qa-engineer/coverage-report" | jq -r '.meets_threshold')
BUILD_STATUS=$(npx claude-flow memory retrieve --key "code-review/${PR_ID}/phase-1/code-analyzer/build-status" | jq -r '.status')

# Check if all passed
if [ "$LINT_STATUS" = "PASS" ] && [ "$TEST_STATUS" = "PASS" ] && [ "$COVERAGE_OK" = "true" ] && [ "$BUILD_STATUS" = "PASS" ]; then
  echo "✅ All automated checks passed. Proceeding to specialist reviews."
  exit 0
else
  echo "❌ Automated checks failed. Requesting fixes from author."
  gh pr review ${PR_NUMBER} --request-changes --body "Automated checks failed. Please fix before review continues."
  exit 1
fi
```

### Parallel Specialist Review

```bash
#!/bin/bash
# Execute Phase 2 specialist reviews in parallel

PR_ID="$1"

echo "👥 Spawning specialist reviewers..."

# Spawn all reviewers concurrently via Claude Flow
npx claude-flow task orchestrate --strategy parallel --max-agents 10 << EOF
  code_quality: Review code quality (readability, maintainability, best practices)
  security: Review security vulnerabilities (OWASP Top 10, secrets, auth)
  performance: Review performance (algorithms, resource usage, optimizations)
  architecture: Review architecture consistency (patterns, integration, scalability)
  documentation: Review documentation completeness (code docs, API docs, changelog)
  style: Review code style consistency
  dependencies: Review dependency security and updates
  test_coverage: Review test coverage gaps
  external_docs: Review README and migration guides
  integration: Review integration fit with existing codebase
EOF

# Wait for all reviews to complete
npx claude-flow task status --wait

echo "✅ All specialist reviews complete."
```

### Final Decision Script

```bash
#!/bin/bash
# Generate final decision and notify author

PR_ID="$1"
PR_NUMBER=$(echo $PR_ID | cut -d'/' -f3)

# Retrieve all review data
npx claude-flow memory retrieve --pattern "code-review/${PR_ID}/**" > "/tmp/${PR_ID}-reviews.json"

# Count issues by severity
CRITICAL_COUNT=$(jq '[.. | .severity? | select(. == "CRITICAL")] | length' /tmp/${PR_ID}-reviews.json)
HIGH_COUNT=$(jq '[.. | .severity? | select(. == "HIGH")] | length' /tmp/${PR_ID}-reviews.json)
BLOCKING_COUNT=$((CRITICAL_COUNT + HIGH_COUNT))

# Determine decision
if [ $CRITICAL_COUNT -gt 0 ] || [ $BLOCKING_COUNT -gt 5 ]; then
  DECISION="REJECT"
elif [ $BLOCKING_COUNT -gt 0 ]; then
  DECISION="REQUEST_CHANGES"
else
  DECISION="APPROVE"
fi

echo "📊 Review Decision: ${DECISION}"
echo "   Critical Issues: ${CRITICAL_COUNT}"
echo "   High-Severity Issues: ${HIGH_COUNT}"

# Notify author via GitHub
case $DECISION in
  APPROVE)
    gh pr review ${PR_NUMBER} --approve --body "✅ All quality checks passed. Ready to merge."
    gh pr edit ${PR_NUMBER} --add-label "approved"
    ;;
  REQUEST_CHANGES)
    gh pr review ${PR_NUMBER} --request-changes --body-file "/tmp/${PR_ID}-summary.md"
    gh pr edit ${PR_NUMBER} --add-label "changes-requested"
    ;;
  REJECT)
    gh pr review ${PR_NUMBER} --request-changes --body-file "/tmp/${PR_ID}-rejection.md"
    gh pr edit ${PR_NUMBER} --add-label "rejected"
    ;;
esac

# Finalize session
npx claude-flow hooks post-task --task-id "code-review-${PR_ID}" --export-metrics true
```

---

## Success Criteria

### Review Quality Metrics
- **Coverage**: All quality dimensions reviewed (code, security, performance, architecture, docs)
- **Consistency**: Reviews follow established guidelines and standards
- **Actionability**: All feedback is specific, constructive, and actionable
- **Timeliness**: Reviews completed within 4 hours (business hours)

### Code Quality Gates
- **Automated Tests**: 100% passing (no failing tests)
- **Code Coverage**: > 80% overall, > 90% for new code
- **Linting**: 0 violations (all style rules followed)
- **Security**: 0 critical issues, 0 high-severity issues
- **Performance**: No high-impact performance regressions
- **Documentation**: 100% of public APIs documented

### Process Metrics
- **Review Turnaround**: < 4 hours (from PR creation to decision)
- **Author Satisfaction**: > 4/5 (feedback is helpful and constructive)
- **Defect Escape Rate**: < 1% (issues found in production that should have been caught)
- **False Positive Rate**: < 5% (flagged issues that weren't actually problems)

---

## Usage Examples

### Example 1: Small Feature PR (Simple)

```bash
# Feature: Add email validation to registration form
PR_NUMBER=245
PR_ID="acme-app/pulls/245"

# Initialize review
./init-review.sh ${PR_NUMBER} "acme/acme-app"

# Phase 1: Automated checks (5 minutes)
./automated-checks.sh ${PR_ID}
# Output: All checks passed

# Phase 2: Specialist reviews (30 minutes - small PR)
./specialist-reviews.sh ${PR_ID}
# Output: 3 minor issues (all LOW severity)

# Phase 3: Integration analysis (10 minutes)
# Output: No integration concerns, backward compatible

# Phase 4: Final decision
./final-decision.sh ${PR_ID}
# Decision: ✅ APPROVE
# Output: "All quality checks passed. 3 minor suggestions for future consideration."
```

### Example 2: Large Refactoring PR (Complex)

```bash
# Refactoring: Migrate from REST to GraphQL
PR_NUMBER=312
PR_ID="acme-app/pulls/312"

# Initialize review
./init-review.sh ${PR_NUMBER} "acme/acme-app"

# Phase 1: Automated checks (10 minutes)
./automated-checks.sh ${PR_ID}
# Output: All checks passed, coverage 94%

# Phase 2: Specialist reviews (2 hours)
./specialist-reviews.sh ${PR_ID}
# Output: 15 findings
#   - 1 HIGH/SECURITY (authentication flow changed, needs verification)
#   - 2 HIGH/PERFORMANCE (N+1 queries in new resolvers)
#   - 3 MAJOR/ARCHITECTURE (GraphQL schema design concerns)
#   - 9 MEDIUM/LOW (documentation, minor improvements)

# Phase 3: Integration analysis (1 hour)
# Output: Breaking changes for API clients, migration guide needed
# Risk: HIGH (affects all API consumers)

# Phase 4: Final decision
./final-decision.sh ${PR_ID}
# Decision: ⏸️ REQUEST CHANGES
# Output: "3 blocking issues (security + performance). Add feature flag for gradual rollout. Provide migration guide for API clients."
```

### Example 3: Security Patch PR (Critical)

```bash
# Security: Fix SQL injection vulnerability
PR_NUMBER=418
PR_ID="acme-app/pulls/418"

# Initialize expedited review
./init-review.sh ${PR_NUMBER} "acme/acme-app"

# Phase 1: Automated checks (5 minutes)
./automated-checks.sh ${PR_ID}
# Output: All checks passed

# Phase 2: Focus on security review (30 minutes)
npx claude-flow agent spawn --type security-manager --focus "comprehensive-audit"
# Output: Vulnerability fixed correctly, no new issues introduced

# Phase 3: Integration analysis (15 minutes)
# Output: Backward compatible, zero downtime deployment

# Phase 4: Fast-track approval
./final-decision.sh ${PR_ID}
# Decision: ✅ APPROVE (EXPEDITED)
# Output: "Security fix verified. No regressions. Approved for immediate merge and deployment."

# Deploy immediately
gh pr merge ${PR_NUMBER} --admin --squash
```

---

## GraphViz Process Diagram

See `when-reviewing-pull-request-orchestrate-comprehensive-code-review-process.dot` for visual workflow representation showing:
- 4 phases with star topology coordination
- 15 specialist reviewer interactions
- Automated gate (Phase 1) preventing bad code from entering review
- Parallel specialist reviews (Phase 2) for efficiency
- Integration analysis (Phase 3) for deployment safety
- Final decision logic with author notification

---

## Quality Checklist

Before considering code review complete, verify:

- [ ] **Phase 1**: All automated checks passing (lint, tests, coverage, build)
- [ ] **Phase 2**: All specialist reviews completed, findings categorized
- [ ] **Phase 3**: Integration impact analyzed, deployment plan documented
- [ ] **Phase 4**: Final decision made, author notified, GitHub status updated

**Memory Verification**:
- [ ] `code-review/${PR_ID}/metadata` - PR information
- [ ] `code-review/${PR_ID}/phase-1/*` - Automated check results
- [ ] `code-review/${PR_ID}/phase-2/*` - Specialist review findings
- [ ] `code-review/${PR_ID}/phase-3/*` - Integration analysis
- [ ] `code-review/${PR_ID}/phase-4/final-summary` - Comprehensive report

**Feedback Quality**:
- [ ] All feedback is specific (file, line, issue clearly identified)
- [ ] All feedback is actionable (how to fix provided)
- [ ] All feedback is constructive (not just criticism, but improvement suggestions)
- [ ] Severity is appropriate (not overstating or understating issues)

---

**Workflow Complexity**: Medium (15 agents, 4 hours, 4 phases)
**Coordination Pattern**: Star topology with parallel specialist reviews
**Memory Footprint**: ~20-30 memory entries per PR review
**Typical Use Case**: Comprehensive PR review requiring validation across multiple quality dimensions
