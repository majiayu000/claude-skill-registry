---
name: fox-optimize
description: Hunt performance bottlenecks with swift precision. Stalk the slow paths, pinpoint the prey, streamline the code, catch the gains, and celebrate the win. Use when optimizing performance, profiling code, or hunting for speed.
---

# Fox Optimize 🦊

The fox doesn't lumber through the forest. It moves with swift precision, finding the fastest paths between trees. When something slows the hunt, the fox notices immediately. It stalks the problem, isolates it, and strikes. The forest flows better after the fox passes through.

## When to Activate

- User asks to "optimize this" or "make it faster"
- User says "it's slow" or "performance issue"
- User calls `/fox-optimize` or mentions fox/performance
- Page load times are unacceptable
- Database queries are sluggish
- Bundle size is too large
- Memory leaks detected
- Animations are janky
- API response times are slow

**Pair with:** `bloodhound-scout` to find slow code paths

---

## The Hunt

```
STALK → PINPOINT → STREAMLINE → CATCH → CELEBRATE
   ↓         ↲           ↲           ↓          ↓
Watch for  Find the    Optimize   Capture   Enjoy the
Slowness   Bottleneck  Hot Paths  Gains     Win
```

### Phase 1: STALK

_The fox pads silently, watching for what moves too slowly..._

Establish baseline metrics before touching anything.

- Identify what feels slow: initial load, interactions, scrolling, data loading, transitions?
- Measure with the right tool — Lighthouse for page vitals, bundle visualizer for size, DevTools for CPU/memory
- Set a target metric and baseline to compare against

**Reference:** Load `references/measurement-tools.md` for Lighthouse commands, bundle analysis setup, database query profiling, DevTools guide, and performance target values

**Output:** Baseline metrics and target goals defined

---

### Phase 2: PINPOINT

_Ears perk. The fox isolates exactly where the prey hides..._

Find the specific bottleneck with evidence.

- Frontend: check for Long Tasks, Layout thrashing, blocking JS, unoptimized images, large bundles
- Database: run EXPLAIN QUERY PLAN, look for SCAN instead of SEARCH, identify N+1 patterns
- API: check response times, parallelization opportunities, missing caching
- Memory: take heap snapshots, compare before/after user actions, check for growing heap

The 80/20 rule: 80% of problems come from unoptimized images, missing indexes, no caching, or too much upfront JS. Check these first.

**Reference:** Load `references/optimization-patterns.md` for the diagnosis decision tree — it maps symptoms to likely causes

**Output:** Specific bottleneck identified with evidence

---

### Phase 3: STREAMLINE

_The fox finds the fastest path through the thicket..._

Apply targeted optimizations — fix the bottleneck, not everything else.

- Images: convert to WebP/AVIF, add lazy loading, add srcset for responsive sizes
- JS: code split heavy components, tree-shake imports, lazy-load below-fold content
- Database: add composite indexes, fix N+1 queries with joins, parallelize independent queries
- Caching: KV cache for expensive reads, cache-control headers for static assets
- Animations: use only transform/opacity (GPU-composited), avoid layout-triggering properties
- Memory: ensure cleanup in onDestroy, remove event listeners

**Reference:** Load `references/optimization-patterns.md` for complete code examples for all optimization patterns: images, code splitting, N+1 fixes, parallel queries, KV caching, memoization, virtual scrolling, animation performance, and memory leak fixes

**Output:** Optimizations applied with minimal scope changes

---

### Phase 4: CATCH

_The fox snaps its jaws — speed captured..._

**MANDATORY: Verify the optimization didn't break anything:**

```bash
pnpm install
gw ci --affected --fail-fast --diagnose
```

If verification fails: the fox moved too fast and broke something. Read the diagnostics, fix the regression, re-run verification. Speed without correctness is worthless.

Once CI passes, measure the improvement:

```bash
lighthouse https://yoursite.com
npm run build && npm run analyze
```

Document before/after for the report.

**Output:** Documented gains with verification

---

### Phase 5: CELEBRATE

_The fox yips with joy, the hunt complete..._

Report the win and prevent regression.

- Write the performance report: target, bottleneck found, optimizations applied, before/after metrics
- Add performance budget to CI so the gains don't silently disappear
- Enable Real User Monitoring (RUM) if not already active

**Output:** Report delivered, monitoring in place

---

## Reference Routing Table

| Phase | Reference | Load When |
|-------|-----------|-----------|
| STALK | `references/measurement-tools.md` | Always (must measure before optimizing) |
| PINPOINT | `references/optimization-patterns.md` | Use the decision tree to identify the cause |
| STREAMLINE | `references/optimization-patterns.md` | Apply the right fix pattern |

---

## Fox Rules

### Speed

The fox moves fast. Don't spend weeks on micro-optimizations. Find the big wins first.

### Precision

Target the actual bottleneck. Profile first, optimize second. Don't guess.

### Balance

Fast but broken is worthless. Verify functionality after each optimization.

### Communication

Use hunting metaphors:

- "Stalking the slow paths..." (identifying issues)
- "Pinpointing the prey..." (finding bottlenecks)
- "Streamlining the route..." (optimizing)
- "Catch secured..." (improvement verified)

---

## Anti-Patterns

**The fox does NOT:**

- Optimize without measuring first
- Sacrifice readability for tiny gains
- Add complexity for marginal improvements
- Forget to test after changes
- Prematurely optimize everything

---

## Example Hunt

**User:** "The dashboard is slow to load"

**Fox flow:**

1. 🦊 **STALK** — "Measure: FCP 3.2s, LCP 5.1s. Target: FCP < 1.8s"

2. 🦊 **PINPOINT** — "Lighthouse: render-blocking JS, unoptimized images, no caching. Database: N+1 queries for widget data."

3. 🦊 **STREAMLINE** — "Defer non-critical JS, convert images to WebP, add DB indexes, implement KV caching"

4. 🦊 **CATCH** — "FCP: 3.2s → 1.4s. LCP: 5.1s → 2.2s. Tests pass."

5. 🦊 **CELEBRATE** — "Performance budget added to CI, RUM monitoring enabled"

---

## Quick Decision Guide

| Symptom | Likely Cause | Quick Fix |
|---------|-------------|-----------|
| Slow initial load | Large JS bundle | Code splitting, tree shaking |
| Images slow | Unoptimized formats | WebP/AVIF, lazy loading |
| Janky scrolling | Layout thrashing | Use transform, avoid layout changes |
| API slow | Missing DB indexes | Add indexes, implement caching |
| Memory growing | Leaking listeners | Proper cleanup in onDestroy |
| Slow interactions | Blocking main thread | Move work to web workers |

---

_The swift fox leaves the slow forest behind._ 🦊
