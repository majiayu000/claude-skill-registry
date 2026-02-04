---
name: ln-501-code-quality-checker
description: "Worker that checks DRY/KISS/YAGNI/architecture compliance with quantitative Code Quality Score. Validates architectural decisions via MCP Ref: (1) Optimality - is chosen approach the best? (2) Compliance - does it follow best practices? (3) Performance - algorithms, configs, bottlenecks. Reports issues with SEC-, PERF-, MNT-, ARCH-, BP-, OPT- prefixes."
---

# Code Quality Checker

Analyzes Done implementation tasks with quantitative Code Quality Score based on metrics, MCP Ref validation, and issue penalties.

## Purpose & Scope
- Load Story and Done implementation tasks (exclude test tasks)
- Calculate Code Quality Score using metrics and issue penalties
- **MCP Ref validation:** Verify optimality, best practices, and performance via external sources
- Check for DRY/KISS/YAGNI violations, architecture boundary breaks, security issues
- Produce quantitative verdict with structured issue list; never edits Linear or kanban

## Code Metrics

| Metric | Threshold | Penalty |
|--------|-----------|---------|
| **Cyclomatic Complexity** | ≤10 OK, 11-20 warning, >20 fail | -5 (warning), -10 (fail) per function |
| **Function size** | ≤50 lines OK, >50 warning | -3 per function |
| **File size** | ≤500 lines OK, >500 warning | -5 per file |
| **Nesting depth** | ≤3 OK, >3 warning | -3 per instance |
| **Parameter count** | ≤4 OK, >4 warning | -2 per function |

## Code Quality Score

Formula: `Code Quality Score = 100 - metric_penalties - issue_penalties`

**Issue penalties by severity:**

| Severity | Penalty | Examples |
|----------|---------|----------|
| **high** | -20 | Security vulnerability, O(n²)+ algorithm, N+1 query |
| **medium** | -10 | DRY violation, suboptimal approach, missing config |
| **low** | -3 | Naming convention, minor code smell |

**Score interpretation:**

| Score | Status | Verdict |
|-------|--------|---------|
| 90-100 | Excellent | PASS |
| 70-89 | Acceptable | CONCERNS |
| <70 | Below threshold | ISSUES_FOUND |

## Issue Prefixes

| Prefix | Category | Default Severity | MCP Ref |
|--------|----------|------------------|---------|
| SEC- | Security (auth, validation, secrets) | high | — |
| PERF- | Performance (algorithms, configs, bottlenecks) | medium/high | ✓ Required |
| MNT- | Maintainability (DRY, SOLID, complexity) | medium | — |
| ARCH- | Architecture (layers, boundaries, patterns) | medium | — |
| BP- | Best Practices (implementation differs from recommended) | medium | ✓ Required |
| OPT- | Optimality (better approach exists for this goal) | medium | ✓ Required |

**PERF- subcategories:**

| Prefix | Category | Severity |
|--------|----------|----------|
| PERF-ALG- | Algorithm complexity (Big O) | high if O(n²)+ |
| PERF-CFG- | Package/library configuration | medium |
| PERF-PTN- | Architectural pattern performance | high |
| PERF-DB- | Database queries, indexes | high |

## When to Use
- **Invoked by ln-500-story-quality-gate** Pass 1 (first gate)
- All implementation tasks in Story status = Done
- Before regression testing (ln-502) and test planning (ln-510)

## Workflow (concise)
1) Load Story (full) and Done implementation tasks (full descriptions) via Linear; skip tasks with label "tests".
2) Collect affected files from tasks (Affected Components/Existing Code Impact) and recent commits/diffs if noted.
3) **Calculate code metrics:**
   - Cyclomatic Complexity per function (target ≤10)
   - Function size (target ≤50 lines)
   - File size (target ≤500 lines)
   - Nesting depth (target ≤3)
   - Parameter count (target ≤4)

3.5) **MCP Ref Validation (MANDATORY for code changes):**

   **Level 1 — OPTIMALITY (OPT-):**
   - Extract goal from task (e.g., "user authentication", "caching", "API rate limiting")
   - Research alternatives: `ref_search_documentation("{goal} approaches comparison {tech_stack} 2026")`
   - Compare chosen approach vs alternatives for project context
   - Flag suboptimal choices as OPT- issues

   **Level 2 — BEST PRACTICES (BP-):**
   - Research: `ref_search_documentation("{chosen_approach} best practices {tech_stack} 2026")`
   - For libraries: `query-docs(library_id, "best practices implementation patterns")`
   - Flag deviations from recommended patterns as BP- issues

   **Level 3 — PERFORMANCE (PERF-):**
   - **PERF-ALG:** Analyze algorithm complexity (detect O(n²)+, research optimal via MCP Ref)
   - **PERF-CFG:** Check library configs (connection pooling, batch sizes, timeouts) via `query-docs`
   - **PERF-PTN:** Research pattern pitfalls: `ref_search_documentation("{pattern} performance bottlenecks")`
   - **PERF-DB:** Check for N+1, missing indexes via `query-docs(orm_library_id, "query optimization")`

   **Triggers for MCP Ref validation:**
   - New dependency added (package.json/requirements.txt changed)
   - New pattern/library used
   - API/database changes
   - Loops/recursion in critical paths
   - ORM queries added

