---
name: ln-624-code-quality-auditor
description: "Checks cyclomatic complexity, nesting, long methods, god classes, O(n2), N+1 queries, constants management. Use when auditing code quality."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__audit_workspace, mcp__hex-graph__analyze_architecture, mcp__hex-line__outline
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Code Quality Auditor (L3 Worker)

**Type:** L3 Worker

Specialized worker auditing code complexity, method signatures, algorithms, and constants management.

## Purpose & Scope

- Audit **code quality** (Categories 5+6+NEW: Medium Priority)
- Check complexity metrics, method signature quality, algorithmic efficiency, constants management
- Return structured findings with severity, location, effort, recommendations
- Calculate compliance score (X/10) for Code Quality category

## Inputs

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

Receives `contextStore` with: `tech_stack`, `best_practices`, `principles`, `codebase_root`, `output_dir`.

**Domain-aware:** Supports `domain_mode` + `current_domain` (see `audit_output_schema.md#domain-aware-worker-output`).

## Workflow

**MANDATORY READ:** Load `shared/references/two_layer_detection.md` for detection methodology.

1) **Parse context** -- extract fields, determine `scan_path` (domain-aware if specified), extract `output_dir`
2) **Scan codebase for violations (Layer 1)**
   - All Grep/Glob patterns use `scan_path` (not codebase_root)
   - **Graph acceleration (if available):** IF `contextStore.graph_indexed` OR `.hex-skills/codegraph/index.db` exists:
     - **Complexity + God classes:** `audit_workspace(path=scan_path, verbosity="full")` -- use returned hotspots to pre-identify complex functions and god classes.
     - **Module metrics:** `analyze_architecture(path=scan_path, verbosity="full")` -- use returned coupling metrics for cascade depth and coupling analysis.
     - Fall back to grep patterns below if graph unavailable.
     - **Outline-first read:** `outline(path)` before reading large source files -- understand function/class structure for complexity analysis.
   - Example: `Grep(pattern="if.*if.*if", path=scan_path)` for nesting detection
3) **Analyze context per candidate (Layer 2 -- MANDATORY)**
   Layer 1 finding without Layer 2 = NOT a valid finding. Before reporting, ask: "Is this violation intentional or justified by design?"
   - Cyclomatic complexity: is complexity from switch/case on enum (valid) or deeply nested conditions (bad)? Enum dispatch -> downgrade to LOW or skip
   - O(n^2): read context -- what's n? If bounded (n < 100), downgrade severity
   - N+1: read ORM config -- does it have eager loading configured elsewhere? Admin-only endpoint -> downgrade severity
   - God class: is it a config/schema/builder class? -> downgrade
   - Cascade depth: already traces calls (implicit Layer 2). Orchestrator function -> SEB does NOT apply (see Conflict Resolution in ARCH-AI-SEB)
4) **Collect findings with severity, location, effort, recommendation**
   - Tag each finding with `domain: domain_name` (if domain-aware)
