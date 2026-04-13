---
name: dora-check
description: "Assess delivery health metrics. For software: DORA + APEX. For content/AI/service products: product-type-appropriate metrics."
---

# Delivery Metrics Check

Assess delivery health using product-type-appropriate metrics. Check `product_type` from `diamonds/active.yml` to determine which assessment to run.

**Product type routing** (v0.11.0):
- **software**: Full DORA + APEX assessment (Parts 1-3 below)
- **content_course, content_publication, content_media**: Content Delivery Assessment (Part 4 below)
- **ai_tool**: AI Tool Assessment (Part 5 below) + DORA/APEX if code components exist
- **service_offering**: Service Delivery Assessment (Part 6 below)

---

## Software Products

Assess delivery health using Forsgren's four DORA metrics AND LinearB's APEX AI-era metrics.

## Part 1: DORA Metrics (Forsgren)

Gather current metrics from CI/CD, deployment logs, incident records:

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

**Mean Time to Recovery**: Time to restore service after failure?
- Elite: Less than one hour
- High: Less than one day
- Medium: Between one day and one week
- Low: More than one week

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

### E — Efficiency (The Shifting Bottleneck)
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
| MTTR | ... | ... | ... | ... |

### APEX Metrics (AI-Era)
| Pillar | Status | Key Signal |
|--------|--------|-----------|
| AI Leverage | ... | AI acceptance rate: ...% |
| Predictability | ... | Planning accuracy: ...%, Rework rate: ...% |
| Efficiency | ... | Cycle time: ..., Review wait: ... |
| Developer Experience | ... | Satisfaction: ..., Burnout: ... |

### Shifting Bottleneck Check
[Is coding faster but review/deployment slower? Yes/No]
[If yes: where is the new bottleneck?]

### DORA Bottleneck
[The metric most constraining overall performance]

### Value Stream Diagnosis (if bottleneck detected)
If DORA shows a bottleneck, map the value stream to identify WHERE in the flow the constraint lives:
- Run `/canvas-update` to update `canvas/value-stream.yml` with current stage timings
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

If SLIs/SLOs defined in `canvas/dora-metrics.yml` sre section:
- Review each service's SLI values against SLO targets
- Calculate error budget remaining: (SLO - actual) / (1 - SLO) * 100%
- **Healthy** (>50%): Ship features. Budget available.
- **Warning** (<25%): Slow down. Increase testing.
- **Depleted** (0%): Feature freeze. Reliability takes priority.

Error budgets are the social contract: reliability earns the right to ship faster. Connects to BVSSH Safer.

If NOT defined: "Consider defining SLIs/SLOs to balance velocity with reliability."

## Decision Log (MANDATORY)
**Always APPEND** a `### DORA Assessment` or `### Delivery Metrics Assessment` entry to `harness/decision-log.md` with:
- Each metric assessed, current baseline, target, and classification level
- The identified bottleneck and recommended improvements
- Any shifting bottleneck signals (AI-era: coding faster but review slower)
This ensures the delivery metrics gate has auditable evidence.

## Canvas Output
**Always update** `canvas/dora-metrics.yml` with:
- DORA metrics, classifications, and capability scores
- APEX section: ai_leverage, predictability, efficiency, developer_experience
- SRE section: SLI/SLO status, error budget remaining
- Measurement history for trend tracking

---

## Part 4: Content Delivery Assessment (v0.11.0)

For content_course, content_publication, content_media products. Read `canvas/content-metrics.yml`.

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
Update `canvas/content-metrics.yml` with current measurements and `last_measured` timestamp.

---

## Part 5: AI Tool Assessment (v0.11.0)

For ai_tool products. Read `canvas/ai-tool-metrics.yml`.

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
Update `canvas/ai-tool-metrics.yml` with current measurements and `last_measured` timestamp.

---

## Part 6: Service Delivery Assessment (v0.11.0)

For service_offering products. Read `canvas/service-metrics.yml`.

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
Update `canvas/service-metrics.yml` with current measurements and `last_measured` timestamp.

---

## Theory Citations
- Forsgren, Humble, Kim: Accelerate (DORA metrics)
- LinearB: APEX Framework (AI-era delivery measurement)
- Beyer, Jones, Petoff, Murphy: Site Reliability Engineering (error budgets, SLIs/SLOs)
- Smart: BVSSH (holistic flow optimization — APEX X maps to Happier)
- Kim: Three Ways (Second Way — amplify feedback loops, detect shifting bottlenecks)
