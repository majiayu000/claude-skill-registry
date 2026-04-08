---
name: ln-645-open-source-replacer
description: "Discovers custom modules replaceable by OSS, evaluates alternatives (stars, license, CVE), generates migration plan. Use when reducing custom code."
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch, mcp__Ref, mcp__context7, mcp__hex-graph__find_references, mcp__hex-graph__analyze_architecture
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Open Source Replacer

**Type:** L3 Worker

L3 Worker that discovers custom modules, analyzes their purpose, and finds battle-tested open-source replacements via MCP Research.

## Purpose & Scope

- Discover significant custom modules (>=100 LOC, utility/integration type)
- Analyze PURPOSE of each module by reading code (goal-based, not pattern-based)
- Search open-source alternatives via WebSearch, Context7, Ref
- Evaluate alternatives: stars, maintenance, license, CVE status, API compatibility
- Score replacement confidence (HIGH/MEDIUM/LOW)
- Generate migration plan for viable replacements
- Output: markdown evidence report in runtime artifacts plus machine-readable JSON summary for coordinator transport

**Out of Scope:**
- Pattern-based detection of known reinvented wheels (custom sorting, hand-rolled validation)
- Package vulnerability scanning (CVE/CVSS for existing dependencies)
- Story-level optimality checks via OPT- prefix

## Input

```
- codebase_root: string        # Project root
- tech_stack: object            # Language, framework, package manager, existing dependencies
- output_dir: string            # e.g., ".hex-skills/runtime-artifacts/runs/{run_id}/audit-report"

# Domain-aware (optional, from coordinator)
- domain_mode: "global" | "domain-aware"   # Default: "global"
- current_domain: string                   # e.g., "users", "billing" (only if domain-aware)
- scan_path: string                        # e.g., "src/users/" (only if domain-aware)
```

## Workflow

**MANDATORY READ:** Load `shared/references/two_layer_detection.md` for detection methodology.

### Phase 1: Discovery + Classification

```
scan_root = scan_path IF domain_mode == "domain-aware" ELSE codebase_root

# Step 1: Find significant custom files
candidates = []
FOR EACH file IN Glob("**/*.{ts,js,py,rb,go,java,cs}", root=scan_root):
  IF file in node_modules/ OR vendor/ OR .venv/ OR dist/ OR build/ OR test/ OR __test__/:
    SKIP
  line_count = wc -l {file}
  IF line_count >= 100:
    candidates.append(file)

# Step 2: Filter to utility/library-like modules
utility_paths = ["utils/", "lib/", "helpers/", "common/", "shared/", "pkg/", "internal/"]
name_patterns = ["parser", "formatter", "validator", "converter", "encoder",
                 "decoder", "serializer", "logger", "cache", "queue", "scheduler",
                 "mailer", "http", "client", "wrapper", "adapter", "connector",
                 "transformer", "mapper", "builder", "factory", "handler"]

modules = []
FOR EACH file IN candidates:
  is_utility_path = any(p in file.lower() for p in utility_paths)
  is_utility_name = any(p in basename(file).lower() for p in name_patterns)
  export_count = count_exports(file)  # Grep for export/module.exports/def/class
  IF is_utility_path OR is_utility_name OR export_count > 5:
    modules.append(file)

# Step 3: Pre-classification gate
FOR EACH module IN modules:
  # Read first 30 lines to classify
  header = Read(module, limit=30)
  classify as:
    - "utility": generic reusable logic (validation, parsing, formatting, HTTP, caching)
    - "integration": wrappers around external services (email, payments, storage)
    - "domain-specific": business logic unique to project (scoring, routing, pricing rules)

  IF classification == "domain-specific":
    no_replacement_found.append({module, reason: "Domain-specific business logic"})
    REMOVE from modules

# Cap: analyze max 15 utility/integration modules per invocation
modules = modules[:15]
```

### Phase 2: Goal Extraction

```
FOR EACH module IN modules:
  # Read code (first 200 lines + exports summary)
  code = Read(module, limit=200)
  exports = Grep("export|module\.exports|def |class |func ", module)

  # Extract goal: what problem does this module solve?
  goal = {
    domain: "email validation" | "HTTP retry" | "CSV parsing" | ...,
    inputs: [types],
    outputs: [types],
    key_operations: ["validates email format", "checks MX records", ...],
    complexity_indicators: ["regex", "network calls", "state machine", "crypto", ...],
    summary: "Custom email validator with MX record checking and disposable domain filtering"
  }
```

### Phase 3: Alternative Search (MCP Research)