5) **Calculate score using penalty algorithm**
6) **Write Report:** Build full markdown report in memory per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/ln-624--{domain}.md` (or `624-quality.md` in global mode) in single Write call
7) **Return Summary:** Return minimal summary to coordinator (see Output Format)

## Audit Rules (Priority: MEDIUM)

### 1. Cyclomatic Complexity
**What:** Too many decision points in single function (> 10)

**Detection:**
- Count if/else, switch/case, ternary, &&, ||, for, while
- Use tools: `eslint-plugin-complexity`, `radon` (Python), `gocyclo` (Go)

**Severity:**
- **HIGH:** Complexity > 20 (extremely hard to test)
- **MEDIUM:** Complexity 11-20 (refactor recommended)
- **LOW:** Complexity 8-10 (acceptable but monitor)
- **Downgrade when:** Enum/switch dispatch, state machines, parser grammars -> downgrade to LOW or skip

**Recommendation:** Split function, extract helper methods, use early returns

**Effort:** M-L (depends on complexity)

### 2. Deep Nesting (> 4 levels)
**What:** Nested if/for/while blocks too deep

**Detection:**
- Count indentation levels
- Pattern: if { if { if { if { if { ... } } } } }

**Severity:**
- **HIGH:** > 6 levels (unreadable)
- **MEDIUM:** 5-6 levels
- **LOW:** 4 levels
- **Downgrade when:** Nesting from early-return guard clauses (structurally deep but linear logic) -> downgrade

**Recommendation:** Extract functions, use guard clauses, invert conditions

**Effort:** M (refactor structure)

### 3. Long Methods (> 50 lines)
**What:** Functions too long, doing too much

**Detection:**
- Count lines between function start and end
- Exclude comments, blank lines

**Severity:**
- **HIGH:** > 100 lines
- **MEDIUM:** 51-100 lines
- **LOW:** 40-50 lines (borderline)
- **Downgrade when:** Orchestrator functions with sequential delegation; data transformation pipelines -> downgrade

**Recommendation:** Split into smaller functions, apply Single Responsibility

**Effort:** M (extract logic)

### 4. God Classes/Modules (> 500 lines)
**What:** Files with too many responsibilities

**Detection:**
- Count lines in file (exclude comments)
- Check number of public methods/functions

**Severity:**
- **HIGH:** > 1000 lines
- **MEDIUM:** 501-1000 lines
- **LOW:** 400-500 lines
- **Downgrade when:** Config/schema/migration files, generated code, barrel/index files -> skip

**Recommendation:** Split into multiple files, apply separation of concerns

**Effort:** L (major refactor)

### 5. Too Many Parameters (> 5)
**What:** Functions with excessive parameters

**Detection:**
- Count function parameters
- Check constructors, methods

**Severity:**
- **MEDIUM:** 6-8 parameters
- **LOW:** 5 parameters (borderline)
- **Downgrade when:** Builder/options pattern constructor; framework-required signatures (middleware, hooks) -> skip

**Recommendation:** Use parameter object, builder pattern, default parameters

**Effort:** S-M (refactor signature + calls)

### 6. O(n^2) or Worse Algorithms
**What:** Inefficient nested loops over collections

**Detection:**
- Nested for loops: `for (i) { for (j) { ... } }`
- Nested array methods: `arr.map(x => arr.filter(...))`

**Severity:**
- **HIGH:** O(n^2) in hot path (API request handler)
- **MEDIUM:** O(n^2) in occasional operations
- **LOW:** O(n^2) on small datasets (n < 100)
- **Downgrade when:** Bounded n (n < 100 guaranteed by domain); one-time init/migration code -> downgrade to LOW or skip

**Recommendation:** Use hash maps, optimize with single pass, use better data structures

**Effort:** M (algorithm redesign)

### 7. N+1 Query Patterns
**What:** ORM lazy loading causing N+1 queries

**Detection:**
- Find loops with database queries inside
- Check ORM patterns: `users.forEach(u => u.getPosts())`

**Severity:**
- **CRITICAL:** N+1 in API endpoint (performance disaster)
- **HIGH:** N+1 in frequent operations
- **MEDIUM:** N+1 in admin panel
- **Downgrade when:** Admin-only endpoint called <=1x/day -> downgrade to LOW. Eager loading configured elsewhere in ORM -> skip

**Recommendation:** Use eager loading, batch queries, JOIN

**Effort:** M (change ORM query)

### 8. Constants Management (NEW)
**What:** Magic numbers/strings, decentralized constants, duplicates

**Detection:**

| Issue | Pattern | Example |
|-------|---------|---------|
| Magic numbers | Hardcoded numbers in conditions/calculations | `if (status === 2)` |
| Magic strings | Hardcoded strings in comparisons | `if (role === 'admin')` |
| Decentralized | Constants scattered across files | `MAX_SIZE = 100` in 5 files |
| Duplicates | Same value multiple times | `STATUS_ACTIVE = 1` in 3 places |
| No central file | Missing `constants.ts` or `config.py` | No single source of truth |

**Severity:**
- **HIGH:** Magic numbers in business logic (payment amounts, statuses)
- **MEDIUM:** Duplicate constants (same value defined 3+ times)
- **MEDIUM:** No central constants file
- **LOW:** Magic strings in logging/debugging
- **Downgrade when:** HTTP status codes (200, 404, 500) -> skip. Math constants (0, 1, -1) in algorithms -> skip. Test data -> skip

**Recommendation:**
- Create central constants file (`constants.ts`, `config.py`, `constants.go`)
- Extract magic numbers to named constants: `const STATUS_ACTIVE = 1`
- Consolidate duplicates, import from central file
- Use enums for related constants

**Effort:** M (extract constants, update imports, consolidate)

### 9. Method Signature Quality
**What:** Poor method contracts reducing readability and maintainability

**Detection:**

| Issue | Pattern | Example |
|-------|---------|---------|
| Boolean flag params | >=2 boolean params in signature | `def process(data, is_async: bool, skip_validation: bool)` |
| Too many optional params | >=3 optional params with defaults | `def query(db, limit=10, offset=0, sort="id", order="asc")` |
| Inconsistent verb naming | Different verbs for same operation type in one module | `get_user()` vs `fetch_account()` vs `load_profile()` |
| Unclear return type | `-> dict`, `-> Any`, `-> tuple` without TypedDict/NamedTuple | `def get_stats() -> dict` instead of `-> StatsResponse` |

**Severity:**
- **MEDIUM:** Boolean flag params (use enum/strategy), unclear return types
- **LOW:** Too many optional params, inconsistent naming

**Recommendation:**
- Boolean flags: replace with enum, strategy pattern, or separate methods
- Optional params: group into config/options dataclass
- Naming: standardize verb conventions per module (`get_` for sync, `fetch_` for async, etc.)
- Return types: use TypedDict, NamedTuple, or dataclass instead of raw dict/tuple

**Effort:** S-M (refactor signatures + callers)

### 10. Side-Effect Cascade Depth

**What:** Functions triggering cascading chains of external side-effects (DB writes -> notifications -> metrics -> limits).

**Detection:**
**MANDATORY READ:** `shared/references/ai_ready_architecture.md` for side-effect markers, false positive exclusions, and opaque sink rules.
- Glob `**/services/**/*.{py,ts,js,cs,java}` to find service files
- For each public function: check body for side-effect markers (per reference)
- Recursively follow called internal functions for additional markers
- Calculate max chain depth from entry point

**Severity:**
- **HIGH:** cascade_depth >= 4
- **MEDIUM:** cascade_depth = 3
- OK: depth <= 2
- **Downgrade when:** Orchestrator/coordinator functions (imports 3+ services AND delegates sequentially) -> skip. Depth from opaque sinks (logging, metrics) -> skip

**Conflict Resolution:** IF function is an orchestrator/coordinator (imports 3+ services AND delegates to them sequentially) -> ARCH-AI-SEB does NOT apply. Orchestrators are EXPECTED to have multiple side-effect categories. Only flag SEB for leaf functions.

**Recommendation:** Refactor to flat orchestration -- extract side-effects into independent sink functions. See reference.

**Effort:** M-L

**Output:** Also generate summary Pipe/Sink table per module:

| Module | Sinks (0-1) | Shallow Pipes (2) | Deep Pipes (3+) | Sink Ratio |
|--------|-------------|-------------------|-----------------|------------|

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/references/audit_scoring.md`.

