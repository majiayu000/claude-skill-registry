---
name: ln-640-pattern-evolution-auditor
description: "Audits architectural patterns against best practices (MCP Ref, Context7, WebSearch). Maintains patterns catalog, calculates 4 scores. Output: docs/project/patterns_catalog.md. Use when user asks to: (1) Check architecture health, (2) Audit patterns before refactoring, (3) Find undocumented patterns in codebase."
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Pattern Evolution Auditor

L2 Coordinator that analyzes implemented architectural patterns against current best practices and tracks evolution over time.

## Purpose & Scope

- Maintain `docs/project/patterns_catalog.md` with implemented patterns
- Research best practices via MCP Ref, Context7, WebSearch
- Audit layer boundaries via ln-642 (detect violations, check coverage)
- Calculate 4 scores per pattern via ln-641
- Track quality trends over time (improving/stable/declining)
- Output: `docs/project/patterns_catalog.md` (file-based)
- **Drift Detection:** Track score changes over time, enforce SLA thresholds
- **Auto-remediation:** Create [REFACTOR] Story in Linear when architecture degrades below SLA
- **Health Timeline:** Append-only log in `docs/project/architecture_health.md`

## 4-Score Model

| Score | What it measures | Threshold |
|-------|------------------|-----------|
| **Compliance** | Industry standards, naming, tech stack conventions, layer boundaries | 70% |
| **Completeness** | All components, error handling, observability, tests | 70% |
| **Quality** | Readability, maintainability, no smells, SOLID, no duplication | 70% |
| **Implementation** | Code exists, production use, integrated, monitored | 70% |

## SLA Thresholds & Drift Detection

| Metric | SLA Threshold | Drift Alert | Auto-Action |
|--------|---------------|-------------|-------------|
| **architecture_health_score** | >= 70 | Drop > 10 points between audits | Create [REFACTOR] Story |
| **Per-pattern compliance** | >= 60% | Drop > 15% between audits | Flag in "Requires Attention" |
| **Per-pattern quality** | >= 60% | Drop > 15% between audits | Flag in "Requires Attention" |
| **Layer violations (critical)** | 0 | Any new critical violation | Create [BUG] Story |
| **Cross-domain cycles** | 0 | Any new cycle | Create [REFACTOR] Story |

**SLA breach = automatic Story creation in Linear** (requires Linear MCP). If Linear unavailable, write to `docs/project/architecture_health.md` with `ACTION_REQUIRED` marker.

## Worker Invocation

> **CRITICAL:** All delegations use Task tool with `subagent_type: "general-purpose"` for context isolation.

| Worker | Purpose | Phase |
|--------|---------|-------|
| ln-641-pattern-analyzer | Calculate 4 scores per pattern | Phase 5 |
| ln-642-layer-boundary-auditor | Detect layer violations | Phase 4 |
| ln-643-api-contract-auditor | Audit API contracts, DTOs, layer leakage | Phase 4 |
| ln-644-dependency-graph-auditor | Build dependency graph, detect cycles, validate boundaries, calculate metrics | Phase 4 |
| ln-645-open-source-replacer | Search OSS replacements for custom modules via MCP Research | Phase 4 |
| ln-646-project-structure-auditor | Audit physical structure, hygiene, naming conventions | Phase 4 |

**Prompt template:**
```
Task(description: "[Audit/Create] via ln-6XX",
     prompt: "Execute {skill-name}. Read skill from {skill-name}/SKILL.md. Pattern: {pattern}",
     subagent_type: "general-purpose")
```

**Anti-Patterns:**
- ❌ Direct Skill tool invocation without Task wrapper
- ❌ Any execution bypassing subagent context isolation

## Workflow

### Phase 1a: Baseline Detection

