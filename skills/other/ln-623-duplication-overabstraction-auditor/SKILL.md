---
name: ln-623-duplication-overabstraction-auditor
description: "Checks evidence-backed duplication, over-abstraction, and unused extensibility. Use when auditing DRY/KISS/YAGNI risk."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__audit_workspace, mcp__hex-graph__find_implementations, mcp__hex-line__read_file, mcp__hex-line__grep_search, mcp__hex-line__outline
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

# Duplication & Over-Abstraction Auditor (L3 Worker)

**Type:** L3 Worker

Specialized worker auditing duplication, over-abstraction, and unused extensibility.

## Purpose & Scope

- Audit **duplication and over-abstraction** (DRY/KISS/YAGNI)
- Return structured findings with severity, location, effort, pattern_signature, recommendations
- Emit `MERGE_DUPLICATION`, `REMOVE_ABSTRACTION`, or `REMOVE_YAGNI`
- Calculate compliance score (X/10) for Duplication & Over-Abstraction category

## Inputs

**MANDATORY READ:** Load `references/audit_worker_core_contract.md`.
Tool policy: follow host AGENTS.md MCP preferences; load `references/mcp_tool_preferences.md` and `references/mcp_integration_patterns.md` only when host policy is absent or MCP behavior is unclear.

Receives `contextStore` with: `tech_stack`, `best_practices`, `principles`, `codebase_root`, `output_dir`.

**Domain-aware:** Supports `domain_mode` + `current_domain` (see `audit_output_schema.md#domain-aware-worker-output`).

Use `hex-graph` first when clone groups, implementations, or semantic relationships materially improve the audit. Use `hex-line` first for local code reads when available. If MCP is unavailable, unsupported, or not indexed, continue with built-in `Read/Grep/Glob/Bash` and state the fallback in the report.

## Workflow

Detection policy: use two-layer detection (candidate scan, then context verification); load `references/two_layer_detection.md` only when the verification method is ambiguous.

1) **Parse context** -- extract fields, determine `scan_path` (domain-aware if specified), extract `output_dir`
2) **Load detection patterns**
   - **MANDATORY READ:** Load `references/detection_patterns.md` for language-specific Grep/Glob patterns
   - Select patterns matching project's `tech_stack`
3) **Scan codebase for violations (Layer 1)**
   - All Grep/Glob patterns use `scan_path` (not codebase_root)
   - **Graph acceleration (if available):** IF `contextStore.graph_indexed` OR `.hex-skills/codegraph/index.db` exists:
     - **DRY (1.1-1.10):** `audit_workspace(path=scan_path, verbosity="minimal", limit=5, clone_member_limit=3)` -- each returned clone group = DRY candidate. Raise limits only for deliberate drill-down. Use clone kind and hotspot context for severity triage. Fall back to grep patterns if unavailable.
     - **KISS inheritance:** `find_implementations(symbol)` for abstract classes -- count implementations (1 = KISS candidate). Trace inheritance depth via graph.
     - **Complexity:** `audit_workspace(path=scan_path, verbosity="minimal", limit=5)` -- use returned hotspots to pre-identify complex functions for KISS/quality analysis. Raise `limit` only for deliberate drill-down.
     - **Outline-first read:** `outline(file_path)` before reading large source files -- understand structure before analyzing principles.
   - Follow step-by-step detection from `detection_patterns.md`
   - Apply exclusions from `detection_patterns.md#exclusions`
4) **Analyze context per candidate (Layer 2)**
   - DRY: read both code blocks to confirm true duplication (not just similar naming or shared interface)
   - KISS: check if abstraction serves DI pattern (valid single-impl interface) or is premature
   - YAGNI: check if feature flag was recently added (intentional) or dormant for months
5) **Generate recommendations**
   - **MANDATORY READ:** Load `references/refactoring_decision_tree.md` for pattern selection
   - Match each finding to appropriate refactoring pattern via decision tree
6) **Collect findings with severity, location, effort, pattern_id, pattern_signature, recommendation**
   - Tag each finding with `domain: domain_name` (if domain-aware)
   - Assign `pattern_signature` for managed aggregation
7) **Calculate score using penalty algorithm**
8) **Write Report:** Build full markdown report in memory per `references/templates/audit_worker_report_template.md`, write to `{output_dir}/ln-623--{domain}.md` (or `623-principles.md` in global mode) in single Write call. **Include `<!-- FINDINGS-EXTENDED -->` JSON block** with pattern_signature fields for cross-domain DRY analysis
9) **Return Summary:** Return minimal summary (see Output Format)

## Two-Layer Detection

Detection policy: use two-layer detection (candidate scan, then context verification); load `references/two_layer_detection.md` only when the verification method is ambiguous.

All findings require Layer 2 context analysis. Layer 1 finding without Layer 2 = NOT a valid finding. Before reporting, ask: "Is this violation intentional or justified by design?"

