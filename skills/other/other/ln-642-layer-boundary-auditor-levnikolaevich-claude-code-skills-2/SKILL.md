---
name: ln-642-layer-boundary-auditor
description: "Checks layer boundary violations, transaction boundaries, session ownership, cross-layer consistency. Use when auditing architecture layers."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__find_references, mcp__hex-graph__trace_paths, mcp__hex-graph__inspect_symbol, mcp__hex-graph__analyze_architecture
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Layer Boundary Auditor

**Type:** L3 Worker

L3 Worker that audits architectural layer boundaries and detects violations.

## Purpose & Scope

- Read architecture.md to discover project's layer structure
- Detect layer violations (I/O code outside infrastructure layer)
- **Detect cross-layer consistency issues:**
  - Transaction boundaries (commit/rollback ownership)
  - Session ownership (DI vs local)
- Check pattern coverage (all HTTP calls use client abstraction)
- Detect error handling duplication
- Return violations list to coordinator

**Out of Scope** (owned by ln-628-concurrency-auditor):
- Blocking I/O in async functions (sync open/read in async def)
- Fire-and-forget tasks (create_task without error handler)

## Input (from ln-640)

```
- architecture_path: string    # Path to docs/architecture.md
- codebase_root: string        # Root directory to scan
- skip_violations: string[]    # Files to skip (legacy)
- output_dir: string           # e.g., ".hex-skills/runtime-artifacts/runs/{run_id}/audit-report"

# Domain-aware (optional, from coordinator)
- domain_mode: "global" | "domain-aware"   # Default: "global"
- current_domain: string                   # e.g., "users", "billing" (only if domain-aware)
- scan_path: string                        # e.g., "src/users/" (only if domain-aware)
```

**When domain_mode="domain-aware":** Use `scan_path` instead of `codebase_root` for all Grep/Glob operations. Tag all findings with `domain` field.

## Workflow

**MANDATORY READ:** Load `shared/references/two_layer_detection.md` for detection methodology.

### Phase 1: Discover Architecture

**MANDATORY READ:** Load `../ln-640-pattern-evolution-auditor/references/layer_rules.md` -- use Architecture Presets (fallback), I/O Pattern Boundary Rules (Phase 2), Coverage Checks (Phase 4), Cross-Layer Consistency rules (Phase 3).

```
Read docs/architecture.md

Extract from Section 4.2 (Top-Level Decomposition):
  - architecture_type: "Layered" | "Hexagonal" | "Clean" | "MVC" | etc.
  - layers: [{name, directories[], purpose}]

Extract from Section 5.3 (Infrastructure Layer Components):
  - infrastructure_components: [{name, responsibility}]

IF architecture.md not found:
  Use fallback presets from layer_rules.md

Build ruleset:
  FOR EACH layer:
    allowed_deps = layers that can be imported
    forbidden_deps = layers that cannot be imported
```


**Graph acceleration (if available):** IF `contextStore.graph_indexed` OR `.hex-skills/codegraph/index.db` exists:
- **Module coupling:** `analyze_architecture(path=scan_root, verbosity="full")` -- use returned coupling metrics to identify tightly-coupled layers.
- **Cross-layer calls:** `find_references(symbol)` for transaction/session functions -- trace commit/rollback ownership across layers.
- **Orchestration depth:** `trace_paths(name="ServiceFn", file="...", path_kind="calls", direction="forward", depth=3, path=scan_root)` -- measure chain depth for flat orchestration check from a concrete service symbol.
- Empty `trace_paths` from a coarse or module-level selector is not enough to clear a layer; fall back to `inspect_symbol` or grep/manual review when the selector is broad.
- Fall back to grep-based detection below if graph unavailable.
### Phase 2: Detect Layer Violations

```
scan_root = scan_path IF domain_mode == "domain-aware" ELSE codebase_root

FOR EACH violation_type IN layer_rules.md I/O Pattern Boundary Rules:
  grep_pattern = violation_type.detection_grep
  forbidden_dirs = violation_type.forbidden_in

  matches = Grep(grep_pattern, scan_root, include="*.py,*.ts,*.js")

  FOR EACH match IN matches:
    IF match.path NOT IN skip_violations:
      IF any(forbidden IN match.path FOR forbidden IN forbidden_dirs):
        violations.append({
          type: "layer_violation",
          severity: "HIGH",
          pattern: violation_type.name,
          file: match.path,
          line: match.line,
          code: match.context,
          allowed_in: violation_type.allowed_in,
          suggestion: f"Move to {violation_type.allowed_in}"
        })
```

### Phase 3: Cross-Layer Consistency Checks

#### 3.1 Transaction Boundary Violations

**What:** commit()/rollback() called at inconsistent layers (repo + service + API)

**Detection:**
```
repo_commits = Grep("\.commit\(\)|\.rollback\(\)", "**/repositories/**/*.py")
service_commits = Grep("\.commit\(\)|\.rollback\(\)", "**/services/**/*.py")
api_commits = Grep("\.commit\(\)|\.rollback\(\)", "**/api/**/*.py")

layers_with_commits = count([repo_commits, service_commits, api_commits].filter(len > 0))
```

**Safe Patterns (ignore):**
- Comment "# best-effort telemetry" in same context
- File ends with `_callbacks.py` (progress notifiers)
- Explicit `# UoW boundary` comment

**Violation Rules:**

