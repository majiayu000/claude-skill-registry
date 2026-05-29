---
name: ln-647-configuration-boundary-auditor
description: "Audits architecture config boundaries: typed settings, scattered env reads, config leakage, and layer ownership. Use for config architecture."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__find_symbols, mcp__hex-graph__find_references, mcp__hex-line__read_file, mcp__hex-line__grep_search, mcp__hex-line__outline
license: MIT
model: claude-haiku-4-5
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

# Configuration Boundary Auditor

**Type:** L3 Worker

Specialized worker auditing whether configuration access has a clear architectural boundary.

## Purpose & Scope

- Audit typed settings boundaries, scattered env reads, config leakage across layers, and configuration ownership
- Identify architecture problems where code reads raw environment/config directly instead of depending on a settings contract
- Emit `ADD_SETTINGS_BOUNDARY`, `STOP_SCATTERED_ENV_READS`, or `TYPE_CONFIG_CONTRACT`
- Calculate compliance score (X/10)

**Out of Scope:**

- `.env` inventory, `.env.example` completeness, committed env files, or secrets hygiene
- Package security, build gates, runtime startup validation, and lifecycle readiness
- Generating env files or modifying configuration

## Inputs

**MANDATORY READ:** Load `references/audit_worker_core_contract.md`.
Tool policy: follow host AGENTS.md MCP preferences; load `references/mcp_tool_preferences.md` and `references/mcp_integration_patterns.md` only when host policy is absent or MCP behavior is unclear.

Receives `contextStore` with tech stack, codebase root, output_dir, domain_mode, scan_path.

Use `hex-graph` first when symbol or reference analysis materially improves config-boundary findings. Use `hex-line` first for local code/config reads when available. If MCP is unavailable, unsupported, or not indexed, continue with built-in `Read/Grep/Glob/Bash` and state the fallback in the report.

## Workflow

Detection policy: use two-layer detection (candidate scan, then context verification); load `references/two_layer_detection.md` only when the verification method is ambiguous.

1) **Parse context** -- determine scan_root from domain-aware scope or codebase root
2) **Detect config access (Layer 1)**
   - Raw env reads in application/domain/service layers
   - Multiple settings/config classes for the same concern
   - Untyped config dictionaries passed through service boundaries
   - Config values read inside deep leaf functions instead of at composition/bootstrap boundary
3) **Verify architecture context (Layer 2)**
   - Framework-managed config access at bootstrap -> skip
   - Test-only env reads -> skip
   - Small script/CLI with no layered architecture -> downgrade or skip
   - Typed settings object passed through boundaries -> skip
4) **Collect findings** with severity, location, action, effort, and recommendation
5) **Calculate score** using `references/audit_scoring.md`
6) **Write report** to `{output_dir}/ln-647--{identifier}.md`
7) **Return summary** per `references/audit_summary_contract.md`

## Audit Rules

### 1. Scattered Env Reads

**What:** Raw environment/config reads appear across multiple architectural layers

**Detection:**
- JavaScript/TypeScript: `process.env`
- Python: `os.getenv`, `os.environ`
- Go: `os.Getenv`
- .NET/Java: direct environment/config access outside bootstrap/settings modules

**Severity:** HIGH when domain/business logic reads env directly, MEDIUM in services, LOW in adapters

**Action:** `STOP_SCATTERED_ENV_READS`

### 2. Missing Typed Settings Boundary

**What:** Configuration is passed as raw dictionaries, strings, or primitives without a typed settings contract

**Detection:**
- Raw `dict`, `Record<string, string>`, `Map<String,String>`, or untyped config objects in service constructors
- Repeated primitive config parameters across services
- Missing settings/schema object despite many config reads

**Severity:** MEDIUM by default, HIGH when security or persistence behavior depends on untyped config

**Action:** `TYPE_CONFIG_CONTRACT`

### 3. Config Ownership Leakage

**What:** Lower layers decide deployment/runtime configuration instead of receiving explicit settings from the composition boundary

**Detection:**
- Repositories, domain services, or utility modules loading env/config directly
- Multiple modules constructing their own config readers
- Feature behavior branching on deployment config deep in domain logic

**Severity:** HIGH for domain/persistence ownership leakage, MEDIUM for service-layer leakage

**Action:** `ADD_SETTINGS_BOUNDARY`

## Scoring Algorithm

**MANDATORY READ:** Load `references/audit_scoring.md`.

## Output Format

**MANDATORY READ:** Load `references/audit_output_schema.md`.
**MANDATORY READ:** Load `references/templates/audit_worker_report_template.md`.

Write JSON summary per `references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/ln-647--{identifier}.md` with `category: "Configuration Boundary"` and checks: scattered_env_reads, typed_settings_boundary, config_ownership_leakage.

When `summaryArtifactPath` is absent, write the standalone runtime summary under `.hex-skills/runtime-artifacts/runs/{run_id}/evaluation-worker/{worker}--{identifier}.json` and optionally echo the same summary in structured output.

## Critical Rules

Apply the already-loaded `references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report only, never modify config or code
- **Unique angle:** Audit configuration architecture boundaries only. Do not audit `.env` hygiene, committed secrets, startup validation, package health, or lifecycle readiness.
- **Layer 2 mandatory:** No raw env read is a finding until its architectural layer and purpose are verified.
- **Action required:** Every finding uses `ADD_SETTINGS_BOUNDARY`, `STOP_SCATTERED_ENV_READS`, or `TYPE_CONFIG_CONTRACT`.

## Definition of Done

Apply the already-loaded `references/audit_worker_core_contract.md`.

- [ ] contextStore parsed successfully
- [ ] scan_root determined
- [ ] Scattered env reads checked
- [ ] Typed settings boundary checked
- [ ] Config ownership leakage checked
- [ ] Layer 2 context verification applied
- [ ] Findings collected with severity, location, action, effort, recommendation
- [ ] Score calculated per `references/audit_scoring.md`
- [ ] Report written to `{output_dir}/ln-647--{identifier}.md` (atomic single Write call)
- [ ] Summary written per contract

---
**Version:** 1.0.0
**Last Updated:** 2026-03-15