```
1. Load docs/project/patterns_catalog.md
   IF missing → create from shared/templates/patterns_template.md
   IF exists → verify template conformance:
     required_sections = ["Score Legend", "Pattern Inventory", "Discovered Patterns",
       "Layer Boundary Status", "API Contract Status", "Quick Wins",
       "Patterns Requiring Attention", "Pattern Recommendations",
       "Excluded Patterns", "Summary"]
     FOR EACH section IN required_sections:
       IF section NOT found in catalog:
         → Append section from shared/templates/patterns_template.md
     Verify table columns match template (e.g., Recommendation in Quick Wins)
     IF columns mismatch → update table headers, preserve existing data rows

2. Load docs/reference/adrs/*.md → link patterns to ADRs
   Load docs/reference/guides/*.md → link patterns to Guides

3. Auto-detect baseline patterns
   FOR EACH pattern IN pattern_library.md "Pattern Detection" table:
     Grep(detection_keywords) on codebase
     IF found but not in catalog → add as "Undocumented (Baseline)"
```

### Phase 1b: Adaptive Discovery

**MANDATORY READ:** Load `references/pattern_library.md` — use "Discovery Heuristics" section.

Predefined patterns are a **seed, not a ceiling**. Discover project-specific patterns beyond the baseline.

```
# Structural heuristics (from pattern_library.md)
1. Class naming: Grep GoF suffixes (Factory|Builder|Strategy|Adapter|Observer|...)
2. Abstract hierarchy: ABC/Protocol with 2+ implementations → Template Method/Strategy
3. Fluent interface: return self chains → Builder
4. Registration dict: _registry + register() → Registry
5. Middleware chain: app.use/add_middleware → Chain of Responsibility
6. Event listeners: @on_event/@receiver/signal → Observer
7. Decorator wrappers: @wraps/functools.wraps → Decorator

# Document-based heuristics
8. ADR/Guide filenames + H1 headers → extract pattern names not in library
9. Architecture.md → grep pattern terminology
10. Code comments → "pattern:|@pattern|design pattern"

# Output per discovered pattern:
  {name, evidence: [files], confidence: HIGH|MEDIUM|LOW, status: "Discovered"}
  → Add to catalog "Discovered Patterns (Adaptive)" section
```

### Phase 1c: Pattern Recommendations

Suggest patterns that COULD improve architecture (advisory, NOT scored).

```
# Check conditions from pattern_library.md "Pattern Recommendations" table
# E.g., external API calls without retry → recommend Resilience
# E.g., 5+ constructor params → recommend Builder/Parameter Object
# E.g., direct DB access from API layer → recommend Repository

→ Add to catalog "Pattern Recommendations" section
```

### Phase 1d: Applicability Verification

Verify each detected pattern is actually implemented, not just a keyword false positive.

**MANDATORY READ:** Load `references/scoring_rules.md` — use "Required components by pattern" table.

```
FOR EACH detected_pattern IN (baseline_detected + adaptive_discovered):
  IF pattern.source == "adaptive":
    # Adaptive patterns: check confidence + evidence volume
    IF pattern.confidence == "LOW" AND len(pattern.evidence.files) < 3:
      pattern.status = "EXCLUDED"
      pattern.exclusion_reason = "Low confidence, insufficient evidence"
      → Add to catalog "Excluded Patterns" section
      CONTINUE
  ELSE:
    # Baseline patterns: check minimum 2 structural components
    components = get_required_components(pattern, scoring_rules.md)
    found_count = 0
    FOR EACH component IN components:
      IF Grep(component.detection_grep, codebase) has matches:
        found_count += 1
    IF found_count < 2:
      pattern.status = "EXCLUDED"
      pattern.exclusion_reason = "Found {found_count}/{len(components)} components"
      → Add to catalog "Excluded Patterns" section
      CONTINUE

  pattern.status = "VERIFIED"

# Step 2: Semantic applicability via MCP Ref (after structural check passes)
FOR EACH pattern WHERE pattern.status == "VERIFIED":
  ref_search_documentation("{pattern.name} {tech_stack.language} idiom vs architectural pattern")
  WebSearch("{pattern.name} {tech_stack.language} — language feature or design pattern?")

  IF evidence shows pattern is language idiom / stdlib feature / framework built-in:
    pattern.status = "EXCLUDED"
    pattern.exclusion_reason = "Language idiom / built-in feature, not architectural pattern"
    → Add to catalog "Excluded Patterns" section

# Cleanup: remove stale patterns from previous audits
FOR EACH pattern IN existing_catalog WHERE NOT detected in current scan:
  → REMOVE from Pattern Inventory
  → Add to "Excluded Patterns" with reason "No longer detected in codebase"
```

