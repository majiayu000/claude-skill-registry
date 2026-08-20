---
name: prd-v08-drift-baseline-compare
description: >
  Establish baseline → snapshot → compare → history monitoring for any KPI, config, or
  metric that can drift during PRD v0.8 Deployment & Ops. Triggers on requests to monitor
  drift, baseline a value for later comparison, or when user asks "how do we track if X
  changes?", "baseline this", "config drift", "performance regression", "metric drift",
  "compare to last week", "is this getting worse?". Outputs MON-DRIFT-* entries with
  baseline + comparison rules.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash

execution_modes:
  default: standard
  supports: [quick, standard, deep]
---

# Drift: Baseline / Compare / History

Position in workflow: v0.8 Monitoring Setup → **v0.8 Drift: Baseline / Compare / History** → v0.8 Runbook Creation

## Execution Mode

Default is **standard**. See [`.claude/rules/08-skill-execution-modes.md`](../../rules/08-skill-execution-modes.md) for selection logic.

| Mode | What this skill produces |
|------|--------------------------|
| **quick** | One metric / config / dataset baselined; weekly compare schedule; simple threshold alert |
| **standard** | 3–5 things monitored; baseline + tiered thresholds (warn / critical); compare cadence; history retention |
| **deep** | Full portfolio; multi-dimensional comparison (per segment, per environment); regression-cause matrix; auto-baselining after intentional change |

## What This Does

Generalizes a pattern AgriciDaniel's `claude-seo` skill encodes for SEO drift — **baseline → snapshot → compare → history** — into a reusable monitoring shape that works for any metric, config, or dataset that can change over time and needs to be watched.

This is **drift monitoring**, distinct from alerting on absolute thresholds. Alerting answers "is X over the line right now?" Drift monitoring answers "is X different from last week's normal?" — which catches slow regressions that absolute thresholds miss.

Examples of things worth drift-monitoring:
- **KPI**: activation rate week-over-week
- **AI search position**: ChatGPT/Perplexity ranking for target queries
- **Config**: feature-flag rollout percentages
- **Performance**: p95 latency by endpoint
- **Cost**: per-user infra cost
- **Marketing**: per-channel CAC trend
- **Content**: changelog post engagement
- **Third-party**: vendor pricing pages (price hikes), competitor feature pages (parity loss)

## How It Works

1. **Pick what to monitor** — One thing per MON-DRIFT- entry. Must be:
   - Quantifiable (number, percentage, list, configuration value)
   - Snapshotable (captureable at a point in time, ideally automatically)
   - Causally interpretable (when it changes, you know enough to investigate)
2. **Capture the baseline** — Take a snapshot. Date it. Store in version control or a known location (`status/baselines/`, `monitoring/snapshots/`, etc.).
3. **Define drift thresholds**:
   - **Warn**: meaningful change (e.g., 10% drift in a KPI; any change in a config value)
   - **Critical**: serious change (e.g., 25% KPI drop; breaking config change)
   - **Recalibrate**: intentional change that should refresh the baseline (e.g., after a feature rollout, the baseline is wrong; refresh it)
4. **Set compare cadence** — How often does this get re-snapshotted?
   - Hot (hourly/daily): production KPIs, AI search positions during a launch
   - Warm (weekly): standard product KPIs, content engagement
   - Cool (monthly): vendor pricing, competitor feature parity, infra cost
5. **Build the compare procedure** — A script or runbook that:
   - Takes a new snapshot
   - Diffs against baseline
   - Computes drift % per dimension
   - Emits warn/critical signals at thresholds
   - Appends to history log
6. **Plan auto-baselining after intentional change** [standard+] — When the team makes a deliberate change (ships a feature that should improve activation), the old baseline becomes wrong. Define what triggers a baseline refresh and who approves it.

## Example

Monitoring AI search position for the target query "best CRO tool for SaaS founders" across 3 surfaces. (Generalized from AEO Audit re-test cadence.)

**Baseline** (2026-04-01):
```
ChatGPT: not mentioned (rank: --)
Perplexity: rank 4 of 5, miscategorized as "analytics"
AI Overviews: not mentioned
Sources cited: [competitor1.com, competitor2.com, reddit.com/r/SaaS]
```

**Thresholds**:
- Warn: rank changes by ≥1, sources list changes, miscategorization persists
- Critical: dropped from any surface where previously mentioned

**Compare cadence**: weekly during launch month, monthly after.

**Re-snapshot** (2026-04-15):
```
ChatGPT: rank 3 of 5 (NEW)         ← improved
Perplexity: rank 3 of 5, category corrected (NEW)   ← improved
AI Overviews: rank 5 of 7 (NEW)    ← improved
Sources cited: [+ ourdomain.com (NEW), ...]
```

**Compare output**: 3 surfaces improved. Likely cause: alternatives-pages campaign + new CRO-anchored blog post indexed.

**History append**: 2026-04-01 → 2026-04-15 row added to history log.

**Action**: No alert; positive drift. Baseline can stay (next compare in 2 weeks). If the trend reverses, the baseline catches it.

## What You Get Back

