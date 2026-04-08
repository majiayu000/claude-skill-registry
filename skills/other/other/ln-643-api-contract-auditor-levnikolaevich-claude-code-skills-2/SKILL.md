---
name: ln-643-api-contract-auditor
description: "Checks layer leakage in method signatures, missing DTOs, entity leakage to API, inconsistent error contracts. Use when auditing API contracts."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__find_references, mcp__hex-graph__find_symbols
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# API Contract Auditor (L3 Worker)

**Type:** L3 Worker

Specialized worker auditing API contracts, method signatures at service boundaries, and DTO usage patterns.

## Purpose & Scope

- Audit **API contracts** at architecture level (service boundaries, layer separation)
- Check layer leakage, DTO patterns, error contract consistency
- Return structured analysis with 4 scores (compliance, completeness, quality, implementation)

**Out of Scope** (owned by ln-623-code-principles-auditor):
- Code duplication (same DTO shape repeated, same mapping logic, same validation)
- Report only ARCHITECTURE BOUNDARY findings (wrong layer, missing contract)

## Inputs

```
- pattern: "API Contracts"     # Pattern name
- locations: string[]          # Service/API directories
- adr_reference: string        # Path to related ADR
- bestPractices: object        # Best practices from MCP Ref/Context7
- output_dir: string           # e.g., ".hex-skills/runtime-artifacts/runs/{run_id}/audit-report"

# Domain-aware (optional, from coordinator)
- domain_mode: "global" | "domain-aware"   # Default: "global"
- current_domain: string                   # e.g., "users", "billing" (only if domain-aware)
- scan_path: string                        # e.g., "src/users/" (only if domain-aware)
```

## Workflow

### Phase 0: Load References

**MANDATORY READ:** Load `shared/references/two_layer_detection.md` for detection methodology. Load `references/detection_patterns.md` -- language-specific Grep patterns for all 5 rules.

### Phase 1: Discover Service Boundaries

```
scan_root = scan_path IF domain_mode == "domain-aware" ELSE codebase_root

1. Find API layer: Glob("**/api/**/*.py", "**/routes/**/*.ts", "**/controllers/**/*.ts", root=scan_root)
2. Find service layer: Glob("**/services/**/*.py", "**/services/**/*.ts", root=scan_root)
3. Find domain layer: Glob("**/domain/**/*.py", "**/models/**/*.py", root=scan_root)
4. Map: which services are called by which API endpoints
```

### Phase 2: Analyze Contracts (5 Rules)

**MANDATORY READ:** Use detection_patterns.md for language-specific Grep patterns per rule.

| # | Rule | Severity | What to Check |
|---|------|----------|---------------|
| 1 | Layer Leakage | HIGH/MEDIUM | Service/domain accepts HTTP types (Request, parsed_body, headers) |
| 2 | Missing DTO | MEDIUM/LOW | 4+ params repeated in 2+ methods without grouping DTO |
| 3 | Entity Leakage | HIGH/MEDIUM | ORM entity returned from API without response DTO. Downgrade when: internal API with no external consumers -> LOW |
| 4 | Error Contracts | MEDIUM/LOW | Mixed error patterns (raise + return None) in same service |
| 5 | Redundant Overloads | LOW/MEDIUM | Method pairs with `_with_`/`_and_` suffix differing by 1-2 params |
| 6 | Architectural Honesty | HIGH/MEDIUM | Read-named function (get_/find_/check_/validate_/is_/has_) body contains write side-effects. Exclusions per `shared/references/ai_ready_architecture.md` |

**Scope boundary:** SKIP DUPLICATION findings (owned by ln-623), REPORT only ARCHITECTURE BOUNDARY findings.

### Phase 3: Calculate 4 Scores

**Compliance Score (0-100):**

| Criterion | Points |
|-----------|--------|
| No layer leakage (HTTP types in service) | +35 |
| Consistent error handling pattern | +25 |
| Follows project naming conventions | +10 |
| No hidden side-effects in read-named functions | +10 |
| No entity leakage to API | +20 |

**Completeness Score (0-100):**

| Criterion | Points |
|-----------|--------|
| All service methods have typed params | +30 |
| All service methods have typed returns | +30 |
| DTOs defined for complex data | +20 |
| Error types documented/typed | +20 |

**Quality Score (0-100):**

| Criterion | Points |
|-----------|--------|
| No boolean flag params in service methods | +15 |
| No opaque return types hiding write actions | +10 |
| No methods with >5 params without DTO | +25 |
| Consistent naming across module | +25 |
| No redundant overloads | +25 |

**Implementation Score (0-100):**

| Criterion | Points |
|-----------|--------|
| DTOs/schemas exist and are used | +30 |
| Type annotations present | +25 |
| Validation at boundaries (Pydantic, Zod) | +25 |
| API response DTOs separate from domain | +20 |

### Phase 3.5: Calculate Score

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/references/audit_scoring.md`.

**Primary score** uses penalty formula (same as all workers):
```
penalty = (critical x 2.0) + (high x 1.0) + (medium x 0.5) + (low x 0.2)
score = max(0, 10 - penalty)
```

**Diagnostic sub-scores** (0-100 each) are calculated separately and reported in AUDIT-META for diagnostic purposes only.

### Phase 4: Write Report

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/templates/audit_worker_report_template.md`.

Write JSON summary per `shared/references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

```
# Build markdown report in memory with:
# - AUDIT-META (extended: score [penalty-based] + diagnostic score_compliance/completeness/quality/implementation)
# - Checks table (layer_leakage, missing_dto, entity_leakage, error_contracts, redundant_overloads)
# - Findings table (issues sorted by severity)
# - DATA-EXTENDED: issues array with principle + domain fields (for cross-domain aggregation)

IF domain_mode == "domain-aware":
  Write to {output_dir}/643-api-contract-{current_domain}.md
ELSE:
  Write to {output_dir}/643-api-contract.md
```

### Phase 5: Return Summary

```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/643-api-contract-users.md
Score: 6.75/10 (C:65 K:70 Q:55 I:80) | Issues: 4 (H:2 M:1 L:1)
```

## Critical Rules

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- **Architecture-level only:** Focus on service boundaries, not internal implementation
- **Read before score:** Never score without reading actual service code
- **Scope boundary:** SKIP duplication findings (owned by ln-623)
- **Detection patterns:** Use language-specific Grep from detection_patterns.md
- **Domain-aware:** When domain_mode="domain-aware", scan only scan_path, tag findings with domain

## Definition of Done

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- [ ] Service boundaries discovered (API, service, domain layers)
- [ ] Method signatures extracted and analyzed
- [ ] All 5 rules checked using detection_patterns.md
- [ ] Scope boundary applied (no duplication with ln-623)
- [ ] 4 scores calculated with justification
- [ ] Issues identified with severity, location, suggestion, effort
- [ ] If domain-aware: findings tagged with domain field
- [ ] Report written to `{output_dir}/643-api-contract[-{domain}].md` (atomic single Write call)
- [ ] Summary written per contract

## Reference Files

- Detection patterns: `references/detection_patterns.md`
- Scoring rules: `../ln-640-pattern-evolution-auditor/references/scoring_rules.md`
- Pattern library: `../ln-640-pattern-evolution-auditor/references/pattern_library.md`

---
**Version:** 2.0.0
**Last Updated:** 2026-02-08