### Phase 2: Best Practices Research

```
FOR EACH pattern WHERE last_audit > 30 days OR never:

  # MCP Ref + Context7 + WebSearch
  ref_search_documentation("{pattern} best practices {tech_stack}")
  IF pattern.library: query-docs(library_id, "{pattern}")
  WebSearch("{pattern} implementation best practices 2026")

  → Store: contextStore.bestPractices[pattern]
```

### Phase 3: Domain Discovery + Output Setup

```
# Detect project structure for domain-aware scanning
domains = detect_domains(src_root)
# e.g., [{name: "users", path: "src/users/"}, {name: "billing", path: "src/billing/"}]

IF len(domains) > 1:
  domain_mode = "domain-aware"
ELSE:
  domain_mode = "global"

# Prepare output directory for worker reports
output_dir = "docs/project/.audit/ln-640/{YYYY-MM-DD}"
mkdir -p {output_dir}   # No deletion — date folders preserve history
```

### Phase 4: Layer Boundary + API Contract + Dependency Graph Audit

```
IF domain_mode == "domain-aware":
  # Per-domain invocation of ln-642, ln-643, ln-644
  FOR EACH domain IN domains (parallel):
    Task(ln-642-layer-boundary-auditor)
      Input: architecture_path, codebase_root, skip_violations, output_dir,
             domain_mode="domain-aware", current_domain=domain.name, scan_path=domain.path
    Task(ln-643-api-contract-auditor)
      Input: pattern="API Contracts", locations=[domain.path], bestPractices, output_dir,
             domain_mode="domain-aware", current_domain=domain.name, scan_path=domain.path
    Task(ln-644-dependency-graph-auditor)
      Input: architecture_path, codebase_root, output_dir,
             domain_mode="domain-aware", current_domain=domain.name, scan_path=domain.path
    Task(ln-645-open-source-replacer)
      Input: codebase_root, tech_stack, output_dir,
             domain_mode="domain-aware", current_domain=domain.name, scan_path=domain.path
    Task(ln-646-project-structure-auditor)
      Input: codebase_root, output_dir,
             domain_mode="domain-aware", current_domain=domain.name, scan_path=domain.path
ELSE:
  Task(ln-642-layer-boundary-auditor)
    Input: architecture_path, codebase_root, skip_violations, output_dir
  Task(ln-643-api-contract-auditor)
    Input: pattern="API Contracts", locations=[service_dirs, api_dirs], bestPractices, output_dir
  Task(ln-644-dependency-graph-auditor)
    Input: architecture_path, codebase_root, output_dir
  Task(ln-645-open-source-replacer)
    Input: codebase_root, tech_stack, output_dir
  Task(ln-646-project-structure-auditor)
    Input: codebase_root, output_dir

# Apply layer deductions from ln-642 return values (score + issue counts)
# Detailed violations read from files in Phase 6
```

### Phase 5: Pattern Analysis Loop

```
# ln-641 stays GLOBAL (patterns are cross-cutting, not per-domain)
# Only VERIFIED patterns from Phase 1d (skip EXCLUDED)
FOR EACH pattern IN catalog WHERE pattern.status == "VERIFIED":
  Task(ln-641-pattern-analyzer)
    Input: pattern, locations, bestPractices, output_dir
```

**Worker Output Contract (file-based):**

**MANDATORY READ:** Load `shared/templates/audit_worker_report_template.md` for file format, naming, AUDIT-META, and DATA-EXTENDED specs.

