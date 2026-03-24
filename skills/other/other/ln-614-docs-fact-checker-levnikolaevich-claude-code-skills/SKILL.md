---
name: ln-614-docs-fact-checker
description: "Verifies claims in .md files (paths, versions, counts, configs, endpoints) against codebase, cross-checks contradictions. Use when auditing docs accuracy."
allowed-tools: Read, Grep, Glob, Bash
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Documentation Fact-Checker (L3 Worker)

Specialized worker that extracts verifiable claims from documentation and validates each against the actual codebase.

## Purpose & Scope

- **Worker in ln-610 coordinator pipeline** - invoked by ln-610-docs-auditor
- Extract **all verifiable claims** from ALL `.md` files in project
- Verify each claim against codebase (Grep/Glob/Read/Bash)
- Detect **cross-document contradictions** (same fact stated differently)
- Includes `docs/reference/`, `docs/tasks/`, `tests/` in scope
- Single invocation (not per-document) — cross-doc checks require global view
- Does NOT check scope alignment or structural quality

## Inputs (from Coordinator)

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

Receives `contextStore` with: `tech_stack`, `project_root`, `output_dir`.

## Workflow

### Phase 1: Parse Context

Extract tech stack, project root, output_dir from contextStore.

### Phase 2: Discover Documents

Glob ALL `.md` files in project. Exclude:
- `node_modules/`, `.git/`, `dist/`, `build/`
- `docs/project/.audit/` (audit output, not project docs)
- `CHANGELOG.md` (historical by design)

### Phase 3: Extract Claims (Layer 1)

**MANDATORY READ:** Load `shared/references/two_layer_detection.md` for detection methodology.

For each document, extract verifiable claims using Grep/regex patterns.

**MANDATORY READ:** Load [references/claim_extraction_rules.md](references/claim_extraction_rules.md) for detailed extraction patterns per claim type.

9 claim types:

| # | Claim Type | What to Extract | Extraction Pattern |
|---|-----------|-----------------|-------------------|
| 1 | **File paths** | Paths to source files, dirs, configs | Backtick paths, link targets matching `src/`, `lib/`, `app/`, `docs/`, `config/`, `tests/` |
| 2 | **Versions** | Package/tool/image versions | Semver patterns near dependency/package/image names |
| 3 | **Counts/Statistics** | Numeric claims about codebase | `\d+ (modules|formats|endpoints|services|tables|parsers|files|workers)` |
| 4 | **API endpoints** | HTTP method + path | `(GET|POST|PUT|DELETE|PATCH) /[\w/{}:]+` |
| 5 | **Config keys/env vars** | Environment variables, config keys | `[A-Z][A-Z_]{2,}` in config context, `process.env.`, `os.environ` |
| 6 | **CLI commands** | Shell commands | `npm run`, `python`, `docker`, `make` in backtick blocks |
| 7 | **Function/class names** | Code entity references | CamelCase/snake_case in backticks or code context |
| 8 | **Line number refs** | file:line patterns | `[\w/.]+:\d+` patterns |
| 9 | **Docker/infra claims** | Image tags, ports, service names | Image names with tags, port mappings in docker context |

Output per claim: `{doc_path, line, claim_type, claim_value, raw_context}`.

### Phase 4: Verify Claims (Layer 2)

For each extracted claim, verify against codebase:

| Claim Type | Verification Method | Finding Type |
|------------|-------------------|--------------|
| File paths | Glob or `ls` for existence | PATH_NOT_FOUND |
| Versions | Grep package files (package.json, requirements.txt, docker-compose.yml), compare | VERSION_MISMATCH |
| Counts | Glob/Grep to count actual entities, compare with claimed number | COUNT_MISMATCH |
| API endpoints | Grep route/controller definitions | ENDPOINT_NOT_FOUND |
| Config keys | Grep in source for actual usage | CONFIG_NOT_FOUND |
| CLI commands | Check package.json scripts, Makefile targets, binary existence | COMMAND_NOT_FOUND |
| Function/class | Grep in source for definition | ENTITY_NOT_FOUND |
| Line numbers | Read file at line, check content matches claimed context | LINE_MISMATCH |
| Docker/infra | Grep docker-compose.yml for image tags, ports | INFRA_MISMATCH |

**False positive filtering (Layer 2 reasoning):**
- Template placeholders (`{placeholder}`, `YOUR_*`, `<project>`, `xxx`) — skip
- Example/hypothetical paths (preceded by "e.g.", "for example", "such as") — skip
- Future-tense claims ("will add", "planned", "TODO") — skip or LOW
- Conditional claims ("if using X, configure Y") — verify only if X detected in tech_stack
- External service paths (URLs, external repos) — skip
- Paths in SCOPE/comment HTML blocks describing other projects — skip
- `.env.example` values — skip (expected to differ from actual)

### Phase 5: Cross-Document Consistency

Compare extracted claims across documents to find contradictions:

