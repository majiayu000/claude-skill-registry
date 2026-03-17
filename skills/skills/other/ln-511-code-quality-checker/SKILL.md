---
name: ln-511-code-quality-checker
description: "Worker that checks DRY/KISS/YAGNI/architecture compliance with quantitative Code Quality Score. Validates architectural decisions via MCP Ref: (1) Optimality (2) Compliance (3) Performance. Reports issues with SEC-, PERF-, MNT-, ARCH-, BP-, OPT- prefixes."
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

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
| MNT- | Maintainability (DRY, SOLID, complexity, dead code) | medium | — |
| ARCH- | Architecture (layers, boundaries, patterns, contracts) | medium | — |
| BP- | Best Practices (implementation differs from recommended) | medium | ✓ Required |
| OPT- | Optimality (better approach exists for this goal) | medium | ✓ Required |

**OPT- subcategories:**

| Prefix | Category | Severity |
|--------|----------|----------|
| OPT-OSS- | Open-source replacement available (cross-ref ln-645 audit) | medium (high if >200 LOC) |

**ARCH- subcategories:**

| Prefix | Category | Severity |
|--------|----------|----------|
| ARCH-LB- | Layer Boundary: I/O outside infra, HTTP in domain | high |
| ARCH-TX- | Transaction Boundaries: commit() in 3+ layers, mixed UoW ownership | high (CRITICAL if auth/payment) |
| ARCH-DTO- | Missing DTO (4+ params without DTO), Entity Leakage (ORM entity in API response) | medium (high if auth/payment) |
| ARCH-DI- | Dependency Injection: direct instantiation in business logic, mixed DI+imports | medium |
| ARCH-CEH- | Centralized Error Handling: no global handler, stack traces in prod, uncaughtException | medium (high if no handler at all) |
| ARCH-SES- | Session Ownership: DI session + local session in same module | medium |
| ARCH-AI-SEB | Side-Effect Breadth: 3+ side-effect categories in one function | medium |
| ARCH-AI-AH | Architectural Honesty: read-named function with write side-effects | medium |
| ARCH-AI-FO | Flat Orchestration: service imports 3+ other services | medium |

**PERF- subcategories:**

| Prefix | Category | Severity |
|--------|----------|----------|
| PERF-ALG- | Algorithm complexity (Big O) | high if O(n²)+ |
| PERF-CFG- | Package/library configuration | medium |
| PERF-PTN- | Architectural pattern performance | high |
| PERF-DB- | Database queries, indexes | high |

**MNT- subcategories:**

| Prefix | Category | Severity |
|--------|----------|----------|
| MNT-DC- | Dead code: replaced implementations, unused exports/re-exports, backward-compat wrappers, deprecated aliases | medium (high if public API) |
| MNT-DRY- | DRY violations: duplicate logic across files | medium |
| MNT-GOD- | God Classes: class with >15 methods or >500 lines (not just file size) | medium (high if >1000 lines) |
| MNT-SIG- | Method Signature Quality: boolean flag params, unclear return types, inconsistent naming, >5 optional params | low |
| MNT-ERR- | Error Contract inconsistency: mixed raise + return None in same service | medium |

## When to Use
- **Invoked by ln-510-quality-coordinator** Phase 2
- All implementation tasks in Story status = Done
- Before ln-512 tech debt cleanup and ln-513 agent review

## Workflow (concise)
1) Load Story (full) and Done implementation tasks (full descriptions) via Linear; skip tasks with label "tests".
2) Collect affected files from tasks (Affected Components/Existing Code Impact) and recent commits/diffs if noted.
3) **Calculate code metrics:**
   - Cyclomatic Complexity per function (target ≤10)
   - Function size (target ≤50 lines)
   - File size (target ≤500 lines)
   - Nesting depth (target ≤3)
   - Parameter count (target ≤4)

4) **MCP Ref Validation (MANDATORY for code changes — SKIP if `--skip-mcp-ref` flag passed):**

   > **Fast-track mode:** When invoked with `--skip-mcp-ref`, skip this entire step (no OPT-, BP-, PERF- checks). Proceed directly to step 5 (static analysis). This reduces cost from ~5000 to ~800 tokens while preserving metrics + static analysis coverage.

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

