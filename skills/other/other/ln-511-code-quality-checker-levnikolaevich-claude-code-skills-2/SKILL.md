---
name: ln-511-code-quality-checker
description: "Checks DRY/KISS/YAGNI/architecture compliance with quantitative Code Quality Score. Use when implementation tasks are Done and need quality scoring."
allowed-tools: Read, Grep, Glob, Bash, WebFetch, mcp__Ref, mcp__context7, mcp__hex-line__outline, mcp__hex-graph__audit_workspace, mcp__hex-graph__analyze_architecture
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Code Quality Checker

**Type:** L3 Worker
**Category:** 5XX Quality

Analyzes Done implementation tasks with quantitative Code Quality Score based on metrics, MCP Ref validation, and issue penalties.

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `storyId` | Yes | args, git branch, kanban, user | Story to process |

**Resolution:** Story Resolution Chain.
**Status filter:** In Progress, To Review

**MANDATORY READ:** Load `shared/references/mcp_tool_preferences.md` and `shared/references/mcp_integration_patterns.md` - use `hex-graph` as the primary path for clone, architecture, and semantic quality evidence when the project is indexed. Fall back to Grep/Read only when graph is unavailable or unsupported.

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
| SEC-DESTR- | Destructive ops (guards: DB, FS, MIG, ENV, FORCE) | high/medium | — |
| PERF- | Performance (algorithms, configs, bottlenecks) | medium/high | ✓ Required |
| MNT- | Maintainability (DRY, SOLID, complexity, dead code) | medium | — |
| ARCH- | Architecture (layers, boundaries, patterns, contracts) | medium | — |
| BP- | Best Practices (implementation differs from recommended) | medium | ✓ Required |
| OPT- | Optimality (better approach exists for this goal) | medium | ✓ Required |

**OPT- subcategories:**

| Prefix | Category | Severity |
|--------|----------|----------|
| OPT-OSS- | Open-source replacement available | medium (high if >200 LOC) |

**ARCH- subcategories:**

| Prefix | Category | Severity |
|--------|----------|----------|
| ARCH-LB- | Layer Boundary: I/O outside infra, HTTP in domain | high |
| ARCH-TX- | Transaction Boundaries: commit() in 3+ layers, mixed UoW ownership | high (CRITICAL if auth/payment) |
| ARCH-DTO- | Missing DTO (4+ params without DTO), Entity Leakage (ORM entity in API response) | medium (high if auth/payment) |
| ARCH-DI- | Dependency Injection: dependencies not replaceable for testing (direct instantiation, no injection mechanism). Exception: small scripts/CLIs where params/closures suffice → skip | medium |
| ARCH-CEH- | Centralized Error Handling: errors silently swallowed, stack traces leak to prod, no consistent error logging. Exception: 50-line scripts → downgrade to LOW | medium (high if no handler at all) |
| ARCH-SES- | Session Ownership: DI session + local session in same module | medium |
| ARCH-AI-SEB | Side-Effect Breadth: 3+ side-effect categories in one **leaf** function. **Conflict Resolution:** orchestrator/coordinator functions (imports 3+ services AND delegates sequentially) are EXPECTED to have multiple categories — do NOT flag SEB | medium |
| ARCH-AI-AH | Architectural Honesty: read-named function with write side-effects | medium |
| ARCH-AI-FO | Flat Orchestration: **leaf** service imports 3+ other services. Orchestrator imports are expected — do NOT flag | medium |
| ARCH-EVENT- | Event Channel Consistency: publisher/subscriber name mismatch (MISMATCH), orphaned channel with no counterpart (ORPHAN) | high (mismatch), medium (orphan) |

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
- All implementation tasks in Story status = Done
- Before tech debt cleanup and inline agent review

## Workflow (concise)

**MANDATORY READ:** Load `shared/references/input_resolution_pattern.md`

