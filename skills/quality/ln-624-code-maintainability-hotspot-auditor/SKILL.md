---
name: ln-624-code-maintainability-hotspot-auditor
description: "Checks local maintainability hotspots: complexity, long methods, god modules, signatures, algorithms, and constants. Also flags identifier drift across API/DTO/DB layers. Use when auditing code hotspots."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__audit_workspace, mcp__hex-graph__analyze_architecture, mcp__hex-line__read_file, mcp__hex-line__grep_search, mcp__hex-line__outline
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

# Code Maintainability Hotspot Auditor (L3 Worker)

**Type:** L3 Worker

Specialized worker auditing local code hotspots that are hard to read, change, or reason about.

## Purpose & Scope

- Audit **code maintainability hotspots** (priority: medium)
- Check complexity metrics, method signature quality, local algorithmic efficiency, constants management, identifier consistency across layers
- Emit `REFACTOR_HOTSPOT`, `SIMPLIFY_SIGNATURE`, `EXTRACT_CONSTANT`, or `UNIFY_IDENTIFIER`
- Return structured findings with severity, location, effort, recommendations
- Calculate compliance score (X/10) for Code Quality category

## Inputs

**MANDATORY READ:** Load `references/audit_worker_core_contract.md`.
Tool policy: follow host AGENTS.md MCP preferences; load `references/mcp_tool_preferences.md` and `references/mcp_integration_patterns.md` only when host policy is absent or MCP behavior is unclear.

Receives `contextStore` with: `tech_stack`, `best_practices`, `principles`, `codebase_root`, `output_dir`.

**Domain-aware:** Supports `domain_mode` + `current_domain` (see `audit_output_schema.md#domain-aware-worker-output`).

## Workflow

Detection policy: use two-layer detection (candidate scan, then context verification); load `references/two_layer_detection.md` only when the verification method is ambiguous.

1) **Parse context** -- extract fields, determine `scan_path` (domain-aware if specified), extract `output_dir`
2) **Scan codebase for violations (Layer 1)**
   - All Grep/Glob patterns use `scan_path` (not codebase_root)
   - **Graph acceleration (if available):** IF `contextStore.graph_indexed` OR `.hex-skills/codegraph/index.db` exists:
     - **Complexity + God classes:** `audit_workspace(path=scan_path, verbosity="minimal", limit=5)` -- use returned hotspots to pre-identify complex functions and god classes. Raise `limit` only for deliberate drill-down.
     - **Module metrics:** `analyze_architecture(path=scan_path, verbosity="full")` -- use returned coupling metrics for cascade depth and coupling analysis.
     - Fall back to grep patterns below if graph unavailable.
     - **Outline-first read:** `outline(file_path)` before reading large source files -- understand function/class structure for complexity analysis.
   - Example: `Grep(pattern="if.*if.*if", path=scan_path)` for nesting detection
3) **Analyze context per candidate (Layer 2 -- MANDATORY)**
   Layer 1 finding without Layer 2 = NOT a valid finding. Before reporting, ask: "Is this violation intentional or justified by design?"
   - Cyclomatic complexity: is complexity from switch/case on enum (valid) or deeply nested conditions (bad)? Enum dispatch -> downgrade to LOW or skip
   - O(n^2): read context -- what's n? If bounded (n < 100), downgrade severity
   - God class: is it a config/schema/builder class? -> downgrade
   - Identifier drift: is the rename mediated by an explicit serializer alias (`@JsonProperty`, `alias_generator`, `@SerializedName`) or an ORM column mapping (`@Column(name=...)`)? If yes -> downgrade or skip
4) **Collect findings with severity, location, effort, recommendation**
   - Tag each finding with `domain: domain_name` (if domain-aware)
5) **Calculate score using penalty algorithm**
6) **Write Report:** Build full markdown report in memory per `references/templates/audit_worker_report_template.md`, write to `{output_dir}/ln-624--{domain}.md` (or `624-quality.md` in global mode) in single Write call
7) **Return Summary:** Return minimal summary (see Output Format)

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

### 7. Constants Management
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

### 8. Method Signature Quality
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

### 9. Identifier Consistency Across Layers
**What:** Same concept uses different identifiers across API contracts, DTOs, services, repositories, DB columns, or internal modules

**Detection:**