## Output Format

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/templates/audit_worker_report_template.md`.

Write JSON summary per `shared/references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/ln-624--{domain}.md` (or `624-quality.md` in global mode) with `category: "Code Quality"` and checks: cyclomatic_complexity, deep_nesting, long_methods, god_classes, too_many_params, quadratic_algorithms, n_plus_one, magic_numbers, method_signatures, cascade_depth.

Return summary per `shared/references/audit_summary_contract.md`.

When `summaryArtifactPath` is absent, write the standalone runtime summary under `.hex-skills/runtime-artifacts/runs/{run_id}/audit-worker/{worker}--{identifier}.json` and optionally echo the same summary in structured output.
```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/ln-624--orders.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Critical Rules

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report only
- **Domain-aware scanning:** If `domain_mode="domain-aware"`, scan ONLY `scan_path` (not entire codebase)
- **Tag findings:** Include `domain` field in each finding when domain-aware
- **Context-aware:** Small functions (n < 100) with O(n^2) may be acceptable
- **Constants detection:** Exclude test files, configs, examples
- **Metrics tools:** Use existing tools when available (ESLint complexity plugin, radon, gocyclo)

## Definition of Done

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- [ ] contextStore parsed (including domain_mode, current_domain, output_dir)
- [ ] scan_path determined (domain path or codebase root)
- [ ] All 10 checks completed (scoped to scan_path):
  - complexity, nesting, length, god classes, parameters, O(n^2), N+1, constants, method signatures, cascade depth
- [ ] Findings collected with severity, location, effort, recommendation, domain
- [ ] Score calculated
- [ ] Report written to `{output_dir}/ln-624--{domain}.md` (atomic single Write call)
- [ ] Summary written per contract

## Reference Files

- **Audit output schema:** `shared/references/audit_output_schema.md`

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
