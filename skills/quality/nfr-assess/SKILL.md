---
name: nfr-assess
description: Assess non-functional requirements across 6 quality categories (Security, Performance, Reliability, Maintainability, Scalability, Usability) with measurable criteria, evidence-based evaluation, and automated checks. Scores each category, identifies gaps with severity ratings, and provides remediation guidance. Use during quality review to evaluate production readiness and NFR compliance.
version: 2.0
category: Quality
acceptance:
  all_categories_assessed: "All 6 NFR categories (Security, Performance, Reliability, Maintainability, Scalability, Usability) scored with evidence"
  gaps_identified: "NFR gaps documented with severity ratings (CRITICAL/HIGH/MEDIUM) and remediation guidance"
  automated_checks_executed: "Automated checks run where available (security scans, linting, test coverage, performance tests)"
  report_generated: "Complete NFR assessment report generated with overall score, category scores, gap summary, and recommendations"
inputs:
  task_id:
    required: true
    description: "Task identifier to assess (e.g., 'task-007')"
  task_file:
    required: true
    description: "Path to task specification file"
  config_file:
    required: false
    description: "Path to project configuration (defaults to .claude/config.yaml)"
  nfr_thresholds:
    required: false
    description: "Custom NFR thresholds (security, performance, maintainability)"
outputs:
  overall_nfr_score:
    description: "Weighted overall NFR score (0-100)"
  category_scores:
    description: "Individual scores for each of 6 NFR categories"
  overall_status:
    description: "Overall NFR status (PASS/CONCERNS/FAIL)"
  critical_gaps_count:
    description: "Number of critical NFR gaps (P0)"
  high_gaps_count:
    description: "Number of high-severity NFR gaps (P1)"
  report_path:
    description: "Path to generated NFR assessment report"
  quality_gate_impact:
    description: "Predicted impact on quality gate (PASS/CONCERNS/FAIL)"
telemetry:
  emit: "skill.nfr-assess.completed"
  track:
    - task_id
    - overall_nfr_score
    - overall_status
    - security_score
    - performance_score
    - reliability_score
    - maintainability_score
    - scalability_score
    - usability_score
    - critical_gaps_count
    - high_gaps_count
    - automated_checks_run
    - assessment_duration_ms
---

# Non-Functional Requirements Assessment

The **nfr-assess** skill performs comprehensive evaluation of non-functional requirements (NFRs) to ensure the implementation meets quality attributes beyond functional correctness. NFRs are cross-cutting concerns that determine system quality, reliability, and long-term viability. This skill assesses 6 critical quality categories with measurable criteria, evidence-based evaluation, and automated checks where possible.

Unlike functional requirements that define *what* the system does, non-functional requirements define *how well* the system performs. This skill provides objective assessment across Security (authentication, encryption, vulnerabilities), Performance (response times, throughput, resource usage), Reliability (error handling, monitoring, fault tolerance), Maintainability (code quality, documentation, testability), Scalability (horizontal scaling, database design, async processing), and Usability (API design, error messages, documentation).

The assessment produces a weighted overall NFR score, individual category scores, identifies gaps with severity ratings, and provides actionable recommendations. Results feed directly into the quality-gate skill to inform merge/release decisions. Automated checks (security scans, linting, test coverage, performance tests) are integrated where available to provide objective, reproducible metrics.

## When to Use This Skill

**This skill should be used when:**
- Non-functional quality attributes need validation during implementation review
- System-wide quality concerns (security, performance, reliability) need assessment
- Gaps in quality attributes need identification with severity ratings
- Evidence-based NFR reports are required for audit/compliance
- NFR metrics need to feed into quality gate decision-making
- Production readiness needs validation from quality perspective

**This skill is particularly valuable:**
- Before quality gate review (identifies issues early)
- After functional testing completes (assess non-functional aspects)
- During architectural review (validate design patterns for NFRs)
- When preparing for production deployment (ensure production readiness)
- For compliance validation (OWASP, WCAG, performance budgets)

**This skill should NOT be used when:**
- Functional requirements haven't been implemented yet (assess functionality first)
- Task is purely planning/design (no implementation to assess)
- You only need to test functional behavior (use run-tests instead)

## Prerequisites

Before running nfr-assess, ensure you have:

1. **Task specification file** with implementation record
2. **Project configuration** (.claude/config.yaml) with quality settings
3. **Implementation files** accessible for code review
4. **Automated tools available** (optional but recommended):
   - Security: `npm audit`, `semgrep`, or equivalent
   - Code quality: linter (eslint, pylint, etc.)
   - Test coverage: coverage tools (jest --coverage, pytest-cov, etc.)
   - Performance: load testing tools (artillery, k6, etc.)