| Finding Type | Layer 2 Downgrade Examples |
|-------------|--------------------------|
| DRY | Modules with different lifecycle/ownership -> skip. Intentional duplication for decoupling -> skip |
| KISS | Framework-required abstraction (e.g., DI in Spring) -> downgrade. Single implementation today but interface for testing -> skip |
| YAGNI | Feature flag used in A/B testing -> skip. Config option used by ops team -> skip |

## Audit Rules

### 1. DRY Violations (Don't Repeat Yourself)

**MANDATORY READ:** Load `references/detection_patterns.md` for detection steps per type.

| Type | What | Severity | Exception (skip/downgrade) | Default Recommendation | Effort |
|------|------|----------|---------------------------|----------------------|--------|
| **1.1** Identical Code | Same functions/constants/blocks (>10 lines) in multiple files | HIGH: business-critical (auth, payment). MEDIUM: utilities. LOW: simple constants <5x | Different lifecycle/ownership modules -> skip. Intentional decoupling -> skip | Extract function -> decide location by duplication scope | M |
| **1.2** Duplicated Validation | Same validation patterns (email, password, phone, URL) across files | HIGH: auth/payment. MEDIUM: user input 3+x. LOW: format checks <3x | Different security contexts (auth vs public) -> skip | Extract to shared validators module | M |
| **1.3** Repeated Error Messages | Hardcoded error strings instead of centralized catalog | MEDIUM: critical messages hardcoded or no error catalog. LOW: <3 places | User-facing strings requiring per-context wording -> downgrade | Create constants/error-messages file | M |
| **1.4** Similar Patterns | Functions with same call sequence/control flow but different names/entities | MEDIUM: business logic in critical paths. LOW: utilities <3x | Modules with divergent evolution expected -> skip | Extract common logic (see decision tree for pattern) | M |
| **1.5** Duplicated SQL/ORM | Same queries in different services | HIGH: payment/auth queries. MEDIUM: common 3+x. LOW: simple <3x | Different bounded contexts; shared DB is worse than duplication -> skip | Extract to Repository layer | M |
| **1.6** Copy-Pasted Tests | Identical setup/teardown/fixtures across test files | MEDIUM: setup in 5+ files. LOW: <5 files | Tests intentionally isolated for clarity/independence -> downgrade | Extract to test helpers | M |
| **1.7** Repeated API Responses | Same response object shapes without DTOs | MEDIUM: in 5+ endpoints. LOW: <5 endpoints | Responses with different versioning lifecycle -> skip | Create DTO/Response classes | M |
| **1.8** Duplicated Middleware Chains | Identical middleware/decorator stacks on multiple routes | MEDIUM: same chain on 5+ routes. LOW: <5 routes | Routes with different auth/rate-limit requirements -> skip | Create named middleware group, apply at router level | M |
| **1.9** Duplicated Type Definitions | Interfaces/structs/types with 80%+ same fields | MEDIUM: in 5+ files. LOW: 2-4 files | Types with different ownership/evolution paths -> skip | Create shared base type, extend where needed | M |
| **1.10** Duplicated Mapping Logic | Same entity->DTO / DTO->entity transformations in multiple locations | MEDIUM: in 3+ locations. LOW: 2 locations | Mappings with different validation/enrichment rules -> skip | Create dedicated Mapper class/function | M |

**Recommendation selection:** Use `references/refactoring_decision_tree.md` to choose the right refactoring pattern based on duplication location (Level 1) and logic type (Level 2).

### 2. KISS Violations (Keep It Simple, Stupid)

| Violation | Detection | Severity | Exception (skip/downgrade) | Recommendation | Effort |
|-----------|-----------|----------|---------------------------|---------------|--------|
| Abstract class with 1 implementation | Grep `abstract class` -> count subclasses | HIGH: prevents understanding core logic | Interface for DI/testing -> skip. Framework-required (Spring, ASP.NET) -> skip | Remove abstraction, inline | L |
| Factory for <3 types | Grep factory patterns -> count branches | MEDIUM: unnecessary pattern | Factory used for DI/testing swap -> downgrade | Replace with direct construction | M |
| Deep inheritance >3 levels | Trace extends chain | HIGH: fragile hierarchy | Framework-mandated hierarchy (UI widgets, ORM models) -> downgrade | Flatten with composition | L |
| Excessive generic constraints | Grep `<T extends ... & ...>` | LOW: acceptable tradeoff | Type safety for public API boundary -> skip | Simplify constraints | M |
| Wrapper-only classes | Read: all methods delegate to inner | MEDIUM: unnecessary indirection | Adapter pattern for external API isolation -> skip | Remove wrapper, use inner directly | M |

### 3. YAGNI Violations (You Aren't Gonna Need It)

