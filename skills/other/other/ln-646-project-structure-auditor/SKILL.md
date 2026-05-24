---
name: ln-646-project-structure-auditor
description: "Audits physical architecture structure: modules, domains, layer layout, junk drawers, and framework placement. Use for structure drift."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__analyze_architecture, mcp__hex-line__read_file, mcp__hex-line__grep_search, mcp__hex-line__outline
license: MIT
model: claude-haiku-4-5
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

# Project Structure Auditor

**Type:** L3 Worker

L3 Worker that audits whether physical project structure reflects the intended architecture.

## Purpose & Scope

- Audit modules, domains, layer layout, framework placement, and junk drawer directories
- Detect structure drift that makes the architecture hard to navigate or enforce
- Complement code-level boundary checks with physical structure evidence
- Emit `MOVE_MODULE`, `SPLIT_JUNK_DRAWER`, or `ALIGN_DOMAIN_STRUCTURE`
- Calculate compliance score (X/10)

**Out of Scope:**

- `.gitignore`, `.dockerignore`, temp files, build artifacts, platform remnants, and large binaries
- Import-level layer violations
- Package security, env-file hygiene, or runtime lifecycle checks
- Moving/deleting files

## Inputs

**MANDATORY READ:** Load `references/audit_worker_core_contract.md`.
Tool policy: follow host AGENTS.md MCP preferences; load `references/mcp_tool_preferences.md` and `references/mcp_integration_patterns.md` only when host policy is absent or MCP behavior is unclear.

Receives `contextStore` with: `tech_stack`, `architecture`, `codebase_root`, `output_dir`, `domain_mode`, `scan_path`.

Use `hex-graph` first when architecture summaries materially improve structure findings. Use `hex-line` first for local code, config, and manifest reads when available. If MCP is unavailable, unsupported, or not indexed, continue with built-in `Read/Grep/Glob/Bash` and state the fallback in the report.

## Workflow

Detection policy: use two-layer detection (candidate scan, then context verification); load `references/two_layer_detection.md` only when the verification method is ambiguous.

1) **Parse context** -- determine scan_root from domain-aware scope or codebase root
2) **Detect tech stack and intended structure**
   - **MANDATORY READ:** Load `references/stack_detection.md`
   - Prefer explicit architecture docs/config when present; otherwise infer from source layout
3) **Run structure checks (Layer 1)**
   - Framework expected source locations
   - Domain/module grouping
   - Layer directory layout
   - Junk drawer directories
   - Naming and placement consistency
4) **Verify context (Layer 2)**
   - Small projects may not need full domain/layer decomposition
   - Framework conventions apply only to detected frameworks
   - Mixed layouts are acceptable when split by app/package/test type and documented
5) **Collect findings** with severity, location, action, effort, and recommendation
6) **Calculate score** using `references/audit_scoring.md`
7) **Write report** to `{output_dir}/ln-646--{identifier}.md`
8) **Return summary** per `references/audit_summary_contract.md`

## Audit Rules

### 1. Framework Placement

**What:** Source files are placed outside framework or stack conventions

**Detection:** Load `references/structure_rules.md` and apply only rules for the detected stack.

**Severity:** HIGH when placement breaks tooling/routing, MEDIUM for maintainability drift

**Action:** `MOVE_MODULE`

### 2. Domain and Layer Layout

**What:** Domain or layer directories do not reflect the intended architecture

**Detection:**
- Compare documented or inferred domains/layers with physical directories
- Find domains missing expected substructure
- Find source files in root or generic folders when the project has a clear modular layout

**Severity:** MEDIUM by default, HIGH when structure hides critical ownership

**Action:** `ALIGN_DOMAIN_STRUCTURE`

### 3. Junk Drawers

**What:** Generic directories accumulate unrelated modules

**Detection:** Check directories such as `utils`, `helpers`, `common`, `shared`, `services`, and `lib` for mixed unrelated responsibilities above project thresholds.

**Severity:** MEDIUM for broad mixed responsibilities, LOW for small localized drift

**Action:** `SPLIT_JUNK_DRAWER`

## Scoring Algorithm

**MANDATORY READ:** Load `references/audit_scoring.md`.

## Output Format

**MANDATORY READ:** Load `references/templates/audit_worker_report_template.md`.

Write JSON summary per `references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/ln-646--{identifier}.md` with `category: "Project Structure"` and checks: framework_placement, domain_layer_layout, junk_drawers.

When `summaryArtifactPath` is absent, write the standalone runtime summary under `.hex-skills/runtime-artifacts/runs/{run_id}/evaluation-worker/{worker}--{identifier}.json` and optionally echo the same summary in structured output.

## Critical Rules

Apply the already-loaded `references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report only, never move or delete files
- **Unique angle:** Audit physical architecture structure only. Do not audit file hygiene, ignore files, package health, env hygiene, import-level boundaries, or runtime lifecycle.
- **Auto-detect, never assume:** Apply framework rules only for detected stack
- **Evidence always:** Include file paths for every finding
- **Action required:** Every finding uses `MOVE_MODULE`, `SPLIT_JUNK_DRAWER`, or `ALIGN_DOMAIN_STRUCTURE`.

## Definition of Done

Apply the already-loaded `references/audit_worker_core_contract.md`.

- [ ] contextStore parsed successfully
- [ ] scan_root determined
- [ ] Tech stack and intended structure detected
- [ ] Framework placement checked
- [ ] Domain/layer layout checked
- [ ] Junk drawer directories checked
- [ ] Layer 2 context verification applied
- [ ] Findings collected with severity, location, action, effort, recommendation
- [ ] Score calculated per `references/audit_scoring.md`
- [ ] Report written to `{output_dir}/ln-646--{identifier}.md` (atomic single Write call)
- [ ] Summary written per contract

---
**Version:** 1.0.0
**Last Updated:** 2026-03-15