| Check | Method | Finding Type |
|-------|--------|--------------|
| Same path, different locations | Group file path claims, check if all point to same real path | CROSS_DOC_PATH_CONFLICT |
| Same entity, different version | Group version claims by entity name, compare values | CROSS_DOC_VERSION_CONFLICT |
| Same metric, different count | Group count claims by subject, compare values | CROSS_DOC_COUNT_CONFLICT |
| Endpoint in spec but not in guide | Compare endpoint claims across api_spec.md vs guides/runbook | CROSS_DOC_ENDPOINT_GAP |

Algorithm:
```
claim_index = {}  # key: normalized(claim_type + entity), value: [{doc, line, value}]
FOR claim IN all_verified_claims WHERE claim.verified == true:
  key = normalize(claim.claim_type, claim.entity_name)
  claim_index[key].append({doc: claim.doc_path, line: claim.line, value: claim.claim_value})

FOR key, entries IN claim_index:
  unique_values = set(entry.value for entry in entries)
  IF len(unique_values) > 1:
    CREATE finding(type=CROSS_DOC_*_CONFLICT, severity=HIGH,
      location=entries[0].doc + ":" + entries[0].line,
      issue="'" + key + "' stated as '" + val1 + "' in " + doc1 + " but '" + val2 + "' in " + doc2)
```

### Phase 6: Score & Report

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/references/audit_scoring.md`.

Calculate score using penalty formula. Write report.

## Audit Categories (for Checks table)

| ID | Check | What It Covers |
|----|-------|---------------|
| `path_claims` | File/Directory Paths | All path references verified against filesystem |
| `version_claims` | Version Numbers | Package, tool, image versions against manifests |
| `count_claims` | Counts & Statistics | Numeric assertions against actual counts |
| `endpoint_claims` | API Endpoints | Route definitions against controllers/routers |
| `config_claims` | Config & Env Vars | Environment variables, config keys against source |
| `command_claims` | CLI Commands | Scripts, commands against package.json/Makefile |
| `entity_claims` | Code Entity Names | Functions, classes against source definitions |
| `line_ref_claims` | Line Number References | file:line against actual file content |
| `cross_doc` | Cross-Document Consistency | Same facts across documents agree |

## Severity Mapping

| Issue Type | Severity | Rationale |
|------------|----------|-----------|
| PATH_NOT_FOUND (critical file: CLAUDE.md, runbook, api_spec) | CRITICAL | Setup/onboarding fails |
| PATH_NOT_FOUND (other docs) | HIGH | Misleading reference |
| VERSION_MISMATCH (major version) | HIGH | Fundamentally wrong |
| VERSION_MISMATCH (minor/patch) | MEDIUM | Cosmetic drift |
| COUNT_MISMATCH | MEDIUM | Misleading metric |
| ENDPOINT_NOT_FOUND | HIGH | API consumers affected |
| CONFIG_NOT_FOUND | HIGH | Deployment breaks |
| COMMAND_NOT_FOUND | HIGH | Setup/CI breaks |
| ENTITY_NOT_FOUND | MEDIUM | Confusion |
| LINE_MISMATCH | LOW | Minor inaccuracy |
| INFRA_MISMATCH | HIGH | Docker/deployment affected |
| CROSS_DOC_*_CONFLICT | HIGH | Trust erosion, contradictory docs |

## Output Format

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/templates/audit_worker_report_template.md`.

Write report to `{output_dir}/614-fact-checker.md` with `category: "Fact Accuracy"` and checks: path_claims, version_claims, count_claims, endpoint_claims, config_claims, command_claims, entity_claims, line_ref_claims, cross_doc.

Return summary to coordinator:
```
Report written: docs/project/.audit/ln-610/{YYYY-MM-DD}/614-fact-checker.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Critical Rules

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report violations only; coordinator aggregates for user
- **Code is truth:** When docs contradict code, document is wrong (unless code is a bug)
- **Evidence required:** Every finding includes verification command used and result
- **No false positives:** Better to miss an issue than report incorrectly. When uncertain, classify as LOW with note
- **Location precision:** Always include `file:line` for programmatic navigation
- **Broad scope:** Scan ALL .md files — do not skip docs/reference/, tests/, or task docs
- **Cross-doc matters:** Contradictions between documents erode trust more than single-doc errors
- **Batch efficiently:** Extract all claims first, then verify in batches by type (all paths together, all versions together)

## Definition of Done

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- [ ] contextStore parsed successfully (including output_dir)
- [ ] All `.md` files discovered (broad scope)
- [ ] Claims extracted across 9 types
- [ ] Each claim verified against codebase with evidence
- [ ] Cross-document consistency checked
- [ ] False positives filtered via Layer 2 reasoning
- [ ] Score calculated using penalty algorithm
- [ ] Report written to `{output_dir}/614-fact-checker.md` (atomic single Write call)
- [ ] Summary returned to coordinator

## Reference Files

- **Audit output schema:** `shared/references/audit_output_schema.md`
- **Detection methodology:** `shared/references/two_layer_detection.md`
- Claim extraction rules: [references/claim_extraction_rules.md](references/claim_extraction_rules.md)

---
**Version:** 1.0.0
**Last Updated:** 2026-03-06