- **MON-DRIFT-\* entries** (one per monitored thing) — Baseline snapshot, thresholds, cadence, compare procedure, history pointer
- **History logs** in `status/drift-history/<id>.jsonl` (or similar) — Append-only record of compare results
- **Compare scripts** (`scripts/drift/<id>.sh` or equivalent) when automatable

## When to Use It

| Trigger | Mode |
|---------|------|
| Post-launch — need ongoing watch on KPIs | standard |
| AEO Audit results to maintain | standard |
| Competitor feature parity tracking | standard |
| Vendor / third-party pricing watch | quick |
| Performance regression hunting | deep |
| Infrastructure cost trend | quick |

Do not use for things that are already covered by **threshold-based alerting** (RED/USE metrics, MON-* alerts). Drift is for trends; alerting is for absolutes.

## Consumes

- **MON-\* monitoring infrastructure** (from v0.8 Monitoring Setup) — Data sources for KPI/performance drift; existing dashboards
- **KPI-\* metric definitions** (from v0.3 + v0.9) — What's worth watching
- **CFD-\* competitor research** (from v0.2 + ongoing) — For competitor-parity drift
- **GTM-AEO-\* Coverage Matrix** (from v0.9 AEO Audit) — For AI search position drift
- **BR-PRICING-\*** (from v0.3 + v0.9 Offer) — For pricing drift on our side; vendor-pricing drift watches their side
- **DEP-\* release entries** — Intentional changes that may trigger baseline refresh

## Produces

- **MON-DRIFT-\* entries** with `Type=Drift-Baseline` — One per monitored thing
- **History logs** in `status/drift-history/` — Append-only diff history
- **Compare scripts** in `scripts/drift/` (when automatable)
- **Baseline-refresh approvals** — Recorded when an intentional change resets a baseline

## Output Template

```
MON-DRIFT-XXX: Baseline — [What is being monitored]
Type: Drift-Baseline
Category: [KPI | AI-Search | Config | Performance | Cost | Vendor | Competitor]
Owner: [Person / role]
Status: Active

Subject: [Specific thing — e.g., "ChatGPT rank for query 'best CRO tool for SaaS'"]

Baseline (YYYY-MM-DD):
  [Snapshot — values, list, config dump, etc.]

Thresholds:
  Warn: [Condition — e.g., "rank change ≥1 OR sources list changes"]
  Critical: [Condition — e.g., "dropped from any surface previously mentioned"]
  Recalibrate-trigger: [What intentional change resets the baseline]

Compare cadence: [Hourly | Daily | Weekly | Monthly | Triggered]
Compare procedure: [Script path OR manual runbook reference]

History: status/drift-history/<id>.jsonl

Re-snapshot history:
  - YYYY-MM-DD: [summary of last compare result]
  - YYYY-MM-DD: ...

Linked IDs: MON-XXX (data source), KPI-YYY or CFD-ZZZ or GTM-AEO-AAA (subject)
```

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| **Stale baseline** | Comparing today's value against a 12-month-old baseline that no longer reflects "normal" | Add recalibrate-trigger conditions; refresh after intentional changes |
| **Drift alerting on noise** | Critical alert fires every week for 2% movement | Threshold is too tight; widen warn, tighten critical |
| **No history log** | Snapshot, compare, alert, forget | Append-only history is the whole point; without it, you can't see trends |
| **Monitoring everything** | 50 MON-DRIFT-* entries, nobody reads any | Pick the 3–5 things that matter; archive the rest |
| **No causal interpretation** | "Drift detected" with no investigation path | Each drift signal should map to candidate causes (recent release, competitor move, AI surface change) |
| **Drift instead of alerting** | Using drift for things that need absolute thresholds | Drift = trends; absolutes (latency > 500ms) = alerting |

## Quality Gates

Before activating drift monitoring:

- [ ] Subject is quantifiable and snapshotable
- [ ] Baseline captured with explicit date
- [ ] Warn and critical thresholds defined
- [ ] Compare cadence committed
- [ ] Compare procedure (script or runbook) exists
- [ ] History log path defined and writable
- [ ] Recalibrate-trigger documented (when does baseline get refreshed?)
- [ ] Owner assigned

## Downstream Connections

| Consumer | What it uses | Example |
|----------|--------------|---------|
| **Runbook Creation (RUN-)** | Drift criticals trigger investigation runbooks | MON-DRIFT-AEO critical → RUN-investigate-aeo-loss |
| **Launch Metrics** | Drift on launch KPIs informs go/no-go decisions | KPI-activation drift ≥10% → re-look at GTM |
| **Feedback Loop Setup** | Drift in customer-facing metrics drives CFD- investigation | Activation drift down → CFD- interview cohort |
| **v0.9 AEO Audit (re-run)** | Drift in AI search positions triggers re-audit | AEO drift → re-run aeo-audit |
| **v1.0 Continuous Discovery** | Drift patterns inform discovery questions | "Why is X drifting?" → Teresa Torres discovery |

## Detailed References

- AgriciDaniel's `seo-drift` skill — original baseline/compare/history pattern for SEO
- Site Reliability Engineering (Google) — SLO-burn-rate alerting (related but different)
- (No bundled `references/` — pattern is reusable; the *content* lives in each MON-DRIFT- entry)