| Violation | Detection | Severity | Exception (skip/downgrade) | Recommendation | Effort |
|-----------|-----------|----------|---------------------------|---------------|--------|
| Dead feature flags (always true/false) | Grep flags -> verify never toggled | LOW: cleanup needed | A/B testing flags -> skip. Ops-controlled toggles -> skip | Remove flag, keep active code path | M |
| Abstract methods never overridden | Grep abstract -> search implementations | MEDIUM: unused extensibility | Plugin/extension point in public library -> downgrade | Remove abstract, make concrete | M |
| Unused config options | Grep config key -> 0 references | LOW: dead config | Env-specific configs (staging/prod) -> verify before flagging | Remove option | S |
| Interface with 1 implementation | Grep interface -> count implementors | MEDIUM: premature abstraction | Interface for DI/testing mock -> skip | Remove interface, use class directly | M |
| Premature generics (used with 1 type) | Grep generic usage -> count type params | LOW: over-engineering | Public library API designed for consumers -> skip | Replace generic with concrete type | S |

### 4. Evidence Gate

Do not report aesthetic preferences. A finding is valid only when the worker can show repeated code, an abstraction with no real variation point, or unused extensibility that adds maintenance cost.

| Issue | Required Evidence | Action |
|-------|-------------------|--------|
| Duplication | matching code blocks, repeated validation/query/mapping, or pattern_signature repeated across files | `MERGE_DUPLICATION` |
| Over-abstraction | abstraction layer with one real implementation and no framework/testing need | `REMOVE_ABSTRACTION` |
| YAGNI | feature flag, config option, generic, or extension point with no current use | `REMOVE_YAGNI` |

## Scoring Algorithm

**MANDATORY READ:** Load `references/audit_scoring.md`.

## Output Format

**MANDATORY READ:** Load `references/templates/audit_worker_report_template.md`.

Write JSON summary per `references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/ln-623--{domain}.md` (or `623-principles.md` in global mode) with `category: "Duplication & Over-Abstraction"`.

**FINDINGS-EXTENDED block (required for this worker):** After the Findings table, include a `<!-- FINDINGS-EXTENDED -->` JSON block containing all DRY findings with `pattern_signature` for managed aggregation. Follow `references/templates/audit_worker_report_template.md`.

**pattern_id:** DRY type identifier (`dry_1.1` through `dry_1.10`). Omit for non-DRY findings.

**pattern_signature:** Normalized key for the detected pattern (e.g., `validation_email`, `sql_users_findByEmail`, `middleware_auth_validate_ratelimit`). Same signature in multiple domains triggers cross-domain DRY finding. Format is defined in `references/detection_patterns.md`.

Return summary per `references/audit_summary_contract.md`.

When `summaryArtifactPath` is absent, write the standalone runtime summary under `.hex-skills/runtime-artifacts/runs/{run_id}/evaluation-worker/{worker}--{identifier}.json` and optionally echo the same summary in structured output.
```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/ln-623--users.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Critical Rules

Apply the already-loaded `references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report only
- **Domain-aware scanning:** If `domain_mode="domain-aware"`, scan ONLY `scan_path`
- **Tag findings:** Include `domain` field in each finding when domain-aware
- **Pattern signatures:** Include `pattern_id` + `pattern_signature` for every DRY finding
- **Context-aware:** Use project's `principles.md` to define what's acceptable
- **Effort realism:** S = <1h, M = 1-4h, L = >4h
- **Exclusions:** Skip generated code, vendor, migrations (see `detection_patterns.md#exclusions`)
- **Unique angle:** Audit only duplication, over-abstraction, and unused extensibility. Do not audit delivery gates, security, package health, local complexity metrics, architecture boundaries, or runtime lifecycle.
- **Action required:** Every finding uses `MERGE_DUPLICATION`, `REMOVE_ABSTRACTION`, or `REMOVE_YAGNI`.

## Definition of Done

Apply the already-loaded `references/audit_worker_core_contract.md`.

- [ ] contextStore parsed (including domain_mode, current_domain, output_dir)
- [ ] scan_path determined (domain path or codebase root)
- [ ] Detection patterns loaded from `references/detection_patterns.md`
- [ ] All 3 checks completed (scoped to scan_path):
  - DRY (10 subcategories: 1.1-1.10), KISS, YAGNI
- [ ] Recommendations selected via `references/refactoring_decision_tree.md`
- [ ] Findings collected with severity, location, effort, action, pattern_id, pattern_signature, recommendation, domain
- [ ] Score calculated per `references/audit_scoring.md`
- [ ] Report written to `{output_dir}/ln-623--{domain}.md` with FINDINGS-EXTENDED block (atomic single Write call)
- [ ] Summary written per contract

## Reference Files

- **Detection patterns:** [references/detection_patterns.md](references/detection_patterns.md)
- **Refactoring decision tree:** [references/refactoring_decision_tree.md](references/refactoring_decision_tree.md)

---
**Version:** 5.0.0
**Last Updated:** 2026-02-08