1) **Resolve storyId:** Run Story Resolution Chain per guide (status filter: [In Progress, To Review]).
2) Load Story (full) and Done implementation tasks (full descriptions) via Linear; skip tasks with label "tests".
3) **Collect changed files** (`changed_files[]`):
   **MANDATORY READ:** `shared/references/git_scope_detection.md`
   - IF invoked by ln-510: use `changed_files[]` from coordinator context → proceed to Enrich step in guide
   - IF invoked standalone: run full algorithm from guide
4) **Two-Layer Detection (MANDATORY):**
   **MANDATORY READ:** `shared/references/two_layer_detection.md`
   All threshold-based findings require Layer 2 context analysis. Layer 1 finding without Layer 2 = NOT a valid finding. Before reporting any metric violation, ask: "Is this violation intentional or justified by design?" See Exception column in metrics below.

5) **Calculate code metrics:**
   - Cyclomatic Complexity per function (target ≤10; Exception: enum/switch dispatch, state machines, parser grammars → downgrade to LOW)
   - Function size (target ≤50 lines; Exception: orchestrator functions with sequential delegation)
   - File size (target ≤500 lines; Exception: config/schema/migration files, generated code)
   - Nesting depth (target ≤3)
   - Parameter count (target ≤4; Exception: builder/options patterns)

6) **MCP Ref Validation (MANDATORY for code changes — SKIP if `--skip-mcp-ref` flag passed):**
   **MANDATORY READ:** Load `shared/references/research_tool_fallback.md`

   > **Fast-track mode:** When invoked with `--skip-mcp-ref`, skip this entire step (no OPT-, BP-, PERF- checks). Proceed directly to step 6 (static analysis). This reduces cost from ~5000 to ~800 tokens while preserving metrics + static analysis coverage.

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

7) **Analyze code for static issues (assign prefixes):**
   **MANDATORY READ:** `shared/references/clean_code_checklist.md`, `shared/references/destructive_operation_safety.md`
   - For large code files, use `outline(path)` before targeted reads.
   - SEC-: hardcoded creds, unvalidated input, SQL injection, race conditions
   - SEC-DESTR-: unguarded destructive operations — use code-level guards table from destructive_operation_safety.md (loaded above). Check all 5 guard categories (DB, FS, MIG, ENV, FORCE).
   - MNT-: DRY violations (MNT-DRY-: duplicate logic), dead code (MNT-DC-: per checklist), complex conditionals, poor naming
   - **MNT-DRY- cross-story hotspot scan:** Grep for common pattern signatures (error handlers: `catch.*Error|handleError`, validators: `validate|isValid`, config access: `getSettings|getConfig`) across ALL `src/` files (count mode). If any pattern appears in 5+ files, sample 3 files (Read 50 lines each) and check structural similarity. If >80% similar → MNT-DRY-CROSS (medium, -10 points): `Pattern X duplicated in N files — extract to shared module.`
   - **MNT-DRY- preferred (hex-graph):** If hex-graph indexed, use `audit_workspace(path=scan_path, verbosity="full")`. Each clone group with 2+ members in different files = MNT-DRY-CROSS. Use returned hotspot and clone context for priority. Fall back to Grep pattern scan above if hex-graph unavailable.
   - **MNT-DC- cross-story unused export scan:** For each file modified by Story, count `export` declarations. Then Grep across ALL `src/` for import references to those exports. Exports with 0 import references → MNT-DC-CROSS (medium, -10 points): `{export} in {file} exported but never imported — remove or mark internal.`
   - **OPT-OSS- cross-reference ln-645 (static, fast-track safe):** IF `docs/project/.audit/ln-640/*/645-open-source-replacer*.md` exists (glob across dates, take latest), check if any HIGH-confidence replacement matches files changed in current Story. IF match found → create OPT-OSS-{N} issue with module path, goal, recommended package, confidence, stars, license from ln-645 report. Severity: high if >200 LOC, medium otherwise. This check reads local files only — no MCP calls — runs even with `--skip-mcp-ref`.
   - ARCH-: layer violations, circular dependencies, guide non-compliance
   - ARCH-LB-: layer boundary violations (HTTP/DB/FS calls outside infrastructure layer)
   - ARCH-TX-: transaction boundary violations (commit() across multiple layers)
   - ARCH-DTO-: missing DTOs (4+ repeated params), entity leakage (ORM entities returned from API)
   - ARCH-DI-: direct instantiation in business logic (no DI container or mixed patterns)
   - ARCH-CEH-: centralized error handling absent or bypassed
   - ARCH-SES-: session ownership conflicts (DI + local session in same module)
   - ARCH-AI-SEB: side-effect breadth (3+ categories in one **leaf** function; orchestrator functions exempt — see Conflict Resolution in table above)
   - ARCH-AI-AH: architectural honesty (read-named function with hidden writes)
   - ARCH-AI-FO: flat orchestration (**leaf** service importing 3+ services; orchestrator imports exempt)
   - ARCH-EVENT-: event channel mismatch — Grep for `NOTIFY|pg_notify|\.publish\(|\.emit\(` (publishers) and `LISTEN|\.subscribe\(|\.on\(` (subscribers) in changed_files[]. Cross-reference channel name strings. <!-- Defense-in-depth: also checked by ln-652 Rule 6 -->
   - MNT-GOD-: god classes (>15 methods or >500 lines per class)
   - MNT-SIG-: method signature quality (boolean flags, unclear returns)
   - MNT-ERR-: error contract inconsistency (mixed raise/return patterns in same service)