All workers write reports to `{output_dir}/` and return minimal summary:

| Worker | Return Format | File |
|--------|--------------|------|
| ln-641 | `Score: X.X/10 (C:N K:N Q:N I:N) \| Issues: N` | `641-pattern-{slug}.md` |
| ln-642 | `Score: X.X/10 \| Issues: N (C:N H:N M:N L:N)` | `642-layer-boundary[-{domain}].md` |
| ln-643 | `Score: X.X/10 (C:N K:N Q:N I:N) \| Issues: N` | `643-api-contract[-{domain}].md` |
| ln-644 | `Score: X.X/10 \| Issues: N (C:N H:N M:N L:N)` | `644-dep-graph[-{domain}].md` |
| ln-645 | `Score: X.X/10 \| Issues: N (C:N H:N M:N L:N)` | `645-open-source-replacer[-{domain}].md` |
| ln-646 | `Score: X.X/10 \| Issues: N (C:N H:N M:N L:N)` | `646-structure[-{domain}].md` |

Coordinator parses scores/counts from return values (0 file reads for aggregation tables). Reads files only for cross-domain aggregation (Phase 6) and report assembly (Phase 8).

### Phase 6: Cross-Domain Aggregation (File-Based)

```
IF domain_mode == "domain-aware":
  # Step 1: Read DATA-EXTENDED from ln-642 files
  FOR EACH file IN Glob("{output_dir}/642-layer-boundary-*.md"):
    Read file → extract <!-- DATA-EXTENDED ... --> JSON + Findings table
  # Group findings by issue type across domains
  FOR EACH issue_type IN unique(ln642_findings.issue):
    domains_with_issue = ln642_findings.filter(f => f.issue == issue_type).map(f => f.domain)
    IF len(domains_with_issue) >= 2:
      systemic_findings.append({
        severity: "CRITICAL",
        issue: f"Systemic layer violation: {issue_type} in {len(domains_with_issue)} domains",
        domains: domains_with_issue,
        recommendation: "Address at architecture level, not per-domain"
      })

  # Step 2: Read DATA-EXTENDED from ln-643 files
  FOR EACH file IN Glob("{output_dir}/643-api-contract-*.md"):
    Read file → extract <!-- DATA-EXTENDED ... --> JSON (issues with principle + domain)
  # Group findings by rule across domains
  FOR EACH rule IN unique(ln643_issues.principle):
    domains_with_issue = ln643_issues.filter(i => i.principle == rule).map(i => i.domain)
    IF len(domains_with_issue) >= 2:
      systemic_findings.append({
        severity: "HIGH",
        issue: f"Systemic API contract issue: {rule} in {len(domains_with_issue)} domains",
        domains: domains_with_issue,
        recommendation: "Create cross-cutting architectural fix"
      })

  # Step 3: Read DATA-EXTENDED from ln-644 files
  FOR EACH file IN Glob("{output_dir}/644-dep-graph-*.md"):
    Read file → extract <!-- DATA-EXTENDED ... --> JSON (cycles, sdp_violations)
  # Cross-domain cycles
  FOR EACH cycle IN ln644_cycles:
    domains_in_cycle = unique(cycle.path.map(m => m.domain))
    IF len(domains_in_cycle) >= 2:
      systemic_findings.append({
        severity: "CRITICAL",
        issue: f"Cross-domain dependency cycle: {cycle.path} spans {len(domains_in_cycle)} domains",
        domains: domains_in_cycle,
        recommendation: "Decouple via domain events or extract shared module"
      })

  # Step 4: Read DATA-EXTENDED from ln-645 files
  FOR EACH file IN Glob("{output_dir}/645-open-source-replacer-*.md"):
    Read file → extract <!-- DATA-EXTENDED ... --> JSON (replacements array)
  # Group findings by goal/alternative across domains
  FOR EACH goal IN unique(ln645_replacements.goal):
    domains_with_same = ln645_replacements.filter(r => r.goal == goal).map(r => r.domain)
    IF len(domains_with_same) >= 2:
      systemic_findings.append({
        severity: "HIGH",
        issue: f"Systemic custom implementation: {goal} duplicated in {len(domains_with_same)} domains",
        domains: domains_with_same,
        recommendation: "Single migration across all domains using recommended OSS package"
      })

  # Step 5: Read DATA-EXTENDED from ln-646 files
  FOR EACH file IN Glob("{output_dir}/646-structure-*.md"):
    Read file -> extract <!-- DATA-EXTENDED ... --> JSON
  # Group findings by dimension across domains
  FOR EACH dimension IN ["junk_drawers", "naming_violations"]:
    domains_with_issue = ln646_data.filter(d => d.dimensions[dimension].issues > 0).map(d => d.domain)
    IF len(domains_with_issue) >= 2:
      systemic_findings.append({
        severity: "MEDIUM",
        issue: f"Systemic structure issue: {dimension} in {len(domains_with_issue)} domains",
        domains: domains_with_issue,
        recommendation: "Standardize project structure conventions across domains"
      })

  # Cross-domain SDP violations
  FOR EACH sdp IN ln644_sdp_violations:
    IF sdp.from.domain != sdp.to.domain:
      systemic_findings.append({
        severity: "HIGH",
        issue: f"Cross-domain stability violation: {sdp.from} (I={sdp.I_from}) depends on {sdp.to} (I={sdp.I_to})",
        domains: [sdp.from.domain, sdp.to.domain],
        recommendation: "Apply DIP: extract interface at domain boundary"
      })
```

