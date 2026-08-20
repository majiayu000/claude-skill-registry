---
name: prd-v08-marketing-ops-handoff
description: >
  Define lifecycle stages and marketing → sales / CSM handoff rules for leads captured by GTM
  channels during PRD v0.8 Deployment & Ops. Triggers on requests to set up lead lifecycle,
  define MQL/SQL criteria, build handoff process, or when user asks "what's an MQL?",
  "marketing to sales handoff", "lead lifecycle", "lead routing", "RevOps", "MOPS", "marketing
  operations". Outputs BR-MOPS-* lifecycle rules and GTM-MOPS-* handoff flow entries.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep

execution_modes:
  default: standard
  supports: [quick, standard, deep]
---

# Marketing-Ops Handoff (Lead Lifecycle + Sales Routing)

Position in workflow: v0.8 Monitoring Setup → **v0.8 Marketing-Ops Handoff** → v0.9 Launch Channels (ORB), v0.9 Cold Outreach

## Execution Mode

Default is **standard**. See [`.claude/rules/08-skill-execution-modes.md`](../../rules/08-skill-execution-modes.md) for selection logic.

| Mode | What this skill produces |
|------|--------------------------|
| **quick** | 3-stage lifecycle (Anonymous → Lead → Customer); single handoff rule; SLA per stage |
| **standard** | Full 5-stage lifecycle (Anonymous → MQL → SQL → Opportunity → Customer); entry/exit criteria; handoff payload spec; SLAs |
| **deep** | Full lifecycle + per-segment routing (by ICP / region / size); scoring model; rejection-loop rules; SLA monitoring + escalation |

## What This Does

Defines the **lifecycle stages** a lead passes through from first touch to customer (or churn), plus the **handoff rules** at each transition. Without this, marketing-captured leads get dropped, double-worked, or never followed up. With this, you have an auditable definition of who owns what at each moment.

This skill applies primarily to B2B and prosumer products with a human-touch sales motion (founder-led sales, BDR/SDR teams, customer-success-led expansion). Pure self-serve products use a simpler version: lifecycle = Anonymous → Trial → Paid, with no human handoff.

## How It Works

1. **Pick the lifecycle shape** — Match the product:
   - **Self-serve**: Anonymous → Signup → Activated → Paid → Expanded
   - **Sales-assisted**: Anonymous → MQL → SQL → Opportunity → Customer
   - **Hybrid (PLG + Sales)**: Anonymous → Signup → Activated → Paid → SQL → Opportunity → Expansion
2. **Define entry criteria per stage** — What event/behavior moves a lead into this stage? Examples:
   - MQL: filled out a high-intent form, downloaded gated content, hit usage threshold
   - SQL: explicit "talk to sales" or scoring threshold reached
   - Opportunity: discovery call held, budget + authority confirmed
3. **Define exit criteria per stage** — Two paths out: progress (to next stage) and disqualify (back to nurture or out). Disqualification rules matter as much as progression.
4. **Map ownership** — Who owns the lead at each stage:
   - Anonymous: marketing automation
   - MQL: BDR/SDR
   - SQL: AE / founder
   - Opportunity: AE / founder
   - Customer: CS / founder
