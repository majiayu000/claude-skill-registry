---
name: lead-scoring
description: Score and prioritize leads based on firmographic fit and behavioral engagement signals, producing ranked tiers for sales team focus. Use when the user requests lead scoring or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: community
  version: "1.0"
---

# Lead Scoring

Score and prioritize inbound and outbound leads by combining firmographic fit (how closely a lead matches your ideal customer profile) with behavioral engagement signals (actions that indicate purchase intent). This skill builds scoring rubrics, assigns weighted points, calculates composite scores, and segments leads into actionable tiers — Hot, Warm, and Cold — so sales teams focus time on the highest-converting opportunities.

## Workflow

1. **Define ICP Criteria** — Establish the firmographic attributes of your ideal customer: target industries, company size ranges, revenue bands, geographic regions, and technology stack indicators. Each attribute gets a weight reflecting its predictive importance based on historical conversion data.

2. **Assign Fit Scores** — Score each lead's company against ICP criteria. A perfect-fit lead earns maximum fit points; partial matches earn proportional scores. Negative scoring applies for explicit disqualifiers (e.g., company size below minimum threshold, industries you don't serve, students or competitors).

3. **Track Engagement Signals** — Capture behavioral signals from marketing automation, CRM, and product analytics: email opens/clicks, website page visits (especially pricing and case study pages), content downloads, webinar attendance, demo requests, free trial signups, and reply sentiment. Weight each signal by its correlation to closed-won deals.

4. **Calculate Composite Score** — Combine fit score (typically 0–50 points) and engagement score (typically 0–50 points) into a composite score (0–100). Apply decay to engagement signals older than 30 days to ensure the score reflects current intent, not stale activity.

5. **Rank and Segment into Tiers** — Sort leads by composite score and assign tiers: Hot (75–100), Warm (40–74), Cold (0–39). Route Hot leads to SDRs for immediate outreach, Warm leads to nurture sequences, and Cold leads to low-touch automated campaigns. Review tier thresholds quarterly against actual conversion rates and adjust.

## Usage

Provide your ICP definition, the engagement signals you track, and a list of leads with their attributes. The skill outputs a scoring rubric and scored/ranked lead list.

**Example prompt:**
> Build a lead scoring model for our B2B analytics platform. ICP: Series A+ SaaS companies, 50–500 employees, US/Canada, using Snowflake or BigQuery. Score these 5 leads and assign Hot/Warm/Cold tiers.

## Examples

### Example 1: Building a Lead Scoring Rubric

**Input:** B2B analytics platform targeting mid-market SaaS companies.

**Fit Scoring Rubric (0–50 points):**

| Criterion | Weight | Scoring Rules |
|---|---|---|
| Company size | 15 pts | 200–500 emp: 15 · 50–199 emp: 10 · 501–1000 emp: 5 · <50 or >1000: 0 |
| Industry | 10 pts | SaaS/Software: 10 · Fintech/E-commerce: 7 · Other tech: 4 · Non-tech: 0 |
| Funding stage | 10 pts | Series A–C: 10 · Seed: 5 · Public/Pre-seed: 2 |
| Geography | 5 pts | US/Canada: 5 · UK/EU: 3 · Other: 1 |
| Tech stack | 10 pts | Snowflake or BigQuery: 10 · Redshift: 6 · No cloud DW: 0 |

**Engagement Scoring Rubric (0–50 points):**

| Signal | Points | Decay |
|---|---|---|
| Demo requested | 20 pts | None (one-time event) |
| Pricing page visit | 8 pts | Halved after 14 days |
| Case study download | 6 pts | Halved after 21 days |
| Email link clicked | 3 pts (per click, max 12) | Halved after 14 days |
| Webinar attended | 7 pts | Halved after 30 days |
| Blog visit | 1 pt (per visit, max 5) | Expires after 30 days |

**Tier Thresholds:**

| Tier | Score Range | Action |
|---|---|---|
| Hot | 75–100 | Immediate SDR outreach within 4 hours |
| Warm | 40–74 | Enroll in high-touch nurture sequence |
| Cold | 0–39 | Low-touch automated drip campaign |

---

### Example 2: Scoring a Batch of Leads

**Input:** 5 leads with attributes and recent activity.

**Scored Output:**

| Lead | Company | Employees | Industry | Funding | Tech Stack | Fit Score | Key Engagement | Eng. Score | **Total** | **Tier** |
|---|---|---|---|---|---|---|---|---|---|---|
| Rachel M. | StreamOps | 320 | SaaS | Series B | Snowflake | 50 | Demo request + pricing visit + 2 email clicks | 34 | **84** | 🔥 Hot |
| David K. | PayFlow | 180 | Fintech | Series A | BigQuery | 37 | Webinar + case study download + 3 email clicks | 22 | **59** | 🟡 Warm |
| Priya S. | HealthBridge | 90 | Healthcare | Series B | Redshift | 21 | Pricing page visit + 1 email click | 11 | **32** | 🔵 Cold |
| Marcus T. | DevLayer | 450 | SaaS | Series C | Snowflake | 50 | 4 blog visits + 1 email click | 8 | **58** | 🟡 Warm |
| Lisa C. | TinyML Labs | 30 | AI/ML | Seed | BigQuery | 20 | Demo request + webinar | 27 | **47** | 🟡 Warm |

**Summary:** 1 Hot lead (route to SDR), 3 Warm leads (nurture sequence), 1 Cold lead (automated drip). Marcus T. has a perfect fit score but low engagement — prioritize getting him to a demo.

## Best Practices

- Weight your scoring model on historical closed-won data, not intuition — run a correlation analysis between lead attributes and conversion to calibrate point values.
- Apply score decay to engagement signals so that a lead who was active 6 months ago doesn't rank above a lead showing intent today.
- Include negative scoring for explicit disqualifiers (competitors, students, non-target geographies) to keep noise out of the Hot tier.
- Review and recalibrate tier thresholds quarterly; as your ICP evolves and marketing channels shift, static thresholds drift from reality.
- Separate fit and engagement scores in your reporting so reps can distinguish "great company, not engaged yet" from "engaged lead at a poor-fit company."
- Set a minimum fit score threshold (e.g., 15 points) below which no amount of engagement can push a lead to Hot — this prevents poor-fit leads from wasting SDR time.

## Edge Cases

- **High engagement, zero fit** — A lead who downloads every resource but works at a 5-person agency outside your ICP. Cap their maximum tier at Warm regardless of engagement score to avoid wasting sales cycles.
- **Perfect fit, no engagement** — A lead matching ICP criteria exactly but showing no behavioral signals. Flag for outbound prospecting rather than inbound follow-up; they may not know you exist yet.
- **Duplicate leads from the same company** — When multiple contacts at one company score independently, consolidate into an account-level score to avoid double-counting the same buying intent.
- **Engagement signal spam** — A lead who opens every email and visits every page may be a researcher, bot, or competitor. Set engagement score caps per signal type and flag anomalous activity patterns for manual review.
- **Scoring model cold-start** — For new products or markets without historical conversion data, start with a simple unweighted model, collect 90 days of pipeline data, then recalibrate weights based on actual outcomes.