### Phase 7: Gap Analysis

```
gaps = {
  undocumentedPatterns: found in code but not in catalog,
  missingComponents: required components not found per scoring_rules.md,
  layerViolations: code in wrong architectural layers,
  consistencyIssues: conflicting patterns,
  systemicIssues: systemic_findings from Phase 6
}
```

### Aggregation Algorithm

```
# Step 1: Parse scores from worker return values (already in-context)
# ln-641: "Score: 7.9/10 (C:72 K:85 Q:68 I:90) | Issues: 3 (H:1 M:2 L:0)"
# ln-642: "Score: 4.5/10 | Issues: 8 (C:1 H:3 M:4 L:0)"
# ln-643: "Score: 6.75/10 (C:65 K:70 Q:55 I:80) | Issues: 4 (H:2 M:1 L:1)"
# ln-644: "Score: 6.5/10 | Issues: 8 (C:1 H:3 M:3 L:1)"
pattern_scores = [parse_score(r) for r in ln641_returns]  # Each 0-10
layer_score = parse_score(ln642_return)                     # 0-10
api_score = parse_score(ln643_return)                       # 0-10
graph_score = parse_score(ln644_return)                     # 0-10
structure_score = parse_score(ln646_return)                   # 0-10

# Step 2: Calculate architecture_health_score (ln-645 NOT included — separate metric)
all_scores = pattern_scores + [layer_score, api_score, graph_score, structure_score]
architecture_health_score = round(average(all_scores) * 10)  # 0-100 scale

# Step 2b: Separate reuse opportunity score (informational, no SLA enforcement)
reuse_opportunity_score = parse_score(ln645_return)  # 0-10, NOT in architecture_health_score

# Status mapping:
# >= 80: "healthy"
# 70-79: "warning"
# < 70: "critical"

# Step 3: Context Validation (Post-Filter)
# MANDATORY READ: shared/references/context_validation.md
# Apply Rules 1, 3 to ln-641 anti-pattern findings:
#   Rule 1: Match god_class/large_file findings against ADR list
#   Rule 3: For god_class deductions (-5 compliance):
#     Read flagged file ONCE, check 4 cohesion indicators
#     (public_func_count <= 2, subdirs, shared_state > 60%, CC=1)
#     IF cohesion >= 3: restore deducted -5 points
#     Note in patterns_catalog.md: "[Advisory: high cohesion module]"
# Recalculate architecture_health_score with restored points
```

