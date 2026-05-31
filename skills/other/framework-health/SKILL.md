---
name: framework-health
description: "Evaluate Mycelium's own process effectiveness. Measures cycle velocity, discard trends, confidence calibration, gate effectiveness, regression rate. Run quarterly or every 20 cycles."
metadata:
  instruction_budget: "50"
  framework_dependency: "mycelium"
  framework_dependency_note: "This skill is designed to run within the Mycelium framework (https://github.com/haabe/mycelium). Standalone use will skip the canvas state, theory gates, and harness behavior the skill assumes. Install: /plugin install mycelium@haabe/mycelium."
---

# Framework Health Check

Mycelium evaluates its own process. This is triple-loop learning — the framework assessing whether it is getting better at producing good outcomes.

## When to Use

- Quarterly review (scheduled)
- After 20 completed leaf cycles (triggered by cycle-history.yml count)
- When process friction is suspected
- Before major framework changes (baseline measurement)

## Workflow

### 1. Load Cycle Data

Read `.claude/canvas/cycle-history.yml`.

**Framework-self-host detection** (per `engine/cycle-learning.md#framework-on-framework-exemption`): if the project root contains `plugins/mycelium/plugin.json` AND `CLAUDE.md` begins with `# Mycelium:`, this is the framework dogfooding itself. Skip the cycle-count gate and route to a corrections-graduation summary:
- Count entries in `.claude/memory/corrections.md` (total, and ×graduated-to-mechanism in the last 90 days).
- Read `.claude/memory/cluster-instances.md` and list clusters at-or-above their graduation criterion that are not yet graduated (this is the framework analogue of "actual outcome vs predicted ICE").
- Skip cycle-derived dimensions (velocity, discard rate, confidence calibration, regression rate) — they do not apply. Still run Steps 2b, 4b, 4c, 4d.

Otherwise (product project, not framework-self-host): if fewer than 5 cycles recorded, report:
"Insufficient cycle data for framework health assessment. [N] cycles recorded; minimum 5 needed. Continue recording outcomes."

### 2. Measure Five Dimensions

For each dimension, compute the metric and compare against trend (if prior assessments exist):

**Cycle Velocity**:
- Average days from diamond creation to completion, grouped by scale
- Trend: improving / stable / degrading
- If degrading: flag for investigation

**Discard Rate**:
- Count of discards per lifecycle phase
- Average discard phase (1-10 scale)
- Trend: shifting earlier (good) / shifting later (bad) / stable
- If >50% of discards at Phase 7+: flag "late discard pattern"

**Confidence Calibration**:
- For all cycles with predicted confidence and actual outcome:
  - Compute: actual success rate per confidence band (0.3-0.5, 0.5-0.7, 0.7-0.9)
  - Compare with expected rate (confidence 0.7 should succeed ~70%)
  - Report calibration factor: actual/expected
- If calibration factor < 0.8 or > 1.2: flag miscalibration

**Gate Effectiveness**:
- For each theory gate, count: times checked, times passed, times failed
- Compute hit rate: failures / total checks
- Flag rubber stamps (0% failure rate) and hard blocks (>80% failure rate)
- **Theory X/Y audit** (per `${CLAUDE_PLUGIN_ROOT}/harness/theory-tensions.md` Tension 7): for any hard-block gate, check it is *scaffolding* (surfaces its why, an escape hatch exists, leaves the user more capable), not *coercion* (compliance for its own sake, no surfaced reason, no escape). A high-block gate that fails this audit is a Theory-X drift to remediate, not just a strict gate.

**Regression Rate**:
- Count diamonds that regressed at least once / total diamonds
- Trend: decreasing (good) / increasing (bad) / stable

### 2b. Re-run Deferred Design-Verification Eval Scenarios

Re-run any eval scenario tagged `regression` AND `router-discipline` from `.claude/evals/scenarios/integration/`. These are deferred design-time decisions that need periodic re-verification (the AGENTS.md router design is the canonical case — see `agents-md-router-discipline.yml`).

For each scenario:
- Run via `/mycelium:eval-runner` against the scenario file
- Compare result against the scenario's `baseline_reference` field
- Report:
  - **Same outcome** → design holding; no action
  - **Improved** → either the design got better OR the model improved; investigate which (a model improvement that hides a design regression is a Goodhart trap)
  - **Regressed** → design drifted; flag for remediation in this assessment

If a scenario fails its `success_criteria` for the first time, log to corrections.md as a new generalizable correction with the scenario name as evidence. Do not auto-remediate — surface the regression for human review.

### 3. Run Threshold Calibration

If cycle count ≥ minimum_n for any threshold in `.claude/canvas/thresholds.yml`:
- Apply calibration rules from `${CLAUDE_PLUGIN_ROOT}/engine/adaptive-thresholds.md`
- Update calibrated values
- Log changes in .claude/harness/decision-log.md

### 4. Check Goodhart Counter-Metrics

For each dimension, verify the counter-metric is not degrading:
- Velocity improving BUT outcome quality declining? Flag.
- Earlier discards BUT false positive rate rising? Flag.
- Better calibration BUT decision speed dropping? Flag.

### 4b. Cluster Graduation-Readiness (added 2026-05-08)