```
FOR EACH module WHERE module.goal extracted:
  # Strategy 1: WebSearch (primary)
  WebSearch("{goal.domain} {tech_stack.language} library package 2026")
  WebSearch("{goal.summary} open source alternative {tech_stack.language}")

  # Strategy 2: Context7 (for known ecosystems)
  IF tech_stack.package_manager == "npm":
    WebSearch("{goal.domain} npm package weekly downloads")
  IF tech_stack.package_manager == "pip":
    WebSearch("{goal.domain} python library pypi")

  # Strategy 3: Ref (documentation search)
  ref_search_documentation("{goal.domain} {tech_stack.language} recommended library")

  # Strategy 4: Ecosystem alignment -- check if existing project dependencies
  # already cover this goal (e.g., project uses Zod -> check zod plugins first)
  FOR EACH dep IN tech_stack.existing_dependencies:
    IF dep.ecosystem overlaps goal.domain:
      WebSearch("{dep.name} {goal.domain} plugin extension")

  # Collect candidates (max 5 per module)
  alternatives = top_5_by_relevance(search_results)
```

### Phase 4: Evaluation

**MANDATORY:** Security Gate and License Classification run for EVERY candidate before confidence assignment.

```
FOR EACH module, FOR EACH alternative:
  # 4a. Basic info
  info = {
    name: "zod" | "email-validator" | ...,
    version: "latest stable",
    weekly_downloads: N,
    github_stars: N,
    last_commit: "YYYY-MM-DD",
  }

  # 4b. Security Gate (mandatory)
  WebSearch("{alternative.name} CVE vulnerability security advisory")
  IF unpatched HIGH/CRITICAL CVE found:
    security_status = "VULNERABLE"
    -> Cap confidence at LOW, add warning to Findings
  ELIF patched CVE (older version):
    security_status = "PATCHED_CVE"
    -> Note in report, no confidence cap
  ELSE:
    security_status = "CLEAN"

  # 4c. License Classification
  license = detect_license(alternative)
  IF license IN ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Unlicense"]:
    license_class = "PERMISSIVE"
  ELIF license IN ["GPL-2.0", "GPL-3.0", "AGPL-3.0", "LGPL-2.1", "LGPL-3.0"]:
    IF project_license is copyleft AND compatible:
      license_class = "COPYLEFT_COMPATIBLE"
    ELSE:
      license_class = "COPYLEFT_INCOMPATIBLE"
  ELSE:
    license_class = "UNKNOWN"

  # 4d. Ecosystem Alignment
  ecosystem_match = alternative.name IN tech_stack.existing_dependencies
                    OR alternative.ecosystem == tech_stack.framework
  # Prefer: zod plugin over standalone if project uses zod

  # 4e. Feature & API Evaluation
  api_surface_match = HIGH | MEDIUM | LOW
  feature_coverage = percentage  # what % of custom module features covered
  migration_effort = S | M | L   # S=<4h, M=4-16h, L=>16h

  # 4f. Confidence Assignment
  # HIGH: >10k stars, active (commit <6mo), >90% coverage,
  #       PERMISSIVE license, CLEAN security, ecosystem_match preferred
  # MEDIUM: >1k stars, maintained (commit <1yr), >70% coverage,
  #         PERMISSIVE license, no unpatched CRITICAL CVEs
  # LOW: <1k stars OR unmaintained OR <70% coverage
  #      OR COPYLEFT_INCOMPATIBLE OR VULNERABLE
```

### Phase 5: Write Report + Migration Plan

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/templates/audit_worker_report_template.md`.

Write JSON summary per `shared/references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Build report in memory, write to `{output_dir}/645-open-source-replacer[-{domain}].md`.

