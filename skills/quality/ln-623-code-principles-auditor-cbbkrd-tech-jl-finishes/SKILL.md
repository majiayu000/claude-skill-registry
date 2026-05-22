---
name: ln-623-code-principles-auditor
description: "Code principles audit worker (L3). Checks DRY (10 types), KISS/YAGNI, error handling, DI patterns. Returns findings with severity, location, effort, pattern_signature."
allowed-tools: Read, Grep, Glob, Bash
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Code Principles Auditor (L3 Worker)

Specialized worker auditing code principles (DRY, KISS, YAGNI) and design patterns.

## Purpose & Scope

- **Worker in ln-620 coordinator pipeline** - invoked by ln-620-codebase-auditor
- Audit **code principles** (DRY/KISS/YAGNI, error handling, DI)
- Return structured findings with severity, location, effort, pattern_signature, recommendations
- Calculate compliance score (X/10) for Code Principles category

## Inputs (from Coordinator)

**MANDATORY READ:** Load `shared/references/task_delegation_pattern.md#audit-coordinator--worker-contract` for contextStore structure.

Receives `contextStore` with: `tech_stack`, `best_practices`, `principles`, `codebase_root`, `output_dir`.

**Domain-aware:** Supports `domain_mode` + `current_domain` (see `audit_output_schema.md#domain-aware-worker-output`).

## Workflow

1) **Parse context** — extract fields, determine `scan_path` (domain-aware if specified), extract `output_dir`
2) **Load detection patterns**
   - **MANDATORY READ:** Load `references/detection_patterns.md` for language-specific Grep/Glob patterns
   - Select patterns matching project's `tech_stack`
3) **Scan codebase for violations**
   - All Grep/Glob patterns use `scan_path` (not codebase_root)
   - Follow step-by-step detection from `detection_patterns.md`
   - Apply exclusions from `detection_patterns.md#exclusions`
4) **Generate recommendations**
   - **MANDATORY READ:** Load `references/refactoring_decision_tree.md` for pattern selection
   - Match each finding to appropriate refactoring pattern via decision tree
5) **Collect findings with severity, location, effort, pattern_id, pattern_signature, recommendation**
   - Tag each finding with `domain: domain_name` (if domain-aware)
   - Assign `pattern_signature` for cross-domain matching by ln-620