8) **Calculate Code Quality Score:**
   - Start with 100
   - Subtract metric penalties (see Code Metrics table)
   - Subtract issue penalties (see Issue penalties table)

9) **Output verdict with score and structured issues.**
   **MANDATORY READ:** Load `references/output_schema.md`
   Format output per schema. Add Linear comment with findings.

## Critical Rules
- Read guides mentioned in Story/Tasks before judging compliance.
- **MCP Ref validation:** For ANY architectural change, MUST verify via ref_search_documentation before judging.
- **Context7 for libraries:** When reviewing library usage, query-docs to verify correct patterns.
- Language preservation in comments (EN/RU).
- Do not create tasks or change statuses; caller decides next actions.

## Runtime Summary Artifact

**MANDATORY READ:** Load `shared/references/quality_summary_contract.md`, `shared/references/quality_worker_runtime_contract.md`

Runtime profile:
- family: `quality-worker`
- worker: `ln-511`
- summary kind: `quality-worker`
- payload fields used by coordinators: `worker`, `status`, `verdict`, `score`, `issues`, `warnings`

Invocation rules:
- standalone: omit `runId` and `summaryArtifactPath`
- managed: pass both `runId` and exact `summaryArtifactPath`
- always write the validated summary before terminal outcome

## Definition of Done

- [ ] Story and Done implementation tasks loaded (test tasks excluded)
- [ ] Code metrics calculated (Cyclomatic Complexity, function/file sizes)
- [ ] MCP Ref validation completed (OPT-, BP-, PERF- categories)
- [ ] ARCH- subcategories checked (LB, TX, DTO, DI, CEH, SES, EVENT); MNT- subcategories checked (DC, DRY, GOD, SIG, ERR)
- [ ] Issues identified with prefixes and severity, sources from MCP Ref/Context7
- [ ] Code Quality Score calculated
- [ ] Output formatted per `references/output_schema.md`
- [ ] Linear comment posted with findings

## Reference Files
- Git scope detection: `shared/references/git_scope_detection.md`
- Code metrics: `references/code_metrics.md` (thresholds and penalties)
- Guides: `docs/guides/`
- Templates for context: `shared/templates/task_template_implementation.md`
- **Clean code checklist:** `shared/references/clean_code_checklist.md`
- Research tool fallback: `shared/references/research_tool_fallback.md`

---
**Version:** 5.1.0
**Last Updated:** 2026-03-15