Read `.claude/memory/cluster-instances.md`. For each cluster:
- **Compare instance count to graduation criterion.** If a cluster has reached or exceeded its stated criterion without being graduated to the corresponding mechanism (e.g., 6+ instances with spec-only status when promotion bar requires implemented detection rules), surface as a graduation-readiness flag.
- **For `spec`-status clusters with linked spec docs** (e.g., `${CLAUDE_PLUGIN_ROOT}/engine/consistency-check-spec.md`): check whether the spec's promotion-bar conditions have been met. Concretely: count detection rules drafted vs. required, FP-rate measurements available vs. needed.
- **Recursive check**: if a cluster's stated graduation criterion has been met for >30 days without graduation action, that's itself an instance of the documented-rule-diverges-from-enforcement cluster — log it.
- **Output**: include cluster status in the dashboard under a new "Cluster Graduation Status" section.

This step closes the recursion the cluster log was created to address: graduation criteria become mechanically auditable rather than promises stored in commit messages.

### 4c. Receipts Highlights Rotation Cadence (added 2026-05-08)

The README's "How Mycelium got smarter" section shows 5 case headers; the full list lives in `docs/receipts/cases/`. Stale README highlights are a Goodhart signal: if the receipts surface freezes, the framework's "we get smarter with each cycle" claim degrades to "we got smarter once".

For each case currently on the README:
- **Check git-log staleness**: when did the case header last change? If >90 days, flag as a rotation candidate.
- **Check for newer cases**: are there cases under `docs/receipts/cases/` newer than the rotation candidate that better demonstrate the framework's recent behavior?
- **Recommend rotation**: surface specific rotate-out / rotate-in pairs in the dashboard. Rotation is a maintainer decision, not automatic — but the flag forces the decision rather than letting it drift.
- **Highlight gap signal**: if no case has been added to `docs/receipts/cases/` in >60 days, flag as a possible-low-friction signal — either the framework genuinely caused no recent friction (rare), or the dogfood loop has weakened (usually).

Per `docs/contributing/style.md#highlights-rotation`. Cases stay in `docs/receipts/cases/` even when rotated off README; only the README mention rotates.

### 4d. Docs Health Cross-Surface (added 2026-05-08)

Run a lightweight version of `/mycelium:canvas-health` step 9b on `docs/`:
- Stub freshness (any forthcoming-doc `Last updated` >60 days)
- Length budget compliance (hard caps)
- Marketing-voice scan
- Information-scent scan on links

Surface in the dashboard. Full details delegate to `/mycelium:canvas-health`.

### 4e. Chat-UX Axiom Audit of Skill Output Templates (added 2026-05-30)

The chat-UX nudges in `${CLAUDE_PLUGIN_ROOT}/harness/design-principles.md` ("the chat is a UI") shape *live* output, which has no stored corpus to audit retroactively. What *is* auditable is the static surface that pre-shapes live output: the `## Output`/`## Output Format` blocks in `${CLAUDE_PLUGIN_ROOT}/skills/*/SKILL.md`. Scan each for two axiom violations:

- **Hick's Law** — an output template that instructs the agent to present a *list of options/recommendations* with no "recommend one" / "priority" / "top-N" cue. A template that emits N equally-weighted choices manufactures decision-tax on every invocation. Flag templates with option-lists lacking a recommendation cue.
- **Von Restorff (isolation)** — an output template that renders a blocker, gate, error, or STOP condition as undifferentiated prose rather than a visually distinct marker (`ON HOLD`, `Gated by:`, a leading verdict line). Flag blocker-bearing templates whose blocker does not visually pop.

This is the **buildable** form of the self-audit; the live-output version is unenforceable (no corpus). Surface counts + offending skills in the dashboard. Do not auto-edit skills — flag for maintainer review (a template's flat option-list may be deliberate). Graduation path: if the same skill is flagged across two assessments, promote to a mechanical `tests/bash` check (then it inherits G-V12 / Check 37).

### 5. Generate Dashboard

## Output

```
## Framework Health Dashboard

Assessment date: [date]
Cycles analyzed: [N]
Period: [date range]

### Dimensions

| Dimension | Current | Trend | Status | Counter-Metric |
|-----------|---------|-------|--------|----------------|
| Cycle velocity | [X days avg] | [improving/stable/degrading] | [healthy/warning/critical] | Outcome quality: [OK/degrading] |
| Discard rate | [avg phase X] | [earlier/stable/later] | [healthy/warning/critical] | False positive rate: [OK/rising] |
| Confidence calibration | [factor X.XX] | [improving/stable/diverging] | [healthy/warning/critical] | Decision speed: [OK/slowing] |
| Gate effectiveness | [see detail] | — | [healthy/warning/critical] | Flow speed: [OK/slowing] |
| Regression rate | [X%] | [decreasing/stable/increasing] | [healthy/warning/critical] | Innovation rate: [OK/declining] |

### Threshold Calibration

| Threshold | Default | Calibrated | Based On | Change |
|-----------|---------|-----------|----------|--------|
| ICE advance | 100 | [value or "insufficient data"] | N cycles | [+/-] |
| Confidence factor | 1.0 | [value or "insufficient data"] | N cycles | [+/-] |
| Bakeoff delta | 20% | [value or "insufficient data"] | N bakeoffs | [+/-] |

### Pattern Signals Active

[List any active pattern detector signals from ${CLAUDE_PLUGIN_ROOT}/engine/pattern-detector.md]

### Recommendations

[Specific actions based on findings — not generic advice]
```

## Rules

- Never modify thresholds without sufficient data (respect minimum_n)
- Always check counter-metrics before celebrating improvement
- Log all threshold changes in .claude/harness/decision-log.md
- If all dimensions are healthy, say so and suggest next review date

## Theory Citations

- Argyris: Triple-loop learning (learning how to learn)
- Forsgren: Accelerate (measuring capabilities, not just outputs)
- Goodhart: Counter-metrics for every metric
- Deming: Statistical process control (data-driven threshold adjustment)