6) **Calculate score using penalty algorithm**
7) **Write Report:** Build full markdown report in memory per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/623-principles-{domain}.md` (or `623-principles.md` in global mode) in single Write call. **Include `<!-- FINDINGS-EXTENDED -->` JSON block** with pattern_signature fields for cross-domain DRY analysis
8) **Return Summary:** Return minimal summary to coordinator (see Output Format)

## Audit Rules

### 1. DRY Violations (Don't Repeat Yourself)

**MANDATORY READ:** Load `references/detection_patterns.md` for detection steps per type.

| Type | What | Severity | Default Recommendation | Effort |
|------|------|----------|----------------------|--------|
| **1.1** Identical Code | Same functions/constants/blocks (>10 lines) in multiple files | HIGH: business-critical (auth, payment). MEDIUM: utilities. LOW: simple constants <5x | Extract function → decide location by duplication scope | M |
| **1.2** Duplicated Validation | Same validation patterns (email, password, phone, URL) across files | HIGH: auth/payment. MEDIUM: user input 3+x. LOW: format checks <3x | Extract to shared validators module | M |
| **1.3** Repeated Error Messages | Hardcoded error strings instead of centralized catalog | MEDIUM: critical messages hardcoded or no error catalog. LOW: <3 places | Create constants/error-messages file | M |
| **1.4** Similar Patterns | Functions with same call sequence/control flow but different names/entities | MEDIUM: business logic in critical paths. LOW: utilities <3x | Extract common logic (see decision tree for pattern) | M |
| **1.5** Duplicated SQL/ORM | Same queries in different services | HIGH: payment/auth queries. MEDIUM: common 3+x. LOW: simple <3x | Extract to Repository layer | M |
| **1.6** Copy-Pasted Tests | Identical setup/teardown/fixtures across test files | MEDIUM: setup in 5+ files. LOW: <5 files | Extract to test helpers | M |
| **1.7** Repeated API Responses | Same response object shapes without DTOs | MEDIUM: in 5+ endpoints. LOW: <5 endpoints | Create DTO/Response classes | M |
| **1.8** Duplicated Middleware Chains | Identical middleware/decorator stacks on multiple routes | MEDIUM: same chain on 5+ routes. LOW: <5 routes | Create named middleware group, apply at router level | M |
| **1.9** Duplicated Type Definitions | Interfaces/structs/types with 80%+ same fields | MEDIUM: in 5+ files. LOW: 2-4 files | Create shared base type, extend where needed | M |
| **1.10** Duplicated Mapping Logic | Same entity→DTO / DTO→entity transformations in multiple locations | MEDIUM: in 3+ locations. LOW: 2 locations | Create dedicated Mapper class/function | M |

**Recommendation selection:** Use `references/refactoring_decision_tree.md` to choose the right refactoring pattern based on duplication location (Level 1) and logic type (Level 2).

### 2. KISS Violations (Keep It Simple, Stupid)

| Violation | Detection | Severity | Recommendation | Effort |
|-----------|-----------|----------|---------------|--------|
| Abstract class with 1 implementation | Grep `abstract class` → count subclasses | HIGH: prevents understanding core logic | Remove abstraction, inline | L |
| Factory for <3 types | Grep factory patterns → count branches | MEDIUM: unnecessary pattern | Replace with direct construction | M |
| Deep inheritance >3 levels | Trace extends chain | HIGH: fragile hierarchy | Flatten with composition | L |
| Excessive generic constraints | Grep `<T extends ... & ...>` | LOW: acceptable tradeoff | Simplify constraints | M |
| Wrapper-only classes | Read: all methods delegate to inner | MEDIUM: unnecessary indirection | Remove wrapper, use inner directly | M |

### 3. YAGNI Violations (You Aren't Gonna Need It)

| Violation | Detection | Severity | Recommendation | Effort |
|-----------|-----------|----------|---------------|--------|
| Dead feature flags (always true/false) | Grep flags → verify never toggled | LOW: cleanup needed | Remove flag, keep active code path | M |
| Abstract methods never overridden | Grep abstract → search implementations | MEDIUM: unused extensibility | Remove abstract, make concrete | M |
| Unused config options | Grep config key → 0 references | LOW: dead config | Remove option | S |
| Interface with 1 implementation | Grep interface → count implementors | MEDIUM: premature abstraction | Remove interface, use class directly | M |
| Premature generics (used with 1 type) | Grep generic usage → count type params | LOW: over-engineering | Replace generic with concrete type | S |

### 4. Missing Error Handling

- Find async functions without try-catch
- Check API routes without error middleware
- Verify database calls have error handling

| Severity | Criteria |
|----------|----------|
| **CRITICAL** | Payment/auth without error handling |
| **HIGH** | User-facing operations without error handling |
| **MEDIUM** | Internal operations without error handling |

**Effort:** M

### 5. Centralized Error Handling

- Search for centralized error handler: `ErrorHandler`, `errorHandler`, `error-handler.*`
- Check if middleware delegates to handler
- Verify async routes use promises/async-await
- **Anti-pattern:** `process.on("uncaughtException")` usage

| Severity | Criteria |
|----------|----------|
| **HIGH** | No centralized error handler |
| **HIGH** | Using `uncaughtException` listener (Express anti-pattern) |
| **MEDIUM** | Middleware handles errors directly (no delegation) |
| **MEDIUM** | Async routes without proper error handling |
| **LOW** | Stack traces exposed in production |

**Recommendation:** Create single ErrorHandler class. Middleware catches and forwards. Use async/await. DO NOT use uncaughtException listeners.

**Effort:** M-L

### 6. Dependency Injection / Centralized Init

- Check for DI container: `inversify`, `awilix`, `tsyringe` (Node), `dependency_injector` (Python), Spring `@Autowired` (Java), ASP.NET `IServiceCollection` (C#)
- Grep for `new SomeService()` in business logic (direct instantiation)
- Check for bootstrap module: `bootstrap.ts`, `init.py`, `Startup.cs`, `app.module.ts`

| Severity | Criteria |
|----------|----------|
| **MEDIUM** | No DI container (tight coupling) |
| **MEDIUM** | Direct instantiation in business logic |
| **LOW** | Mixed DI and direct imports |

**Recommendation:** Use DI container. Centralize init in bootstrap module. Inject via constructor.

**Effort:** L

### 7. Missing Best Practices Guide

- Check for: `docs/architecture.md`, `docs/best-practices.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`

| Severity | Criteria |
|----------|----------|
| **LOW** | No architecture/best practices guide |

**Recommendation:** Create `docs/architecture.md` with layering rules, error handling patterns, DI usage, coding conventions.

**Effort:** S

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_scoring.md` for unified scoring formula.