4) **Analyze code for static issues (assign prefixes):**
   - SEC-: hardcoded creds, unvalidated input, SQL injection, race conditions
   - MNT-: DRY violations, dead code, complex conditionals, poor naming
   - ARCH-: layer violations, circular dependencies, guide non-compliance

5) **Calculate Code Quality Score:**
   - Start with 100
   - Subtract metric penalties (see Code Metrics table)
   - Subtract issue penalties (see Issue penalties table)

6) Output verdict with score and structured issues. Add Linear comment with findings.

## Critical Rules
- Read guides mentioned in Story/Tasks before judging compliance.
- **MCP Ref validation:** For ANY architectural change, MUST verify via ref_search_documentation before judging.
- **Context7 for libraries:** When reviewing library usage, query-docs to verify correct patterns.
- Language preservation in comments (EN/RU).
- Do not create tasks or change statuses; caller decides next actions.

## Definition of Done
- Story and Done implementation tasks loaded (test tasks excluded).
- Code metrics calculated (Cyclomatic Complexity, function/file sizes).
- **MCP Ref validation completed:**
  - OPT-: Optimality checked (is chosen approach the best for the goal?)
  - BP-: Best practices verified (correct implementation of chosen approach?)
  - PERF-: Performance analyzed (algorithms, configs, patterns, DB)
- Issues identified with prefixes and severity, sources from MCP Ref/Context7.
- Code Quality Score calculated.
- **Output format:**
  ```yaml
  verdict: PASS | CONCERNS | ISSUES_FOUND
  code_quality_score: {0-100}
  metrics:
    avg_cyclomatic_complexity: {value}
    functions_over_50_lines: {count}
    files_over_500_lines: {count}
  issues:
    # OPTIMALITY
    - id: "OPT-001"
      severity: medium
      file: "src/auth/index.ts"
      goal: "User session management"
      finding: "Suboptimal approach for session management"
      chosen: "Custom JWT with localStorage"
      recommended: "httpOnly cookies + refresh token rotation"
      reason: "httpOnly cookies prevent XSS token theft"
      source: "ref://owasp-session-management"

    # BEST PRACTICES
    - id: "BP-001"
      severity: medium
      file: "src/api/routes.ts"
      finding: "POST for idempotent operation"
      best_practice: "Use PUT for idempotent updates (RFC 7231)"
      source: "ref://api-design-guide#idempotency"

    # PERFORMANCE - Algorithm
    - id: "PERF-ALG-001"
      severity: high
      file: "src/utils/search.ts:42"
      finding: "Nested loops cause O(n²) complexity"
      current: "O(n²) - nested filter().find()"
      optimal: "O(n) - use Map/Set for lookup"
      source: "ref://javascript-performance#data-structures"

    # PERFORMANCE - Config
    - id: "PERF-CFG-001"
      severity: medium
      file: "src/db/connection.ts"
      finding: "Missing connection pool config"
      current_config: "default (pool: undefined)"
      recommended: "pool: { min: 2, max: 10 }"
      source: "context7://pg#connection-pooling"

    # PERFORMANCE - Database
    - id: "PERF-DB-001"
      severity: high
      file: "src/repositories/user.ts:89"
      finding: "N+1 query pattern detected"
      issue: "users.map(u => u.posts) triggers N queries"
      solution: "Use eager loading: include: { posts: true }"
      source: "context7://prisma#eager-loading"

    # MAINTAINABILITY
    - id: "MNT-001"
      severity: medium
      file: "src/service.ts:42"
      finding: "DRY violation: duplicate validation logic"
      suggested_action: "Extract to shared validator"
  ```
- Linear comment posted with findings.

## Reference Files
- Code metrics: `references/code_metrics.md` (thresholds and penalties)
- Guides: `docs/guides/`
- Templates for context: `shared/templates/task_template_implementation.md`

---
**Version:** 5.0.0 (Added 3-level MCP Ref validation: Optimality, Best Practices, Performance with PERF-ALG/CFG/PTN/DB subcategories)
**Last Updated:** 2026-01-29
