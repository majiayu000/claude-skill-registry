---
name: ln-832-bundle-optimizer
description: "Reduces JS/TS bundle size via tree-shaking, code splitting, and unused dependency removal. Use when optimizing frontend bundle size."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__audit_workspace
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-832-bundle-optimizer

**Type:** L3 Worker
**Category:** 8XX Optimization

Reduces JavaScript or TypeScript bundle size using keep/discard verification. JS/TS projects only.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | JS/TS project path plus optional optimization scope |
| **Output** | Smaller bundle plus a machine-readable modernization summary |
| **Scope** | JS/TS only |

---

## Workflow

**Phases:** Pre-flight -> Baseline -> Analyze -> Optimize Loop -> Report

---

## Phase 0: Pre-flight Checks

| Check | Required | Action if Missing |
|-------|----------|-------------------|
| `package.json` exists | Yes | Block optimization |
| Build command available | Yes | Block optimization |
| Output directory (`dist/` or `build/`) detectable | Yes | Build once to establish baseline |
| Workspace baseline safe | Yes | In managed runs coordinator already prepared it; in standalone runs protect rollback locally |

**MANDATORY READ:** Load `shared/references/ci_tool_detection.md` for build detection.

### Runtime Coordination

Managed runs receive deterministic `runId` and exact `summaryArtifactPath` from `ln-830`.
Standalone runs remain supported; if runtime arguments are omitted, generate a standalone run-scoped artifact before returning.

---

## Phase 1: Establish Baseline

```text
1. Run the detected build command.
2. Measure total size of the output directory.
3. Record baseline bytes and per-chunk sizes.
```

| Metric | How |
|--------|-----|
| Total size | Sum all bundle output files except source maps |
| Per-chunk sizes | Measure individual JS and CSS files |
| Source map handling | Exclude `.map` files |

---

## Phase 2: Analyze Opportunities

| Check | Tool | What It Finds |
|-------|------|---------------|
| Unused dependencies | `depcheck` or equivalent | Packages not imported anywhere |
| Bundle composition | Bundle analyzer | Large dependencies or duplicates |
| Tree-shaking gaps | Manual scan | Namespace imports or heavy entrypoints |
| Code splitting gaps | Route analysis | Lazy-load candidates |

Optimization categories:

| Category | Example | Typical Savings |
|----------|---------|----------------|
| Remove unused deps | dead dependencies | 10-50KB per package |
| Named imports | `lodash-es` named imports | 50-200KB |
| Lighter alternatives | replace heavy date or utility libs | 50-300KB |
| Dynamic imports | lazy-load heavy components | lower initial bundle |
| CSS optimization | remove unused CSS, minify | 10-100KB |

---

## Phase 3: Optimize Loop (Keep/Discard)

Per-optimization cycle:

```text
FOR each optimization:
  1. APPLY the change
  2. BUILD
     IF build fails -> DISCARD and revert
  3. MEASURE new bundle size
  4. KEEP only if the bundle is smaller than the current baseline
  5. LOG the result
```

Stop conditions:

| Condition | Action |
|-----------|--------|
| All optimizations processed | Stop and report |
| 3 consecutive discards | Stop for plateau |
| Build infrastructure breaks | Revert to last keep and stop |
| Bundle already below target | Stop and report |

Optimization order:
1. remove unused dependencies
2. improve tree-shaking and imports
3. replace heavy libraries
4. introduce code splitting
5. optimize CSS

---

## Phase 4: Report Results

| Field | Description |
|-------|-------------|
| `project` | Project path |
| `baseline_bytes` | Original bundle size |
| `final_bytes` | Final bundle size |
| `reduction_bytes` | Bytes saved |
| `reduction_percent` | Percentage reduction |
| `optimizations_applied` | Count of kept optimizations |
| `optimizations_discarded` | Count plus reasons |
| `deps_removed[]` | Dependencies removed |
| `details[]` | Per-optimization savings |
| `artifact_path` | Durable worker report path, if written |

---

## Configuration

```yaml
Options:
  build_command: ""             # Auto-detect
  output_dir: ""                # Auto-detect
  run_depcheck: true
  run_bundle_analyzer: false
  remove_unused_deps: true
  fix_tree_shaking: true
  replace_heavy_libraries: true
  enable_code_splitting: true
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Build fails after optimization | Invalid code or config change | Revert that optimization |
| No size reduction | Optimization ineffective | Discard it |
| Analyzer unavailable | Tooling missing | Continue with manual inspection |

---

## References

- [optimization_categories.md](references/optimization_categories.md)
- `shared/references/ci_tool_detection.md`

---

## Runtime Summary Artifact

**MANDATORY READ:** Load `shared/references/coordinator_summary_contract.md`

Emit a `modernization-worker` summary envelope.

Managed mode:
- `ln-830` passes deterministic `runId` and exact `summaryArtifactPath`
- write the summary to the provided `summaryArtifactPath`

Standalone mode:
- omit `runId` and `summaryArtifactPath`
- write `.hex-skills/runtime-artifacts/runs/{run_id}/modernization-worker/ln-832--{identifier}.json`

## Definition of Done

- [ ] Baseline bundle size established from real build output
- [ ] Optimization opportunities analyzed from bundle composition and project usage
- [ ] Each optimization evaluated with keep/discard verification
- [ ] Only size-reducing optimizations kept
- [ ] Final report captures bundle delta, discarded attempts, and removed dependencies
- [ ] `modernization-worker` summary artifact written to the managed or standalone path

---

**Version:** 1.0.0
**Last Updated:** 2026-03-08
