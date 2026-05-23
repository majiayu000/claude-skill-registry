---
name: dora-check
description: "Assess delivery health metrics. For software: DORA + APEX. For content/AI/service products: product-type-appropriate metrics."
metadata:
  instruction_budget: "126"
---

# Delivery Metrics Check

Assess delivery health using product-type-appropriate metrics. Check `product_type` from `.claude/diamonds/active.yml` to determine which assessment to run.

**Product type routing** (v0.11.0):
- **software**: Full DORA + APEX assessment (Parts 1-3 below)
- **content_course, content_publication, content_media**: Content Delivery Assessment (Part 4 below)
- **ai_tool**: AI Tool Assessment (Part 5 below) + DORA/APEX if code components exist
- **service_offering**: Service Delivery Assessment (Part 6 below)

---

## Preflight: Read target canvas file(s) before any Write/Edit

**Hard rule.** Before issuing `Write` or `Edit` against any `.claude/canvas/*.yml`, use the **Read tool** on that file in this session. Claude Code's Read-before-Write check requires the `Read` tool specifically — `cat`/`head`/`grep` via Bash do NOT satisfy it.

**Edit vs Write — different cost profiles** (verified 2026-05-14):
- **`Edit`** (exact-string replacement): `Read` with `limit: 1` satisfies the check at ~50 tokens. State-tracking is per-file, not per-byte — subsequent `Edit` calls work anywhere in the file. Use this for partial updates against large canvas files (e.g., `purpose.yml` at 800+ lines).
- **`Write`** (full replacement): do a **full Read** first. Write obliterates the file; you should see what you're about to replace. The `limit:1` shortcut is *not* appropriate here.

**ID-bearing entries — scan the ID space before assigning** (added 2026-05-15, v0.23.19): When adding a new component, opportunity, solution, or any other ID-bearing entry to a canvas file, run a Bash grep first to confirm the next ID in your prefix sequence is actually free:

```
grep "^  - id: <prefix>-" .claude/canvas/<file>.yml | sort -u
```

Replace `<prefix>` with the canvas's ID prefix (`comp` for landscape, `opp` for opportunities, `sol` for solutions, `ht` for human-tasks, etc.). Then pick the next free integer. `validate_canvas.py` has a duplicate-ID check (lines 230-239) that catches the failure on CI, but a duplicate can persist in the working tree for days if CI isn't run between edit and discovery — see roadmap-repo `corrections.md` 2026-05-15 "Duplicate canvas ID created in landscape.yml" for the worked example.

Original failure mode: anti-pattern #7 instance #5, 2026-05-09 — agent conflated Bash `head` with the Read tool, lost ~14k tokens to a Write-fail → remedial-full-Read → re-Write loop. The `limit:1` discipline (graduated 2026-05-14, v0.23.18) prevents the second-order cost where the agent *correctly* follows the rule but full-Reads every time. The ID-scan discipline (graduated 2026-05-15, v0.23.19) prevents the related class where the agent reads enough of the file to satisfy the Edit check but not enough to see existing ID assignments — kin to anti-pattern #8 (Stale State Read).

If this skill writes to multiple canvas files, register each one first (limit:1 for Edit-only paths; full Read for Write paths) AND ID-scan any prefix you intend to assign.

See `CLAUDE.md` *Canvas writes — Read before Write* for the canonical rule.

## Software Products

Assess delivery health using Forsgren's five DORA metrics AND LinearB's APEX AI-era metrics.

## Part 1: DORA Metrics (Forsgren)

Gather current metrics from CI/CD, deployment logs, incident records.

*Note: DORA expanded from 4 to 5 metrics. "MTTR" was renamed to "Failed Deployment Recovery Time" (FDRT) for precision — the original name was ambiguous with other mean-time-to-X metrics. "Reliability" was added as the 5th metric in the 2024 State of DevOps report.*

**Deployment Frequency**: How often does code reach production?
- Elite: On-demand (multiple deploys/day)
- High: Between once/day and once/week
- Medium: Between once/week and once/month
- Low: Less than once/month

**Lead Time for Changes**: Commit to production time?
- Elite: Less than one hour
- High: Between one day and one week
- Medium: Between one week and one month
- Low: More than one month

**Change Failure Rate**: % of deployments causing failure?
- Elite: 0-15%
- High: 16-30%
- Medium: 31-45%
- Low: 46-100%

**Failed Deployment Recovery Time (FDRT)**: Time to restore service after a failed deployment?
- Elite: Less than one hour
- High: Less than one day
- Medium: Between one day and one week
- Low: More than one week

*Formerly "Mean Time to Recovery (MTTR)." Renamed for precision — FDRT measures recovery from failed deployments specifically, not all incidents.*

