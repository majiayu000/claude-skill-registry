---
name: ln-644-dependency-graph-auditor
description: "Builds dependency graph, detects cycles, validates boundary rules, calculates coupling metrics (Ca/Ce/I). Use when auditing dependency structure."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__index_project, mcp__hex-graph__analyze_architecture, mcp__hex-graph__trace_paths
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

**Type:** L3 Worker
**Category:** 6XX Audit

# Dependency Graph Auditor

L3 Worker that builds and analyzes the module dependency graph to enforce architectural boundaries.

## Purpose & Scope

- Build module dependency graph from import statements (Python, TS/JS, C#, Java)
- Detect circular dependencies: pairwise (HIGH) + transitive via DFS (CRITICAL)
- Validate boundary rules: forbidden, allowed, required (per dependency-cruiser pattern)
- Calculate Robert C. Martin metrics (Ca, Ce, Instability) + Lakos aggregate (CCD, NCCD)
- Validate Stable Dependencies Principle (SDP)
- Support baseline/freeze for incremental legacy adoption (per ArchUnit FreezingArchRule)
- **Adaptive:** 3-tier architecture detection -- custom rules > docs > auto-detect

**Out of Scope** (owned by other workers):
- I/O isolation violations (grep-based) -> ln-642-layer-boundary-auditor
- API contract violations -> ln-643-api-contract-auditor
- Code duplication -> ln-623-code-principles-auditor

## Input (from ln-640)

```
- architecture_path: string    # Path to docs/architecture.md
- codebase_root: string        # Root directory to scan
- output_dir: string           # e.g., ".hex-skills/runtime-artifacts/runs/{run_id}/audit-report"

# Domain-aware (optional, from coordinator)
- domain_mode: "global" | "domain-aware"   # Default: "global"
- current_domain: string                   # e.g., "users", "billing" (only if domain-aware)
- scan_path: string                        # e.g., "src/users/" (only if domain-aware)

# Baseline (optional)
- update_baseline: boolean                 # If true, save current state as baseline
```

**When domain_mode="domain-aware":** Use `scan_path` instead of `codebase_root` for all Grep/Glob operations. Tag all findings with `domain` field.

## Workflow

**MANDATORY READ:** Load `shared/references/two_layer_detection.md` for detection methodology.

### Phase 1: Discover Architecture (Adaptive)

**MANDATORY READ:** Load `references/dependency_rules.md` -- use 3-Tier Priority Chain, Architecture Presets, Auto-Detection Heuristics.

Architecture detection uses **3-tier priority** -- explicit config wins over docs, docs win over auto-detection:

```
# Priority 1: Explicit project config
IF docs/project/dependency_rules.yaml exists:
  Load custom rules (modules, forbidden, allowed, required)
  SKIP preset detection

# Priority 2: Architecture documentation
ELIF docs/architecture.md exists:
  Read Section 4.2 (modules, layers, architecture_type)
  Read Section 6.4 (boundary rules, if defined)
  Map documented layers to presets from dependency_rules.md
  Apply preset rules, override with explicit rules from Section 6.4

# Priority 3: Auto-detection from directory structure
ELSE:
  scan_root = scan_path IF domain_mode == "domain-aware" ELSE codebase_root
  Run structure heuristics:

  signals = {}
  IF Glob("**/domain/**") AND Glob("**/infrastructure/**"):
    signals["clean"] = HIGH
  IF Glob("**/controllers/**") AND Glob("**/services/**") AND Glob("**/repositories/**"):
    signals["layered"] = HIGH
  IF Glob("**/features/*/") with internal structure:
    signals["vertical"] = HIGH
  IF Glob("**/adapters/**") AND Glob("**/ports/**"):
    signals["hexagonal"] = HIGH
  IF Glob("**/views/**") AND Glob("**/models/**"):
    signals["mvc"] = HIGH

  IF len(signals) == 0:
    architecture_mode = "custom"
    confidence = "LOW"
    # Only check cycles + metrics, no boundary presets
  ELIF len(signals) == 1:
    architecture_mode = signals.keys()[0]
    confidence = signals.values()[0]
    Apply matching preset from dependency_rules.md
  ELSE:
    architecture_mode = "hybrid"
    confidence = "MEDIUM"
    # Identify zones, apply different presets per zone (see dependency_rules.md Hybrid section)
    FOR EACH detected_style IN signals:
      zone_path = identify_zone(detected_style)
      zone_preset = load_preset(detected_style)
      zones.append({path: zone_path, preset: zone_preset})
    Add cross-zone rules: inner zones accessible, outer zones forbidden to depend on inner
```

### Phase 2: Build Dependency Graph

**MANDATORY READ:** Load `references/import_patterns.md` -- use Language Detection, Import Grep Patterns, Module Resolution Algorithm, Exclusion Lists.

```
scan_root = scan_path IF domain_mode == "domain-aware" ELSE codebase_root

# Step 1: Detect primary language
tech_stack = Read(docs/project/tech_stack.md) IF exists
  ELSE detect from file extensions: Glob("**/*.py", "**/*.ts", "**/*.cs", "**/*.java", root=scan_root)

# Step 2: Extract imports per language
FOR EACH source_file IN Glob(language_glob_pattern, root=scan_root):
  imports = []

  # Python
  IF language == "python":
    from_imports = Grep("^from\s+([\w.]+)\s+import", source_file)
    plain_imports = Grep("^import\s+([\w.]+)", source_file)
    imports = from_imports + plain_imports

  # TypeScript / JavaScript
  ELIF language == "typescript" OR language == "javascript":
    es6_imports = Grep("import\s+.*\s+from\s+['\"]([^'\"]+)['\"]", source_file)
    require_imports = Grep("require\(['\"]([^'\"]+)['\"]\)", source_file)
    imports = es6_imports + require_imports

  # C#
  ELIF language == "csharp":
    using_imports = Grep("^using\s+([\w.]+);", source_file)
    imports = using_imports

  # Java
  ELIF language == "java":
    java_imports = Grep("^import\s+([\w.]+);", source_file)
    imports = java_imports

  # Step 3: Filter internal only (per import_patterns.md Exclusion Lists)
  internal_imports = filter_internal(imports, scan_root)

  # Step 4: Resolve to modules
  FOR EACH imp IN internal_imports:
    source_module = resolve_module(source_file, scan_root)
    target_module = resolve_module(imp, scan_root)
    IF source_module != target_module:
      graph[source_module].add(target_module)
```

### Phase 3: Detect Cycles (ADP)

**hex-graph acceleration:** For projects with `.hex-skills/codegraph/index.db`, use `analyze_architecture(verbosity="full")` and inspect returned `cycles` for instant cycle detection. These cycle and coupling metrics are workspace-module level, so single-package repos may collapse to one module. Fall back to grep-based DFS or symbol/file-level tracing when graph output is too coarse for intra-package analysis.

Per Robert C. Martin (Clean Architecture Ch14): "Allow no cycles in the component dependency graph."

```
# Pairwise cycles (A <-> B)
FOR EACH (A, B) WHERE B IN graph[A] AND A IN graph[B]:
  cycles.append({
    type: "pairwise",
    path: [A, B, A],
    severity: "HIGH",
    fix: suggest_cycle_fix(A, B)
  })
  # Layer 2: Test-only dependencies (devDependencies, test imports) -> skip cycle
  # Plugin/extension architecture with documented bidirectional design -> downgrade to LOW

# Transitive cycles via DFS (A -> B -> C -> A)
visited = {}
rec_stack = {}

FUNCTION dfs(node, path):
  visited[node] = true
  rec_stack[node] = true

  FOR EACH neighbor IN graph[node]:
    IF NOT visited[neighbor]:
      dfs(neighbor, path + [node])
    ELIF rec_stack[neighbor]:
      cycle_path = extract_cycle(path + [node], neighbor)
      IF len(cycle_path) > 2:  # Skip pairwise (already detected)
        cycles.append({
          type: "transitive",
          path: cycle_path,
          severity: "CRITICAL",
          fix: suggest_cycle_fix_transitive(cycle_path)
        })

  rec_stack[node] = false

FOR EACH module IN graph:
  IF NOT visited[module]:
    dfs(module, [])

# Folder-level cycles (per dependency-cruiser pattern)
folder_graph = collapse_to_folders(graph)
Repeat DFS on folder_graph for folder-level cycles
```

**Cycle-breaking recommendations** (from Clean Architecture Ch14):
1. **DIP** -- extract interface in depended-upon module, implement in depending module
2. **Extract Shared Component** -- move shared code to new module both depend on
3. **Domain Events / Message Bus** -- for cross-domain cycles, decouple via async communication

### Phase 4: Validate Boundary Rules

```
# Load rules from Phase 1 discovery
# rules = {forbidden: [], allowed: [], required: []}

# Check FORBIDDEN rules
FOR EACH rule IN rules.forbidden:
  FOR EACH edge (source -> target) IN graph:
    IF matches(source, rule.from) AND matches(target, rule.to):
      IF rule.cross AND same_group(source, target):
        CONTINUE  # cross=true means only cross-group violations
      boundary_violations.append({
        rule_type: "forbidden",
        from: source,
        to: target,
        file: get_import_location(source, target),
        severity: rule.severity,
        reason: rule.reason
      })

# Check ALLOWED rules (whitelist mode)
IF rules.allowed.length > 0:
  FOR EACH edge (source -> target) IN graph:
    allowed = false
    FOR EACH rule IN rules.allowed:
      IF matches(source, rule.from) AND matches(target, rule.to):
        allowed = true
        BREAK
    IF NOT allowed:
      boundary_violations.append({
        rule_type: "not_in_allowed",
        from: source,
        to: target,
        file: get_import_location(source, target),
        severity: "MEDIUM",
        reason: "Dependency not in allowed list"
      })

# Check REQUIRED rules
FOR EACH rule IN rules.required:
  FOR EACH module IN graph WHERE matches(module, rule.module):
    has_required = false
    FOR EACH dep IN graph[module]:
      IF matches(dep, rule.must_depend_on):
        has_required = true
        BREAK
    IF NOT has_required:
      boundary_violations.append({
        rule_type: "required_missing",
        module: module,
        missing: rule.must_depend_on,
        severity: "MEDIUM",
        reason: rule.reason
      })
```

### Phase 5: Calculate Graph Metrics

**hex-graph acceleration:** For projects with `.hex-skills/codegraph/index.db`, use `analyze_architecture(verbosity="full")` and inspect returned `coupling` metrics for instant Ca/Ce/I calculation. Fall back to manual computation when graph is unavailable.

**MANDATORY READ:** Load `references/graph_metrics.md` -- use Metric Definitions, Thresholds per Layer, SDP Algorithm, Lakos Formulas.

```
# Per-module metrics (Robert C. Martin)
FOR EACH module IN graph:
  Ce = len(graph[module])                          # Efferent: outgoing
  Ca = count(m for m in graph if module in graph[m])  # Afferent: incoming
  I = Ce / (Ca + Ce) IF (Ca + Ce) > 0 ELSE 0      # Instability

  metrics[module] = {Ca, Ce, I}

# SDP validation (Stable Dependencies Principle)
FOR EACH edge (A -> B) IN graph:
  IF metrics[A].I < metrics[B].I:
    # Stable module depends on less stable module -- SDP violation
    sdp_violations.append({
      from: A, to: B,
      I_from: metrics[A].I, I_to: metrics[B].I,
      severity: "HIGH"
    })

# Threshold checks (per graph_metrics.md, considering detected layer)
FOR EACH module IN metrics:
  layer = get_layer(module)  # From Phase 1 discovery
  thresholds = get_thresholds(layer)  # From graph_metrics.md

  IF metrics[module].I > thresholds.max_instability:
    findings.append({severity: thresholds.severity, issue: f"{module} instability {I} exceeds {thresholds.max_instability}"})
  IF metrics[module].Ce > thresholds.max_ce:
    findings.append({severity: "MEDIUM", issue: f"{module} efferent coupling {Ce} exceeds {thresholds.max_ce}"})

# Lakos aggregate metrics
CCD = 0
FOR EACH module IN graph:
  DependsOn = count_transitive_deps(module, graph) + 1  # Including self
  CCD += DependsOn

N = len(graph)
CCD_balanced = N * log2(N)  # CCD of balanced binary tree with N nodes
NCCD = CCD / CCD_balanced IF CCD_balanced > 0 ELSE 0

IF NCCD > 1.5:
  findings.append({severity: "MEDIUM", issue: f"Graph complexity (NCCD={NCCD:.2f}) exceeds balanced tree threshold (1.5)"})
```

**Cascade chain extension:** For service files (`**/services/**`), extend module-level graph to function-level. Find longest side-effect chain per public function (markers per `shared/references/ai_ready_architecture.md`). If chain_length >= 3: add to cascade_findings. Output `"runtime_cascades"` array in Phase 8 DATA-EXTENDED JSON. Severity: HIGH (4+), MEDIUM (3).

### Phase 6: Baseline Support

Inspired by ArchUnit FreezingArchRule -- enables incremental adoption in legacy projects.

```
baseline_path = docs/project/dependency_baseline.json

IF file_exists(baseline_path):
  known = load_json(baseline_path)
  current = serialize_violations(cycles + boundary_violations + sdp_violations)

  new_violations = current - known
  resolved_violations = known - current

  # Report only NEW violations as findings
  active_findings = new_violations
  baseline_info = {new: len(new_violations), resolved: len(resolved_violations), frozen: len(known - resolved_violations)}

  IF input.update_baseline == true:
    save_json(baseline_path, current)

ELSE:
  # First run -- report all
  active_findings = all_violations
  baseline_info = {new: len(all_violations), resolved: 0, frozen: 0}
  # Suggest: output note "Run with update_baseline=true to freeze current violations"
```

### Phase 7: Calculate Score

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/references/audit_scoring.md`.

```
penalty = (critical * 2.0) + (high * 1.0) + (medium * 0.5) + (low * 0.2)
score = max(0, 10 - penalty)
```

**Note:** When baseline is active, penalty is calculated from `active_findings` only (new violations), not frozen ones.

### Phase 8: Write Report

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/templates/audit_worker_report_template.md`.

Write JSON summary per `shared/references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

```
# Build markdown report in memory with:
# - AUDIT-META (standard penalty-based: score, counts)
# - Checks table (cycle_detection, boundary_rules, sdp_validation, metrics_thresholds, baseline_comparison)
# - Findings table (active violations sorted by severity)
# - DATA-EXTENDED: {graph_stats, cycles, boundary_violations, sdp_violations, metrics, baseline}

IF domain_mode == "domain-aware":
  Write to {output_dir}/644-dep-graph-{current_domain}.md
ELSE:
  Write to {output_dir}/644-dep-graph.md
```

### Phase 9: Return Summary

```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/644-dep-graph-users.md
Score: 6.5/10 | Issues: 8 (C:1 H:3 M:3 L:1)
```

## Critical Rules

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- **Adaptive architecture** -- never assume one style; detect from project structure or docs
- **3-tier priority** -- custom rules > architecture.md > auto-detection
- **Hybrid support** -- projects mix styles; apply different presets per zone
- **Custom = safe mode** -- if no pattern detected, only check cycles + metrics (no false boundary violations)
- **Internal only** -- exclude stdlib, third-party from graph (only project modules)
- **Baseline mode** -- when baseline exists, report only NEW violations
- **Cycle fixes** -- always provide actionable recommendation (DIP, Extract Shared, Domain Events)
- **File + line** -- always provide exact import location for violations

## Definition of Done

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- [ ] Architecture discovered (adaptive 3-tier detection applied)
- [ ] Dependency graph built from import statements (internal modules only)
- [ ] Circular dependencies detected (pairwise + transitive DFS + folder-level)
- [ ] Boundary rules validated (forbidden + allowed + required)
- [ ] Metrics calculated (Ca, Ce, I per module + CCD, NCCD aggregate)
- [ ] SDP validated (stable modules not depending on unstable)
- [ ] Baseline applied if exists (only new violations reported)
- [ ] If domain-aware: all Grep/Glob scoped to scan_path, findings tagged with domain
- [ ] Score calculated per audit_scoring.md
- [ ] Report written to `{output_dir}/644-dep-graph[-{domain}].md` (atomic single Write call)
- [ ] Summary written per contract

## Reference Files

- Boundary rules & presets: `references/dependency_rules.md`
- Metrics & thresholds: `references/graph_metrics.md`
- Import patterns: `references/import_patterns.md`
- Scoring algorithm: `shared/references/audit_scoring.md`

---

**Version:** 1.0.0
**Last Updated:** 2026-02-11