| Condition | Severity | Issue |
|-----------|----------|-------|
| layers_with_commits >= 3 | CRITICAL | Mixed UoW ownership across all layers |
| repo + api commits | HIGH | Transaction control bypasses service layer |
| repo + service commits | HIGH | Ambiguous UoW owner (repo vs service) |
| service + api commits | MEDIUM | Transaction control spans service + API |

**Exception:** Saga pattern / distributed transactions with explicit compensating actions -> downgrade CRITICAL to MEDIUM. UoW boundary documented with `// architecture decision` or ADR -> skip.

**Recommendation:** Choose single UoW owner (service layer recommended), remove commit() from other layers

**Effort:** L (requires architectural decision + refactoring)

#### 3.2 Session Ownership Violations

**What:** Mixed DI-injected and locally-created sessions in same call chain

**Detection:**
```
di_session = Grep("Depends\(get_session\)|Depends\(get_db\)", "**/api/**/*.py")
local_session = Grep("AsyncSessionLocal\(\)|async_sessionmaker", "**/services/**/*.py")
local_in_repo = Grep("AsyncSessionLocal\(\)", "**/repositories/**/*.py")
```

**Violation Rules:**

| Condition | Severity | Issue |
|-----------|----------|-------|
| di_session AND local_in_repo in same module | HIGH | Repo creates own session while API injects different |
| local_session in service calling DI-based repo | MEDIUM | Session mismatch in call chain |

**Recommendation:** Use DI consistently OR use local sessions consistently. Document exceptions (e.g., telemetry)

**Effort:** M

#### 3.3 Flat Orchestration Violations

**What:** Service-layer functions calling other services that call yet other services -- deep orchestration chains.

**Detection:** **MANDATORY READ:** Load `shared/references/ai_ready_architecture.md` -- map service imports, find chain depth.

**Violation Rules:**

| Condition | Severity | Issue |
|-----------|----------|-------|
| Service chain >= 3 (A->B->C->D) | HIGH | Deep orchestration |
| Service chain = 2 (A->B->C) | MEDIUM | Consider flattening |

**Recommendation:** Extract orchestrator calling all services at same level. Each service becomes a sink.

**Effort:** L

---

### Phase 4: Check Pattern Coverage

```
# HTTP Client Coverage
all_http_calls = Grep("httpx\\.|aiohttp\\.|requests\\.", codebase_root)
abstracted_calls = Grep("client\\.(get|post|put|delete)", infrastructure_dirs)

IF len(all_http_calls) > 0:
  coverage = len(abstracted_calls) / len(all_http_calls) * 100
  IF coverage < 90%:
    violations.append({
      type: "low_coverage",
      severity: "MEDIUM",
      pattern: "HTTP Client Abstraction",
      coverage: coverage,
      uncovered_files: files with direct calls outside infrastructure
    })

# Error Handling Duplication
http_error_handlers = Grep("except\\s+(httpx\\.|aiohttp\\.|requests\\.)", codebase_root)
unique_files = set(f.path for f in http_error_handlers)

IF len(unique_files) > 2:
  violations.append({
    type: "duplication",
    severity: "MEDIUM",
    pattern: "HTTP Error Handling",
    files: list(unique_files),
    suggestion: "Centralize in infrastructure layer"
  })
```

### Phase 5: Calculate Score

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/references/audit_scoring.md`.

### Phase 6: Write Report

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/templates/audit_worker_report_template.md`.

Write JSON summary per `shared/references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

```
# Build markdown report in memory with:
# - AUDIT-META (standard penalty-based: score, counts)
# - Checks table (io_isolation, http_abstraction, error_centralization, transaction_boundary, session_ownership)
# - Findings table (violations sorted by severity)
# - DATA-EXTENDED: {architecture, coverage}

IF domain_mode == "domain-aware":
  Write to {output_dir}/642-layer-boundary-{current_domain}.md
ELSE:
  Write to {output_dir}/642-layer-boundary.md
```

### Phase 7: Return Summary

```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/642-layer-boundary-users.md
Score: 4.5/10 | Issues: 8 (C:1 H:3 M:4 L:0)
```

## Critical Rules

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- **Read architecture.md first** - never assume architecture type
- **Skip violations list** - respect legacy files marked for gradual fix
- **File + line + code** - always provide exact location with context
- **Actionable suggestions** - always tell WHERE to move the code
- **No false positives** - verify path contains forbidden dir, not just substring

## Definition of Done

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- [ ] Architecture discovered from docs/architecture.md (or fallback used)
- [ ] All violation types from layer_rules.md checked
- [ ] **Cross-layer consistency checked:**
  - Transaction boundaries analyzed (commit/rollback distribution)
  - Session ownership analyzed (DI vs local)
- [ ] Coverage calculated for HTTP abstraction + 2 consistency metrics
- [ ] Violations list with severity, location, suggestion
- [ ] If domain-aware: all Grep scoped to scan_path, findings tagged with domain
- [ ] Report written to `{output_dir}/642-layer-boundary[-{domain}].md` (atomic single Write call)
- [ ] Summary written per contract

## Reference Files

- Layer rules: `../ln-640-pattern-evolution-auditor/references/layer_rules.md`
- Scoring impact: `../ln-640-pattern-evolution-auditor/references/scoring_rules.md`

---

**Version:** 2.1.0
**Last Updated:** 2026-02-08
