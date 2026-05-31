---
name: ln-625-dependency-reuse-auditor
description: "Checks dependency health and generic custom utility/integration replacement opportunities. Use when auditing dependency and reuse risk."
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch, mcp__hex-graph__audit_workspace, mcp__hex-graph__find_references, mcp__hex-line__read_file, mcp__hex-line__grep_search, mcp__hex-line__outline
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

# Dependencies & Reuse Auditor (L3 Worker)

**Type:** L3 Worker

Specialized worker auditing dependency health and reuse risk.

## Purpose & Scope

- Supports `vulnerabilities_only` mode for vulnerability-only runs
- Audit **dependency and reuse risk** (Categories 7+8: Medium Priority)
- Check outdated/unmaintained packages, unused deps, **CVE vulnerabilities**, and generic custom utility/integration modules that should use native/existing/OSS alternatives
- Emit `PATCH_DEPENDENCY`, `REMOVE_DEPENDENCY`, or `REPLACE_CUSTOM_UTILITY`
- Calculate compliance score (X/10)

## Parameters

| Param | Values | Default | Description |
|-------|--------|---------|-------------|
| mode | `full` / `vulnerabilities_only` | `full` | `full` = all 5 checks, `vulnerabilities_only` = only CVE scan |

## Inputs

**MANDATORY READ:** Load `references/audit_worker_core_contract.md`.
Tool policy: follow host AGENTS.md MCP preferences; load `references/mcp_tool_preferences.md` and `references/mcp_integration_patterns.md` only when host policy is absent or MCP behavior is unclear.

Receives `contextStore` with tech stack, package manifest paths, codebase root, output_dir.

Use `mode=full` by default. Use `mode=vulnerabilities_only` when only package vulnerability findings are requested.

Use `hex-graph` first when dependency references or code reuse evidence materially improve the audit. Use `hex-line` first for local code reads when available. If MCP is unavailable, unsupported, or not indexed, continue with built-in `Read/Grep/Glob/Bash` and state the fallback in the report.

## Workflow

Detection policy: use two-layer detection (candidate scan, then context verification); load `references/two_layer_detection.md` only when the verification method is ambiguous.

1) Parse context + mode parameter + output_dir
2) Run dependency checks (Layer 1: audit tools, based on mode)
3) Analyze context per candidate (Layer 2):
   - Available Features: read usage -- is lodash used for 1 function (easy replace) or deeply integrated (hard)?
   - Custom Utility Replacement: read code -- truly generic utility/integration, or domain-specific logic?
   - Vulnerability: read code -- is the vulnerable API actually called in this project?
4) Collect findings
5) Calculate score
6) **Write Report:** Build full markdown report in memory per `references/templates/audit_worker_report_template.md`, write to `{output_dir}/ln-625--global.md` in single Write call
7) **Return Summary:** Return minimal summary

---

## Audit Rules (5 Checks)

### 1. Outdated Packages
**Mode:** full only

**Detection:**
- Run `npm outdated --json` (Node.js)
- Run `pip list --outdated --format=json` (Python)
- Run `cargo outdated --format=json` (Rust)

**Severity:**
- **HIGH:** Major version behind (security risk)
- **MEDIUM:** Minor version behind
- **LOW:** Patch version behind

**Recommendation:** Update to latest version, test for breaking changes

**Effort:** S-M (update version, run tests)

### 2. Unused Dependencies
**Mode:** full only

**Detection:**
- Parse package.json/requirements.txt
- Grep codebase for `import`/`require` statements
- Find dependencies never imported

**Severity:**
- **MEDIUM:** Unused production dependency (bloats bundle)
- **LOW:** Unused dev dependency

**Recommendation:** Remove from package manifest

**Effort:** S (delete line, test)

### 3. Available Features Not Used
**Mode:** full only

**Detection:**
- Check for axios when native fetch available (Node 18+)
- Check for lodash when Array methods sufficient
- Check for moment when Date.toLocaleString sufficient

**Severity:**
- **MEDIUM:** Unnecessary dependency (increases bundle size)

**Recommendation:** Use native alternative

**Effort:** M (refactor code to use native API)

### 4. Generic Custom Utility / Integration Replacement
**Mode:** full only

**Detection:**
- Find significant custom utility/integration files in `utils/`, `lib/`, `helpers/`, `common/`, `shared/`, `pkg/`, `internal/`
- Look for names such as parser, formatter, validator, converter, encoder, serializer, logger, cache, queue, scheduler, mailer, http, client, wrapper, adapter, connector
- Read code to classify purpose before recommending replacement
- Prefer native platform APIs, existing project dependencies, then well-maintained OSS packages