**Reliability**: Does the software meet or exceed its reliability targets?
- Elite: Meets or exceeds targets
- High: Slightly below targets
- Medium: Moderately below targets
- Low: Significantly below targets

*Added in DORA 2024. Measures operational reliability via SLOs/SLIs. Connects to SRE metrics in Part 3.*

## Part 2: APEX Metrics (LinearB)

**"Faster coding doesn't mean faster delivery."**

Assess the four APEX pillars to detect AI-era delivery problems:

### A — AI Leverage
- What % of PRs/code changes are AI-generated or AI-assisted?
- What is the AI suggestion acceptance rate? (Benchmark: 32.7% for AI vs 84.4% for human — LinearB 2026)
- What is the AI rework rate? (% of AI code rewritten within 21 days)
- Is AI code quality comparable to human code? (Check corrections.md origin field)

### P — Predictability
- Planning accuracy: % of planned work completed per cycle?
- Rework rate: % of ALL code rewritten within 21 days?
- Are delivery estimates getting more or less reliable with AI?

### E — Flow Efficiency (The Shifting Bottleneck)
- End-to-end cycle time: is it actually decreasing?
- Review wait time: are PRs waiting longer before first review?
- AI review wait ratio: do AI PRs wait longer than human PRs? (Benchmark: 4.6x — LinearB 2026)
- **KEY CHECK**: Is coding faster but review/testing/deployment slower? If yes, the bottleneck has shifted. AI is generating code the pipeline can't absorb.

### X — Developer Experience
- Developer satisfaction with AI tools (survey or conversation)
- Cognitive load: is AI helping or adding complexity?
- Burnout signals: unsustainable pace? Context-switching? Alert fatigue?
- Maps to BVSSH "Happier" dimension

## Output

```
## DORA + APEX Assessment

### DORA Metrics
| Metric | Current | Level | Target | Gap |
|--------|---------|-------|--------|-----|
| Deploy freq | ... | ... | ... | ... |
| Lead time | ... | ... | ... | ... |
| Change fail rate | ... | ... | ... | ... |
| FDRT | ... | ... | ... | ... |
| Reliability | ... | ... | ... | ... |

### APEX Metrics (AI-Era)
| Pillar | Status | Key Signal |
|--------|--------|-----------|
| AI Leverage | ... | AI acceptance rate: ...% |
| Predictability | ... | Planning accuracy: ...%, Rework rate: ...% |
| Flow Efficiency | ... | Cycle time: ..., Review wait: ... |
| Developer Experience | ... | Satisfaction: ..., Burnout: ... |

### Shifting Bottleneck Check
[Is coding faster but review/deployment slower? Yes/No]
[If yes: where is the new bottleneck?]

### DORA Bottleneck
[The metric most constraining overall performance]

### Value Stream Diagnosis (if bottleneck detected)
If DORA shows a bottleneck, map the value stream to identify WHERE in the flow the constraint lives:
- Run `/mycelium:canvas-update` to update `.claude/canvas/value-stream.yml` with current stage timings
- Apply Theory of Constraints Five Focusing Steps (Goldratt): Identify -> Exploit -> Subordinate -> Elevate -> Repeat
- Look for wait times >> process times (a sign of queuing, not capacity, problems)
- Look for high handoff counts (each handoff adds delay and information loss)
- Calculate flow efficiency: process_time / lead_time -- target >25%

### Top 3 Improvements
1. [specific action]
2. [specific action]
3. [specific action]
```

## Part 3: SRE Metrics (Error Budgets)

If SLIs/SLOs defined in `.claude/canvas/dora-metrics.yml` sre section:
- Review each service's SLI values against SLO targets
- Calculate error budget remaining: (SLO - actual) / (1 - SLO) * 100%
- **Healthy** (>50%): Ship features. Budget available.
- **Warning** (<25%): Slow down. Increase testing.
- **Depleted** (0%): Feature freeze. Reliability takes priority.

Error budgets are the social contract: reliability earns the right to ship faster. Connects to BVSSH Safer.

If NOT defined: "Consider defining SLIs/SLOs to balance velocity with reliability."

## Decision Log (MANDATORY)
**Always APPEND** a `### DORA Assessment` or `### Delivery Metrics Assessment` entry to `.claude/harness/decision-log.md` with:
- Each metric assessed, current baseline, target, and classification level
- The identified bottleneck and recommended improvements
- Any shifting bottleneck signals (AI-era: coding faster but review slower)
This ensures the delivery metrics gate has auditable evidence.

## Canvas Output
**Always update** `.claude/canvas/dora-metrics.yml` with:
- DORA metrics, classifications, and capability scores
- APEX section: ai_leverage, predictability, efficiency, developer_experience
- SRE section: SLI/SLO status, error budget remaining
- Measurement history for trend tracking