**Dependencies on other skills:**
- Optional: risk-profile (provides security/performance risk context)
- Optional: trace-requirements (provides implementation evidence)
- Optional: test-design (provides performance/load test specifications)

## Sequential NFR Assessment Process

This skill executes through 9 sequential steps. Each step must complete successfully before proceeding. The process is designed to systematically evaluate all 6 NFR categories with evidence collection, automated checks, and gap identification.

### Step 0: Load Configuration and Context

**Purpose:** Load project configuration, task specification, and all relevant context needed for NFR assessment. Identify implementation files, prepare automated checks, and determine which NFR categories are most relevant based on task type.

**Actions:**
1. Load project configuration from `.claude/config.yaml` (quality settings, NFR thresholds)
2. Read task specification file (extract task ID, title, type, NFR requirements, implementation record)
3. Load related assessments if available (risk profile, traceability matrix, test design)
4. Identify implementation files from implementation record (source, config, infrastructure, dependencies)
5. Identify relevant NFR categories based on task type (e.g., API tasks prioritize Security/Performance)
6. Prepare automated checks (security scans, linting, test coverage, performance tests)
7. Prepare output file path (`.claude/quality/assessments/{task-id}-nfr-{YYYYMMDD}.md`)

**Halt If:**
- Config file missing or invalid
- Task file not found
- Cannot create output directory

**Output:** Configuration loaded, task spec loaded, related assessments checked, implementation files identified, NFR categories prioritized, automated checks prepared, output path set

**See:** `references/templates.md#step-0-configuration-loading-output` for complete format and [nfr-categories.md](references/nfr-categories.md) for category descriptions

---

### Step 1: Security Assessment

**Purpose:** Evaluate security posture including authentication, authorization, input validation, dependency vulnerabilities, and security best practices. Leverage automated security scans (npm audit, semgrep) and manual code review to identify security gaps with evidence.

**Actions:**
1. Define security criteria (10 criteria: authentication, authorization, input validation, output encoding, dependency vulnerabilities, secrets management, HTTPS/TLS, rate limiting, CORS, security headers)
2. Run automated security checks:
   - Dependency vulnerability scan (`npm audit --json` or equivalent)
   - Code security scan (`semgrep --config=auto` if available)
   - Secret detection (check for hardcoded credentials)
3. Manual code review for security:
   - Search for authentication/authorization code
   - Check input validation implementation (Zod, Joi, etc.)
   - Check for SQL injection risks (parameterized queries?)
   - Check for XSS risks (output encoding?)
   - Check CORS configuration and rate limiting
4. Collect evidence for each criterion (file paths, line numbers, code snippets, scan results)
5. Score each criterion (PASS/CONCERNS/FAIL/UNCLEAR)
6. Calculate overall security score (weighted average: PASS=100, CONCERNS=50, FAIL=0)
7. Identify security gaps with severity ratings (CRITICAL/HIGH/MEDIUM)

**Output:** Overall security score, criteria breakdown (PASS/CONCERNS/FAIL), automated check results (vulnerabilities, secrets), critical gaps count