5. **Define handoff payload** — When a lead moves between owners, what context goes with them? At minimum:
   - Source (which GTM-* channel produced this lead)
   - Touchpoint history (what they've engaged with)
   - Best-fit signals (firmographic match, behavioral fit)
   - Disqualifiers (anything that ruled out an earlier stage)
   - Open questions (what the next owner should clarify)
6. **Set SLAs per stage** — How fast must the new owner respond after handoff? MQL → BDR typically <1 business hour for high-signal, <1 business day for low-signal. SQL → AE typically <30 minutes.
7. **Plan rejection routing** — When SQL → AE handoff is rejected ("not a fit"), where does the lead go? Back to nurture, disqualified, requeued? Without this rule, leads die in limbo.

## Example

B2B SaaS, $200/month entry price, sales-assisted motion.

| Stage | Entry criteria | Exit criteria | Owner | SLA |
|-------|----------------|---------------|-------|-----|
| Anonymous | Any first touch | Filled form OR signed up | Marketing | n/a |
| MQL | Filled high-intent form (demo request, pricing page) | BDR qualifies in OR disqualifies | BDR | 1 business hour |
| SQL | BDR confirms fit + intent | AE accepts OR rejects | BDR → AE | 30 min |
| Opportunity | AE held discovery, budget + authority confirmed | Closed-won OR closed-lost | AE | 24 hr per touch |
| Customer | Closed-won contract signed | Churn OR expand | CS | Onboarding kickoff <1 business day |

Handoff payload at MQL → SQL (BDR → AE):
- Source: GTM-002 (Product Hunt) + retargeting
- Touchpoints: 3 blog posts, demo video, pricing page (3×)
- Best-fit signals: 50-person SaaS (matches PER-001), VP Eng signed up
- Disqualifiers: none
- Open questions: confirm budget owner; confirm timeline

Rejection routing at SQL → AE rejection ("too small"): lead returns to MQL queue with "small-team" tag; BDR can re-engage in 90 days if size signal changes.

## What You Get Back

- **BR-MOPS-\* lifecycle rule entries** — One per stage with entry/exit/owner/SLA
- **GTM-MOPS-\* handoff flow entries** — One per transition (MQL→SQL, SQL→OPP, etc.) with payload spec
- **Rejection-routing rules** — Disqualifier-aware routing back to nurture
- **SLA monitoring plan** — Hooks into MON-DRIFT-* for SLA drift watching

## When to Use It

| Trigger | Mode |
|---------|------|
| B2B / sales-assisted product, pre-launch | standard |
| Hybrid PLG + Sales motion | deep |
| Pure self-serve consumer product | **skip** — overkill |
| Adding human sales to existing self-serve | standard |
| Sales velocity issues (leads dying in queue) | deep (rebuild with SLAs) |
| Pre-Series A audit (investor wants to see process) | deep |

## Consumes

- **PER-\* best-fit characteristics** (sharpened by v0.9 Positioning when available) — Defines what fit-signal scoring looks like
- **GTM-\* channel mix** (from v0.9 Launch Channels ORB, when available) — Lead sources feed into Anonymous stage
- **GTM-\* offer card** (from v0.9 Offer Construction) — Determines what "qualified" means (price tier sets bar)
- **BR-PRICING-\*** (from v0.3 + v0.9) — Sets stage thresholds (above $X/year → SQL; below → self-serve)
- **KPI-\* baseline targets** — Stage conversion targets feed into KPI- entries

> When this skill runs before v0.9, channel and offer references use placeholders that get reconciled when v0.9 finalizes.

## Produces

- **BR-MOPS-\* entries** (lifecycle stage rules) in `SoT/SoT.BUSINESS_RULES.md`
- **GTM-MOPS-\* entries** (handoff flow specs) — One per stage transition
- **CFD-\* gaps surfaced** — When stage criteria can't be cleanly defined, log as research gap

## Output Template

```
BR-MOPS-XXX: Lifecycle Stage — [Stage name]
Type: Lifecycle-Stage
Order: [#]
Status: Active

Stage: [Anonymous | Signup | Activated | MQL | SQL | Opportunity | Customer | Expansion]

Entry criteria:
  - [Criterion 1 — e.g., "Filled out demo request form"]
  - [Criterion 2 — e.g., "Reached usage threshold X"]

Exit criteria (progression):
  - To [next stage]: [Criterion]

Exit criteria (disqualification):
  - [Criterion that routes back to earlier stage or out]

Owner: [Marketing automation | BDR/SDR | AE | CS | Founder]

SLA:
  Response time after entering this stage: [duration]
  Escalation: [What happens if SLA missed]

Linked IDs: PER-XXX (fit signals), GTM-YYY (source channels), BR-PRICING-ZZZ (tier threshold), KPI-AAA (conversion rate)
```

```
GTM-MOPS-XXX: Handoff — [Stage A] → [Stage B]
Type: Handoff
Status: Active

From: [Stage A] (owner: ...)
To: [Stage B] (owner: ...)

Trigger: [Specific event — e.g., "BDR marks lead as Qualified in CRM"]

Payload (what context transfers):
  - Source: [GTM-* channel]
  - Touchpoint history: [What they engaged with]
  - Best-fit signals: [Firmographic + behavioral match]
  - Disqualifiers: [Anything that ruled out earlier stages]
  - Open questions: [What new owner should clarify]

Rejection rule:
  Condition: [When does the new owner reject this handoff?]
  Routing: [Where does the rejected lead go? Nurture / disqualified / requeue]
  Re-engagement: [Conditions under which this lead can return]

SLA: [Response time required from new owner]

Linked IDs: BR-MOPS-AAA (Stage A rule), BR-MOPS-BBB (Stage B rule)
```

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| **MQL = "anyone who filled a form"** | High-volume MQLs with 1% SQL conversion | Tighten MQL entry criteria; add fit-signal scoring |
| **No rejection routing** | Leads die when SQL → AE rejects | Define where rejected leads go (nurture, disqualified, requeue) |
| **SLA without escalation** | "Respond in 1 hour" with no consequence if missed | SLA must have an escalation path |
| **Handoff without payload** | New owner asks "who is this?" | Mandatory payload fields at every handoff |
| **Stages without owners** | "We'll figure out who handles SQLs later" | One owner per stage; named role minimum |
| **Lifecycle for self-serve** | $20/month consumer product with MQL/SQL/OPP | Use Signup → Activated → Paid; no human handoff |
| **No SLA monitoring** | SLAs exist on paper, missed in practice | Drift-monitor SLA via MON-DRIFT- |

## Quality Gates

Before activating handoff:

- [ ] Lifecycle shape matches product motion (self-serve / sales-assisted / hybrid)
- [ ] Every stage has entry, exit-progression, and exit-disqualification criteria
- [ ] Every stage has a named owner (role minimum)
- [ ] Every stage has an SLA with escalation path
- [ ] Every transition has a handoff payload spec
- [ ] Rejection routing defined for every owner-changing handoff
- [ ] SLA drift monitoring set up via MON-DRIFT-

## Downstream Connections

| Consumer | What it uses | Example |
|----------|--------------|---------|
| **Launch Channels (ORB)** | Each channel's leads enter the lifecycle at Anonymous | GTM-002 (Product Hunt) → Anonymous → MQL routing |
| **Cold Outreach (Tiered)** | Tier 1/2/3 sequences map to lifecycle stages | Tier 1 = SQL-tier ABM; Tier 3 = MQL nurture |
| **Launch Metrics** | Stage conversion rates become KPI- entries | KPI-MQL-to-SQL-conversion |
| **Feedback Loop Setup** | Rejected leads' "why we passed" reasons feed CFD- | Pattern: "too small" rejections → CFD- pricing signal |
| **Drift Monitoring** | SLA drift catches process decay | MON-DRIFT-MQL-response-SLA |

## Detailed References

- alirezarezvani's `marketing-ops` and `revenue-operations` skills (claude-skills)
- *Predictable Revenue* (Aaron Ross) — sales handoff structure
- *From Impossible to Inevitable* (Aaron Ross + Jason Lemkin) — stage discipline
- SiriusDecisions lead-lifecycle framework (the canonical B2B reference)
- (No bundled `references/` — lifecycle shapes vary; this skill encodes the discipline, not a specific shape)