```markdown
# Open Source Replacement Audit Report

<!-- AUDIT-META
worker: ln-645
category: Open Source Replacement
domain: {domain_name|global}
scan_path: {scan_path|.}
score: {X.X}
total_issues: {N}
critical: 0
high: {N}
medium: {N}
low: {N}
status: completed
-->

## Checks

| ID | Check | Status | Details |
|----|-------|--------|---------|
| module_discovery | Module Discovery | passed/warning | Found N modules >= 100 LOC |
| classification | Pre-Classification | passed | N utility, M integration, K domain-specific (excluded) |
| goal_extraction | Goal Extraction | passed/warning | Extracted goals for N/M modules |
| alternative_search | Alternative Search | passed/warning | Found alternatives for N modules |
| security_gate | Security Gate | passed/warning | N candidates checked, M clean, K vulnerable |
| evaluation | Replacement Evaluation | passed/failed | N HIGH confidence, M MEDIUM |
| migration_plan | Migration Plan | passed/skipped | Generated for N replacements |

## Findings

| Severity | Location | Issue | Principle | Recommendation | Effort |
|----------|----------|-------|-----------|----------------|--------|
| HIGH | src/utils/email-validator.ts (245 LOC) | Custom email validation with MX checking | Reuse / OSS Available | Replace with zod + zod-email (28k stars, MIT, 95% coverage) | M |

## Migration Plan

| Priority | Module | Lines | Replacement | Confidence | Effort | Steps |
|----------|--------|-------|-------------|------------|--------|-------|
| 1 | src/utils/email-validator.ts | 245 | zod + zod-email | HIGH | M | 1. Install 2. Create schema 3. Replace calls 4. Remove module 5. Test |

<!-- DATA-EXTENDED
{
  "modules_scanned": 15,
  "modules_with_alternatives": 8,
  "reuse_opportunity_score": 6.5,
  "replacements": [
    {
      "module": "src/utils/email-validator.ts",
      "lines": 245,
      "classification": "utility",
      "goal": "Email validation with MX checking",
      "alternative": "zod + zod-email",
      "confidence": "HIGH",
      "stars": 28000,
      "last_commit": "2026-02-10",
      "license": "MIT",
      "license_class": "PERMISSIVE",
      "security_status": "CLEAN",
      "ecosystem_match": true,
      "feature_coverage": 95,
      "effort": "M",
      "migration_steps": ["Install zod + zod-email", "Create validation schema", "Replace validate() calls", "Remove custom module", "Run tests"]
    }
  ],
  "no_replacement_found": [
    {"module": "src/lib/domain-scorer.ts", "reason": "Domain-specific business logic", "classification": "domain-specific"}
  ]
}
-->
```

### Phase 6: Return Summary

```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/645-open-source-replacer[-{domain}].md
Score: X.X/10 | Issues: N (C:0 H:N M:N L:N)
```

## Scoring

Uses standard penalty formula from `shared/references/audit_scoring.md`:

```
penalty = (critical x 2.0) + (high x 1.0) + (medium x 0.5) + (low x 0.2)
score = max(0, 10 - penalty)
```

Severity mapping:
- **HIGH:** HIGH confidence replacement for module >200 LOC
- **MEDIUM:** MEDIUM confidence, or HIGH confidence for 100-200 LOC
- **LOW:** LOW confidence (partial coverage only)
- **Exception:** Custom module with domain-specific logic not covered by OSS package -> skip. Feature parity <80% -> skip recommendation. **Layer 2:** Verify replacement has full feature parity before recommending

## Critical Rules

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- **Goal-based, not pattern-based:** Read code to understand PURPOSE before searching alternatives
- **MCP Research mandatory:** Always search via WebSearch/Context7/Ref, never assume packages exist
- **Security gate mandatory:** WebSearch for CVEs before recommending any package; never recommend packages with unpatched HIGH/CRITICAL CVEs
- **License classification mandatory:** Permissive (MIT/Apache/BSD) preferred; copyleft only if project-compatible
- **Ecosystem alignment:** Prefer packages from project's existing dependency tree (e.g., zod plugin over standalone if project uses zod)
- **Pre-classification gate:** Categorize modules before analysis; exclude domain-specific business logic
- **No auto-fix:** Report only, never install packages or modify code
- **Effort realism:** S = <4h, M = 4-16h, L = >16h (migration effort is larger than simple fixes)
- **Cap analysis:** Max 15 modules per invocation to stay within token budget
- **Evidence always:** Include file paths + line counts for every finding

## Definition of Done

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- [ ] Custom modules discovered (>= 100 LOC, utility/integration type)
- [ ] Pre-classification gate applied: domain-specific modules excluded with documented reason
- [ ] Goals extracted for each module (domain, inputs, outputs, operations)
- [ ] Open-source alternatives searched via MCP Research (WebSearch, Context7, Ref)
- [ ] Security gate passed: all candidates checked for CVEs via WebSearch
- [ ] License classified: Permissive/Copyleft/Unknown for each candidate
- [ ] Ecosystem alignment checked: existing project dependencies considered
- [ ] Confidence scored for each replacement (HIGH/MEDIUM/LOW)
- [ ] Migration plan generated for HIGH/MEDIUM confidence replacements
- [ ] Report written to `{output_dir}/645-open-source-replacer[-{domain}].md`
- [ ] Summary written per contract

## Reference Files

- **Scoring algorithm:** `shared/references/audit_scoring.md`
- **MANDATORY READ:** `shared/references/research_tool_fallback.md`

---
**Version:** 1.0.0
**Last Updated:** 2026-02-26