5) **Analyze code for static issues (assign prefixes):**
   **MANDATORY READ:** `shared/references/clean_code_checklist.md`
   - SEC-: hardcoded creds, unvalidated input, SQL injection, race conditions
   - MNT-: DRY violations (MNT-DRY-: duplicate logic), dead code (MNT-DC-: per checklist), complex conditionals, poor naming
   - **MNT-DRY- cross-story hotspot scan:** Grep for common pattern signatures (error handlers: `catch.*Error|handleError`, validators: `validate|isValid`, config access: `getSettings|getConfig`) across ALL `src/` files (count mode). If any pattern appears in 5+ files, sample 3 files (Read 50 lines each) and check structural similarity. If >80% similar → MNT-DRY-CROSS (medium, -10 points): `Pattern X duplicated in N files — extract to shared module.`
   - **MNT-DC- cross-story unused export scan:** For each file modified by Story, count `export` declarations. Then Grep across ALL `src/` for import references to those exports. Exports with 0 import references → MNT-DC-CROSS (medium, -10 points): `{export} in {file} exported but never imported — remove or mark internal.`
   - **OPT-OSS- cross-reference ln-645 (static, fast-track safe):** IF `docs/project/.audit/ln-640/*/645-open-source-replacer*.md` exists (glob across dates, take latest), check if any HIGH-confidence replacement matches files changed in current Story. IF match found → create OPT-OSS-{N} issue with module path, goal, recommended package, confidence, stars, license from ln-645 report. Severity: high if >200 LOC, medium otherwise. This check reads local files only — no MCP calls — runs even with `--skip-mcp-ref`.
   - ARCH-: layer violations, circular dependencies, guide non-compliance
   - ARCH-LB-: layer boundary violations (HTTP/DB/FS calls outside infrastructure layer)
   - ARCH-TX-: transaction boundary violations (commit() across multiple layers)
   - ARCH-DTO-: missing DTOs (4+ repeated params), entity leakage (ORM entities returned from API)
   - ARCH-DI-: direct instantiation in business logic (no DI container or mixed patterns)
   - ARCH-CEH-: centralized error handling absent or bypassed
   - ARCH-SES-: session ownership conflicts (DI + local session in same module)
   - ARCH-AI-SEB: side-effect breadth (3+ categories in one function)
   - ARCH-AI-AH: architectural honesty (read-named function with hidden writes)
   - ARCH-AI-FO: flat orchestration (service importing 3+ services)
   - MNT-GOD-: god classes (>15 methods or >500 lines per class)
   - MNT-SIG-: method signature quality (boolean flags, unclear returns)
   - MNT-ERR-: error contract inconsistency (mixed raise/return patterns in same service)

6) **Calculate Code Quality Score:**
   - Start with 100
   - Subtract metric penalties (see Code Metrics table)
   - Subtract issue penalties (see Issue penalties table)

7) Output verdict with score and structured issues. Add Linear comment with findings.

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
- ARCH- subcategories checked (LB, TX, DTO, DI, CEH, SES); MNT- subcategories checked (DC, DRY, GOD, SIG, ERR).
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

    # OPTIMALITY - OSS Replacement (from ln-645, fast-track safe)
    - id: "OPT-OSS-001"
      severity: high
      file: "src/utils/email-validator.ts"
      goal: "Email validation with MX checking"
      finding: "Custom 245-line module has HIGH-confidence OSS replacement"
      chosen: "Custom email-validator.ts (245 lines)"
      recommended: "zod + zod-email (28k stars, MIT, 95% coverage)"
      reason: "Battle-tested, actively maintained, reduces maintenance burden"
      source: "ln-645-audit"

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

    # ARCHITECTURE - Entity Leakage
    - id: "ARCH-DTO-001"
      severity: high
      file: "src/api/users.ts:35"
      finding: "ORM entity returned directly from API endpoint"
      issue: "User entity with password hash exposed in GET /users response"
      fix: "Create UserResponseDTO, map entity → DTO before return"

    # ARCHITECTURE - Centralized Error Handling
    - id: "ARCH-CEH-001"
      severity: medium
      file: "src/app.ts"
      finding: "No global error handler registered"
      issue: "Unhandled exceptions return stack traces to client in production"
      fix: "Add app.use(globalErrorHandler) with sanitized error responses"

    # MAINTAINABILITY - God Class
    - id: "MNT-GOD-001"
      severity: medium
      file: "src/services/order-service.ts"
      finding: "God class with 22 methods and 680 lines"
      issue: "OrderService handles creation, payment, shipping, notifications"
      fix: "Extract PaymentService, ShippingService, NotificationService"

    # MAINTAINABILITY - Dead Code
    - id: "MNT-DC-001"
      severity: medium
      file: "src/auth/legacy-adapter.ts"
      finding: "Backward-compatibility wrapper kept after migration"
      dead_code: "legacyLogin() wraps newLogin() — callers already migrated"
      action: "Delete legacy-adapter.ts, remove re-export from index.ts"

    # MAINTAINABILITY - DRY
    - id: "MNT-DRY-001"
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
- **Clean code checklist:** `shared/references/clean_code_checklist.md`

---
**Version:** 5.0.0
**Last Updated:** 2026-01-29