## Output Format

**MANDATORY READ:** Load `shared/templates/audit_worker_report_template.md` for file format.

Write report to `{output_dir}/623-principles-{domain}.md` (or `623-principles.md` in global mode) with `category: "Architecture & Design"`.

**FINDINGS-EXTENDED block (required for this worker):** After the Findings table, include a `<!-- FINDINGS-EXTENDED -->` JSON block containing all DRY findings with `pattern_signature` for cross-domain matching by ln-620 coordinator. See template for format.

**pattern_id:** DRY type identifier (`dry_1.1` through `dry_1.10`). Omit for non-DRY findings.

**pattern_signature:** Normalized key for the detected pattern (e.g., `validation_email`, `sql_users_findByEmail`, `middleware_auth_validate_ratelimit`). Same signature in multiple domains triggers cross-domain DRY finding. See `detection_patterns.md` for format per DRY type.

Return summary to coordinator:
```
Report written: docs/project/.audit/623-principles-users.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Critical Rules

- **Do not auto-fix:** Report only
- **Domain-aware scanning:** If `domain_mode="domain-aware"`, scan ONLY `scan_path`
- **Tag findings:** Include `domain` field in each finding when domain-aware
- **Pattern signatures:** Include `pattern_id` + `pattern_signature` for every DRY finding
- **Context-aware:** Use project's `principles.md` to define what's acceptable
- **Effort realism:** S = <1h, M = 1-4h, L = >4h
- **Exclusions:** Skip generated code, vendor, migrations (see `detection_patterns.md#exclusions`)

## Definition of Done

- contextStore parsed (including domain_mode, current_domain, output_dir)
- scan_path determined (domain path or codebase root)
- Detection patterns loaded from `references/detection_patterns.md`
- All 7 checks completed (scoped to scan_path):
  - DRY (10 subcategories: 1.1-1.10), KISS, YAGNI, Error Handling, Centralized Errors, DI/Init, Best Practices Guide
- Recommendations selected via `references/refactoring_decision_tree.md`
- Findings collected with severity, location, effort, pattern_id, pattern_signature, recommendation, domain
- Score calculated per `shared/references/audit_scoring.md`
- Report written to `{output_dir}/623-principles-{domain}.md` with FINDINGS-EXTENDED block (atomic single Write call)
- Summary returned to coordinator

## Reference Files

- **Worker report template:** `shared/templates/audit_worker_report_template.md`
- **Detection patterns:** [references/detection_patterns.md](references/detection_patterns.md)
- **Refactoring decision tree:** [references/refactoring_decision_tree.md](references/refactoring_decision_tree.md)
- **Audit scoring formula:** `shared/references/audit_scoring.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`

---
**Version:** 5.0.0
**Last Updated:** 2026-02-08