| Issue | Pattern | Example |
|-------|---------|---------|
| External contract drift | API/OpenAPI/external-schema field name differs from DTO/service/repo/DB column | `user_id` in OpenAPI but `uid` in DTO, `userId` in service, `user` column in DB |
| Synonym drift (internal) | Same entity referenced by competing names across modules | `customer` vs `client` vs `account` vs `user` for one concept |
| Unmediated casing/translation | snake/camel/kebab swap without an explicit serializer alias | `created_at` API field assigned to `creationTime` with no alias declared |
| Abbreviation drift | Full and abbreviated forms coexist for one concept | `organization` vs `org` vs `orgId` vs `organizationId` |

**Severity:**
- **HIGH:** External-contract field renamed inside code without an explicit serializer alias -- silent breakage risk when the upstream contract changes
- **MEDIUM:** Synonym drift for one entity across 3+ modules (`customer` / `client` / `account`)
- **MEDIUM:** Casing translation without an explicit alias mapping
- **LOW:** Two-variant drift in one bounded module; abbreviation drift in internal-only code
- **Downgrade when:** ORM-mediated mapping with explicit column alias, framework-required transforms (e.g. GraphQL camelCase via codegen), generated DTOs from contract, language-keyword collision forcing rename -> downgrade or skip

**Layer 2 requirement:** Synonym drift detection relies on a curated project glossary or on reading usage context. Grep alone is insufficient -- always confirm the two identifiers refer to the same concept before reporting.

**Recommendation:**
- **External-contract case:** carry the external API name as-is through DTO / service / repository / DB column. If casing or language conventions conflict, configure a serializer alias once at the boundary (`@JsonProperty`, `alias_generator`, `@SerializedName`) rather than renaming the field inside the code
- **Internal-only case:** pick the most semantically precise variant, apply find/replace across the modules, record the canonical term in a shared glossary or shared constants/enum module. Add a lint rule or codegen step where possible to prevent reintroduction
- For verb naming within a single module, see Rule #8 (Method Signature Quality)

**Effort:** S-M (rename + serializer config). L when a DB column rename plus migration is required

## Scoring Algorithm

**MANDATORY READ:** Load `references/audit_scoring.md`.

## Output Format

**MANDATORY READ:** Load `references/templates/audit_worker_report_template.md`.

Write JSON summary per `references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/ln-624--{domain}.md` (or `624-quality.md` in global mode) with `category: "Code Maintainability Hotspots"` and checks: cyclomatic_complexity, deep_nesting, long_methods, god_classes, too_many_params, quadratic_algorithms, magic_numbers, method_signatures, identifier_consistency.

When `summaryArtifactPath` is absent, write the standalone runtime summary under `.hex-skills/runtime-artifacts/runs/{run_id}/evaluation-worker/{worker}--{identifier}.json` and optionally echo the same summary in structured output.
```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/ln-624--orders.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Critical Rules

Apply the already-loaded `references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report only
- **Domain-aware scanning:** If `domain_mode="domain-aware"`, scan ONLY `scan_path` (not entire codebase)
- **Tag findings:** Include `domain` field in each finding when domain-aware
- **Metrics tools:** Use existing tools when available (ESLint complexity plugin, radon, gocyclo)
- **Unique angle:** Audit local maintainability hotspots only. Do not audit duplication, package health, architecture boundaries, N+1 persistence behavior, or orchestration ownership. Identifier-consistency findings cover naming continuity of one concept across layers; this is distinct from ln-623 (code duplication) and ln-643 (DTO presence / layer leakage in signatures).
- **Action required:** Every finding uses `REFACTOR_HOTSPOT`, `SIMPLIFY_SIGNATURE`, `EXTRACT_CONSTANT`, or `UNIFY_IDENTIFIER`.

## Definition of Done

Apply the already-loaded `references/audit_worker_core_contract.md`.

- [ ] contextStore parsed (including domain_mode, current_domain, output_dir)
- [ ] scan_path determined (domain path or codebase root)
- [ ] All 9 checks completed (scoped to scan_path):
  - complexity, nesting, length, god classes, parameters, O(n^2), constants, method signatures, identifier consistency
- [ ] Findings collected with severity, location, effort, recommendation, domain
- [ ] Score calculated
- [ ] Report written to `{output_dir}/ln-624--{domain}.md` (atomic single Write call)
- [ ] Summary written per contract

## Reference Files

- **Audit output schema:** `references/audit_output_schema.md`

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
