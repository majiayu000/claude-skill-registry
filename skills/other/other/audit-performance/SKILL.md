---
name: audit-performance
description: Audit performance against Core Web Vitals and performance budgets when the user asks to check performance, audit speed, or analyze web vitals
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[page, feature, or endpoint to audit for performance]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: audit, performance, optimization
---

# Audit Performance

## Overview

Generate a performance budget audit against Core Web Vitals (LCP, INP, CLS), bundle size, and API latency. Defines thresholds, identifies violations, and provides actionable recommendations for image optimization, code splitting, lazy loading, and caching improvements.

## Workflow

1. **Read engineering context** -- Scan `.chalk/docs/engineering/` for architecture docs, existing performance budgets, and infrastructure configuration. Check the codebase for build configuration (webpack, vite, next.config) and existing performance tooling.

2. **Parse the audit target** -- Extract from `$ARGUMENTS` the page, feature, or endpoint to audit. If unspecified, audit the most critical user-facing page (typically the landing page or main dashboard).

3. **Determine the next file number** -- Read filenames in `.chalk/docs/engineering/` to find the highest numbered file. The next number is `highest + 1`.

4. **Define performance budgets** -- Set thresholds (use existing budgets from docs if available, otherwise use industry standards):

   | Metric | Good | Needs Improvement | Poor |
   |--------|------|-------------------|------|
   | LCP | < 2.5s | 2.5-4.0s | > 4.0s |
   | INP | < 200ms | 200-500ms | > 500ms |
   | CLS | < 0.1 | 0.1-0.25 | > 0.25 |
   | Bundle size (JS) | < 200KB gzipped | 200-350KB | > 350KB |
   | API latency (p95) | < 300ms | 300-1000ms | > 1000ms |

5. **Analyze the codebase for performance issues** -- Review:
   - Bundle: large dependencies, tree-shaking gaps, missing code splitting
   - Images: unoptimized formats, missing lazy loading, no responsive sizes
   - Rendering: layout shifts from dynamic content, render-blocking resources
   - Data fetching: waterfall requests, missing caching, over-fetching
   - API: slow queries, missing indexes, N+1 problems

6. **Report violations** -- For each budget exceeded or at risk, document: current value (if measurable from code analysis), threshold, root cause, and recommended fix.

7. **Prioritize recommendations** -- Rank fixes by impact (how much improvement) and effort (how hard to implement). Quick wins first.

8. **Write the file** -- Save to `.chalk/docs/engineering/<n>_performance_audit.md`.

9. **Confirm** -- Share the file path and highlight the top 3 highest-impact fixes.

## Output

- **File**: `.chalk/docs/engineering/<n>_performance_audit.md`
- **Format**: Plain markdown with budget table, violations list, and prioritized recommendations
- **First line**: `# Performance Audit: <Target>`

## Anti-patterns

- **Auditing without budgets** -- "The page is slow" is not actionable. Define thresholds first, then measure against them. Without budgets, there is no pass/fail.
- **Only measuring lab data** -- Lab metrics (Lighthouse) and field metrics (CrUX) can differ significantly. Note which measurements are lab-based and recommend field monitoring.
- **Recommendations without priority** -- A list of 20 optimizations without ranking overwhelms teams. Prioritize by impact-to-effort ratio and present quick wins first.
- **Ignoring bundle composition** -- "Bundle is too large" without identifying which dependencies contribute most is not helpful. Break down the bundle and identify the largest contributors.
- **Missing API latency** -- Frontend performance audits that ignore API response times miss half the picture. Include backend latency in the audit scope.