### Phase 8: Report + Trend Analysis
```
1. Update patterns_catalog.md:
   - Pattern scores, dates
   - Layer Boundary Status section
   - Quick Wins section
   - Patterns Requiring Attention section
2. Calculate trend: compare current vs previous scores
3. Output summary (see Return Result below)
```

### Phase 9: Drift Detection & SLA Enforcement

```
1. Load previous scores from docs/project/architecture_health.md
   IF file missing → create with current scores as baseline, skip drift check
   IF exists → parse last entry

2. Calculate drift:
   health_drift = current.architecture_health_score - previous.architecture_health_score
   FOR EACH pattern:
     compliance_drift = current.compliance - previous.compliance
     quality_drift = current.quality - previous.quality

3. Check SLA thresholds (see SLA Thresholds table):
   breaches = []
   IF architecture_health_score < 70:
     breaches.append({type: "health_below_sla", score: architecture_health_score})
   IF health_drift < -10:
     breaches.append({type: "health_drift", delta: health_drift})
   FOR EACH pattern WHERE compliance_drift < -15 OR quality_drift < -15:
     breaches.append({type: "pattern_drift", pattern: name, delta: min(compliance_drift, quality_drift)})
   FOR EACH new_critical_violation NOT in previous:
     breaches.append({type: "new_critical", violation: description})
   FOR EACH new_cycle NOT in previous:
     breaches.append({type: "new_cycle", cycle: path})

4. Auto-remediation (if breaches found AND Linear MCP available):
   FOR EACH breach:
     IF type IN ["health_below_sla", "health_drift", "new_cycle"]:
       create_issue(title: "[REFACTOR] Architecture health degraded: {breach.type}",
                    description: "SLA breach detected by ln-640...")
     IF type == "new_critical":
       create_issue(title: "[BUG] Critical layer violation: {breach.violation}",
                    description: "New critical violation detected...")

5. Append to docs/project/architecture_health.md:
   ## YYYY-MM-DD
   | Metric | Score | Prev | Delta | Status |
   |--------|-------|------|-------|--------|
   | Health Score | 78 | 82 | -4 | OK |
   | Pattern: Caching | 72/85/68/90 | 75/85/70/90 | -3/0/-2/0 | WARNING |
   ...
   SLA Breaches: {count} | Stories Created: {count}
```

### Phase 10: Return Result

```json
{
  "audit_date": "2026-02-04",
  "architecture_health_score": 78,
  "trend": "improving",
  "patterns_analyzed": 5,
  "layer_audit": {
    "architecture_type": "Layered",
    "violations_total": 5,
    "violations_by_severity": {"high": 2, "medium": 3, "low": 0},
    "coverage": {"http_abstraction": 85, "error_centralization": true}
  },
  "patterns": [
    {
      "name": "Job Processing",
      "scores": {"compliance": 72, "completeness": 85, "quality": 68, "implementation": 90},
      "avg_score": 79,
      "status": "warning",
      "issues_count": 3
    }
  ],
  "quick_wins": [
    {"pattern": "Caching", "issue": "Add TTL config", "effort": "2h", "impact": "+10 completeness"}
  ],
  "requires_attention": [
    {"pattern": "Event-Driven", "avg_score": 58, "critical_issues": ["No DLQ", "No schema versioning"]}
  ],
  "project_structure": {
    "structure_score": 7.5,
    "tech_stack_detected": "react",
    "dimensions": {
      "file_hygiene": {"checks": 6, "issues": 1},
      "ignore_files": {"checks": 4, "issues": 0},
      "framework_conventions": {"checks": 3, "issues": 1},
      "domain_organization": {"checks": 3, "issues": 1},
      "naming_conventions": {"checks": 3, "issues": 0}
    },
    "junk_drawers": 1,
    "naming_violations_pct": 3
  },
  "reuse_opportunities": {
    "reuse_opportunity_score": 6.5,
    "modules_scanned": 15,
    "high_confidence_replacements": 3,
    "medium_confidence_replacements": 5,
    "systemic_custom_implementations": 1
  },
  "dependency_graph": {
    "architecture_detected": "hybrid",
    "architecture_confidence": "MEDIUM",
    "modules_analyzed": 12,
    "cycles_detected": 2,
    "boundary_violations": 3,
    "sdp_violations": 1,
    "nccd": 1.3,
    "score": 6.5
  },
  "cross_domain_issues": [
    {
      "severity": "CRITICAL",
      "issue": "Systemic layer violation: HTTP client in domain layer in 3 domains",
      "domains": ["users", "billing", "orders"],
      "recommendation": "Address at architecture level"
    }
  ],
  "drift": {
    "health_drift": -4,
    "pattern_drifts": [
      {"pattern": "Caching", "compliance_drift": -3, "quality_drift": -2}
    ],
    "sla_breaches": 0,
    "stories_created": 0
  }
}
```

