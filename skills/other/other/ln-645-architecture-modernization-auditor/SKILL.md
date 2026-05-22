---
name: ln-645-architecture-modernization-auditor
description: "Finds architecture-level modernization opportunities: obsolete custom mechanisms, overbuilt extension points, and simplifiable architecture. Use when auditing architecture evolution."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__find_references, mcp__hex-graph__analyze_architecture, mcp__hex-line__read_file, mcp__hex-line__grep_search, mcp__hex-line__outline
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

# Architecture Modernization Auditor

**Type:** L3 Worker

L3 Worker that finds architecture-level simplification and modernization opportunities.

## Purpose & Scope

- Audit obsolete custom architectural mechanisms, overbuilt extension points, and avoidable architecture indirection
- Identify mechanisms that increase maintenance cost without current architectural value
- Generate migration-safe modernization findings
- Emit `SIMPLIFY_ARCHITECTURE`, `RETIRE_CUSTOM_MECHANISM`, or `CONSOLIDATE_EXTENSION_POINT`
- Calculate compliance score (X/10)

## Inputs

**MANDATORY READ:** Load `references/audit_worker_core_contract.md`.
Tool policy: follow host AGENTS.md MCP preferences; load `references/mcp_tool_preferences.md` and `references/mcp_integration_patterns.md` only when host policy is absent or MCP behavior is unclear.

Receives `contextStore` with: `tech_stack`, `architecture`, `codebase_root`, `output_dir`, `domain_mode`, `scan_path`.

Use `hex-graph` first when references, architecture metrics, or implementation relationships materially improve modernization findings. Use `hex-line` first for local code reads when available. If MCP is unavailable, unsupported, or not indexed, continue with built-in `Read/Grep/Glob/Bash` and state the fallback in the report.

## Workflow

Detection policy: use two-layer detection (candidate scan, then context verification); load `references/two_layer_detection.md` only when the verification method is ambiguous.

1) **Parse context** -- determine scan_root from domain-aware scope or codebase root
2) **Find modernization candidates (Layer 1)**
   - Custom plugin/extension systems with one implementation
   - Hand-built service locators, registries, dispatchers, buses, adapters, or factories with limited use
   - Legacy architecture mechanisms with deprecation comments or unused compatibility branches
   - Parallel architectural mechanisms solving the same problem
3) **Verify architectural value (Layer 2)**
   - Is the mechanism required by the framework or deployment model? -> skip
   - Is it a public extension API with external consumers? -> downgrade or skip
   - Does it isolate a volatile boundary with multiple real implementations? -> skip
   - Is the replacement only a package swap or utility rewrite? -> skip
4) **Collect findings** with severity, location, action, effort, migration risk, and recommendation
5) **Calculate score** using `references/audit_scoring.md`
6) **Write report** to `{output_dir}/ln-645--{identifier}.md`
7) **Return summary** per `references/audit_summary_contract.md`

## Audit Rules

### 1. Obsolete Custom Mechanisms

**What:** Custom architecture mechanisms kept after the project no longer needs them

**Detection:**
- Search for `Legacy`, `Compat`, `Shim`, `Adapter`, `Registry`, `Plugin`, `Extension`, `ServiceLocator`, `Dispatcher`, `EventBus`
- Check references and implementation count
- Read deprecation/TODO comments and ADRs when present

**Severity:** HIGH for critical-path mechanisms, MEDIUM for broad but non-critical mechanisms, LOW for isolated cleanup

**Action:** `RETIRE_CUSTOM_MECHANISM`

### 2. Overbuilt Extension Points

**What:** Extension or plugin architecture with one implementation and no active variation point

**Detection:**
- Interfaces/abstract classes used only by one implementation
- Factories or registries with one registered type
- Configuration-driven plugin loading with one hardcoded plugin

**Severity:** MEDIUM by default, HIGH when the indirection hides critical flow

**Action:** `CONSOLIDATE_EXTENSION_POINT`

### 3. Parallel Architectural Mechanisms

**What:** Two or more architecture mechanisms solve the same problem in different modules

**Detection:**
- Multiple dispatch/registry/event mechanisms
- Multiple service composition styles
- Multiple adapter conventions for the same boundary

**Severity:** HIGH when it creates inconsistent behavior, MEDIUM when it mainly increases maintenance cost

**Action:** `SIMPLIFY_ARCHITECTURE`

## Scoring Algorithm

**MANDATORY READ:** Load `references/audit_scoring.md`.

## Output Format

**MANDATORY READ:** Load `references/templates/audit_worker_report_template.md`.

Write JSON summary per `references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/ln-645--{identifier}.md` with `category: "Architecture Modernization"` and checks: obsolete_mechanisms, overbuilt_extension_points, parallel_mechanisms.

When `summaryArtifactPath` is absent, write the standalone runtime summary under `.hex-skills/runtime-artifacts/runs/{run_id}/evaluation-worker/{worker}--{identifier}.json` and optionally echo the same summary in structured output.

## Critical Rules

Apply the already-loaded `references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report only, never rewrite architecture
- **Unique angle:** Audit architecture-level modernization only. Do not audit package health, CVEs, generic utility replacement, code complexity, or runtime configuration hygiene.
- **No package recommendations:** Do not search for OSS replacements or recommend dependency swaps.
- **Evidence required:** Every modernization finding must include implementation count, reference evidence, and migration risk.
- **Action required:** Every finding uses `SIMPLIFY_ARCHITECTURE`, `RETIRE_CUSTOM_MECHANISM`, or `CONSOLIDATE_EXTENSION_POINT`.

## Definition of Done

Apply the already-loaded `references/audit_worker_core_contract.md`.

- [ ] contextStore parsed successfully
- [ ] scan_root determined
- [ ] obsolete custom mechanisms checked
- [ ] overbuilt extension points checked
- [ ] parallel architectural mechanisms checked
- [ ] Layer 2 architectural value verification applied
- [ ] Findings collected with severity, location, action, effort, migration risk, and recommendation
- [ ] Score calculated per `references/audit_scoring.md`
- [ ] Report written to `{output_dir}/ln-645--{identifier}.md` (atomic single Write call)
- [ ] Summary written per contract

---
**Version:** 1.0.0
**Last Updated:** 2026-02-26
