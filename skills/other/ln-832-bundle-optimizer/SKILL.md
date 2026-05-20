---
name: ln-832-bundle-optimizer
description: "Reduces JS/TS bundle size via tree-shaking, code splitting, and unused dependency removal. Use when optimizing frontend bundle size."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/{path}`.

# ln-832-bundle-optimizer

**Type:** L3 Worker
**Category:** 8XX Optimization
**Parent:** ln-830-code-modernization-coordinator

Reduces JavaScript/TypeScript bundle size. Metric: bundle size in bytes. Each optimization verified via build with keep/discard pattern. JS/TS projects only.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | JS/TS project (auto-detect from package.json) |
| **Output** | Smaller bundle, optimization report |
| **Scope** | JS/TS only (skip for other stacks) |

---

## Workflow

**Phases:** Pre-flight → Baseline → Analyze → Optimize Loop → Report

---

## Phase 0: Pre-flight Checks

| Check | Required | Action if Missing |
|-------|----------|-------------------|
| package.json exists | Yes | Block (not a JS/TS project) |
| Build command available | Yes | Block (need build for size measurement) |
| dist/ or build/ output | Yes | Run build first to establish baseline |
| Git clean state | Yes | Block (need clean baseline for revert) |

**MANDATORY READ:** Load `shared/references/ci_tool_detection.md` — use Build section for build command detection.

### Worktree & Branch Isolation

**MANDATORY READ:** Load `shared/references/git_worktree_fallback.md` — use ln-832 row.

---

## Phase 1: Establish Baseline

### Measure Current Bundle Size

```
1. Run build: npm run build (or detected build command)
2. Measure: total size of dist/ or build/ directory
3. Record: baseline_bytes, baseline_files
```

| Metric | How |
|--------|-----|
| Total size | Sum of all files in output directory |
| Per-chunk sizes | Individual JS/CSS file sizes |
| Source map excluded | Do not count .map files |

---

## Phase 2: Analyze Opportunities

### Analysis Tools

| Check | Tool | What It Finds |
|-------|------|--------------|
| Unused dependencies | `npx depcheck` | Packages in package.json not imported anywhere |
| Bundle composition | `npx vite-bundle-visualizer` or `webpack-bundle-analyzer` | Large dependencies, duplicates |
| Tree-shaking gaps | Manual scan | `import * as` instead of named imports |
| Code splitting | Route analysis | Large initial bundle, lazy-loadable routes |

### Optimization Categories

| Category | Example | Typical Savings |
|----------|---------|----------------|
| Remove unused deps | `lodash` installed but not imported | 10-50KB per dep |
| Named imports | `import { debounce } from 'lodash-es'` vs `import _ from 'lodash'` | 50-200KB |
| Lighter alternatives | `date-fns` instead of `moment` | 50-300KB |
| Dynamic imports | `React.lazy(() => import('./HeavyComponent'))` | Reduce initial load |
| CSS optimization | Purge unused CSS, minify | 10-100KB |

---

## Phase 3: Optimize Loop (Keep/Discard)

### Per-Optimization Cycle

```
FOR each optimization (O1..ON):
  1. APPLY: Make change (remove dep, rewrite import, add lazy load)
  2. BUILD: Run build command
     IF build FAILS → DISCARD (revert) → next optimization
  3. MEASURE: New bundle size
  4. COMPARE:
     IF new_bytes < baseline_bytes → KEEP (new baseline = new_bytes)
     IF new_bytes >= baseline_bytes → DISCARD (revert, no improvement)
  5. LOG: Record result
```

### Stop Conditions (Optimize Loop)

| Condition | Action |
|-----------|--------|
| All optimizations processed | STOP — proceed to Report |
| 3 consecutive DISCARDs (no size reduction) | STOP — plateau: "No further reductions found" |
| Build infrastructure breaks | STOP — revert to last KEEP, report partial results |
| Bundle already below target size | STOP — "Bundle already optimized" |

### Keep/Discard Decision

| Condition | Decision |
|-----------|----------|
| Build fails | DISCARD |
| Bundle smaller | KEEP (update baseline) |
| Bundle same or larger | DISCARD |

### Optimization Order

| Order | Category | Reason |
|-------|----------|--------|
| 1 | Remove unused deps | Safest, immediate savings |
| 2 | Named imports / tree-shaking | Medium risk, good savings |
| 3 | Lighter alternatives | Higher risk (API changes) |
| 4 | Dynamic imports / code splitting | Structural change, test carefully |
| 5 | CSS optimization | Lowest priority |

---

## Phase 4: Report Results

### Report Schema

| Field | Description |
|-------|-------------|
| project | Project path |
| baseline_bytes | Original bundle size |
| final_bytes | Final bundle size |
| reduction_bytes | Bytes saved |
| reduction_percent | Percentage reduction |
| optimizations_applied | Count of kept optimizations |
| optimizations_discarded | Count + reasons |
| details[] | Per-optimization: category, description, bytes saved |
| deps_removed[] | Unused dependencies removed |

---

## Configuration

```yaml
Options:
  # Build
  build_command: ""             # Auto-detect from ci_tool_detection.md
  output_dir: ""                # Auto-detect: dist/ or build/

  # Analysis
  run_depcheck: true
  run_bundle_analyzer: false    # Opens browser, skip in CI

  # Optimization scope
  remove_unused_deps: true
  fix_tree_shaking: true
  suggest_alternatives: true
  add_code_splitting: false     # Structural change, opt-in

  # Verification
  run_build: true
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| depcheck not available | Not installed | `npx depcheck` (runs without install) |
| Build fails after removal | Dep used in dynamic import / config | Revert, mark as false positive |
| No output directory | Non-standard build setup | Check package.json for output config |
| Not a JS/TS project | No package.json | Skip entirely with info message |

---

## References

- `shared/references/ci_tool_detection.md` (build detection)

---

## Definition of Done

- [ ] JS/TS project confirmed (package.json present)
- [ ] Baseline bundle size measured (build + measure dist/)
- [ ] Unused deps identified via depcheck
- [ ] Each optimization applied with keep/discard: build passes + smaller → keep
- [ ] Compound: each kept optimization updates baseline for next
- [ ] Report returned with baseline, final, reduction%, per-optimization details

---

**Version:** 1.0.0
**Last Updated:** 2026-03-08