**See:** `references/templates.md#step-1-security-assessment-output` for complete format, [nfr-categories.md](references/nfr-categories.md#security-assessment) for criteria, [nfr-examples.md](references/nfr-examples.md#security-evidence) for evidence examples

---

### Step 2: Performance Assessment

**Purpose:** Evaluate performance characteristics including response times, throughput, resource usage, caching, and optimization. Run performance tests if available, analyze database queries for N+1 problems, and check algorithm complexity in hot paths.

**Actions:**
1. Define performance criteria (10 criteria: response time, throughput, resource usage, database queries, caching, asset optimization, algorithm complexity, connection pooling, async operations, load testing)
2. Run automated performance checks:
   - Performance tests (`npm run test:perf` if available)
   - Load tests (artillery, k6, etc. if available)
   - Bundle size analysis (if UI application)
   - Database query analysis (EXPLAIN ANALYZE)
3. Manual code review for performance:
   - Check database queries for N+1 problems
   - Check for blocking operations in request handlers
   - Check algorithm complexity in hot paths (O(n log n) or better?)
   - Check caching implementation (Redis, in-memory)
   - Check connection pooling configuration
4. Collect evidence (performance test results, query analysis, code review findings)
5. Score each criterion (PASS/CONCERNS/FAIL/UNCLEAR)
6. Calculate overall performance score
7. Identify performance gaps (e.g., missing caching, N+1 queries, no load testing)

**Output:** Overall performance score, response time metrics (p50/p95/p99), throughput, load test results, performance gaps

**See:** `references/templates.md#step-2-performance-assessment-output` for complete format with benchmark tables

---

### Step 3: Reliability Assessment

**Purpose:** Evaluate system reliability including error handling, fault tolerance, recovery, monitoring, and logging. Check for comprehensive error handling, graceful degradation when dependencies fail, and proper observability (logging, monitoring, health checks).

**Actions:**
1. Define reliability criteria (10 criteria: error handling, input validation errors, graceful degradation, retry logic, circuit breakers, logging, monitoring, idempotency, data integrity, disaster recovery)
2. Manual code review for reliability:
   - Check try-catch blocks in async operations
   - Check error response formatting
   - Check database transaction usage
   - Check logging implementation (winston, pino, structured logs?)
   - Check health check endpoints
   - Check monitoring integration (Prometheus, Datadog, etc.)
3. Collect evidence (error handlers, logging examples, monitoring configuration)
4. Score each criterion (PASS/CONCERNS/FAIL/UNCLEAR)
5. Calculate overall reliability score
6. Identify reliability gaps (e.g., no monitoring, no log aggregation, missing health checks)

**Output:** Overall reliability score, error handling status, logging status (structured/aggregation), monitoring status (health checks/metrics), reliability gaps

**See:** `references/templates.md#step-3-reliability-assessment-output` for complete format

---

### Step 4: Maintainability Assessment

**Purpose:** Evaluate code maintainability including code quality, documentation, testability, modularity, and technical debt. Leverage automated tools (linting, test coverage, complexity analysis) and manual review for documentation, naming, and code organization.

**Actions:**
1. Define maintainability criteria (10 criteria: code quality, test coverage, documentation, modularity, naming, complexity, duplication, type safety, dependencies, technical debt)
2. Run automated maintainability checks:
   - Linting (`npm run lint` or equivalent)
   - Test coverage (`npm run test:coverage`)
   - Complexity analysis (cyclomatic complexity ≤10?)
   - Duplication detection (jscpd, etc.)
   - Type checking (TypeScript strict mode)
3. Manual code review for maintainability:
   - Check code structure and organization
   - Check naming conventions (clear, descriptive?)
   - Check function/class sizes (≤50 lines?)
   - Check documentation completeness (README, API docs, JSDoc)
   - Check for technical debt (TODO/FIXME comments)
4. Collect evidence (coverage reports, complexity metrics, lint results, documentation)
5. Score each criterion (PASS/CONCERNS/FAIL/UNCLEAR)
6. Calculate overall maintainability score
7. Identify maintainability gaps (e.g., missing documentation, high complexity, low coverage)

**Output:** Overall maintainability score, test coverage %, avg/max complexity, linting results, documentation status, maintainability gaps

**See:** `references/templates.md#step-4-maintainability-assessment-output` for complete format with metrics breakdown

---

### Step 5: Scalability Assessment

**Purpose:** Evaluate system scalability including horizontal/vertical scaling capability, load handling, database design, and caching strategy. Check for stateless design, proper database indexing, async processing for expensive operations, and readiness for load balancing.

**Actions:**
1. Define scalability criteria (10 criteria: stateless design, horizontal scaling, database design, connection pooling, caching, async processing, rate limiting, load balancing readiness, resource limits, auto-scaling)
2. Review architecture for scalability:
   - Check if application is stateless (no in-memory session state)
   - Check database schema and indexing (foreign keys indexed?)
   - Check for file uploads (should use object storage like S3)
   - Check for background job processing (should use queue like Bull/BullMQ)
   - Check for proper shutdown handlers (graceful shutdown)
3. Collect evidence (architecture review, schema analysis, code review)
4. Score each criterion (PASS/CONCERNS/FAIL/UNCLEAR)
5. Calculate overall scalability score
6. Identify scalability gaps (e.g., stateful design, missing indexes, no async processing)

**Output:** Overall scalability score, stateless design status, database indexing (count/missing), async processing status, horizontal scaling readiness, scalability gaps

**See:** `references/templates.md#step-5-scalability-assessment-output` for complete format with DB analysis

---

### Step 6: Usability Assessment

**Purpose:** Evaluate system usability including API design, error messages, documentation, and accessibility (if UI). For APIs, check RESTful conventions, error message clarity, and API documentation. For UIs, check WCAG compliance, responsive design, and user experience.

**Actions:**
1. Define usability criteria:
   - **For APIs** (10 criteria): API design, error messages, documentation, versioning, pagination, filtering, HTTP status codes, response format, HATEOAS, developer experience
   - **For UIs** (10 criteria): accessibility (WCAG 2.1 AA), responsive design, loading states, error handling, keyboard navigation, color contrast, screen reader support, form validation, intuitive navigation, performance
2. Review API/UI design:
   - Check REST conventions (proper HTTP verbs, resource naming)
   - Check error response format (clear, actionable messages?)
   - Check API documentation (OpenAPI/Swagger spec?)
   - Check pagination/filtering implementation
   - For UIs: Check accessibility with automated tools (axe, lighthouse)
3. Collect evidence (route definitions, error responses, documentation, accessibility scan results)
4. Score each criterion (PASS/CONCERNS/FAIL/UNCLEAR)
5. Calculate overall usability score
6. Identify usability gaps (e.g., missing API docs, generic error messages, accessibility issues)

**Output:** Overall usability score, API/UI design status, error messages quality, documentation status, accessibility status (if UI), usability gaps

**See:** `references/templates.md#step-6-usability-assessment-output` for API and UI formats

---

### Step 7: Generate NFR Assessment Report

**Purpose:** Create comprehensive NFR assessment report using template with all category assessments, overall score calculation, gap summary, and recommendations.

**Actions:**
1. Load NFR assessment template
2. Compute overall NFR score using weighted formula (Security 25%, Performance 20%, Reliability 20%, Maintainability 15%, Scalability 10%, Usability 10%)
3. Determine overall status (≥90%: Excellent, 75-89%: Good, 60-74%: CONCERNS, <60%: FAIL)
4. Aggregate gaps with priorities (P0/P1/P2)
5. Generate prioritized recommendations
6. Predict quality gate impact
7. Populate template and write report

**Output:** Report path, overall NFR score/status, category scores, total gaps breakdown (P0/P1/P2), report size

**See:** `references/templates.md#step-7-overall-nfr-scoring-formula` for complete formula and examples, [nfr-scoring.md](references/nfr-scoring.md) for methodology, [nfr-gaps.md](references/nfr-gaps.md) for gap categorization

---

### Step 8: Present Summary to User

**Purpose:** Provide concise summary with key metrics, critical gaps, quality gate impact, and recommended next steps.

**Actions:**
1. Display formatted summary: Task metadata, overall NFR score/status, category scores (6), critical gaps (P0), high gaps (P1), quality gate impact + reasoning, actionable recommendations with time estimates, report path
2. Suggest next steps: Review report, prioritize P0 gaps, create tickets for P1 gaps, re-run after fixes, proceed to quality-gate when ≥75%
3. Emit telemetry

**Output:** Complete formatted summary with scores, gaps, quality gate prediction, recommendations, next steps

**See:** `references/templates.md#step-8-complete-user-summary-format` for full formatted output, [nfr-examples.md](references/nfr-examples.md#summary-formats) for examples

---

## Integration with Other Skills

**Integration with risk-profile:** Security/performance/reliability risks from risk profile inform NFR assessment priorities and amplify gap severity (e.g., HIGH gap + HIGH risk = CRITICAL P0)

**Integration with trace-requirements:** Implementation evidence validates NFR implementation; NFR gaps feed back as coverage gaps in traceability matrix

**Integration with test-design:** Performance/load/security test specifications inform corresponding NFR category assessments

**Integration with quality-gate:** Overall NFR score + category scores + critical gaps feed into quality gate decision (≥90%: PASS-excellent, 75-89%: PASS-good, 60-74%: CONCERNS, <60%: FAIL; Security/Reliability <50%: production blocker)

**See:** `references/templates.md#integration-examples` for detailed integration workflows and decision logic

---

## Best Practices

Run NFR assessment before quality gate | Integrate automated checks (security, linting, coverage) | Document evidence thoroughly (file paths, line numbers, snippets) | Prioritize Security and Reliability (production blockers) | Set measurable thresholds in config | Re-run after fixes to validate | Customize category weights per project | Review with stakeholders (cross-functional decisions)

---

## References

- **[templates.md](references/templates.md)** - All output formats, complete examples, scoring formulas, integration workflows, JSON structures

- **[nfr-categories.md](references/nfr-categories.md)** - Detailed assessment criteria for all 6 NFR categories with examples and thresholds

- **[nfr-scoring.md](references/nfr-scoring.md)** - Scoring methodology, weighting formulas, status thresholds, automated check integration

- **[nfr-gaps.md](references/nfr-gaps.md)** - Gap identification, severity levels (CRITICAL/HIGH/MEDIUM), prioritization (P0/P1/P2), remediation guidance

- **[nfr-examples.md](references/nfr-examples.md)** - Complete example assessments, evidence formats, benchmarks, summary outputs

---

*NFR Assessment skill - Version 2.0 - Minimal V2 Architecture*