**Severity:**
- **HIGH:** high-confidence replacement for generic module >200 LOC or custom crypto/serialization with safer established alternative
- **MEDIUM:** high-confidence replacement for 100-200 LOC, or medium-confidence replacement with clear maintenance win
- **LOW:** partial replacement opportunity or native API cleanup

**Layer 2:**
- Skip domain-specific business logic
- Skip when feature parity is <80%
- Before recommending OSS, check maintenance, license compatibility, and known security advisories using available research tools

**Recommendation:** Replace with native API, existing dependency feature, or vetted OSS alternative

**Effort:** M (integrate library, replace calls)

### 5. Vulnerability Scan (CVE/CVSS)
**Mode:** full AND vulnerabilities_only

**Detection:**
- Detect ecosystems: npm, NuGet, pip, Go, Bundler, Cargo, Composer
- Run audit commands per `references/vulnerability_commands.md`
- Parse results with CVSS mapping per `references/cvss_severity_mapping.md`

**Severity:**
- **CRITICAL:** CVSS 9.0-10.0 (immediate fix required)
- **HIGH:** CVSS 7.0-8.9 (fix within 48h)
- **MEDIUM:** CVSS 4.0-6.9 (fix within 1 week)
- **LOW:** CVSS 0.1-3.9 (fix when convenient)

**Fix Classification:**
- Patch update (x.x.Y) -> safe auto-fix
- Minor update (x.Y.0) -> usually safe
- Major update (Y.0.0) -> manual review required
- No fix available -> document and monitor

**Recommendation:** Update to fixed version, verify lock file integrity

**Effort:** S-L (depends on breaking changes)

---

## Scoring Algorithm

**MANDATORY READ:** Load `references/audit_scoring.md`.

**Note:** When mode=vulnerabilities_only, score based only on vulnerability findings.

## Output Format

**MANDATORY READ:** Load `references/templates/audit_worker_report_template.md`.

Write JSON summary per `references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/ln-625--global.md` with `category: "Dependency & Reuse Risk"` and checks: outdated_packages, unused_deps, available_natives, custom_utility_replacement, vulnerability_scan.

Return summary per `references/audit_summary_contract.md`.

When `summaryArtifactPath` is absent, write the standalone runtime summary under `.hex-skills/runtime-artifacts/runs/{run_id}/evaluation-worker/{worker}--{identifier}.json` and optionally echo the same summary in structured output.
```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/ln-625--global.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Reference Files

| File | Purpose |
|------|---------|
| `references/vulnerability_commands.md` | Ecosystem-specific audit commands |
| `references/ci_integration_guide.md` | CI/CD integration guidance |
| `references/cvss_severity_mapping.md` | CVSS to severity level mapping |
| `references/audit_output_schema.md` | Audit output schema |

## Critical Rules

Apply the already-loaded `references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report only, never modify package manifests or lock files
- **Mode-aware execution:** In `vulnerabilities_only` mode, skip checks 1-4 entirely
- **Effort realism:** S = <1h, M = 1-4h, L = >4h
- **CVSS-based severity:** Map vulnerability severity strictly via `references/cvss_severity_mapping.md`
- **Exclusions:** Skip devDependencies for vulnerability severity escalation, skip vendored/bundled deps
- **Unique angle:** Audit dependency/package health and generic reuse opportunities only. Do not audit application exploitability, architecture modernization, or domain-specific business logic.
- **Action required:** Every finding uses `PATCH_DEPENDENCY`, `REMOVE_DEPENDENCY`, or `REPLACE_CUSTOM_UTILITY`.

## Definition of Done

Apply the already-loaded `references/audit_worker_core_contract.md`.

- [ ] contextStore parsed (including mode parameter and output_dir)
- [ ] All applicable checks completed (5 for full, 1 for vulnerabilities_only)
- [ ] Generic custom utility/integration candidates classified before replacement recommendations
- [ ] Findings collected with severity, location, effort, action, fix_type, recommendation
- [ ] Score calculated per `references/audit_scoring.md`
- [ ] Report written to `{output_dir}/ln-625--global.md` (atomic single Write call)
- [ ] Summary written per contract

---
**Version:** 4.0.0
**Last Updated:** 2026-02-05
