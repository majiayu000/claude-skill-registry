---
name: tracking-cache-costs
description: Measures OpenCode prompt caching efficiency using ccusage-opencode. Use when investigating API costs, evaluating cache hit rates, or checking if upstream caching fixes have landed.
---

# Tracking OpenCode Cache Costs

## Quick Check

```bash
ccusage-opencode daily
```

## Full Analysis

Run the analysis script for per-day cache efficiency breakdown and savings estimate:

```bash
node .opencode/skills/tracking-cache-costs/analyze.mjs
```

Output includes: daily cache read/write/uncached ratios, cost breakdown at model-specific rates, and projected monthly savings if cache writes were reduced.

Adjust the `REDUCTION` env var to model different improvement scenarios (default: 0.44 = 44%, per PR #5422's benchmark):

```bash
REDUCTION=0.30 node .opencode/skills/tracking-cache-costs/analyze.mjs
```

## Interpreting Results

| Write % | Assessment | Action |
|---------|-----------|--------|
| <10% | Healthy | No action needed |
| 10-20% | Moderate | Check for short sessions or frequent subagent spawning |
| 20-40% | Poor | Cache busting likely -- tool reordering or file tree churn |
| >40% | Severe | Investigate immediately, major cost impact |

**Root causes of high writes**: tool definition order instability (prefix-based cache busted by reordering), file tree changes in system prompt, only 4 cache breakpoints in current opencode, short sessions / subagent spawning.

## Check Upstream Progress

```bash
gh pr view 5422 --repo anomalyco/opencode --json state,comments --jq '{state, lastComment: .comments[-1].body[:200]}'
gh pr list --repo anomalyco/opencode --search "cache" --state merged --limit 5 --json number,title,mergedAt
```

Key items:
- [PR #5422](https://github.com/anomalyco/opencode/pull/5422) -- provider-specific cache config (not merged)
- [Issue #5416](https://github.com/anomalyco/opencode/issues/5416) -- caching improvement request
- [Issue #5224](https://github.com/anomalyco/opencode/issues/5224) -- system prompt cache invalidation
- Any PR touching `packages/opencode/src/provider/transform.ts` signals caching work