---

## Part 4: Content Delivery Assessment (v0.11.0)

For content_course, content_publication, content_media products. Read `.claude/canvas/content-metrics.yml`.

### Producer-Side (how well we make it)

**Publication Cadence**: How often does content reach the audience?
- Consistent: meeting target cadence
- Improving: cadence accelerating
- Declining: cadence slowing -- investigate bottleneck

**Production Lead Time**: Idea to published -- how long?
- Identify the bottleneck: writing, editing, recording, review, publishing?

**Revision Rate**: % of published content requiring significant revision?
- Low (<10%): healthy quality process
- Medium (10-25%): review process may need strengthening
- High (>25%): quality issues -- root cause analysis needed

**Completion Rate**: % of planned content actually completed on schedule?

### Customer-Side (how well it sells and retains)

**Time to First Value (TTFV)**: How quickly does a buyer access and get value after purchase?
- Instant download/access: excellent
- Hours (email delivery, account setup): acceptable
- Days (manual enrollment, approval): investigate bottleneck
- Lower TTFV = lower refund risk.

**Engagement & Drop-off**: Course completion rate, satisfaction, return rate?
- Where do users abandon? (drop_off_points) If >30% drop at the same point, the content has a structural problem there.

**Acquisition**: Conversion rate, cost per acquisition, cart abandonment?
- Healthy CVR varies by channel (organic: 2-5%, paid: 1-3%, email: 5-15%)

**Revenue Health**: Refund rate, CLV, churn (subscriptions), NRR?
- Refund rate is the most honest quality signal. Target: < 5%.
- Refund rate > 10% = product-market fit problem, not just delivery quality.

### Canvas Output
Update `.claude/canvas/content-metrics.yml` with current measurements and `last_measured` timestamp.

---

## Part 5: AI Tool Assessment (v0.11.0)

For ai_tool products. Read `.claude/canvas/ai-tool-metrics.yml`.

### Producer-Side (quality & safety)

**Eval Frequency**: How often are prompts/models evaluated?
- Regular evaluation prevents quality drift

**Accuracy & Consistency**: Are eval scores stable or improving?

**Safety Score**: Red-team results -- are adversarial inputs handled?

**Bias Assessment**: Last assessed when? Any demographic gaps found?

**Version Cadence**: How often are prompt/model versions shipped?

**Regulatory Status**: EU AI Act risk classification current?

### Customer-Side (usage & retention)

**Time to First Value (TTFV)**: How quickly does a user get useful output after first access?
- Seconds (paste prompt, get result): excellent
- Minutes (configure API key, learn UI): acceptable
- Hours (training required): investigate onboarding friction

**Usage & Retention**: DAU, task success rate, retention (7-day, 30-day)?
- Task success rate < 70% = prompt/model quality issue
- Drop-off points: where do users abandon? (onboarding, first complex task, pricing wall)

**Revenue Health**: Refund rate, CLV, churn, NRR?
- Same benchmarks as content: refund rate target < 5%

### Canvas Output
Update `.claude/canvas/ai-tool-metrics.yml` with current measurements and `last_measured` timestamp.

---

## Part 6: Service Delivery Assessment (v0.11.0)

For service_offering products. Read `.claude/canvas/service-metrics.yml`.

### Producer-Side (delivery capacity & quality)

**Client Throughput**: How many clients/engagements per period?

**Delivery Lead Time**: Engagement start to delivery -- how long?
- Identify bottleneck: client feedback, research, production?

**Client Satisfaction**: NPS, CSAT, retention rate, referral rate?

**Repeatability**: Is the delivery workflow documented and templated? Score 1-5.

### Customer-Side (acquisition & revenue)

**Time to First Value (TTFV)**: How quickly does a client receive meaningful value after engaging?
- First deliverable or quick win within days: excellent
- Weeks before any tangible output: investigate onboarding process

**Acquisition**: Conversion rate, cost per acquisition, proposal win rate?

**Revenue Health**: Refund/dispute rate, CLV, churn (retainers), NRR?

### Canvas Output
Update `.claude/canvas/service-metrics.yml` with current measurements and `last_measured` timestamp.

---

## Theory Citations
- Forsgren, Humble, Kim: Accelerate (DORA metrics -- 5 metrics including Reliability and FDRT naming from 2024 report)
- LinearB: APEX Framework (AI-era delivery measurement)
- Beyer, Jones, Petoff, Murphy: Site Reliability Engineering (error budgets, SLIs/SLOs)
- Smart: BVSSH (holistic flow optimization — APEX X maps to Happier)
- Kim: Three Ways (Second Way — amplify feedback loops, detect shifting bottlenecks)
