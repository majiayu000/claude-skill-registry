---
name: multi-agent-review
description: Perform comprehensive multi-agent parallel code review using Wave/Gate architecture. Simulates security, performance, maintainability, requirements, and operations reviewers.
---

I need a comprehensive multi-agent parallel code review using the Wave/Gate architecture.

CODE TO REVIEW:
[paste code or specify: "Review all files in src/auth/"]

ARCHITECTURE:
Wave 1 (Parallel) → Gate 1 (Sequential) → Wave 2 (Parallel) → Gate 2 (Sequential) → Wave 3 (Sequential)

Execute this workflow:

═══════════════════════════════════════════════════════════════
WAVE 1: PARALLEL INDEPENDENT ANALYSIS
═══════════════════════════════════════════════════════════════

Launch 5 parallel tasks. Each task is independent and can run simultaneously.

TASK 1: Security Review
Role: Security Engineer
Focus:
- OWASP Top 10 vulnerabilities
- Input validation and sanitization
- Authentication and authorization flaws
- SQL injection, XSS, CSRF, SSRF
- Secret management and data exposure
- API security and rate limiting
- Cryptography usage

Output JSON format:
{
  "issues": [
    {
      "id": "SEC-001",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "category": "authentication|input-validation|data-exposure|cryptography",
      "cwe_id": "CWE-XXX",
      "location": "file.js:line",
      "description": "Detailed description",
      "attack_vector": "How an attacker could exploit this",
      "recommendation": "Specific fix with code example"
    }
  ],
  "security_score": 0-3,
  "summary": "One-line summary"
}

TASK 2: Performance Review
Role: Performance Engineer
Focus:
- Time complexity (O(n²), O(n³) patterns)
- Database queries (N+1, missing indexes, full table scans)
- Memory allocation and leaks
- Unnecessary loops and iterations
- Caching opportunities
- Blocking I/O operations
- Resource pooling

TASK 3: Maintainability Review
Role: Future Developer (6 months out, original author gone)
Focus:
- Code clarity and readability
- Documentation (comments, docstrings, README)
- Pattern consistency across codebase
- Naming conventions (clear, descriptive)
- Technical debt indicators
- DRY violations
- Magic numbers and hard-coded values
- Complex conditionals

TASK 4: Requirements Validation
Role: QA Engineer
Focus:
- Requirements coverage (are all requirements implemented?)
- Edge case handling
- Test coverage gaps
- Behavioral correctness
- Missing functionality
- Acceptance criteria satisfaction

TASK 5: Operations Review
Role: SRE (on-call at 3am when this breaks)
Focus:
- Failure modes and error handling
- Observability (logging, metrics, tracing)
- Timeout and retry logic
- Circuit breakers and graceful degradation
- Resource management (connections, files, memory)
- Deployment/rollback complexity
- Configuration management
- Health checks and readiness probes

═══════════════════════════════════════════════════════════════
GATE 1: CONFLICT RESOLUTION (Wait for all Wave 1 tasks)
═══════════════════════════════════════════════════════════════

After all 5 tasks complete, consolidate findings:

TASK 6: Consolidation
Role: Senior Technical Lead

Tasks:
1. DEDUPLICATE ISSUES
   - Same issue reported by multiple reviewers → merge
   - Similar issues → merge if same root cause
   - Different perspectives on same code → keep separate if addressing different concerns

2. RESOLVE SEVERITY CONFLICTS
   Rules:
   - Security CRITICAL always wins
   - Take highest severity if 2+ reviewers agree it's a problem
   - Downgrade if only 1 reviewer flagged and others cleared

3. CALCULATE CONFIDENCE
   - Found by 1 reviewer: confidence = 0.60
   - Found by 2 reviewers: confidence = 0.80
   - Found by 3+ reviewers: confidence = 0.95
   - Severity disagreement: reduce confidence by 0.15

4. IDENTIFY CROSS-CUTTING CONCERNS
   - Issues affecting multiple domains
   - Systemic patterns (same problem in multiple places)

═══════════════════════════════════════════════════════════════
WAVE 2: PARALLEL CROSS-VALIDATION
═══════════════════════════════════════════════════════════════

Launch 2-3 parallel tasks reviewing the consolidated findings.

TASK 7: Meta-Review
Role: Quality Control Lead

Check:
1. COVERAGE GAPS - What wasn't examined?
2. FALSE POSITIVES - Are flagged issues actually problems?
3. SEVERITY CALIBRATION - Are CRITICAL ratings actually critical?
4. REVIEWER QUALITY - Did reviewers follow their focus areas?
5. SYSTEMIC PATTERNS - Do issues indicate deeper architectural problems?

TASK 8: Integration Analysis
Role: Systems Architect

Check for:
- System-wide impacts of issues
- Cascading failure scenarios
- Service dependency problems
- Data flow issues across boundaries

═══════════════════════════════════════════════════════════════
GATE 2: FINAL SYNTHESIS (Wait for Wave 2)
═══════════════════════════════════════════════════════════════

TASK 9: Final Report

Generate:
1. EXECUTIVE SUMMARY
   - Total issues by severity
   - Blockers (CRITICAL issues that prevent merge/deploy)
   - Key systemic issues

2. PRIORITIZED ACTION LIST
   - Must fix before merge (CRITICAL)
   - Should fix before deploy (HIGH)
   - Can fix later (MEDIUM/LOW)

3. BLOCKING ASSESSMENT
   - BLOCKS MERGE: Has CRITICAL issues
   - BLOCKS DEPLOY: Has HIGH operational risks
   - APPROVED: Ready for production
   - APPROVED_WITH_NOTES: Deploy with monitoring plan

4. CONVERGENCE METRICS
   - Number of issues found: CRITICAL/HIGH/MEDIUM/LOW
   - Confidence level: X% high-confidence issues
   - False positive estimate: X%
   - Coverage assessment: X% of code reviewed thoroughly

═══════════════════════════════════════════════════════════════
WAVE 3: CONVERGENCE CHECK
═══════════════════════════════════════════════════════════════

Determine if another iteration is needed:

CONVERGED if:
- new_critical_count == 0 AND
- new_issue_rate < 0.10 AND
- false_positive_rate < 0.20

ESCALATE_TO_HUMAN if:
- iteration >= 3 OR
- Found conflicting CRITICAL issues OR
- Uncertain about severity

ITERATE if:
- new_critical_count > 0 OR
- new_issue_rate >= 0.10

If ITERATE: Start Wave 1 again focusing only on CRITICAL and HIGH issues.