## Critical Rules

- **MCP Ref first:** Always research best practices before analysis
- **Layer audit first:** Run ln-642 before ln-641 pattern analysis
- **4 scores mandatory:** Never skip any score calculation
- **Layer deductions:** Apply scoring_rules.md deductions for violations
- **File output only:** Write results to patterns_catalog.md; exception: SLA breach creates Linear Stories
- **SLA enforcement:** Always run Phase 9 drift detection; skip only on first audit (no baseline)
- **Append-only timeline:** Never overwrite `architecture_health.md`, only append new entries

## Definition of Done

- Pattern catalog loaded or created
- Applicability verified for all detected patterns (Phase 1d); excluded patterns documented
- Best practices researched for all VERIFIED patterns needing audit
- Domain discovery completed (global or domain-aware mode selected)
- Output directory `docs/project/.audit/ln-640/{YYYY-MM-DD}/` created (no deletion of previous runs)
- Layer boundaries audited via ln-642 (reports written to `{output_dir}/`)
- API contracts audited via ln-643 (reports written to `{output_dir}/`)
- Dependency graph audited via ln-644 (reports written to `{output_dir}/`)
- All patterns analyzed via ln-641 (reports written to `{output_dir}/`)
- Open-source replacement opportunities audited via ln-645 (reports written to `{output_dir}/`)
- Project structure audited via ln-646 (reports written to `{output_dir}/`)
- If domain-aware: cross-domain aggregation completed via DATA-EXTENDED from files
- Gaps identified (undocumented, missing components, layer violations, inconsistent, systemic)
- Catalog updated with scores, dates, Layer Boundary Status
- Trend analysis completed
- Summary report output
- Drift detection completed (Phase 9): scores compared to previous, SLA thresholds checked
- SLA breaches handled: [REFACTOR]/[BUG] Stories created in Linear (or ACTION_REQUIRED in health file)
- Architecture health timeline appended to `docs/project/architecture_health.md`

## Reference Files

- **Worker report template:** `shared/templates/audit_worker_report_template.md`
- **Task delegation pattern:** `shared/references/task_delegation_pattern.md`
- Pattern catalog template: `shared/templates/patterns_template.md`
- Pattern library (detection + best practices + discovery): `references/pattern_library.md`
- Layer boundary rules (for ln-642): `references/layer_rules.md`
- Scoring rules: `references/scoring_rules.md`
- Pattern analysis: `../ln-641-pattern-analyzer/SKILL.md`
- Layer boundary audit: `../ln-642-layer-boundary-auditor/SKILL.md`
- API contract audit: `../ln-643-api-contract-auditor/SKILL.md`
- Dependency graph audit: `../ln-644-dependency-graph-auditor/SKILL.md`
- Open-source replacement audit: `../ln-645-open-source-replacer/SKILL.md`
- Project structure audit: `../ln-646-project-structure-auditor/SKILL.md`

---
**Version:** 2.0.0
**Last Updated:** 2026-02-08
